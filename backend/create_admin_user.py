#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create Admin User Script
Creates a default admin user for testing the inventory system.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from main import app, db  # noqa: E402
from models.user import User, Role  # noqa: E402
from sqlalchemy.exc import SQLAlchemyError  # noqa: E402


def create_admin_user():
    """Create a default admin user"""
    with app.app_context():
        try:
            # Check if admin user already exists
            existing_admin = User.query.filter_by(username="admin").first()
            if existing_admin:
                print("✅ Admin user already exists!")
                print("   Username: admin")
                print(f"   Email: {existing_admin.email}")
                print(
                    f"   Role: {existing_admin.role.name if existing_admin.role else 'N/A'}"
                )
                return existing_admin

            # Check if admin role exists
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                # Create admin role
                admin_role = Role()
                admin_role.name = "admin"
                admin_role.description = "System Administrator - Full system access"
                admin_role.permissions = {"all": True}
                admin_role.is_active = True
                db.session.add(admin_role)
                db.session.commit()
                print("✅ Created admin role")

            # Create admin user
            admin_user: User = User.create_user(  # type: ignore[attr-defined]
                username="admin",
                password=os.getenv("ADMIN_PASSWORD", "change_me"),
                email="admin@inventory.com",
                full_name="System Administrator",
                role_id=admin_role.id,
                is_active=True,
            )

            print("✅ Admin user created successfully!")
            print("   Username: admin")
            print("   Password: admin123")
            print(f"   Email: {admin_user.email}")
            print(f"   Role: {admin_role.name}")
            print("\n⚠️  IMPORTANT: Change the password after first login!")

            return admin_user

        except (SQLAlchemyError, ValueError) as exc:
            print(f"❌ Error creating admin user: {exc}")
            db.session.rollback()
            import traceback

            traceback.print_exc()
            return None


def test_login():
    """Test the login functionality"""
    with app.app_context():
        try:
            print("\n🔍 Testing login functionality...")

            # Try to authenticate
            user = User.authenticate("admin", "admin123")

            if user:
                print("✅ Login test successful!")
                print(f"   Authenticated as: {user.username}")
                print(f"   Full name: {user.full_name}")
                print(f"   Email: {user.email}")
                return True
            else:
                print("❌ Login test failed - authentication returned None")
                return False

        except SQLAlchemyError as exc:
            print(f"❌ Login test error: {exc}")
            import traceback

            traceback.print_exc()
            return False


def main():
    """Main function"""
    print("=" * 60)
    print("Creating Admin User for Inventory System")
    print("=" * 60)

    # Create admin user
    admin = create_admin_user()

    if admin:
        # Test login
        test_login()

        print("\n" + "=" * 60)
        print("✅ Setup complete!")
        print("=" * 60)
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nFrontend: http://localhost:5502")
        print("Backend API: http://127.0.0.1:8000")
        print("=" * 60)
    else:
        print("\n❌ Failed to create admin user")
        sys.exit(1)


if __name__ == "__main__":
    main()
