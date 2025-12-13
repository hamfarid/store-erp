-- Migration: Create Purchases Tables
-- Date: 2025-12-13
-- Description: إنشاء جداول نظام المشتريات الكامل

-- ===================================
-- 1. جدول أوامر الشراء (Purchase Orders)
-- ===================================
CREATE TABLE IF NOT EXISTS purchase_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- معلومات أمر الشراء
    po_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Foreign Keys
    supplier_id INTEGER NOT NULL,
    warehouse_id INTEGER,
    
    -- التواريخ
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expected_date DATETIME,
    received_date DATETIME,
    
    -- الحالة
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    -- draft, pending, approved, ordered, partial, received, cancelled
    
    -- المبالغ
    total_amount DECIMAL(15,2) DEFAULT 0,
    paid_amount DECIMAL(15,2) DEFAULT 0,
    
    -- ملاحظات
    notes TEXT,
    terms TEXT,
    
    -- الاعتماد
    approved_by INTEGER,
    approved_at DATETIME,
    
    -- Audit
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE RESTRICT,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE RESTRICT,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes for purchase_orders
CREATE INDEX IF NOT EXISTS idx_po_number ON purchase_orders(po_number);
CREATE INDEX IF NOT EXISTS idx_po_supplier ON purchase_orders(supplier_id);
CREATE INDEX IF NOT EXISTS idx_po_warehouse ON purchase_orders(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_po_status ON purchase_orders(status);
CREATE INDEX IF NOT EXISTS idx_po_order_date ON purchase_orders(order_date);

-- ===================================
-- 2. جدول عناصر أمر الشراء (Purchase Order Items)
-- ===================================
CREATE TABLE IF NOT EXISTS purchase_order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys
    po_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    batch_id INTEGER,
    
    -- الكميات
    quantity DECIMAL(10,3) NOT NULL,
    received_quantity DECIMAL(10,3) DEFAULT 0,
    
    -- الأسعار
    unit_price DECIMAL(10,2) NOT NULL,
    discount_percentage DECIMAL(5,2) DEFAULT 0,
    tax_percentage DECIMAL(5,2) DEFAULT 0,
    
    -- الإجماليات
    subtotal DECIMAL(15,2),
    discount_amount DECIMAL(15,2),
    tax_amount DECIMAL(15,2),
    total_price DECIMAL(15,2),
    final_price DECIMAL(15,2),
    
    -- معلومات المنتج
    expiry_date DATE,
    manufacture_date DATE,
    
    -- ملاحظات
    notes TEXT,
    
    -- Audit
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (po_id) REFERENCES purchase_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    FOREIGN KEY (batch_id) REFERENCES batches_advanced(id) ON DELETE SET NULL
);

-- Indexes for purchase_order_items
CREATE INDEX IF NOT EXISTS idx_poi_po ON purchase_order_items(po_id);
CREATE INDEX IF NOT EXISTS idx_poi_product ON purchase_order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_poi_batch ON purchase_order_items(batch_id);

-- ===================================
-- 3. جدول إيصالات الاستلام (Purchase Receipts)
-- ===================================
CREATE TABLE IF NOT EXISTS purchase_receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- معلومات الإيصال
    receipt_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Foreign Keys
    po_id INTEGER NOT NULL,
    warehouse_id INTEGER,
    received_by INTEGER,
    
    -- التاريخ
    receipt_date DATE NOT NULL,
    
    -- الحالة
    status VARCHAR(20) DEFAULT 'pending',
    -- pending, completed, cancelled
    
    -- ملاحظات
    notes TEXT,
    delivery_notes TEXT,
    quality_notes TEXT,
    
    -- معلومات التوصيل
    driver_name VARCHAR(100),
    vehicle_number VARCHAR(50),
    delivery_company VARCHAR(100),
    
    -- Audit
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    
    FOREIGN KEY (po_id) REFERENCES purchase_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE RESTRICT,
    FOREIGN KEY (received_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes for purchase_receipts
CREATE INDEX IF NOT EXISTS idx_pr_number ON purchase_receipts(receipt_number);
CREATE INDEX IF NOT EXISTS idx_pr_po ON purchase_receipts(po_id);
CREATE INDEX IF NOT EXISTS idx_pr_warehouse ON purchase_receipts(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_pr_date ON purchase_receipts(receipt_date);
CREATE INDEX IF NOT EXISTS idx_pr_status ON purchase_receipts(status);

-- ===================================
-- Triggers
-- ===================================

-- Trigger: تحديث updated_at عند التعديل
CREATE TRIGGER IF NOT EXISTS update_po_timestamp 
AFTER UPDATE ON purchase_orders
BEGIN
    UPDATE purchase_orders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_poi_timestamp 
AFTER UPDATE ON purchase_order_items
BEGIN
    UPDATE purchase_order_items SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_pr_timestamp 
AFTER UPDATE ON purchase_receipts
BEGIN
    UPDATE purchase_receipts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ===================================
-- بيانات تجريبية
-- ===================================

-- إضافة بعض أوامر الشراء التجريبية
INSERT OR IGNORE INTO purchase_orders (id, po_number, supplier_id, warehouse_id, order_date, expected_date, status, total_amount, created_by)
VALUES 
(1, 'PO-2025-0001', 1, 1, '2025-12-01', '2025-12-15', 'approved', 50000.00, 1),
(2, 'PO-2025-0002', 2, 1, '2025-12-05', '2025-12-20', 'pending', 35000.00, 1),
(3, 'PO-2025-0003', 1, 2, '2025-12-10', '2025-12-25', 'draft', 25000.00, 1);

-- إضافة عناصر أوامر الشراء
INSERT OR IGNORE INTO purchase_order_items (id, po_id, product_id, quantity, unit_price, discount_percentage, tax_percentage)
VALUES 
(1, 1, 1, 100, 250.00, 5, 14),
(2, 1, 2, 50, 180.00, 0, 14),
(3, 2, 3, 200, 75.00, 10, 14),
(4, 2, 4, 150, 120.00, 5, 14),
(5, 3, 1, 75, 260.00, 0, 14);

-- حساب الإجماليات للعناصر
UPDATE purchase_order_items 
SET 
    subtotal = quantity * unit_price,
    discount_amount = (quantity * unit_price) * (discount_percentage / 100),
    total_price = (quantity * unit_price) - ((quantity * unit_price) * (discount_percentage / 100)),
    tax_amount = ((quantity * unit_price) - ((quantity * unit_price) * (discount_percentage / 100))) * (tax_percentage / 100),
    final_price = ((quantity * unit_price) - ((quantity * unit_price) * (discount_percentage / 100))) + (((quantity * unit_price) - ((quantity * unit_price) * (discount_percentage / 100))) * (tax_percentage / 100))
WHERE id IN (1, 2, 3, 4, 5);

-- تحديث إجماليات أوامر الشراء
UPDATE purchase_orders 
SET total_amount = (
    SELECT SUM(final_price) 
    FROM purchase_order_items 
    WHERE po_id = purchase_orders.id
)
WHERE id IN (1, 2, 3);
