"""
FILE: backend/src/models/tenant.py | PURPOSE: Tenant model for multi-tenancy
OWNER: Backend Team | LAST-AUDITED: 2026-01-31

Tenant Model - Multi-tenant Support

Represents tenants (organizations) for data isolation in enterprise deployments.

Version: 1.0.0
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, JSON
from sqlalchemy.orm import relationship

from ..core.database import Base


class Tenant(Base):
    """Tenant model for multi-tenant data isolation"""

    __tablename__ = 'tenants'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Tenant Identification
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255))
    slug = Column(String(100), unique=True, nullable=False, index=True)
    
    # Contact Information
    email = Column(String(255), index=True)
    phone = Column(String(50))
    website = Column(String(255))
    
    # Address
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100), default='Saudi Arabia')
    
    # Branding
    logo_url = Column(String(500))
    primary_color = Column(String(20), default='#0F6CBD')
    
    # Subscription & Limits
    plan = Column(String(50), default='free')  # free, pro, enterprise
    max_users = Column(Integer, default=5)
    max_farms = Column(Integer, default=10)
    max_diagnoses_per_month = Column(Integer, default=100)
    
    # Features (JSON for flexibility)
    features = Column(JSON, default=dict)
    settings = Column(JSON, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime)
    
    # Billing
    billing_email = Column(String(255))
    billing_address = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    deleted_at = Column(DateTime)  # Soft delete
    
    # Relationships (will be configured in relationships.py)
    # users = relationship("User", back_populates="tenant")
    # farms = relationship("Farm", back_populates="tenant")

    def __repr__(self):
        return f"<Tenant(id={self.id}, name='{self.name}', slug='{self.slug}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'name_ar': self.name_ar,
            'slug': self.slug,
            'email': self.email,
            'phone': self.phone,
            'website': self.website,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'logo_url': self.logo_url,
            'primary_color': self.primary_color,
            'plan': self.plan,
            'max_users': self.max_users,
            'max_farms': self.max_farms,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'features': self.features or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def has_feature(self, feature_name: str) -> bool:
        """Check if tenant has a specific feature enabled"""
        if not self.features:
            return False
        return self.features.get(feature_name, False)

    def get_setting(self, key: str, default=None):
        """Get a tenant-specific setting"""
        if not self.settings:
            return default
        return self.settings.get(key, default)

    def can_add_user(self, current_count: int) -> bool:
        """Check if tenant can add more users"""
        return current_count < self.max_users

    def can_add_farm(self, current_count: int) -> bool:
        """Check if tenant can add more farms"""
        return current_count < self.max_farms

