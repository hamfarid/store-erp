#!/usr/bin/env python3
"""
Comprehensive Model Registration Test
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))


def test_model_registration():
    """Test model registration and relationships"""
    print("🧪 Testing model registration...")

    try:
        # Test Flask app creation
        from app import create_app

        app = create_app()
        print("✅ Flask app created successfully")

        with app.app_context():
            # Test database initialization
            from database import db

            print("✅ Database imported successfully")

            # Test basic model imports
            from models import User, Role, Customer, Product, Category, Warehouse

            print("✅ Basic models imported successfully")

            # Test advanced model imports
            from models import UnifiedInvoice, UnifiedInvoiceItem, InvoicePayment

            print("✅ Advanced models imported successfully")

            # Test sales models
            from models import SalesInvoice, SalesInvoiceItem, CustomerPayment

            print("✅ Sales models imported successfully")

            # Test database table creation
            db.create_all()
            print("✅ Database tables created successfully")

            # List all tables
            print("📊 Available tables:")
            for table_name in db.metadata.tables.keys():
                print(f"  - {table_name}")

            # Test model instantiation
            if User:
                user = User(
                    username="test",
                    email="test@example.com",
                    full_name="Test User",
                    role_id=1,
                )
                print("✅ User model instantiation successful")

            if Customer:
                customer = Customer(name="Test Customer", email="customer@example.com")
                print("✅ Customer model instantiation successful")

            if Product:
                product = Product(name="Test Product", selling_price=100.0)
                print("✅ Product model instantiation successful")

            print("🎉 All tests passed successfully!")
            return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_model_registration()
    sys.exit(0 if success else 1)
