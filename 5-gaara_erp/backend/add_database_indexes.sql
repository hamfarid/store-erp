-- إضافة Indexes مهمة لتحسين الأداء
-- /home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/add_database_indexes.sql

-- Indexes للمنتجات
CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_rank_id ON products(rank_id);
CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);

-- Indexes للحركات
CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(movement_date);
CREATE INDEX IF NOT EXISTS idx_stock_movements_product_id ON stock_movements(product_id);
CREATE INDEX IF NOT EXISTS idx_stock_movements_warehouse_id ON stock_movements(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_stock_movements_type ON stock_movements(movement_type);
CREATE INDEX IF NOT EXISTS idx_stock_movements_reference ON stock_movements(reference_number);

-- Indexes للوطات
CREATE INDEX IF NOT EXISTS idx_batches_expiry ON batches(expiry_date);
CREATE INDEX IF NOT EXISTS idx_batches_product_id ON batches(product_id);
CREATE INDEX IF NOT EXISTS idx_batches_warehouse_id ON batches(warehouse_id);
CREATE INDEX IF NOT EXISTS idx_batches_status ON batches(status);
CREATE INDEX IF NOT EXISTS idx_batches_batch_number ON batches(batch_number);

-- Indexes للوطات الوزارة
CREATE INDEX IF NOT EXISTS idx_ministry_batches_cert_expiry ON ministry_batches(certificate_expiry);
CREATE INDEX IF NOT EXISTS idx_ministry_batches_approval_status ON ministry_batches(approval_status);
CREATE INDEX IF NOT EXISTS idx_ministry_batches_test_date ON ministry_batches(test_date);
CREATE INDEX IF NOT EXISTS idx_ministry_batches_ministry_number ON ministry_batches(ministry_batch_number);

-- Indexes للعملاء والموردين
CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name);
CREATE INDEX IF NOT EXISTS idx_customers_is_active ON customers(is_active);
CREATE INDEX IF NOT EXISTS idx_suppliers_name ON suppliers(name);
CREATE INDEX IF NOT EXISTS idx_suppliers_is_active ON suppliers(is_active);

-- Indexes للمستخدمين
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);

-- Indexes للتواريخ
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);
CREATE INDEX IF NOT EXISTS idx_batches_created_at ON batches(created_at);
CREATE INDEX IF NOT EXISTS idx_stock_movements_created_at ON stock_movements(created_at);

-- Composite Indexes للاستعلامات المعقدة
CREATE INDEX IF NOT EXISTS idx_stock_movements_product_warehouse ON stock_movements(product_id, warehouse_id);
CREATE INDEX IF NOT EXISTS idx_batches_product_warehouse ON batches(product_id, warehouse_id);
CREATE INDEX IF NOT EXISTS idx_stock_movements_date_type ON stock_movements(movement_date, movement_type);

