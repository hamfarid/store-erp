# FILE: backend/migrations/add_mfa_fields.py | PURPOSE: P0.1.3 - Add MFA fields to users table | OWNER: Backend Security | RELATED: models/user.py | LAST-AUDITED: 2025-10-25

"""
Database Migration: Add MFA Fields to Users Table
P0.1.3: Multi-Factor Authentication Support

This migration adds two fields to the users table:
- mfa_enabled: Boolean flag indicating if MFA is enabled for the user
- mfa_secret: TOTP secret (base32 encoded) for generating MFA codes
"""

import sys
from pathlib import Path

# Add backend/src to path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from database import db
from models.user import User


def upgrade():
    """
    Add MFA fields to users table

    This migration is idempotent - it checks if columns exist before adding them.
    """
    print("🔄 Starting MFA fields migration...")

    try:
        # Check if columns already exist
        inspector = db.inspect(db.engine)
        columns = [col["name"] for col in inspector.get_columns("users")]

        if "mfa_enabled" in columns and "mfa_secret" in columns:
            print("✅ MFA fields already exist. Skipping migration.")
            return

        # Add columns using raw SQL for SQLite compatibility
        with db.engine.connect() as conn:
            if "mfa_enabled" not in columns:
                print("  Adding mfa_enabled column...")
                conn.execute(
                    db.text(
                        "ALTER TABLE users ADD COLUMN mfa_enabled BOOLEAN DEFAULT 0"
                    )
                )
                print("  ✅ mfa_enabled column added")

            if "mfa_secret" not in columns:
                print("  Adding mfa_secret column...")
                conn.execute(
                    db.text("ALTER TABLE users ADD COLUMN mfa_secret VARCHAR(32)")
                )
                print("  ✅ mfa_secret column added")

            conn.commit()

        print("✅ MFA fields migration completed successfully")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise


def downgrade():
    """
    Remove MFA fields from users table

    WARNING: This will delete all MFA configurations for users.
    """
    print("🔄 Starting MFA fields rollback...")

    try:
        # Check if columns exist
        inspector = db.inspect(db.engine)
        columns = [col["name"] for col in inspector.get_columns("users")]

        if "mfa_enabled" not in columns and "mfa_secret" not in columns:
            print("✅ MFA fields don't exist. Skipping rollback.")
            return

        # SQLite doesn't support DROP COLUMN directly
        # We need to recreate the table without these columns
        print("⚠️  WARNING: SQLite doesn't support DROP COLUMN.")
        print("⚠️  To rollback, you need to:")
        print("    1. Export user data")
        print("    2. Drop users table")
        print("    3. Recreate without mfa_enabled and mfa_secret")
        print("    4. Re-import user data")
        print("")
        print("For PostgreSQL/MySQL, use:")
        print("  ALTER TABLE users DROP COLUMN mfa_enabled;")
        print("  ALTER TABLE users DROP COLUMN mfa_secret;")

    except Exception as e:
        print(f"❌ Rollback failed: {e}")
        raise


if __name__ == "__main__":
    """
    Run migration from command line

    Usage:
        python backend/migrations/add_mfa_fields.py upgrade
        python backend/migrations/add_mfa_fields.py downgrade
    """
    import sys
    import os
    from flask import Flask

    # Change to backend directory
    backend_path = Path(__file__).parent.parent
    os.chdir(str(backend_path))

    # Create minimal Flask app for database context
    app = Flask(__name__)

    # Use absolute path for database
    db_path = backend_path / "instance" / "inventory.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    print(f"📁 Database path: {db_path}")
    print(f"📁 Database exists: {db_path.exists()}")

    db.init_app(app)

    with app.app_context():
        if len(sys.argv) > 1 and sys.argv[1] == "downgrade":
            downgrade()
        else:
            upgrade()
