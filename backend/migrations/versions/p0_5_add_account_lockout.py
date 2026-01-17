"""P0.5: Add account lockout fields to users table

Revision ID: p0_5_lockout
Revises:
Create Date: 2025-12-01

This migration adds the following security fields:
- failed_login_count: Tracks failed login attempts
- locked_until: Timestamp when account lockout expires
- last_failed_login: Timestamp of last failed login attempt
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "p0_5_lockout"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Add account lockout fields to users table"""
    # Add columns with defaults
    op.add_column(
        "users",
        sa.Column(
            "failed_login_count", sa.Integer(), nullable=True, server_default="0"
        ),
    )
    op.add_column("users", sa.Column("locked_until", sa.DateTime(), nullable=True))
    op.add_column("users", sa.Column("last_failed_login", sa.DateTime(), nullable=True))

    # Update existing rows to have 0 failed login count
    op.execute(
        "UPDATE users SET failed_login_count = 0 WHERE failed_login_count IS NULL"
    )


def downgrade():
    """Remove account lockout fields from users table"""
    op.drop_column("users", "last_failed_login")
    op.drop_column("users", "locked_until")
    op.drop_column("users", "failed_login_count")
