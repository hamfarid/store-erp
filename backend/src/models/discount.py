#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.75: Discount/Coupon System

Models for managing discounts and coupons.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from src.database import db
import secrets
import string


class DiscountType:
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    BUY_X_GET_Y = "buy_x_get_y"
    FREE_SHIPPING = "free_shipping"


class DiscountScope:
    ALL = "all"
    PRODUCT = "product"
    CATEGORY = "category"
    CUSTOMER = "customer"


class Discount(db.Model):
    """
    P2.75: Discount model for sales promotions.
    """

    __tablename__ = "discounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100))
    description = db.Column(db.Text)

    # Type and Value
    discount_type = db.Column(db.String(20), default=DiscountType.PERCENTAGE)
    value = db.Column(db.Float, nullable=False)  # Percentage or fixed amount
    max_discount = db.Column(db.Float)  # Maximum discount amount (for percentage)

    # Scope
    scope = db.Column(db.String(20), default=DiscountScope.ALL)

    # Conditions
    min_purchase = db.Column(db.Float, default=0)  # Minimum purchase amount
    min_quantity = db.Column(db.Integer, default=0)  # Minimum quantity

    # Buy X Get Y
    buy_quantity = db.Column(db.Integer)  # Buy X
    get_quantity = db.Column(db.Integer)  # Get Y
    get_discount = db.Column(db.Float)  # Discount on Y (usually 100%)

    # Validity
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Usage limits
    usage_limit = db.Column(db.Integer)  # Total usage limit
    usage_count = db.Column(db.Integer, default=0)
    per_customer_limit = db.Column(db.Integer)  # Per customer usage limit

    # Priority
    priority = db.Column(db.Integer, default=0)  # Higher = applied first
    stackable = db.Column(
        db.Boolean, default=False
    )  # Can be combined with other discounts

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    products = db.relationship(
        "DiscountProduct", back_populates="discount", cascade="all, delete-orphan"
    )
    categories = db.relationship(
        "DiscountCategory", back_populates="discount", cascade="all, delete-orphan"
    )
    coupons = db.relationship(
        "Coupon", back_populates="discount", cascade="all, delete-orphan"
    )

    @property
    def is_valid(self) -> bool:
        """Check if discount is currently valid."""
        now = datetime.utcnow()

        if not self.is_active:
            return False

        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False

        return True

    def calculate_discount(self, amount: float, quantity: int = 1) -> float:
        """Calculate discount amount for given purchase."""
        if not self.is_valid:
            return 0

        # Check minimum purchase
        if amount < self.min_purchase:
            return 0

        # Check minimum quantity
        if quantity < self.min_quantity:
            return 0

        discount_amount = 0

        if self.discount_type == DiscountType.PERCENTAGE:
            discount_amount = amount * (self.value / 100)
            if self.max_discount:
                discount_amount = min(discount_amount, self.max_discount)

        elif self.discount_type == DiscountType.FIXED:
            discount_amount = min(self.value, amount)

        return round(discount_amount, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "name_ar": self.name_ar,
            "description": self.description,
            "discount_type": self.discount_type,
            "value": self.value,
            "max_discount": self.max_discount,
            "scope": self.scope,
            "min_purchase": self.min_purchase,
            "min_quantity": self.min_quantity,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_active": self.is_active,
            "is_valid": self.is_valid,
            "usage_limit": self.usage_limit,
            "usage_count": self.usage_count,
            "stackable": self.stackable,
        }


class DiscountProduct(db.Model):
    """Links discounts to specific products."""

    __tablename__ = "discount_products"

    id = db.Column(db.Integer, primary_key=True)
    discount_id = db.Column(db.Integer, db.ForeignKey("discounts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    discount = db.relationship("Discount", back_populates="products")


class DiscountCategory(db.Model):
    """Links discounts to specific categories."""

    __tablename__ = "discount_categories"

    id = db.Column(db.Integer, primary_key=True)
    discount_id = db.Column(db.Integer, db.ForeignKey("discounts.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    discount = db.relationship("Discount", back_populates="categories")


class Coupon(db.Model):
    """
    P2.75: Coupon model for promotional codes.
    """

    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    discount_id = db.Column(db.Integer, db.ForeignKey("discounts.id"), nullable=False)

    # Additional restrictions
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.id")
    )  # For single customer
    first_purchase_only = db.Column(db.Boolean, default=False)

    # Validity
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Usage
    usage_limit = db.Column(db.Integer, default=1)
    usage_count = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    discount = db.relationship("Discount", back_populates="coupons")
    usages = db.relationship(
        "CouponUsage", back_populates="coupon", cascade="all, delete-orphan"
    )

    @property
    def is_valid(self) -> bool:
        """Check if coupon is currently valid."""
        now = datetime.utcnow()

        if not self.is_active:
            return False

        if self.start_date and now < self.start_date:
            return False

        if self.end_date and now > self.end_date:
            return False

        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False

        if not self.discount.is_valid:
            return False

        return True

    def can_use(self, customer_id: int = None) -> tuple:
        """Check if coupon can be used by customer."""
        if not self.is_valid:
            return False, "الكوبون غير صالح أو منتهي الصلاحية"

        if self.customer_id and self.customer_id != customer_id:
            return False, "هذا الكوبون مخصص لعميل آخر"

        # Check per-customer usage
        if customer_id and self.discount.per_customer_limit:
            customer_usage = CouponUsage.query.filter_by(
                coupon_id=self.id, customer_id=customer_id
            ).count()

            if customer_usage >= self.discount.per_customer_limit:
                return False, "لقد استخدمت هذا الكوبون الحد الأقصى من المرات"

        return True, None

    def apply(self, customer_id: int, order_id: int):
        """Record coupon usage."""
        usage = CouponUsage(
            coupon_id=self.id, customer_id=customer_id, order_id=order_id
        )
        db.session.add(usage)
        self.usage_count += 1
        self.discount.usage_count += 1
        db.session.commit()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "discount": self.discount.to_dict(),
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_active": self.is_active,
            "is_valid": self.is_valid,
            "usage_limit": self.usage_limit,
            "usage_count": self.usage_count,
        }

    @staticmethod
    def generate_code(length: int = 8, prefix: str = "") -> str:
        """Generate a unique coupon code."""
        chars = string.ascii_uppercase + string.digits
        while True:
            code = prefix + "".join(secrets.choice(chars) for _ in range(length))
            if not Coupon.query.filter_by(code=code).first():
                return code


class CouponUsage(db.Model):
    """Tracks coupon usage."""

    __tablename__ = "coupon_usages"

    id = db.Column(db.Integer, primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey("coupons.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("invoices.id"))
    used_at = db.Column(db.DateTime, default=datetime.utcnow)
    discount_amount = db.Column(db.Float)

    coupon = db.relationship("Coupon", back_populates="usages")


# =============================================================================
# Helper Functions
# =============================================================================


def get_applicable_discounts(
    product_ids: List[int] = None,
    category_ids: List[int] = None,
    customer_id: int = None,
    amount: float = 0,
) -> List[Discount]:
    """Get all applicable discounts for given criteria."""
    now = datetime.utcnow()

    query = Discount.query.filter(
        Discount.is_active,
        db.or_(Discount.start_date.is_(None), Discount.start_date <= now),
        db.or_(Discount.end_date.is_(None), Discount.end_date >= now),
        db.or_(
            Discount.usage_limit.is_(None), Discount.usage_count < Discount.usage_limit
        ),
        Discount.min_purchase <= amount,
    )

    discounts = query.order_by(Discount.priority.desc()).all()

    applicable = []
    for discount in discounts:
        if discount.scope == DiscountScope.ALL:
            applicable.append(discount)
        elif discount.scope == DiscountScope.PRODUCT and product_ids:
            product_discount_ids = [dp.product_id for dp in discount.products]
            if any(pid in product_discount_ids for pid in product_ids):
                applicable.append(discount)
        elif discount.scope == DiscountScope.CATEGORY and category_ids:
            cat_discount_ids = [dc.category_id for dc in discount.categories]
            if any(cid in cat_discount_ids for cid in category_ids):
                applicable.append(discount)

    return applicable


def validate_coupon(code: str, customer_id: int = None) -> tuple:
    """Validate a coupon code."""
    coupon = Coupon.query.filter_by(code=code.upper()).first()

    if not coupon:
        return None, "الكوبون غير موجود"

    can_use, error = coupon.can_use(customer_id)
    if not can_use:
        return None, error

    return coupon, None


__all__ = [
    "Discount",
    "DiscountType",
    "DiscountScope",
    "DiscountProduct",
    "DiscountCategory",
    "Coupon",
    "CouponUsage",
    "get_applicable_discounts",
    "validate_coupon",
]
