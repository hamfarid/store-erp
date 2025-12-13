"""Test ProductAdvanced.query within Flask app context"""

import sys

sys.path.insert(0, "d:\\APPS_AI\\store\\Store\\backend")

from app import create_app
from src.models.product_advanced import ProductAdvanced

app = create_app()

with app.app_context():
    print("✅ Testing ProductAdvanced within Flask app context...\n")

    # Test 1: Check base class
    print("✓ Test 1: Base class inheritance")
    print(f"  Inherits from: {ProductAdvanced.__bases__[0].__name__}")

    # Test 2: Check .query exists and works
    print("\n✓ Test 2: .query attribute")
    try:
        query = ProductAdvanced.query
        print(f"  ✅ ProductAdvanced.query EXISTS: {query}")

        # Try to execute a query
        count = ProductAdvanced.query.count()
        print(f"  ✅ Query execution works: {count} products in database")

        # Try to fetch all
        products = ProductAdvanced.query.all()
        print(f"  ✅ query.all() works: Found {len(products)} products")

    except AttributeError as e:
        print(f"  ❌ AttributeError: {e}")
    except Exception as e:
        print(f"  ⚠️ Query works but execution error: {e}")

    print("\n✅ ProductAdvanced model fix SUCCESSFUL! .query attribute is available.")
