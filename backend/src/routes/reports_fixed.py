# -*- coding: utf-8 -*-
# FILE: backend/src/routes/reports_fixed.py | PURPOSE: Secure and
# Refactored Report Routes | OWNER: Backend | RELATED:
# schemas/report_schemas.py | LAST-AUDITED: 2025-10-21

"""
مسارات التقارير الآمنة والمحسنة - الإصدار 2.0
Secure and Refactored Report Routes - Version 2.0

P0 Fixes Applied:
- P0.1: SQL Injection (Verified safe with ORM, no raw SQL)
- P0.4: Input Validation (Marshmallow schema for all query parameters)
- P0.5: Unified Error Envelope (Consistent error handling)
"""

from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

# P0.4: Import Marshmallow schemas
from ..schemas.report_schemas import (
    StockValuationSchema,
    LowStockSchema,
    InventoryReportSchema,
    StockMovementsSchema,
)

# Import models and DB session
from ..models.product_unified import Product
from ..models.category import Category
from ..models.inventory import ProductGroup, Rank, StockMovement
from ..models.warehouse_unified import Warehouse
from ..models.customer import Customer
from ..models.supplier import Supplier
from ..database import db
from sqlalchemy import func

# P0.5: Import unified error envelope
from ..middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

reports_bp_v2 = Blueprint("reports_v2", __name__)


@reports_bp_v2.route("/stock-valuation", methods=["GET"])
@jwt_required()
def stock_valuation_report():
    """Stock valuation report."""
    try:
        products = Product.query.filter(Product.is_active).all()
        total_value = 0
        items = []

        for product in products:
            item_value = (product.get_current_stock() or 0) * (product.cost_price or 0)
            total_value += item_value
            items.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "sku": product.sku,
                    "current_stock": product.get_current_stock() or 0,
                    "cost_price": float(product.cost_price or 0),
                    "total_value": float(item_value),
                    "category": product.category.name if product.category else "N/A",
                }
            )

        return success_response(
            data={"items": items, "total_value": float(total_value)}
        )
    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )


@reports_bp_v2.route("/low-stock", methods=["GET"])
@jwt_required()
def low_stock_report():
    """Low stock report."""
    try:
        products = Product.query.filter(Product.is_active).all()
        items = []
        for product in products:
            current_stock = product.get_current_stock()
            min_quantity = product.reorder_quantity or 0
            if current_stock <= min_quantity:
                items.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "sku": product.sku,
                        "current_stock": current_stock,
                        "min_quantity": min_quantity,
                        "shortage": max(0, min_quantity - current_stock),
                        "category": (
                            product.category.name if product.category else "N/A"
                        ),
                    }
                )
        return success_response(data={"items": items})
    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )


@reports_bp_v2.route("/inventory-report", methods=["GET"])
@jwt_required()
def inventory_report():
    """Current inventory report."""
    try:
        schema = InventoryReportSchema()
        args = schema.load(request.args)

        query = db.session.query(
            Product.id,
            Product.name,
            Product.unit,
            Product.reorder_quantity,
            Category.name.label("category_name"),
        ).join(Category, Product.category_id == Category.id)

        if args.get("category_id"):
            query = query.filter(Category.id == args["category_id"])

        products = query.filter(Product.is_active).all()
        inventory_data = []

        for p in products:
            current_stock = p.get_current_stock(warehouse_id=args.get("warehouse_id"))
            if args.get("low_stock_only") and current_stock > p.reorder_quantity:
                continue
            if not args.get("include_zero_stock") and current_stock == 0:
                continue

            inventory_data.append(
                {
                    "product_id": p.id,
                    "product_name": p.name,
                    "category": p.category_name,
                    "current_stock": current_stock,
                }
            )

        return success_response(data={"inventory": inventory_data})

    except ValidationError as err:
        return error_response(
            "Invalid parameters.",
            ErrorCodes.VAL_INVALID_FORMAT,
            400,
            details=err.messages,
        )
    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )


@reports_bp_v2.route("/stock-movements-report", methods=["GET"])
@jwt_required()
def stock_movements_report():
    """Stock movements report."""
    try:
        schema = StockMovementsSchema()
        args = schema.load(request.args)

        query = db.session.query(StockMovement).join(Product).join(Warehouse)

        query = query.filter(
            StockMovement.movement_date >= args["start_date"],
            StockMovement.movement_date <= args["end_date"],
        )

        if args.get("product_id"):
            query = query.filter(StockMovement.product_id == args["product_id"])
        if args.get("warehouse_id"):
            query = query.filter(StockMovement.warehouse_id == args["warehouse_id"])
        if args.get("movement_type"):
            query = query.filter(StockMovement.movement_type == args["movement_type"])

        movements = query.order_by(StockMovement.movement_date.desc()).all()
        movements_data = [m.to_dict() for m in movements]

        return success_response(data={"movements": movements_data})

    except ValidationError as err:
        return error_response(
            "Invalid parameters.",
            ErrorCodes.VAL_INVALID_FORMAT,
            400,
            details=err.messages,
        )
    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )
