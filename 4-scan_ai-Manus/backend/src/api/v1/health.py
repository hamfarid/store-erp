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
