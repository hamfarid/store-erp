#!/usr/bin/env python
"""
Seed Admin Script

This script seeds the database with default permissions, roles, and optionally an admin user.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from src.database import db
from src.models.admin import (
    Permission,
    Role,
    SystemSetup,
    seed_permissions_and_roles,
    DEFAULT_PERMISSIONS,
    DEFAULT_ROLES,
)
from src.models.user import User


def create_app():
    """Create Flask app for seeding."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///store.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


def seed_all():
    """Seed all admin data."""
    print("=" * 60)
    print("Store Pro - Admin Data Seeder")
    print("=" * 60)

    # Seed permissions and roles
    print("\n📦 Seeding permissions...")
    perm_count = Permission.query.count()
    if perm_count == 0:
        for perm_data in DEFAULT_PERMISSIONS:
            permission = Permission(**perm_data)
            db.session.add(permission)
        db.session.commit()
        print(f"   ✅ Created {len(DEFAULT_PERMISSIONS)} permissions")
    else:
        print(f"   ℹ️  {perm_count} permissions already exist")

    print("\n🛡️  Seeding roles...")
    role_count = Role.query.count()
    if role_count == 0:
        for role_data in DEFAULT_ROLES:
            perms = role_data.pop("permissions")
            role = Role(**role_data)

            # Assign permissions
            if perms == "*":
                role.permissions = Permission.query.all()
            else:
                for perm_pattern in perms:
                    if perm_pattern.endswith(".*"):
                        module = perm_pattern.replace(".*", "")
                        role.permissions.extend(
                            Permission.query.filter_by(module=module).all()
                        )
                    else:
                        perm = Permission.query.filter_by(code=perm_pattern).first()
                        if perm:
                            role.permissions.append(perm)

            db.session.add(role)
        db.session.commit()
        print(f"   ✅ Created {len(DEFAULT_ROLES)} roles")
    else:
        print(f"   ℹ️  {role_count} roles already exist")

    print("\n🔧 Checking system setup...")
    setup = SystemSetup.query.first()
    if not setup:
        setup = SystemSetup()
        db.session.add(setup)
        db.session.commit()
        print("   ✅ System setup initialized")
    else:
        print("   ℹ️  System setup already exists")

    print("\n" + "=" * 60)
    print("✨ Seeding complete!")
    print("=" * 60)

    # Summary
    print("\n📊 Summary:")
    print(f"   • Permissions: {Permission.query.count()}")
    print(f"   • Roles: {Role.query.count()}")
    print(f"   • Users: {User.query.count()}")
    print(f"   • Setup completed: {setup.is_completed}")


def create_admin_user(username, email, password, name):
    """Create an admin user."""
    print(f"\n👤 Creating admin user: {username}")

    existing = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing:
        print("   ⚠️  User already exists!")
        return None

    user = User(username=username, email=email, name=name, is_active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    # Assign super_admin role
    super_admin_role = Role.query.filter_by(code="super_admin").first()
    if super_admin_role:
        user.roles = [super_admin_role]

    db.session.commit()
    print(f"   ✅ Admin user created: {username}")
    return user


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Seed data
        seed_all()

        # Check if we should create admin user
        if len(sys.argv) > 1 and sys.argv[1] == "--create-admin":
            username = input("Enter admin username: ")
            email = input("Enter admin email: ")
            password = input("Enter admin password: ")
            name = input("Enter admin name: ")
            create_admin_user(username, email, password, name)
