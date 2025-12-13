-- Migration: Create batches_advanced table
-- Date: 2025-12-13
-- Description: إنشاء جدول اللوطات المتقدم مع جميع الحقول المطلوبة للبذور والأسمدة

-- إنشاء الجدول الرئيسي
CREATE TABLE IF NOT EXISTS batches_advanced (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- المعلومات الأساسية
    batch_number VARCHAR(100) UNIQUE NOT NULL,
    internal_batch_number VARCHAR(100),
    supplier_batch_number VARCHAR(100),
    ministry_batch_number VARCHAR(100),
    
    -- الربط مع الجداول الأخرى
    product_id INTEGER NOT NULL,
    warehouse_id INTEGER,
    supplier_id INTEGER,
    
    -- الكميات والأسعار
    quantity INTEGER NOT NULL DEFAULT 0,
    original_quantity INTEGER,
    reserved_quantity INTEGER DEFAULT 0,
    cost_price DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    
    -- التواريخ
    manufacture_date DATE,
    expiry_date DATE,
    received_date DATE,
    first_sale_date DATE,
    last_sale_date DATE,
    
    -- معلومات الجودة (للبذور والأسمدة)
    germination_rate FLOAT CHECK (germination_rate >= 0 AND germination_rate <= 100),
    purity_percentage FLOAT CHECK (purity_percentage >= 0 AND purity_percentage <= 100),
    moisture_content FLOAT CHECK (moisture_content >= 0 AND moisture_content <= 100),
    temperature_storage FLOAT,
    ph_level FLOAT,
    nutrient_content TEXT,
    
    -- الحالات
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'expired', 'quarantine', 'recalled', 'damaged', 'reserved', 'sold_out')),
    quality_status VARCHAR(20) DEFAULT 'pending' CHECK (quality_status IN ('pending', 'approved', 'rejected', 'conditional')),
    
    -- فحص الجودة
    quality_test_date DATE,
    quality_test_by INTEGER,
    quality_notes TEXT,
    quality_certificate_number VARCHAR(100),
    quality_certificate_url VARCHAR(255),
    
    -- موافقة الوزارة
    ministry_approval_date DATE,
    ministry_approval_number VARCHAR(100),
    ministry_inspector VARCHAR(200),
    ministry_notes TEXT,
    ministry_certificate_url VARCHAR(255),
    
    -- معلومات إضافية
    storage_location VARCHAR(100),
    storage_conditions TEXT,
    handling_instructions TEXT,
    safety_warnings TEXT,
    notes TEXT,
    tags TEXT,
    
    -- التدقيق
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    updated_by INTEGER,
    
    -- Foreign Keys
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE SET NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (quality_test_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes للأداء
CREATE INDEX IF NOT EXISTS idx_batch_batch_number ON batches_advanced(batch_number);
CREATE INDEX IF NOT EXISTS idx_batch_product ON batches_advanced(product_id);
CREATE INDEX IF NOT EXISTS idx_batch_warehouse ON batches_advanced(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_batch_supplier ON batches_advanced(supplier_id);
CREATE INDEX IF NOT EXISTS idx_batch_status ON batches_advanced(status);
CREATE INDEX IF NOT EXISTS idx_batch_quality_status ON batches_advanced(quality_status);
CREATE INDEX IF NOT EXISTS idx_batch_expiry ON batches_advanced(expiry_date);
CREATE INDEX IF NOT EXISTS idx_batch_ministry ON batches_advanced(ministry_batch_number);
CREATE INDEX IF NOT EXISTS idx_batch_created ON batches_advanced(created_at);
CREATE INDEX IF NOT EXISTS idx_batch_product_status ON batches_advanced(product_id, status);
CREATE INDEX IF NOT EXISTS idx_batch_warehouse_status ON batches_advanced(warehouse_id, status);

-- Trigger للتحديث التلقائي للـ updated_at
CREATE TRIGGER IF NOT EXISTS update_batch_timestamp 
AFTER UPDATE ON batches_advanced
BEGIN
    UPDATE batches_advanced SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger لتحديث حالة اللوط عند انتهاء الصلاحية
CREATE TRIGGER IF NOT EXISTS check_batch_expiry
AFTER UPDATE ON batches_advanced
WHEN NEW.expiry_date < DATE('now') AND NEW.status = 'active'
BEGIN
    UPDATE batches_advanced SET status = 'expired' WHERE id = NEW.id;
END;

-- Trigger لتحديث حالة اللوط عند نفاد الكمية
CREATE TRIGGER IF NOT EXISTS check_batch_quantity
AFTER UPDATE ON batches_advanced
WHEN NEW.quantity <= 0 AND NEW.status = 'active'
BEGIN
    UPDATE batches_advanced SET status = 'sold_out' WHERE id = NEW.id;
END;
