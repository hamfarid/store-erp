#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0.16: سكريبت لإعادة تعيين كلمة مرور المستخدم admin
Reset admin password script - uses secure random password generation

SECURITY: Never hardcode passwords. This script generates a cryptographically
secure random password at runtime.
"""

import sys
import os
import secrets
import string

from src.models.user_unified import User
from werkzeug.security import generate_password_hash

try:
    from src.database import db
except Exception:
    from database import db

try:
    from app import create_app
except Exception:
    from backend.app import create_app  # fallback when running from repo root


def generate_secure_password(length: int = 24) -> str:
    """
    P0.16: Generate a cryptographically secure random password

    Args:
        length: Password length (default 24 characters)

    Returns:
        Secure random password with mixed case, numbers, and symbols
    """
    # Use secrets module for cryptographically secure random generation
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"

    # Ensure at least one of each character type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*"),
    ]

    # Fill the rest randomly
    password.extend(secrets.choice(alphabet) for _ in range(length - 4))

    # Shuffle to avoid predictable positions
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)

    return "".join(password_list)


def reset_admin_password(custom_password: str = None):
    """
    إعادة تعيين كلمة مرور admin

    Args:
        custom_password: Optional custom password (will generate random if not provided)
    """
    app = create_app()

    with app.app_context():
        # البحث عن المستخدم admin
        admin = User.query.filter_by(username="admin").first()

        if not admin:
            print("❌ المستخدم admin غير موجود!")
            print("Creating admin user...")

            # إنشاء مستخدم admin جديد
            admin = User()
            admin.username = "admin"
            admin.email = "admin@example.com"
            admin.full_name = "System Administrator"
            admin.role_id = 1
            admin.is_active = True
            db.session.add(admin)

        # P0.16: Generate or use secure password
        if custom_password:
            new_password = custom_password
        else:
            new_password = generate_secure_password()

        admin.password_hash = generate_password_hash(new_password)

        try:
            db.session.commit()
            print("✅ تم إعادة تعيين كلمة مرور admin بنجاح!")
            print("Username: admin")
            print(f"Password: {new_password}")
            print(
                "\n⚠️  IMPORTANT: Store this password securely and change it after first login!"
            )
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ: {e}")


if __name__ == "__main__":
    # Allow passing password as command line argument
    custom_pwd = sys.argv[1] if len(sys.argv) > 1 else None
    reset_admin_password(custom_pwd)
