#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.71: Product Variants Model

Support for product variants (size, color, etc.)
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from src.database import db


class VariantAttribute(db.Model):
    """
    Defines variant attributes like Size, Color, Material, etc.
    """

    __tablename__ = "variant_attributes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(50), unique=True, nullable=False
    )  # e.g., "Size", "Color"
    name_ar = db.Column(db.String(50))  # Arabic name
    description = db.Column(db.String(200))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    values = db.relationship(
        "VariantAttributeValue",
        back_populates="attribute",
        cascade="all, delete-orphan",
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "name_ar": self.name_ar,
            "description": self.description,
            "display_order": self.display_order,
            "is_active": self.is_active,
            "values": [v.to_dict() for v in self.values],
        }


class VariantAttributeValue(db.Model):
    """
    Defines possible values for variant attributes (e.g., Small, Medium, Large for Size)
    """

    __tablename__ = "variant_attribute_values"

    id = db.Column(db.Integer, primary_key=True)
    attribute_id = db.Column(
        db.Integer, db.ForeignKey("variant_attributes.id"), nullable=False
    )
    value = db.Column(db.String(50), nullable=False)  # e.g., "Small", "Red"
    value_ar = db.Column(db.String(50))
    color_code = db.Column(
        db.String(7)
    )  # Hex color for color variants, e.g., "#FF0000"
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    attribute = db.relationship("VariantAttribute", back_populates="values")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "attribute_id": self.attribute_id,
            "value": self.value,
            "value_ar": self.value_ar,
            "color_code": self.color_code,
            "display_order": self.display_order,
            "is_active": self.is_active,
        }


class ProductVariant(db.Model):
    """
    Represents a specific variant of a product (e.g., Red T-Shirt in Size Medium)
    """

    __tablename__ = "product_variants"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    sku = db.Column(db.String(50), unique=True)
    barcode = db.Column(db.String(50), unique=True)

    # Pricing
    price_adjustment = db.Column(db.Float, default=0)  # +/- from base price
    cost_adjustment = db.Column(db.Float, default=0)

    # Stock
    quantity = db.Column(db.Integer, default=0)
    min_stock_level = db.Column(db.Integer, default=5)

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)

    # Image
    image_url = db.Column(db.String(500))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    product = db.relationship("Product", back_populates="variants")
    variant_values = db.relationship(
        "ProductVariantValue", back_populates="variant", cascade="all, delete-orphan"
    )

    @property
    def variant_name(self) -> str:
        """Generate variant name from attribute values"""
        values = [pv.attribute_value.value for pv in self.variant_values]
        return " / ".join(values)

    @property
    def effective_price(self) -> float:
        """Calculate effective price including adjustment"""
        base_price = self.product.price if self.product else 0
        return base_price + self.price_adjustment

    @property
    def effective_cost(self) -> float:
        """Calculate effective cost including adjustment"""
        base_cost = self.product.cost if self.product else 0
        return base_cost + self.cost_adjustment

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "sku": self.sku,
            "barcode": self.barcode,
            "variant_name": self.variant_name,
            "price_adjustment": self.price_adjustment,
            "effective_price": self.effective_price,
            "cost_adjustment": self.cost_adjustment,
            "effective_cost": self.effective_cost,
            "quantity": self.quantity,
            "min_stock_level": self.min_stock_level,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "image_url": self.image_url,
            "attributes": [
                {
                    "attribute": pv.attribute_value.attribute.name,
                    "value": pv.attribute_value.value,
                    "color_code": pv.attribute_value.color_code,
                }
                for pv in self.variant_values
            ],
        }


class ProductVariantValue(db.Model):
    """
    Junction table linking product variants to their attribute values
    """

    __tablename__ = "product_variant_values"

    id = db.Column(db.Integer, primary_key=True)
    variant_id = db.Column(
        db.Integer, db.ForeignKey("product_variants.id"), nullable=False
    )
    attribute_value_id = db.Column(
        db.Integer, db.ForeignKey("variant_attribute_values.id"), nullable=False
    )

    # Relationships
    variant = db.relationship("ProductVariant", back_populates="variant_values")
    attribute_value = db.relationship("VariantAttributeValue")

    __table_args__ = (
        db.UniqueConstraint(
            "variant_id", "attribute_value_id", name="uq_variant_attribute_value"
        ),
    )


# =============================================================================
# Helper Functions
# =============================================================================


def create_default_attributes():
    """Create default variant attributes"""
    defaults = [
        {
            "name": "Size",
            "name_ar": "المقاس",
            "values": [
                {"value": "XS", "value_ar": "صغير جداً"},
                {"value": "S", "value_ar": "صغير"},
                {"value": "M", "value_ar": "متوسط"},
                {"value": "L", "value_ar": "كبير"},
                {"value": "XL", "value_ar": "كبير جداً"},
                {"value": "XXL", "value_ar": "كبير جداً جداً"},
            ],
        },
        {
            "name": "Color",
            "name_ar": "اللون",
            "values": [
                {"value": "Red", "value_ar": "أحمر", "color_code": "#EF4444"},
                {"value": "Blue", "value_ar": "أزرق", "color_code": "#3B82F6"},
                {"value": "Green", "value_ar": "أخضر", "color_code": "#22C55E"},
                {"value": "Black", "value_ar": "أسود", "color_code": "#000000"},
                {"value": "White", "value_ar": "أبيض", "color_code": "#FFFFFF"},
                {"value": "Yellow", "value_ar": "أصفر", "color_code": "#EAB308"},
            ],
        },
        {
            "name": "Material",
            "name_ar": "الخامة",
            "values": [
                {"value": "Cotton", "value_ar": "قطن"},
                {"value": "Polyester", "value_ar": "بوليستر"},
                {"value": "Leather", "value_ar": "جلد"},
                {"value": "Wool", "value_ar": "صوف"},
            ],
        },
    ]

    for attr_data in defaults:
        if not VariantAttribute.query.filter_by(name=attr_data["name"]).first():
            attr = VariantAttribute(
                name=attr_data["name"], name_ar=attr_data["name_ar"]
            )
            db.session.add(attr)
            db.session.flush()

            for i, val_data in enumerate(attr_data["values"]):
                val = VariantAttributeValue(
                    attribute_id=attr.id,
                    value=val_data["value"],
                    value_ar=val_data.get("value_ar"),
                    color_code=val_data.get("color_code"),
                    display_order=i,
                )
                db.session.add(val)

    db.session.commit()


def generate_variant_combinations(
    product_id: int, attribute_value_ids: List[List[int]]
) -> List[ProductVariant]:
    """
    Generate all possible variant combinations from attribute values.

    Args:
        product_id: The product ID
        attribute_value_ids: List of lists, each containing attribute value IDs for one attribute
                            e.g., [[1,2,3], [4,5]] for sizes [S,M,L] and colors [Red,Blue]

    Returns:
        List of created ProductVariant instances
    """
    from itertools import product as cartesian_product

    if not attribute_value_ids:
        return []

    combinations = list(cartesian_product(*attribute_value_ids))
    variants = []

    for combo in combinations:
        variant = ProductVariant(
            product_id=product_id,
            sku=f"P{product_id}-V{'-'.join(str(v) for v in combo)}",
        )
        db.session.add(variant)
        db.session.flush()

        for attr_val_id in combo:
            pvv = ProductVariantValue(
                variant_id=variant.id, attribute_value_id=attr_val_id
            )
            db.session.add(pvv)

        variants.append(variant)

    db.session.commit()
    return variants


__all__ = [
    "VariantAttribute",
    "VariantAttributeValue",
    "ProductVariant",
    "ProductVariantValue",
    "create_default_attributes",
    "generate_variant_combinations",
]
