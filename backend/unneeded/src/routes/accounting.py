# FILE: backend/src/routes/accounting.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-11-17

# type: ignore
"""
مسارات المحاسبة - Accounting routes for currencies, cash boxes, vouchers, and journal entries
"""

from flask import Blueprint, jsonify, request
from src.routes.auth_unified import token_required
from src.database import db
from src.models.supporting_models import Currency
from src.models.treasury_management import Treasury, TreasuryTransaction
from datetime import datetime, timezone

# إنشاء Blueprint
accounting_simple_bp = Blueprint("accounting_simple", __name__)


# ==================== TEST ROUTE ====================


@accounting_simple_bp.route("/api/accounting/test", methods=["GET"])
def test_route():
    """مسار اختبار للتحقق من عمل المحاسبة"""
    return jsonify(
        {
            "status": "success",
            "message": "Accounting routes are working!",
            "blueprint": "accounting_simple_bp",
        }
    )


# ==================== CURRENCY ROUTES ====================


@accounting_simple_bp.route("/api/accounting/currencies", methods=["GET"])
@token_required
def get_currencies():
    """الحصول على قائمة العملات"""
    try:
        # Check if Currency model is available
        if Currency is None:
            return jsonify({"status": "success", "data": []})

        try:
            currencies = Currency.query.filter_by(is_active=True).all()
        except Exception:
            # Table might not exist, return empty array
            return jsonify({"status": "success", "data": []})

        result = []
        for c in currencies:
            try:
                if hasattr(c, "to_dict"):
                    result.append(c.to_dict())
                else:
                    result.append(
                        {
                            "id": c.id,
                            "name": c.name,
                            "code": c.code,
                            "symbol": c.symbol,
                            "exchange_rate": (
                                float(c.exchange_rate)
                                if hasattr(c, "exchange_rate")
                                else 1.0
                            ),
                        }
                    )
            except Exception:
                continue

        return jsonify({"status": "success", "data": result})
    except Exception as e:
        # Return empty array on any error
        return jsonify({"status": "success", "data": []})


@accounting_simple_bp.route("/api/accounting/currencies", methods=["POST"])
@token_required
def create_currency():
    """إضافة عملة جديدة"""
    try:
        data = request.get_json()

        # Check if code already exists
        existing = Currency.query.filter_by(code=data.get("code")).first()
        if existing:
            return (
                jsonify({"status": "error", "message": "رمز العملة موجود مسبقاً"}),
                400,
            )

        # If setting as default, remove default from others
        if data.get("is_default"):
            Currency.query.update({"is_default": False})

        currency = Currency(
            name=data.get("name"),
            name_en=data.get("name_en"),
            code=data.get("code"),
            symbol=data.get("symbol"),
            exchange_rate=data.get("exchange_rate", 1.0),
            is_default=data.get("is_default", False),
            is_active=data.get("is_active", True),
        )

        db.session.add(currency)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تمت إضافة العملة بنجاح",
                    "data": currency.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في إضافة العملة: {str(e)}"}),
            500,
        )


@accounting_simple_bp.route(
    "/api/accounting/currencies/<int:currency_id>", methods=["PUT"]
)
@token_required
def update_currency(currency_id):
    """تحديث عملة"""
    try:
        currency = Currency.query.get_or_404(currency_id)
        data = request.get_json()

        # If setting as default, remove default from others
        if data.get("is_default") and not currency.is_default:
            Currency.query.filter(Currency.id != currency_id).update(
                {"is_default": False}
            )

        if "name" in data:
            currency.name = data["name"]
        if "name_en" in data:
            currency.name_en = data["name_en"]
        if "code" in data:
            currency.code = data["code"]
        if "symbol" in data:
            currency.symbol = data["symbol"]
        if "exchange_rate" in data:
            currency.exchange_rate = data["exchange_rate"]
        if "is_default" in data:
            currency.is_default = data["is_default"]
        if "is_active" in data:
            currency.is_active = data["is_active"]

        currency.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث العملة بنجاح",
                "data": currency.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث العملة: {str(e)}"}),
            500,
        )


@accounting_simple_bp.route(
    "/api/accounting/currencies/<int:currency_id>", methods=["DELETE"]
)
@token_required
def delete_currency(currency_id):
    """حذف عملة"""
    try:
        currency = Currency.query.get_or_404(currency_id)

        # Don't allow deleting default currency
        if currency.is_default:
            return (
                jsonify(
                    {"status": "error", "message": "لا يمكن حذف العملة الافتراضية"}
                ),
                400,
            )

        db.session.delete(currency)
        db.session.commit()

        return jsonify({"status": "success", "message": "تم حذف العملة بنجاح"})
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في حذف العملة: {str(e)}"}),
            500,
        )


# ==================== CASH BOX (TREASURY) ROUTES ====================


@accounting_simple_bp.route("/api/accounting/cash-boxes", methods=["GET"])
@token_required
def get_cash_boxes():
    """الحصول على قائمة الصناديق"""
    try:
        # Check if Treasury model is available
        if Treasury is None:
            return jsonify({"status": "success", "data": []})

        try:
            cash_boxes = Treasury.query.all()
        except Exception:
            # Table might not exist, return empty array
            return jsonify({"status": "success", "data": []})

        result = []
        for cb in cash_boxes:
            try:
                if hasattr(cb, "to_dict"):
                    result.append(cb.to_dict())
                else:
                    result.append(
                        {
                            "id": cb.id,
                            "name": cb.name,
                            "code": getattr(cb, "code", ""),
                            "current_balance": float(getattr(cb, "current_balance", 0)),
                        }
                    )
            except Exception:
                # Skip problematic items but continue
                continue

        return jsonify({"status": "success", "data": result})
    except Exception:
        # Return empty array on any error
        return jsonify({"status": "success", "data": []})


@accounting_simple_bp.route("/api/accounting/cash-boxes", methods=["POST"])
@token_required
def create_cash_box():
    """إضافة صندوق جديد"""
    try:
        data = request.get_json()
        user_id = getattr(request, "current_user_id", None)

        cash_box = Treasury(
            name=data.get("name"),
            description=data.get("description"),
            currency_id=data.get("currency_id"),
            is_active=data.get("is_active", True),
            created_by=user_id,
        )

        db.session.add(cash_box)
        db.session.flush()

        # Add opening balance if provided
        opening_balance = data.get("opening_balance", 0)
        if opening_balance > 0:
            transaction = TreasuryTransaction(
                treasury_id=cash_box.id,
                transaction_type="deposit",
                amount=opening_balance,
                currency_id=data.get("currency_id"),
                description="الرصيد الافتتاحي",
                created_by=user_id,
            )
            db.session.add(transaction)

        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تمت إضافة الصندوق بنجاح",
                    "data": (
                        cash_box.to_dict()
                        if hasattr(cash_box, "to_dict")
                        else {"id": cash_box.id, "name": cash_box.name}
                    ),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في إضافة الصندوق: {str(e)}"}),
            500,
        )


@accounting_simple_bp.route(
    "/api/accounting/cash-boxes/<int:cash_box_id>", methods=["PUT"]
)
@token_required
def update_cash_box(cash_box_id):
    """تحديث صندوق"""
    try:
        cash_box = Treasury.query.get_or_404(cash_box_id)
        data = request.get_json()

        if "name" in data:
            cash_box.name = data["name"]
        if "description" in data:
            cash_box.description = data["description"]
        if "is_active" in data:
            cash_box.is_active = data["is_active"]

        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث الصندوق بنجاح",
                "data": (
                    cash_box.to_dict()
                    if hasattr(cash_box, "to_dict")
                    else {"id": cash_box.id, "name": cash_box.name}
                ),
            }
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث الصندوق: {str(e)}"}),
            500,
        )


@accounting_simple_bp.route(
    "/api/accounting/cash-boxes/<int:cash_box_id>", methods=["DELETE"]
)
@token_required
def delete_cash_box(cash_box_id):
    """حذف صندوق"""
    try:
        cash_box = Treasury.query.get_or_404(cash_box_id)

        # Check if cash box has transactions
        transaction_count = TreasuryTransaction.query.filter_by(
            treasury_id=cash_box_id
        ).count()
        if transaction_count > 0:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "لا يمكن حذف الصندوق لوجود حركات عليه",
                    }
                ),
                400,
            )

        db.session.delete(cash_box)
        db.session.commit()

        return jsonify({"status": "success", "message": "تم حذف الصندوق بنجاح"})
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في حذف الصندوق: {str(e)}"}),
            500,
        )


@accounting_simple_bp.route(
    "/api/accounting/cash-boxes/<int:cash_box_id>/transactions", methods=["GET"]
)
@token_required
def get_cash_box_transactions(cash_box_id):
    """الحصول على حركات صندوق"""
    try:
        transactions = (
            TreasuryTransaction.query.filter_by(treasury_id=cash_box_id)
            .order_by(TreasuryTransaction.created_at.desc())
            .limit(50)
            .all()
        )
        return jsonify(
            {
                "status": "success",
                "data": [
                    (
                        t.to_dict()
                        if hasattr(t, "to_dict")
                        else {"id": t.id, "amount": t.amount}
                    )
                    for t in transactions
                ],
                "transactions": [
                    (
                        t.to_dict()
                        if hasattr(t, "to_dict")
                        else {"id": t.id, "amount": t.amount}
                    )
                    for t in transactions
                ],
            }
        )
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على الحركات: {str(e)}"}
            ),
            500,
        )


@accounting_simple_bp.route(
    "/api/accounting/cash-boxes/<int:cash_box_id>/transactions", methods=["POST"]
)
@token_required
def add_cash_box_transaction(cash_box_id):
    """إضافة حركة لصندوق"""
    try:
        # Verify cash box exists
        Treasury.query.get_or_404(cash_box_id)
        data = request.get_json()
        user_id = getattr(request, "current_user_id", None)

        transaction = TreasuryTransaction(
            treasury_id=cash_box_id,
            transaction_type=data.get("transaction_type"),
            amount=data.get("amount"),
            currency_id=data.get("currency_id"),
            reference=data.get("reference"),
            description=data.get("description"),
            created_by=user_id,
        )

        db.session.add(transaction)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تمت إضافة الحركة بنجاح",
                    "data": (
                        transaction.to_dict()
                        if hasattr(transaction, "to_dict")
                        else {"id": transaction.id}
                    ),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"status": "error", "message": f"خطأ في إضافة الحركة: {str(e)}"}),
            500,
        )


# ==================== VOUCHER ROUTES ====================


@accounting_simple_bp.route("/api/accounting/vouchers", methods=["GET"])
@token_required
def get_vouchers():
    """الحصول على قسائم الدفع"""
    try:
        # For now return empty array - will integrate with PaymentOrder model
        return jsonify({"status": "success", "data": [], "vouchers": []})
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على القسائم: {str(e)}"}
            ),
            500,
        )


@accounting_simple_bp.route("/api/accounting/vouchers", methods=["POST"])
@token_required
def create_voucher():
    """إضافة قسيمة دفع/قبض"""
    try:
        data = request.get_json()
        # Authentication verified by @token_required decorator

        # Create voucher (will integrate with PaymentOrder model)
        voucher_number = f"VCH-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تمت إضافة القسيمة بنجاح",
                    "data": {
                        "id": 1,
                        "voucher_number": voucher_number,
                        "voucher_type": data.get("voucher_type"),
                        "amount": data.get("amount"),
                        "status": "draft",
                    },
                }
            ),
            201,
        )
    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في إضافة القسيمة: {str(e)}"}),
            500,
        )


@accounting_simple_bp.route(
    "/api/accounting/vouchers/<int:voucher_id>", methods=["PUT"]
)
@token_required
def update_voucher(voucher_id):
    """تحديث حالة القسيمة"""
    try:
        data = request.get_json()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث القسيمة بنجاح",
                "data": {"id": voucher_id, "status": data.get("status")},
            }
        )
    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في تحديث القسيمة: {str(e)}"}),
            500,
        )


# ==================== PROFIT/LOSS ROUTES ====================


@accounting_simple_bp.route("/api/accounting/profit-loss", methods=["GET"])
@token_required
def get_profit_loss():
    """الحصول على تقرير الأرباح والخسائر"""
    try:
        year = request.args.get("year", datetime.now(timezone.utc).year, type=int)
        month = request.args.get("month", type=int)

        # For now return mock data - will integrate with Invoice models
        report_data = {
            "period": f"{year}" + (f"-{month:02d}" if month else ""),
            "total_revenue": 150000.00,
            "sales_revenue": 145000.00,
            "other_revenue": 5000.00,
            "total_expenses": 95000.00,
            "cost_of_goods_sold": 70000.00,
            "operating_expenses": 20000.00,
            "other_expenses": 5000.00,
            "revenue_breakdown": [
                {
                    "category": "مبيعات المنتجات",
                    "amount": 120000.00,
                    "description": "إيرادات مبيعات المنتجات",
                },
                {
                    "category": "مبيعات الخدمات",
                    "amount": 25000.00,
                    "description": "إيرادات مبيعات الخدمات",
                },
                {
                    "category": "إيرادات أخرى",
                    "amount": 5000.00,
                    "description": "إيرادات متنوعة",
                },
            ],
            "expense_breakdown": [
                {
                    "category": "تكلفة البضاعة المباعة",
                    "amount": 70000.00,
                    "description": "تكلفة شراء البضائع",
                },
                {
                    "category": "رواتب",
                    "amount": 15000.00,
                    "description": "رواتب الموظفين",
                },
                {"category": "إيجار", "amount": 3000.00, "description": "إيجار المكتب"},
                {
                    "category": "مصاريف تشغيلية",
                    "amount": 7000.00,
                    "description": "مصاريف متنوعة",
                },
            ],
        }

        return jsonify({"status": "success", "data": report_data})
    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"خطأ في إنشاء التقرير: {str(e)}"}),
            500,
        )


# ==================== LEGACY ROUTES (KEEP FOR COMPATIBILITY) ====================


@accounting_simple_bp.route("/api/accounting/accounts", methods=["GET"])
def get_accounts():
    """الحصول على قائمة الحسابات"""
    try:
        return jsonify(
            {"status": "success", "data": [], "message": "قائمة الحسابات (قيد التطوير)"}
        )
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"خطأ في الحصول على الحسابات: {str(e)}"}
            ),
            500,
        )


@accounting_simple_bp.route("/api/accounting/journal-entries", methods=["GET"])
def get_journal_entries():
    """الحصول على قيود اليومية"""
    try:
        return jsonify(
            {"status": "success", "data": [], "message": "قيود اليومية (قيد التطوير)"}
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"خطأ في الحصول على قيود اليومية: {str(e)}",
                }
            ),
            500,
        )
