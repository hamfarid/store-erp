#!/usr/bin/env python3
"""Database initialization script - Creates tables and seeds data"""
import sqlite3
import os
from datetime import datetime

DB_PATH = "instance/inventory.db"


def init_database():
    """Initialize database with all required tables and seed data"""
    os.makedirs("instance", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=== DATABASE INITIALIZATION ===\n")

    # 1. Create audit_logs table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username VARCHAR(100),
        action VARCHAR(50) NOT NULL,
        resource_type VARCHAR(100) NOT NULL,
        resource_id INTEGER,
        resource_name VARCHAR(200),
        old_values TEXT,
        new_values TEXT,
        changed_fields TEXT,
        ip_address VARCHAR(45),
        user_agent VARCHAR(500),
        request_id VARCHAR(50),
        extra_data TEXT,
        status VARCHAR(20) DEFAULT 'success',
        error_message TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at)"
    )
    print("[OK] audit_logs table ready")

    # 2. Create role_permissions table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS role_permissions (
        role_id INTEGER NOT NULL,
        permission_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (role_id, permission_id)
    )
    """
    )
    print("[OK] role_permissions table ready")

    # 3. Create user_roles table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS user_roles (
        user_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        assigned_by INTEGER,
        PRIMARY KEY (user_id, role_id)
    )
    """
    )
    print("[OK] user_roles table ready")

    conn.commit()

    # 4. Seed roles
    cursor.execute("SELECT COUNT(*) FROM roles")
    if cursor.fetchone()[0] == 0:
        roles = [
            ("admin", "Administrator", "Full system access", 1, "مدير النظام"),
            ("user", "User", "Basic user access", 0, "مستخدم"),
            ("manager", "Manager", "Management access", 0, "مدير"),
            ("accountant", "Accountant", "Financial access", 0, "محاسب"),
            ("warehouse", "Warehouse", "Inventory access", 0, "أمين مخزن"),
        ]
        cursor.executemany(
            """
            INSERT INTO roles (code, name, description, is_system, name_ar) 
            VALUES (?, ?, ?, ?, ?)
        """,
            roles,
        )
        conn.commit()
        print("[OK] Seeded 5 roles")
    else:
        print("[SKIP] Roles already exist")

    # Get admin role id
    cursor.execute("SELECT id FROM roles WHERE code = 'admin' LIMIT 1")
    admin_role = cursor.fetchone()
    admin_role_id = admin_role[0] if admin_role else 1

    # 5. Seed admin user
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        # bcrypt hash for 'admin123'
        admin_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VLPpOGH3kS.Yay"
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, full_name, role_id, is_active, created_at)
            VALUES ('admin', 'admin@store.local', ?, 'System Administrator', ?, 1, ?)
        """,
            (admin_hash, admin_role_id, datetime.now().isoformat()),
        )
        conn.commit()
        print("[OK] Created admin user (admin/admin123)")
    else:
        print("[SKIP] Admin user already exists")

    # 6. Seed categories
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        categories = [
            ("Electronics", "Electronic devices and components"),
            ("Clothing", "Apparel and fashion accessories"),
            ("Food & Beverages", "Food items and drinks"),
            ("Office Supplies", "Office and stationery items"),
            ("Hardware", "Tools and hardware supplies"),
            ("Furniture", "Office and home furniture"),
        ]
        cursor.executemany(
            "INSERT INTO categories (name, description) VALUES (?, ?)", categories
        )
        conn.commit()
        print("[OK] Seeded 6 categories")
    else:
        print("[SKIP] Categories already exist")

    # 7. Seed warehouses
    cursor.execute("SELECT COUNT(*) FROM warehouses")
    if cursor.fetchone()[0] == 0:
        warehouses = [
            ("Main Warehouse", "WH001", "Central District, Building A", 1),
            ("Branch Store", "WH002", "North District, Mall Zone", 1),
            ("Distribution Center", "WH003", "Industrial Area, Block 5", 1),
        ]
        cursor.executemany(
            """
            INSERT INTO warehouses (name, code, address, is_active) VALUES (?, ?, ?, ?)
        """,
            warehouses,
        )
        conn.commit()
        print("[OK] Seeded 3 warehouses")
    else:
        print("[SKIP] Warehouses already exist")

    # 8. Seed permissions
    cursor.execute("SELECT COUNT(*) FROM permissions")
    if cursor.fetchone()[0] == 0:
        permissions = [
            ("products.view", "View Products", "عرض المنتجات", "products"),
            ("products.create", "Create Products", "إضافة منتجات", "products"),
            ("products.edit", "Edit Products", "تعديل المنتجات", "products"),
            ("products.delete", "Delete Products", "حذف المنتجات", "products"),
            ("invoices.view", "View Invoices", "عرض الفواتير", "invoices"),
            ("invoices.create", "Create Invoices", "إنشاء فواتير", "invoices"),
            ("invoices.edit", "Edit Invoices", "تعديل الفواتير", "invoices"),
            ("invoices.delete", "Delete Invoices", "حذف الفواتير", "invoices"),
            ("customers.view", "View Customers", "عرض العملاء", "customers"),
            ("customers.create", "Create Customers", "إضافة عملاء", "customers"),
            ("customers.edit", "Edit Customers", "تعديل العملاء", "customers"),
            ("reports.view", "View Reports", "عرض التقارير", "reports"),
            ("reports.export", "Export Reports", "تصدير التقارير", "reports"),
            ("settings.view", "View Settings", "عرض الإعدادات", "settings"),
            ("settings.edit", "Edit Settings", "تعديل الإعدادات", "settings"),
            ("users.view", "View Users", "عرض المستخدمين", "users"),
            ("users.manage", "Manage Users", "إدارة المستخدمين", "users"),
        ]
        cursor.executemany(
            """
            INSERT INTO permissions (code, name, name_ar, module) VALUES (?, ?, ?, ?)
        """,
            permissions,
        )
        conn.commit()
        print("[OK] Seeded 17 permissions")
    else:
        print("[SKIP] Permissions already exist")

    # 9. Seed sample products
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT id FROM categories LIMIT 1")
        cat = cursor.fetchone()
        cat_id = cat[0] if cat else 1

        products = [
            ("Laptop Pro 15", "SKU001", "BAR001", 2000.00, 2500.00, 50, 10, cat_id, 1),
            ("Wireless Mouse", "SKU002", "BAR002", 35.00, 45.00, 200, 20, cat_id, 1),
            ("USB-C Cable", "SKU003", "BAR003", 10.00, 15.00, 500, 50, cat_id, 1),
            ('Monitor 27"', "SKU004", "BAR004", 380.00, 450.00, 30, 5, cat_id, 1),
            (
                "Keyboard Mechanical",
                "SKU005",
                "BAR005",
                90.00,
                120.00,
                75,
                10,
                cat_id,
                1,
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO products (name, sku, barcode, cost_price, selling_price, current_stock, min_stock_level, category_id, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            products,
        )
        conn.commit()
        print("[OK] Seeded 5 sample products")
    else:
        print("[SKIP] Products already exist")

    # 10. Seed sample customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        customers = [
            (
                "CUST001",
                "Tech Solutions Ltd",
                "contact@techsolutions.com",
                "+1234567890",
                "Downtown Office Park",
                "New York",
                "USA",
                1,
            ),
            (
                "CUST002",
                "Global Imports",
                "info@globalimports.com",
                "+1234567891",
                "Trade Center, Floor 5",
                "London",
                "UK",
                1,
            ),
            (
                "CUST003",
                "Local Store",
                "manager@localstore.com",
                "+1234567892",
                "Main Street 123",
                "Cairo",
                "Egypt",
                1,
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO customers (customer_code, name, email, phone, address, city, country, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            customers,
        )
        conn.commit()
        print("[OK] Seeded 3 sample customers")
    else:
        print("[SKIP] Customers already exist")

    # 11. Seed sample suppliers
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    if cursor.fetchone()[0] == 0:
        suppliers = [
            (
                "Electronics Wholesale",
                "sales@ewholesale.com",
                "+9876543210",
                "Industrial Zone A",
                "Shenzhen",
                "China",
                "manufacturer",
                1,
            ),
            (
                "Office Pro Supply",
                "orders@officepro.com",
                "+9876543211",
                "Business District B",
                "Dubai",
                "UAE",
                "distributor",
                1,
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO suppliers (name, email, phone, address, city, country, supplier_type, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            suppliers,
        )
        conn.commit()
        print("[OK] Seeded 2 sample suppliers")
    else:
        print("[SKIP] Suppliers already exist")

    # Final status
    print("\n=== DATABASE STATUS ===")
    tables = [
        "users",
        "roles",
        "permissions",
        "categories",
        "warehouses",
        "products",
        "customers",
        "suppliers",
        "audit_logs",
    ]

    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count} rows")
        except:
            print(f"  {table}: [NOT FOUND]")

    conn.close()
    print("\n[DONE] Database initialization complete!")


if __name__ == "__main__":
    init_database()
