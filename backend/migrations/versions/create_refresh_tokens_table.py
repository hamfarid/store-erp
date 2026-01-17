# FILE: backend/migrations/versions/create_refresh_tokens_table.py | PURPOSE: Create refresh_tokens table for JWT token rotation | OWNER: security | RELATED: backend/src/models/refresh_token.py | LAST-AUDITED: 2025-11-04

"""create refresh_tokens table

Revision ID: refresh_tokens_001
Revises:
Create Date: 2025-11-04

P0.2: JWT token rotation with refresh token storage
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone


# revision identifiers, used by Alembic.
revision = "refresh_tokens_001"
down_revision = None  # Update this to the latest migration ID
branch_labels = None
depends_on = None


def upgrade():
    """Create refresh_tokens table"""
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("jti", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revocation_reason", sa.String(length=255), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("device_fingerprint", sa.String(length=128), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "last_used_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    # Create indexes
    op.create_index("idx_refresh_token_jti", "refresh_tokens", ["jti"], unique=True)
    op.create_index("idx_refresh_token_user_id", "refresh_tokens", ["user_id"])
    op.create_index("idx_refresh_token_expires_at", "refresh_tokens", ["expires_at"])
    op.create_index("idx_refresh_token_is_revoked", "refresh_tokens", ["is_revoked"])
    op.create_index(
        "idx_refresh_token_user_active",
        "refresh_tokens",
        ["user_id", "is_revoked", "expires_at"],
    )
    op.create_index(
        "idx_refresh_token_jti_active", "refresh_tokens", ["jti", "is_revoked"]
    )


def downgrade():
    """Drop refresh_tokens table"""
    op.drop_index("idx_refresh_token_jti_active", table_name="refresh_tokens")
    op.drop_index("idx_refresh_token_user_active", table_name="refresh_tokens")
    op.drop_index("idx_refresh_token_is_revoked", table_name="refresh_tokens")
    op.drop_index("idx_refresh_token_expires_at", table_name="refresh_tokens")
    op.drop_index("idx_refresh_token_user_id", table_name="refresh_tokens")
    op.drop_index("idx_refresh_token_jti", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
