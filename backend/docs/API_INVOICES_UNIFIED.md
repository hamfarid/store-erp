# 📄 توثيق API الفواتير الموحدة

# Unified Invoices API Documentation

## 📋 نظرة عامة | Overview

هذا التوثيق يغطي جميع مسارات API الخاصة بالفواتير الموحدة (المبيعات، المشتريات، المرتجعات، والدفعات).

**الإصدار:** v2.0  
**المسار الأساسي:** `/api/invoices`  
**المصادقة:** مطلوبة (JWT Token)

---

## 🔐 المصادقة | Authentication

جميع المسارات تتطلب JWT Token في الرأس:

```http
Authorization: Bearer <your_jwt_token>
```

---

## 📊 المسارات المتاحة | Available Endpoints

### 1. قائمة الفواتير | List Invoices

**GET** `/api/invoices`

الحصول على قائمة الفواتير مع إمكانية التصفية والبحث.

#### معاملات الاستعلام | Query Parameters

| المعامل | النوع | الوصف | مثال |
|---------|------|-------|------|
| `page` | integer | رقم الصفحة (افتراضي: 1) | `?page=2` |
| `per_page` | integer | عدد العناصر في الصفحة (افتراضي: 20) | `?per_page=50` |
| `search` | string | البحث في رقم الفاتورة | `?search=SAL-000001` |
| `invoice_type` | string | نوع الفاتورة | `?invoice_type=sales` |
| `status` | string | حالة الفاتورة | `?status=paid` |
| `customer_id` | integer | معرف العميل | `?customer_id=5` |
| `supplier_id` | integer | معرف المورد | `?supplier_id=3` |
| `date_from` | string | من تاريخ (YYYY-MM-DD) | `?date_from=2025-01-01` |
| `date_to` | string | إلى تاريخ (YYYY-MM-DD) | `?date_to=2025-12-31` |
| `sort_by` | string | الترتيب حسب | `?sort_by=invoice_date` |
| `order` | string | اتجاه الترتيب (asc/desc) | `?order=desc` |

#### أنواع الفواتير | Invoice Types

- `sales` - فاتورة مبيعات
- `purchase` - فاتورة مشتريات
- `sales_return` - مرتجع مبيعات
- `purchase_return` - مرتجع مشتريات

#### حالات الفاتورة | Invoice Status

- `draft` - مسودة
- `confirmed` - مؤكدة
- `paid` - مدفوعة
- `partial` - مدفوعة جزئياً
- `cancelled` - ملغاة
- `overdue` - متأخرة

#### مثال الطلب | Request Example

```http
GET /api/invoices?page=1&per_page=20&invoice_type=sales&status=paid
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### مثال الاستجابة | Response Example

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "invoice_number": "SAL-000001",
      "invoice_type": "sales",
      "invoice_date": "2025-10-08",
      "due_date": "2025-10-22",
      "customer_id": 5,
      "customer_name": "أحمد محمد",
      "subtotal": 1000.00,
      "tax_amount": 150.00,
      "discount_amount": 50.00,
      "total_amount": 1100.00,
      "paid_amount": 1100.00,
      "remaining_amount": 0.00,
      "status": "paid",
      "payment_status": "paid",
      "notes": "فاتورة مبيعات",
      "created_at": "2025-10-08T10:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

### 2. الحصول على فاتورة محددة | Get Invoice

**GET** `/api/invoices/{invoice_id}`

الحصول على تفاصيل فاتورة محددة مع العناصر والدفعات.

#### مثال الطلب | Request Example

```http
GET /api/invoices/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### مثال الاستجابة | Response Example

```json
{
  "success": true,
  "data": {
    "id": 1,
    "invoice_number": "SAL-000001",
    "invoice_type": "sales",
    "invoice_date": "2025-10-08",
    "due_date": "2025-10-22",
    "customer": {
      "id": 5,
      "name": "أحمد محمد",
      "email": "ahmed@example.com",
      "phone": "0501234567"
    },
    "warehouse": {
      "id": 1,
      "name": "المستودع الرئيسي"
    },
    "subtotal": 1000.00,
    "tax_amount": 150.00,
    "tax_rate": 15.00,
    "discount_amount": 50.00,
    "discount_type": "fixed",
    "discount_value": 50.00,
    "shipping_cost": 0.00,
    "total_amount": 1100.00,
    "paid_amount": 1100.00,
    "remaining_amount": 0.00,
    "status": "paid",
    "payment_status": "paid",
    "notes": "فاتورة مبيعات",
    "items": [
      {
        "id": 1,
        "product_id": 10,
        "product": {
          "id": 10,
          "name": "منتج تجريبي",
          "sku": "PROD-001"
        },
        "quantity": 10,
        "price": 100.00,
        "discount": 0.00,
        "tax": 15.00,
        "total": 1015.00
      }
    ],
    "payments": [
      {
        "id": 1,
        "amount": 1100.00,
        "payment_date": "2025-10-08",
        "payment_method": "cash",
        "reference": "PAY-001",
        "notes": "دفعة كاملة"
      }
    ]
  }
}
```

---

### 3. إنشاء فاتورة | Create Invoice

**POST** `/api/invoices`

إنشاء فاتورة جديدة.

#### البيانات المطلوبة | Request Body

```json
{
  "invoice_type": "sales",
  "invoice_date": "2025-10-08",
  "due_date": "2025-10-22",
  "customer_id": 5,
  "warehouse_id": 1,
  "items": [
    {
      "product_id": 10,
      "quantity": 10,
      "price": 100.00,
      "discount": 0.00,
      "tax": 15.00
    }
  ],
  "tax_rate": 15.00,
  "discount_type": "fixed",
  "discount_value": 50.00,
  "shipping_cost": 0.00,
  "notes": "فاتورة مبيعات"
}
```

#### الحقول المطلوبة | Required Fields

- `invoice_type` - نوع الفاتورة
- `items` - قائمة العناصر (عنصر واحد على الأقل)
- `customer_id` - للمبيعات والمرتجعات
- `supplier_id` - للمشتريات ومرتجعات المشتريات

#### مثال الاستجابة | Response Example

```json
{
  "success": true,
  "message": "تم إنشاء الفاتورة بنجاح",
  "data": {
    "id": 1,
    "invoice_number": "SAL-000001"
  }
}
```

---

### 4. تحديث فاتورة | Update Invoice

**PUT** `/api/invoices/{invoice_id}`

تحديث بيانات فاتورة (المسودات والمؤكدة فقط).

#### البيانات | Request Body

```json
{
  "invoice_date": "2025-10-09",
  "due_date": "2025-10-23",
  "notes": "ملاحظات محدثة",
  "status": "confirmed"
}
```

#### مثال الاستجابة | Response Example

```json
{
  "success": true,
  "message": "تم تحديث الفاتورة بنجاح"
}
```

---

### 5. حذف فاتورة | Delete Invoice

**DELETE** `/api/invoices/{invoice_id}`

حذف فاتورة (مدير فقط - لا يمكن حذف الفواتير المدفوعة).

#### مثال الطلب | Request Example

```http
DELETE /api/invoices/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### مثال الاستجابة | Response Example

```json
{
  "success": true,
  "message": "تم حذف الفاتورة بنجاح"
}
```

---

### 6. إحصائيات الفواتير | Invoices Statistics

**GET** `/api/invoices/stats`

الحصول على إحصائيات شاملة للفواتير.

#### مثال الاستجابة | Response Example

```json
{
  "success": true,
  "data": {
    "total_invoices": 150,
    "by_type": {
      "sales": 80,
      "purchase": 70
    },
    "by_status": {
      "draft": 10,
      "confirmed": 20,
      "paid": 120
    },
    "amounts": {
      "total_sales": 500000.00,
      "total_purchases": 300000.00,
      "total_paid": 450000.00,
      "total_remaining": 50000.00
    }
  }
}
```

---

### 7. البحث السريع | Quick Search

**GET** `/api/invoices/search?q={query}&limit={limit}`

البحث السريع في الفواتير.

#### مثال الطلب | Request Example

```http
GET /api/invoices/search?q=SAL-000001&limit=10
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### 8. تصدير الفواتير | Export Invoices

**GET** `/api/invoices/export`

تصدير جميع الفواتير.

---

### 9. إضافة دفعة | Add Payment

**POST** `/api/invoices/{invoice_id}/payments`

إضافة دفعة للفاتورة.

#### البيانات المطلوبة | Request Body

```json
{
  "amount": 500.00,
  "payment_date": "2025-10-08",
  "payment_method": "cash",
  "reference": "PAY-001",
  "notes": "دفعة جزئية"
}
```

---

### 10. تأكيد فاتورة | Confirm Invoice

**POST** `/api/invoices/{invoice_id}/confirm`

تأكيد فاتورة (المسودات فقط).

---

### 11. إلغاء فاتورة | Cancel Invoice

**POST** `/api/invoices/{invoice_id}/cancel`

إلغاء فاتورة (مدير فقط - لا يمكن إلغاء الفواتير المدفوعة).

---

## 📝 ملاحظات | Notes

1. **المصادقة:** جميع المسارات تتطلب JWT Token
2. **الصلاحيات:** بعض المسارات تتطلب صلاحيات مدير (حذف، إلغاء)
3. **التحقق:** يتم التحقق من صحة البيانات قبل الحفظ
4. **الأخطاء:** يتم إرجاع رسائل خطأ واضحة مع أكواد HTTP مناسبة

---

## 🔢 أكواد الحالة | Status Codes

- `200` - نجح الطلب
- `201` - تم الإنشاء بنجاح
- `400` - خطأ في البيانات المرسلة
- `401` - غير مصرح (يتطلب مصادقة)
- `403` - ممنوع (يتطلب صلاحيات)
- `404` - غير موجود
- `500` - خطأ في الخادم
- `501` - غير مطبق (النموذج غير متاح)

---

**آخر تحديث:** 2025-10-08  
**الإصدار:** v2.0
