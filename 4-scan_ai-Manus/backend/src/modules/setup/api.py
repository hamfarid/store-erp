"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/api.py
الوصف: واجهة برمجة التطبيقات (API) لمديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.modules.activity_log import service as activity_log_service
from src.modules.security import service as security_service
from src.modules.setup import schemas
from src.modules.setup import service as setup_service

router = APIRouter(
    prefix="/api/setup",
    tags=["setup"],
    responses={404: {"description": "Not found"}},
)


@router.get("/status", response_model=schemas.SetupStatusResponse)
async def get_setup_status(db: Session = Depends(get_db)):
    """
    الحصول على حالة الإعداد الحالية

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد الحالية
    """
    try:
        setup_status = setup_service.get_setup_status(db)
        return setup_status
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في الحصول على حالة الإعداد", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الحصول على حالة الإعداد: {str(e)}",
        ) from e


@router.post("/initialize", response_model=schemas.SetupStatusResponse)
async def initialize_setup(db: Session = Depends(get_db)):
    """
    تهيئة عملية الإعداد

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد التهيئة
    """
    try:
        # التحقق من عدم وجود إعداد سابق
        current_status = setup_service.get_setup_status(db)
        if current_status.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="تم إكمال الإعداد بالفعل. لا يمكن إعادة التهيئة.",
            )

        # تهيئة الإعداد
        setup_status = setup_service.initialize_setup(db)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db, "setup", "info", "تم تهيئة عملية الإعداد", {}
        )

        return setup_status
    except HTTPException:
        raise
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في تهيئة عملية الإعداد", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء تهيئة عملية الإعداد: {str(e)}",
        ) from e


@router.get("/step/{step_id}", response_model=schemas.StepDataResponse)
async def get_step_data(step_id: str, db: Session = Depends(get_db)):
    """
    الحصول على بيانات خطوة معينة

    Args:
        step_id (str): معرف الخطوة

    Returns:
        schemas.StepDataResponse: بيانات الخطوة
    """
    try:
        step_data = setup_service.get_step_data(db, step_id)
        if not step_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"الخطوة {step_id} غير موجودة",
            )
        return step_data
    except HTTPException:
        raise
    except Exception as e:
        activity_log_service.log_activity(
            db,
            "setup",
            "error",
            f"فشل في الحصول على بيانات الخطوة {step_id}",
            {"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الحصول على بيانات الخطوة: {str(e)}",
        )


@router.post("/step/{step_id}", response_model=schemas.StepUpdateResponse)
async def update_step_data(step_id: str,
                           step_data: Dict[str,
                                           Any] = Body(...),
                           db: Session = Depends(get_db)):
    """
    تحديث بيانات خطوة معينة

    Args:
        step_id (str): معرف الخطوة
        step_data (Dict[str, Any]): بيانات الخطوة الجديدة

    Returns:
        schemas.StepUpdateResponse: نتيجة تحديث الخطوة
    """
    try:
        # التحقق من صحة البيانات
        validation_result = setup_service.validate_step_data(
            db, step_id, step_data)
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"بيانات غير صالحة: {validation_result.errors}",
            )

        # تحديث بيانات الخطوة
        result = setup_service.update_step_data(db, step_id, step_data)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db,
            "setup",
            "info",
            f"تم تحديث بيانات الخطوة {step_id}",
            {"step_id": step_id},
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        activity_log_service.log_activity(
            db,
            "setup",
            "error",
            f"فشل في تحديث بيانات الخطوة {step_id}",
            {"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء تحديث بيانات الخطوة: {str(e)}",
        )


@router.post("/next-step", response_model=schemas.SetupStatusResponse)
async def next_step(db: Session = Depends(get_db)):
    """
    الانتقال إلى الخطوة التالية

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد الانتقال
    """
    try:
        result = setup_service.next_step(db)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db, "setup", "info", f"تم الانتقال إلى الخطوة {result.current_step}", {})

        return result
    except Exception as e:
        activity_log_service.log_activity(
            db,
            "setup",
            "error",
            "فشل في الانتقال إلى الخطوة التالية",
            {"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الانتقال إلى الخطوة التالية: {str(e)}",
        )


@router.post("/previous-step", response_model=schemas.SetupStatusResponse)
async def previous_step(db: Session = Depends(get_db)):
    """
    العودة إلى الخطوة السابقة

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد العودة
    """
    try:
        result = setup_service.previous_step(db)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db, "setup", "info", f"تم العودة إلى الخطوة {result.current_step}", {})

        return result
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في العودة إلى الخطوة السابقة", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء العودة إلى الخطوة السابقة: {str(e)}",
        )


@router.post("/complete", response_model=schemas.SetupCompletionResponse)
async def complete_setup(db: Session = Depends(get_db)):
    """
    إكمال عملية الإعداد

    Returns:
        schemas.SetupCompletionResponse: نتيجة إكمال الإعداد
    """
    try:
        # التحقق من اكتمال جميع الخطوات الإلزامية
        validation_result = setup_service.validate_setup_completion(db)
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"لا يمكن إكمال الإعداد: {validation_result.errors}",
            )

        # إكمال الإعداد
        result = setup_service.complete_setup(db)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db, "setup", "info", "تم إكمال عملية الإعداد بنجاح", {}
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في إكمال عملية الإعداد", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء إكمال عملية الإعداد: {str(e)}",
        )


@router.post("/test-database-connection",
             response_model=schemas.DatabaseConnectionTestResponse)
async def test_database_connection(
    connection_data: schemas.DatabaseConnectionTest = Body(...),
    db: Session = Depends(get_db),
):
    """
    اختبار اتصال قاعدة البيانات

    Args:
        connection_data (schemas.DatabaseConnectionTest): بيانات الاتصال

    Returns:
        schemas.DatabaseConnectionTestResponse: نتيجة اختبار الاتصال
    """
    try:
        result = setup_service.test_database_connection(connection_data)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db,
            "setup",
            "info",
            "تم اختبار اتصال قاعدة البيانات",
            {"success": result.success},
        )

        return result
    except Exception as e:
        activity_log_service.log_activity(
            db,
            "setup",
            "error",
            "فشل في اختبار اتصال قاعدة البيانات",
            {"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء اختبار اتصال قاعدة البيانات: {str(e)}",
        )


@router.post("/test-email-settings",
             response_model=schemas.EmailSettingsTestResponse)
async def test_email_settings(
        email_settings: schemas.EmailSettingsTest = Body(...),
        db: Session = Depends(get_db)):
    """
    اختبار إعدادات البريد الإلكتروني

    Args:
        email_settings (schemas.EmailSettingsTest): إعدادات البريد الإلكتروني

    Returns:
        schemas.EmailSettingsTestResponse: نتيجة اختبار إعدادات البريد الإلكتروني
    """
    try:
        result = setup_service.test_email_settings(email_settings)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db,
            "setup",
            "info",
            "تم اختبار إعدادات البريد الإلكتروني",
            {"success": result.success},
        )

        return result
    except Exception as e:
        activity_log_service.log_activity(
            db,
            "setup",
            "error",
            "فشل في اختبار إعدادات البريد الإلكتروني",
            {"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء اختبار إعدادات البريد الإلكتروني: {str(e)}",
        )


@router.get("/available-modules", response_model=List[schemas.ModuleInfo])
async def get_available_modules(db: Session = Depends(get_db)):
    """
    الحصول على قائمة المديولات المتاحة

    Returns:
        List[schemas.ModuleInfo]: قائمة المديولات المتاحة
    """
    try:
        modules = setup_service.get_available_modules(db)
        return modules
    except Exception as e:
        activity_log_service.log_activity(
            db,
            "setup",
            "error",
            "فشل في الحصول على قائمة المديولات المتاحة",
            {"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الحصول على قائمة المديولات المتاحة: {str(e)}",
        )


@router.get("/countries", response_model=List[schemas.CountryInfo])
async def get_countries(db: Session = Depends(get_db)):
    """
    الحصول على قائمة الدول

    Returns:
        List[schemas.CountryInfo]: قائمة الدول
    """
    try:
        countries = setup_service.get_countries(db)
        return countries
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في الحصول على قائمة الدول", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الحصول على قائمة الدول: {str(e)}",
        )


@router.get("/currencies", response_model=List[schemas.CurrencyInfo])
async def get_currencies(db: Session = Depends(get_db)):
    """
    الحصول على قائمة العملات

    Returns:
        List[schemas.CurrencyInfo]: قائمة العملات
    """
    try:
        currencies = setup_service.get_currencies(db)
        return currencies
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في الحصول على قائمة العملات", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الحصول على قائمة العملات: {str(e)}",
        )


@router.get("/timezones", response_model=List[schemas.TimezoneInfo])
async def get_timezones(db: Session = Depends(get_db)):
    """
    الحصول على قائمة المناطق الزمنية

    Returns:
        List[schemas.TimezoneInfo]: قائمة المناطق الزمنية
    """
    try:
        timezones = setup_service.get_timezones(db)
        return timezones
    except Exception as e:
        activity_log_service.log_activity(
            db,
            "setup",
            "error",
            "فشل في الحصول على قائمة المناطق الزمنية",
            {"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الحصول على قائمة المناطق الزمنية: {str(e)}",
        )


@router.get("/languages", response_model=List[schemas.LanguageInfo])
async def get_languages(db: Session = Depends(get_db)):
    """
    الحصول على قائمة اللغات

    Returns:
        List[schemas.LanguageInfo]: قائمة اللغات
    """
    try:
        languages = setup_service.get_languages(db)
        return languages
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في الحصول على قائمة اللغات", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الحصول على قائمة اللغات: {str(e)}",
        )


@router.post("/reset", response_model=schemas.SetupStatusResponse)
async def reset_setup(db: Session = Depends(get_db)):
    """
    إعادة تعيين عملية الإعداد

    Returns:
        schemas.SetupStatusResponse: حالة الإعداد بعد إعادة التعيين
    """
    try:
        # التحقق من الصلاحيات (يجب أن يكون المستخدم مسؤولاً)
        # هذا سيتم تنفيذه لاحقاً عندما يكون نظام المصادقة جاهزاً

        # إعادة تعيين الإعداد
        result = setup_service.reset_setup(db)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db, "setup", "warning", "تم إعادة تعيين عملية الإعداد", {}
        )

        return result
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في إعادة تعيين عملية الإعداد", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء إعادة تعيين عملية الإعداد: {str(e)}",
        )


@router.post("/validate-security-settings",
             response_model=schemas.SecurityValidationResponse)
async def validate_security_settings(
    security_settings: schemas.SecuritySettings = Body(...),
    db: Session = Depends(get_db),
):
    """
    التحقق من صحة إعدادات الأمان

    Args:
        security_settings (schemas.SecuritySettings): إعدادات الأمان

    Returns:
        schemas.SecurityValidationResponse: نتيجة التحقق من صحة إعدادات الأمان
    """
    try:
        result = security_service.validate_security_settings(security_settings)

        # تسجيل النشاط
        activity_log_service.log_activity(
            db,
            "setup",
            "info",
            "تم التحقق من صحة إعدادات الأمان",
            {"is_valid": result.is_valid},
        )

        return result
    except Exception as e:
        activity_log_service.log_activity(
            db,
            "setup",
            "error",
            "فشل في التحقق من صحة إعدادات الأمان",
            {"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء التحقق من صحة إعدادات الأمان: {str(e)}",
        )


@router.get("/setup-logs", response_model=List[schemas.SetupLogEntry])
async def get_setup_logs(db: Session = Depends(get_db)):
    """
    الحصول على سجلات الإعداد

    Returns:
        List[schemas.SetupLogEntry]: سجلات الإعداد
    """
    try:
        logs = setup_service.get_setup_logs(db)
        return logs
    except Exception as e:
        activity_log_service.log_activity(
            db, "setup", "error", "فشل في الحصول على سجلات الإعداد", {
                "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ أثناء الحصول على سجلات الإعداد: {str(e)}",
        )
