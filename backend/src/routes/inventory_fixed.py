# -*- coding: utf-8 -*-
# FILE: backend/src/routes/inventory_fixed.py | PURPOSE: Secure and
# Refactored Inventory Routes | OWNER: Backend | RELATED:
# schemas/inventory_schemas.py | LAST-AUDITED: 2025-10-21

"""
مسارات المخزون الآمنة والمحسنة - الإصدار 2.0
Secure and Refactored Inventory Routes - Version 2.0

P0 Fixes Applied:
- P0.1: SQL Injection (Verified safe with ORM)
- P0.2: CSRF Protection (JWT-based for JSON API)
- P0.3: Authentication (jwt_required on all state-changing endpoints)
- P0.4: Input Validation (Marshmallow schemas for all inputs)
- P0.5: Unified Error Envelope (Consistent error handling)
"""

from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

# P0.4: Import Marshmallow schemas
from ..schemas.inventory_schemas import CategorySchema, ProductGroupSchema, RankSchema

# Import models and DB session
from ..models.category import Category
from ..models.inventory import ProductGroup, Rank  # Assuming these models exist
from ..database import db

# P0.5: Import unified error envelope
from ..middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

inventory_bp_v2 = Blueprint("inventory_v2", __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
product_group_schema = ProductGroupSchema()
product_groups_schema = ProductGroupSchema(many=True)
rank_schema = RankSchema()
ranks_schema = RankSchema(many=True)

# --- Category Routes ---


@inventory_bp_v2.route("/api/categories", methods=["GET"])
def get_categories():
    """Get all categories."""
    try:
        categories = Category.query.all()
        return success_response(data=categories_schema.dump(categories))
    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )


@inventory_bp_v2.route("/api/categories", methods=["POST"])
@jwt_required()
def create_category():
    """Create a new category."""
    try:
        validated_data = category_schema.load(request.get_json())

        if Category.query.filter_by(name=validated_data["name"]).first():
            return error_response(
                "Category with this name already exists.",
                ErrorCodes.DB_DUPLICATE_ENTRY,
                409,
            )

        new_category = Category(**validated_data)
        db.session.add(new_category)
        db.session.commit()
        return success_response(
            data=category_schema.dump(new_category), status_code=201
        )
    except ValidationError as err:
        return error_response(
            "Invalid input.", ErrorCodes.VAL_INVALID_FORMAT, 400, details=err.messages
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )


# --- Product Group Routes ---


@inventory_bp_v2.route("/api/product-groups", methods=["GET"])
def get_product_groups():
    """Get all product groups."""
    try:
        product_groups = ProductGroup.query.all()
        return success_response(data=product_groups_schema.dump(product_groups))
    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )


@inventory_bp_v2.route("/api/product-groups", methods=["POST"])
@jwt_required()
def create_product_group():
    """Create a new product group."""
    try:
        validated_data = product_group_schema.load(request.get_json())

        if not Category.query.get(validated_data["category_id"]):
            return error_response(
                "Category not found.", ErrorCodes.VAL_INVALID_REFERENCE, 404
            )

        new_group = ProductGroup(**validated_data)
        db.session.add(new_group)
        db.session.commit()
        return success_response(
            data=product_group_schema.dump(new_group), status_code=201
        )
    except ValidationError as err:
        return error_response(
            "Invalid input.", ErrorCodes.VAL_INVALID_FORMAT, 400, details=err.messages
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )


# --- Rank Routes ---


@inventory_bp_v2.route("/api/ranks", methods=["GET"])
def get_ranks():
    """Get all ranks."""
    try:
        ranks = Rank.query.all()
        return success_response(data=ranks_schema.dump(ranks))
    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )


@inventory_bp_v2.route("/api/ranks", methods=["POST"])
@jwt_required()
def create_rank():
    """Create a new rank."""
    try:
        validated_data = rank_schema.load(request.get_json())

        if not ProductGroup.query.get(validated_data["group_id"]):
            return error_response(
                "Product group not found.", ErrorCodes.VAL_INVALID_REFERENCE, 404
            )

        new_rank = Rank(**validated_data)
        db.session.add(new_rank)
        db.session.commit()
        return success_response(data=rank_schema.dump(new_rank), status_code=201)
    except ValidationError as err:
        return error_response(
            "Invalid input.", ErrorCodes.VAL_INVALID_FORMAT, 400, details=err.messages
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )
