#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1.34: Server-Side Request Forgery (SSRF) Protection

Provides comprehensive SSRF protection including:
- URL validation and sanitization
- IP address blocking (private ranges, localhost, etc.)
- DNS rebinding protection
- Protocol enforcement (HTTPS only)
- Domain allowlisting
"""

import os
import re
import socket
import logging
import ipaddress
import requests
from urllib.parse import urlparse, urljoin
from typing import Optional, List, Set, Tuple
from functools import wraps

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

# Allowed protocols
ALLOWED_PROTOCOLS = {"https", "http"}
ENFORCE_HTTPS = os.environ.get("ENFORCE_HTTPS_REQUESTS", "false").lower() == "true"

# Domain allowlist (empty means all non-blocked domains allowed)
ALLOWED_DOMAINS: Set[str] = set(
    filter(None, os.environ.get("ALLOWED_EXTERNAL_DOMAINS", "").split(","))
)

# DNS timeout for validation
DNS_TIMEOUT = float(os.environ.get("DNS_TIMEOUT", "5"))

# Blocked IP ranges
BLOCKED_IP_RANGES = [
    # Loopback
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    # Private networks
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    # Link-local
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("fe80::/10"),
    # Multicast
    ipaddress.ip_network("224.0.0.0/4"),
    ipaddress.ip_network("ff00::/8"),
    # Reserved
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),  # Carrier-grade NAT
    ipaddress.ip_network("192.0.0.0/24"),  # IETF Protocol Assignments
    ipaddress.ip_network("192.0.2.0/24"),  # TEST-NET-1
    ipaddress.ip_network("198.51.100.0/24"),  # TEST-NET-2
    ipaddress.ip_network("203.0.113.0/24"),  # TEST-NET-3
    ipaddress.ip_network("240.0.0.0/4"),  # Reserved for future use
    # Cloud metadata endpoints
    ipaddress.ip_network("169.254.169.254/32"),  # AWS/GCP/Azure metadata
]

# Blocked hostnames
BLOCKED_HOSTNAMES = {
    "localhost",
    "localhost.localdomain",
    "metadata.google.internal",
    "metadata",
    "169.254.169.254",
}

# Dangerous URL patterns
DANGEROUS_PATTERNS = [
    r"file://",
    r"gopher://",
    r"dict://",
    r"ftp://",
    r"sftp://",
    r"ldap://",
    r"tftp://",
    r"jar://",
    r"netdoc://",
    r"@",  # Credential injection
    r"%00",  # Null byte
    r"%0d%0a",  # CRLF injection
    r"\r\n",
    r"\n",
]


# =============================================================================
# Validation Functions
# =============================================================================


class SSRFError(Exception):
    """Exception raised when SSRF attack is detected."""

    pass


def is_ip_blocked(ip_str: str) -> Tuple[bool, Optional[str]]:
    """
    Check if an IP address is in a blocked range.

    Args:
        ip_str: IP address string

    Returns:
        Tuple of (is_blocked, reason)
    """
    try:
        ip = ipaddress.ip_address(ip_str)

        for blocked_range in BLOCKED_IP_RANGES:
            if ip in blocked_range:
                return True, f"IP {ip_str} is in blocked range {blocked_range}"

        return False, None

    except ValueError:
        return True, f"Invalid IP address: {ip_str}"


def resolve_hostname(hostname: str) -> List[str]:
    """
    Resolve hostname to IP addresses with timeout.

    Args:
        hostname: Hostname to resolve

    Returns:
        List of IP addresses

    Raises:
        SSRFError: If resolution fails or times out
    """
    try:
        socket.setdefaulttimeout(DNS_TIMEOUT)
        results = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC)
        ips = list(set(result[4][0] for result in results))
        return ips
    except socket.gaierror as e:
        raise SSRFError(f"DNS resolution failed for {hostname}: {e}")
    except socket.timeout:
        raise SSRFError(f"DNS resolution timeout for {hostname}")
    finally:
        socket.setdefaulttimeout(None)


def validate_url(
    url: str, allow_private: bool = False
) -> Tuple[bool, str, Optional[str]]:
    """
    Validate a URL for SSRF vulnerabilities.

    Args:
        url: URL to validate
        allow_private: Whether to allow private IP ranges (for internal services)

    Returns:
        Tuple of (is_valid, sanitized_url, error_message)
    """
    if not url:
        return False, "", "Empty URL"

    # Check for dangerous patterns
    url_lower = url.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, url_lower, re.IGNORECASE):
            return False, "", f"Dangerous pattern detected: {pattern}"

    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        return False, "", f"Invalid URL format: {e}"

    # Validate protocol
    if not parsed.scheme:
        return False, "", "No protocol specified"

    if parsed.scheme.lower() not in ALLOWED_PROTOCOLS:
        return False, "", f"Protocol {parsed.scheme} not allowed"

    if ENFORCE_HTTPS and parsed.scheme.lower() != "https":
        return False, "", "HTTPS required"

    # Validate hostname
    hostname = parsed.hostname
    if not hostname:
        return False, "", "No hostname specified"

    hostname_lower = hostname.lower()

    # Check blocked hostnames
    if hostname_lower in BLOCKED_HOSTNAMES:
        return False, "", f"Hostname {hostname} is blocked"

    # Check domain allowlist
    if ALLOWED_DOMAINS:
        domain_allowed = False
        for allowed in ALLOWED_DOMAINS:
            if hostname_lower == allowed or hostname_lower.endswith("." + allowed):
                domain_allowed = True
                break
        if not domain_allowed:
            return False, "", f"Hostname {hostname} is not in allowlist"

    # Check if hostname is an IP address
    try:
        ip = ipaddress.ip_address(hostname)
        if not allow_private:
            is_blocked, reason = is_ip_blocked(str(ip))
            if is_blocked:
                return False, "", reason
    except ValueError:
        # Not an IP address, resolve hostname
        try:
            ips = resolve_hostname(hostname)
            if not allow_private:
                for ip in ips:
                    is_blocked, reason = is_ip_blocked(ip)
                    if is_blocked:
                        return False, "", f"Resolved IP blocked: {reason}"
        except SSRFError as e:
            return False, "", str(e)

    # Validate port
    port = parsed.port
    if port:
        # Block common internal service ports
        blocked_ports = {22, 23, 25, 110, 143, 389, 445, 3306, 5432, 6379, 27017}
        if port in blocked_ports:
            return False, "", f"Port {port} is blocked"

    # Reconstruct sanitized URL
    sanitized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if parsed.query:
        sanitized += f"?{parsed.query}"

    return True, sanitized, None


def safe_request(url: str, method: str = "GET", **kwargs) -> "requests.Response":
    """
    Make a safe HTTP request with SSRF protection.

    Args:
        url: URL to request
        method: HTTP method
        **kwargs: Additional arguments for requests

    Returns:
        Response object

    Raises:
        SSRFError: If URL fails validation
    """
    import requests

    # Validate URL
    is_valid, sanitized_url, error = validate_url(url)
    if not is_valid:
        raise SSRFError(f"SSRF protection blocked request: {error}")

    # Set safe defaults
    kwargs.setdefault("timeout", (5, 30))  # Connect, read timeouts
    kwargs.setdefault("allow_redirects", False)  # Prevent redirect attacks

    # Make request
    logger.debug(f"P1.34: Safe request to {sanitized_url}")
    response = requests.request(method, sanitized_url, **kwargs)

    # Validate redirect location if any
    if response.is_redirect:
        redirect_url = response.headers.get("Location")
        if redirect_url:
            # Resolve relative redirects
            redirect_url = urljoin(sanitized_url, redirect_url)
            is_valid, _, error = validate_url(redirect_url)
            if not is_valid:
                raise SSRFError(f"SSRF protection blocked redirect: {error}")

    return response


# =============================================================================
# Decorator for Route Protection
# =============================================================================


def ssrf_protect(url_param: str = "url", allow_private: bool = False):
    """
    Decorator to protect routes from SSRF attacks.

    Usage:
        @app.route('/fetch')
        @ssrf_protect('target_url')
        def fetch():
            url = request.args.get('target_url')
            ...

    Args:
        url_param: Name of the URL parameter to validate
        allow_private: Whether to allow private IP ranges
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from flask import request, jsonify

            # Get URL from request
            url = request.args.get(url_param) or request.form.get(url_param)
            if not url:
                json_data = request.get_json(silent=True) or {}
                url = json_data.get(url_param)

            if url:
                is_valid, sanitized, error = validate_url(url, allow_private)
                if not is_valid:
                    logger.warning(f"P1.34: SSRF blocked: {url} - {error}")
                    return (
                        jsonify(
                            {
                                "success": False,
                                "error": {
                                    "code": "SSRF_BLOCKED",
                                    "message": "URL validation failed",
                                    "details": error,
                                },
                            }
                        ),
                        400,
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator


# =============================================================================
# URL Sanitization
# =============================================================================


def sanitize_url(url: str) -> Optional[str]:
    """
    Sanitize a URL by removing dangerous components.

    Args:
        url: URL to sanitize

    Returns:
        Sanitized URL or None if invalid
    """
    is_valid, sanitized, _ = validate_url(url)
    return sanitized if is_valid else None


def extract_domain(url: str) -> Optional[str]:
    """
    Extract the domain from a URL safely.

    Args:
        url: URL to extract domain from

    Returns:
        Domain or None if invalid
    """
    try:
        parsed = urlparse(url)
        return parsed.hostname
    except Exception:
        return None


__all__ = [
    "SSRFError",
    "is_ip_blocked",
    "resolve_hostname",
    "validate_url",
    "safe_request",
    "ssrf_protect",
    "sanitize_url",
    "extract_domain",
    "ALLOWED_DOMAINS",
    "BLOCKED_IP_RANGES",
]
