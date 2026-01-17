"""Test login logic directly"""

import sys
import traceback

# Add the backend directory to the path
sys.path.insert(0, ".")

try:
    from app import create_app
    from src.database import db

    print("Creating app...")
    app = create_app()

    with app.app_context():
        print("Querying for admin user...")
        from src.models.user import User

        user = db.session.query(User).filter_by(username="admin").first()

        if user:
            print(f"✅ Found user: {user.username}, email: {user.email}")
            print(f"   Active: {user.is_active}")
            print(f"   Role ID: {user.role_id}")

            # Test password verification
            print("\nTesting password verification...")
            from werkzeug.security import check_password_hash
            import bcrypt

            password = "admin123"

            # Try bcrypt first
            try:
                is_valid = bcrypt.checkpw(
                    password.encode("utf-8"), user.password_hash.encode("utf-8")
                )
                print(f"   Bcrypt check: {is_valid}")
            except Exception as e:
                print(f"   Bcrypt check failed: {e}")

            # Try werkzeug
            try:
                is_valid = check_password_hash(user.password_hash, password)
                print(f"   Werkzeug check: {is_valid}")
            except Exception as e:
                print(f"   Werkzeug check failed: {e}")

        else:
            print("❌ User not found!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
