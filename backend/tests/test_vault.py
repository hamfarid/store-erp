"""
Tests for Vault Client Integration

Tests cover:
- Vault client initialization
- Secret retrieval with caching
- Secret rotation
- Fallback to environment variables
- Error handling
- Health checks

Author: Store ERP Team
Date: 2025-11-06
Part of: T21 - KMS/Vault Integration
"""

import os
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Import Vault client
from src.vault_client import VaultClient, get_vault_client, get_secret, HVAC_AVAILABLE


class TestVaultClientInitialization:
    """Test Vault client initialization."""

    def test_client_initialization_with_env_vars(self):
        """Test client initialization using environment variables."""
        with patch.dict(
            os.environ,
            {
                "VAULT_ADDR": "http://vault.example.com:8200",
                "VAULT_TOKEN": "test-token",
                "FLASK_ENV": "development",
            },
        ):
            client = VaultClient()

            assert client.vault_url == "http://vault.example.com:8200"
            assert client.vault_token == "test-token"
            assert client.environment == "development"

    def test_client_initialization_with_parameters(self):
        """Test client initialization with explicit parameters."""
        client = VaultClient(
            vault_url="http://localhost:8200",
            vault_token="test-token",
            environment="production",
        )

        assert client.vault_url == "http://localhost:8200"
        assert client.vault_token == "test-token"
        assert client.environment == "production"

    def test_client_initialization_defaults(self):
        """Test client initialization with default values."""
        with patch.dict(os.environ, {}, clear=True):
            client = VaultClient()

            assert client.vault_url == "http://127.0.0.1:8200"
            assert client.environment == "development"
            assert client.mount_point == "secret"
            assert client.cache_ttl == 300


class TestSecretRetrieval:
    """Test secret retrieval functionality."""

    @pytest.mark.skipif(not HVAC_AVAILABLE, reason="hvac not installed")
    def test_get_secret_path_construction(self):
        """Test secret path construction."""
        client = VaultClient(environment="development")

        path = client._get_secret_path("flask/secret_key")
        assert path == "store-erp/development/flask/secret_key"

    @pytest.mark.skipif(not HVAC_AVAILABLE, reason="hvac not installed")
    def test_get_secret_with_cache(self):
        """Test secret retrieval with caching."""
        client = VaultClient()

        # Mock the Vault client
        mock_response = {
            "data": {
                "data": {
                    "secret_key": "test-secret-key",
                    "jwt_secret": "test-jwt-secret",
                }
            }
        }

        with patch.object(client, "client") as mock_vault:
            mock_vault.secrets.kv.v2.read_secret_version.return_value = mock_response
            client.authenticated = True

            # First call - should hit Vault
            result1 = client.get_secret("flask", use_cache=True)
            assert result1 == mock_response["data"]["data"]
            assert mock_vault.secrets.kv.v2.read_secret_version.call_count == 1

            # Second call - should use cache
            result2 = client.get_secret("flask", use_cache=True)
            assert result2 == mock_response["data"]["data"]
            # Call count should still be 1 (cached)
            assert mock_vault.secrets.kv.v2.read_secret_version.call_count == 1

    @pytest.mark.skipif(not HVAC_AVAILABLE, reason="hvac not installed")
    def test_get_secret_specific_field(self):
        """Test retrieving specific field from secret."""
        client = VaultClient()

        mock_response = {
            "data": {
                "data": {
                    "secret_key": "test-secret-key",
                    "jwt_secret": "test-jwt-secret",
                }
            }
        }

        with patch.object(client, "client") as mock_vault:
            mock_vault.secrets.kv.v2.read_secret_version.return_value = mock_response
            client.authenticated = True

            result = client.get_secret("flask", field="secret_key")
            assert result == "test-secret-key"

    def test_get_secret_fallback_to_env(self):
        """Test fallback to environment variable."""
        client = VaultClient()
        client.authenticated = False  # Simulate Vault not available

        with patch.dict(os.environ, {"SECRET_KEY": "env-secret-key"}):
            result = client.get_secret("flask", fallback_env="SECRET_KEY")
            assert result == "env-secret-key"

    def test_get_secret_not_found(self):
        """Test behavior when secret not found."""
        client = VaultClient()
        client.authenticated = False

        result = client.get_secret("nonexistent")
        assert result is None


class TestSecretRotation:
    """Test secret rotation functionality."""

    @pytest.mark.skipif(not HVAC_AVAILABLE, reason="hvac not installed")
    def test_rotate_secret(self):
        """Test secret rotation."""
        client = VaultClient()

        mock_response = {"data": {"data": {"secret_key": "old-secret-key"}}}

        with patch.object(client, "client") as mock_vault:
            mock_vault.secrets.kv.v2.read_secret_version.return_value = mock_response
            mock_vault.secrets.kv.v2.create_or_update_secret.return_value = None
            client.authenticated = True

            result = client.rotate_secret("flask", "secret_key", "new-secret-key")

            assert result is True
            # Verify set_secret was called with new value
            mock_vault.secrets.kv.v2.create_or_update_secret.assert_called_once()


class TestCaching:
    """Test caching functionality."""

    def test_cache_validity(self):
        """Test cache validity checking."""
        client = VaultClient(cache_ttl=1)  # 1 second TTL

        # Add to cache
        client._cache["test_key"] = ("test_value", datetime.now())

        # Should be valid immediately
        assert client._is_cache_valid("test_key") is True

        # Simulate time passing
        client._cache["test_key"] = (
            "test_value",
            datetime.now() - timedelta(seconds=2),
        )

        # Should be invalid after TTL
        assert client._is_cache_valid("test_key") is False

    def test_cache_invalidation(self):
        """Test cache invalidation."""
        client = VaultClient()

        # Add multiple entries to cache
        client._cache["flask:secret_key"] = ("value1", datetime.now())
        client._cache["flask:jwt_secret"] = ("value2", datetime.now())
        client._cache["database:password"] = ("value3", datetime.now())

        # Invalidate flask secrets
        client._invalidate_cache("flask")

        # Flask secrets should be removed
        assert "flask:secret_key" not in client._cache
        assert "flask:jwt_secret" not in client._cache

        # Database secret should remain
        assert "database:password" in client._cache

    def test_clear_cache(self):
        """Test clearing all cache."""
        client = VaultClient()

        # Add to cache
        client._cache["test_key"] = ("test_value", datetime.now())
        assert len(client._cache) > 0

        # Clear cache
        client.clear_cache()

        assert len(client._cache) == 0


class TestHealthCheck:
    """Test health check functionality."""

    def test_health_check_basic(self):
        """Test basic health check."""
        client = VaultClient()

        health = client.health_check()

        assert "vault_available" in health
        assert "vault_url" in health
        assert "authenticated" in health
        assert "environment" in health
        assert "cache_size" in health

    @pytest.mark.skipif(not HVAC_AVAILABLE, reason="hvac not installed")
    def test_health_check_with_vault(self):
        """Test health check with Vault connection."""
        client = VaultClient()

        mock_health = {"initialized": True, "sealed": False}

        with patch.object(client, "client") as mock_vault:
            mock_vault.sys.read_health_status.return_value = mock_health
            client.authenticated = True

            health = client.health_check()

            assert health["vault_initialized"] is True
            assert health["vault_sealed"] is False


class TestGlobalClient:
    """Test global client instance."""

    def test_get_vault_client_singleton(self):
        """Test that get_vault_client returns singleton."""
        client1 = get_vault_client()
        client2 = get_vault_client()

        assert client1 is client2

    def test_get_secret_convenience_function(self):
        """Test get_secret convenience function."""
        with patch("src.vault_client.get_vault_client") as mock_get_client:
            mock_client = Mock()
            mock_client.get_secret.return_value = "test-secret"
            mock_get_client.return_value = mock_client

            result = get_secret("flask", "secret_key", "SECRET_KEY")

            assert result == "test-secret"
            mock_client.get_secret.assert_called_once_with(
                "flask", "secret_key", "SECRET_KEY"
            )


class TestErrorHandling:
    """Test error handling."""

    @pytest.mark.skipif(not HVAC_AVAILABLE, reason="hvac not installed")
    def test_invalid_path_error(self):
        """Test handling of invalid path error."""
        client = VaultClient()

        with patch.object(client, "client") as mock_vault:
            import hvac

            mock_vault.secrets.kv.v2.read_secret_version.side_effect = (
                hvac.exceptions.InvalidPath()
            )
            client.authenticated = True

            result = client.get_secret("nonexistent")
            assert result is None

    @pytest.mark.skipif(not HVAC_AVAILABLE, reason="hvac not installed")
    def test_generic_error_handling(self):
        """Test handling of generic errors."""
        client = VaultClient()

        with patch.object(client, "client") as mock_vault:
            mock_vault.secrets.kv.v2.read_secret_version.side_effect = Exception(
                "Connection error"
            )
            client.authenticated = True

            result = client.get_secret("flask")
            assert result is None


# Integration tests (require actual Vault instance)
@pytest.mark.integration
class TestVaultIntegration:
    """Integration tests with actual Vault instance."""

    @pytest.fixture
    def vault_client(self):
        """Create Vault client for integration tests."""
        return VaultClient(
            vault_url=os.getenv("VAULT_ADDR", "http://127.0.0.1:8200"),
            vault_token=os.getenv("VAULT_TOKEN", "dev-root-token-change-me"),
        )

    def test_vault_connection(self, vault_client):
        """Test connection to Vault."""
        health = vault_client.health_check()
        assert health["authenticated"] is True or not HVAC_AVAILABLE

    def test_secret_retrieval_integration(self, vault_client):
        """Test actual secret retrieval from Vault."""
        if not vault_client.authenticated:
            pytest.skip("Vault not available")

        # This assumes secrets were created by setup_vault.ps1
        secret = vault_client.get_secret("flask", use_cache=False)
        assert secret is not None
