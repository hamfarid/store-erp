"""
ملف تكوين مديول الصلاحيات (permissions)

يحتوي هذا الملف على إعدادات وثوابت مديول الصلاحيات في نظام Gaara ERP.
"""

from enum import Enum
import os
from typing import Dict, List, Set

# الإعدادات الأساسية للمديول
MODULE_NAME = "permissions"
MODULE_DESCRIPTION = "مديول إدارة الصلاحيات في نظام Gaara ERP"
MODULE_VERSION = "3.0.0"
MODULE_AUTHOR = "Gaara Team"

# أنواع الصلاحيات المدعومة


class PermissionType(str, Enum):
    READ = "read"  # قراءة
    WRITE = "write"  # كتابة
    DELETE = "delete"  # حذف
    ADMIN = "admin"  # إدارة
    APPROVE = "approve"  # موافقة
    VIEW_SUMMARY = "view_summary"  # اطلاع بدون تفاصيل

# مستويات الصلاحيات


class PermissionLevel(int, Enum):
    NONE = 0  # لا توجد صلاحية
    LOW = 1  # صلاحية منخفضة
    MEDIUM = 2  # صلاحية متوسطة
    HIGH = 3  # صلاحية عالية
    FULL = 4  # صلاحية كاملة

# نطاقات الصلاحيات


class PermissionScope(str, Enum):
    SYSTEM = "system"  # على مستوى النظام
    MODULE = "module"  # على مستوى المديول
    FEATURE = "feature"  # على مستوى الميزة
    RECORD = "record"  # على مستوى السجل
    FIELD = "field"  # على مستوى الحقل


# الأدوار الافتراضية في النظام
DEFAULT_ROLES = {
    "superadmin": "مدير النظام الأعلى",
    "admin": "مدير النظام",
    "manager": "مدير",
    "user": "مستخدم",
    "guest": "ضيف",
    "ai_agent": "وكيل ذكاء اصطناعي",
}

# الصلاحيات الافتراضية للأدوار
DEFAULT_ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "superadmin": ["*"],  # جميع الصلاحيات
    "admin": ["*.read", "*.write", "*.delete", "*.approve"],
    "manager": ["*.read", "*.write", "*.approve"],
    "user": ["*.read", "*.write"],
    "guest": ["*.read"],
    "ai_agent": ["*.read"],
}

# الصلاحيات المطلوبة للوصول إلى واجهة إدارة الصلاحيات
PERMISSIONS_ADMIN_REQUIRED_PERMISSIONS = ["permissions.admin"]

# إعدادات التخزين المؤقت للصلاحيات
PERMISSIONS_CACHE_ENABLED = True
PERMISSIONS_CACHE_TTL = 3600  # بالثواني (ساعة واحدة)
PERMISSIONS_CACHE_KEY_PREFIX = "permissions:"

# إعدادات التدقيق والمراقبة
PERMISSIONS_AUDIT_ENABLED = True
PERMISSIONS_AUDIT_LOG_LEVEL = "INFO"

# قائمة المديولات التي يجب أن تتكامل مع نظام الصلاحيات
REQUIRED_INTEGRATION_MODULES: Set[str] = {
    "auth",
    "ai_agent_module",
    "ai_management",
    "plant_diagnosis",
    "image_search",
    "memory",
}

# مسارات API الصلاحيات
API_PREFIX = "/api/v3/permissions"
API_TAGS = ["permissions"]

# إعدادات قاعدة البيانات
DB_TABLE_PREFIX = "perm_"
DB_SCHEMA = "public"

# إعدادات الواجهة الأمامية
FRONTEND_ROUTES = {
    "dashboard": "/permissions",
    "roles": "/permissions/roles",
    "users": "/permissions/users",
    "agents": "/permissions/agents",
}

# استيراد الإعدادات من ملف البيئة


def load_from_env():
    """
    تحميل إعدادات المديول من متغيرات البيئة
    """
    global PERMISSIONS_CACHE_ENABLED, PERMISSIONS_CACHE_TTL, PERMISSIONS_AUDIT_ENABLED

    PERMISSIONS_CACHE_ENABLED = os.getenv("PERMISSIONS_CACHE_ENABLED", "True").lower() == "true"
    PERMISSIONS_CACHE_TTL = int(os.getenv("PERMISSIONS_CACHE_TTL", "3600"))
    PERMISSIONS_AUDIT_ENABLED = os.getenv("PERMISSIONS_AUDIT_ENABLED", "True").lower() == "true"


# تحميل الإعدادات عند استيراد الملف
load_from_env()
