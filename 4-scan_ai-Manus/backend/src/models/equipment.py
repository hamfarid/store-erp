"""
FILE: backend/src/models/equipment.py | PURPOSE: Equipment database model | OWNER: Backend Team | LAST-AUDITED: 2025-12-08

Equipment Model

Represents farm equipment and machinery.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from ..core.database import Base


class Equipment(Base):
    """Equipment model for farm machinery and tools"""

    __tablename__ = 'equipment'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    farm_id = Column(
        Integer,
        ForeignKey('farms.id'),
        nullable=True,
        index=True)

    # Basic Information
    name = Column(String(255), nullable=False)
    # tractor, harvester, irrigation, sprayer, other
    type = Column(String(100), nullable=False, index=True)
    brand = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100), unique=True, index=True)

    # Purchase Information
    purchase_date = Column(DateTime)
    purchase_price = Column(Float)

    # Status
    # operational, maintenance, out_of_service
    status = Column(String(50), default='operational')

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
    # farm = relationship("Farm", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment(id={self.id}, name='{self.name}', type='{self.type}')>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'name': self.name,
            'type': self.type,
            'brand': self.brand,
            'model': self.model,
            'serial_number': self.serial_number,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'purchase_price': self.purchase_price,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
