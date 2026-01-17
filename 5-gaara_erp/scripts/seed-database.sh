#!/bin/bash
# =============================================================================
# Gaara ERP - Database Seeding Script
# =============================================================================
# Populates database with initial data for development/testing
# =============================================================================

set -euo pipefail

echo "=========================================="
echo "Gaara ERP - Database Seeding"
echo "=========================================="

# Check if running in Docker
if [ -f "/.dockerenv" ]; then
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

echo ""
echo "Creating initial data..."

# Seed data using Django management command
$PYTHON_CMD manage.py shell << EOF
from django.contrib.auth import get_user_model
from core_modules.organization.models import Company
from business_modules.inventory.models import Category, Warehouse
from business_modules.contacts.models import Customer

User = get_user_model()

# Create default company if not exists
company, created = Company.objects.get_or_create(
    code="GAARA",
    defaults={
        "name": "Gaara ERP",
        "is_active": True
    }
)
if created:
    print("✓ Default company created")
else:
    print("✓ Company already exists")

# Create default categories
categories = [
    {"name": "بذور", "code": "SEEDS"},
    {"name": "أسمدة", "code": "FERTILIZERS"},
    {"name": "مبيدات", "code": "PESTICIDES"},
    {"name": "أدوات", "code": "TOOLS"},
]

for cat_data in categories:
    cat, created = Category.objects.get_or_create(
        code=cat_data["code"],
        defaults={"name": cat_data["name"]}
    )
    if created:
        print(f"✓ Category created: {cat_data['name']}")

# Create default warehouse
warehouse, created = Warehouse.objects.get_or_create(
    code="MAIN",
    defaults={
        "name": "مخزن الرئيسي",
        "is_active": True
    }
)
if created:
    print("✓ Default warehouse created")
else:
    print("✓ Warehouse already exists")

# Create test customer
customer, created = Customer.objects.get_or_create(
    email="test@example.com",
    defaults={
        "name": "عميل تجريبي",
        "phone": "+966501234567",
        "is_active": True
    }
)
if created:
    print("✓ Test customer created")
else:
    print("✓ Test customer already exists")

print("")
print("✓ Database seeding completed!")
EOF

echo ""
echo "=========================================="
