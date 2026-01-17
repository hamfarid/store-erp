# -*- coding: utf-8 -*-
"""
ترحيل قاعدة البيانات للمصادقة الثنائية
MFA Database Migration

إنشاء جداول MFA
Creates MFA tables
"""

MIGRATION_SQL = """
-- MFA Devices Table
CREATE TABLE IF NOT EXISTS mfa_devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) DEFAULT 'Primary Device',
    device_type VARCHAR(20) DEFAULT 'totp',
    secret VARCHAR(32) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP,
    last_used_at TIMESTAMP,
    failed_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for faster user lookups
CREATE INDEX IF NOT EXISTS idx_mfa_devices_user_id ON mfa_devices(user_id);
CREATE INDEX IF NOT EXISTS idx_mfa_devices_active ON mfa_devices(user_id, is_active, is_verified);

-- MFA Backup Codes Table
CREATE TABLE IF NOT EXISTS mfa_backup_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    code_hash VARCHAR(128) NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for faster code lookups
CREATE INDEX IF NOT EXISTS idx_mfa_backup_codes_user_id ON mfa_backup_codes(user_id);
CREATE INDEX IF NOT EXISTS idx_mfa_backup_codes_unused ON mfa_backup_codes(user_id, is_used);
"""


def run_migration(db_path: str = None):
    """
    Run MFA migration.
    
    Args:
        db_path: Path to SQLite database (optional)
    """
    import sqlite3
    import os
    
    if db_path is None:
        # Default path
        db_path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..', 'instance', 'inventory.db'
        )
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.executescript(MIGRATION_SQL)
        conn.commit()
        print("✅ MFA tables created successfully")
    except Exception as e:
        print(f"❌ Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    run_migration()
