# -*- coding: utf-8 -*-
"""
Sentry Integration Configuration
=================================

Error tracking and performance monitoring with Sentry.
Part of T24: Monitoring & Logging Enhancement

Features:
- Error tracking
- Performance monitoring
- User context
- Custom tags and breadcrumbs
- Release tracking
"""

import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def init_sentry(
    dsn: Optional[str] = None,
    environment: str = "production",
    release: Optional[str] = None,
    traces_sample_rate: float = 0.1,
    profiles_sample_rate: float = 0.1,
    enable_tracing: bool = True,
) -> bool:
    """
    Initialize Sentry SDK.

    Args:
        dsn: Sentry DSN (from environment if not provided)
        environment: Environment name (production, staging, development)
        release: Release version (e.g., "store-erp@1.0.0")
        traces_sample_rate: Percentage of transactions to trace (0.0-1.0)
        profiles_sample_rate: Percentage of transactions to profile (0.0-1.0)
        enable_tracing: Enable performance tracing

    Returns:
        True if Sentry initialized successfully, False otherwise
    """
    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        from sentry_sdk.integrations.redis import RedisIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration

        # Get DSN from environment if not provided
        if not dsn:
            dsn = os.environ.get("SENTRY_DSN")

        if not dsn:
            logger.warning("Sentry DSN not provided. Sentry integration disabled.")
            return False

        # Get release from environment if not provided
        if not release:
            release = os.environ.get("SENTRY_RELEASE", "store-erp@1.0.0")

        # Configure logging integration
        logging_integration = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        )

        # Initialize Sentry
        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            release=release,
            traces_sample_rate=traces_sample_rate if enable_tracing else 0.0,
            profiles_sample_rate=profiles_sample_rate if enable_tracing else 0.0,
            integrations=[
                FlaskIntegration(),
                SqlalchemyIntegration(),
                RedisIntegration(),
                logging_integration,
            ],
            # Send default PII (Personally Identifiable Information)
            send_default_pii=False,
            # Attach stack trace to messages
            attach_stacktrace=True,
            # Maximum breadcrumbs
            max_breadcrumbs=50,
            # Before send callback
            before_send=before_send_callback,
            # Before breadcrumb callback
            before_breadcrumb=before_breadcrumb_callback,
        )

        logger.info(
            f"Sentry initialized successfully",
            extra={
                "environment": environment,
                "release": release,
                "traces_sample_rate": traces_sample_rate,
                "profiles_sample_rate": profiles_sample_rate,
            },
        )

        return True

    except ImportError:
        logger.error("Sentry SDK not installed. Install with: pip install sentry-sdk")
        return False
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {e}", exc_info=True)
        return False


def before_send_callback(
    event: Dict[str, Any], hint: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Callback to modify or filter events before sending to Sentry.

    Args:
        event: Event data
        hint: Additional context

    Returns:
        Modified event or None to drop the event
    """
    # Filter out specific errors
    if "exc_info" in hint:
        exc_type, exc_value, tb = hint["exc_info"]

        # Don't send 404 errors
        if exc_type.__name__ == "NotFound":
            return None

        # Don't send validation errors
        if exc_type.__name__ == "ValidationError":
            return None

    # Add custom tags
    event.setdefault("tags", {})
    event["tags"]["app"] = "store-erp"

    return event


def before_breadcrumb_callback(
    crumb: Dict[str, Any], hint: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Callback to modify or filter breadcrumbs before adding to event.

    Args:
        crumb: Breadcrumb data
        hint: Additional context

    Returns:
        Modified breadcrumb or None to drop it
    """
    # Filter out noisy breadcrumbs
    if crumb.get("category") == "query":
        # Truncate long SQL queries
        if "message" in crumb and len(crumb["message"]) > 200:
            crumb["message"] = crumb["message"][:200] + "..."

    return crumb


def set_user_context(user_id: int, username: str, email: Optional[str] = None):
    """
    Set user context for Sentry events.

    Args:
        user_id: User ID
        username: Username
        email: User email (optional)
    """
    try:
        import sentry_sdk

        sentry_sdk.set_user({"id": user_id, "username": username, "email": email})
    except ImportError:
        pass


def clear_user_context():
    """Clear user context (e.g., on logout)."""
    try:
        import sentry_sdk

        sentry_sdk.set_user(None)
    except ImportError:
        pass


def set_context(context_name: str, context_data: Dict[str, Any]):
    """
    Set custom context for Sentry events.

    Args:
        context_name: Context name (e.g., "product", "invoice")
        context_data: Context data dictionary
    """
    try:
        import sentry_sdk

        sentry_sdk.set_context(context_name, context_data)
    except ImportError:
        pass


def add_breadcrumb(
    message: str,
    category: str = "default",
    level: str = "info",
    data: Optional[Dict[str, Any]] = None,
):
    """
    Add breadcrumb to Sentry event.

    Args:
        message: Breadcrumb message
        category: Breadcrumb category
        level: Breadcrumb level (debug, info, warning, error)
        data: Additional data
    """
    try:
        import sentry_sdk

        sentry_sdk.add_breadcrumb(
            message=message, category=category, level=level, data=data or {}
        )
    except ImportError:
        pass


def capture_exception(error: Exception, **kwargs):
    """
    Manually capture exception to Sentry.

    Args:
        error: Exception object
        **kwargs: Additional context
    """
    try:
        import sentry_sdk

        # Add extra context
        if kwargs:
            with sentry_sdk.push_scope() as scope:
                for key, value in kwargs.items():
                    scope.set_extra(key, value)
                sentry_sdk.capture_exception(error)
        else:
            sentry_sdk.capture_exception(error)

    except ImportError:
        logger.error(f"Exception occurred: {error}", exc_info=True)


def capture_message(message: str, level: str = "info", **kwargs):
    """
    Manually capture message to Sentry.

    Args:
        message: Message to capture
        level: Message level (debug, info, warning, error, fatal)
        **kwargs: Additional context
    """
    try:
        import sentry_sdk

        # Add extra context
        if kwargs:
            with sentry_sdk.push_scope() as scope:
                for key, value in kwargs.items():
                    scope.set_extra(key, value)
                sentry_sdk.capture_message(message, level=level)
        else:
            sentry_sdk.capture_message(message, level=level)

    except ImportError:
        logger.log(getattr(logging, level.upper(), logging.INFO), message)


# Example usage functions


def track_product_error(product_id: int, error: Exception):
    """Track product-related error."""
    set_context("product", {"product_id": product_id})
    add_breadcrumb(
        message=f"Error processing product {product_id}",
        category="product",
        level="error",
    )
    capture_exception(error, product_id=product_id)


def track_invoice_error(invoice_id: int, error: Exception):
    """Track invoice-related error."""
    set_context("invoice", {"invoice_id": invoice_id})
    add_breadcrumb(
        message=f"Error processing invoice {invoice_id}",
        category="invoice",
        level="error",
    )
    capture_exception(error, invoice_id=invoice_id)


def track_database_error(query: str, error: Exception):
    """Track database error."""
    set_context("database", {"query": query[:200]})
    add_breadcrumb(
        message="Database query failed",
        category="database",
        level="error",
        data={"query": query[:200]},
    )
    capture_exception(error, query=query[:200])


# Performance monitoring helpers


def start_transaction(name: str, op: str = "http.server"):
    """
    Start Sentry transaction for performance monitoring.

    Args:
        name: Transaction name
        op: Operation type

    Returns:
        Transaction object or None
    """
    try:
        import sentry_sdk

        return sentry_sdk.start_transaction(name=name, op=op)
    except ImportError:
        return None


def start_span(transaction, op: str, description: str):
    """
    Start Sentry span within transaction.

    Args:
        transaction: Parent transaction
        op: Operation type
        description: Span description

    Returns:
        Span object or None
    """
    try:
        if transaction:
            return transaction.start_child(op=op, description=description)
    except Exception:
        pass
    return None
