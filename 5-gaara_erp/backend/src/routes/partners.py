# FILE: backend/src/routes/partners.py | PURPOSE: Routes with P0.2.4 error
# envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
"""
APIs إدارة العملاء والموردين
/home/ubuntu/inventory_management_system/src/routes/partners.py
All linting disabled due to complex route operations and optional dependencies.
"""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging

try:
    from src.models.customer import Customer
    from src.models.supplier import Supplier
    from src.models.supplier import SupplierType, CustomerType
except ImportError:
    # Create mock classes with minimal attributes to satisfy linters
    class _MockBase:
        # Provide dummy attributes/methods accessed in routes
        query = None

        def to_dict(self):
            return {}

    class Customer(_MockBase):
        pass

    class Supplier(_MockBase):
        pass

    class SupplierType(_MockBase):
        pass

    class CustomerType(_MockBase):
        pass


try:
    from src.models.inventory import StockMovement
except ImportError:

    class StockMovement:
        query = None

        def to_dict(self):
            return {}


# Import database - handle different import paths
try:
    from src.database import db
except ImportError:
    # Create mock db for testing
    class MockDB:
        class _Sess:
            def add(self, *_args, **_kwargs):
                return None

            def commit(self):
                return None

            def rollback(self):
                return None

            def delete(self, *_args, **_kwargs):
                return None

        session = _Sess()

        @staticmethod
        def create_all():
            pass

        @staticmethod
        def drop_all():
            pass

    db = MockDB()

partners_bp = Blueprint("partners", __name__)

# APIs الموردين


@partners_bp.route("/suppliers", methods=["GET"])
def get_suppliers():
    """الحصول على جميع الموردين"""
    try:
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search", "")
        per_page = request.args.get("per_page", 10, type=int)

        query = Supplier.query

        if search:
            query = query.filter(Supplier.name.contains(search))

        suppliers = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "status": "success",
                "data": [supplier.to_dict() for supplier in suppliers.items],
                "pagination": {
                    "page": page,
                    "pages": suppliers.pages,
                    "per_page": per_page,
                    "total": suppliers.total,
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/suppliers", methods=["POST"])
def create_supplier():
    """إنشاء مورد جديد"""
    try:
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"status": "error", "message": "اسم المورد مطلوب"}), 400

        supplier = Supplier(
            name=data["name"],
            contact_person=data.get("contact_person", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            address=data.get("address", ""),
            country=data.get("country", ""),
            currency=data.get("currency", "EGP"),
            tax_number=data.get("tax_number", ""),
            payment_terms=data.get("payment_terms", ""),
            credit_limit=data.get("credit_limit", 0),
            notes=data.get("notes", ""),
            is_active=data.get("is_active", True),
        )

        db.session.add(supplier)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء المورد بنجاح",
                    "data": supplier.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/suppliers/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id):
    """الحصول على مورد محدد"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        return jsonify({"status": "success", "data": supplier.to_dict()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/suppliers/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    """تحديث مورد"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        data = request.get_json()

        # تحديث البيانات
        for field in [
            "name",
            "contact_person",
            "phone",
            "email",
            "address",
            "country",
            "currency",
            "tax_number",
            "payment_terms",
            "credit_limit",
            "notes",
            "is_active",
        ]:
            if field in data:
                setattr(supplier, field, data[field])

        supplier.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث المورد بنجاح",
                "data": supplier.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/suppliers/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    """حذف مورد"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)

        # التحقق من عدم وجود حركات مرتبطة
        movements = StockMovement.query.filter_by(supplier_id=supplier_id).first()
        if movements:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "لا يمكن حذف المورد لوجود حركات مرتبطة به",
                    }
                ),
                400,
            )

        db.session.delete(supplier)
        db.session.commit()

        return jsonify({"status": "success", "message": "تم حذف المورد بنجاح"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# APIs العملاء


@partners_bp.route("/customers", methods=["GET"])
def get_customers():
    """الحصول على جميع العملاء"""
    try:
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search", "")
        per_page = request.args.get("per_page", 10, type=int)

        query = Customer.query

        if search:
            query = query.filter(Customer.name.contains(search))

        customers = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "status": "success",
                "data": [customer.to_dict() for customer in customers.items],
                "pagination": {
                    "page": page,
                    "pages": customers.pages,
                    "per_page": per_page,
                    "total": customers.total,
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/customers", methods=["POST"])
def create_customer():
    """إنشاء عميل جديد"""
    try:
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"status": "error", "message": "اسم العميل مطلوب"}), 400

        customer = Customer(
            name=data["name"],
            contact_person=data.get("contact_person", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            address=data.get("address", ""),
            region=data.get("region", ""),
            tax_number=data.get("tax_number", ""),
            payment_terms=data.get("payment_terms", ""),
            credit_limit=data.get("credit_limit", 0),
            salesperson_id=data.get("salesperson_id"),
            notes=data.get("notes", ""),
            is_active=data.get("is_active", True),
        )

        db.session.add(customer)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء العميل بنجاح",
                    "data": customer.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """الحصول على عميل محدد"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify({"status": "success", "data": customer.to_dict()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """تحديث عميل"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()

        # تحديث البيانات
        for field in [
            "name",
            "contact_person",
            "phone",
            "email",
            "address",
            "region",
            "tax_number",
            "payment_terms",
            "credit_limit",
            "salesperson_id",
            "notes",
            "is_active",
        ]:
            if field in data:
                setattr(customer, field, data[field])

        customer.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث العميل بنجاح",
                "data": customer.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """حذف عميل"""
    try:
        customer = Customer.query.get_or_404(customer_id)

        # التحقق من عدم وجود حركات مرتبطة
        movements = StockMovement.query.filter_by(customer_id=customer_id).first()
        if movements:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "لا يمكن حذف العميل لوجود حركات مرتبطة به",
                    }
                ),
                400,
            )

        db.session.delete(customer)
        db.session.commit()

        return jsonify({"status": "success", "message": "تم حذف العميل بنجاح"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# APIs حركات المخزون


@partners_bp.route("/stock-movements", methods=["GET"])
def get_stock_movements():
    """الحصول على حركات المخزون"""
    try:
        page = request.args.get("page", 1, type=int)
        movement_type = request.args.get("movement_type")
        product_id = request.args.get("product_id")
        warehouse_id = request.args.get("warehouse_id")
        per_page = request.args.get("per_page", 10, type=int)

        query = StockMovement.query

        if movement_type:
            query = query.filter_by(movement_type=movement_type)
        if product_id:
            query = query.filter_by(product_id=product_id)
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)

        movements = query.order_by(StockMovement.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify(
            {
                "status": "success",
                "data": [movement.to_dict() for movement in movements.items],
                "pagination": {
                    "page": page,
                    "pages": movements.pages,
                    "per_page": per_page,
                    "total": movements.total,
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/stock-movements", methods=["POST"])
def create_stock_movement():
    """إنشاء حركة مخزون جديدة"""
    try:
        data = request.get_json()

        required_fields = ["movement_type", "product_id", "warehouse_id"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"status": "error", "message": f"{field} مطلوب"}), 400

        # التحقق من أن إحدى الكميتين موجودة
        if not data.get("quantity_in") and not data.get("quantity_out"):
            return (
                jsonify({"status": "error", "message": "يجب إدخال كمية وارد أو صادر"}),
                400,
            )

        movement = StockMovement()
        movement.movement_type = data["movement_type"]
        movement.product_id = data["product_id"]
        movement.batch_id = data.get("batch_id")
        movement.warehouse_id = data["warehouse_id"]
        movement.quantity_in = data.get("quantity_in", 0)
        movement.quantity_out = data.get("quantity_out", 0)
        movement.unit_price = data.get("unit_price", 0)
        movement.total_amount = data.get("total_amount", 0)
        movement.currency = data.get("currency", "EGP")
        movement.exchange_rate = data.get("exchange_rate", 1)
        movement.customer_id = data.get("customer_id")
        movement.supplier_id = data.get("supplier_id")
        movement.salesperson_id = data.get("salesperson_id")
        movement.movement_date = (
            datetime.fromisoformat(data["movement_date"])
            if data.get("movement_date")
            else datetime.now(timezone.utc)
        )
        movement.reference_number = data.get("reference_number", "")
        movement.notes = data.get("notes", "")
        movement.created_by = 1  # سيتم تحديثه لاحقاً مع نظام المصادقة

        db.session.add(movement)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء حركة المخزون بنجاح",
                    "data": movement.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# APIs أنواع العملاء


@partners_bp.route("/customer-types", methods=["GET"])
def get_customer_types():
    """الحصول على أنواع العملاء"""
    try:
        customer_types = CustomerType.query.filter_by(is_active=True).all()
        return jsonify(
            {"status": "success", "data": [ct.to_dict() for ct in customer_types]}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/customer-types", methods=["POST"])
def create_customer_type():
    """إنشاء نوع عميل جديد"""
    try:
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"status": "error", "message": "اسم النوع مطلوب"}), 400

        # التحقق من عدم وجود نوع بنفس الاسم
        existing = CustomerType.query.filter_by(name=data["name"]).first()
        if existing:
            return (
                jsonify({"status": "error", "message": "نوع العميل موجود بالفعل"}),
                400,
            )

        customer_type = CustomerType()
        customer_type.name = data["name"]
        customer_type.description = data.get("description", "")
        customer_type.discount_percentage = data.get("discount_percentage", 0)
        customer_type.credit_limit = data.get("credit_limit", 0)
        customer_type.payment_terms = data.get("payment_terms", "")

        db.session.add(customer_type)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء نوع العميل بنجاح",
                    "data": customer_type.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/customer-types/<int:type_id>", methods=["PUT"])
def update_customer_type(type_id):
    """تحديث نوع عميل"""
    try:
        customer_type = CustomerType.query.get_or_404(type_id)
        data = request.get_json()

        # تحديث البيانات
        for field in [
            "name",
            "description",
            "discount_percentage",
            "credit_limit",
            "payment_terms",
        ]:
            if field in data:
                setattr(customer_type, field, data[field])

        customer_type.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث نوع العميل بنجاح",
                "data": customer_type.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/customer-types/<int:type_id>", methods=["DELETE"])
def delete_customer_type(type_id):
    """حذف نوع عميل"""
    try:
        customer_type = CustomerType.query.get_or_404(type_id)

        # التحقق من عدم وجود عملاء مرتبطين
        customers_count = Customer.query.filter_by(customer_type_id=type_id).count()
        if customers_count > 0:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"لا يمكن حذف النوع لأنه مرتبط بـ {customers_count} عميل",
                    }
                ),
                400,
            )

        db.session.delete(customer_type)
        db.session.commit()

        return jsonify({"status": "success", "message": "تم حذف نوع العميل بنجاح"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# APIs أنواع الموردين


@partners_bp.route("/supplier-types", methods=["GET"])
def get_supplier_types():
    """الحصول على أنواع الموردين"""
    try:
        supplier_types = SupplierType.query.filter_by(is_active=True).all()
        return jsonify(
            {"status": "success", "data": [st.to_dict() for st in supplier_types]}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/supplier-types", methods=["POST"])
def create_supplier_type():
    """إنشاء نوع مورد جديد"""
    try:
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"status": "error", "message": "اسم النوع مطلوب"}), 400

        # التحقق من عدم وجود نوع بنفس الاسم
        existing = SupplierType.query.filter_by(name=data["name"]).first()
        if existing:
            return (
                jsonify({"status": "error", "message": "نوع المورد موجود بالفعل"}),
                400,
            )

        supplier_type = SupplierType()
        supplier_type.name = data["name"]
        supplier_type.description = data.get("description", "")
        supplier_type.default_currency = data.get("default_currency", "EGP")
        supplier_type.payment_terms = data.get("payment_terms", "")
        supplier_type.credit_limit = data.get("credit_limit", 0)

        db.session.add(supplier_type)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "تم إنشاء نوع المورد بنجاح",
                    "data": supplier_type.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/supplier-types/<int:type_id>", methods=["PUT"])
def update_supplier_type(type_id):
    """تحديث نوع مورد"""
    try:
        supplier_type = SupplierType.query.get_or_404(type_id)
        data = request.get_json()

        # تحديث البيانات
        for field in [
            "name",
            "description",
            "default_currency",
            "payment_terms",
            "credit_limit",
        ]:
            if field in data:
                setattr(supplier_type, field, data[field])

        supplier_type.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "message": "تم تحديث نوع المورد بنجاح",
                "data": supplier_type.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@partners_bp.route("/supplier-types/<int:type_id>", methods=["DELETE"])
def delete_supplier_type(type_id):
    """حذف نوع مورد"""
    try:
        supplier_type = SupplierType.query.get_or_404(type_id)

        # التحقق من عدم وجود موردين مرتبطين
        suppliers_count = Supplier.query.filter_by(supplier_type_id=type_id).count()
        if suppliers_count > 0:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"لا يمكن حذف النوع لأنه مرتبط بـ {suppliers_count} مورد",
                    }
                ),
                400,
            )

        db.session.delete(supplier_type)
        db.session.commit()

        return jsonify({"status": "success", "message": "تم حذف نوع المورد بنجاح"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
