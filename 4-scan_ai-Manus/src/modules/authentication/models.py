"""
/home/ubuntu/implemented_files/v3/src/modules/authentication/models.py

نماذج قاعدة البيانات لمديول المصادقة

يحتوي هذا الملف على نماذج SQLAlchemy لمديول المصادقة، بما في ذلك:
- نماذج الرموز (Tokens)
- نماذج جلسات المستخدمين
- نماذج المصادقة متعددة العوامل
- نماذج مزودي المصادقة الخارجيين
- نماذج سجلات المصادقة
"""

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Enum as SQLAlchemyEnum,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from src.modules.database import Base
from src.modulesuser_management.models import User  # استيراد نموذج المستخدم

# تعريف الثوابت
USERS_ID_FK = "users.id"


# تعريف التعدادات
class TokenType(enum.Enum):
    """أنواع الرموز"""

    ACCESS = "access"
    REFRESH = "refresh"
    PASSWORD_RESET = "password_reset"
    EMAIL_VERIFICATION = "email_verification"
    MFA_SETUP = "mfa_setup"
    API_KEY = "api_key"


class TokenStatus(enum.Enum):
    """حالات الرموز"""

    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    USED = "used"


class AuthProvider(enum.Enum):
    """مزودو المصادقة"""

    LOCAL = "local"
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    LDAP = "ldap"
    SAML = "saml"


class MFAMethod(enum.Enum):
    """طرق المصادقة متعددة العوامل"""

    TOTP = "totp"
    SMS = "sms"
    EMAIL = "email"
    BACKUP_CODE = "backup_code"
    SECURITY_KEY = "security_key"


class LoginStatus(enum.Enum):
    """حالات تسجيل الدخول"""

    SUCCESS = "success"
    FAILURE = "failure"
    MFA_REQUIRED = "mfa_required"
    LOCKED_OUT = "locked_out"


# نماذج قاعدة البيانات


class Token(Base):
    """نموذج الرموز"""

    __tablename__ = "auth_tokens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(USERS_ID_FK, ondelete="CASCADE"), nullable=False)
    token_type = Column(SQLAlchemyEnum(TokenType), nullable=False)
    token_hash = Column(String, nullable=False, unique=True, index=True)
    status = Column(
        SQLAlchemyEnum(TokenStatus), nullable=False, default=TokenStatus.ACTIVE
    )
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
    used_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, nullable=True)

    user = relationship("User", back_populates="tokens")


class UserSession(Base):
    """نموذج جلسات المستخدمين"""

    __tablename__ = "auth_user_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(USERS_ID_FK, ondelete="CASCADE"), nullable=False)
    session_token_hash = Column(String, nullable=False, unique=True, index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    last_activity_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)

    user = relationship("User", back_populates="sessions")


class MFAConfiguration(Base):
    """نموذج تكوين المصادقة متعددة العوامل"""

    __tablename__ = "auth_mfa_configurations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String, ForeignKey(USERS_ID_FK, ondelete="CASCADE"), nullable=False, unique=True
    )
    preferred_method = Column(SQLAlchemyEnum(MFAMethod), nullable=True)
    is_mfa_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="mfa_config")
    mfa_methods = relationship(
        "MFAMethodConfiguration",
        back_populates="mfa_config",
        cascade="all, delete-orphan",
    )


class MFAMethodConfiguration(Base):
    """نموذج تكوين طرق المصادقة متعددة العوامل"""

    __tablename__ = "auth_mfa_method_configurations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mfa_config_id = Column(
        String,
        ForeignKey("auth_mfa_configurations.id", ondelete="CASCADE"),
        nullable=False,
    )
    method_type = Column(SQLAlchemyEnum(MFAMethod), nullable=False)
    secret = Column(String, nullable=True)  # لـ TOTP
    phone_number = Column(String, nullable=True)  # لـ SMS
    email = Column(String, nullable=True)  # لـ Email
    backup_codes_hashed = Column(JSON, nullable=True)  # لـ Backup Codes
    security_key_credential_id = Column(String, nullable=True)  # لـ Security Key
    is_verified = Column(Boolean, default=False)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mfa_config = relationship("MFAConfiguration", back_populates="mfa_methods")


class AuthLog(Base):
    """نموذج سجلات المصادقة"""

    __tablename__ = "auth_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(USERS_ID_FK, ondelete="SET NULL"), nullable=True)
    username_attempt = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(
        String, nullable=False
    )  # مثل: login, logout, password_reset_request, mfa_attempt
    status = Column(SQLAlchemyEnum(LoginStatus), nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    provider = Column(SQLAlchemyEnum(AuthProvider), nullable=True)
    error_message = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)

    user = relationship("User")


class OAuthAccount(Base):
    """نموذج حسابات OAuth"""

    __tablename__ = "auth_oauth_accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(USERS_ID_FK, ondelete="CASCADE"), nullable=False)
    provider = Column(SQLAlchemyEnum(AuthProvider), nullable=False)
    provider_user_id = Column(String, nullable=False)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    scope = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="oauth_accounts")

    __table_args__ = (
        {'schema': None}  # يمكن تخصيص schema حسب الحاجة
    )


# إضافة العلاقات العكسية إلى نموذج المستخدم
User.tokens = relationship("Token", order_by=Token.created_at, back_populates="user")
User.sessions = relationship(
    "UserSession", order_by=UserSession.created_at, back_populates="user"
)
User.mfa_config = relationship("MFAConfiguration", uselist=False, back_populates="user")
User.oauth_accounts = relationship(
    "OAuthAccount", order_by=OAuthAccount.created_at, back_populates="user"
)

# تصدير النماذج والتعدادات
__all__ = [
    "Base",
    "TokenType",
    "TokenStatus",
    "AuthProvider",
    "MFAMethod",
    "LoginStatus",
    "Token",
    "UserSession",
    "MFAConfiguration",
    "MFAMethodConfiguration",
    "AuthLog",
    "OAuthAccount",
]
