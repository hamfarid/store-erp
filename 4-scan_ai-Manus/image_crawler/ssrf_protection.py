"""
SSRF Protection Module
======================

Purpose: Protect against Server-Side Request Forgery (SSRF) attacks.
This module validates URLs before allowing the crawler to fetch them,
blocking access to internal networks and sensitive endpoints.

Security Features:
- Block localhost and loopback addresses
- Block private network ranges (RFC 1918)
- Block cloud metadata endpoints (AWS, GCP, Azure)
- Block link-local addresses
- Scheme validation (HTTP/HTTPS only)
- DNS resolution validation

Usage:
    from ssrf_protection import SSRFProtection, validate_url
    
    if validate_url("https://example.com/image.jpg"):
        # Safe to fetch
        response = requests.get(url)
    else:
        # Blocked - potential SSRF
        raise SecurityError("URL blocked by SSRF protection")

Author: Global System v35.0
Date: 2026-01-17
References:
    - OWASP SSRF Prevention Cheat Sheet
    - CWE-918: Server-Side Request Forgery
"""

import ipaddress
import logging
import socket
from typing import List, Optional, Set, Tuple
from urllib.parse import urlparse

# Configure logger
logger = logging.getLogger(__name__)


class SSRFConfig:
    """
    Configuration for SSRF protection rules.
    
    Attributes:
        ALLOWED_SCHEMES: Permitted URL schemes
        BLOCKED_HOSTS: Explicitly blocked hostnames
        BLOCKED_NETWORKS: IP ranges that are blocked
        BLOCKED_PORTS: Ports that should not be accessed
        ALLOW_PRIVATE_IPS: Whether to allow private IP ranges
    """
    
    # Only allow HTTP and HTTPS
    ALLOWED_SCHEMES: Set[str] = {'http', 'https'}
    
    # Standard ports for HTTP(S)
    ALLOWED_PORTS: Set[int] = {80, 443, 8080, 8443}
    
    # Explicitly blocked hostnames
    BLOCKED_HOSTS: Set[str] = {
        # Loopback
        'localhost',
        'localhost.localdomain',
        '127.0.0.1',
        '::1',
        '0.0.0.0',
        
        # Cloud metadata endpoints
        'metadata.google.internal',          # GCP
        'metadata.goog',                     # GCP
        'instance-data',                     # AWS
        '169.254.169.254',                   # AWS/GCP/Azure metadata
        '169.254.170.2',                     # AWS ECS metadata
        'fd00:ec2::254',                     # AWS IPv6 metadata
        
        # Kubernetes
        'kubernetes.default',
        'kubernetes.default.svc',
        'kubernetes.default.svc.cluster.local',
    }
    
    # Blocked IP networks (RFC 1918 + special ranges)
    BLOCKED_NETWORKS: List[ipaddress.IPv4Network | ipaddress.IPv6Network] = [
        # Loopback
        ipaddress.ip_network('127.0.0.0/8'),
        ipaddress.ip_network('::1/128'),
        
        # Private networks (RFC 1918)
        ipaddress.ip_network('10.0.0.0/8'),
        ipaddress.ip_network('172.16.0.0/12'),
        ipaddress.ip_network('192.168.0.0/16'),
        
        # Link-local
        ipaddress.ip_network('169.254.0.0/16'),
        ipaddress.ip_network('fe80::/10'),
        
        # Broadcast
        ipaddress.ip_network('255.255.255.255/32'),
        
        # Documentation ranges
        ipaddress.ip_network('192.0.2.0/24'),
        ipaddress.ip_network('198.51.100.0/24'),
        ipaddress.ip_network('203.0.113.0/24'),
        
        # CGNAT
        ipaddress.ip_network('100.64.0.0/10'),
        
        # Unique Local IPv6
        ipaddress.ip_network('fc00::/7'),
    ]


class SSRFProtection:
    """
    SSRF protection validator for URLs.
    
    This class provides comprehensive protection against SSRF attacks
    by validating URLs before they are fetched. It checks:
    
    1. URL scheme (must be HTTP or HTTPS)
    2. Hostname against blocklist
    3. Resolved IP address against blocked networks
    4. Port number against allowed list
    
    Example:
        >>> validator = SSRFProtection()
        >>> validator.is_safe("https://google.com/image.jpg")
        True
        >>> validator.is_safe("http://localhost/secret")
        False
        >>> validator.is_safe("http://169.254.169.254/metadata")
        False
    """
    
    def __init__(self, config: Optional[SSRFConfig] = None):
        """
        Initialize SSRF protection with optional custom config.
        
        Args:
            config: Custom SSRFConfig, or None for defaults
        """
        self.config = config or SSRFConfig()
        self._dns_cache: dict = {}
    
    def is_safe(self, url: str) -> bool:
        """
        Check if a URL is safe to fetch.
        
        This is the main validation method that combines all checks.
        
        Args:
            url: The URL to validate
            
        Returns:
            bool: True if URL is safe, False if blocked
            
        Example:
            >>> validator.is_safe("https://example.com/image.jpg")
            True
        """
        try:
            return self._validate_url(url)
        except Exception as e:
            logger.warning(f"URL validation error: {url} - {e}")
            return False
    
    def _validate_url(self, url: str) -> bool:
        """
        Perform comprehensive URL validation.
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if valid and safe
            
        Raises:
            ValueError: If URL is malformed
        """
        # Parse URL
        try:
            parsed = urlparse(url)
        except Exception as e:
            logger.warning(f"Failed to parse URL: {url} - {e}")
            return False
        
        # Validate scheme
        if not self._validate_scheme(parsed.scheme):
            logger.warning(f"Blocked scheme: {parsed.scheme} in {url}")
            return False
        
        # Validate hostname exists
        hostname = parsed.hostname
        if not hostname:
            logger.warning(f"No hostname in URL: {url}")
            return False
        
        # Check hostname blocklist
        if self._is_blocked_host(hostname):
            logger.warning(f"Blocked host: {hostname}")
            return False
        
        # Validate port
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        if not self._validate_port(port):
            logger.warning(f"Blocked port: {port} in {url}")
            return False
        
        # Resolve and check IP
        if not self._validate_resolved_ip(hostname):
            logger.warning(f"Blocked IP for host: {hostname}")
            return False
        
        return True
    
    def _validate_scheme(self, scheme: str) -> bool:
        """
        Validate URL scheme.
        
        Args:
            scheme: URL scheme (http, https, etc.)
            
        Returns:
            bool: True if scheme is allowed
        """
        return scheme.lower() in self.config.ALLOWED_SCHEMES
    
    def _validate_port(self, port: int) -> bool:
        """
        Validate port number.
        
        Args:
            port: Port number
            
        Returns:
            bool: True if port is allowed
        """
        return port in self.config.ALLOWED_PORTS
    
    def _is_blocked_host(self, hostname: str) -> bool:
        """
        Check if hostname is in blocklist.
        
        Args:
            hostname: Hostname to check
            
        Returns:
            bool: True if blocked
        """
        hostname_lower = hostname.lower()
        
        # Direct match
        if hostname_lower in self.config.BLOCKED_HOSTS:
            return True
        
        # Check for blocked patterns
        for blocked in self.config.BLOCKED_HOSTS:
            if hostname_lower.endswith('.' + blocked):
                return True
        
        return False
    
    def _validate_resolved_ip(self, hostname: str) -> bool:
        """
        Resolve hostname and validate IP address.
        
        This prevents DNS rebinding attacks by checking the
        resolved IP against blocked networks.
        
        Args:
            hostname: Hostname to resolve
            
        Returns:
            bool: True if resolved IP is safe
        """
        try:
            # Check cache first
            if hostname in self._dns_cache:
                ip_str = self._dns_cache[hostname]
            else:
                # Resolve hostname
                ip_str = socket.gethostbyname(hostname)
                self._dns_cache[hostname] = ip_str
            
            # Parse IP address
            ip_addr = ipaddress.ip_address(ip_str)
            
            # Check against blocked networks
            for network in self.config.BLOCKED_NETWORKS:
                if ip_addr in network:
                    logger.warning(
                        f"IP {ip_str} for {hostname} is in blocked network {network}"
                    )
                    return False
            
            return True
            
        except socket.gaierror as e:
            logger.warning(f"DNS resolution failed for {hostname}: {e}")
            return False
        except Exception as e:
            logger.warning(f"IP validation error for {hostname}: {e}")
            return False
    
    def get_validation_details(self, url: str) -> Tuple[bool, str]:
        """
        Get detailed validation result with reason.
        
        Args:
            url: URL to validate
            
        Returns:
            Tuple[bool, str]: (is_safe, reason)
            
        Example:
            >>> is_safe, reason = validator.get_validation_details(url)
            >>> if not is_safe:
            ...     print(f"URL blocked: {reason}")
        """
        try:
            parsed = urlparse(url)
            
            if not parsed.scheme:
                return False, "No scheme specified"
            
            if parsed.scheme.lower() not in self.config.ALLOWED_SCHEMES:
                return False, f"Blocked scheme: {parsed.scheme}"
            
            if not parsed.hostname:
                return False, "No hostname specified"
            
            if self._is_blocked_host(parsed.hostname):
                return False, f"Blocked hostname: {parsed.hostname}"
            
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            if port not in self.config.ALLOWED_PORTS:
                return False, f"Blocked port: {port}"
            
            if not self._validate_resolved_ip(parsed.hostname):
                return False, f"Blocked IP address for: {parsed.hostname}"
            
            return True, "URL is safe"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"


# Create default instance
_default_validator = SSRFProtection()


def validate_url(url: str) -> bool:
    """
    Convenience function to validate URL with default settings.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if URL is safe to fetch
        
    Example:
        >>> from ssrf_protection import validate_url
        >>> if validate_url(image_url):
        ...     download_image(image_url)
    """
    return _default_validator.is_safe(url)


def is_safe_url(url: str) -> bool:
    """
    Alias for validate_url for semantic clarity.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if URL is safe
    """
    return validate_url(url)


def get_url_validation_reason(url: str) -> Tuple[bool, str]:
    """
    Get validation result with detailed reason.
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple[bool, str]: (is_safe, reason)
    """
    return _default_validator.get_validation_details(url)
