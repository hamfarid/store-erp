# FILE: backend/scripts/migrate_password_hashes.py | PURPOSE: Migrate existing password hashes to Argon2id | OWNER: security | RELATED: backend/src/password_hasher.py | LAST-AUDITED: 2025-11-04

"""
Password Hash Migration Script
Migrates existing bcrypt/SHA-256 password hashes to Argon2id

IMPORTANT: This script requires users to log in to trigger rehashing.
It does NOT directly rehash passwords (impossible without plaintext).

Instead, it:
1. Identifies users with legacy password hashes
2. Flags them for rehashing on next login
3. Provides migration statistics
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

try:
    from password_hasher import needs_rehash, get_algorithm, ARGON2_AVAILABLE
    from models.user import db, User
    from flask import Flask
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the backend directory")
    sys.exit(1)


def create_app():
    """Create Flask app for database access"""
    app = Flask(__name__)

    # Database configuration
    instance_dir = Path(__file__).resolve().parents[2] / "instance"
    instance_dir.mkdir(exist_ok=True)
    db_path = instance_dir / "inventory.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    return app


def analyze_password_hashes():
    """
    Analyze existing password hashes and identify migration needs

    Returns:
        dict: Statistics about password hashes
    """
    app = create_app()

    with app.app_context():
        users = User.query.all()

        stats = {
            "total_users": len(users),
            "argon2id": 0,
            "bcrypt": 0,
            "sha256": 0,
            "unknown": 0,
            "needs_rehash": 0,
            "users_needing_rehash": [],
        }

        for user in users:
            if not user.password_hash:
                stats["unknown"] += 1
                continue

            # Identify hash type
            if user.password_hash.startswith("$argon2"):
                stats["argon2id"] += 1
                # Check if parameters are outdated
                if needs_rehash(user.password_hash):
                    stats["needs_rehash"] += 1
                    stats["users_needing_rehash"].append(
                        {
                            "id": user.id,
                            "username": user.username,
                            "reason": "Outdated Argon2id parameters",
                        }
                    )
            elif user.password_hash.startswith("$2"):  # bcrypt
                stats["bcrypt"] += 1
                stats["needs_rehash"] += 1
                stats["users_needing_rehash"].append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "reason": "Legacy bcrypt hash",
                    }
                )
            elif len(user.password_hash) == 64:  # SHA-256
                stats["sha256"] += 1
                stats["needs_rehash"] += 1
                stats["users_needing_rehash"].append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "reason": "INSECURE SHA-256 hash",
                    }
                )
            else:
                stats["unknown"] += 1

        return stats


def print_migration_report(stats):
    """Print migration report"""
    print("=" * 70)
    print("PASSWORD HASH MIGRATION REPORT")
    print("=" * 70)
    print()

    print(f"Current hashing algorithm: {get_algorithm()}")
    print(f"Argon2id available: {'✅ Yes' if ARGON2_AVAILABLE else '❌ No'}")
    print()

    print("HASH TYPE DISTRIBUTION:")
    print(f"  Total users: {stats['total_users']}")
    print(f"  ✅ Argon2id (current): {stats['argon2id']}")
    print(f"  ⚠️  bcrypt (legacy): {stats['bcrypt']}")
    print(f"  ❌ SHA-256 (INSECURE): {stats['sha256']}")
    print(f"  ❓ Unknown: {stats['unknown']}")
    print()

    print(f"MIGRATION NEEDED: {stats['needs_rehash']} users")
    print()

    if stats["users_needing_rehash"]:
        print("USERS REQUIRING REHASH:")
        for user in stats["users_needing_rehash"]:
            print(f"  - User #{user['id']} ({user['username']}): {user['reason']}")
        print()

    print("=" * 70)
    print("MIGRATION INSTRUCTIONS:")
    print("=" * 70)
    print()
    print("Password hashes CANNOT be migrated directly (no plaintext available).")
    print("Instead, hashes will be upgraded automatically on next user login.")
    print()
    print("AUTOMATIC REHASHING:")
    print("  1. User logs in with correct password")
    print("  2. System verifies password against legacy hash")
    print("  3. System detects legacy hash and rehashes with Argon2id")
    print("  4. New Argon2id hash replaces legacy hash in database")
    print()
    print("MANUAL MIGRATION OPTIONS:")
    print("  1. Force password reset for all users (sends reset emails)")
    print("  2. Notify users to log in within 30 days")
    print("  3. Expire legacy hashes after grace period")
    print()
    print("=" * 70)


def main():
    """Main migration analysis"""
    print("Analyzing password hashes...")
    print()

    try:
        stats = analyze_password_hashes()
        print_migration_report(stats)

        # Exit code based on migration needs
        if stats["sha256"] > 0:
            print("⚠️  WARNING: INSECURE SHA-256 hashes detected!")
            print("   Action required: Force password reset for affected users")
            return 2
        elif stats["needs_rehash"] > 0:
            print("ℹ️  INFO: Legacy hashes detected")
            print("   Hashes will be upgraded on next user login")
            return 1
        else:
            print("✅ All password hashes are up to date")
            return 0

    except Exception as e:
        print(f"❌ Migration analysis failed: {e}")
        import traceback

        traceback.print_exc()
        return 3


if __name__ == "__main__":
    sys.exit(main())
