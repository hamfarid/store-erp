# مسارات الواجهة الخلفية - Gaara ERP v12

## نظرة عامة
توثيق شامل لجميع مسارات API الخلفية في نظام Gaara ERP v12.

## 1. مسارات المصادقة
- `POST /api/auth/login/` - تسجيل الدخول
- `POST /api/auth/logout/` - تسجيل الخروج
- `POST /api/auth/refresh/` - تجديد الرمز المميز
- `POST /api/auth/mfa/setup/` - إعداد MFA
- `POST /api/auth/mfa/verify/` - التحقق من MFA

## 2. مسارات المحاسبة
- `GET /api/accounting/accounts/` - قائمة الحسابات
- `POST /api/accounting/accounts/` - إنشاء حساب جديد
- `GET /api/accounting/journal-entries/` - قائمة القيود
- `POST /api/accounting/journal-entries/` - إنشاء قيد جديد

## 3. مسارات المخزون
- `GET /api/inventory/products/` - قائمة المنتجات
- `POST /api/inventory/products/` - إنشاء منتج جديد
- `GET /api/inventory/stock-moves/` - حركات المخزون
- `POST /api/inventory/stock-moves/` - تسجيل حركة مخزون

## 4. مسارات المبيعات
- `GET /api/sales/customers/` - قائمة العملاء
- `POST /api/sales/customers/` - إنشاء عميل جديد
- `GET /api/sales/orders/` - أوامر البيع
- `POST /api/sales/orders/` - إنشاء أمر بيع

## 5. مسارات المشتريات
- `GET /api/purchasing/suppliers/` - قائمة الموردين
- `POST /api/purchasing/suppliers/` - إنشاء مورد جديد
- `GET /api/purchasing/orders/` - أوامر الشراء
- `POST /api/purchasing/orders/` - إنشاء أمر شراء

---
**تاريخ التوثيق**: نوفمبر 2025
**إصدار النظام**: Gaara ERP v12 Enhanced Security Edition
