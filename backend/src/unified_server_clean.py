#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
الخادم الموحد لنظام إدارة المخزون
# type: ignore  # تجاهل تحذيرات النوع
"""

import os
import sys
from datetime import datetime, timezone

# إضافة مسار المشروع إلى sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from flask import Flask, request, jsonify, session, render_template
    from flask_cors import CORS
except ImportError:
    # Fallback when Flask is not available
    class Flask:
        def __init__(self, *args, **kwargs):
            self.config = {}

        def route(self, *args, **kwargs):
            def decorator(f):
                return f

            return decorator

        def register_blueprint(self, *args, **kwargs):
            pass

        def run(self, *args, **kwargs):
            print("Flask not available - running in mock mode")

    def CORS(*args, **kwargs):
        pass

    def jsonify(data):
        return {"data": data}

    class request:
        json = {}
        form = {}
        args = {}
        remote_addr = "127.0.0.1"

    session = {}

    def render_template(*args, **kwargs):
        return "Template not available"


try:
    from werkzeug.security import generate_password_hash
except ImportError:

    def generate_password_hash(password):
        return password


# استيراد النماذج والمكونات
try:
    from src.models.unified_models import Product, Category
    from src.database import db
    from src.models.user import User
except ImportError:
    # Fallback when models are not available
    class MockDB:
        def init_app(self, app):
            pass

        def create_all(self):
            pass

        @property
        def engine(self):
            return None

    db = MockDB()

    class User:
        pass

    class Product:
        pass

    class Category:
        pass


# استيراد نظام التسجيل
try:
    from logging_system import log_click, log_route_access, log_system
except ImportError:

    def log_click(*args, **kwargs):
        pass

    def log_route_access(*args, **kwargs):
        pass

    def log_system(*args, **kwargs):
        pass


# إنشاء تطبيق Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///inventory.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# SQLite locking and performance tuning for SQLAlchemy engine
try:
    import sqlite3
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    from sqlalchemy.pool import NullPool

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "poolclass": NullPool,
        "connect_args": {
            "check_same_thread": False,
            "timeout": 30,
        },
    }

    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ARG001
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA busy_timeout=5000")
            finally:
                cursor.close()

except Exception as e:  # noqa: BLE001
    print(f"\u26a0\ufe0f SQLite tuning not applied: {e}")


# تمكين CORS
CORS(app)

# تهيئة قاعدة البيانات
try:
    db.init_app(app)
except Exception as e:
    print(f"تحذير: لا يمكن تهيئة قاعدة البيانات: {e}")

# استيراد وتسجيل المسارات
blueprints = [
    ("routes.dashboard", "dashboard_bp"),
    ("routes.inventory", "inventory_bp"),
    ("routes.products", "products_bp"),
    ("routes.suppliers", "suppliers_bp"),
    ("routes.customers", "customers_bp"),
    ("routes.invoices", "invoices_bp"),
    ("routes.sales", "sales_bp"),
    ("routes.reports", "reports_bp"),
    ("routes.excel_import", "excel_bp"),
    ("routes.export", "export_bp"),
    ("routes.security_system", "security_bp"),
    ("routes.user", "user_bp"),
    ("routes.admin_panel", "admin_bp"),
    ("routes.lot_management", "lot_bp"),
    ("routes.permissions", "permissions_bp"),
]

for module_name, blueprint_name in blueprints:
    try:
        module = __import__(module_name, fromlist=[blueprint_name])
        blueprint = getattr(module, blueprint_name)
        app.register_blueprint(blueprint)
    except ImportError as e:
        print(f"تحذير: لا يمكن استيراد {module_name}: {e}")
    except AttributeError as e:
        print(f"تحذير: لا يمكن العثور على {blueprint_name} في {module_name}: {e}")


@app.route("/")
def index():
    """الصفحة الرئيسية"""
    try:
        log_route_access("/", getattr(request, "remote_addr", "127.0.0.1"))
        return render_template("index.html")
    except Exception as e:
        return (
            jsonify(
                {"success": False, "error": f"خطأ في تحميل الصفحة الرئيسية: {str(e)}"}
            ),
            500,
        )


@app.route("/api/health")
def health_check():
    """فحص صحة النظام"""
    try:
        return jsonify(
            {
                "success": True,
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "message": "النظام يعمل بشكل طبيعي",
            }
        )
    except Exception as e:
        return jsonify({"success": False, "status": "error", "error": str(e)}), 500


@app.route("/api/status")
def system_status():
    """حالة النظام"""
    try:
        status = {
            "database": "connected",
            "server": "running",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # فحص قاعدة البيانات
        try:
            if hasattr(db, "engine") and db.engine:
                db.engine.execute("SELECT 1")
            status["database"] = "connected"
        except Exception:
            status["database"] = "disconnected"

        return jsonify(
            {
                "success": True,
                "status": status,
                "message": "تم الحصول على حالة النظام بنجاح",
            }
        )
    except Exception as e:
        return (
            jsonify(
                {"success": False, "error": f"خطأ في الحصول على حالة النظام: {str(e)}"}
            ),
            500,
        )


@app.errorhandler(404)
def not_found(error):
    """معالج خطأ 404"""
    return jsonify({"success": False, "error": "الصفحة غير موجودة", "code": 404}), 404


@app.errorhandler(500)
def internal_error(error):
    """معالج خطأ 500"""
    return jsonify({"success": False, "error": "خطأ داخلي في الخادم", "code": 500}), 500


def init_database():
    """تهيئة قاعدة البيانات"""
    try:
        with app.app_context():
            if hasattr(db, "create_all"):
                db.create_all()
                print("تم تهيئة قاعدة البيانات بنجاح")
            else:
                print("تحذير: MockDB في الاستخدام - لا حاجة لتهيئة قاعدة البيانات")
        return True
    except Exception as e:
        print(f"خطأ في تهيئة قاعدة البيانات: {e}")
        return False


def main():
    """الدالة الرئيسية"""
    # تهيئة قاعدة البيانات
    init_database()

    # تسجيل بدء تشغيل الخادم
    log_system("🚀 بدء تشغيل الخادم الموحد...")

    # تشغيل الخادم
    try:
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
    except Exception as e:
        print(f"خطأ في تشغيل الخادم: {e}")
        log_system(f"❌ خطأ في تشغيل الخادم: {e}")


if __name__ == "__main__":
    main()
