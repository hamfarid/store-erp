"""
FILE: backend/src/models/diagnosis.py | PURPOSE: Diagnosis database model | OWNER: Backend Team | LAST-AUDITED: 2025-11-18

Diagnosis Model

Represents AI-powered plant disease diagnoses.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, Text

from ..core.database import Base


class Diagnosis(Base):
    """Diagnosis model for plant disease detection"""

    __tablename__ = 'diagnoses'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        index=True)
    farm_id = Column(Integer, ForeignKey('farms.id'), index=True)

    # Image Information
    image_url = Column(String(500), nullable=False)
    image_path = Column(String(500))
    thumbnail_url = Column(String(500))

    # Diagnosis Results
    disease = Column(String(255))  # Disease name
    disease_ar = Column(String(255))  # Disease name in Arabic
    confidence = Column(Float)  # Confidence score (0.0 - 1.0)
    severity = Column(String(50))  # low, medium, high, critical

    # AI Model Information
    model_name = Column(String(100))
    model_version = Column(String(50))
    processing_time = Column(Float)  # in seconds

    # Recommendations
    recommendations = Column(JSON)  # Array of treatment recommendations
    recommendations_ar = Column(JSON)  # Arabic recommendations

    # Additional Analysis
    affected_area_percentage = Column(Float)  # Percentage of affected area
    plant_health_score = Column(Float)  # Overall plant health (0-100)

    # Status
    # pending, processing, completed, failed
    status = Column(String(50), default='completed')
    error_message = Column(Text)

    # User Feedback
    user_rating = Column(Integer)  # 1-5 stars
    user_feedback = Column(Text)
    is_accurate = Column(String(20))  # yes, no, partially

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)
    deleted_at = Column(DateTime)  # Soft delete

    # Relationships
    # user = relationship("User", back_populates="diagnoses")
    # farm = relationship("Farm", back_populates="diagnoses")

    def __repr__(self):
        return f"<Diagnosis(id={self.id}, disease='{self.disease}', confidence={self.confidence})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'farm_id': self.farm_id,
            'image_url': self.image_url,
            'thumbnail_url': self.thumbnail_url,
            'disease': self.disease,
            'disease_ar': self.disease_ar,
            'confidence': self.confidence,
            'severity': self.severity,
            'model_name': self.model_name,
            'model_version': self.model_version,
            'recommendations': self.recommendations,
            'recommendations_ar': self.recommendations_ar,
            'affected_area_percentage': self.affected_area_percentage,
            'plant_health_score': self.plant_health_score,
            'status': self.status,
            'user_rating': self.user_rating,
            'is_accurate': self.is_accurate,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
