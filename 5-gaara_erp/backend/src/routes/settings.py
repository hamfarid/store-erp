#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.66: Settings Management Routes

API endpoints for managing application settings.
"""

import logging
from flask import Blueprint, request, jsonify
from src.routes.auth_unified import token_required
from src.permissions import require_permission, Permissions
from src.models.settings import Setting, initialize_default_settings

logger = logging.getLogger(__name__)

settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")


@settings_bp.route("", methods=["GET"])
@token_required
def get_all_settings():
    """
    Get all settings (admin only) or public settings.

    Query params:
        category: Filter by category
    """
    category = request.args.get("category")

    # Check if user has admin permission
    has_admin = getattr(request, "is_admin", False)

    if has_admin:
        if category:
            settings = Setting.get_by_category(category)
        else:
            settings = Setting.query.all()
    else:
        if category:
            settings = Setting.query.filter_by(category=category, is_public=True).all()
        else:
            settings = Setting.get_public()

    return jsonify(
        {"success": True, "data": {"settings": [s.to_dict() for s in settings]}}
    )


@settings_bp.route("/public", methods=["GET"])
def get_public_settings():
    """Get all public settings (no auth required)."""
    settings = Setting.get_public()

    return jsonify(
        {
            "success": True,
            "data": {"settings": {s.key: s.get_value() for s in settings}},
        }
    )


@settings_bp.route("/category/<category>", methods=["GET"])
@token_required
def get_settings_by_category(category: str):
    """Get settings by category."""
    has_admin = getattr(request, "is_admin", False)

    if has_admin:
        settings = Setting.get_by_category(category)
    else:
        settings = Setting.query.filter_by(category=category, is_public=True).all()

    return jsonify(
        {
            "success": True,
            "data": {"category": category, "settings": [s.to_dict() for s in settings]},
        }
    )


@settings_bp.route("/<key>", methods=["GET"])
@token_required
def get_setting(key: str):
    """Get a specific setting by key."""
    setting = Setting.query.filter_by(key=key).first()

    if not setting:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f'Setting "{key}" not found',
                    },
                }
            ),
            404,
        )

    # Check access
    has_admin = getattr(request, "is_admin", False)
    if not setting.is_public and not has_admin:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {"code": "FORBIDDEN", "message": "Access denied"},
                }
            ),
            403,
        )

    return jsonify({"success": True, "data": setting.to_dict()})


@settings_bp.route("/<key>", methods=["PUT"])
@token_required
@require_permission(Permissions.SYSTEM_SETTINGS_EDIT)
def update_setting(key: str):
    """Update a setting value."""
    setting = Setting.query.filter_by(key=key).first()

    if not setting:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f'Setting "{key}" not found',
                    },
                }
            ),
            404,
        )

    if not setting.is_editable:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "This setting cannot be modified",
                    },
                }
            ),
            403,
        )

    data = request.get_json()
    value = data.get("value")

    if value is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Value is required",
                    },
                }
            ),
            400,
        )

    setting.set_value(value)

    from src.database import db

    db.session.commit()

    logger.info(f"P2.66: Updated setting {key}")

    return jsonify({"success": True, "data": setting.to_dict()})


@settings_bp.route("/bulk", methods=["PUT"])
@token_required
@require_permission(Permissions.SYSTEM_SETTINGS_EDIT)
def update_settings_bulk():
    """Update multiple settings at once."""
    data = request.get_json()
    settings_data = data.get("settings", {})

    if not settings_data:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "No settings provided",
                    },
                }
            ),
            400,
        )

    from src.database import db

    updated = []
    errors = []

    for key, value in settings_data.items():
        setting = Setting.query.filter_by(key=key).first()

        if not setting:
            errors.append({"key": key, "error": "Not found"})
            continue

        if not setting.is_editable:
            errors.append({"key": key, "error": "Not editable"})
            continue

        setting.set_value(value)
        updated.append(key)

    db.session.commit()

    logger.info(f"P2.66: Bulk updated {len(updated)} settings")

    return jsonify(
        {"success": len(errors) == 0, "data": {"updated": updated, "errors": errors}}
    )


@settings_bp.route("/reset/<key>", methods=["POST"])
@token_required
@require_permission(Permissions.SYSTEM_SETTINGS_EDIT)
def reset_setting(key: str):
    """Reset a setting to its default value."""
    from src.models.settings import DEFAULT_SETTINGS

    setting = Setting.query.filter_by(key=key).first()

    if not setting:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f'Setting "{key}" not found',
                    },
                }
            ),
            404,
        )

    # Find default value
    default = next((s for s in DEFAULT_SETTINGS if s["key"] == key), None)

    if default:
        setting.value = default["value"]
        from src.database import db

        db.session.commit()

        return jsonify({"success": True, "data": setting.to_dict()})

    return (
        jsonify(
            {
                "success": False,
                "error": {
                    "code": "NO_DEFAULT",
                    "message": "No default value available",
                },
            }
        ),
        400,
    )


@settings_bp.route("/initialize", methods=["POST"])
@token_required
@require_permission(Permissions.ADMIN_FULL)
def initialize_settings():
    """Initialize or reset all default settings."""
    initialize_default_settings()

    logger.info("P2.66: Initialized default settings")

    return jsonify({"success": True, "message": "Settings initialized successfully"})


@settings_bp.route("/categories", methods=["GET"])
@token_required
def get_categories():
    """Get list of setting categories."""
    from sqlalchemy import distinct

    categories = Setting.query.with_entities(distinct(Setting.category)).all()

    return jsonify(
        {"success": True, "data": {"categories": [c[0] for c in categories]}}
    )


__all__ = ["settings_bp"]
