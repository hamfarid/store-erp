#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct Admin User Creation Script
Creates admin user by directly accessing the database without loading all routes.

NOTE: This script uses raw SQL to avoid SQLAlchemy mapper conflicts with the main app.
"""

import sys
import os
import sqlite3
import hashlib

# Get the correct database path
db_path = os.path.join(os.path.dirname(__file__), "instance", "inventory.db")
db_dir = os.path.dirname(db_path)

# Create instance directory if it doesn't exist
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    print(f"Created directory: {db_dir}")

print(f"Database path: {db_path}")


def hash_password(password):
    """Hash password using bcrypt"""
    try:
        import bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    except ImportError:
        # Fallback to SHA-256 if bcrypt not available
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


def check_password(password, password_hash):
    """Check password against hash"""
    try:
        import bcrypt
        if password_hash.startswith("$2"):
            return bcrypt.checkpw(password.encode(), password_hash.encode())
    except ImportError:
        pass
    # Fallback to SHA-256
    return hashlib.sha256(password.encode("utf-8")).hexdigest() == password_hash


def create_admin():
    """Create admin user using raw SQL"""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Check if admin exists
        cur.execute("SELECT id, username, email, password_hash FROM users WHERE username='admin'")
        existing = cur.fetchone()
        
        if existing:
            print("Admin user already exists!")
            print(f"   ID: {existing[0]}")
            print(f"   Username: {existing[1]}")
            print(f"   Email: {existing[2]}")
            
            # Test password
            if check_password("admin123", existing[3]):
                print("Password 'admin123' is correct!")
            else:
                print("Password 'admin123' does not match. Updating...")
                new_hash = hash_password("admin123")
                cur.execute("UPDATE users SET password_hash = ? WHERE username = 'admin'", (new_hash,))
                conn.commit()
                print("Password updated to 'admin123'")
            
            conn.close()
            return True
        
        # Check if admin role exists
        cur.execute("SELECT id FROM roles WHERE name='admin'")
        role = cur.fetchone()
        
        if not role:
            cur.execute("""
                INSERT INTO roles (code, name, name_ar, description, is_active) 
                VALUES ('admin', 'admin', 'مدير النظام', 'System Administrator', 1)
            """)
            conn.commit()
            cur.execute("SELECT id FROM roles WHERE name='admin'")
            role = cur.fetchone()
            print("Created admin role")
        
        role_id = role[0]
        
        # Create admin user
        password_hash = hash_password("admin123")
        cur.execute("""
            INSERT INTO users (username, email, full_name, password_hash, role_id, is_active)
            VALUES ('admin', 'admin@inventory.com', 'System Administrator', ?, ?, 1)
        """, (password_hash, role_id))
        conn.commit()
        
        print("Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        
        # Verify password works
        cur.execute("SELECT password_hash FROM users WHERE username='admin'")
        stored_hash = cur.fetchone()[0]
        if check_password("admin123", stored_hash):
            print("Password verification successful!")
        else:
            print("Password verification failed!")
        
        conn.close()
        return True
        
    except Exception as exc:
        print(f"Error: {exc}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Creating Admin User")
    print("=" * 60)

    success = create_admin()

    if success:
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nFrontend: http://localhost:5505")
        print("Backend: http://127.0.0.1:5506")
        print("=" * 60)
    else:
        print("\nFailed to create admin user")
        sys.exit(1)
