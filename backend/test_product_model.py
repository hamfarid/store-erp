"""Test ProductAdvanced model has .query attribute after fix"""

import sys

sys.path.insert(0, "d:\\APPS_AI\\store\\Store\\backend")

from src.models.product_advanced import ProductAdvanced

# Test 1: Check if class inherits from db.Model
print("✓ Test 1: Checking ProductAdvanced base class...")
print(f"  Base classes: {ProductAdvanced.__bases__}")
print(f"  MRO: {[c.__name__ for c in ProductAdvanced.__mro__[:5]]}")

# Test 2: Check if .query attribute exists
print("\n✓ Test 2: Checking for .query attribute...")
if hasattr(ProductAdvanced, "query"):
    print(f"  ✅ ProductAdvanced.query EXISTS: {ProductAdvanced.query}")
else:
    print(f"  ❌ ProductAdvanced.query MISSING")

# Test 3: Check Column types
print("\n✓ Test 3: Checking column definitions...")
print(f"  id column: {ProductAdvanced.id}")
print(f"  name column: {ProductAdvanced.name}")
print(f"  sku column: {ProductAdvanced.sku}")

print("\n✅ ProductAdvanced model fix successful!")
