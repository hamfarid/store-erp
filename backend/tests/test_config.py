# -*- coding: utf-8 -*-
"""
Unit Tests for Configuration Module
اختبارات الوحدة لوحدة الإعدادات

Tests for:
- Production config validation
- Secret key requirements
- JWT secret key requirements
- Database configuration
- Session configuration

Target: >= 80% coverage
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import timedelta


class TestProductionConfig:
    """Test ProductionConfig class"""

    def test_production_config_with_valid_secrets(self):
        """Test production config loads with valid environment variables"""
        # Set environment variables
        test_secret = "a" * 64  # 64 character secret (32 bytes hex)
        test_jwt_secret = "b" * 64

        with patch.dict(
            os.environ,
            {
                "SECRET_KEY": test_secret,
                "JWT_SECRET_KEY": test_jwt_secret,
                "DATABASE_URL": "postgresql://user:pass@localhost/testdb",
            },
        ):
            # Import config (will validate secrets)
            from src.config.production import ProductionConfig

            # Verify config loaded
            assert ProductionConfig.SECRET_KEY == test_secret
            assert ProductionConfig.JWT_SECRET_KEY == test_jwt_secret
            assert (
                ProductionConfig.SQLALCHEMY_DATABASE_URI
                == "postgresql://user:pass@localhost/testdb"
            )

    def test_production_config_database_defaults(self):
        """Test database configuration defaults"""
        test_secret = "a" * 64
        test_jwt_secret = "b" * 64

        with patch.dict(
            os.environ,
            {"SECRET_KEY": test_secret, "JWT_SECRET_KEY": test_jwt_secret},
            clear=True,
        ):
            # Reload module to get fresh config
            import importlib
            from src.config import production

            importlib.reload(production)

            # Verify database defaults
            assert production.ProductionConfig.SQLALCHEMY_TRACK_MODIFICATIONS is False
            assert (
                "pool_timeout" in production.ProductionConfig.SQLALCHEMY_ENGINE_OPTIONS
            )
            assert (
                "pool_pre_ping" in production.ProductionConfig.SQLALCHEMY_ENGINE_OPTIONS
            )

    def test_production_config_session_settings(self):
        """Test session configuration"""
        test_secret = "a" * 64
        test_jwt_secret = "b" * 64

        with patch.dict(
            os.environ, {"SECRET_KEY": test_secret, "JWT_SECRET_KEY": test_jwt_secret}
        ):
            from src.config.production import ProductionConfig

            # Verify session settings
            assert ProductionConfig.SESSION_TYPE == "filesystem"
            assert ProductionConfig.SESSION_PERMANENT is False
            assert ProductionConfig.SESSION_USE_SIGNER is True
            assert ProductionConfig.SESSION_KEY_PREFIX == "inventory_"
            assert isinstance(ProductionConfig.PERMANENT_SESSION_LIFETIME, timedelta)

    def test_production_config_jwt_expiration(self):
        """Test JWT token expiration settings"""
        test_secret = "a" * 64
        test_jwt_secret = "b" * 64

        with patch.dict(
            os.environ, {"SECRET_KEY": test_secret, "JWT_SECRET_KEY": test_jwt_secret}
        ):
            from src.config.production import ProductionConfig

            # Verify JWT expiration
            assert isinstance(ProductionConfig.JWT_ACCESS_TOKEN_EXPIRES, timedelta)
            assert ProductionConfig.JWT_ACCESS_TOKEN_EXPIRES == timedelta(hours=24)

    def test_production_config_cors_settings(self):
        """Test CORS configuration"""
        test_secret = "a" * 64
        test_jwt_secret = "b" * 64

        with patch.dict(
            os.environ, {"SECRET_KEY": test_secret, "JWT_SECRET_KEY": test_jwt_secret}
        ):
            from src.config.production import ProductionConfig

            # Verify CORS settings
            assert hasattr(ProductionConfig, "CORS_ORIGINS")
            assert isinstance(ProductionConfig.CORS_ORIGINS, list)
            assert len(ProductionConfig.CORS_ORIGINS) > 0


class TestSecretValidation:
    """Test secret key validation"""

    def test_missing_secret_key_exits(self):
        """Test that missing SECRET_KEY causes exit"""
        # Clear SECRET_KEY from environment
        with patch.dict(os.environ, {"JWT_SECRET_KEY": "b" * 64}, clear=True):
            # Mock sys.exit to prevent actual exit
            with patch("sys.exit") as mock_exit:
                # Try to import config
                try:
                    import importlib
                    from src.config import production

                    importlib.reload(production)
                except SystemExit:
                    pass

                # Verify exit was called
                mock_exit.assert_called_once_with(1)

    def test_missing_jwt_secret_key_exits(self):
        """Test that missing JWT_SECRET_KEY causes exit"""
        # Clear JWT_SECRET_KEY from environment
        with patch.dict(os.environ, {"SECRET_KEY": "a" * 64}, clear=True):
            # Mock sys.exit to prevent actual exit
            with patch("sys.exit") as mock_exit:
                # Try to import config
                try:
                    import importlib
                    from src.config import production

                    importlib.reload(production)
                except SystemExit:
                    pass

                # Verify exit was called
                mock_exit.assert_called_once_with(1)

    def test_secret_validator_availability_flag(self):
        """Test that VALIDATOR_AVAILABLE flag is set correctly"""
        test_secret = "a" * 64
        test_jwt_secret = "b" * 64

        with patch.dict(
            os.environ, {"SECRET_KEY": test_secret, "JWT_SECRET_KEY": test_jwt_secret}
        ):
            from src.config.production import VALIDATOR_AVAILABLE

            # Verify flag is boolean
            assert isinstance(VALIDATOR_AVAILABLE, bool)

            # Note: Actual value depends on whether security.secret_validator is available
            # This test just verifies the flag exists and is boolean


class TestConfigImport:
    """Test config module imports"""

    def test_config_module_exports_production_config(self):
        """Test that config module exports ProductionConfig"""
        from src.config import ProductionConfig

        # Verify ProductionConfig is available
        assert ProductionConfig is not None
        assert hasattr(ProductionConfig, "SECRET_KEY")
        assert hasattr(ProductionConfig, "JWT_SECRET_KEY")

    def test_config_all_exports(self):
        """Test __all__ exports"""
        import src.config as config_module

        # Verify __all__ is defined
        assert hasattr(config_module, "__all__")
        assert "ProductionConfig" in config_module.__all__


class TestDatabaseConfiguration:
    """Test database configuration"""

    def test_database_uri_from_environment(self):
        """Test DATABASE_URL from environment"""
        test_secret = "a" * 64
        test_jwt_secret = "b" * 64
        test_db_url = "postgresql://user:pass@localhost:5432/store_erp"

        with patch.dict(
            os.environ,
            {
                "SECRET_KEY": test_secret,
                "JWT_SECRET_KEY": test_jwt_secret,
                "DATABASE_URL": test_db_url,
            },
        ):
            # Reload config to pick up new environment variable
            import importlib
            from src.config import production

            importlib.reload(production)

            # Verify database URL
            assert production.ProductionConfig.SQLALCHEMY_DATABASE_URI == test_db_url

    def test_database_uri_default_sqlite(self):
        """Test default SQLite database when DATABASE_URL not set"""
        test_secret = "a" * 64
        test_jwt_secret = "b" * 64

        with patch.dict(
            os.environ,
            {"SECRET_KEY": test_secret, "JWT_SECRET_KEY": test_jwt_secret},
            clear=True,
        ):
            # Reload config
            import importlib
            from src.config import production

            importlib.reload(production)

            # Verify default SQLite
            assert "sqlite:///" in production.ProductionConfig.SQLALCHEMY_DATABASE_URI
            assert "inventory.db" in production.ProductionConfig.SQLALCHEMY_DATABASE_URI

    def test_database_pool_settings(self):
        """Test database connection pool settings"""
        test_secret = "a" * 64
        test_jwt_secret = "b" * 64

        with patch.dict(
            os.environ, {"SECRET_KEY": test_secret, "JWT_SECRET_KEY": test_jwt_secret}
        ):
            from src.config.production import ProductionConfig

            # Verify pool settings
            pool_options = ProductionConfig.SQLALCHEMY_ENGINE_OPTIONS
            assert pool_options["pool_timeout"] == 20
            assert pool_options["pool_recycle"] == -1
            assert pool_options["pool_pre_ping"] is True


# Note: These tests require environment variables to be set
# Run with: SECRET_KEY=<key> JWT_SECRET_KEY=<key> pytest tests/test_config.py
