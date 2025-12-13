#!/usr/bin/env python
"""Standalone database initialization - FINAL approach"""
import os
import sys

print("=" * 60)
print("FINAL DATABASE INITIALIZATION")
print("=" * 60)

# First, rename the old database
db_dir = os.path.join(os.path.dirname(__file__), "instance")
old_db = os.path.join(db_dir, "inventory.db")
backup_db = os.path.join(db_dir, "inventory.db.backup")

print(f"\n[1/4] Backing up old database...")
if os.path.exists(old_db):
    if os.path.exists(backup_db):
        os.remove(backup_db)
    os.rename(old_db, backup_db)
    print(f"✅ Old DB backed up to: {backup_db}")
else:
    print("ℹ️  No existing database")

print("\n[2/4] Initializing application...")
try:
    # Fresh import with clean database
    from src.database import db, configure_database
    from flask import Flask

    app = Flask(__name__)
    configure_database(app)
    print("✅ Flask app initialized")

except Exception as e:
    print(f"❌ Error initializing Flask: {e}")
    sys.exit(1)

print("\n[3/4] Loading ONLY essential models...")
try:
    with app.app_context():
        # Import ONLY from the primary model files
        # Do NOT import from models/__init__.py or duplicate files
        from src.models.user import User, Role  # noqa: F401
        from src.models.customer import Customer  # noqa: F401
        from src.models.supplier import Supplier  # noqa: F401
        from src.models.sales_engineer import SalesEngineer  # noqa: F401
        from src.models.inventory import Category, Product, Warehouse  # noqa: F401
        from src.models.unified_invoice import (  # noqa: F401
            UnifiedInvoice,
            UnifiedInvoiceItem,
            InvoicePayment,
        )
        from src.models.invoice import Invoice, InvoiceItem, Payment  # noqa: F401

        # Create all tables
        db.create_all()
        print("✅ All database tables created")

        # Verify
        tables = list(db.metadata.tables.keys())
        print(f"   {len(tables)} tables registered in metadata")

        # List them
        for t in sorted(tables):
            print(f"   - {t}")

except Exception as e:
    print(f"❌ Error creating schema: {e}")
    import traceback

    traceback.print_exc()

    # Restore backup
    if os.path.exists(backup_db):
        os.remove(old_db)
        os.rename(backup_db, old_db)
        print("⚠️  Restored backup database")
    sys.exit(1)

print("\n[4/4] Verifying database file...")
if os.path.exists(old_db):
    size_kb = os.path.getsize(old_db) / 1024
    print(f"✅ Database file created: {size_kb:.1f} KB")
else:
    print("❌ Database file not found!")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ DATABASE INITIALIZATION COMPLETE!")
print("=" * 60)
print("\nNext steps:")
print("1. Run tests: pytest -xvs")
print("2. Start backend: python app.py")
print("3. Test API endpoints with Postman")
