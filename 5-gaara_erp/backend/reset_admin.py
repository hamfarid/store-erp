#!/usr/bin/env python3
"""Reset admin user with Argon2 password hash"""

import sqlite3
from datetime import datetime
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from argon2 import PasswordHasher
    ph = PasswordHasher()
    password_hash = ph.hash('admin123')
    print("Using Argon2 password hasher")
except ImportError:
    from werkzeug.security import generate_password_hash
    password_hash = generate_password_hash('admin123')
    print("Using Werkzeug password hasher")

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'inventory.db')
print(f"DB Path: {db_path}")

if not os.path.exists(db_path):
    print("Database does not exist!")
    sys.exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Delete existing admin
cursor.execute("DELETE FROM users WHERE username = ?", ('admin',))
print("Deleted existing admin user")

# Create new admin
now = datetime.utcnow().isoformat()

cursor.execute("""
    INSERT INTO users (username, email, full_name, password_hash, role_id, is_active, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", ('admin', 'admin@store.com', 'Admin', password_hash, 1, 1, now, now))

conn.commit()
conn.close()

print("Admin user recreated successfully!")
print("Username: admin")
print("Password: admin123")
