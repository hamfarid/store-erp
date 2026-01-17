#!/usr/bin/env python3
"""
Ensure all required database tables exist
"""

import sys
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))


def ensure_all_tables():
    """Ensure all required tables exist"""
    try:
        from app import create_app

        app = create_app()

        with app.app_context():
            from database import db

            # Import all models to ensure they are registered
            from models import (
                User,
                Role,
                Customer,
                Product,
                Category,
                Warehouse,
                UnifiedInvoice,
                UnifiedInvoiceItem,
                InvoicePayment,
                SalesInvoice,
                SalesInvoiceItem,
                CustomerPayment,
            )

            # Create all tables
            db.create_all()

            # List created tables
            tables = list(db.metadata.tables.keys())
            print(f"✅ Ensured {len(tables)} tables exist:")
            for table in sorted(tables):
                print(f"  - {table}")

            return True

    except Exception as e:
        print(f"❌ Error ensuring tables: {e}")
        return False


if __name__ == "__main__":
    success = ensure_all_tables()
    sys.exit(0 if success else 1)
