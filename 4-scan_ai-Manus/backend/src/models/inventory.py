"""
FILE: backend/src/models/inventory.py | PURPOSE: Inventory database model | OWNER: Backend Team | LAST-AUDITED: 2025-12-08

Inventory Model

Represents inventory items and stock management.

Version: 1.0.0
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from ..core.database import Base


class Inventory(Base):
    """Inventory model for stock management"""

    __tablename__ = 'inventory'

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    # seeds, fertilizers, pesticides, tools, fuel, parts, other
    category = Column(String(100), nullable=False, index=True)
    sku = Column(String(100), unique=True, index=True)

    # Quantity Information
    quantity = Column(Float, nullable=False, default=0)
    unit = Column(String(50), default='kg')  # kg, g, l, ml, pcs, box, bag
    min_quantity = Column(Float)  # Alert threshold

    # Pricing
    price = Column(Float)

    # Supplier Information
    supplier = Column(String(255))
    location = Column(String(255))  # Storage location

    # Expiry
    expiry_date = Column(DateTime)

    # Additional Information
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)  # Soft delete

    def __repr__(self):
        return f"<Inventory(id={self.id}, name='{self.name}', quantity={self.quantity})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'sku': self.sku,
            'quantity': self.quantity,
            'unit': self.unit,
            'min_quantity': self.min_quantity,
            'price': self.price,
            'supplier': self.supplier,
            'location': self.location,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
