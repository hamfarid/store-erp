"""
/home/ubuntu/implemented_files/v3/src/modules/user_management/schemas.py

مخططات البيانات لمديول إدارة المستخدمين

يوفر هذا الملف مخططات البيانات (Schemas) لمديول إدارة المستخدمين في نظام Gaara ERP.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, EmailStr, validator, root_validator
from datetime import datetime
import re

from .models import Gender

# ==================== مخططات المستخدم ====================


class UserBase(BaseModel):
    """المخطط الأساسي للمستخدم"""

    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    organization_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    @validator("username")
    def username_must_be_valid(cls, v):
        """التحقق من صحة اسم المستخدم"""
        if not re.match(r"^[a-zA-Z0-9_.-]+$", v):
            raise ValueError(
                "اسم المستخدم يجب أن يحتوي على أحرف وأرقام وشرطات وشرطات سفلية فقط"
            )
        if len(v) < 3:
            raise ValueError("اسم المستخدم يجب أن يكون 3 أحرف على الأقل")
        if len(v) > 50:
            raise ValueError("اسم المستخدم يجب أن يكون 50 حرفاً على الأكثر")
        return v


class UserCreate(UserBase):
    """مخطط إنشاء المستخدم"""

    password: str
    confirm_password: str
    is_email_verified: Optional[bool] = False

    @validator("password")
    def password_must_be_strong(cls, v):
        """التحقق من قوة كلمة المرور"""
        if len(v) < 8:
            raise ValueError("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
        if not re.search(r"[A-Z]", v):
            raise ValueError("كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل")
        if not re.search(r"[a-z]", v):
            raise ValueError("كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل")
        if not re.search(r"\d", v):
            raise ValueError("كلمة المرور يجب أن تحتوي على رقم واحد على الأقل")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError(
                "كلمة المرور يجب أن تحتوي على حرف خاص واحد على الأقل"
            )
        return v

    @root_validator
    def passwords_match(cls, values):
        """التحقق من تطابق كلمات المرور"""
        password = values.get("password")
        confirm_password = values.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValueError("كلمات المرور غير متطابقة")
        return values


class UserUpdate(BaseModel):
    """مخطط تحديث المستخدم"""

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    is_email_verified: Optional[bool] = None
    organization_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UserResponse(BaseModel):
    """مخطط استجابة المستخدم"""

    id: str
    username: str
    email: str
    is_active: bool
    is_admin: bool
    is_email_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    organization_id: Optional[str] = None
    metadata: Dict[str, Any]

    class Config:
        orm_mode = True


class UserDetailResponse(UserResponse):
    """مخطط استجابة تفاصيل المستخدم"""

    profile: Optional["UserProfileResponse"] = None
    preferences: Optional["UserPreferenceResponse"] = None
    roles: List["RoleResponse"] = []

    class Config:
        orm_mode = True


# ==================== مخططات الملف الشخصي ====================


class UserProfileBase(BaseModel):
    """المخطط الأساسي للملف الشخصي"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[Gender] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UserProfileCreate(UserProfileBase):
    """مخطط إنشاء الملف الشخصي"""

    user_id: str


class UserProfileUpdate(UserProfileBase):
    """مخطط تحديث الملف الشخصي"""

    pass


class UserProfileResponse(UserProfileBase):
    """مخطط استجابة الملف الشخصي"""

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ==================== مخططات التفضيلات ====================


class UserPreferenceBase(BaseModel):
    """المخطط الأساسي للتفضيلات"""

    language: Optional[str] = "ar"
    timezone: Optional[str] = "Africa/Cairo"
    date_format: Optional[str] = "YYYY-MM-DD"
    time_format: Optional[str] = "HH:mm:ss"
    theme: Optional[str] = "light"
    notifications_enabled: Optional[bool] = True
    email_notifications: Optional[bool] = True
    sms_notifications: Optional[bool] = False
    push_notifications: Optional[bool] = True
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UserPreferenceCreate(UserPreferenceBase):
    """مخطط إنشاء التفضيلات"""

    user_id: str


class UserPreferenceUpdate(UserPreferenceBase):
    """مخطط تحديث التفضيلات"""

    pass


class UserPreferenceResponse(UserPreferenceBase):
    """مخطط استجابة التفضيلات"""

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ==================== مخططات الدور ====================


class RoleBase(BaseModel):
    """المخطط الأساسي للدور"""

    name: str
    description: Optional[str] = None
    is_system: Optional[bool] = False
    is_default: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class RoleCreate(RoleBase):
    """مخطط إنشاء الدور"""

    pass


class RoleUpdate(BaseModel):
    """مخطط تحديث الدور"""

    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class RoleResponse(RoleBase):
    """مخطط استجابة الدور"""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ==================== مخططات المؤسسة ====================


class OrganizationBase(BaseModel):
    """المخطط الأساسي للمؤسسة"""

    name: str
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    logo: Optional[str] = None
    is_active: Optional[bool] = True
    parent_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class OrganizationCreate(OrganizationBase):
    """مخطط إنشاء المؤسسة"""

    pass


class OrganizationUpdate(BaseModel):
    """مخطط تحديث المؤسسة"""

    name: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    logo: Optional[str] = None
    is_active: Optional[bool] = None
    parent_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class OrganizationResponse(OrganizationBase):
    """مخطط استجابة المؤسسة"""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrganizationDetailResponse(OrganizationResponse):
    """مخطط استجابة تفاصيل المؤسسة"""

    parent: Optional["OrganizationResponse"] = None
    branches: List["OrganizationResponse"] = []

    class Config:
        orm_mode = True


# ==================== مخططات أخرى ====================


class ChangePasswordRequest(BaseModel):
    """مخطط طلب تغيير كلمة المرور"""

    current_password: str
    new_password: str
    confirm_password: str

    @validator("new_password")
    def password_must_be_strong(cls, v):
        """التحقق من قوة كلمة المرور الجديدة"""
        if len(v) < 8:
            raise ValueError("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
        if not re.search(r"[A-Z]", v):
            raise ValueError("كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل")
        if not re.search(r"[a-z]", v):
            raise ValueError("كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل")
        if not re.search(r"\d", v):
            raise ValueError("كلمة المرور يجب أن تحتوي على رقم واحد على الأقل")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError(
                "كلمة المرور يجب أن تحتوي على حرف خاص واحد على الأقل"
            )
        return v

    @root_validator
    def passwords_match(cls, values):
        """التحقق من تطابق كلمات المرور"""
        new_password = values.get("new_password")
        confirm_password = values.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            raise ValueError("كلمات المرور غير متطابقة")
        return values


class ChangePasswordResponse(BaseModel):
    """مخطط استجابة تغيير كلمة المرور"""

    message: str
    success: bool


class AssignRoleRequest(BaseModel):
    """مخطط طلب تعيين الدور"""

    user_id: str
    role_id: str


class AssignRoleResponse(BaseModel):
    """مخطط استجابة تعيين الدور"""

    message: str
    success: bool
    user_id: str
    role_id: str


class UserSearchRequest(BaseModel):
    """مخطط طلب البحث عن المستخدمين"""

    query: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    organization_id: Optional[str] = None
    role_id: Optional[str] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0


class UserSearchResponse(BaseModel):
    """مخطط استجابة البحث عن المستخدمين"""

    total: int
    items: List[UserResponse]


# تصدير المخططات
__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserDetailResponse",
    "UserProfileBase",
    "UserProfileCreate",
    "UserProfileUpdate",
    "UserProfileResponse",
    "UserPreferenceBase",
    "UserPreferenceCreate",
    "UserPreferenceUpdate",
    "UserPreferenceResponse",
    "RoleBase",
    "RoleCreate",
    "RoleUpdate",
    "RoleResponse",
    "OrganizationBase",
    "OrganizationCreate",
    "OrganizationUpdate",
    "OrganizationResponse",
    "OrganizationDetailResponse",
    "ChangePasswordRequest",
    "ChangePasswordResponse",
    "AssignRoleRequest",
    "AssignRoleResponse",
    "UserSearchRequest",
    "UserSearchResponse",
]
