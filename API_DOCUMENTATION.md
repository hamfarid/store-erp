# 📚 وثائق API - نظام إدارة المخزون

## API Documentation - Inventory Management System

## 🔗 معلومات عامة

- **Base URL**: `http://localhost:8000/api`
- **Content-Type**: `application/json`
- **Authentication**: Session-based
- **Language**: Arabic/English

## 🔐 المصادقة (Authentication)

### تسجيل الدخول

```http
POST /api/user/login
```

**Request Body:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "تم تسجيل الدخول بنجاح",
  "user": {
    "id": 1,
    "username": "admin",
    "full_name": "مدير النظام",
    "email": "admin@example.com",
    "role": "admin",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "token": "session-token"
}
```

**Response (Error):**

```json
{
  "success": false,
  "message": "اسم المستخدم أو كلمة المرور غير صحيحة"
}
```

### تسجيل الخروج

```http
POST /api/user/logout
```

**Response:**

```json
{
  "success": true,
  "message": "تم تسجيل الخروج بنجاح"
}
```

### الحصول على ملف المستخدم

```http
GET /api/user/profile
```

**Response:**

```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin",
    "full_name": "مدير النظام",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

## 📦 إدارة المنتجات (Products)

### الحصول على جميع المنتجات

```http
GET /api/products
```

**Query Parameters:**

- `page` (optional): رقم الصفحة (افتراضي: 1)
- `per_page` (optional): عدد العناصر في الصفحة (افتراضي: 20)
- `search` (optional): البحث في اسم المنتج
- `category_id` (optional): تصفية حسب الفئة

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "طماطم",
      "description": "طماطم طازجة",
      "sku": "TOM001",
      "barcode": "1234567890123",
      "category": {
        "id": 1,
        "name": "خضروات"
      },
      "group": {
        "id": 1,
        "name": "خضروات ورقية"
      },
      "rank": {
        "id": 1,
        "name": "درجة أولى"
      },
      "unit": "كيلو",
      "price": 15.50,
      "cost": 12.00,
      "stock_quantity": 100,
      "min_stock": 10,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 50,
    "pages": 3
  }
}
```

### إضافة منتج جديد

```http
POST /api/products
```

**Request Body:**

```json
{
  "name": "طماطم",
  "description": "طماطم طازجة",
  "sku": "TOM001",
  "barcode": "1234567890123",
  "category_id": 1,
  "group_id": 1,
  "rank_id": 1,
  "unit": "كيلو",
  "price": 15.50,
  "cost": 12.00,
  "min_stock": 10
}
```

### تحديث منتج

```http
PUT /api/products/{id}
```

### حذف منتج

```http
DELETE /api/products/{id}
```

## 🏷️ إدارة الفئات (Categories)

### الحصول على جميع الفئات

```http
GET /api/categories
```

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "خضروات",
      "description": "جميع أنواع الخضروات",
      "groups": [
        {
          "id": 1,
          "name": "خضروات ورقية",
          "ranks": [
            {
              "id": 1,
              "name": "درجة أولى"
            }
          ]
        }
      ]
    }
  ]
}
```

### إضافة فئة جديدة

```http
POST /api/categories
```

**Request Body:**

```json
{
  "name": "خضروات",
  "description": "جميع أنواع الخضروات"
}
```

## 👥 إدارة الشركاء (Partners)

### الحصول على جميع الشركاء

```http
GET /api/partners
```

**Query Parameters:**

- `type` (optional): نوع الشريك (customer, supplier)

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "شركة الأهرام",
      "type": "customer",
      "email": "info@ahram.com",
      "phone": "01234567890",
      "address": "القاهرة، مصر",
      "tax_number": "123456789",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### إضافة شريك جديد

```http
POST /api/partners
```

**Request Body:**

```json
{
  "name": "شركة الأهرام",
  "type": "customer",
  "email": "info@ahram.com",
  "phone": "01234567890",
  "address": "القاهرة، مصر",
  "tax_number": "123456789"
}
```

## 📊 حركات المخزون (Stock Movements)

### الحصول على حركات المخزون

```http
GET /api/stock-movements
```

**Query Parameters:**

- `product_id` (optional): تصفية حسب المنتج
- `movement_type` (optional): نوع الحركة (in, out, adjustment)
- `start_date` (optional): تاريخ البداية
- `end_date` (optional): تاريخ النهاية

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "طماطم"
      },
      "movement_type": "in",
      "quantity": 50,
      "unit_cost": 12.00,
      "total_cost": 600.00,
      "reference": "PO-001",
      "notes": "شراء من المورد",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### إضافة حركة مخزون

```http
POST /api/stock-movements
```

**Request Body:**

```json
{
  "product_id": 1,
  "movement_type": "in",
  "quantity": 50,
  "unit_cost": 12.00,
  "reference": "PO-001",
  "notes": "شراء من المورد"
}
```

## 📈 التقارير والإحصائيات (Reports & Statistics)

### إحصائيات عامة

```http
GET /api/stats/overview
```

**Response:**

```json
{
  "success": true,
  "data": {
    "products": {
      "total": 150,
      "low_stock": 5
    },
    "partners": {
      "customers": 25,
      "suppliers": 10
    },
    "movements": {
      "today": 15,
      "this_month": 450
    },
    "value": {
      "total_inventory": 125000.00,
      "monthly_sales": 85000.00
    }
  }
}
```

### المنتجات منخفضة المخزون

```http
GET /api/stats/low-stock
```

### الأنشطة الحديثة

```http
GET /api/stats/recent-activities
```

## 🔍 البحث (Search)

### البحث العام

```http
GET /api/search
```

**Query Parameters:**

- `q`: نص البحث
- `type` (optional): نوع البحث (products, partners, movements)

## ⚡ فحص الحالة (Health Check)

### فحص حالة الخادم

```http
GET /api/health
```

**Response:**

```json
{
  "status": "healthy",
  "message": "Server is running",
  "database": "connected",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🚨 رموز الأخطاء (Error Codes)

| Code | Message | Description |
|------|---------|-------------|
| 200 | Success | العملية تمت بنجاح |
| 400 | Bad Request | طلب غير صحيح |
| 401 | Unauthorized | غير مصرح |
| 403 | Forbidden | ممنوع |
| 404 | Not Found | غير موجود |
| 500 | Internal Server Error | خطأ في الخادم |

## 📝 ملاحظات مهمة

1. **المصادقة**: جميع endpoints تتطلب مصادقة عدا `/health` و `/user/login`
2. **التواريخ**: جميع التواريخ بصيغة ISO 8601
3. **الأرقام**: الأسعار والكميات بصيغة decimal
4. **الترقيم**: جميع الـ IDs أرقام صحيحة موجبة
5. **اللغة**: النظام يدعم العربية والإنجليزية

---

**هذه الوثائق تغطي جميع endpoints المتاحة في النظام** 📋
