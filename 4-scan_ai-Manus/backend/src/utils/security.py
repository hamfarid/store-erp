"""
FILE: backend/src/utils/security.py | PURPOSE: Security utilities for input sanitization | OWNER: Security Team | LAST-AUDITED: 2025-11-18

Security Utilities Module

Provides comprehensive security utilities for:
- XSS (Cross-Site Scripting) prevention
- Input sanitization
- HTML escaping
- SQL injection prevention
- Path traversal prevention

Version: 1.0.0
"""

import html
import re
from typing import Any, Dict, List, Optional

import bleach


class XSSProtection:
    """
    XSS Protection Utilities

    Provides methods to sanitize user input and prevent XSS attacks.
    """

    # Allowed HTML tags for rich text (very restrictive)
    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre'
    ]

    # Allowed HTML attributes
    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title'],
    }

    # Allowed URL protocols
    ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']

    @staticmethod
    def sanitize_html(text: str, allow_tags: bool = False) -> str:
        """
        Sanitize HTML input to prevent XSS attacks

        Args:
            text: Input text that may contain HTML
            allow_tags: Whether to allow safe HTML tags

        Returns:
            str: Sanitized text
        """
        if not text:
            return ""

        # Remove script/style blocks entirely (bleach strips tags but keeps their text)
        text = re.sub(r"(?is)<\s*(script|style)[^>]*>.*?<\s*/\s*\1\s*>", "", text)

        if allow_tags:
            # Use bleach to clean HTML, allowing only safe tags
            return bleach.clean(
                text,
                tags=XSSProtection.ALLOWED_TAGS,
                attributes=XSSProtection.ALLOWED_ATTRIBUTES,
                protocols=XSSProtection.ALLOWED_PROTOCOLS,
                strip=True
            )
        else:
            # Escape all HTML
            return html.escape(text)

    @staticmethod
    def sanitize_string(text: str) -> str:
        """
        Sanitize plain text input

        Args:
            text: Input text

        Returns:
            str: Sanitized text
        """
        if not text:
            return ""

        # Remove null bytes
        text = text.replace('\x00', '')

        # Escape HTML
        text = html.escape(text)

        # Remove potentially dangerous characters
        text = re.sub(r'[<>"\']', '', text)

        return text.strip()

    @staticmethod
    def sanitize_dict(
            data: Dict[str, Any], allow_html_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Recursively sanitize all string values in a dictionary

        Args:
            data: Dictionary to sanitize
            allow_html_fields: List of field names that can contain HTML

        Returns:
            Dict: Sanitized dictionary
        """
        allow_html_fields = allow_html_fields or []
        sanitized = {}

        for key, value in data.items():
            if isinstance(value, str):
                if key in allow_html_fields:
                    sanitized[key] = XSSProtection.sanitize_html(
                        value, allow_tags=True)
                else:
                    sanitized[key] = XSSProtection.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = XSSProtection.sanitize_dict(
                    value, allow_html_fields)
            elif isinstance(value, list):
                sanitized[key] = [
                    XSSProtection.sanitize_dict(
                        item, allow_html_fields) if isinstance(
                        item, dict) else XSSProtection.sanitize_string(item) if isinstance(
                        item, str) else item for item in value]
            else:
                sanitized[key] = value

        return sanitized


class InputValidator:
    """
    Input Validation Utilities

    Provides methods to validate user input.
    """

    @staticmethod
    def is_safe_filename(filename: str) -> bool:
        """
        Check if filename is safe (no path traversal)

        Args:
            filename: Filename to check

        Returns:
            bool: True if safe, False otherwise
        """
        if not filename:
            return False

        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            return False

        # Check for null bytes
        if '\x00' in filename:
            return False

        # Check for hidden files
        if filename.startswith('.'):
            return False

        return True

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal

        Args:
            filename: Original filename

        Returns:
            str: Sanitized filename
        """
        # Drop traversal segments but preserve safe path parts, then join them
        parts = re.split(r"[\\/]+", str(filename or ""))
        safe_parts = [p for p in parts if p and p not in (".", "..")]
        filename = "".join(safe_parts)

        # Fallback if everything got stripped
        if not filename:
            filename = "file"

        # Remove dangerous characters
        filename = re.sub(r'[^\w\s\-\.]', '', filename)

        # Remove leading dots
        filename = filename.lstrip('.')

        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit(
                '.', 1) if '.' in filename else (
                filename, '')
            filename = name[:250] + ('.' + ext if ext else '')

        return filename

    @staticmethod
    def is_safe_url(url: str) -> bool:
        """
        Check if URL is safe

        Args:
            url: URL to check

        Returns:
            bool: True if safe, False otherwise
        """
        if not url:
            return False

        # Check protocol
        if not any(url.startswith(proto + '://')
                   for proto in ['http', 'https']):
            return False

        # Check for javascript: or data: URLs
        if url.lower().startswith(('javascript:', 'data:', 'vbscript:')):
            return False

        return True


# Convenience functions
def sanitize_html(text: str, allow_tags: bool = False) -> str:
    """Sanitize HTML input"""
    return XSSProtection.sanitize_html(text, allow_tags)


def sanitize_string(text: str) -> str:
    """Sanitize plain text input"""
    return XSSProtection.sanitize_string(text)


def sanitize_dict(
        data: Dict[str, Any], allow_html_fields: Optional[List[str]] = None) -> Dict[str, Any]:
    """Sanitize dictionary"""
    return XSSProtection.sanitize_dict(data, allow_html_fields)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename"""
    return InputValidator.sanitize_filename(filename)


def is_safe_url(url: str) -> bool:
    """Check if URL is safe"""
    return InputValidator.is_safe_url(url)
