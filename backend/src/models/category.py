# -*- coding: utf-8 -*-
# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
نموذج الفئات - Categories Model
/backend/src/models/category.py

نموذج قاعدة البيانات لإدارة فئات المنتجات
CANONICAL DEFINITION - Import this file for Category model
"""

from datetime import datetime, timezone

from src.database import db


class Category(db.Model):
    """نموذج الفئات - CANONICAL DEFINITION"""

    __tablename__ = "categories"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    name_ar = db.Column(db.String(100), nullable=True, index=True)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Self-referential relationships
    parent = db.relationship("Category", remote_side=[id], backref="children")
    # products relationship defined via backref in Product model

    def to_dict(self):
        """تحويل إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "name_ar": self.name_ar,
            "description": self.description,
            "parent_id": self.parent_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Category {self.name}>"
