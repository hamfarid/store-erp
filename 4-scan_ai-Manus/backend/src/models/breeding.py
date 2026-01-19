"""
FILE: backend/src/models/breeding.py | PURPOSE: Breeding database model | OWNER: Backend Team | LAST-AUDITED: 2025-12-08

Breeding Model

Represents breeding programs and genetic improvement projects.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from ..core.database import Base


class BreedingProgram(Base):
    """Breeding program model for genetic improvement"""

    __tablename__ = 'breeding_programs'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        index=True)
    farm_id = Column(
        Integer,
        ForeignKey('farms.id'),
        nullable=True,
        index=True)

    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    crop_type = Column(String(100), nullable=False, index=True)

    # Program Details
    objective = Column(Text, nullable=False)
    # hybridization, selection, mutation, tissue_culture, marker_assisted
    method = Column(String(100), nullable=False)
    # planning, in_progress, testing, completed, cancelled
    status = Column(String(50), default='planning')

    # Timeline
    start_date = Column(DateTime)
    expected_end_date = Column(DateTime)

    # Genetic Information
    parent_varieties = Column(Text)  # JSON or comma-separated
    target_traits = Column(Text)  # JSON or comma-separated

    # Progress
    progress = Column(Integer, default=0)  # 0-100 percentage

    # Additional Information
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)  # Soft delete

    # Relationships
    # user = relationship("User", back_populates="breeding_programs")
    # farm = relationship("Farm", back_populates="breeding_programs")

    def __repr__(self):
        return f"<BreedingProgram(id={self.id}, name='{self.name}', status='{self.status}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'farm_id': self.farm_id,
            'name': self.name,
            'description': self.description,
            'crop_type': self.crop_type,
            'objective': self.objective,
            'method': self.method,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'expected_end_date': self.expected_end_date.isoformat() if self.expected_end_date else None,
            'parent_varieties': self.parent_varieties,
            'target_traits': self.target_traits,
            'progress': self.progress,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
