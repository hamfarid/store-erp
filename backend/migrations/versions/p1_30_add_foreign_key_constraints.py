"""P1.30: Add missing foreign key constraints

Revision ID: p1_30_fk_constraints
Revises: p1_31_indexes
Create Date: 2025-12-01 14:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "p1_30_fk_constraints"
down_revision = "p1_31_indexes"
branch_labels = None
depends_on = None


def upgrade():
    """
    P1.30: Add missing foreign key constraints for referential integrity.

    Foreign keys ensure:
    - Data consistency across tables
    - Cascade delete/update behavior
    - Prevention of orphan records
    """

    # ==========================================================================
    # Users Table Foreign Keys
    # ==========================================================================

    # users.role_id -> roles.id
    op.create_foreign_key(
        "fk_users_role_id", "users", "roles", ["role_id"], ["id"], ondelete="SET NULL"
    )

    # ==========================================================================
    # Products Table Foreign Keys
    # ==========================================================================

    # products.category_id -> categories.id
    op.create_foreign_key(
        "fk_products_category_id",
        "products",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # products.brand_id -> brands.id
    op.create_foreign_key(
        "fk_products_brand_id",
        "products",
        "brands",
        ["brand_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # products.created_by -> users.id
    op.create_foreign_key(
        "fk_products_created_by",
        "products",
        "users",
        ["created_by"],
        ["id"],
        ondelete="SET NULL",
    )

    # ==========================================================================
    # Product Images Table Foreign Keys
    # ==========================================================================

    # product_images.product_id -> products.id
    op.create_foreign_key(
        "fk_product_images_product_id",
        "product_images",
        "products",
        ["product_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # ==========================================================================
    # Categories Table Foreign Keys (Self-referential)
    # ==========================================================================

    # categories.parent_id -> categories.id
    op.create_foreign_key(
        "fk_categories_parent_id",
        "categories",
        "categories",
        ["parent_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # ==========================================================================
    # Inventory Table Foreign Keys
    # ==========================================================================

    # inventory.product_id -> products.id
    op.create_foreign_key(
        "fk_inventory_product_id",
        "inventory",
        "products",
        ["product_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # inventory.warehouse_id -> warehouses.id
    op.create_foreign_key(
        "fk_inventory_warehouse_id",
        "inventory",
        "warehouses",
        ["warehouse_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # ==========================================================================
    # Stock Movements Table Foreign Keys
    # ==========================================================================

    # stock_movements.product_id -> products.id
    op.create_foreign_key(
        "fk_stock_movements_product_id",
        "stock_movements",
        "products",
        ["product_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # stock_movements.warehouse_id -> warehouses.id
    op.create_foreign_key(
        "fk_stock_movements_warehouse_id",
        "stock_movements",
        "warehouses",
        ["warehouse_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # stock_movements.created_by -> users.id
    op.create_foreign_key(
        "fk_stock_movements_created_by",
        "stock_movements",
        "users",
        ["created_by"],
        ["id"],
        ondelete="SET NULL",
    )

    # ==========================================================================
    # Invoices Table Foreign Keys
    # ==========================================================================

    # invoices.customer_id -> customers.id
    op.create_foreign_key(
        "fk_invoices_customer_id",
        "invoices",
        "customers",
        ["customer_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # invoices.supplier_id -> suppliers.id
    op.create_foreign_key(
        "fk_invoices_supplier_id",
        "invoices",
        "suppliers",
        ["supplier_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # invoices.warehouse_id -> warehouses.id
    op.create_foreign_key(
        "fk_invoices_warehouse_id",
        "invoices",
        "warehouses",
        ["warehouse_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # invoices.user_id -> users.id
    op.create_foreign_key(
        "fk_invoices_user_id",
        "invoices",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # ==========================================================================
    # Invoice Items Table Foreign Keys
    # ==========================================================================

    # invoice_items.invoice_id -> invoices.id
    op.create_foreign_key(
        "fk_invoice_items_invoice_id",
        "invoice_items",
        "invoices",
        ["invoice_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # invoice_items.product_id -> products.id
    op.create_foreign_key(
        "fk_invoice_items_product_id",
        "invoice_items",
        "products",
        ["product_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # ==========================================================================
    # Payments Table Foreign Keys
    # ==========================================================================

    # payments.invoice_id -> invoices.id
    op.create_foreign_key(
        "fk_payments_invoice_id",
        "payments",
        "invoices",
        ["invoice_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # payments.created_by -> users.id
    op.create_foreign_key(
        "fk_payments_created_by",
        "payments",
        "users",
        ["created_by"],
        ["id"],
        ondelete="SET NULL",
    )

    # ==========================================================================
    # Refresh Tokens Table Foreign Keys
    # ==========================================================================

    # refresh_tokens.user_id -> users.id
    op.create_foreign_key(
        "fk_refresh_tokens_user_id",
        "refresh_tokens",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # ==========================================================================
    # Activity Logs Table Foreign Keys
    # ==========================================================================

    # activity_logs.user_id -> users.id
    op.create_foreign_key(
        "fk_activity_logs_user_id",
        "activity_logs",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # ==========================================================================
    # Notifications Table Foreign Keys
    # ==========================================================================

    # notifications.user_id -> users.id
    op.create_foreign_key(
        "fk_notifications_user_id",
        "notifications",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade():
    """Remove all foreign key constraints."""

    # Notifications
    op.drop_constraint("fk_notifications_user_id", "notifications", type_="foreignkey")

    # Activity Logs
    op.drop_constraint("fk_activity_logs_user_id", "activity_logs", type_="foreignkey")

    # Refresh Tokens
    op.drop_constraint(
        "fk_refresh_tokens_user_id", "refresh_tokens", type_="foreignkey"
    )

    # Payments
    op.drop_constraint("fk_payments_created_by", "payments", type_="foreignkey")
    op.drop_constraint("fk_payments_invoice_id", "payments", type_="foreignkey")

    # Invoice Items
    op.drop_constraint(
        "fk_invoice_items_product_id", "invoice_items", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_invoice_items_invoice_id", "invoice_items", type_="foreignkey"
    )

    # Invoices
    op.drop_constraint("fk_invoices_user_id", "invoices", type_="foreignkey")
    op.drop_constraint("fk_invoices_warehouse_id", "invoices", type_="foreignkey")
    op.drop_constraint("fk_invoices_supplier_id", "invoices", type_="foreignkey")
    op.drop_constraint("fk_invoices_customer_id", "invoices", type_="foreignkey")

    # Stock Movements
    op.drop_constraint(
        "fk_stock_movements_created_by", "stock_movements", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_stock_movements_warehouse_id", "stock_movements", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_stock_movements_product_id", "stock_movements", type_="foreignkey"
    )

    # Inventory
    op.drop_constraint("fk_inventory_warehouse_id", "inventory", type_="foreignkey")
    op.drop_constraint("fk_inventory_product_id", "inventory", type_="foreignkey")

    # Categories
    op.drop_constraint("fk_categories_parent_id", "categories", type_="foreignkey")

    # Product Images
    op.drop_constraint(
        "fk_product_images_product_id", "product_images", type_="foreignkey"
    )

    # Products
    op.drop_constraint("fk_products_created_by", "products", type_="foreignkey")
    op.drop_constraint("fk_products_brand_id", "products", type_="foreignkey")
    op.drop_constraint("fk_products_category_id", "products", type_="foreignkey")

    # Users
    op.drop_constraint("fk_users_role_id", "users", type_="foreignkey")
