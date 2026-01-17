#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.58: Notification Service

Business logic for creating and managing notifications.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from src.database import db
from src.models.notification import Notification, NotificationPreferences

logger = logging.getLogger(__name__)


class NotificationService:
    """
    P2.58: Service for managing notifications.

    Handles notification creation, delivery, and management.
    """

    # ==========================================================================
    # Notification Types
    # ==========================================================================

    TYPES = {
        "info": {"icon": "ℹ️", "color": "blue"},
        "success": {"icon": "✅", "color": "green"},
        "warning": {"icon": "⚠️", "color": "yellow"},
        "error": {"icon": "❌", "color": "red"},
        "alert": {"icon": "🔔", "color": "purple"},
    }

    CATEGORIES = {
        "system": "System",
        "inventory": "Inventory",
        "sales": "Sales",
        "purchases": "Purchases",
        "security": "Security",
        "payment": "Payment",
        "report": "Report",
    }

    # ==========================================================================
    # Core Methods
    # ==========================================================================

    @staticmethod
    def create(
        user_id: int,
        title: str,
        message: str,
        type: str = "info",
        category: str = "system",
        priority: str = "normal",
        action_url: str = None,
        action_label: str = None,
        expires_at: datetime = None,
        metadata: dict = None,
    ) -> Notification:
        """
        Create a new notification.

        Args:
            user_id: Target user ID
            title: Notification title
            message: Notification message
            type: info, success, warning, error, alert
            category: system, inventory, sales, etc.
            priority: low, normal, high, urgent
            action_url: Optional action URL
            action_label: Optional action button label
            expires_at: Optional expiration date
            metadata: Optional additional data

        Returns:
            Created notification
        """
        notification = Notification.create_notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            category=category,
            priority=priority,
            action_url=action_url,
            action_label=action_label,
            expires_at=expires_at,
            metadata=metadata,
        )

        logger.info(f"P2.58: Created notification {notification.id} for user {user_id}")
        return notification

    @staticmethod
    def create_for_users(
        user_ids: List[int], title: str, message: str, **kwargs
    ) -> List[Notification]:
        """Create notifications for multiple users."""
        notifications = []
        for user_id in user_ids:
            notification = NotificationService.create(
                user_id=user_id, title=title, message=message, **kwargs
            )
            notifications.append(notification)
        return notifications

    @staticmethod
    def create_broadcast(title: str, message: str, **kwargs) -> List[Notification]:
        """Broadcast notification to all users."""
        from src.models.user import User

        user_ids = [u.id for u in User.query.filter_by(is_active=True).all()]
        return NotificationService.create_for_users(user_ids, title, message, **kwargs)

    # ==========================================================================
    # Query Methods
    # ==========================================================================

    @staticmethod
    def get_user_notifications(
        user_id: int,
        unread_only: bool = False,
        category: str = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Notification]:
        """Get notifications for a user."""
        query = Notification.query.filter_by(user_id=user_id)

        if unread_only:
            query = query.filter_by(is_read=False)

        if category:
            query = query.filter_by(category=category)

        # Exclude expired notifications
        query = query.filter(
            db.or_(
                Notification.expires_at.is_(None),
                Notification.expires_at > datetime.utcnow(),
            )
        )

        return (
            query.order_by(Notification.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """Get count of unread notifications."""
        return Notification.get_unread_count(user_id)

    @staticmethod
    def mark_as_read(notification_id: int, user_id: int) -> bool:
        """Mark a notification as read."""
        notification = Notification.query.filter_by(
            id=notification_id, user_id=user_id
        ).first()

        if notification:
            notification.mark_as_read()
            return True
        return False

    @staticmethod
    def mark_all_as_read(user_id: int):
        """Mark all notifications as read for a user."""
        Notification.mark_all_as_read(user_id)

    @staticmethod
    def delete_notification(notification_id: int, user_id: int) -> bool:
        """Delete a notification."""
        notification = Notification.query.filter_by(
            id=notification_id, user_id=user_id
        ).first()

        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_all_read(user_id: int) -> int:
        """Delete all read notifications for a user."""
        count = Notification.query.filter_by(user_id=user_id, is_read=True).delete()
        db.session.commit()
        return count

    # ==========================================================================
    # Predefined Notifications
    # ==========================================================================

    @staticmethod
    def notify_low_stock(
        user_id: int, product_name: str, quantity: int, min_level: int
    ):
        """Create low stock notification."""
        return NotificationService.create(
            user_id=user_id,
            title="Low Stock Alert",
            message=f'Product "{product_name}" is low on stock. Current: {quantity}, Minimum: {min_level}',
            type="warning",
            category="inventory",
            priority="high",
            action_url="/inventory/products",
            action_label="View Inventory",
            metadata={
                "product_name": product_name,
                "quantity": quantity,
                "min_level": min_level,
            },
        )

    @staticmethod
    def notify_new_order(
        user_id: int, order_number: str, total: float, customer_name: str
    ):
        """Create new order notification."""
        return NotificationService.create(
            user_id=user_id,
            title="New Order Received",
            message=f"New order #{order_number} from {customer_name}. Total: ${total:.2f}",
            type="success",
            category="sales",
            priority="normal",
            action_url=f"/sales/orders/{order_number}",
            action_label="View Order",
            metadata={
                "order_number": order_number,
                "total": total,
                "customer": customer_name,
            },
        )

    @staticmethod
    def notify_payment_received(user_id: int, invoice_number: str, amount: float):
        """Create payment received notification."""
        return NotificationService.create(
            user_id=user_id,
            title="Payment Received",
            message=f"Payment of ${amount:.2f} received for invoice #{invoice_number}",
            type="success",
            category="payment",
            priority="normal",
            action_url=f"/invoices/{invoice_number}",
            action_label="View Invoice",
            metadata={"invoice_number": invoice_number, "amount": amount},
        )

    @staticmethod
    def notify_payment_overdue(
        user_id: int, invoice_number: str, days_overdue: int, amount: float
    ):
        """Create payment overdue notification."""
        return NotificationService.create(
            user_id=user_id,
            title="Payment Overdue",
            message=f"Invoice #{invoice_number} is {days_overdue} days overdue. Amount: ${amount:.2f}",
            type="error",
            category="payment",
            priority="high",
            action_url=f"/invoices/{invoice_number}",
            action_label="View Invoice",
            metadata={
                "invoice_number": invoice_number,
                "days_overdue": days_overdue,
                "amount": amount,
            },
        )

    @staticmethod
    def notify_security_alert(user_id: int, message: str, details: dict = None):
        """Create security alert notification."""
        return NotificationService.create(
            user_id=user_id,
            title="Security Alert",
            message=message,
            type="alert",
            category="security",
            priority="urgent",
            metadata=details,
        )

    @staticmethod
    def notify_report_ready(user_id: int, report_name: str, download_url: str):
        """Create report ready notification."""
        return NotificationService.create(
            user_id=user_id,
            title="Report Ready",
            message=f'Your report "{report_name}" is ready for download.',
            type="info",
            category="report",
            priority="normal",
            action_url=download_url,
            action_label="Download Report",
            expires_at=datetime.utcnow() + timedelta(days=7),
            metadata={"report_name": report_name},
        )

    # ==========================================================================
    # Preferences
    # ==========================================================================

    @staticmethod
    def get_preferences(user_id: int) -> NotificationPreferences:
        """Get user notification preferences."""
        prefs = NotificationPreferences.query.filter_by(user_id=user_id).first()

        if not prefs:
            # Create default preferences
            prefs = NotificationPreferences(user_id=user_id)
            db.session.add(prefs)
            db.session.commit()

        return prefs

    @staticmethod
    def update_preferences(user_id: int, updates: dict) -> NotificationPreferences:
        """Update user notification preferences."""
        prefs = NotificationService.get_preferences(user_id)

        for key, value in updates.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)

        db.session.commit()
        return prefs

    # ==========================================================================
    # Cleanup
    # ==========================================================================

    @staticmethod
    def cleanup_expired() -> int:
        """Delete expired notifications."""
        count = Notification.query.filter(
            Notification.expires_at.isnot(None),
            Notification.expires_at < datetime.utcnow(),
        ).delete()
        db.session.commit()
        logger.info(f"P2.58: Cleaned up {count} expired notifications")
        return count

    @staticmethod
    def cleanup_old(days: int = 90) -> int:
        """Delete old read notifications."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        count = Notification.query.filter(
            Notification.is_read, Notification.created_at < cutoff
        ).delete()
        db.session.commit()
        logger.info(f"P2.58: Cleaned up {count} old notifications")
        return count


__all__ = ["NotificationService"]
