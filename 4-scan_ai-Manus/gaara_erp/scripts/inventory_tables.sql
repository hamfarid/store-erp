-- إنشاء جداول وحدة المخزون لنظام Gaara ERP

-- جدول المستودعات
CREATE TABLE IF NOT EXISTS warehouses (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    manager_id INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    branch_id INTEGER REFERENCES branches(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول فئات المنتجات
CREATE TABLE IF NOT EXISTS product_categories (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER REFERENCES product_categories(id),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول وحدات القياس
CREATE TABLE IF NOT EXISTS units_of_measure (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10),
    is_base_unit BOOLEAN DEFAULT FALSE,
    base_unit_id INTEGER REFERENCES units_of_measure(id),
    conversion_factor DECIMAL(15, 5) DEFAULT 1.0,
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول المنتجات
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    barcode VARCHAR(50),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES product_categories(id),
    base_unit_id INTEGER NOT NULL REFERENCES units_of_measure(id),
    purchase_unit_id INTEGER REFERENCES units_of_measure(id),
    sales_unit_id INTEGER REFERENCES units_of_measure(id),
    inventory_unit_id INTEGER REFERENCES units_of_measure(id),
    cost_price DECIMAL(15, 5) DEFAULT 0,
    selling_price DECIMAL(15, 5) DEFAULT 0,
    min_stock_level DECIMAL(15, 5) DEFAULT 0,
    max_stock_level DECIMAL(15, 5) DEFAULT 0,
    reorder_point DECIMAL(15, 5) DEFAULT 0,
    is_stockable BOOLEAN DEFAULT TRUE,
    is_purchasable BOOLEAN DEFAULT TRUE,
    is_sellable BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    tax_group_id INTEGER REFERENCES tax_groups(id),
    inventory_account_id INTEGER REFERENCES accounts(id),
    cogs_account_id INTEGER REFERENCES accounts(id),
    revenue_account_id INTEGER REFERENCES accounts(id),
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول المخزون
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    quantity_on_hand DECIMAL(15, 5) DEFAULT 0,
    quantity_reserved DECIMAL(15, 5) DEFAULT 0,
    quantity_available DECIMAL(15, 5) GENERATED ALWAYS AS (quantity_on_hand - quantity_reserved) STORED,
    last_cost_price DECIMAL(15, 5) DEFAULT 0,
    average_cost DECIMAL(15, 5) DEFAULT 0,
    last_count_date TIMESTAMP WITH TIME ZONE,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id),
    UNIQUE(product_id, warehouse_id, company_id)
);

-- جدول حركات المخزون
CREATE TABLE IF NOT EXISTS inventory_transactions (
    id SERIAL PRIMARY KEY,
    transaction_number VARCHAR(50) NOT NULL UNIQUE,
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL, -- (purchase, sale, transfer, adjustment, return, etc.)
    reference_type VARCHAR(50), -- (purchase_order, sales_order, transfer_order, etc.)
    reference_id INTEGER,
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    source_warehouse_id INTEGER REFERENCES warehouses(id), -- للتحويلات
    notes TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'draft', -- (draft, posted, cancelled)
    journal_entry_id INTEGER REFERENCES journal_entries(id),
    company_id INTEGER NOT NULL REFERENCES companies(id),
    branch_id INTEGER REFERENCES branches(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id),
    posted_at TIMESTAMP WITH TIME ZONE,
    posted_by INTEGER REFERENCES users(id)
);

-- جدول تفاصيل حركات المخزون
CREATE TABLE IF NOT EXISTS inventory_transaction_items (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL REFERENCES inventory_transactions(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity DECIMAL(15, 5) NOT NULL,
    unit_id INTEGER NOT NULL REFERENCES units_of_measure(id),
    unit_cost DECIMAL(15, 5) DEFAULT 0,
    total_cost DECIMAL(15, 5) DEFAULT 0,
    lot_number VARCHAR(50),
    expiry_date DATE,
    notes TEXT,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول الجرد
CREATE TABLE IF NOT EXISTS inventory_counts (
    id SERIAL PRIMARY KEY,
    count_number VARCHAR(50) NOT NULL UNIQUE,
    count_date TIMESTAMP WITH TIME ZONE NOT NULL,
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    status VARCHAR(20) NOT NULL DEFAULT 'draft', -- (draft, in_progress, completed, posted, cancelled)
    notes TEXT,
    adjustment_transaction_id INTEGER REFERENCES inventory_transactions(id),
    company_id INTEGER NOT NULL REFERENCES companies(id),
    branch_id INTEGER REFERENCES branches(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id),
    completed_at TIMESTAMP WITH TIME ZONE,
    completed_by INTEGER REFERENCES users(id),
    posted_at TIMESTAMP WITH TIME ZONE,
    posted_by INTEGER REFERENCES users(id)
);

-- جدول تفاصيل الجرد
CREATE TABLE IF NOT EXISTS inventory_count_items (
    id SERIAL PRIMARY KEY,
    count_id INTEGER NOT NULL REFERENCES inventory_counts(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    expected_quantity DECIMAL(15, 5) DEFAULT 0,
    actual_quantity DECIMAL(15, 5),
    variance DECIMAL(15, 5) GENERATED ALWAYS AS (actual_quantity - expected_quantity) STORED,
    unit_id INTEGER NOT NULL REFERENCES units_of_measure(id),
    unit_cost DECIMAL(15, 5) DEFAULT 0,
    variance_cost DECIMAL(15, 5) GENERATED ALWAYS AS ((actual_quantity - expected_quantity) * unit_cost) STORED,
    notes TEXT,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول أوامر الشراء
CREATE TABLE IF NOT EXISTS purchase_orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    order_date TIMESTAMP WITH TIME ZONE NOT NULL,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    expected_delivery_date DATE,
    currency_id INTEGER NOT NULL REFERENCES currencies(id),
    exchange_rate DECIMAL(15, 5) DEFAULT 1.0,
    subtotal DECIMAL(15, 2) DEFAULT 0,
    tax_amount DECIMAL(15, 2) DEFAULT 0,
    discount_amount DECIMAL(15, 2) DEFAULT 0,
    total_amount DECIMAL(15, 2) DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'draft', -- (draft, approved, sent, partially_received, received, cancelled)
    notes TEXT,
    payment_terms TEXT,
    shipping_terms TEXT,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    branch_id INTEGER REFERENCES branches(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id),
    approved_at TIMESTAMP WITH TIME ZONE,
    approved_by INTEGER REFERENCES users(id)
);

-- جدول تفاصيل أوامر الشراء
CREATE TABLE IF NOT EXISTS purchase_order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES purchase_orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    description TEXT,
    quantity DECIMAL(15, 5) NOT NULL,
    unit_id INTEGER NOT NULL REFERENCES units_of_measure(id),
    unit_price DECIMAL(15, 5) NOT NULL,
    tax_rate DECIMAL(5, 2) DEFAULT 0,
    tax_amount DECIMAL(15, 2) DEFAULT 0,
    discount_rate DECIMAL(5, 2) DEFAULT 0,
    discount_amount DECIMAL(15, 2) DEFAULT 0,
    total_amount DECIMAL(15, 2) DEFAULT 0,
    received_quantity DECIMAL(15, 5) DEFAULT 0,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول استلام البضائع
CREATE TABLE IF NOT EXISTS goods_receipts (
    id SERIAL PRIMARY KEY,
    receipt_number VARCHAR(50) NOT NULL UNIQUE,
    receipt_date TIMESTAMP WITH TIME ZONE NOT NULL,
    purchase_order_id INTEGER REFERENCES purchase_orders(id),
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    supplier_invoice_number VARCHAR(50),
    supplier_invoice_date DATE,
    currency_id INTEGER NOT NULL REFERENCES currencies(id),
    exchange_rate DECIMAL(15, 5) DEFAULT 1.0,
    subtotal DECIMAL(15, 2) DEFAULT 0,
    tax_amount DECIMAL(15, 2) DEFAULT 0,
    discount_amount DECIMAL(15, 2) DEFAULT 0,
    total_amount DECIMAL(15, 2) DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'draft', -- (draft, posted, cancelled)
    notes TEXT,
    inventory_transaction_id INTEGER REFERENCES inventory_transactions(id),
    journal_entry_id INTEGER REFERENCES journal_entries(id),
    company_id INTEGER NOT NULL REFERENCES companies(id),
    branch_id INTEGER REFERENCES branches(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id),
    posted_at TIMESTAMP WITH TIME ZONE,
    posted_by INTEGER REFERENCES users(id)
);

-- جدول تفاصيل استلام البضائع
CREATE TABLE IF NOT EXISTS goods_receipt_items (
    id SERIAL PRIMARY KEY,
    receipt_id INTEGER NOT NULL REFERENCES goods_receipts(id),
    purchase_order_item_id INTEGER REFERENCES purchase_order_items(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    description TEXT,
    quantity DECIMAL(15, 5) NOT NULL,
    unit_id INTEGER NOT NULL REFERENCES units_of_measure(id),
    unit_price DECIMAL(15, 5) NOT NULL,
    tax_rate DECIMAL(5, 2) DEFAULT 0,
    tax_amount DECIMAL(15, 2) DEFAULT 0,
    discount_rate DECIMAL(5, 2) DEFAULT 0,
    discount_amount DECIMAL(15, 2) DEFAULT 0,
    total_amount DECIMAL(15, 2) DEFAULT 0,
    lot_number VARCHAR(50),
    expiry_date DATE,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول أوامر التحويل بين المستودعات
CREATE TABLE IF NOT EXISTS transfer_orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    order_date TIMESTAMP WITH TIME ZONE NOT NULL,
    source_warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    destination_warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    expected_delivery_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'draft', -- (draft, approved, in_transit, completed, cancelled)
    notes TEXT,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    branch_id INTEGER REFERENCES branches(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id),
    approved_at TIMESTAMP WITH TIME ZONE,
    approved_by INTEGER REFERENCES users(id),
    completed_at TIMESTAMP WITH TIME ZONE,
    completed_by INTEGER REFERENCES users(id)
);

-- جدول تفاصيل أوامر التحويل
CREATE TABLE IF NOT EXISTS transfer_order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES transfer_orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    description TEXT,
    quantity DECIMAL(15, 5) NOT NULL,
    unit_id INTEGER NOT NULL REFERENCES units_of_measure(id),
    unit_cost DECIMAL(15, 5) DEFAULT 0,
    total_cost DECIMAL(15, 2) DEFAULT 0,
    shipped_quantity DECIMAL(15, 5) DEFAULT 0,
    received_quantity DECIMAL(15, 5) DEFAULT 0,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id)
);

-- جدول التكامل مع النظام الزراعي
CREATE TABLE IF NOT EXISTS agricultural_inventory_integration (
    id SERIAL PRIMARY KEY,
    agricultural_product_id INTEGER NOT NULL,
    erp_product_id INTEGER NOT NULL REFERENCES products(id),
    last_sync_date TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(20) DEFAULT 'pending', -- (pending, synced, error)
    error_message TEXT,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES users(id),
    UNIQUE(agricultural_product_id, company_id)
);

-- إنشاء الفهارس لتحسين الأداء
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_company_id ON products(company_id);
CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_warehouse_id ON inventory(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_warehouse_id ON inventory_transactions(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_status ON inventory_transactions(status);
CREATE INDEX IF NOT EXISTS idx_inventory_transaction_items_transaction_id ON inventory_transaction_items(transaction_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transaction_items_product_id ON inventory_transaction_items(product_id);
CREATE INDEX IF NOT EXISTS idx_purchase_orders_supplier_id ON purchase_orders(supplier_id);
CREATE INDEX IF NOT EXISTS idx_purchase_orders_status ON purchase_orders(status);
CREATE INDEX IF NOT EXISTS idx_purchase_order_items_order_id ON purchase_order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_goods_receipts_purchase_order_id ON goods_receipts(purchase_order_id);
CREATE INDEX IF NOT EXISTS idx_goods_receipt_items_receipt_id ON goods_receipt_items(receipt_id);
CREATE INDEX IF NOT EXISTS idx_transfer_orders_source_warehouse_id ON transfer_orders(source_warehouse_id);
CREATE INDEX IF NOT EXISTS idx_transfer_orders_destination_warehouse_id ON transfer_orders(destination_warehouse_id);
CREATE INDEX IF NOT EXISTS idx_transfer_order_items_order_id ON transfer_order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_agricultural_inventory_integration_agricultural_product_id ON agricultural_inventory_integration(agricultural_product_id);
CREATE INDEX IF NOT EXISTS idx_agricultural_inventory_integration_erp_product_id ON agricultural_inventory_integration(erp_product_id);
