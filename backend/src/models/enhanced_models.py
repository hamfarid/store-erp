"""
Enhanced Models: Brand, ProductImage, StockMovement

This file contains ONLY new models that don't exist in inventory.py
DO NOT duplicate existing models here - it causes SQLAlchemy registry conflicts!
"""

from datetime import datetime
from sqlalchemy import Index
from src.database import db


class Brand(db.Model):
    """نموذج العلامات التجارية للمنتجات"""

    __tablename__ = "brands"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    name_ar = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    logo_url = db.Column(db.String(255))
    website = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # العلاقات
    products = db.relationship(
        "Product", backref="brand", lazy="dynamic", foreign_keys="Product.brand_id"
    )

    # فهارس مركبة
    __table_args__ = (
        Index("idx_brand_name", "name"),
        Index("idx_brand_name_ar", "name_ar"),
        Index("idx_brand_active", "is_active"),
        {"extend_existing": True},
    )

    def to_dict(self, include_products=False):
        data = {
            "id": self.id,
            "name": self.name,
            "name_ar": self.name_ar,
            "description": self.description,
            "description_ar": self.description_ar,
            "logo_url": self.logo_url,
            "website": self.website,
            "is_active": self.is_active,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }

        if include_products:
            data["products_count"] = self.products.filter_by(is_active=True).count()

        return data


class ProductImage(db.Model):
    """نموذج صور المنتجات (متعدد)"""

    __tablename__ = "product_images"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    image_url = db.Column(db.String(255), nullable=False)
    thumbnail_url = db.Column(db.String(255))
    medium_url = db.Column(db.String(255))
    large_url = db.Column(db.String(255))
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    alt_text = db.Column(db.String(255))
    alt_text_ar = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # فهارس مركبة
    __table_args__ = (
        Index("idx_image_product", "product_id"),
        Index("idx_image_primary", "product_id", "is_primary"),
        {"extend_existing": True},
    )

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "medium_url": self.medium_url,
            "large_url": self.large_url,
            "is_primary": self.is_primary,
            "sort_order": self.sort_order,
            "alt_text": self.alt_text,
            "alt_text_ar": self.alt_text_ar,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }


class StockMovement(db.Model):
    """نموذج حركات المخزون (Audit Trail)"""

    __tablename__ = "stock_movements"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False, index=True
    )
    movement_type = db.Column(
        db.String(20), nullable=False, index=True
    )  # 'in', 'out', 'transfer', 'adjustment'
    quantity = db.Column(db.Integer, nullable=False)
    quantity_before = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)
    reference_type = db.Column(db.String(50))  # 'sale', 'purchase'
    reference_id = db.Column(db.Integer)
    notes = db.Column(db.Text)
    notes_ar = db.Column(db.Text)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # العلاقات
    user = db.relationship("src.models.user.User", backref="stock_movements")

    # فهارس مركبة
    __table_args__ = (
        Index("idx_movement_product_date", "product_id", "created_at"),
        Index("idx_movement_warehouse_date", "warehouse_id", "created_at"),
        Index("idx_movement_type_date", "movement_type", "created_at"),
        Index("idx_movement_reference", "reference_type", "reference_id"),
        Index("idx_movement_user", "user_id"),
        {"extend_existing": True},
    )

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "quantity_before": self.quantity_before,
            "quantity_after": self.quantity_after,
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "notes": self.notes,
            "notes_ar": self.notes_ar,
            "user_id": self.user_id,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "user": self.user.to_dict() if self.user else None,
        }
