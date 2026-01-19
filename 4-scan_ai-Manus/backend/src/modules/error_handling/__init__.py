"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/error_handling/__init__.py
الوصف: ملف تهيئة مديول معالجة الأخطاء الموحد
المؤلف: فريق Scan AI
تاريخ الإنشاء: 30 مايو 2025
"""

from .decorators import api_error_handler, catch_errors
from .error_handlers import (
    handle_application_error,
    handle_http_error,
    handle_security_error,
)
from .error_manager import ErrorManager, get_error_manager
from .error_types import ErrorSeverity, ErrorType

__all__ = [
    'ErrorManager',
    'get_error_manager',
    'ErrorType',
    'ErrorSeverity',
    'handle_http_error',
    'handle_application_error',
    'handle_security_error',
    'catch_errors',
    'api_error_handler'
]
