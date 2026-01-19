"""
FILE: backend/src/models/disease.py | PURPOSE: Disease database model | OWNER: Backend Team | LAST-AUDITED: 2025-12-08

Disease Model

Represents plant diseases and their information.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from ..core.database import Base


class Disease(Base):
    """Disease model for plant disease database"""

    __tablename__ = 'diseases'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    name_en = Column(String(255))
    scientific_name = Column(String(255))

    # Classification
    # fungal, bacterial, viral, pest, nutritional, environmental
    category = Column(String(100), nullable=False, index=True)
    # low, medium, high, critical
    severity = Column(String(50), default='medium')

    # Disease Information
    symptoms = Column(Text, nullable=False)
    causes = Column(Text)
    treatment = Column(Text)
    prevention = Column(Text)
    affected_crops = Column(Text)  # JSON array or comma-separated

    # Media
    image_url = Column(String(500))

    # Statistics
    cases_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)  # Soft delete

    def __repr__(self):
        return f"<Disease(id={self.id}, name='{self.name}', category='{self.category}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'scientific_name': self.scientific_name,
            'category': self.category,
            'severity': self.severity,
            'symptoms': self.symptoms,
            'causes': self.causes,
            'treatment': self.treatment,
            'prevention': self.prevention,
            'affected_crops': self.affected_crops,
            'image_url': self.image_url,
            'cases_count': self.cases_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
