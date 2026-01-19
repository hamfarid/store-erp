"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/activity_log/error_logger.py
الوصف: وحدة تسجيل الأخطاء في سجل النشاط
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import logging
import traceback
import time
from datetime import datetime
from typing import Dict, Any, Optional

from src.modules.activity_log.service import ActivityLogService
from src.modules.activity_log.models import ActivityLogType, ActivityLogSeverity
from src.modules.security.security_middleware import get_current_user_id

# إعداد المسجل
logger = logging.getLogger(__name__)


class ErrorLogger:
    """
    فئة مسؤولة عن تسجيل الأخطاء في سجل النشاط
    """

    def __init__(self, activity_log_service: ActivityLogService = None):
        """
        تهيئة مسجل الأخطاء

        Args:
            activity_log_service: خدمة سجل النشاط، إذا كانت None سيتم إنشاء مثيل جديد
        """
        self.activity_log_service = activity_log_service or ActivityLogService()

    def log_http_error(
        self,
        error_code: int,
        request_path: str,
        request_method: str,
        user_id: Optional[int] = None,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
        request_data: Optional[Dict[str, Any]] = None,
        error_details: Optional[str] = None,
    ) -> None:
        """
        تسجيل خطأ HTTP في سجل النشاط

        Args:
            error_code: رمز خطأ HTTP (مثل 404، 500، 504)
            request_path: مسار الطلب
            request_method: طريقة الطلب (GET، POST، إلخ)
            user_id: معرف المستخدم (اختياري)
            user_agent: وكيل المستخدم (اختياري)
            ip_address: عنوان IP (اختياري)
            request_data: بيانات الطلب (اختياري)
            error_details: تفاصيل الخطأ (اختياري)
        """
        # تحديد نوع وشدة الخطأ بناءً على رمز الخطأ
        severity = self._get_severity_from_http_code(error_code)

        # إنشاء تفاصيل الخطأ
        details = {
            "error_code": error_code,
            "request_path": request_path,
            "request_method": request_method,
            "timestamp": datetime.now().isoformat(),
            "user_agent": user_agent,
            "ip_address": ip_address,
        }

        # إضافة بيانات الطلب إذا كانت متوفرة
        if request_data:
            # تنظيف البيانات الحساسة قبل التسجيل
            sanitized_data = self._sanitize_sensitive_data(request_data)
            details["request_data"] = sanitized_data

        # إضافة تفاصيل الخطأ إذا كانت متوفرة
        if error_details:
            details["error_details"] = error_details

        # تحديد نوع الخطأ بناءً على رمز الخطأ
        if 400 <= error_code < 500:
            log_type = ActivityLogType.CLIENT_ERROR
            action = f"http_client_error_{error_code}"
        else:
            log_type = ActivityLogType.SERVER_ERROR
            action = f"http_server_error_{error_code}"

        # تسجيل الخطأ في سجل النشاط
        try:
            self.activity_log_service.create_log_entry(
                user_id=user_id,
                action=action,
                target_type="http_request",
                target_id=str(int(time.time())),  # استخدام الطابع الزمني كمعرف فريد
                details=details,
                log_type=log_type,
                severity=severity,
            )
        except Exception as e:
            # تسجيل الخطأ في السجل المحلي إذا فشل التسجيل في سجل النشاط
            logger.error("Failed to log HTTP error to activity log: %s", str(e))
            logger.error(traceback.format_exc())

    def log_application_error(
        self,
        error: Exception,
        module_name: str,
        function_name: str,
        user_id: Optional[int] = None,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        تسجيل خطأ تطبيق في سجل النشاط

        Args:
            error: كائن الاستثناء
            module_name: اسم الوحدة التي حدث فيها الخطأ
            function_name: اسم الدالة التي حدث فيها الخطأ
            user_id: معرف المستخدم (اختياري)
            additional_context: سياق إضافي للخطأ (اختياري)
        """
        # إنشاء تفاصيل الخطأ
        details = {
            "error_type": error.__class__.__name__,
            "error_message": str(error),
            "module_name": module_name,
            "function_name": function_name,
            "timestamp": datetime.now().isoformat(),
            "traceback": traceback.format_exc(),
        }

        # إضافة سياق إضافي إذا كان متوفراً
        if additional_context:
            # تنظيف البيانات الحساسة قبل التسجيل
            sanitized_context = self._sanitize_sensitive_data(additional_context)
            details["context"] = sanitized_context

        # تسجيل الخطأ في سجل النشاط
        try:
            self.activity_log_service.create_log_entry(
                user_id=user_id,
                action="application_error",
                target_type="application",
                target_id=module_name,
                details=details,
                log_type=ActivityLogType.APPLICATION_ERROR,
                severity=ActivityLogSeverity.ERROR,
            )
        except Exception as e:
            # تسجيل الخطأ في السجل المحلي إذا فشل التسجيل في سجل النشاط
            logger.error("Failed to log application error to activity log: %s", str(e))
            logger.error(traceback.format_exc())

    def log_security_error(
        self,
        error_type: str,
        description: str,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        request_path: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        تسجيل خطأ أمني في سجل النشاط

        Args:
            error_type: نوع الخطأ الأمني (مثل "sql_injection_attempt", "xss_attempt", "csrf_failure")
            description: وصف الخطأ
            user_id: معرف المستخدم (اختياري)
            ip_address: عنوان IP (اختياري)
            request_path: مسار الطلب (اختياري)
            additional_data: بيانات إضافية (اختياري)
        """
        # إنشاء تفاصيل الخطأ
        details = {
            "error_type": error_type,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "ip_address": ip_address,
            "request_path": request_path,
        }

        # إضافة بيانات إضافية إذا كانت متوفرة
        if additional_data:
            # تنظيف البيانات الحساسة قبل التسجيل
            sanitized_data = self._sanitize_sensitive_data(additional_data)
            details["additional_data"] = sanitized_data

        # تسجيل الخطأ في سجل النشاط
        try:
            self.activity_log_service.create_log_entry(
                user_id=user_id,
                action=f"security_error_{error_type}",
                target_type="security",
                target_id=error_type,
                details=details,
                log_type=ActivityLogType.SECURITY_ERROR,
                severity=ActivityLogSeverity.CRITICAL,
            )
        except Exception as e:
            # تسجيل الخطأ في السجل المحلي إذا فشل التسجيل في سجل النشاط
            logger.error("Failed to log security error to activity log: %s", str(e))
            logger.error(traceback.format_exc())

    def _get_severity_from_http_code(self, error_code: int) -> ActivityLogSeverity:
        """
        تحديد شدة الخطأ بناءً على رمز خطأ HTTP

        Args:
            error_code: رمز خطأ HTTP

        Returns:
            شدة الخطأ
        """
        if error_code == 404:
            return ActivityLogSeverity.INFO
        elif 400 <= error_code < 500:
            return ActivityLogSeverity.WARNING
        elif error_code == 500:
            return ActivityLogSeverity.ERROR
        elif error_code == 504:
            return ActivityLogSeverity.WARNING
        else:
            return ActivityLogSeverity.ERROR

    def _sanitize_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تنظيف البيانات الحساسة قبل التسجيل

        Args:
            data: البيانات المراد تنظيفها

        Returns:
            البيانات بعد التنظيف
        """
        # إنشاء نسخة من البيانات
        sanitized = data.copy()

        # قائمة بالحقول الحساسة التي يجب إخفاؤها
        sensitive_fields = [
            "password",
            "token",
            "secret",
            "key",
            "auth",
            "credential",
            "credit_card",
            "card_number",
            "cvv",
            "ssn",
            "social_security",
            "كلمة_المرور",
            "رمز",
            "سر",
            "مفتاح",
            "بطاقة_ائتمان",
            "رقم_بطاقة",
        ]

        # تنظيف البيانات بشكل متكرر
        def _sanitize_recursive(obj):
            if isinstance(obj, dict):
                result = {}
                for k, v in obj.items():
                    # التحقق مما إذا كان الحقل حساساً
                    is_sensitive = any(
                        field.lower() in k.lower() for field in sensitive_fields
                    )
                    if is_sensitive:
                        result[k] = "***REDACTED***"
                    else:
                        result[k] = _sanitize_recursive(v)
                return result
            elif isinstance(obj, list):
                return [_sanitize_recursive(item) for item in obj]
            else:
                return obj

        return _sanitize_recursive(sanitized)


# دالة مساعدة للحصول على مثيل مسجل الأخطاء
_error_logger_instance = None


def get_error_logger() -> ErrorLogger:
    """
    الحصول على مثيل مسجل الأخطاء

    Returns:
        مثيل مسجل الأخطاء
    """
    global _error_logger_instance  # pylint: disable=global-statement
    if _error_logger_instance is None:
        _error_logger_instance = ErrorLogger()
    return _error_logger_instance


# مزخرفات لتسهيل تسجيل الأخطاء


def log_errors(module_name: str = None):
    """
    مزخرف لتسجيل الأخطاء في الدوال

    Args:
        module_name: اسم الوحدة، إذا كان None سيتم استخدام اسم الوحدة الحالية

    Returns:
        مزخرف الدالة
    """

    def decorator(func):
        # استخدام اسم الوحدة من الدالة إذا لم يتم تحديده
        nonlocal module_name
        if module_name is None:
            module_name = func.__module__

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # الحصول على معرف المستخدم الحالي إذا كان متاحاً
                user_id = None
                try:
                    user_id = get_current_user_id()
                except Exception:
                    pass

                # تسجيل الخطأ
                error_logger = get_error_logger()
                error_logger.log_application_error(
                    error=e,
                    module_name=module_name,
                    function_name=func.__name__,
                    user_id=user_id,
                    additional_context={"args": str(args), "kwargs": str(kwargs)},
                )

                # إعادة رفع الاستثناء
                raise

        return wrapper

    return decorator
