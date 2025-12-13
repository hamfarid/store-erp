# FILE: backend/alembic/versions/002_add_foreign_keys.py
# PURPOSE: Add foreign key constraints to database tables
# OWNER: Gaara Store Team
# RELATED: backend/database.py, backend/src/models/
# LAST-AUDITED: 2025-10-27

"""
Add foreign key constraints to database tables.

Revision ID: 002
Revises: 001
Create Date: 2025-10-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    """Add foreign key constraints"""

    # ============================================================================
    # Users Table Foreign Keys
    # ============================================================================
    op.create_foreign_key(
        "fk_users_role_id", "users", "roles", ["role_id"], ["id"], ondelete="RESTRICT"
    )

    # ============================================================================
    # Products Table Foreign Keys
    # ============================================================================
    op.create_foreign_key(
        "fk_products_category_id",
        "products",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # ============================================================================
    # Invoices Table Foreign Keys
    # ============================================================================
    op.create_foreign_key(
        "fk_invoices_customer_id",
        "invoices",
        "customers",
        ["customer_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # ============================================================================
    # Invoice Items Table Foreign Keys
    # ============================================================================
    op.create_foreign_key(
        "fk_invoice_items_invoice_id",
        "invoice_items",
        "invoices",
        ["invoice_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "fk_invoice_items_product_id",
        "invoice_items",
        "products",
        ["product_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # ============================================================================
    # Stock Movements Table Foreign Keys
    # ============================================================================
    op.create_foreign_key(
        "fk_stock_movements_product_id",
        "stock_movements",
        "products",
        ["product_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    op.create_foreign_key(
        "fk_stock_movements_warehouse_id",
        "stock_movements",
        "warehouses",
        ["warehouse_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # ============================================================================
    # Categories Table Foreign Keys (for hierarchical categories)
    # ============================================================================
    op.create_foreign_key(
        "fk_categories_parent_id",
        "categories",
        "categories",
        ["parent_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade():
    """Remove foreign key constraints"""

    # Drop all foreign keys in reverse order
    op.drop_constraint("fk_categories_parent_id", "categories", type_="foreignkey")
    op.drop_constraint(
        "fk_stock_movements_warehouse_id", "stock_movements", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_stock_movements_product_id", "stock_movements", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_invoice_items_product_id", "invoice_items", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_invoice_items_invoice_id", "invoice_items", type_="foreignkey"
    )
    op.drop_constraint("fk_invoices_customer_id", "invoices", type_="foreignkey")
    op.drop_constraint("fk_products_category_id", "products", type_="foreignkey")
    op.drop_constraint("fk_users_role_id", "users", type_="foreignkey")
