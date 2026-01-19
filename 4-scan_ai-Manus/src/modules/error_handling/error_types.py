"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/error_handling/error_types.py
الوصف: تعريف أنواع وشدة الأخطاء في النظام
المؤلف: فريق Scan AI
تاريخ الإنشاء: 30 مايو 2025
"""

from enum import Enum, auto
from typing import Dict, List, Optional, Any


class ErrorType(Enum):
    """
    تعداد لأنواع الأخطاء المختلفة في النظام
    """
    HTTP_ERROR = auto()           # أخطاء HTTP
    APPLICATION_ERROR = auto()    # أخطاء التطبيق
    SECURITY_ERROR = auto()       # أخطاء الأمان
    DATABASE_ERROR = auto()       # أخطاء قاعدة البيانات
    VALIDATION_ERROR = auto()     # أخطاء التحقق من الصحة
    AUTHENTICATION_ERROR = auto()  # أخطاء المصادقة
    AUTHORIZATION_ERROR = auto()  # أخطاء التفويض
    INTEGRATION_ERROR = auto()    # أخطاء التكامل مع أنظمة خارجية
    AI_ERROR = auto()             # أخطاء الذكاء الاصطناعي
    MEMORY_ERROR = auto()         # أخطاء الذاكرة
    RESOURCE_ERROR = auto()       # أخطاء الموارد
    CONFIGURATION_ERROR = auto()  # أخطاء التكوين
    NETWORK_ERROR = auto()        # أخطاء الشبكة
    UNKNOWN_ERROR = auto()        # أخطاء غير معروفة


class ErrorSeverity(Enum):
    """
    تعداد لشدة الأخطاء المختلفة في النظام
    """
    DEBUG = auto()       # معلومات تصحيح الأخطاء
    INFO = auto()        # معلومات
    WARNING = auto()     # تحذير
    ERROR = auto()       # خطأ
    CRITICAL = auto()    # خطأ حرج
    FATAL = auto()       # خطأ قاتل


class ErrorData:
    """
    فئة لتمثيل بيانات الخطأ
    """

    def __init__(
        self,
        error_type: ErrorType,
        severity: ErrorSeverity,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None,
        user_id: Optional[int] = None,
        module_name: Optional[str] = None,
        function_name: Optional[str] = None,
        stack_trace: Optional[str] = None,
        http_status_code: Optional[int] = None,
        request_data: Optional[Dict[str, Any]] = None,
        response_data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None,
        related_errors: Optional[List['ErrorData']] = None
    ):
        """
        تهيئة بيانات الخطأ

        Args:
            error_type: نوع الخطأ
            severity: شدة الخطأ
            message: رسالة الخطأ
            code: رمز الخطأ (اختياري)
            details: تفاصيل إضافية للخطأ (اختياري)
            exception: كائن الاستثناء (اختياري)
            user_id: معرف المستخدم (اختياري)
            module_name: اسم الوحدة التي حدث فيها الخطأ (اختياري)
            function_name: اسم الدالة التي حدث فيها الخطأ (اختياري)
            stack_trace: تتبع المكدس (اختياري)
            http_status_code: رمز حالة HTTP (اختياري)
            request_data: بيانات الطلب (اختياري)
            response_data: بيانات الاستجابة (اختياري)
            timestamp: الطابع الزمني (اختياري)
            related_errors: قائمة بالأخطاء ذات الصلة (اختياري)
        """
        self.error_type = error_type
        self.severity = severity
        self.message = message
        self.code = code
        self.details = details or {}
        self.exception = exception
        self.user_id = user_id
        self.module_name = module_name
        self.function_name = function_name
        self.stack_trace = stack_trace
        self.http_status_code = http_status_code
        self.request_data = request_data
        self.response_data = response_data
        self.timestamp = timestamp
        self.related_errors = related_errors or []

    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل بيانات الخطأ إلى قاموس

        Returns:
            قاموس يمثل بيانات الخطأ
        """
        result = {
            "error_type": self.error_type.name,
            "severity": self.severity.name,
            "message": self.message
        }

        # إضافة الحقول الاختيارية إذا كانت متوفرة
        if self.code:
            result["code"] = self.code

        if self.details:
            result["details"] = self.details

        if self.user_id:
            result["user_id"] = self.user_id

        if self.module_name:
            result["module_name"] = self.module_name

        if self.function_name:
            result["function_name"] = self.function_name

        if self.stack_trace:
            result["stack_trace"] = self.stack_trace

        if self.http_status_code:
            result["http_status_code"] = self.http_status_code

        if self.timestamp:
            result["timestamp"] = self.timestamp

        if self.related_errors:
            result["related_errors"] = [error.to_dict() for error in self.related_errors]

        return result

    def to_user_friendly_dict(self) -> Dict[str, Any]:
        """
        تحويل بيانات الخطأ إلى قاموس صديق للمستخدم (يخفي التفاصيل الفنية)

        Returns:
            قاموس يمثل بيانات الخطأ بشكل صديق للمستخدم
        """
        result = {
            "message": self.message
        }

        # إضافة رمز الخطأ إذا كان متوفراً
        if self.code:
            result["code"] = self.code

        # إضافة رمز حالة HTTP إذا كان متوفراً
        if self.http_status_code:
            result["status"] = self.http_status_code

        # إضافة تفاصيل صديقة للمستخدم إذا كانت متوفرة
        if self.details and "user_friendly_details" in self.details:
            result["details"] = self.details["user_friendly_details"]

        return result

    @classmethod
    def from_exception(
        cls,
        exception: Exception,
        error_type: ErrorType = ErrorType.APPLICATION_ERROR,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        module_name: Optional[str] = None,
        function_name: Optional[str] = None,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> 'ErrorData':
        """
        إنشاء كائن ErrorData من استثناء

        Args:
            exception: كائن الاستثناء
            error_type: نوع الخطأ (اختياري، الافتراضي هو APPLICATION_ERROR)
            severity: شدة الخطأ (اختياري، الافتراضي هو ERROR)
            module_name: اسم الوحدة (اختياري)
            function_name: اسم الدالة (اختياري)
            user_id: معرف المستخدم (اختياري)
            details: تفاصيل إضافية (اختياري)

        Returns:
            كائن ErrorData
        """
        import traceback
        from datetime import datetime

        # الحصول على تتبع المكدس
        stack_trace = traceback.format_exc()

        # إنشاء كائن ErrorData
        return cls(
            error_type=error_type,
            severity=severity,
            message=str(exception),
            exception=exception,
            user_id=user_id,
            module_name=module_name,
            function_name=function_name,
            stack_trace=stack_trace,
            details=details,
            timestamp=datetime.now().isoformat()
        )
