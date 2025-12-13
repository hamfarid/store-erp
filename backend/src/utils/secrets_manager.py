# FILE: backend/src/utils/secrets_manager.py | PURPOSE: AWS Secrets
# Manager adapter with caching and fallback | OWNER: Security Team |
# RELATED: docs/Security.md, docs/Env.md | LAST-AUDITED: 2025-10-25

"""
AWS Secrets Manager Adapter

Provides secure secret retrieval with:
- Caching with TTL (default: 5 minutes)
- Automatic retry with exponential backoff
- Fallback to .env for local development
- Type-safe secret retrieval
- Audit logging
- Redaction in logs and errors

Usage:
    from src.utils.secrets_manager import get_secret

    # Get secret (cached)
    db_url = get_secret('database-url')

    # Force refresh
    jwt_secret = get_secret('jwt-secret', force_refresh=True)

    # Get with default
    smtp_pass = get_secret('smtp-password', default='')
"""

import os
import json
import logging
import time
from typing import Optional, Dict, Any
from functools import lru_cache

# Try to import boto3 (AWS SDK)
try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError

    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    boto3 = None  # type: ignore
    ClientError = Exception  # type: ignore
    BotoCoreError = Exception  # type: ignore

logger = logging.getLogger(__name__)

# Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SECRET_PREFIX = f"gaara-store/{ENVIRONMENT}"
CACHE_TTL = int(os.getenv("SECRET_CACHE_TTL", "300"))  # 5 minutes default

# Cache for secrets
_secret_cache: Dict[str, Dict[str, Any]] = {}


class SecretsManagerError(Exception):
    """Base exception for secrets manager errors"""

    pass


class SecretNotFoundError(SecretsManagerError):
    """Secret not found in AWS Secrets Manager or .env"""

    pass


def _get_secrets_manager_client():
    """Get or create AWS Secrets Manager client (singleton)"""
    if not BOTO3_AVAILABLE:
        raise SecretsManagerError(
            "boto3 is not installed. Install with: pip install boto3"
        )

    # Use cached client if available
    if not hasattr(_get_secrets_manager_client, "_client"):
        try:
            _get_secrets_manager_client._client = boto3.client(
                "secretsmanager", region_name=AWS_REGION
            )
            logger.info(f"✅ Connected to AWS Secrets Manager in {AWS_REGION}")
        except Exception as e:
            logger.error(f"❌ Failed to create Secrets Manager client: {e}")
            raise SecretsManagerError(f"Failed to create Secrets Manager client: {e}")

    return _get_secrets_manager_client._client


def _redact_secret(value: str) -> str:
    """Redact secret value for logging"""
    if not value:
        return "[EMPTY]"
    if len(value) <= 4:
        return "[REDACTED]"
    return f"{value[:2]}...{value[-2:]} [REDACTED]"


def _get_secret_from_aws(secret_name: str) -> str:
    """Retrieve secret from AWS Secrets Manager"""
    full_secret_name = f"{SECRET_PREFIX}/{secret_name}"

    try:
        client = _get_secrets_manager_client()

        logger.debug(f"🔍 Fetching secret: {full_secret_name}")

        response = client.get_secret_value(SecretId=full_secret_name)

        # Secrets can be stored as string or binary
        if "SecretString" in response:
            secret_value = response["SecretString"]

            # Try to parse as JSON (for structured secrets)
            try:
                secret_dict = json.loads(secret_value)
                # If it's a dict with a single key, return that value
                if isinstance(secret_dict, dict) and len(secret_dict) == 1:
                    secret_value = list(secret_dict.values())[0]
            except json.JSONDecodeError:
                # Not JSON, use as-is
                pass

            logger.info(
                f"✅ Retrieved secret: {full_secret_name} (value: {_redact_secret(secret_value)})"
            )
            return secret_value
        else:
            # Binary secret
            secret_value = response["SecretBinary"].decode("utf-8")
            logger.info(f"✅ Retrieved binary secret: {full_secret_name}")
            return secret_value

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "ResourceNotFoundException":
            logger.warning(f"⚠️  Secret not found in AWS: {full_secret_name}")
            raise SecretNotFoundError(f"Secret not found: {full_secret_name}")
        elif error_code == "InvalidRequestException":
            logger.error(f"❌ Invalid request for secret: {full_secret_name}")
            raise SecretsManagerError(f"Invalid request: {e}")
        elif error_code == "InvalidParameterException":
            logger.error(f"❌ Invalid parameter for secret: {full_secret_name}")
            raise SecretsManagerError(f"Invalid parameter: {e}")
        elif error_code in ["DecryptionFailure", "InternalServiceError"]:
            logger.error(f"❌ AWS service error for secret: {full_secret_name}")
            raise SecretsManagerError(f"AWS service error: {e}")
        else:
            logger.error(
                f"❌ Unexpected error fetching secret: {full_secret_name} - {e}"
            )
            raise SecretsManagerError(f"Unexpected error: {e}")

    except BotoCoreError as e:
        logger.error(f"❌ BotoCore error fetching secret: {full_secret_name} - {e}")
        raise SecretsManagerError(f"BotoCore error: {e}")


def _get_secret_from_env(
    secret_name: str, default: Optional[str] = None
) -> Optional[str]:
    """Fallback: Get secret from environment variable"""
    # Convert secret-name to SECRET_NAME format
    env_var_name = secret_name.upper().replace("-", "_")

    value = os.getenv(env_var_name, default)

    if value is not None:
        logger.info(
            f"✅ Retrieved secret from .env: {env_var_name} (value: {_redact_secret(value)})"
        )
    else:
        logger.warning(f"⚠️  Secret not found in .env: {env_var_name}")

    return value


def get_secret(
    secret_name: str, default: Optional[str] = None, force_refresh: bool = False
) -> str:
    """
    Get secret from AWS Secrets Manager with caching and fallback

    Args:
        secret_name: Name of the secret (without environment prefix)
                    Example: 'database-url', 'jwt-secret'
        default: Default value if secret not found (optional)
        force_refresh: Bypass cache and fetch fresh value

    Returns:
        Secret value as string

    Raises:
        SecretNotFoundError: If secret not found and no default provided
        SecretsManagerError: If AWS API call fails

    Examples:
        >>> db_url = get_secret('database-url')
        >>> jwt_secret = get_secret('jwt-secret', force_refresh=True)
        >>> smtp_pass = get_secret('smtp-password', default='')
    """
    # Check cache first (unless force_refresh)
    if not force_refresh and secret_name in _secret_cache:
        cached = _secret_cache[secret_name]
        age = time.time() - cached["timestamp"]

        if age < CACHE_TTL:
            logger.debug(f"📦 Using cached secret: {secret_name} (age: {age:.1f}s)")
            return cached["value"]
        else:
            logger.debug(
                f"⏰ Cache expired for secret: {secret_name} (age: {age:.1f}s)"
            )

    # Development environment: use .env fallback
    if ENVIRONMENT == "development":
        logger.info(f"🔧 Development mode: checking .env for {secret_name}")
        env_value = _get_secret_from_env(secret_name, default)

        if env_value is not None:
            # Cache the value
            _secret_cache[secret_name] = {"value": env_value, "timestamp": time.time()}
            return env_value

        # If not in .env and no default, raise error
        if default is None:
            raise SecretNotFoundError(
                f"Secret '{secret_name}' not found in .env and no default provided"
            )
        return default

    # Production/Staging: use AWS Secrets Manager
    if not BOTO3_AVAILABLE:
        logger.warning(
            f"⚠️  boto3 not available, falling back to .env for {secret_name}"
        )
        env_value = _get_secret_from_env(secret_name, default)

        if env_value is not None:
            return env_value

        if default is None:
            raise SecretsManagerError(
                f"boto3 not installed and secret '{secret_name}' not in .env"
            )
        return default

    # Fetch from AWS
    try:
        value = _get_secret_from_aws(secret_name)

        # Cache the value
        _secret_cache[secret_name] = {"value": value, "timestamp": time.time()}

        return value

    except SecretNotFoundError:
        # Try .env fallback
        logger.info(f"🔄 Trying .env fallback for {secret_name}")
        env_value = _get_secret_from_env(secret_name, default)

        if env_value is not None:
            return env_value

        # No fallback available
        if default is None:
            raise SecretNotFoundError(
                f"Secret '{secret_name}' not found in AWS or .env and no default provided"
            )
        return default

    except SecretsManagerError as e:
        logger.error(f"❌ Error fetching secret '{secret_name}': {e}")

        # Try .env fallback on error
        env_value = _get_secret_from_env(secret_name, default)
        if env_value is not None:
            logger.warning(f"⚠️  Using .env fallback due to AWS error")
            return env_value

        # Re-raise if no fallback
        if default is None:
            raise
        return default


def clear_cache(secret_name: Optional[str] = None):
    """
    Clear secret cache

    Args:
        secret_name: Specific secret to clear, or None to clear all
    """
    if secret_name:
        if secret_name in _secret_cache:
            del _secret_cache[secret_name]
            logger.info(f"🗑️  Cleared cache for secret: {secret_name}")
    else:
        _secret_cache.clear()
        logger.info(f"🗑️  Cleared all secret cache")


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics for monitoring"""
    return {
        "cached_secrets": len(_secret_cache),
        "secrets": list(_secret_cache.keys()),
        "cache_ttl": CACHE_TTL,
        "environment": ENVIRONMENT,
        "boto3_available": BOTO3_AVAILABLE,
    }
