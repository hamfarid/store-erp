#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.66: Settings Management Model

Database model for storing application settings.
"""

from datetime import datetime
from typing import Any, Optional
import json
from src.database import db


class Setting(db.Model):
    """
    P2.66: Application settings model.

    Stores key-value pairs for application configuration.
    """

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    value_type = db.Column(
        db.String(20), default="string"
    )  # string, int, float, bool, json
    category = db.Column(db.String(50), default="general", index=True)
    description = db.Column(db.String(500), nullable=True)
    is_public = db.Column(db.Boolean, default=False)  # Can be read by non-admins
    is_editable = db.Column(db.Boolean, default=True)  # Can be modified via UI

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def get_value(self) -> Any:
        """Get the typed value."""
        if self.value is None:
            return None

        if self.value_type == "int":
            return int(self.value)
        elif self.value_type == "float":
            return float(self.value)
        elif self.value_type == "bool":
            return self.value.lower() in ("true", "1", "yes")
        elif self.value_type == "json":
            return json.loads(self.value)
        else:
            return self.value

    def set_value(self, value: Any):
        """Set the value with type conversion."""
        if value is None:
            self.value = None
        elif self.value_type == "json":
            self.value = json.dumps(value)
        else:
            self.value = str(value)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "key": self.key,
            "value": self.get_value(),
            "value_type": self.value_type,
            "category": self.category,
            "description": self.description,
            "is_public": self.is_public,
            "is_editable": self.is_editable,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a setting value by key."""
        setting = cls.query.filter_by(key=key).first()
        return setting.get_value() if setting else default

    @classmethod
    def set(
        cls,
        key: str,
        value: Any,
        value_type: str = "string",
        category: str = "general",
        description: str = None,
        is_public: bool = False,
        is_editable: bool = True,
    ) -> "Setting":
        """Set a setting value."""
        setting = cls.query.filter_by(key=key).first()

        if setting:
            setting.set_value(value)
            setting.value_type = value_type
        else:
            setting = cls(
                key=key,
                value_type=value_type,
                category=category,
                description=description,
                is_public=is_public,
                is_editable=is_editable,
            )
            setting.set_value(value)
            db.session.add(setting)

        db.session.commit()
        return setting

    @classmethod
    def get_by_category(cls, category: str) -> list:
        """Get all settings in a category."""
        return cls.query.filter_by(category=category).all()

    @classmethod
    def get_public(cls) -> list:
        """Get all public settings."""
        return cls.query.filter_by(is_public=True).all()

    @classmethod
    def get_all_as_dict(cls) -> dict:
        """Get all settings as a dictionary."""
        settings = cls.query.all()
        return {s.key: s.get_value() for s in settings}

    def __repr__(self):
        return f"<Setting {self.key}={self.value}>"


# =============================================================================
# Default Settings
# =============================================================================

DEFAULT_SETTINGS = [
    # General
    {
        "key": "app_name",
        "value": "Store Management",
        "category": "general",
        "is_public": True,
    },
    {
        "key": "app_version",
        "value": "1.0.0",
        "category": "general",
        "is_public": True,
        "is_editable": False,
    },
    {"key": "company_name", "value": "", "category": "general", "is_public": True},
    {"key": "company_address", "value": "", "category": "general", "is_public": True},
    {"key": "company_phone", "value": "", "category": "general", "is_public": True},
    {"key": "company_email", "value": "", "category": "general", "is_public": True},
    {"key": "company_logo", "value": "", "category": "general", "is_public": True},
    {"key": "tax_id", "value": "", "category": "general", "is_public": True},
    # Localization
    {"key": "language", "value": "en", "category": "localization", "is_public": True},
    {"key": "currency", "value": "USD", "category": "localization", "is_public": True},
    {
        "key": "currency_symbol",
        "value": "$",
        "category": "localization",
        "is_public": True,
    },
    {
        "key": "date_format",
        "value": "YYYY-MM-DD",
        "category": "localization",
        "is_public": True,
    },
    {
        "key": "time_format",
        "value": "24h",
        "category": "localization",
        "is_public": True,
    },
    {"key": "timezone", "value": "UTC", "category": "localization", "is_public": True},
    # Inventory
    {
        "key": "low_stock_threshold",
        "value": "10",
        "value_type": "int",
        "category": "inventory",
    },
    {
        "key": "allow_negative_stock",
        "value": "false",
        "value_type": "bool",
        "category": "inventory",
    },
    {
        "key": "auto_generate_sku",
        "value": "true",
        "value_type": "bool",
        "category": "inventory",
    },
    {"key": "sku_prefix", "value": "PRD", "category": "inventory"},
    # Invoice
    {"key": "invoice_prefix", "value": "INV", "category": "invoice"},
    {
        "key": "invoice_start_number",
        "value": "1000",
        "value_type": "int",
        "category": "invoice",
    },
    {
        "key": "default_payment_terms",
        "value": "30",
        "value_type": "int",
        "category": "invoice",
    },
    {
        "key": "default_tax_rate",
        "value": "0.15",
        "value_type": "float",
        "category": "invoice",
    },
    {"key": "invoice_notes", "value": "", "category": "invoice"},
    {"key": "invoice_terms", "value": "", "category": "invoice"},
    # Security
    {
        "key": "session_timeout",
        "value": "30",
        "value_type": "int",
        "category": "security",
    },
    {
        "key": "max_login_attempts",
        "value": "5",
        "value_type": "int",
        "category": "security",
    },
    {
        "key": "lockout_duration",
        "value": "30",
        "value_type": "int",
        "category": "security",
    },
    {
        "key": "require_2fa",
        "value": "false",
        "value_type": "bool",
        "category": "security",
    },
    {
        "key": "password_min_length",
        "value": "8",
        "value_type": "int",
        "category": "security",
    },
    # Notifications
    {
        "key": "email_notifications",
        "value": "true",
        "value_type": "bool",
        "category": "notifications",
    },
    {
        "key": "low_stock_alert",
        "value": "true",
        "value_type": "bool",
        "category": "notifications",
    },
    {
        "key": "new_order_alert",
        "value": "true",
        "value_type": "bool",
        "category": "notifications",
    },
    {
        "key": "payment_alert",
        "value": "true",
        "value_type": "bool",
        "category": "notifications",
    },
    # Backup
    {"key": "auto_backup", "value": "true", "value_type": "bool", "category": "backup"},
    {"key": "backup_frequency", "value": "daily", "category": "backup"},
    {
        "key": "backup_retention_days",
        "value": "30",
        "value_type": "int",
        "category": "backup",
    },
    # API
    {"key": "api_rate_limit", "value": "100", "value_type": "int", "category": "api"},
    {"key": "api_timeout", "value": "30", "value_type": "int", "category": "api"},
]


def initialize_default_settings():
    """Initialize default settings if they don't exist."""
    for setting_data in DEFAULT_SETTINGS:
        if not Setting.query.filter_by(key=setting_data["key"]).first():
            setting = Setting(
                key=setting_data["key"],
                value=setting_data["value"],
                value_type=setting_data.get("value_type", "string"),
                category=setting_data.get("category", "general"),
                description=setting_data.get("description"),
                is_public=setting_data.get("is_public", False),
                is_editable=setting_data.get("is_editable", True),
            )
            db.session.add(setting)

    db.session.commit()


__all__ = ["Setting", "DEFAULT_SETTINGS", "initialize_default_settings"]
