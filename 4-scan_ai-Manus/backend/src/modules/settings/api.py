# File: /home/ubuntu/ai_web_organized/src/modules/settings/api.py
"""
واجهة برمجة التطبيقات للإعدادات العامة
توفر هذه الوحدة واجهة برمجة التطبيقات لإدارة الإعدادات العامة للنظام
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, UploadFile
from fastapi.responses import FileResponse

from src.modules.auth.auth_service import check_permission, get_current_user

from .settings_service import SettingsService

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("settings_api.log"),
        logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ثوابت للأذونات
SETTINGS_VIEW_PERMISSION = "settings:view"
SETTINGS_EDIT_PERMISSION = "settings:edit"
SETTINGS_EXPORT_PERMISSION = "settings:export"
SETTINGS_IMPORT_PERMISSION = "settings:import"

# ثوابت للرسائل
ACCESS_DENIED_MESSAGE = "ليس لديك صلاحية للوصول إلى هذه الإعدادات"
EDIT_DENIED_MESSAGE = "ليس لديك صلاحية لتعديل هذه الإعدادات"
SETTINGS_TYPE_DESCRIPTION = "نوع الإعدادات (general, company, system, connection, all)"
PASSWORD_MASK = "********"

# إنشاء موجه
router = APIRouter(
    prefix="/api/settings",
    tags=["settings"],
    responses={404: {"description": "Not found"}},
)

# إنشاء خدمة الإعدادات
settings_service = SettingsService()


@router.get("/general")
async def get_general_settings(current_user: dict = Depends(get_current_user)):
    """
    الحصول على الإعدادات العامة

    Args:
        current_user (dict): المستخدم الحالي

    Returns:
        dict: الإعدادات العامة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_VIEW_PERMISSION):
        raise HTTPException(status_code=403, detail=ACCESS_DENIED_MESSAGE)

    try:
        # الحصول على الإعدادات العامة
        settings = settings_service.get_general_settings()
        return settings
    except Exception as e:
        logger.exception(f"Error getting general settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء الحصول على الإعدادات العامة: {str(e)}",
        )


@router.post("/general")
async def update_general_settings(
    settings: Dict[str, Any] = Body(...), current_user: dict = Depends(get_current_user)
):
    """
    تحديث الإعدادات العامة

    Args:
        settings (Dict[str, Any]): الإعدادات الجديدة
        current_user (dict): المستخدم الحالي

    Returns:
        dict: الإعدادات المحدثة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_EDIT_PERMISSION):
        raise HTTPException(status_code=403, detail=EDIT_DENIED_MESSAGE)

    try:
        # التحقق من صحة الإعدادات
        valid, message = settings_service.validate_settings(
            "general", settings)
        if not valid:
            raise HTTPException(status_code=400, detail=message)

        # تحديث الإعدادات العامة
        updated_settings = settings_service.update_general_settings(settings)
        return updated_settings
    except Exception as e:
        logger.exception(f"Error updating general settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء تحديث الإعدادات العامة: {str(e)}")


@router.get("/company")
async def get_company_settings(current_user: dict = Depends(get_current_user)):
    """
    الحصول على إعدادات الشركة

    Args:
        current_user (dict): المستخدم الحالي

    Returns:
        dict: إعدادات الشركة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_VIEW_PERMISSION):
        raise HTTPException(status_code=403, detail=ACCESS_DENIED_MESSAGE)

    try:
        # الحصول على إعدادات الشركة
        settings = settings_service.get_company_settings()
        return settings
    except Exception as e:
        logger.exception(f"Error getting company settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء الحصول على إعدادات الشركة: {str(e)}")


@router.post("/company")
async def update_company_settings(
    settings: Dict[str, Any] = Body(...), current_user: dict = Depends(get_current_user)
):
    """
    تحديث إعدادات الشركة

    Args:
        settings (Dict[str, Any]): الإعدادات الجديدة
        current_user (dict): المستخدم الحالي

    Returns:
        dict: الإعدادات المحدثة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_EDIT_PERMISSION):
        raise HTTPException(status_code=403, detail=EDIT_DENIED_MESSAGE)

    try:
        # التحقق من صحة الإعدادات
        valid, message = settings_service.validate_settings(
            "company", settings)
        if not valid:
            raise HTTPException(status_code=400, detail=message)

        # تحديث إعدادات الشركة
        updated_settings = settings_service.update_company_settings(settings)
        return updated_settings
    except Exception as e:
        logger.exception(f"Error updating company settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء تحديث إعدادات الشركة: {str(e)}")


@router.get("/system")
async def get_system_settings(current_user: dict = Depends(get_current_user)):
    """
    الحصول على إعدادات النظام

    Args:
        current_user (dict): المستخدم الحالي

    Returns:
        dict: إعدادات النظام
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_VIEW_PERMISSION):
        raise HTTPException(status_code=403, detail=ACCESS_DENIED_MESSAGE)

    try:
        # الحصول على إعدادات النظام
        settings = settings_service.get_system_settings()
        return settings
    except Exception as e:
        logger.exception(f"Error getting system settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء الحصول على إعدادات النظام: {str(e)}")


@router.post("/system")
async def update_system_settings(
    settings: Dict[str, Any] = Body(...), current_user: dict = Depends(get_current_user)
):
    """
    تحديث إعدادات النظام

    Args:
        settings (Dict[str, Any]): الإعدادات الجديدة
        current_user (dict): المستخدم الحالي

    Returns:
        dict: الإعدادات المحدثة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_EDIT_PERMISSION):
        raise HTTPException(status_code=403, detail=EDIT_DENIED_MESSAGE)

    try:
        # التحقق من صحة الإعدادات
        valid, message = settings_service.validate_settings("system", settings)
        if not valid:
            raise HTTPException(status_code=400, detail=message)

        # تحديث إعدادات النظام
        updated_settings = settings_service.update_system_settings(settings)
        return updated_settings
    except Exception as e:
        logger.exception(f"Error updating system settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء تحديث إعدادات النظام: {str(e)}")


@router.get("/connection")
async def get_connection_settings(
        current_user: dict = Depends(get_current_user)):
    """
    الحصول على إعدادات الاتصال

    Args:
        current_user (dict): المستخدم الحالي

    Returns:
        dict: إعدادات الاتصال (مع إخفاء كلمات المرور وبيانات الاعتماد الحساسة)
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_VIEW_PERMISSION):
        raise HTTPException(status_code=403, detail=ACCESS_DENIED_MESSAGE)

    try:
        # الحصول على إعدادات الاتصال
        settings = settings_service.get_connection_settings()

        # إخفاء كلمات المرور وبيانات الاعتماد الحساسة
        masked_settings = _mask_sensitive_data(settings, "connection")
        return masked_settings
    except Exception as e:
        logger.exception(f"Error getting connection settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء الحصول على إعدادات الاتصال: {str(e)}",
        )


def _mask_sensitive_data(
    settings: Dict[str, Any], settings_type: str
) -> Dict[str, Any]:
    """
    إخفاء البيانات الحساسة في الإعدادات

    Args:
        settings: الإعدادات المراد إخفاء البيانات الحساسة فيها
        settings_type: نوع الإعدادات

    Returns:
        الإعدادات مع البيانات المخفية
    """
    masked_settings = settings.copy()

    if settings_type == "connection":
        if "database" in masked_settings and "password" in masked_settings["database"]:
            masked_settings["database"]["password"] = PASSWORD_MASK

        if (
            "redis" in masked_settings
            and "password" in masked_settings["redis"]
            and masked_settings["redis"]["password"]
        ):
            masked_settings["redis"]["password"] = PASSWORD_MASK

        if "email" in masked_settings and "smtp_password" in masked_settings["email"]:
            masked_settings["email"]["smtp_password"] = PASSWORD_MASK

        if "sms" in masked_settings and "auth_token" in masked_settings["sms"]:
            masked_settings["sms"]["auth_token"] = PASSWORD_MASK

        if "ai" in masked_settings and "api_key" in masked_settings["ai"]:
            masked_settings["ai"]["api_key"] = PASSWORD_MASK

    return masked_settings


@router.post("/connection")
async def update_connection_settings(
    settings: Dict[str, Any] = Body(...), current_user: dict = Depends(get_current_user)
):
    """
    تحديث إعدادات الاتصال

    Args:
        settings (Dict[str, Any]): الإعدادات الجديدة
        current_user (dict): المستخدم الحالي

    Returns:
        dict: الإعدادات المحدثة (مع إخفاء كلمات المرور وبيانات الاعتماد الحساسة)
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_EDIT_PERMISSION):
        raise HTTPException(status_code=403, detail=EDIT_DENIED_MESSAGE)

    try:
        # التحقق من صحة الإعدادات
        valid, message = settings_service.validate_settings(
            "connection", settings)
        if not valid:
            raise HTTPException(status_code=400, detail=message)

        # تحديث إعدادات الاتصال
        updated_settings = settings_service.update_connection_settings(
            settings)

        # إخفاء كلمات المرور وبيانات الاعتماد الحساسة
        masked_settings = _mask_sensitive_data(updated_settings, "connection")
        return masked_settings
    except Exception as e:
        logger.exception(f"Error updating connection settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء تحديث إعدادات الاتصال: {str(e)}")


@router.get("/all")
async def get_all_settings(current_user: dict = Depends(get_current_user)):
    """
    الحصول على جميع الإعدادات

    Args:
        current_user (dict): المستخدم الحالي

    Returns:
        dict: جميع الإعدادات (مع إخفاء كلمات المرور وبيانات الاعتماد الحساسة)
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_VIEW_PERMISSION):
        raise HTTPException(status_code=403, detail=ACCESS_DENIED_MESSAGE)

    try:
        # الحصول على جميع الإعدادات
        settings = settings_service.get_all_settings()

        # إخفاء كلمات المرور وبيانات الاعتماد الحساسة
        if "connection" in settings:
            settings["connection"] = _mask_sensitive_data(
                settings["connection"], "connection"
            )

        return settings
    except Exception as e:
        logger.exception(f"Error getting all settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء الحصول على جميع الإعدادات: {str(e)}")


@router.post("/reset/{settings_type}")
async def reset_settings(
    settings_type: str = Path(..., description=SETTINGS_TYPE_DESCRIPTION),
    current_user: dict = Depends(get_current_user),
):
    """
    إعادة تعيين الإعدادات إلى القيم الافتراضية

    Args:
        settings_type (str): نوع الإعدادات
        current_user (dict): المستخدم الحالي

    Returns:
        dict: الإعدادات بعد إعادة التعيين
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_EDIT_PERMISSION):
        raise HTTPException(status_code=403, detail=EDIT_DENIED_MESSAGE)

    # التحقق من نوع الإعدادات
    if settings_type not in [
        "general",
        "company",
        "system",
        "connection",
            "all"]:
        raise HTTPException(
            status_code=400, detail=f"نوع إعدادات غير صالح: {settings_type}"
        )

    try:
        # إعادة تعيين الإعدادات
        reset_settings = settings_service.reset_settings(settings_type)

        # إخفاء كلمات المرور وبيانات الاعتماد الحساسة
        if settings_type == "connection":
            reset_settings = _mask_sensitive_data(reset_settings, "connection")
        elif settings_type == "all" and "connection" in reset_settings:
            reset_settings["connection"] = _mask_sensitive_data(
                reset_settings["connection"], "connection"
            )

        return reset_settings
    except Exception as e:
        logger.exception(f"Error resetting settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء إعادة تعيين الإعدادات: {str(e)}")


@router.post("/export/{settings_type}")
async def export_settings(
    settings_type: str = Path(..., description=SETTINGS_TYPE_DESCRIPTION),
    current_user: dict = Depends(get_current_user),
):
    """
    تصدير الإعدادات إلى ملف

    Args:
        settings_type (str): نوع الإعدادات
        current_user (dict): المستخدم الحالي

    Returns:
        dict: معلومات الملف المصدر
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_EXPORT_PERMISSION):
        raise HTTPException(
            status_code=403, detail="ليس لديك صلاحية لتصدير هذه الإعدادات"
        )

    # التحقق من نوع الإعدادات
    if settings_type not in [
        "general",
        "company",
        "system",
        "connection",
            "all"]:
        raise HTTPException(
            status_code=400, detail=f"نوع إعدادات غير صالح: {settings_type}"
        )

    # التحقق من صلاحيات إضافية لإعدادات الاتصال
    if (
        settings_type == "connection" or settings_type == "all"
    ) and not check_permission(current_user, "settings:export:connection"):
        raise HTTPException(
            status_code=403, detail="ليس لديك صلاحية لتصدير إعدادات الاتصال"
        )

    try:
        # تصدير الإعدادات
        file_path = settings_service.export_settings(settings_type)

        # إنشاء اسم الملف
        file_name = os.path.basename(file_path)

        return {
            "success": True,
            "file_path": file_path,
            "file_name": file_name,
            "settings_type": settings_type,
            "export_time": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.exception(f"Error exporting settings: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"حدث خطأ أثناء تصدير الإعدادات: {str(e)}"
        )


@router.get("/export/download/{file_name}")
async def download_exported_settings(
    file_name: str = Path(..., description="اسم الملف المصدر"),
    current_user: dict = Depends(get_current_user),
):
    """
    تنزيل الإعدادات المصدرة

    Args:
        file_name (str): اسم الملف المصدر
        current_user (dict): المستخدم الحالي

    Returns:
        FileResponse: ملف الإعدادات المصدرة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_EXPORT_PERMISSION):
        raise HTTPException(
            status_code=403, detail="ليس لديك صلاحية لتنزيل هذه الإعدادات"
        )

    # تحديد مسار الملف
    file_path = os.path.join(settings_service.config_dir, file_name)

    # التحقق من وجود الملف
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404,
                            detail=f"الملف غير موجود: {file_name}")

    # التحقق من أن الملف في مجلد الإعدادات
    if not file_path.startswith(settings_service.config_dir):
        raise HTTPException(
            status_code=403, detail="ليس لديك صلاحية للوصول إلى هذا الملف"
        )

    # تنزيل الملف
    return FileResponse(
        path=file_path, filename=file_name, media_type="application/json"
    )


@router.post("/import/{settings_type}")
async def import_settings(
    settings_type: str = Path(..., description=SETTINGS_TYPE_DESCRIPTION),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """
    استيراد الإعدادات من ملف

    Args:
        settings_type (str): نوع الإعدادات
        file (UploadFile): ملف الإعدادات
        current_user (dict): المستخدم الحالي

    Returns:
        dict: الإعدادات المستوردة
    """
    # التحقق من الصلاحيات
    if not check_permission(current_user, SETTINGS_IMPORT_PERMISSION):
        raise HTTPException(
            status_code=403, detail="ليس لديك صلاحية لاستيراد هذه الإعدادات"
        )

    # التحقق من نوع الإعدادات
    if settings_type not in [
        "general",
        "company",
        "system",
        "connection",
            "all"]:
        raise HTTPException(
            status_code=400, detail=f"نوع إعدادات غير صالح: {settings_type}"
        )

    # التحقق من صلاحيات إضافية لإعدادات الاتصال
    if (
        settings_type == "connection" or settings_type == "all"
    ) and not check_permission(current_user, "settings:import:connection"):
        raise HTTPException(
            status_code=403, detail="ليس لديك صلاحية لاستيراد إعدادات الاتصال"
        )

    temp_file_path = None
    try:
        # حفظ الملف مؤقتاً
        temp_file_path = os.path.join(
            settings_service.config_dir,
            f"temp_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )

        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        # استيراد الإعدادات
        imported_settings = settings_service.import_settings(
            settings_type, temp_file_path
        )

        # إخفاء كلمات المرور وبيانات الاعتماد الحساسة
        if settings_type == "connection":
            imported_settings = _mask_sensitive_data(
                imported_settings, "connection")
        elif settings_type == "all" and "connection" in imported_settings:
            imported_settings["connection"] = _mask_sensitive_data(
                imported_settings["connection"], "connection"
            )

        return imported_settings
    except Exception as e:
        logger.exception(f"Error importing settings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ أثناء استيراد الإعدادات: {str(e)}")
    finally:
        # حذف الملف المؤقت إذا كان موجوداً
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
