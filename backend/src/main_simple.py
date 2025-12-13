"""
#!/usr/bin/env python3

نظام إدارة المخزون - الملف الرئيسي المبسط
"""

# pylint: disable=wrong-import-position


import os
import sys

# DON'T CHANGE THIS !!! - Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Now import Flask modules and app components - import order matters for Flask
from flask import Flask, send_from_directory, jsonify, request  # noqa: E402
from flask_cors import CORS  # noqa: E402

# Import Flask-Session extension - simpler approach
try:
    # Import as Flask would internally access it during setup
    import flask_session  # pylint: disable=unused-import  # noqa: E402, F401
except ImportError:
    # If import fails, log a warning but continue
    print("⚠️ Warning: flask_session module not found, using Flask defaults")

from auth import AuthManager  # noqa: E402
from models.user import Role, User, db  # noqa: E402

# Import Customer model early to avoid conflicts


# Import essential blueprints - minimal set to avoid conflicts
from routes.users_unified import (
    users_unified_bp,
)  # noqa: E402  # FIXED: was user_bp from deleted user.py
from routes.inventory import inventory_bp  # noqa: E402
from routes.dashboard import dashboard_bp  # noqa: E402

# from routes.partners import partners_bp  # noqa: E402  # Commented out to avoid Customer conflicts
# from routes.admin import admin_bp  # noqa: E402  # Commented out - causing hangs

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))

# Enable CORS for frontend
CORS(app, supports_credentials=True)

# إعداد نظام المصادقة والجلسات
auth_manager = AuthManager(app)

# تسجيل blueprints الأساسية
app.register_blueprint(users_unified_bp, url_prefix="/api/users")
app.register_blueprint(inventory_bp, url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api")
# app.register_blueprint(partners_bp, url_prefix='/api')
# Commented out to avoid Customer conflicts
# app.register_blueprint(admin_bp, url_prefix='/api')  # Commented out - causing hangs

# إعداد قاعدة البيانات
db_path = os.path.join(os.path.dirname(__file__), "database", "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def create_default_data():
    """إنشاء البيانات الافتراضية"""

    try:
        # إنشاء الأدوار الافتراضية
        if not Role.query.first():
            # Using correct parameter names from Role class definition
            admin_role = Role()
            admin_role.name = "مدير النظام"
            admin_role.description = "صلاحيات كاملة لإدارة النظام"
            admin_role.permissions = {"admin": True, "all_modules": True}

            user_role = Role()
            user_role.name = "مستخدم عادي"
            user_role.description = "صلاحيات محدودة للاستخدام العادي"
            user_role.permissions = {"view": True, "edit": False}

            db.session.add(admin_role)
            db.session.add(user_role)
            db.session.commit()

            # إنشاء المستخدم الافتراضي
            admin_user = User(
                username="admin",
                email="admin@system.com",
                full_name="مدير النظام",
                role_id=admin_role.id,
            )
            admin_user.set_password("admin123")

            db.session.add(admin_user)
            db.session.commit()

            print("✅ تم إنشاء البيانات الافتراضية بنجاح")

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"❌ خطأ في إنشاء البيانات الافتراضية: {e}")
        db.session.rollback()


# إضافة مسارات API بسيطة للبيانات الأساسية


@app.route("/api/categories", methods=["GET", "POST"])
def categories():
    """Categories API (demo)."""
    if request.method == "GET":
        return jsonify(
            {
                "status": "success",
                "data": [
                    {"id": 1, "name": "بذور", "description": "بذور الخضروات والفواكه"},
                    {"id": 2, "name": "شتلات", "description": "شتلات جاهزة للزراعة"},
                    {"id": 3, "name": "أسمدة", "description": "أسمدة كيماوية وعضوية"},
                    {"id": 4, "name": "مبيدات", "description": "مبيدات حشرية وفطرية"},
                    {
                        "id": 5,
                        "name": "أدوات زراعية",
                        "description": "أدوات ومعدات زراعية",
                    },
                ],
            }
        )
    if request.method == "POST":
        return jsonify({"status": "success", "message": "تم إضافة التصنيف بنجاح"})

    return jsonify({"status": "error", "message": "طريقة غير مدعومة"}), 405


@app.route("/api/warehouses", methods=["GET", "POST"])
def warehouses():
    """Warehouses API (demo)."""
    if request.method == "GET":
        return jsonify(
            {
                "status": "success",
                "data": [
                    {"id": 1, "name": "المخزن الرئيسي", "location": "القاهرة"},
                    {"id": 2, "name": "مخزن الإسكندرية", "location": "الإسكندرية"},
                    {"id": 3, "name": "مخزن أسوان", "location": "أسوان"},
                ],
            }
        )
    if request.method == "POST":
        return jsonify({"status": "success", "message": "تم إضافة المخزن بنجاح"})

    return jsonify({"status": "error", "message": "طريقة غير مدعومة"}), 405


@app.route("/api/suppliers", methods=["GET", "POST"])
def suppliers():
    """Suppliers API (demo)."""
    if request.method == "GET":
        return jsonify(
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "name": "شركة البذور المصرية",
                        "contact_person": "أحمد محمد",
                        "phone": "01234567890",
                        "email": "ahmed@seeds.com",
                        "address": "القاهرة",
                    },
                    {
                        "id": 2,
                        "name": "مؤسسة الأسمدة الحديثة",
                        "contact_person": "محمد علي",
                        "phone": "01234567891",
                        "email": "mohamed@fertilizers.com",
                        "address": "الجيزة",
                    },
                ],
            }
        )
    if request.method == "POST":
        return jsonify({"status": "success", "message": "تم إضافة المورد بنجاح"})

    return jsonify({"status": "error", "message": "طريقة غير مدعومة"}), 405


@app.route("/api/customers", methods=["GET", "POST"])
def customers():
    """Customers API (demo)."""
    if request.method == "GET":
        return jsonify(
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "name": "مزرعة النيل",
                        "contact_person": "خالد حسن",
                        "phone": "01234567893",
                        "email": "khaled@nilfarm.com",
                        "address": "المنيا",
                    },
                    {
                        "id": 2,
                        "name": "شركة الزراعة الحديثة",
                        "contact_person": "فاطمة محمود",
                        "phone": "01234567894",
                        "email": "fatma@modern-agri.com",
                        "address": "بني سويف",
                    },
                ],
            }
        )
    if request.method == "POST":
        return jsonify({"status": "success", "message": "تم إضافة العميل بنجاح"})

    return jsonify({"status": "error", "message": "طريقة غير مدعومة"}), 405


# مسارات الفواتير


@app.route("/api/sales-invoices", methods=["GET", "POST"])
def sales_invoices():
    """Sales invoices API (demo)."""
    if request.method == "GET":
        return jsonify(
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "invoice_number": "INV-2025-001",
                        "customer_name": "مزرعة النيل",
                        "date": "2025-06-21",
                        "total_amount": 1500.0,
                        "status": "مدفوعة",
                        "items": [
                            {
                                "product_name": "بذور طماطم هجين",
                                "quantity": 10,
                                "price": 75.0,
                                "total": 750.0,
                            },
                            {
                                "product_name": "سماد NPK",
                                "quantity": 5,
                                "price": 150.0,
                                "total": 750.0,
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "invoice_number": "INV-2025-002",
                        "customer_name": "شركة الزراعة الحديثة",
                        "date": "2025-06-20",
                        "total_amount": 2000.0,
                        "status": "معلقة",
                        "items": [
                            {
                                "product_name": "شتلات طماطم",
                                "quantity": 50,
                                "price": 40.0,
                                "total": 2000.0,
                            }
                        ],
                    },
                ],
            }
        )
    if request.method == "POST":
        return jsonify(
            {"status": "success", "message": "تم إنشاء فاتورة المبيعات بنجاح"}
        )

    return jsonify({"status": "error", "message": "طريقة غير مدعومة"}), 405


@app.route("/api/purchase-invoices", methods=["GET", "POST"])
def purchase_invoices():
    """Purchase invoices API (demo)."""
    if request.method == "GET":
        return jsonify(
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "invoice_number": "PUR-2025-001",
                        "supplier_name": "شركة البذور المصرية",
                        "date": "2025-06-19",
                        "total_amount": 5000.0,
                        "status": "مدفوعة",
                        "items": [
                            {
                                "product_name": "بذور طماطم هجين",
                                "quantity": 100,
                                "price": 50.0,
                                "total": 5000.0,
                            }
                        ],
                    },
                    {
                        "id": 2,
                        "invoice_number": "PUR-2025-002",
                        "supplier_name": "مؤسسة الأسمدة الحديثة",
                        "date": "2025-06-18",
                        "total_amount": 3000.0,
                        "status": "معلقة",
                        "items": [
                            {
                                "product_name": "سماد NPK",
                                "quantity": 25,
                                "price": 120.0,
                                "total": 3000.0,
                            }
                        ],
                    },
                ],
            }
        )
    if request.method == "POST":
        return jsonify(
            {"status": "success", "message": "تم إنشاء فاتورة المشتريات بنجاح"}
        )

    return jsonify({"status": "error", "message": "طريقة غير مدعومة"}), 405


# مسارات الإدارة


@app.route("/api/admin/users", methods=["GET", "POST"])
def admin_users():
    """Admin users API (demo)."""
    if request.method == "GET":
        return jsonify(
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "username": "admin",
                        "full_name": "مدير النظام",
                        "email": "admin@system.com",
                        "role": "مدير النظام",
                        "is_active": True,
                        "created_at": "2025-06-21",
                    }
                ],
            }
        )
    if request.method == "POST":
        return jsonify({"status": "success", "message": "تم إضافة المستخدم بنجاح"})

    return jsonify({"status": "error", "message": "طريقة غير مدعومة"}), 405


@app.route("/api/admin/roles", methods=["GET"])
def admin_roles():
    """Admin roles list (demo)."""
    return jsonify(
        {
            "status": "success",
            "data": [
                {"id": 1, "name": "مدير النظام", "description": "صلاحيات كاملة"},
                {"id": 2, "name": "مدير المخزون", "description": "إدارة المخزون"},
                {"id": 3, "name": "موظف المبيعات", "description": "إدارة المبيعات"},
                {"id": 4, "name": "موظف المشتريات", "description": "إدارة المشتريات"},
                {"id": 5, "name": "محاسب", "description": "التقارير المالية"},
            ],
        }
    )


with app.app_context():
    db.create_all()
    create_default_data()


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    """Serve static files with index.html fallback."""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)

    index_path = os.path.join(static_folder_path, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, "index.html")

    return "index.html not found", 404


if __name__ == "__main__":
    # تشغيل الخادم على منفذ 8000
    app.run(host="0.0.0.0", port=8000, debug=True)
