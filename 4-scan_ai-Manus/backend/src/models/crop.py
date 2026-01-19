"""
FILE: backend/src/models/crop.py | PURPOSE: Crop database model | OWNER: Backend Team | LAST-AUDITED: 2025-12-08

Crop Model

Represents crop types and their characteristics.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from ..core.database import Base


class Crop(Base):
    """Crop model for crop database"""

    __tablename__ = 'crops'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    name_en = Column(String(255))
    scientific_name = Column(String(255))

    # Classification
    # vegetables, fruits, grains, herbs, trees, flowers
    category = Column(String(100), nullable=False, index=True)

    # Growing Information
    # spring, summer, fall, winter, year-round
    growing_season = Column(String(100))
    water_needs = Column(String(50), default='medium')  # low, medium, high
    sunlight_needs = Column(String(50), default='full')  # full, partial, shade

    # Environmental Requirements
    temperature_min = Column(Float)
    temperature_max = Column(Float)
    growth_duration = Column(Integer)  # days

    # Additional Information
    description = Column(Text)
    care_tips = Column(Text)
    common_diseases = Column(Text)  # JSON array or comma-separated
    image_url = Column(String(500))

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)  # Soft delete

    def __repr__(self):
        return f"<Crop(id={self.id}, name='{self.name}', category='{self.category}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'scientific_name': self.scientific_name,
            'category': self.category,
            'growing_season': self.growing_season,
            'water_needs': self.water_needs,
            'sunlight_needs': self.sunlight_needs,
            'temperature_min': self.temperature_min,
            'temperature_max': self.temperature_max,
            'growth_duration': self.growth_duration,
            'description': self.description,
            'care_tips': self.care_tips,
            'common_diseases': self.common_diseases,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
