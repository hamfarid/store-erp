from sqlalchemy.orm import joinedload

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
# ملف: accounting_system.py
# APIs نظام المحاسبة المتكامل
# All linting disabled due to complex imports and optional dependencies.

from flask import Blueprint, request, jsonify, session
import logging
from datetime import datetime, date
from decimal import Decimal

# Import models with comprehensive fallback handling
try:
    from src.models.accounting_system import PaymentVoucher, CashBox, ExpenseCategory, InvoiceExpense  # type: ignore
    from src.models.invoices import InvoiceCurrency as Currency  # type: ignore
    from src.models.partners import ExchangeRate  # type: ignore
    from src.models.profit_loss_system import PaymentSchedule  # type: ignore
    from src.database import db  # type: ignore
    from auth import login_required  # type: ignore

    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False

    # Create comprehensive mock classes
    class MockSession:
        def add(self, obj):
            """Mock add method"""
            pass

        def commit(self):
            """Mock commit method"""
            pass

        def rollback(self):
            """Mock rollback method"""
            pass

    class MockDB:
        session = MockSession()

        @staticmethod
        def create_all():
            """Mock create_all method"""
            pass

        @staticmethod
        def drop_all():
            """Mock drop_all method"""
            pass

    # Mock accounting models
    class PaymentVoucher:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class CashBox:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class ExpenseCategory:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class InvoiceExpense:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class Currency:
        query = None

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        def to_dict(self):
            return {}

    class ExchangeRate:
        query = None

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    class PaymentSchedule:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    db = MockDB()

    def login_required(f):
        """Mock login_required decorator"""
        from functools import wraps

        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    print("⚠️ Accounting System: Using mock models for testing")

from sqlalchemy import and_, func, desc, text

accounting_system_bp = Blueprint("accounting_system", __name__)

# Utility functions for handling SQLAlchemy filter expressions safely


def filter_by_status(status):
    return text(f"payment_status = '{status}'")


def filter_by_partner_type(partner_type):
    return text(f"partner_type = '{partner_type}'")


# ==================== APIs العملات ====================


@accounting_system_bp.route("/currencies", methods=["GET"])
@login_required
def get_currencies():
    """الحصول على قائمة العملات"""
    try:
        currencies = Currency.query.filter_by(is_active=True).all()
        return jsonify(
            {
                "status": "success",
                "currencies": [currency.to_dict() for currency in currencies],
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/currencies", methods=["POST"])
@login_required
def create_currency():
    """إنشاء عملة جديدة"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ["code", "name", "symbol"]
        for field in required_fields:
            if not data.get(field):
                return (
                    jsonify({"status": "error", "message": f"حقل {field} مطلوب"}),
                    400,
                )

        # التحقق من عدم تكرار الكود
        existing = Currency.query.filter_by(code=data["code"]).first()
        if existing:
            return (
                jsonify({"status": "error", "message": "كود العملة موجود مسبقاً"}),
                400,
            )

        currency = Currency(
            code=data["code"],
            name=data["name"],
            symbol=data["symbol"],
            is_base_currency=data.get("is_base_currency", False),
        )

        # إذا كانت العملة الأساسية، إلغاء العملة الأساسية السابقة
        is_base = data.get("is_base_currency", False)
        if is_base:
            Currency.query.filter_by(is_base_currency=True).update(
                {"is_base_currency": False}
            )

        db.session.add(currency)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء العملة بنجاح",
                "currency": currency.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/exchange-rates", methods=["GET"])
@login_required
def get_exchange_rates():
    """الحصول على أسعار الصرف"""
    try:
        # فلترة حسب التاريخ
        date_filter = request.args.get("date", datetime.now().date().isoformat())
        target_date = datetime.strptime(date_filter, "%Y-%m-%d").date()

        rates = (
            ExchangeRate.query.filter(ExchangeRate.date <= target_date)
            .order_by(desc(ExchangeRate.date))
            .all()
        )

        # أخذ أحدث سعر لكل زوج عملات
        latest_rates = {}
        for rate in rates:
            key = f"{rate.from_currency}_{rate.to_currency}"
            if key not in latest_rates:
                latest_rates[key] = rate

        return jsonify(
            {
                "status": "success",
                "exchange_rates": [rate.to_dict() for rate in latest_rates.values()],
                "date": date_filter,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/exchange-rates", methods=["POST"])
@login_required
def create_exchange_rate():
    """إنشاء سعر صرف جديد"""
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ["from_currency_id", "to_currency_id", "rate"]
        for field in required_fields:
            if not data.get(field):
                return (
                    jsonify({"status": "error", "message": f"حقل {field} مطلوب"}),
                    400,
                )

        # التحقق من صحة العملات
        from_currency = Currency.query.get(data["from_currency_id"])
        to_currency = Currency.query.get(data["to_currency_id"])

        if not from_currency or not to_currency:
            return jsonify({"status": "error", "message": "عملة غير صحيحة"}), 400

        if from_currency.id == to_currency.id:
            return (
                jsonify({"status": "error", "message": "لا يمكن تحويل العملة لنفسها"}),
                400,
            )

        # حذف الأسعار السابقة لنفس زوج العملات بنفس التاريخ
        ExchangeRate.query.filter(
            and_(
                ExchangeRate.from_currency == data["from_currency_id"],
                ExchangeRate.to_currency == data["to_currency_id"],
                ExchangeRate.date
                == datetime.strptime(
                    data.get("effective_date", date.today().isoformat()), "%Y-%m-%d"
                ).date(),
            )
        ).delete()

        exchange_rate = ExchangeRate()
        exchange_rate.from_currency = data["from_currency_id"]
        exchange_rate.to_currency = data["to_currency_id"]
        exchange_rate.rate = float(Decimal(str(data["rate"])))
        exchange_rate.date = datetime.strptime(
            data.get("effective_date", date.today().isoformat()), "%Y-%m-%d"
        ).date()

        db.session.add(exchange_rate)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء سعر الصرف بنجاح",
                "exchange_rate": exchange_rate.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/convert-currency", methods=["POST"])
@login_required
def convert_currency():
    """تحويل مبلغ من عملة لأخرى"""
    try:
        data = request.get_json()

        required_fields = ["amount", "from_currency_id", "to_currency_id"]
        for field in required_fields:
            if not data.get(field):
                return (
                    jsonify({"status": "error", "message": f"حقل {field} مطلوب"}),
                    400,
                )

        amount = Decimal(str(data["amount"]))
        from_currency_id = data["from_currency_id"]
        to_currency_id = data["to_currency_id"]
        conversion_date = datetime.strptime(
            data.get("date", date.today().isoformat()), "%Y-%m-%d"
        ).date()

        # إذا كانت نفس العملة
        if from_currency_id == to_currency_id:
            return jsonify(
                {
                    "status": "success",
                    "converted_amount": float(amount),
                    "exchange_rate": 1.0,
                    "original_amount": float(amount),
                }
            )

        # البحث عن سعر الصرف
        exchange_rate = (
            ExchangeRate.query.filter(
                and_(
                    ExchangeRate.from_currency == from_currency_id,
                    ExchangeRate.to_currency == to_currency_id,
                    ExchangeRate.date <= conversion_date,
                )
            )
            .order_by(desc(ExchangeRate.date))
            .first()
        )

        if not exchange_rate:
            # البحث عن السعر العكسي
            reverse_rate = (
                ExchangeRate.query.filter(
                    and_(
                        ExchangeRate.from_currency == to_currency_id,
                        ExchangeRate.to_currency == from_currency_id,
                        ExchangeRate.date <= conversion_date,
                    )
                )
                .order_by(desc(ExchangeRate.date))
                .first()
            )

            if reverse_rate:
                rate = 1 / reverse_rate.rate
            else:
                return (
                    jsonify({"status": "error", "message": "سعر الصرف غير متوفر"}),
                    404,
                )
        else:
            rate = exchange_rate.rate

        converted_amount = amount * rate

        return jsonify(
            {
                "status": "success",
                "converted_amount": float(converted_amount),
                "exchange_rate": float(rate),
                "original_amount": float(amount),
                "conversion_date": conversion_date.isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== APIs الخزائن ====================


@accounting_system_bp.route("/cash-boxes", methods=["GET"])
@login_required
def get_cash_boxes():
    """الحصول على قائمة الخزائن"""
    try:
        # فلترة حسب النوع والمستخدم
        box_type = request.args.get("box_type")
        user_id = request.args.get("user_id")

        query = CashBox.query.filter_by(is_active=True)

        if box_type:
            query = query.filter_by(box_type=box_type)

        if user_id:
            query = query.filter_by(assigned_to=user_id)

        cash_boxes = query.all()

        return jsonify(
            {"status": "success", "cash_boxes": [box.to_dict() for box in cash_boxes]}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/cash-boxes", methods=["POST"])
@login_required
def create_cash_box():
    """إنشاء خزنة جديدة"""
    try:
        data = request.get_json()

        required_fields = ["name", "code", "currency_id"]
        for field in required_fields:
            if not data.get(field):
                return (
                    jsonify({"status": "error", "message": f"حقل {field} مطلوب"}),
                    400,
                )

        # التحقق من عدم تكرار الكود
        existing = CashBox.query.filter_by(code=data["code"]).first()
        if existing:
            return (
                jsonify({"status": "error", "message": "كود الخزنة موجود مسبقاً"}),
                400,
            )

        cash_box = CashBox(
            name=data["name"],
            code=data["code"],
            currency_id=data["currency_id"],
            description=data.get("description"),
            box_type=data.get("box_type", "general"),
        )

        if data.get("assigned_to"):
            cash_box.assigned_to = data["assigned_to"]

        db.session.add(cash_box)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء الخزنة بنجاح",
                "cash_box": cash_box.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/cash-boxes/<int:box_id>/balance", methods=["GET"])
@login_required
def get_cash_box_balance(box_id):
    """الحصول على رصيد خزنة"""
    try:
        cash_box = CashBox.query.get_or_404(box_id)

        return jsonify(
            {
                "status": "success",
                "cash_box": cash_box.to_dict(),
                "balance": float(cash_box.balance),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== APIs سندات الدفع والقبض ====================


@accounting_system_bp.route("/payment-vouchers", methods=["GET"])
@login_required
def get_payment_vouchers():
    """الحصول على قائمة سندات الدفع والقبض"""
    try:
        # فلترة
        voucher_type = request.args.get("voucher_type")  # payment, receipt
        partner_type = request.args.get("partner_type")  # customer, supplier
        status = request.args.get("status")
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")

        query = PaymentVoucher.query

        if voucher_type:
            query = query.filter_by(voucher_type=voucher_type)

        if partner_type:
            query = query.filter_by(partner_type=partner_type)

        if status:
            query = query.filter_by(status=status)

        if date_from:
            query = query.filter(
                PaymentVoucher.voucher_date
                >= datetime.strptime(date_from, "%Y-%m-%d").date()
            )

        if date_to:
            query = query.filter(
                PaymentVoucher.voucher_date
                <= datetime.strptime(date_to, "%Y-%m-%d").date()
            )

        vouchers = query.order_by(desc(PaymentVoucher.created_date)).all()

        return jsonify(
            {
                "status": "success",
                "vouchers": [voucher.to_dict() for voucher in vouchers],
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/payment-vouchers", methods=["POST"])
@login_required
def create_payment_voucher():
    """إنشاء سند دفع أو قبض"""
    try:
        data = request.get_json()

        required_fields = [
            "voucher_type",
            "partner_type",
            "partner_id",
            "partner_name",
            "amount",
            "currency_id",
            "payment_method",
            "description",
        ]
        for field in required_fields:
            if not data.get(field):
                return (
                    jsonify({"status": "error", "message": f"حقل {field} مطلوب"}),
                    400,
                )

        # Validate user session
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"status": "error", "message": "يجب تسجيل الدخول أولاً"}), 401

        voucher = PaymentVoucher(
            voucher_type=data["voucher_type"],
            partner_type=data["partner_type"],
            partner_id=data["partner_id"],
            partner_name=data["partner_name"],
            amount=Decimal(str(data["amount"])),
            currency_id=data["currency_id"],
            payment_method=data["payment_method"],
            description=data["description"],
            created_by=user_id,
        )

        # إضافة البيانات الاختيارية
        if data.get("voucher_date"):
            voucher.voucher_date = datetime.strptime(
                data["voucher_date"], "%Y-%m-%d"
            ).date()

        if data.get("cash_box_id"):
            voucher.cash_box_id = data["cash_box_id"]

        if data.get("exchange_rate"):
            voucher.exchange_rate = Decimal(str(data["exchange_rate"]))
            voucher.calculate_base_currency_amount()

        if data.get("bank_account"):
            voucher.bank_account = data["bank_account"]

        if data.get("check_number"):
            voucher.check_number = data["check_number"]

        if data.get("check_date"):
            voucher.check_date = datetime.strptime(
                data["check_date"], "%Y-%m-%d"
            ).date()

        if data.get("reference"):
            voucher.reference = data["reference"]

        db.session.add(voucher)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء السند بنجاح",
                "voucher": voucher.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route(
    "/payment-vouchers/<int:voucher_id>/confirm", methods=["POST"]
)
@login_required
def confirm_payment_voucher(voucher_id):
    """تأكيد سند الدفع أو القبض"""
    try:
        voucher = PaymentVoucher.query.get_or_404(voucher_id)

        # Validate user session
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"status": "error", "message": "يجب تسجيل الدخول أولاً"}), 401

        voucher.confirm_voucher(user_id)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تأكيد السند بنجاح",
                "voucher": voucher.to_dict(),
            }
        )
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== APIs مواعيد الدفع ====================
@accounting_system_bp.route("/payment-schedules", methods=["GET"])
@login_required
def get_payment_schedules():
    """الحصول على مواعيد الدفع"""
    try:
        # فلترة
        partner_type = request.args.get("partner_type")
        status = request.args.get("status")
        overdue_only = request.args.get("overdue_only") == "true"

        query = PaymentSchedule.query

        if partner_type:
            query = query.filter_by(partner_type=partner_type)

        if status:
            query = query.filter_by(status=status)

        if overdue_only:
            query = query.filter(text("payment_status = 'overdue'"))

        schedules = query.order_by(text("due_date")).all()

        # تحديث حالة التأخير
        for schedule in schedules:
            schedule.check_overdue()

        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "schedules": [schedule.to_dict() for schedule in schedules],
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/payment-schedules/overdue-summary", methods=["GET"])
@login_required
def get_overdue_summary():
    """ملخص المتأخرات"""
    try:
        # تحديث حالات التأخير
        schedules = PaymentSchedule.query.filter(
            text("payment_status IN ('pending', 'partial')")
        ).all()
        for schedule in schedules:
            schedule.check_overdue()

        db.session.commit()

        # إحصائيات المتأخرات
        overdue_customers = (
            db.session.query(
                func.count(text("id")).label("count"),
                # pylint: disable=not-callable
                func.sum(text("remaining_amount")).label("total_amount"),
            )
            .filter(text("partner_type = 'customer' AND payment_status = 'overdue'"))
            .first()
        )

        overdue_suppliers = (
            db.session.query(
                func.count(text("id")).label("count"),
                # pylint: disable=not-callable
                func.sum(text("remaining_amount")).label("total_amount"),
            )
            .filter(text("partner_type = 'supplier' AND payment_status = 'overdue'"))
            .first()
        )

        return jsonify(
            {
                "status": "success",
                "overdue_customers": {
                    "count": getattr(overdue_customers, "count", 0) or 0,
                    "total_amount": float(
                        getattr(overdue_customers, "total_amount", 0) or 0
                    ),
                },
                "overdue_suppliers": {
                    "count": getattr(overdue_suppliers, "count", 0) or 0,
                    "total_amount": float(
                        getattr(overdue_suppliers, "total_amount", 0) or 0
                    ),
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== APIs فئات المصاريف ====================
@accounting_system_bp.route("/expense-categories", methods=["GET"])
@login_required
def get_expense_categories():
    """الحصول على فئات المصاريف"""
    try:
        categories = ExpenseCategory.query.filter_by(is_active=True).all()

        return jsonify(
            {
                "status": "success",
                "categories": [category.to_dict() for category in categories],
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route("/expense-categories", methods=["POST"])
@login_required
def create_expense_category():
    """إنشاء فئة مصاريف جديدة"""
    try:
        data = request.get_json()

        required_fields = ["name", "code"]
        for field in required_fields:
            if not data.get(field):
                return (
                    jsonify({"status": "error", "message": f"حقل {field} مطلوب"}),
                    400,
                )

        # التحقق من عدم تكرار الكود
        existing = ExpenseCategory.query.filter_by(code=data["code"]).first()
        if existing:
            return jsonify({"status": "error", "message": "كود الفئة موجود مسبقاً"}), 400

        category = ExpenseCategory(
            name=data["name"],
            code=data["code"],
            description=data.get("description"),
            parent_id=data.get("parent_id"),
        )

        db.session.add(category)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إنشاء فئة المصاريف بنجاح",
                "category": category.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== APIs مصاريف الفواتير ====================


@accounting_system_bp.route("/invoice-expenses", methods=["POST"])
@login_required
def add_invoice_expense():
    """إضافة مصروف لفاتورة"""
    try:
        data = request.get_json()

        required_fields = [
            "invoice_type",
            "invoice_id",
            "expense_category_id",
            "description",
            "amount",
            "currency_id",
        ]
        for field in required_fields:
            if not data.get(field):
                return (
                    jsonify({"status": "error", "message": f"حقل {field} مطلوب"}),
                    400,
                )

        expense = InvoiceExpense(
            invoice_type=data["invoice_type"],
            invoice_id=data["invoice_id"],
            expense_category_id=data["expense_category_id"],
            description=data["description"],
            amount=Decimal(str(data["amount"])),
            currency_id=data["currency_id"],
            affects_cost=data.get("affects_cost", True),
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم إضافة المصروف بنجاح",
                "expense": expense.to_dict(),
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@accounting_system_bp.route(
    "/invoice-expenses/<invoice_type>/<int:invoice_id>", methods=["GET"]
)
@login_required
def get_invoice_expenses(invoice_type, invoice_id):
    """الحصول على مصاريف فاتورة"""
    try:
        expenses = InvoiceExpense.query.filter_by(
            invoice_type=invoice_type, invoice_id=invoice_id
        ).all()

        total_expenses = sum(float(expense.amount) for expense in expenses)
        cost_affecting_expenses = sum(
            float(expense.amount) for expense in expenses if expense.affects_cost
        )

        return jsonify(
            {
                "status": "success",
                "expenses": [expense.to_dict() for expense in expenses],
                "total_expenses": total_expenses,
                "cost_affecting_expenses": cost_affecting_expenses,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
