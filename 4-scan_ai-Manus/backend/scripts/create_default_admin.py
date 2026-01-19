"""
FILE: backend/scripts/create_default_admin.py | PURPOSE: Create default admin user | OWNER: DevOps Team | LAST-AUDITED: 2025-11-18

Create Default Admin User Script

Creates a default admin user with predefined credentials.

Version: 1.0.0
"""

import sys
from pathlib import Path

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir / "src"))

from datetime import datetime
from src.core import database
from src.core.config import get_settings
from src.models.user import User
from src.utils.password_policy import hash_password


def create_default_admin():
    """Create default admin user"""

    print("=" * 60)
    print("🚀 Gaara AI - Create Default Admin User")
    print("=" * 60)
    print()

    # Initialize database
    print("Initializing database...")
    settings = get_settings()
    database.init_database(settings)
    print("✅ Database initialized")
    print()

    # Default admin credentials
    email = "admin@gaara.ai"
    name = "Admin User"
    password = "Admin@Gaara123"  # Change this after first login!

    print("Creating default admin user...")
    print(f"Email: {email}")
    print(f"Name: {name}")
    print()

    # Create database session (access SessionLocal after initialization)
    db = database.SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"✅ Admin user already exists (ID: {existing_user.id})")
            print()
            print("Credentials:")
            print(f"  Email: {email}")
            print(f"  Password: Admin@Gaara123")
            print()
            return
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create admin user
        admin_user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            role="ADMIN",
            is_active=True,
            is_verified=True,
            email_verified_at=datetime.utcnow(),
            password_changed_at=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("=" * 60)
        print("✅ Default admin user created successfully!")
        print("=" * 60)
        print()
        print(f"ID:    {admin_user.id}")
        print(f"Email: {admin_user.email}")
        print(f"Name:  {admin_user.name}")
        print(f"Role:  {admin_user.role}")
        print()
        print("⚠️  IMPORTANT: Change the password after first login!")
        print()
        print("Login Credentials:")
        print(f"  Email:    {email}")
        print(f"  Password: Admin@Gaara123")
        print()
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_default_admin()

