"""
FILE: backend/src/modules/security/__init__.py
PURPOSE: Security module exports
OWNER: Security Team
LAST-AUDITED: 2025-12-31

Security Module for Gaara Scan AI

This module provides comprehensive security features including:
- SSTI (Server-Side Template Injection) Protection
- XSS (Cross-Site Scripting) Protection
- SQL Injection Protection
- CSRF Protection
- Rate Limiting
- IP Blocking
- Access Control

Version: 2.0.0
"""

from .ssti_protection import (
    SSTIProtection,
    SSTIMiddleware,
    create_safe_template_context,
    validate_template_string,
    sanitize_user_input,
    check_for_ssti,
    SSTI_PATTERNS,
    DANGEROUS_CHARS,
)

from .security_middleware import SecurityMiddleware, SECURITY_HEADERS
from .access_control import *
from .url_validator import *

__all__ = [
    # SSTI Protection
    "SSTIProtection",
    "SSTIMiddleware",
    "create_safe_template_context",
    "validate_template_string",
    "sanitize_user_input",
    "check_for_ssti",
    "SSTI_PATTERNS",
    "DANGEROUS_CHARS",

    # Security Middleware
    "SecurityMiddleware",
    "SECURITY_HEADERS",
]
