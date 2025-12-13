"""P1.31: Add performance indexes for common queries

Revision ID: p1_31_indexes
Revises: p0_5_add_account_lockout
Create Date: 2025-12-01 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "p1_31_indexes"
down_revision = "p0_5_add_account_lockout"
branch_labels = None
depends_on = None


def upgrade():
    """
    P1.31: Add performance indexes for common queries.

    These indexes improve query performance for:
    - Search operations (name, barcode, email)
    - Filtering (status, type, date)
    - Foreign key lookups
    - Composite queries
    """

    # ==========================================================================
    # Products Table Indexes
    # ==========================================================================
    op.create_index("ix_products_barcode", "products", ["barcode"], unique=False)
    op.create_index("ix_products_name", "products", ["name"], unique=False)
    op.create_index("ix_products_sku", "products", ["sku"], unique=False)
    op.create_index("ix_products_is_active", "products", ["is_active"], unique=False)
    op.create_index(
        "ix_products_category_id", "products", ["category_id"], unique=False
    )
    op.create_index("ix_products_created_at", "products", ["created_at"], unique=False)

    # ==========================================================================
    # Users Table Indexes
    # ==========================================================================
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_is_active", "users", ["is_active"], unique=False)
    op.create_index("ix_users_role_id", "users", ["role_id"], unique=False)
    op.create_index("ix_users_last_login", "users", ["last_login"], unique=False)

    # ==========================================================================
    # Customers Table Indexes
    # ==========================================================================
    op.create_index("ix_customers_name", "customers", ["name"], unique=False)
    op.create_index("ix_customers_email", "customers", ["email"], unique=False)
    op.create_index("ix_customers_phone", "customers", ["phone"], unique=False)
    op.create_index("ix_customers_is_active", "customers", ["is_active"], unique=False)
    op.create_index("ix_customers_city", "customers", ["city"], unique=False)

    # ==========================================================================
    # Suppliers Table Indexes
    # ==========================================================================
    op.create_index("ix_suppliers_name", "suppliers", ["name"], unique=False)
    op.create_index("ix_suppliers_email", "suppliers", ["email"], unique=False)
    op.create_index("ix_suppliers_is_active", "suppliers", ["is_active"], unique=False)

    # ==========================================================================
    # Stock Movements Table Indexes
    # ==========================================================================
    op.create_index(
        "ix_stock_movements_product_id", "stock_movements", ["product_id"], unique=False
    )
    op.create_index(
        "ix_stock_movements_warehouse_id",
        "stock_movements",
        ["warehouse_id"],
        unique=False,
    )
    op.create_index(
        "ix_stock_movements_type", "stock_movements", ["movement_type"], unique=False
    )
    op.create_index(
        "ix_stock_movements_date", "stock_movements", ["movement_date"], unique=False
    )
    op.create_index(
        "ix_stock_movements_reference",
        "stock_movements",
        ["reference_number"],
        unique=False,
    )
    op.create_index(
        "ix_stock_movements_created_at", "stock_movements", ["created_at"], unique=False
    )

    # ==========================================================================
    # Invoices Table Indexes
    # ==========================================================================
    op.create_index(
        "ix_invoices_invoice_number", "invoices", ["invoice_number"], unique=False
    )
    op.create_index(
        "ix_invoices_customer_id", "invoices", ["customer_id"], unique=False
    )
    op.create_index(
        "ix_invoices_supplier_id", "invoices", ["supplier_id"], unique=False
    )
    op.create_index("ix_invoices_status", "invoices", ["status"], unique=False)
    op.create_index("ix_invoices_type", "invoices", ["invoice_type"], unique=False)
    op.create_index("ix_invoices_date", "invoices", ["invoice_date"], unique=False)
    op.create_index("ix_invoices_created_at", "invoices", ["created_at"], unique=False)

    # ==========================================================================
    # Refresh Tokens Table Indexes
    # ==========================================================================
    op.create_index("ix_refresh_tokens_jti", "refresh_tokens", ["jti"], unique=True)
    op.create_index(
        "ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"], unique=False
    )
    op.create_index(
        "ix_refresh_tokens_expires_at", "refresh_tokens", ["expires_at"], unique=False
    )
    op.create_index(
        "ix_refresh_tokens_revoked", "refresh_tokens", ["revoked"], unique=False
    )

    # ==========================================================================
    # Composite Indexes for Common Query Patterns
    # ==========================================================================
    # Stock movements by product and warehouse
    op.create_index(
        "ix_stock_movements_product_warehouse",
        "stock_movements",
        ["product_id", "warehouse_id"],
        unique=False,
    )

    # Stock movements by date and type (for reports)
    op.create_index(
        "ix_stock_movements_date_type",
        "stock_movements",
        ["movement_date", "movement_type"],
        unique=False,
    )

    # Invoices by customer and date
    op.create_index(
        "ix_invoices_customer_date",
        "invoices",
        ["customer_id", "invoice_date"],
        unique=False,
    )

    # Users by role and active status
    op.create_index(
        "ix_users_role_active", "users", ["role_id", "is_active"], unique=False
    )


def downgrade():
    """Remove all performance indexes."""

    # Composite indexes
    op.drop_index("ix_users_role_active", "users")
    op.drop_index("ix_invoices_customer_date", "invoices")
    op.drop_index("ix_stock_movements_date_type", "stock_movements")
    op.drop_index("ix_stock_movements_product_warehouse", "stock_movements")

    # Refresh tokens indexes
    op.drop_index("ix_refresh_tokens_revoked", "refresh_tokens")
    op.drop_index("ix_refresh_tokens_expires_at", "refresh_tokens")
    op.drop_index("ix_refresh_tokens_user_id", "refresh_tokens")
    op.drop_index("ix_refresh_tokens_jti", "refresh_tokens")

    # Invoices indexes
    op.drop_index("ix_invoices_created_at", "invoices")
    op.drop_index("ix_invoices_date", "invoices")
    op.drop_index("ix_invoices_type", "invoices")
    op.drop_index("ix_invoices_status", "invoices")
    op.drop_index("ix_invoices_supplier_id", "invoices")
    op.drop_index("ix_invoices_customer_id", "invoices")
    op.drop_index("ix_invoices_invoice_number", "invoices")

    # Stock movements indexes
    op.drop_index("ix_stock_movements_created_at", "stock_movements")
    op.drop_index("ix_stock_movements_reference", "stock_movements")
    op.drop_index("ix_stock_movements_date", "stock_movements")
    op.drop_index("ix_stock_movements_type", "stock_movements")
    op.drop_index("ix_stock_movements_warehouse_id", "stock_movements")
    op.drop_index("ix_stock_movements_product_id", "stock_movements")

    # Suppliers indexes
    op.drop_index("ix_suppliers_is_active", "suppliers")
    op.drop_index("ix_suppliers_email", "suppliers")
    op.drop_index("ix_suppliers_name", "suppliers")

    # Customers indexes
    op.drop_index("ix_customers_city", "customers")
    op.drop_index("ix_customers_is_active", "customers")
    op.drop_index("ix_customers_phone", "customers")
    op.drop_index("ix_customers_email", "customers")
    op.drop_index("ix_customers_name", "customers")

    # Users indexes
    op.drop_index("ix_users_last_login", "users")
    op.drop_index("ix_users_role_id", "users")
    op.drop_index("ix_users_is_active", "users")
    op.drop_index("ix_users_email", "users")
    op.drop_index("ix_users_username", "users")

    # Products indexes
    op.drop_index("ix_products_created_at", "products")
    op.drop_index("ix_products_category_id", "products")
    op.drop_index("ix_products_is_active", "products")
    op.drop_index("ix_products_sku", "products")
    op.drop_index("ix_products_name", "products")
    op.drop_index("ix_products_barcode", "products")
