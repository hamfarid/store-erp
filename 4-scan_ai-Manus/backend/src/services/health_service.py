"""
Health Check Service
=====================

Purpose: Comprehensive health monitoring for all system components.
Provides detailed status for deployment readiness and monitoring.

Features:
- Database connectivity check
- Redis connectivity check
- ML Service availability
- Image Crawler status
- Disk space monitoring
- Memory usage monitoring
- Response time tracking

Usage:
    from src.services.health_service import HealthService
    
    health = HealthService()
    status = await health.get_full_status()
    
    if status["status"] == "healthy":
        print("All systems operational")

Author: Global System v35.0
Date: 2026-01-17
"""

import asyncio
import logging
import os
import platform
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..core.config import get_settings

logger = logging.getLogger(__name__)


class ComponentStatus:
    """
    Status of a single component.
    
    Attributes:
        name: Component name
        status: 'healthy', 'degraded', 'unhealthy'
        latency_ms: Response time in milliseconds
        message: Status message
        details: Additional details
    """
    
    def __init__(
        self,
        name: str,
        status: str = "unknown",
        latency_ms: Optional[float] = None,
        message: Optional[str] = None,
        details: Optional[Dict] = None
    ):
        self.name = name
        self.status = status
        self.latency_ms = latency_ms
        self.message = message
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "latency_ms": self.latency_ms,
            "message": self.message,
            "details": self.details if self.details else None
        }


class HealthService:
    """
    Comprehensive health monitoring service.
    
    Checks all system components and reports overall health status.
    Used by Kubernetes probes, load balancers, and monitoring systems.
    
    Example:
        >>> health = HealthService(db_session)
        >>> status = await health.get_full_status()
        >>> print(status["status"])  # 'healthy', 'degraded', or 'unhealthy'
    """
    
    def __init__(self, db: Optional[Session] = None):
        """
        Initialize health service.
        
        Args:
            db: Database session for DB health checks
        """
        self.db = db
        self.settings = get_settings()
        self._start_time = datetime.utcnow()
    
    async def get_full_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status of all components.
        
        Returns:
            Dict with overall status and component details
        """
        components = []
        
        # Run all checks concurrently
        checks = await asyncio.gather(
            self._check_database(),
            self._check_redis(),
            self._check_ml_service(),
            self._check_crawler_service(),
            return_exceptions=True
        )
        
        for check in checks:
            if isinstance(check, Exception):
                logger.error(f"Health check failed: {check}")
                components.append(ComponentStatus(
                    name="unknown",
                    status="unhealthy",
                    message=str(check)
                ))
            else:
                components.append(check)
        
        # Add system metrics
        system_status = self._check_system()
        components.append(system_status)
        
        # Determine overall status
        overall_status = self._calculate_overall_status(components)
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "uptime_seconds": (datetime.utcnow() - self._start_time).total_seconds(),
            "version": self.settings.APP_VERSION if hasattr(self.settings, 'APP_VERSION') else "4.3.1",
            "environment": self.settings.ENVIRONMENT if hasattr(self.settings, 'ENVIRONMENT') else "production",
            "components": [c.to_dict() for c in components]
        }
    
    async def get_liveness(self) -> Dict[str, Any]:
        """
        Simple liveness check (Kubernetes liveness probe).
        
        Returns True if the application is running.
        Used to detect if the app needs to be restarted.
        """
        return {
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
    
    async def get_readiness(self) -> Dict[str, Any]:
        """
        Readiness check (Kubernetes readiness probe).
        
        Returns True if the application can accept traffic.
        Checks critical dependencies (DB, Redis).
        """
        db_status = await self._check_database()
        redis_status = await self._check_redis()
        
        is_ready = (
            db_status.status in ["healthy", "degraded"] and
            redis_status.status in ["healthy", "degraded"]
        )
        
        return {
            "status": "ready" if is_ready else "not_ready",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "checks": {
                "database": db_status.status,
                "redis": redis_status.status
            }
        }
    
    async def _check_database(self) -> ComponentStatus:
        """Check PostgreSQL database connectivity."""
        start_time = time.time()
        
        try:
            if self.db is None:
                return ComponentStatus(
                    name="database",
                    status="unknown",
                    message="No database session provided"
                )
            
            # Execute simple query
            result = self.db.execute(text("SELECT 1"))
            result.fetchone()
            
            latency = (time.time() - start_time) * 1000
            
            # Check if latency is acceptable
            if latency > 1000:  # > 1 second
                return ComponentStatus(
                    name="database",
                    status="degraded",
                    latency_ms=round(latency, 2),
                    message="High latency detected"
                )
            
            return ComponentStatus(
                name="database",
                status="healthy",
                latency_ms=round(latency, 2),
                message="PostgreSQL connected"
            )
            
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            logger.error(f"Database health check failed: {e}")
            return ComponentStatus(
                name="database",
                status="unhealthy",
                latency_ms=round(latency, 2),
                message=f"Connection failed: {str(e)[:100]}"
            )
    
    async def _check_redis(self) -> ComponentStatus:
        """Check Redis connectivity."""
        start_time = time.time()
        
        try:
            import redis
            
            redis_host = getattr(self.settings, 'REDIS_HOST', 'localhost')
            redis_port = getattr(self.settings, 'REDIS_PORT', 6379)
            redis_password = getattr(self.settings, 'REDIS_PASSWORD', None)
            
            client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                socket_timeout=5
            )
            
            # Ping Redis
            client.ping()
            
            # Get info
            info = client.info(section='memory')
            used_memory = info.get('used_memory_human', 'unknown')
            
            latency = (time.time() - start_time) * 1000
            
            return ComponentStatus(
                name="redis",
                status="healthy",
                latency_ms=round(latency, 2),
                message="Redis connected",
                details={"memory_used": used_memory}
            )
            
        except ImportError:
            return ComponentStatus(
                name="redis",
                status="unknown",
                message="Redis client not installed"
            )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            logger.warning(f"Redis health check failed: {e}")
            return ComponentStatus(
                name="redis",
                status="unhealthy",
                latency_ms=round(latency, 2),
                message=f"Connection failed: {str(e)[:100]}"
            )
    
    async def _check_ml_service(self) -> ComponentStatus:
        """Check ML Service availability."""
        start_time = time.time()
        
        try:
            ml_url = getattr(self.settings, 'ML_SERVICE_URL', 'http://ml_service:8000')
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{ml_url}/health")
                
                latency = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    return ComponentStatus(
                        name="ml_service",
                        status="healthy",
                        latency_ms=round(latency, 2),
                        message="ML Service operational",
                        details=data
                    )
                else:
                    return ComponentStatus(
                        name="ml_service",
                        status="degraded",
                        latency_ms=round(latency, 2),
                        message=f"HTTP {response.status_code}"
                    )
                    
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            logger.warning(f"ML Service health check failed: {e}")
            return ComponentStatus(
                name="ml_service",
                status="unhealthy",
                latency_ms=round(latency, 2),
                message=f"Unavailable: {str(e)[:100]}"
            )
    
    async def _check_crawler_service(self) -> ComponentStatus:
        """Check Image Crawler Service availability."""
        start_time = time.time()
        
        try:
            crawler_url = getattr(self.settings, 'CRAWLER_SERVICE_URL', 'http://image_crawler:8001')
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{crawler_url}/health")
                
                latency = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    return ComponentStatus(
                        name="image_crawler",
                        status="healthy",
                        latency_ms=round(latency, 2),
                        message="Crawler operational"
                    )
                else:
                    return ComponentStatus(
                        name="image_crawler",
                        status="degraded",
                        latency_ms=round(latency, 2),
                        message=f"HTTP {response.status_code}"
                    )
                    
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return ComponentStatus(
                name="image_crawler",
                status="unhealthy",
                latency_ms=round(latency, 2),
                message=f"Unavailable: {str(e)[:100]}"
            )
    
    def _check_system(self) -> ComponentStatus:
        """Check system resources (disk, memory)."""
        try:
            import psutil
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Determine status
            if disk_percent > 90 or memory_percent > 90:
                status = "unhealthy"
                message = "Critical resource usage"
            elif disk_percent > 80 or memory_percent > 80:
                status = "degraded"
                message = "High resource usage"
            else:
                status = "healthy"
                message = "Resources OK"
            
            return ComponentStatus(
                name="system",
                status=status,
                message=message,
                details={
                    "disk_used_percent": disk_percent,
                    "disk_free_gb": round(disk.free / (1024**3), 2),
                    "memory_used_percent": memory_percent,
                    "memory_available_gb": round(memory.available / (1024**3), 2),
                    "cpu_percent": cpu_percent,
                    "platform": platform.system(),
                    "python_version": platform.python_version()
                }
            )
            
        except ImportError:
            return ComponentStatus(
                name="system",
                status="unknown",
                message="psutil not installed"
            )
        except Exception as e:
            logger.warning(f"System health check failed: {e}")
            return ComponentStatus(
                name="system",
                status="unknown",
                message=str(e)[:100]
            )
    
    def _calculate_overall_status(self, components: List[ComponentStatus]) -> str:
        """
        Calculate overall system status from component statuses.
        
        Args:
            components: List of component statuses
            
        Returns:
            str: 'healthy', 'degraded', or 'unhealthy'
        """
        statuses = [c.status for c in components]
        
        # Critical components (must be healthy)
        critical = ['database']
        
        for comp in components:
            if comp.name in critical and comp.status == 'unhealthy':
                return 'unhealthy'
        
        if 'unhealthy' in statuses:
            # Non-critical unhealthy = degraded
            return 'degraded'
        
        if 'degraded' in statuses:
            return 'degraded'
        
        return 'healthy'


# Singleton instance
_health_service: Optional[HealthService] = None


def get_health_service(db: Optional[Session] = None) -> HealthService:
    """Get or create health service instance."""
    global _health_service
    
    if _health_service is None:
        _health_service = HealthService(db)
    elif db is not None:
        _health_service.db = db
    
    return _health_service
