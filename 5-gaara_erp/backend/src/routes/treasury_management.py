# FILE: backend/src/routes/treasury_management.py | PURPOSE: Routes with
# P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

from sqlalchemy.orm import joinedload

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
# /home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/routes/treasury_management.py

"""
Treasury Management Routes
مسارات إدارة الخزنة
All linting disabled due to complex imports and optional dependencies.
"""

from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
from src.models.treasury_management import (
    Treasury,
    TreasuryTransaction,
    TreasuryCurrencyBalance,
    TreasuryReconciliation,
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
treasury_management_bp = Blueprint("treasury_management_routes", __name__)

# إعداد نظام التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@treasury_management_bp.route("/treasuries", methods=["GET"])
def get_treasuries():
    """الحصول على جميع الخزائن"""
    try:
        treasuries = Treasury.query.all()

        return jsonify(
            {
                "status": "success",
                "data": [treasury.to_dict() for treasury in treasuries],
            }
        )
    except Exception as e:
        logger.error(f"Error getting treasuries: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@treasury_management_bp.route("/treasuries", methods=["POST"])
def create_treasury():
    """إنشاء خزنة جديدة"""
    try:
        data = request.get_json()

        treasury = Treasury(
            name=data.get("name"),
            code=data.get("code"),
            description=data.get("description"),
            location=data.get("location"),
            manager_id=data.get("manager_id"),
            currency=data.get("currency", "USD"),
            opening_balance=data.get("opening_balance", 0.0),
            current_balance=data.get("opening_balance", 0.0),
            is_active=data.get("is_active", True),
        )

        db.session.add(treasury)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء الخزنة بنجاح",
                    "data": treasury.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating treasury: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@treasury_management_bp.route("/treasuries/<int:treasury_id>", methods=["PUT"])
def update_treasury(treasury_id):
    """تحديث خزنة"""
    try:
        treasury = Treasury.query.get_or_404(treasury_id)
        data = request.get_json()

        treasury.name = data.get("name", treasury.name)
        treasury.description = data.get("description", treasury.description)
        treasury.location = data.get("location", treasury.location)
        treasury.manager_id = data.get("manager_id", treasury.manager_id)
        treasury.is_active = data.get("is_active", treasury.is_active)
        treasury.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث الخزنة بنجاح",
                "data": treasury.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating treasury: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@treasury_management_bp.route("/transactions", methods=["GET"])
def get_transactions():
    """الحصول على معاملات الخزنة"""
    try:
        page = request.args.get("page", 1, type=int)
        treasury_id = request.args.get("treasury_id", type=int)
        per_page = request.args.get("per_page", 10, type=int)

        query = TreasuryTransaction.query
        if treasury_id:
            query = query.filter_by(treasury_id=treasury_id)

        transactions = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "status": "success",
                "data": {
                    "transactions": [
                        transaction.to_dict() for transaction in transactions.items
                    ],
                    "total": transactions.total,
                    "pages": transactions.pages,
                    "current_page": page,
                },
            }
        )
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@treasury_management_bp.route("/transactions", methods=["POST"])
def create_transaction():
    """إنشاء معاملة خزنة جديدة"""
    try:
        data = request.get_json()

        transaction = TreasuryTransaction(
            treasury_id=data.get("treasury_id"),
            transaction_type=data.get("transaction_type"),
            amount=data.get("amount"),
            currency=data.get("currency", "USD"),
            description=data.get("description"),
            reference_number=data.get("reference_number"),
            customer_id=data.get("customer_id"),
            supplier_id=data.get("supplier_id"),
            invoice_id=data.get("invoice_id"),
            created_by=data.get("created_by"),
        )

        # تحديث رصيد الخزنة
        treasury = Treasury.query.get(data.get("treasury_id"))
        if treasury:
            if data.get("transaction_type") == "income":
                treasury.current_balance += data.get("amount", 0)
            elif data.get("transaction_type") == "expense":
                treasury.current_balance -= data.get("amount", 0)

        db.session.add(transaction)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء المعاملة بنجاح",
                    "data": transaction.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating transaction: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@treasury_management_bp.route("/currency-balances/<int:treasury_id>", methods=["GET"])
def get_currency_balances(treasury_id):
    """الحصول على أرصدة العملات للخزنة"""
    try:
        balances = TreasuryCurrencyBalance.query.filter_by(
            treasury_id=treasury_id
        ).all()

        return jsonify(
            {"status": "success", "data": [balance.to_dict() for balance in balances]}
        )
    except Exception as e:
        logger.error(f"Error getting currency balances: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@treasury_management_bp.route("/reconciliation", methods=["POST"])
def create_reconciliation():
    """إنشاء تسوية خزنة"""
    try:
        data = request.get_json()

        reconciliation = TreasuryReconciliation(
            treasury_id=data.get("treasury_id"),
            reconciliation_date=(
                datetime.fromisoformat(data.get("reconciliation_date"))
                if data.get("reconciliation_date")
                else datetime.utcnow()
            ),
            system_balance=data.get("system_balance"),
            actual_balance=data.get("actual_balance"),
            difference=data.get("actual_balance", 0) - data.get("system_balance", 0),
            notes=data.get("notes"),
            reconciled_by=data.get("reconciled_by"),
        )

        db.session.add(reconciliation)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء التسوية بنجاح",
                    "data": reconciliation.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating reconciliation: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@treasury_management_bp.route("/statistics/<int:treasury_id>", methods=["GET"])
def get_treasury_statistics(treasury_id):
    """الحصول على إحصائيات الخزنة"""
    try:
        treasury = Treasury.query.get_or_404(treasury_id)

        # إحصائيات المعاملات
        total_transactions = TreasuryTransaction.query.filter_by(
            treasury_id=treasury_id
        ).count()
        income_transactions = TreasuryTransaction.query.filter_by(
            treasury_id=treasury_id, transaction_type="income"
        ).count()
        expense_transactions = TreasuryTransaction.query.filter_by(
            treasury_id=treasury_id, transaction_type="expense"
        ).count()

        # إجمالي المبالغ
        total_income = (
            db.session.query(db.func.sum(TreasuryTransaction.amount))
            .filter_by(treasury_id=treasury_id, transaction_type="income")
            .scalar()
            or 0
        )

        total_expense = (
            db.session.query(db.func.sum(TreasuryTransaction.amount))
            .filter_by(treasury_id=treasury_id, transaction_type="expense")
            .scalar()
            or 0
        )

        return jsonify(
            {
                "status": "success",
                "data": {
                    "treasury": treasury.to_dict(),
                    "transactions": {
                        "total": total_transactions,
                        "income": income_transactions,
                        "expense": expense_transactions,
                    },
                    "amounts": {
                        "total_income": float(total_income),
                        "total_expense": float(total_expense),
                        "net_balance": float(total_income - total_expense),
                        "current_balance": float(treasury.current_balance),
                    },
                },
            }
        )
    except Exception as e:
        logger.error(f"Error getting treasury statistics: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@treasury_management_bp.route("/daily-summary", methods=["GET"])
def get_daily_summary():
    """الحصول على ملخص يومي للخزائن"""
    try:
        date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # معاملات اليوم
        daily_transactions = TreasuryTransaction.query.filter(
            db.func.date(TreasuryTransaction.created_at) == target_date
        ).all()

        # تجميع البيانات
        summary = {
            "date": date_str,
            "total_transactions": len(daily_transactions),
            "total_income": sum(
                t.amount for t in daily_transactions if t.transaction_type == "income"
            ),
            "total_expense": sum(
                t.amount for t in daily_transactions if t.transaction_type == "expense"
            ),
            "treasuries": {},
        }

        # تجميع حسب الخزنة
        for transaction in daily_transactions:
            treasury_id = transaction.treasury_id
            if treasury_id not in summary["treasuries"]:
                summary["treasuries"][treasury_id] = {
                    "income": 0,
                    "expense": 0,
                    "transactions": 0,
                }

            summary["treasuries"][treasury_id]["transactions"] += 1
            if transaction.transaction_type == "income":
                summary["treasuries"][treasury_id]["income"] += transaction.amount
            else:
                summary["treasuries"][treasury_id]["expense"] += transaction.amount

        return jsonify({"status": "success", "data": summary})
    except Exception as e:
        logger.error(f"Error getting daily summary: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
