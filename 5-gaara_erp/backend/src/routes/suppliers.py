#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.83: Supplier Management Routes

Complete CRUD API for supplier management.
"""

from flask import Blueprint, request, jsonify, g
from datetime import datetime
from typing import Dict, Any, List
from src.database import db
from src.models.supplier import Supplier
from src.permissions import require_permission, Permissions
from src.utils.validation import validate_json
from marshmallow import Schema, fields, validate
import logging

logger = logging.getLogger(__name__)

suppliers_bp = Blueprint("suppliers", __name__, url_prefix="/api/suppliers")


# =============================================================================
# Schemas
# =============================================================================


class SupplierSchema(Schema):
    """Supplier validation schema."""

    name = fields.String(required=True, validate=validate.Length(min=2, max=200))
    name_ar = fields.String(validate=validate.Length(max=200))
    code = fields.String(validate=validate.Length(max=50))
    email = fields.Email()
    phone = fields.String(validate=validate.Length(max=20))
    mobile = fields.String(validate=validate.Length(max=20))
    fax = fields.String(validate=validate.Length(max=20))
    website = fields.String(validate=validate.Length(max=200))

    # Address
    address = fields.String(validate=validate.Length(max=500))
    city = fields.String(validate=validate.Length(max=100))
    region = fields.String(validate=validate.Length(max=100))
    country = fields.String(validate=validate.Length(max=100))
    postal_code = fields.String(validate=validate.Length(max=20))

    # Contact person
    contact_person = fields.String(validate=validate.Length(max=200))
    contact_title = fields.String(validate=validate.Length(max=100))
    contact_phone = fields.String(validate=validate.Length(max=20))
    contact_email = fields.Email()

    # Business info
    tax_number = fields.String(validate=validate.Length(max=50))
    commercial_register = fields.String(validate=validate.Length(max=50))
    bank_name = fields.String(validate=validate.Length(max=100))
    bank_account = fields.String(validate=validate.Length(max=50))
    iban = fields.String(validate=validate.Length(max=50))

    # Payment terms
    payment_terms = fields.String(validate=validate.Length(max=200))
    credit_limit = fields.Float(validate=validate.Range(min=0))
    payment_days = fields.Integer(validate=validate.Range(min=0, max=365))

    # Status
    is_active = fields.Boolean()

    # Notes
    notes = fields.String()


# =============================================================================
# Routes
# =============================================================================


@suppliers_bp.route("", methods=["GET"])
@require_permission(Permissions.PARTNERS_VIEW)
def get_suppliers():
    """Get all suppliers with filtering and pagination."""
    try:
        # Query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        search = request.args.get("search", "")
        is_active = request.args.get("is_active", type=lambda x: x.lower() == "true")
        sort_by = request.args.get("sort_by", "name")
        sort_order = request.args.get("sort_order", "asc")

        # Build query
        query = Supplier.query

        # Filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Supplier.name.ilike(search_term),
                    Supplier.code.ilike(search_term),
                    Supplier.email.ilike(search_term),
                    Supplier.phone.ilike(search_term),
                )
            )

        if is_active is not None:
            query = query.filter_by(is_active=is_active)

        # Sorting
        sort_column = getattr(Supplier, sort_by, Supplier.name)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

        # Pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "success": True,
                "data": [s.to_dict() for s in pagination.items],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev,
                },
            }
        )

    except Exception as e:
        logger.error(f"Error fetching suppliers: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@suppliers_bp.route("/<int:supplier_id>", methods=["GET"])
@require_permission(Permissions.PARTNERS_VIEW)
def get_supplier(supplier_id: int):
    """Get a single supplier by ID."""
    try:
        supplier = Supplier.query.get(supplier_id)

        if not supplier:
            return jsonify({"success": False, "message": "المورد غير موجود"}), 404

        return jsonify({"success": True, "data": supplier.to_dict()})

    except Exception as e:
        logger.error(f"Error fetching supplier {supplier_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@suppliers_bp.route("", methods=["POST"])
@require_permission(Permissions.PARTNERS_ADD)
@validate_json(SupplierSchema)
def create_supplier():
    """Create a new supplier."""
    try:
        data = g.validated_data

        # Check for duplicate code/email
        if data.get("code"):
            existing = Supplier.query.filter_by(code=data["code"]).first()
            if existing:
                return (
                    jsonify({"success": False, "message": "كود المورد موجود مسبقاً"}),
                    400,
                )

        if data.get("email"):
            existing = Supplier.query.filter_by(email=data["email"]).first()
            if existing:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "البريد الإلكتروني مسجل لمورد آخر",
                        }
                    ),
                    400,
                )

        # Generate code if not provided
        if not data.get("code"):
            last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
            next_id = (last_supplier.id + 1) if last_supplier else 1
            data["code"] = f"SUP{next_id:05d}"

        supplier = Supplier(**data)
        supplier.created_by = getattr(request, "current_user_id", None)

        db.session.add(supplier)
        db.session.commit()

        logger.info(f"Created supplier: {supplier.id} - {supplier.name}")

        return (
            jsonify(
                {
                    "success": True,
                    "message": "تم إنشاء المورد بنجاح",
                    "data": supplier.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating supplier: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@suppliers_bp.route("/<int:supplier_id>", methods=["PUT"])
@require_permission(Permissions.PARTNERS_EDIT)
@validate_json(SupplierSchema)
def update_supplier(supplier_id: int):
    """Update an existing supplier."""
    try:
        supplier = Supplier.query.get(supplier_id)

        if not supplier:
            return jsonify({"success": False, "message": "المورد غير موجود"}), 404

        data = g.validated_data

        # Check for duplicate code/email (excluding current)
        if data.get("code") and data["code"] != supplier.code:
            existing = Supplier.query.filter(
                Supplier.code == data["code"], Supplier.id != supplier_id
            ).first()
            if existing:
                return (
                    jsonify({"success": False, "message": "كود المورد موجود مسبقاً"}),
                    400,
                )

        if data.get("email") and data["email"] != supplier.email:
            existing = Supplier.query.filter(
                Supplier.email == data["email"], Supplier.id != supplier_id
            ).first()
            if existing:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "البريد الإلكتروني مسجل لمورد آخر",
                        }
                    ),
                    400,
                )

        # Update fields
        for key, value in data.items():
            if hasattr(supplier, key):
                setattr(supplier, key, value)

        supplier.updated_at = datetime.utcnow()
        db.session.commit()

        logger.info(f"Updated supplier: {supplier.id}")

        return jsonify(
            {
                "success": True,
                "message": "تم تحديث المورد بنجاح",
                "data": supplier.to_dict(),
            }
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating supplier {supplier_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@suppliers_bp.route("/<int:supplier_id>", methods=["DELETE"])
@require_permission(Permissions.PARTNERS_DELETE)
def delete_supplier(supplier_id: int):
    """Delete a supplier."""
    try:
        supplier = Supplier.query.get(supplier_id)

        if not supplier:
            return jsonify({"success": False, "message": "المورد غير موجود"}), 404

        # Check for related records
        if supplier.purchase_orders:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "لا يمكن حذف المورد لوجود أوامر شراء مرتبطة به",
                    }
                ),
                400,
            )

        db.session.delete(supplier)
        db.session.commit()

        logger.info(f"Deleted supplier: {supplier_id}")

        return jsonify({"success": True, "message": "تم حذف المورد بنجاح"})

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting supplier {supplier_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@suppliers_bp.route("/<int:supplier_id>/toggle-status", methods=["POST"])
@require_permission(Permissions.PARTNERS_EDIT)
def toggle_supplier_status(supplier_id: int):
    """Toggle supplier active status."""
    try:
        supplier = Supplier.query.get(supplier_id)

        if not supplier:
            return jsonify({"success": False, "message": "المورد غير موجود"}), 404

        supplier.is_active = not supplier.is_active
        supplier.updated_at = datetime.utcnow()
        db.session.commit()

        status = "تفعيل" if supplier.is_active else "إيقاف"

        return jsonify(
            {
                "success": True,
                "message": f"تم {status} المورد بنجاح",
                "data": {"is_active": supplier.is_active},
            }
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error toggling supplier status {supplier_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@suppliers_bp.route("/<int:supplier_id>/purchase-history", methods=["GET"])
@require_permission(Permissions.PARTNERS_VIEW)
def get_supplier_purchase_history(supplier_id: int):
    """Get purchase history for a supplier."""
    try:
        from src.models.purchase_order import PurchaseOrder

        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            return jsonify({"success": False, "message": "المورد غير موجود"}), 404

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        query = PurchaseOrder.query.filter_by(supplier_id=supplier_id)
        query = query.order_by(PurchaseOrder.created_at.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "success": True,
                "data": [po.to_dict() for po in pagination.items],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                },
            }
        )

    except Exception as e:
        logger.error(f"Error fetching purchase history for supplier {supplier_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@suppliers_bp.route("/stats", methods=["GET"])
@require_permission(Permissions.PARTNERS_VIEW)
def get_suppliers_stats():
    """Get supplier statistics."""
    try:
        from sqlalchemy import func
        from src.models.purchase_order import PurchaseOrder

        total = Supplier.query.count()
        active = Supplier.query.filter_by(is_active=True).count()

        # Top suppliers by purchase volume
        top_suppliers = (
            db.session.query(
                Supplier.id,
                Supplier.name,
                func.count(PurchaseOrder.id).label("order_count"),
                func.sum(PurchaseOrder.total).label("total_purchases"),
            )
            .join(PurchaseOrder, PurchaseOrder.supplier_id == Supplier.id)
            .group_by(Supplier.id)
            .order_by(func.sum(PurchaseOrder.total).desc())
            .limit(10)
            .all()
        )

        return jsonify(
            {
                "success": True,
                "data": {
                    "total_suppliers": total,
                    "active_suppliers": active,
                    "inactive_suppliers": total - active,
                    "top_suppliers": [
                        {
                            "id": s.id,
                            "name": s.name,
                            "order_count": s.order_count,
                            "total_purchases": float(s.total_purchases or 0),
                        }
                        for s in top_suppliers
                    ],
                },
            }
        )

    except Exception as e:
        logger.error(f"Error fetching supplier stats: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


__all__ = ["suppliers_bp"]
