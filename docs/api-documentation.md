# 📚 API Documentation - توثيق واجهة برمجة التطبيقات

## 🌐 نظرة عامة

يوفر نظام إدارة المخزون الكامل واجهة برمجة تطبيقات RESTful شاملة لإدارة جميع جوانب المخزون والمبيعات والمالية.

### 🔗 Base URL
```
http://localhost:8000/api
```

### 🔐 المصادقة
جميع endpoints تتطلب مصادقة باستثناء endpoints تسجيل الدخول.

```http
Authorization: Bearer <token>
```

## 📦 إدارة المنتجات - Products Management

### GET /api/products
استرجاع قائمة المنتجات

**Parameters:**
- `page` (optional): رقم الصفحة
- `per_page` (optional): عدد العناصر في الصفحة
- `search` (optional): البحث في اسم المنتج
- `category` (optional): فلترة حسب الفئة
- `status` (optional): فلترة حسب الحالة

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "اسم المنتج",
      "sku": "SKU001",
      "category": "الفئة",
      "price": 100.00,
      "quantity": 50,
      "status": "active"
    }
  ],
  "total": 100,
  "pages": 10,
  "current_page": 1
}
```

### POST /api/products
إضافة منتج جديد

**Request Body:**
```json
{
  "name": "اسم المنتج",
  "sku": "SKU001",
  "category": "الفئة",
  "price": 100.00,
  "quantity": 50,
  "description": "وصف المنتج"
}
```

### PUT /api/products/{id}
تحديث منتج موجود

### DELETE /api/products/{id}
حذف منتج

## 🛒 إدارة المبيعات - Sales Management

### GET /api/sales
استرجاع قائمة المبيعات

### POST /api/sales
إنشاء فاتورة مبيعات جديدة

**Request Body:**
```json
{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 100.00
    }
  ],
  "payment_method": "cash",
  "notes": "ملاحظات"
}
```

### GET /api/sales/{id}
استرجاع تفاصيل فاتورة مبيعات

## 🏪 إدارة المشتريات - Purchases Management

### GET /api/purchases
استرجاع قائمة المشتريات

### POST /api/purchases
إنشاء فاتورة مشتريات جديدة

### GET /api/purchases/{id}
استرجاع تفاصيل فاتورة مشتريات

## 👥 إدارة العملاء - Customers Management

### GET /api/customers
استرجاع قائمة العملاء

### POST /api/customers
إضافة عميل جديد

**Request Body:**
```json
{
  "name": "اسم العميل",
  "phone": "123456789",
  "email": "customer@example.com",
  "address": "العنوان",
  "customer_type": "individual"
}
```

### PUT /api/customers/{id}
تحديث بيانات عميل

### DELETE /api/customers/{id}
حذف عميل

## 🏭 إدارة الموردين - Suppliers Management

### GET /api/suppliers
استرجاع قائمة الموردين

### POST /api/suppliers
إضافة مورد جديد

### PUT /api/suppliers/{id}
تحديث بيانات مورد

### DELETE /api/suppliers/{id}
حذف مورد

## 🏢 إدارة المستودعات - Warehouses Management

### GET /api/warehouses
استرجاع قائمة المستودعات

### POST /api/warehouses
إضافة مستودع جديد

**Request Body:**
```json
{
  "name": "اسم المستودع",
  "location": "الموقع",
  "manager": "مدير المستودع",
  "capacity": 1000,
  "status": "active"
}
```

## 💰 إدارة الخزنة - Treasury Management

### GET /api/treasury
استرجاع حالة الخزنة

### POST /api/treasury/transactions
إضافة معاملة خزنة

**Request Body:**
```json
{
  "type": "income", // income, expense
  "amount": 1000.00,
  "description": "وصف المعاملة",
  "category": "sales",
  "reference_id": 123
}
```

### GET /api/treasury/balance
استرجاع رصيد الخزنة

## 💳 إدارة المدفوعات - Payments Management

### GET /api/payments
استرجاع قائمة المدفوعات

### POST /api/payments
تسجيل دفعة جديدة

**Request Body:**
```json
{
  "invoice_id": 1,
  "amount": 500.00,
  "payment_method": "cash", // cash, card, bank_transfer
  "notes": "ملاحظات"
}
```

## 🔄 إدارة المرتجعات - Returns Management

### GET /api/returns
استرجاع قائمة المرتجعات

### POST /api/returns
تسجيل مرتجع جديد

**Request Body:**
```json
{
  "invoice_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 1,
      "reason": "سبب الإرجاع"
    }
  ],
  "return_type": "refund" // refund, exchange
}
```

## 📊 التقارير - Reports

### GET /api/reports/sales
تقرير المبيعات

**Parameters:**
- `start_date`: تاريخ البداية
- `end_date`: تاريخ النهاية
- `customer_id` (optional): فلترة حسب العميل
- `product_id` (optional): فلترة حسب المنتج

### GET /api/reports/inventory
تقرير المخزون

### GET /api/reports/financial
التقرير المالي

### GET /api/reports/customers
تقرير العملاء

## 👤 إدارة المستخدمين - Users Management

### GET /api/users
استرجاع قائمة المستخدمين

### POST /api/users
إضافة مستخدم جديد

**Request Body:**
```json
{
  "username": "اسم المستخدم",
  "email": "user@example.com",
  "password": "كلمة المرور",
  "role": "employee", // admin, manager, employee
  "permissions": ["read_products", "write_sales"]
}
```

### PUT /api/users/{id}
تحديث بيانات مستخدم

### DELETE /api/users/{id}
حذف مستخدم

## 🔐 المصادقة والتفويض - Authentication

### POST /api/auth/login
تسجيل الدخول

**Request Body:**
```json
{
  "username": "اسم المستخدم",
  "password": "كلمة المرور"
}
```

**Response:**
```json
{
  "token": "jwt_token_here",
  "user": {
    "id": 1,
    "username": "اسم المستخدم",
    "role": "admin",
    "permissions": ["all"]
  }
}
```

### POST /api/auth/logout
تسجيل الخروج

### POST /api/auth/refresh
تجديد الرمز المميز

## ⚙️ إعدادات النظام - System Settings

### GET /api/settings
استرجاع إعدادات النظام

### PUT /api/settings
تحديث إعدادات النظام

**Request Body:**
```json
{
  "company_name": "اسم الشركة",
  "currency": "SAR",
  "tax_rate": 15.0,
  "language": "ar",
  "timezone": "Asia/Riyadh"
}
```

## 📤 الاستيراد والتصدير - Import/Export

### POST /api/import/products
استيراد المنتجات من ملف Excel

### GET /api/export/products
تصدير المنتجات إلى ملف Excel

### POST /api/import/customers
استيراد العملاء

### GET /api/export/sales
تصدير تقرير المبيعات

## 🔍 البحث العام - Global Search

### GET /api/search
البحث العام في النظام

**Parameters:**
- `q`: نص البحث
- `type` (optional): نوع البحث (products, customers, suppliers)

## ❌ رموز الأخطاء - Error Codes

- `200`: نجح الطلب
- `201`: تم إنشاء المورد بنجاح
- `400`: خطأ في البيانات المرسلة
- `401`: غير مصرح بالوصول
- `403`: ممنوع الوصول
- `404`: المورد غير موجود
- `500`: خطأ في الخادم

## 📝 ملاحظات مهمة

1. جميع التواريخ بصيغة ISO 8601
2. جميع المبالغ بالعملة المحددة في الإعدادات
3. الترقيم التلقائي للفواتير والمعاملات
4. نظام صلاحيات متقدم لكل endpoint
5. تسجيل جميع العمليات في سجل النظام
