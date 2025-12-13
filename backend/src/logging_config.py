# -*- coding: utf-8 -*-
"""
Structured Logging Configuration
=================================

JSON-based structured logging for Store ERP System.
Part of T24: Monitoring & Logging Enhancement

Features:
- JSON format for easy parsing
- Contextual information (request_id, user_id, etc.)
- Multiple log levels
- File and console handlers
- Integration with Sentry
"""

import logging
import logging.config
import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional
import traceback


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.

    Outputs logs in JSON format with contextual information.
    """

    def __init__(self, include_extra: bool = True):
        super().__init__()
        self.include_extra = include_extra

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        # Base log data
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info),
            }

        # Add extra contextual information
        if self.include_extra:
            # Request context
            if hasattr(record, "request_id"):
                log_data["request_id"] = record.request_id
            if hasattr(record, "user_id"):
                log_data["user_id"] = record.user_id
            if hasattr(record, "username"):
                log_data["username"] = record.username
            if hasattr(record, "ip_address"):
                log_data["ip_address"] = record.ip_address
            if hasattr(record, "method"):
                log_data["http_method"] = record.method
            if hasattr(record, "path"):
                log_data["http_path"] = record.path
            if hasattr(record, "status_code"):
                log_data["http_status"] = record.status_code
            if hasattr(record, "duration_ms"):
                log_data["duration_ms"] = record.duration_ms

            # Business context
            if hasattr(record, "product_id"):
                log_data["product_id"] = record.product_id
            if hasattr(record, "invoice_id"):
                log_data["invoice_id"] = record.invoice_id
            if hasattr(record, "warehouse_id"):
                log_data["warehouse_id"] = record.warehouse_id

            # Performance metrics
            if hasattr(record, "db_queries"):
                log_data["db_queries"] = record.db_queries
            if hasattr(record, "cache_hits"):
                log_data["cache_hits"] = record.cache_hits
            if hasattr(record, "cache_misses"):
                log_data["cache_misses"] = record.cache_misses

        return json.dumps(log_data, ensure_ascii=False)


class ContextFilter(logging.Filter):
    """
    Add contextual information to log records.

    Automatically adds request context from Flask request object.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Add context to log record."""
        try:
            from flask import request, g

            # Add request ID
            if hasattr(g, "request_id"):
                record.request_id = g.request_id

            # Add user info
            if hasattr(g, "current_user"):
                record.user_id = getattr(g.current_user, "id", None)
                record.username = getattr(g.current_user, "username", None)

            # Add request info
            if request:
                record.method = request.method
                record.path = request.path
                record.ip_address = request.remote_addr
        except (RuntimeError, ImportError):
            # Outside request context or Flask not available
            pass

        return True


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = True,
    sentry_dsn: Optional[str] = None,
) -> None:
    """
    Setup structured logging configuration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        json_format: Use JSON format (default: True)
        sentry_dsn: Sentry DSN for error tracking (optional)
    """
    # Create formatters
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    console_handler.addFilter(ContextFilter())

    # File handler (if specified)
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        file_handler.addFilter(ContextFilter())
        handlers.append(file_handler)

    # Root logger configuration
    logging.basicConfig(level=level, handlers=handlers, force=True)

    # Sentry integration (if DSN provided)
    if sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration
            from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[
                    FlaskIntegration(),
                    SqlalchemyIntegration(),
                ],
                traces_sample_rate=0.1,  # 10% of transactions
                profiles_sample_rate=0.1,  # 10% of transactions
                environment="production",
                release="store-erp@1.0.0",
            )

            logging.info(
                "Sentry integration enabled",
                extra={"sentry_dsn": sentry_dsn[:20] + "..."},
            )
        except ImportError:
            logging.warning(
                "Sentry SDK not installed. Install with: pip install sentry-sdk"
            )

    # Silence noisy loggers
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logging.info(
        "Logging configured",
        extra={
            "level": level,
            "json_format": json_format,
            "log_file": log_file,
            "sentry_enabled": bool(sentry_dsn),
        },
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance with context filter.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.addFilter(ContextFilter())
    return logger


# Example usage functions
def log_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: Optional[int] = None,
) -> None:
    """
    Log HTTP request with structured data.

    Args:
        logger: Logger instance
        method: HTTP method
        path: Request path
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        user_id: User ID (optional)
    """
    logger.info(
        f"{method} {path} - {status_code}",
        extra={
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "user_id": user_id,
        },
    )


def log_database_query(
    logger: logging.Logger, query: str, duration_ms: float, rows_affected: int = 0
) -> None:
    """
    Log database query with performance metrics.

    Args:
        logger: Logger instance
        query: SQL query (sanitized)
        duration_ms: Query duration in milliseconds
        rows_affected: Number of rows affected
    """
    logger.debug(
        "Database query executed",
        extra={
            "query": query[:200],  # Truncate long queries
            "duration_ms": duration_ms,
            "rows_affected": rows_affected,
        },
    )


def log_business_event(
    logger: logging.Logger, event_type: str, message: str, **kwargs
) -> None:
    """
    Log business event with custom data.

    Args:
        logger: Logger instance
        event_type: Type of business event
        message: Event message
        **kwargs: Additional context data
    """
    logger.info(message, extra={"event_type": event_type, **kwargs})


# Example: Log product creation
def log_product_created(
    logger: logging.Logger, product_id: int, product_name: str, user_id: int
) -> None:
    """Log product creation event."""
    log_business_event(
        logger,
        event_type="product_created",
        message=f"Product '{product_name}' created",
        product_id=product_id,
        product_name=product_name,
        user_id=user_id,
    )


# Example: Log error with context
def log_error_with_context(
    logger: logging.Logger, error: Exception, context: Dict[str, Any]
) -> None:
    """
    Log error with full context.

    Args:
        logger: Logger instance
        error: Exception object
        context: Additional context data
    """
    logger.error(f"Error occurred: {str(error)}", exc_info=True, extra=context)
