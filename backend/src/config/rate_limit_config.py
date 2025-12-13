#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1.32: Flask-Limiter Configuration with Redis Backend

This module provides centralized rate limiting configuration for the application.
Uses Redis as the storage backend for distributed rate limiting in production.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# =============================================================================
# Rate Limit Configurations
# =============================================================================


class RateLimitConfig:
    """
    P1.32: Centralized rate limit configuration.

    All rate limits are defined here for easy management and consistency.
    """

    # Default limits for all endpoints
    DEFAULT_LIMITS = ["100 per minute", "2000 per hour"]

    # Authentication endpoints - stricter limits
    AUTH_LOGIN = "5 per minute"
    AUTH_REGISTER = "3 per minute"
    AUTH_REFRESH = "10 per minute"
    AUTH_PASSWORD_RESET = "3 per hour"
    AUTH_PASSWORD_CHANGE = "5 per hour"

    # API endpoints
    API_READ = "100 per minute"
    API_WRITE = "30 per minute"
    API_DELETE = "10 per minute"
    API_BULK = "5 per minute"

    # Search and report endpoints
    SEARCH = "30 per minute"
    REPORTS = "10 per minute"
    EXPORT = "5 per minute"

    # File upload
    FILE_UPLOAD = "10 per minute"

    # RAG/AI endpoints
    RAG_QUERY = "20 per minute"

    # Admin endpoints
    ADMIN = "50 per minute"


def get_redis_url() -> Optional[str]:
    """
    Get Redis URL from environment variables.

    Checks multiple environment variable names for flexibility.
    """
    redis_url = (
        os.environ.get("REDIS_URL")
        or os.environ.get("RATELIMIT_STORAGE_URL")
        or os.environ.get("CACHE_REDIS_URL")
    )

    if redis_url:
        logger.info("P1.32: Redis URL configured for rate limiting")
    else:
        logger.warning("P1.32: No Redis URL found - using in-memory storage")

    return redis_url


def get_storage_uri() -> str:
    """
    Get the storage URI for Flask-Limiter.

    Returns Redis URL if available, otherwise uses in-memory storage.
    """
    redis_url = get_redis_url()

    if redis_url:
        return redis_url

    # Fallback to in-memory storage (not recommended for production)
    return "memory://"


def get_key_func():
    """
    Get the key function for identifying clients.

    Uses X-Forwarded-For header if behind a proxy, otherwise remote_addr.
    """
    from flask import request

    def key_func():
        # Check for proxy headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP (client IP)
            return forwarded_for.split(",")[0].strip()

        # Check for X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fallback to remote_addr
        return request.remote_addr or "127.0.0.1"

    return key_func


def init_limiter(app):
    """
    P1.32: Initialize Flask-Limiter with Redis backend.

    Args:
        app: Flask application instance

    Returns:
        Limiter instance or None if not available
    """
    try:
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address
    except ImportError:
        logger.warning("P1.32: Flask-Limiter not installed - rate limiting disabled")
        logger.info("Install with: pip install Flask-Limiter[redis]")
        return None

    storage_uri = get_storage_uri()

    # Configure limiter
    limiter = Limiter(
        app=app,
        key_func=get_key_func(),
        default_limits=RateLimitConfig.DEFAULT_LIMITS,
        storage_uri=storage_uri,
        strategy="fixed-window",  # or "moving-window" for stricter limiting
        headers_enabled=True,  # Add rate limit headers to responses
        # Retry-After header on rate limit exceeded
        retry_after="delta-seconds",
        # Enable swallow_errors in production to not fail on storage errors
        swallow_errors=app.config.get("ENV") == "production",
    )

    # Configure exempt routes
    @limiter.request_filter
    def exempt_health_check():
        """Exempt health check endpoint from rate limiting."""
        from flask import request

        return request.path in ["/api/health", "/health", "/api/system/health"]

    # Log configuration
    logger.info(f"P1.32: Flask-Limiter initialized with storage: {storage_uri[:20]}...")
    logger.info(f"P1.32: Default limits: {RateLimitConfig.DEFAULT_LIMITS}")

    return limiter


def apply_auth_limits(limiter):
    """
    P1.32: Apply rate limits to authentication endpoints.

    Args:
        limiter: Flask-Limiter instance
    """
    if not limiter:
        return

    # These decorators will be applied in the auth routes
    return {
        "login": limiter.limit(RateLimitConfig.AUTH_LOGIN),
        "register": limiter.limit(RateLimitConfig.AUTH_REGISTER),
        "refresh": limiter.limit(RateLimitConfig.AUTH_REFRESH),
        "password_reset": limiter.limit(RateLimitConfig.AUTH_PASSWORD_RESET),
        "password_change": limiter.limit(RateLimitConfig.AUTH_PASSWORD_CHANGE),
    }


def apply_api_limits(limiter):
    """
    P1.32: Apply rate limits to API endpoints.

    Args:
        limiter: Flask-Limiter instance
    """
    if not limiter:
        return

    return {
        "read": limiter.limit(RateLimitConfig.API_READ),
        "write": limiter.limit(RateLimitConfig.API_WRITE),
        "delete": limiter.limit(RateLimitConfig.API_DELETE),
        "bulk": limiter.limit(RateLimitConfig.API_BULK),
        "search": limiter.limit(RateLimitConfig.SEARCH),
        "reports": limiter.limit(RateLimitConfig.REPORTS),
        "export": limiter.limit(RateLimitConfig.EXPORT),
        "upload": limiter.limit(RateLimitConfig.FILE_UPLOAD),
        "rag": limiter.limit(RateLimitConfig.RAG_QUERY),
        "admin": limiter.limit(RateLimitConfig.ADMIN),
    }


# Rate limit exceeded handler
def rate_limit_exceeded_handler(e):
    """
    P1.32: Custom handler for rate limit exceeded errors.

    Returns a JSON response with error details.
    """
    from flask import jsonify

    return (
        jsonify(
            {
                "success": False,
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "تم تجاوز الحد الأقصى للطلبات. يرجى المحاولة لاحقاً.",
                    "message_en": "Too many requests. Please try again later.",
                    "retry_after": e.description if hasattr(e, "description") else 60,
                },
            }
        ),
        429,
    )


__all__ = [
    "RateLimitConfig",
    "get_redis_url",
    "get_storage_uri",
    "get_key_func",
    "init_limiter",
    "apply_auth_limits",
    "apply_api_limits",
    "rate_limit_exceeded_handler",
]
