#!/usr/bin/env python
"""Check admin user and create if not exists"""
import sqlite3
import sys

# Check if admin exists
conn = sqlite3.connect("instance/inventory.db")
cursor = conn.cursor()

# Get admin user
cursor.execute('SELECT id, username, password_hash FROM users WHERE username="admin"')
user = cursor.fetchone()

if user:
    print(f"Admin user: id={user[0]}, username={user[1]}")
    print(f'Password hash: {user[2][:80] if user[2] else "None"}...')
else:
    print("No admin user found!")

conn.close()
