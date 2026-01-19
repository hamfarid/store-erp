"""
Tenant Models - SQLAlchemy Version
نماذج المستأجر - نسخة SQLAlchemy

Multi-tenancy models for Gaara ERP using SQLAlchemy.
Compatible with Flask and the existing database infrastructure.

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17
"""

from __future__ import annotations

import uuid
import secrets
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional, List, Dict, Any

from sqlalchemy import (
    Column, String, Boolean, Integer, DateTime, Text,
    ForeignKey, JSON, Enum, Index, UniqueConstraint,
    Numeric, event
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

# Import the db instance from your Flask app
try:
    from src.models.user import db
except ImportError:
    try:
        from flask_sqlalchemy import SQLAlchemy
        db = SQLAlchemy()
    except ImportError:
        # Fallback for testing
        from sqlalchemy.ext.declarative import declarative_base
        db = type('db', (), {'Model': declarative_base()})()


class TenantPlan(db.Model):
    """
    خطة اشتراك المستأجر
    Subscription plan for tenants defining quotas and features.

    Attributes:
        id: UUID primary key
        name: Plan name in English
        name_ar: Plan name in Arabic
        code: Unique plan identifier (e.g., 'pro', 'enterprise')
        plan_type: Type of plan (free, basic, pro, enterprise, custom)
        max_users: Maximum allowed users
        max_storage_gb: Maximum storage in GB
        max_api_calls_per_day: Daily API call limit
        features: JSON dict of enabled features
        price_monthly: Monthly subscription price
        price_yearly: Yearly subscription price
        is_active: Whether plan is available for new subscriptions
    """

    __tablename__ = 'tenant_plans'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100), default='')
    code = Column(String(50), unique=True, nullable=False, index=True)
    plan_type = Column(
        String(20),
        default='basic',
        nullable=False
    )
    max_users = Column(Integer, default=5, nullable=False)
    max_storage_gb = Column(Integer, default=10, nullable=False)
    max_api_calls_per_day = Column(Integer, default=10000, nullable=False)
    max_modules = Column(Integer, default=10, nullable=False)
    features = Column(JSON, default=dict)
    price_monthly = Column(Numeric(10, 2), default=0)
    price_yearly = Column(Numeric(10, 2), default=0)
    currency = Column(String(3), default='SAR')
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tenants = relationship('Tenant', back_populates='plan', lazy='dynamic')

    def __repr__(self) -> str:
        return f"<TenantPlan {self.name} ({self.code})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'id': str(self.id),
            'name': self.name,
            'name_ar': self.name_ar,
            'code': self.code,
            'plan_type': self.plan_type,
            'max_users': self.max_users,
            'max_storage_gb': self.max_storage_gb,
            'max_api_calls_per_day': self.max_api_calls_per_day,
            'max_modules': self.max_modules,
            'features': self.features or {},
            'price_monthly': float(self.price_monthly) if self.price_monthly else 0,
            'price_yearly': float(self.price_yearly) if self.price_yearly else 0,
            'currency': self.currency,
            'is_active': self.is_active
        }

    def has_feature(self, feature_name: str) -> bool:
        """Check if feature is enabled in this plan."""
        return self.features.get(feature_name, False) if self.features else False


class Tenant(db.Model):
    """
    المستأجر الرئيسي
    Main tenant model representing an organization/company.

    Each tenant has:
    - Unique slug for URL identification
    - Dedicated PostgreSQL schema for data isolation
    - Optional custom domain support
    - Subscription plan with quotas

    Attributes:
        id: UUID primary key
        name: Organization name
        name_ar: Arabic organization name
        slug: URL-safe unique identifier
        schema_name: PostgreSQL schema name
        custom_domain: Optional custom domain
        logo: URL to organization logo
        plan_id: Foreign key to TenantPlan
        owner_id: Foreign key to User (owner)
        status: Tenant status (active, suspended, trial, etc.)
        is_active: Quick active check
        trial_ends_at: Trial period end date
        subscription_ends_at: Subscription expiry date
        settings: JSON tenant-specific settings
        metadata: JSON additional metadata
    """

    __tablename__ = 'tenants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255), default='')
    slug = Column(String(63), unique=True, nullable=False, index=True)
    schema_name = Column(String(63), unique=True, nullable=False)
    custom_domain = Column(String(255), unique=True, nullable=True, index=True)
    logo = Column(String(500), nullable=True)

    # Foreign keys
    plan_id = Column(UUID(as_uuid=True), ForeignKey('tenant_plans.id'), nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Status
    status = Column(String(20), default='trial', nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Dates
    trial_ends_at = Column(DateTime, nullable=True)
    subscription_ends_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # JSON fields
    settings = Column(JSON, default=dict)
    metadata = Column(JSON, default=dict)

    # Relationships
    plan = relationship('TenantPlan', back_populates='tenants')
    owner = relationship('User', foreign_keys=[owner_id])
    tenant_users = relationship('TenantUser', back_populates='tenant', lazy='dynamic',
                                cascade='all, delete-orphan')
    extended_settings = relationship('TenantSettings', back_populates='tenant',
                                     uselist=False, cascade='all, delete-orphan')
    invitations = relationship('TenantInvitation', back_populates='tenant',
                               lazy='dynamic', cascade='all, delete-orphan')

    # Indexes
    __table_args__ = (
        Index('ix_tenant_status_active', 'status', 'is_active'),
    )

    def __repr__(self) -> str:
        return f"<Tenant {self.name} ({self.slug})>"

    @hybrid_property
    def is_trial(self) -> bool:
        """Check if tenant is in trial period."""
        return self.status == 'trial'

    @hybrid_property
    def is_subscription_active(self) -> bool:
        """Check if subscription is currently active."""
        if self.status == 'trial':
            return self.trial_ends_at is None or self.trial_ends_at > datetime.utcnow()
        if self.subscription_ends_at is None:
            return False
        return self.subscription_ends_at > datetime.utcnow()

    def to_dict(self, include_plan: bool = True, include_stats: bool = False) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        data = {
            'id': str(self.id),
            'name': self.name,
            'name_ar': self.name_ar,
            'slug': self.slug,
            'schema_name': self.schema_name,
            'custom_domain': self.custom_domain,
            'logo': self.logo,
            'status': self.status,
            'is_active': self.is_active,
            'trial_ends_at': self.trial_ends_at.isoformat() if self.trial_ends_at else None,
            'subscription_ends_at': self.subscription_ends_at.isoformat() if self.subscription_ends_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'settings': self.settings or {}
        }

        if include_plan and self.plan:
            data['plan'] = self.plan.to_dict()

        if include_stats:
            data['stats'] = {
                'users_count': self.tenant_users.filter_by(is_active=True).count(),
                'storage_used': self.metadata.get('storage_used', 0) if self.metadata else 0
            }

        return data

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a tenant-specific setting."""
        if self.settings:
            return self.settings.get(key, default)
        return default


class TenantUser(db.Model):
    """
    ربط المستخدم بالمستأجر
    Mapping between users and tenants with roles.

    A user can belong to multiple tenants with different roles.

    Attributes:
        id: UUID primary key
        tenant_id: Foreign key to Tenant
        user_id: Foreign key to User
        role: User's role in this tenant (owner, admin, manager, member, viewer)
        is_primary: Is this user's primary tenant
        permissions: Additional permissions JSON
        is_active: Is membership active
        joined_at: When user joined tenant
        last_accessed_at: Last access timestamp
    """

    __tablename__ = 'tenant_users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'),
                       nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role = Column(String(20), default='member', nullable=False)
    is_primary = Column(Boolean, default=False)
    permissions = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_accessed_at = Column(DateTime, nullable=True)

    # Relationships
    tenant = relationship('Tenant', back_populates='tenant_users')
    user = relationship('User')

    # Constraints
    __table_args__ = (
        UniqueConstraint('tenant_id', 'user_id', name='uq_tenant_user'),
        Index('ix_tenant_user_lookup', 'tenant_id', 'user_id'),
        Index('ix_user_primary', 'user_id', 'is_primary'),
    )

    def __repr__(self) -> str:
        return f"<TenantUser {self.user_id} @ {self.tenant_id} ({self.role})>"

    def to_dict(self, include_user: bool = True) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        data = {
            'id': str(self.id),
            'tenant_id': str(self.tenant_id),
            'role': self.role,
            'is_primary': self.is_primary,
            'permissions': self.permissions or {},
            'is_active': self.is_active,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None
        }

        if include_user and self.user:
            data['user'] = {
                'id': self.user.id,
                'email': self.user.email,
                'username': getattr(self.user, 'username', self.user.email),
                'name': getattr(self.user, 'full_name', None) or self.user.email
            }

        return data

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        # Owner and admin have all permissions
        if self.role in ['owner', 'admin']:
            return True
        if self.permissions:
            return self.permissions.get(permission, False)
        return False

    def update_last_access(self) -> None:
        """Update the last_accessed_at timestamp."""
        self.last_accessed_at = datetime.utcnow()


class TenantSettings(db.Model):
    """
    إعدادات المستأجر الموسعة
    Extended settings for a tenant.

    Attributes:
        id: UUID primary key
        tenant_id: One-to-one relation with Tenant
        timezone: Tenant's timezone
        language: Primary language
        date_format: Preferred date format
        currency: Primary currency
        fiscal_year_start_month: Month fiscal year starts
        modules_enabled: List of enabled module codes
        theme_settings: UI theme configuration
        notification_settings: Notification preferences
        security_settings: Security configuration
    """

    __tablename__ = 'tenant_settings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'),
                       unique=True, nullable=False)

    # Localization
    timezone = Column(String(50), default='Asia/Riyadh')
    language = Column(String(10), default='ar')
    secondary_language = Column(String(10), default='en')
    date_format = Column(String(20), default='YYYY-MM-DD')
    time_format = Column(String(10), default='24h')

    # Business
    currency = Column(String(3), default='SAR')
    currency_symbol = Column(String(5), default='ر.س')
    fiscal_year_start_month = Column(Integer, default=1)

    # Configuration
    modules_enabled = Column(JSON, default=list)
    theme_settings = Column(JSON, default=dict)
    notification_settings = Column(JSON, default=dict)
    security_settings = Column(JSON, default=dict)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tenant = relationship('Tenant', back_populates='extended_settings')

    def __repr__(self) -> str:
        return f"<TenantSettings for {self.tenant_id}>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'timezone': self.timezone,
            'language': self.language,
            'secondary_language': self.secondary_language,
            'date_format': self.date_format,
            'time_format': self.time_format,
            'currency': self.currency,
            'currency_symbol': self.currency_symbol,
            'fiscal_year_start_month': self.fiscal_year_start_month,
            'modules_enabled': self.modules_enabled or [],
            'theme_settings': self.theme_settings or {},
            'notification_settings': self.notification_settings or {},
            'security_settings': self.security_settings or {}
        }

    def is_module_enabled(self, module_code: str) -> bool:
        """Check if a module is enabled."""
        if self.modules_enabled:
            return module_code in self.modules_enabled
        return False


class TenantInvitation(db.Model):
    """
    دعوة للانضمام إلى مستأجر
    Invitation to join a tenant.

    Attributes:
        id: UUID primary key
        tenant_id: Foreign key to Tenant
        email: Email of invitee
        role: Role to assign on join
        token: Unique invitation token
        invited_by_id: User who sent invitation
        message: Optional invitation message
        expires_at: Invitation expiry
        accepted_at: When invitation was accepted
    """

    __tablename__ = 'tenant_invitations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'),
                       nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(20), default='member', nullable=False)
    token = Column(String(64), unique=True, nullable=False, index=True)
    invited_by_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    message = Column(Text, default='')
    expires_at = Column(DateTime, nullable=False)
    accepted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship('Tenant', back_populates='invitations')
    invited_by = relationship('User')

    # Constraints
    __table_args__ = (
        UniqueConstraint('tenant_id', 'email', name='uq_tenant_invitation'),
    )

    def __repr__(self) -> str:
        return f"<TenantInvitation {self.email} -> {self.tenant_id}>"

    @property
    def is_expired(self) -> bool:
        """Check if invitation has expired."""
        return datetime.utcnow() > self.expires_at

    @property
    def is_accepted(self) -> bool:
        """Check if invitation was accepted."""
        return self.accepted_at is not None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            'id': str(self.id),
            'email': self.email,
            'role': self.role,
            'message': self.message,
            'is_expired': self.is_expired,
            'is_accepted': self.is_accepted,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def create_invitation(
        cls,
        tenant_id: str,
        email: str,
        role: str,
        invited_by_id: int,
        message: str = '',
        days_valid: int = 7
    ) -> 'TenantInvitation':
        """
        Create a new invitation with auto-generated token.

        Args:
            tenant_id: UUID of tenant
            email: Email address to invite
            role: Role to assign
            invited_by_id: User ID sending invitation
            message: Optional invitation message
            days_valid: Days until expiry

        Returns:
            TenantInvitation: The created invitation
        """
        return cls(
            tenant_id=tenant_id,
            email=email,
            role=role,
            token=secrets.token_urlsafe(48),
            invited_by_id=invited_by_id,
            message=message,
            expires_at=datetime.utcnow() + timedelta(days=days_valid)
        )


# Event listeners for auto-generating schema_name
@event.listens_for(Tenant, 'before_insert')
def generate_schema_name(mapper, connection, target):
    """Auto-generate schema_name from slug before insert."""
    if not target.schema_name and target.slug:
        target.schema_name = f"tenant_{target.slug.replace('-', '_')}"


# Helper function to create all tables
def create_tenant_tables(engine):
    """Create all tenant-related tables."""
    TenantPlan.__table__.create(engine, checkfirst=True)
    Tenant.__table__.create(engine, checkfirst=True)
    TenantUser.__table__.create(engine, checkfirst=True)
    TenantSettings.__table__.create(engine, checkfirst=True)
    TenantInvitation.__table__.create(engine, checkfirst=True)
