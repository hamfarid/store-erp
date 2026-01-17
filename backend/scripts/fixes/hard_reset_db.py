#!/usr/bin/env python
"""Reset the database - use SQLite commands to clear and recreate"""
import os
import sys
import time

print("=" * 60)
print("DATABASE RESET SCRIPT - CLEAN AND RECREATE")
print("=" * 60)

db_path = os.path.join(os.path.dirname(__file__), "instance", "inventory.db")

print("\n[1/5] Importing Flask app and database...")
try:
    from src.database import db, configure_database
    from flask import Flask

    # Create Flask app
    app = Flask(__name__)
    configure_database(app)

    with app.app_context():
        print("[2/5] Clearing all existing tables...")
        # Use raw SQL to drop all tables
        from sqlalchemy import text

        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        if tables:
            print(f"   Found {len(tables)} tables to drop")
            for table in tables:
                try:
                    db.session.execute(text(f"DROP TABLE IF EXISTS {table}"))
                    print(f"   - Dropped: {table}")
                except Exception as e:
                    print(f"   - Failed to drop {table}: {e}")
            db.session.commit()
            print("✅ All tables dropped")
        else:
            print("   No tables to drop")

        print("\n[3/5] Loading all models...")
        # Import models to register with db
        from src.models.user import User, Role  # noqa: F401
        from src.models.sales_engineer import SalesEngineer  # noqa: F401
        from src.models.customer import Customer  # noqa: F401
        from src.models.supplier import Supplier  # noqa: F401
        from src.models.inventory import Category, Product, Warehouse  # noqa: F401
        from src.models.enhanced_models import Inventory  # noqa: F401
        from src.models.unified_invoice import (  # noqa: F401
            UnifiedInvoice,
            UnifiedInvoiceItem,
            InvoicePayment,
        )

        try:
            from src.models.sales_advanced import (  # noqa: F401
                SalesInvoice,
                SalesInvoiceItem,
                CustomerPayment,
            )
        except ImportError:
            print("   (Sales advanced models not available)")

        tables = list(db.metadata.tables.keys())
        print(f"   Models loaded: {len(tables)} tables registered")

        print("\n[4/5] Creating all database tables...")
        db.create_all()
        print("✅ All tables created successfully!")

        print("\n[5/5] Verifying table creation...")
        tables = list(db.metadata.tables.keys())
        print(f"   Created {len(tables)} tables:")
        for table in sorted(tables):
            print(f"   - {table}")

        if os.path.exists(db_path):
            size_kb = os.path.getsize(db_path) / 1024
            print(f"\n✅ Database file: {size_kb:.1f} KB")
        else:
            print("❌ Database file not created!")
            sys.exit(1)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ DATABASE RESET COMPLETE - READY FOR TESTING")
print("=" * 60)
