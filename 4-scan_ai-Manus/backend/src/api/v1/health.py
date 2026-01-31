"""
FILE: backend/src/api/v1/health.py | PURPOSE: Health check API | OWNER: Backend Team | LAST-AUDITED: 2025-12-08

Health Check API Routes

Provides health check endpoints for monitoring.

Version: 1.0.0
"""

from datetime import datetime

import psutil
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

try:
    from src.core import database  # preferred for tests/patching
    from src.core.database import check_db_health, get_db
except ModuleNotFoundError:  # pragma: no cover
    # Fallback when importing via package-qualified paths (e.g., backend.src...)
    from ...core import database
    from ...core.database import check_db_health, get_db

# Router
router = APIRouter(prefix="/api/v1", tags=["health"])


# Pydantic Schemas
class HealthResponse(BaseModel):
    status: str
    service: str = "Gaara Scan AI"
    timestamp: datetime
    version: str = "2.0.0"
    database: str = "unknown"
    uptime: str = "unknown"


# Routes
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    db_status = "healthy" if database.check_db_health() else "unhealthy"

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        database=db_status,
    )


@router.get("/ping")
async def ping() -> dict:
    """Simple ping endpoint"""
    return {"message": "pong"}


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check endpoint."""
    db_ok = database.check_db_health()

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    payload = {
        "status": "healthy" if db_ok else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "database": {"status": "healthy" if db_ok else "unhealthy"},
            "system": {
                "cpu_usage": f"{cpu}%",
                "memory_usage": f"{memory.percent}%",
                "disk_usage": f"{disk.percent}%",
            },
        },
    }

    if not db_ok:
        return JSONResponse(status_code=503, content=payload)

    return payload


@router.get("/health/live")
async def liveness_check():
    """Liveness probe for Kubernetes/Docker"""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe for Kubernetes/Docker"""
    db_ready = check_db_health()
    if not db_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not ready"
        )
    return {"status": "ready"}


@router.get("/system/metrics")
async def metrics_endpoint():
    """
    Prometheus metrics endpoint
    Returns basic system metrics in Prometheus format
    """
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        # Format metrics in Prometheus text format
        metrics = f"""# HELP system_cpu_usage_percent CPU usage percentage
# TYPE system_cpu_usage_percent gauge
system_cpu_usage_percent {cpu}

# HELP system_memory_usage_percent Memory usage percentage
# TYPE system_memory_usage_percent gauge
system_memory_usage_percent {memory.percent}

# HELP system_memory_available_bytes Available memory in bytes
# TYPE system_memory_available_bytes gauge
system_memory_available_bytes {memory.available}

# HELP system_disk_usage_percent Disk usage percentage
# TYPE system_disk_usage_percent gauge
system_disk_usage_percent {disk.percent}

# HELP system_disk_free_bytes Free disk space in bytes
# TYPE system_disk_free_bytes gauge
system_disk_free_bytes {disk.free}

# HELP system_disk_total_bytes Total disk space in bytes
# TYPE system_disk_total_bytes gauge
system_disk_total_bytes {disk.total}
"""
        from fastapi.responses import Response
        return Response(content=metrics, media_type="text/plain")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error collecting metrics: {str(e)}"
        )
