"""Test login with verbose error output"""

import sys

sys.path.insert(0, ".")

from app import create_app
from src.database import db
from src.models.user import User
import traceback

app = create_app()

with app.app_context():
    try:
        print("Testing login logic...")

        # Find user
        user = db.session.query(User).filter_by(username="admin").first()

        if not user:
            print("❌ User not found!")
            sys.exit(1)

        print(f"✅ Found user: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Active: {user.is_active}")
        print(f"   Password hash: {user.password_hash[:50]}...")

        # Test password verification using the User model method
        print("\nTesting password verification via user.check_password()...")
        result = user.check_password("admin123")
        print(f"   check_password result: {result}")

        if result:
            print("✅ Password verification successful!")
        else:
            print("❌ Password verification failed!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
