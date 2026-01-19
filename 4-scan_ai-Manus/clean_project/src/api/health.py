"""
API الصحة - فحص حالة النظام والخدمات
Health API - System and services health check
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
import psutil
import logging

from src.core.database import check_db_health

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check():
    """
    فحص الصحة الأساسي
    Basic health check
    """
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Gaara Scan AI",
        "version": "2.0.0"
    })

@router.get("/health/detailed")
async def detailed_health_check():
    """
    فحص الصحة المفصل
    Detailed health check
    """
    
    # فحص قاعدة البيانات
    db_healthy = check_db_health()
    
    # معلومات النظام
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    health_data = {
        "status": "healthy" if db_healthy else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Gaara Scan AI",
        "version": "2.0.0",
        "components": {
            "database": {
                "status": "healthy" if db_healthy else "unhealthy",
                "type": "PostgreSQL"
            },
            "system": {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "disk_usage": f"{disk.percent}%",
                "available_memory": f"{memory.available / (1024**3):.2f} GB",
                "available_disk": f"{disk.free / (1024**3):.2f} GB"
            }
        }
    }
    
    status_code = 200 if db_healthy else 503
    return JSONResponse(content=health_data, status_code=status_code)

@router.get("/ping")
async def ping():
    """
    Ping بسيط
    Simple ping
    """
    return {"message": "pong"}

