"""Create admin tables for roles and permissions

Revision ID: admin_001
Revises:
Create Date: 2024-12-02

"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = "admin_001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create permissions table
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("name_ar", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("description_ar", sa.Text(), nullable=True),
        sa.Column("module", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(), default=datetime.utcnow),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_permissions_code", "permissions", ["code"])
    op.create_index("ix_permissions_module", "permissions", ["module"])

    # Create roles table
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("name_ar", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("description_ar", sa.Text(), nullable=True),
        sa.Column("color", sa.String(20), default="blue"),
        sa.Column("icon", sa.String(50), default="shield"),
        sa.Column("is_system", sa.Boolean(), default=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("priority", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(), default=datetime.utcnow),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        ),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
    )
    op.create_index("ix_roles_code", "roles", ["code"])

    # Create role_permissions association table
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["permission_id"], ["permissions.id"], ondelete="CASCADE"
        ),
    )

    # Create user_roles association table
    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(), default=datetime.utcnow),
        sa.Column("assigned_by", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["assigned_by"], ["users.id"]),
    )

    # Create system_setup table
    op.create_table(
        "system_setup",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_completed", sa.Boolean(), default=False),
        sa.Column("setup_step", sa.Integer(), default=0),
        sa.Column("company_name", sa.String(200), nullable=True),
        sa.Column("company_name_ar", sa.String(200), nullable=True),
        sa.Column("company_email", sa.String(200), nullable=True),
        sa.Column("company_phone", sa.String(50), nullable=True),
        sa.Column("company_address", sa.Text(), nullable=True),
        sa.Column("company_logo", sa.String(500), nullable=True),
        sa.Column("tax_number", sa.String(50), nullable=True),
        sa.Column("commercial_register", sa.String(50), nullable=True),
        sa.Column("currency", sa.String(10), default="EGP"),
        sa.Column("timezone", sa.String(50), default="Asia/Riyadh"),
        sa.Column("language", sa.String(10), default="ar"),
        sa.Column("fiscal_year_start", sa.Integer(), default=1),
        sa.Column("admin_created", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), default=datetime.utcnow),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create audit_logs table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("resource_type", sa.String(50), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=True),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("ip_address", sa.String(50), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"])


def downgrade():
    op.drop_table("audit_logs")
    op.drop_table("system_setup")
    op.drop_table("user_roles")
    op.drop_table("role_permissions")
    op.drop_table("roles")
    op.drop_table("permissions")
