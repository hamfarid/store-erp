# Gaara ERP Database Schema Documentation

**Generated**: 2025-12-01
**Total Models**: ~450+ across all modules
**Database**: PostgreSQL (Production) / SQLite (Development)

---

## Module Overview

| Module Category | # Models | Primary Tables |
|-----------------|----------|----------------|
| Core Modules | 125 | User, Company, Branch, Department, Permission |
| Business Modules | 162 | Account, Product, Invoice, Customer, Order |
| Services Modules | ~80 | Project, Task, Document, HR Employee |
| Admin Modules | ~40 | Backup, SystemSetting, Notification |
| Agricultural Modules | ~50 | Experiment, Variety, Harvest, Seed |
| AI Modules | ~30 | AIAgent, AIRole, Memory, Message |

---

## Core Schema (ERD)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     Company     │───────│     Branch      │───────│   Department    │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ name            │       │ name            │
│ code (UNIQUE)   │       │ code (UNIQUE)   │       │ code (UNIQUE)   │
│ is_active       │       │ company_id (FK) │       │ branch_id (FK)  │
│ created_at      │       │ is_active       │       │ company_id (FK) │
│ updated_at      │       │ created_at      │       │ parent_id (FK)  │
└─────────────────┘       └─────────────────┘       └─────────────────┘
         │                                                   │
         │                                                   │
         ▼                                                   ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│      User       │───────│   UserCompany   │       │   UserDept      │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (UUID PK)    │       │ user_id (FK)    │       │ user_id (FK)    │
│ username        │       │ company_id (FK) │       │ dept_id (FK)    │
│ email (UNIQUE)  │       └─────────────────┘       └─────────────────┘
│ password_hash   │
│ is_active       │
│ is_superuser    │
│ failed_logins   │
│ locked_until    │
└─────────────────┘
         │
         │ ◄──── Security (Account Lockout)
         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   Permission    │◄──────│  RolePermission │───────│      Role       │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ role_id (FK)    │       │ id (PK)         │
│ codename        │       │ permission_id   │       │ name            │
│ name            │       └─────────────────┘       │ description     │
│ content_type_id │                                 └─────────────────┘
└─────────────────┘
```

---

## Security Schema

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   SecurityEvent │       │   LoginAttempt  │       │    AuditLog     │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (UUID PK)    │       │ id (PK)         │       │ id (UUID PK)    │
│ event_type      │       │ user_id (FK)    │       │ user_id (FK)    │
│ severity        │       │ ip_address      │       │ action          │
│ user_id (FK)    │       │ success         │       │ model_name      │
│ ip_address      │       │ user_agent      │       │ object_id       │
│ details (JSON)  │       │ failure_reason  │       │ changes (JSON)  │
│ timestamp       │       │ created_at      │       │ ip_address      │
└─────────────────┘       └─────────────────┘       │ timestamp       │
                                                     └─────────────────┘
                                                            │
                                                     Indexes:
                                                     - user_id + timestamp
                                                     - action + timestamp
                                                     - model_name + timestamp
                                                     - ip_address + timestamp
```

---

## Accounting Schema

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    Account      │◄──────│  JournalEntry   │───────│   JournalLine   │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ code (UNIQUE)   │       │ date            │       │ entry_id (FK)   │
│ name            │       │ reference       │       │ account_id (FK) │
│ account_type    │       │ description     │       │ debit           │
│ parent_id (FK)  │       │ is_posted       │       │ credit          │
│ is_active       │       │ company_id (FK) │       │ description     │
│ balance         │       │ created_by (FK) │       └─────────────────┘
└─────────────────┘       └─────────────────┘
         │
         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    FiscalYear   │       │    Invoice      │───────│  InvoiceLine    │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ number (UNIQUE) │       │ invoice_id (FK) │
│ start_date      │       │ date            │       │ product_id (FK) │
│ end_date        │       │ customer_id (FK)│       │ quantity        │
│ is_closed       │       │ total_amount    │       │ unit_price      │
│ company_id (FK) │       │ status          │       │ total           │
└─────────────────┘       │ due_date        │       └─────────────────┘
                          │ company_id (FK) │
                          └─────────────────┘
```

---

## Inventory Schema

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ ProductCategory │◄──────│     Product     │───────│  StockMovement  │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ code (UNIQUE)   │       │ product_id (FK) │
│ code (UNIQUE)   │       │ name            │       │ warehouse_id(FK)│
│ parent_id (FK)  │       │ category_id (FK)│       │ quantity        │
└─────────────────┘       │ uom_id (FK)     │       │ movement_type   │
                          │ price           │       │ reference       │
                          │ cost            │       │ date            │
                          │ track_inventory │       └─────────────────┘
                          └─────────────────┘
                                  │
                                  ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  UnitOfMeasure  │       │    Warehouse    │───────│   StockLevel    │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ name            │       │ product_id (FK) │
│ symbol          │       │ code (UNIQUE)   │       │ warehouse_id(FK)│
│ category        │       │ branch_id (FK)  │       │ quantity        │
└─────────────────┘       │ is_active       │       │ reserved_qty    │
                          └─────────────────┘       │ available_qty   │
                                                     └─────────────────┘
```

---

## Key Relationships Summary

### One-to-Many
- Company → Branches
- Branch → Departments
- User → AuditLogs
- Product → StockMovements
- Invoice → InvoiceLines
- JournalEntry → JournalLines

### Many-to-Many
- User ↔ Companies (UserCompany)
- User ↔ Permissions (UserPermission)
- Role ↔ Permissions (RolePermission)
- User ↔ Roles (UserRole)

### Self-Referential
- Department → parent_department
- Account → parent_account
- ProductCategory → parent_category

---

## Index Strategy

### Primary Indexes (Auto-created)
- All primary keys (id fields)
- All unique constraints (code, email, etc.)

### Performance Indexes
- **User**: username, email, is_active
- **Company**: code, is_active
- **AuditLog**: user_id+timestamp, action+timestamp
- **StockMovement**: product_id+date, warehouse_id
- **Invoice**: number, customer_id, date, status
- **JournalEntry**: date, is_posted, company_id

### Composite Indexes
- (company_id, is_active) - Common filter combination
- (user_id, created_at) - Activity tracking
- (product_id, warehouse_id) - Stock queries

---

## Database Statistics

| Metric | Value |
|--------|-------|
| Total Tables | ~450+ |
| Core Tables | ~50 |
| Business Tables | ~150 |
| Indexes | 309+ |
| Foreign Keys | ~300+ |

---

## Migration Notes

- Django migrations in each app's `migrations/` folder
- Run `python manage.py migrate` for all migrations
- Use `python manage.py showmigrations` to check status

---

**Last Updated**: 2025-12-01

