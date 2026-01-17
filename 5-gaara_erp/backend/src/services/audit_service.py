#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.59: Audit Service

Business logic for audit logging with decorators and helpers.
"""

import logging
import functools
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Callable
from flask import request, g, has_request_context
from src.database import db
from src.models.audit_log import AuditLog, AuditActions

logger = logging.getLogger(__name__)


class AuditService:
    """
    P2.59: Service for audit logging.

    Provides methods and decorators for comprehensive audit trails.
    """

    # ==========================================================================
    # Core Logging Methods
    # ==========================================================================

    @staticmethod
    def log(
        action: str,
        resource_type: str,
        resource_id: int = None,
        resource_name: str = None,
        old_values: dict = None,
        new_values: dict = None,
        metadata: dict = None,
        status: str = "success",
        error_message: str = None,
    ) -> AuditLog:
        """
        Create an audit log entry.

        Automatically captures user and request context when available.
        """
        # Get user info from context
        user_id = None
        username = None

        if has_request_context():
            user_id = getattr(request, "current_user_id", None)
            username = getattr(g, "current_username", None)

        # Get request info
        ip_address = None
        user_agent = None
        request_id = None

        if has_request_context():
            ip_address = request.remote_addr
            user_agent = request.headers.get("User-Agent", "")[:500]
            request_id = getattr(g, "request_id", None)

        return AuditLog.log(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            user_id=user_id,
            username=username,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            metadata=metadata,
            status=status,
            error_message=error_message,
        )

    @staticmethod
    def log_create(
        resource_type: str,
        resource_id: int,
        resource_name: str = None,
        new_values: dict = None,
        metadata: dict = None,
    ) -> AuditLog:
        """Log a CREATE action."""
        return AuditService.log(
            action=AuditActions.CREATE,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            new_values=new_values,
            metadata=metadata,
        )

    @staticmethod
    def log_update(
        resource_type: str,
        resource_id: int,
        resource_name: str = None,
        old_values: dict = None,
        new_values: dict = None,
        metadata: dict = None,
    ) -> AuditLog:
        """Log an UPDATE action."""
        return AuditService.log(
            action=AuditActions.UPDATE,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            old_values=old_values,
            new_values=new_values,
            metadata=metadata,
        )

    @staticmethod
    def log_delete(
        resource_type: str,
        resource_id: int,
        resource_name: str = None,
        old_values: dict = None,
        metadata: dict = None,
    ) -> AuditLog:
        """Log a DELETE action."""
        return AuditService.log(
            action=AuditActions.DELETE,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            old_values=old_values,
            metadata=metadata,
        )

    # ==========================================================================
    # Authentication Logging
    # ==========================================================================

    @staticmethod
    def log_login(
        user_id: int, username: str, success: bool = True, reason: str = None
    ):
        """Log a login attempt."""
        return AuditService.log(
            action=AuditActions.LOGIN if success else AuditActions.LOGIN_FAILED,
            resource_type="auth",
            resource_name=username,
            metadata={"reason": reason} if reason else None,
            status="success" if success else "failed",
            error_message=reason if not success else None,
        )

    @staticmethod
    def log_logout(user_id: int, username: str):
        """Log a logout."""
        return AuditService.log(
            action=AuditActions.LOGOUT, resource_type="auth", resource_name=username
        )

    @staticmethod
    def log_password_change(user_id: int, username: str):
        """Log a password change."""
        return AuditService.log(
            action=AuditActions.PASSWORD_CHANGE,
            resource_type="auth",
            resource_id=user_id,
            resource_name=username,
        )

    # ==========================================================================
    # Query Methods
    # ==========================================================================

    @staticmethod
    def get_logs(
        user_id: int = None,
        action: str = None,
        resource_type: str = None,
        resource_id: int = None,
        from_date: datetime = None,
        to_date: datetime = None,
        status: str = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AuditLog]:
        """Query audit logs with filters."""
        query = AuditLog.query

        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        if resource_id:
            query = query.filter(AuditLog.resource_id == resource_id)
        if from_date:
            query = query.filter(AuditLog.created_at >= from_date)
        if to_date:
            query = query.filter(AuditLog.created_at <= to_date)
        if status:
            query = query.filter(AuditLog.status == status)

        return (
            query.order_by(AuditLog.created_at.desc()).offset(offset).limit(limit).all()
        )

    @staticmethod
    def get_resource_history(
        resource_type: str, resource_id: int, limit: int = 50
    ) -> List[AuditLog]:
        """Get change history for a specific resource."""
        return (
            AuditLog.query.filter(
                AuditLog.resource_type == resource_type,
                AuditLog.resource_id == resource_id,
            )
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_user_activity(
        user_id: int, from_date: datetime = None, limit: int = 100
    ) -> List[AuditLog]:
        """Get activity history for a user."""
        query = AuditLog.query.filter(AuditLog.user_id == user_id)

        if from_date:
            query = query.filter(AuditLog.created_at >= from_date)

        return query.order_by(AuditLog.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_recent_failed_logins(
        username: str = None, ip_address: str = None, hours: int = 24
    ) -> List[AuditLog]:
        """Get recent failed login attempts."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        query = AuditLog.query.filter(
            AuditLog.action == AuditActions.LOGIN_FAILED, AuditLog.created_at >= cutoff
        )

        if username:
            query = query.filter(AuditLog.resource_name == username)
        if ip_address:
            query = query.filter(AuditLog.ip_address == ip_address)

        return query.order_by(AuditLog.created_at.desc()).all()

    # ==========================================================================
    # Statistics
    # ==========================================================================

    @staticmethod
    def get_stats(
        from_date: datetime = None, to_date: datetime = None
    ) -> Dict[str, Any]:
        """Get audit log statistics."""
        from sqlalchemy import func

        if not from_date:
            from_date = datetime.utcnow() - timedelta(days=30)
        if not to_date:
            to_date = datetime.utcnow()

        base_query = AuditLog.query.filter(
            AuditLog.created_at >= from_date, AuditLog.created_at <= to_date
        )

        # Total count
        total = base_query.count()

        # By action
        by_action = (
            db.session.query(AuditLog.action, func.count(AuditLog.id))
            .filter(AuditLog.created_at >= from_date, AuditLog.created_at <= to_date)
            .group_by(AuditLog.action)
            .all()
        )

        # By resource type
        by_resource = (
            db.session.query(AuditLog.resource_type, func.count(AuditLog.id))
            .filter(AuditLog.created_at >= from_date, AuditLog.created_at <= to_date)
            .group_by(AuditLog.resource_type)
            .all()
        )

        # Failed actions
        failed = base_query.filter(AuditLog.status == "failed").count()

        return {
            "total": total,
            "failed": failed,
            "success_rate": ((total - failed) / total * 100) if total > 0 else 100,
            "by_action": {action: count for action, count in by_action},
            "by_resource": {resource: count for resource, count in by_resource},
            "period": {"from": from_date.isoformat(), "to": to_date.isoformat()},
        }

    # ==========================================================================
    # Cleanup
    # ==========================================================================

    @staticmethod
    def cleanup_old_logs(days: int = 365) -> int:
        """Delete audit logs older than specified days."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        count = AuditLog.query.filter(AuditLog.created_at < cutoff).delete()
        db.session.commit()
        logger.info(f"P2.59: Cleaned up {count} old audit logs")
        return count


# =============================================================================
# Decorators
# =============================================================================


def audit_action(
    action: str,
    resource_type: str,
    get_resource_id: Callable = None,
    get_resource_name: Callable = None,
    get_old_values: Callable = None,
    include_request_body: bool = False,
):
    """
    Decorator to automatically audit function calls.

    Usage:
        @audit_action('UPDATE', 'product', get_resource_id=lambda args: args[0])
        def update_product(product_id, data):
            ...
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Capture old values if getter provided
            old_values = None
            if get_old_values:
                try:
                    old_values = get_old_values(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Failed to get old values for audit: {e}")

            # Get resource identifiers
            resource_id = None
            resource_name = None

            if get_resource_id:
                try:
                    resource_id = get_resource_id(*args, **kwargs)
                except BaseException:
                    pass

            if get_resource_name:
                try:
                    resource_name = get_resource_name(*args, **kwargs)
                except BaseException:
                    pass

            # Execute function
            status = "success"
            error_message = None
            result = None

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                status = "failed"
                error_message = str(e)
                raise
            finally:
                # Build new values
                new_values = None
                if include_request_body and has_request_context():
                    try:
                        new_values = request.get_json()
                    except BaseException:
                        pass

                # Log the action
                try:
                    AuditService.log(
                        action=action,
                        resource_type=resource_type,
                        resource_id=resource_id,
                        resource_name=resource_name,
                        old_values=old_values,
                        new_values=new_values,
                        status=status,
                        error_message=error_message,
                    )
                except Exception as e:
                    logger.error(f"Failed to create audit log: {e}")

            return result

        return wrapper

    return decorator


__all__ = ["AuditService", "audit_action", "AuditActions"]
