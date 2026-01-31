"""
FILE: backend/src/models/worker.py | PURPOSE: Worker database model | OWNER: Backend Team

Worker Model

Represents farm workers and staff.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from ..core.database import Base


class Worker(Base):
    """Worker model for farm labor management"""

    __tablename__ = 'workers'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    # Worker is usually assigned to a specific farm for management context
    # or could be per user if multi-farm? Assuming farm-level for now as per prompt implied CRUD structure.
    # But wait, Inventory/Equipment are farm-level logic.
    farm_id = Column(
        Integer,
        ForeignKey('farms.id'),
        nullable=False,
        index=True)

    # Personal Information
    name = Column(String(255), nullable=False)
    role = Column(String(100), nullable=False)  # e.g., Manager, Field Worker, machine operator
    phone = Column(String(50))
    email = Column(String(255))
    address = Column(Text)

    # Status
    # active, inactive, vacation, terminated
    status = Column(String(50), default='active')

    # Additional Information
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False)
    deleted_at = Column(DateTime)  # Soft delete

    def __repr__(self):
        return f"<Worker(id={self.id}, name='{self.name}', role='{self.role}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'name': self.name,
            'role': self.role,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
