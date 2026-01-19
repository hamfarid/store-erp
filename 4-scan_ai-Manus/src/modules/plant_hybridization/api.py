# File: /home/ubuntu/ai_web_organized/src/modules/plant_hybridization/api.py
"""
واجهة برمجة التطبيقات لمحاكاة التهجين النباتي
توفر هذه الوحدة واجهة برمجية للتفاعل مع محاكي التهجين النباتي
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path, Body, status
from fastapi.responses import FileResponse

from .hybridization_simulator import HybridizationSimulator

try:
    from src.modules.auth.auth_service import get_current_user, check_permission
except ImportError:
    # Fallback for testing or standalone usage
    def get_current_user():
        """Fallback function for testing"""
        return {"id": "test_user", "username": "test"}
    
    def check_permission(user, permission):
        """Fallback function for testing"""
        return True

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# إنشاء موجه API
router = APIRouter(
    prefix="/api/plant-hybridization",
    tags=["plant-hybridization"],
    responses={404: {"description": "Not found"}},
)

# إنشاء محاكي التهجين
simulator = HybridizationSimulator()

# تخزين مهام المحاكاة الجارية
running_simulations = {}

# Constants for permissions
PERMISSION_READ = "plant_hybridization:read"
PERMISSION_WRITE = "plant_hybridization:write"
PERMISSION_ADMIN = "plant_hybridization:admin"

# Constants for error messages
ERROR_ACCESS_DENIED = "ليس لديك صلاحية للوصول إلى هذا المورد"
ERROR_SIMULATION_ACCESS_DENIED = "ليس لديك صلاحية للوصول إلى هذه المحاكاة"


@router.get("/varieties")
async def get_varieties(
    crop_type: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على قائمة الأصناف النباتية

    المعلمات:
        crop_type: نوع المحصول (اختياري)
        current_user: المستخدم الحالي

    العائد:
        قائمة الأصناف النباتية
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        varieties = simulator.get_varieties(crop_type)
        return {"success": True, "varieties": varieties}
    except Exception as e:
        logger.error("خطأ أثناء استرجاع الأصناف: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء استرجاع الأصناف: {str(e)}"
        ) from e


@router.get("/traits")
async def get_traits(
    trait_ids: Optional[List[str]] = Query(None),
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على قائمة الصفات النباتية

    المعلمات:
        trait_ids: قائمة معرفات الصفات (اختياري)
        current_user: المستخدم الحالي

    العائد:
        قائمة الصفات النباتية
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        traits = simulator.get_traits(trait_ids)
        return {"success": True, "traits": traits}
    except Exception as e:
        logger.error("خطأ أثناء استرجاع الصفات: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء استرجاع الصفات: {str(e)}"
        ) from e


@router.get("/objectives")
async def get_objectives(
    objective_ids: Optional[List[str]] = Query(None),
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على قائمة أهداف التهجين

    المعلمات:
        objective_ids: قائمة معرفات الأهداف (اختياري)
        current_user: المستخدم الحالي

    العائد:
        قائمة أهداف التهجين
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        objectives = simulator.get_objectives(objective_ids)
        return {"success": True, "objectives": objectives}
    except Exception as e:
        logger.error("خطأ أثناء استرجاع الأهداف: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء استرجاع الأهداف: {str(e)}"
        ) from e


@router.post("/varieties")
async def add_variety(
    crop_type: str = Body(...),
    variety_id: str = Body(...),
    variety_data: Dict = Body(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    إضافة صنف نباتي جديد

    المعلمات:
        crop_type: نوع المحصول
        variety_id: معرف الصنف
        variety_data: بيانات الصنف
        current_user: المستخدم الحالي

    العائد:
        نتيجة العملية
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإضافة أصناف جديدة"
        )

    try:
        result = simulator.add_variety(crop_type, variety_id, variety_data)
        if result:
            return {"success": True, "message": f"تم إضافة الصنف {variety_id} بنجاح"}
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="فشل في إضافة الصنف"
        )
    except Exception as e:
        logger.error("خطأ أثناء إضافة الصنف: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء إضافة الصنف: {str(e)}"
        ) from e


@router.post("/traits")
async def add_trait(
    trait_id: str = Body(...),
    trait_data: Dict = Body(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    إضافة صفة نباتية جديدة

    المعلمات:
        trait_id: معرف الصفة
        trait_data: بيانات الصفة
        current_user: المستخدم الحالي

    العائد:
        نتيجة العملية
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإضافة صفات جديدة"
        )

    try:
        result = simulator.add_trait(trait_id, trait_data)
        if result:
            return {"success": True, "message": f"تم إضافة الصفة {trait_id} بنجاح"}
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="فشل في إضافة الصفة"
        )
    except Exception as e:
        logger.error("خطأ أثناء إضافة الصفة: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء إضافة الصفة: {str(e)}"
        ) from e


@router.post("/objectives")
async def add_objective(
    objective_id: str = Body(...),
    objective_data: Dict = Body(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    إضافة هدف تهجين جديد

    المعلمات:
        objective_id: معرف الهدف
        objective_data: بيانات الهدف
        current_user: المستخدم الحالي

    العائد:
        نتيجة العملية
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_WRITE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإضافة أهداف جديدة"
        )

    try:
        result = simulator.add_objective(objective_id, objective_data)
        if result:
            return {"success": True, "message": f"تم إضافة الهدف {objective_id} بنجاح"}
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="فشل في إضافة الهدف"
        )
    except Exception as e:
        logger.error("خطأ أثناء إضافة الهدف: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء إضافة الهدف: {str(e)}"
        ) from e


async def run_simulation_task(simulation_params: Dict, task_id: str):
    """
    تشغيل مهمة محاكاة التهجين في الخلفية

    المعلمات:
        simulation_params: معلمات المحاكاة
        task_id: معرف المهمة
    """
    try:
        # تحديث حالة المهمة
        running_simulations[task_id] = {
            "status": "running",
            "start_time": datetime.now().isoformat(),
            "params": simulation_params
        }

        # تشغيل المحاكاة
        result = simulator.run_simulation(simulation_params)
        
        # حفظ النتيجة
        running_simulations[task_id] = {
            "status": "completed",
            "result": result,
            "params": simulation_params,
            "created_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat()
        }
        
        logger.info("تم إكمال محاكاة التهجين: %s", task_id)
        
    except Exception as e:
        # حفظ حالة الخطأ
        running_simulations[task_id] = {
            "status": "failed",
            "error": str(e),
            "params": simulation_params,
            "created_at": datetime.now().isoformat(),
            "failed_at": datetime.now().isoformat()
        }
        
        logger.error("فشل في محاكاة التهجين %s: %s", task_id, str(e))


@router.post("/simulate")
async def start_simulation(
    simulation_params: Dict = Body(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: Dict = Depends(get_current_user)
):
    """
    بدء محاكاة تهجين جديدة

    المعلمات:
        simulation_params: معلمات المحاكاة
        background_tasks: مهام الخلفية
        current_user: المستخدم الحالي

    العائد:
        معرف المهمة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, "plant_hybridization:simulate"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لتشغيل محاكاة التهجين"
        )

    try:
        # إنشاء معرف المهمة
        task_id = f"simulation_task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{current_user['id']}"

        # إضافة معلومات المستخدم إلى معلمات المحاكاة
        simulation_params["user_id"] = current_user["id"]
        simulation_params["username"] = current_user.get("username", "unknown")

        # إضافة المهمة إلى مهام الخلفية
        background_tasks.add_task(run_simulation_task, simulation_params, task_id)

        # تحديث حالة المهمة
        running_simulations[task_id] = {
            "status": "pending",
            "start_time": datetime.now().isoformat(),
            "params": simulation_params
        }

        return {
            "success": True,
            "task_id": task_id,
            "message": "تم بدء محاكاة التهجين"
        }
    except Exception as e:
        logger.error("خطأ أثناء بدء محاكاة التهجين: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء بدء محاكاة التهجين: {str(e)}"
        ) from e


@router.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str = Path(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على حالة مهمة محاكاة

    المعلمات:
        task_id: معرف المهمة
        current_user: المستخدم الحالي

    العائد:
        حالة المهمة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        # التحقق من وجود المهمة
        if task_id not in running_simulations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"المهمة {task_id} غير موجودة"
            )

        # التحقق من ملكية المهمة
        task_info = running_simulations[task_id]
        if task_info["params"]["user_id"] != current_user["id"] and not check_permission(current_user, PERMISSION_ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ليس لديك صلاحية للوصول إلى هذه المهمة"
            )

        return {
            "success": True,
            "task_id": task_id,
            "status": task_info["status"],
            "start_time": task_info["start_time"],
            "end_time": task_info.get("end_time"),
            "simulation_id": task_info.get("simulation_id"),
            "error": task_info.get("error")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ أثناء استرجاع حالة المهمة: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء استرجاع حالة المهمة: {str(e)}"
        )


@router.get("/tasks")
async def get_user_tasks(
    limit: int = Query(10, ge=1, le=100),
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على قائمة مهام المستخدم

    المعلمات:
        limit: عدد المهام المراد استرجاعها
        current_user: المستخدم الحالي

    العائد:
        قائمة المهام
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        # استرجاع مهام المستخدم
        user_tasks = []

        for task_id, task_info in running_simulations.items():
            # التحقق من ملكية المهمة
            if task_info["params"]["user_id"] == current_user["id"] or check_permission(current_user, PERMISSION_ADMIN):
                user_tasks.append({
                    "task_id": task_id,
                    "status": task_info["status"],
                    "start_time": task_info["start_time"],
                    "end_time": task_info.get("end_time"),
                    "simulation_id": task_info.get("simulation_id"),
                    "error": task_info.get("error"),
                    "crop_type": task_info["params"].get("crop_type"),
                    "parent1_id": task_info["params"].get("parent1_id"),
                    "parent2_id": task_info["params"].get("parent2_id")
                })

        # ترتيب المهام حسب وقت البدء (من الأحدث إلى الأقدم)
        user_tasks.sort(key=lambda x: x["start_time"], reverse=True)

        # تحديد عدد المهام المراد استرجاعها
        user_tasks = user_tasks[:limit]

        return {
            "success": True,
            "tasks": user_tasks
        }
    except Exception as e:
        logger.error("خطأ أثناء استرجاع مهام المستخدم: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء استرجاع مهام المستخدم: {str(e)}"
        )


@router.get("/simulations/{simulation_id}")
async def get_simulation_result(
    simulation_id: str = Path(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على نتيجة محاكاة

    المعلمات:
        simulation_id: معرف المحاكاة
        current_user: المستخدم الحالي

    العائد:
        نتيجة المحاكاة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        # استرجاع نتيجة المحاكاة
        result = simulator.get_simulation_result(simulation_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"المحاكاة {simulation_id} غير موجودة"
            )

        # التحقق من ملكية المحاكاة
        if result["params"]["user_id"] != current_user["id"] and not check_permission(current_user, PERMISSION_ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_SIMULATION_ACCESS_DENIED
            )

        return {
            "success": True,
            "simulation": result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ أثناء استرجاع نتيجة المحاكاة: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء استرجاع نتيجة المحاكاة: {str(e)}"
        )


@router.get("/simulations")
async def get_simulation_history(
    limit: int = Query(10, ge=1, le=100),
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على سجل المحاكاة

    المعلمات:
        limit: عدد النتائج المراد استرجاعها
        current_user: المستخدم الحالي

    العائد:
        سجل المحاكاة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        # استرجاع سجل المحاكاة
        history = simulator.get_simulation_history(limit)

        return {
            "success": True,
            "history": history
        }
    except Exception as e:
        logger.error("خطأ أثناء استرجاع سجل المحاكاة: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء استرجاع سجل المحاكاة: {str(e)}"
        )


@router.get("/export/{simulation_id}")
async def export_simulation_to_csv(
    simulation_id: str = Path(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    تصدير نتيجة محاكاة إلى ملف CSV

    المعلمات:
        simulation_id: معرف المحاكاة
        current_user: المستخدم الحالي

    العائد:
        ملف CSV
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        # التحقق من وجود المحاكاة
        simulation = simulator.get_simulation_result(simulation_id)
        if not simulation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"المحاكاة {simulation_id} غير موجودة"
            )

        # التحقق من ملكية المحاكاة
        if simulation["params"]["user_id"] != current_user["id"] and not check_permission(current_user, PERMISSION_ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_SIMULATION_ACCESS_DENIED
            )

        # تصدير المحاكاة إلى ملف CSV
        csv_path = simulator.export_simulation_to_csv(simulation_id)

        if not csv_path:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في تصدير المحاكاة إلى ملف CSV"
            )

        # إرجاع ملف CSV
        return FileResponse(
            path=csv_path,
            filename=os.path.basename(csv_path),
            media_type="text/csv"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ أثناء تصدير المحاكاة: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء تصدير المحاكاة: {str(e)}"
        )


@router.get("/recommendations/{simulation_id}")
async def get_recommendations(
    simulation_id: str = Path(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على توصيات بناءً على نتيجة محاكاة

    المعلمات:
        simulation_id: معرف المحاكاة
        current_user: المستخدم الحالي

    العائد:
        توصيات للمزارع
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, PERMISSION_READ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_ACCESS_DENIED
        )

    try:
        # التحقق من وجود المحاكاة
        simulation = simulator.get_simulation_result(simulation_id)
        if not simulation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"المحاكاة {simulation_id} غير موجودة"
            )

        # التحقق من ملكية المحاكاة
        if simulation["params"]["user_id"] != current_user["id"] and not check_permission(current_user, PERMISSION_ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ERROR_SIMULATION_ACCESS_DENIED
            )

        # توليد التوصيات
        recommendations = simulator.generate_recommendations(simulation_id)

        if not recommendations["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=recommendations.get("error", "فشل في توليد التوصيات")
            )

        return recommendations
    except HTTPException:
        raise
    except Exception as e:
        logger.error("خطأ أثناء توليد التوصيات: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ أثناء توليد التوصيات: {str(e)}"
        )
