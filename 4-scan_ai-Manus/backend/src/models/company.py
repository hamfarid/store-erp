"""
FILE: backend/src/models/company.py | PURPOSE: Company database model | OWNER: Backend Team | LAST-AUDITED: 2025-12-08

Company Model

Represents companies (farms, suppliers, distributors, etc.).

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from ..core.database import Base


class Company(Base):
    """Company model for business entities"""

    __tablename__ = 'companies'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    name_en = Column(String(255))
    # farm, supplier, distributor, research, government, other
    type = Column(String(100), nullable=False, index=True)
    industry = Column(String(100))

    # Registration
    registration_number = Column(String(100), unique=True, index=True)

    # Contact Information
    email = Column(String(255), index=True)
    phone = Column(String(50))
    website = Column(String(255))

    # Address
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100), default='Saudi Arabia')

    # Additional Information
    description = Column(Text)
    employees_count = Column(Integer)
    founded_year = Column(Integer)
    logo_url = Column(String(500))

    # Status
    status = Column(String(50), default='active')  # active, inactive, pending

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)  # Soft delete

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', type='{self.type}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'type': self.type,
            'industry': self.industry,
            'registration_number': self.registration_number,
            'email': self.email,
            'phone': self.phone,
            'website': self.website,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'description': self.description,
            'employees_count': self.employees_count,
            'founded_year': self.founded_year,
            'logo_url': self.logo_url,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
