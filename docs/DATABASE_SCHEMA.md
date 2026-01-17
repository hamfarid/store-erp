# Database Schema Documentation

**Store Management System - Database Schema**  
**Version:** 1.0  
**Last Updated:** 2025-12-01  
**Database:** SQLite (Development) / PostgreSQL (Production)

---

## Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STORE MANAGEMENT SYSTEM ERD                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    roles     │       │    users     │       │refresh_tokens│
├──────────────┤       ├──────────────┤       ├──────────────┤
│ PK id        │◄──────┤ FK role_id   │◄──────┤ FK user_id   │
│    name      │       │ PK id        │       │ PK id        │
│    name_ar   │       │    username  │       │    jti       │
│    permissions│      │    email     │       │    token     │
│    is_system │       │    password  │       │    expires_at│
│    created_at│       │    full_name │       │    revoked   │
└──────────────┘       │    is_active │       │    created_at│
                       │    last_login│       └──────────────┘
                       │    failed_attempts│
                       │    locked_until│
                       │    created_at│
                       └──────────────┘
                              │
                              │ (created_by)
                              ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  categories  │       │   products   │       │   brands     │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ PK id        │◄──────┤ FK category_id│      │ PK id        │
│    name      │       │ FK brand_id  │◄──────┤    name      │
│    name_ar   │       │ PK id        │       │    logo_url  │
│    description│      │    name      │       │    is_active │
│    parent_id │       │    name_en   │       └──────────────┘
│    is_active │       │    sku       │
│    sort_order│       │    barcode   │       ┌──────────────┐
└──────────────┘       │    description│      │product_images│
                       │    unit      │       ├──────────────┤
                       │    cost_price│       │ PK id        │
                       │    sell_price│       │ FK product_id│◄─┐
                       │    min_stock │       │    url       │  │
                       │    max_stock │       │    is_primary│  │
                       │    is_active │       │    sort_order│  │
                       │    created_at│       └──────────────┘  │
                       └──────────────┘                         │
                              │                                 │
                              │                                 │
        ┌─────────────────────┼─────────────────────┐          │
        │                     │                     │          │
        ▼                     ▼                     ▼          │
┌──────────────┐       ┌──────────────┐       ┌──────────────┐│
│  warehouses  │       │  inventory   │       │stock_movements││
├──────────────┤       ├──────────────┤       ├──────────────┤│
│ PK id        │◄──────┤ FK warehouse_id│     │ PK id        ││
│    name      │       │ FK product_id │──────┤ FK product_id│┘
│    code      │       │ PK id        │       │ FK warehouse_id│
│    location  │       │    quantity  │       │    movement_type│
│    manager   │       │    reserved  │       │    quantity  │
│    phone     │       │    updated_at│       │    reference │
│    is_active │       └──────────────┘       │    notes     │
│    created_at│                              │    movement_date│
└──────────────┘                              │    created_by│
                                              │    created_at│
                                              └──────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  customers   │       │   invoices   │       │invoice_items │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ PK id        │◄──────┤ FK customer_id│      │ PK id        │
│    name      │       │ FK supplier_id│◄─────┤ FK invoice_id│
│    code      │       │ FK user_id   │       │ FK product_id│
│    email     │       │ PK id        │       │    quantity  │
│    phone     │       │    invoice_no│       │    unit_price│
│    mobile    │       │    invoice_type│     │    discount  │
│    address   │       │    status    │       │    tax_amount│
│    city      │       │    subtotal  │       │    total     │
│    country   │       │    tax       │       │    notes     │
│    tax_number│       │    discount  │       └──────────────┘
│    credit_limit│     │    total     │
│    balance   │       │    paid      │       ┌──────────────┐
│    is_active │       │    due_date  │       │   payments   │
│    notes     │       │    notes     │       ├──────────────┤
│    created_at│       │    invoice_date│     │ PK id        │
└──────────────┘       │    created_at│       │ FK invoice_id│
                       └──────────────┘       │    amount    │
┌──────────────┐              │               │    method    │
│  suppliers   │              │               │    reference │
├──────────────┤              │               │    payment_date│
│ PK id        │──────────────┘               │    notes     │
│    name      │                              │    created_at│
│    code      │                              └──────────────┘
│    email     │
│    phone     │       ┌──────────────┐       ┌──────────────┐
│    address   │       │activity_logs │       │ notifications│
│    city      │       ├──────────────┤       ├──────────────┤
│    country   │       │ PK id        │       │ PK id        │
│    tax_number│       │ FK user_id   │       │ FK user_id   │
│    payment_terms│    │    action    │       │    title     │
│    balance   │       │    entity    │       │    message   │
│    is_active │       │    entity_id │       │    type      │
│    notes     │       │    old_values│       │    is_read   │
│    created_at│       │    new_values│       │    data      │
└──────────────┘       │    ip_address│       │    created_at│
                       │    user_agent│       └──────────────┘
                       │    created_at│
                       └──────────────┘
```

---

## Table Definitions

### Users & Authentication

#### `roles`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Role name (English) |
| name_ar | VARCHAR(50) | | Role name (Arabic) |
| description | TEXT | | Role description |
| permissions | JSON | | List of permission strings |
| is_system | BOOLEAN | DEFAULT FALSE | System role (cannot delete) |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | | Last update timestamp |

#### `users`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(100) | UNIQUE, NOT NULL | User email |
| password_hash | VARCHAR(255) | NOT NULL | Argon2id hashed password |
| full_name | VARCHAR(100) | | User's full name |
| role_id | INTEGER | FK → roles.id | User's role |
| is_active | BOOLEAN | DEFAULT TRUE | Account active status |
| last_login | DATETIME | | Last login timestamp |
| failed_login_attempts | INTEGER | DEFAULT 0 | Failed login counter |
| locked_until | DATETIME | | Account lockout expiry |
| last_failed_login | DATETIME | | Last failed attempt |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | | Last update timestamp |

#### `refresh_tokens`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| user_id | INTEGER | FK → users.id | Token owner |
| jti | VARCHAR(36) | UNIQUE, NOT NULL | JWT ID |
| token | TEXT | NOT NULL | Encrypted token |
| expires_at | DATETIME | NOT NULL | Token expiry |
| revoked | BOOLEAN | DEFAULT FALSE | Revocation status |
| revoked_at | DATETIME | | Revocation timestamp |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |

---

### Product Management

#### `categories`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| name | VARCHAR(100) | NOT NULL | Category name (Arabic) |
| name_en | VARCHAR(100) | | Category name (English) |
| description | TEXT | | Category description |
| parent_id | INTEGER | FK → categories.id | Parent category |
| image_url | VARCHAR(255) | | Category image |
| sort_order | INTEGER | DEFAULT 0 | Display order |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |

#### `brands`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| name | VARCHAR(100) | NOT NULL | Brand name |
| logo_url | VARCHAR(255) | | Brand logo |
| website | VARCHAR(255) | | Brand website |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |

#### `products`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| name | VARCHAR(200) | NOT NULL | Product name (Arabic) |
| name_en | VARCHAR(200) | | Product name (English) |
| sku | VARCHAR(50) | UNIQUE | Stock keeping unit |
| barcode | VARCHAR(50) | UNIQUE | Product barcode |
| description | TEXT | | Product description |
| category_id | INTEGER | FK → categories.id | Product category |
| brand_id | INTEGER | FK → brands.id | Product brand |
| unit | VARCHAR(20) | DEFAULT 'piece' | Unit of measure |
| cost_price | DECIMAL(12,2) | DEFAULT 0 | Purchase cost |
| sell_price | DECIMAL(12,2) | DEFAULT 0 | Selling price |
| min_stock | INTEGER | DEFAULT 0 | Minimum stock level |
| max_stock | INTEGER | | Maximum stock level |
| weight | DECIMAL(10,3) | | Product weight |
| dimensions | VARCHAR(50) | | Product dimensions |
| tax_rate | DECIMAL(5,2) | DEFAULT 15 | Tax percentage |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| created_by | INTEGER | FK → users.id | Created by user |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | | Last update |

---

### Inventory Management

#### `warehouses`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| name | VARCHAR(100) | NOT NULL | Warehouse name |
| code | VARCHAR(20) | UNIQUE | Warehouse code |
| location | TEXT | | Physical address |
| manager | VARCHAR(100) | | Manager name |
| phone | VARCHAR(20) | | Contact phone |
| email | VARCHAR(100) | | Contact email |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| is_default | BOOLEAN | DEFAULT FALSE | Default warehouse |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |

#### `inventory`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| product_id | INTEGER | FK → products.id, NOT NULL | Product reference |
| warehouse_id | INTEGER | FK → warehouses.id, NOT NULL | Warehouse reference |
| quantity | DECIMAL(12,3) | DEFAULT 0 | Available quantity |
| reserved | DECIMAL(12,3) | DEFAULT 0 | Reserved quantity |
| updated_at | DATETIME | | Last update |

**Unique Constraint:** (product_id, warehouse_id)

#### `stock_movements`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| product_id | INTEGER | FK → products.id, NOT NULL | Product reference |
| warehouse_id | INTEGER | FK → warehouses.id, NOT NULL | Warehouse reference |
| movement_type | ENUM | NOT NULL | in/out/adjustment/transfer |
| quantity | DECIMAL(12,3) | NOT NULL | Movement quantity |
| reference_number | VARCHAR(50) | | Reference document |
| reference_type | VARCHAR(50) | | Type of reference |
| unit_cost | DECIMAL(12,2) | | Unit cost at time |
| notes | TEXT | | Movement notes |
| movement_date | DATETIME | NOT NULL | Movement date |
| created_by | INTEGER | FK → users.id | Created by user |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |

---

### Partners (Customers & Suppliers)

#### `customers`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| name | VARCHAR(100) | NOT NULL | Customer name |
| code | VARCHAR(20) | UNIQUE | Customer code |
| email | VARCHAR(100) | | Contact email |
| phone | VARCHAR(20) | | Contact phone |
| mobile | VARCHAR(20) | | Mobile phone |
| address | TEXT | | Street address |
| city | VARCHAR(50) | | City |
| country | VARCHAR(50) | | Country |
| postal_code | VARCHAR(20) | | Postal code |
| tax_number | VARCHAR(50) | | Tax registration |
| credit_limit | DECIMAL(12,2) | DEFAULT 0 | Credit limit |
| balance | DECIMAL(12,2) | DEFAULT 0 | Current balance |
| payment_terms | INTEGER | DEFAULT 0 | Payment days |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| notes | TEXT | | Customer notes |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | | Last update |

#### `suppliers`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| name | VARCHAR(100) | NOT NULL | Supplier name |
| code | VARCHAR(20) | UNIQUE | Supplier code |
| email | VARCHAR(100) | | Contact email |
| phone | VARCHAR(20) | | Contact phone |
| mobile | VARCHAR(20) | | Mobile phone |
| address | TEXT | | Street address |
| city | VARCHAR(50) | | City |
| country | VARCHAR(50) | | Country |
| tax_number | VARCHAR(50) | | Tax registration |
| payment_terms | INTEGER | DEFAULT 30 | Payment days |
| balance | DECIMAL(12,2) | DEFAULT 0 | Current balance |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| notes | TEXT | | Supplier notes |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | | Last update |

---

### Invoices & Payments

#### `invoices`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| invoice_number | VARCHAR(50) | UNIQUE, NOT NULL | Invoice number |
| invoice_type | ENUM | NOT NULL | sales/purchase/return |
| status | ENUM | DEFAULT 'draft' | draft/confirmed/paid/cancelled |
| customer_id | INTEGER | FK → customers.id | Customer (for sales) |
| supplier_id | INTEGER | FK → suppliers.id | Supplier (for purchases) |
| warehouse_id | INTEGER | FK → warehouses.id | Warehouse |
| user_id | INTEGER | FK → users.id | Created by |
| subtotal | DECIMAL(12,2) | DEFAULT 0 | Subtotal before tax |
| tax_amount | DECIMAL(12,2) | DEFAULT 0 | Total tax |
| discount_amount | DECIMAL(12,2) | DEFAULT 0 | Total discount |
| total | DECIMAL(12,2) | DEFAULT 0 | Grand total |
| paid_amount | DECIMAL(12,2) | DEFAULT 0 | Amount paid |
| due_date | DATE | | Payment due date |
| invoice_date | DATE | NOT NULL | Invoice date |
| notes | TEXT | | Invoice notes |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | | Last update |

#### `invoice_items`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| invoice_id | INTEGER | FK → invoices.id, NOT NULL | Parent invoice |
| product_id | INTEGER | FK → products.id, NOT NULL | Product |
| quantity | DECIMAL(12,3) | NOT NULL | Quantity |
| unit_price | DECIMAL(12,2) | NOT NULL | Unit price |
| discount | DECIMAL(12,2) | DEFAULT 0 | Item discount |
| tax_rate | DECIMAL(5,2) | DEFAULT 15 | Tax percentage |
| tax_amount | DECIMAL(12,2) | DEFAULT 0 | Tax amount |
| total | DECIMAL(12,2) | NOT NULL | Line total |
| notes | TEXT | | Item notes |

#### `payments`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| invoice_id | INTEGER | FK → invoices.id, NOT NULL | Invoice reference |
| amount | DECIMAL(12,2) | NOT NULL | Payment amount |
| payment_method | ENUM | NOT NULL | cash/card/transfer/check |
| reference | VARCHAR(100) | | Payment reference |
| payment_date | DATE | NOT NULL | Payment date |
| notes | TEXT | | Payment notes |
| created_by | INTEGER | FK → users.id | Recorded by |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |

---

### System Tables

#### `activity_logs`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| user_id | INTEGER | FK → users.id | User who performed action |
| action | VARCHAR(50) | NOT NULL | Action type |
| entity_type | VARCHAR(50) | NOT NULL | Entity type |
| entity_id | INTEGER | | Entity ID |
| old_values | JSON | | Previous values |
| new_values | JSON | | New values |
| ip_address | VARCHAR(45) | | Client IP |
| user_agent | VARCHAR(255) | | Client user agent |
| created_at | DATETIME | DEFAULT NOW | Action timestamp |

#### `notifications`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Primary key |
| user_id | INTEGER | FK → users.id, NOT NULL | Recipient |
| title | VARCHAR(200) | NOT NULL | Notification title |
| message | TEXT | NOT NULL | Notification content |
| type | VARCHAR(50) | DEFAULT 'info' | info/warning/error/success |
| is_read | BOOLEAN | DEFAULT FALSE | Read status |
| data | JSON | | Additional data |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |

---

## Indexes

### Performance Indexes

```sql
-- Users
CREATE INDEX ix_users_username ON users(username);
CREATE INDEX ix_users_email ON users(email);
CREATE INDEX ix_users_is_active ON users(is_active);
CREATE INDEX ix_users_role_id ON users(role_id);

-- Products
CREATE INDEX ix_products_barcode ON products(barcode);
CREATE INDEX ix_products_sku ON products(sku);
CREATE INDEX ix_products_name ON products(name);
CREATE INDEX ix_products_category_id ON products(category_id);
CREATE INDEX ix_products_is_active ON products(is_active);

-- Inventory
CREATE INDEX ix_inventory_product_warehouse ON inventory(product_id, warehouse_id);

-- Stock Movements
CREATE INDEX ix_stock_movements_product_id ON stock_movements(product_id);
CREATE INDEX ix_stock_movements_warehouse_id ON stock_movements(warehouse_id);
CREATE INDEX ix_stock_movements_date ON stock_movements(movement_date);
CREATE INDEX ix_stock_movements_product_warehouse ON stock_movements(product_id, warehouse_id);

-- Invoices
CREATE INDEX ix_invoices_invoice_number ON invoices(invoice_number);
CREATE INDEX ix_invoices_customer_id ON invoices(customer_id);
CREATE INDEX ix_invoices_supplier_id ON invoices(supplier_id);
CREATE INDEX ix_invoices_status ON invoices(status);
CREATE INDEX ix_invoices_date ON invoices(invoice_date);
CREATE INDEX ix_invoices_customer_date ON invoices(customer_id, invoice_date);

-- Customers/Suppliers
CREATE INDEX ix_customers_name ON customers(name);
CREATE INDEX ix_suppliers_name ON suppliers(name);

-- Activity Logs
CREATE INDEX ix_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX ix_activity_logs_entity ON activity_logs(entity_type, entity_id);
CREATE INDEX ix_activity_logs_created_at ON activity_logs(created_at);
```

---

## Relationships Summary

| Parent | Child | Relationship | On Delete |
|--------|-------|--------------|-----------|
| roles | users | 1:N | SET NULL |
| users | refresh_tokens | 1:N | CASCADE |
| users | activity_logs | 1:N | SET NULL |
| users | notifications | 1:N | CASCADE |
| categories | categories | 1:N (self) | SET NULL |
| categories | products | 1:N | SET NULL |
| brands | products | 1:N | SET NULL |
| products | inventory | 1:N | CASCADE |
| products | stock_movements | 1:N | RESTRICT |
| products | invoice_items | 1:N | RESTRICT |
| products | product_images | 1:N | CASCADE |
| warehouses | inventory | 1:N | RESTRICT |
| warehouses | stock_movements | 1:N | RESTRICT |
| customers | invoices | 1:N | RESTRICT |
| suppliers | invoices | 1:N | RESTRICT |
| invoices | invoice_items | 1:N | CASCADE |
| invoices | payments | 1:N | CASCADE |

---

## Migration History

| Version | Date | Description |
|---------|------|-------------|
| Initial | 2025-10-01 | Initial schema |
| p0_5 | 2025-12-01 | Add account lockout fields |
| p1_31 | 2025-12-01 | Add performance indexes |

---

**Last Updated:** 2025-12-01  
**Maintained By:** Database Team
