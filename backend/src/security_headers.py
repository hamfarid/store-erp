# -*- coding: utf-8 -*-
# FILE: backend/src/security_headers.py | PURPOSE: Security Headers
# Middleware | OWNER: Backend | RELATED: app.py | LAST-AUDITED: 2025-10-21

"""
وسيط رؤوس الأمان - الإصدار 2.0
Security Headers Middleware - Version 2.0

P0 Fixes Applied:
- P0.4: Secure HTTP Headers (CSP, HSTS, etc.)
"""


def add_security_headers(response):
    """Add security headers to all responses."""
    # Prevent content type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    # Enable XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # Enforce HTTPS
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    # Content Security Policy (CSP) - a restrictive example
    csp = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self'"
    )
    response.headers["Content-Security-Policy"] = csp
    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
