# FILE: backend/src/config/secrets_loader.py | PURPOSE: Load secrets from
# AWS Secrets Manager or .env | OWNER: DevOps | RELATED: app.py, .env |
# LAST-AUDITED: 2025-10-27

"""
Secrets Loader

Handles loading secrets from either AWS Secrets Manager (production)
or .env files (development/testing).
"""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class SecretsLoader:
    """
    Unified secrets loader for development and production
    """

    def __init__(self):
        """Initialize SecretsLoader"""
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.use_aws = self.environment == "production"

        if self.use_aws:
            try:
                from src.services.secrets_adapter import get_secrets_adapter

                self.adapter = get_secrets_adapter(
                    region=os.getenv("AWS_REGION", "us-east-1")
                )
                logger.info("Using AWS Secrets Manager for secrets")
            except Exception as e:
                logger.warning(f"Failed to initialize AWS Secrets Manager: {e}")
                logger.warning("Falling back to .env file")
                self.use_aws = False
        else:
            logger.info("Using .env file for secrets (development mode)")

    def get_secret(self, secret_name: str, key: Optional[str] = None) -> str:
        """
        Get a secret value

        Args:
            secret_name: Name of the secret
            key: Optional key within the secret

        Returns:
            Secret value as string
        """
        if self.use_aws:
            try:
                return self.adapter.get_secret_value(secret_name, key)
            except Exception as e:
                logger.error(f"Failed to get secret {secret_name} from AWS: {e}")
                # Fallback to .env
                return self._get_from_env(secret_name, key)
        else:
            return self._get_from_env(secret_name, key)

    def _get_from_env(self, secret_name: str, key: Optional[str] = None) -> str:
        """
        Get secret from .env file

        Args:
            secret_name: Name of the secret
            key: Optional key within the secret

        Returns:
            Secret value from environment
        """
        # Convert secret_name to environment variable format
        # e.g., 'gaara/prod/database' -> 'GAARA_PROD_DATABASE'
        env_var = secret_name.upper().replace("/", "_")

        if key:
            # For nested secrets, append the key
            env_var = f"{env_var}_{key.upper()}"

        value = os.getenv(env_var, "")

        if not value:
            logger.warning(f"Secret {secret_name} not found in environment")

        return value

    def load_app_config(self) -> Dict[str, Any]:
        """
        Load all application configuration from secrets

        Returns:
            Dictionary with application configuration
        """
        config = {
            "SQLALCHEMY_DATABASE_URI": self.get_secret("gaara/database-url"),
            "JWT_SECRET_KEY": self.get_secret("gaara/jwt-secret"),
            "JWT_REFRESH_SECRET_KEY": self.get_secret("gaara/jwt-refresh-secret"),
            "ENCRYPTION_KEY": self.get_secret("gaara/encryption-key"),
            "SENDGRID_API_KEY": self.get_secret("gaara/sendgrid-api-key"),
            "STRIPE_API_KEY": self.get_secret("gaara/stripe-api-key"),
        }

        # Optional secrets
        optional_secrets = [
            "OAUTH_CLIENT_ID",
            "OAUTH_CLIENT_SECRET",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
        ]

        for secret in optional_secrets:
            value = self.get_secret(f"gaara/{secret.lower()}")
            if value:
                config[secret] = value

        return config


# Singleton instance
_loader: Optional[SecretsLoader] = None


def get_secrets_loader() -> SecretsLoader:
    """
    Get or create SecretsLoader singleton

    Returns:
        SecretsLoader instance
    """
    global _loader

    if _loader is None:
        _loader = SecretsLoader()

    return _loader


def load_secrets_to_app(app) -> None:
    """
    Load secrets into Flask app configuration

    Args:
        app: Flask application instance
    """
    loader = get_secrets_loader()
    config = loader.load_app_config()

    for key, value in config.items():
        if value:
            app.config[key] = value
            logger.debug(f"Loaded secret {key}")
        else:
            logger.warning(f"Secret {key} is empty")
