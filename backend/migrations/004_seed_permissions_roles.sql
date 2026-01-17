-- Migration: Seed Permissions and Roles
-- Date: 2025-12-13
-- Description: إنشاء الأذونات والأدوار الافتراضية

-- ===================================
-- إنشاء الأذونات
-- ===================================

-- المنتجات
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('products.create', 'إنشاء منتج', 'إذن إنشاء منتج في products', 'products', 'create', 'inventory', 1),
('products.read', 'عرض المنتجات', 'إذن عرض المنتجات في products', 'products', 'read', 'inventory', 1),
('products.update', 'تعديل منتج', 'إذن تعديل منتج في products', 'products', 'update', 'inventory', 1),
('products.delete', 'حذف منتج', 'إذن حذف منتج في products', 'products', 'delete', 'inventory', 1),
('products.import', 'استيراد منتجات', 'إذن استيراد منتجات في products', 'products', 'import', 'inventory', 1),
('products.export', 'تصدير منتجات', 'إذن تصدير منتجات في products', 'products', 'export', 'inventory', 1);

-- اللوطات
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('batches.create', 'إنشاء لوط', 'إذن إنشاء لوط في batches', 'batches', 'create', 'inventory', 1),
('batches.read', 'عرض اللوطات', 'إذن عرض اللوطات في batches', 'batches', 'read', 'inventory', 1),
('batches.update', 'تعديل لوط', 'إذن تعديل لوط في batches', 'batches', 'update', 'inventory', 1),
('batches.delete', 'حذف لوط', 'إذن حذف لوط في batches', 'batches', 'delete', 'inventory', 1),
('batches.quality_test', 'فحص جودة', 'إذن فحص جودة في batches', 'batches', 'quality_test', 'inventory', 1),
('batches.ministry_approval', 'موافقة وزارة', 'إذن موافقة وزارة في batches', 'batches', 'ministry_approval', 'inventory', 1);

-- المبيعات
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('sales.create', 'إنشاء فاتورة بيع', 'إذن إنشاء فاتورة بيع في sales', 'sales', 'create', 'sales', 1),
('sales.read', 'عرض المبيعات', 'إذن عرض المبيعات في sales', 'sales', 'read', 'sales', 1),
('sales.update', 'تعديل فاتورة', 'إذن تعديل فاتورة في sales', 'sales', 'update', 'sales', 1),
('sales.delete', 'حذف فاتورة', 'إذن حذف فاتورة في sales', 'sales', 'delete', 'sales', 1),
('sales.approve', 'اعتماد فاتورة', 'إذن اعتماد فاتورة في sales', 'sales', 'approve', 'sales', 1),
('sales.cancel', 'إلغاء فاتورة', 'إذن إلغاء فاتورة في sales', 'sales', 'cancel', 'sales', 1);

-- المشتريات
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('purchases.create', 'إنشاء أمر شراء', 'إذن إنشاء أمر شراء في purchases', 'purchases', 'create', 'purchases', 1),
('purchases.read', 'عرض المشتريات', 'إذن عرض المشتريات في purchases', 'purchases', 'read', 'purchases', 1),
('purchases.update', 'تعديل أمر شراء', 'إذن تعديل أمر شراء في purchases', 'purchases', 'update', 'purchases', 1),
('purchases.delete', 'حذف أمر شراء', 'إذن حذف أمر شراء في purchases', 'purchases', 'delete', 'purchases', 1),
('purchases.approve', 'اعتماد أمر شراء', 'إذن اعتماد أمر شراء في purchases', 'purchases', 'approve', 'purchases', 1),
('purchases.receive', 'استلام أمر شراء', 'إذن استلام أمر شراء في purchases', 'purchases', 'receive', 'purchases', 1);

-- نقطة البيع
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('pos.access', 'الوصول لنقطة البيع', 'إذن الوصول لنقطة البيع في pos', 'pos', 'access', 'sales', 1),
('pos.open_session', 'فتح جلسة', 'إذن فتح جلسة في pos', 'pos', 'open_session', 'sales', 1),
('pos.close_session', 'إغلاق جلسة', 'إذن إغلاق جلسة في pos', 'pos', 'close_session', 'sales', 1),
('pos.refund', 'استرجاع', 'إذن استرجاع في pos', 'pos', 'refund', 'sales', 1);

-- العملاء
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('customers.create', 'إنشاء عميل', 'إذن إنشاء عميل في customers', 'customers', 'create', 'sales', 1),
('customers.read', 'عرض العملاء', 'إذن عرض العملاء في customers', 'customers', 'read', 'sales', 1),
('customers.update', 'تعديل عميل', 'إذن تعديل عميل في customers', 'customers', 'update', 'sales', 1),
('customers.delete', 'حذف عميل', 'إذن حذف عميل في customers', 'customers', 'delete', 'sales', 1);

-- الموردين
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('suppliers.create', 'إنشاء مورد', 'إذن إنشاء مورد في suppliers', 'suppliers', 'create', 'purchases', 1),
('suppliers.read', 'عرض الموردين', 'إذن عرض الموردين في suppliers', 'suppliers', 'read', 'purchases', 1),
('suppliers.update', 'تعديل مورد', 'إذن تعديل مورد في suppliers', 'suppliers', 'update', 'purchases', 1),
('suppliers.delete', 'حذف مورد', 'إذن حذف مورد في suppliers', 'suppliers', 'delete', 'purchases', 1);

-- المخازن
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('warehouses.create', 'إنشاء مخزن', 'إذن إنشاء مخزن في warehouses', 'warehouses', 'create', 'inventory', 1),
('warehouses.read', 'عرض المخازن', 'إذن عرض المخازن في warehouses', 'warehouses', 'read', 'inventory', 1),
('warehouses.update', 'تعديل مخزن', 'إذن تعديل مخزن في warehouses', 'warehouses', 'update', 'inventory', 1),
('warehouses.delete', 'حذف مخزن', 'إذن حذف مخزن في warehouses', 'warehouses', 'delete', 'inventory', 1),
('warehouses.transfer', 'نقل بين المخازن', 'إذن نقل بين المخازن في warehouses', 'warehouses', 'transfer', 'inventory', 1);

-- التقارير
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('reports.sales', 'تقارير المبيعات', 'إذن تقارير المبيعات في reports', 'reports', 'sales', 'reports', 1),
('reports.purchases', 'تقارير المشتريات', 'إذن تقارير المشتريات في reports', 'reports', 'purchases', 'reports', 1),
('reports.inventory', 'تقارير المخزون', 'إذن تقارير المخزون في reports', 'reports', 'inventory', 'reports', 1),
('reports.financial', 'تقارير مالية', 'إذن تقارير مالية في reports', 'reports', 'financial', 'reports', 1),
('reports.custom', 'تقارير مخصصة', 'إذن تقارير مخصصة في reports', 'reports', 'custom', 'reports', 1),
('reports.export', 'تصدير تقارير', 'إذن تصدير تقارير في reports', 'reports', 'export', 'reports', 1);

-- المستخدمين
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('users.create', 'إنشاء مستخدم', 'إذن إنشاء مستخدم في users', 'users', 'create', 'admin', 1),
('users.read', 'عرض المستخدمين', 'إذن عرض المستخدمين في users', 'users', 'read', 'admin', 1),
('users.update', 'تعديل مستخدم', 'إذن تعديل مستخدم في users', 'users', 'update', 'admin', 1),
('users.delete', 'حذف مستخدم', 'إذن حذف مستخدم في users', 'users', 'delete', 'admin', 1),
('users.reset_password', 'إعادة تعيين كلمة المرور', 'إذن إعادة تعيين كلمة المرور في users', 'users', 'reset_password', 'admin', 1);

-- الأدوار
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('roles.create', 'إنشاء دور', 'إذن إنشاء دور في roles', 'roles', 'create', 'admin', 1),
('roles.read', 'عرض الأدوار', 'إذن عرض الأدوار في roles', 'roles', 'read', 'admin', 1),
('roles.update', 'تعديل دور', 'إذن تعديل دور في roles', 'roles', 'update', 'admin', 1),
('roles.delete', 'حذف دور', 'إذن حذف دور في roles', 'roles', 'delete', 'admin', 1),
('roles.assign', 'تعيين دور', 'إذن تعيين دور في roles', 'roles', 'assign', 'admin', 1);

-- الإعدادات
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('settings.read', 'عرض الإعدادات', 'إذن عرض الإعدادات في settings', 'settings', 'read', 'admin', 1),
('settings.update', 'تعديل الإعدادات', 'إذن تعديل الإعدادات في settings', 'settings', 'update', 'admin', 1),
('settings.backup', 'النسخ الاحتياطي', 'إذن النسخ الاحتياطي في settings', 'settings', 'backup', 'admin', 1),
('settings.restore', 'الاستعادة', 'إذن الاستعادة في settings', 'settings', 'restore', 'admin', 1);

-- الجودة
INSERT OR IGNORE INTO permissions (name, display_name, description, resource, action, category, is_system) VALUES
('quality.create_test', 'إنشاء فحص جودة', 'إذن إنشاء فحص جودة في quality', 'quality', 'create_test', 'quality', 1),
('quality.read_tests', 'عرض فحوصات الجودة', 'إذن عرض فحوصات الجودة في quality', 'quality', 'read_tests', 'quality', 1),
('quality.approve_test', 'اعتماد فحص', 'إذن اعتماد فحص في quality', 'quality', 'approve_test', 'quality', 1),
('quality.reject_test', 'رفض فحص', 'إذن رفض فحص في quality', 'quality', 'reject_test', 'quality', 1);

-- ===================================
-- إنشاء الأدوار
-- ===================================

-- مسؤول النظام
INSERT OR IGNORE INTO roles (name, display_name, description, permissions, is_system) VALUES
('superadmin', 'مسؤول النظام', 'صلاحيات كاملة على النظام', '["*"]', 1);

-- مدير
INSERT OR IGNORE INTO roles (name, display_name, description, permissions, is_system) VALUES
('admin', 'مدير', 'صلاحيات إدارية', '["products.*", "batches.*", "sales.*", "purchases.*", "customers.*", "suppliers.*", "warehouses.*", "reports.*", "users.read", "users.create", "users.update"]', 1);

-- مدير فرع
INSERT OR IGNORE INTO roles (name, display_name, description, permissions, is_system) VALUES
('manager', 'مدير فرع', 'إدارة الفرع والعمليات اليومية', '["products.read", "products.update", "batches.read", "batches.update", "sales.*", "purchases.read", "purchases.create", "customers.*", "pos.*", "reports.sales", "reports.inventory"]', 1);

-- كاشير
INSERT OR IGNORE INTO roles (name, display_name, description, permissions, is_system) VALUES
('cashier', 'كاشير', 'نقطة البيع والعمليات البسيطة', '["products.read", "batches.read", "sales.create", "sales.read", "customers.read", "customers.create", "pos.access", "pos.open_session", "pos.close_session"]', 1);

-- أمين مخزن
INSERT OR IGNORE INTO roles (name, display_name, description, permissions, is_system) VALUES
('warehouse_keeper', 'أمين مخزن', 'إدارة المخزون واللوطات', '["products.read", "products.update", "batches.*", "purchases.read", "purchases.receive", "warehouses.read", "warehouses.transfer", "quality.create_test", "quality.read_tests", "reports.inventory"]', 1);

-- محاسب
INSERT OR IGNORE INTO roles (name, display_name, description, permissions, is_system) VALUES
('accountant', 'محاسب', 'العمليات المالية والتقارير', '["sales.read", "sales.approve", "purchases.read", "purchases.approve", "customers.read", "suppliers.read", "reports.sales", "reports.purchases", "reports.financial"]', 1);

-- مشاهد
INSERT OR IGNORE INTO roles (name, display_name, description, permissions, is_system) VALUES
('viewer', 'مشاهد', 'عرض فقط بدون تعديل', '["products.read", "batches.read", "sales.read", "purchases.read", "customers.read", "suppliers.read", "warehouses.read", "reports.sales", "reports.inventory"]', 1);
