#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.82: Purchase Orders Model

Models for managing purchase orders from suppliers.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from src.database import db
from enum import Enum


class POStatus(str, Enum):
    """Purchase order statuses."""

    DRAFT = "draft"  # مسودة
    PENDING = "pending"  # معلق
    APPROVED = "approved"  # معتمد
    ORDERED = "ordered"  # تم الطلب
    PARTIAL = "partial"  # استلام جزئي
    RECEIVED = "received"  # مستلم
    CANCELLED = "cancelled"  # ملغي


class PurchaseOrder(db.Model):
    """
    P2.82: Purchase order model.
    """

    __tablename__ = "purchase_orders"

    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Supplier
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)

    # Warehouse
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"))

    # Dates
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    expected_date = db.Column(db.DateTime)
    received_date = db.Column(db.DateTime)

    # Status
    status = db.Column(db.String(20), default=POStatus.DRAFT.value, index=True)

    # Amounts
    subtotal = db.Column(db.Float, default=0)
    tax_amount = db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    shipping_cost = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    # Payment
    payment_terms = db.Column(db.String(100))
    payment_status = db.Column(db.String(20), default="pending")

    # Notes
    notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)

    # Approval
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    approved_at = db.Column(db.DateTime)

    # User and timestamps
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    supplier = db.relationship("Supplier", backref="purchase_orders")
    items = db.relationship(
        "PurchaseOrderItem",
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )
    receipts = db.relationship(
        "PurchaseReceipt", back_populates="purchase_order", cascade="all, delete-orphan"
    )

    def calculate_totals(self):
        """Calculate order totals."""
        self.subtotal = sum(item.total for item in self.items)
        self.total = (
            self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount
        )

    @property
    def status_ar(self) -> str:
        """Get Arabic status."""
        translations = {
            POStatus.DRAFT.value: "مسودة",
            POStatus.PENDING.value: "معلق",
            POStatus.APPROVED.value: "معتمد",
            POStatus.ORDERED.value: "تم الطلب",
            POStatus.PARTIAL.value: "استلام جزئي",
            POStatus.RECEIVED.value: "مستلم",
            POStatus.CANCELLED.value: "ملغي",
        }
        return translations.get(self.status, self.status)

    @property
    def received_quantity(self) -> int:
        """Get total received quantity."""
        return sum(item.received_quantity for item in self.items)

    @property
    def is_fully_received(self) -> bool:
        """Check if all items are received."""
        return all(item.received_quantity >= item.quantity for item in self.items)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "po_number": self.po_number,
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier.name if self.supplier else None,
            "warehouse_id": self.warehouse_id,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "expected_date": (
                self.expected_date.isoformat() if self.expected_date else None
            ),
            "received_date": (
                self.received_date.isoformat() if self.received_date else None
            ),
            "status": self.status,
            "status_ar": self.status_ar,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "shipping_cost": self.shipping_cost,
            "total": self.total,
            "payment_terms": self.payment_terms,
            "payment_status": self.payment_status,
            "notes": self.notes,
            "items": [item.to_dict() for item in self.items],
            "item_count": len(self.items),
            "is_fully_received": self.is_fully_received,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @staticmethod
    def generate_po_number() -> str:
        """Generate unique PO number."""
        today = datetime.utcnow()
        prefix = f"PO{today.strftime('%Y%m')}"

        last_po = (
            PurchaseOrder.query.filter(PurchaseOrder.po_number.like(f"{prefix}%"))
            .order_by(PurchaseOrder.id.desc())
            .first()
        )

        if last_po:
            last_num = int(last_po.po_number[-4:])
            new_num = last_num + 1
        else:
            new_num = 1

        return f"{prefix}{new_num:04d}"


class PurchaseOrderItem(db.Model):
    """Purchase order line item."""

    __tablename__ = "purchase_order_items"

    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(
        db.Integer, db.ForeignKey("purchase_orders.id"), nullable=False
    )
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"))

    # Quantities
    quantity = db.Column(db.Integer, nullable=False)
    received_quantity = db.Column(db.Integer, default=0)

    # Pricing
    unit_cost = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0)
    tax_rate = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    # Notes
    notes = db.Column(db.String(500))

    # Relationships
    purchase_order = db.relationship("PurchaseOrder", back_populates="items")
    product = db.relationship("Product")

    def calculate_total(self):
        """Calculate item total."""
        subtotal = self.quantity * self.unit_cost
        discount_amount = subtotal * (self.discount / 100) if self.discount else 0
        tax_amount = (
            (subtotal - discount_amount) * (self.tax_rate / 100) if self.tax_rate else 0
        )
        self.total = subtotal - discount_amount + tax_amount

    @property
    def pending_quantity(self) -> int:
        """Get pending quantity to receive."""
        return max(0, self.quantity - self.received_quantity)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "product_sku": self.product.sku if self.product else None,
            "variant_id": self.variant_id,
            "quantity": self.quantity,
            "received_quantity": self.received_quantity,
            "pending_quantity": self.pending_quantity,
            "unit_cost": self.unit_cost,
            "discount": self.discount,
            "tax_rate": self.tax_rate,
            "total": self.total,
            "notes": self.notes,
        }


class PurchaseReceipt(db.Model):
    """Record of goods received against a PO."""

    __tablename__ = "purchase_receipts"

    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False)
    purchase_order_id = db.Column(
        db.Integer, db.ForeignKey("purchase_orders.id"), nullable=False
    )

    # Receipt date
    receipt_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Notes
    notes = db.Column(db.Text)

    # User
    received_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    purchase_order = db.relationship("PurchaseOrder", back_populates="receipts")
    items = db.relationship(
        "PurchaseReceiptItem", back_populates="receipt", cascade="all, delete-orphan"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "receipt_number": self.receipt_number,
            "purchase_order_id": self.purchase_order_id,
            "po_number": self.purchase_order.po_number if self.purchase_order else None,
            "receipt_date": (
                self.receipt_date.isoformat() if self.receipt_date else None
            ),
            "notes": self.notes,
            "items": [item.to_dict() for item in self.items],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PurchaseReceiptItem(db.Model):
    """Line item for purchase receipt."""

    __tablename__ = "purchase_receipt_items"

    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(
        db.Integer, db.ForeignKey("purchase_receipts.id"), nullable=False
    )
    po_item_id = db.Column(
        db.Integer, db.ForeignKey("purchase_order_items.id"), nullable=False
    )
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    # Quantity
    quantity_received = db.Column(db.Integer, nullable=False)

    # Batch tracking
    batch_number = db.Column(db.String(50))
    expiry_date = db.Column(db.Date)

    # Notes
    notes = db.Column(db.String(500))

    # Relationships
    receipt = db.relationship("PurchaseReceipt", back_populates="items")
    po_item = db.relationship("PurchaseOrderItem")
    product = db.relationship("Product")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "po_item_id": self.po_item_id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "quantity_received": self.quantity_received,
            "batch_number": self.batch_number,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "notes": self.notes,
        }


__all__ = [
    "PurchaseOrder",
    "PurchaseOrderItem",
    "PurchaseReceipt",
    "PurchaseReceiptItem",
    "POStatus",
]
