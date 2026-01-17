# FILE: backend/src/routes/payment_management.py | PURPOSE: Routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# type: ignore
# pylint: disable=all
# flake8: noqa
# /home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/routes/payment_management.py

"""
Payment Management Routes
مسارات إدارة المدفوعات
"""

from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from models.payment_management import (
    PaymentOrder,
    DebtRecord,
    DebtPayment,
    DebtFollowUp,
    PaymentProcessingLog,
    PaymentAttachment,
    BankAccount,
)

# Import database - handle different import paths
try:
    from database import db
except ImportError:
    # Create mock db for testing
    class MockDB:
        session = None

        @staticmethod
        def create_all():
            pass

        @staticmethod
        def drop_all():
            pass

    db = MockDB()
from datetime import datetime
import logging

# إنشاء Blueprint
payment_management_bp = Blueprint("payment_management", __name__)

# إعداد نظام التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@payment_management_bp.route("/payment-orders", methods=["GET"])
def get_payment_orders():
    """الحصول على جميع أوامر الدفع"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        orders = PaymentOrder.query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify(
            {
                "status": "success",
                "data": {
                    "orders": [order.to_dict() for order in orders.items],
                    "total": orders.total,
                    "pages": orders.pages,
                    "current_page": page,
                },
            }
        )
    except Exception as e:
        logger.error(f"Error getting payment orders: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_management_bp.route("/payment-orders", methods=["POST"])
def create_payment_order():
    """إنشاء أمر دفع جديد"""
    try:
        data = request.get_json()

        order = PaymentOrder(
            order_number=data.get("order_number"),
            customer_id=data.get("customer_id"),
            supplier_id=data.get("supplier_id"),
            amount=data.get("amount"),
            currency=data.get("currency", "USD"),
            payment_type=data.get("payment_type"),
            due_date=(
                datetime.fromisoformat(data.get("due_date"))
                if data.get("due_date")
                else None
            ),
            description=data.get("description"),
            status=data.get("status", "pending"),
        )

        db.session.add(order)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء أمر الدفع بنجاح",
                    "data": order.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating payment order: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_management_bp.route("/debt-records", methods=["GET"])
def get_debt_records():
    """الحصول على سجلات الديون"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        records = DebtRecord.query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify(
            {
                "status": "success",
                "data": {
                    "records": [record.to_dict() for record in records.items],
                    "total": records.total,
                    "pages": records.pages,
                    "current_page": page,
                },
            }
        )
    except Exception as e:
        logger.error(f"Error getting debt records: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_management_bp.route("/debt-records", methods=["POST"])
def create_debt_record():
    """إنشاء سجل دين جديد"""
    try:
        data = request.get_json()

        record = DebtRecord(
            customer_id=data.get("customer_id"),
            supplier_id=data.get("supplier_id"),
            invoice_id=data.get("invoice_id"),
            debt_amount=data.get("debt_amount"),
            currency=data.get("currency", "USD"),
            due_date=(
                datetime.fromisoformat(data.get("due_date"))
                if data.get("due_date")
                else None
            ),
            description=data.get("description"),
            status=data.get("status", "active"),
        )

        db.session.add(record)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء سجل الدين بنجاح",
                    "data": record.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating debt record: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_management_bp.route("/debt-payments", methods=["POST"])
def create_debt_payment():
    """إنشاء دفعة دين"""
    try:
        data = request.get_json()

        payment = DebtPayment(
            debt_record_id=data.get("debt_record_id"),
            payment_amount=data.get("payment_amount"),
            payment_method=data.get("payment_method"),
            payment_date=(
                datetime.fromisoformat(data.get("payment_date"))
                if data.get("payment_date")
                else datetime.utcnow()
            ),
            reference_number=data.get("reference_number"),
            notes=data.get("notes"),
        )

        db.session.add(payment)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم تسجيل الدفعة بنجاح",
                    "data": payment.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating debt payment: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_management_bp.route("/bank-accounts", methods=["GET"])
def get_bank_accounts():
    """الحصول على الحسابات البنكية"""
    try:
        accounts = BankAccount.query.all()

        return jsonify(
            {"status": "success", "data": [account.to_dict() for account in accounts]}
        )
    except Exception as e:
        logger.error(f"Error getting bank accounts: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_management_bp.route("/bank-accounts", methods=["POST"])
def create_bank_account():
    """إنشاء حساب بنكي جديد"""
    try:
        data = request.get_json()

        account = BankAccount(
            bank_name=data.get("bank_name"),
            account_number=data.get("account_number"),
            account_name=data.get("account_name"),
            iban=data.get("iban"),
            swift_code=data.get("swift_code"),
            currency=data.get("currency", "USD"),
            balance=data.get("balance", 0.0),
            is_active=data.get("is_active", True),
        )

        db.session.add(account)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء الحساب البنكي بنجاح",
                    "data": account.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating bank account: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@payment_management_bp.route("/statistics", methods=["GET"])
def get_payment_statistics():
    """الحصول على إحصائيات المدفوعات"""
    try:
        # إحصائيات أوامر الدفع
        total_orders = PaymentOrder.query.count()
        pending_orders = PaymentOrder.query.filter_by(status="pending").count()
        completed_orders = PaymentOrder.query.filter_by(status="completed").count()

        # إحصائيات الديون
        total_debts = DebtRecord.query.count()
        active_debts = DebtRecord.query.filter_by(status="active").count()

        # إجمالي المبالغ
        total_debt_amount = (
            db.session.query(db.func.sum(DebtRecord.debt_amount)).scalar() or 0
        )
        total_paid_amount = (
            db.session.query(db.func.sum(DebtPayment.payment_amount)).scalar() or 0
        )

        return jsonify(
            {
                "status": "success",
                "data": {
                    "orders": {
                        "total": total_orders,
                        "pending": pending_orders,
                        "completed": completed_orders,
                    },
                    "debts": {"total": total_debts, "active": active_debts},
                    "amounts": {
                        "total_debt": float(total_debt_amount),
                        "total_paid": float(total_paid_amount),
                        "remaining": float(total_debt_amount - total_paid_amount),
                    },
                },
            }
        )
    except Exception as e:
        logger.error(f"Error getting payment statistics: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
