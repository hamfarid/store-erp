#!/usr/bin/env python
"""Nuclear option: Direct SQLite cleanup"""
import os
import sys
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), "instance", "inventory.db")

print("=" * 60)
print("DATABASE - DIRECT SQLite CLEANUP")
print("=" * 60)
print(f"\nTarget database: {db_path}")

if not os.path.exists(db_path):
    print("Database doesn't exist, creating fresh...")
else:
    print(f"Database exists ({os.path.getsize(db_path)} bytes)")
    print("\nConnecting to database...")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Disable foreign keys during cleanup
        cursor.execute("PRAGMA foreign_keys=OFF")

        print("Getting list of tables...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Found {len(tables)} tables")

        print("\nDropping all tables...")
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"  Dropped: {table}")
            except Exception as e:
                print(f"  Warning: Could not drop {table}: {e}")

        # Get all indexes and drop them
        print("\nGetting list of indexes...")
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' "
            "AND name NOT LIKE 'sqlite_autoindex_%'"
        )
        indexes = [row[0] for row in cursor.fetchall()]
        print(f"Found {len(indexes)} indexes")

        print("\nDropping all indexes...")
        for index in indexes:
            try:
                cursor.execute(f"DROP INDEX IF EXISTS {index}")
                print(f"  Dropped: {index}")
            except Exception as e:
                print(f"  Warning: Could not drop {index}: {e}")

        conn.commit()
        conn.close()
        print("\n✅ Database cleaned successfully")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

print("\n" + "=" * 60)
print("✅ DATABASE CLEANUP COMPLETE")
print("=" * 60)
