# FILE: backend/alembic/versions/003_add_check_constraints.py
# PURPOSE: Add check constraints to database tables
# OWNER: Gaara Store Team
# RELATED: backend/database.py, backend/src/models/
# LAST-AUDITED: 2025-10-27

"""
Add check constraints to database tables for data integrity.

Revision ID: 003
Revises: 002
Create Date: 2025-10-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade():
    """Add check constraints"""

    # ============================================================================
    # Products Table Check Constraints
    # ============================================================================
    op.create_check_constraint("ck_products_price_positive", "products", "price > 0")

    op.create_check_constraint(
        "ck_products_quantity_non_negative", "products", "quantity >= 0"
    )

    op.create_check_constraint(
        "ck_products_reorder_level_non_negative", "products", "reorder_level >= 0"
    )

    # ============================================================================
    # Invoices Table Check Constraints
    # ============================================================================
    op.create_check_constraint(
        "ck_invoices_total_non_negative", "invoices", "total >= 0"
    )

    op.create_check_constraint(
        "ck_invoices_paid_amount_non_negative", "invoices", "paid_amount >= 0"
    )

    op.create_check_constraint(
        "ck_invoices_due_date_after_invoice_date",
        "invoices",
        "due_date >= invoice_date",
    )

    # ============================================================================
    # Invoice Items Table Check Constraints
    # ============================================================================
    op.create_check_constraint(
        "ck_invoice_items_quantity_positive", "invoice_items", "quantity > 0"
    )

    op.create_check_constraint(
        "ck_invoice_items_unit_price_positive", "invoice_items", "unit_price > 0"
    )

    op.create_check_constraint(
        "ck_invoice_items_discount_percent_valid",
        "invoice_items",
        "discount_percent >= 0 AND discount_percent <= 100",
    )

    op.create_check_constraint(
        "ck_invoice_items_tax_percent_valid",
        "invoice_items",
        "tax_percent >= 0 AND tax_percent <= 100",
    )

    # ============================================================================
    # Stock Movements Table Check Constraints
    # ============================================================================
    op.create_check_constraint(
        "ck_stock_movements_quantity_positive", "stock_movements", "quantity > 0"
    )

    # ============================================================================
    # Categories Table Check Constraints
    # ============================================================================
    op.create_check_constraint(
        "ck_categories_not_parent_of_self", "categories", "id != parent_id"
    )


def downgrade():
    """Remove check constraints"""

    # Drop all check constraints in reverse order
    op.drop_constraint("ck_categories_not_parent_of_self", "categories", type_="check")
    op.drop_constraint(
        "ck_stock_movements_quantity_positive", "stock_movements", type_="check"
    )
    op.drop_constraint(
        "ck_invoice_items_tax_percent_valid", "invoice_items", type_="check"
    )
    op.drop_constraint(
        "ck_invoice_items_discount_percent_valid", "invoice_items", type_="check"
    )
    op.drop_constraint(
        "ck_invoice_items_unit_price_positive", "invoice_items", type_="check"
    )
    op.drop_constraint(
        "ck_invoice_items_quantity_positive", "invoice_items", type_="check"
    )
    op.drop_constraint(
        "ck_invoices_due_date_after_invoice_date", "invoices", type_="check"
    )
    op.drop_constraint(
        "ck_invoices_paid_amount_non_negative", "invoices", type_="check"
    )
    op.drop_constraint("ck_invoices_total_non_negative", "invoices", type_="check")
    op.drop_constraint(
        "ck_products_reorder_level_non_negative", "products", type_="check"
    )
    op.drop_constraint("ck_products_quantity_non_negative", "products", type_="check")
    op.drop_constraint("ck_products_price_positive", "products", type_="check")
