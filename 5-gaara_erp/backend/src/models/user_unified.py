#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج المستخدمين الموحد
Unified User Model

IMPORTANT: All User, Role, UserSession, UserActivity classes are now defined
only in src.models.user to avoid SQLAlchemy duplicate model conflicts.

Import them from: from src.models.user import User, Role, UserSession, UserActivity
"""

import json
from datetime import datetime, timezone

from src.database import db

# Ensure related models are registered before relationship resolution
try:
    from src.models import supporting_models  # noqa: F401
except Exception:
    pass

# IMPORTANT: User and Role classes are imported from user.py (CANONICAL DEFINITIONS)
# Routes should import from src.models.user import User, Role
from src.models.user import User, Role, UserSession, UserActivity

# Re-export for backward compatibility
__all__ = ["User", "Role", "UserSession", "UserActivity", "create_default_roles"]


def create_default_roles():
    """إنشاء الأدوار الافتراضية"""
    default_roles = [
        {
            "name": "admin",
            "description": "صلاحيات كاملة على النظام",
            "permissions": ["*"],  # جميع الصلاحيات
        },
        {
            "name": "manager",
            "description": "صلاحيات إدارية محدودة",
            "permissions": [
                "view_dashboard",
                "view_reports",
                "manage_products",
                "manage_inventory",
                "manage_customers",
                "manage_suppliers",
                "create_invoice",
                "view_invoice",
            ],
        },
        {
            "name": "user",
            "description": "صلاحيات أساسية",
            "permissions": [
                "view_dashboard",
                "view_products",
                "view_inventory",
                "view_customers",
                "view_suppliers",
                "create_invoice",
                "view_invoice",
            ],
        },
    ]

    for role_data in default_roles:
        role = Role.query.filter_by(name=role_data["name"]).first()
        if not role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"],
                permissions=role_data["permissions"],
            )
            db.session.add(role)

    db.session.commit()
