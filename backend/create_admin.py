#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create admin user directly in the database
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

# Database path
db_path = os.path.join(os.path.dirname(__file__), "instance", "inventory.db")


# Create admin user
def create_admin():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if admin exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if cursor.fetchone():
        print("✅ Admin user already exists")
        conn.close()
        return

    # Create admin user
    password_hash = generate_password_hash("admin123")
    now = datetime.utcnow().isoformat()

    cursor.execute(
        """
        INSERT INTO users (username, email, full_name, password_hash, role, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            "admin",
            "admin@store.com",
            "مدير النظام",
            password_hash,
            "admin",
            1,
            now,
            now,
        ),
    )

    conn.commit()
    conn.close()

    print("✅ Admin user created successfully!")
    print("   Username: admin")
    print("   Password: admin123")


if __name__ == "__main__":
    create_admin()
