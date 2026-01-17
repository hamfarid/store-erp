# -*- coding: utf-8 -*-
"""
Comprehensive Logging System for Store Backend
================================================

Features:
- Structured JSON logging
- Multiple log levels with color coding
- Request/Response logging middleware
- Database query logging
- Performance metrics
- Error tracking with stack traces
- User action audit trail
- No file output - console/stdout only
"""

import logging
import sys
import json
import time
from datetime import datetime
from functools import wraps
from flask import request, g, has_request_context
from typing import Any, Dict, Optional
import traceback


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color codes for console output."""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record):
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Add color to level name
        record.levelname = f"{color}{record.levelname}{reset}"

        return super().format(record)


class StructuredLogger:
    """
    Structured logger that outputs JSON-formatted logs to stdout.
    No file writing - designed for containerized environments.
    """

    def __init__(self, name: str = "store", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Remove existing handlers
        self.logger.handlers = []

        # Console handler with JSON formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # Use colored formatter for better readability
        formatter = ColoredFormatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def _build_log_entry(
        self,
        level: str,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        exc_info: Optional[Exception] = None,
    ) -> Dict[str, Any]:
        """Build structured log entry."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "logger": self.logger.name,
        }

        # Add request context if available
        if has_request_context():
            log_entry["request"] = {
                "method": request.method,
                "path": request.path,
                "remote_addr": request.remote_addr,
                "user_agent": request.headers.get("User-Agent", "Unknown"),
            }

            # Add user info if available
            if hasattr(g, "current_user") and g.current_user:
                log_entry["user"] = {
                    "id": getattr(g.current_user, "id", None),
                    "username": getattr(g.current_user, "username", None),
                }

        # Add extra data
        if extra:
            log_entry["extra"] = extra

        # Add exception info
        if exc_info:
            log_entry["exception"] = {
                "type": type(exc_info).__name__,
                "message": str(exc_info),
                "traceback": traceback.format_exc(),
            }

        return log_entry

    def debug(self, message: str, extra: Optional[Dict] = None):
        """Log debug message."""
        log_entry = self._build_log_entry("DEBUG", message, extra)
        self.logger.debug(json.dumps(log_entry, ensure_ascii=False))

    def info(self, message: str, extra: Optional[Dict] = None):
        """Log info message."""
        log_entry = self._build_log_entry("INFO", message, extra)
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))

    def warning(self, message: str, extra: Optional[Dict] = None):
        """Log warning message."""
        log_entry = self._build_log_entry("WARNING", message, extra)
        self.logger.warning(json.dumps(log_entry, ensure_ascii=False))

    def error(
        self,
        message: str,
        extra: Optional[Dict] = None,
        exc_info: Optional[Exception] = None,
    ):
        """Log error message with optional exception."""
        log_entry = self._build_log_entry("ERROR", message, extra, exc_info)
        self.logger.error(json.dumps(log_entry, ensure_ascii=False))

    def critical(
        self,
        message: str,
        extra: Optional[Dict] = None,
        exc_info: Optional[Exception] = None,
    ):
        """Log critical message with optional exception."""
        log_entry = self._build_log_entry("CRITICAL", message, extra, exc_info)
        self.logger.critical(json.dumps(log_entry, ensure_ascii=False))

    def audit(
        self,
        action: str,
        resource: str,
        resource_id: Optional[int] = None,
        extra: Optional[Dict] = None,
    ):
        """Log user action for audit trail."""
        audit_data = {
            "action": action,
            "resource": resource,
            "resource_id": resource_id,
        }

        if extra:
            audit_data.update(extra)

        log_entry = self._build_log_entry("INFO", "User Action", audit_data)
        log_entry["type"] = "audit"
        self.logger.info(json.dumps(log_entry, ensure_ascii=False))


# Global logger instance
app_logger = StructuredLogger(name="store", level="INFO")


def log_request_response(func):
    """Decorator to log request/response details."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Log request
        start_time = time.time()

        app_logger.info(
            "Incoming Request",
            extra={
                "method": request.method,
                "path": request.path,
                "query_params": dict(request.args),
                "content_type": request.content_type,
            },
        )

        try:
            # Execute route handler
            response = func(*args, **kwargs)

            # Calculate duration
            duration = (time.time() - start_time) * 1000  # ms

            # Log response
            status_code = response[1] if isinstance(response, tuple) else 200
            app_logger.info(
                "Outgoing Response",
                extra={
                    "method": request.method,
                    "path": request.path,
                    "status_code": status_code,
                    "duration_ms": round(duration, 2),
                },
            )

            return response

        except Exception as e:
            duration = (time.time() - start_time) * 1000
            app_logger.error(
                "Request Failed",
                extra={
                    "method": request.method,
                    "path": request.path,
                    "duration_ms": round(duration, 2),
                },
                exc_info=e,
            )
            raise

    return wrapper


def log_db_query(query_type: str, table: str, duration_ms: float, **kwargs):
    """Log database query for monitoring."""
    app_logger.debug(
        "Database Query",
        extra={
            "query_type": query_type,
            "table": table,
            "duration_ms": round(duration_ms, 2),
            **kwargs,
        },
    )


def log_performance_metric(
    metric_name: str, value: float, unit: str = "ms", extra: Optional[Dict] = None
):
    """Log performance metric."""
    metric_data = {"metric": metric_name, "value": value, "unit": unit}

    if extra:
        metric_data.update(extra)

    log_entry = app_logger._build_log_entry("INFO", "Performance Metric", metric_data)
    log_entry["type"] = "performance"
    app_logger.logger.info(json.dumps(log_entry, ensure_ascii=False))


class RequestLoggingMiddleware:
    """
    Flask middleware to automatically log all requests and responses.
    """

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize middleware with Flask app."""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_request(self.teardown_request)

    def before_request(self):
        """Log before request processing."""
        g.request_start_time = time.time()

        app_logger.debug(
            "Request Started",
            extra={
                "method": request.method,
                "path": request.path,
                "endpoint": request.endpoint,
            },
        )

    def after_request(self, response):
        """Log after request processing."""
        if hasattr(g, "request_start_time"):
            duration = (time.time() - g.request_start_time) * 1000

            app_logger.info(
                "Request Completed",
                extra={
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration, 2),
                },
            )

        return response

    def teardown_request(self, exception=None):
        """Log request teardown and any errors."""
        if exception:
            app_logger.error(
                "Request Exception",
                extra={"method": request.method, "path": request.path},
                exc_info=exception,
            )


def init_logging(app, level: str = "INFO"):
    """
    Initialize logging for Flask application.

    Usage:
        from src.utils.logger import init_logging

        app = Flask(__name__)
        init_logging(app, level='INFO')
    """
    global app_logger

    # Set log level from config or parameter
    log_level = app.config.get("LOG_LEVEL", level).upper()
    app_logger = StructuredLogger(name="store", level=log_level)

    # Add request logging middleware
    RequestLoggingMiddleware(app)

    # Log startup
    app_logger.info(
        "Application Started",
        extra={
            "environment": app.config.get("ENV", "production"),
            "debug": app.config.get("DEBUG", False),
        },
    )

    return app_logger


# Export convenience functions
def get_logger(name: Optional[str] = None) -> StructuredLogger:
    """Get logger instance."""
    if name:
        return StructuredLogger(name=name)
    return app_logger


__all__ = [
    "app_logger",
    "get_logger",
    "init_logging",
    "log_request_response",
    "log_db_query",
    "log_performance_metric",
    "RequestLoggingMiddleware",
    "StructuredLogger",
]
