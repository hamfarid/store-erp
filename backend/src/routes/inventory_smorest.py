# -*- coding: utf-8 -*-
# FILE: backend/src/routes/inventory_smorest.py | PURPOSE: Inventory
# routes with flask-smorest and OpenAPI | OWNER: Backend | RELATED: T11 |
# LAST-AUDITED: 2025-11-06

"""
Inventory Routes with flask-smorest - T11
==========================================

Flask-smorest implementation of inventory endpoints with automatic OpenAPI documentation.

Endpoints:
- GET /api/inventory/categories - List all categories
- POST /api/inventory/categories - Create new category
- GET /api/inventory/warehouses - List all warehouses
- POST /api/inventory/warehouses - Create new warehouse
- GET /api/inventory/stock-movements - List stock movements with filters
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, validate, EXCLUDE

from src.database import db
from src.models.inventory import Category, Warehouse, StockMovement

# Create blueprint
inventory_smorest_bp = Blueprint(
    "inventory_smorest",
    __name__,
    url_prefix="/api/inventory",
    description="Inventory management endpoints - Categories, Warehouses, Stock Movements",
)

# ==================== Schemas ====================


class CategorySchema(Schema):
    """Category schema with detailed documentation."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(
        dump_only=True,
        metadata={"description": "Unique category identifier", "example": 1},
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        metadata={"description": "Category name in Arabic", "example": "بذور"},
    )
    name_ar = fields.Str(
        allow_none=True,
        metadata={"description": "Category name in Arabic", "example": "بذور"},
    )
    name_en = fields.Str(
        allow_none=True,
        metadata={"description": "Category name in English", "example": "Seeds"},
    )
    description = fields.Str(
        allow_none=True,
        metadata={
            "description": "Category description",
            "example": "جميع أنواع البذور الزراعية",
        },
    )
    is_active = fields.Bool(
        load_default=True,
        metadata={"description": "Whether category is active", "example": True},
    )
    created_at = fields.Str(
        dump_only=True,
        allow_none=True,
        metadata={
            "description": "Creation timestamp",
            "example": "2025-11-06T10:00:00Z",
        },
    )


class CategoryListSchema(Schema):
    """Schema for category list response."""

    success = fields.Bool(
        metadata={"description": "Request success status", "example": True}
    )
    data = fields.List(
        fields.Nested(CategorySchema), metadata={"description": "List of categories"}
    )
    items = fields.List(
        fields.Nested(CategorySchema), metadata={"description": "List of categories"}
    )
    message = fields.Str(
        metadata={
            "description": "Response message",
            "example": "تم جلب التصنيفات بنجاح",
        }
    )


class WarehouseSchema(Schema):
    """Warehouse schema with detailed documentation."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(
        dump_only=True,
        metadata={"description": "Unique warehouse identifier", "example": 1},
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        metadata={"description": "Warehouse name", "example": "المخزن الرئيسي"},
    )
    name_ar = fields.Str(
        allow_none=True,
        metadata={"description": "Warehouse name in Arabic", "example": "المخزن الرئيسي"},
    )
    code = fields.Str(
        allow_none=True, metadata={"description": "Warehouse code", "example": "WH-001"}
    )
    location = fields.Str(
        allow_none=True,
        metadata={"description": "Warehouse location", "example": "Riyadh"},
    )
    region = fields.Str(
        allow_none=True,
        metadata={"description": "Warehouse region", "example": "Central"},
    )
    address = fields.Str(
        allow_none=True,
        metadata={
            "description": "Warehouse address",
            "example": "الرياض، المملكة العربية السعودية",
        },
    )
    manager_id = fields.Int(
        allow_none=True,
        metadata={"description": "Warehouse manager user id", "example": 1},
    )
    phone = fields.Str(
        allow_none=True,
        metadata={"description": "Contact phone number", "example": "+966501234567"},
    )
    email = fields.Str(
        allow_none=True,
        metadata={"description": "Contact email", "example": "warehouse@example.com"},
    )
    manager_name = fields.Str(
        allow_none=True,
        metadata={"description": "Warehouse manager name", "example": "أحمد محمد"},
    )
    capacity = fields.Float(
        allow_none=True,
        metadata={
            "description": "Warehouse capacity in cubic meters",
            "example": 1000.0,
        },
    )
    current_stock = fields.Float(
        allow_none=True,
        metadata={"description": "Current stock level", "example": 750.5},
    )
    is_active = fields.Bool(
        load_default=True,
        metadata={"description": "Whether warehouse is active", "example": True},
    )
    warehouse_type = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["main", "branch", "temporary"]),
        metadata={"description": "Warehouse type", "example": "main"},
    )
    created_at = fields.Str(
        dump_only=True,
        allow_none=True,
        metadata={
            "description": "Creation timestamp",
            "example": "2025-11-06T10:00:00Z",
        },
    )


class WarehouseListSchema(Schema):
    """Schema for warehouse list response."""

    success = fields.Bool(
        metadata={"description": "Request success status", "example": True}
    )
    data = fields.List(
        fields.Nested(WarehouseSchema), metadata={"description": "List of warehouses"}
    )
    items = fields.List(
        fields.Nested(WarehouseSchema), metadata={"description": "List of warehouses"}
    )
    message = fields.Str(
        metadata={"description": "Response message", "example": "تم جلب المخازن بنجاح"}
    )


class StockMovementQuerySchema(Schema):
    """Query parameters for stock movements list."""

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
    movement_type = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["in", "out", "adjustment", "transfer"]),
        metadata={"description": "Filter by movement type", "example": "in"},
    )
    product_id = fields.Int(
        allow_none=True, metadata={"description": "Filter by product ID", "example": 1}
    )
    warehouse_id = fields.Int(
        allow_none=True,
        metadata={"description": "Filter by warehouse ID", "example": 1},
    )


class StockMovementSchema(Schema):
    """Stock movement schema with detailed documentation."""

    id = fields.Int(
        dump_only=True,
        metadata={"description": "Unique movement identifier", "example": 1},
    )
    product_id = fields.Int(
        required=True, metadata={"description": "Product ID", "example": 1}
    )
    warehouse_id = fields.Int(
        allow_none=True, metadata={"description": "Warehouse ID", "example": 1}
    )
    movement_type = fields.Str(
        required=True,
        validate=validate.OneOf(["in", "out", "adjustment", "transfer"]),
        metadata={"description": "Movement type", "example": "in"},
    )
    quantity = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        metadata={"description": "Movement quantity", "example": 100.0},
    )
    unit_price = fields.Float(
        allow_none=True, metadata={"description": "Unit price in EGP", "example": 25.50}
    )
    total_value = fields.Float(
        allow_none=True,
        metadata={"description": "Total value in EGP", "example": 2550.00},
    )
    reference_number = fields.Str(
        allow_none=True,
        metadata={"description": "Reference number", "example": "PO-2025-001"},
    )
    notes = fields.Str(
        allow_none=True,
        metadata={
            "description": "Movement notes",
            "example": "استلام دفعة جديدة من البذور",
        },
    )
    created_at = fields.Str(
        dump_only=True,
        allow_none=True,
        metadata={
            "description": "Creation timestamp",
            "example": "2025-11-06T10:00:00Z",
        },
    )


class StockMovementListSchema(Schema):
    """Schema for stock movements list response with pagination."""

    success = fields.Bool(
        metadata={"description": "Request success status", "example": True}
    )
    data = fields.List(
        fields.Nested(StockMovementSchema),
        metadata={"description": "List of stock movements"},
    )
    pagination = fields.Dict(
        metadata={
            "description": "Pagination information",
            "example": {"page": 1, "per_page": 20, "total": 150, "pages": 8},
        }
    )
    message = fields.Str(
        metadata={
            "description": "Response message",
            "example": "تم جلب حركات المخزون بنجاح",
        }
    )


# ==================== Routes ====================


@inventory_smorest_bp.route("/categories")
class CategoryList(MethodView):
    """Category list and creation endpoints."""

    @inventory_smorest_bp.response(200, CategoryListSchema)
    def get(self):
        """
        List all categories

        Returns a list of all product categories in the system.
        """
        try:
            categories = Category.query.all()
            items = [
                (
                    cat.to_dict()
                    if hasattr(cat, "to_dict")
                    else {
                        "id": cat.id,
                        "name": cat.name,
                        "name_ar": getattr(cat, "name_ar", None),
                        "name_en": getattr(cat, "name_en", None),
                        "description": getattr(cat, "description", None),
                        "is_active": getattr(cat, "is_active", True),
                        "created_at": getattr(cat, "created_at", None),
                    }
                )
                for cat in categories
            ]
            return {
                "success": True,
                "data": items,
                "items": items,
                "message": "تم جلب التصنيفات بنجاح",
            }
        except Exception as e:
            abort(500, message=f"خطأ في جلب التصنيفات: {str(e)}")

    @inventory_smorest_bp.arguments(CategorySchema)
    @inventory_smorest_bp.response(201, CategorySchema)
    def post(self, category_data):
        """
        Create a new category

        Creates a new product category with the provided data.
        """
        try:
            allowed_columns = {c.name for c in Category.__table__.columns}
            filtered_data = {
                k: v for k, v in category_data.items() if k in allowed_columns
            }
            new_category = Category(**filtered_data)
            db.session.add(new_category)
            db.session.commit()

            return {
                "id": new_category.id,
                "name": new_category.name,
                "name_ar": getattr(new_category, "name_ar", None),
                "name_en": getattr(new_category, "name_en", None),
                "description": getattr(new_category, "description", None),
                "is_active": getattr(new_category, "is_active", True),
                "created_at": getattr(new_category, "created_at", None),
            }
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"خطأ في إنشاء التصنيف: {str(e)}")


@inventory_smorest_bp.route("/warehouses")
class WarehouseList(MethodView):
    """Warehouse list and creation endpoints."""

    @inventory_smorest_bp.response(200, WarehouseListSchema)
    def get(self):
        """
        List all warehouses

        Returns a list of all warehouses in the system.
        """
        try:
            warehouses = Warehouse.query.all()
            items = [
                (
                    wh.to_dict()
                    if hasattr(wh, "to_dict")
                    else {
                        "id": wh.id,
                        "name": wh.name,
                        "name_ar": getattr(wh, "name_ar", None),
                        "code": getattr(wh, "code", None),
                        "location": getattr(wh, "location", None),
                        "region": getattr(wh, "region", None),
                        "address": getattr(wh, "address", None),
                        "phone": getattr(wh, "phone", None),
                        "email": getattr(wh, "email", None),
                        "manager_name": getattr(wh, "manager_name", None),
                        "capacity": getattr(wh, "capacity", None),
                        "current_stock": getattr(wh, "current_stock", 0.0),
                        "is_active": getattr(wh, "is_active", True),
                        "warehouse_type": getattr(wh, "warehouse_type", "main"),
                        "created_at": getattr(wh, "created_at", None),
                    }
                )
                for wh in warehouses
            ]
            return {
                "success": True,
                "data": items,
                "items": items,
                "message": "تم جلب المخازن بنجاح",
            }
        except Exception as e:
            abort(500, message=f"خطأ في جلب المخازن: {str(e)}")

    @inventory_smorest_bp.arguments(WarehouseSchema)
    @inventory_smorest_bp.response(201, WarehouseSchema)
    def post(self, warehouse_data):
        """
        Create a new warehouse

        Creates a new warehouse with the provided data.
        """
        try:
            allowed_columns = {c.name for c in Warehouse.__table__.columns}
            filtered_data = {
                k: v for k, v in warehouse_data.items() if k in allowed_columns
            }
            new_warehouse = Warehouse(**filtered_data)
            db.session.add(new_warehouse)
            db.session.commit()

            return {
                "id": new_warehouse.id,
                "name": new_warehouse.name,
                "name_ar": getattr(new_warehouse, "name_ar", None),
                "code": getattr(new_warehouse, "code", None),
                "address": getattr(new_warehouse, "address", None),
                "location": getattr(new_warehouse, "location", None),
                "region": getattr(new_warehouse, "region", None),
                "phone": getattr(new_warehouse, "phone", None),
                "email": getattr(new_warehouse, "email", None),
                "manager_name": getattr(new_warehouse, "manager_name", None),
                "capacity": getattr(new_warehouse, "capacity", None),
                "current_stock": getattr(new_warehouse, "current_stock", 0.0),
                "is_active": getattr(new_warehouse, "is_active", True),
                "warehouse_type": getattr(new_warehouse, "warehouse_type", "main"),
                "created_at": getattr(new_warehouse, "created_at", None),
            }
        except Exception as e:
            db.session.rollback()
            abort(500, message=f"خطأ في إنشاء المخزن: {str(e)}")


@inventory_smorest_bp.route("/stock-movements")
class StockMovementList(MethodView):
    """Stock movement list endpoint with filtering and pagination."""

    @inventory_smorest_bp.arguments(StockMovementQuerySchema, location="query")
    @inventory_smorest_bp.response(200, StockMovementListSchema)
    def get(self, query_args):
        """
        List stock movements with filters

        Returns a paginated list of stock movements with optional filters.
        Supports filtering by movement type, product, and warehouse.
        """
        try:
            page = query_args.get("page", 1)
            per_page = query_args.get("per_page", 20)

            # Build query
            query = StockMovement.query

            # Apply filters
            if query_args.get("movement_type"):
                query = query.filter(
                    StockMovement.movement_type == query_args["movement_type"]
                )

            if query_args.get("product_id"):
                query = query.filter(
                    StockMovement.product_id == query_args["product_id"]
                )

            if query_args.get("warehouse_id"):
                query = query.filter(
                    StockMovement.warehouse_id == query_args["warehouse_id"]
                )

            # Paginate
            movements = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [
                    (
                        mov.to_dict()
                        if hasattr(mov, "to_dict")
                        else {
                            "id": mov.id,
                            "product_id": mov.product_id,
                            "warehouse_id": getattr(mov, "warehouse_id", None),
                            "movement_type": mov.movement_type,
                            "quantity": mov.quantity,
                            "unit_price": getattr(mov, "unit_price", None),
                            "total_value": getattr(mov, "total_value", None),
                            "reference_number": getattr(mov, "reference_number", None),
                            "notes": getattr(mov, "notes", None),
                            "created_at": getattr(mov, "created_at", None),
                        }
                    )
                    for mov in movements.items
                ],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": movements.total,
                    "pages": movements.pages,
                },
                "message": "تم جلب حركات المخزون بنجاح",
            }
        except Exception as e:
            abort(500, message=f"خطأ في جلب حركات المخزون: {str(e)}")
