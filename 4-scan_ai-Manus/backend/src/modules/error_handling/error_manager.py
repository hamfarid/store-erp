"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/error_handling/error_manager.py
الوصف: مدير الأخطاء للنظام
المؤلف: فريق Scan AI
تاريخ الإنشاء: 30 مايو 2025
"""

import logging
from typing import Any, Dict, Optional

from .error_types import ErrorData, ErrorSeverity, ErrorType


class ErrorManager:
    """مدير الأخطاء للنظام"""

    def __init__(self):
        """تهيئة مدير الأخطاء"""
        self.logger = logging.getLogger(__name__)
        self.errors = []
        self.error_counts = {}
        self.last_error = None

    def handle_error(self, error_data: ErrorData) -> None:
        """
        معالجة خطأ جديد

        Args:
            error_data: بيانات الخطأ
        """
        self.errors.append(error_data)
        self.last_error = error_data

        # تحديث عداد الأخطاء
        error_key = f"{error_data.error_type.value}_{error_data.severity.value}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1

        # تسجيل الخطأ
        self.logger.error(
            f"Error: {error_data.message} (Type: {error_data.error_type.value}, "
            f"Severity: {error_data.severity.value})")

    def handle_exception(
        self,
        exception: Exception,
        error_type: ErrorType = ErrorType.APPLICATION_ERROR,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        module_name: Optional[str] = None,
        function_name: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> ErrorData:
        """
        معالجة استثناء

        Args:
            exception: الاستثناء
            error_type: نوع الخطأ
            severity: شدة الخطأ
            module_name: اسم الوحدة
            function_name: اسم الدالة
            user_id: معرف المستخدم
            details: تفاصيل إضافية

        Returns:
            بيانات الخطأ
        """
        error_data = ErrorData(
            error_type=error_type,
            severity=severity,
            message=str(exception),
            code=type(exception).__name__,
            details=details or {},
            user_id=user_id,
            module_name=module_name,
            function_name=function_name
        )

        self.handle_error(error_data)
        return error_data

    def get_error_stats(self) -> Dict[str, Any]:
        """
        الحصول على إحصائيات الأخطاء

        Returns:
            إحصائيات الأخطاء
        """
        return {
            "total_errors": len(
                self.errors),
            "error_counts": self.error_counts,
            "last_error": self.last_error.to_dict() if self.last_error else None}

    def clear_errors(self) -> None:
        """مسح جميع الأخطاء"""
        self.errors = []
        self.error_counts = {}
        self.last_error = None

    def get_errors(
        self,
        error_type: Optional[ErrorType] = None,
        severity: Optional[ErrorSeverity] = None,
        limit: Optional[int] = None
    ) -> list:
        """
        الحصول على قائمة الأخطاء

        Args:
            error_type: نوع الخطأ
            severity: شدة الخطأ
            limit: الحد الأقصى لعدد الأخطاء

        Returns:
            قائمة الأخطاء
        """
        filtered_errors = self.errors

        if error_type:
            filtered_errors = [
                e for e in filtered_errors if e.error_type == error_type]

        if severity:
            filtered_errors = [
                e for e in filtered_errors if e.severity == severity]

        if limit:
            filtered_errors = filtered_errors[-limit:]

        return [e.to_dict() for e in filtered_errors]


# إنشاء نسخة وحيدة من مدير الأخطاء
_error_manager = None


def get_error_manager() -> ErrorManager:
    """
    الحصول على نسخة مدير الأخطاء

    Returns:
        مدير الأخطاء
    """
    global _error_manager
    if _error_manager is None:
        _error_manager = ErrorManager()
    return _error_manager
