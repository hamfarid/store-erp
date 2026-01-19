"""
FILE: backend/src/models/farm.py | PURPOSE: Farm database model | OWNER: Backend Team | LAST-AUDITED: 2025-11-18

Farm Model

Represents agricultural farms managed by users.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from ..core.database import Base


class Farm(Base):
    """Farm model for agricultural land management"""

    __tablename__ = 'farms'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    owner_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        index=True)

    # Farm Details
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=False)
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)

    # Farm Specifications
    area = Column(Float, nullable=False)  # in hectares or acres
    area_unit = Column(String(20), default='hectare')  # hectare, acre, etc.
    crop_type = Column(String(100))  # wheat, corn, rice, tomato, etc.
    soil_type = Column(String(100))  # clay, sandy, loamy, etc.

    # Farm Status
    # active, inactive, archived
    is_active = Column(String(20), default='active')

    # Additional Information
    description = Column(Text)
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)
    deleted_at = Column(DateTime)  # Soft delete

    # Relationships
    # owner = relationship("User", back_populates="farms")
    # diagnoses = relationship("Diagnosis", back_populates="farm")
    # sensors = relationship("Sensor", back_populates="farm")

    def __repr__(self):
        return f"<Farm(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'location': self.location,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'area': self.area,
            'area_unit': self.area_unit,
            'crop_type': self.crop_type,
            'soil_type': self.soil_type,
            'is_active': self.is_active,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
