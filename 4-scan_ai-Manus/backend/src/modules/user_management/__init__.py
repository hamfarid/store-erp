"""
/home/ubuntu/implemented_files/v3/src/modules/user_management/__init__.py

مديول إدارة المستخدمين لنظام Gaara ERP

يوفر هذا المديول وظائف إدارة المستخدمين الأساسية، بما في ذلك:
- إنشاء وتعديل وحذف المستخدمين
- إدارة معلومات الملف الشخصي
- إدارة الأدوار والصلاحيات
- إدارة تفضيلات المستخدم
"""

from .models import Role, User, UserPreference, UserProfile, UserRole
from .service import UserService

__all__ = [
    'UserService',
    'User',
    'UserProfile',
    'UserPreference',
    'UserRole',
    'Role'
]
