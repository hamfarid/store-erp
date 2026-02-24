#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test login functionality directly"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Suppress print encoding issues
os.environ['PYTHONIOENCODING'] = 'utf-8'

def test_login():
    """Test the login process step by step"""
    print("=" * 60)
    print("Testing Login Process")
    print("=" * 60)
    
    # Step 1: Create Flask app
    print("\n1. Creating Flask app...")
    try:
        from app import create_app
        app = create_app()
        print("   OK: App created")
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
        return
    
    with app.app_context():
        # Step 2: Test database connection
        print("\n2. Testing database...")
        try:
            from src.database import db
            result = db.session.execute(db.text("SELECT COUNT(*) FROM users")).scalar()
            print(f"   OK: {result} users in database")
        except Exception as e:
            print(f"   ERROR: {e}")
            return
        
        # Step 3: Test User model import
        print("\n3. Testing User model import...")
        try:
            from src.models.user import User, Role
            print("   OK: User model imported")
        except Exception as e:
            print(f"   ERROR: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 4: Query for admin user using raw SQL first
        print("\n4. Querying admin user (raw SQL)...")
        try:
            row = db.session.execute(
                db.text("SELECT id, username, password_hash FROM users WHERE username='admin'")
            ).fetchone()
            if row:
                print(f"   OK: Admin found - ID: {row[0]}, Username: {row[1]}")
                print(f"   Password hash: {row[2][:30]}...")
            else:
                print("   ERROR: Admin not found")
                return
        except Exception as e:
            print(f"   ERROR: {e}")
            return
        
        # Step 5: Query using ORM
        print("\n5. Querying admin user (ORM)...")
        try:
            admin = User.query.filter_by(username='admin').first()
            print(f"   OK: Admin found - {admin}")
            print(f"   Username: {admin.username}")
        except Exception as e:
            print(f"   ERROR: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 6: Test password verification
        print("\n6. Testing password verification...")
        try:
            result = admin.check_password('admin123')
            print(f"   Password check result: {result}")
        except Exception as e:
            print(f"   ERROR: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 7: Test role access
        print("\n7. Testing role access...")
        try:
            role = admin.role
            print(f"   Role: {role}")
            if role:
                print(f"   Role name: {role.name}")
        except Exception as e:
            print(f"   ERROR: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 8: Test to_dict()
        print("\n8. Testing to_dict()...")
        try:
            user_dict = admin.to_dict()
            print(f"   OK: to_dict() returned {len(user_dict)} keys")
            print(f"   Keys: {list(user_dict.keys())}")
        except Exception as e:
            print(f"   ERROR: {e}")
            import traceback
            traceback.print_exc()
            return
        
        print("\n" + "=" * 60)
        print("All tests passed!")
        print("=" * 60)


if __name__ == "__main__":
    test_login()
