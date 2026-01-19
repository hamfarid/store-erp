"""
واجهة برمجة التطبيقات لمعالج الإعداد التفاعلي
Setup Wizard API Interface
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from .setup_wizard import SetupWizard

router = APIRouter(
    prefix="/api/setup",
    tags=["setup"],
    responses={404: {"description": "Not found"}},
)

# تهيئة معالج الإعداد
setup_wizard = SetupWizard()


class StepData(BaseModel):
    """نموذج بيانات الخطوة"""
    data: Dict[str, Any]


@router.get("/status")
async def get_setup_status():
    """
    الحصول على حالة الإعداد
    """
    return {
        "is_complete": setup_wizard.is_setup_complete(),
        "progress": setup_wizard.get_setup_progress()
    }


@router.get("/current-step")
async def get_current_step():
    """
    الحصول على الخطوة الحالية
    """
    return setup_wizard.get_current_step()


@router.post("/next-step")
async def next_step():
    """
    الانتقال إلى الخطوة التالية
    """
    return setup_wizard.next_step()


@router.post("/previous-step")
async def previous_step():
    """
    العودة إلى الخطوة السابقة
    """
    return setup_wizard.previous_step()


@router.put("/step/{step_id}")
async def update_step(step_id: str, step_data: StepData):
    """
    تحديث بيانات خطوة معينة
    """
    success = setup_wizard.update_step_data(step_id, step_data.data)
    if not success:
        raise HTTPException(status_code=400, detail="فشل تحديث بيانات الخطوة")

    return {"success": True, "message": f"تم تحديث بيانات الخطوة {step_id} بنجاح"}


@router.post("/complete")
async def complete_setup():
    """
    إكمال عملية الإعداد
    """
    success = setup_wizard.complete_setup()
    if not success:
        raise HTTPException(status_code=400, detail="فشل إكمال عملية الإعداد")

    return {"success": True, "message": "تم إكمال عملية الإعداد بنجاح"}


@router.post("/reset")
async def reset_setup():
    """
    إعادة تعيين عملية الإعداد
    """
    success = setup_wizard.reset_setup()
    if not success:
        raise HTTPException(status_code=400, detail="فشل إعادة تعيين عملية الإعداد")

    return {"success": True, "message": "تم إعادة تعيين عملية الإعداد بنجاح"}


@router.get("/config")
async def get_config():
    """
    الحصول على التكوين الكامل
    """
    return setup_wizard.get_config()


@router.post("/export")
async def export_config(export_path: str = Body(..., embed=True)):
    """
    تصدير التكوين إلى ملف
    """
    success = setup_wizard.export_config(export_path)
    if not success:
        raise HTTPException(status_code=400, detail="فشل تصدير التكوين")

    return {"success": True, "message": f"تم تصدير التكوين إلى {export_path} بنجاح"}


@router.post("/import")
async def import_config(import_path: str = Body(..., embed=True)):
    """
    استيراد التكوين من ملف
    """
    success = setup_wizard.import_config(import_path)
    if not success:
        raise HTTPException(status_code=400, detail="فشل استيراد التكوين")

    return {"success": True, "message": f"تم استيراد التكوين من {import_path} بنجاح"}


@router.get("/validate/{step_id}")
async def validate_step(step_id: str, data: Dict[str, Any] = Body(...)):
    """
    التحقق من صحة بيانات خطوة معينة
    """
    # Note: Using protected method _validate_step_data is acceptable here
    # as this is part of the setup wizard's intended API
    validation_result = setup_wizard._validate_step_data(step_id, data)
    return validation_result
