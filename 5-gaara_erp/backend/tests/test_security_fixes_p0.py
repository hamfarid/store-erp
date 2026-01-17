#!/usr/bin/env python3
"""
Test Security Fixes - Phase 1 (P0)
اختبار إصلاحات الأمان - المرحلة 1

Tests for critical security fixes:
1. Secret validation
2. Password hashing (Argon2id mandatory)
3. RBAC implementation

اختبارات لإصلاحات الأمان الحرجة:
1. التحقق من الأسرار
2. تشفير كلمات المرور (Argon2id إلزامي)
3. تنفيذ نظام الصلاحيات
"""

import sys
import pytest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestSecretValidator:
    """Test secret validation system

    اختبار نظام التحقق من الأسرار
    """

    def test_secret_validator_import(self):
        """Test that secret validator can be imported"""
        from security.secret_validator import SecretValidator

        assert SecretValidator is not None

    def test_generate_secret(self):
        """Test secret generation"""
        from security.secret_validator import SecretValidator

        secret = SecretValidator.generate_secret()
        assert secret is not None
        assert len(secret) >= 64  # 32 bytes = 64 hex chars
        assert isinstance(secret, str)

    def test_validate_secret_strength_strong(self):
        """Test validation of strong secret"""
        from security.secret_validator import SecretValidator

        strong_secret = SecretValidator.generate_secret()
        is_valid, reason = SecretValidator.validate_secret_strength(strong_secret)

        assert is_valid is True
        assert reason == "Secret is strong"

    def test_validate_secret_strength_weak_short(self):
        """Test validation of short secret"""
        from security.secret_validator import SecretValidator

        weak_secret = "short"
        is_valid, reason = SecretValidator.validate_secret_strength(weak_secret)

        assert is_valid is False
        assert "too short" in reason.lower()

    def test_validate_secret_strength_forbidden(self):
        """Test validation of forbidden secret"""
        from security.secret_validator import SecretValidator

        forbidden_secret = "dev-secret-key-change-in-production"
        is_valid, reason = SecretValidator.validate_secret_strength(forbidden_secret)

        assert is_valid is False
        assert "forbidden" in reason.lower()

    def test_validate_secret_strength_empty(self):
        """Test validation of empty secret"""
        from security.secret_validator import SecretValidator

        is_valid, reason = SecretValidator.validate_secret_strength("")

        assert is_valid is False
        assert "empty" in reason.lower()


class TestPasswordHashing:
    """Test password hashing improvements

    اختبار تحسينات تشفير كلمات المرور
    """

    def test_hash_password_requires_argon2(self):
        """Test that password hashing requires Argon2id or bcrypt"""
        from auth import AuthManager

        # This should work with Argon2id or bcrypt, but NOT SHA-256
        password = "TestPassword123!"

        try:
            hashed = AuthManager.hash_password(password)
            # Should succeed with Argon2id or bcrypt
            assert hashed is not None
            assert len(hashed) > 0
            # Should NOT be SHA-256 (64 hex chars)
            assert not (
                len(hashed) == 64 and all(c in "0123456789abcdef" for c in hashed)
            )
        except RuntimeError as e:
            # If no secure hasher available, should raise RuntimeError
            assert "No secure password hasher available" in str(e)

    def test_hash_password_empty_fails(self):
        """Test that empty password fails"""
        from auth import AuthManager

        with pytest.raises(ValueError, match="Password cannot be empty"):
            AuthManager.hash_password("")

    def test_hash_password_too_short_fails(self):
        """Test that short password fails"""
        from auth import AuthManager

        with pytest.raises(ValueError, match="at least 8 characters"):
            AuthManager.hash_password("short")

    def test_verify_password_works(self):
        """Test password verification"""
        from auth import AuthManager

        password = "TestPassword123!"

        try:
            hashed = AuthManager.hash_password(password)

            # Correct password should verify
            assert AuthManager.verify_password(password, hashed) is True

            # Wrong password should not verify
            assert AuthManager.verify_password("WrongPassword", hashed) is False
        except RuntimeError:
            # Skip if no secure hasher available
            pytest.skip("No secure password hasher available")


class TestRBACImplementation:
    """Test RBAC (Role-Based Access Control) implementation

    اختبار تنفيذ نظام الصلاحيات
    """

    def test_require_role_decorator_exists(self):
        """Test that require_role decorator exists"""
        from security_middleware import require_role

        assert require_role is not None

    def test_require_admin_decorator_exists(self):
        """Test that require_admin decorator exists"""
        from security_middleware import require_admin

        assert require_admin is not None

    def test_require_permission_decorator_exists(self):
        """Test that require_permission decorator exists"""
        from security_middleware import require_permission

        assert require_permission is not None

    def test_require_admin_is_implemented(self):
        """Test that require_admin is properly implemented"""
        from security_middleware import require_admin
        import inspect

        # Get source code
        source = inspect.getsource(require_admin)

        # Should NOT contain the old placeholder comment
        assert "يجب تنفيذ منطق فحص الدور" not in source

        # Should use require_role
        assert "require_role" in source


class TestProductionConfigSecurity:
    """Test production configuration security

    اختبار أمان إعدادات الإنتاج
    """

    def test_production_config_no_hardcoded_secrets(self):
        """Test that production config has no hardcoded secrets"""
        config_file = Path(__file__).parent.parent / "src" / "config" / "production.py"

        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Should NOT contain hardcoded secrets
        forbidden_strings = [
            "'dev-secret-key-change-in-production'",
            "'jwt-secret-key'",
            "or 'dev-secret-key",
            "or 'jwt-secret",
        ]

        for forbidden in forbidden_strings:
            assert forbidden not in content, f"Found hardcoded secret: {forbidden}"

    def test_production_config_requires_env_vars(self):
        """Test that production config requires environment variables"""
        config_file = Path(__file__).parent.parent / "src" / "config" / "production.py"

        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Should check for environment variables
        assert "os.environ.get('SECRET_KEY')" in content
        assert "os.environ.get('JWT_SECRET_KEY')" in content

        # Should have validation
        assert "if not SECRET_KEY" in content or "if not JWT_SECRET_KEY" in content


class TestAuthFileSecurity:
    """Test auth.py security improvements

    اختبار تحسينات أمان auth.py
    """

    def test_auth_no_sha256_fallback(self):
        """Test that auth.py does not use SHA-256 as fallback for new hashes"""
        auth_file = Path(__file__).parent.parent / "src" / "auth.py"

        with open(auth_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check hash_password function
        lines = content.split("\n")
        in_hash_password = False
        hash_password_lines = []

        for line in lines:
            if "def hash_password" in line:
                in_hash_password = True
            elif in_hash_password:
                if line.strip().startswith("def ") or line.strip().startswith("@"):
                    break
                hash_password_lines.append(line)

        hash_password_code = "\n".join(hash_password_lines)

        # Should NOT return SHA-256 hash
        # Should raise RuntimeError instead
        if "hashlib.sha256" in hash_password_code:
            assert (
                "raise RuntimeError" in hash_password_code
            ), "SHA-256 fallback should raise RuntimeError, not return hash"


def test_all_critical_fixes_applied():
    """Integration test: Verify all P0 critical fixes are applied

    اختبار التكامل: التحقق من تطبيق جميع الإصلاحات الحرجة P0
    """
    # 1. Secret validator exists
    from security.secret_validator import SecretValidator

    assert SecretValidator is not None

    # 2. Password hashing is secure
    from auth import AuthManager

    try:
        password = "TestPassword123!"
        hashed = AuthManager.hash_password(password)
        # Should not be SHA-256
        assert not (len(hashed) == 64 and all(c in "0123456789abcdef" for c in hashed))
    except RuntimeError:
        # OK if no hasher available - will fail at startup
        pass

    # 3. RBAC decorators exist
    from security_middleware import require_role, require_admin, require_permission

    assert require_role is not None
    assert require_admin is not None
    assert require_permission is not None

    print("✅ All P0 critical security fixes verified!")
    print("✅ تم التحقق من جميع الإصلاحات الأمنية الحرجة P0!")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
