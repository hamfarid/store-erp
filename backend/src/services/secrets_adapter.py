# FILE: backend/src/services/secrets_adapter.py | PURPOSE: AWS Secrets
# Manager adapter for secure secrets retrieval | OWNER: DevOps | RELATED:
# app.py, .env | LAST-AUDITED: 2025-10-27

"""
AWS Secrets Manager Adapter

Provides a unified interface for retrieving secrets from AWS Secrets Manager
with caching, error handling, and audit logging.
"""

import boto3
import json
import logging
from typing import Dict, Any, Optional
from functools import lru_cache
from datetime import datetime

logger = logging.getLogger(__name__)


class SecretsAdapter:
    """
    Adapter for AWS Secrets Manager

    Handles:
    - Secret retrieval with caching
    - Error handling and logging
    - Secret rotation
    - Audit trail
    """

    def __init__(self, region: str = "us-east-1", cache_ttl: int = 3600):
        """
        Initialize SecretsAdapter

        Args:
            region: AWS region (default: us-east-1)
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.region = region
        self.cache_ttl = cache_ttl
        self.cache: Dict[str, Dict[str, Any]] = {}

        try:
            self.client = boto3.client("secretsmanager", region_name=region)
            logger.info(f"SecretsAdapter initialized for region {region}")
        except Exception as e:
            logger.error(f"Failed to initialize SecretsAdapter: {str(e)}")
            raise RuntimeError(
                f"Failed to initialize AWS Secrets Manager client: {str(e)}"
            )

    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """
        Retrieve secret from AWS Secrets Manager

        Args:
            secret_name: Name of the secret (e.g., 'gaara/prod/database')

        Returns:
            Dictionary containing secret data

        Raises:
            RuntimeError: If secret retrieval fails
        """
        # Check cache first
        if secret_name in self.cache:
            cached_data = self.cache[secret_name]
            if self._is_cache_valid(cached_data):
                logger.debug(f"Retrieved secret {secret_name} from cache")
                return cached_data["value"]

        try:
            logger.info(f"Retrieving secret {secret_name} from AWS Secrets Manager")
            response = self.client.get_secret_value(SecretId=secret_name)

            # Parse secret value
            if "SecretString" in response:
                secret_value = json.loads(response["SecretString"])
            else:
                secret_value = {"value": response["SecretBinary"]}

            # Cache the secret
            self.cache[secret_name] = {
                "value": secret_value,
                "timestamp": datetime.now().timestamp(),
            }

            logger.info(f"Successfully retrieved secret {secret_name}")
            return secret_value

        except self.client.exceptions.ResourceNotFoundException:
            logger.error(f"Secret {secret_name} not found in AWS Secrets Manager")
            raise RuntimeError(f"Secret {secret_name} not found")
        except Exception as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {str(e)}")
            raise RuntimeError(f"Failed to retrieve secret {secret_name}: {str(e)}")

    def get_secret_value(self, secret_name: str, key: Optional[str] = None) -> str:
        """
        Get a specific secret value

        Args:
            secret_name: Name of the secret
            key: Optional key within the secret (for JSON secrets)

        Returns:
            Secret value as string
        """
        secret = self.get_secret(secret_name)

        if key:
            value = secret.get(key, "")
        else:
            value = secret.get("value", "")

        if not value:
            logger.warning(f"Secret value not found for {secret_name}:{key}")

        return str(value)

    def rotate_secret(self, secret_name: str) -> bool:
        """
        Trigger secret rotation

        Args:
            secret_name: Name of the secret to rotate

        Returns:
            True if rotation was triggered successfully
        """
        try:
            logger.info(f"Triggering rotation for secret {secret_name}")
            self.client.rotate_secret(SecretId=secret_name)

            # Clear cache for this secret
            self.cache.pop(secret_name, None)

            logger.info(f"Successfully triggered rotation for {secret_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to rotate secret {secret_name}: {str(e)}")
            raise RuntimeError(f"Failed to rotate secret {secret_name}: {str(e)}")

    def clear_cache(self, secret_name: Optional[str] = None) -> None:
        """
        Clear cache for a specific secret or all secrets

        Args:
            secret_name: Optional secret name to clear. If None, clears all.
        """
        if secret_name:
            self.cache.pop(secret_name, None)
            logger.debug(f"Cleared cache for secret {secret_name}")
        else:
            self.cache.clear()
            logger.debug("Cleared all cached secrets")

    def _is_cache_valid(self, cached_data: Dict[str, Any]) -> bool:
        """
        Check if cached data is still valid

        Args:
            cached_data: Cached data with timestamp

        Returns:
            True if cache is still valid
        """
        current_time = datetime.now().timestamp()
        cache_time = cached_data.get("timestamp", 0)
        return (current_time - cache_time) < self.cache_ttl


class VaultAdapter:
    """
    Adapter for HashiCorp Vault (future implementation)

    Provides similar interface to SecretsAdapter but uses Vault API
    """

    def __init__(self, vault_addr: str, vault_token: str):
        """
        Initialize VaultAdapter

        Args:
            vault_addr: Vault server address
            vault_token: Vault authentication token
        """
        self.vault_addr = vault_addr
        self.vault_token = vault_token
        logger.info(f"VaultAdapter initialized for {vault_addr}")

    def get_secret(self, secret_path: str) -> Dict[str, Any]:
        """
        Retrieve secret from Vault

        Args:
            secret_path: Path to secret in Vault

        Returns:
            Dictionary containing secret data
        """
        # TODO: Implement Vault API integration
        raise NotImplementedError("Vault integration not yet implemented")


# Singleton instance
_secrets_adapter: Optional[SecretsAdapter] = None


def get_secrets_adapter(region: str = "us-east-1") -> SecretsAdapter:
    """
    Get or create SecretsAdapter singleton

    Args:
        region: AWS region

    Returns:
        SecretsAdapter instance
    """
    global _secrets_adapter

    if _secrets_adapter is None:
        _secrets_adapter = SecretsAdapter(region=region)

    return _secrets_adapter
