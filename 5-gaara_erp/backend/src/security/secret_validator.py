#!/usr/bin/env python3
"""
Secret Validator - Validate application secrets
نظام التحقق من الأسرار - التحقق من أسرار التطبيق

This module validates that all required secrets are present and strong enough.
يتحقق هذا الوحدة من وجود جميع الأسرار المطلوبة وقوتها الكافية.

CRITICAL: This prevents the application from starting with weak or missing secrets.
حرج: يمنع هذا التطبيق من البدء بأسرار ضعيفة أو مفقودة.
"""

import os
import sys
import secrets
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class SecretValidator:
    """Validate and manage application secrets

    التحقق من وإدارة أسرار التطبيق
    """

    # Required secrets for the application
    # الأسرار المطلوبة للتطبيق
    REQUIRED_SECRETS = [
        "SECRET_KEY",
        "JWT_SECRET_KEY",
    ]

    # Minimum length for secrets (OWASP recommendation: 32+ chars)
    # الحد الأدنى لطول الأسرار (توصية OWASP: 32+ حرف)
    MIN_SECRET_LENGTH = 32

    # Weak/default secrets that should never be used
    # الأسرار الضعيفة/الافتراضية التي لا يجب استخدامها أبداً
    FORBIDDEN_SECRETS = [
        "dev-secret-key-change-in-production",
        "jwt-secret-key",
        "your-production-secret-key-change-this",
        "your-jwt-secret-key-change-this",
        "dev_secret_key_for_development_only_change_in_production_min_32_chars",
        "dev_jwt_secret_key_for_development_only_change_in_production_32",
        "change-this",
        "changeme",
        "secret",
        "password",
        "12345",
    ]

    @classmethod
    def validate_all(cls, environment: str = "development") -> bool:
        """Validate all required secrets are present and strong

        التحقق من وجود جميع الأسرار المطلوبة وقوتها

        Args:
            environment: Application environment (development/production)

        Returns:
            True if all secrets are valid, False otherwise

        Raises:
            SystemExit: If validation fails in production
        """
        missing = []
        weak = []
        forbidden = []

        for secret_name in cls.REQUIRED_SECRETS:
            value = os.environ.get(secret_name)

            if not value:
                missing.append(secret_name)
                continue

            # Check length
            if len(value) < cls.MIN_SECRET_LENGTH:
                weak.append((secret_name, len(value)))

            # Check if it's a forbidden/default secret
            if any(
                forbidden_val in value.lower()
                for forbidden_val in cls.FORBIDDEN_SECRETS
            ):
                forbidden.append(secret_name)

        # In production, fail hard if any issues
        if environment == "production":
            if missing or weak or forbidden:
                cls._print_error(missing, weak, forbidden, environment)
                logger.critical("❌ FATAL: Secret validation failed in production")
                sys.exit(1)
            return True

        # In development, warn but allow
        if missing or weak or forbidden:
            cls._print_warning(missing, weak, forbidden, environment)
            return False

        logger.info("✅ All secrets validated successfully")
        return True

    @classmethod
    def _print_error(
        cls,
        missing: List[str],
        weak: List[Tuple[str, int]],
        forbidden: List[str],
        environment: str,
    ):
        """Print detailed error message

        طباعة رسالة خطأ مفصلة
        """
        print("\n" + "=" * 70)
        print("❌ FATAL: Secret Validation Failed")
        print("❌ فشل التحقق من الأسرار")
        print("=" * 70)
        print(f"\nEnvironment: {environment}")
        print(f"البيئة: {environment}")

        if missing:
            print("\n🔴 Missing Required Secrets:")
            print("🔴 الأسرار المطلوبة المفقودة:")
            for secret in missing:
                print(f"  - {secret}")

        if weak:
            print(f"\n🔴 Weak Secrets (minimum {cls.MIN_SECRET_LENGTH} characters):")
            print(f"🔴 أسرار ضعيفة (الحد الأدنى {cls.MIN_SECRET_LENGTH} حرف):")
            for secret, length in weak:
                print(f"  - {secret}: {length} chars (need {cls.MIN_SECRET_LENGTH})")

        if forbidden:
            print("\n🔴 Forbidden/Default Secrets Detected:")
            print("🔴 تم اكتشاف أسرار محظورة/افتراضية:")
            for secret in forbidden:
                print(f"  - {secret}")
            print("\n⚠️  Never use default/example secrets in production!")
            print("⚠️  لا تستخدم أبداً الأسرار الافتراضية/الأمثلة في الإنتاج!")

        print("\n📝 How to fix:")
        print("📝 كيفية الإصلاح:")
        print("\n1. Generate secure secrets:")
        print("1. توليد أسرار آمنة:")
        print('   python -c "import secrets; print(secrets.token_hex(32))"')
        print("\n2. Set environment variables:")
        print("2. تعيين متغيرات البيئة:")
        for secret in cls.REQUIRED_SECRETS:
            print(f"   export {secret}='<your-secure-secret-here>'")
        print("\n3. Or update your .env file")
        print("3. أو تحديث ملف .env الخاص بك")
        print("\n" + "=" * 70)

    @classmethod
    def _print_warning(
        cls,
        missing: List[str],
        weak: List[Tuple[str, int]],
        forbidden: List[str],
        environment: str,
    ):
        """Print warning message for development

        طباعة رسالة تحذير للتطوير
        """
        print("\n" + "=" * 70)
        print("⚠️  WARNING: Secret Validation Issues (Development Mode)")
        print("⚠️  تحذير: مشاكل في التحقق من الأسرار (وضع التطوير)")
        print("=" * 70)

        if missing:
            print("\n⚠️  Missing secrets:")
            for secret in missing:
                print(f"  - {secret}")

        if weak:
            print(f"\n⚠️  Weak secrets (minimum {cls.MIN_SECRET_LENGTH} chars):")
            for secret, length in weak:
                print(f"  - {secret}: {length} chars")

        if forbidden:
            print("\n⚠️  Using default/example secrets:")
            for secret in forbidden:
                print(f"  - {secret}")

        print("\n💡 This is OK for development, but MUST be fixed for production!")
        print("💡 هذا مقبول للتطوير، ولكن يجب إصلاحه للإنتاج!")
        print("=" * 70 + "\n")

    @classmethod
    def generate_secret(cls, length: int = 32) -> str:
        """Generate a secure random secret

        توليد سر عشوائي آمن

        Args:
            length: Length of the secret in bytes (default: 32)

        Returns:
            Hexadecimal string of the secret
        """
        return secrets.token_hex(length)

    @classmethod
    def validate_secret_strength(cls, secret: str) -> Tuple[bool, str]:
        """Validate the strength of a single secret

        التحقق من قوة سر واحد

        Args:
            secret: The secret to validate

        Returns:
            Tuple of (is_valid, reason)
        """
        if not secret:
            return (False, "Secret is empty")

        if len(secret) < cls.MIN_SECRET_LENGTH:
            return (False, f"Secret too short (min {cls.MIN_SECRET_LENGTH} chars)")

        if any(forbidden in secret.lower() for forbidden in cls.FORBIDDEN_SECRETS):
            return (False, "Secret contains forbidden/default values")

        # Check for sufficient entropy (basic check)
        unique_chars = len(set(secret))
        if unique_chars < 10:
            return (
                False,
                "Secret has insufficient entropy (too few unique characters)",
            )

        return (True, "Secret is strong")


def validate_secrets_on_startup(environment: str = None):
    """Validate secrets when application starts

    التحقق من الأسرار عند بدء التطبيق

    Args:
        environment: Application environment (auto-detected if None)
    """
    if environment is None:
        environment = os.environ.get("FLASK_ENV", "development")

    logger.info(f"Validating secrets for environment: {environment}")
    SecretValidator.validate_all(environment)


if __name__ == "__main__":
    # Test the validator
    print("🔐 Secret Validator Test")
    print("🔐 اختبار مدقق الأسرار\n")

    # Generate example secrets
    print("Example secure secrets:")
    print("أمثلة على الأسرار الآمنة:\n")
    print(f"SECRET_KEY={SecretValidator.generate_secret()}")
    print(f"JWT_SECRET_KEY={SecretValidator.generate_secret()}")

    print("\n" + "=" * 70)
    print("Testing validation...")
    print("اختبار التحقق...")
    validate_secrets_on_startup()
