#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check admin user in database"""

import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "instance", "inventory.db")
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Check users table
    cur.execute("SELECT id, username, email, password_hash FROM users WHERE username='admin'")
    row = cur.fetchone()
    
    if row:
        user_id, username, email, password_hash = row
        print(f"\nAdmin user found:")
        print(f"  ID: {user_id}")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print(f"  Password hash (first 50 chars): {password_hash[:50] if password_hash else 'None'}")
        print(f"  Password hash type: {'bcrypt' if password_hash.startswith('$2') else 'argon2' if password_hash.startswith('$argon2') else 'sha256 or other'}")
        
        # Test password verification
        import bcrypt
        try:
            result = bcrypt.checkpw("admin123".encode(), password_hash.encode())
            print(f"  bcrypt verify admin123: {result}")
        except Exception as e:
            print(f"  bcrypt verify failed: {e}")
    else:
        print("Admin user not found!")
    
    conn.close()
else:
    print("Database not found!")
