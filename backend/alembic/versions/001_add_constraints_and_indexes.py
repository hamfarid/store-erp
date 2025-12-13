# FILE: backend/alembic/versions/001_add_constraints_and_indexes.py
# PURPOSE: Add database constraints and indexes for performance
# OWNER: Gaara Store Team
# RELATED: backend/database.py, backend/src/models/
# LAST-AUDITED: 2025-10-27

"""
Add constraints and indexes to database tables.

Revision ID: 001
Revises: None
Create Date: 2025-10-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Add constraints and indexes"""

    # ============================================================================
    # Users Table Indexes
    # ============================================================================
    op.create_index("idx_users_username", "users", ["username"], unique=True)
    op.create_index("idx_users_email", "users", ["email"], unique=True)
    op.create_index("idx_users_role_id", "users", ["role_id"])
    op.create_index("idx_users_is_active", "users", ["is_active"])
    op.create_index("idx_users_created_at", "users", ["created_at"])

    # ============================================================================
    # Products Table Indexes
    # ============================================================================
    op.create_index("idx_products_sku", "products", ["sku"], unique=True)
    op.create_index("idx_products_category_id", "products", ["category_id"])
    op.create_index("idx_products_is_active", "products", ["is_active"])
    op.create_index("idx_products_created_at", "products", ["created_at"])
    op.create_index("idx_products_name", "products", ["name"])

    # ============================================================================
    # Customers Table Indexes
    # ============================================================================
    op.create_index("idx_customers_email", "customers", ["email"], unique=True)
    op.create_index("idx_customers_phone", "customers", ["phone"])
    op.create_index("idx_customers_is_active", "customers", ["is_active"])
    op.create_index("idx_customers_created_at", "customers", ["created_at"])

    # ============================================================================
    # Suppliers Table Indexes
    # ============================================================================
    op.create_index("idx_suppliers_email", "suppliers", ["email"], unique=True)
    op.create_index("idx_suppliers_phone", "suppliers", ["phone"])
    op.create_index("idx_suppliers_is_active", "suppliers", ["is_active"])
    op.create_index("idx_suppliers_created_at", "suppliers", ["created_at"])

    # ============================================================================
    # Invoices Table Indexes
    # ============================================================================
    op.create_index(
        "idx_invoices_invoice_number", "invoices", ["invoice_number"], unique=True
    )
    op.create_index("idx_invoices_customer_id", "invoices", ["customer_id"])
    op.create_index("idx_invoices_status", "invoices", ["status"])
    op.create_index("idx_invoices_invoice_date", "invoices", ["invoice_date"])
    op.create_index("idx_invoices_due_date", "invoices", ["due_date"])
    op.create_index("idx_invoices_created_at", "invoices", ["created_at"])

    # ============================================================================
    # Invoice Items Table Indexes
    # ============================================================================
    op.create_index("idx_invoice_items_invoice_id", "invoice_items", ["invoice_id"])
    op.create_index("idx_invoice_items_product_id", "invoice_items", ["product_id"])

    # ============================================================================
    # Stock Movements Table Indexes
    # ============================================================================
    op.create_index("idx_stock_movements_product_id", "stock_movements", ["product_id"])
    op.create_index(
        "idx_stock_movements_warehouse_id", "stock_movements", ["warehouse_id"]
    )
    op.create_index(
        "idx_stock_movements_movement_type", "stock_movements", ["movement_type"]
    )
    op.create_index("idx_stock_movements_created_at", "stock_movements", ["created_at"])

    # ============================================================================
    # Categories Table Indexes
    # ============================================================================
    op.create_index("idx_categories_name", "categories", ["name"], unique=True)
    op.create_index("idx_categories_is_active", "categories", ["is_active"])
    op.create_index("idx_categories_parent_id", "categories", ["parent_id"])

    # ============================================================================
    # Warehouses Table Indexes
    # ============================================================================
    op.create_index("idx_warehouses_name", "warehouses", ["name"], unique=True)
    op.create_index("idx_warehouses_is_active", "warehouses", ["is_active"])

    # ============================================================================
    # Roles Table Indexes
    # ============================================================================
    op.create_index("idx_roles_name", "roles", ["name"], unique=True)


def downgrade():
    """Remove constraints and indexes"""

    # Drop all indexes in reverse order
    op.drop_index("idx_roles_name")
    op.drop_index("idx_warehouses_is_active")
    op.drop_index("idx_warehouses_name")
    op.drop_index("idx_categories_parent_id")
    op.drop_index("idx_categories_is_active")
    op.drop_index("idx_categories_name")
    op.drop_index("idx_stock_movements_created_at")
    op.drop_index("idx_stock_movements_movement_type")
    op.drop_index("idx_stock_movements_warehouse_id")
    op.drop_index("idx_stock_movements_product_id")
    op.drop_index("idx_invoice_items_product_id")
    op.drop_index("idx_invoice_items_invoice_id")
    op.drop_index("idx_invoices_created_at")
    op.drop_index("idx_invoices_due_date")
    op.drop_index("idx_invoices_invoice_date")
    op.drop_index("idx_invoices_status")
    op.drop_index("idx_invoices_customer_id")
    op.drop_index("idx_invoices_invoice_number")
    op.drop_index("idx_suppliers_created_at")
    op.drop_index("idx_suppliers_is_active")
    op.drop_index("idx_suppliers_phone")
    op.drop_index("idx_suppliers_email")
    op.drop_index("idx_customers_created_at")
    op.drop_index("idx_customers_is_active")
    op.drop_index("idx_customers_phone")
    op.drop_index("idx_customers_email")
    op.drop_index("idx_products_name")
    op.drop_index("idx_products_created_at")
    op.drop_index("idx_products_is_active")
    op.drop_index("idx_products_category_id")
    op.drop_index("idx_products_sku")
    op.drop_index("idx_users_created_at")
    op.drop_index("idx_users_is_active")
    op.drop_index("idx_users_role_id")
    op.drop_index("idx_users_email")
    op.drop_index("idx_users_username")
