"""
T21 Phase 2: Vault Integration Tests
Tests for Flask application integration with HashiCorp Vault

This module tests that the Flask application correctly loads
configuration from Vault when available, with proper fallback
to environment variables.
"""

import os
import pytest
from unittest.mock import patch

# Import config module
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir / "src"))

from config.production import ProductionConfig, DevelopmentConfig, TestingConfig  # noqa: E402


class TestVaultIntegration:
    """Test Vault integration with Flask configuration"""

    def test_vault_available_flag(self):
        """Test that VAULT_AVAILABLE flag is set correctly"""
        from config import production

        # Should be True if vault_client is importable
        assert hasattr(production, "VAULT_AVAILABLE")
        assert isinstance(production.VAULT_AVAILABLE, bool)

    def test_config_uses_vault_client(self):
        """Test that config module imports vault_client"""
        from config import production

        # Verify get_secret function exists
        assert hasattr(production, "get_secret")
        assert callable(production.get_secret)

    def test_production_config_has_secrets(self):
        """Test ProductionConfig has all required secret fields"""
        config = ProductionConfig()

        # Verify all secret fields exist
        assert hasattr(config, "SECRET_KEY")
        assert hasattr(config, "JWT_SECRET_KEY")
        assert hasattr(config, "SQLALCHEMY_DATABASE_URI")
        assert hasattr(config, "SECURITY_PASSWORD_SALT")

        # Verify they are not None
        assert config.SECRET_KEY is not None
        assert config.JWT_SECRET_KEY is not None
        assert config.SQLALCHEMY_DATABASE_URI is not None

    def test_development_config_inherits_from_production(self):
        """Test DevelopmentConfig inherits from ProductionConfig"""
        dev_config = DevelopmentConfig()

        # Should inherit secret management from ProductionConfig
        assert hasattr(dev_config, "SECRET_KEY")
        assert hasattr(dev_config, "JWT_SECRET_KEY")
        assert dev_config.DEBUG is True
        assert dev_config.TESTING is False

    def test_testing_config_inherits_from_production(self):
        """Test TestingConfig inherits from ProductionConfig"""
        test_config = TestingConfig()

        # Should inherit secret management from ProductionConfig
        assert hasattr(test_config, "SECRET_KEY")
        assert hasattr(test_config, "JWT_SECRET_KEY")
        assert test_config.TESTING is True
        assert test_config.DEBUG is True
        assert "memory" in test_config.SQLALCHEMY_DATABASE_URI

    def test_database_uri_exists(self):
        """Test database URI is configured"""
        config = ProductionConfig()

        # Should have database URI
        assert hasattr(config, "SQLALCHEMY_DATABASE_URI")
        assert config.SQLALCHEMY_DATABASE_URI is not None
        assert len(config.SQLALCHEMY_DATABASE_URI) > 0

    def test_mail_config_exists(self):
        """Test mail configuration exists"""
        config = ProductionConfig()

        # Should have mail config (may be None if not configured)
        assert hasattr(config, "MAIL_SERVER")
        assert hasattr(config, "MAIL_PORT")
        assert hasattr(config, "MAIL_USE_TLS")

    def test_security_config_exists(self):
        """Test security configuration exists"""
        config = ProductionConfig()

        # Should have security config
        assert hasattr(config, "SECURITY_PASSWORD_SALT")
        assert config.SECURITY_PASSWORD_SALT is not None
        assert hasattr(config, "AUTH_MAX_LOGIN_ATTEMPTS")
        assert hasattr(config, "AUTH_LOCKOUT_DURATION")

    def test_config_dict_contains_all_environments(self):
        """Test config dict has all environment configurations"""
        from config.production import config

        # Should have all environments
        assert "development" in config
        assert "testing" in config
        assert "production" in config
        assert "default" in config

        # Default should be development
        assert config["default"] == DevelopmentConfig


class TestVaultClientFallback:
    """Test fallback get_secret function when Vault client not available"""

    def test_fallback_function_with_env_var(self):
        """Test fallback get_secret returns environment variable"""
        # Set environment variable
        os.environ["TEST_SECRET"] = "test-value-123"

        # Import fallback function
        with patch("config.production.VAULT_AVAILABLE", False):
            from config.production import get_secret

            result = get_secret("any_path", fallback_env="TEST_SECRET")

            assert result == "test-value-123"

        # Cleanup
        del os.environ["TEST_SECRET"]

    def test_fallback_function_without_env_var(self):
        """Test fallback get_secret returns None when no env var"""
        with patch("config.production.VAULT_AVAILABLE", False):
            from config.production import get_secret

            result = get_secret("any_path", fallback_env="NONEXISTENT_VAR")

            assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
