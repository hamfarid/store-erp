"""
/home/ubuntu/implemented_files/v3/src/modules/authentication/config.py

ملف تكوين مديول المصادقة

يحتوي هذا الملف على إعدادات تكوين مديول المصادقة، بما في ذلك:
- إعدادات JWT
- إعدادات جلسات المستخدمين
- إعدادات المصادقة متعددة العوامل
- إعدادات مزودي المصادقة الخارجيين
- إعدادات أمان كلمات المرور
"""

from typing import Dict
import os

from pydantic import BaseModel, Field, validator


class JWTConfig(BaseModel):
    """تكوين JWT"""

    secret_key_env_var: str = Field(
        "JWT_SECRET_KEY", description="متغير البيئة لمفتاح JWT السري"
    )
    algorithm: str = Field("HS256", description="خوارزمية التوقيع")
    access_token_expire_minutes: int = Field(
        30, description="مدة صلاحية رمز الوصول بالدقائق"
    )
    refresh_token_expire_days: int = Field(
        7, description="مدة صلاحية رمز التحديث بالأيام"
    )
    token_url: str = Field("/api/v1/auth/token", description="مسار الحصول على الرمز")

    @validator("secret_key_env_var")
    @classmethod
    def validate_secret_key_env_var(cls, v):
        """التحقق من وجود متغير البيئة لمفتاح JWT السري"""
        if not os.environ.get(v):
            # تسجيل تحذير بدلاً من رفع استثناء
            print(f"تحذير: متغير البيئة {v} غير موجود")
        return v


class SessionConfig(BaseModel):
    """تكوين جلسات المستخدمين"""

    session_cookie_name: str = Field(
        "gaara_session", description="اسم ملف تعريف ارتباط الجلسة"
    )
    session_expire_minutes: int = Field(60, description="مدة صلاحية الجلسة بالدقائق")
    session_secure: bool = Field(
        True, description="ما إذا كانت ملفات تعريف الارتباط آمنة (HTTPS فقط)"
    )
    session_httponly: bool = Field(
        True, description="ما إذا كانت ملفات تعريف الارتباط متاحة فقط عبر HTTP"
    )
    session_samesite: str = Field(
        "lax", description="سياسة SameSite لملفات تعريف الارتباط"
    )
    max_active_sessions_per_user: int = Field(
        5, description="الحد الأقصى لعدد الجلسات النشطة لكل مستخدم"
    )
    enable_session_tracking: bool = Field(True, description="تمكين تتبع الجلسات")


class MFAConfig(BaseModel):
    """تكوين المصادقة متعددة العوامل"""

    enable_mfa: bool = Field(True, description="تمكين المصادقة متعددة العوامل")
    default_mfa_method: str = Field(
        "totp", description="طريقة المصادقة متعددة العوامل الافتراضية"
    )
    totp_issuer: str = Field("Gaara ERP", description="مصدر TOTP")
    totp_digits: int = Field(6, description="عدد أرقام TOTP")
    totp_interval: int = Field(30, description="فترة TOTP بالثواني")
    totp_algorithm: str = Field("SHA1", description="خوارزمية TOTP")
    backup_codes_count: int = Field(10, description="عدد رموز النسخ الاحتياطي")
    enforce_mfa_for_admins: bool = Field(
        True, description="فرض المصادقة متعددة العوامل للمسؤولين"
    )
    enforce_mfa_for_sensitive_operations: bool = Field(
        True, description="فرض المصادقة متعددة العوامل للعمليات الحساسة"
    )


class PasswordConfig(BaseModel):
    """تكوين أمان كلمات المرور"""

    min_length: int = Field(8, description="الحد الأدنى لطول كلمة المرور")
    require_uppercase: bool = Field(True, description="طلب حرف كبير واحد على الأقل")
    require_lowercase: bool = Field(True, description="طلب حرف صغير واحد على الأقل")
    require_digit: bool = Field(True, description="طلب رقم واحد على الأقل")
    require_special_char: bool = Field(True, description="طلب حرف خاص واحد على الأقل")
    password_history_count: int = Field(
        5, description="عدد كلمات المرور السابقة التي لا يمكن إعادة استخدامها"
    )
    max_password_age_days: int = Field(
        90, description="العمر الأقصى لكلمة المرور بالأيام"
    )
    password_reset_token_expire_minutes: int = Field(
        15, description="مدة صلاحية رمز إعادة تعيين كلمة المرور بالدقائق"
    )
    lockout_threshold: int = Field(
        5, description="عدد محاولات تسجيل الدخول الفاشلة قبل قفل الحساب"
    )
    lockout_duration_minutes: int = Field(15, description="مدة قفل الحساب بالدقائق")


class OAuthProviderConfig(BaseModel):
    """تكوين مزود OAuth"""

    name: str = Field(..., description="اسم المزود")
    client_id_env_var: str = Field(..., description="متغير البيئة لمعرف العميل")
    client_secret_env_var: str = Field(..., description="متغير البيئة لسر العميل")
    authorize_url: str = Field(..., description="عنوان URL للتفويض")
    token_url: str = Field(..., description="عنوان URL للرمز")
    userinfo_url: str = Field(..., description="عنوان URL لمعلومات المستخدم")
    redirect_uri: str = Field(..., description="عنوان URI لإعادة التوجيه")
    scope: str = Field(..., description="نطاق الوصول")
    is_enabled: bool = Field(True, description="ما إذا كان المزود ممكّناً")

    @validator("client_id_env_var", "client_secret_env_var")
    @classmethod
    def validate_env_vars(cls, v):
        """التحقق من وجود متغيرات البيئة"""
        if not os.environ.get(v):
            # تسجيل تحذير بدلاً من رفع استثناء
            print(f"تحذير: متغير البيئة {v} غير موجود")
        return v


class AuthenticationConfig(BaseModel):
    """التكوين الرئيسي لمديول المصادقة"""

    jwt: JWTConfig = Field(default_factory=JWTConfig, description="تكوين JWT")
    session: SessionConfig = Field(
        default_factory=SessionConfig, description="تكوين الجلسات"
    )
    mfa: MFAConfig = Field(
        default_factory=MFAConfig, description="تكوين المصادقة متعددة العوامل"
    )
    password: PasswordConfig = Field(
        default_factory=PasswordConfig, description="تكوين كلمات المرور"
    )
    oauth_providers: Dict[str, OAuthProviderConfig] = Field(
        default_factory=dict, description="مزودو OAuth"
    )
    enable_module: bool = Field(True, description="تمكين المديول")
    debug_mode: bool = Field(False, description="وضع التصحيح")
    allow_registration: bool = Field(False, description="السماح بالتسجيل")
    require_email_verification: bool = Field(
        True, description="طلب التحقق من البريد الإلكتروني"
    )
    email_verification_token_expire_hours: int = Field(
        24, description="مدة صلاحية رمز التحقق من البريد الإلكتروني بالساعات"
    )
    enable_remember_me: bool = Field(True, description="تمكين خاصية تذكرني")
    remember_me_days: int = Field(30, description="مدة تذكر المستخدم بالأيام")
    login_rate_limit_per_minute: int = Field(
        5, description="حد معدل تسجيل الدخول في الدقيقة"
    )
    enable_ip_tracking: bool = Field(True, description="تمكين تتبع عنوان IP")
    enable_user_agent_tracking: bool = Field(
        True, description="تمكين تتبع وكيل المستخدم"
    )
    enable_login_notifications: bool = Field(
        True, description="تمكين إشعارات تسجيل الدخول"
    )
    notify_on_suspicious_login: bool = Field(
        True, description="إشعار عند تسجيل الدخول المشبوه"
    )


# تكوين مزودي OAuth
google_provider = OAuthProviderConfig(
    name="Google",
    client_id_env_var="GOOGLE_CLIENT_ID",
    client_secret_env_var="GOOGLE_CLIENT_SECRET",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    token_url="https://oauth2.googleapis.com/token",
    userinfo_url="https://www.googleapis.com/oauth2/v3/userinfo",
    redirect_uri="/api/v1/auth/oauth/google/callback",
    scope="openid email profile",
)

microsoft_provider = OAuthProviderConfig(
    name="Microsoft",
    client_id_env_var="MICROSOFT_CLIENT_ID",
    client_secret_env_var="MICROSOFT_CLIENT_SECRET",
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    userinfo_url="https://graph.microsoft.com/v1.0/me",
    redirect_uri="/api/v1/auth/oauth/microsoft/callback",
    scope="openid email profile User.Read",
)

# التكوين الافتراضي
default_config = AuthenticationConfig(
    jwt=JWTConfig(access_token_expire_minutes=30, refresh_token_expire_days=7),
    session=SessionConfig(session_expire_minutes=60, max_active_sessions_per_user=5),
    mfa=MFAConfig(enable_mfa=True, enforce_mfa_for_admins=True),
    password=PasswordConfig(
        min_length=8, password_history_count=5, max_password_age_days=90
    ),
    oauth_providers={"google": google_provider, "microsoft": microsoft_provider},
    enable_module=True,
    debug_mode=False,
    allow_registration=False,
    require_email_verification=True,
    enable_remember_me=True,
    login_rate_limit_per_minute=5,
)

# تصدير الدوال والكائنات
__all__ = ["AuthenticationConfig", "default_config"]
