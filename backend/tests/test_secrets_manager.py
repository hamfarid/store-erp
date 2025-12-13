# FILE: backend/tests/test_secrets_manager.py | PURPOSE: Tests for secrets manager | OWNER: Security Team | RELATED: backend/src/utils/secrets_manager.py | LAST-AUDITED: 2025-10-25

"""
Tests for AWS Secrets Manager adapter

Tests cover:
- Secret retrieval from AWS
- Caching behavior
- Fallback to .env
- Error handling
- Cache management
"""

import os
import pytest
import time

# Import the module under test
from src.utils.secrets_manager import (
    get_secret,
    clear_cache,
    get_cache_stats,
    SecretNotFoundError,
    SecretsManagerError,
    _redact_secret,
    _get_secret_from_env,
)


class TestSecretRedaction:
    """Test secret redaction for logging"""

    def test_redact_empty_secret(self):
        """Empty secrets should show [EMPTY]"""
        assert _redact_secret("") == "[EMPTY]"
        assert _redact_secret(None) == "[EMPTY]"  # type: ignore

    def test_redact_short_secret(self):
        """Short secrets (≤4 chars) should be fully redacted"""
        assert _redact_secret("abc") == "[REDACTED]"
        assert _redact_secret("1234") == "[REDACTED]"

    def test_redact_long_secret(self):
        """Long secrets should show first 2 and last 2 chars"""
        assert _redact_secret("my-secret-key-12345") == "my...45 [REDACTED]"
        assert _redact_secret("abcdefghij") == "ab...ij [REDACTED]"


class TestEnvFallback:
    """Test fallback to environment variables"""

    def test_get_secret_from_env_found(self, monkeypatch):
        """Should retrieve secret from .env"""
        monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")

        value = _get_secret_from_env("database-url")
        assert value == "postgresql://localhost/test"

    def test_get_secret_from_env_not_found(self, monkeypatch):
        """Should return None if not found"""
        monkeypatch.delenv("JWT_SECRET", raising=False)

        value = _get_secret_from_env("jwt-secret")
        assert value is None

    def test_get_secret_from_env_with_default(self, monkeypatch):
        """Should return default if not found"""
        monkeypatch.delenv("SMTP_PASSWORD", raising=False)

        value = _get_secret_from_env("smtp-password", default="default-pass")
        assert value == "default-pass"


class TestDevelopmentMode:
    """Test secrets manager in development mode"""

    @pytest.fixture(autouse=True)
    def setup_dev_mode(self, monkeypatch):
        """Set environment to development"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        clear_cache()  # Clear cache before each test

    def test_get_secret_from_env_in_dev(self, monkeypatch):
        """Development mode should use .env"""
        monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/dev")

        value = get_secret("database-url")
        assert value == "postgresql://localhost/dev"

    def test_get_secret_not_found_in_dev(self, monkeypatch):
        """Should raise error if not in .env and no default"""
        monkeypatch.delenv("MISSING_SECRET", raising=False)

        with pytest.raises(SecretNotFoundError, match="not found in .env"):
            get_secret("missing-secret")

    def test_get_secret_with_default_in_dev(self, monkeypatch):
        """Should return default if not in .env"""
        monkeypatch.delenv("OPTIONAL_SECRET", raising=False)

        value = get_secret("optional-secret", default="default-value")
        assert value == "default-value"


class TestCaching:
    """Test secret caching behavior"""

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        """Setup for caching tests"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("SECRET_CACHE_TTL", "10")  # 10 seconds TTL
        clear_cache()

    def test_secret_cached_on_first_access(self, monkeypatch):
        """First access should cache the secret"""
        monkeypatch.setenv("TEST_SECRET", "cached-value")

        # First access
        value1 = get_secret("test-secret")

        # Check cache
        stats = get_cache_stats()
        assert stats["cached_secrets"] == 1
        assert "test-secret" in stats["secrets"]

        # Second access should use cache
        value2 = get_secret("test-secret")
        assert value1 == value2

    def test_force_refresh_bypasses_cache(self, monkeypatch):
        """force_refresh should bypass cache"""
        monkeypatch.setenv("TEST_SECRET", "initial-value")

        # First access (cached)
        value1 = get_secret("test-secret")
        assert value1 == "initial-value"

        # Change env var
        monkeypatch.setenv("TEST_SECRET", "updated-value")

        # Without force_refresh, should use cache
        value2 = get_secret("test-secret")
        assert value2 == "initial-value"  # Still cached

        # With force_refresh, should get new value
        value3 = get_secret("test-secret", force_refresh=True)
        assert value3 == "updated-value"

    def test_cache_expiration(self, monkeypatch):
        """Cache should expire after TTL"""
        # Note: CACHE_TTL is read at module import time, so we can't change it dynamically
        # Instead, we'll manually manipulate the cache timestamp to simulate expiration

        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("TEST_SECRET", "initial-value")
        clear_cache()

        # First access (cached)
        value1 = get_secret("test-secret")
        assert value1 == "initial-value"

        # Manually expire the cache by setting timestamp to past
        from src.utils import secrets_manager

        secrets_manager._secret_cache["test-secret"]["timestamp"] = (
            time.time() - 400
        )  # Older than TTL

        # Change env var
        monkeypatch.setenv("TEST_SECRET", "updated-value")

        # Should fetch new value (cache expired)
        value2 = get_secret("test-secret")
        assert value2 == "updated-value"

    def test_clear_cache_specific_secret(self, monkeypatch):
        """Should clear cache for specific secret"""
        monkeypatch.setenv("SECRET_1", "value1")
        monkeypatch.setenv("SECRET_2", "value2")

        # Cache both secrets
        get_secret("secret-1")
        get_secret("secret-2")

        assert get_cache_stats()["cached_secrets"] == 2

        # Clear only secret-1
        clear_cache("secret-1")

        stats = get_cache_stats()
        assert stats["cached_secrets"] == 1
        assert "secret-2" in stats["secrets"]
        assert "secret-1" not in stats["secrets"]

    def test_clear_all_cache(self, monkeypatch):
        """Should clear all cached secrets"""
        monkeypatch.setenv("SECRET_1", "value1")
        monkeypatch.setenv("SECRET_2", "value2")

        # Cache both secrets
        get_secret("secret-1")
        get_secret("secret-2")

        assert get_cache_stats()["cached_secrets"] == 2

        # Clear all
        clear_cache()

        assert get_cache_stats()["cached_secrets"] == 0


class TestCacheStats:
    """Test cache statistics"""

    def test_cache_stats_empty(self):
        """Empty cache should return correct stats"""
        clear_cache()

        stats = get_cache_stats()
        assert stats["cached_secrets"] == 0
        assert stats["secrets"] == []
        assert "cache_ttl" in stats
        assert "environment" in stats
        assert "boto3_available" in stats

    def test_cache_stats_with_secrets(self, monkeypatch):
        """Stats should reflect cached secrets"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("SECRET_1", "value1")
        monkeypatch.setenv("SECRET_2", "value2")
        clear_cache()

        # Cache secrets
        get_secret("secret-1")
        get_secret("secret-2")

        stats = get_cache_stats()
        assert stats["cached_secrets"] == 2
        assert set(stats["secrets"]) == {"secret-1", "secret-2"}


@pytest.mark.skipif(
    os.getenv("SKIP_AWS_TESTS", "true").lower() == "true",
    reason="AWS integration tests disabled (set SKIP_AWS_TESTS=false to enable)",
)
class TestAWSIntegration:
    """Integration tests with AWS Secrets Manager (requires AWS credentials)"""

    @pytest.fixture(autouse=True)
    def setup_prod_mode(self, monkeypatch):
        """Set environment to production"""
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("AWS_REGION", "us-east-1")
        clear_cache()

    def test_get_secret_from_aws(self):
        """Should retrieve secret from AWS (requires real AWS setup)"""
        # This test requires:
        # 1. AWS credentials configured
        # 2. Secret 'gaara-store/production/test-secret' exists in AWS

        try:
            value = get_secret("test-secret")
            assert value is not None
            assert len(value) > 0
        except SecretsManagerError as e:
            pytest.skip(f"AWS not configured: {e}")

    def test_secret_not_found_in_aws(self):
        """Should raise error for non-existent secret"""
        with pytest.raises(SecretNotFoundError):
            get_secret("non-existent-secret-12345")


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
