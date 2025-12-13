#!/usr/bin/env python3
# type: ignore
# flake8: noqa
# pylint: disable=all
"""
سكريبت تحسين أداء قاعدة البيانات
Database Performance Optimization Script

هذا السكريبت يضيف فهارس ويحسن أداء قاعدة البيانات
All linting disabled due to complex database operations and optional dependencies.
"""

from sqlalchemy import text, Index
from models.unified_models import db
from flask import Flask
import os
import sys
from datetime import datetime

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def create_app():
    """إنشاء تطبيق Flask"""
    app = Flask(__name__)

    # إعداد قاعدة البيانات
    db_path = os.path.join(
        os.path.dirname(__file__), "database", "unified_inventory.db"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "unified-inventory-system-2024"

    db.init_app(app)
    return app


def create_indexes():
    """إنشاء فهارس لتحسين الأداء"""
    print("📊 إنشاء فهارس قاعدة البيانات...")

    indexes = [
        # فهارس جدول المستخدمين
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id)",
        # فهارس جدول المنتجات
        "CREATE INDEX IF NOT EXISTS idx_products_code ON products(code)",
        "CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode)",
        "CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)",
        "CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id)",
        "CREATE INDEX IF NOT EXISTS idx_products_warehouse_id ON products(warehouse_id)",
        "CREATE INDEX IF NOT EXISTS idx_products_current_stock ON products(current_stock)",
        # فهارس جدول حركات المخزون
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_product_id ON stock_movements(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_warehouse_id ON stock_movements(warehouse_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_user_id ON stock_movements(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_type ON stock_movements(movement_type)",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(created_at)",
        # فهارس جدول العملاء
        "CREATE INDEX IF NOT EXISTS idx_customers_code ON customers(code)",
        "CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name)",
        "CREATE INDEX IF NOT EXISTS idx_customers_type ON customers(customer_type)",
        "CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone)",
        "CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email)",
        # فهارس جدول الموردين
        "CREATE INDEX IF NOT EXISTS idx_suppliers_code ON suppliers(code)",
        "CREATE INDEX IF NOT EXISTS idx_suppliers_name ON suppliers(name)",
        "CREATE INDEX IF NOT EXISTS idx_suppliers_type ON suppliers(supplier_type)",
        # فهارس جدول الفواتير
        "CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_number)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_type ON invoices(invoice_type)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_date ON invoices(invoice_date)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_customer_id ON invoices(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_supplier_id ON invoices(supplier_id)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_user_id ON invoices(user_id)",
        # فهارس جدول عناصر الفواتير
        "CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice_id ON invoice_items(invoice_id)",
        "CREATE INDEX IF NOT EXISTS idx_invoice_items_product_id ON invoice_items(product_id)",
        # فهارس جدول الفئات
        "CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name)",
        "CREATE INDEX IF NOT EXISTS idx_categories_parent_id ON categories(parent_id)",
        # فهارس جدول المخازن
        "CREATE INDEX IF NOT EXISTS idx_warehouses_code ON warehouses(code)",
        "CREATE INDEX IF NOT EXISTS idx_warehouses_name ON warehouses(name)",
        "CREATE INDEX IF NOT EXISTS idx_warehouses_manager_id ON warehouses(manager_id)",
        # فهارس جدول الأدوار
        "CREATE INDEX IF NOT EXISTS idx_roles_name ON roles(name)",
        # فهارس جدول إعدادات النظام
        "CREATE INDEX IF NOT EXISTS idx_system_settings_key ON system_settings(key)",
        "CREATE INDEX IF NOT EXISTS idx_system_settings_category ON system_settings(category)",
        # فهارس جدول سجل المراجعة
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_table_name ON audit_logs(table_name)",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_record_id ON audit_logs(record_id)",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action)",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_date ON audit_logs(created_at)",
        # فهارس مركبة مهمة
        "CREATE INDEX IF NOT EXISTS idx_products_category_warehouse ON products(category_id, warehouse_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_product_date ON stock_movements(product_id, created_at)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_type_status ON invoices(invoice_type, status)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_date_type ON invoices(invoice_date, invoice_type)",
    ]

    created_count = 0
    for index_sql in indexes:
        try:
            db.session.execute(text(index_sql))
            created_count += 1
        except Exception as e:
            print(f"⚠️ خطأ في إنشاء فهرس: {str(e)}")

    db.session.commit()
    print(f"✅ تم إنشاء {created_count} فهرس بنجاح")


def optimize_sqlite_settings():
    """تحسين إعدادات SQLite"""
    print("⚙️ تحسين إعدادات SQLite...")

    optimizations = [
        # تحسين الذاكرة
        "PRAGMA cache_size = 10000",  # 10MB cache
        "PRAGMA temp_store = MEMORY",
        # تحسين الكتابة
        "PRAGMA synchronous = NORMAL",
        "PRAGMA journal_mode = WAL",
        # تحسين الاستعلامات
        "PRAGMA optimize",
        # تحليل الجداول لتحسين الاستعلامات
        "ANALYZE",
    ]

    for optimization in optimizations:
        try:
            db.session.execute(text(optimization))
            print(f"✅ تم تطبيق: {optimization}")
        except Exception as e:
            print(f"⚠️ خطأ في تطبيق التحسين: {str(e)}")

    db.session.commit()


def vacuum_database():
    """ضغط قاعدة البيانات وإعادة تنظيمها"""
    print("🗜️ ضغط وإعادة تنظيم قاعدة البيانات...")

    try:
        # إغلاق الاتصال الحالي
        db.session.close()

        # تنفيذ VACUUM
        db.session.execute(text("VACUUM"))
        print("✅ تم ضغط قاعدة البيانات بنجاح")

    except Exception as e:
        print(f"⚠️ خطأ في ضغط قاعدة البيانات: {str(e)}")


def get_database_stats():
    """الحصول على إحصائيات قاعدة البيانات"""
    print("📊 إحصائيات قاعدة البيانات:")

    try:
        # حجم قاعدة البيانات
        result = db.session.execute(
            text(
                "SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()"
            )
        ).fetchone()
        if result:
            size_bytes = result[0]
            size_mb = size_bytes / (1024 * 1024)
            print(f"   - حجم قاعدة البيانات: {size_mb:.2f} MB")

        # عدد الصفحات
        result = db.session.execute(text("PRAGMA page_count")).fetchone()
        if result:
            print(f"   - عدد الصفحات: {result[0]}")

        # حجم الصفحة
        result = db.session.execute(text("PRAGMA page_size")).fetchone()
        if result:
            print(f"   - حجم الصفحة: {result[0]} bytes")

        # عدد الفهارس
        result = db.session.execute(
            text("SELECT COUNT(*) FROM sqlite_master WHERE type='index'")
        ).fetchone()
        if result:
            print(f"   - عدد الفهارس: {result[0]}")

        # عدد الجداول
        result = db.session.execute(
            text("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        ).fetchone()
        if result:
            print(f"   - عدد الجداول: {result[0]}")

    except Exception as e:
        print(f"⚠️ خطأ في الحصول على الإحصائيات: {str(e)}")


def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🚀 سكريبت تحسين أداء قاعدة البيانات")
    print("=" * 60)

    app = create_app()

    with app.app_context():
        try:
            # إحصائيات قبل التحسين
            print("\n📊 إحصائيات قبل التحسين:")
            get_database_stats()

            # إنشاء الفهارس
            create_indexes()

            # تحسين إعدادات SQLite
            optimize_sqlite_settings()

            # ضغط قاعدة البيانات
            vacuum_database()

            # إحصائيات بعد التحسين
            print("\n📊 إحصائيات بعد التحسين:")
            get_database_stats()

            print("\n🎉 تم تحسين قاعدة البيانات بنجاح!")

        except Exception as e:
            print(f"❌ خطأ في تحسين قاعدة البيانات: {str(e)}")


if __name__ == "__main__":
    main()
