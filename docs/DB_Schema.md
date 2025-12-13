# Database Schema Documentation

**Last Updated:** 2025-11-04  
**Owner:** Backend/Database Team  
**Status:** ✅ Current

---

## Overview

Complete database schema with 39 models, relationships, indexes, and constraints.

## Core Models

### User Model
```
Table: user
├── id (PK, Integer)
├── username (String, Unique, Not Null)
├── email (String, Unique, Not Null)
├── password_hash (String, Not Null)
├── first_name (String)
├── last_name (String)
├── is_active (Boolean, Default: True)
├── created_at (DateTime, Default: now)
├── updated_at (DateTime, Default: now)
├── last_login (DateTime)
└── Indexes: username, email
```

### Role Model
```
Table: role
├── id (PK, Integer)
├── name (String, Unique, Not Null)
├── description (String)
├── permissions (JSON)
├── created_at (DateTime)
└── Indexes: name
```

### Product Model
```
Table: product
├── id (PK, Integer)
├── name (String, Not Null)
├── description (Text)
├── sku (String, Unique, Not Null)
├── category_id (FK → category)
├── price (Decimal, Not Null)
├── cost (Decimal)
├── is_active (Boolean, Default: True)
├── created_at (DateTime)
├── updated_at (DateTime)
└── Indexes: sku, category_id, name
```

### Category Model
```
Table: category
├── id (PK, Integer)
├── name (String, Unique, Not Null)
├── description (Text)
├── parent_id (FK → category, Self-referential)
├── is_active (Boolean, Default: True)
├── created_at (DateTime)
└── Indexes: name, parent_id
```

### Warehouse Model
```
Table: warehouse
├── id (PK, Integer)
├── name (String, Unique, Not Null)
├── location (String)
├── capacity (Integer)
├── is_active (Boolean, Default: True)
├── created_at (DateTime)
└── Indexes: name
```

### Inventory Model
```
Table: inventory
├── id (PK, Integer)
├── product_id (FK → product)
├── warehouse_id (FK → warehouse)
├── quantity (Integer, Check: >= 0)
├── reorder_level (Integer)
├── last_counted (DateTime)
├── created_at (DateTime)
├── updated_at (DateTime)
└── Indexes: product_id, warehouse_id, (product_id, warehouse_id)
```

### Order Model
```
Table: order
├── id (PK, Integer)
├── order_number (String, Unique, Not Null)
├── user_id (FK → user)
├── status (Enum: pending, confirmed, shipped, delivered, cancelled)
├── total_amount (Decimal)
├── created_at (DateTime)
├── updated_at (DateTime)
└── Indexes: order_number, user_id, status
```

### OrderItem Model
```
Table: order_item
├── id (PK, Integer)
├── order_id (FK → order)
├── product_id (FK → product)
├── quantity (Integer, Check: > 0)
├── unit_price (Decimal)
├── subtotal (Decimal)
└── Indexes: order_id, product_id
```

### Invoice Model
```
Table: invoice
├── id (PK, Integer)
├── invoice_number (String, Unique, Not Null)
├── order_id (FK → order)
├── user_id (FK → user)
├── status (Enum: draft, issued, paid, overdue, cancelled)
├── total_amount (Decimal)
├── tax_amount (Decimal)
├── due_date (DateTime)
├── issued_date (DateTime)
├── paid_date (DateTime)
├── created_at (DateTime)
├── updated_at (DateTime)
└── Indexes: invoice_number, order_id, user_id, status
```

### InvoiceItem Model
```
Table: invoice_item
├── id (PK, Integer)
├── invoice_id (FK → invoice)
├── product_id (FK → product)
├── quantity (Integer)
├── unit_price (Decimal)
├── subtotal (Decimal)
└── Indexes: invoice_id, product_id
```

### Payment Model
```
Table: payment
├── id (PK, Integer)
├── invoice_id (FK → invoice)
├── amount (Decimal, Check: > 0)
├── payment_method (Enum: cash, card, bank_transfer, check)
├── reference (String)
├── paid_date (DateTime)
├── created_at (DateTime)
└── Indexes: invoice_id, paid_date
```

## Relationships

### One-to-Many
- User → Orders (1:N)
- User → Invoices (1:N)
- Category → Products (1:N)
- Warehouse → Inventory (1:N)
- Product → Inventory (1:N)
- Order → OrderItems (1:N)
- Invoice → InvoiceItems (1:N)
- Invoice → Payments (1:N)

### Many-to-Many
- User ↔ Role (via user_role junction table)

### Self-Referential
- Category → Category (parent_id)

## Constraints

### Primary Keys
- All tables have `id` as primary key (auto-increment)

### Foreign Keys
- All FK relationships have ON DELETE CASCADE or ON DELETE RESTRICT
- Referential integrity enforced

### Unique Constraints
- user.username, user.email
- product.sku
- category.name
- warehouse.name
- order.order_number
- invoice.invoice_number

### Check Constraints
- inventory.quantity >= 0
- order_item.quantity > 0
- payment.amount > 0

### Not Null Constraints
- Applied to all required fields

## Indexes

### Single-Column Indexes
- user(username), user(email)
- product(sku), product(category_id), product(name)
- category(name), category(parent_id)
- warehouse(name)
- order(order_number), order(user_id), order(status)
- invoice(invoice_number), invoice(order_id), invoice(user_id), invoice(status)
- payment(invoice_id), payment(paid_date)

### Composite Indexes
- inventory(product_id, warehouse_id)
- order_item(order_id, product_id)
- invoice_item(invoice_id, product_id)

### Performance Indexes
- order(created_at DESC) for recent orders
- invoice(due_date) for overdue invoices
- inventory(quantity) for low stock alerts

## Migrations

### Migration Tool
- **Framework:** Flask-Migrate (Alembic)
- **Location:** `backend/migrations/`
- **Naming:** `YYYYMMDD_HHMMSS_description.py`

### Migration Process
1. Create model changes
2. Generate migration: `flask db migrate -m "description"`
3. Review migration file
4. Apply migration: `flask db upgrade`
5. Commit to version control

### Rollback
```bash
flask db downgrade  # Rollback one migration
flask db downgrade <revision>  # Rollback to specific revision
```

## Database Environments

### Development
- **Type:** SQLite
- **File:** `backend/instance/inventory.db`
- **Backup:** Manual or via script
- **Reset:** Delete file and run migrations

### Staging
- **Type:** PostgreSQL
- **Host:** `db.staging.internal`
- **Backup:** Daily automated
- **Restore:** From backup on demand

### Production
- **Type:** PostgreSQL
- **Host:** `db.prod.internal`
- **Backup:** Hourly automated + daily snapshots
- **Restore:** From backup with minimal downtime
- **Replication:** Read replicas for scaling

## Backup & Recovery

### Backup Strategy
- **Frequency:** Hourly (prod), Daily (staging)
- **Retention:** 30 days
- **Location:** Encrypted storage (S3/GCS)
- **Verification:** Weekly restore test

### Recovery Procedure
1. Identify backup point
2. Restore to staging first
3. Verify data integrity
4. Promote to production
5. Monitor for issues

## Performance Optimization

### Query Optimization
- Use indexes for WHERE, JOIN, ORDER BY clauses
- Avoid N+1 queries (use eager loading)
- Paginate large result sets
- Use connection pooling

### Caching
- Cache frequently accessed data (categories, warehouses)
- Invalidate cache on updates
- TTL: 1 hour for static data

### Monitoring
- Query performance monitoring
- Slow query log analysis
- Index usage statistics
- Connection pool monitoring

## Data Integrity

### Validation
- Database constraints (FK, unique, check)
- Application-level validation (Pydantic)
- Business logic validation

### Audit Trail
- created_at, updated_at timestamps
- User tracking (who created/updated)
- Change history (optional)

---

**Next Steps:**
- [ ] Generate ERD diagram (Mermaid)
- [ ] Document stored procedures (if any)
- [ ] Create backup/restore runbook
- [ ] Implement data archival strategy

