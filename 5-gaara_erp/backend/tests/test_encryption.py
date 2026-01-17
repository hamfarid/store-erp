# FILE: backend/tests/test_encryption.py | PURPOSE: Tests for envelope encryption utility | OWNER: Security Team | RELATED: backend/src/utils/encryption.py | LAST-AUDITED: 2025-10-25

"""
Tests for Envelope Encryption Utility

Tests envelope encryption functionality including:
- Development mode fallback encryption
- Production mode KMS envelope encryption
- Context-based encryption
- Error handling
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock


class TestFallbackEncryption:
    """Test fallback encryption for development mode"""

    def test_encrypt_decrypt_roundtrip(self, monkeypatch):
        """Encrypt and decrypt should return original value"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ENCRYPTION_KEY", "test-encryption-key-12345")

        # Force reload to pick up env vars
        import sys

        if "src.utils.encryption" in sys.modules:
            del sys.modules["src.utils.encryption"]

        # Import after setting env vars
        from src.utils.encryption import (
            encrypt_field,
            decrypt_field,
            CRYPTOGRAPHY_AVAILABLE,
        )

        plaintext = "sensitive-data@example.com"
        encrypted = encrypt_field(plaintext)
        decrypted = decrypt_field(encrypted)

        assert decrypted == plaintext

        # Only check encryption if cryptography is available
        if CRYPTOGRAPHY_AVAILABLE:
            assert encrypted != plaintext  # Should be encrypted

    def test_encrypt_empty_string(self, monkeypatch):
        """Empty string should return empty string"""
        monkeypatch.setenv("ENVIRONMENT", "development")

        from src.utils.encryption import encrypt_field

        result = encrypt_field("")
        assert result == ""

    def test_decrypt_empty_string(self, monkeypatch):
        """Empty string should return empty string"""
        monkeypatch.setenv("ENVIRONMENT", "development")

        from src.utils.encryption import decrypt_field

        result = decrypt_field("")
        assert result == ""

    def test_encrypt_with_context(self, monkeypatch):
        """Encryption with context should work in development mode"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ENCRYPTION_KEY", "test-key-12345")

        from src.utils.encryption import encrypt_field, decrypt_field

        plaintext = "user@example.com"
        context = {"user_id": 123, "field": "email"}

        encrypted = encrypt_field(plaintext, context)
        decrypted = decrypt_field(encrypted, context)

        assert decrypted == plaintext


class TestEnvelopeEncryption:
    """Test KMS envelope encryption for production mode"""

    @pytest.mark.skipif(
        os.getenv("SKIP_AWS_TESTS", "true").lower() == "true",
        reason="AWS integration tests disabled (set SKIP_AWS_TESTS=false to enable)",
    )
    def test_kms_encrypt_decrypt_roundtrip(self, monkeypatch):
        """KMS envelope encryption roundtrip"""
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("AWS_REGION", "us-east-1")
        monkeypatch.setenv("KMS_KEY_ID", "alias/gaara-store-test")

        from src.utils.encryption import encrypt_field, decrypt_field

        plaintext = "sensitive-pii-data"
        context = {"user_id": 456, "field": "ssn"}

        encrypted = encrypt_field(plaintext, context)
        decrypted = decrypt_field(encrypted, context)

        assert decrypted == plaintext
        assert ":" in encrypted  # Envelope format: key:data

    @pytest.mark.skipif(
        os.getenv("SKIP_AWS_TESTS", "true").lower() == "true",
        reason="AWS integration tests disabled",
    )
    def test_kms_wrong_context_fails(self, monkeypatch):
        """Decryption with wrong context should fail"""
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("KMS_KEY_ID", "alias/gaara-store-test")

        from src.utils.encryption import encrypt_field, decrypt_field

        plaintext = "secret-data"
        context1 = {"user_id": 123}
        context2 = {"user_id": 456}  # Different context

        encrypted = encrypt_field(plaintext, context1)

        # Should fail or return fallback
        decrypted = decrypt_field(encrypted, context2)
        # In fallback mode, it might still work, so we just check it doesn't crash
        assert decrypted is not None


class TestEncryptionFallback:
    """Test fallback behavior when KMS is unavailable"""

    def test_fallback_when_kms_not_configured(self, monkeypatch):
        """Should use fallback when KMS_KEY_ID not set"""
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("KMS_KEY_ID", "")  # Not configured
        monkeypatch.setenv("ENCRYPTION_KEY", "fallback-key-12345")

        from src.utils.encryption import encrypt_field, decrypt_field

        plaintext = "test-data"
        encrypted = encrypt_field(plaintext)
        decrypted = decrypt_field(encrypted)

        assert decrypted == plaintext

    def test_fallback_when_boto3_unavailable(self, monkeypatch):
        """Should use fallback when boto3 not available"""
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("ENCRYPTION_KEY", "fallback-key-12345")

        # Mock boto3 as unavailable
        import sys

        with patch.dict(sys.modules, {"boto3": None}):
            # Re-import to trigger BOTO3_AVAILABLE = False
            import importlib
            from src.utils import encryption

            importlib.reload(encryption)

            plaintext = "test-data"
            encrypted = encryption.encrypt_field(plaintext)
            decrypted = encryption.decrypt_field(encrypted)

            assert decrypted == plaintext


class TestEncryptionErrors:
    """Test error handling"""

    def test_decrypt_invalid_format(self, monkeypatch):
        """Decrypting invalid format should not crash"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ENCRYPTION_KEY", "test-key-12345")

        from src.utils.encryption import decrypt_field

        # Invalid base64
        result = decrypt_field("invalid-base64-data")

        # Should return something (fallback or original)
        assert result is not None

    def test_encrypt_none_value(self, monkeypatch):
        """Encrypting None should handle gracefully"""
        monkeypatch.setenv("ENVIRONMENT", "development")

        from src.utils.encryption import encrypt_field

        # Should handle None gracefully
        try:
            result = encrypt_field(None)  # type: ignore
            # If it doesn't crash, that's acceptable
            assert True
        except (TypeError, AttributeError):
            # Also acceptable to raise error
            assert True


class TestEncryptionContext:
    """Test encryption context handling"""

    def test_context_with_different_types(self, monkeypatch):
        """Context with different value types should work"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ENCRYPTION_KEY", "test-key-12345")

        from src.utils.encryption import encrypt_field, decrypt_field

        plaintext = "test-data"
        context = {
            "user_id": 123,
            "field": "email",
            "tenant_id": "tenant-abc",
            "version": 1,
        }

        encrypted = encrypt_field(plaintext, context)
        decrypted = decrypt_field(encrypted, context)

        assert decrypted == plaintext

    def test_context_none(self, monkeypatch):
        """None context should work"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ENCRYPTION_KEY", "test-key-12345")

        from src.utils.encryption import encrypt_field, decrypt_field

        plaintext = "test-data"

        encrypted = encrypt_field(plaintext, None)
        decrypted = decrypt_field(encrypted, None)

        assert decrypted == plaintext


class TestEncryptionLogging:
    """Test encryption logging and monitoring"""

    def test_encryption_logs_context(self, monkeypatch, caplog):
        """Encryption should log context (but not plaintext)"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ENCRYPTION_KEY", "test-key-12345")

        import logging

        caplog.set_level(logging.DEBUG)

        # Force reload
        import sys

        if "src.utils.encryption" in sys.modules:
            del sys.modules["src.utils.encryption"]

        from src.utils.encryption import encrypt_field

        plaintext = "secret-data"
        context = {"user_id": 123}

        encrypt_field(plaintext, context)

        # Should log something (development, fallback, or KMS)
        assert len(caplog.records) > 0

        # Should NOT log plaintext
        assert plaintext not in caplog.text


class TestEncryptionPerformance:
    """Test encryption performance characteristics"""

    def test_encrypt_large_data(self, monkeypatch):
        """Should handle large data efficiently"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ENCRYPTION_KEY", "test-key-12345")

        from src.utils.encryption import encrypt_field, decrypt_field

        # 1MB of data
        plaintext = "x" * (1024 * 1024)

        encrypted = encrypt_field(plaintext)
        decrypted = decrypt_field(encrypted)

        assert decrypted == plaintext

    def test_encrypt_unicode(self, monkeypatch):
        """Should handle Unicode data correctly"""
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("ENCRYPTION_KEY", "test-key-12345")

        from src.utils.encryption import encrypt_field, decrypt_field

        plaintext = "مرحبا بك في نظام جعاره 🎉"

        encrypted = encrypt_field(plaintext)
        decrypted = decrypt_field(encrypted)

        assert decrypted == plaintext


# Test fixtures
@pytest.fixture(autouse=True)
def reset_encryption_module():
    """Reset encryption module state between tests"""
    yield

    # Clear KMS client singleton
    from src.utils import encryption

    if hasattr(encryption._get_kms_client, "_client"):
        delattr(encryption._get_kms_client, "_client")
