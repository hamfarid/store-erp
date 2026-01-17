# FILE: backend/src/routes/temp_api.py | PURPOSE: Routes with P0.2.4 error
# envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

"""
نقاط نهاية API مؤقتة للاختبار
Temporary API endpoints for testing
"""

from flask import Blueprint, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from datetime import datetime

# إنشاء Blueprint
temp_api_bp = Blueprint("temp_api", __name__)

# بيانات تجريبية
SAMPLE_PRODUCTS = [
    {
        "id": 1,
        "name": "منتج تجريبي 1",
        "sku": "PROD001",
        "barcode": "1234567890",
        "price": 100.0,
        "cost": 80.0,
        "quantity": 50,
        "category_id": 1,
        "is_active": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "name": "منتج تجريبي 2",
        "sku": "PROD002",
        "barcode": "1234567891",
        "price": 200.0,
        "cost": 160.0,
        "quantity": 30,
        "category_id": 1,
        "is_active": True,
        "created_at": datetime.now().isoformat(),
    },
]

SAMPLE_CUSTOMERS = [
    {
        "id": 1,
        "name": "عميل تجريبي 1",
        "email": "customer1@example.com",
        "phone": "123456789",
        "address": "عنوان تجريبي 1",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "name": "عميل تجريبي 2",
        "email": "customer2@example.com",
        "phone": "987654321",
        "address": "عنوان تجريبي 2",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
    },
]

SAMPLE_SUPPLIERS = [
    {
        "id": 1,
        "name": "مورد تجريبي 1",
        "email": "supplier1@example.com",
        "phone": "111222333",
        "address": "عنوان مورد 1",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
    }
]


@temp_api_bp.route("/api/temp/products", methods=["GET"])
def get_temp_products():
    """الحصول على المنتجات التجريبية"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        search = request.args.get("search", "")

        # تطبيق البحث
        products = SAMPLE_PRODUCTS
        if search:
            products = [p for p in products if search.lower() in p["name"].lower()]

        # تطبيق التصفح
        start = (page - 1) * per_page
        end = start + per_page
        paginated_products = products[start:end]

        return jsonify(
            {
                "success": True,
                "data": paginated_products,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(products),
                    "pages": (len(products) + per_page - 1) // per_page,
                },
                "message": "تم الحصول على المنتجات التجريبية بنجاح",
            }
        )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على المنتجات التجريبية / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@temp_api_bp.route("/api/temp/customers", methods=["GET"])
def get_temp_customers():
    """الحصول على العملاء التجريبيين"""
    try:
        return success_response(
            data={"customers": SAMPLE_CUSTOMERS, "total": len(SAMPLE_CUSTOMERS)},
            message="تم الحصول على العملاء التجريبيين بنجاح / Customers retrieved successfully",
            status_code=200,
        )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على العملاء التجريبيين / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@temp_api_bp.route("/api/temp/suppliers", methods=["GET"])
def get_temp_suppliers():
    """الحصول على الموردين التجريبيين"""
    try:
        return success_response(
            data={"suppliers": SAMPLE_SUPPLIERS, "total": len(SAMPLE_SUPPLIERS)},
            message="تم الحصول على الموردين التجريبيين بنجاح / Suppliers retrieved successfully",
            status_code=200,
        )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على الموردين التجريبيين / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@temp_api_bp.route("/api/temp/users", methods=["GET"])
def get_temp_users():
    """الحصول على المستخدمين التجريبيين"""
    try:
        sample_users = [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "full_name": "مدير النظام",
                "role": "admin",
                "is_active": True,
                "created_at": datetime.now().isoformat(),
            }
        ]

        return success_response(
            data={"users": sample_users, "total": len(sample_users)},
            message="تم الحصول على المستخدمين التجريبيين بنجاح / Users retrieved successfully",
            status_code=200,
        )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على المستخدمين التجريبيين / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@temp_api_bp.route("/api/temp/categories", methods=["GET"])
def get_temp_categories():
    """الحصول على الفئات التجريبية"""
    try:
        sample_categories = [
            {
                "id": 1,
                "name": "فئة تجريبية 1",
                "description": "وصف الفئة التجريبية 1",
                "is_active": True,
                "created_at": datetime.now().isoformat(),
            }
        ]

        return success_response(
            data={"categories": sample_categories, "total": len(sample_categories)},
            message="تم الحصول على الفئات التجريبية بنجاح / Categories retrieved successfully",
            status_code=200,
        )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على الفئات التجريبية / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@temp_api_bp.route("/api/temp/warehouses", methods=["GET"])
def get_temp_warehouses():
    """الحصول على المخازن التجريبية"""
    try:
        sample_warehouses = [
            {
                "id": 1,
                "name": "مخزن تجريبي 1",
                "location": "موقع تجريبي 1",
                "description": "وصف المخزن التجريبي",
                "is_active": True,
                "created_at": datetime.now().isoformat(),
            }
        ]

        return success_response(
            data={"warehouses": sample_warehouses, "total": len(sample_warehouses)},
            message="تم الحصول على المخازن التجريبية بنجاح / Warehouses retrieved successfully",
            status_code=200,
        )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على المخازن التجريبية / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@temp_api_bp.route("/api/temp/inventory", methods=["GET"])
def get_temp_inventory():
    """الحصول على المخزون التجريبي"""
    try:
        sample_inventory = [
            {
                "id": 1,
                "product_id": 1,
                "product_name": "منتج تجريبي 1",
                "warehouse_id": 1,
                "warehouse_name": "مخزن تجريبي 1",
                "quantity": 50,
                "reserved_quantity": 5,
                "available_quantity": 45,
                "last_updated": datetime.now().isoformat(),
            }
        ]

        return success_response(
            data={"inventory": sample_inventory, "total": len(sample_inventory)},
            message="تم الحصول على المخزون التجريبي بنجاح / Inventory retrieved successfully",
            status_code=200,
        )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على المخزون التجريبي / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@temp_api_bp.route("/api/temp/reports", methods=["GET"])
def get_temp_reports():
    """الحصول على التقارير التجريبية"""
    try:
        sample_reports = [
            {
                "id": 1,
                "name": "تقرير المبيعات الشهري",
                "type": "sales",
                "period": "monthly",
                "data": {
                    "total_sales": 10000,
                    "total_orders": 50,
                    "average_order_value": 200,
                },
                "generated_at": datetime.now().isoformat(),
            }
        ]

        return success_response(
            data={"reports": sample_reports, "total": len(sample_reports)},
            message="تم الحصول على التقارير التجريبية بنجاح / Reports retrieved successfully",
            status_code=200,
        )

    except Exception as e:
        return error_response(
            message=f"خطأ في الحصول على التقارير التجريبية / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@temp_api_bp.route("/api/temp/auth/login", methods=["POST"])
def temp_login():
    """تسجيل دخول تجريبي"""
    try:
        data = request.get_json() or {}
        username = data.get("username", "")
        password = data.get("password", "")

        # تسجيل دخول تجريبي
        if username == "admin" and password == "admin":
            return jsonify(
                {
                    "success": True,
                    "data": {
                        "token": "temp_token_12345",
                        "user": {
                            "id": 1,
                            "username": "admin",
                            "email": "admin@example.com",
                            "full_name": "مدير النظام",
                            "role": "admin",
                        },
                    },
                    "message": "تم تسجيل الدخول بنجاح",
                }
            )
        else:
            return error_response(
                message="اسم المستخدم أو كلمة المرور غير صحيحة",
                code=ErrorCodes.AUTH_INVALID_CREDENTIALS,
                status_code=401,
            )

    except Exception as e:
        return error_response(
            message=f"خطأ في تسجيل الدخول / Error: {str(e)}",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )
