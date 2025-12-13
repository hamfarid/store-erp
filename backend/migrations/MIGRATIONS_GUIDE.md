# Database Migrations Guide

**Task:** P1.28  
**Last Updated:** 2025-12-01  
**Technology:** Flask-Migrate (Alembic)

---

## Overview

This project uses Flask-Migrate (built on Alembic) for database schema management. 
All migrations are stored in `backend/migrations/versions/`.

---

## Quick Commands

### Check Migration Status
```bash
cd backend
flask db current    # Show current migration
flask db history    # Show migration history
flask db heads      # Show latest migration
```

### Create New Migration
```bash
# Auto-generate migration from model changes
flask db migrate -m "Description of changes"

# Create empty migration for manual SQL
flask db revision -m "Description of changes"
```

### Apply Migrations
```bash
# Apply all pending migrations
flask db upgrade

# Apply specific migration
flask db upgrade <revision_id>

# Upgrade to latest
flask db upgrade head
```

### Rollback Migrations
```bash
# Rollback last migration
flask db downgrade -1

# Rollback to specific migration
flask db downgrade <revision_id>

# Rollback all migrations (DANGEROUS!)
flask db downgrade base
```

---

## Migration File Structure

```python
"""Description of migration

Revision ID: xxxxxxxxxxxx
Revises: yyyyyyyyyyyy
Create Date: 2025-12-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'xxxxxxxxxxxx'
down_revision = 'yyyyyyyyyyyy'
branch_labels = None
depends_on = None


def upgrade():
    """Apply migration changes."""
    # Add column
    op.add_column('users', sa.Column('new_field', sa.String(100)))
    
    # Create table
    op.create_table(
        'new_table',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    
    # Create index
    op.create_index('ix_users_email', 'users', ['email'])


def downgrade():
    """Revert migration changes."""
    op.drop_index('ix_users_email', 'users')
    op.drop_table('new_table')
    op.drop_column('users', 'new_field')
```

---

## Best Practices

### 1. Always Test Migrations Locally
```bash
# Test upgrade
flask db upgrade

# Test downgrade
flask db downgrade -1

# Re-apply
flask db upgrade
```

### 2. Use Meaningful Descriptions
```bash
# Good
flask db migrate -m "Add invoice_items table with foreign keys"

# Bad
flask db migrate -m "changes"
```

### 3. Handle Data Migrations Carefully
```python
def upgrade():
    # Step 1: Add nullable column
    op.add_column('users', sa.Column('status', sa.String(20), nullable=True))
    
    # Step 2: Populate data
    op.execute("UPDATE users SET status = 'active' WHERE is_active = true")
    op.execute("UPDATE users SET status = 'inactive' WHERE is_active = false")
    
    # Step 3: Make non-nullable
    op.alter_column('users', 'status', nullable=False)
```

### 4. Use Batch Operations for SQLite
```python
def upgrade():
    # SQLite doesn't support ALTER for all operations
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('new_field', sa.String(100)))
        batch_op.drop_column('old_field')
```

### 5. Always Provide Downgrade
Every `upgrade()` should have a corresponding `downgrade()` that reverses the changes.

---

## Common Operations

### Add Column
```python
op.add_column('table_name', sa.Column('column_name', sa.String(100)))
```

### Drop Column
```python
op.drop_column('table_name', 'column_name')
```

### Rename Column
```python
op.alter_column('table_name', 'old_name', new_column_name='new_name')
```

### Change Column Type
```python
op.alter_column('table_name', 'column_name',
    existing_type=sa.String(50),
    type_=sa.String(100))
```

### Add Foreign Key
```python
op.create_foreign_key(
    'fk_orders_user_id', 'orders', 'users',
    ['user_id'], ['id'], ondelete='CASCADE'
)
```

### Add Index
```python
op.create_index('ix_users_email', 'users', ['email'], unique=True)
```

### Create Enum Type (PostgreSQL)
```python
from sqlalchemy.dialects import postgresql

status_enum = postgresql.ENUM('pending', 'active', 'completed', name='status_type')
status_enum.create(op.get_bind())

op.add_column('orders', sa.Column('status', status_enum))
```

---

## Existing Migrations

| Revision | Description | Date |
|----------|-------------|------|
| `p0_5_add_account_lockout` | Add account lockout fields | 2025-12-01 |
| `create_refresh_tokens_table` | JWT refresh tokens | 2025-12-01 |
| `6efc3153bd83` | Add Brand, ProductImage, StockMovement | 2025-10-XX |
| `3cab280570b6` | Add brand_id to products | 2025-10-XX |

---

## Troubleshooting

### Migration Conflicts
If you get "Revision has multiple heads":
```bash
flask db merge heads -m "Merge branch migrations"
```

### Reset Migrations (Development Only!)
```bash
# CAUTION: This deletes all data!
flask db downgrade base
flask db upgrade
```

### Database Out of Sync
```bash
# Stamp database with current revision (no migration)
flask db stamp head
```

---

## Production Deployment

1. **Never auto-generate in production**
2. **Review migrations before applying**
3. **Backup database before migrating**
4. **Test rollback procedure**

```bash
# Production deployment script
#!/bin/bash
set -e

# Backup database
pg_dump -U user dbname > backup_$(date +%Y%m%d).sql

# Apply migrations
flask db upgrade

# Verify
flask db current
```

---

## Environment Setup

Ensure Flask app is configured:

```python
from flask_migrate import Migrate
from src.database import db

migrate = Migrate(app, db)
```

Set environment variables:
```bash
export FLASK_APP=src.main:app
export FLASK_ENV=development
```

---

## Related Files

- `migrations/env.py` - Alembic environment configuration
- `migrations/script.py.mako` - Migration template
- `migrations/versions/` - Migration scripts
- `backend/src/models/` - SQLAlchemy models

