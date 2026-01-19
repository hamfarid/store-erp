"""
FILE: backend/src/modules/security/ssti_protection.py
PURPOSE: Server-Side Template Injection (SSTI) Protection
OWNER: Security Team
LAST-AUDITED: 2025-12-31

SSTI (Server-Side Template Injection) Protection Module

This module provides comprehensive protection against SSTI attacks by:
- Detecting SSTI payloads in user input
- Sanitizing template-related characters
- Providing safe template rendering utilities
- Blocking malicious template expressions

Supported Template Engines Protection:
- Jinja2
- Django Templates
- Mako
- Tornado
- Chameleon
- Cheetah

Security Features:
- Pattern-based detection for multiple template engines
- Input sanitization before template rendering
- Safe template environment configuration
- Audit logging of blocked attempts

Version: 1.0.0
"""

import html
import json
import logging
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Setup logger
logger = logging.getLogger(__name__)


# SSTI detection patterns for various template engines
SSTI_PATTERNS = {
    # Jinja2 patterns
    "jinja2": [
        r"\{\{.*?\}\}",  # {{ expression }}
        r"\{%.*?%\}",    # {% statement %}
        r"\{#.*?#\}",    # {# comment #}
        r"\{\{.*?config.*?\}\}",  # Config access
        r"\{\{.*?request.*?\}\}",  # Request access
        r"\{\{.*?self.*?\}\}",    # Self reference
        r"\{\{.*?__class__.*?\}\}",  # Class access
        r"\{\{.*?__mro__.*?\}\}",    # MRO access
        r"\{\{.*?__subclasses__.*?\}\}",  # Subclasses
        r"\{\{.*?__globals__.*?\}\}",     # Globals
        r"\{\{.*?__builtins__.*?\}\}",    # Builtins
        r"\{\{.*?lipsum.*?\}\}",          # Lipsum (common bypass)
        r"\{\{.*?cycler.*?\}\}",          # Cycler
        r"\{\{.*?joiner.*?\}\}",          # Joiner
        r"\{\{.*?namespace.*?\}\}",       # Namespace
        r"\{\{.*?\|attr\(.*?\}\}",        # attr filter
        r"\{\{.*?\.popen\(.*?\}\}",       # popen execution
        r"\{\{.*?subprocess.*?\}\}",       # subprocess
        r"\{\{.*?os\..*?\}\}",             # os module
        r"\{\{.*?importlib.*?\}\}",        # importlib
    ],

    # Django Template patterns
    "django": [
        r"\{\{.*?\}\}",
        r"\{%.*?%\}",
        r"\{%\s*debug\s*%\}",        # Debug tag
        r"\{%\s*include\s+.*?%\}",    # Include tag
        r"\{%\s*load\s+.*?%\}",       # Load tag
        r"\{%\s*ssi\s+.*?%\}",        # SSI tag
        r"\{%\s*templatetag.*?%\}",   # Templatetag
    ],

    # Mako patterns
    "mako": [
        r"\$\{.*?\}",           # ${expression}
        r"<%.*?%>",             # <% code %>
        r"<%!.*?%>",            # <%! module-level %>
        r"<%def.*?>.*?</%def>",  # <%def> blocks
        r"<%block.*?>.*?</%block>",  # <%block>
        r"<%namespace.*?/>",         # <%namespace>
        r"<%include.*?/>",           # <%include>
    ],

    # Tornado patterns
    "tornado": [
        r"\{\{.*?\}\}",
        r"\{%.*?%\}",
        r"\{\{.*?handler.*?\}\}",     # Handler access
        r"\{\{.*?application.*?\}\}",  # Application access
    ],

    # Expression Language patterns
    "expression_language": [
        r"\$\{.*?\}",    # ${expression}
        r"#\{.*?\}",     # #{expression}
        r"\[\%.*?\%\]",  # [% expression %]
    ],

    # Python code execution patterns (general)
    "python_exec": [
        r"exec\s*\(",
        r"eval\s*\(",
        r"compile\s*\(",
        r"__import__\s*\(",
        r"open\s*\(",
        r"file\s*\(",
        r"input\s*\(",
        r"raw_input\s*\(",
        r"execfile\s*\(",
        r"reload\s*\(",
    ],

    # Common SSTI payloads
    "common_payloads": [
        r"7\*7",              # Basic arithmetic test
        r"{{7\*7}}",          # Jinja2 arithmetic
        r"\${7\*7}",          # Mako arithmetic
        r"{{7\*\'7\'}}",      # String multiplication
        r"{{config}}",        # Config access
        r"{{self}}",          # Self reference
        r"{{request}}",       # Request object
        r"{{\'\'.__class__}}",  # Class access
        r"\[\[.*?\]\]",       # Double brackets (some engines)
        r"<%=.*?%>",          # ERB-style
        r"#set\s*\(",         # Velocity
        r"#foreach",          # Velocity loop
    ],
}

# Dangerous characters/strings to sanitize
DANGEROUS_CHARS = {
    "{{": "&#123;&#123;",
    "}}": "&#125;&#125;",
    "{%": "&#123;&#37;",
    "%}": "&#37;&#125;",
    "{#": "&#123;&#35;",
    "#}": "&#35;&#125;",
    "${": "&#36;&#123;",
    "<%": "&#60;&#37;",
    "%>": "&#37;&#62;",
    "#{": "&#35;&#123;",
}


class SSTIProtection:
    """
    SSTI Protection Class

    Provides methods to detect and sanitize SSTI payloads.
    """

    def __init__(
        self,
        enabled_engines: Optional[List[str]] = None,
        custom_patterns: Optional[List[str]] = None,
        strict_mode: bool = True,
        log_attempts: bool = True,
        block_on_detection: bool = True
    ):
        """
        Initialize SSTI Protection

        Args:
            enabled_engines: List of template engines to protect against
            custom_patterns: Additional custom patterns to detect
            strict_mode: If True, blocks any template-like syntax
            log_attempts: If True, logs all blocked attempts
            block_on_detection: If True, blocks request on detection
        """
        self.strict_mode = strict_mode
        self.log_attempts = log_attempts
        self.block_on_detection = block_on_detection

        # Build regex patterns
        self.patterns: List[re.Pattern] = []

        # Add patterns for enabled engines
        engines = enabled_engines or list(SSTI_PATTERNS.keys())
        for engine in engines:
            if engine in SSTI_PATTERNS:
                for pattern in SSTI_PATTERNS[engine]:
                    try:
                        self.patterns.append(
                            re.compile(pattern, re.IGNORECASE | re.DOTALL)
                        )
                    except re.error as e:
                        logger.warning(f"Invalid regex pattern {pattern}: {e}")

        # Add custom patterns
        if custom_patterns:
            for pattern in custom_patterns:
                try:
                    self.patterns.append(
                        re.compile(pattern, re.IGNORECASE | re.DOTALL)
                    )
                except re.error as e:
                    logger.warning(f"Invalid custom pattern {pattern}: {e}")

        logger.info(f"SSTI Protection initialized with {len(self.patterns)} patterns")

    def detect_ssti(self, content: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Detect SSTI payload in content

        Args:
            content: String content to check

        Returns:
            Tuple of (is_detected, matched_pattern, matched_content)
        """
        if not content:
            return False, None, None

        for pattern in self.patterns:
            match = pattern.search(content)
            if match:
                if self.log_attempts:
                    logger.warning(
                        f"SSTI attempt detected - Pattern: {pattern.pattern}, "
                        f"Match: {match.group()[:100]}"
                    )
                return True, pattern.pattern, match.group()

        return False, None, None

    def detect_in_dict(
        self,
        data: Dict[str, Any],
        path: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Recursively detect SSTI in dictionary values

        Args:
            data: Dictionary to check
            path: Current path in dictionary (for logging)

        Returns:
            List of detections with details
        """
        detections = []

        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            if isinstance(value, str):
                is_detected, pattern, match = self.detect_ssti(value)
                if is_detected:
                    detections.append({
                        "path": current_path,
                        "pattern": pattern,
                        "match": match,
                        "value": value[:200]  # Truncate for logging
                    })
            elif isinstance(value, dict):
                detections.extend(self.detect_in_dict(value, current_path))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str):
                        is_detected, pattern, match = self.detect_ssti(item)
                        if is_detected:
                            detections.append({
                                "path": f"{current_path}[{i}]",
                                "pattern": pattern,
                                "match": match,
                                "value": item[:200]
                            })
                    elif isinstance(item, dict):
                        detections.extend(
                            self.detect_in_dict(item, f"{current_path}[{i}]")
                        )

        return detections

    def sanitize(self, content: str) -> str:
        """
        Sanitize content by escaping template-related characters

        Args:
            content: String content to sanitize

        Returns:
            Sanitized content
        """
        if not content:
            return content

        result = content

        # Replace dangerous character sequences
        for dangerous, safe in DANGEROUS_CHARS.items():
            result = result.replace(dangerous, safe)

        # Additional HTML escaping for special characters
        result = html.escape(result)

        return result

    def sanitize_dict(
        self,
        data: Dict[str, Any],
        deep: bool = True
    ) -> Dict[str, Any]:
        """
        Recursively sanitize all string values in dictionary

        Args:
            data: Dictionary to sanitize
            deep: If True, recursively sanitize nested structures

        Returns:
            Sanitized dictionary
        """
        result = {}

        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.sanitize(value)
            elif deep and isinstance(value, dict):
                result[key] = self.sanitize_dict(value, deep=True)
            elif deep and isinstance(value, list):
                result[key] = [
                    self.sanitize(item) if isinstance(item, str)
                    else self.sanitize_dict(item, deep=True) if isinstance(item, dict)
                    else item
                    for item in value
                ]
            else:
                result[key] = value

        return result

    def get_safe_jinja2_env(self):
        """
        Get a safe Jinja2 environment with restricted features

        Returns:
            Jinja2 Environment with security restrictions
        """
        try:
            from jinja2 import Environment, select_autoescape
            from jinja2.sandbox import SandboxedEnvironment

            # Use sandboxed environment
            env = SandboxedEnvironment(
                autoescape=select_autoescape(['html', 'xml']),
            )

            # Remove dangerous globals
            env.globals.clear()

            # Add only safe globals
            env.globals['True'] = True
            env.globals['False'] = False
            env.globals['None'] = None

            return env

        except ImportError:
            logger.warning("Jinja2 not installed, returning None")
            return None


class SSTIMiddleware(BaseHTTPMiddleware):
    """
    SSTI Protection Middleware

    Intercepts requests and checks for SSTI payloads in:
    - Query parameters
    - Request body (JSON)
    - Form data
    - Headers
    """

    def __init__(
        self,
        app,
        enabled: bool = True,
        strict_mode: bool = True,
        exempt_paths: Optional[List[str]] = None,
        log_attempts: bool = True,
        notify_admin: bool = False
    ):
        """
        Initialize SSTI Middleware

        Args:
            app: FastAPI application
            enabled: Enable/disable middleware
            strict_mode: Block any template-like syntax
            exempt_paths: Paths exempt from SSTI checking
            log_attempts: Log blocked attempts
            notify_admin: Send notifications on detection
        """
        super().__init__(app)
        self.enabled = enabled
        self.protection = SSTIProtection(
            strict_mode=strict_mode,
            log_attempts=log_attempts
        )
        self.exempt_paths = exempt_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
        ]
        self.notify_admin = notify_admin

        # Track blocked attempts
        self.blocked_attempts: List[Dict[str, Any]] = []

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process request and check for SSTI payloads

        Args:
            request: Incoming request
            call_next: Next middleware

        Returns:
            Response
        """
        if not self.enabled:
            return await call_next(request)

        # Check exempt paths
        if any(request.url.path.startswith(p) for p in self.exempt_paths):
            return await call_next(request)

        try:
            # Check query parameters
            for key, value in request.query_params.items():
                is_detected, pattern, match = self.protection.detect_ssti(value)
                if is_detected:
                    return self._create_blocked_response(
                        request, "query_param", key, pattern, match
                    )

            # Check headers (selected ones)
            dangerous_headers = [
                "x-forwarded-for", "x-custom-header",
                "user-agent", "referer"
            ]
            for header in dangerous_headers:
                value = request.headers.get(header)
                if value:
                    is_detected, pattern, match = self.protection.detect_ssti(value)
                    if is_detected:
                        return self._create_blocked_response(
                            request, "header", header, pattern, match
                        )

            # Check request body for POST/PUT/PATCH
            if request.method in ["POST", "PUT", "PATCH"]:
                content_type = request.headers.get("content-type", "")

                if "application/json" in content_type:
                    try:
                        body = await request.body()
                        if body:
                            json_data = json.loads(body)
                            detections = self.protection.detect_in_dict(json_data)
                            if detections:
                                return self._create_blocked_response(
                                    request,
                                    "json_body",
                                    detections[0]["path"],
                                    detections[0]["pattern"],
                                    detections[0]["match"]
                                )
                    except json.JSONDecodeError:
                        pass  # Not valid JSON, skip

                elif "application/x-www-form-urlencoded" in content_type:
                    try:
                        form = await request.form()
                        for key, value in form.items():
                            if isinstance(value, str):
                                is_detected, pattern, match = self.protection.detect_ssti(value)
                                if is_detected:
                                    return self._create_blocked_response(
                                        request, "form_data", key, pattern, match
                                    )
                    except Exception:
                        pass

            # No SSTI detected, continue
            return await call_next(request)

        except Exception as e:
            logger.error(f"Error in SSTI middleware: {e}")
            return await call_next(request)

    def _create_blocked_response(
        self,
        request: Request,
        source: str,
        field: str,
        pattern: str,
        match: str
    ) -> JSONResponse:
        """
        Create blocked response and log the attempt

        Args:
            request: Original request
            source: Source of detection (query_param, header, etc.)
            field: Field name where SSTI was detected
            pattern: Pattern that matched
            match: Matched content

        Returns:
            JSONResponse with 400 status
        """
        client_ip = request.client.host if request.client else "unknown"

        attempt_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_ip": client_ip,
            "path": request.url.path,
            "method": request.method,
            "source": source,
            "field": field,
            "pattern": pattern,
            "match": match[:100],  # Truncate
        }

        self.blocked_attempts.append(attempt_info)

        logger.warning(
            f"SSTI attempt blocked - IP: {client_ip}, "
            f"Path: {request.url.path}, Source: {source}, Field: {field}"
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": "SSTI_DETECTED",
                "message": (
                    "Potentially malicious template injection detected. "
                    "This request has been blocked."
                ),
                "details": {
                    "source": source,
                    "field": field
                }
            }
        )

    def get_blocked_attempts(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get recent blocked attempts

        Args:
            limit: Maximum number of attempts to return

        Returns:
            List of blocked attempt records
        """
        return self.blocked_attempts[-limit:]


def create_safe_template_context(
    user_data: Dict[str, Any],
    allowed_keys: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Create a safe template context from user data

    Only includes whitelisted keys and sanitizes all values.

    Args:
        user_data: User-provided data
        allowed_keys: List of allowed keys (whitelist)

    Returns:
        Safe dictionary for template rendering
    """
    protection = SSTIProtection()

    if allowed_keys:
        # Only include allowed keys
        filtered_data = {
            k: v for k, v in user_data.items()
            if k in allowed_keys
        }
    else:
        filtered_data = user_data

    # Sanitize all values
    return protection.sanitize_dict(filtered_data)


def validate_template_string(
    template_str: str,
    allow_variables: bool = False
) -> Tuple[bool, Optional[str]]:
    """
    Validate a template string for safety

    Args:
        template_str: Template string to validate
        allow_variables: If True, allow simple variable substitution

    Returns:
        Tuple of (is_valid, error_message)
    """
    protection = SSTIProtection()

    # Check for SSTI patterns
    is_detected, pattern, match = protection.detect_ssti(template_str)

    if is_detected:
        return False, f"Dangerous pattern detected: {pattern}"

    # If variables not allowed, check for any template syntax
    if not allow_variables:
        if re.search(r'[\{\}\[\]\$\#\%]', template_str):
            return False, "Template syntax characters not allowed"

    return True, None


# Utility functions for common use cases

def sanitize_user_input(input_str: str) -> str:
    """
    Sanitize user input for safe template rendering

    Args:
        input_str: User input string

    Returns:
        Sanitized string
    """
    protection = SSTIProtection()
    return protection.sanitize(input_str)


def check_for_ssti(content: str) -> bool:
    """
    Quick check if content contains SSTI payload

    Args:
        content: Content to check

    Returns:
        True if SSTI detected, False otherwise
    """
    protection = SSTIProtection()
    is_detected, _, _ = protection.detect_ssti(content)
    return is_detected


__all__ = [
    "SSTIProtection",
    "SSTIMiddleware",
    "create_safe_template_context",
    "validate_template_string",
    "sanitize_user_input",
    "check_for_ssti",
    "SSTI_PATTERNS",
    "DANGEROUS_CHARS",
]
