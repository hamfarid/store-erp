"""add missing columns to core tables

Revision ID: a1b2c3d4e5f6
Revises: e593e8338c1e
Create Date: 2025-10-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'e593e8338c1e'
branch_labels = None
depends_on = None


def _missing(table: str, columns: list[str]) -> set[str]:
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    existing = {col['name'] for col in inspector.get_columns(table)}
    return set(columns) - existing


def upgrade():
    # users table
    try:
        miss = _missing(
            'users',
            ['login_count', 'last_login', 'updated_at', 'phone', 'department', 'notes']
        )
        if 'login_count' in miss:
            op.add_column(
                'users',
                sa.Column('login_count', sa.Integer(), server_default='0')
            )
        if 'last_login' in miss:
            op.add_column(
                'users',
                sa.Column('last_login', sa.DateTime(), nullable=True)
            )
        if 'updated_at' in miss:
            op.add_column(
                'users',
                sa.Column('updated_at', sa.DateTime(), nullable=True)
            )
        if 'phone' in miss:
            op.add_column(
                'users',
                sa.Column('phone', sa.String(length=20), nullable=True)
            )
        if 'department' in miss:
            op.add_column(
                'users',
                sa.Column('department', sa.String(length=50), nullable=True)
            )
        if 'notes' in miss:
            op.add_column(
                'users',
                sa.Column('notes', sa.Text(), nullable=True)
            )
    except Exception:
        # best-effort; don't fail upgrade entirely
        pass

    # categories table
    try:
        miss = _missing(
            'categories',
            ['description', 'parent_id', 'is_active', 'created_at', 'updated_at']
        )
        if 'description' in miss:
            op.add_column(
                'categories',
                sa.Column('description', sa.Text(), nullable=True)
            )
        if 'parent_id' in miss:
            op.add_column(
                'categories',
                sa.Column('parent_id', sa.Integer(), nullable=True)
            )
        if 'is_active' in miss:
            op.add_column(
                'categories',
                sa.Column('is_active', sa.Boolean(), server_default=sa.text('1'))
            )
        if 'created_at' in miss:
            op.add_column(
                'categories',
                sa.Column('created_at', sa.DateTime(), nullable=True)
            )
        if 'updated_at' in miss:
            op.add_column(
                'categories',
                sa.Column('updated_at', sa.DateTime(), nullable=True)
            )
    except Exception:
        pass

    # warehouses table
    try:
        miss = _missing(
            'warehouses',
            ['code', 'address', 'manager_id', 'is_active', 'created_at']
        )
        if 'code' in miss:
            op.add_column(
                'warehouses',
                sa.Column('code', sa.String(length=20), nullable=True)
            )
        if 'address' in miss:
            op.add_column(
                'warehouses',
                sa.Column('address', sa.Text(), nullable=True)
            )
        if 'manager_id' in miss:
            op.add_column(
                'warehouses',
                sa.Column('manager_id', sa.Integer(), nullable=True)
            )
        if 'is_active' in miss:
            op.add_column(
                'warehouses',
                sa.Column('is_active', sa.Boolean(), server_default=sa.text('1'))
            )
        if 'created_at' in miss:
            op.add_column(
                'warehouses',
                sa.Column('created_at', sa.DateTime(), nullable=True)
            )
    except Exception:
        pass


def downgrade():
    # Attempt to drop columns if supported by the backend
    try:
        op.drop_column('warehouses', 'created_at')
        op.drop_column('warehouses', 'is_active')
        op.drop_column('warehouses', 'manager_id')
        op.drop_column('warehouses', 'address')
        op.drop_column('warehouses', 'code')
    except Exception:
        pass
    try:
        op.drop_column('categories', 'updated_at')
        op.drop_column('categories', 'created_at')
        op.drop_column('categories', 'is_active')
        op.drop_column('categories', 'parent_id')
        op.drop_column('categories', 'description')
    except Exception:
        pass
    try:
        op.drop_column('users', 'notes')
        op.drop_column('users', 'department')
        op.drop_column('users', 'phone')
        op.drop_column('users', 'updated_at')
        op.drop_column('users', 'last_login')
        op.drop_column('users', 'login_count')
    except Exception:
        pass
