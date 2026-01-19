"""
API endpoints لإدارة التحديثات المجدولة
Scheduled Updates Management API
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ...services.scheduled_updater import get_scheduled_updater

router = APIRouter(prefix="/scheduled-updates", tags=["Scheduled Updates"])


# Pydantic Models
class UpdateHistoryItem(BaseModel):
    type: str
    timestamp: str
    stats: dict


class NextRunTime(BaseModel):
    job_id: str
    name: str
    next_run_time: Optional[str]


class SchedulerStatus(BaseModel):
    is_running: bool
    jobs_count: int
    next_run_times: dict
    last_updates: List[UpdateHistoryItem]


# Endpoints

@router.get("/status", response_model=SchedulerStatus)
async def get_scheduler_status():
    """
    الحصول على حالة المجدول
    """
    try:
        updater = get_scheduled_updater()

        return SchedulerStatus(
            is_running=updater.is_running,
            jobs_count=len(updater.scheduler.get_jobs()) if updater.is_running else 0,
            next_run_times=updater.get_next_run_times() if updater.is_running else {},
            last_updates=[
                UpdateHistoryItem(**item)
                for item in updater.get_update_history(limit=10)
            ]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start")
async def start_scheduler():
    """
    بدء المجدول
    """
    try:
        updater = get_scheduled_updater()

        if updater.is_running:
            return {
                "success": False,
                "message": "Scheduler is already running"
            }

        updater.start()

        return {
            "success": True,
            "message": "Scheduler started successfully",
            "next_run_times": updater.get_next_run_times()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_scheduler():
    """
    إيقاف المجدول
    """
    try:
        updater = get_scheduled_updater()

        if not updater.is_running:
            return {
                "success": False,
                "message": "Scheduler is not running"
            }

        updater.stop()

        return {
            "success": True,
            "message": "Scheduler stopped successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trigger/{update_type}")
async def trigger_manual_update(update_type: str):
    """
    تشغيل تحديث يدوي

    - **update_type**: نوع التحديث (database, nutrients, sources)
    """
    try:
        if update_type not in ["database", "nutrients", "sources"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid update type. Must be: database, nutrients, or sources"
            )

        updater = get_scheduled_updater()

        if not updater.is_running:
            raise HTTPException(
                status_code=400,
                detail="Scheduler is not running. Start it first."
            )

        updater.trigger_manual_update(update_type)

        return {
            "success": True,
            "message": f"Manual {update_type} update triggered successfully",
            "triggered_at": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[UpdateHistoryItem])
async def get_update_history(limit: int = 20):
    """
    الحصول على سجل التحديثات

    - **limit**: عدد السجلات (افتراضي: 20)
    """
    try:
        updater = get_scheduled_updater()
        history = updater.get_update_history(limit=limit)

        return [UpdateHistoryItem(**item) for item in history]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/next-runs")
async def get_next_run_times():
    """
    الحصول على أوقات التشغيل التالية لجميع المهام
    """
    try:
        updater = get_scheduled_updater()

        if not updater.is_running:
            return {
                "success": False,
                "message": "Scheduler is not running",
                "next_run_times": {}
            }

        return {
            "success": True,
            "next_run_times": updater.get_next_run_times()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedule")
async def get_schedule_info():
    """
    الحصول على معلومات الجدول الزمني
    """
    return {
        "schedules": {
            "database_update": {
                "frequency": "Weekly",
                "schedule": "Every Sunday at 2:00 AM",
                "description": "تحديث قاعدة بيانات الأمراض من المصادر الموثوقة"
            },
            "nutrients_update": {
                "frequency": "Monthly",
                "schedule": "First day of each month at 3:00 AM",
                "description": "تحديث معلومات نقص العناصر الغذائية"
            },
            "sources_check": {
                "frequency": "Daily",
                "schedule": "Every day at 4:00 AM",
                "description": "فحص توفر المصادر الموثوقة"
            },
            "cleanup": {
                "frequency": "Weekly",
                "schedule": "Every Saturday at 1:00 AM",
                "description": "تنظيف السجلات القديمة"
            }
        },
        "timezone": "UTC",
        "note": "جميع الأوقات بتوقيت UTC"
    }


@router.get("/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "service": "Scheduled Updates API",
        "timestamp": datetime.utcnow().isoformat()
    }
