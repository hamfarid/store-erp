# مسارات العملاء والموردين الموحدة

# Unified Customers & Suppliers API Routes

## نظرة عامة | Overview

هذا الملف يوثق جميع مسارات API الخاصة بالعملاء والموردين في النظام الموحد.

This file documents all API routes for customers and suppliers in the unified system.

---

## 🔐 المصادقة | Authentication

جميع المسارات تتطلب مصادقة باستخدام JWT Token في الـ Header:

All routes require JWT authentication in the header:

```
Authorization: Bearer <token>
```

---

## 📋 مسارات العملاء | Customer Routes

### 1. الحصول على قائمة العملاء | Get Customers List

**Endpoint:** `GET /api/customers`

**Parameters:**

- `page` (optional): رقم الصفحة (default: 1)
- `per_page` (optional): عدد العناصر في الصفحة (default: 20)
- `search` (optional): نص البحث

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "اسم العميل",
      "email": "customer@example.com",
      "phone": "123456789",
      "is_active": true,
      ...
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

---

### 2. الحصول على عميل محدد | Get Single Customer

**Endpoint:** `GET /api/customers/<customer_id>`

**Response:**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "اسم العميل",
    "email": "customer@example.com",
    "phone": "123456789",
    "is_active": true,
    ...
  }
}
```

---

### 3. إنشاء عميل جديد | Create Customer

**Endpoint:** `POST /api/customers`

**Request Body:**

```json
{
  "name": "اسم العميل",
  "email": "customer@example.com",
  "phone": "123456789",
  "mobile": "987654321",
  "address": "العنوان",
  "city": "المدينة",
  "country": "البلد",
  "postal_code": "12345",
  "company_name": "اسم الشركة",
  "tax_number": "123456",
  "credit_limit": 10000.00,
  "payment_terms": "net_30",
  "currency": "EGP",
  "discount_rate": 5.0,
  "category": "RETAIL",
  "notes": "ملاحظات",
  "tags": ["vip", "regular"],
  "is_active": true
}
```

**Response:**

```json
{
  "success": true,
  "data": { ... },
  "message": "تم إنشاء العميل بنجاح"
}
```

---

### 4. تحديث عميل | Update Customer

**Endpoint:** `PUT /api/customers/<customer_id>`

**Request Body:** (نفس حقول الإنشاء)

**Response:**

```json
{
  "success": true,
  "data": { ... },
  "message": "تم تحديث العميل بنجاح"
}
```

---

### 5. حذف عميل | Delete Customer

**Endpoint:** `DELETE /api/customers/<customer_id>`

**Permissions:** Admin only

**Response:**

```json
{
  "success": true,
  "message": "تم حذف العميل بنجاح"
}
```

---

### 6. إحصائيات العملاء | Customer Statistics

**Endpoint:** `GET /api/customers/stats`

**Response:**

```json
{
  "success": true,
  "data": {
    "total_customers": 100,
    "active_customers": 85,
    "inactive_customers": 15,
    "by_category": {
      "RETAIL": 50,
      "WHOLESALE": 30,
      "DISTRIBUTOR": 20
    }
  }
}
```

---

### 7. البحث السريع في العملاء | Quick Search Customers

**Endpoint:** `GET /api/customers/search`

**Parameters:**

- `q` (required): نص البحث
- `limit` (optional): عدد النتائج (default: 10)

**Response:**

```json
{
  "success": true,
  "data": [ ... ],
  "total": 5
}
```

---

### 8. تصدير العملاء | Export Customers

**Endpoint:** `GET /api/customers/export`

**Parameters:**

- `format` (optional): صيغة التصدير (json, csv) (default: json)

**Response:**

```json
{
  "success": true,
  "data": [ ... ],
  "total": 100,
  "format": "json"
}
```

---

## 🏭 مسارات الموردين | Supplier Routes

### 1. الحصول على قائمة الموردين | Get Suppliers List

**Endpoint:** `GET /api/suppliers`

**Parameters:**

- `page` (optional): رقم الصفحة (default: 1)
- `per_page` (optional): عدد العناصر في الصفحة (default: 20)
- `search` (optional): نص البحث

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "اسم المورد",
      "email": "supplier@example.com",
      "phone": "123456789",
      "is_active": true,
      ...
    }
  ],
  "pagination": { ... }
}
```

---

### 2. الحصول على مورد محدد | Get Single Supplier

**Endpoint:** `GET /api/suppliers/<supplier_id>`

**Response:**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "اسم المورد",
    "email": "supplier@example.com",
    "phone": "123456789",
    "is_active": true,
    ...
  }
}
```

---

### 3. إنشاء مورد جديد | Create Supplier

**Endpoint:** `POST /api/suppliers`

**Request Body:**

```json
{
  "name": "اسم المورد",
  "company_type": "manufacturer",
  "email": "supplier@example.com",
  "phone": "123456789",
  "mobile": "987654321",
  "website": "https://example.com",
  "address": "العنوان",
  "tax_number": "123456",
  "payment_terms": "net_30",
  "preferred_payment_method": "bank_transfer",
  "currency": "EGP",
  "language": "ar",
  "notes": "ملاحظات",
  "is_active": true
}
```

**Response:**

```json
{
  "success": true,
  "data": { ... },
  "message": "تم إنشاء المورد بنجاح"
}
```

---

### 4. تحديث مورد | Update Supplier

**Endpoint:** `PUT /api/suppliers/<supplier_id>`

**Request Body:** (نفس حقول الإنشاء)

**Response:**

```json
{
  "success": true,
  "data": { ... },
  "message": "تم تحديث المورد بنجاح"
}
```

---

### 5. حذف مورد | Delete Supplier

**Endpoint:** `DELETE /api/suppliers/<supplier_id>`

**Permissions:** Admin only

**Response:**

```json
{
  "success": true,
  "message": "تم حذف المورد بنجاح"
}
```

---

### 6. إحصائيات الموردين | Supplier Statistics

**Endpoint:** `GET /api/suppliers/stats`

**Response:**

```json
{
  "success": true,
  "data": {
    "total_suppliers": 50,
    "active_suppliers": 45,
    "inactive_suppliers": 5
  }
}
```

---

### 7. البحث السريع في الموردين | Quick Search Suppliers

**Endpoint:** `GET /api/suppliers/search`

**Parameters:**

- `q` (required): نص البحث
- `limit` (optional): عدد النتائج (default: 10)

**Response:**

```json
{
  "success": true,
  "data": [ ... ],
  "total": 5
}
```

---

### 8. تصدير الموردين | Export Suppliers

**Endpoint:** `GET /api/suppliers/export`

**Parameters:**

- `format` (optional): صيغة التصدير (json, csv) (default: json)

**Response:**

```json
{
  "success": true,
  "data": [ ... ],
  "total": 50,
  "format": "json"
}
```

---

## ⚠️ رموز الأخطاء | Error Codes

- `200`: نجح الطلب | Success
- `201`: تم الإنشاء بنجاح | Created
- `400`: طلب غير صحيح | Bad Request
- `401`: غير مصرح | Unauthorized
- `404`: غير موجود | Not Found
- `500`: خطأ في الخادم | Server Error
- `501`: غير مدعوم | Not Implemented

---

## 📝 ملاحظات | Notes

1. جميع المسارات تتطلب مصادقة JWT
2. المسارات التي تحتوي على `DELETE` تتطلب صلاحيات المدير
3. البحث يدعم البحث في الاسم، البريد الإلكتروني، والهاتف
4. التصدير بصيغة CSV غير مدعوم حالياً
5. جميع التواريخ بصيغة ISO 8601

---

## 🔄 التحديثات المستقبلية | Future Updates

- [ ] دعم تصدير CSV
- [ ] دعم الاستيراد من ملفات Excel
- [ ] إضافة مسارات للتقارير المتقدمة
- [ ] دعم الفلترة المتقدمة
- [ ] إضافة مسارات للمرفقات

---

**آخر تحديث:** 2025-10-08
**الإصدار:** 2.0
