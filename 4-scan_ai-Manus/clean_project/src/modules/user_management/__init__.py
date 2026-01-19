"""
/home/ubuntu/implemented_files/v3/src/modules/user_management/__init__.py

مديول إدارة المستخدمين لنظام Gaara ERP

يوفر هذا المديول وظائف إدارة المستخدمين الأساسية، بما في ذلك:
- إنشاء وتعديل وحذف المستخدمين
- إدارة معلومات الملف الشخصي
- إدارة الأدوار والصلاحيات
- إدارة تفضيلات المستخدم
"""

from .service import UserService
from .models import User, UserProfile, UserPreference, UserRole, Role

__all__ = [
    'UserService',
    'User',
    'UserProfile',
    'UserPreference',
    'UserRole',
    'Role'
]
