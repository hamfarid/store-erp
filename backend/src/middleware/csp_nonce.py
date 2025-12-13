#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FILE: backend/src/middleware/csp_nonce.py | PURPOSE: P0.13 CSP Nonce Generation | OWNER: Security
"""
/backend/src/middleware/csp_nonce.py

P0.13: Content Security Policy (CSP) Nonce Generation

Provides:
- Cryptographically secure nonce generation per request
- CSP header configuration with nonces
- Template context injection for nonce usage

This replaces 'unsafe-inline' with nonce-based script/style execution.
"""

import secrets
import base64
from flask import g, request
import logging

logger = logging.getLogger(__name__)


def generate_nonce() -> str:
    """
    P0.13: Generate a cryptographically secure nonce

    Returns:
        Base64-encoded 128-bit random nonce
    """
    return base64.b64encode(secrets.token_bytes(16)).decode("utf-8")


def get_csp_nonce() -> str:
    """
    P0.13: Get or create CSP nonce for current request

    The nonce is stored in Flask's g object to ensure
    the same nonce is used throughout the request.

    Returns:
        The CSP nonce for the current request
    """
    if not hasattr(g, "csp_nonce"):
        g.csp_nonce = generate_nonce()
    return g.csp_nonce


def build_csp_header(nonce: str, is_production: bool = True) -> str:
    """
    P0.13: Build CSP header with nonce

    Args:
        nonce: The request-specific nonce
        is_production: Whether running in production mode

    Returns:
        Complete CSP header value
    """
    if is_production:
        # Production CSP - strict with nonces
        return (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
            f"style-src 'self' 'nonce-{nonce}' https://fonts.googleapis.com; "
            f"font-src 'self' https://fonts.gstatic.com; "
            f"img-src 'self' data: https:; "
            f"connect-src 'self' https:; "
            f"frame-ancestors 'none'; "
            f"base-uri 'self'; "
            f"form-action 'self'; "
            f"upgrade-insecure-requests"
        )
    else:
        # Development CSP - more permissive but still uses nonces
        return (
            f"default-src 'self' 'unsafe-eval'; "
            f"script-src 'self' 'nonce-{nonce}' 'unsafe-eval' https://cdn.jsdelivr.net; "
            f"style-src 'self' 'nonce-{nonce}' 'unsafe-inline' https://fonts.googleapis.com; "
            f"font-src 'self' https://fonts.gstatic.com data:; "
            f"img-src 'self' data: https: http:; "
            f"connect-src 'self' ws: wss: http: https:; "
            f"frame-ancestors 'self'"
        )


def init_csp_nonce(app):
    """
    P0.13: Initialize CSP nonce middleware for Flask app

    This sets up:
    1. Before-request handler to generate nonce
    2. After-request handler to set CSP header
    3. Context processor for template nonce access

    Args:
        app: Flask application instance
    """
    import os

    is_production = os.environ.get("FLASK_ENV") == "production"

    @app.before_request
    def _generate_csp_nonce():
        """Generate nonce before each request"""
        g.csp_nonce = generate_nonce()

    @app.after_request
    def _add_csp_header(response):
        """Add CSP header with nonce to response"""
        try:
            nonce = getattr(g, "csp_nonce", None)
            if nonce:
                # Only set CSP for HTML responses (not API JSON)
                content_type = response.headers.get("Content-Type", "")
                if "text/html" in content_type:
                    response.headers["Content-Security-Policy"] = build_csp_header(
                        nonce, is_production
                    )
                    # Also set report-only header for monitoring in production
                    if is_production:
                        response.headers["Content-Security-Policy-Report-Only"] = (
                            "default-src 'self'; " "report-uri /api/csp-report"
                        )
        except Exception as e:
            logger.warning(f"Error setting CSP header: {e}")
        return response

    @app.context_processor
    def _inject_csp_nonce():
        """Inject nonce into Jinja2 template context"""
        return {"csp_nonce": get_csp_nonce}

    logger.info("✅ P0.13: CSP nonce middleware initialized")


def csp_report_endpoint(app):
    """
    P0.13: Set up CSP violation report endpoint

    This endpoint receives CSP violation reports from browsers.
    """

    @app.route("/api/csp-report", methods=["POST"])
    def _csp_report():
        """Receive and log CSP violation reports"""
        try:
            report = request.get_json(force=True, silent=True)
            if report:
                csp_report = report.get("csp-report", report)
                logger.warning(
                    f"P0.13 CSP Violation: {csp_report.get('violated-directive', 'unknown')} "
                    f"on {csp_report.get('document-uri', 'unknown')} "
                    f"blocked: {csp_report.get('blocked-uri', 'unknown')}"
                )
        except Exception as e:
            logger.error(f"Error processing CSP report: {e}")

        # Always return 204 to acknowledge receipt
        return "", 204


# Utility function for templates
def nonce_attr() -> str:
    """
    P0.13: Get nonce attribute for inline scripts/styles

    Usage in Jinja2 templates:
        <script {{ nonce_attr() }}>...</script>
        <style {{ nonce_attr() }}>...</style>

    Returns:
        HTML attribute string: nonce="xxx"
    """
    return f'nonce="{get_csp_nonce()}"'


__all__ = [
    "generate_nonce",
    "get_csp_nonce",
    "build_csp_header",
    "init_csp_nonce",
    "csp_report_endpoint",
    "nonce_attr",
]
