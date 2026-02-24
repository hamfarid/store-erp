"""Test password verification"""

import sqlite3
import bcrypt

# Get the password hash from the database
conn = sqlite3.connect("instance/inventory.db")
cursor = conn.cursor()
cursor.execute(
    "SELECT username, password_hash FROM users WHERE username = ?", ("admin",)
)
result = cursor.fetchone()
conn.close()

if result:
    username, password_hash = result
    print(f"\n=== PASSWORD TEST ===")
    print(f"Username: {username}")
    print(f"Password hash (first 50 chars): {password_hash[:50]}...")

    # Test password verification
    test_password = "admin123"
    try:
        is_valid = bcrypt.checkpw(
            test_password.encode("utf-8"), password_hash.encode("utf-8")
        )
        print(f"Password 'admin123' is valid: {is_valid}")
    except Exception as e:
        print(f"Error checking password: {e}")
else:
    print("Admin user not found!")
