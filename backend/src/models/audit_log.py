#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.59: Audit Log Model

Database model for tracking all system changes and user actions.
"""

from datetime import datetime
from src.database import db
import json


class AuditLog(db.Model):
    """
    P2.59: Audit log model for tracking system changes.

    Records all CRUD operations, authentication events, and system changes.
    """

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    # Who performed the action
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    username = db.Column(db.String(100), nullable=True)  # Denormalized for performance

    # What action was performed
    action = db.Column(
        db.String(50), nullable=False
    )  # CREATE, UPDATE, DELETE, LOGIN, etc.

    # What resource was affected
    resource_type = db.Column(
        db.String(100), nullable=False
    )  # products, users, invoices, etc.
    resource_id = db.Column(db.Integer, nullable=True)
    resource_name = db.Column(
        db.String(200), nullable=True
    )  # Human-readable identifier

    # Details of the change
    old_values = db.Column(db.JSON, nullable=True)  # Previous state
    new_values = db.Column(db.JSON, nullable=True)  # New state
    changed_fields = db.Column(db.JSON, nullable=True)  # List of changed field names

    # Request context
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    request_id = db.Column(db.String(50), nullable=True)

    # Additional metadata (renamed to avoid SQLAlchemy reserved name conflict)
    extra_data = db.Column(db.JSON, nullable=True)

    # Status
    status = db.Column(db.String(20), default="success")  # success, failed, pending
    error_message = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships - use viewonly to avoid sync conflicts
    user = db.relationship(
        "src.models.user.User",
        backref=db.backref("audit_logs", lazy="dynamic"),
        viewonly=True,
    )

    # Indexes for common queries - include extend_existing
    __table_args__ = (
        db.Index("idx_audit_user_action", "user_id", "action"),
        db.Index("idx_audit_resource", "resource_type", "resource_id"),
        db.Index("idx_audit_created", "created_at"),
        {"extend_existing": True},
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "changed_fields": self.changed_fields,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "request_id": self.request_id,
            "extra_data": self.extra_data,
            "status": self.status,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def log(
        cls,
        action: str,
        resource_type: str,
        resource_id: int = None,
        resource_name: str = None,
        user_id: int = None,
        username: str = None,
        old_values: dict = None,
        new_values: dict = None,
        ip_address: str = None,
        user_agent: str = None,
        request_id: str = None,
        extra_data: dict = None,
        status: str = "success",
        error_message: str = None,
    ):
        """Create a new audit log entry."""
        # Calculate changed fields
        changed_fields = None
        if old_values and new_values:
            changed_fields = [
                key
                for key in set(old_values.keys()) | set(new_values.keys())
                if old_values.get(key) != new_values.get(key)
            ]

        log_entry = cls(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            user_id=user_id,
            username=username,
            old_values=old_values,
            new_values=new_values,
            changed_fields=changed_fields,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            extra_data=extra_data,
            status=status,
            error_message=error_message,
        )

        db.session.add(log_entry)
        db.session.commit()

        return log_entry

    def __repr__(self):
        return f"<AuditLog {self.id}: {self.action} {self.resource_type}>"


# Action constants
class AuditActions:
    """Standardized audit action names."""

    # CRUD
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    # Auth
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    LOGIN_FAILED = "LOGIN_FAILED"
    PASSWORD_CHANGE = "PASSWORD_CHANGE"
    PASSWORD_RESET = "PASSWORD_RESET"

    # User management
    USER_ACTIVATE = "USER_ACTIVATE"
    USER_DEACTIVATE = "USER_DEACTIVATE"
    USER_LOCK = "USER_LOCK"
    USER_UNLOCK = "USER_UNLOCK"
    ROLE_ASSIGN = "ROLE_ASSIGN"
    PERMISSION_CHANGE = "PERMISSION_CHANGE"

    # Business operations
    INVOICE_CREATE = "INVOICE_CREATE"
    INVOICE_VOID = "INVOICE_VOID"
    PAYMENT_RECEIVE = "PAYMENT_RECEIVE"
    STOCK_ADJUST = "STOCK_ADJUST"
    STOCK_TRANSFER = "STOCK_TRANSFER"

    # System
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    CONFIG_CHANGE = "CONFIG_CHANGE"
    BACKUP = "BACKUP"
    RESTORE = "RESTORE"


__all__ = ["AuditLog", "AuditActions"]
