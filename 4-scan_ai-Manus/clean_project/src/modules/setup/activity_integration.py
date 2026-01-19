"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/setup/activity_integration.py
الوصف: تكامل سجل النشاط مع مديول الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.modules.activity_log import service as activity_log_service
from src.modules.activity_log.models import ActivityLog
from src.modules.setup import models

# إعداد التسجيل
logger = logging.getLogger(__name__)

# تعريف أنواع الأحداث
SETUP_EVENT_TYPES = {
    # أحداث التهيئة
    "initialize": "تهيئة معالج الإعداد",
    "reset": "إعادة تعيين معالج الإعداد",

    # أحداث التنقل
    "next_step": "الانتقال إلى الخطوة التالية",
    "previous_step": "العودة إلى الخطوة السابقة",
    "navigate_to_step": "الانتقال إلى خطوة محددة",

    # أحداث البيانات
    "get_step_data": "الحصول على بيانات الخطوة",
    "validate_step_data": "التحقق من صحة بيانات الخطوة",
    "update_step_data": "تحديث بيانات الخطوة",
    "update_step_data_error": "خطأ في تحديث بيانات الخطوة",

    # أحداث الإكمال
    "validate_setup_completion": "التحقق من اكتمال الإعداد",
    "complete_setup": "إكمال عملية الإعداد",
    "complete_setup_error": "خطأ في إكمال عملية الإعداد",

    # أحداث الأمان
    "security_check": "فحص الأمان",
    "security_warning": "تحذير أمني",
    "security_error": "خطأ أمني",
    "ssl_config": "تكوين SSL",
    "ssl_config_error": "خطأ في تكوين SSL",
    "login_attempt": "محاولة تسجيل دخول",
    "login_success": "نجاح تسجيل الدخول",
    "login_failure": "فشل تسجيل الدخول",
    "token_validation": "التحقق من صحة الرمز",
    "token_validation_error": "خطأ في التحقق من صحة الرمز",
    "ip_blocked": "حظر عنوان IP",
    "rate_limit_exceeded": "تجاوز معدل الطلبات",

    # أحداث النظام
    "system_settings_update": "تحديث إعدادات النظام",
    "database_settings_update": "تحديث إعدادات قاعدة البيانات",
    "company_settings_update": "تحديث إعدادات الشركة",
    "branch_settings_update": "تحديث إعدادات الفروع",
    "user_settings_update": "تحديث إعدادات المستخدمين",
    "module_settings_update": "تحديث إعدادات المديولات",
    "ai_settings_update": "تحديث إعدادات الذكاء الاصطناعي",
    "notification_settings_update": "تحديث إعدادات الإشعارات",
    "security_settings_update": "تحديث إعدادات الأمان",
    "backup_settings_update": "تحديث إعدادات النسخ الاحتياطي",

    # أحداث الخطأ
    "error": "خطأ عام",
    "validation_error": "خطأ في التحقق",
    "database_error": "خطأ في قاعدة البيانات",
    "api_error": "خطأ في واجهة برمجة التطبيقات",
    "network_error": "خطأ في الشبكة",
    "permission_error": "خطأ في الصلاحيات",

    # أحداث الطلبات
    "setup_request": "طلب إعداد",
    "setup_response": "استجابة إعداد",
    "setup_error": "خطأ في طلب الإعداد"
}


def log_setup_activity(
    db: Session,
    event_type: str,
    description: str,
    data: Dict[str, Any],
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    status: str = "info"
) -> ActivityLog:
    """
    تسجيل نشاط الإعداد في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        event_type (str): نوع الحدث
        description (str): وصف الحدث
        data (Dict[str, Any]): بيانات الحدث
        user_id (Optional[int]): معرف المستخدم
        ip_address (Optional[str]): عنوان IP
        status (str): حالة الحدث (info, warning, error, success)

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد نوع الحدث المعروض
    display_event_type = SETUP_EVENT_TYPES.get(event_type, event_type)

    # تسجيل النشاط
    activity_log = activity_log_service.log_activity(
        db=db,
        log_type="setup",
        module_id="setup",
        action_id=event_type,
        description=description,
        user_id=user_id,
        details=data,
        ip_address=ip_address,
        status=status
    )

    # تسجيل في سجل الإعداد
    setup_log = models.SetupLog(
        step=data.get("step_id", data.get("current_step", "general")),
        status=status,
        message=description,
        details=data,
        user_id=user_id,
        ip_address=ip_address,
        activity_log_id=activity_log.id
    )

    # إضافة سجل الإعداد إلى قاعدة البيانات
    db.add(setup_log)
    db.commit()

    # تسجيل في سجل التطبيق
    log_level = logging.INFO
    if status == "warning":
        log_level = logging.WARNING
    elif status == "error":
        log_level = logging.ERROR

    logger.log(log_level, "[%s] %s", display_event_type, description)

    return activity_log


def log_security_event(
    db: Session,
    event_type: str,
    description: str,
    data: Dict[str, Any],
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> ActivityLog:
    """
    تسجيل حدث أمني في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        event_type (str): نوع الحدث
        description (str): وصف الحدث
        data (Dict[str, Any]): بيانات الحدث
        user_id (Optional[int]): معرف المستخدم
        ip_address (Optional[str]): عنوان IP

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد حالة الحدث
    status = "warning"
    if event_type.endswith("_error"):
        status = "error"
    elif event_type.endswith("_success"):
        status = "success"

    # تسجيل الحدث
    return log_setup_activity(
        db=db,
        event_type=event_type,
        description=description,
        data=data,
        user_id=user_id,
        ip_address=ip_address,
        status=status
    )


def log_step_navigation(
    db: Session,
    event_type: str,
    current_step: str,
    previous_step: Optional[str] = None,
    next_step: Optional[str] = None,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> ActivityLog:
    """
    تسجيل التنقل بين الخطوات في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        event_type (str): نوع الحدث
        current_step (str): الخطوة الحالية
        previous_step (Optional[str]): الخطوة السابقة
        next_step (Optional[str]): الخطوة التالية
        user_id (Optional[int]): معرف المستخدم
        ip_address (Optional[str]): عنوان IP

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد البيانات
    data = {
        "current_step": current_step,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    if previous_step:
        data["previous_step"] = previous_step

    if next_step:
        data["next_step"] = next_step

    # تحديد الوصف
    if event_type == "next_step":
        description = f"الانتقال إلى الخطوة التالية: {next_step}"
    elif event_type == "previous_step":
        description = f"العودة إلى الخطوة السابقة: {previous_step}"
    elif event_type == "navigate_to_step":
        description = f"الانتقال إلى الخطوة: {current_step}"
    else:
        description = f"تنقل بين الخطوات: {current_step}"

    # تسجيل النشاط
    return log_setup_activity(
        db=db,
        event_type=event_type,
        description=description,
        data=data,
        user_id=user_id,
        ip_address=ip_address,
        status="info"
    )


def log_step_data_operation(
    db: Session,
    event_type: str,
    step_id: str,
    operation_result: bool,
    message: str,
    data: Optional[Dict[str, Any]] = None,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> ActivityLog:
    """
    تسجيل عملية على بيانات الخطوة في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        event_type (str): نوع الحدث
        step_id (str): معرف الخطوة
        operation_result (bool): نتيجة العملية
        message (str): رسالة العملية
        data (Optional[Dict[str, Any]]): بيانات إضافية
        user_id (Optional[int]): معرف المستخدم
        ip_address (Optional[str]): عنوان IP

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد البيانات
    operation_data = {
        "step_id": step_id,
        "operation_result": operation_result,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    if data:
        # تنظيف البيانات الحساسة
        sanitized_data = sanitize_sensitive_data(data)
        operation_data["operation_data"] = sanitized_data

    # تحديد الحالة
    operation_status = "success" if operation_result else "error"

    # تسجيل النشاط
    return log_setup_activity(
        db=db,
        event_type=event_type,
        description=message,
        data=operation_data,
        user_id=user_id,
        ip_address=ip_address,
        status=operation_status
    )


def log_setup_completion(
    db: Session,
    success: bool,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> ActivityLog:
    """
    تسجيل إكمال عملية الإعداد في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        success (bool): نجاح العملية
        message (str): رسالة الإكمال
        details (Optional[Dict[str, Any]]): تفاصيل إضافية
        user_id (Optional[int]): معرف المستخدم
        ip_address (Optional[str]): عنوان IP

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد نوع الحدث
    event_type = "complete_setup" if success else "complete_setup_error"

    # تحديد البيانات
    completion_data = {
        "success": success,
        "completion_time": datetime.now(timezone.utc).isoformat()
    }

    if details:
        # تنظيف البيانات الحساسة
        sanitized_details = sanitize_sensitive_data(details)
        completion_data["details"] = sanitized_details

    # تحديد الحالة
    completion_status = "success" if success else "error"

    # تسجيل النشاط
    try:
        activity_log = log_setup_activity(
            db=db,
            event_type=event_type,
            description=message,
            data=completion_data,
            user_id=user_id,
            ip_address=ip_address,
            status=completion_status
        )

        return activity_log
    except Exception as e:
        logger.error("خطأ في تسجيل إكمال الإعداد: %s", str(e))
        raise


def log_security_check(
    db: Session,
    check_type: str,
    success: bool,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> ActivityLog:
    """
    تسجيل فحص أمني في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        check_type (str): نوع الفحص الأمني
        success (bool): نجاح الفحص
        message (str): رسالة الفحص
        details (Optional[Dict[str, Any]]): تفاصيل إضافية
        user_id (Optional[int]): معرف المستخدم
        ip_address (Optional[str]): عنوان IP

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد نوع الحدث
    if success:
        event_type = "security_check"
    else:
        event_type = "security_error"

    # تحديد البيانات
    security_data = {
        "check_type": check_type,
        "success": success,
        "check_time": datetime.now(timezone.utc).isoformat()
    }

    if details:
        # تنظيف البيانات الحساسة
        sanitized_details = sanitize_sensitive_data(details)
        security_data["details"] = sanitized_details

    # تحديد الحالة
    security_status = "success" if success else "error"

    # تسجيل النشاط
    try:
        activity_log = log_setup_activity(
            db=db,
            event_type=event_type,
            description=message,
            data=security_data,
            user_id=user_id,
            ip_address=ip_address,
            status=security_status
        )

        return activity_log
    except Exception as e:
        logger.error("خطأ في تسجيل الفحص الأمني: %s", str(e))
        raise


def log_login_attempt(
    db: Session,
    username: str,
    success: bool,
    ip_address: str,
    user_agent: Optional[str] = None,
    error_message: Optional[str] = None
) -> ActivityLog:
    """
    تسجيل محاولة تسجيل دخول في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        username (str): اسم المستخدم
        success (bool): نجاح محاولة تسجيل الدخول
        ip_address (str): عنوان IP
        user_agent (Optional[str]): وكيل المستخدم
        error_message (Optional[str]): رسالة الخطأ

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد نوع الحدث
    event_type = "login_success" if success else "login_failure"

    # تحديد البيانات
    login_data = {
        "username": username,
        "success": success,
        "ip_address": ip_address,
        "attempt_time": datetime.now(timezone.utc).isoformat()
    }

    if user_agent:
        login_data["user_agent"] = user_agent

    if error_message:
        login_data["error_message"] = error_message

    # تحديد الوصف
    if success:
        description = f"نجح تسجيل الدخول للمستخدم: {username}"
    else:
        description = f"فشل تسجيل الدخول للمستخدم: {username}"

    # تحديد الحالة
    login_status = "success" if success else "error"

    # تسجيل النشاط
    try:
        activity_log = log_setup_activity(
            db=db,
            event_type=event_type,
            description=description,
            data=login_data,
            user_id=None,
            ip_address=ip_address,
            status=login_status
        )

        return activity_log
    except Exception as e:
        logger.error("خطأ في تسجيل محاولة تسجيل الدخول: %s", str(e))
        raise


def log_ip_blocked(
    db: Session,
    ip_address: str,
    reason: str,
    duration: int,
    details: Optional[Dict[str, Any]] = None
) -> ActivityLog:
    """
    تسجيل حظر عنوان IP في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        ip_address (str): عنوان IP المحظور
        reason (str): سبب الحظر
        duration (int): مدة الحظر بالدقائق
        details (Optional[Dict[str, Any]]): تفاصيل إضافية

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد البيانات
    block_data = {
        "ip_address": ip_address,
        "reason": reason,
        "duration_minutes": duration,
        "block_time": datetime.now(timezone.utc).isoformat()
    }

    if details:
        # تنظيف البيانات الحساسة
        sanitized_details = sanitize_sensitive_data(details)
        block_data["details"] = sanitized_details

    # تحديد الوصف
    description = f"تم حظر عنوان IP {ip_address} لمدة {duration} دقيقة بسبب: {reason}"

    # تسجيل النشاط
    try:
        activity_log = log_setup_activity(
            db=db,
            event_type="ip_blocked",
            description=description,
            data=block_data,
            user_id=None,
            ip_address=ip_address,
            status="warning"
        )

        return activity_log
    except Exception as e:
        logger.error("خطأ في تسجيل حظر عنوان IP: %s", str(e))
        raise


def log_rate_limit_exceeded(
    db: Session,
    ip_address: str,
    request_count: int,
    max_requests: int,
    time_window: int
) -> ActivityLog:
    """
    تسجيل تجاوز معدل الطلبات في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        ip_address (str): عنوان IP
        request_count (int): عدد الطلبات
        max_requests (int): الحد الأقصى للطلبات
        time_window (int): نافذة الوقت بالثواني

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد البيانات
    rate_limit_data = {
        "ip_address": ip_address,
        "request_count": request_count,
        "max_requests": max_requests,
        "time_window_seconds": time_window,
        "exceeded_time": datetime.now(timezone.utc).isoformat()
    }

    # تحديد الوصف
    description = f"تجاوز عنوان IP {ip_address} معدل الطلبات المسموح: {request_count}/{max_requests} في {time_window} ثانية"

    # تسجيل النشاط
    try:
        activity_log = log_setup_activity(
            db=db,
            event_type="rate_limit_exceeded",
            description=description,
            data=rate_limit_data,
            user_id=None,
            ip_address=ip_address,
            status="warning"
        )

        return activity_log
    except Exception as e:
        logger.error("خطأ في تسجيل تجاوز معدل الطلبات: %s", str(e))
        raise


def log_settings_update(
    db: Session,
    settings_type: str,
    success: bool,
    message: str,
    settings: Dict[str, Any],
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> ActivityLog:
    """
    تسجيل تحديث الإعدادات في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        settings_type (str): نوع الإعدادات
        success (bool): نجاح التحديث
        message (str): رسالة التحديث
        settings (Dict[str, Any]): الإعدادات المحدثة
        user_id (Optional[int]): معرف المستخدم
        ip_address (Optional[str]): عنوان IP

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد نوع الحدث
    event_type = f"{settings_type}_settings_update"

    # تحديد البيانات
    settings_data = {
        "settings_type": settings_type,
        "success": success,
        "update_time": datetime.now(timezone.utc).isoformat(),
        "settings": sanitize_sensitive_data(settings)
    }

    # تحديد الحالة
    settings_status = "success" if success else "error"

    # تسجيل النشاط
    try:
        activity_log = log_setup_activity(
            db=db,
            event_type=event_type,
            description=message,
            data=settings_data,
            user_id=user_id,
            ip_address=ip_address,
            status=settings_status
        )

        return activity_log
    except Exception as e:
        logger.error("خطأ في تسجيل تحديث الإعدادات: %s", str(e))
        raise


def log_api_request(
    db: Session,
    method: str,
    url: str,
    status_code: int,
    client_ip: str,
    user_agent: Optional[str] = None,
    user_id: Optional[int] = None,
    request_data: Optional[Dict[str, Any]] = None,
    response_data: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None
) -> ActivityLog:
    """
    تسجيل طلب API في سجل النشاط

    Args:
        db (Session): جلسة قاعدة البيانات
        method (str): طريقة الطلب
        url (str): عنوان URL
        status_code (int): رمز الحالة
        client_ip (str): عنوان IP للعميل
        user_agent (Optional[str]): وكيل المستخدم
        user_id (Optional[int]): معرف المستخدم
        request_data (Optional[Dict[str, Any]]): بيانات الطلب
        response_data (Optional[Dict[str, Any]]): بيانات الاستجابة
        error_message (Optional[str]): رسالة الخطأ

    Returns:
        ActivityLog: سجل النشاط
    """
    # تحديد نوع الحدث
    event_type = "setup_request"
    if status_code >= 400:
        event_type = "setup_error"

    # تحديد وصف الحدث
    description = f"طلب {method} إلى {url} (الحالة: {status_code})"
    if error_message:
        description += f": {error_message}"

    # تحديد بيانات الحدث
    data = {
        "method": method,
        "url": url,
        "status_code": status_code,
        "client_ip": client_ip
    }

    if user_agent:
        data["user_agent"] = user_agent

    if request_data:
        # إزالة البيانات الحساسة
        sanitized_request_data = sanitize_sensitive_data(request_data)
        data["request_data"] = sanitized_request_data

    if response_data:
        # إزالة البيانات الحساسة
        sanitized_response_data = sanitize_sensitive_data(response_data)
        data["response_data"] = sanitized_response_data

    if error_message:
        data["error_message"] = error_message

    # تحديد حالة الحدث
    status = "error" if status_code >= 400 else "info"

    # تسجيل الحدث
    return log_setup_activity(
        db=db,
        event_type=event_type,
        description=description,
        data=data,
        user_id=user_id,
        ip_address=client_ip,
        status=status
    )


def sanitize_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    إزالة البيانات الحساسة من القاموس

    Args:
        data (Dict[str, Any]): البيانات

    Returns:
        Dict[str, Any]: البيانات بعد إزالة البيانات الحساسة
    """
    # نسخ البيانات
    sanitized_data = {}

    # قائمة المفاتيح الحساسة
    sensitive_keys = [
        "password", "token", "secret", "key", "api_key", "auth", "credential",
        "cert", "certificate", "private", "ssl_key", "smtp_password"
    ]

    # إزالة البيانات الحساسة
    for key, value in data.items():
        # التحقق من وجود المفتاح في قائمة المفاتيح الحساسة
        is_sensitive = any(sensitive_key in key.lower() for sensitive_key in sensitive_keys)

        if is_sensitive and isinstance(value, str) and value:
            # استبدال القيمة بنص مشفر
            sanitized_data[key] = "********"
        elif isinstance(value, dict):
            # تنظيف القاموس بشكل متكرر
            sanitized_data[key] = sanitize_sensitive_data(value)
        elif isinstance(value, list):
            # تنظيف القائمة بشكل متكرر
            sanitized_data[key] = [
                sanitize_sensitive_data(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            # نسخ القيمة كما هي
            sanitized_data[key] = value

    return sanitized_data


def get_setup_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    step: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> List[models.SetupLog]:
    """
    الحصول على سجلات الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
        skip (int): عدد السجلات للتخطي
        limit (int): عدد السجلات للإرجاع
        step (Optional[str]): الخطوة
        status (Optional[str]): الحالة
        start_date (Optional[datetime]): تاريخ البداية
        end_date (Optional[datetime]): تاريخ النهاية
        user_id (Optional[int]): معرف المستخدم
        ip_address (Optional[str]): عنوان IP

    Returns:
        List[models.SetupLog]: سجلات الإعداد
    """
    # إنشاء استعلام
    query = db.query(models.SetupLog)

    # تطبيق المرشحات
    if step:
        query = query.filter(models.SetupLog.step == step)

    if status:
        query = query.filter(models.SetupLog.status == status)

    if start_date:
        query = query.filter(models.SetupLog.created_at >= start_date)

    if end_date:
        query = query.filter(models.SetupLog.created_at <= end_date)

    if user_id:
        query = query.filter(models.SetupLog.user_id == user_id)

    if ip_address:
        query = query.filter(models.SetupLog.ip_address == ip_address)

    # ترتيب النتائج
    query = query.order_by(models.SetupLog.created_at.desc())

    # تطبيق التخطي والحد
    query = query.offset(skip).limit(limit)

    # إرجاع النتائج
    return query.all()


def get_setup_security_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    event_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    ip_address: Optional[str] = None
) -> List[ActivityLog]:
    """
    الحصول على سجلات الأمان للإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
        skip (int): عدد السجلات للتخطي
        limit (int): عدد السجلات للإرجاع
        event_type (Optional[str]): نوع الحدث
        start_date (Optional[datetime]): تاريخ البداية
        end_date (Optional[datetime]): تاريخ النهاية
        ip_address (Optional[str]): عنوان IP

    Returns:
        List[ActivityLog]: سجلات الأمان
    """
    # قائمة أنواع أحداث الأمان
    security_event_types = [
        "security_check", "security_warning", "security_error",
        "ssl_config", "ssl_config_error", "login_attempt",
        "login_success", "login_failure", "token_validation",
        "token_validation_error", "ip_blocked", "rate_limit_exceeded"
    ]

    # إنشاء استعلام
    query = db.query(ActivityLog).filter(
        ActivityLog.module == "setup",
        ActivityLog.action_type.in_(security_event_types)
    )

    # تطبيق المرشحات
    if event_type:
        query = query.filter(ActivityLog.action_type == event_type)

    if start_date:
        query = query.filter(ActivityLog.created_at >= start_date)

    if end_date:
        query = query.filter(ActivityLog.created_at <= end_date)

    if ip_address:
        query = query.filter(ActivityLog.ip_address == ip_address)

    # ترتيب النتائج
    query = query.order_by(ActivityLog.created_at.desc())

    # تطبيق التخطي والحد
    query = query.offset(skip).limit(limit)

    # إرجاع النتائج
    return query.all()


def get_setup_activity_summary(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    الحصول على ملخص نشاط الإعداد

    Args:
        db (Session): جلسة قاعدة البيانات
        start_date (Optional[datetime]): تاريخ البداية
        end_date (Optional[datetime]): تاريخ النهاية

    Returns:
        Dict[str, Any]: ملخص النشاط
    """
    # إنشاء استعلام
    query = db.query(models.SetupLog)

    # تطبيق المرشحات
    if start_date:
        query = query.filter(models.SetupLog.created_at >= start_date)

    if end_date:
        query = query.filter(models.SetupLog.created_at <= end_date)

    # الحصول على جميع السجلات
    logs = query.all()

    # إنشاء ملخص
    summary = {
        "total_logs": len(logs),
        "status_counts": {
            "info": 0,
            "warning": 0,
            "error": 0,
            "success": 0
        },
        "step_counts": {},
        "user_counts": {},
        "ip_counts": {},
        "hourly_distribution": {hour: 0 for hour in range(24)},
        "daily_distribution": {day: 0 for day in range(7)}
    }

    # حساب الإحصائيات
    for log in logs:
        # حساب عدد السجلات حسب الحالة
        summary["status_counts"][log.status] = summary["status_counts"].get(log.status, 0) + 1

        # حساب عدد السجلات حسب الخطوة
        summary["step_counts"][log.step] = summary["step_counts"].get(log.step, 0) + 1

        # حساب عدد السجلات حسب المستخدم
        if log.user_id:
            summary["user_counts"][log.user_id] = summary["user_counts"].get(log.user_id, 0) + 1

        # حساب عدد السجلات حسب عنوان IP
        if log.ip_address:
            summary["ip_counts"][log.ip_address] = summary["ip_counts"].get(log.ip_address, 0) + 1

        # حساب توزيع السجلات حسب الساعة
        hour = log.created_at.hour
        summary["hourly_distribution"][hour] = summary["hourly_distribution"].get(hour, 0) + 1

        # حساب توزيع السجلات حسب اليوم
        day = log.created_at.weekday()
        summary["daily_distribution"][day] = summary["daily_distribution"].get(day, 0) + 1

    return summary
