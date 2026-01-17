#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.59: Audit Log Routes

API endpoints for querying audit logs.
"""

import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from src.routes.auth_unified import token_required
from src.permissions import require_permission, Permissions
from src.services.audit_service import AuditService

logger = logging.getLogger(__name__)

audit_bp = Blueprint("audit", __name__, url_prefix="/api/audit")


@audit_bp.route("/logs", methods=["GET"])
@token_required
@require_permission(Permissions.SECURITY_VIEW)
def get_logs():
    """
    Query audit logs with filters.

    Query params:
        user_id: Filter by user ID
        action: Filter by action type
        resource_type: Filter by resource type
        resource_id: Filter by resource ID
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        status: Filter by status (success/failed)
        limit: Max results (default 100)
        offset: Pagination offset
    """
    # Parse filters
    user_id = request.args.get("user_id", type=int)
    action = request.args.get("action")
    resource_type = request.args.get("resource_type")
    resource_id = request.args.get("resource_id", type=int)
    status = request.args.get("status")
    limit = min(request.args.get("limit", 100, type=int), 500)
    offset = request.args.get("offset", 0, type=int)

    # Parse dates
    from_date = None
    to_date = None

    if request.args.get("from_date"):
        try:
            from_date = datetime.strptime(request.args.get("from_date"), "%Y-%m-%d")
        except ValueError:
            pass

    if request.args.get("to_date"):
        try:
            to_date = datetime.strptime(request.args.get("to_date"), "%Y-%m-%d")
            to_date = to_date.replace(hour=23, minute=59, second=59)
        except ValueError:
            pass

    # Query logs
    logs = AuditService.get_logs(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        from_date=from_date,
        to_date=to_date,
        status=status,
        limit=limit,
        offset=offset,
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "logs": [log.to_dict() for log in logs],
                "limit": limit,
                "offset": offset,
            },
        }
    )


@audit_bp.route("/resource/<resource_type>/<int:resource_id>", methods=["GET"])
@token_required
@require_permission(Permissions.SECURITY_VIEW)
def get_resource_history(resource_type: str, resource_id: int):
    """Get change history for a specific resource."""
    limit = min(request.args.get("limit", 50, type=int), 200)

    logs = AuditService.get_resource_history(
        resource_type=resource_type, resource_id=resource_id, limit=limit
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "resource_type": resource_type,
                "resource_id": resource_id,
                "history": [log.to_dict() for log in logs],
            },
        }
    )


@audit_bp.route("/user/<int:user_id>", methods=["GET"])
@token_required
@require_permission(Permissions.SECURITY_VIEW)
def get_user_activity(user_id: int):
    """Get activity history for a user."""
    days = request.args.get("days", 30, type=int)
    limit = min(request.args.get("limit", 100, type=int), 500)

    from_date = datetime.utcnow() - timedelta(days=days)

    logs = AuditService.get_user_activity(
        user_id=user_id, from_date=from_date, limit=limit
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "user_id": user_id,
                "period_days": days,
                "activities": [log.to_dict() for log in logs],
            },
        }
    )


@audit_bp.route("/failed-logins", methods=["GET"])
@token_required
@require_permission(Permissions.SECURITY_MANAGE)
def get_failed_logins():
    """Get recent failed login attempts."""
    hours = request.args.get("hours", 24, type=int)
    username = request.args.get("username")
    ip_address = request.args.get("ip_address")

    logs = AuditService.get_recent_failed_logins(
        username=username, ip_address=ip_address, hours=hours
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "period_hours": hours,
                "count": len(logs),
                "attempts": [log.to_dict() for log in logs],
            },
        }
    )


@audit_bp.route("/stats", methods=["GET"])
@token_required
@require_permission(Permissions.SECURITY_VIEW)
def get_stats():
    """Get audit log statistics."""
    days = request.args.get("days", 30, type=int)

    from_date = datetime.utcnow() - timedelta(days=days)
    to_date = datetime.utcnow()

    stats = AuditService.get_stats(from_date=from_date, to_date=to_date)

    return jsonify({"success": True, "data": stats})


__all__ = ["audit_bp"]
