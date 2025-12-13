# 📊 مخطط قاعدة البيانات الموحدة
## Unified Database Schema

**التاريخ:** 2025-10-08  
**الإصدار:** 2.0 (Unified Models)

---

## 🎯 نظرة عامة

تم توحيد جميع نماذج قاعدة البيانات المكررة في نماذج موحدة ومحسّنة مع:
- ✅ علاقات صحيحة ومحددة
- ✅ فهارس (Indexes) لتحسين الأداء
- ✅ قيود (Constraints) للحفاظ على سلامة البيانات
- ✅ دوال مساعدة (Helper Methods)
- ✅ توثيق شامل

---

## 📋 الجداول الرئيسية

### 1. Users (المستخدمون)
**الملف:** `backend/src/models/user_unified.py`

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    phone VARCHAR(20),
    avatar VARCHAR(255),
    department VARCHAR(100),
    position VARCHAR(100),
    role_id INTEGER REFERENCES roles(id),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    permissions TEXT,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until DATETIME,
    password_changed_at DATETIME,
    must_change_password BOOLEAN DEFAULT FALSE,
    last_login DATETIME,
    last_activity DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    settings TEXT
);

-- Indexes
CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_is_active ON users(is_active);
CREATE INDEX idx_user_role_id ON users(role_id);
```

**العلاقات:**
- `role_id` → `roles.id` (Many-to-One)
- `created_invoices` ← `invoices.created_by` (One-to-Many)
- `audit_logs` ← `audit_logs.user_id` (One-to-Many)

---

### 2. Roles (الأدوار)
**الملف:** `backend/src/models/user_unified.py`

```sql
CREATE TABLE roles (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    description TEXT,
    permissions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_role_name ON roles(name);
```

**الأدوار الافتراضية:**
- `admin` - مدير النظام (جميع الصلاحيات)
- `manager` - مدير (صلاحيات إدارية محدودة)
- `user` - مستخدم (صلاحيات أساسية)

---

### 3. Products (المنتجات)
**الملف:** `backend/src/models/product_unified.py`

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    name_en VARCHAR(200),
    sku VARCHAR(100) UNIQUE NOT NULL,
    barcode VARCHAR(100) UNIQUE,
    category_id INTEGER REFERENCES categories(id),
    supplier_id INTEGER REFERENCES suppliers(id),
    brand VARCHAR(100),
    product_type ENUM('storable', 'consumable', 'service', 'digital'),
    tracking_type ENUM('none', 'lot', 'serial', 'expiry'),
    cost_price DECIMAL(10,2) DEFAULT 0.00,
    sale_price DECIMAL(10,2) DEFAULT 0.00,
    wholesale_price DECIMAL(10,2) DEFAULT 0.00,
    min_price DECIMAL(10,2) DEFAULT 0.00,
    current_stock DECIMAL(10,3) DEFAULT 0.000,
    min_quantity DECIMAL(10,3) DEFAULT 0.000,
    max_quantity DECIMAL(10,3) DEFAULT 1000.000,
    reorder_point DECIMAL(10,3) DEFAULT 0.000,
    reorder_quantity DECIMAL(10,3) DEFAULT 0.000,
    unit VARCHAR(20) DEFAULT 'قطعة',
    unit_en VARCHAR(20) DEFAULT 'piece',
    weight DECIMAL(10,3),
    weight_unit VARCHAR(10) DEFAULT 'kg',
    length DECIMAL(10,2),
    width DECIMAL(10,2),
    height DECIMAL(10,2),
    dimension_unit VARCHAR(10) DEFAULT 'cm',
    tax_rate DECIMAL(5,2) DEFAULT 0.00,
    is_taxable BOOLEAN DEFAULT TRUE,
    discount_rate DECIMAL(5,2) DEFAULT 0.00,
    description TEXT,
    description_en TEXT,
    image VARCHAR(255),
    images TEXT,
    manufacturer VARCHAR(100),
    country_of_origin VARCHAR(50),
    warranty_period INTEGER,
    shelf_life INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    meta_title VARCHAR(200),
    meta_description TEXT,
    meta_keywords TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_product_name ON products(name);
CREATE INDEX idx_product_sku ON products(sku);
CREATE INDEX idx_product_barcode ON products(barcode);
CREATE INDEX idx_product_category ON products(category_id);
CREATE INDEX idx_product_supplier ON products(supplier_id);
CREATE INDEX idx_product_is_active ON products(is_active);
```

**العلاقات:**
- `category_id` → `categories.id` (Many-to-One)
- `supplier_id` → `suppliers.id` (Many-to-One)
- `inventory_items` ← `inventory.product_id` (One-to-Many)
- `invoice_items` ← `invoice_items.product_id` (One-to-Many)
- `stock_movements` ← `stock_movements.product_id` (One-to-Many)

---

### 4. Invoices (الفواتير)
**الملف:** `backend/src/models/invoice_unified.py`

```sql
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    invoice_type ENUM('sales', 'purchase', 'sales_return', 'purchase_return'),
    invoice_date DATE NOT NULL,
    due_date DATE,
    delivery_date DATE,
    customer_id INTEGER REFERENCES customers(id),
    supplier_id INTEGER REFERENCES suppliers(id),
    warehouse_id INTEGER REFERENCES warehouses(id),
    created_by INTEGER REFERENCES users(id) NOT NULL,
    subtotal DECIMAL(15,2) DEFAULT 0.00,
    tax_amount DECIMAL(15,2) DEFAULT 0.00,
    discount_amount DECIMAL(15,2) DEFAULT 0.00,
    shipping_cost DECIMAL(15,2) DEFAULT 0.00,
    other_charges DECIMAL(15,2) DEFAULT 0.00,
    total_amount DECIMAL(15,2) DEFAULT 0.00,
    paid_amount DECIMAL(15,2) DEFAULT 0.00,
    remaining_amount DECIMAL(15,2) DEFAULT 0.00,
    discount_type VARCHAR(20) DEFAULT 'fixed',
    discount_value DECIMAL(10,2) DEFAULT 0.00,
    tax_rate DECIMAL(5,2) DEFAULT 0.00,
    is_tax_inclusive BOOLEAN DEFAULT FALSE,
    currency VARCHAR(3) DEFAULT 'USD',
    exchange_rate DECIMAL(10,4) DEFAULT 1.0000,
    status ENUM('draft', 'confirmed', 'paid', 'partial', 'cancelled', 'overdue'),
    payment_status ENUM('unpaid', 'partial', 'paid'),
    payment_method VARCHAR(50),
    payment_terms VARCHAR(100),
    shipping_address TEXT,
    shipping_method VARCHAR(50),
    tracking_number VARCHAR(100),
    notes TEXT,
    internal_notes TEXT,
    terms_conditions TEXT,
    reference_number VARCHAR(50),
    po_number VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    confirmed_at DATETIME,
    paid_at DATETIME,
    cancelled_at DATETIME
);

-- Indexes
CREATE INDEX idx_invoice_number ON invoices(invoice_number);
CREATE INDEX idx_invoice_type ON invoices(invoice_type);
CREATE INDEX idx_invoice_status ON invoices(status);
CREATE INDEX idx_invoice_date ON invoices(invoice_date);
CREATE INDEX idx_invoice_customer ON invoices(customer_id);
CREATE INDEX idx_invoice_supplier ON invoices(supplier_id);
CREATE INDEX idx_invoice_warehouse ON invoices(warehouse_id);
```

**العلاقات:**
- `customer_id` → `customers.id` (Many-to-One)
- `supplier_id` → `suppliers.id` (Many-to-One)
- `warehouse_id` → `warehouses.id` (Many-to-One)
- `created_by` → `users.id` (Many-to-One)
- `items` ← `invoice_items.invoice_id` (One-to-Many)
- `payments` ← `payments.invoice_id` (One-to-Many)

---

### 5. Warehouses (المستودعات)
**الملف:** `backend/src/models/warehouse_unified.py`

```sql
CREATE TABLE warehouses (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(20) UNIQUE,
    location VARCHAR(200),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(120),
    manager_name VARCHAR(100),
    manager_phone VARCHAR(20),
    total_area DECIMAL(10,2),
    storage_capacity DECIMAL(10,2),
    area_unit VARCHAR(10) DEFAULT 'm2',
    description TEXT,
    warehouse_type VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    is_main BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_warehouse_name ON warehouses(name);
CREATE INDEX idx_warehouse_code ON warehouses(code);
CREATE INDEX idx_warehouse_is_active ON warehouses(is_active);
```

**العلاقات:**
- `inventory_records` ← `inventory.warehouse_id` (One-to-Many)
- `invoices` ← `invoices.warehouse_id` (One-to-Many)
- `stock_movements` ← `stock_movements.warehouse_id` (One-to-Many)

---

## 📋 الجداول المساعدة

### 6. Invoice Items (أصناف الفاتورة)
**الملف:** `backend/src/models/supporting_models.py`

```sql
CREATE TABLE invoice_items (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) NOT NULL,
    product_id INTEGER REFERENCES products(id) NOT NULL,
    quantity DECIMAL(10,3) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    line_total DECIMAL(15,2) NOT NULL,
    description TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_invoice_item_invoice ON invoice_items(invoice_id);
CREATE INDEX idx_invoice_item_product ON invoice_items(product_id);
```

---

### 7. Payments (الدفعات)

```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('cash', 'card', 'bank_transfer', 'check', 'mobile_payment', 'other'),
    reference_number VARCHAR(100),
    bank_name VARCHAR(100),
    check_number VARCHAR(50),
    check_date DATE,
    notes TEXT,
    received_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_payment_invoice ON payments(invoice_id);
CREATE INDEX idx_payment_date ON payments(payment_date);
CREATE INDEX idx_payment_method ON payments(payment_method);
```

---

### 8. Stock Movements (حركات المخزون)

```sql
CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) NOT NULL,
    warehouse_id INTEGER REFERENCES warehouses(id) NOT NULL,
    movement_type ENUM('in', 'out', 'transfer', 'adjustment', 'return'),
    quantity DECIMAL(10,3) NOT NULL,
    movement_date DATETIME NOT NULL,
    balance_before DECIMAL(10,3),
    balance_after DECIMAL(10,3),
    reference_type VARCHAR(50),
    reference_id INTEGER,
    notes TEXT,
    cost_price DECIMAL(10,2),
    created_by INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_stock_movement_product ON stock_movements(product_id);
CREATE INDEX idx_stock_movement_warehouse ON stock_movements(warehouse_id);
CREATE INDEX idx_stock_movement_date ON stock_movements(movement_date);
CREATE INDEX idx_stock_movement_type ON stock_movements(movement_type);
```

---

### 9. Audit Logs (سجل التدقيق)

```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action_type ENUM('create', 'update', 'delete', 'login', 'logout', 'view', 'export', 'import'),
    entity_type VARCHAR(50),
    entity_id INTEGER,
    description TEXT,
    old_values TEXT,
    new_values TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_audit_log_user ON audit_logs(user_id);
CREATE INDEX idx_audit_log_action ON audit_logs(action_type);
CREATE INDEX idx_audit_log_date ON audit_logs(created_at);
CREATE INDEX idx_audit_log_entity ON audit_logs(entity_type, entity_id);
```

---

## 🔗 مخطط العلاقات (ERD)

```
┌─────────────┐       ┌──────────────┐
│    Roles    │◄──────┤    Users     │
└─────────────┘       └──────────────┘
                             │
                             │ created_by
                             ▼
┌─────────────┐       ┌──────────────┐       ┌──────────────┐
│ Categories  │◄──────┤   Products   │──────►│  Suppliers   │
└─────────────┘       └──────────────┘       └──────────────┘
                             │
                             │
                    ┌────────┼────────┐
                    │        │        │
                    ▼        ▼        ▼
            ┌──────────┐ ┌──────────┐ ┌──────────┐
            │Inventory │ │Invoice   │ │  Stock   │
            │          │ │  Items   │ │Movements │
            └──────────┘ └──────────┘ └──────────┘
                    │        │
                    │        │
                    ▼        ▼
            ┌──────────────────────┐
            │      Invoices        │
            └──────────────────────┘
                    │
                    │
            ┌───────┼───────┐
            │       │       │
            ▼       ▼       ▼
      ┌──────┐ ┌──────┐ ┌──────┐
      │Cust. │ │Supp. │ │Ware. │
      └──────┘ └──────┘ └──────┘
```

---

## 📝 ملاحظات مهمة

1. **التوافق مع النظام القديم**: تم الحفاظ على حقل `role` في جدول `users` للتوافق
2. **الفهارس**: تم إضافة فهارس على جميع الحقول المستخدمة في البحث والفلترة
3. **القيود**: جميع العلاقات محمية بـ Foreign Keys
4. **الأمان**: كلمات المرور مشفرة باستخدام bcrypt
5. **التدقيق**: جميع العمليات مسجلة في `audit_logs`

---

**آخر تحديث:** 2025-10-08

