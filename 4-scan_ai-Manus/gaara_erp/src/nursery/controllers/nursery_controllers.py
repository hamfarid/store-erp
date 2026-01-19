"""
وحدة التحكم في المشاتل والمزارع
يحتوي هذا الملف على وحدات التحكم للتعامل مع طلبات المشاتل والمزارع
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse

from ..services.nursery_services import NurseryService, FarmService
from ..models.nursery_models import Nursery, NurserySection, Farm, FarmPlot
from ....core.database.db_manager import DBManager
from ....core.auth.auth_manager import get_current_user, check_permissions


# إنشاء موجه API للمشاتل
nursery_router = APIRouter(
    prefix="/api/nursery",
    tags=["nursery"],
    responses={404: {"description": "غير موجود"}},
)

# إنشاء موجه API للمزارع
farm_router = APIRouter(
    prefix="/api/farm",
    tags=["farm"],
    responses={404: {"description": "غير موجود"}},
)


# وظيفة للحصول على خدمة المشاتل
def get_nursery_service():
    db_manager = DBManager()
    return NurseryService(db_manager)


# وظيفة للحصول على خدمة المزارع
def get_farm_service():
    db_manager = DBManager()
    return FarmService(db_manager)


# مسارات API للمشاتل
@nursery_router.post("/", response_model=Dict[str, Any])
async def create_nursery(
    nursery_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    nursery_service: NurseryService = Depends(get_nursery_service)
):
    """
    إنشاء مشتل جديد
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "nursery:create"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإنشاء مشتل")
    
    # إضافة معلومات الشركة والفرع من المستخدم الحالي
    if "company_id" not in nursery_data and "company_id" in current_user:
        nursery_data["company_id"] = current_user["company_id"]
    if "branch_id" not in nursery_data and "branch_id" in current_user:
        nursery_data["branch_id"] = current_user["branch_id"]
    
    # إنشاء المشتل
    try:
        nursery = nursery_service.create_nursery(nursery_data)
        return {"status": "success", "data": nursery.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل في إنشاء المشتل: {str(e)}")


@nursery_router.get("/", response_model=Dict[str, Any])
async def get_all_nurseries(
    company_id: Optional[str] = Query(None, description="معرف الشركة للتصفية"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع للتصفية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    nursery_service: NurseryService = Depends(get_nursery_service)
):
    """
    الحصول على قائمة المشاتل
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "nursery:view"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض المشاتل")
    
    # تطبيق تصفية الشركة والفرع بناءً على صلاحيات المستخدم
    if not check_permissions(current_user, "nursery:view_all"):
        if "company_id" in current_user:
            company_id = current_user["company_id"]
        if "branch_id" in current_user:
            branch_id = current_user["branch_id"]
    
    # الحصول على المشاتل
    try:
        nurseries = nursery_service.get_all_nurseries(company_id, branch_id)
        return {
            "status": "success", 
            "count": len(nurseries), 
            "data": [nursery.to_dict() for nursery in nurseries]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل في الحصول على المشاتل: {str(e)}")


@nursery_router.get("/{nursery_id}", response_model=Dict[str, Any])
async def get_nursery(
    nursery_id: str = Path(..., description="معرف المشتل"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    nursery_service: NurseryService = Depends(get_nursery_service)
):
    """
    الحصول على مشتل بواسطة المعرف
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "nursery:view"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض المشتل")
    
    # الحصول على المشتل
    nursery = nursery_service.get_nursery(nursery_id)
    if not nursery:
        raise HTTPException(status_code=404, detail="المشتل غير موجود")
    
    # التحقق من صلاحية الوصول للمشتل
    if not check_permissions(current_user, "nursery:view_all"):
        if "company_id" in current_user and nursery.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى هذا المشتل")
        if "branch_id" in current_user and nursery.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى هذا المشتل")
    
    return {"status": "success", "data": nursery.to_dict()}


@nursery_router.put("/{nursery_id}", response_model=Dict[str, Any])
async def update_nursery(
    nursery_data: Dict[str, Any],
    nursery_id: str = Path(..., description="معرف المشتل"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    nursery_service: NurseryService = Depends(get_nursery_service)
):
    """
    تحديث مشتل
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "nursery:update"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتحديث المشتل")
    
    # التحقق من وجود المشتل
    nursery = nursery_service.get_nursery(nursery_id)
    if not nursery:
        raise HTTPException(status_code=404, detail="المشتل غير موجود")
    
    # التحقق من صلاحية الوصول للمشتل
    if not check_permissions(current_user, "nursery:update_all"):
        if "company_id" in current_user and nursery.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتحديث هذا المشتل")
        if "branch_id" in current_user and nursery.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتحديث هذا المشتل")
    
    # تحديث المشتل
    try:
        updated_nursery = nursery_service.update_nursery(nursery_id, nursery_data)
        return {"status": "success", "data": updated_nursery.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل في تحديث المشتل: {str(e)}")


@nursery_router.delete("/{nursery_id}", response_model=Dict[str, Any])
async def delete_nursery(
    nursery_id: str = Path(..., description="معرف المشتل"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    nursery_service: NurseryService = Depends(get_nursery_service)
):
    """
    حذف مشتل
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "nursery:delete"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف المشتل")
    
    # التحقق من وجود المشتل
    nursery = nursery_service.get_nursery(nursery_id)
    if not nursery:
        raise HTTPException(status_code=404, detail="المشتل غير موجود")
    
    # التحقق من صلاحية الوصول للمشتل
    if not check_permissions(current_user, "nursery:delete_all"):
        if "company_id" in current_user and nursery.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف هذا المشتل")
        if "branch_id" in current_user and nursery.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف هذا المشتل")
    
    # حذف المشتل
    success = nursery_service.delete_nursery(nursery_id)
    if success:
        return {"status": "success", "message": "تم حذف المشتل بنجاح"}
    else:
        raise HTTPException(status_code=500, detail="فشل في حذف المشتل")


@nursery_router.get("/{nursery_id}/statistics", response_model=Dict[str, Any])
async def get_nursery_statistics(
    nursery_id: str = Path(..., description="معرف المشتل"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    nursery_service: NurseryService = Depends(get_nursery_service)
):
    """
    الحصول على إحصائيات المشتل
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "nursery:view"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض إحصائيات المشتل")
    
    # التحقق من وجود المشتل
    nursery = nursery_service.get_nursery(nursery_id)
    if not nursery:
        raise HTTPException(status_code=404, detail="المشتل غير موجود")
    
    # التحقق من صلاحية الوصول للمشتل
    if not check_permissions(current_user, "nursery:view_all"):
        if "company_id" in current_user and nursery.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى إحصائيات هذا المشتل")
        if "branch_id" in current_user and nursery.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى إحصائيات هذا المشتل")
    
    # الحصول على إحصائيات المشتل
    statistics = nursery_service.get_nursery_statistics(nursery_id)
    return {"status": "success", "data": statistics}


@nursery_router.get("/{nursery_id}/report", response_model=Dict[str, Any])
async def generate_nursery_report(
    nursery_id: str = Path(..., description="معرف المشتل"),
    report_type: str = Query("summary", description="نوع التقرير (summary, detailed, financial)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    nursery_service: NurseryService = Depends(get_nursery_service)
):
    """
    إنشاء تقرير عن المشتل
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "nursery:view"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض تقارير المشتل")
    
    # التحقق من وجود المشتل
    nursery = nursery_service.get_nursery(nursery_id)
    if not nursery:
        raise HTTPException(status_code=404, detail="المشتل غير موجود")
    
    # التحقق من صلاحية الوصول للمشتل
    if not check_permissions(current_user, "nursery:view_all"):
        if "company_id" in current_user and nursery.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى تقارير هذا المشتل")
        if "branch_id" in current_user and nursery.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى تقارير هذا المشتل")
    
    # التحقق من صلاحية الوصول للتقارير المالية
    if report_type == "financial" and not check_permissions(current_user, "nursery:view_financial"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى التقارير المالية")
    
    # إنشاء التقرير
    report = nursery_service.generate_nursery_report(nursery_id, report_type)
    return {"status": "success", "data": report}


# مسارات API للمزارع
@farm_router.post("/", response_model=Dict[str, Any])
async def create_farm(
    farm_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    farm_service: FarmService = Depends(get_farm_service)
):
    """
    إنشاء مزرعة جديدة
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "farm:create"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لإنشاء مزرعة")
    
    # إضافة معلومات الشركة والفرع من المستخدم الحالي
    if "company_id" not in farm_data and "company_id" in current_user:
        farm_data["company_id"] = current_user["company_id"]
    if "branch_id" not in farm_data and "branch_id" in current_user:
        farm_data["branch_id"] = current_user["branch_id"]
    
    # إنشاء المزرعة
    try:
        farm = farm_service.create_farm(farm_data)
        return {"status": "success", "data": farm.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل في إنشاء المزرعة: {str(e)}")


@farm_router.get("/", response_model=Dict[str, Any])
async def get_all_farms(
    company_id: Optional[str] = Query(None, description="معرف الشركة للتصفية"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع للتصفية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    farm_service: FarmService = Depends(get_farm_service)
):
    """
    الحصول على قائمة المزارع
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "farm:view"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض المزارع")
    
    # تطبيق تصفية الشركة والفرع بناءً على صلاحيات المستخدم
    if not check_permissions(current_user, "farm:view_all"):
        if "company_id" in current_user:
            company_id = current_user["company_id"]
        if "branch_id" in current_user:
            branch_id = current_user["branch_id"]
    
    # الحصول على المزارع
    try:
        farms = farm_service.get_all_farms(company_id, branch_id)
        return {
            "status": "success", 
            "count": len(farms), 
            "data": [farm.to_dict() for farm in farms]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل في الحصول على المزارع: {str(e)}")


@farm_router.get("/{farm_id}", response_model=Dict[str, Any])
async def get_farm(
    farm_id: str = Path(..., description="معرف المزرعة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    farm_service: FarmService = Depends(get_farm_service)
):
    """
    الحصول على مزرعة بواسطة المعرف
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "farm:view"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض المزرعة")
    
    # الحصول على المزرعة
    farm = farm_service.get_farm(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="المزرعة غير موجودة")
    
    # التحقق من صلاحية الوصول للمزرعة
    if not check_permissions(current_user, "farm:view_all"):
        if "company_id" in current_user and farm.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى هذه المزرعة")
        if "branch_id" in current_user and farm.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى هذه المزرعة")
    
    return {"status": "success", "data": farm.to_dict()}


@farm_router.put("/{farm_id}", response_model=Dict[str, Any])
async def update_farm(
    farm_data: Dict[str, Any],
    farm_id: str = Path(..., description="معرف المزرعة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    farm_service: FarmService = Depends(get_farm_service)
):
    """
    تحديث مزرعة
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "farm:update"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتحديث المزرعة")
    
    # التحقق من وجود المزرعة
    farm = farm_service.get_farm(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="المزرعة غير موجودة")
    
    # التحقق من صلاحية الوصول للمزرعة
    if not check_permissions(current_user, "farm:update_all"):
        if "company_id" in current_user and farm.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتحديث هذه المزرعة")
        if "branch_id" in current_user and farm.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لتحديث هذه المزرعة")
    
    # تحديث المزرعة
    try:
        updated_farm = farm_service.update_farm(farm_id, farm_data)
        return {"status": "success", "data": updated_farm.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل في تحديث المزرعة: {str(e)}")


@farm_router.delete("/{farm_id}", response_model=Dict[str, Any])
async def delete_farm(
    farm_id: str = Path(..., description="معرف المزرعة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    farm_service: FarmService = Depends(get_farm_service)
):
    """
    حذف مزرعة
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "farm:delete"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف المزرعة")
    
    # التحقق من وجود المزرعة
    farm = farm_service.get_farm(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="المزرعة غير موجودة")
    
    # التحقق من صلاحية الوصول للمزرعة
    if not check_permissions(current_user, "farm:delete_all"):
        if "company_id" in current_user and farm.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف هذه المزرعة")
        if "branch_id" in current_user and farm.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية لحذف هذه المزرعة")
    
    # حذف المزرعة
    success = farm_service.delete_farm(farm_id)
    if success:
        return {"status": "success", "message": "تم حذف المزرعة بنجاح"}
    else:
        raise HTTPException(status_code=500, detail="فشل في حذف المزرعة")


@farm_router.get("/{farm_id}/statistics", response_model=Dict[str, Any])
async def get_farm_statistics(
    farm_id: str = Path(..., description="معرف المزرعة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    farm_service: FarmService = Depends(get_farm_service)
):
    """
    الحصول على إحصائيات المزرعة
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "farm:view"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض إحصائيات المزرعة")
    
    # التحقق من وجود المزرعة
    farm = farm_service.get_farm(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="المزرعة غير موجودة")
    
    # التحقق من صلاحية الوصول للمزرعة
    if not check_permissions(current_user, "farm:view_all"):
        if "company_id" in current_user and farm.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى إحصائيات هذه المزرعة")
        if "branch_id" in current_user and farm.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى إحصائيات هذه المزرعة")
    
    # الحصول على إحصائيات المزرعة
    statistics = farm_service.get_farm_statistics(farm_id)
    return {"status": "success", "data": statistics}


@farm_router.get("/{farm_id}/report", response_model=Dict[str, Any])
async def generate_farm_report(
    farm_id: str = Path(..., description="معرف المزرعة"),
    report_type: str = Query("summary", description="نوع التقرير (summary, detailed, financial)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    farm_service: FarmService = Depends(get_farm_service)
):
    """
    إنشاء تقرير عن المزرعة
    """
    # التحقق من الصلاحيات
    if not check_permissions(current_user, "farm:view"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية لعرض تقارير المزرعة")
    
    # التحقق من وجود المزرعة
    farm = farm_service.get_farm(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="المزرعة غير موجودة")
    
    # التحقق من صلاحية الوصول للمزرعة
    if not check_permissions(current_user, "farm:view_all"):
        if "company_id" in current_user and farm.company_id != current_user["company_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى تقارير هذه المزرعة")
        if "branch_id" in current_user and farm.branch_id != current_user["branch_id"]:
            raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى تقارير هذه المزرعة")
    
    # التحقق من صلاحية الوصول للتقارير المالية
    if report_type == "financial" and not check_permissions(current_user, "farm:view_financial"):
        raise HTTPException(status_code=403, detail="ليس لديك صلاحية للوصول إلى التقارير المالية")
    
    # إنشاء التقرير
    report = farm_service.generate_farm_report(farm_id, report_type)
    return {"status": "success", "data": report}
