# File: /home/ubuntu/ai_web_organized/src/modules/alert_management/api.py
"""
واجهة برمجة التطبيقات لإدارة التنبيهات
توفر هذه الوحدة واجهات برمجية للتعامل مع التنبيهات والإشعارات
"""

import logging
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query

# استيراد وحدة إدارة التنبيهات
from . import (
    alert_monitor,
    create_alert,
    delete_alert,
    get_alert,
    get_alerts,
    get_alerts_config,
    update_alert_status,
    update_alerts_config,
)

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# إنشاء مخطط للواجهة البرمجية
router = APIRouter(prefix="/api/alerts", tags=["alerts"])

# واجهات برمجة التطبيقات للتنبيهات


@router.get("/")
def api_get_alerts(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    module: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: Optional[int] = Query(None)
):
    """الحصول على التنبيهات"""
    # الحصول على التنبيهات
    alerts = get_alerts(status, severity, module, start_date, end_date, limit)
    return alerts


@router.get("/{alert_id}")
def api_get_alert(alert_id: str = Path(...)):
    """الحصول على تنبيه محدد"""
    # الحصول على التنبيه
    alert = get_alert(alert_id)

    if alert:
        return alert
    else:
        raise HTTPException(status_code=404, detail="Alert not found")


@router.post("/")
def api_create_alert(data: dict = Body(...)):
    """إنشاء تنبيه جديد"""
    # التحقق من وجود البيانات المطلوبة
    if not data:
        raise HTTPException(status_code=400, detail="Missing alert data")

    # التحقق من وجود الحقول المطلوبة
    required_fields = ["type", "severity", "module", "messageAr", "messageEn"]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400,
                                detail=f"Missing required field: {field}")

    # إنشاء التنبيه
    alert = create_alert(
        data["type"],
        data["severity"],
        data["module"],
        data["messageAr"],
        data["messageEn"],
        data.get("details")
    )

    if alert:
        return alert
    else:
        raise HTTPException(status_code=500, detail="Failed to create alert")


@router.put("/{alert_id}/status")
def api_update_alert_status(alert_id: str = Path(...), data: dict = Body(...)):
    """تحديث حالة التنبيه"""
    # التحقق من وجود البيانات المطلوبة
    if not data or "status" not in data:
        raise HTTPException(status_code=400, detail="Missing status data")

    # التحقق من صحة الحالة
    status = data["status"]
    if status not in ["active", "acknowledged", "resolved"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    # تحديث حالة التنبيه
    alert = update_alert_status(alert_id, status, data.get("user"))

    if alert:
        return alert
    else:
        raise HTTPException(status_code=404, detail="Alert not found")


@router.delete("/{alert_id}")
def api_delete_alert(alert_id: str = Path(...)):
    """حذف تنبيه"""
    # حذف التنبيه
    result = delete_alert(alert_id)

    if result:
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Alert not found")


@router.get("/config")
def api_get_alerts_config():
    """الحصول على إعدادات التنبيهات"""
    # الحصول على إعدادات التنبيهات
    config = get_alerts_config()
    return config


@router.put("/config")
def api_update_alerts_config(data: dict = Body(...)):
    """تحديث إعدادات التنبيهات"""
    # التحقق من وجود البيانات المطلوبة
    if not data:
        raise HTTPException(status_code=400, detail="Missing config data")

    # تحديث إعدادات التنبيهات
    config = update_alerts_config(data)
    return config


@router.post("/monitor/start")
def api_start_alert_monitor():
    """بدء مراقب التنبيهات"""
    try:
        # بدء مراقب التنبيهات
        alert_monitor.start()

        return {
            "success": True,
            "message": "Alert monitor started successfully"
        }
    except Exception as e:
        logger.error(f"Error starting alert monitor: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start alert monitor: {str(e)}")


@router.post("/monitor/stop")
def api_stop_alert_monitor():
    """إيقاف مراقب التنبيهات"""
    try:
        # إيقاف مراقب التنبيهات
        alert_monitor.stop()

        return {
            "success": True,
            "message": "Alert monitor stopped successfully"
        }
    except Exception as e:
        logger.error(f"Error stopping alert monitor: {str(e)}")
        raise HTTPException(status_code=500,
                            detail=f"Failed to stop alert monitor: {str(e)}")


@router.get("/monitor/status")
def api_get_alert_monitor_status():
    """الحصول على حالة مراقب التنبيهات"""
    try:
        # الحصول على حالة مراقب التنبيهات
        status = {
            "running": alert_monitor.running,
            "interval": alert_monitor.interval
        }

        return status
    except Exception as e:
        logger.error(f"Error getting alert monitor status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get alert monitor status: {str(e)}")


@router.post("/test")
def api_test_alert():
    """إنشاء تنبيه اختباري"""
    try:
        # إنشاء تنبيه اختباري
        alert = create_alert(
            "test",
            "low",
            "alert_management",
            "تنبيه اختباري",
            "Test alert",
            {"test": True}
        )

        if alert:
            return {
                "success": True,
                "message": "Test alert created successfully",
                "alert": alert
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to create test alert")
    except Exception as e:
        logger.error(f"Error creating test alert: {str(e)}")
        raise HTTPException(status_code=500,
                            detail=f"Failed to create test alert: {str(e)}")


# تسجيل البلوبرنت في التطبيق
