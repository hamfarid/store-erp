"""
/home/ubuntu/implemented_files/v3/src/modules/user_management/config.py

ملف تكوين مديول إدارة المستخدمين

يوفر هذا الملف إعدادات التكوين لمديول إدارة المستخدمين في نظام Gaara ERP.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class PasswordPolicy(BaseModel):
    """سياسة كلمة المرور"""
    min_length: int = 8
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digit: bool = True
    require_special_char: bool = True
    password_history_size: int = 5
    max_age_days: int = 90
    lockout_threshold: int = 5
    lockout_duration_minutes: int = 30


class UserConfig(BaseModel):
    """تكوين المستخدم"""
    default_role: str = "user"
    default_is_active: bool = True
    default_is_email_verified: bool = False
    username_min_length: int = 3
    username_max_length: int = 50
    username_pattern: str = r"^[a-zA-Z0-9_.-]+$"
    allow_username_change: bool = False
    allow_email_change: bool = True
    require_email_verification: bool = True
    auto_create_profile: bool = True
    default_language: str = "ar"
    default_timezone: str = "Africa/Cairo"
    default_date_format: str = "YYYY-MM-DD"
    default_time_format: str = "HH:mm:ss"
    default_theme: str = "light"
    default_avatar: str = "/static/images/default_avatar.png"
    allowed_avatar_extensions: List[str] = ["jpg", "jpeg", "png", "gif"]
    max_avatar_size_kb: int = 1024


class UserManagementConfig(BaseModel):
    """تكوين مديول إدارة المستخدمين"""
    password_policy: PasswordPolicy = Field(default_factory=PasswordPolicy)
    user_config: UserConfig = Field(default_factory=UserConfig)
    admin_email: str = "admin@gaaraerp.com"
    admin_username: str = "admin"
    admin_role: str = "admin"
    system_roles: List[str] = ["admin", "user", "guest"]
    allow_registration: bool = False
    allow_self_delete: bool = False
    allow_admin_impersonation: bool = True
    max_users_per_organization: int = 1000
    user_profile_fields: List[str] = [
        "first_name", "last_name", "phone", "address", "city", "country",
        "postal_code", "bio", "avatar", "birth_date", "gender"
    ]
    required_profile_fields: List[str] = ["first_name", "last_name"]
    searchable_fields: List[str] = ["username", "email", "first_name", "last_name"]


# إعدادات افتراضية
default_config = UserManagementConfig()

# تصدير الدوال والكائنات
__all__ = ['UserManagementConfig', 'PasswordPolicy', 'UserConfig', 'default_config']
