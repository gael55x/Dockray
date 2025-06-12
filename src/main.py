#!/usr/bin/env python3
"""
Dockray eBPF Monitor - Main Entry Point
Real-time network monitoring for Docker Compose stacks
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

from .monitor import EBPFMonitor
from .container_mapper import ContainerMapper
from .health_server import HealthServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class DockrayService:
    """Main Dockray service orchestrator"""
    
    def __init__(self):
        self.monitor = None
        self.container_mapper = None
        self.health_server = None
        self.running = False
        
    async def start(self):
        """Initialize and start all service components"""
        logger.info("Dockray starting up...")
        
        try:
            # Initialize container mapping service
            self.container_mapper = ContainerMapper()
            await self.container_mapper.start()
            
            # Initialize eBPF monitor
            self.monitor = EBPFMonitor(self.container_mapper)
            await self.monitor.start()
            
            # Start health check server
            self.health_server = HealthServer()
            await self.health_server.start()
            
            self.running = True
            logger.info("Dockray fully operational")
            
            # Keep service running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Failed to start Dockray: {e}")
            await self.stop()
            sys.exit(1)
    
    async def stop(self):
        """Gracefully shutdown all components"""
        logger.info("Dockray shutting down...")
        self.running = False
        
        if self.monitor:
            await self.monitor.stop()
        if self.container_mapper:
            await self.container_mapper.stop()
        if self.health_server:
            await self.health_server.stop()
            
        logger.info("Dockray stopped")

async def main():
    """Main async entry point"""
    service = DockrayService()
    
    # Handle graceful shutdown
    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(service.stop())
    
    # Register signal handlers
    loop = asyncio.get_event_loop()
    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, signal_handler)
    
    # Start the service
    await service.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1) 