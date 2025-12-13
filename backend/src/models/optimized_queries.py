# -*- coding: utf-8 -*-
# FILE: backend/src/models/optimized_queries.py
# PURPOSE: Optimized Database Queries
# OWNER: Backend
# RELATED: models/
# LAST-AUDITED: 2025-10-21

"""
استعلامات قاعدة البيانات المحسنة - الإصدار 2.0
Optimized Database Queries - Version 2.0

P1 Fixes Applied:
- P1.7: Fix N+1 query problems with eager loading
- P1.8: Optimize complex queries with joins
- P1.9: Add query result caching
"""

from sqlalchemy import select, func, or_
from sqlalchemy.orm import joinedload
from ..database import db
from .product_unified import Product
from .inventory import Category, StockMovement
from ..cache_manager import cached


class OptimizedQueries:
    """Collection of optimized database queries."""

    @staticmethod
    @cached(timeout=600, key_prefix="optimized_products")
    def get_products_with_categories(page=1, per_page=20, search=""):
        """Get products with categories - optimized to avoid N+1."""
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .filter(Product.is_active.is_(True))
        )

        if search:
            search_term = f"%{search}%"
            stmt = stmt.filter(
                or_(
                    Product.name.like(search_term),
                    Product.sku.like(search_term),
                    Product.barcode.like(search_term),
                )
            )

        products = db.paginate(stmt, page=page, per_page=per_page, error_out=False)

        result = []
        for product in products.items:
            result.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "sku": product.sku,
                    "price": product.price,
                    "category": (
                        {"id": product.category.id, "name": product.category.name}
                        if product.category
                        else None
                    ),
                }
            )

        return {
            "products": result,
            "pagination": {
                "page": products.page,
                "pages": products.pages,
                "per_page": products.per_page,
                "total": products.total,
            },
        }

    @staticmethod
    @cached(timeout=300, key_prefix="optimized_stock_movements")
    def get_stock_movements_with_relations(
        product_id=None, warehouse_id=None, limit=100
    ):
        """Get stock movements with all related data - optimized."""
        stmt = select(StockMovement).options(
            joinedload(StockMovement.product),
            joinedload(StockMovement.warehouse),
            joinedload(StockMovement.customer),
            joinedload(StockMovement.supplier),
        )

        if product_id:
            stmt = stmt.filter(StockMovement.product_id == product_id)
        if warehouse_id:
            stmt = stmt.filter(StockMovement.warehouse_id == warehouse_id)

        stmt = stmt.order_by(StockMovement.movement_date.desc()).limit(limit)
        movements = db.session.execute(stmt).scalars().all()

        result = []
        for movement in movements:
            result.append(
                {
                    "id": movement.id,
                    "movement_type": movement.movement_type,
                    "movement_date": movement.movement_date.isoformat(),
                    "quantity_in": movement.quantity_in,
                    "quantity_out": movement.quantity_out,
                    "product": (
                        {"id": movement.product.id, "name": movement.product.name}
                        if movement.product
                        else None
                    ),
                    "warehouse": (
                        {"id": movement.warehouse.id, "name": movement.warehouse.name}
                        if movement.warehouse
                        else None
                    ),
                    "customer": (
                        {"id": movement.customer.id, "name": movement.customer.name}
                        if movement.customer
                        else None
                    ),
                    "supplier": (
                        {"id": movement.supplier.id, "name": movement.supplier.name}
                        if movement.supplier
                        else None
                    ),
                }
            )

        return result

    @staticmethod
    @cached(timeout=1800, key_prefix="optimized_inventory_summary")
    def get_inventory_summary_by_category():
        """Get inventory summary grouped by category - optimized."""
        # Use a single query with joins and aggregation
        stmt = (
            select(
                Category.id.label("category_id"),
                Category.name.label("category_name"),
                func.count(Product.id).label("product_count"),
                func.sum(Product.current_stock * Product.cost_price).label(
                    "total_value"
                ),
            )
            .join(Product, Category.id == Product.category_id)
            .filter(Product.is_active.is_(True))
            .group_by(Category.id, Category.name)
        )
        result = db.session.execute(stmt).all()

        return [
            {
                "category_id": row.category_id,
                "category_name": row.category_name,
                "product_count": row.product_count,
                "total_value": float(row.total_value or 0),
            }
            for row in result
        ]

    @staticmethod
    @cached(timeout=600, key_prefix="optimized_low_stock")
    def get_low_stock_products():
        """Get products with low stock - optimized."""
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .filter(
                Product.is_active.is_(True),
                Product.current_stock <= Product.reorder_quantity,
            )
        )
        products = db.session.execute(stmt).scalars().all()

        result = []
        for product in products:
            shortage = max(0, product.reorder_quantity - product.current_stock)
            result.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "sku": product.sku,
                    "current_stock": product.current_stock,
                    "reorder_quantity": product.reorder_quantity,
                    "shortage": shortage,
                    "category": (
                        {"id": product.category.id, "name": product.category.name}
                        if product.category
                        else None
                    ),
                }
            )

        return result

    @staticmethod
    @cached(timeout=1200, key_prefix="optimized_customer_orders")
    def get_customers_with_recent_orders(days=30):  # noqa: ARG004
        """Get customers with their recent orders - optimized.

        Note: Currently returns empty list.
        TODO: Re-enable when Sale model is properly defined.
        """
        # Placeholder: Return empty list until Sale model available
        return []

    @staticmethod
    def bulk_update_stock(stock_updates):
        """Bulk update stock levels - optimized for performance."""
        try:
            for update in stock_updates:
                product_id = update["product_id"]
                new_stock = update["new_stock"]

                # Use bulk update for better performance
                stmt = select(Product).filter(Product.id == product_id)
                product = db.session.execute(stmt).scalar_one()
                product.current_stock = new_stock

            db.session.commit()

            # Invalidate related cache
            from ..cache_manager import invalidate_cache_pattern

            invalidate_cache_pattern("optimized_*")
            invalidate_cache_pattern("stock:*")

            return True
        except Exception as e:
            db.session.rollback()
            raise e


# Helper functions for common query patterns


def get_products_by_ids(product_ids):
    """Get multiple products by IDs in a single query."""
    stmt = select(Product).filter(Product.id.in_(product_ids))
    return db.session.execute(stmt).scalars().all()


def get_categories_with_product_counts():
    """Get categories with their product counts."""
    stmt = (
        select(Category, func.count(Product.id).label("product_count"))
        .outerjoin(Product)
        .group_by(Category.id)
    )
    return db.session.execute(stmt).all()


def search_products_optimized(search_term, limit=50):
    """Optimized product search with full-text capabilities."""
    search_pattern = f"%{search_term}%"

    stmt = (
        select(Product)
        .options(joinedload(Product.category))
        .filter(
            or_(
                Product.name.like(search_pattern),
                Product.sku.like(search_pattern),
                Product.barcode.like(search_pattern),
                Product.description.like(search_pattern),
            )
        )
        .filter(Product.is_active.is_(True))
        .limit(limit)
    )
    return db.session.execute(stmt).scalars().all()
