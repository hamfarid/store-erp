# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Database Audit Trail System
Tracks all database changes with user, timestamp, IP, and change details
"""

from datetime import datetime, timezone
from flask import request, g
from sqlalchemy import event
from sqlalchemy.orm import Session
import json


class DatabaseAuditTrail:
    """Database audit trail system"""

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.tracked_tables = set()

    def track_table(self, model):
        """Track changes to a specific table"""
        table_name = model.__tablename__

        if table_name in self.tracked_tables:
            return

        self.tracked_tables.add(table_name)

        # Listen for INSERT events
        @event.listens_for(model, "after_insert")
        def receive_after_insert(mapper, connection, target):
            self._log_change("INSERT", table_name, target)

        # Listen for UPDATE events
        @event.listens_for(model, "after_update")
        def receive_after_update(mapper, connection, target):
            self._log_change("UPDATE", table_name, target)

        # Listen for DELETE events
        @event.listens_for(model, "after_delete")
        def receive_after_delete(mapper, connection, target):
            self._log_change("DELETE", table_name, target)

    def track_all_models(self, models):
        """Track changes to all models"""
        for model in models:
            self.track_table(model)

    def _log_change(self, operation, table_name, target):
        """Log database change"""
        try:
            # Get user info
            user_id = "system"
            username = "system"
            ip = "unknown"

            if hasattr(g, "current_user") and g.current_user:
                user_id = getattr(g.current_user, "id", "system")
                username = getattr(g.current_user, "username", "system")

            if request:
                if request.headers.get("X-Forwarded-For"):
                    ip = request.headers.get("X-Forwarded-For").split(",")[0]
                else:
                    ip = request.remote_addr or "unknown"

            # Get record data
            record_data = {}
            try:
                if hasattr(target, "to_dict"):
                    record_data = target.to_dict()
                else:
                    # Fallback: get all columns
                    for column in target.__table__.columns:
                        value = getattr(target, column.name, None)
                        if value is not None:
                            # Convert datetime to string
                            if isinstance(value, datetime):
                                value = value.isoformat()
                            record_data[column.name] = value
            except Exception as e:
                record_data = {"error": f"Could not serialize: {str(e)}"}

            # Get record ID
            record_id = getattr(target, "id", "unknown")

            # Log the change
            self.logger.log_database(
                operation=operation,
                table=table_name,
                record_id=record_id,
                user_id=user_id,
                username=username,
                ip=ip,
                data=record_data,
            )

        except Exception as e:
            # Don't let audit logging break the application
            print(f"Error logging database change: {e}")

    def get_audit_log(self, table_name=None, record_id=None, user_id=None, limit=100):
        """Get audit log entries (read from log file)"""
        # This would read from the database.log file
        # For now, just return empty list
        # In production, you might want to store audit logs in a separate database table
        return []


def create_audit_trail(db, logger):
    """Create and configure database audit trail"""
    audit = DatabaseAuditTrail(db, logger)

    # Import all models to track
    try:
        from src.models.user import User, Role
        from src.models.customer import Customer
        from src.models.supplier import Supplier
        from src.models.inventory import Category, Product, Warehouse

        # Track all models
        models_to_track = [User, Role, Customer, Supplier, Category, Product, Warehouse]

        for model in models_to_track:
            audit.track_table(model)

        logger.log_startup(
            event="audit_trail_configured", tracked_tables=len(models_to_track)
        )

    except Exception as e:
        logger.log_error(error=f"Failed to configure audit trail: {str(e)}")

    return audit
