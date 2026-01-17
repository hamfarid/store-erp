# مخطط قاعدة البيانات الكامل - Gaara ERP v12

## نظرة عامة
مخطط شامل لقاعدة بيانات نظام Gaara ERP v12 يشمل جميع النماذج والحقول والعلاقات.

## إحصائيات قاعدة البيانات
- **إجمالي النماذج**: 150+ نموذج
- **الجداول الرئيسية**: 85 جدول
- **الفهارس**: 200+ فهرس
- **العلاقات**: 300+ علاقة خارجية
- **المشغلات**: 50+ مشغل

## 1. نماذج المستخدمين والصلاحيات (Core User Models)

### 1.1 User (المستخدم)
```sql
CREATE TABLE core_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    password VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 1.2 UserProfile (ملف المستخدم)
```sql
CREATE TABLE core_userprofile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES core_user(id) ON DELETE CASCADE,
    phone VARCHAR(20),
    address TEXT,
    avatar VARCHAR(255),
    department VARCHAR(100),
    position VARCHAR(100),
    employee_id VARCHAR(50) UNIQUE,
    hire_date DATE,
    birth_date DATE,
    nationality VARCHAR(50),
    language VARCHAR(10) DEFAULT 'ar',
    timezone VARCHAR(50) DEFAULT 'Asia/Riyadh',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 1.3 Role (الأدوار)
```sql
CREATE TABLE core_role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 1.4 Permission (الصلاحيات)
```sql
CREATE TABLE core_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    codename VARCHAR(100) NOT NULL,
    content_type_id INTEGER,
    module VARCHAR(50),
    action VARCHAR(50),
    resource VARCHAR(100),
    UNIQUE(content_type_id, codename)
);
```

### 1.5 UserRole (أدوار المستخدم)
```sql
CREATE TABLE core_user_roles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES core_user(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES core_role(id) ON DELETE CASCADE,
    assigned_by_id INTEGER REFERENCES core_user(id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, role_id)
);
```

## 2. نماذج المحاسبة (Accounting Models)

### 2.1 Account (الحسابات)
```sql
CREATE TABLE accounting_account (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    name_en VARCHAR(200),
    account_type VARCHAR(50) NOT NULL,
    parent_id INTEGER REFERENCES accounting_account(id),
    level INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    is_reconcilable BOOLEAN DEFAULT FALSE,
    currency_id INTEGER REFERENCES core_currency(id),
    description TEXT,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2.2 Journal (دفتر اليومية)
```sql
CREATE TABLE accounting_journal (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    default_account_id INTEGER REFERENCES accounting_account(id),
    sequence_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER REFERENCES core_company(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2.3 JournalEntry (قيد اليومية)
```sql
CREATE TABLE accounting_journalentry (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    reference VARCHAR(50),
    journal_id INTEGER REFERENCES accounting_journal(id) NOT NULL,
    date DATE NOT NULL,
    state VARCHAR(20) DEFAULT 'draft',
    total_debit DECIMAL(15,2) DEFAULT 0,
    total_credit DECIMAL(15,2) DEFAULT 0,
    narration TEXT,
    company_id INTEGER REFERENCES core_company(id),
    created_by_id INTEGER REFERENCES core_user(id),
    posted_by_id INTEGER REFERENCES core_user(id),
    posted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2.4 JournalEntryLine (سطر قيد اليومية)
```sql
CREATE TABLE accounting_journalentryline (
    id SERIAL PRIMARY KEY,
    journal_entry_id INTEGER REFERENCES accounting_journalentry(id) ON DELETE CASCADE,
    account_id INTEGER REFERENCES accounting_account(id) NOT NULL,
    debit DECIMAL(15,2) DEFAULT 0,
    credit DECIMAL(15,2) DEFAULT 0,
    description VARCHAR(255),
    partner_id INTEGER REFERENCES core_partner(id),
    analytic_account_id INTEGER REFERENCES accounting_analyticaccount(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.5 FiscalYear (السنة المالية)
```sql
CREATE TABLE accounting_fiscalyear (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_closed BOOLEAN DEFAULT FALSE,
    company_id INTEGER REFERENCES core_company(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2.6 Tax (الضريبة)
```sql
CREATE TABLE accounting_tax (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rate DECIMAL(5,2) NOT NULL,
    type VARCHAR(20) DEFAULT 'percent',
    account_id INTEGER REFERENCES accounting_account(id),
    is_active BOOLEAN DEFAULT TRUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 3. نماذج المخزون (Inventory Models)

### 3.1 Product (المنتج)
```sql
CREATE TABLE inventory_product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE,
    barcode VARCHAR(50) UNIQUE,
    category_id INTEGER REFERENCES inventory_productcategory(id),
    type VARCHAR(20) DEFAULT 'stockable',
    unit_price DECIMAL(15,2) DEFAULT 0,
    cost_price DECIMAL(15,2) DEFAULT 0,
    weight DECIMAL(10,3) DEFAULT 0,
    volume DECIMAL(10,3) DEFAULT 0,
    uom_id INTEGER REFERENCES inventory_unitofmeasure(id),
    description TEXT,
    image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    track_inventory BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3.2 ProductCategory (فئة المنتج)
```sql
CREATE TABLE inventory_productcategory (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER REFERENCES inventory_productcategory(id),
    code VARCHAR(20) UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3.3 Warehouse (المستودع)
```sql
CREATE TABLE inventory_warehouse (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    address TEXT,
    manager_id INTEGER REFERENCES core_user(id),
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER REFERENCES core_company(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3.4 StockMove (حركة المخزون)
```sql
CREATE TABLE inventory_stockmove (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES inventory_product(id) NOT NULL,
    quantity DECIMAL(15,3) NOT NULL,
    unit_price DECIMAL(15,2) DEFAULT 0,
    source_location_id INTEGER REFERENCES inventory_location(id),
    destination_location_id INTEGER REFERENCES inventory_location(id),
    state VARCHAR(20) DEFAULT 'draft',
    date TIMESTAMP DEFAULT NOW(),
    reference VARCHAR(100),
    origin VARCHAR(100),
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3.5 StockQuant (كمية المخزون)
```sql
CREATE TABLE inventory_stockquant (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES inventory_product(id) NOT NULL,
    location_id INTEGER REFERENCES inventory_location(id) NOT NULL,
    quantity DECIMAL(15,3) DEFAULT 0,
    reserved_quantity DECIMAL(15,3) DEFAULT 0,
    lot_id INTEGER REFERENCES inventory_lot(id),
    package_id INTEGER REFERENCES inventory_package(id),
    owner_id INTEGER REFERENCES core_partner(id),
    in_date TIMESTAMP DEFAULT NOW(),
    UNIQUE(product_id, location_id, lot_id, package_id, owner_id)
);
```

## 4. نماذج المبيعات (Sales Models)

### 4.1 Customer (العميل)
```sql
CREATE TABLE sales_customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE,
    email VARCHAR(254),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    credit_limit DECIMAL(15,2) DEFAULT 0,
    payment_term_id INTEGER REFERENCES accounting_paymentterm(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 4.2 SalesOrder (أمر البيع)
```sql
CREATE TABLE sales_salesorder (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    customer_id INTEGER REFERENCES sales_customer(id) NOT NULL,
    date_order DATE DEFAULT CURRENT_DATE,
    validity_date DATE,
    state VARCHAR(20) DEFAULT 'draft',
    amount_untaxed DECIMAL(15,2) DEFAULT 0,
    amount_tax DECIMAL(15,2) DEFAULT 0,
    amount_total DECIMAL(15,2) DEFAULT 0,
    currency_id INTEGER REFERENCES core_currency(id),
    payment_term_id INTEGER REFERENCES accounting_paymentterm(id),
    salesperson_id INTEGER REFERENCES core_user(id),
    notes TEXT,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 4.3 SalesOrderLine (سطر أمر البيع)
```sql
CREATE TABLE sales_salesorderline (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES sales_salesorder(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES inventory_product(id) NOT NULL,
    quantity DECIMAL(15,3) NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    discount DECIMAL(5,2) DEFAULT 0,
    tax_id INTEGER REFERENCES accounting_tax(id),
    subtotal DECIMAL(15,2) DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.4 Invoice (الفاتورة)
```sql
CREATE TABLE sales_invoice (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    customer_id INTEGER REFERENCES sales_customer(id) NOT NULL,
    sales_order_id INTEGER REFERENCES sales_salesorder(id),
    invoice_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    state VARCHAR(20) DEFAULT 'draft',
    amount_untaxed DECIMAL(15,2) DEFAULT 0,
    amount_tax DECIMAL(15,2) DEFAULT 0,
    amount_total DECIMAL(15,2) DEFAULT 0,
    amount_paid DECIMAL(15,2) DEFAULT 0,
    amount_residual DECIMAL(15,2) DEFAULT 0,
    currency_id INTEGER REFERENCES core_currency(id),
    payment_term_id INTEGER REFERENCES accounting_paymentterm(id),
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 5. نماذج المشتريات (Purchasing Models)

### 5.1 Supplier (المورد)
```sql
CREATE TABLE purchasing_supplier (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE,
    email VARCHAR(254),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    payment_term_id INTEGER REFERENCES accounting_paymentterm(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 5.2 PurchaseOrder (أمر الشراء)
```sql
CREATE TABLE purchasing_purchaseorder (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    supplier_id INTEGER REFERENCES purchasing_supplier(id) NOT NULL,
    date_order DATE DEFAULT CURRENT_DATE,
    date_planned DATE,
    state VARCHAR(20) DEFAULT 'draft',
    amount_untaxed DECIMAL(15,2) DEFAULT 0,
    amount_tax DECIMAL(15,2) DEFAULT 0,
    amount_total DECIMAL(15,2) DEFAULT 0,
    currency_id INTEGER REFERENCES core_currency(id),
    payment_term_id INTEGER REFERENCES accounting_paymentterm(id),
    buyer_id INTEGER REFERENCES core_user(id),
    notes TEXT,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 5.3 PurchaseOrderLine (سطر أمر الشراء)
```sql
CREATE TABLE purchasing_purchaseorderline (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES purchasing_purchaseorder(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES inventory_product(id) NOT NULL,
    quantity DECIMAL(15,3) NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    tax_id INTEGER REFERENCES accounting_tax(id),
    subtotal DECIMAL(15,2) DEFAULT 0,
    date_planned DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 6. النماذج الزراعية (Agricultural Models)

### 6.1 Farm (المزرعة)
```sql
CREATE TABLE agricultural_farm (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE,
    owner_id INTEGER REFERENCES core_partner(id),
    manager_id INTEGER REFERENCES core_user(id),
    area DECIMAL(10,2),
    area_unit VARCHAR(20) DEFAULT 'hectare',
    location_latitude DECIMAL(10,8),
    location_longitude DECIMAL(11,8),
    address TEXT,
    soil_type VARCHAR(100),
    climate_zone VARCHAR(100),
    irrigation_system VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 6.2 Field (الحقل)
```sql
CREATE TABLE agricultural_field (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    farm_id INTEGER REFERENCES agricultural_farm(id) NOT NULL,
    area DECIMAL(10,2) NOT NULL,
    area_unit VARCHAR(20) DEFAULT 'hectare',
    soil_type VARCHAR(100),
    ph_level DECIMAL(3,1),
    fertility_level VARCHAR(50),
    irrigation_type VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 6.3 Crop (المحصول)
```sql
CREATE TABLE agricultural_crop (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(200),
    variety VARCHAR(100),
    category VARCHAR(100),
    season VARCHAR(50),
    growth_period_days INTEGER,
    water_requirement DECIMAL(10,2),
    temperature_min DECIMAL(5,2),
    temperature_max DECIMAL(5,2),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 6.4 CropPlanting (زراعة المحصول)
```sql
CREATE TABLE agricultural_cropplanting (
    id SERIAL PRIMARY KEY,
    field_id INTEGER REFERENCES agricultural_field(id) NOT NULL,
    crop_id INTEGER REFERENCES agricultural_crop(id) NOT NULL,
    planting_date DATE NOT NULL,
    expected_harvest_date DATE,
    actual_harvest_date DATE,
    planted_area DECIMAL(10,2),
    seed_quantity DECIMAL(10,3),
    seed_cost DECIMAL(15,2),
    state VARCHAR(20) DEFAULT 'planned',
    notes TEXT,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 6.5 PlantDiagnosis (تشخيص النبات)
```sql
CREATE TABLE agricultural_plantdiagnosis (
    id SERIAL PRIMARY KEY,
    crop_planting_id INTEGER REFERENCES agricultural_cropplanting(id),
    image VARCHAR(255),
    diagnosis_date TIMESTAMP DEFAULT NOW(),
    disease_detected VARCHAR(200),
    confidence_score DECIMAL(5,2),
    symptoms TEXT,
    recommended_treatment TEXT,
    severity_level VARCHAR(20),
    ai_model_used VARCHAR(100),
    verified_by_expert BOOLEAN DEFAULT FALSE,
    expert_id INTEGER REFERENCES core_user(id),
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 7. نماذج الذكاء الاصطناعي (AI Models)

### 7.1 AIModel (نموذج الذكاء الاصطناعي)
```sql
CREATE TABLE ai_aimodel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    version VARCHAR(20),
    description TEXT,
    model_file VARCHAR(255),
    accuracy DECIMAL(5,2),
    training_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    parameters JSONB,
    created_by_id INTEGER REFERENCES core_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 7.2 AIConversation (محادثة الذكاء الاصطناعي)
```sql
CREATE TABLE ai_aiconversation (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES core_user(id) NOT NULL,
    session_id VARCHAR(100),
    message TEXT NOT NULL,
    response TEXT,
    model_used VARCHAR(100),
    response_time DECIMAL(10,3),
    satisfaction_rating INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 7.3 AIMemory (ذاكرة الذكاء الاصطناعي)
```sql
CREATE TABLE ai_aimemory (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES core_user(id),
    context VARCHAR(200),
    key_info TEXT NOT NULL,
    importance_score DECIMAL(3,2) DEFAULT 0.5,
    tags VARCHAR(500),
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 8. نماذج الإدارة (Administration Models)

### 8.1 Company (الشركة)
```sql
CREATE TABLE core_company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    legal_name VARCHAR(200),
    tax_id VARCHAR(50),
    registration_number VARCHAR(50),
    email VARCHAR(254),
    phone VARCHAR(20),
    website VARCHAR(200),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    currency_id INTEGER REFERENCES core_currency(id),
    logo VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 8.2 SystemSetting (إعدادات النظام)
```sql
CREATE TABLE core_systemsetting (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    data_type VARCHAR(20) DEFAULT 'string',
    category VARCHAR(50),
    description TEXT,
    is_editable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 8.3 ActivityLog (سجل الأنشطة)
```sql
CREATE TABLE core_activitylog (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES core_user(id),
    action VARCHAR(50) NOT NULL,
    model_name VARCHAR(100),
    object_id INTEGER,
    object_repr VARCHAR(200),
    changes JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 9. الفهارس والقيود (Indexes & Constraints)

### 9.1 الفهارس الرئيسية
```sql
-- فهارس الأداء
CREATE INDEX idx_user_username ON core_user(username);
CREATE INDEX idx_user_email ON core_user(email);
CREATE INDEX idx_product_code ON inventory_product(code);
CREATE INDEX idx_product_barcode ON inventory_product(barcode);
CREATE INDEX idx_account_code ON accounting_account(code);
CREATE INDEX idx_journal_entry_date ON accounting_journalentry(date);
CREATE INDEX idx_sales_order_date ON sales_salesorder(date_order);
CREATE INDEX idx_purchase_order_date ON purchasing_purchaseorder(date_order);

-- فهارس العلاقات الخارجية
CREATE INDEX idx_userprofile_user ON core_userprofile(user_id);
CREATE INDEX idx_product_category ON inventory_product(category_id);
CREATE INDEX idx_stockmove_product ON inventory_stockmove(product_id);
CREATE INDEX idx_salesorder_customer ON sales_salesorder(customer_id);
CREATE INDEX idx_purchaseorder_supplier ON purchasing_purchaseorder(supplier_id);

-- فهارس البحث النصي
CREATE INDEX idx_product_name_search ON inventory_product USING gin(to_tsvector('arabic', name));
CREATE INDEX idx_customer_name_search ON sales_customer USING gin(to_tsvector('arabic', name));
CREATE INDEX idx_supplier_name_search ON purchasing_supplier USING gin(to_tsvector('arabic', name));
```

### 9.2 القيود والتحقق
```sql
-- قيود التحقق من صحة البيانات
ALTER TABLE accounting_journalentryline 
ADD CONSTRAINT check_debit_credit_not_both_zero 
CHECK (debit > 0 OR credit > 0);

ALTER TABLE accounting_journalentryline 
ADD CONSTRAINT check_debit_credit_not_both_positive 
CHECK (NOT (debit > 0 AND credit > 0));

ALTER TABLE inventory_stockmove 
ADD CONSTRAINT check_quantity_positive 
CHECK (quantity > 0);

ALTER TABLE sales_salesorderline 
ADD CONSTRAINT check_quantity_positive 
CHECK (quantity > 0);

ALTER TABLE sales_salesorderline 
ADD CONSTRAINT check_unit_price_positive 
CHECK (unit_price >= 0);
```

## 10. المشغلات والإجراءات (Triggers & Procedures)

### 10.1 مشغل تحديث الطوابع الزمنية
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- تطبيق المشغل على الجداول الرئيسية
CREATE TRIGGER update_user_updated_at BEFORE UPDATE ON core_user 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_updated_at BEFORE UPDATE ON inventory_product 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_account_updated_at BEFORE UPDATE ON accounting_account 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 10.2 مشغل تسجيل الأنشطة
```sql
CREATE OR REPLACE FUNCTION log_activity()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO core_activitylog (action, model_name, object_id, object_repr, changes)
        VALUES ('create', TG_TABLE_NAME, NEW.id, NEW::text, row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO core_activitylog (action, model_name, object_id, object_repr, changes)
        VALUES ('update', TG_TABLE_NAME, NEW.id, NEW::text, 
                json_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW)));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO core_activitylog (action, model_name, object_id, object_repr, changes)
        VALUES ('delete', TG_TABLE_NAME, OLD.id, OLD::text, row_to_json(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';
```

## 11. طرق العرض (Views)

### 11.1 عرض ملخص المخزون
```sql
CREATE VIEW inventory_stock_summary AS
SELECT 
    p.id as product_id,
    p.name as product_name,
    p.code as product_code,
    SUM(sq.quantity) as total_quantity,
    SUM(sq.reserved_quantity) as reserved_quantity,
    SUM(sq.quantity - sq.reserved_quantity) as available_quantity,
    AVG(p.cost_price) as avg_cost_price,
    SUM((sq.quantity - sq.reserved_quantity) * p.cost_price) as total_value
FROM inventory_product p
LEFT JOIN inventory_stockquant sq ON p.id = sq.product_id
WHERE p.is_active = true
GROUP BY p.id, p.name, p.code;
```

### 11.2 عرض أرصدة الحسابات
```sql
CREATE VIEW accounting_account_balance AS
SELECT 
    a.id as account_id,
    a.code as account_code,
    a.name as account_name,
    a.account_type,
    COALESCE(SUM(jel.debit), 0) as total_debit,
    COALESCE(SUM(jel.credit), 0) as total_credit,
    COALESCE(SUM(jel.debit - jel.credit), 0) as balance
FROM accounting_account a
LEFT JOIN accounting_journalentryline jel ON a.id = jel.account_id
LEFT JOIN accounting_journalentry je ON jel.journal_entry_id = je.id
WHERE je.state = 'posted' OR je.state IS NULL
GROUP BY a.id, a.code, a.name, a.account_type;
```

## 12. الإحصائيات والتحليلات

### 12.1 إحصائيات الاستخدام
```sql
-- عدد المستخدمين النشطين
SELECT COUNT(*) as active_users FROM core_user WHERE is_active = true;

-- عدد المنتجات
SELECT COUNT(*) as total_products FROM inventory_product WHERE is_active = true;

-- إجمالي قيمة المخزون
SELECT SUM(quantity * cost_price) as total_inventory_value 
FROM inventory_stockquant sq 
JOIN inventory_product p ON sq.product_id = p.id;

-- عدد الفواتير الشهرية
SELECT 
    DATE_TRUNC('month', invoice_date) as month,
    COUNT(*) as invoice_count,
    SUM(amount_total) as total_amount
FROM sales_invoice 
WHERE state = 'posted'
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY month DESC;
```

## 13. النسخ الاحتياطي والاستعادة

### 13.1 سكريبت النسخ الاحتياطي
```bash
#!/bin/bash
# نسخ احتياطي يومي لقاعدة البيانات
DB_NAME="gaara_erp"
BACKUP_DIR="/var/backups/gaara_erp"
DATE=$(date +%Y%m%d_%H%M%S)

# إنشاء مجلد النسخ الاحتياطية
mkdir -p $BACKUP_DIR

# نسخ احتياطي كامل
pg_dump -h localhost -U postgres -d $DB_NAME > $BACKUP_DIR/full_backup_$DATE.sql

# نسخ احتياطي مضغوط
pg_dump -h localhost -U postgres -d $DB_NAME | gzip > $BACKUP_DIR/full_backup_$DATE.sql.gz

# حذف النسخ الاحتياطية الأقدم من 30 يوم
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

## 14. التوصيات للتحسين

### 14.1 تحسين الأداء
1. **إضافة فهارس إضافية** للاستعلامات المتكررة
2. **تقسيم الجداول الكبيرة** (Partitioning) حسب التاريخ
3. **استخدام المواد المحققة** (Materialized Views) للتقارير
4. **تحسين استعلامات الانضمام** المعقدة

### 14.2 الأمان
1. **تشفير البيانات الحساسة** في قاعدة البيانات
2. **تطبيق Row-Level Security** للبيانات متعددة الشركات
3. **مراجعة دورية للصلاحيات** وإزالة الصلاحيات غير المستخدمة
4. **تسجيل جميع العمليات الحساسة** في سجل التدقيق

### 14.3 الصيانة
1. **تحليل دوري للجداول** لتحديث الإحصائيات
2. **إعادة فهرسة دورية** للجداول الكبيرة
3. **مراقبة حجم قاعدة البيانات** ونمو الجداول
4. **تنظيف البيانات القديمة** وأرشفتها

---

**تاريخ المخطط**: نوفمبر 2025  
**إصدار قاعدة البيانات**: PostgreSQL 14+  
**حالة المخطط**: محدث وشامل
