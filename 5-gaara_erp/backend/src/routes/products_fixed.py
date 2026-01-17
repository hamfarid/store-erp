# -*- coding: utf-8 -*-
# FILE: backend/src/routes/products.py | PURPOSE: Secure and Refactored
# Product Routes | OWNER: Backend | RELATED: models/inventory.py,
# schemas/product_schema.py | LAST-AUDITED: 2025-10-21

"""
مسارات المنتجات الآمنة والمحسنة - الإصدار 2.0
Secure and Refactored Products Routes - Version 2.0

P0 Fixes Applied:
- P0.1: SQL Injection (Verified safe with ORM, no raw SQL)
- P0.2: CSRF Protection (JWT-based for JSON API)
- P0.3: Authentication (jwt_required on all state-changing endpoints)
- P0.4: Input Validation (Marshmallow schema for all inputs)
- P0.5: Unified Error Envelope (Consistent error handling)
"""

from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

# P0.4: Import Marshmallow schema for validation
from ..schemas.product_schema import ProductSchema

# Import models and DB session
from ..models.product_unified import Product
from ..models.inventory import Category  # Assuming Category model exists
from ..database import db

# P0.5: Import unified error envelope
from ..middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

products_bp = Blueprint("products_v2", __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@products_bp.route("/api/products", methods=["GET"])
def get_products():
    """Get a paginated list of products with search functionality."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        search = request.args.get("search", "")

        query = Product.query

        if search:
            from sqlalchemy import or_

            # P0.1: Using ORM's `contains` is safe against SQLi
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.like(search_term),
                    Product.sku.like(search_term),
                    Product.barcode.like(search_term),
                )
            )

        paginated_products = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        return success_response(
            data={
                "products": products_schema.dump(paginated_products.items),
                "pagination": {
                    "page": paginated_products.page,
                    "pages": paginated_products.pages,
                    "per_page": paginated_products.per_page,
                    "total": paginated_products.total,
                },
            },
            message="Products retrieved successfully.",
        )

    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )
    except Exception as e:
        return error_response(
            "An unexpected error occurred.",
            ErrorCodes.SYS_INTERNAL_ERROR,
            500,
            details=str(e),
        )


@products_bp.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get a single product by its ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return error_response("Product not found.", ErrorCodes.DB_NOT_FOUND, 404)

        return success_response(data=product_schema.dump(product))

    except SQLAlchemyError as e:
        return error_response(
            "Database error.", ErrorCodes.DB_ERROR, 500, details=str(e)
        )
    except Exception as e:
        return error_response(
            "An unexpected error occurred.",
            ErrorCodes.SYS_INTERNAL_ERROR,
            500,
            details=str(e),
        )


@products_bp.route("/api/products", methods=["POST"])
@jwt_required()  # P0.3: Secure endpoint with JWT
def create_product():
    """Create a new product."""
    try:
        # P0.4: Validate input with Marshmallow schema
        json_data = request.get_json()
        validated_data = product_schema.load(json_data)

        # Optional: Check if category exists
        category_id = validated_data.get("category_id")
        if category_id and not Category.query.get(category_id):
            return error_response(
                "Category not found.", ErrorCodes.VAL_INVALID_REFERENCE, 400
            )

        new_product = Product(**validated_data)

        db.session.add(new_product)
        db.session.commit()

        return success_response(
            data=product_schema.dump(new_product),
            message="Product created successfully.",
            status_code=201,
        )

    except ValidationError as err:
        return error_response(
            "Invalid input.", ErrorCodes.VAL_INVALID_FORMAT, 400, details=err.messages
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(
            "Database error while creating product.",
            ErrorCodes.DB_ERROR,
            500,
            details=str(e),
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            "An unexpected error occurred.",
            ErrorCodes.SYS_INTERNAL_ERROR,
            500,
            details=str(e),
        )


@products_bp.route("/api/products/<int:product_id>", methods=["PUT"])
@jwt_required()  # P0.3: Secure endpoint with JWT
def update_product(product_id):
    """Update an existing product."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return error_response("Product not found.", ErrorCodes.DB_NOT_FOUND, 404)

        # P0.4: Validate input with Marshmallow schema
        json_data = request.get_json()
        validated_data = product_schema.load(
            json_data, partial=True
        )  # Allow partial updates

        # Optional: Check if category exists
        category_id = validated_data.get("category_id")
        if category_id and not Category.query.get(category_id):
            return error_response(
                "Category not found.", ErrorCodes.VAL_INVALID_REFERENCE, 400
            )

        for key, value in validated_data.items():
            setattr(product, key, value)

        db.session.commit()

        return success_response(
            data=product_schema.dump(product), message="Product updated successfully."
        )

    except ValidationError as err:
        return error_response(
            "Invalid input.", ErrorCodes.VAL_INVALID_FORMAT, 400, details=err.messages
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(
            "Database error while updating product.",
            ErrorCodes.DB_ERROR,
            500,
            details=str(e),
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            "An unexpected error occurred.",
            ErrorCodes.SYS_INTERNAL_ERROR,
            500,
            details=str(e),
        )


@products_bp.route("/api/products/<int:product_id>", methods=["DELETE"])
@jwt_required()  # P0.3: Secure endpoint with JWT
def delete_product(product_id):
    """Delete a product."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return error_response("Product not found.", ErrorCodes.DB_NOT_FOUND, 404)

        db.session.delete(product)
        db.session.commit()

        return success_response(
            message="Product deleted successfully.", status_code=200
        )  # Or 204 No Content

    except SQLAlchemyError as e:
        db.session.rollback()
        # Check for foreign key constraint violation
        if "FOREIGN KEY" in str(e).upper():
            return error_response(
                "Cannot delete product. It is referenced by other records (e.g., sales, inventory).",
                ErrorCodes.DB_INTEGRITY_ERROR,
                409,
            )
        return error_response(
            "Database error while deleting product.",
            ErrorCodes.DB_ERROR,
            500,
            details=str(e),
        )
    except Exception as e:
        db.session.rollback()
        return error_response(
            "An unexpected error occurred.",
            ErrorCodes.SYS_INTERNAL_ERROR,
            500,
            details=str(e),
        )
