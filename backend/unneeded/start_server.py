"""
خادم نظام ERP المتكامل
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import logging

# إنشاء التطبيق
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🚀 بدء تشغيل نظام ERP المتكامل...")
print("📍 الخادم متاح على: http://localhost:5000")
print("🔗 فحص الصحة: http://localhost:5000/api/health")
print("=" * 50)

# ==================== APIs الأساسية ====================


@app.route("/api/health", methods=["GET"])
def health_check():
    """فحص صحة النظام"""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "message": "نظام ERP المتكامل يعمل بنجاح! ✅",
        }
    )


@app.route("/api/auth/login", methods=["POST"])
def login():
    """تسجيل الدخول"""
    try:
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")

        # بيانات تجريبية
        demo_users = {
            "admin": {
                "password": "admin123",
                "name": "مدير النظام",
                "role": "مدير عام",
            },
            "manager": {
                "password": "manager123",
                "name": "مدير المخزون",
                "role": "مدير مخزون",
            },
            "user": {"password": "user123", "name": "موظف المبيعات", "role": "موظف"},
        }

        if username in demo_users and demo_users[username]["password"] == password:
            user_data = demo_users[username]
            token = f"token_{username}_{datetime.now().timestamp()}"

            return jsonify(
                {
                    "success": True,
                    "token": token,
                    "user": {
                        "id": list(demo_users.keys()).index(username) + 1,
                        "username": username,
                        "name": user_data["name"],
                        "role": user_data["role"],
                        "last_login": datetime.now().isoformat(),
                    },
                    "message": f'مرحباً {user_data["name"]}',
                }
            )
        else:
            return (
                jsonify(
                    {"success": False, "error": "اسم المستخدم أو كلمة المرور غير صحيحة"}
                ),
                401,
            )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/dashboard/data", methods=["GET"])
def get_dashboard_data():
    """بيانات لوحة التحكم"""
    return jsonify(
        {
            "success": True,
            "data": {
                "summary": {
                    "total_products": 150,
                    "total_inventory_value": 125000,
                    "low_stock_alerts": 5,
                    "monthly_sales": 85000,
                    "profit_margin": 32.5,
                    "inventory_turnover": 4.2,
                },
                "inventory_trends": [
                    {"month": "يناير", "value": 120000, "quantity": 4800},
                    {"month": "فبراير", "value": 115000, "quantity": 4600},
                    {"month": "مارس", "value": 125000, "quantity": 5000},
                    {"month": "أبريل", "value": 130000, "quantity": 5200},
                    {"month": "مايو", "value": 128000, "quantity": 5100},
                    {"month": "يونيو", "value": 125000, "quantity": 5000},
                ],
                "category_distribution": [
                    {"name": "بذور", "value": 48, "amount": 60000},
                    {"name": "أسمدة", "value": 36, "amount": 45000},
                    {"name": "مبيدات", "value": 16, "amount": 20000},
                ],
                "warehouse_performance": [
                    {"name": "المخزن الرئيسي", "utilization": 75, "value": 80000},
                    {"name": "مخزن الفرع الأول", "utilization": 60, "value": 30000},
                ],
                "recent_activities": [
                    {
                        "id": 1,
                        "type": "stock_movement",
                        "description": "استلام دفعة بذور طماطم - 100 كيلو",
                        "timestamp": "2024-12-01 14:30",
                        "user": "أحمد محمد",
                    },
                    {
                        "id": 2,
                        "type": "sale_order",
                        "description": "أمر بيع جديد - العميل: مزرعة النيل",
                        "timestamp": "2024-12-01 13:15",
                        "user": "فاطمة علي",
                    },
                ],
            },
        }
    )


@app.route("/api/products-advanced", methods=["GET"])
def get_products():
    """المنتجات المتقدمة"""
    return jsonify(
        {
            "success": True,
            "products": [
                {
                    "id": 1,
                    "name": "بذور طماطم هجين",
                    "sku": "TOM-HYB-001",
                    "category": "بذور",
                    "current_stock": 150.0,
                    "sale_price": 35.00,
                    "cost_price": 25.50,
                    "quality_grade": "premium",
                    "is_active": True,
                },
                {
                    "id": 2,
                    "name": "سماد NPK متوازن",
                    "sku": "NPK-BAL-001",
                    "category": "أسمدة",
                    "current_stock": 75.0,
                    "sale_price": 60.00,
                    "cost_price": 45.00,
                    "quality_grade": "standard",
                    "is_active": True,
                },
            ],
            "count": 2,
        }
    )


@app.route("/api/dashboard/alerts", methods=["GET"])
def get_alerts():
    """التنبيهات"""
    return jsonify(
        {
            "success": True,
            "alerts": [
                {
                    "id": 1,
                    "type": "low_stock",
                    "title": "مخزون منخفض",
                    "message": "5 منتجات تحتاج إعادة طلب",
                    "urgency": "high",
                    "timestamp": "2024-12-01 10:00",
                },
                {
                    "id": 2,
                    "type": "expiring_batches",
                    "title": "لوط قريبة الانتهاء",
                    "message": "3 لوط تنتهي خلال 30 يوم",
                    "urgency": "medium",
                    "timestamp": "2024-12-01 09:30",
                },
            ],
        }
    )


@app.route("/api/integration/reports/comprehensive-inventory", methods=["GET"])
def get_comprehensive_report():
    """التقرير الشامل"""
    return jsonify(
        {
            "success": True,
            "report": {
                "summary": {
                    "total_products": 150,
                    "total_quantity": 5000.0,
                    "total_value": 125000.0,
                    "low_stock_products": 5,
                    "expiring_batches": 3,
                }
            },
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
