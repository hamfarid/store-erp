#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1.35: Route Security & Obfuscation Middleware

Provides security enhancements for API routes:
- Route obfuscation (hiding internal structure)
- Request fingerprinting
- Honeypot endpoints
- API versioning abstraction
- Response sanitization
"""

import os
import re
import uuid
import hmac
import hashlib
import logging
import time
from functools import wraps
from typing import Dict, List, Optional, Callable, Any
from flask import request, jsonify, g, current_app
from datetime import datetime

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

ROUTE_SECRET = os.environ.get("ROUTE_OBFUSCATION_SECRET", "change-me-in-production")
ENABLE_HONEYPOTS = os.environ.get("ENABLE_HONEYPOTS", "true").lower() == "true"
ENABLE_FINGERPRINTING = (
    os.environ.get("ENABLE_REQUEST_FINGERPRINTING", "true").lower() == "true"
)
BLOCK_SUSPICIOUS_PATTERNS = (
    os.environ.get("BLOCK_SUSPICIOUS_PATTERNS", "true").lower() == "true"
)


# =============================================================================
# Suspicious Pattern Detection
# =============================================================================

# Patterns that indicate automated scanning or attack attempts
SUSPICIOUS_PATTERNS = [
    # Common vulnerability scanners
    r"\.\./",  # Directory traversal
    r"%2e%2e",  # URL encoded traversal
    r"\.git",
    r"\.env",
    r"\.htaccess",
    r"wp-admin",
    r"wp-login",
    r"wp-content",
    r"phpinfo",
    r"phpmyadmin",
    r"administrator",
    r"admin\.php",
    r"config\.php",
    r"shell\.php",
    r"eval\(",
    r"base64_decode",
    r"<script",
    r"javascript:",
    r"onload=",
    r"onerror=",
    # SQL injection patterns
    r"'(\s)*(or|and)(\s)*'",
    r"union(\s)+select",
    r"select(\s)+.*(\s)+from",
    r"insert(\s)+into",
    r"delete(\s)+from",
    r"drop(\s)+table",
    r"exec(\s)*\(",
    # Command injection
    r";\s*(ls|cat|pwd|whoami|id|uname)",
    r"\|\s*(ls|cat|pwd|whoami|id|uname)",
    r"`.*`",
    r"\$\(.*\)",
]

# Compile patterns for efficiency
COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in SUSPICIOUS_PATTERNS]


# =============================================================================
# Request Fingerprinting
# =============================================================================


class RequestFingerprinter:
    """
    P1.35: Creates unique fingerprints for requests to detect bots and abuse.
    """

    @staticmethod
    def generate_fingerprint() -> str:
        """Generate a fingerprint from request characteristics."""
        components = [
            request.remote_addr or "",
            request.headers.get("User-Agent", ""),
            request.headers.get("Accept-Language", ""),
            request.headers.get("Accept-Encoding", ""),
            request.headers.get("Accept", ""),
            str(request.headers.get("DNT", "")),
        ]

        fingerprint_string = "|".join(components)
        return hashlib.sha256(fingerprint_string.encode()).hexdigest()[:32]

    @staticmethod
    def is_likely_bot() -> bool:
        """Detect if request is likely from a bot."""
        user_agent = request.headers.get("User-Agent", "").lower()

        # No user agent
        if not user_agent:
            return True

        # Known bot patterns
        bot_patterns = [
            "bot",
            "spider",
            "crawl",
            "scrape",
            "scan",
            "curl",
            "wget",
            "python",
            "java",
            "ruby",
            "nikto",
            "sqlmap",
            "nmap",
            "masscan",
            "dirbuster",
            "gobuster",
            "wfuzz",
            "ffuf",
            "nuclei",
            "httpx",
            "burp",
            "zap",
        ]

        for pattern in bot_patterns:
            if pattern in user_agent:
                return True

        # Missing typical browser headers
        if not request.headers.get("Accept-Language"):
            return True

        return False


# =============================================================================
# Honeypot Endpoints
# =============================================================================


class HoneypotManager:
    """
    P1.35: Manages honeypot endpoints to detect attackers.

    Honeypots are fake endpoints that legitimate users would never access.
    Any access to these endpoints indicates malicious activity.
    """

    HONEYPOT_PATHS = [
        "/admin.php",
        "/wp-admin",
        "/wp-login.php",
        "/phpmyadmin",
        "/phpMyAdmin",
        "/.env",
        "/.git/config",
        "/config.php",
        "/backup.sql",
        "/database.sql",
        "/debug",
        "/trace",
        "/actuator",
        "/actuator/health",
        "/console",
        "/manager/html",
        "/solr/admin",
        "/api/v1/debug",
        "/api/internal",
    ]

    _blocked_ips: Dict[str, datetime] = {}

    @classmethod
    def is_honeypot_path(cls, path: str) -> bool:
        """Check if path is a honeypot."""
        path_lower = path.lower()
        return any(hp.lower() in path_lower for hp in cls.HONEYPOT_PATHS)

    @classmethod
    def record_honeypot_access(cls, ip: str, path: str) -> None:
        """Record access to honeypot and potentially block IP."""
        logger.warning(
            f"P1.35: Honeypot accessed - IP: {ip}, Path: {path}, "
            f"User-Agent: {request.headers.get('User-Agent', 'N/A')}"
        )

        # Block the IP
        cls._blocked_ips[ip] = datetime.utcnow()

    @classmethod
    def is_ip_blocked(cls, ip: str) -> bool:
        """Check if IP is blocked due to honeypot access."""
        if ip in cls._blocked_ips:
            # Block for 24 hours
            blocked_at = cls._blocked_ips[ip]
            hours_blocked = (datetime.utcnow() - blocked_at).total_seconds() / 3600
            return hours_blocked < 24
        return False


# =============================================================================
# Route Obfuscation
# =============================================================================


class RouteObfuscator:
    """
    P1.35: Obfuscates internal route information from error responses.
    """

    # Internal paths to hide from error messages
    INTERNAL_PATHS = [
        "/backend/",
        "/src/",
        "/app/",
        "/internal/",
        "/private/",
        "/admin/",
    ]

    @classmethod
    def sanitize_error_response(cls, error_message: str) -> str:
        """Remove internal path information from error messages."""
        sanitized = error_message

        # Remove file paths
        sanitized = re.sub(
            r"/[a-zA-Z0-9_\-./]+\.(py|js|ts|jsx|tsx)", "[redacted]", sanitized
        )

        # Remove line numbers
        sanitized = re.sub(r"line \d+", "line [redacted]", sanitized)

        # Remove stack trace details
        sanitized = re.sub(r'File "[^"]+"', 'File "[redacted]"', sanitized)

        # Remove internal function names
        sanitized = re.sub(r"in \w+\(\)", "in [redacted]()", sanitized)

        return sanitized

    @classmethod
    def generate_request_id(cls) -> str:
        """Generate a unique, non-sequential request ID."""
        timestamp = int(time.time() * 1000)
        random_part = uuid.uuid4().hex[:8]

        # Create HMAC to prevent guessing
        message = f"{timestamp}:{random_part}"
        signature = hmac.new(
            ROUTE_SECRET.encode(), message.encode(), hashlib.sha256
        ).hexdigest()[:8]

        return f"req_{random_part}{signature}"


# =============================================================================
# Security Headers
# =============================================================================


def add_security_headers(response):
    """Add security headers to prevent information leakage."""
    # Remove server identification
    response.headers.pop("Server", None)
    response.headers.pop("X-Powered-By", None)

    # Add security headers
    response.headers["X-Request-ID"] = g.get("request_id", "unknown")
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Remove headers that leak info
    response.headers.pop("X-AspNet-Version", None)
    response.headers.pop("X-AspNetMvc-Version", None)

    return response


# =============================================================================
# Middleware Functions
# =============================================================================


def route_security_middleware():
    """
    P1.35: Main security middleware for all requests.

    Call this in before_request handler.
    """
    # Generate request ID
    g.request_id = RouteObfuscator.generate_request_id()
    g.request_start_time = time.time()

    # Get client IP
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(",")[0].strip()

    # Check if IP is blocked
    if ENABLE_HONEYPOTS and HoneypotManager.is_ip_blocked(client_ip):
        logger.warning(f"P1.35: Blocked IP attempted access: {client_ip}")
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "ACCESS_DENIED",
                        "message": "Access denied",
                        "request_id": g.request_id,
                    },
                }
            ),
            403,
        )

    # Check honeypot
    if ENABLE_HONEYPOTS and HoneypotManager.is_honeypot_path(request.path):
        HoneypotManager.record_honeypot_access(client_ip, request.path)
        # Return fake response to waste attacker's time
        time.sleep(2)  # Slow down automated tools
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": "Resource not found",
                        "request_id": g.request_id,
                    },
                }
            ),
            404,
        )

    # Check for suspicious patterns
    if BLOCK_SUSPICIOUS_PATTERNS:
        full_path = request.full_path or ""
        for pattern in COMPILED_PATTERNS:
            if pattern.search(full_path):
                logger.warning(
                    f"P1.35: Suspicious pattern detected - IP: {client_ip}, "
                    f"Path: {full_path}, Pattern: {pattern.pattern}"
                )
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": {
                                "code": "BAD_REQUEST",
                                "message": "Invalid request",
                                "request_id": g.request_id,
                            },
                        }
                    ),
                    400,
                )

    # Generate fingerprint
    if ENABLE_FINGERPRINTING:
        g.request_fingerprint = RequestFingerprinter.generate_fingerprint()
        g.is_likely_bot = RequestFingerprinter.is_likely_bot()

    return None


def secure_route(require_human: bool = False):
    """
    P1.35: Decorator for additional route security.

    Usage:
        @app.route('/api/sensitive')
        @secure_route(require_human=True)
        def sensitive_endpoint():
            ...

    Args:
        require_human: If True, block likely bot requests
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if bot when human required
            if require_human and g.get("is_likely_bot", False):
                logger.warning(
                    f"P1.35: Bot blocked from human-only endpoint - "
                    f"Path: {request.path}, Fingerprint: {g.get('request_fingerprint', 'N/A')}"
                )
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": {
                                "code": "ACCESS_DENIED",
                                "message": "This endpoint requires a valid browser session",
                                "request_id": g.get("request_id", "unknown"),
                            },
                        }
                    ),
                    403,
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator


# =============================================================================
# Flask App Integration
# =============================================================================


def init_route_security(app):
    """
    P1.35: Initialize route security for Flask app.

    Usage:
        from src.middleware.route_security import init_route_security
        init_route_security(app)
    """

    @app.before_request
    def _security_middleware():
        return route_security_middleware()

    @app.after_request
    def _add_security_headers(response):
        return add_security_headers(response)

    # Register honeypot endpoints
    if ENABLE_HONEYPOTS:
        for path in HoneypotManager.HONEYPOT_PATHS:
            try:

                @app.route(path, methods=["GET", "POST", "PUT", "DELETE"])
                def honeypot_handler():
                    return jsonify({"error": "Not found"}), 404

            except Exception:
                pass  # Path might conflict with existing routes

    logger.info("P1.35: Route security middleware initialized")


__all__ = [
    "init_route_security",
    "route_security_middleware",
    "secure_route",
    "RouteObfuscator",
    "RequestFingerprinter",
    "HoneypotManager",
    "add_security_headers",
]
