#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.81: Stock Movement Tracking

Models and services for tracking inventory movements.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from src.database import db
from enum import Enum


class MovementType(str, Enum):
    """Types of stock movements."""

    PURCHASE = "purchase"  # شراء
    SALE = "sale"  # بيع
    RETURN_IN = "return_in"  # مرتجع من عميل
    RETURN_OUT = "return_out"  # مرتجع لمورد
    ADJUSTMENT_IN = "adjustment_in"  # تعديل بالزيادة
    ADJUSTMENT_OUT = "adjustment_out"  # تعديل بالنقصان
    TRANSFER_IN = "transfer_in"  # تحويل داخل
    TRANSFER_OUT = "transfer_out"  # تحويل خارج
    DAMAGE = "damage"  # تالف
    EXPIRED = "expired"  # منتهي الصلاحية
    INITIAL = "initial"  # رصيد افتتاحي


class StockMovement(db.Model):
    """
    P2.81: Stock movement record.

    Tracks every change in inventory quantity.
    """

    __tablename__ = "stock_movements"

    id = db.Column(db.Integer, primary_key=True)

    # Product and warehouse
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), index=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"))

    # Movement details
    movement_type = db.Column(db.String(20), nullable=False, index=True)
    quantity = db.Column(
        db.Integer, nullable=False
    )  # Positive for in, negative for out

    # Stock levels
    quantity_before = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)

    # Cost tracking
    unit_cost = db.Column(db.Float, default=0)
    total_cost = db.Column(db.Float, default=0)

    # Reference
    reference_type = db.Column(
        db.String(50)
    )  # 'invoice', 'purchase_order', 'adjustment', etc.
    reference_id = db.Column(db.Integer)
    reference_number = db.Column(db.String(50))

    # Batch/Lot tracking
    batch_number = db.Column(db.String(50))
    expiry_date = db.Column(db.Date)

    # Notes and reason
    reason = db.Column(db.String(200))
    notes = db.Column(db.Text)

    # User and timestamps
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    product = db.relationship("Product", backref="stock_movements")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "warehouse_id": self.warehouse_id,
            "variant_id": self.variant_id,
            "movement_type": self.movement_type,
            "movement_type_ar": self._get_type_ar(),
            "quantity": self.quantity,
            "quantity_before": self.quantity_before,
            "quantity_after": self.quantity_after,
            "unit_cost": self.unit_cost,
            "total_cost": self.total_cost,
            "reference_type": self.reference_type,
            "reference_id": self.reference_id,
            "reference_number": self.reference_number,
            "batch_number": self.batch_number,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "reason": self.reason,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def _get_type_ar(self) -> str:
        """Get Arabic translation of movement type."""
        translations = {
            MovementType.PURCHASE.value: "شراء",
            MovementType.SALE.value: "بيع",
            MovementType.RETURN_IN.value: "مرتجع من عميل",
            MovementType.RETURN_OUT.value: "مرتجع لمورد",
            MovementType.ADJUSTMENT_IN.value: "تعديل بالزيادة",
            MovementType.ADJUSTMENT_OUT.value: "تعديل بالنقصان",
            MovementType.TRANSFER_IN.value: "تحويل داخل",
            MovementType.TRANSFER_OUT.value: "تحويل خارج",
            MovementType.DAMAGE.value: "تالف",
            MovementType.EXPIRED.value: "منتهي الصلاحية",
            MovementType.INITIAL.value: "رصيد افتتاحي",
        }
        return translations.get(self.movement_type, self.movement_type)


class StockMovementService:
    """Service for managing stock movements."""

    @staticmethod
    def record_movement(
        product_id: int,
        movement_type: str,
        quantity: int,
        warehouse_id: int = None,
        variant_id: int = None,
        unit_cost: float = 0,
        reference_type: str = None,
        reference_id: int = None,
        reference_number: str = None,
        batch_number: str = None,
        expiry_date: datetime = None,
        reason: str = None,
        notes: str = None,
        user_id: int = None,
    ) -> StockMovement:
        """
        Record a stock movement and update product quantity.

        Args:
            product_id: Product ID
            movement_type: Type of movement
            quantity: Quantity (positive for in, negative for out)
            warehouse_id: Optional warehouse ID
            variant_id: Optional variant ID
            unit_cost: Cost per unit
            reference_type: Type of reference document
            reference_id: ID of reference document
            reference_number: Number of reference document
            batch_number: Batch/Lot number
            expiry_date: Expiry date for batch
            reason: Reason for movement
            notes: Additional notes
            user_id: User making the change

        Returns:
            StockMovement record
        """
        from src.models.product import Product

        product = Product.query.get(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")

        # Get current quantity
        quantity_before = product.quantity or 0

        # Calculate new quantity
        quantity_after = quantity_before + quantity

        if quantity_after < 0:
            raise ValueError("Insufficient stock")

        # Create movement record
        movement = StockMovement(
            product_id=product_id,
            warehouse_id=warehouse_id,
            variant_id=variant_id,
            movement_type=movement_type,
            quantity=quantity,
            quantity_before=quantity_before,
            quantity_after=quantity_after,
            unit_cost=unit_cost,
            total_cost=abs(quantity) * unit_cost,
            reference_type=reference_type,
            reference_id=reference_id,
            reference_number=reference_number,
            batch_number=batch_number,
            expiry_date=expiry_date,
            reason=reason,
            notes=notes,
            created_by=user_id,
        )

        # Update product quantity
        product.quantity = quantity_after

        db.session.add(movement)
        db.session.commit()

        return movement

    @staticmethod
    def record_sale(
        product_id: int,
        quantity: int,
        invoice_id: int = None,
        invoice_number: str = None,
        user_id: int = None,
    ) -> StockMovement:
        """Record a sale (stock out)."""
        return StockMovementService.record_movement(
            product_id=product_id,
            movement_type=MovementType.SALE.value,
            quantity=-abs(quantity),
            reference_type="invoice",
            reference_id=invoice_id,
            reference_number=invoice_number,
            user_id=user_id,
        )

    @staticmethod
    def record_purchase(
        product_id: int,
        quantity: int,
        unit_cost: float,
        purchase_order_id: int = None,
        purchase_order_number: str = None,
        batch_number: str = None,
        expiry_date: datetime = None,
        user_id: int = None,
    ) -> StockMovement:
        """Record a purchase (stock in)."""
        return StockMovementService.record_movement(
            product_id=product_id,
            movement_type=MovementType.PURCHASE.value,
            quantity=abs(quantity),
            unit_cost=unit_cost,
            reference_type="purchase_order",
            reference_id=purchase_order_id,
            reference_number=purchase_order_number,
            batch_number=batch_number,
            expiry_date=expiry_date,
            user_id=user_id,
        )

    @staticmethod
    def record_adjustment(
        product_id: int,
        quantity: int,
        reason: str,
        notes: str = None,
        user_id: int = None,
    ) -> StockMovement:
        """Record a stock adjustment."""
        movement_type = (
            MovementType.ADJUSTMENT_IN.value
            if quantity > 0
            else MovementType.ADJUSTMENT_OUT.value
        )

        return StockMovementService.record_movement(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity,
            reference_type="adjustment",
            reason=reason,
            notes=notes,
            user_id=user_id,
        )

    @staticmethod
    def record_transfer(
        product_id: int,
        quantity: int,
        from_warehouse_id: int,
        to_warehouse_id: int,
        user_id: int = None,
    ) -> tuple:
        """
        Record a warehouse transfer.

        Returns:
            Tuple of (out_movement, in_movement)
        """
        # Record outgoing movement
        out_movement = StockMovementService.record_movement(
            product_id=product_id,
            movement_type=MovementType.TRANSFER_OUT.value,
            quantity=-abs(quantity),
            warehouse_id=from_warehouse_id,
            reference_type="transfer",
            user_id=user_id,
        )

        # Record incoming movement
        in_movement = StockMovementService.record_movement(
            product_id=product_id,
            movement_type=MovementType.TRANSFER_IN.value,
            quantity=abs(quantity),
            warehouse_id=to_warehouse_id,
            reference_type="transfer",
            reference_id=out_movement.id,
            user_id=user_id,
        )

        return out_movement, in_movement

    @staticmethod
    def get_product_history(
        product_id: int,
        start_date: datetime = None,
        end_date: datetime = None,
        movement_type: str = None,
        limit: int = 100,
    ) -> List[StockMovement]:
        """Get stock movement history for a product."""
        query = StockMovement.query.filter_by(product_id=product_id)

        if start_date:
            query = query.filter(StockMovement.created_at >= start_date)
        if end_date:
            query = query.filter(StockMovement.created_at <= end_date)
        if movement_type:
            query = query.filter_by(movement_type=movement_type)

        return query.order_by(StockMovement.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_movement_summary(
        product_id: int = None, start_date: datetime = None, end_date: datetime = None
    ) -> Dict[str, Any]:
        """Get summary of stock movements."""
        from sqlalchemy import func

        query = db.session.query(
            StockMovement.movement_type,
            func.sum(StockMovement.quantity).label("total_quantity"),
            func.sum(StockMovement.total_cost).label("total_cost"),
            func.count(StockMovement.id).label("count"),
        )

        if product_id:
            query = query.filter_by(product_id=product_id)
        if start_date:
            query = query.filter(StockMovement.created_at >= start_date)
        if end_date:
            query = query.filter(StockMovement.created_at <= end_date)

        results = query.group_by(StockMovement.movement_type).all()

        summary = {}
        for row in results:
            summary[row.movement_type] = {
                "quantity": row.total_quantity or 0,
                "cost": row.total_cost or 0,
                "count": row.count,
            }

        return summary


__all__ = ["StockMovement", "MovementType", "StockMovementService"]
