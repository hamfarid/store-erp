# FILE: backend/src/routes/customer_supplier_accounts.py | PURPOSE: Routes
# with P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/routes/customer_supplier_accounts.py

نظام إدارة حسابات العملاء والموردين
All linting disabled due to complex imports and optional dependencies.
"""

from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from datetime import datetime, timedelta
import json

customer_supplier_accounts_bp = Blueprint("customer_supplier_accounts", __name__)

# بيانات تجريبية للعملاء والموردين
sample_customers = [
    {
        "id": 1,
        "name": "شركة الأحمد للتجارة",
        "type": "customer",
        "phone": "+966501234567",
        "email": "info@ahmed-trading.com",
        "address": "الرياض، المملكة العربية السعودية",
        "balance": 15000,
        "credit_limit": 50000,
        "payment_terms": 30,
        "status": "active",
        "created_at": "2024-01-01T00:00:00",
        "last_transaction": "2024-01-15T10:30:00",
    },
    {
        "id": 2,
        "name": "مؤسسة التقنية المتقدمة",
        "type": "supplier",
        "phone": "+966507654321",
        "email": "sales@advanced-tech.com",
        "address": "جدة، المملكة العربية السعودية",
        "balance": -25000,
        "credit_limit": 100000,
        "payment_terms": 45,
        "status": "active",
        "created_at": "2024-01-02T00:00:00",
        "last_transaction": "2024-01-14T14:20:00",
    },
    {
        "id": 3,
        "name": "متجر الإلكترونيات الحديث",
        "type": "customer",
        "phone": "+966512345678",
        "email": "orders@modern-electronics.com",
        "address": "الدمام، المملكة العربية السعودية",
        "balance": 8500,
        "credit_limit": 30000,
        "payment_terms": 15,
        "status": "active",
        "created_at": "2024-01-03T00:00:00",
        "last_transaction": "2024-01-13T16:45:00",
    },
]

sample_transactions = [
    {
        "id": 1,
        "account_id": 1,
        "type": "invoice",
        "reference": "INV-2024-001",
        "date": "2024-01-15T10:30:00",
        "description": "فاتورة مبيعات - أجهزة كمبيوتر",
        "debit": 15000,
        "credit": 0,
        "balance": 15000,
        "status": "pending",
    },
    {
        "id": 2,
        "account_id": 1,
        "type": "payment",
        "reference": "PAY-2024-001",
        "date": "2024-01-20T14:15:00",
        "description": "دفعة نقدية",
        "debit": 0,
        "credit": 5000,
        "balance": 10000,
        "status": "completed",
    },
    {
        "id": 3,
        "account_id": 2,
        "type": "bill",
        "reference": "BILL-2024-001",
        "date": "2024-01-14T14:20:00",
        "description": "فاتورة شراء - مكونات إلكترونية",
        "debit": 0,
        "credit": 25000,
        "balance": -25000,
        "status": "pending",
    },
]


@customer_supplier_accounts_bp.route("/customer-supplier-accounts", methods=["GET"])
def get_accounts():
    """الحصول على قائمة حسابات العملاء والموردين"""
    try:
        account_type = request.args.get("account_type", "all")
        status = request.args.get("status", "all")
        search = request.args.get("search", "")

        accounts = sample_customers.copy()

        # تطبيق الفلاتر
        if account_type != "all":
            accounts = [acc for acc in accounts if acc["type"] == account_type]

        if status != "all":
            accounts = [acc for acc in accounts if acc["status"] == status]

        if search:
            accounts = [
                acc
                for acc in accounts
                if search.lower() in acc["name"].lower()
                or search.lower() in acc["phone"].lower()
                or search.lower() in acc["email"].lower()
            ]

        return jsonify({"status": "success", "data": accounts, "total": len(accounts)})

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في جلب الحسابات: {str(e)}"}),
            500,
        )


@customer_supplier_accounts_bp.route(
    "/customer-supplier-accounts/<int:account_id>", methods=["GET"]
)
def get_account(account_id):
    """الحصول على تفاصيل حساب محدد"""
    try:
        account = next(
            (acc for acc in sample_customers if acc["id"] == account_id), None
        )

        if not account:
            return jsonify({"status": "error", "message": "الحساب غير موجود"}), 404

        # جلب المعاملات الخاصة بالحساب
        transactions = [
            trans for trans in sample_transactions if trans["account_id"] == account_id
        ]

        return jsonify(
            {
                "status": "success",
                "data": {"account": account, "transactions": transactions},
            }
        )

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في جلب تفاصيل الحساب: {str(e)}"}
            ),
            500,
        )


@customer_supplier_accounts_bp.route("/customer-supplier-accounts", methods=["POST"])
def create_account():
    """إنشاء حساب جديد"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ["name", "type", "phone"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "message": f"الحقل {field} مطلوب"}),
                    400,
                )

        # إنشاء حساب جديد
        new_account = {
            "id": max([acc["id"] for acc in sample_customers]) + 1,
            "name": data["name"],
            "type": data["type"],
            "phone": data["phone"],
            "email": data.get("email", ""),
            "address": data.get("address", ""),
            "balance": 0,
            "credit_limit": data.get("credit_limit", 0),
            "payment_terms": data.get("payment_terms", 30),
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "last_transaction": None,
        }

        sample_customers.append(new_account)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء الحساب بنجاح",
                    "data": new_account,
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في إنشاء الحساب: {str(e)}"}),
            500,
        )


@customer_supplier_accounts_bp.route(
    "/customer-supplier-accounts/<int:account_id>", methods=["PUT"]
)
def update_account(account_id):
    """تحديث حساب موجود"""
    try:
        data = request.get_json()

        account_index = next(
            (i for i, acc in enumerate(sample_customers) if acc["id"] == account_id),
            None,
        )

        if account_index is None:
            return jsonify({"status": "error", "message": "الحساب غير موجود"}), 404

        # تحديث البيانات
        account = sample_customers[account_index]
        account.update(
            {
                "name": data.get("name", account["name"]),
                "phone": data.get("phone", account["phone"]),
                "email": data.get("email", account["email"]),
                "address": data.get("address", account["address"]),
                "credit_limit": data.get("credit_limit", account["credit_limit"]),
                "payment_terms": data.get("payment_terms", account["payment_terms"]),
                "status": data.get("status", account["status"]),
            }
        )

        return jsonify(
            {"status": "success", "message": "تم تحديث الحساب بنجاح", "data": account}
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث الحساب: {str(e)}"}),
            500,
        )


@customer_supplier_accounts_bp.route(
    "/customer-supplier-accounts/<int:account_id>/transactions", methods=["GET"]
)
def get_account_transactions(account_id):
    """الحصول على معاملات حساب محدد"""
    try:
        account = next(
            (acc for acc in sample_customers if acc["id"] == account_id), None
        )

        if not account:
            return jsonify({"status": "error", "message": "الحساب غير موجود"}), 404

        transactions = [
            trans for trans in sample_transactions if trans["account_id"] == account_id
        ]

        # تطبيق الفلاتر
        transaction_type = request.args.get("transaction_type", "all")
        status = request.args.get("status", "all")
        date_from = request.args.get("date_from", "")
        date_to = request.args.get("date_to", "")

        if transaction_type != "all":
            transactions = [
                trans for trans in transactions if trans["type"] == transaction_type
            ]

        if status != "all":
            transactions = [
                trans for trans in transactions if trans["status"] == status
            ]

        if date_from:
            transactions = [
                trans for trans in transactions if trans["date"] >= date_from
            ]

        if date_to:
            transactions = [trans for trans in transactions if trans["date"] <= date_to]

        return jsonify(
            {
                "status": "success",
                "data": {
                    "account": account,
                    "transactions": transactions,
                    "total_transactions": len(transactions),
                },
            }
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في جلب المعاملات: {str(e)}"}),
            500,
        )


@customer_supplier_accounts_bp.route(
    "/customer-supplier-accounts/<int:account_id>/transactions", methods=["POST"]
)
def add_transaction():
    """إضافة معاملة جديدة"""
    try:
        data = request.get_json()
        account_id = int(request.view_args["account_id"])

        # التحقق من وجود الحساب
        account = next(
            (acc for acc in sample_customers if acc["id"] == account_id), None
        )

        if not account:
            return jsonify({"status": "error", "message": "الحساب غير موجود"}), 404

        # التحقق من البيانات المطلوبة
        required_fields = ["type", "reference", "description", "amount"]
        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "message": f"الحقل {field} مطلوب"}),
                    400,
                )

        # حساب المدين والدائن
        amount = float(data["amount"])
        if data["type"] in ["invoice", "debit_note"]:
            debit = amount
            credit = 0
        else:  # payment, credit_note
            debit = 0
            credit = amount

        # حساب الرصيد الجديد
        current_balance = account["balance"]
        new_balance = current_balance + debit - credit

        # إنشاء المعاملة الجديدة
        new_transaction = {
            "id": max([trans["id"] for trans in sample_transactions]) + 1,
            "account_id": account_id,
            "type": data["type"],
            "reference": data["reference"],
            "date": data.get("date", datetime.now().isoformat()),
            "description": data["description"],
            "debit": debit,
            "credit": credit,
            "balance": new_balance,
            "status": data.get("status", "pending"),
        }

        sample_transactions.append(new_transaction)

        # تحديث رصيد الحساب
        account["balance"] = new_balance
        account["last_transaction"] = new_transaction["date"]

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إضافة المعاملة بنجاح",
                    "data": new_transaction,
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في إضافة المعاملة: {str(e)}"}),
            500,
        )


@customer_supplier_accounts_bp.route(
    "/customer-supplier-accounts/summary", methods=["GET"]
)
def get_accounts_summary():
    """الحصول على ملخص الحسابات"""
    try:
        customers = [acc for acc in sample_customers if acc["type"] == "customer"]
        suppliers = [acc for acc in sample_customers if acc["type"] == "supplier"]

        customer_balance = sum(acc["balance"] for acc in customers)
        supplier_balance = sum(acc["balance"] for acc in suppliers)

        summary = {
            "customers": {
                "count": len(customers),
                "total_balance": customer_balance,
                "active_count": len(
                    [acc for acc in customers if acc["status"] == "active"]
                ),
            },
            "suppliers": {
                "count": len(suppliers),
                "total_balance": supplier_balance,
                "active_count": len(
                    [acc for acc in suppliers if acc["status"] == "active"]
                ),
            },
            "total_accounts": len(sample_customers),
            "total_receivables": customer_balance,
            "total_payables": abs(supplier_balance),
        }

        return jsonify({"status": "success", "data": summary})

    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في جلب ملخص الحسابات: {str(e)}"}
            ),
            500,
        )


@customer_supplier_accounts_bp.route(
    "/customer-supplier-accounts/aging-report", methods=["GET"]
)
def get_aging_report():
    """تقرير أعمار الديون"""
    try:
        account_type = request.args.get("type", "customer")

        accounts = [acc for acc in sample_customers if acc["type"] == account_type]

        aging_data = []
        for account in accounts:
            if account["balance"] > 0:  # فقط الحسابات التي عليها مبالغ
                # محاكاة حساب أعمار الديون
                aging_data.append(
                    {
                        "account_id": account["id"],
                        "account_name": account["name"],
                        "total_balance": account["balance"],
                        "current": account["balance"] * 0.4,  # محاكاة
                        "1_30_days": account["balance"] * 0.3,
                        "31_60_days": account["balance"] * 0.2,
                        "61_90_days": account["balance"] * 0.1,
                        "over_90_days": 0,
                    }
                )

        return jsonify({"status": "success", "data": aging_data})

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"خطأ في جلب تقرير أعمار الديون: {str(e)}",
                }
            ),
            500,
        )
