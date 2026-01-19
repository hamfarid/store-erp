# File: /home/ubuntu/clean_project/src/modules/activity_log/api.py
"""
مسار الملف: /home/ubuntu/clean_project/src/modules/activity_log/api.py

واجهة برمجة تطبيقات سجل النشاط
توفر نقاط نهاية لإدارة وعرض سجلات النشاط
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/logs")
async def get_activity_logs(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    log_type: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """الحصول على سجلات النشاط"""
    try:
        # محاكاة سجلات النشاط
        logs = [
            {
                "id": "log_001",
                "type": "ai",
                "level": "info",
                "message": "تم تشخيص مرض اللفحة المبكرة بنجاح",
                "details": {
                    "crop": "الطماطم",
                    "confidence": 92.5,
                    "user_id": "user_123"
                },
                "timestamp": "2025-06-14T10:45:00Z",
                "source": "disease_diagnosis"
            },
            {
                "id": "log_002",
                "type": "system",
                "level": "warning",
                "message": "ارتفاع في استخدام المعالج",
                "details": {
                    "cpu_usage": 85.2,
                    "threshold": 80.0
                },
                "timestamp": "2025-06-14T10:40:00Z",
                "source": "system_monitor"
            },
            {
                "id": "log_003",
                "type": "user",
                "level": "info",
                "message": "تسجيل دخول مستخدم جديد",
                "details": {
                    "username": "farmer_001",
                    "ip_address": "192.168.1.100"
                },
                "timestamp": "2025-06-14T10:35:00Z",
                "source": "auth_system"
            },
            {
                "id": "log_004",
                "type": "ai",
                "level": "success",
                "message": "اكتمل تدريب النموذج الجديد",
                "details": {
                    "model_name": "disease_detection_v3",
                    "accuracy": 96.1,
                    "training_time": "2.5 hours"
                },
                "timestamp": "2025-06-14T10:30:00Z",
                "source": "ai_training"
            },
            {
                "id": "log_005",
                "type": "error",
                "level": "error",
                "message": "فشل في الاتصال بقاعدة البيانات",
                "details": {
                    "error_code": "DB_CONNECTION_FAILED",
                    "retry_count": 3
                },
                "timestamp": "2025-06-14T10:25:00Z",
                "source": "database"
            },
            {
                "id": "log_006",
                "type": "diagnosis",
                "level": "info",
                "message": "تشخيص جديد للبطاطس",
                "details": {
                    "crop": "البطاطس",
                    "disease": "اللفحة المتأخرة",
                    "confidence": 89.3
                },
                "timestamp": "2025-06-14T10:20:00Z",
                "source": "disease_diagnosis"
            }
        ]

        # تطبيق الفلاتر
        filtered_logs = logs

        if log_type:
            filtered_logs = [
                log for log in filtered_logs if log["type"] == log_type]

        # تطبيق التصفح
        total = len(filtered_logs)
        paginated_logs = filtered_logs[offset:offset + limit]

        return {
            "logs": paginated_logs,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }

    except Exception as e:
        logger.error(f"خطأ في الحصول على سجلات النشاط: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")


@router.post("/logs")
async def create_activity_log(log_data: Dict[str, Any]):
    """إنشاء سجل نشاط جديد"""
    try:
        # التحقق من البيانات المطلوبة
        required_fields = ["type", "level", "message", "source"]
        for field in required_fields:
            if field not in log_data:
                raise HTTPException(
                    status_code=400, detail=f"الحقل {field} مطلوب")

        # إنشاء السجل الجديد
        new_log = {
            "id": f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": log_data["type"],
            "level": log_data["level"],
            "message": log_data["message"],
            "details": log_data.get("details", {}),
            "timestamp": datetime.now().isoformat() + "Z",
            "source": log_data["source"]
        }

        return {
            "message": "تم إنشاء سجل النشاط بنجاح",
            "log": new_log
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في إنشاء سجل النشاط: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")


@router.get("/logs/{log_id}")
async def get_activity_log(log_id: str):
    """الحصول على تفاصيل سجل نشاط محدد"""
    try:
        # محاكاة البحث عن السجل
        log = {
            "id": log_id,
            "type": "ai",
            "level": "info",
            "message": "تم تشخيص مرض اللفحة المبكرة بنجاح",
            "details": {
                "crop": "الطماطم",
                "confidence": 92.5,
                "user_id": "user_123",
                "image_size": "1024x768",
                "processing_time": "0.8 seconds",
                "model_version": "v2.1"
            },
            "timestamp": "2025-06-14T10:45:00Z",
            "source": "disease_diagnosis",
            "related_logs": [
                {
                    "id": "log_002",
                    "message": "بدء معالجة الصورة",
                    "timestamp": "2025-06-14T10:44:58Z"
                },
                {
                    "id": "log_003",
                    "message": "اكتمال تحليل الصورة",
                    "timestamp": "2025-06-14T10:45:02Z"
                }
            ]
        }

        return log

    except Exception as e:
        logger.error(f"خطأ في الحصول على سجل النشاط: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")


@router.get("/statistics")
async def get_log_statistics():
    """الحصول على إحصائيات سجلات النشاط"""
    try:
        return {
            "total_logs": 15420,
            "today_logs": 234,
            "log_types": [
                {
                    "type": "ai",
                    "count": 5678,
                    "percentage": 36.8
                },
                {
                    "type": "system",
                    "count": 3456,
                    "percentage": 22.4
                },
                {
                    "type": "user",
                    "count": 2890,
                    "percentage": 18.7
                },
                {
                    "type": "diagnosis",
                    "count": 2234,
                    "percentage": 14.5
                },
                {
                    "type": "error",
                    "count": 1162,
                    "percentage": 7.5
                }
            ],
            "log_levels": [
                {
                    "level": "info",
                    "count": 12456,
                    "percentage": 80.8
                },
                {
                    "level": "warning",
                    "count": 1890,
                    "percentage": 12.3
                },
                {
                    "level": "error",
                    "count": 789,
                    "percentage": 5.1
                },
                {
                    "level": "success",
                    "count": 285,
                    "percentage": 1.8
                }
            ],
            "hourly_distribution": [
                {"hour": 0, "count": 45},
                {"hour": 1, "count": 23},
                {"hour": 2, "count": 12},
                {"hour": 3, "count": 8},
                {"hour": 4, "count": 15},
                {"hour": 5, "count": 34},
                {"hour": 6, "count": 67},
                {"hour": 7, "count": 89},
                {"hour": 8, "count": 156},
                {"hour": 9, "count": 234},
                {"hour": 10, "count": 289},
                {"hour": 11, "count": 267}
            ]
        }

    except Exception as e:
        logger.error(f"خطأ في الحصول على إحصائيات السجلات: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")


@router.delete("/logs")
async def cleanup_old_logs(days: int = Query(30, ge=1, le=365)):
    """تنظيف السجلات القديمة"""
    try:
        # محاكاة تنظيف السجلات
        cutoff_date = datetime.now() - timedelta(days=days)

        # في التطبيق الحقيقي، سيتم حذف السجلات من قاعدة البيانات
        deleted_count = 1250  # محاكاة

        return {
            "message": f"تم حذف السجلات الأقدم من {days} يوم",
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }

    except Exception as e:
        logger.error(f"خطأ في تنظيف السجلات: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")
