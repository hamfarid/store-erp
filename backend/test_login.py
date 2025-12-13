#!/usr/bin/env python
"""Test login functionality"""
import sqlite3
import sys

# Add src to path
sys.path.insert(0, ".")

# Check if bcrypt is available
try:
    import bcrypt

    print(
        f'bcrypt version: {bcrypt.__about__.__version__ if hasattr(bcrypt, "__about__") else "available"}'
    )
except ImportError:
    print("bcrypt NOT available")
    sys.exit(1)

# Get admin user password hash
conn = sqlite3.connect("instance/inventory.db")
cursor = conn.cursor()
cursor.execute('SELECT id, username, password_hash FROM users WHERE username="admin"')
user = cursor.fetchone()
conn.close()

if not user:
    print("No admin user found!")
    sys.exit(1)

user_id, username, password_hash = user
print(f"Admin user: {username}")
print(f"Password hash: {password_hash}")

# Test password verification
password_to_test = "admin123"
print(f"\nTesting password: {password_to_test}")

try:
    result = bcrypt.checkpw(
        password_to_test.encode("utf-8"), password_hash.encode("utf-8")
    )
    print(f"Password verification result: {result}")
except Exception as e:
    print(f"Password verification error: {e}")
