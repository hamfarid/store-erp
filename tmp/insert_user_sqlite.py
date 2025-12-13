import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join('backend', 'instance', 'inventory.db')

pwd_hash = generate_password_hash('456789+9')
now = datetime.utcnow().isoformat()

conn = sqlite3.connect(DB_PATH)
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

# Ensure roles table has a 'user' role; ignore if table or row missing
try:
    cur.execute("CREATE TABLE IF NOT EXISTS roles (id INTEGER PRIMARY KEY, name TEXT UNIQUE, display_name TEXT, description TEXT, permissions TEXT, is_active INTEGER, created_at TEXT, updated_at TEXT)")
    conn.commit()
    cur.execute("INSERT OR IGNORE INTO roles(name, display_name, description, is_active, created_at, updated_at) VALUES(?,?,?,?,?,?)", ('user', 'User', 'Normal user', 1, now, now))
    conn.commit()
    cur.execute("SELECT id FROM roles WHERE name=?", ('user',))
    row = cur.fetchone()
    role_id = row[0] if row else None
except Exception:
    role_id = None

# Create user if not exists
cur.execute("SELECT id FROM users WHERE username=?", ('gaara',))
if cur.fetchone():
    print('EXISTS')
else:
    # Attempt to insert with columns that likely exist
    # Use role_id if present; else set role='user'
    try:
        if role_id is not None:
            cur.execute("INSERT INTO users(username, email, password_hash, role_id, role, is_active, created_at, updated_at) VALUES(?,?,?,?,?,?,?,?)",
                        ('gaara', '', pwd_hash, role_id, 'user', 1, now, now))
        else:
            cur.execute("INSERT INTO users(username, email, password_hash, role, is_active, created_at, updated_at) VALUES(?,?,?,?,?,?,?)",
                        ('gaara', '', pwd_hash, 'user', 1, now, now))
        conn.commit()
        print('CREATED')
    except Exception as e:
        print('ERROR', e)
        conn.rollback()

conn.close()

