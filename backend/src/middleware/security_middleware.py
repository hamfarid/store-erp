# FILE: backend/src/middleware/security_middleware.py
# PURPOSE: Comprehensive security middleware
#          (HTTPS, HSTS, Headers, CSRF, Rate Limiting)
# OWNER: Backend Security
# RELATED: GLOBAL_GUIDELINES v2.3 §XXI, §XXXIV
# LAST-AUDITED: 2025-10-25

"""
Security Middleware Suite - Production Grade
Implements P0.3, P0.4, P0.5, P0.6 from Global Guidelines Analysis

Features:
- HTTPS enforcement with HSTS
- Comprehensive security headers
- CSRF protection (Flask-WTF)
- Rate limiting (Flask-Limiter)
"""

from functools import wraps
from flask import request, redirect, jsonify, current_app, g
import os
import secrets


class HTTPSMiddleware:
    """
    P0.3: HTTPS Enforcement + HSTS
    Redirects all HTTP traffic to HTTPS in production
    """

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize HTTPS enforcement"""
        app.before_request(self.redirect_to_https)
        app.after_request(self.add_hsts_header)

    def redirect_to_https(self):
        """Redirect HTTP to HTTPS in production"""
        # Check if HTTPS enforcement is enabled
        force_https = os.getenv("FORCE_HTTPS", "false").lower() == "true"

        if force_https and not request.is_secure:
            # Allow localhost for development
            if request.host.startswith("localhost") or request.host.startswith(
                "127.0.0.1"
            ):
                return None

            # Redirect to HTTPS
            url = request.url.replace("http://", "https://", 1)
            return redirect(url, code=301)

        return None

    def add_hsts_header(self, response):
        """Add HSTS header to enforce HTTPS"""
        force_https = os.getenv("FORCE_HTTPS", "false").lower() == "true"

        if force_https:
            # HSTS: Force HTTPS for 1 year, include subdomains
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response


class SecurityHeadersMiddleware:
    """
    P0.6: Security Headers Suite
    Adds comprehensive security headers to all responses
    """

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize security headers"""
        # Generate a per-request CSP nonce before handlers run
        app.before_request(self._generate_csp_nonce)
        app.after_request(self.add_security_headers)

    def _generate_csp_nonce(self):
        """Create a random nonce per request for CSP."""
        try:
            g.csp_nonce = secrets.token_urlsafe(16)
        except Exception:
            g.csp_nonce = None

    def add_security_headers(self, response):
        """Add security headers to response"""

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # XSS Protection (legacy but still useful)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer Policy - strict for privacy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy - disable unnecessary features
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        # Content Security Policy with per-request nonces
        nonce = getattr(g, "csp_nonce", None)
        # Allow external scripts for documentation pages
        script_src_extra = "https://unpkg.com https://cdn.jsdelivr.net"
        extras = f" {script_src_extra}" if script_src_extra else ""
        nonce_part = f" 'nonce-{nonce}'" if nonce else ""
        script_src = f"script-src 'self'{extras}{nonce_part}"
        style_src = "style-src 'self' 'unsafe-inline'"
        csp = (
            "default-src 'self'; "
            f"{script_src}; "
            f"{style_src}; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers["Content-Security-Policy"] = csp

        # Remove server header for security through obscurity
        response.headers.pop("Server", None)

        return response


def init_csrf_protection(app):
    """
    P0.4: Global CSRF Middleware
    Initialize Flask-WTF CSRF protection
    """
    try:
        from flask_wtf.csrf import CSRFProtect

        csrf = CSRFProtect()
        csrf.init_app(app)

        # Configure CSRF
        app.config["WTF_CSRF_ENABLED"] = True
        app.config["WTF_CSRF_TIME_LIMIT"] = None  # No time limit
        app.config["WTF_CSRF_SSL_STRICT"] = True  # Require HTTPS in production
        app.config["WTF_CSRF_METHODS"] = ["POST", "PUT", "PATCH", "DELETE"]

        print("✅ CSRF Protection enabled globally")
        return csrf

    except ImportError:
        print("⚠️  Flask-WTF not installed. CSRF protection disabled.")
        print("   Install: pip install Flask-WTF")
        return None


def init_rate_limiting(app):
    """
    P0.5: Rate Limiting (Flask-Limiter)
    Prevent brute force attacks
    """
    try:
        from flask_limiter import Limiter
        from flask_limiter.util import get_remote_address

        # Initialize limiter
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=["100 per minute", "2000 per hour"],
            storage_uri=os.getenv("REDIS_URL", "memory://"),
            strategy="fixed-window",
        )

        # Stricter limits for authentication endpoints
        # Applied in routes via @limiter.limit("5 per minute")

        print("✅ Rate Limiting enabled")
        print("   Global: 100 req/min, 2000 req/hour")
        print(f"   Storage: {os.getenv('REDIS_URL', 'memory (development)')}")

        return limiter

    except ImportError:
        print("⚠️  Flask-Limiter not installed. Rate limiting disabled.")
        print("   Install: pip install Flask-Limiter")
        return None


def require_api_key(f):
    """
    Optional: API Key authentication decorator
    Use for external API clients
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return (
                jsonify(
                    {
                        "code": "MISSING_API_KEY",
                        "message": "API key is required",
                        "traceId": request.headers.get("X-Trace-Id", "unknown"),
                    }
                ),
                401,
            )

        # Validate API key (implement your validation logic)
        valid_keys = current_app.config.get("VALID_API_KEYS", [])

        if api_key not in valid_keys:
            return (
                jsonify(
                    {
                        "code": "INVALID_API_KEY",
                        "message": "Invalid API key",
                        "traceId": request.headers.get("X-Trace-Id", "unknown"),
                    }
                ),
                401,
            )

        return f(*args, **kwargs)

    return decorated_function


def init_all_security_middleware(app):
    """
    Initialize all security middleware
    Call this from app.py

    Returns:
        dict: Initialized middleware objects (csrf, limiter)
    """
    print("\n🔒 Initializing Security Middleware Suite...")

    # P0.3: HTTPS Enforcement + HSTS
    https_middleware = HTTPSMiddleware(app)
    print("✅ HTTPS Enforcement enabled")

    # P0.6: Security Headers
    headers_middleware = SecurityHeadersMiddleware(app)
    print("✅ Security Headers enabled")

    # P0.4: CSRF Protection
    csrf = init_csrf_protection(app)

    # P0.5: Rate Limiting
    limiter = init_rate_limiting(app)

    print("🔒 Security Middleware Suite initialized\n")

    return {
        "https": https_middleware,
        "headers": headers_middleware,
        "csrf": csrf,
        "limiter": limiter,
    }


# Startup validation
def validate_security_config(app):
    """
    Validate that all security requirements are met
    Fails fast on production if security is compromised
    """
    errors = []
    warnings = []

    # Check bcrypt availability
    try:
        import bcrypt

        if not hasattr(bcrypt, "checkpw"):
            errors.append("bcrypt is installed but broken")
    except ImportError:
        errors.append("bcrypt is not installed - CRITICAL for password hashing")

    # Check HTTPS enforcement in production
    env = os.getenv("FLASK_ENV", "production")
    force_https = os.getenv("FORCE_HTTPS", "false").lower() == "true"

    if env == "production" and not force_https:
        errors.append("FORCE_HTTPS must be 'true' in production")

    # Check secret key
    secret_key = app.config.get("SECRET_KEY")
    if not secret_key or secret_key == "dev":
        errors.append("SECRET_KEY must be set to a strong random value")

    # Check CSRF
    if not app.config.get("WTF_CSRF_ENABLED"):
        warnings.append("CSRF protection is disabled")

    # Report
    if errors:
        print("\n❌ SECURITY VALIDATION FAILED:")
        for error in errors:
            print(f"   - {error}")

        if env == "production":
            raise RuntimeError(
                "Security validation failed. Cannot start in production mode. "
                f"Errors: {'; '.join(errors)}"
            )

    if warnings:
        print("\n⚠️  SECURITY WARNINGS:")
        for warning in warnings:
            print(f"   - {warning}")

    if not errors and not warnings:
        print("✅ Security validation passed")

    return len(errors) == 0
