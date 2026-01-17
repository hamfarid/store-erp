"""Add journal_entries and journal_config tables

Revision ID: add_journal_001
Revises: 6efc3153bd83
Create Date: 2025-11-28
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_journal_001"
down_revision = "6efc3153bd83"
branch_labels = None
depends_on = None


def upgrade():
    # Create journal_entries table
    op.create_table(
        "journal_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("event_type", sa.String(50), nullable=False, index=True),
        sa.Column("model_type", sa.String(50), nullable=True, index=True),
        sa.Column("model_id", sa.Integer(), nullable=True, index=True),
        sa.Column("reference_number", sa.String(100), nullable=True, index=True),
        sa.Column("source_reference", sa.String(100), nullable=True),
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("old_values", sa.JSON(), nullable=True),
        sa.Column("new_values", sa.JSON(), nullable=True),
        sa.Column("extra_data", sa.JSON(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(100), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # Create journal_config table
    op.create_table(
        "journal_config",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("event_type", sa.String(50), nullable=False, unique=True),
        sa.Column("is_enabled", sa.Boolean(), default=True),
        sa.Column("send_notification", sa.Boolean(), default=False),
        sa.Column("send_email", sa.Boolean(), default=False),
        sa.Column("email_recipients", sa.JSON(), nullable=True),
        sa.Column("webhook_url", sa.String(500), nullable=True),
        sa.Column("retention_days", sa.Integer(), default=365),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), onupdate=sa.func.now()),
    )

    # Create indexes for better query performance
    op.create_index("ix_journal_created_at", "journal_entries", ["created_at"])
    op.create_index("ix_journal_model", "journal_entries", ["model_type", "model_id"])


def downgrade():
    op.drop_index("ix_journal_model", "journal_entries")
    op.drop_index("ix_journal_created_at", "journal_entries")
    op.drop_table("journal_config")
    op.drop_table("journal_entries")
