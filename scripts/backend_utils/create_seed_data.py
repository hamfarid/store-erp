#!/usr/bin/env python3
"""
Seed Data Generator - Creates sample data for testing
Part of PROMPT 84: PROJECT ANALYSIS & CLEANUP
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import db
from src.models.user import User, Role
from src.models.product_unified import Product
from src.models.inventory import Category
from src.models.warehouse_unified import Warehouse
from src.models.customer import Customer
from src.models.supplier import Supplier
from app import create_app

# Sample data
CATEGORIES = [
    {"name": "إلكترونيات", "description": "أجهزة إلكترونية ومعدات"},
    {"name": "ملابس", "description": "ملابس رجالية ونسائية"},
    {"name": "أغذية", "description": "مواد غذائية ومشروبات"},
    {"name": "أثاث", "description": "أثاث منزلي ومكتبي"},
    {"name": "أدوات منزلية", "description": "أدوات ومعدات منزلية"},
]

PRODUCTS = [
    {
        "name": "لابتوب HP",
        "sku": "LAP-HP-001",
        "category": "إلكترونيات",
        "price": 15000,
        "cost": 12000,
        "stock": 25,
    },
    {
        "name": "لابتوب Dell",
        "sku": "LAP-DELL-001",
        "category": "إلكترونيات",
        "price": 18000,
        "cost": 14500,
        "stock": 15,
    },
    {
        "name": "شاشة Samsung 24 بوصة",
        "sku": "MON-SAM-24",
        "category": "إلكترونيات",
        "price": 3500,
        "cost": 2800,
        "stock": 40,
    },
    {
        "name": "لوحة مفاتيح لاسلكية",
        "sku": "KEY-WL-001",
        "category": "إلكترونيات",
        "price": 250,
        "cost": 180,
        "stock": 100,
    },
    {
        "name": "ماوس لاسلكي",
        "sku": "MOU-WL-001",
        "category": "إلكترونيات",
        "price": 150,
        "cost": 100,
        "stock": 150,
    },
    {
        "name": "قميص رجالي",
        "sku": "SHR-M-001",
        "category": "ملابس",
        "price": 200,
        "cost": 120,
        "stock": 80,
    },
    {
        "name": "بنطلون جينز",
        "sku": "PAN-JN-001",
        "category": "ملابس",
        "price": 350,
        "cost": 220,
        "stock": 60,
    },
    {
        "name": "فستان نسائي",
        "sku": "DRS-W-001",
        "category": "ملابس",
        "price": 450,
        "cost": 280,
        "stock": 45,
    },
    {
        "name": "أرز 5 كجم",
        "sku": "RIC-5KG",
        "category": "أغذية",
        "price": 80,
        "cost": 60,
        "stock": 200,
    },
    {
        "name": "زيت زيتون 1 لتر",
        "sku": "OIL-OLV-1L",
        "category": "أغذية",
        "price": 120,
        "cost": 90,
        "stock": 150,
    },
    {
        "name": "سكر 1 كجم",
        "sku": "SUG-1KG",
        "category": "أغذية",
        "price": 25,
        "cost": 18,
        "stock": 300,
    },
    {
        "name": "كرسي مكتب",
        "sku": "CHR-OFF-001",
        "category": "أثاث",
        "price": 1200,
        "cost": 850,
        "stock": 30,
    },
    {
        "name": "طاولة مكتب",
        "sku": "DSK-OFF-001",
        "category": "أثاث",
        "price": 2500,
        "cost": 1800,
        "stock": 20,
    },
    {
        "name": "خزانة ملابس",
        "sku": "WRD-CLO-001",
        "category": "أثاث",
        "price": 3500,
        "cost": 2500,
        "stock": 15,
    },
    {
        "name": "مكنسة كهربائية",
        "sku": "VAC-ELC-001",
        "category": "أدوات منزلية",
        "price": 800,
        "cost": 600,
        "stock": 35,
    },
    {
        "name": "مكواة بخار",
        "sku": "IRN-STM-001",
        "category": "أدوات منزلية",
        "price": 350,
        "cost": 250,
        "stock": 50,
    },
]

WAREHOUSES = [
    {"name": "المخزن الرئيسي", "address": "القاهرة - مدينة نصر", "code": "WH-001"},
    {"name": "مخزن الإسكندرية", "address": "الإسكندرية - سموحة", "code": "WH-002"},
    {"name": "مخزن الجيزة", "address": "الجيزة - المهندسين", "code": "WH-003"},
]

CUSTOMERS = [
    {
        "name": "شركة الأحمد للتجارة",
        "email": "ahmad@example.com",
        "phone": "01012345678",
        "address": "القاهرة",
    },
    {
        "name": "مؤسسة النور",
        "email": "nour@example.com",
        "phone": "01112345678",
        "address": "الإسكندرية",
    },
    {
        "name": "شركة الفجر",
        "email": "fajr@example.com",
        "phone": "01212345678",
        "address": "الجيزة",
    },
    {
        "name": "محمد علي",
        "email": "mali@example.com",
        "phone": "01512345678",
        "address": "القاهرة",
    },
    {
        "name": "فاطمة حسن",
        "email": "fhassan@example.com",
        "phone": "01612345678",
        "address": "الإسكندرية",
    },
]

SUPPLIERS = [
    {
        "name": "شركة التقنية المتقدمة",
        "email": "tech@example.com",
        "phone": "02012345678",
        "address": "القاهرة",
    },
    {
        "name": "مصنع النسيج الحديث",
        "email": "textile@example.com",
        "phone": "02112345678",
        "address": "المحلة",
    },
    {
        "name": "شركة الأغذية الطازجة",
        "email": "food@example.com",
        "phone": "02212345678",
        "address": "الإسكندرية",
    },
]


def create_seed_data():
    """Create all seed data"""
    app = create_app()

    with app.app_context():
        print("🌱 Creating seed data...")

        # 1. Create Categories
        print("\n📁 Creating categories...")
        category_map = {}
        for cat_data in CATEGORIES:
            category = Category.query.filter_by(name=cat_data["name"]).first()
            if not category:
                category = Category(
                    name=cat_data["name"], description=cat_data["description"]
                )
                db.session.add(category)
                print(f"  ✅ Created category: {cat_data['name']}")
            category_map[cat_data["name"]] = category

        db.session.commit()
        print(f"✅ Created {len(CATEGORIES)} categories")

        # 2. Create Warehouses
        print("\n🏭 Creating warehouses...")
        warehouse_list = []
        for wh_data in WAREHOUSES:
            warehouse = Warehouse.query.filter_by(name=wh_data["name"]).first()
            if not warehouse:
                warehouse = Warehouse(
                    name=wh_data["name"],
                    address=wh_data["address"],
                    code=wh_data["code"],
                )
                db.session.add(warehouse)
                print(f"  ✅ Created warehouse: {wh_data['name']}")
            warehouse_list.append(warehouse)

        db.session.commit()
        print(f"✅ Created {len(WAREHOUSES)} warehouses")

        # 3. Create Products
        print("\n📦 Creating products...")
        product_list = []
        for prod_data in PRODUCTS:
            product = Product.query.filter_by(sku=prod_data["sku"]).first()
            if not product:
                category = category_map.get(prod_data["category"])
                product = Product(
                    name=prod_data["name"],
                    sku=prod_data["sku"],
                    category_id=category.id if category else None,
                    sale_price=prod_data["price"],
                    cost_price=prod_data["cost"],
                    min_quantity=10,
                    max_quantity=500,
                )
                db.session.add(product)
                print(f"  ✅ Created product: {prod_data['name']}")
            product_list.append(product)

        db.session.commit()
        print(f"✅ Created {len(PRODUCTS)} products")

        # 4. Create Customers
        print("\n👥 Creating customers...")
        customer_list = []
        for cust_data in CUSTOMERS:
            customer = Customer.query.filter_by(email=cust_data["email"]).first()
            if not customer:
                customer = Customer(
                    name=cust_data["name"],
                    email=cust_data["email"],
                    phone=cust_data["phone"],
                    address=cust_data["address"],
                )
                db.session.add(customer)
                print(f"  ✅ Created customer: {cust_data['name']}")
            customer_list.append(customer)

        db.session.commit()
        print(f"✅ Created {len(CUSTOMERS)} customers")

        # 5. Create Suppliers
        print("\n🏢 Creating suppliers...")
        supplier_list = []
        for supp_data in SUPPLIERS:
            supplier = Supplier.query.filter_by(email=supp_data["email"]).first()
            if not supplier:
                supplier = Supplier(
                    name=supp_data["name"],
                    email=supp_data["email"],
                    phone=supp_data["phone"],
                    address=supp_data["address"],
                )
                db.session.add(supplier)
                print(f"  ✅ Created supplier: {supp_data['name']}")
            supplier_list.append(supplier)

        db.session.commit()
        print(f"✅ Created {len(SUPPLIERS)} suppliers")

        print("\n" + "=" * 60)
        print("🎉 SEED DATA CREATION COMPLETE!")
        print("=" * 60)
        print(f"✅ Categories: {len(CATEGORIES)}")
        print(f"✅ Warehouses: {len(WAREHOUSES)}")
        print(f"✅ Products: {len(PRODUCTS)}")
        print(f"✅ Customers: {len(CUSTOMERS)}")
        print(f"✅ Suppliers: {len(SUPPLIERS)}")
        print("=" * 60)


if __name__ == "__main__":
    create_seed_data()
