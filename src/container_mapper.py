"""
Container Mapper for Dockray
Maps process IDs to container IDs using /proc/$PID/cgroup and Docker API
"""

import asyncio
import logging
import re
from typing import Dict, Optional, Set
from pathlib import Path

import docker
import psutil

logger = logging.getLogger(__name__)

class ContainerMapper:
    """Maps PIDs to container IDs and maintains container metadata"""
    
    def __init__(self):
        self.docker_client = None
        self.pid_to_container: Dict[int, str] = {}
        self.container_info: Dict[str, Dict] = {}
        self.running = False
        self._update_task = None
    
    async def start(self):
        """Initialize the container mapper"""
        logger.info("🗺️  Starting container mapper...")
        
        try:
            # Initialize Docker client
            self.docker_client = docker.from_env()
            
            # Initial container discovery
            await self._discover_containers()
            
            # Start background update task
            self.running = True
            self._update_task = asyncio.create_task(self._update_loop())
            
            logger.info("🗺️  Container mapper started")
            
        except Exception as e:
            logger.error(f"Failed to start container mapper: {e}")
            raise
    
    async def stop(self):
        """Stop the container mapper"""
        logger.info("🗺️  Stopping container mapper...")
        self.running = False
        
        if self._update_task:
            self._update_task.cancel()
            try:
                await self._update_task
            except asyncio.CancelledError:
                pass
        
        if self.docker_client:
            self.docker_client.close()
            
        logger.info("🗺️  Container mapper stopped")
    
    async def _update_loop(self):
        """Background task to update container mappings"""
        while self.running:
            try:
                await self._discover_containers()
                await asyncio.sleep(5)  # Update every 5 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in container mapper update loop: {e}")
                await asyncio.sleep(10)  # Wait longer on error
    
    async def _discover_containers(self):
        """Discover running containers and their PIDs"""
        if not self.docker_client:
            return
            
        try:
            # Get all running containers
            containers = self.docker_client.containers.list()
            
            # Clear old mappings
            self.pid_to_container.clear()
            self.container_info.clear()
            
            for container in containers:
                container_id = container.id[:12]  # Short ID
                
                # Store container metadata
                self.container_info[container_id] = {
                    'name': container.name,
                    'image': container.image.tags[0] if container.image.tags else 'unknown',
                    'status': container.status,
                    'networks': list(container.attrs.get('NetworkSettings', {}).get('Networks', {}).keys()),
                    'created': container.attrs.get('Created', ''),
                    'ports': self._extract_ports(container)
                }
                
                # Map container PIDs
                await self._map_container_pids(container, container_id)
                
            logger.debug(f"Mapped {len(self.pid_to_container)} PIDs to {len(self.container_info)} containers")
            
        except Exception as e:
            logger.error(f"Error discovering containers: {e}")
    
    async def _map_container_pids(self, container, container_id: str):
        """Map all PIDs in a container to its ID"""
        try:
            # Get container's main PID
            top_result = container.top()
            if top_result and 'Processes' in top_result:
                for process in top_result['Processes']:
                    if len(process) > 1:  # Ensure we have PID column
                        try:
                            pid = int(process[1])  # PID is usually second column
                            self.pid_to_container[pid] = container_id
                        except (ValueError, IndexError):
                            continue
            
            # Also check /proc/*/cgroup for additional PIDs
            await self._map_cgroup_pids(container_id)
            
        except Exception as e:
            logger.debug(f"Error mapping PIDs for container {container_id}: {e}")
    
    async def _map_cgroup_pids(self, container_id: str):
        """Map PIDs using cgroup information"""
        cgroup_pattern = re.compile(rf'.*/{container_id}.*')
        
        try:
            # Check all running processes
            for proc in psutil.process_iter(['pid']):
                try:
                    pid = proc.info['pid']
                    cgroup_path = Path(f"/proc/{pid}/cgroup")
                    
                    if cgroup_path.exists():
                        with open(cgroup_path, 'r') as f:
                            content = f.read()
                            if cgroup_pattern.search(content):
                                self.pid_to_container[pid] = container_id
                                
                except (psutil.NoSuchProcess, FileNotFoundError, PermissionError):
                    continue
                    
        except Exception as e:
            logger.debug(f"Error mapping cgroup PIDs: {e}")
    
    def _extract_ports(self, container) -> Dict[str, str]:
        """Extract port mappings from container"""
        ports = {}
        port_mappings = container.attrs.get('NetworkSettings', {}).get('Ports', {})
        
        for internal_port, external_configs in port_mappings.items():
            if external_configs:
                for config in external_configs:
                    host_port = config.get('HostPort', '')
                    if host_port:
                        ports[internal_port] = f"{config.get('HostIp', '0.0.0.0')}:{host_port}"
        
        return ports
    
    def get_container_by_pid(self, pid: int) -> Optional[str]:
        """Get container ID for a given PID"""
        return self.pid_to_container.get(pid)
    
    def get_container_info(self, container_id: str) -> Optional[Dict]:
        """Get container metadata"""
        return self.container_info.get(container_id)
    
    def get_all_containers(self) -> Dict[str, Dict]:
        """Get all container information"""
        return self.container_info.copy()
    
    def get_container_count(self) -> int:
        """Get number of tracked containers"""
        return len(self.container_info) 