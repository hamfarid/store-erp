#!/usr/bin/env python
"""Debug login flow step by step"""
import sys
import os

# Add src to path
sys.path.insert(0, ".")
os.environ["FLASK_ENV"] = "development"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-debugging"

from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "test-secret"
app.config["JWT_SECRET_KEY"] = "test-secret-key-for-debugging"
import os

db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "instance", "inventory.db"
)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
print(f"Database path: {db_path}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db
from src.database import db

db.init_app(app)

with app.app_context():
    print("\n=== Step 1: Import User model ===")
    try:
        from src.models.user import User, Role, AccountLockedError

        print("✅ User, Role, AccountLockedError imported successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)

    print("\n=== Step 2: Query User ===")
    try:
        user = User.query.filter_by(username="admin", is_active=True).first()
        print(f"✅ User found: {user}")
        print(f"   - id: {user.id}")
        print(f"   - username: {user.username}")
        print(f"   - email: {user.email}")
        print(f"   - role_id: {user.role_id}")
    except Exception as e:
        print(f"❌ User query error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    print("\n=== Step 3: Get Role ===")
    try:
        role = user.role
        print(f"✅ Role found: {role}")
        if role:
            print(f"   - name: {role.name}")
    except Exception as e:
        print(f"❌ Role error: {e}")
        import traceback

        traceback.print_exc()

    print("\n=== Step 4: Check Password ===")
    try:
        result = user.check_password("admin123")
        print(f"✅ Password check result: {result}")
    except Exception as e:
        print(f"❌ Password check error: {e}")
        import traceback

        traceback.print_exc()

    print("\n=== Step 5: Authenticate ===")
    try:
        authenticated_user = User.authenticate("admin", "admin123")
        print(f"✅ Authentication result: {authenticated_user}")
    except AccountLockedError as e:
        print(f"⚠️ Account locked: {e}")
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        import traceback

        traceback.print_exc()

    print("\n=== Step 6: to_dict() ===")
    try:
        user_dict = user.to_dict()
        print(f"✅ to_dict() result: {user_dict}")
    except Exception as e:
        print(f"❌ to_dict() error: {e}")
        import traceback

        traceback.print_exc()

    print("\n=== Step 7: JWT Token Creation ===")
    try:
        from src.jwt_manager import JWTManager

        access_token = JWTManager.create_access_token(user.id)
        print(f"✅ Access token created: {access_token[:50]}...")

        refresh_token, jti, exp = JWTManager.create_refresh_token(user.id)
        print(f"✅ Refresh token created: {refresh_token[:50]}...")
    except Exception as e:
        print(f"❌ JWT error: {e}")
        import traceback

        traceback.print_exc()

    print("\n=== All steps completed ===")
