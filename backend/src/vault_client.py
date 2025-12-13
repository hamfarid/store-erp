"""
Vault Client Module for Secret Management

This module provides a client for HashiCorp Vault to manage application secrets.
It supports:
- Secret retrieval with caching
- Secret rotation
- Multiple environments (development, production)
- Fallback to environment variables

Author: Store ERP Team
Date: 2025-11-06
Part of: T21 - KMS/Vault Integration
"""

import os
import logging
from functools import lru_cache
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

try:
    import hvac

    HVAC_AVAILABLE = True
except ImportError:
    HVAC_AVAILABLE = False
    logging.warning("hvac library not installed. Vault integration disabled.")


logger = logging.getLogger(__name__)


class VaultClient:
    """
    HashiCorp Vault client for secret management.

    Features:
    - Automatic authentication
    - Secret caching with TTL
    - Fallback to environment variables
    - Multiple environment support
    - Error handling and logging

    Usage:
        vault = VaultClient()
        secret = vault.get_secret('flask/secret_key')
        db_config = vault.get_secret('database')
    """

    def __init__(
        self,
        vault_url: Optional[str] = None,
        vault_token: Optional[str] = None,
        environment: Optional[str] = None,
        mount_point: str = "secret",
        cache_ttl: int = 300,  # 5 minutes
    ):
        """
        Initialize Vault client.

        Args:
            vault_url: Vault server URL (default: from VAULT_ADDR env)
            vault_token: Vault token (default: from VAULT_TOKEN env)
            environment: Environment name (default: from FLASK_ENV or 'development')
            mount_point: KV secrets engine mount point (default: 'secret')
            cache_ttl: Cache TTL in seconds (default: 300)
        """
        self.vault_url = vault_url or os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
        self.vault_token = vault_token or os.getenv("VAULT_TOKEN")
        self.environment = environment or os.getenv("FLASK_ENV", "development")
        self.mount_point = mount_point
        self.cache_ttl = cache_ttl

        self.client: Optional[hvac.Client] = None
        self.authenticated = False
        self._cache: Dict[str, tuple[Any, datetime]] = {}

        # Initialize client if hvac is available
        if HVAC_AVAILABLE:
            self._initialize_client()
        else:
            logger.warning("Vault client not initialized - hvac library not available")

    def _initialize_client(self) -> None:
        """Initialize and authenticate Vault client."""
        if not self.vault_token:
            logger.warning("VAULT_TOKEN not set - Vault integration disabled")
            return

        try:
            self.client = hvac.Client(url=self.vault_url, token=self.vault_token)

            # Verify authentication
            if self.client.is_authenticated():
                self.authenticated = True
                logger.info(
                    f"Vault client authenticated successfully (env: {self.environment})"
                )
            else:
                logger.error("Vault authentication failed - invalid token")
                self.client = None

        except Exception as e:
            logger.error(f"Failed to initialize Vault client: {e}")
            self.client = None

    def _get_secret_path(self, path: str) -> str:
        """
        Construct full secret path with environment.

        Args:
            path: Relative secret path (e.g., 'flask/secret_key')

        Returns:
            Full path (e.g., 'store-erp/development/flask/secret_key')
        """
        return f"store-erp/{self.environment}/{path}"

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached value is still valid."""
        if cache_key not in self._cache:
            return False

        _, cached_time = self._cache[cache_key]
        return datetime.now() - cached_time < timedelta(seconds=self.cache_ttl)

    @lru_cache(maxsize=128)
    def get_secret(
        self,
        path: str,
        field: Optional[str] = None,
        fallback_env: Optional[str] = None,
        use_cache: bool = True,
    ) -> Any:
        """
        Get secret from Vault with caching and fallback.

        Args:
            path: Secret path (e.g., 'flask/secret_key')
            field: Specific field to retrieve (optional)
            fallback_env: Environment variable to use as fallback
            use_cache: Whether to use cache (default: True)

        Returns:
            Secret value or None if not found

        Example:
            # Get entire secret
            flask_config = vault.get_secret('flask')

            # Get specific field
            secret_key = vault.get_secret('flask', field='secret_key')

            # With fallback
            secret_key = vault.get_secret(
                'flask',
                field='secret_key',
                fallback_env='SECRET_KEY'
            )
        """
        cache_key = f"{path}:{field}" if field else path

        # Check cache first
        if use_cache and self._is_cache_valid(cache_key):
            value, _ = self._cache[cache_key]
            logger.debug(f"Retrieved secret from cache: {cache_key}")
            return value

        # Try to get from Vault
        if self.authenticated and self.client:
            try:
                full_path = self._get_secret_path(path)
                response = self.client.secrets.kv.v2.read_secret_version(
                    path=full_path, mount_point=self.mount_point
                )

                data = response["data"]["data"]

                # Get specific field or entire secret
                value = data.get(field) if field else data

                # Cache the value
                if use_cache:
                    self._cache[cache_key] = (value, datetime.now())

                logger.info(f"Retrieved secret from Vault: {cache_key}")
                return value

            except hvac.exceptions.InvalidPath:
                logger.warning(f"Secret not found in Vault: {path}")
            except Exception as e:
                logger.error(f"Failed to retrieve secret from Vault: {e}")

        # Fallback to environment variable
        if fallback_env:
            value = os.getenv(fallback_env)
            if value:
                logger.info(f"Using fallback environment variable: {fallback_env}")
                return value

        logger.warning(f"Secret not found: {cache_key}")
        return None

    def set_secret(
        self, path: str, data: Dict[str, Any], cas: Optional[int] = None
    ) -> bool:
        """
        Set secret in Vault.

        Args:
            path: Secret path
            data: Secret data (dict)
            cas: Check-and-Set parameter for versioning

        Returns:
            True if successful, False otherwise

        Example:
            vault.set_secret('flask', {
                'secret_key': 'new-secret-key',
                'jwt_secret': 'new-jwt-secret'
            })
        """
        if not self.authenticated or not self.client:
            logger.error("Cannot set secret - Vault not authenticated")
            return False

        try:
            full_path = self._get_secret_path(path)
            self.client.secrets.kv.v2.create_or_update_secret(
                path=full_path, secret=data, cas=cas, mount_point=self.mount_point
            )

            # Invalidate cache
            self._invalidate_cache(path)

            logger.info(f"Secret updated in Vault: {path}")
            return True

        except Exception as e:
            logger.error(f"Failed to set secret in Vault: {e}")
            return False

    def rotate_secret(self, path: str, field: str, new_value: str) -> bool:
        """
        Rotate a specific secret field.

        Args:
            path: Secret path
            field: Field to rotate
            new_value: New secret value

        Returns:
            True if successful, False otherwise

        Example:
            vault.rotate_secret('flask', 'secret_key', 'new-secret-key')
        """
        # Get current secret
        current_secret = self.get_secret(path, use_cache=False)
        if not current_secret:
            logger.error(f"Cannot rotate - secret not found: {path}")
            return False

        # Update the field
        current_secret[field] = new_value

        # Save back to Vault
        return self.set_secret(path, current_secret)

    def _invalidate_cache(self, path: str) -> None:
        """Invalidate all cache entries for a given path."""
        keys_to_remove = [key for key in self._cache.keys() if key.startswith(path)]
        for key in keys_to_remove:
            del self._cache[key]

        # Also clear lru_cache
        self.get_secret.cache_clear()

        logger.debug(f"Cache invalidated for path: {path}")

    def clear_cache(self) -> None:
        """Clear all cached secrets."""
        self._cache.clear()
        self.get_secret.cache_clear()
        logger.info("All secret cache cleared")

    def health_check(self) -> Dict[str, Any]:
        """
        Check Vault health and authentication status.

        Returns:
            Health status dict
        """
        status = {
            "vault_available": HVAC_AVAILABLE,
            "vault_url": self.vault_url,
            "authenticated": self.authenticated,
            "environment": self.environment,
            "cache_size": len(self._cache),
        }

        if self.authenticated and self.client:
            try:
                health = self.client.sys.read_health_status()
                status["vault_initialized"] = health.get("initialized", False)
                status["vault_sealed"] = health.get("sealed", True)
            except Exception as e:
                status["error"] = str(e)

        return status


# Global Vault client instance
_vault_client: Optional[VaultClient] = None


def get_vault_client() -> VaultClient:
    """
    Get or create global Vault client instance.

    Returns:
        VaultClient instance
    """
    global _vault_client

    if _vault_client is None:
        _vault_client = VaultClient()

    return _vault_client


def get_secret(
    path: str, field: Optional[str] = None, fallback_env: Optional[str] = None
) -> Any:
    """
    Convenience function to get secret from global Vault client.

    Args:
        path: Secret path
        field: Specific field (optional)
        fallback_env: Fallback environment variable

    Returns:
        Secret value

    Example:
        from vault_client import get_secret

        secret_key = get_secret('flask', 'secret_key', 'SECRET_KEY')
    """
    client = get_vault_client()
    return client.get_secret(path, field, fallback_env)
