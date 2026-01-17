#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.93: Inventory Alerts Service

Service for monitoring inventory levels and sending alerts.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from src.database import db
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)


class AlertType:
    """Alert types."""

    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    OVERSTOCK = "overstock"
    EXPIRING_SOON = "expiring_soon"
    EXPIRED = "expired"
    SLOW_MOVING = "slow_moving"
    REORDER_POINT = "reorder_point"


class AlertPriority:
    """Alert priority levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class InventoryAlert(db.Model):
    """
    P2.93: Inventory alert model.
    """

    __tablename__ = "inventory_alerts"

    id = db.Column(db.Integer, primary_key=True)

    # Alert details
    alert_type = db.Column(db.String(30), nullable=False, index=True)
    priority = db.Column(db.String(20), default=AlertPriority.MEDIUM)

    # Product
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"))

    # Alert message
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)

    # Data
    current_value = db.Column(db.Float)
    threshold_value = db.Column(db.Float)

    # Status
    is_read = db.Column(db.Boolean, default=False)
    is_resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    product = db.relationship("Product", backref="alerts")

    @property
    def type_ar(self) -> str:
        """Get Arabic alert type."""
        translations = {
            AlertType.LOW_STOCK: "مخزون منخفض",
            AlertType.OUT_OF_STOCK: "نفاد المخزون",
            AlertType.OVERSTOCK: "فائض مخزون",
            AlertType.EXPIRING_SOON: "قرب انتهاء الصلاحية",
            AlertType.EXPIRED: "منتهي الصلاحية",
            AlertType.SLOW_MOVING: "بطيء الحركة",
            AlertType.REORDER_POINT: "نقطة إعادة الطلب",
        }
        return translations.get(self.alert_type, self.alert_type)

    @property
    def priority_ar(self) -> str:
        """Get Arabic priority."""
        translations = {
            AlertPriority.CRITICAL: "حرج",
            AlertPriority.HIGH: "عالي",
            AlertPriority.MEDIUM: "متوسط",
            AlertPriority.LOW: "منخفض",
        }
        return translations.get(self.priority, self.priority)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "alert_type": self.alert_type,
            "type_ar": self.type_ar,
            "priority": self.priority,
            "priority_ar": self.priority_ar,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "warehouse_id": self.warehouse_id,
            "title": self.title,
            "message": self.message,
            "current_value": self.current_value,
            "threshold_value": self.threshold_value,
            "is_read": self.is_read,
            "is_resolved": self.is_resolved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class InventoryAlertsService:
    """Service for managing inventory alerts."""

    @staticmethod
    def check_all_alerts() -> List[InventoryAlert]:
        """Run all inventory checks and create alerts."""
        alerts = []

        alerts.extend(InventoryAlertsService.check_low_stock())
        alerts.extend(InventoryAlertsService.check_out_of_stock())
        alerts.extend(InventoryAlertsService.check_expiring_products())
        alerts.extend(InventoryAlertsService.check_reorder_points())

        return alerts

    @staticmethod
    def check_low_stock() -> List[InventoryAlert]:
        """Check for products with low stock."""
        from src.models.inventory import Product

        low_stock = Product.query.filter(
            Product.quantity > 0, Product.quantity <= Product.min_stock_level
        ).all()

        alerts = []
        for product in low_stock:
            # Check if alert already exists
            existing = InventoryAlert.query.filter(
                InventoryAlert.product_id == product.id,
                InventoryAlert.alert_type == AlertType.LOW_STOCK,
                InventoryAlert.is_resolved == False,
            ).first()

            if not existing:
                alert = InventoryAlert(
                    alert_type=AlertType.LOW_STOCK,
                    priority=(
                        AlertPriority.HIGH
                        if product.quantity <= product.min_stock_level / 2
                        else AlertPriority.MEDIUM
                    ),
                    product_id=product.id,
                    title=f"مخزون منخفض: {product.name}",
                    message=f"الكمية الحالية ({product.quantity}) أقل من الحد الأدنى ({product.min_stock_level})",
                    current_value=product.quantity,
                    threshold_value=product.min_stock_level,
                )
                db.session.add(alert)
                alerts.append(alert)

        db.session.commit()
        return alerts

    @staticmethod
    def check_out_of_stock() -> List[InventoryAlert]:
        """Check for out of stock products."""
        from src.models.inventory import Product

        out_of_stock = Product.query.filter(Product.quantity <= 0).all()

        alerts = []
        for product in out_of_stock:
            existing = InventoryAlert.query.filter(
                InventoryAlert.product_id == product.id,
                InventoryAlert.alert_type == AlertType.OUT_OF_STOCK,
                InventoryAlert.is_resolved == False,
            ).first()

            if not existing:
                alert = InventoryAlert(
                    alert_type=AlertType.OUT_OF_STOCK,
                    priority=AlertPriority.CRITICAL,
                    product_id=product.id,
                    title=f"نفاد المخزون: {product.name}",
                    message=f"المنتج غير متوفر في المخزون",
                    current_value=product.quantity,
                    threshold_value=0,
                )
                db.session.add(alert)
                alerts.append(alert)

        db.session.commit()
        return alerts

    @staticmethod
    def check_expiring_products(days_threshold: int = 30) -> List[InventoryAlert]:
        """Check for products expiring soon."""
        from src.models.inventory import Lot as Batch

        cutoff_date = datetime.utcnow().date() + timedelta(days=days_threshold)

        expiring = Batch.query.filter(
            Batch.expiry_date <= cutoff_date,
            Batch.expiry_date >= datetime.utcnow().date(),
            Batch.quantity > 0,
        ).all()

        alerts = []
        for batch in expiring:
            existing = InventoryAlert.query.filter(
                InventoryAlert.product_id == batch.product_id,
                InventoryAlert.alert_type == AlertType.EXPIRING_SOON,
                InventoryAlert.is_resolved == False,
            ).first()

            if not existing:
                days_until = (batch.expiry_date - datetime.utcnow().date()).days
                priority = (
                    AlertPriority.CRITICAL
                    if days_until <= 7
                    else (
                        AlertPriority.HIGH if days_until <= 14 else AlertPriority.MEDIUM
                    )
                )

                alert = InventoryAlert(
                    alert_type=AlertType.EXPIRING_SOON,
                    priority=priority,
                    product_id=batch.product_id,
                    title=f"قرب انتهاء الصلاحية: {batch.product.name}",
                    message=f"الدفعة {batch.batch_number} تنتهي صلاحيتها خلال {days_until} يوم",
                    current_value=days_until,
                    threshold_value=days_threshold,
                )
                db.session.add(alert)
                alerts.append(alert)

        db.session.commit()
        return alerts

    @staticmethod
    def check_reorder_points() -> List[InventoryAlert]:
        """Check for products at reorder point."""
        from src.models.inventory import Product

        # Products at or below reorder point
        reorder = Product.query.filter(
            Product.quantity <= Product.reorder_point,
            Product.quantity > 0,
            Product.reorder_point > 0,
        ).all()

        alerts = []
        for product in reorder:
            existing = InventoryAlert.query.filter(
                InventoryAlert.product_id == product.id,
                InventoryAlert.alert_type == AlertType.REORDER_POINT,
                InventoryAlert.is_resolved == False,
            ).first()

            if not existing:
                alert = InventoryAlert(
                    alert_type=AlertType.REORDER_POINT,
                    priority=AlertPriority.MEDIUM,
                    product_id=product.id,
                    title=f"نقطة إعادة الطلب: {product.name}",
                    message=f"الكمية الحالية ({product.quantity}) وصلت لنقطة إعادة الطلب ({product.reorder_point})",
                    current_value=product.quantity,
                    threshold_value=product.reorder_point,
                )
                db.session.add(alert)
                alerts.append(alert)

        db.session.commit()
        return alerts

    @staticmethod
    def get_alerts(
        alert_type: str = None,
        priority: str = None,
        is_resolved: bool = None,
        product_id: int = None,
        limit: int = 50,
    ) -> List[InventoryAlert]:
        """Get alerts with filters."""
        query = InventoryAlert.query

        if alert_type:
            query = query.filter_by(alert_type=alert_type)
        if priority:
            query = query.filter_by(priority=priority)
        if is_resolved is not None:
            query = query.filter_by(is_resolved=is_resolved)
        if product_id:
            query = query.filter_by(product_id=product_id)

        return query.order_by(InventoryAlert.created_at.desc()).limit(limit).all()

    @staticmethod
    def mark_as_read(alert_ids: List[int]):
        """Mark alerts as read."""
        InventoryAlert.query.filter(InventoryAlert.id.in_(alert_ids)).update(
            {"is_read": True}, synchronize_session=False
        )
        db.session.commit()

    @staticmethod
    def resolve_alert(alert_id: int, user_id: int = None):
        """Resolve an alert."""
        alert = InventoryAlert.query.get(alert_id)
        if alert:
            alert.is_resolved = True
            alert.resolved_at = datetime.utcnow()
            alert.resolved_by = user_id
            db.session.commit()
        return alert

    @staticmethod
    def auto_resolve_alerts():
        """Auto-resolve alerts that are no longer valid."""
        from src.models.inventory import Product

        # Resolve low stock alerts for products no longer low
        low_stock_alerts = InventoryAlert.query.filter(
            InventoryAlert.alert_type == AlertType.LOW_STOCK,
            InventoryAlert.is_resolved == False,
        ).all()

        for alert in low_stock_alerts:
            product = Product.query.get(alert.product_id)
            if product and product.quantity > product.min_stock_level:
                alert.is_resolved = True
                alert.resolved_at = datetime.utcnow()

        # Resolve out of stock alerts
        oos_alerts = InventoryAlert.query.filter(
            InventoryAlert.alert_type == AlertType.OUT_OF_STOCK,
            InventoryAlert.is_resolved == False,
        ).all()

        for alert in oos_alerts:
            product = Product.query.get(alert.product_id)
            if product and product.quantity > 0:
                alert.is_resolved = True
                alert.resolved_at = datetime.utcnow()

        db.session.commit()

    @staticmethod
    def get_summary() -> Dict[str, Any]:
        """Get alert summary."""
        unresolved = InventoryAlert.query.filter_by(is_resolved=False)

        return {
            "total_unresolved": unresolved.count(),
            "critical": unresolved.filter_by(priority=AlertPriority.CRITICAL).count(),
            "high": unresolved.filter_by(priority=AlertPriority.HIGH).count(),
            "medium": unresolved.filter_by(priority=AlertPriority.MEDIUM).count(),
            "low": unresolved.filter_by(priority=AlertPriority.LOW).count(),
            "by_type": {
                AlertType.OUT_OF_STOCK: unresolved.filter_by(
                    alert_type=AlertType.OUT_OF_STOCK
                ).count(),
                AlertType.LOW_STOCK: unresolved.filter_by(
                    alert_type=AlertType.LOW_STOCK
                ).count(),
                AlertType.EXPIRING_SOON: unresolved.filter_by(
                    alert_type=AlertType.EXPIRING_SOON
                ).count(),
                AlertType.REORDER_POINT: unresolved.filter_by(
                    alert_type=AlertType.REORDER_POINT
                ).count(),
            },
        }


__all__ = ["InventoryAlert", "AlertType", "AlertPriority", "InventoryAlertsService"]
