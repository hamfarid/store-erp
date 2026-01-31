"""
FILE: backend/src/models/user.py | PURPOSE: User database model
OWNER: Backend Team | LAST-AUDITED: 2026-01-31

User Model - Multi-tenant Support

Represents system users with authentication, authorization, and tenant isolation.

Version: 2.0.0 - Added tenant_id for multi-tenancy
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    """User model for authentication and authorization"""

    __tablename__ = 'users'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Multi-tenancy
    tenant_id = Column(
        Integer,
        ForeignKey('tenants.id'),
        nullable=True,  # Nullable for system admins
        index=True
    )

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Profile
    name = Column(String(255), nullable=False)
    phone = Column(String(50))
    avatar_url = Column(String(500))

    # Authorization
    # ADMIN, MANAGER, USER, GUEST
    role = Column(String(50), default='USER', nullable=False)

    # MFA
    mfa_secret = Column(String(255))
    mfa_enabled = Column(Boolean, default=False)
    # JSON array of backup codes
    mfa_backup_codes = Column(Text)

    # Account Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime)

    # Password Management
    password_changed_at = Column(DateTime, default=datetime.utcnow)
    # JSON array of previous password hashes
    password_history = Column(Text)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    last_login_at = Column(DateTime)
    last_login_ip = Column(String(50))

    # Timestamps
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    # Soft delete
    deleted_at = Column(DateTime)

    # Relationships
    # farms = relationship("Farm", back_populates="owner")
    # diagnoses = relationship("Diagnosis", back_populates="user")
    # reports = relationship("Report", back_populates="user")
    notifications = relationship("Notification", back_populates="user", lazy="dynamic")

    def __repr__(self):
        return (
            f"<User(id={self.id}, email='{self.email}', "
            f"role='{self.role}')>"
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'avatar_url': self.avatar_url,
            'role': self.role,
            'mfa_enabled': self.mfa_enabled,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'last_login_at': (
                self.last_login_at.isoformat()
                if self.last_login_at else None
            ),
            'created_at': (
                self.created_at.isoformat()
                if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat()
                if self.updated_at else None
            ),
        }
