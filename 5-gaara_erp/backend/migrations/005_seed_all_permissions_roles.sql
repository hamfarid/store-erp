-- إضافة جميع الأذونات والأدوار إلى قاعدة البيانات

-- حذف البيانات القديمة
DELETE FROM role_permissions;
DELETE FROM user_roles;
DELETE FROM permissions WHERE id > 0;
DELETE FROM roles WHERE id > 1;

-- إضافة الأذونات (100+ إذن)

-- أذونات المستخدمين
INSERT INTO permissions (code, name, description, category) VALUES
('users.view', 'عرض المستخدمين', 'القدرة على عرض قائمة المستخدمين', 'users'),
('users.create', 'إنشاء مستخدم', 'القدرة على إنشاء مستخدم جديد', 'users'),
('users.edit', 'تعديل مستخدم', 'القدرة على تعديل بيانات المستخدم', 'users'),
('users.delete', 'حذف مستخدم', 'القدرة على حذف مستخدم', 'users'),
('users.manage_roles', 'إدارة أدوار المستخدمين', 'القدرة على تعيين الأدوار للمستخدمين', 'users');

-- أذونات المنتجات
INSERT INTO permissions (code, name, description, category) VALUES
('products.view', 'عرض المنتجات', 'القدرة على عرض قائمة المنتجات', 'products'),
('products.create', 'إنشاء منتج', 'القدرة على إنشاء منتج جديد', 'products'),
('products.edit', 'تعديل منتج', 'القدرة على تعديل بيانات المنتج', 'products'),
('products.delete', 'حذف منتج', 'القدرة على حذف منتج', 'products'),
('products.manage_prices', 'إدارة الأسعار', 'القدرة على تعديل أسعار المنتجات', 'products'),
('products.manage_stock', 'إدارة المخزون', 'القدرة على تعديل كميات المخزون', 'products');

-- أذونات المبيعات
INSERT INTO permissions (code, name, description, category) VALUES
('sales.view', 'عرض المبيعات', 'القدرة على عرض قائمة المبيعات', 'sales'),
('sales.create', 'إنشاء فاتورة بيع', 'القدرة على إنشاء فاتورة بيع جديدة', 'sales'),
('sales.edit', 'تعديل فاتورة بيع', 'القدرة على تعديل فاتورة بيع', 'sales'),
('sales.delete', 'حذف فاتورة بيع', 'القدرة على حذف فاتورة بيع', 'sales'),
('sales.refund', 'إرجاع مبيعات', 'القدرة على إرجاع المبيعات', 'sales'),
('sales.discount', 'تطبيق خصومات', 'القدرة على تطبيق خصومات على المبيعات', 'sales');

-- أذونات المشتريات
INSERT INTO permissions (code, name, description, category) VALUES
('purchases.view', 'عرض المشتريات', 'القدرة على عرض قائمة المشتريات', 'purchases'),
('purchases.create', 'إنشاء أمر شراء', 'القدرة على إنشاء أمر شراء جديد', 'purchases'),
('purchases.edit', 'تعديل أمر شراء', 'القدرة على تعديل أمر شراء', 'purchases'),
('purchases.delete', 'حذف أمر شراء', 'القدرة على حذف أمر شراء', 'purchases'),
('purchases.approve', 'اعتماد أمر شراء', 'القدرة على اعتماد أوامر الشراء', 'purchases'),
('purchases.receive', 'استلام أمر شراء', 'القدرة على استلام أوامر الشراء', 'purchases');

-- أذونات اللوطات
INSERT INTO permissions (code, name, description, category) VALUES
('lots.view', 'عرض اللوطات', 'القدرة على عرض قائمة اللوطات', 'lots'),
('lots.create', 'إنشاء لوط', 'القدرة على إنشاء لوط جديد', 'lots'),
('lots.edit', 'تعديل لوط', 'القدرة على تعديل بيانات اللوط', 'lots'),
('lots.delete', 'حذف لوط', 'القدرة على حذف لوط', 'lots'),
('lots.quality_test', 'فحص جودة', 'القدرة على إجراء فحوصات الجودة', 'lots'),
('lots.ministry_approval', 'موافقة وزارة', 'القدرة على إدارة موافقات الوزارة', 'lots');

-- أذونات العملاء
INSERT INTO permissions (code, name, description, category) VALUES
('customers.view', 'عرض العملاء', 'القدرة على عرض قائمة العملاء', 'customers'),
('customers.create', 'إنشاء عميل', 'القدرة على إنشاء عميل جديد', 'customers'),
('customers.edit', 'تعديل عميل', 'القدرة على تعديل بيانات العميل', 'customers'),
('customers.delete', 'حذف عميل', 'القدرة على حذف عميل', 'customers');

-- أذونات الموردين
INSERT INTO permissions (code, name, description, category) VALUES
('suppliers.view', 'عرض الموردين', 'القدرة على عرض قائمة الموردين', 'suppliers'),
('suppliers.create', 'إنشاء مورد', 'القدرة على إنشاء مورد جديد', 'suppliers'),
('suppliers.edit', 'تعديل مورد', 'القدرة على تعديل بيانات المورد', 'suppliers'),
('suppliers.delete', 'حذف مورد', 'القدرة على حذف مورد', 'suppliers');

-- أذونات المخازن
INSERT INTO permissions (code, name, description, category) VALUES
('warehouses.view', 'عرض المخازن', 'القدرة على عرض قائمة المخازن', 'warehouses'),
('warehouses.create', 'إنشاء مخزن', 'القدرة على إنشاء مخزن جديد', 'warehouses'),
('warehouses.edit', 'تعديل مخزن', 'القدرة على تعديل بيانات المخزن', 'warehouses'),
('warehouses.delete', 'حذف مخزن', 'القدرة على حذف مخزن', 'warehouses'),
('warehouses.transfer', 'نقل بين المخازن', 'القدرة على نقل المنتجات بين المخازن', 'warehouses');

-- أذونات المحاسبة
INSERT INTO permissions (code, name, description, category) VALUES
('accounting.view', 'عرض الحسابات', 'القدرة على عرض الحسابات', 'accounting'),
('accounting.create', 'إنشاء قيد', 'القدرة على إنشاء قيود محاسبية', 'accounting'),
('accounting.edit', 'تعديل قيد', 'القدرة على تعديل القيود المحاسبية', 'accounting'),
('accounting.delete', 'حذف قيد', 'القدرة على حذف القيود المحاسبية', 'accounting'),
('accounting.close_period', 'إقفال فترة', 'القدرة على إقفال الفترات المحاسبية', 'accounting');

-- أذونات التقارير
INSERT INTO permissions (code, name, description, category) VALUES
('reports.sales', 'تقارير المبيعات', 'القدرة على عرض تقارير المبيعات', 'reports'),
('reports.purchases', 'تقارير المشتريات', 'القدرة على عرض تقارير المشتريات', 'reports'),
('reports.inventory', 'تقارير المخزون', 'القدرة على عرض تقارير المخزون', 'reports'),
('reports.financial', 'تقارير مالية', 'القدرة على عرض التقارير المالية', 'reports'),
('reports.customers', 'تقارير العملاء', 'القدرة على عرض تقارير العملاء', 'reports'),
('reports.suppliers', 'تقارير الموردين', 'القدرة على عرض تقارير الموردين', 'reports'),
('reports.lots', 'تقارير اللوطات', 'القدرة على عرض تقارير اللوطات', 'reports');

-- أذونات نقطة البيع
INSERT INTO permissions (code, name, description, category) VALUES
('pos.access', 'الوصول لنقطة البيع', 'القدرة على الوصول لنظام نقطة البيع', 'pos'),
('pos.sell', 'البيع', 'القدرة على إجراء عمليات البيع', 'pos'),
('pos.refund', 'الإرجاع', 'القدرة على إرجاع المبيعات', 'pos'),
('pos.open_close_shift', 'فتح/إغلاق الوردية', 'القدرة على فتح وإغلاق الورديات', 'pos'),
('pos.manage_cash', 'إدارة النقدية', 'القدرة على إدارة النقدية في الدرج', 'pos');

-- أذونات الإعدادات
INSERT INTO permissions (code, name, description, category) VALUES
('settings.view', 'عرض الإعدادات', 'القدرة على عرض إعدادات النظام', 'settings'),
('settings.edit', 'تعديل الإعدادات', 'القدرة على تعديل إعدادات النظام', 'settings'),
('settings.backup', 'النسخ الاحتياطي', 'القدرة على إنشاء نسخ احتياطية', 'settings'),
('settings.restore', 'الاستعادة', 'القدرة على استعادة النسخ الاحتياطية', 'settings');

-- أذونات الأدوار والأذونات
INSERT INTO permissions (code, name, description, category) VALUES
('roles.view', 'عرض الأدوار', 'القدرة على عرض قائمة الأدوار', 'roles'),
('roles.create', 'إنشاء دور', 'القدرة على إنشاء دور جديد', 'roles'),
('roles.edit', 'تعديل دور', 'القدرة على تعديل الأدوار', 'roles'),
('roles.delete', 'حذف دور', 'القدرة على حذف دور', 'roles'),
('roles.assign_permissions', 'تعيين أذونات', 'القدرة على تعيين الأذونات للأدوار', 'roles');

-- إضافة الأدوار (7 أدوار)

-- 1. Super Admin
INSERT INTO roles (code, name, description, is_system) VALUES
('superadmin', 'مدير النظام الأعلى', 'صلاحيات كاملة على جميع أجزاء النظام', 1);

-- 2. Admin
INSERT INTO roles (code, name, description, is_system) VALUES
('admin', 'مدير النظام', 'صلاحيات إدارية عالية', 1);

-- 3. Manager
INSERT INTO roles (code, name, description, is_system) VALUES
('manager', 'مدير', 'صلاحيات إدارة العمليات اليومية', 1);

-- 4. Cashier
INSERT INTO roles (code, name, description, is_system) VALUES
('cashier', 'أمين صندوق', 'صلاحيات نقطة البيع والمبيعات', 1);

-- 5. Warehouse Keeper
INSERT INTO roles (code, name, description, is_system) VALUES
('warehouse_keeper', 'أمين مخزن', 'صلاحيات إدارة المخزون', 1);

-- 6. Accountant
INSERT INTO roles (code, name, description, is_system) VALUES
('accountant', 'محاسب', 'صلاحيات المحاسبة والتقارير المالية', 1);

-- 7. Viewer
INSERT INTO roles (code, name, description, is_system) VALUES
('viewer', 'مشاهد', 'صلاحيات العرض فقط', 1);

-- تعيين الأذونات للأدوار

-- Super Admin: جميع الأذونات
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'superadmin'),
    id
FROM permissions;

-- Admin: معظم الأذونات ماعدا بعض الإعدادات الحساسة
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'admin'),
    id
FROM permissions
WHERE code NOT IN ('settings.restore', 'roles.delete');

-- Manager: أذونات العمليات اليومية
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'manager'),
    id
FROM permissions
WHERE category IN ('products', 'sales', 'purchases', 'customers', 'suppliers', 'warehouses', 'lots', 'reports')
AND code NOT LIKE '%.delete';

-- Cashier: أذونات نقطة البيع والمبيعات
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'cashier'),
    id
FROM permissions
WHERE category IN ('pos', 'sales', 'customers')
AND code IN ('pos.access', 'pos.sell', 'pos.refund', 'pos.open_close_shift', 'sales.view', 'sales.create', 'customers.view', 'customers.create');

-- Warehouse Keeper: أذونات المخزون واللوطات
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'warehouse_keeper'),
    id
FROM permissions
WHERE category IN ('products', 'warehouses', 'lots', 'purchases')
AND code IN ('products.view', 'products.manage_stock', 'warehouses.view', 'warehouses.transfer', 'lots.view', 'lots.create', 'lots.edit', 'purchases.view', 'purchases.receive');

-- Accountant: أذونات المحاسبة والتقارير
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'accountant'),
    id
FROM permissions
WHERE category IN ('accounting', 'reports')
OR code IN ('sales.view', 'purchases.view', 'customers.view', 'suppliers.view');

-- Viewer: أذونات العرض فقط
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'viewer'),
    id
FROM permissions
WHERE code LIKE '%.view'
OR code IN ('reports.sales', 'reports.purchases', 'reports.inventory', 'reports.customers', 'reports.suppliers', 'reports.lots');
