"""
Base models for the application

This module provides abstract base classes that other models can inherit from.
"""

from datetime import datetime
from src.database import db


class BasicModel(db.Model):
    """
    Abstract base model with common fields for all entities.

    Provides:
    - id: Primary key
    - created_at: Timestamp of creation
    - updated_at: Timestamp of last update
    - is_active: Soft delete flag
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        """Convert model to dictionary representation"""
        return {
            "id": self.id,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
            "is_active": self.is_active,
        }

    def __repr__(self):
        """String representation of the model"""
        return f"<{self.__class__.__name__} {self.id}>"
