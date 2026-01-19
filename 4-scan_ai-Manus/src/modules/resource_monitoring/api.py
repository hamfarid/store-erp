# File: /home/ubuntu/ai_web_organized/src/modules/resource_monitoring/api.py
"""
واجهة برمجة التطبيقات لمراقبة الموارد
توفر هذه الوحدة واجهات برمجية للتعامل مع مراقبة موارد النظام وتخزين البيانات التاريخية
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException

from src.modules.auth.api import get_current_user, check_permission
from . import db_service
from .resource_collector import ResourceCollector

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for repeated string literals
ERROR_METRIC_NOT_FOUND = "المقياس غير موجود"
ERROR_MANAGE_METRICS_PERMISSION = "ليس لديك صلاحية لإدارة مقاييس الموارد"
ERROR_VIEW_RESOURCES_PERMISSION = "ليس لديك صلاحية لعرض بيانات الموارد"
TIMEZONE_OFFSET = "+00:00"
ERROR_MANAGE_SYSTEM_PERMISSION = "ليس لديك صلاحية لإدارة موارد النظام"

# إنشاء موجه API
router = APIRouter(
    prefix="/api/resource-monitoring",
    tags=["resource-monitoring"],
    responses={404: {"description": "Not found"}},
)

# تهيئة جامع الموارد
resource_collector = ResourceCollector()

# واجهات برمجية للمقاييس


@router.get("/metrics")
async def get_metrics(
    resource_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على قائمة المقاييس"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض مقاييس الموارد")

        if resource_type:
            metrics = db_service.get_metrics_by_type(resource_type)
        else:
            metrics = db_service.get_all_metrics()

        return {"status": "success", "data": metrics}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على المقاييس: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/metrics/{metric_id}")
async def get_metric(
    metric_id: int,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على مقياس بواسطة المعرف"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض مقاييس الموارد")

        metric = db_service.get_metric_by_id(metric_id)
        if not metric:
            raise HTTPException(status_code=404, detail=ERROR_METRIC_NOT_FOUND)

        return {"status": "success", "data": metric}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على المقياس %s: %s", metric_id, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/metrics")
async def create_metric(
    metric_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """إنشاء مقياس جديد"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_METRICS_PERMISSION)

        # التحقق من صحة البيانات
        if not metric_data.get("resourceType"):
            raise HTTPException(status_code=400, detail="نوع المورد مطلوب")
        if not metric_data.get("metricName"):
            raise HTTPException(status_code=400, detail="اسم المقياس مطلوب")

        metric = db_service.create_metric(metric_data)
        if not metric:
            raise HTTPException(status_code=400, detail="فشل إنشاء المقياس، قد يكون موجوداً بالفعل")

        return {"status": "success", "data": metric, "message": "تم إنشاء المقياس بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في إنشاء مقياس جديد: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/metrics/{metric_id}")
async def update_metric(
    metric_id: int,
    metric_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """تحديث مقياس موجود"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_METRICS_PERMISSION)

        metric = db_service.update_metric(metric_id, metric_data)
        if not metric:
            raise HTTPException(status_code=404, detail=ERROR_METRIC_NOT_FOUND)

        return {"status": "success", "data": metric, "message": "تم تحديث المقياس بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في تحديث المقياس %s: %s", metric_id, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/metrics/{metric_id}")
async def delete_metric(
    metric_id: int,
    current_user: dict = Depends(get_current_user)
):
    """حذف مقياس"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_METRICS_PERMISSION)

        result = db_service.delete_metric(metric_id)
        if result is None:
            raise HTTPException(status_code=404, detail=ERROR_METRIC_NOT_FOUND)
        if result is False:
            raise HTTPException(status_code=400, detail="لا يمكن حذف المقياس لأنه مرتبط بنقاط بيانات")

        return {"status": "success", "data": result, "message": "تم حذف المقياس بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في حذف المقياس %s: %s", metric_id, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

# واجهات برمجية لنقاط البيانات


@router.post("/data-points")
async def add_data_point(
    data_point: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """إضافة نقطة بيانات جديدة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "add_resource_data"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإضافة بيانات الموارد")

        # التحقق من صحة البيانات
        if not (data_point.get("metricId") or data_point.get("metricName")):
            raise HTTPException(status_code=400, detail="معرف المقياس أو اسمه مطلوب")
        if "value" not in data_point:
            raise HTTPException(status_code=400, detail="قيمة نقطة البيانات مطلوبة")

        result = db_service.add_data_point(data_point)
        if not result:
            raise HTTPException(status_code=400, detail="فشل إضافة نقطة البيانات")

        return {"status": "success", "data": result, "message": "تم إضافة نقطة البيانات بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في إضافة نقطة بيانات جديدة: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/data-points/batch")
async def add_multiple_data_points(
    data_points: List[Dict[str, Any]],
    current_user: dict = Depends(get_current_user)
):
    """إضافة عدة نقاط بيانات دفعة واحدة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "add_resource_data"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإضافة بيانات الموارد")

        # التحقق من صحة البيانات
        if not data_points:
            raise HTTPException(status_code=400, detail="قائمة نقاط البيانات مطلوبة")

        results = db_service.add_multiple_data_points(data_points)

        return {
            "status": "success",
            "data": results,
            "message": f"تم إضافة {len(results)} نقطة بيانات بنجاح"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في إضافة نقاط بيانات متعددة: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/data-points")
async def get_data_points(
    metric_id: Optional[int] = None,
    metric_name: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    module_name: Optional[str] = None,
    server_id: Optional[str] = None,
    limit: int = 1000,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على نقاط البيانات"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        # تحويل المعلمات
        if metric_name and not metric_id:
            metric = db_service.get_metric_by_name(metric_name)
            if metric:
                metric_id = metric["id"]

        # تحويل الأوقات إلى كائنات datetime
        start_datetime = None
        if start_time:
            try:
                start_datetime = datetime.fromisoformat(start_time.replace('Z', TIMEZONE_OFFSET))
            except ValueError as exc:
                raise HTTPException(status_code=400, detail="صيغة وقت البداية غير صالحة") from exc

        end_datetime = None
        if end_time:
            try:
                end_datetime = datetime.fromisoformat(end_time.replace('Z', TIMEZONE_OFFSET))
            except ValueError as exc:
                raise HTTPException(status_code=400, detail="صيغة وقت النهاية غير صالحة") from exc

        data_points = db_service.get_data_points(
            metric_id=metric_id,
            start_time=start_datetime,
            end_time=end_datetime,
            module_name=module_name,
            server_id=server_id,
            limit=limit
        )

        return {"status": "success", "data": data_points}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على نقاط البيانات: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/data-points/latest")
async def get_latest_data_point(
    metric_id: Optional[int] = None,
    metric_name: Optional[str] = None,
    module_name: Optional[str] = None,
    server_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على أحدث نقطة بيانات"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        # تحويل المعلمات
        if metric_name and not metric_id:
            metric = db_service.get_metric_by_name(metric_name)
            if metric:
                metric_id = metric["id"]

        data_point = db_service.get_latest_data_point(
            metric_id=metric_id,
            module_name=module_name,
            server_id=server_id
        )

        return {"status": "success", "data": data_point}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على أحدث نقطة بيانات: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/data-points/old")
async def delete_old_data_points(
    days_to_keep: int = 30,
    current_user: dict = Depends(get_current_user)
):
    """حذف نقاط البيانات القديمة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإدارة بيانات الموارد")

        # حساب التاريخ المحدد
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        # حذف البيانات القديمة
        deleted_count = db_service.delete_old_data_points(cutoff_date)

        return {
            "status": "success",
            "data": {"deletedCount": deleted_count},
            "message": f"تم حذف {deleted_count} نقطة بيانات قديمة"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في حذف نقاط البيانات القديمة: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

# واجهات برمجية للعتبات


@router.get("/thresholds")
async def get_thresholds(
    current_user: dict = Depends(get_current_user)
):
    """الحصول على قائمة العتبات"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        thresholds = db_service.get_all_thresholds()

        return {"status": "success", "data": thresholds}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على العتبات: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/thresholds/metric/{metric_id}")
async def get_threshold_by_metric(
    metric_id: int,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على عتبة بواسطة معرف المقياس"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        threshold = db_service.get_threshold_by_metric_id(metric_id)
        if not threshold:
            raise HTTPException(status_code=404, detail="العتبة غير موجودة")

        return {"status": "success", "data": threshold}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على العتبة للمقياس %s: %s", metric_id, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/thresholds")
async def create_or_update_threshold(
    threshold_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """إنشاء أو تحديث عتبة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإدارة عتبات الموارد")

        threshold = db_service.create_or_update_threshold(threshold_data)

        return {"status": "success", "data": threshold, "message": "تم حفظ العتبة بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في إنشاء أو تحديث العتبة: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/thresholds/{threshold_id}")
async def delete_threshold(
    threshold_id: int,
    current_user: dict = Depends(get_current_user)
):
    """حذف عتبة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإدارة عتبات الموارد")

        result = db_service.delete_threshold(threshold_id)
        if not result:
            raise HTTPException(status_code=404, detail="العتبة غير موجودة")

        return {"status": "success", "data": result, "message": "تم حذف العتبة بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في حذف العتبة %s: %s", threshold_id, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

# واجهات برمجية للبيانات المجمعة


@router.get("/aggregated-data")
async def get_aggregated_data(
    aggregation_type: str = "hourly",
    metric_id: Optional[int] = None,
    metric_name: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    module_name: Optional[str] = None,
    server_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على البيانات المجمعة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        # تحويل المعلمات
        if metric_name and not metric_id:
            metric = db_service.get_metric_by_name(metric_name)
            if metric:
                metric_id = metric["id"]

        # تحويل الأوقات إلى كائنات datetime
        start_datetime = None
        if start_time:
            try:
                start_datetime = datetime.fromisoformat(start_time.replace('Z', TIMEZONE_OFFSET))
            except ValueError:
                raise HTTPException(status_code=400, detail="صيغة وقت البداية غير صالحة")

        end_datetime = None
        if end_time:
            try:
                end_datetime = datetime.fromisoformat(end_time.replace('Z', TIMEZONE_OFFSET))
            except ValueError:
                raise HTTPException(status_code=400, detail="صيغة وقت النهاية غير صالحة")

        # التحقق من نوع التجميع
        valid_aggregation_types = ["hourly", "daily", "weekly", "monthly"]
        if aggregation_type not in valid_aggregation_types:
            raise HTTPException(
                status_code=400,
                detail=f"نوع التجميع غير صالح. القيم المسموح بها: {', '.join(valid_aggregation_types)}"
            )

        aggregated_data = db_service.get_aggregated_data(
            aggregation_type=aggregation_type,
            metric_id=metric_id,
            start_time=start_datetime,
            end_time=end_datetime,
            module_name=module_name,
            server_id=server_id
        )

        return {"status": "success", "data": aggregated_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على البيانات المجمعة: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/aggregated-data/store")
async def store_aggregated_data(
    aggregation_type: str = "hourly",
    current_user: dict = Depends(get_current_user)
):
    """تخزين البيانات المجمعة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإدارة البيانات المجمعة")

        # التحقق من نوع التجميع
        valid_aggregation_types = ["hourly", "daily", "weekly", "monthly"]
        if aggregation_type not in valid_aggregation_types:
            raise HTTPException(
                status_code=400,
                detail=f"نوع التجميع غير صالح. القيم المسموح بها: {', '.join(valid_aggregation_types)}"
            )

        result = db_service.store_aggregated_data(aggregation_type)

        return {"status": "success", "data": result, "message": "تم تخزين البيانات المجمعة بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في تخزين البيانات المجمعة: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

# واجهات برمجية للخوادم


@router.get("/servers")
async def get_servers(
    current_user: dict = Depends(get_current_user)
):
    """الحصول على قائمة الخوادم"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        servers = db_service.get_all_servers()

        return {"status": "success", "data": servers}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على الخوادم: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/servers/{server_id}")
async def get_server(
    server_id: str,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على خادم بواسطة المعرف"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        server = db_service.get_server_by_id(server_id)
        if not server:
            raise HTTPException(status_code=404, detail="الخادم غير موجود")

        return {"status": "success", "data": server}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على الخادم %s: %s", server_id, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/servers")
async def create_or_update_server(
    server_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """إنشاء أو تحديث خادم"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_SYSTEM_PERMISSION)

        server = db_service.create_or_update_server(server_data)

        return {"status": "success", "data": server, "message": "تم حفظ الخادم بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في إنشاء أو تحديث الخادم: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/servers/{server_id}")
async def delete_server(
    server_id: str,
    current_user: dict = Depends(get_current_user)
):
    """حذف خادم"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_SYSTEM_PERMISSION)

        result = db_service.delete_server(server_id)
        if not result:
            raise HTTPException(status_code=404, detail="الخادم غير موجود")

        return {"status": "success", "data": result, "message": "تم حذف الخادم بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في حذف الخادم %s: %s", server_id, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

# واجهات برمجية للوحدات


@router.get("/modules")
async def get_modules(
    current_user: dict = Depends(get_current_user)
):
    """الحصول على قائمة الوحدات"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        modules = db_service.get_all_modules()

        return {"status": "success", "data": modules}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على الوحدات: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/modules/{module_name}")
async def get_module(
    module_name: str,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على وحدة بواسطة الاسم"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail=ERROR_VIEW_RESOURCES_PERMISSION)

        module = db_service.get_module_by_name(module_name)
        if not module:
            raise HTTPException(status_code=404, detail="الوحدة غير موجودة")

        return {"status": "success", "data": module}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على الوحدة %s: %s", module_name, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/modules")
async def create_or_update_module(
    module_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """إنشاء أو تحديث وحدة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_SYSTEM_PERMISSION)

        module = db_service.create_or_update_module(module_data)

        return {"status": "success", "data": module, "message": "تم حفظ الوحدة بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في إنشاء أو تحديث الوحدة: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/modules/{module_name}")
async def delete_module(
    module_name: str,
    current_user: dict = Depends(get_current_user)
):
    """حذف وحدة"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_SYSTEM_PERMISSION)

        result = db_service.delete_module(module_name)
        if not result:
            raise HTTPException(status_code=404, detail="الوحدة غير موجودة")

        return {"status": "success", "data": result, "message": "تم حذف الوحدة بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في حذف الوحدة %s: %s", module_name, str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

# واجهات برمجية لجمع الموارد


@router.get("/collect/system")
async def collect_system_resources(
    current_user: dict = Depends(get_current_user)
):
    """جمع بيانات موارد النظام"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_SYSTEM_PERMISSION)

        # جمع بيانات الموارد
        resources = resource_collector.collect_system_resources()

        # تخزين البيانات في قاعدة البيانات
        data_points = []
        for resource_type, metrics in resources.items():
            for metric_name, value in metrics.items():
                data_point = {
                    "metricName": metric_name,
                    "value": value,
                    "timestamp": datetime.now(),
                    "metadata": {"source": "system_collector"}
                }
                data_points.append(data_point)

        # إضافة نقاط البيانات
        if data_points:
            db_service.add_multiple_data_points(data_points)

        return {"status": "success", "data": resources, "message": "تم جمع بيانات موارد النظام بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في جمع بيانات موارد النظام: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/collect/database")
async def collect_database_resources(
    current_user: dict = Depends(get_current_user)
):
    """جمع بيانات موارد قاعدة البيانات"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_SYSTEM_PERMISSION)

        # جمع بيانات موارد قاعدة البيانات
        resources = resource_collector.collect_database_resources()

        # تخزين البيانات في قاعدة البيانات
        data_points = []
        for metric_name, value in resources.items():
            data_point = {
                "metricName": metric_name,
                "value": value,
                "timestamp": datetime.now(),
                "metadata": {"source": "database_collector"}
            }
            data_points.append(data_point)

        # إضافة نقاط البيانات
        if data_points:
            db_service.add_multiple_data_points(data_points)

        return {"status": "success", "data": resources, "message": "تم جمع بيانات موارد قاعدة البيانات بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في جمع بيانات موارد قاعدة البيانات: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/collect/all")
async def collect_all_resources(
    current_user: dict = Depends(get_current_user)
):
    """جمع جميع بيانات الموارد"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "manage_resources"):
            raise HTTPException(status_code=403, detail=ERROR_MANAGE_SYSTEM_PERMISSION)

        # جمع بيانات موارد النظام
        system_resources = resource_collector.collect_system_resources()

        # جمع بيانات موارد قاعدة البيانات
        db_resources = resource_collector.collect_database_resources()

        # تجميع جميع البيانات
        all_resources = {
            "system": system_resources,
            "database": db_resources
        }

        # تخزين البيانات في قاعدة البيانات
        data_points = []

        # إضافة بيانات موارد النظام
        for resource_type, metrics in system_resources.items():
            for metric_name, value in metrics.items():
                data_point = {
                    "metricName": metric_name,
                    "value": value,
                    "timestamp": datetime.now(),
                    "metadata": {"source": "system_collector", "type": resource_type}
                }
                data_points.append(data_point)

        # إضافة بيانات موارد قاعدة البيانات
        for metric_name, value in db_resources.items():
            data_point = {
                "metricName": metric_name,
                "value": value,
                "timestamp": datetime.now(),
                "metadata": {"source": "database_collector"}
            }
            data_points.append(data_point)

        # إضافة نقاط البيانات
        if data_points:
            db_service.add_multiple_data_points(data_points)

        return {"status": "success", "data": all_resources, "message": "تم جمع جميع بيانات الموارد بنجاح"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في جمع جميع بيانات الموارد: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

# واجهات برمجية للتقارير


@router.get("/reports/summary")
async def get_resources_summary(
    current_user: dict = Depends(get_current_user)
):
    """الحصول على ملخص الموارد"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض ملخص الموارد")

        # جمع بيانات الموارد الحالية
        current_resources = resource_collector.collect_system_resources()

        # الحصول على أحدث نقاط البيانات لكل مقياس
        metrics = db_service.get_all_metrics()
        latest_data_points = {}

        for metric in metrics:
            metric_id = metric["id"]
            latest_point = db_service.get_latest_data_point(metric_id=metric_id)
            if latest_point:
                latest_data_points[metric["metricName"]] = latest_point

        # الحصول على العتبات
        thresholds = db_service.get_all_thresholds()
        thresholds_by_metric = {}

        for threshold in thresholds:
            metric_id = threshold["metricId"]
            metric = db_service.get_metric_by_id(metric_id)
            if metric:
                thresholds_by_metric[metric["metricName"]] = threshold

        # بناء ملخص الموارد
        summary = {
            "currentResources": current_resources,
            "latestDataPoints": latest_data_points,
            "thresholds": thresholds_by_metric,
            "timestamp": datetime.now().isoformat()
        }

        return {"status": "success", "data": summary}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على ملخص الموارد: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/reports/trends")
async def get_resource_trends(
    metric_id: Optional[int] = None,
    metric_name: Optional[str] = None,
    days: int = 7,
    current_user: dict = Depends(get_current_user)
):
    """الحصول على اتجاهات الموارد"""
    try:
        # التحقق من الصلاحيات
        if not check_permission(current_user, "view_resources"):
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض اتجاهات الموارد")

        # تحويل المعلمات
        if metric_name and not metric_id:
            metric = db_service.get_metric_by_name(metric_name)
            if metric:
                metric_id = metric["id"]

        if not metric_id:
            raise HTTPException(status_code=400, detail="معرف المقياس أو اسمه مطلوب")

        # حساب نطاق التاريخ
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        # الحصول على البيانات
        data_points = db_service.get_data_points(
            metric_id=metric_id,
            start_time=start_time,
            end_time=end_time,
            limit=10000
        )

        # تحليل الاتجاهات
        trends = db_service.analyze_trends(data_points)

        return {"status": "success", "data": {"dataPoints": data_points, "trends": trends}}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ في الحصول على اتجاهات الموارد: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e
