import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field, root_validator, validator

from src.modules.authentication.models import (
    AuthProvider,
    LoginStatus,
    MFAMethod,
    TokenStatus,
    TokenType,
)

"""
/home/ubuntu/implemented_files/v3/src/modules/authentication/schemas.py

مخططات البيانات لمديول المصادقة

يحتوي هذا الملف على مخططات Pydantic لمديول المصادقة، بما في ذلك:
- مخططات الرموز
- مخططات جلسات المستخدمين
- مخططات المصادقة متعددة العوامل
- مخططات مزودي المصادقة الخارجيين
- مخططات سجلات المصادقة
"""


USER_ID_DESC = "معرف المستخدم"
TOKEN_TYPE_DESC = "نوع الرمز"
METADATA_DESC = "بيانات وصفية إضافية"
REVOKE_TIME_DESC = "وقت الإلغاء"
IP_ADDRESS_DESC = "عنوان IP"
USER_AGENT_DESC = "وكيل المستخدم"
EXPIRES_AT_DESC = "وقت انتهاء الصلاحية"
PREFERRED_METHOD_DESC = "طريقة المصادقة المفضلة"
MFA_ENABLED_DESC = "ما إذا كانت المصادقة متعددة العوامل ممكّنة"
AUTH_METHOD_TYPE_DESC = "نوع طريقة المصادقة"
PHONE_NUMBER_DESC = "رقم الهاتف (لـ SMS)"
EMAIL_DESC = "البريد الإلكتروني (لـ Email)"
IS_VERIFIED_DESC = "ما إذا كانت الطريقة مُتحقق منها"
IS_ENABLED_DESC = "ما إذا كانت الطريقة ممكّنة"
STATUS_DESC = "الحالة"
AUTH_PROVIDER_DESC = "مزود المصادقة"
ACCESS_TOKEN_DESC = "رمز الوصول"
REFRESH_TOKEN_DESC = "رمز التحديث"
SCOPE_DESC = "النطاق"
ID_DESC = "المعرف"
CREATED_AT_DESC = "وقت الإنشاء"
UPDATED_AT_DESC = "وقت التحديث"
EXPIRES_IN_SECONDS_DESC = "مدة الصلاحية بالثواني"
MESSAGE_DESC = "الرسالة"
SUCCESS_DESC = "نجاح العملية"

# ==================== مخططات الإدخال ====================


class TokenCreate(BaseModel):
    """مخطط إنشاء رمز"""

    user_id: str = Field(..., description=USER_ID_DESC)
    token_type: TokenType = Field(..., description=TOKEN_TYPE_DESC)
    expires_in_seconds: Optional[int] = Field(
        None, description="مدة صلاحية الرمز بالثواني"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)


class TokenUpdate(BaseModel):
    """مخطط تحديث رمز"""

    status: Optional[TokenStatus] = Field(None, description="حالة الرمز")
    revoked_at: Optional[datetime] = Field(None, description=REVOKE_TIME_DESC)
    used_at: Optional[datetime] = Field(None, description="وقت الاستخدام")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)


class UserSessionCreate(BaseModel):
    """مخطط إنشاء جلسة مستخدم"""

    user_id: str = Field(..., description=USER_ID_DESC)
    ip_address: Optional[str] = Field(None, description=IP_ADDRESS_DESC)
    user_agent: Optional[str] = Field(None, description=USER_AGENT_DESC)
    expires_in_seconds: Optional[int] = Field(
        None, description="مدة صلاحية الجلسة بالثواني"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)


class UserSessionUpdate(BaseModel):
    """مخطط تحديث جلسة مستخدم"""

    last_activity_at: Optional[datetime] = Field(
        None, description="وقت آخر نشاط")
    expires_at: Optional[datetime] = Field(None, description=EXPIRES_AT_DESC)
    revoked_at: Optional[datetime] = Field(None, description=REVOKE_TIME_DESC)
    is_active: Optional[bool] = Field(
        None, description="ما إذا كانت الجلسة نشطة")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)


class MFAConfigurationCreate(BaseModel):
    """مخطط إنشاء تكوين المصادقة متعددة العوامل"""

    user_id: str = Field(..., description=USER_ID_DESC)
    preferred_method: Optional[MFAMethod] = Field(
        None, description=PREFERRED_METHOD_DESC
    )
    is_mfa_enabled: bool = Field(False, description=MFA_ENABLED_DESC)


class MFAConfigurationUpdate(BaseModel):
    """مخطط تحديث تكوين المصادقة متعددة العوامل"""

    preferred_method: Optional[MFAMethod] = Field(
        None, description=PREFERRED_METHOD_DESC
    )
    is_mfa_enabled: Optional[bool] = Field(None, description=MFA_ENABLED_DESC)


class MFAMethodConfigurationCreate(BaseModel):
    """مخطط إنشاء تكوين طريقة المصادقة متعددة العوامل"""

    mfa_config_id: str = Field(...,
                               description="معرف تكوين المصادقة متعددة العوامل")
    method_type: MFAMethod = Field(..., description=AUTH_METHOD_TYPE_DESC)
    secret: Optional[str] = Field(None, description="السر (لـ TOTP)")
    phone_number: Optional[str] = Field(None, description=PHONE_NUMBER_DESC)
    email: Optional[EmailStr] = Field(None, description=EMAIL_DESC)
    backup_codes_hashed: Optional[List[str]] = Field(
        None, description="رموز النسخ الاحتياطي المشفرة (لـ Backup Codes)"
    )
    security_key_credential_id: Optional[str] = Field(
        None, description="معرف بيانات اعتماد مفتاح الأمان (لـ Security Key)"
    )
    is_verified: bool = Field(False, description=IS_VERIFIED_DESC)
    is_enabled: bool = Field(True, description=IS_ENABLED_DESC)

    @root_validator
    @classmethod
    def validate_method_fields(cls, values):
        """التحقق من حقول الطريقة"""
        method_type = values.get("method_type")

        if method_type == MFAMethod.TOTP and not values.get("secret"):
            raise ValueError("يجب توفير السر لطريقة TOTP")

        if method_type == MFAMethod.SMS and not values.get("phone_number"):
            raise ValueError("يجب توفير رقم الهاتف لطريقة SMS")

        if method_type == MFAMethod.EMAIL and not values.get("email"):
            raise ValueError("يجب توفير البريد الإلكتروني لطريقة Email")

        if method_type == MFAMethod.BACKUP_CODE and not values.get(
            "backup_codes_hashed"
        ):
            raise ValueError(
                "يجب توفير رموز النسخ الاحتياطي المشفرة لطريقة Backup Code"
            )

        if method_type == MFAMethod.SECURITY_KEY and not values.get(
            "security_key_credential_id"
        ):
            raise ValueError(
                "يجب توفير معرف بيانات اعتماد مفتاح الأمان لطريقة Security Key"
            )

        return values


class MFAMethodConfigurationUpdate(BaseModel):
    """مخطط تحديث تكوين طريقة المصادقة متعددة العوامل"""

    secret: Optional[str] = Field(None, description="السر (لـ TOTP)")
    phone_number: Optional[str] = Field(None, description=PHONE_NUMBER_DESC)
    email: Optional[EmailStr] = Field(None, description=EMAIL_DESC)
    backup_codes_hashed: Optional[List[str]] = Field(
        None, description="رموز النسخ الاحتياطي المشفرة (لـ Backup Codes)"
    )
    security_key_credential_id: Optional[str] = Field(
        None, description="معرف بيانات اعتماد مفتاح الأمان (لـ Security Key)"
    )
    is_verified: Optional[bool] = Field(None, description=IS_VERIFIED_DESC)
    is_enabled: Optional[bool] = Field(None, description=IS_ENABLED_DESC)


class AuthLogCreate(BaseModel):
    """مخطط إنشاء سجل مصادقة"""

    user_id: Optional[str] = Field(None, description=USER_ID_DESC)
    username_attempt: Optional[str] = Field(
        None, description="محاولة اسم المستخدم")
    action: str = Field(..., description="الإجراء")
    status: LoginStatus = Field(..., description=STATUS_DESC)
    ip_address: Optional[str] = Field(None, description=IP_ADDRESS_DESC)
    user_agent: Optional[str] = Field(None, description=USER_AGENT_DESC)
    provider: Optional[AuthProvider] = Field(
        None, description=AUTH_PROVIDER_DESC)
    error_message: Optional[str] = Field(None, description="رسالة الخطأ")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)


class OAuthAccountCreate(BaseModel):
    """مخطط إنشاء حساب OAuth"""

    user_id: str = Field(..., description=USER_ID_DESC)
    provider: AuthProvider = Field(..., description=AUTH_PROVIDER_DESC)
    provider_user_id: str = Field(..., description="معرف المستخدم لدى المزود")
    access_token: Optional[str] = Field(None, description=ACCESS_TOKEN_DESC)
    refresh_token: Optional[str] = Field(None, description=REFRESH_TOKEN_DESC)
    expires_at: Optional[datetime] = Field(None, description=EXPIRES_AT_DESC)
    scope: Optional[str] = Field(None, description=SCOPE_DESC)


class OAuthAccountUpdate(BaseModel):
    """مخطط تحديث حساب OAuth"""

    access_token: Optional[str] = Field(None, description=ACCESS_TOKEN_DESC)
    refresh_token: Optional[str] = Field(None, description=REFRESH_TOKEN_DESC)
    expires_at: Optional[datetime] = Field(None, description=EXPIRES_AT_DESC)
    scope: Optional[str] = Field(None, description=SCOPE_DESC)


class LoginRequest(BaseModel):
    """مخطط طلب تسجيل الدخول"""

    username: str = Field(..., description="اسم المستخدم")
    password: str = Field(..., description="كلمة المرور")
    remember_me: Optional[bool] = Field(False, description="تذكرني")


class MFAVerifyRequest(BaseModel):
    """مخطط طلب التحقق من المصادقة متعددة العوامل"""

    mfa_token: str = Field(..., description="رمز المصادقة متعددة العوامل")
    mfa_code: str = Field(..., description="رمز التحقق")
    method_type: MFAMethod = Field(..., description=AUTH_METHOD_TYPE_DESC)


class PasswordResetRequest(BaseModel):
    """مخطط طلب إعادة تعيين كلمة المرور"""

    email: EmailStr = Field(..., description="البريد الإلكتروني")


class PasswordResetConfirmRequest(BaseModel):
    """مخطط طلب تأكيد إعادة تعيين كلمة المرور"""

    token: str = Field(..., description="الرمز")
    new_password: str = Field(..., description="كلمة المرور الجديدة")
    confirm_password: str = Field(..., description="تأكيد كلمة المرور")

    @validator("new_password")
    @classmethod
    def validate_password_strength(cls, v):
        """التحقق من قوة كلمة المرور"""
        if len(v) < 8:
            raise ValueError("يجب أن تكون كلمة المرور 8 أحرف على الأقل")

        if not re.search(r"[A-Z]", v):
            raise ValueError(
                "يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل")

        if not re.search(r"[a-z]", v):
            raise ValueError(
                "يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل")

        if not re.search(r"\d", v):
            raise ValueError("يجب أن تحتوي كلمة المرور على رقم واحد على الأقل")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError(
                "يجب أن تحتوي كلمة المرور على حرف خاص واحد على الأقل")

        return v

    @validator("confirm_password")
    @classmethod
    def validate_passwords_match(cls, v, values):
        """التحقق من تطابق كلمات المرور"""
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("كلمات المرور غير متطابقة")
        return v


# ==================== مخططات الاستجابة ====================


class EmailVerificationRequest(BaseModel):
    """مخطط طلب التحقق من البريد الإلكتروني"""

    token: str = Field(..., description="الرمز")


class RefreshTokenRequest(BaseModel):
    """مخطط طلب تحديث الرمز"""

    refresh_token: str = Field(..., description=REFRESH_TOKEN_DESC)


class LogoutRequest(BaseModel):
    """مخطط طلب تسجيل الخروج"""

    all_sessions: Optional[bool] = Field(
        False, description="تسجيل الخروج من جميع الجلسات"
    )


class OAuthLoginRequest(BaseModel):
    """مخطط طلب تسجيل الدخول باستخدام OAuth"""

    provider: AuthProvider = Field(..., description=AUTH_PROVIDER_DESC)
    code: str = Field(..., description="رمز التفويض")
    redirect_uri: str = Field(..., description="عنوان URI لإعادة التوجيه")
    state: Optional[str] = Field(None, description="الحالة")


# ==================== مخططات الاستجابة ====================


class TokenResponse(BaseModel):
    """مخطط استجابة الرمز"""

    id: str = Field(..., description=ID_DESC)
    user_id: str = Field(..., description=USER_ID_DESC)
    token_type: TokenType = Field(..., description=TOKEN_TYPE_DESC)
    status: TokenStatus = Field(..., description="حالة الرمز")
    expires_at: datetime = Field(..., description=EXPIRES_AT_DESC)
    created_at: datetime = Field(..., description=CREATED_AT_DESC)
    revoked_at: Optional[datetime] = Field(None, description=REVOKE_TIME_DESC)
    used_at: Optional[datetime] = Field(None, description="وقت الاستخدام")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)

    class Config:
        orm_mode = True


class UserSessionResponse(BaseModel):
    """مخطط استجابة جلسة المستخدم"""

    id: str = Field(..., description=ID_DESC)
    user_id: str = Field(..., description=USER_ID_DESC)
    ip_address: Optional[str] = Field(None, description=IP_ADDRESS_DESC)
    user_agent: Optional[str] = Field(None, description=USER_AGENT_DESC)
    last_activity_at: datetime = Field(..., description="وقت آخر نشاط")
    expires_at: datetime = Field(..., description=EXPIRES_AT_DESC)
    created_at: datetime = Field(..., description=CREATED_AT_DESC)
    revoked_at: Optional[datetime] = Field(None, description=REVOKE_TIME_DESC)
    is_active: bool = Field(..., description="ما إذا كانت الجلسة نشطة")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)

    class Config:
        orm_mode = True


class MFAMethodConfigurationResponse(BaseModel):
    """مخطط استجابة تكوين طريقة المصادقة متعددة العوامل"""

    id: str = Field(..., description=ID_DESC)
    mfa_config_id: str = Field(...,
                               description="معرف تكوين المصادقة متعددة العوامل")
    method_type: MFAMethod = Field(..., description=AUTH_METHOD_TYPE_DESC)
    phone_number: Optional[str] = Field(None, description=PHONE_NUMBER_DESC)
    email: Optional[str] = Field(None, description=EMAIL_DESC)
    is_verified: bool = Field(..., description=IS_VERIFIED_DESC)
    is_enabled: bool = Field(..., description=IS_ENABLED_DESC)
    created_at: datetime = Field(..., description=CREATED_AT_DESC)
    updated_at: datetime = Field(..., description=UPDATED_AT_DESC)

    class Config:
        orm_mode = True


class MFAConfigurationResponse(BaseModel):
    """مخطط استجابة تكوين المصادقة متعددة العوامل"""

    id: str = Field(..., description=ID_DESC)
    user_id: str = Field(..., description=USER_ID_DESC)
    preferred_method: Optional[MFAMethod] = Field(
        None, description=PREFERRED_METHOD_DESC
    )
    is_mfa_enabled: bool = Field(..., description=MFA_ENABLED_DESC)
    created_at: datetime = Field(..., description=CREATED_AT_DESC)
    updated_at: datetime = Field(..., description=UPDATED_AT_DESC)
    mfa_methods: List[MFAMethodConfigurationResponse] = Field(
        [], description="طرق المصادقة متعددة العوامل"
    )

    class Config:
        orm_mode = True


class AuthLogResponse(BaseModel):
    """مخطط استجابة سجل المصادقة"""

    id: str = Field(..., description=ID_DESC)
    user_id: Optional[str] = Field(None, description=USER_ID_DESC)
    username_attempt: Optional[str] = Field(
        None, description="محاولة اسم المستخدم")
    timestamp: datetime = Field(..., description="الوقت")
    action: str = Field(..., description="الإجراء")
    status: LoginStatus = Field(..., description=STATUS_DESC)
    ip_address: Optional[str] = Field(None, description=IP_ADDRESS_DESC)
    user_agent: Optional[str] = Field(None, description=USER_AGENT_DESC)
    provider: Optional[AuthProvider] = Field(
        None, description=AUTH_PROVIDER_DESC)
    error_message: Optional[str] = Field(None, description="رسالة الخطأ")
    metadata: Optional[Dict[str, Any]] = Field(None, description=METADATA_DESC)

    class Config:
        orm_mode = True


class OAuthAccountResponse(BaseModel):
    """مخطط استجابة حساب OAuth"""

    id: str = Field(..., description=ID_DESC)
    user_id: str = Field(..., description=USER_ID_DESC)
    provider: AuthProvider = Field(..., description=AUTH_PROVIDER_DESC)
    provider_user_id: str = Field(..., description="معرف المستخدم لدى المزود")
    scope: Optional[str] = Field(None, description=SCOPE_DESC)
    created_at: datetime = Field(..., description=CREATED_AT_DESC)
    updated_at: datetime = Field(..., description=UPDATED_AT_DESC)

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    """مخطط استجابة تسجيل الدخول"""

    access_token: str = Field(..., description=ACCESS_TOKEN_DESC)
    token_type: str = Field("bearer", description=TOKEN_TYPE_DESC)
    expires_in: int = Field(..., description=EXPIRES_IN_SECONDS_DESC)
    refresh_token: str = Field(..., description=REFRESH_TOKEN_DESC)
    user_id: str = Field(..., description=USER_ID_DESC)
    requires_mfa: bool = Field(
        False, description="ما إذا كانت المصادقة متعددة العوامل مطلوبة"
    )
    mfa_token: Optional[str] = Field(
        None, description="رمز المصادقة متعددة العوامل")
    available_mfa_methods: Optional[List[MFAMethod]] = Field(
        None, description="طرق المصادقة متعددة العوامل المتاحة"
    )
    session_id: Optional[str] = Field(None, description="معرف الجلسة")


class MFAVerifyResponse(BaseModel):
    """مخطط استجابة التحقق من المصادقة متعددة العوامل"""

    access_token: str = Field(..., description=ACCESS_TOKEN_DESC)
    token_type: str = Field("bearer", description=TOKEN_TYPE_DESC)
    expires_in: int = Field(..., description=EXPIRES_IN_SECONDS_DESC)
    refresh_token: str = Field(..., description=REFRESH_TOKEN_DESC)
    user_id: str = Field(..., description=USER_ID_DESC)
    session_id: Optional[str] = Field(None, description="معرف الجلسة")


class PasswordResetResponse(BaseModel):
    """مخطط استجابة إعادة تعيين كلمة المرور"""

    message: str = Field(..., description=MESSAGE_DESC)
    email: str = Field(..., description="البريد الإلكتروني")


class PasswordResetConfirmResponse(BaseModel):
    """مخطط استجابة تأكيد إعادة تعيين كلمة المرور"""

    message: str = Field(..., description=MESSAGE_DESC)
    success: bool = Field(..., description=SUCCESS_DESC)


class EmailVerificationResponse(BaseModel):
    """مخطط استجابة التحقق من البريد الإلكتروني"""

    message: str = Field(..., description=MESSAGE_DESC)
    success: bool = Field(..., description=SUCCESS_DESC)


class RefreshTokenResponse(BaseModel):
    """مخطط استجابة تحديث الرمز"""

    access_token: str = Field(..., description=ACCESS_TOKEN_DESC)
    token_type: str = Field("bearer", description=TOKEN_TYPE_DESC)
    expires_in: int = Field(..., description=EXPIRES_IN_SECONDS_DESC)
    refresh_token: str = Field(..., description=REFRESH_TOKEN_DESC)


class LogoutResponse(BaseModel):
    """مخطط استجابة تسجيل الخروج"""

    message: str = Field(..., description=MESSAGE_DESC)
    success: bool = Field(..., description=SUCCESS_DESC)


class OAuthLoginResponse(BaseModel):
    """مخطط استجابة تسجيل الدخول باستخدام OAuth"""

    access_token: str = Field(..., description=ACCESS_TOKEN_DESC)
    token_type: str = Field("bearer", description=TOKEN_TYPE_DESC)
    expires_in: int = Field(..., description=EXPIRES_IN_SECONDS_DESC)
    refresh_token: str = Field(..., description=REFRESH_TOKEN_DESC)
    user_id: str = Field(..., description=USER_ID_DESC)
    is_new_user: bool = Field(False, description="ما إذا كان المستخدم جديداً")


# تصدير جميع المخططات
__all__ = [
    "TokenCreate",
    "TokenUpdate",
    "TokenResponse",
    "UserSessionCreate",
    "UserSessionUpdate",
    "UserSessionResponse",
    "MFAConfigurationCreate",
    "MFAConfigurationUpdate",
    "MFAConfigurationResponse",
    "MFAMethodConfigurationCreate",
    "MFAMethodConfigurationUpdate",
    "MFAMethodConfigurationResponse",
    "AuthLogCreate",
    "AuthLogResponse",
    "OAuthAccountCreate",
    "OAuthAccountUpdate",
    "OAuthAccountResponse",
    "LoginRequest",
    "LoginResponse",
    "MFAVerifyRequest",
    "MFAVerifyResponse",
    "PasswordResetRequest",
    "PasswordResetResponse",
    "PasswordResetConfirmRequest",
    "PasswordResetConfirmResponse",
    "EmailVerificationRequest",
    "EmailVerificationResponse",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    "LogoutRequest",
    "LogoutResponse",
    "OAuthLoginRequest",
    "OAuthLoginResponse",
]
