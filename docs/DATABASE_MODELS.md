# 🗄️ Database Models Documentation

**Version:** 2.0.0  
**Last Updated:** 2026-01-17  
**Total Models:** 70+

---

## 📋 Table of Contents

1. [Core Models](#core-models)
2. [Inventory Models](#inventory-models)
3. [Sales & Invoicing Models](#sales--invoicing-models)
4. [User & Security Models](#user--security-models)
5. [Financial Models](#financial-models)
6. [Warehouse Models](#warehouse-models)
7. [Relationships Diagram](#relationships-diagram)
8. [Database Configuration](#database-configuration)

---

## 🔵 Core Models

### User
**File:** `backend/src/models/user.py`

```python
class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    full_name = Column(String(120))
    role_id = Column(Integer, ForeignKey('roles.id'))
    is_active = Column(Boolean, default=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

**Relationships:**
- `role` → Role (Many-to-One)
- `invoices` → Invoice (One-to-Many)
- `shifts` → Shift (One-to-Many)
- `audit_logs` → AuditLog (One-to-Many)

---

### Role
**File:** `backend/src/models/role.py`

```python
class Role(db.Model):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(80), nullable=False)
    name_ar = Column(String(80))
    description = Column(String(255))
    description_ar = Column(String(255))
    permissions = Column(JSON)  # Array of permission strings
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)
```

**Relationships:**
- `users` → User (One-to-Many)

---

## 📦 Inventory Models

### Category
**File:** `backend/src/models/inventory.py`

```python
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    image_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
```

**Relationships:**
- `parent` → Category (Self-referential)
- `children` → Category (One-to-Many)
- `products` → Product (One-to-Many)

---

### Product
**File:** `backend/src/models/product_unified.py`

```python
class Product(db.Model):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True)
    barcode = Column(String(50), unique=True)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))
    unit = Column(String(50))
    purchase_price = Column(Numeric(10, 2), default=0)
    selling_price = Column(Numeric(10, 2), default=0)
    min_stock = Column(Integer, default=0)
    max_stock = Column(Integer, default=1000)
    current_stock = Column(Integer, default=0)
    track_lots = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
```

**Relationships:**
- `category` → Category (Many-to-One)
- `lots` → Lot (One-to-Many)
- `invoice_items` → InvoiceItem (One-to-Many)
- `price_history` → PriceHistory (One-to-Many)

---

### Lot (Advanced)
**File:** `backend/src/models/lot_advanced.py`

```python
class Lot(db.Model):
    __tablename__ = 'lots'
    
    id = Column(Integer, primary_key=True)
    lot_number = Column(String(50), unique=True, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    
    # Quantity Fields
    initial_quantity = Column(Integer, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    reserved_quantity = Column(Integer, default=0)
    sold_quantity = Column(Integer, default=0)
    
    # Pricing
    unit_cost = Column(Numeric(10, 2))
    selling_price = Column(Numeric(10, 2))
    
    # Dates
    production_date = Column(Date)
    expiry_date = Column(Date)
    received_date = Column(Date, default=date.today)
    
    # Quality Fields (Agricultural)
    germination_rate = Column(Numeric(5, 2))
    purity_percentage = Column(Numeric(5, 2))
    moisture_percentage = Column(Numeric(5, 2))
    ministry_lot_number = Column(String(50))
    
    # Status
    status = Column(Enum('available', 'reserved', 'sold', 'expired', 'damaged'))
    is_active = Column(Boolean, default=True)
```

**Relationships:**
- `product` → Product (Many-to-One)
- `warehouse` → Warehouse (Many-to-One)
- `supplier` → Supplier (Many-to-One)
- `invoice_items` → InvoiceItem (One-to-Many)

---

## 💰 Sales & Invoicing Models

### Invoice (Unified)
**File:** `backend/src/models/unified_invoice.py`

```python
class UnifiedInvoice(db.Model):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    invoice_type = Column(Enum('sale', 'purchase', 'return', 'quotation'))
    
    # Relations
    customer_id = Column(Integer, ForeignKey('customers.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    shift_id = Column(Integer, ForeignKey('shifts.id'))
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    
    # Amounts
    subtotal = Column(Numeric(12, 2), default=0)
    discount_amount = Column(Numeric(12, 2), default=0)
    discount_percentage = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), default=0)
    paid_amount = Column(Numeric(12, 2), default=0)
    
    # Payment
    payment_method = Column(String(50))
    payment_status = Column(Enum('pending', 'partial', 'paid', 'refunded'))
    
    # Status
    status = Column(Enum('draft', 'pending', 'confirmed', 'completed', 'cancelled'))
    
    # Dates
    invoice_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    
    # Additional
    notes = Column(Text)
    terms = Column(Text)
```

**Relationships:**
- `customer` → Customer (Many-to-One)
- `supplier` → Supplier (Many-to-One)
- `user` → User (Many-to-One)
- `items` → InvoiceItem (One-to-Many)
- `payments` → InvoicePayment (One-to-Many)

---

### InvoiceItem
**File:** `backend/src/models/unified_invoice.py`

```python
class UnifiedInvoiceItem(db.Model):
    __tablename__ = 'invoice_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    lot_id = Column(Integer, ForeignKey('lots.id'))
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), default=0)
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    subtotal = Column(Numeric(12, 2))
    total = Column(Numeric(12, 2))
```

---

## 👥 Customer & Supplier Models

### Customer
**File:** `backend/src/models/customer.py`

```python
class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    phone = Column(String(20))
    email = Column(String(120))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    tax_number = Column(String(50))
    credit_limit = Column(Numeric(12, 2), default=0)
    current_balance = Column(Numeric(12, 2), default=0)
    is_active = Column(Boolean, default=True)
```

**Relationships:**
- `invoices` → Invoice (One-to-Many)
- `payments` → Payment (One-to-Many)

---

### Supplier
**File:** `backend/src/models/supplier.py`

```python
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    phone = Column(String(20))
    email = Column(String(120))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    tax_number = Column(String(50))
    payment_terms = Column(Integer)  # Days
    current_balance = Column(Numeric(12, 2), default=0)
    is_active = Column(Boolean, default=True)
```

**Relationships:**
- `lots` → Lot (One-to-Many)
- `invoices` → Invoice (One-to-Many)

---

## 🏢 Warehouse Models

### Warehouse
**File:** `backend/src/models/warehouse_unified.py`

```python
class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True)
    address = Column(Text)
    city = Column(String(100))
    phone = Column(String(20))
    manager_id = Column(Integer, ForeignKey('users.id'))
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
```

**Relationships:**
- `lots` → Lot (One-to-Many)
- `invoices` → Invoice (One-to-Many)
- `transfers_from` → WarehouseTransfer (One-to-Many)
- `transfers_to` → WarehouseTransfer (One-to-Many)

---

### WarehouseTransfer
**File:** `backend/src/models/warehouse_transfer.py`

```python
class WarehouseTransfer(db.Model):
    __tablename__ = 'warehouse_transfers'
    
    id = Column(Integer, primary_key=True)
    transfer_number = Column(String(50), unique=True)
    from_warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    to_warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum('pending', 'in_transit', 'completed', 'cancelled'))
    transfer_date = Column(DateTime, default=datetime.utcnow)
    completed_date = Column(DateTime)
    notes = Column(Text)
```

---

## 🔐 Security Models

### Shift
**File:** `backend/src/models/shift.py`

```python
class Shift(db.Model):
    __tablename__ = 'shifts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    opening_cash = Column(Numeric(12, 2), default=0)
    closing_cash = Column(Numeric(12, 2))
    total_sales = Column(Numeric(12, 2), default=0)
    total_returns = Column(Numeric(12, 2), default=0)
    status = Column(Enum('open', 'closed'))
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime)
    notes = Column(Text)
```

---

### AuditLog
**File:** `backend/src/models/audit_log.py`

```python
class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## 📊 Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        STORE ERP DATABASE                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────┐     ┌──────────┐     ┌──────────┐
│   Role   │1───*│   User   │1───*│  Shift   │
└──────────┘     └──────────┘     └──────────┘
                       │1
                       │
                       ▼*
                ┌──────────┐
                │ AuditLog │
                └──────────┘

┌──────────┐     ┌──────────┐     ┌──────────┐
│ Category │1───*│ Product  │1───*│   Lot    │
└──────────┘     └──────────┘     └──────────┘
      │                │                │
      ▼                ▼                ▼
  (self-ref)    ┌──────────┐     ┌──────────┐
                │InvoiceItm│*───1│ Warehouse│
                └──────────┘     └──────────┘
                      │*
                      │
                      ▼1
                ┌──────────┐
                │ Invoice  │
                └──────────┘
                    │*          │*
                    ▼1          ▼1
              ┌──────────┐ ┌──────────┐
              │ Customer │ │ Supplier │
              └──────────┘ └──────────┘
```

---

## ⚙️ Database Configuration

### SQLite (Development)
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///instance/inventory.db"
```

### PostgreSQL (Production)
```python
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
# postgresql://user:password@host:5432/database
```

### Connection Pool Settings
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 10,
    "max_overflow": 20
}
```

### Migration Commands
```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback
flask db downgrade
```

---

*Database Models Documentation - Store ERP v2.0.0*
