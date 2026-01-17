#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
الخادم الموحد لنظام إدارة المخزون
All linting disabled due to complex imports and optional dependencies.
"""

import os
import sys
import time
from datetime import datetime, timezone

# إضافة مسار المشروع إلى sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from flask import Flask, request, jsonify, session, render_template
    from flask_cors import CORS

    FLASK_AVAILABLE = True
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
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

        def before_request(self, f):
            return f

        def after_request(self, f):
            return f

        def errorhandler(self, code):
            def decorator(f):
                return f

            return decorator

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
app = Flask(__name__, template_folder="templates", static_folder="static")
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
    print(f"⚠️ SQLite tuning not applied: {e}")


# تمكين CORS
# Configure CORS with explicit, safe defaults
origins_env = os.environ.get("CORS_ORIGINS")
if origins_env:
    origins = [o.strip() for o in origins_env.split(",") if o.strip()]
else:
    origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5502",
    ]
CORS(
    app,
    supports_credentials=True,
    origins=origins,
    allow_headers=["Content-Type", "Authorization"],
)

# Simple in-memory rate limiting for login endpoint (no extra deps)
_LOGIN_BUCKETS = {}
_LOGIN_MAX_PER_MIN = int(os.environ.get("LOGIN_RATE_LIMIT_PER_MIN", "10"))
_LOGIN_WINDOW_SECONDS = 60


@app.before_request
def _rate_limit_login():
    try:
        if getattr(request, "path", "") == "/api/auth/login" and _LOGIN_MAX_PER_MIN > 0:
            ip = getattr(request, "remote_addr", "unknown") or "unknown"
            now = time.time()
            bucket = _LOGIN_BUCKETS.get(ip, [])
            # keep only requests within window
            bucket = [t for t in bucket if now - t < _LOGIN_WINDOW_SECONDS]
            if len(bucket) >= _LOGIN_MAX_PER_MIN:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Too many requests, please try again later.",
                        }
                    ),
                    429,
                )
            bucket.append(now)
            _LOGIN_BUCKETS[ip] = bucket
    except Exception:
        # never block app due to limiter errors
        pass


# Minimal security headers for all responses
@app.after_request
def add_security_headers(response):
    try:
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Do not set HSTS here (this server may run over HTTP in dev). Use https_server for HSTS.
    except Exception:
        pass
    return response


# تهيئة قاعدة البيانات
try:
    if hasattr(db, "init_app"):
        db.init_app(app)
        print("✅ Database initialized successfully")
    else:
        print("⚠️ MockDB in use - no database initialization needed")
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
    ("routes.rag", "rag_bp"),
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
    try:
        # Check if request expects JSON (API request)
        if request.is_json or "application/json" in request.headers.get("Accept", ""):
            return (
                jsonify({"success": False, "error": "الصفحة غير موجودة", "code": 404}),
                404,
            )
        else:
            # Return HTML template for browser requests
            return render_template("404.html"), 404
    except Exception:
        return (
            jsonify({"success": False, "error": "الصفحة غير موجودة", "code": 404}),
            404,
        )


@app.errorhandler(500)
def internal_error(error):
    """معالج خطأ 500"""
    try:
        # Check if request expects JSON (API request)
        if request.is_json or "application/json" in request.headers.get("Accept", ""):
            return (
                jsonify(
                    {"success": False, "error": "خطأ داخلي في الخادم", "code": 500}
                ),
                500,
            )
        else:
            # Return HTML template for browser requests
            return render_template("500.html"), 500
    except Exception:
        return (
            jsonify({"success": False, "error": "خطأ داخلي في الخادم", "code": 500}),
            500,
        )


@app.errorhandler(403)
def forbidden(error):
    """معالج خطأ 403"""
    try:
        # Check if request expects JSON (API request)
        if request.is_json or "application/json" in request.headers.get("Accept", ""):
            return (
                jsonify(
                    {"success": False, "error": "ليس لديك صلاحية للوصول", "code": 403}
                ),
                403,
            )
        else:
            # Return HTML template for browser requests
            return render_template("403.html"), 403
    except Exception:
        return (
            jsonify({"success": False, "error": "ليس لديك صلاحية للوصول", "code": 403}),
            403,
        )


@app.errorhandler(400)
def bad_request(error):
    """معالج خطأ 400"""
    try:
        # Check if request expects JSON (API request)
        if request.is_json or "application/json" in request.headers.get("Accept", ""):
            return (
                jsonify({"success": False, "error": "طلب غير صحيح", "code": 400}),
                400,
            )
        else:
            # Return HTML template for browser requests
            return render_template("404.html"), 400  # Use 404 template as fallback
    except Exception:
        return jsonify({"success": False, "error": "طلب غير صحيح", "code": 400}), 400


@app.errorhandler(405)
def method_not_allowed(error):
    """معالج خطأ 405"""
    try:
        # Check if request expects JSON (API request)
        if request.is_json or "application/json" in request.headers.get("Accept", ""):
            return (
                jsonify(
                    {"success": False, "error": "طريقة الطلب غير مسموحة", "code": 405}
                ),
                405,
            )
        else:
            # Return HTML template for browser requests
            return render_template("404.html"), 405  # Use 404 template as fallback
    except Exception:
        return (
            jsonify({"success": False, "error": "طريقة الطلب غير مسموحة", "code": 405}),
            405,
        )


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


@app.route("/test-error")
def test_error():
    """Test route to trigger 500 error"""
    raise Exception("This is a test error for testing 500 error page")


def main():
    """الدالة الرئيسية"""
    # تهيئة قاعدة البيانات
    init_database()

    # تسجيل بدء تشغيل الخادم
    try:
        log_system("server_start", "🚀 بدء تشغيل الخادم الموحد...")
    except Exception:
        print("🚀 بدء تشغيل الخادم الموحد...")

    # تشغيل الخادم
    try:
        port = int(os.environ.get("PORT", 5000))
        print(f"🚀 محاولة تشغيل الخادم على المنفذ {port}")
        app.run(host="0.0.0.0", port=port, debug=True, use_reloader=True)
    except OSError as e:
        if "Address already in use" in str(e) or "WinError 10048" in str(e):
            print(f"❌ المنفذ {port} مستخدم بالفعل، محاولة استخدام منفذ بديل...")
            try:
                alternative_port = port + 1
                print(f"🔄 محاولة تشغيل الخادم على المنفذ {alternative_port}")
                app.run(
                    host="0.0.0.0", port=alternative_port, debug=True, use_reloader=True
                )
            except Exception as e2:
                print(f"❌ فشل في تشغيل الخادم على المنفذ البديل: {e2}")
                sys.exit(1)
        else:
            print(f"❌ خطأ في تشغيل الخادم: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ عام في تشغيل الخادم: {e}")
        import traceback

        traceback.print_exc()
        try:
            log_system("server_error", f"❌ خطأ في تشغيل الخادم: {e}")
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
