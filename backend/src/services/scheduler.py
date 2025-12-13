#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.68: Scheduled Tasks (Cron) Service

Background job scheduler using APScheduler.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Callable, Dict, Any, List, Optional
from dataclasses import dataclass
from functools import wraps

logger = logging.getLogger(__name__)


@dataclass
class ScheduledJob:
    """Information about a scheduled job."""

    id: str
    name: str
    description: str
    trigger: str  # 'cron', 'interval', 'date'
    schedule: str
    next_run: Optional[datetime]
    last_run: Optional[datetime]
    enabled: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "trigger": self.trigger,
            "schedule": self.schedule,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "enabled": self.enabled,
        }


class TaskScheduler:
    """
    P2.68: Background task scheduler.

    Uses APScheduler for cron-like scheduling.
    """

    def __init__(self, app=None):
        self.app = app
        self.scheduler = None
        self._jobs: Dict[str, Dict[str, Any]] = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize with Flask app."""
        self.app = app

        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.jobstores.memory import MemoryJobStore

            jobstores = {"default": MemoryJobStore()}

            self.scheduler = BackgroundScheduler(jobstores=jobstores, timezone="UTC")

            # Register default jobs
            self._register_default_jobs()

            logger.info("P2.68: Scheduler initialized")

        except ImportError:
            logger.warning("P2.68: APScheduler not installed. Scheduler disabled.")
            self.scheduler = None

    def start(self):
        """Start the scheduler."""
        if self.scheduler and not self.scheduler.running:
            self.scheduler.start()
            logger.info("P2.68: Scheduler started")

    def shutdown(self):
        """Shutdown the scheduler."""
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logger.info("P2.68: Scheduler shutdown")

    def add_job(
        self,
        func: Callable,
        trigger: str,
        id: str,
        name: str = None,
        description: str = None,
        **trigger_args,
    ):
        """
        Add a scheduled job.

        Args:
            func: Function to execute
            trigger: 'cron', 'interval', or 'date'
            id: Unique job ID
            name: Human-readable name
            description: Job description
            **trigger_args: Trigger-specific arguments
        """
        if not self.scheduler:
            logger.warning(f"P2.68: Scheduler not available, job {id} not added")
            return

        # Wrap function with error handling
        @wraps(func)
        def wrapped_func():
            try:
                with self.app.app_context():
                    logger.info(f"P2.68: Running job {id}")
                    func()
                    self._jobs[id]["last_run"] = datetime.utcnow()
            except Exception as e:
                logger.error(f"P2.68: Job {id} failed: {e}")

        self.scheduler.add_job(
            wrapped_func,
            trigger=trigger,
            id=id,
            name=name or id,
            replace_existing=True,
            **trigger_args,
        )

        # Store job info
        self._jobs[id] = {
            "id": id,
            "name": name or id,
            "description": description or "",
            "trigger": trigger,
            "schedule": str(trigger_args),
            "last_run": None,
            "enabled": True,
        }

        logger.info(f"P2.68: Added job {id}")

    def remove_job(self, job_id: str):
        """Remove a scheduled job."""
        if self.scheduler:
            try:
                self.scheduler.remove_job(job_id)
                self._jobs.pop(job_id, None)
                logger.info(f"P2.68: Removed job {job_id}")
            except Exception as e:
                logger.error(f"P2.68: Failed to remove job {job_id}: {e}")

    def pause_job(self, job_id: str):
        """Pause a scheduled job."""
        if self.scheduler:
            self.scheduler.pause_job(job_id)
            if job_id in self._jobs:
                self._jobs[job_id]["enabled"] = False
            logger.info(f"P2.68: Paused job {job_id}")

    def resume_job(self, job_id: str):
        """Resume a paused job."""
        if self.scheduler:
            self.scheduler.resume_job(job_id)
            if job_id in self._jobs:
                self._jobs[job_id]["enabled"] = True
            logger.info(f"P2.68: Resumed job {job_id}")

    def run_job_now(self, job_id: str):
        """Run a job immediately."""
        if self.scheduler:
            job = self.scheduler.get_job(job_id)
            if job:
                job.func()
                logger.info(f"P2.68: Manually triggered job {job_id}")

    def get_jobs(self) -> List[ScheduledJob]:
        """Get list of all scheduled jobs."""
        jobs = []

        if self.scheduler:
            for job in self.scheduler.get_jobs():
                job_info = self._jobs.get(job.id, {})
                jobs.append(
                    ScheduledJob(
                        id=job.id,
                        name=job.name,
                        description=job_info.get("description", ""),
                        trigger=job_info.get("trigger", "unknown"),
                        schedule=job_info.get("schedule", ""),
                        next_run=job.next_run_time,
                        last_run=job_info.get("last_run"),
                        enabled=job_info.get("enabled", True),
                    )
                )

        return jobs

    def get_job(self, job_id: str) -> Optional[ScheduledJob]:
        """Get a specific job by ID."""
        if self.scheduler:
            job = self.scheduler.get_job(job_id)
            if job:
                job_info = self._jobs.get(job_id, {})
                return ScheduledJob(
                    id=job.id,
                    name=job.name,
                    description=job_info.get("description", ""),
                    trigger=job_info.get("trigger", "unknown"),
                    schedule=job_info.get("schedule", ""),
                    next_run=job.next_run_time,
                    last_run=job_info.get("last_run"),
                    enabled=job_info.get("enabled", True),
                )
        return None

    def _register_default_jobs(self):
        """Register default scheduled jobs."""
        # Daily backup
        self.add_job(
            func=self._job_daily_backup,
            trigger="cron",
            id="daily_backup",
            name="Daily Backup",
            description="Creates a daily database backup",
            hour=2,
            minute=0,
        )

        # Cleanup old notifications
        self.add_job(
            func=self._job_cleanup_notifications,
            trigger="cron",
            id="cleanup_notifications",
            name="Cleanup Notifications",
            description="Removes old notifications",
            hour=3,
            minute=0,
        )

        # Cleanup expired tokens
        self.add_job(
            func=self._job_cleanup_tokens,
            trigger="interval",
            id="cleanup_tokens",
            name="Cleanup Tokens",
            description="Removes expired JWT tokens from blacklist",
            hours=1,
        )

        # Low stock alerts
        self.add_job(
            func=self._job_low_stock_alerts,
            trigger="cron",
            id="low_stock_alerts",
            name="Low Stock Alerts",
            description="Sends alerts for low stock items",
            hour=8,
            minute=0,
        )

        # Cleanup audit logs
        self.add_job(
            func=self._job_cleanup_audit_logs,
            trigger="cron",
            id="cleanup_audit_logs",
            name="Cleanup Audit Logs",
            description="Archives old audit logs",
            day=1,  # First day of month
            hour=4,
            minute=0,
        )

    # ==========================================================================
    # Job Functions
    # ==========================================================================

    def _job_daily_backup(self):
        """Daily backup job."""
        from src.services.backup_service import BackupService

        service = BackupService()
        backup = service.create_backup(backup_type="full", compress=True)
        service.cleanup_old_backups(keep=7)

        logger.info(f"P2.68: Daily backup created: {backup.filename}")

    def _job_cleanup_notifications(self):
        """Cleanup old notifications."""
        from src.models.notification import Notification
        from src.database import db

        cutoff = datetime.utcnow() - timedelta(days=30)
        count = Notification.query.filter(
            Notification.is_read, Notification.created_at < cutoff
        ).delete()

        db.session.commit()
        logger.info(f"P2.68: Cleaned up {count} old notifications")

    def _job_cleanup_tokens(self):
        """Cleanup expired tokens."""
        from src.token_blacklist import token_blacklist

        if hasattr(token_blacklist, "cleanup_expired"):
            token_blacklist.cleanup_expired()

        logger.info("P2.68: Token cleanup completed")

    def _job_low_stock_alerts(self):
        """Send low stock alerts."""
        from src.models.product import Product
        from src.services.notification_service import NotificationService
        from src.models.user import User

        low_stock = Product.query.filter(
            Product.quantity <= Product.min_stock_level
        ).all()

        if low_stock:
            # Notify admin users
            admins = User.query.filter_by(role="admin", is_active=True).all()

            for admin in admins:
                for product in low_stock[:10]:  # Limit to 10 products per notification
                    NotificationService.notify_low_stock(
                        user_id=admin.id,
                        product_name=product.name,
                        quantity=product.quantity,
                        min_level=product.min_stock_level,
                    )

        logger.info(f"P2.68: Low stock alerts sent for {len(low_stock)} products")

    def _job_cleanup_audit_logs(self):
        """Archive old audit logs."""
        from src.services.audit_service import AuditService

        deleted = AuditService.cleanup_old_logs(days=365)
        logger.info(f"P2.68: Cleaned up {deleted} old audit logs")


# Global scheduler instance
scheduler = TaskScheduler()


def init_scheduler(app):
    """Initialize the global scheduler with Flask app."""
    scheduler.init_app(app)
    return scheduler


__all__ = ["TaskScheduler", "ScheduledJob", "scheduler", "init_scheduler"]
