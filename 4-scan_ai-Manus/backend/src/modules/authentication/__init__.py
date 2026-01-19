"""
/home/ubuntu/implemented_files/v3/src/modules/authentication/__init__.py

مديول المصادقة لنظام Gaara ERP

يوفر هذا المديول وظائف المصادقة والتحقق من الهوية، بما في ذلك:
- تسجيل الدخول والخروج
- التحقق من الهوية باستخدام JWT
- إدارة جلسات المستخدمين
- المصادقة متعددة العوامل
- استعادة كلمات المرور
"""

from .config import default_config
from .models import AuthProvider, TokenStatus, TokenType

__version__ = "1.0.0"
__author__ = "Gaara ERP Team"

# تصدير الدوال والكائنات
__all__ = [
    'default_config',
    'TokenType',
    'TokenStatus',
    'AuthProvider'
]
