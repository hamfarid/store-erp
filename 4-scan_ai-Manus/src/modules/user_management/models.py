"""
/home/ubuntu/implemented_files/v3/src/modules/user_management/models.py

نماذج قاعدة البيانات لمديول إدارة المستخدمين

يوفر هذا الملف نماذج قاعدة البيانات لمديول إدارة المستخدمين في نظام Gaara ERP.
"""

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Integer,
    ForeignKey,
    Table,
    Text,
    JSON,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ...database import Base

# ثوابت الجداول
USERS_TABLE_ID = "users.id"
ROLES_TABLE_ID = "roles.id"
ORGANIZATIONS_TABLE_ID = "organizations.id"

# جدول العلاقة بين المستخدمين والأدوار
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String(36), ForeignKey(USERS_TABLE_ID), primary_key=True),
    Column("role_id", String(36), ForeignKey(ROLES_TABLE_ID), primary_key=True),
    Column("created_at", DateTime, default=func.now()),
    Column("created_by", String(36), ForeignKey(USERS_TABLE_ID)),
)


class Gender(str, enum.Enum):
    """تعداد الجنس"""

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class User(Base):
    """نموذج المستخدم"""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_system = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    updated_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    organization_id = Column(
        String(36), ForeignKey(ORGANIZATIONS_TABLE_ID), nullable=True
    )
    password_history = Column(JSON, default=list)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    user_metadata = Column(JSON, default=dict)

    # العلاقات
    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    preferences = relationship(
        "UserPreference",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    organization = relationship("Organization", back_populates="users")

    # العلاقات الذاتية
    created_users = relationship(
        "User",
        foreign_keys=[created_by],
        backref="created_by_user",
        remote_side=[id],
    )
    updated_users = relationship(
        "User",
        foreign_keys=[updated_by],
        backref="updated_by_user",
        remote_side=[id],
    )

    def __repr__(self):
        return f"<User {self.username}>"


class UserProfile(Base):
    """نموذج الملف الشخصي للمستخدم"""

    __tablename__ = "user_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey(USERS_TABLE_ID), unique=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)
    avatar = Column(String(255), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    updated_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    profile_metadata = Column(JSON, default=dict)

    # العلاقات
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile {self.user_id}>"


class UserPreference(Base):
    """نموذج تفضيلات المستخدم"""

    __tablename__ = "user_preferences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey(USERS_TABLE_ID), unique=True, nullable=False)
    language = Column(String(10), default="ar")
    timezone = Column(String(50), default="Africa/Cairo")
    date_format = Column(String(20), default="YYYY-MM-DD")
    time_format = Column(String(20), default="HH:mm:ss")
    theme = Column(String(20), default="light")
    notifications_enabled = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    push_notifications = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    updated_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    preference_metadata = Column(JSON, default=dict)

    # العلاقات
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference {self.user_id}>"


class Role(Base):
    """نموذج الدور"""

    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_system = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    updated_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    role_metadata = Column(JSON, default=dict)

    # العلاقات
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship(
        "Permission", secondary="role_permissions", back_populates="roles"
    )

    def __repr__(self):
        return f"<Role {self.name}>"


class UserRole(Base):
    """نموذج علاقة المستخدم بالدور"""

    __tablename__ = "user_role_assignments"

    user_id = Column(String(36), ForeignKey(USERS_TABLE_ID), primary_key=True)
    role_id = Column(String(36), ForeignKey(ROLES_TABLE_ID), primary_key=True)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)

    def __repr__(self):
        return f"<UserRole {self.user_id}:{self.role_id}>"


class UserSession(Base):
    """نموذج جلسة المستخدم"""

    __tablename__ = "user_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    session_metadata = Column(JSON, default=dict)

    # العلاقات
    user = relationship("User", backref="sessions")

    def __repr__(self):
        return f"<UserSession {self.user_id}:{self.token[:8]}...>"


class Organization(Base):
    """نموذج المؤسسة"""

    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    logo = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    parent_id = Column(String(36), ForeignKey(ORGANIZATIONS_TABLE_ID), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    updated_by = Column(String(36), ForeignKey(USERS_TABLE_ID), nullable=True)
    org_metadata = Column(JSON, default=dict)

    # العلاقات
    users = relationship("User", back_populates="organization")
    parent = relationship("Organization", remote_side=[id], backref="branches")

    def __repr__(self):
        return f"<Organization {self.name}>"


# تصدير الدوال والكائنات
__all__ = [
    "User",
    "UserProfile",
    "UserPreference",
    "Role",
    "UserRole",
    "UserSession",
    "Organization",
    "Gender",
    "user_roles",
]
