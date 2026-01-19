# File: /home/ubuntu/ai_web_organized/src/modules/auth/__init__.py
"""
وحدة المصادقة والتحقق من الهوية
توفر هذه الوحدة خدمات المصادقة وإدارة الجلسات والتحقق من الصلاحيات
"""

from .api import router
from .auth_service import AuthService, check_permission, get_current_user

__all__ = [
    'router',
    'AuthService',
    'get_current_user',
    'check_permission'
]
