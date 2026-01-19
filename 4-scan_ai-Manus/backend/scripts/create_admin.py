"""
FILE: backend/scripts/create_admin.py | PURPOSE: Create admin user | OWNER: DevOps Team | LAST-AUDITED: 2025-11-18

Create Admin User Script

Creates the first admin user for the Gaara AI application.

Version: 1.0.0
"""

import sys
from pathlib import Path

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir / "src"))

from datetime import datetime
from src.core.database import SessionLocal
from src.models.user import User
from src.utils.password_policy import hash_password


def create_admin_user():
    """Create the first admin user"""
    
    print("=" * 60)
    print("🚀 Gaara AI - Create Admin User")
    print("=" * 60)
    print()
    
    # Get user input
    print("Please enter admin user details:")
    print()
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Error: Email is required")
        return
    
    name = input("Name: ").strip()
    if not name:
        print("❌ Error: Name is required")
        return
    
    password = input("Password (min 12 chars): ").strip()
    if not password or len(password) < 12:
        print("❌ Error: Password must be at least 12 characters")
        return
    
    password_confirm = input("Confirm Password: ").strip()
    if password != password_confirm:
        print("❌ Error: Passwords do not match")
        return
    
    phone = input("Phone (optional): ").strip() or None
    
    print()
    print("Creating admin user...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ Error: User with email '{email}' already exists")
            return
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create admin user
        admin_user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            phone=phone,
            role="ADMIN",
            is_active=True,
            is_verified=True,
            email_verified_at=datetime.utcnow(),
            password_changed_at=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print()
        print("=" * 60)
        print("✅ Admin user created successfully!")
        print("=" * 60)
        print()
        print(f"ID:    {admin_user.id}")
        print(f"Email: {admin_user.email}")
        print(f"Name:  {admin_user.name}")
        print(f"Role:  {admin_user.role}")
        print()
        print("You can now login with these credentials.")
        print()
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()

