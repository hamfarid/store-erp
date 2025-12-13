-- إضافة جميع الأذونات والأدوار إلى قاعدة البيانات (متوافق مع الهيكل الفعلي)

-- حذف البيانات القديمة
DELETE FROM role_permissions;
DELETE FROM user_roles;
DELETE FROM permissions WHERE id > 0;
DELETE FROM roles WHERE id > 1;

-- إضافة الأذونات (85+ إذن)

-- أذونات المستخدمين
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('users.view', 'View Users', 'عرض المستخدمين', 'Ability to view users list', 'القدرة على عرض قائمة المستخدمين', 'users', 1),
('users.create', 'Create User', 'إنشاء مستخدم', 'Ability to create new user', 'القدرة على إنشاء مستخدم جديد', 'users', 1),
('users.edit', 'Edit User', 'تعديل مستخدم', 'Ability to edit user data', 'القدرة على تعديل بيانات المستخدم', 'users', 1),
('users.delete', 'Delete User', 'حذف مستخدم', 'Ability to delete user', 'القدرة على حذف مستخدم', 'users', 1),
('users.manage_roles', 'Manage User Roles', 'إدارة أدوار المستخدمين', 'Ability to assign roles to users', 'القدرة على تعيين الأدوار للمستخدمين', 'users', 1);

-- أذونات المنتجات
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('products.view', 'View Products', 'عرض المنتجات', 'Ability to view products list', 'القدرة على عرض قائمة المنتجات', 'products', 1),
('products.create', 'Create Product', 'إنشاء منتج', 'Ability to create new product', 'القدرة على إنشاء منتج جديد', 'products', 1),
('products.edit', 'Edit Product', 'تعديل منتج', 'Ability to edit product data', 'القدرة على تعديل بيانات المنتج', 'products', 1),
('products.delete', 'Delete Product', 'حذف منتج', 'Ability to delete product', 'القدرة على حذف منتج', 'products', 1),
('products.manage_prices', 'Manage Prices', 'إدارة الأسعار', 'Ability to modify product prices', 'القدرة على تعديل أسعار المنتجات', 'products', 1),
('products.manage_stock', 'Manage Stock', 'إدارة المخزون', 'Ability to modify stock quantities', 'القدرة على تعديل كميات المخزون', 'products', 1);

-- أذونات المبيعات
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('sales.view', 'View Sales', 'عرض المبيعات', 'Ability to view sales list', 'القدرة على عرض قائمة المبيعات', 'sales', 1),
('sales.create', 'Create Sale Invoice', 'إنشاء فاتورة بيع', 'Ability to create new sale invoice', 'القدرة على إنشاء فاتورة بيع جديدة', 'sales', 1),
('sales.edit', 'Edit Sale Invoice', 'تعديل فاتورة بيع', 'Ability to edit sale invoice', 'القدرة على تعديل فاتورة بيع', 'sales', 1),
('sales.delete', 'Delete Sale Invoice', 'حذف فاتورة بيع', 'Ability to delete sale invoice', 'القدرة على حذف فاتورة بيع', 'sales', 1),
('sales.refund', 'Refund Sales', 'إرجاع مبيعات', 'Ability to refund sales', 'القدرة على إرجاع المبيعات', 'sales', 1),
('sales.discount', 'Apply Discounts', 'تطبيق خصومات', 'Ability to apply discounts on sales', 'القدرة على تطبيق خصومات على المبيعات', 'sales', 1);

-- أذونات المشتريات
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('purchases.view', 'View Purchases', 'عرض المشتريات', 'Ability to view purchases list', 'القدرة على عرض قائمة المشتريات', 'purchases', 1),
('purchases.create', 'Create Purchase Order', 'إنشاء أمر شراء', 'Ability to create new purchase order', 'القدرة على إنشاء أمر شراء جديد', 'purchases', 1),
('purchases.edit', 'Edit Purchase Order', 'تعديل أمر شراء', 'Ability to edit purchase order', 'القدرة على تعديل أمر شراء', 'purchases', 1),
('purchases.delete', 'Delete Purchase Order', 'حذف أمر شراء', 'Ability to delete purchase order', 'القدرة على حذف أمر شراء', 'purchases', 1),
('purchases.approve', 'Approve Purchase Order', 'اعتماد أمر شراء', 'Ability to approve purchase orders', 'القدرة على اعتماد أوامر الشراء', 'purchases', 1),
('purchases.receive', 'Receive Purchase Order', 'استلام أمر شراء', 'Ability to receive purchase orders', 'القدرة على استلام أوامر الشراء', 'purchases', 1);

-- أذونات اللوطات
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('lots.view', 'View Lots', 'عرض اللوطات', 'Ability to view lots list', 'القدرة على عرض قائمة اللوطات', 'lots', 1),
('lots.create', 'Create Lot', 'إنشاء لوط', 'Ability to create new lot', 'القدرة على إنشاء لوط جديد', 'lots', 1),
('lots.edit', 'Edit Lot', 'تعديل لوط', 'Ability to edit lot data', 'القدرة على تعديل بيانات اللوط', 'lots', 1),
('lots.delete', 'Delete Lot', 'حذف لوط', 'Ability to delete lot', 'القدرة على حذف لوط', 'lots', 1),
('lots.quality_test', 'Quality Test', 'فحص جودة', 'Ability to perform quality tests', 'القدرة على إجراء فحوصات الجودة', 'lots', 1),
('lots.ministry_approval', 'Ministry Approval', 'موافقة وزارة', 'Ability to manage ministry approvals', 'القدرة على إدارة موافقات الوزارة', 'lots', 1);

-- أذونات العملاء
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('customers.view', 'View Customers', 'عرض العملاء', 'Ability to view customers list', 'القدرة على عرض قائمة العملاء', 'customers', 1),
('customers.create', 'Create Customer', 'إنشاء عميل', 'Ability to create new customer', 'القدرة على إنشاء عميل جديد', 'customers', 1),
('customers.edit', 'Edit Customer', 'تعديل عميل', 'Ability to edit customer data', 'القدرة على تعديل بيانات العميل', 'customers', 1),
('customers.delete', 'Delete Customer', 'حذف عميل', 'Ability to delete customer', 'القدرة على حذف عميل', 'customers', 1);

-- أذونات الموردين
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('suppliers.view', 'View Suppliers', 'عرض الموردين', 'Ability to view suppliers list', 'القدرة على عرض قائمة الموردين', 'suppliers', 1),
('suppliers.create', 'Create Supplier', 'إنشاء مورد', 'Ability to create new supplier', 'القدرة على إنشاء مورد جديد', 'suppliers', 1),
('suppliers.edit', 'Edit Supplier', 'تعديل مورد', 'Ability to edit supplier data', 'القدرة على تعديل بيانات المورد', 'suppliers', 1),
('suppliers.delete', 'Delete Supplier', 'حذف مورد', 'Ability to delete supplier', 'القدرة على حذف مورد', 'suppliers', 1);

-- أذونات المخازن
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('warehouses.view', 'View Warehouses', 'عرض المخازن', 'Ability to view warehouses list', 'القدرة على عرض قائمة المخازن', 'warehouses', 1),
('warehouses.create', 'Create Warehouse', 'إنشاء مخزن', 'Ability to create new warehouse', 'القدرة على إنشاء مخزن جديد', 'warehouses', 1),
('warehouses.edit', 'Edit Warehouse', 'تعديل مخزن', 'Ability to edit warehouse data', 'القدرة على تعديل بيانات المخزن', 'warehouses', 1),
('warehouses.delete', 'Delete Warehouse', 'حذف مخزن', 'Ability to delete warehouse', 'القدرة على حذف مخزن', 'warehouses', 1),
('warehouses.transfer', 'Transfer Between Warehouses', 'نقل بين المخازن', 'Ability to transfer products between warehouses', 'القدرة على نقل المنتجات بين المخازن', 'warehouses', 1);

-- أذونات المحاسبة
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('accounting.view', 'View Accounts', 'عرض الحسابات', 'Ability to view accounts', 'القدرة على عرض الحسابات', 'accounting', 1),
('accounting.create', 'Create Entry', 'إنشاء قيد', 'Ability to create accounting entries', 'القدرة على إنشاء قيود محاسبية', 'accounting', 1),
('accounting.edit', 'Edit Entry', 'تعديل قيد', 'Ability to edit accounting entries', 'القدرة على تعديل القيود المحاسبية', 'accounting', 1),
('accounting.delete', 'Delete Entry', 'حذف قيد', 'Ability to delete accounting entries', 'القدرة على حذف القيود المحاسبية', 'accounting', 1),
('accounting.close_period', 'Close Period', 'إقفال فترة', 'Ability to close accounting periods', 'القدرة على إقفال الفترات المحاسبية', 'accounting', 1);

-- أذونات التقارير
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('reports.sales', 'Sales Reports', 'تقارير المبيعات', 'Ability to view sales reports', 'القدرة على عرض تقارير المبيعات', 'reports', 1),
('reports.purchases', 'Purchases Reports', 'تقارير المشتريات', 'Ability to view purchases reports', 'القدرة على عرض تقارير المشتريات', 'reports', 1),
('reports.inventory', 'Inventory Reports', 'تقارير المخزون', 'Ability to view inventory reports', 'القدرة على عرض تقارير المخزون', 'reports', 1),
('reports.financial', 'Financial Reports', 'تقارير مالية', 'Ability to view financial reports', 'القدرة على عرض التقارير المالية', 'reports', 1),
('reports.customers', 'Customers Reports', 'تقارير العملاء', 'Ability to view customers reports', 'القدرة على عرض تقارير العملاء', 'reports', 1),
('reports.suppliers', 'Suppliers Reports', 'تقارير الموردين', 'Ability to view suppliers reports', 'القدرة على عرض تقارير الموردين', 'reports', 1),
('reports.lots', 'Lots Reports', 'تقارير اللوطات', 'Ability to view lots reports', 'القدرة على عرض تقارير اللوطات', 'reports', 1);

-- أذونات نقطة البيع
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('pos.access', 'Access POS', 'الوصول لنقطة البيع', 'Ability to access POS system', 'القدرة على الوصول لنظام نقطة البيع', 'pos', 1),
('pos.sell', 'Sell', 'البيع', 'Ability to perform sales', 'القدرة على إجراء عمليات البيع', 'pos', 1),
('pos.refund', 'Refund', 'الإرجاع', 'Ability to refund sales', 'القدرة على إرجاع المبيعات', 'pos', 1),
('pos.open_close_shift', 'Open/Close Shift', 'فتح/إغلاق الوردية', 'Ability to open and close shifts', 'القدرة على فتح وإغلاق الورديات', 'pos', 1),
('pos.manage_cash', 'Manage Cash', 'إدارة النقدية', 'Ability to manage cash drawer', 'القدرة على إدارة النقدية في الدرج', 'pos', 1);

-- أذونات الإعدادات
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('settings.view', 'View Settings', 'عرض الإعدادات', 'Ability to view system settings', 'القدرة على عرض إعدادات النظام', 'settings', 1),
('settings.edit', 'Edit Settings', 'تعديل الإعدادات', 'Ability to edit system settings', 'القدرة على تعديل إعدادات النظام', 'settings', 1),
('settings.backup', 'Backup', 'النسخ الاحتياطي', 'Ability to create backups', 'القدرة على إنشاء نسخ احتياطية', 'settings', 1),
('settings.restore', 'Restore', 'الاستعادة', 'Ability to restore backups', 'القدرة على استعادة النسخ الاحتياطية', 'settings', 1);

-- أذونات الأدوار والأذونات
INSERT INTO permissions (code, name, name_ar, description, description_ar, module, is_active) VALUES
('roles.view', 'View Roles', 'عرض الأدوار', 'Ability to view roles list', 'القدرة على عرض قائمة الأدوار', 'roles', 1),
('roles.create', 'Create Role', 'إنشاء دور', 'Ability to create new role', 'القدرة على إنشاء دور جديد', 'roles', 1),
('roles.edit', 'Edit Role', 'تعديل دور', 'Ability to edit roles', 'القدرة على تعديل الأدوار', 'roles', 1),
('roles.delete', 'Delete Role', 'حذف دور', 'Ability to delete role', 'القدرة على حذف دور', 'roles', 1),
('roles.assign_permissions', 'Assign Permissions', 'تعيين أذونات', 'Ability to assign permissions to roles', 'القدرة على تعيين الأذونات للأدوار', 'roles', 1);

-- إضافة الأدوار (7 أدوار)

-- 1. Super Admin
INSERT INTO roles (code, name, name_ar, description, description_ar, is_system, is_active, priority, color, icon) VALUES
('superadmin', 'Super Admin', 'مدير النظام الأعلى', 'Full permissions on all system parts', 'صلاحيات كاملة على جميع أجزاء النظام', 1, 1, 1, '#FF0000', 'shield');

-- 2. Admin
INSERT INTO roles (code, name, name_ar, description, description_ar, is_system, is_active, priority, color, icon) VALUES
('admin', 'Admin', 'مدير النظام', 'High administrative permissions', 'صلاحيات إدارية عالية', 1, 1, 2, '#FF5722', 'admin_panel_settings');

-- 3. Manager
INSERT INTO roles (code, name, name_ar, description, description_ar, is_system, is_active, priority, color, icon) VALUES
('manager', 'Manager', 'مدير', 'Daily operations management permissions', 'صلاحيات إدارة العمليات اليومية', 1, 1, 3, '#2196F3', 'manage_accounts');

-- 4. Cashier
INSERT INTO roles (code, name, name_ar, description, description_ar, is_system, is_active, priority, color, icon) VALUES
('cashier', 'Cashier', 'أمين صندوق', 'POS and sales permissions', 'صلاحيات نقطة البيع والمبيعات', 1, 1, 4, '#4CAF50', 'point_of_sale');

-- 5. Warehouse Keeper
INSERT INTO roles (code, name, name_ar, description, description_ar, is_system, is_active, priority, color, icon) VALUES
('warehouse_keeper', 'Warehouse Keeper', 'أمين مخزن', 'Inventory management permissions', 'صلاحيات إدارة المخزون', 1, 1, 5, '#9C27B0', 'warehouse');

-- 6. Accountant
INSERT INTO roles (code, name, name_ar, description, description_ar, is_system, is_active, priority, color, icon) VALUES
('accountant', 'Accountant', 'محاسب', 'Accounting and financial reports permissions', 'صلاحيات المحاسبة والتقارير المالية', 1, 1, 6, '#FF9800', 'account_balance');

-- 7. Viewer
INSERT INTO roles (code, name, name_ar, description, description_ar, is_system, is_active, priority, color, icon) VALUES
('viewer', 'Viewer', 'مشاهد', 'View only permissions', 'صلاحيات العرض فقط', 1, 1, 7, '#607D8B', 'visibility');

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
WHERE module IN ('products', 'sales', 'purchases', 'customers', 'suppliers', 'warehouses', 'lots', 'reports')
AND code NOT LIKE '%.delete';

-- Cashier: أذونات نقطة البيع والمبيعات
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'cashier'),
    id
FROM permissions
WHERE code IN ('pos.access', 'pos.sell', 'pos.refund', 'pos.open_close_shift', 'sales.view', 'sales.create', 'customers.view', 'customers.create');

-- Warehouse Keeper: أذونات المخزون واللوطات
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'warehouse_keeper'),
    id
FROM permissions
WHERE code IN ('products.view', 'products.manage_stock', 'warehouses.view', 'warehouses.transfer', 'lots.view', 'lots.create', 'lots.edit', 'purchases.view', 'purchases.receive');

-- Accountant: أذونات المحاسبة والتقارير
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'accountant'),
    id
FROM permissions
WHERE module IN ('accounting', 'reports')
OR code IN ('sales.view', 'purchases.view', 'customers.view', 'suppliers.view');

-- Viewer: أذونات العرض فقط
INSERT INTO role_permissions (role_id, permission_id)
SELECT 
    (SELECT id FROM roles WHERE code = 'viewer'),
    id
FROM permissions
WHERE code LIKE '%.view'
OR code IN ('reports.sales', 'reports.purchases', 'reports.inventory', 'reports.customers', 'reports.suppliers', 'reports.lots');
