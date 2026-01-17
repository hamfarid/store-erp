# -*- coding: utf-8 -*-
# FILE: backend/src/database_indexes.py | PURPOSE: Database Indexes for
# Performance Optimization | OWNER: Backend | RELATED: models/ |
# LAST-AUDITED: 2025-10-21

"""
فهارس قاعدة البيانات لتحسين الأداء - الإصدار 2.0
Database Indexes for Performance Optimization - Version 2.0

P1 Fixes Applied:
- P1.1: Add indexes on frequently queried columns
- P1.2: Add composite indexes for complex queries
- P1.3: Add foreign key indexes for joins
"""

from sqlalchemy import Index
from .database import db
from .models.product_unified import Product
from .models.inventory import Category, ProductGroup, Rank, StockMovement
from .models.customer import Customer
from .models.supplier import Supplier
from .models.user import User
from .models.warehouse_unified import Warehouse


def create_performance_indexes():
    """Create database indexes for performance optimization."""

    # Product indexes
    if hasattr(Product, "name") and getattr(Product, "name", None) is not None:
        Index("idx_products_name", Product.name)
    if hasattr(Product, "sku") and getattr(Product, "sku", None) is not None:
        Index("idx_products_sku", Product.sku)
    if hasattr(Product, "barcode") and getattr(Product, "barcode", None) is not None:
        Index("idx_products_barcode", Product.barcode)
    if (
        hasattr(Product, "category_id")
        and getattr(Product, "category_id", None) is not None
    ):
        Index("idx_products_category_id", Product.category_id)
    if hasattr(Product, "is_active"):
        try:
            Index("idx_products_is_active", Product.is_active)
        except (AttributeError, TypeError):
            pass

    if hasattr(Product, "name") and hasattr(Product, "is_active"):
        try:
            Index("idx_products_name_active", Product.name, Product.is_active)
        except (AttributeError, TypeError):
            pass

    # Customer indexes
    Index("idx_customers_email", Customer.email)
    Index("idx_customers_phone", Customer.phone)
    Index("idx_customers_name", Customer.name)

    # Supplier indexes
    Index("idx_suppliers_email", Supplier.email)
    Index("idx_suppliers_phone", Supplier.phone)
    Index("idx_suppliers_name", Supplier.name)

    # User indexes
    Index("idx_users_email", User.email)
    Index("idx_users_username", User.username)

    # Stock Movement indexes
    Index("idx_stock_movements_product_id", StockMovement.product_id)
    Index("idx_stock_movements_warehouse_id", StockMovement.warehouse_id)
    Index("idx_stock_movements_date", StockMovement.movement_date)
    Index("idx_stock_movements_type", StockMovement.movement_type)
    Index(
        "idx_stock_movements_product_date",
        StockMovement.product_id,
        StockMovement.movement_date,
    )  # Composite

    # Category indexes
    Index("idx_categories_name", Category.name)

    # Warehouse indexes
    Index("idx_warehouses_name", Warehouse.name)
    Index("idx_warehouses_is_active", Warehouse.is_active)

    print("Performance indexes created successfully!")


def create_indexes_sql():
    """Generate SQL commands to create indexes manually if needed."""
    sql_commands = [
        "CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);",
        "CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);",
        "CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode);",
        "CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);",
        "CREATE INDEX IF NOT EXISTS idx_products_name_active ON products(name, is_active);",
        "CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);",
        "CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone);",
        "CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name);",
        "CREATE INDEX IF NOT EXISTS idx_suppliers_email ON suppliers(email);",
        "CREATE INDEX IF NOT EXISTS idx_suppliers_phone ON suppliers(phone);",
        "CREATE INDEX IF NOT EXISTS idx_suppliers_name ON suppliers(name);",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_product_id ON stock_movements(product_id);",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_warehouse_id ON stock_movements(warehouse_id);",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(movement_date);",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_type ON stock_movements(movement_type);",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_product_date ON stock_movements(product_id, movement_date);",
        "CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);",
        "CREATE INDEX IF NOT EXISTS idx_warehouses_name ON warehouses(name);",
        "CREATE INDEX IF NOT EXISTS idx_warehouses_is_active ON warehouses(is_active);",
    ]

    return sql_commands


if __name__ == "__main__":
    # Print SQL commands for manual execution
    print("SQL commands to create indexes:")
    for cmd in create_indexes_sql():
        print(cmd)
