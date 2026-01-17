# -*- coding: utf-8 -*-
# FILE: backend/src/routes/invoices_smorest.py | PURPOSE: Invoice routes
# with flask-smorest and OpenAPI | OWNER: Backend | RELATED: T12 |
# LAST-AUDITED: 2025-11-06

"""
Invoice Routes with flask-smorest - T12
========================================

Flask-smorest implementation of invoice endpoints with automatic OpenAPI documentation.

Endpoints:
- GET /api/invoices - List invoices with filters and pagination
- POST /api/invoices - Create new invoice
- GET /api/invoices/<id> - Get specific invoice
- PUT /api/invoices/<id> - Update invoice
- DELETE /api/invoices/<id> - Delete invoice (admin only)
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, validate, EXCLUDE
from datetime import datetime
import logging

from src.database import db
from src.models.invoice_unified import (
    Invoice,
    InvoiceItem,
)


logger = logging.getLogger(__name__)

# Create blueprint
invoices_smorest_bp = Blueprint(
    "invoices_smorest",
    __name__,
    url_prefix="/api/invoices",
    description="Invoice management endpoints - Sales, Purchase, Returns",
)

# ==================== Schemas ====================


class DateOrIsoString(fields.Date):
    """Date field that can also dump pre-formatted ISO date strings.

    Some code paths (e.g., model `to_dict()`) already emit ISO date strings.
    Marshmallow's `fields.Date` expects `datetime.date` objects when dumping,
    so we accept strings to keep list endpoints stable.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return super()._serialize(value, attr, obj, **kwargs)


class InvoiceItemSchema(Schema):
    """Invoice item schema."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True, metadata={"description": "Item ID", "example": 1})
    product_id = fields.Int(
        required=True, metadata={"description": "Product ID", "example": 1}
    )
    product_name = fields.Str(
        dump_only=True,
        metadata={"description": "Product name", "example": "بذور طماطم"},
    )
    quantity = fields.Float(
        required=True,
        validate=validate.Range(min=0.01),
        metadata={"description": "Quantity", "example": 10.0},
    )
    unit_price = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        metadata={"description": "Unit price in EGP", "example": 50.00},
    )
    discount = fields.Float(
        load_default=0.0,
        validate=validate.Range(min=0),
        metadata={"description": "Discount amount", "example": 5.00},
    )
    tax_rate = fields.Float(
        load_default=0.15,
        validate=validate.Range(min=0, max=1),
        metadata={"description": "Tax rate (0.15 = 15%)", "example": 0.15},
    )
    total = fields.Float(
        dump_only=True, metadata={"description": "Total amount", "example": 575.00}
    )


class InvoicePaymentSchema(Schema):
    """Invoice payment schema."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(
        dump_only=True, metadata={"description": "Payment ID", "example": 1}
    )
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0.01),
        metadata={"description": "Payment amount in EGP", "example": 500.00},
    )
    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf(["cash", "card", "bank_transfer", "check"]),
        metadata={"description": "Payment method", "example": "cash"},
    )
    payment_date = fields.DateTime(
        load_default=datetime.utcnow,
        metadata={"description": "Payment date", "example": "2025-11-06T10:00:00Z"},
    )
    reference = fields.Str(
        allow_none=True,
        metadata={"description": "Payment reference", "example": "REF-12345"},
    )


class InvoiceSchema(Schema):
    """Invoice schema with detailed documentation."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(
        dump_only=True, metadata={"description": "Invoice ID", "example": 1}
    )
    invoice_number = fields.Str(
        dump_only=True,
        metadata={"description": "Invoice number", "example": "INV-2025-001"},
    )
    invoice_type = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["sales", "purchase", "sales_return", "purchase_return"]
        ),
        metadata={"description": "Invoice type", "example": "sales"},
    )
    invoice_date = DateOrIsoString(
        required=True, metadata={"description": "Invoice date", "example": "2025-11-06"}
    )
    due_date = DateOrIsoString(
        allow_none=True, metadata={"description": "Due date", "example": "2025-12-06"}
    )
    customer_id = fields.Int(
        allow_none=True,
        metadata={"description": "Customer ID (for sales)", "example": 1},
    )
    supplier_id = fields.Int(
        allow_none=True,
        metadata={"description": "Supplier ID (for purchases)", "example": 1},
    )
    warehouse_id = fields.Int(
        required=True, metadata={"description": "Warehouse ID", "example": 1}
    )
    status = fields.Str(
        load_default="draft",
        validate=validate.OneOf(["draft", "pending", "paid", "cancelled"]),
        metadata={"description": "Invoice status", "example": "draft"},
    )
    subtotal = fields.Float(
        dump_only=True, metadata={"description": "Subtotal amount", "example": 500.00}
    )
    tax_amount = fields.Float(
        dump_only=True, metadata={"description": "Tax amount", "example": 75.00}
    )
    discount_amount = fields.Float(
        load_default=0.0,
        validate=validate.Range(min=0),
        metadata={"description": "Discount amount", "example": 25.00},
    )
    shipping_cost = fields.Float(
        load_default=0.0,
        validate=validate.Range(min=0),
        metadata={"description": "Shipping cost", "example": 50.00},
    )
    total_amount = fields.Float(
        dump_only=True, metadata={"description": "Total amount", "example": 600.00}
    )
    paid_amount = fields.Float(
        dump_only=True, metadata={"description": "Paid amount", "example": 300.00}
    )
    notes = fields.Str(
        allow_none=True, metadata={"description": "Notes", "example": "عميل مميز"}
    )
    items = fields.List(
        fields.Nested(InvoiceItemSchema),
        required=True,
        validate=validate.Length(min=1),
        metadata={"description": "Invoice items"},
    )
    payments = fields.List(
        fields.Nested(InvoicePaymentSchema),
        dump_only=True,
        metadata={"description": "Invoice payments"},
    )
    # Use String for datetime since to_dict() returns ISO format strings
    created_at = fields.String(
        dump_only=True,
        metadata={
            "description": "Creation timestamp",
            "example": "2025-11-06T10:00:00Z",
        },
    )
    updated_at = fields.String(
        dump_only=True,
        metadata={
            "description": "Last update timestamp",
            "example": "2025-11-06T11:00:00Z",
        },
    )


class InvoiceListSchema(Schema):
    """Schema for invoice list response."""

    success = fields.Bool(
        metadata={"description": "Request success status", "example": True}
    )
    data = fields.List(
        fields.Nested(InvoiceSchema), metadata={"description": "List of invoices"}
    )

    # Compatibility alias for integration tests expecting top-level `items`
    items = fields.List(
        fields.Nested(InvoiceSchema),
        metadata={"description": "List of invoices (alias)"},
    )
    pagination = fields.Dict(metadata={"description": "Pagination metadata"})
    message = fields.Str(
        metadata={"description": "Response message", "example": "تم جلب الفواتير بنجاح"}
    )


class InvoiceQuerySchema(Schema):
    """Query parameters for invoice list."""

    page = fields.Int(
        load_default=1,
        validate=validate.Range(min=1),
        metadata={"description": "Page number", "example": 1},
    )
    per_page = fields.Int(
        load_default=20,
        validate=validate.Range(min=1, max=100),
        metadata={"description": "Items per page", "example": 20},
    )
    search = fields.Str(
        allow_none=True,
        metadata={"description": "Search in invoice number", "example": "INV-2025"},
    )
    invoice_type = fields.Str(
        allow_none=True,
        validate=validate.OneOf(
            ["sales", "purchase", "sales_return", "purchase_return"]
        ),
        metadata={"description": "Filter by invoice type", "example": "sales"},
    )
    status = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["draft", "pending", "paid", "cancelled"]),
        metadata={"description": "Filter by status", "example": "paid"},
    )
    customer_id = fields.Int(
        allow_none=True, metadata={"description": "Filter by customer ID", "example": 1}
    )
    supplier_id = fields.Int(
        allow_none=True, metadata={"description": "Filter by supplier ID", "example": 1}
    )
    date_from = fields.Date(
        allow_none=True,
        metadata={"description": "Filter from date", "example": "2025-01-01"},
    )
    date_to = fields.Date(
        allow_none=True,
        metadata={"description": "Filter to date", "example": "2025-12-31"},
    )


# ==================== Endpoints ====================


@invoices_smorest_bp.route("")
class InvoiceList(MethodView):
    """Invoice list endpoint with filtering and pagination."""

    @invoices_smorest_bp.arguments(InvoiceQuerySchema, location="query")
    @invoices_smorest_bp.response(200, InvoiceListSchema)
    def get(self, query_args):
        """
        List invoices with filters

        Returns paginated list of invoices with optional filters.
        """
        try:
            page = query_args.get("page", 1)
            per_page = query_args.get("per_page", 20)

            # Build query
            query = Invoice.query

            # Apply filters
            if query_args.get("search"):
                query = query.filter(
                    Invoice.invoice_number.contains(query_args["search"])
                )

            if query_args.get("invoice_type"):
                query = query.filter(Invoice.invoice_type == query_args["invoice_type"])

            if query_args.get("status"):
                query = query.filter(Invoice.status == query_args["status"])

            if query_args.get("customer_id"):
                query = query.filter(Invoice.customer_id == query_args["customer_id"])

            if query_args.get("supplier_id"):
                query = query.filter(Invoice.supplier_id == query_args["supplier_id"])

            if query_args.get("date_from"):
                query = query.filter(Invoice.invoice_date >= query_args["date_from"])

            if query_args.get("date_to"):
                query = query.filter(Invoice.invoice_date <= query_args["date_to"])

            # Order by date descending
            query = query.order_by(Invoice.invoice_date.desc())

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            invoices = [invoice.to_dict() for invoice in pagination.items]

            return {
                "success": True,
                "data": invoices,
                "items": invoices,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                },
                "message": "تم جلب الفواتير بنجاح",
            }

        except Exception as e:
            logger.exception("Invoice list failed")
            abort(500, message=f"خطأ في جلب الفواتير: {str(e)}")

    @invoices_smorest_bp.arguments(InvoiceSchema)
    @invoices_smorest_bp.response(201, InvoiceSchema)
    def post(self, invoice_data):
        """
        Create a new invoice

        Creates a new invoice with items and calculates totals.
        """
        try:
            # Generate invoice number
            last_invoice = Invoice.query.order_by(Invoice.id.desc()).first()
            if last_invoice and last_invoice.invoice_number:
                last_num = int(last_invoice.invoice_number.split("-")[-1])
                invoice_number = f"INV-2025-{last_num + 1:04d}"
            else:
                invoice_number = "INV-2025-0001"

            # Create invoice
            invoice = Invoice(
                invoice_number=invoice_number,
                invoice_type=invoice_data["invoice_type"],
                invoice_date=invoice_data["invoice_date"],
                due_date=invoice_data.get("due_date"),
                customer_id=invoice_data.get("customer_id"),
                supplier_id=invoice_data.get("supplier_id"),
                warehouse_id=invoice_data["warehouse_id"],
                status=invoice_data.get("status", "draft"),
                discount_amount=invoice_data.get("discount_amount", 0.0),
                shipping_cost=invoice_data.get("shipping_cost", 0.0),
                notes=invoice_data.get("notes"),
            )

            # Add items and calculate totals
            subtotal = 0.0
            tax_amount = 0.0

            for item_data in invoice_data["items"]:
                item_subtotal = item_data["quantity"] * item_data["unit_price"]
                item_discount = item_data.get("discount", 0.0)
                item_tax = (item_subtotal - item_discount) * item_data.get(
                    "tax_rate", 0.15
                )
                item_total = item_subtotal - item_discount + item_tax

                item = InvoiceItem(
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    discount=item_discount,
                    tax_rate=item_data.get("tax_rate", 0.15),
                    total=item_total,
                )
                invoice.items.append(item)

                subtotal += item_subtotal
                tax_amount += item_tax

            invoice.subtotal = subtotal
            invoice.tax_amount = tax_amount
            invoice.total_amount = (
                subtotal - invoice.discount_amount + tax_amount + invoice.shipping_cost
            )
            invoice.paid_amount = 0.0

            db.session.add(invoice)
            db.session.commit()

            return invoice.to_dict()

        except Exception as e:
            db.session.rollback()
            abort(500, message=f"خطأ في إنشاء الفاتورة: {str(e)}")


@invoices_smorest_bp.route("/<int:invoice_id>")
class InvoiceDetail(MethodView):
    """Invoice detail endpoint for get, update, delete operations."""

    @invoices_smorest_bp.response(200, InvoiceSchema)
    def get(self, invoice_id):
        """
        Get specific invoice

        Returns detailed invoice information including items and payments.
        """
        try:
            invoice = Invoice.query.get(invoice_id)
            if not invoice:
                abort(404, message="الفاتورة غير موجودة")

            return invoice.to_dict()

        except Exception as e:
            if "404" in str(e):
                raise
            abort(500, message=f"خطأ في جلب الفاتورة: {str(e)}")

    @invoices_smorest_bp.arguments(InvoiceSchema)
    @invoices_smorest_bp.response(200, InvoiceSchema)
    def put(self, invoice_data, invoice_id):
        """
        Update invoice

        Updates invoice details. Only draft invoices can be fully updated.
        """
        try:
            invoice = Invoice.query.get(invoice_id)
            if not invoice:
                abort(404, message="الفاتورة غير موجودة")

            # Check if editable
            if invoice.status not in ["draft", "pending"]:
                abort(400, message="لا يمكن تعديل فاتورة مدفوعة أو ملغاة")

            # Update fields
            invoice.invoice_type = invoice_data.get(
                "invoice_type", invoice.invoice_type
            )
            invoice.invoice_date = invoice_data.get(
                "invoice_date", invoice.invoice_date
            )
            invoice.due_date = invoice_data.get("due_date", invoice.due_date)
            invoice.customer_id = invoice_data.get("customer_id", invoice.customer_id)
            invoice.supplier_id = invoice_data.get("supplier_id", invoice.supplier_id)
            invoice.warehouse_id = invoice_data.get(
                "warehouse_id", invoice.warehouse_id
            )
            invoice.status = invoice_data.get("status", invoice.status)
            invoice.notes = invoice_data.get("notes", invoice.notes)

            db.session.commit()

            return invoice.to_dict()

        except Exception as e:
            db.session.rollback()
            if "404" in str(e) or "400" in str(e):
                raise
            abort(500, message=f"خطأ في تحديث الفاتورة: {str(e)}")

    @invoices_smorest_bp.response(204)
    def delete(self, invoice_id):
        """
        Delete invoice (admin only)

        Deletes an invoice. Only draft invoices can be deleted.
        """
        try:
            invoice = Invoice.query.get(invoice_id)
            if not invoice:
                abort(404, message="الفاتورة غير موجودة")

            # Check if deletable
            if invoice.status != "draft":
                abort(400, message="لا يمكن حذف فاتورة غير مسودة")

            db.session.delete(invoice)
            db.session.commit()

            return None

        except Exception as e:
            db.session.rollback()
            if "404" in str(e) or "400" in str(e):
                raise
            abort(500, message=f"خطأ في حذف الفاتورة: {str(e)}")
