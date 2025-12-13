# 📚 توثيق API - نظام إدارة المخزون v2.0
## API Documentation - Inventory Management System v2.0

**الإصدار:** 2.0.0 (Unified Models)  
**التاريخ:** 2025-10-08  
**Base URL:** `http://localhost:5002`  
**Content-Type:** `application/json`

---

## 📋 جدول المحتويات

1. [نظرة عامة](#-نظرة-عامة)
2. [المصادقة](#-المصادقة)
3. [صيغة الردود](#-صيغة-الردود)
4. [رموز الحالة](#-رموز-الحالة)
5. [APIs المصادقة](#-apis-المصادقة)
6. [APIs المستخدمين](#-apis-المستخدمين)
7. [APIs الأدوار](#-apis-الأدوار)
8. [APIs المنتجات](#-apis-المنتجات)
9. [APIs الفواتير](#-apis-الفواتير)

---

## 🎯 نظرة عامة

نظام إدارة المخزون يوفر RESTful API كامل لإدارة جميع جوانب المخزون والمبيعات والمشتريات.

### ما الجديد في v2.0؟

- ✅ **نظام JWT محسّن** - Access Tokens + Refresh Tokens
- ✅ **نظام صلاحيات RBAC** - إدارة كاملة للأدوار والصلاحيات
- ✅ **سجل تدقيق** - تتبع جميع العمليات
- ✅ **ردود موحدة** - صيغة JSON موحدة لجميع الردود
- ✅ **معالجة أخطاء محسّنة** - رسائل خطأ واضحة ومفيدة
- ✅ **تصفح وبحث متقدم** - Pagination + Filtering + Search

---

## 🔐 المصادقة

يستخدم النظام **JWT (JSON Web Tokens)** للمصادقة.

### آلية العمل:

1. **تسجيل الدخول** - الحصول على Access Token + Refresh Token
2. **استخدام Access Token** - إرسال مع كل طلب في Header
3. **تحديث Access Token** - استخدام Refresh Token عند انتهاء الصلاحية

### تنسيق Header:

```http
Authorization: Bearer <access_token>
```

### مدة الصلاحية:

- **Access Token:** ساعة واحدة
- **Refresh Token:** 30 يوم

---

## 📦 صيغة الردود

### رد ناجح:

```json
{
  "success": true,
  "data": { ... },
  "message": "رسالة نجاح"
}
```

### رد فاشل:

```json
{
  "success": false,
  "error": "رسالة الخطأ"
}
```

### رد مع تصفح (Pagination):

```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 🔢 رموز الحالة

| الرمز | المعنى | الوصف |
|------|--------|-------|
| 200 | OK | نجح الطلب |
| 201 | Created | تم إنشاء المورد بنجاح |
| 400 | Bad Request | بيانات الطلب غير صحيحة |
| 401 | Unauthorized | المصادقة مطلوبة |
| 403 | Forbidden | ليس لديك صلاحية |
| 404 | Not Found | المورد غير موجود |
| 500 | Internal Server Error | خطأ في الخادم |
| 501 | Not Implemented | الميزة غير متاحة |

---

## 🔑 APIs المصادقة

### 1. تسجيل الدخول

```http
POST /api/auth/login
```

**Request Body:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "المدير",
      "role": "admin"
    }
  },
  "message": "تم تسجيل الدخول بنجاح"
}
```

**Errors:**

- `400` - اسم المستخدم وكلمة المرور مطلوبان
- `401` - اسم المستخدم أو كلمة المرور غير صحيحة
- `403` - الحساب مقفل أو غير نشط

---

### 2. تسجيل الخروج

```http
POST /api/auth/logout
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "message": "تم تسجيل الخروج بنجاح"
}
```

---

### 3. تحديث الرمز

```http
POST /api/auth/refresh
```

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  },
  "message": "تم تحديث رمز الوصول بنجاح"
}
```

---

### 4. التحقق من الرمز

```http
GET /api/auth/verify
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "valid": true,
  "data": {
    "user": { ... },
    "expires_at": 1696800000
  }
}
```

---

### 5. تغيير كلمة المرور

```http
POST /api/auth/change-password
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "old_password": "old_password123",
  "new_password": "new_password456"
}
```

**Response (200):**

```json
{
  "success": true,
  "message": "تم تغيير كلمة المرور بنجاح"
}
```

---

### 6. المستخدم الحالي

```http
GET /api/auth/me
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "المدير",
    "role": "admin",
    "is_active": true,
    "last_login": "2025-10-08T10:00:00",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

---

## 👥 APIs المستخدمين

### 1. قائمة المستخدمين

```http
GET /api/users?page=1&per_page=10&search=admin&role=admin&is_active=true
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Query Parameters:**

| المعامل | النوع | الوصف | افتراضي |
|---------|------|-------|---------|
| page | integer | رقم الصفحة | 1 |
| per_page | integer | عدد العناصر | 10 |
| search | string | البحث في الاسم/البريد | - |
| role | string | تصفية حسب الدور | - |
| is_active | boolean | تصفية حسب الحالة | - |

**Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "المدير",
      "role": "admin",
      "is_active": true
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 1,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

**Permissions:** Admin only

---

### 2. الحصول على مستخدم

```http
GET /api/users/{user_id}
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "المدير",
    "phone": "+966500000000",
    "role": "admin",
    "is_active": true,
    "last_login": "2025-10-08T10:00:00",
    "created_at": "2025-01-01T00:00:00"
  }
}
```

**Errors:**

- `404` - المستخدم غير موجود

---

### 3. إنشاء مستخدم

```http
POST /api/users
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "username": "user1",
  "password": "password123",
  "email": "user1@example.com",
  "full_name": "مستخدم جديد",
  "phone": "+966500000000",
  "role_id": 2,
  "is_active": true
}
```

**Response (201):**

```json
{
  "success": true,
  "data": {
    "id": 2,
    "username": "user1",
    "email": "user1@example.com",
    "full_name": "مستخدم جديد",
    "role": "user",
    "is_active": true
  },
  "message": "تم إنشاء المستخدم بنجاح"
}
```

**Errors:**

- `400` - اسم المستخدم موجود بالفعل
- `400` - البريد الإلكتروني مستخدم بالفعل
- `404` - الدور غير موجود

**Permissions:** Admin only

---

### 4. تحديث مستخدم

```http
PUT /api/users/{user_id}
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "email": "newemail@example.com",
  "full_name": "اسم محدث",
  "phone": "+966500000001",
  "role_id": 3,
  "is_active": false
}
```

**Response (200):**

```json
{
  "success": true,
  "data": { ... },
  "message": "تم تحديث المستخدم بنجاح"
}
```

**Permissions:** Admin only

---

### 5. حذف مستخدم

```http
DELETE /api/users/{user_id}
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "message": "تم حذف المستخدم بنجاح"
}
```

**Errors:**

- `400` - لا يمكنك حذف حسابك الخاص
- `404` - المستخدم غير موجود

**Permissions:** Admin only

---

## 🎭 APIs الأدوار

### 1. قائمة الأدوار

```http
GET /api/roles
```

**Headers:**

```http
Authorization: Bearer <access_token>
```

**Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "admin",
      "display_name": "مدير النظام",
      "description": "صلاحيات كاملة",
      "permissions": ["*"]
    },
    {
      "id": 2,
      "name": "manager",
      "display_name": "مدير",
      "description": "صلاحيات محدودة",
      "permissions": ["view_products", "create_product", "view_invoices"]
    }
  ]
}
```

---

### 2. الحصول على دور

```http
GET /api/roles/{role_id}
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "admin",
    "display_name": "مدير النظام",
    "description": "صلاحيات كاملة",
    "permissions": ["*"],
    "users_count": 5
  }
}
```

---

### 3. إنشاء دور

```http
POST /api/roles
```

**Request Body:**

```json
{
  "name": "accountant",
  "display_name": "محاسب",
  "description": "صلاحيات المحاسبة",
  "permissions": [
    "view_invoices",
    "create_invoice",
    "view_reports",
    "view_payments"
  ]
}
```

**Response (201):**

```json
{
  "success": true,
  "data": { ... },
  "message": "تم إنشاء الدور بنجاح"
}
```

**Permissions:** Admin only

---

### 4. تحديث دور

```http
PUT /api/roles/{role_id}
```

**Request Body:**

```json
{
  "display_name": "محاسب رئيسي",
  "description": "صلاحيات محاسبة متقدمة",
  "permissions": [
    "view_invoices",
    "create_invoice",
    "edit_invoice",
    "delete_invoice",
    "view_reports",
    "view_payments",
    "create_payment"
  ]
}
```

**Response (200):**

```json
{
  "success": true,
  "data": { ... },
  "message": "تم تحديث الدور بنجاح"
}
```

**Permissions:** Admin only

---

### 5. حذف دور

```http
DELETE /api/roles/{role_id}
```

**Response (200):**

```json
{
  "success": true,
  "message": "تم حذف الدور بنجاح"
}
```

**Errors:**

- `400` - لا يمكن حذف الأدوار الافتراضية
- `400` - الدور مستخدم من قبل مستخدمين

**Permissions:** Admin only

---

## 📦 APIs المنتجات

### 1. قائمة المنتجات

```http
GET /api/products?page=1&per_page=10&search=laptop&category_id=1&low_stock=true
```

**Query Parameters:**

| المعامل | النوع | الوصف |
|---------|------|-------|
| page | integer | رقم الصفحة |
| per_page | integer | عدد العناصر |
| search | string | البحث في الاسم/SKU/Barcode |
| category_id | integer | تصفية حسب الفئة |
| low_stock | boolean | المنتجات منخفضة المخزون |
| out_of_stock | boolean | المنتجات نافدة |

**Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "لابتوب HP",
      "sku": "LAP-HP-001",
      "barcode": "1234567890",
      "product_type": "storable",
      "cost_price": 2000.00,
      "sale_price": 2500.00,
      "current_stock": 10,
      "min_quantity": 5,
      "is_active": true
    }
  ],
  "pagination": { ... }
}
```

---

### 2. الحصول على منتج

```http
GET /api/products/{product_id}
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "لابتوب HP",
    "name_en": "HP Laptop",
    "sku": "LAP-HP-001",
    "barcode": "1234567890",
    "product_type": "storable",
    "tracking_type": "serial",
    "cost_price": 2000.00,
    "sale_price": 2500.00,
    "wholesale_price": 2300.00,
    "min_price": 2100.00,
    "current_stock": 10,
    "min_quantity": 5,
    "max_quantity": 100,
    "reorder_point": 8,
    "category_id": 1,
    "supplier_id": 1,
    "warehouse_id": 1,
    "is_active": true,
    "description": "لابتوب HP عالي الأداء",
    "specifications": "معالج i7، رام 16GB، SSD 512GB",
    "weight": 2.5,
    "dimensions": "35x25x2 cm",
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-10-08T10:00:00"
  }
}
```

---

## 🧾 APIs الفواتير

### 1. قائمة الفواتير

```http
GET /api/invoices?page=1&type=sales&status=confirmed&from_date=2025-01-01&to_date=2025-12-31
```

**Query Parameters:**

| المعامل | النوع | الوصف |
|---------|------|-------|
| page | integer | رقم الصفحة |
| per_page | integer | عدد العناصر |
| type | string | نوع الفاتورة (sales, purchase, sales_return, purchase_return) |
| status | string | حالة الفاتورة (draft, confirmed, paid, cancelled) |
| from_date | date | من تاريخ |
| to_date | date | إلى تاريخ |
| customer_id | integer | تصفية حسب العميل |
| supplier_id | integer | تصفية حسب المورد |

**Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "invoice_number": "INV-2025-001",
      "invoice_type": "sales",
      "invoice_status": "confirmed",
      "invoice_date": "2025-10-08",
      "customer_id": 1,
      "customer_name": "عميل 1",
      "subtotal": 1000.00,
      "tax_amount": 150.00,
      "discount_amount": 50.00,
      "total_amount": 1100.00,
      "paid_amount": 500.00,
      "remaining_amount": 600.00,
      "payment_status": "partial"
    }
  ],
  "pagination": { ... }
}
```

---

## 📊 ملخص الصلاحيات

| الصلاحية | الوصف | الأدوار |
|----------|-------|---------|
| `*` | جميع الصلاحيات | admin |
| `view_users` | عرض المستخدمين | admin, manager |
| `create_user` | إنشاء مستخدم | admin |
| `edit_user` | تعديل مستخدم | admin |
| `delete_user` | حذف مستخدم | admin |
| `view_products` | عرض المنتجات | admin, manager, user |
| `create_product` | إنشاء منتج | admin, manager |
| `edit_product` | تعديل منتج | admin, manager |
| `delete_product` | حذف منتج | admin |
| `view_invoices` | عرض الفواتير | admin, manager, user |
| `create_invoice` | إنشاء فاتورة | admin, manager |
| `edit_invoice` | تعديل فاتورة | admin, manager |
| `delete_invoice` | حذف فاتورة | admin |
| `view_reports` | عرض التقارير | admin, manager |

---

## 🔧 أمثلة استخدام

### مثال 1: تسجيل الدخول والحصول على المنتجات

```javascript
// 1. تسجيل الدخول
const loginResponse = await fetch('http://localhost:5002/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});

const { data } = await loginResponse.json();
const accessToken = data.access_token;

// 2. الحصول على المنتجات
const productsResponse = await fetch('http://localhost:5002/api/products', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const products = await productsResponse.json();
console.log(products);
```

---

## 📝 ملاحظات

1. **جميع التواريخ** بصيغة ISO 8601: `YYYY-MM-DDTHH:MM:SS`
2. **جميع الأسعار** بالريال السعودي (SAR)
3. **التصفح الافتراضي:** 10 عناصر في الصفحة
4. **الحد الأقصى للتصفح:** 100 عنصر في الصفحة
5. **معدل الطلبات:** 100 طلب في الدقيقة (قريباً)

---

**آخر تحديث:** 2025-10-08
**الإصدار:** 2.0.0
**الحالة:** ✅ قيد التطوير النشط

