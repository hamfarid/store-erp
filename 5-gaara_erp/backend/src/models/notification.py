#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.58: Notification Model

Database model for user notifications.
"""

from datetime import datetime
from src.database import db


class Notification(db.Model):
    """
    P2.58: User notification model.

    Stores notifications for users with different types and read status.
    """

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Notification content
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # Type: info, warning, error, success, alert
    type = db.Column(db.String(20), default="info")

    # Category: system, inventory, sales, security, etc.
    category = db.Column(db.String(50), default="system")

    # Status
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime, nullable=True)

    # Action link (optional)
    action_url = db.Column(db.String(500), nullable=True)
    action_label = db.Column(db.String(100), nullable=True)

    # Priority: low, normal, high, urgent
    priority = db.Column(db.String(20), default="normal")

    # Expiration (optional)
    expires_at = db.Column(db.DateTime, nullable=True)

    # Metadata (JSON)
    metadata = db.Column(db.JSON, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user = db.relationship(
        "src.models.user.User", backref=db.backref("user_notifications", lazy="dynamic")
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "category": self.category,
            "is_read": self.is_read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "action_url": self.action_url,
            "action_label": self.action_label,
            "priority": self.priority,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def create_notification(
        cls,
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
    ):
        """Create a new notification."""
        notification = cls(
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
        db.session.add(notification)
        db.session.commit()
        return notification

    @classmethod
    def get_unread_count(cls, user_id: int) -> int:
        """Get count of unread notifications for a user."""
        return cls.query.filter_by(user_id=user_id, is_read=False).count()

    @classmethod
    def mark_all_as_read(cls, user_id: int):
        """Mark all notifications as read for a user."""
        cls.query.filter_by(user_id=user_id, is_read=False).update(
            {"is_read": True, "read_at": datetime.utcnow()}
        )
        db.session.commit()

    def __repr__(self):
        return f"<Notification {self.id}: {self.title[:30]}>"


class NotificationPreferences(db.Model):
    """
    P2.58: User notification preferences.

    Stores user preferences for notification delivery.
    """

    __tablename__ = "notification_preferences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )

    # In-app notifications
    in_app_enabled = db.Column(db.Boolean, default=True)

    # Email notifications
    email_enabled = db.Column(db.Boolean, default=True)
    email_frequency = db.Column(
        db.String(20), default="instant"
    )  # instant, daily, weekly

    # Push notifications
    push_enabled = db.Column(db.Boolean, default=False)

    # Category preferences (JSON)
    category_preferences = db.Column(db.JSON, default=dict)

    # Quiet hours
    quiet_hours_enabled = db.Column(db.Boolean, default=False)
    quiet_hours_start = db.Column(db.String(5), default="22:00")
    quiet_hours_end = db.Column(db.String(5), default="08:00")

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship
    user = db.relationship(
        "src.models.user.User",
        backref=db.backref("user_notification_preferences", uselist=False),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "in_app_enabled": self.in_app_enabled,
            "email_enabled": self.email_enabled,
            "email_frequency": self.email_frequency,
            "push_enabled": self.push_enabled,
            "category_preferences": self.category_preferences,
            "quiet_hours_enabled": self.quiet_hours_enabled,
            "quiet_hours_start": self.quiet_hours_start,
            "quiet_hours_end": self.quiet_hours_end,
        }


__all__ = ["Notification", "NotificationPreferences"]
