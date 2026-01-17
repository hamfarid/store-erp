# 📚 API Reference - Store ERP v2.0.0

**Version:** 2.0.0  
**Base URL:** `http://localhost:6001/api`  
**Authentication:** JWT Bearer Token

---

## 🔐 Authentication

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@store.com",
    "role": "admin"
  }
}
```

### Refresh Token
```http
POST /api/auth/refresh
Content-Type: application/json
Authorization: Bearer {refresh_token}
```

### Logout
```http
POST /api/auth/logout
Authorization: Bearer {access_token}
```

### Get Current User
```http
GET /api/auth/me
Authorization: Bearer {access_token}
```

---

## 📦 Products

### List Products
```http
GET /api/products
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20) |
| search | string | Search by name/SKU |
| category_id | int | Filter by category |
| status | string | Filter by status |

### Get Product
```http
GET /api/products/{id}
Authorization: Bearer {token}
```

### Create Product
```http
POST /api/products
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "منتج جديد",
  "sku": "PROD-001",
  "barcode": "1234567890123",
  "category_id": 1,
  "unit": "قطعة",
  "purchase_price": 50.00,
  "selling_price": 75.00,
  "min_stock": 10,
  "description": "وصف المنتج"
}
```

### Update Product
```http
PUT /api/products/{id}
Authorization: Bearer {token}
Content-Type: application/json
```

### Delete Product
```http
DELETE /api/products/{id}
Authorization: Bearer {token}
```

---

## 📂 Categories

### List Categories
```http
GET /api/categories
Authorization: Bearer {token}
```

### Create Category
```http
POST /api/categories
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "بذور",
  "description": "فئة البذور الزراعية",
  "parent_id": null
}
```

### Update Category
```http
PUT /api/categories/{id}
Authorization: Bearer {token}
```

### Delete Category
```http
DELETE /api/categories/{id}
Authorization: Bearer {token}
```

---

## 📦 Lots (Batches)

### List Lots
```http
GET /api/lots
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| product_id | int | Filter by product |
| status | string | available, reserved, sold, expired |
| expiring_days | int | Lots expiring within X days |

### Get Lot
```http
GET /api/lots/{id}
Authorization: Bearer {token}
```

### Create Lot
```http
POST /api/lots
Authorization: Bearer {token}
Content-Type: application/json

{
  "lot_number": "LOT-2026-001",
  "product_id": 1,
  "quantity": 100,
  "unit_cost": 50.00,
  "expiry_date": "2027-12-31",
  "supplier_id": 1,
  "warehouse_id": 1,
  "quality_data": {
    "germination_rate": 95,
    "purity_percentage": 98,
    "moisture_percentage": 10
  }
}
```

### Update Lot
```http
PUT /api/lots/{id}
Authorization: Bearer {token}
```

### Update Lot Status
```http
PATCH /api/lots/{id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "reserved",
  "reason": "محجوز لطلب #123"
}
```

### Get Expiring Lots
```http
GET /api/lots/expiring
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| days | int | Days until expiry (default: 30) |

---

## 🛒 POS (Point of Sale)

### Create Sale
```http
POST /api/pos/sale
Authorization: Bearer {token}
Content-Type: application/json

{
  "customer_id": 1,
  "payment_method": "cash",
  "items": [
    {
      "product_id": 1,
      "lot_id": 1,
      "quantity": 5,
      "unit_price": 75.00,
      "discount": 0
    }
  ],
  "discount": 0,
  "tax": 15,
  "notes": "ملاحظات"
}
```

**Response:**
```json
{
  "id": 123,
  "invoice_number": "INV-2026-001",
  "total": 431.25,
  "subtotal": 375.00,
  "tax_amount": 56.25,
  "status": "completed",
  "created_at": "2026-01-16T12:00:00Z"
}
```

### Get Open Shift
```http
GET /api/pos/shift/current
Authorization: Bearer {token}
```

### Open Shift
```http
POST /api/pos/shift/open
Authorization: Bearer {token}
Content-Type: application/json

{
  "opening_cash": 500.00
}
```

### Close Shift
```http
POST /api/pos/shift/close
Authorization: Bearer {token}
Content-Type: application/json

{
  "closing_cash": 1500.00,
  "notes": "ملاحظات الإغلاق"
}
```

### Process Return
```http
POST /api/pos/return
Authorization: Bearer {token}
Content-Type: application/json

{
  "invoice_id": 123,
  "items": [
    {
      "invoice_item_id": 1,
      "quantity": 2,
      "reason": "منتج تالف"
    }
  ]
}
```

---

## 🧾 Invoices

### List Invoices
```http
GET /api/invoices
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | sale, purchase, return |
| status | string | pending, completed, cancelled |
| from_date | date | Filter from date |
| to_date | date | Filter to date |
| customer_id | int | Filter by customer |

### Get Invoice
```http
GET /api/invoices/{id}
Authorization: Bearer {token}
```

### Print Invoice
```http
GET /api/invoices/{id}/print
Authorization: Bearer {token}
Accept: application/pdf
```

---

## 📊 Reports

### Sales Report
```http
GET /api/reports/sales
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| from_date | date | Start date |
| to_date | date | End date |
| group_by | string | day, week, month, year |

### Inventory Report
```http
GET /api/reports/inventory
Authorization: Bearer {token}
```

### Profit/Loss Report
```http
GET /api/reports/profit-loss
Authorization: Bearer {token}
```

### Lot Expiry Report
```http
GET /api/reports/lot-expiry
Authorization: Bearer {token}
```

### Export Report
```http
GET /api/reports/{type}/export
Authorization: Bearer {token}
Accept: application/pdf | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | text/csv
```

---

## 👥 Customers

### List Customers
```http
GET /api/customers
Authorization: Bearer {token}
```

### Create Customer
```http
POST /api/customers
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "عميل جديد",
  "phone": "0501234567",
  "email": "customer@example.com",
  "address": "الرياض، السعودية",
  "tax_number": "300123456789012",
  "credit_limit": 10000.00
}
```

### Get Customer Balance
```http
GET /api/customers/{id}/balance
Authorization: Bearer {token}
```

---

## 🏢 Suppliers

### List Suppliers
```http
GET /api/suppliers
Authorization: Bearer {token}
```

### Create Supplier
```http
POST /api/suppliers
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "مورد جديد",
  "phone": "0501234567",
  "email": "supplier@example.com",
  "address": "جدة، السعودية",
  "tax_number": "300123456789012",
  "payment_terms": 30
}
```

---

## 👤 Users & Roles

### List Users
```http
GET /api/users
Authorization: Bearer {token}
```

### Create User
```http
POST /api/users
Authorization: Bearer {token}
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "SecurePass123!",
  "role_id": 2,
  "full_name": "مستخدم جديد"
}
```

### List Roles
```http
GET /api/roles
Authorization: Bearer {token}
```

### Get Role Permissions
```http
GET /api/roles/{id}/permissions
Authorization: Bearer {token}
```

---

## ⚙️ Settings

### Get Settings
```http
GET /api/settings
Authorization: Bearer {token}
```

### Update Settings
```http
PUT /api/settings
Authorization: Bearer {token}
Content-Type: application/json

{
  "company_name": "شركة المتجر",
  "tax_rate": 15,
  "currency": "EGP",
  "timezone": "Asia/Riyadh"
}
```

### Create Backup
```http
POST /api/settings/backup
Authorization: Bearer {token}
```

### Restore Backup
```http
POST /api/settings/restore
Authorization: Bearer {token}
Content-Type: multipart/form-data

backup_file: [file]
```

---

## 🔔 Error Responses

### Standard Error Format
```json
{
  "error": true,
  "message": "Error description",
  "code": "ERROR_CODE",
  "details": {}
}
```

### HTTP Status Codes
| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Server Error |

---

## 🔒 Rate Limiting

| Endpoint | Limit |
|----------|-------|
| `/api/auth/login` | 5 requests/minute |
| `/api/*` | 100 requests/second |

---

## 📝 Pagination Response

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

*API Reference - Store ERP v2.0.0*
