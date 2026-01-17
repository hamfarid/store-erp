#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.58: Notification Routes

API endpoints for user notifications.
"""

import logging
from flask import Blueprint, request, jsonify
from src.routes.auth_unified import token_required
from src.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")


# =============================================================================
# Routes
# =============================================================================


@notifications_bp.route("", methods=["GET"])
@token_required
def get_notifications():
    """
    Get notifications for the current user.

    Query params:
        unread_only: Filter to unread only (default: false)
        category: Filter by category
        limit: Max results (default: 50)
        offset: Pagination offset (default: 0)
    """
    user_id = request.current_user_id

    unread_only = request.args.get("unread_only", "false").lower() == "true"
    category = request.args.get("category")
    limit = min(request.args.get("limit", 50, type=int), 100)
    offset = request.args.get("offset", 0, type=int)

    notifications = NotificationService.get_user_notifications(
        user_id=user_id,
        unread_only=unread_only,
        category=category,
        limit=limit,
        offset=offset,
    )

    unread_count = NotificationService.get_unread_count(user_id)

    return jsonify(
        {
            "success": True,
            "data": {
                "notifications": [n.to_dict() for n in notifications],
                "unread_count": unread_count,
                "limit": limit,
                "offset": offset,
            },
        }
    )


@notifications_bp.route("/unread-count", methods=["GET"])
@token_required
def get_unread_count():
    """Get count of unread notifications."""
    user_id = request.current_user_id
    count = NotificationService.get_unread_count(user_id)

    return jsonify({"success": True, "data": {"unread_count": count}})


@notifications_bp.route("/<int:notification_id>/read", methods=["POST"])
@token_required
def mark_as_read(notification_id: int):
    """Mark a notification as read."""
    user_id = request.current_user_id

    success = NotificationService.mark_as_read(notification_id, user_id)

    if success:
        return jsonify({"success": True, "message": "Notification marked as read"})

    return (
        jsonify(
            {
                "success": False,
                "error": {"code": "NOT_FOUND", "message": "Notification not found"},
            }
        ),
        404,
    )


@notifications_bp.route("/read-all", methods=["POST"])
@token_required
def mark_all_as_read():
    """Mark all notifications as read."""
    user_id = request.current_user_id

    NotificationService.mark_all_as_read(user_id)

    return jsonify({"success": True, "message": "All notifications marked as read"})


@notifications_bp.route("/<int:notification_id>", methods=["DELETE"])
@token_required
def delete_notification(notification_id: int):
    """Delete a notification."""
    user_id = request.current_user_id

    success = NotificationService.delete_notification(notification_id, user_id)

    if success:
        return jsonify({"success": True, "message": "Notification deleted"})

    return (
        jsonify(
            {
                "success": False,
                "error": {"code": "NOT_FOUND", "message": "Notification not found"},
            }
        ),
        404,
    )


@notifications_bp.route("/delete-read", methods=["DELETE"])
@token_required
def delete_all_read():
    """Delete all read notifications."""
    user_id = request.current_user_id

    count = NotificationService.delete_all_read(user_id)

    return jsonify({"success": True, "message": f"{count} read notifications deleted"})


# =============================================================================
# Preferences
# =============================================================================


@notifications_bp.route("/preferences", methods=["GET"])
@token_required
def get_preferences():
    """Get notification preferences."""
    user_id = request.current_user_id

    prefs = NotificationService.get_preferences(user_id)

    return jsonify({"success": True, "data": prefs.to_dict()})


@notifications_bp.route("/preferences", methods=["PUT"])
@token_required
def update_preferences():
    """Update notification preferences."""
    user_id = request.current_user_id
    updates = request.get_json()

    # Validate fields
    allowed_fields = [
        "in_app_enabled",
        "email_enabled",
        "email_frequency",
        "push_enabled",
        "category_preferences",
        "quiet_hours_enabled",
        "quiet_hours_start",
        "quiet_hours_end",
    ]

    filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields}

    prefs = NotificationService.update_preferences(user_id, filtered_updates)

    return jsonify({"success": True, "data": prefs.to_dict()})


# =============================================================================
# Admin Routes (for testing/debugging)
# =============================================================================


@notifications_bp.route("/test", methods=["POST"])
@token_required
def create_test_notification():
    """Create a test notification (for development)."""
    user_id = request.current_user_id
    data = request.get_json()

    notification = NotificationService.create(
        user_id=user_id,
        title=data.get("title", "Test Notification"),
        message=data.get("message", "This is a test notification"),
        type=data.get("type", "info"),
        category=data.get("category", "system"),
        priority=data.get("priority", "normal"),
        action_url=data.get("action_url"),
        action_label=data.get("action_label"),
    )

    return jsonify({"success": True, "data": notification.to_dict()}), 201


__all__ = ["notifications_bp"]
