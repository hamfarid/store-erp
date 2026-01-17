# FILE: backend/src/routes/partners_smorest.py | PURPOSE: P1.24 OpenAPI
# documented partners endpoints | OWNER: Backend
"""
P1.24: Partners (Customers/Suppliers) API with OpenAPI 3.0 documentation
"""
from __future__ import annotations

try:
    from flask.views import MethodView
    from flask_smorest import Blueprint  # type: ignore
    from marshmallow import Schema, fields, validate

    SMOREST_AVAILABLE = True
except Exception:  # pragma: no cover
    Blueprint = None  # type: ignore
    MethodView = None  # type: ignore
    Schema = None  # type: ignore
    fields = None  # type: ignore
    SMOREST_AVAILABLE = False

partners_smorest_bp = None

if SMOREST_AVAILABLE and Blueprint is not None:
    partners_smorest_bp = Blueprint(
        "partners_smorest",
        __name__,
        description="Partners API - إدارة العملاء والموردين",
        url_prefix="/api",
    )

    # ========================================================================
    # Schemas
    # ========================================================================

    class CustomerSchema(Schema):
        """Customer information schema."""

        id = fields.Integer(dump_only=True, metadata={"example": 1})
        name = fields.String(
            required=True,
            validate=validate.Length(min=2, max=100),
            metadata={"example": "شركة الأمل للتجارة", "description": "Customer name"},
        )
        code = fields.String(
            metadata={"example": "CUST-001", "description": "Customer code"}
        )
        email = fields.Email(metadata={"example": "info@alamal.com"})
        phone = fields.String(metadata={"example": "+966501234567"})
        mobile = fields.String(metadata={"example": "+966551234567"})
        address = fields.String(metadata={"example": "الرياض، شارع الملك فهد"})
        city = fields.String(metadata={"example": "الرياض"})
        country = fields.String(metadata={"example": "المملكة العربية السعودية"})
        tax_number = fields.String(metadata={"example": "300123456789012"})
        credit_limit = fields.Float(metadata={"example": 50000.00})
        balance = fields.Float(dump_only=True, metadata={"example": 15000.00})
        is_active = fields.Boolean(metadata={"example": True})
        notes = fields.String(metadata={"example": "عميل VIP"})
        # Use String for datetime fields since to_dict() returns ISO format strings
        created_at = fields.String(
            dump_only=True, metadata={"example": "2025-01-01T00:00:00+00:00"}
        )
        updated_at = fields.String(
            dump_only=True, metadata={"example": "2025-01-01T00:00:00+00:00"}
        )

    class SupplierSchema(Schema):
        """Supplier information schema."""

        id = fields.Integer(dump_only=True, metadata={"example": 1})
        name = fields.String(
            required=True,
            validate=validate.Length(min=2, max=100),
            metadata={
                "example": "مؤسسة التوريدات الحديثة",
                "description": "Supplier name",
            },
        )
        code = fields.String(
            metadata={"example": "SUP-001", "description": "Supplier code"}
        )
        email = fields.Email(metadata={"example": "supplies@modern.com"})
        phone = fields.String(metadata={"example": "+966112345678"})
        mobile = fields.String(metadata={"example": "+966551234567"})
        address = fields.String(metadata={"example": "جدة، حي الصناعية"})
        city = fields.String(metadata={"example": "جدة"})
        country = fields.String(metadata={"example": "المملكة العربية السعودية"})
        tax_number = fields.String(metadata={"example": "300987654321098"})
        payment_terms = fields.Integer(
            metadata={"example": 30, "description": "Payment terms in days"}
        )
        balance = fields.Float(dump_only=True, metadata={"example": -25000.00})
        is_active = fields.Boolean(metadata={"example": True})
        notes = fields.String(metadata={"example": "مورد رئيسي للإلكترونيات"})
        # Use String for datetime fields since to_dict() returns ISO format strings
        created_at = fields.String(
            dump_only=True, metadata={"example": "2025-01-01T00:00:00+00:00"}
        )
        updated_at = fields.String(
            dump_only=True, metadata={"example": "2025-01-01T00:00:00+00:00"}
        )

    class CustomerListSchema(Schema):
        """Paginated customer list."""

        success = fields.Boolean(metadata={"example": True})
        data = fields.Dict(
            metadata={
                "example": {"customers": [], "total": 100, "page": 1, "per_page": 10}
            }
        )
        message = fields.String(
            metadata={"example": "Customers retrieved successfully"}
        )

    class SupplierListSchema(Schema):
        """Paginated supplier list."""

        success = fields.Boolean(metadata={"example": True})
        data = fields.Dict(
            metadata={
                "example": {"suppliers": [], "total": 50, "page": 1, "per_page": 10}
            }
        )
        message = fields.String(
            metadata={"example": "Suppliers retrieved successfully"}
        )

    class CustomerResponseSchema(Schema):
        """Single customer response."""

        success = fields.Boolean(metadata={"example": True})
        data = fields.Nested(CustomerSchema)
        message = fields.String(metadata={"example": "Customer retrieved successfully"})

    class SupplierResponseSchema(Schema):
        """Single supplier response."""

        success = fields.Boolean(metadata={"example": True})
        data = fields.Nested(SupplierSchema)
        message = fields.String(metadata={"example": "Supplier retrieved successfully"})

    class ErrorSchema(Schema):
        """Standard error response."""

        success = fields.Boolean(metadata={"example": False})
        error = fields.String(metadata={"example": "Validation error"})
        code = fields.String(metadata={"example": "VALIDATION_ERROR"})

    # ========================================================================
    # Customer Endpoints
    # ========================================================================

    @partners_smorest_bp.route("/customers")
    class CustomersCollection(MethodView):
        """Customer collection endpoints."""

        @partners_smorest_bp.arguments(
            Schema.from_dict(
                {
                    "page": fields.Integer(load_default=1),
                    "per_page": fields.Integer(load_default=10),
                    "search": fields.String(),
                    "city": fields.String(),
                    "is_active": fields.Boolean(),
                }
            )(),
            location="query",
        )
        @partners_smorest_bp.response(200, CustomerListSchema)
        def get(self, args):
            """
            Get paginated list of customers.

            Returns all customers with optional filtering.
            Requires `partners_view` permission.
            """
            from src.database import db
            from src.models.customer import Customer

            page = args.get("page", 1)
            per_page = args.get("per_page", 10)
            search = args.get("search")

            query = Customer.query

            if search:
                query = query.filter(
                    db.or_(
                        Customer.name.ilike(f"%{search}%"),
                        Customer.email.ilike(f"%{search}%"),
                        Customer.phone.ilike(f"%{search}%"),
                    )
                )

            if args.get("city"):
                query = query.filter(Customer.city == args["city"])

            if args.get("is_active") is not None:
                query = query.filter(Customer.is_active == args["is_active"])

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": {
                    "customers": [c.to_dict() for c in pagination.items],
                    "total": pagination.total,
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "pages": pagination.pages,
                },
                "message": "تم استرجاع العملاء بنجاح",
            }

        @partners_smorest_bp.arguments(CustomerSchema)
        @partners_smorest_bp.response(201, CustomerResponseSchema)
        @partners_smorest_bp.alt_response(400, schema=ErrorSchema)
        def post(self, json_data):
            """
            Create a new customer.

            Creates a new customer record with the provided details.
            Requires `partners_add` permission.
            """
            from src.database import db
            from src.models.customer import Customer

            customer = Customer(**json_data)
            db.session.add(customer)
            db.session.commit()

            return {
                "success": True,
                "data": customer.to_dict(),
                "message": "تم إنشاء العميل بنجاح",
            }, 201

    @partners_smorest_bp.route("/customers/<int:customer_id>")
    class CustomerResource(MethodView):
        """Single customer endpoints."""

        @partners_smorest_bp.response(200, CustomerResponseSchema)
        @partners_smorest_bp.alt_response(404, schema=ErrorSchema)
        def get(self, customer_id):
            """
            Get customer by ID.

            Returns detailed information about a specific customer.
            Requires `partners_view` permission.
            """
            from src.models.customer import Customer

            customer = Customer.query.get(customer_id)
            if not customer:
                return {
                    "success": False,
                    "error": "Customer not found",
                    "code": "NOT_FOUND",
                }, 404

            return {
                "success": True,
                "data": customer.to_dict(),
                "message": "تم استرجاع العميل بنجاح",
            }

        @partners_smorest_bp.arguments(CustomerSchema(partial=True))
        @partners_smorest_bp.response(200, CustomerResponseSchema)
        @partners_smorest_bp.alt_response(404, schema=ErrorSchema)
        def put(self, json_data, customer_id):
            """
            Update customer by ID.

            Updates the specified customer's information.
            Requires `partners_edit` permission.
            """
            from src.database import db
            from src.models.customer import Customer

            customer = Customer.query.get(customer_id)
            if not customer:
                return {
                    "success": False,
                    "error": "Customer not found",
                    "code": "NOT_FOUND",
                }, 404

            for key, value in json_data.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)

            db.session.commit()

            return {
                "success": True,
                "data": customer.to_dict(),
                "message": "تم تحديث العميل بنجاح",
            }

        @partners_smorest_bp.response(
            200,
            Schema.from_dict(
                {"success": fields.Boolean(), "message": fields.String()}
            )(),
        )
        @partners_smorest_bp.alt_response(404, schema=ErrorSchema)
        def delete(self, customer_id):
            """
            Delete customer by ID.

            Permanently removes a customer from the system.
            Requires `partners_delete` permission.
            """
            from src.database import db
            from src.models.customer import Customer

            customer = Customer.query.get(customer_id)
            if not customer:
                return {
                    "success": False,
                    "error": "Customer not found",
                    "code": "NOT_FOUND",
                }, 404

            db.session.delete(customer)
            db.session.commit()

            return {"success": True, "message": "تم حذف العميل بنجاح"}

    # ========================================================================
    # Supplier Endpoints
    # ========================================================================

    @partners_smorest_bp.route("/suppliers")
    class SuppliersCollection(MethodView):
        """Supplier collection endpoints."""

        @partners_smorest_bp.arguments(
            Schema.from_dict(
                {
                    "page": fields.Integer(load_default=1),
                    "per_page": fields.Integer(load_default=10),
                    "search": fields.String(),
                    "city": fields.String(),
                    "is_active": fields.Boolean(),
                }
            )(),
            location="query",
        )
        @partners_smorest_bp.response(200, SupplierListSchema)
        def get(self, args):
            """
            Get paginated list of suppliers.

            Returns all suppliers with optional filtering.
            Requires `partners_view` permission.
            """
            from src.database import db
            from src.models.supplier import Supplier

            page = args.get("page", 1)
            per_page = args.get("per_page", 10)
            search = args.get("search")

            query = Supplier.query

            if search:
                query = query.filter(
                    db.or_(
                        Supplier.name.ilike(f"%{search}%"),
                        Supplier.email.ilike(f"%{search}%"),
                        Supplier.phone.ilike(f"%{search}%"),
                    )
                )

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": {
                    "suppliers": [s.to_dict() for s in pagination.items],
                    "total": pagination.total,
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "pages": pagination.pages,
                },
                "message": "تم استرجاع الموردين بنجاح",
            }

        @partners_smorest_bp.arguments(SupplierSchema)
        @partners_smorest_bp.response(201, SupplierResponseSchema)
        @partners_smorest_bp.alt_response(400, schema=ErrorSchema)
        def post(self, json_data):
            """
            Create a new supplier.

            Creates a new supplier record with the provided details.
            Requires `partners_add` permission.
            """
            from src.database import db
            from src.models.supplier import Supplier

            supplier = Supplier(**json_data)
            db.session.add(supplier)
            db.session.commit()

            return {
                "success": True,
                "data": supplier.to_dict(),
                "message": "تم إنشاء المورد بنجاح",
            }, 201

    @partners_smorest_bp.route("/suppliers/<int:supplier_id>")
    class SupplierResource(MethodView):
        """Single supplier endpoints."""

        @partners_smorest_bp.response(200, SupplierResponseSchema)
        @partners_smorest_bp.alt_response(404, schema=ErrorSchema)
        def get(self, supplier_id):
            """
            Get supplier by ID.

            Returns detailed information about a specific supplier.
            Requires `partners_view` permission.
            """
            from src.models.supplier import Supplier

            supplier = Supplier.query.get(supplier_id)
            if not supplier:
                return {
                    "success": False,
                    "error": "Supplier not found",
                    "code": "NOT_FOUND",
                }, 404

            return {
                "success": True,
                "data": supplier.to_dict(),
                "message": "تم استرجاع المورد بنجاح",
            }

        @partners_smorest_bp.arguments(SupplierSchema(partial=True))
        @partners_smorest_bp.response(200, SupplierResponseSchema)
        @partners_smorest_bp.alt_response(404, schema=ErrorSchema)
        def put(self, json_data, supplier_id):
            """
            Update supplier by ID.

            Updates the specified supplier's information.
            Requires `partners_edit` permission.
            """
            from src.database import db
            from src.models.supplier import Supplier

            supplier = Supplier.query.get(supplier_id)
            if not supplier:
                return {
                    "success": False,
                    "error": "Supplier not found",
                    "code": "NOT_FOUND",
                }, 404

            for key, value in json_data.items():
                if hasattr(supplier, key):
                    setattr(supplier, key, value)

            db.session.commit()

            return {
                "success": True,
                "data": supplier.to_dict(),
                "message": "تم تحديث المورد بنجاح",
            }

        @partners_smorest_bp.response(
            200,
            Schema.from_dict(
                {"success": fields.Boolean(), "message": fields.String()}
            )(),
        )
        @partners_smorest_bp.alt_response(404, schema=ErrorSchema)
        def delete(self, supplier_id):
            """
            Delete supplier by ID.

            Permanently removes a supplier from the system.
            Requires `partners_delete` permission.
            """
            from src.database import db
            from src.models.supplier import Supplier

            supplier = Supplier.query.get(supplier_id)
            if not supplier:
                return {
                    "success": False,
                    "error": "Supplier not found",
                    "code": "NOT_FOUND",
                }, 404

            db.session.delete(supplier)
            db.session.commit()

            return {"success": True, "message": "تم حذف المورد بنجاح"}
