#!/usr/bin/env python3
"""
إنشاء بيانات تجريبية للاختبار
Create seed data for testing
"""

import sys
import os

# إضافة المسار الجذري للمشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from src.database import db
from src.models.inventory import Category, Product, Warehouse
from src.models.customer import Customer
from src.models.supplier import Supplier
from datetime import datetime, timezone
from decimal import Decimal


def clear_database():
    """مسح البيانات الموجودة"""
    print("🗑️  Clearing existing data...")
    try:
        Product.query.delete()
        Category.query.filter(Category.id > 4).delete()  # Keep default categories
        Warehouse.query.filter(Warehouse.id > 3).delete()  # Keep default warehouses
        Customer.query.delete()
        Supplier.query.delete()
        db.session.commit()
        print("✅ Database cleared")
    except Exception as e:
        db.session.rollback()
        print(f"⚠️  Error clearing database: {e}")


def seed_categories():
    """إنشاء تصنيفات إضافية"""
    print("\n📁 Creating additional categories...")

    categories_data = [
        {
            "name": "بذور هجينة",
            "description": "بذور محسنة عالية الإنتاجية",
            "parent_id": 1,
        },
        {
            "name": "أسمدة عضوية",
            "description": "أسمدة طبيعية صديقة للبيئة",
            "parent_id": 3,
        },
        {
            "name": "أسمدة كيماوية",
            "description": "أسمدة صناعية سريعة المفعول",
            "parent_id": 3,
        },
        {"name": "مبيدات حشرية", "description": "مبيدات للحشرات", "parent_id": 4},
        {
            "name": "مبيدات فطرية",
            "description": "مبيدات للأمراض الفطرية",
            "parent_id": 4,
        },
    ]

    for cat_data in categories_data:
        try:
            category = Category(**cat_data)
            db.session.add(category)
            print(f"  ✓ {cat_data['name']}")
        except Exception as e:
            print(f"  ✗ Error with {cat_data['name']}: {e}")

    db.session.commit()
    print("✅ Categories created")


def seed_products():
    """إنشاء منتجات تجريبية"""
    print("\n📦 Creating products...")

    products_data = [
        # بذور
        {
            "name": "بذور طماطم هجين - سوبر ستار",
            "barcode": "8901234567801",
            "sku": "TOM-HYB-001",
            "category_id": 5,  # بذور هجينة
            "selling_price": Decimal("35.00"),
            "cost_price": Decimal("25.00"),
            "current_stock": 150,
            "min_stock_level": 20,
            "description": "بذور طماطم هجينة عالية الإنتاجية، مقاومة للأمراض",
        },
        {
            "name": "بذور خيار هولندي - جرين ماستر",
            "barcode": "8901234567802",
            "sku": "CUC-HYB-002",
            "category_id": 5,
            "selling_price": Decimal("42.00"),
            "cost_price": Decimal("30.00"),
            "current_stock": 100,
            "min_stock_level": 15,
            "description": "بذور خيار هجينة للزراعة المحمية",
        },
        {
            "name": "بذور فلفل حلو - سويت بيل",
            "barcode": "8901234567803",
            "sku": "PEP-HYB-003",
            "category_id": 5,
            "selling_price": Decimal("38.00"),
            "cost_price": Decimal("28.00"),
            "current_stock": 80,
            "min_stock_level": 10,
            "description": "بذور فلفل حلو ملون عالي الجودة",
        },
        # أسمدة عضوية
        {
            "name": "سماد عضوي كومبوست - 25 كجم",
            "barcode": "8901234567804",
            "sku": "FERT-ORG-001",
            "category_id": 6,
            "selling_price": Decimal("45.00"),
            "cost_price": Decimal("32.00"),
            "current_stock": 200,
            "min_stock_level": 30,
            "description": "سماد عضوي متخمر غني بالمواد العضوية",
        },
        {
            "name": "سماد دودة الأرض (Vermicompost) - 10 كجم",
            "barcode": "8901234567805",
            "sku": "FERT-ORG-002",
            "category_id": 6,
            "selling_price": Decimal("65.00"),
            "cost_price": Decimal("45.00"),
            "current_stock": 120,
            "min_stock_level": 20,
            "description": "سماد عضوي عالي الجودة من مخلفات الدود",
        },
        # أسمدة كيماوية
        {
            "name": "سماد NPK متوازن 20-20-20 - 50 كجم",
            "barcode": "8901234567806",
            "sku": "FERT-NPK-001",
            "category_id": 7,
            "selling_price": Decimal("180.00"),
            "cost_price": Decimal("140.00"),
            "current_stock": 75,
            "min_stock_level": 10,
            "description": "سماد مركب متوازن للاستخدام العام",
        },
        {
            "name": "سماد يوريا 46% نيتروجين - 50 كجم",
            "barcode": "8901234567807",
            "sku": "FERT-URE-002",
            "category_id": 7,
            "selling_price": Decimal("120.00"),
            "cost_price": Decimal("95.00"),
            "current_stock": 150,
            "min_stock_level": 20,
            "description": "سماد نيتروجيني عالي التركيز",
        },
        {
            "name": "سماد سوبر فوسفات 45% - 50 كجم",
            "barcode": "8901234567808",
            "sku": "FERT-PHO-003",
            "category_id": 7,
            "selling_price": Decimal("95.00"),
            "cost_price": Decimal("75.00"),
            "current_stock": 100,
            "min_stock_level": 15,
            "description": "سماد فوسفاتي لتقوية الجذور",
        },
        # مبيدات
        {
            "name": "مبيد حشري طبيعي - نيم أويل 1 لتر",
            "barcode": "8901234567809",
            "sku": "PEST-NAT-001",
            "category_id": 8,
            "selling_price": Decimal("85.00"),
            "cost_price": Decimal("60.00"),
            "current_stock": 60,
            "min_stock_level": 10,
            "description": "مبيد حشري طبيعي آمن من زيت النيم",
        },
        {
            "name": "مبيد فطري - كوبروكسات 500 مل",
            "barcode": "8901234567810",
            "sku": "FUNG-COP-001",
            "category_id": 9,
            "selling_price": Decimal("95.00"),
            "cost_price": Decimal("70.00"),
            "current_stock": 80,
            "min_stock_level": 12,
            "description": "مبيد فطري نحاسي واسع الطيف",
        },
    ]

    for prod_data in products_data:
        try:
            product = Product(**prod_data)
            db.session.add(product)
            print(f"  ✓ {prod_data['name']}")
        except Exception as e:
            print(f"  ✗ Error with {prod_data['name']}: {e}")

    db.session.commit()
    print("✅ Products created")


def seed_customers():
    """إنشاء عملاء تجريبيين"""
    print("\n👥 Creating customers...")

    customers_data = [
        {
            "name": "مزرعة النخيل الأخضر",
            "email": "info@greenpalm.com",
            "phone": "0501234567",
            "address": "الرياض - حي الياسمين",
            "tax_number": "300123456789001",
            "credit_limit": Decimal("50000.00"),
        },
        {
            "name": "مؤسسة الزراعة الحديثة",
            "email": "contact@modernagri.com",
            "phone": "0509876543",
            "address": "جدة - حي الروضة",
            "tax_number": "300123456789002",
            "credit_limit": Decimal("75000.00"),
        },
        {
            "name": "شركة المحاصيل المتقدمة",
            "email": "sales@advcrops.com",
            "phone": "0551234567",
            "address": "الدمام - حي الفيصلية",
            "tax_number": "300123456789003",
            "credit_limit": Decimal("100000.00"),
        },
    ]

    for cust_data in customers_data:
        try:
            customer = Customer(**cust_data)
            db.session.add(customer)
            print(f"  ✓ {cust_data['name']}")
        except Exception as e:
            print(f"  ✗ Error with {cust_data['name']}: {e}")

    db.session.commit()
    print("✅ Customers created")


def seed_suppliers():
    """إنشاء موردين تجريبيين"""
    print("\n🏢 Creating suppliers...")

    suppliers_data = [
        {
            "name": "شركة البذور العالمية",
            "email": "orders@globalseeds.com",
            "phone": "0112345678",
            "address": "الرياض - طريق الملك فهد",
            "tax_number": "300987654321001",
            "payment_terms": "net_30",
        },
        {
            "name": "مصنع الأسمدة الوطنية",
            "email": "sales@nationalfert.com",
            "phone": "0123456789",
            "address": "الجبيل - المنطقة الصناعية",
            "tax_number": "300987654321002",
            "payment_terms": "net_45",
        },
        {
            "name": "مستورد المبيدات الزراعية",
            "email": "info@agripest.com",
            "phone": "0555555555",
            "address": "جدة - حي الزهراء",
            "tax_number": "300987654321003",
            "payment_terms": "net_30",
        },
    ]

    for supp_data in suppliers_data:
        try:
            supplier = Supplier(**supp_data)
            db.session.add(supplier)
            print(f"  ✓ {supp_data['name']}")
        except Exception as e:
            print(f"  ✗ Error with {supp_data['name']}: {e}")

    db.session.commit()
    print("✅ Suppliers created")


def main():
    """البرنامج الرئيسي"""
    print("=" * 60)
    print("🌱 Inventory Management System - Seed Database")
    print("=" * 60)

    app = create_app()

    with app.app_context():
        try:
            # مسح البيانات القديمة (اختياري)
            response = input("\n⚠️  Clear existing data? (y/N): ").strip().lower()
            if response == "y":
                clear_database()

            # إنشاء البيانات التجريبية
            seed_categories()
            seed_products()
            seed_customers()
            seed_suppliers()

            print("\n" + "=" * 60)
            print("✅ Seed data created successfully!")
            print("=" * 60)

            # عرض الإحصائيات
            print("\n📊 Database Statistics:")
            print(f"  Categories: {Category.query.count()}")
            print(f"  Products: {Product.query.count()}")
            print(f"  Warehouses: {Warehouse.query.count()}")
            print(f"  Customers: {Customer.query.count()}")
            print(f"  Suppliers: {Supplier.query.count()}")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            traceback.print_exc()
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
