"""
FILE: backend/src/models/user.py
PURPOSE: User database model
OWNER: Backend Team
LAST-AUDITED: 2025-11-18

User Model

Represents system users with authentication and authorization.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from ..core.database import Base


class User(Base):
    """User model for authentication and authorization"""

    __tablename__ = 'users'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

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

    def __repr__(self):
        return (
            f"<User(id={self.id}, email='{self.email}', "
            f"role='{self.role}')>"
        )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
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
