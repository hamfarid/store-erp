#!/usr/bin/env python
"""Reset the database by dropping all tables and recreating"""
import os
import sys

print("=" * 60)
print("DATABASE RESET SCRIPT")
print("=" * 60)

try:
    from src.database import db, configure_database
    from flask import Flask

    # Create Flask app
    app = Flask(__name__)
    configure_database(app)

    with app.app_context():
        print("\n[0/5] Loading all models...")
        # Import all models BEFORE create_all() so they register with db
        from src.models.user import User, Role, UserSession, UserActivity
        from src.models.sales_engineer import SalesEngineer
        from src.models.customer import Customer
        from src.models.supplier import Supplier
        from src.models.inventory import Category, Product, Warehouse
        from src.models.enhanced_models import Inventory
        from src.models.unified_invoice import (
            UnifiedInvoice,
            UnifiedInvoiceItem,
            InvoicePayment,
        )

        try:
            from src.models.sales_advanced import (
                SalesInvoice,
                SalesInvoiceItem,
                CustomerPayment,
            )
        except ImportError:
            print("⚠️ Sales advanced models not available")

        print(f"✅ Models loaded: {len(db.metadata.tables)} tables")

        print("\n[1/5] Dropping all existing tables...")
        db.drop_all()
        print("✅ All tables dropped")

        print("\n[2/5] Creating fresh tables...")
        db.create_all()
        print("✅ All tables created")

        print("\n[3/5] Verifying table creation...")
        tables = list(db.metadata.tables.keys())
        print(f"✅ Created {len(tables)} tables:")
        for table in sorted(tables):
            print(f"   - {table}")

        print("\n[4/5] Checking database file...")
        db_path = os.path.join(os.path.dirname(__file__), "instance", "inventory.db")
        if os.path.exists(db_path):
            size_kb = os.path.getsize(db_path) / 1024
            print(f"✅ Database file created: {size_kb:.1f} KB")
        else:
            print(f"❌ Database file not found: {db_path}")
            sys.exit(1)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ DATABASE RESET COMPLETE - READY FOR TESTING")
print("=" * 60)
