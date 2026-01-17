-- إنشاء جداول نظام نقطة البيع (POS)

-- جدول الورديات
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_number VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    branch_id INTEGER,
    
    -- معلومات الوردية
    opening_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closing_time DATETIME,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    
    -- النقدية
    opening_cash REAL NOT NULL DEFAULT 0.0,
    closing_cash REAL,
    expected_cash REAL,
    cash_difference REAL,
    
    -- الإحصائيات
    total_sales REAL NOT NULL DEFAULT 0.0,
    total_refunds REAL NOT NULL DEFAULT 0.0,
    total_transactions INTEGER NOT NULL DEFAULT 0,
    
    -- طرق الدفع
    cash_sales REAL NOT NULL DEFAULT 0.0,
    card_sales REAL NOT NULL DEFAULT 0.0,
    other_sales REAL NOT NULL DEFAULT 0.0,
    
    -- ملاحظات
    opening_notes TEXT,
    closing_notes TEXT,
    
    -- التواريخ
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- جدول المبيعات
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- معلومات العميل
    customer_id INTEGER,
    customer_name VARCHAR(200),
    
    -- معلومات الوردية والفرع
    shift_id INTEGER,
    branch_id INTEGER,
    user_id INTEGER NOT NULL,
    
    -- المبالغ
    subtotal REAL NOT NULL DEFAULT 0.0,
    discount_amount REAL NOT NULL DEFAULT 0.0,
    discount_percentage REAL NOT NULL DEFAULT 0.0,
    tax_amount REAL NOT NULL DEFAULT 0.0,
    tax_percentage REAL NOT NULL DEFAULT 0.0,
    total REAL NOT NULL DEFAULT 0.0,
    
    -- الدفع
    payment_method VARCHAR(20) NOT NULL DEFAULT 'cash',
    paid_amount REAL NOT NULL DEFAULT 0.0,
    change_amount REAL NOT NULL DEFAULT 0.0,
    
    -- الحالة
    status VARCHAR(20) NOT NULL DEFAULT 'completed',
    is_refund BOOLEAN DEFAULT 0,
    refund_of_sale_id INTEGER,
    
    -- ملاحظات
    notes TEXT,
    
    -- التواريخ
    sale_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (shift_id) REFERENCES shifts(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (refund_of_sale_id) REFERENCES sales(id)
);

-- جدول عناصر المبيعات
CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    batch_id INTEGER,
    
    -- معلومات المنتج
    product_name VARCHAR(200) NOT NULL,
    product_code VARCHAR(100),
    
    -- الكميات والأسعار
    quantity REAL NOT NULL,
    unit_price REAL NOT NULL,
    discount_amount REAL NOT NULL DEFAULT 0.0,
    discount_percentage REAL NOT NULL DEFAULT 0.0,
    total REAL NOT NULL,
    
    -- معلومات اللوط
    lot_number VARCHAR(100),
    expiry_date DATETIME,
    
    -- التواريخ
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (batch_id) REFERENCES batches_advanced(id)
);

-- الفهارس
CREATE INDEX IF NOT EXISTS idx_shifts_user_id ON shifts(user_id);
CREATE INDEX IF NOT EXISTS idx_shifts_status ON shifts(status);
CREATE INDEX IF NOT EXISTS idx_shifts_opening_time ON shifts(opening_time);

CREATE INDEX IF NOT EXISTS idx_sales_invoice_number ON sales(invoice_number);
CREATE INDEX IF NOT EXISTS idx_sales_customer_id ON sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_shift_id ON sales(shift_id);
CREATE INDEX IF NOT EXISTS idx_sales_user_id ON sales(user_id);
CREATE INDEX IF NOT EXISTS idx_sales_sale_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_status ON sales(status);

CREATE INDEX IF NOT EXISTS idx_sale_items_sale_id ON sale_items(sale_id);
CREATE INDEX IF NOT EXISTS idx_sale_items_product_id ON sale_items(product_id);
CREATE INDEX IF NOT EXISTS idx_sale_items_batch_id ON sale_items(batch_id);

-- بيانات تجريبية (وردية واحدة مفتوحة)
INSERT INTO shifts (shift_number, user_id, opening_cash, status) VALUES
('SH-20251213150000', 1, 1000.0, 'open');
