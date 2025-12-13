#!/usr/bin/env python3
"""
Generate Secure Secrets - توليد أسرار آمنة

This script generates cryptographically secure random secrets for the application.
يولد هذا السكريبت أسرار عشوائية آمنة تشفيرياً للتطبيق.

Usage:
    python scripts/generate_secrets.py

الاستخدام:
    python scripts/generate_secrets.py
"""

import secrets
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from security.secret_validator import SecretValidator
except ImportError:
    # Fallback if module not available
    class SecretValidator:
        @staticmethod
        def generate_secret(length=32):
            return secrets.token_hex(length)


def generate_all_secrets():
    """Generate all required secrets

    توليد جميع الأسرار المطلوبة
    """
    print("=" * 70)
    print("🔐 Secure Secret Generator")
    print("🔐 مولد الأسرار الآمنة")
    print("=" * 70)
    print()
    print("Generated cryptographically secure secrets:")
    print("الأسرار الآمنة المولدة تشفيرياً:")
    print()

    # Generate secrets
    secret_key = SecretValidator.generate_secret(32)
    jwt_secret_key = SecretValidator.generate_secret(32)

    # Display for .env file
    print("📝 Add these to your .env file:")
    print("📝 أضف هذه إلى ملف .env الخاص بك:")
    print()
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET_KEY={jwt_secret_key}")
    print()

    # Display for export commands
    print("=" * 70)
    print("🔧 Or set as environment variables:")
    print("🔧 أو قم بتعيينها كمتغيرات بيئة:")
    print()
    print("# Windows (PowerShell):")
    print(f"$env:SECRET_KEY='{secret_key}'")
    print(f"$env:JWT_SECRET_KEY='{jwt_secret_key}'")
    print()
    print("# Linux/Mac (Bash):")
    print(f"export SECRET_KEY='{secret_key}'")
    print(f"export JWT_SECRET_KEY='{jwt_secret_key}'")
    print()

    # Security warnings
    print("=" * 70)
    print("⚠️  SECURITY WARNINGS:")
    print("⚠️  تحذيرات الأمان:")
    print()
    print("1. Never commit these secrets to version control")
    print("   لا تقم أبداً بإرسال هذه الأسرار إلى نظام التحكم في الإصدار")
    print()
    print("2. Use different secrets for each environment")
    print("   استخدم أسرار مختلفة لكل بيئة")
    print()
    print("3. Store production secrets in a secure vault")
    print("   قم بتخزين أسرار الإنتاج في خزنة آمنة")
    print()
    print("4. Rotate secrets regularly (every 90 days)")
    print("   قم بتدوير الأسرار بانتظام (كل 90 يوماً)")
    print()
    print("=" * 70)

    # Save to file option
    print()
    response = input("💾 Save to .env.secrets file? (y/N): ")
    if response.lower() == "y":
        env_file = Path(__file__).parent.parent / ".env.secrets"
        with open(env_file, "w") as f:
            f.write(f"# Generated secrets - {secrets.token_hex(8)}\n")
            f.write(
                f"# IMPORTANT: Copy these to your .env file and delete this file!\n\n"
            )
            f.write(f"SECRET_KEY={secret_key}\n")
            f.write(f"JWT_SECRET_KEY={jwt_secret_key}\n")

        print(f"✅ Secrets saved to: {env_file}")
        print(f"✅ الأسرار محفوظة في: {env_file}")
        print()
        print("⚠️  Remember to:")
        print("⚠️  تذكر أن:")
        print("   1. Copy secrets to .env")
        print("   1. انسخ الأسرار إلى .env")
        print("   2. Delete .env.secrets file")
        print("   2. احذف ملف .env.secrets")
        print()


if __name__ == "__main__":
    generate_all_secrets()
