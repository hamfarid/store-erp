#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.84: Price History Tracking

Track historical price changes for products.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from src.database import db


class PriceHistory(db.Model):
    """
    P2.84: Price history model.

    Records every price change for audit and analytics.
    """

    __tablename__ = "price_history"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"))

    # Price changes
    price_type = db.Column(db.String(20), default="selling")  # selling, cost, wholesale
    old_price = db.Column(db.Float, nullable=False)
    new_price = db.Column(db.Float, nullable=False)

    # Percentage change
    change_percent = db.Column(db.Float)

    # Reason
    reason = db.Column(db.String(200))
    notes = db.Column(db.Text)

    # Reference (e.g., promotion, purchase)
    reference_type = db.Column(db.String(50))
    reference_id = db.Column(db.Integer)

    # User and timestamp
    changed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    product = db.relationship("Product", backref="price_history")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.old_price and self.new_price and self.old_price != 0:
            self.change_percent = (
                (self.new_price - self.old_price) / self.old_price
            ) * 100

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "variant_id": self.variant_id,
            "price_type": self.price_type,
            "old_price": self.old_price,
            "new_price": self.new_price,
            "change_percent": (
                round(self.change_percent, 2) if self.change_percent else 0
            ),
            "reason": self.reason,
            "notes": self.notes,
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "changed_by": self.changed_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PriceHistoryService:
    """Service for managing price history."""

    @staticmethod
    def record_price_change(
        product_id: int,
        old_price: float,
        new_price: float,
        price_type: str = "selling",
        variant_id: int = None,
        reason: str = None,
        notes: str = None,
        reference_type: str = None,
        reference_id: int = None,
        user_id: int = None,
    ) -> PriceHistory:
        """Record a price change."""
        if old_price == new_price:
            return None

        history = PriceHistory(
            product_id=product_id,
            variant_id=variant_id,
            price_type=price_type,
            old_price=old_price,
            new_price=new_price,
            reason=reason,
            notes=notes,
            reference_type=reference_type,
            reference_id=reference_id,
            changed_by=user_id,
        )

        db.session.add(history)
        db.session.commit()

        return history

    @staticmethod
    def get_product_price_history(
        product_id: int,
        price_type: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 50,
    ) -> List[PriceHistory]:
        """Get price history for a product."""
        query = PriceHistory.query.filter_by(product_id=product_id)

        if price_type:
            query = query.filter_by(price_type=price_type)
        if start_date:
            query = query.filter(PriceHistory.created_at >= start_date)
        if end_date:
            query = query.filter(PriceHistory.created_at <= end_date)

        return query.order_by(PriceHistory.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_price_at_date(
        product_id: int, date: datetime, price_type: str = "selling"
    ) -> Optional[float]:
        """Get the price of a product at a specific date."""
        history = (
            PriceHistory.query.filter(
                PriceHistory.product_id == product_id,
                PriceHistory.price_type == price_type,
                PriceHistory.created_at <= date,
            )
            .order_by(PriceHistory.created_at.desc())
            .first()
        )

        return history.new_price if history else None

    @staticmethod
    def get_average_price(
        product_id: int,
        start_date: datetime,
        end_date: datetime,
        price_type: str = "selling",
    ) -> Optional[float]:
        """Calculate average price in a period."""
        from sqlalchemy import func

        result = (
            db.session.query(func.avg(PriceHistory.new_price))
            .filter(
                PriceHistory.product_id == product_id,
                PriceHistory.price_type == price_type,
                PriceHistory.created_at >= start_date,
                PriceHistory.created_at <= end_date,
            )
            .scalar()
        )

        return float(result) if result else None


__all__ = ["PriceHistory", "PriceHistoryService"]
