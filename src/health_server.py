"""
Health Check Server for Dockray
Provides HTTP endpoints for container health monitoring
"""

import asyncio
import logging
from typing import Dict, Any

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import uvicorn

logger = logging.getLogger(__name__)

class HealthServer:
    """Simple health check HTTP server"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.app = FastAPI(title="Dockray Health", version="0.1.0")
        self.server = None
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup health check endpoints"""
        
        @self.app.get("/health")
        async def health_check():
            """Basic health check endpoint"""
            return JSONResponse({
                "status": "healthy",
                "service": "dockray-ebpf-monitor",
                "version": "0.1.0"
            })
        
        @self.app.get("/status")
        async def status_check():
            """Detailed status information"""
            return JSONResponse({
                "status": "operational",
                "components": {
                    "ebpf_monitor": "running",
                    "container_mapper": "running",
                    "health_server": "running"
                },
                "capabilities": {
                    "ebpf_tracing": self._check_ebpf_access(),
                    "docker_socket": self._check_docker_access()
                }
            })
    
    def _check_ebpf_access(self) -> bool:
        """Check if eBPF tracing is accessible"""
        try:
            with open("/sys/kernel/debug/tracing/trace", "r") as f:
                return True
        except (FileNotFoundError, PermissionError):
            return False
    
    def _check_docker_access(self) -> bool:
        """Check if Docker socket is accessible"""
        import os
        return os.path.exists("/var/run/docker.sock")
    
    async def start(self):
        """Start the health server"""
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=self.port,
            log_level="info",
            access_log=False
        )
        self.server = uvicorn.Server(config)
        
        # Start server in background task
        self._server_task = asyncio.create_task(self.server.serve())
        logger.info(f"Health server started on port {self.port}")
    
    async def stop(self):
        """Stop the health server"""
        if self.server:
            self.server.should_exit = True
            await self._server_task
            logger.info("Health server stopped") 