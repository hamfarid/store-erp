from __future__ import annotations

try:
    from flask.views import MethodView
    from flask_smorest import Blueprint  # type: ignore
    from marshmallow import Schema, fields, EXCLUDE

    SMOREST_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    Blueprint = None  # type: ignore
    MethodView = None  # type: ignore
    Schema = None  # type: ignore
    fields = None  # type: ignore
    SMOREST_AVAILABLE = False


# Only define the blueprint if flask_smorest is available
products_smorest_bp = None
if SMOREST_AVAILABLE and Blueprint is not None:
    products_smorest_bp = Blueprint(
        "products_smorest",
        __name__,
        description="Real Products endpoints (migrated to flask-smorest)",
    )

    class PaginationSchema(Schema):
        """Pagination metadata for list responses."""

        page = fields.Integer(
            required=True, metadata={"description": "Current page number", "example": 1}
        )
        pages = fields.Integer(
            required=True,
            metadata={"description": "Total number of pages", "example": 5},
        )
        per_page = fields.Integer(
            required=True, metadata={"description": "Items per page", "example": 10}
        )
        total = fields.Integer(
            required=True,
            metadata={"description": "Total number of items", "example": 42},
        )

    class ProductItemSchema(Schema):
        """Product item with full details."""

        id = fields.Integer(
            required=True, metadata={"description": "Product ID", "example": 1}
        )
        name = fields.String(
            required=True,
            metadata={"description": "Product name", "example": "Laptop Dell XPS 15"},
        )
        barcode = fields.String(
            metadata={"description": "Product barcode", "example": "1234567890123"}
        )
        sku = fields.String(
            metadata={"description": "Stock Keeping Unit", "example": "DELL-XPS15-001"}
        )
        category_id = fields.Integer(
            metadata={"description": "Category ID", "example": 1}
        )
        cost_price = fields.Float(
            metadata={"description": "Cost price (SAR)", "example": 4500.00}
        )
        selling_price = fields.Float(
            metadata={"description": "Selling price (SAR)", "example": 5999.00}
        )
        current_stock = fields.Integer(
            metadata={"description": "Current stock quantity", "example": 25}
        )
        min_stock_level = fields.Integer(
            metadata={"description": "Minimum stock level", "example": 5}
        )
        max_stock_level = fields.Integer(
            metadata={"description": "Maximum stock level", "example": 100}
        )
        description = fields.String(
            metadata={
                "description": "Product description",
                "example": "High-performance laptop with 16GB RAM",
            }
        )
        specifications = fields.String(
            metadata={
                "description": "Technical specifications",
                "example": "Intel i7, 16GB RAM, 512GB SSD",
            }
        )
        is_active = fields.Boolean(
            metadata={"description": "Product active status", "example": True}
        )
        is_trackable = fields.Boolean(
            metadata={"description": "Inventory tracking enabled", "example": True}
        )

    class ProductsResponseSchema(Schema):
        """Standard API response envelope for products list."""

        status = fields.String(
            required=True,
            metadata={"description": "Response status", "example": "success"},
        )
        data = fields.List(
            fields.Nested(ProductItemSchema),
            required=True,
            metadata={"description": "List of products"},
        )

        # Compatibility alias for integration tests expecting top-level `items`
        items = fields.List(
            fields.Nested(ProductItemSchema),
            required=False,
            metadata={"description": "List of products (alias)"},
        )
        pagination = fields.Nested(
            PaginationSchema,
            required=True,
            metadata={"description": "Pagination information"},
        )

    class ProductsQueryArgsSchema(Schema):
        """Query parameters for products list endpoint."""

        class Meta:
            # Tolerate extra query params used by other handlers/tests
            unknown = EXCLUDE

        page = fields.Integer(
            load_default=1,
            metadata={"description": "Page number (1-based)", "example": 1},
        )
        per_page = fields.Integer(
            load_default=10,
            metadata={"description": "Items per page (max 100)", "example": 10},
        )
        search = fields.String(
            load_default="",
            metadata={
                "description": "Search term for product name",
                "example": "laptop",
            },
        )

        category_id = fields.Integer(
            load_default=None,
            allow_none=True,
            metadata={"description": "Filter by category ID", "example": 1},
        )

    @products_smorest_bp.route("/products")
    class ProductsView(MethodView):
        @products_smorest_bp.arguments(ProductsQueryArgsSchema, location="query")
        @products_smorest_bp.response(200, ProductsResponseSchema)
        def get(self, args):
            """Get paginated list of products with optional search (real endpoint)."""
            # Import here to avoid circular imports and missing dependencies
            from src.models.inventory import Product

            page = args.get("page", 1)
            per_page = args.get("per_page", 10)
            search = args.get("search", "")
            category_id = args.get("category_id")

            query = Product.query

            if search:
                query = query.filter(Product.name.contains(search))

            if category_id:
                query = query.filter(Product.category_id == category_id)

            products = query.paginate(page=page, per_page=per_page, error_out=False)

            items = [product.to_dict() for product in products.items]

            return {
                "status": "success",
                "data": items,
                "items": items,
                "pagination": {
                    "page": page,
                    "pages": products.pages,
                    "per_page": per_page,
                    "total": products.total,
                },
            }, 200
