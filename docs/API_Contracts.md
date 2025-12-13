# API Contracts

**Store Management System - API Reference**  
**Version:** 1.0  
**Base URL:** `https://api.store.example.com/api`  
**Last Updated:** 2025-12-01

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Response Format](#response-format)
4. [Error Codes](#error-codes)
5. [Endpoints](#endpoints)
   - [Auth](#auth-endpoints)
   - [Users](#user-endpoints)
   - [Products](#product-endpoints)
   - [Inventory](#inventory-endpoints)
   - [Customers](#customer-endpoints)
   - [Suppliers](#supplier-endpoints)
   - [Invoices](#invoice-endpoints)
   - [Reports](#report-endpoints)

---

## Overview

### API Design Principles

- **RESTful:** Resource-oriented URLs
- **JSON:** All request/response bodies use JSON
- **UTF-8:** All text encoded in UTF-8
- **Bilingual:** Supports Arabic and English messages

### Rate Limits

| Endpoint Type | Limit | Window |
|---------------|-------|--------|
| Authentication | 5 requests | per minute |
| Read operations | 100 requests | per minute |
| Write operations | 30 requests | per minute |
| Bulk operations | 5 requests | per minute |

### Headers

**Required Headers:**
```
Content-Type: application/json
Accept: application/json
Authorization: Bearer <access_token>
```

**Optional Headers:**
```
Accept-Language: ar|en
X-Request-ID: <uuid>
X-CSRF-Token: <token>
```

---

## Authentication

### JWT Token Flow

1. Login with username/password → Receive access + refresh tokens
2. Use access token for API requests (15 min expiry)
3. Use refresh token to get new access token (7 day expiry)
4. Logout revokes refresh token

### Token Refresh

```
POST /api/auth/refresh
Authorization: Bearer <refresh_token>

Response:
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "expires_in": 900
  }
}
```

---

## Response Format

### Success Response

```json
{
  "success": true,
  "status": "success",
  "data": { ... },
  "message": "Operation completed successfully",
  "meta": {
    "pagination": {
      "total": 100,
      "page": 1,
      "per_page": 10,
      "pages": 10
    }
  },
  "request_id": "abc123",
  "timestamp": "2025-12-01T12:00:00Z"
}
```

### Error Response

```json
{
  "success": false,
  "status": "error",
  "error": {
    "code": "VAL_INVALID_FORMAT",
    "message": "Validation failed",
    "details": {
      "email": ["Invalid email format"]
    }
  },
  "request_id": "abc123",
  "timestamp": "2025-12-01T12:00:00Z"
}
```

---

## Error Codes

### Authentication Errors (AUTH_*)

| Code | HTTP | Description |
|------|------|-------------|
| AUTH_INVALID_CREDENTIALS | 401 | Invalid username/password |
| AUTH_INVALID_TOKEN | 401 | Token malformed or invalid |
| AUTH_TOKEN_EXPIRED | 401 | Token has expired |
| AUTH_TOKEN_REVOKED | 401 | Token was revoked |
| AUTH_UNAUTHORIZED | 403 | No permission for action |
| AUTH_ACCOUNT_LOCKED | 403 | Account temporarily locked |

### Validation Errors (VAL_*)

| Code | HTTP | Description |
|------|------|-------------|
| VAL_INVALID_FORMAT | 400 | Invalid data format |
| VAL_MISSING_FIELD | 400 | Required field missing |
| VAL_DUPLICATE_VALUE | 409 | Value already exists |
| VAL_OUT_OF_RANGE | 400 | Value outside allowed range |

### Resource Errors (RES_*)

| Code | HTTP | Description |
|------|------|-------------|
| RES_NOT_FOUND | 404 | Resource not found |
| RES_ALREADY_EXISTS | 409 | Resource already exists |
| RES_IN_USE | 409 | Resource is being used |

### System Errors (SYS_*)

| Code | HTTP | Description |
|------|------|-------------|
| SYS_INTERNAL_ERROR | 500 | Internal server error |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |

---

## Endpoints

### Auth Endpoints

#### Login

```
POST /api/auth/login

Request:
{
  "username": "admin",
  "password": "SecurePass123!"
}

Response (200):
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "is_active": true
    },
    "expires_in": 900
  },
  "message": "تم تسجيل الدخول بنجاح"
}
```

#### Refresh Token

```
POST /api/auth/refresh
Authorization: Bearer <refresh_token>

Response (200):
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "expires_in": 900
  }
}
```

#### Logout

```
POST /api/auth/logout
Authorization: Bearer <access_token>

Response (200):
{
  "success": true,
  "message": "تم تسجيل الخروج بنجاح"
}
```

---

### User Endpoints

#### List Users

```
GET /api/users?page=1&per_page=10&search=ahmed&role=admin
Authorization: Bearer <token>
Permission: user_management_view

Response (200):
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "username": "ahmed_ali",
        "email": "ahmed@example.com",
        "full_name": "أحمد علي",
        "role": "admin",
        "is_active": true,
        "last_login": "2025-12-01T10:00:00Z",
        "created_at": "2025-01-01T00:00:00Z"
      }
    ],
    "total": 50,
    "page": 1,
    "per_page": 10,
    "pages": 5
  }
}
```

#### Create User

```
POST /api/users
Authorization: Bearer <token>
Permission: user_management_add

Request:
{
  "username": "new_user",
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "محمد أحمد",
  "role_id": 2,
  "is_active": true
}

Response (201):
{
  "success": true,
  "data": {
    "id": 5,
    "username": "new_user",
    "email": "user@example.com",
    "full_name": "محمد أحمد",
    "role": "user",
    "is_active": true,
    "created_at": "2025-12-01T12:00:00Z"
  },
  "message": "تم إنشاء المستخدم بنجاح"
}
```

#### Get User

```
GET /api/users/{id}
Authorization: Bearer <token>
Permission: user_management_view

Response (200):
{
  "success": true,
  "data": {
    "id": 1,
    "username": "ahmed_ali",
    "email": "ahmed@example.com",
    "full_name": "أحمد علي",
    "role": "admin",
    "role_id": 1,
    "is_active": true,
    "last_login": "2025-12-01T10:00:00Z",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-12-01T10:00:00Z"
  }
}
```

#### Update User

```
PUT /api/users/{id}
Authorization: Bearer <token>
Permission: user_management_edit

Request:
{
  "email": "updated@example.com",
  "full_name": "أحمد محمد",
  "role_id": 2,
  "is_active": true
}

Response (200):
{
  "success": true,
  "data": { ... },
  "message": "تم تحديث المستخدم بنجاح"
}
```

#### Delete User

```
DELETE /api/users/{id}
Authorization: Bearer <token>
Permission: user_management_delete

Response (200):
{
  "success": true,
  "message": "تم حذف المستخدم بنجاح"
}
```

---

### Product Endpoints

#### List Products

```
GET /api/products?page=1&per_page=20&search=laptop&category_id=5
Authorization: Bearer <token>
Permission: products_view

Response (200):
{
  "success": true,
  "data": {
    "products": [
      {
        "id": 1,
        "name": "لابتوب HP",
        "name_en": "HP Laptop",
        "sku": "HP-LAP-001",
        "barcode": "1234567890123",
        "category": {
          "id": 5,
          "name": "إلكترونيات"
        },
        "brand": {
          "id": 2,
          "name": "HP"
        },
        "cost_price": 3000.00,
        "sell_price": 3500.00,
        "stock_quantity": 50,
        "is_active": true
      }
    ],
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

#### Create Product

```
POST /api/products
Authorization: Bearer <token>
Permission: products_add

Request:
{
  "name": "منتج جديد",
  "name_en": "New Product",
  "sku": "SKU-001",
  "barcode": "1234567890123",
  "category_id": 5,
  "brand_id": 2,
  "unit": "piece",
  "cost_price": 100.00,
  "sell_price": 150.00,
  "min_stock": 10,
  "tax_rate": 15,
  "description": "وصف المنتج"
}

Response (201):
{
  "success": true,
  "data": { ... },
  "message": "تم إنشاء المنتج بنجاح"
}
```

---

### Customer Endpoints

#### List Customers

```
GET /api/customers?page=1&per_page=10&search=شركة
Authorization: Bearer <token>
Permission: partners_view

Response (200):
{
  "success": true,
  "data": {
    "customers": [
      {
        "id": 1,
        "name": "شركة الأمل للتجارة",
        "code": "CUST-001",
        "email": "info@alamal.com",
        "phone": "+966501234567",
        "city": "الرياض",
        "country": "المملكة العربية السعودية",
        "tax_number": "300123456789012",
        "credit_limit": 50000.00,
        "balance": 15000.00,
        "is_active": true
      }
    ],
    "total": 50,
    "page": 1,
    "per_page": 10
  }
}
```

#### Create Customer

```
POST /api/customers
Authorization: Bearer <token>
Permission: partners_add

Request:
{
  "name": "عميل جديد",
  "email": "customer@example.com",
  "phone": "+966501234567",
  "address": "الرياض، حي النخيل",
  "city": "الرياض",
  "country": "المملكة العربية السعودية",
  "tax_number": "300123456789012",
  "credit_limit": 10000.00
}

Response (201):
{
  "success": true,
  "data": { ... },
  "message": "تم إنشاء العميل بنجاح"
}
```

---

### Invoice Endpoints

#### List Invoices

```
GET /api/invoices?page=1&type=sales&status=confirmed&customer_id=5
Authorization: Bearer <token>
Permission: sales_view (for sales) / purchases_view (for purchases)

Response (200):
{
  "success": true,
  "data": {
    "invoices": [
      {
        "id": 1,
        "invoice_number": "INV-2025-001",
        "invoice_type": "sales",
        "status": "confirmed",
        "customer": {
          "id": 5,
          "name": "شركة الأمل"
        },
        "subtotal": 10000.00,
        "tax_amount": 1500.00,
        "discount_amount": 500.00,
        "total": 11000.00,
        "paid_amount": 5000.00,
        "invoice_date": "2025-12-01",
        "due_date": "2025-12-31"
      }
    ],
    "total": 200,
    "page": 1,
    "per_page": 10
  }
}
```

#### Create Invoice

```
POST /api/invoices
Authorization: Bearer <token>
Permission: sales_add / purchases_add

Request:
{
  "invoice_type": "sales",
  "customer_id": 5,
  "warehouse_id": 1,
  "invoice_date": "2025-12-01",
  "due_date": "2025-12-31",
  "notes": "فاتورة مبيعات",
  "items": [
    {
      "product_id": 10,
      "quantity": 5,
      "unit_price": 100.00,
      "discount": 10.00
    },
    {
      "product_id": 15,
      "quantity": 3,
      "unit_price": 200.00
    }
  ]
}

Response (201):
{
  "success": true,
  "data": {
    "id": 50,
    "invoice_number": "INV-2025-050",
    "status": "draft",
    "subtotal": 1100.00,
    "tax_amount": 165.00,
    "total": 1255.00,
    ...
  },
  "message": "تم إنشاء الفاتورة بنجاح"
}
```

---

### Inventory Endpoints

#### Get Stock Levels

```
GET /api/inventory?warehouse_id=1&low_stock=true
Authorization: Bearer <token>
Permission: inventory_view

Response (200):
{
  "success": true,
  "data": {
    "inventory": [
      {
        "product_id": 10,
        "product_name": "منتج 1",
        "warehouse_id": 1,
        "warehouse_name": "المستودع الرئيسي",
        "quantity": 50,
        "reserved": 5,
        "available": 45,
        "min_stock": 20,
        "status": "normal"
      }
    ],
    "summary": {
      "total_products": 100,
      "low_stock_count": 5,
      "out_of_stock_count": 2
    }
  }
}
```

#### Stock Adjustment

```
POST /api/inventory/adjust
Authorization: Bearer <token>
Permission: inventory_stock_adjust

Request:
{
  "product_id": 10,
  "warehouse_id": 1,
  "adjustment_type": "in",  // in/out/adjustment
  "quantity": 10,
  "reason": "تصحيح جرد",
  "reference": "ADJ-001"
}

Response (200):
{
  "success": true,
  "data": {
    "new_quantity": 60,
    "movement_id": 150
  },
  "message": "تم تعديل المخزون بنجاح"
}
```

---

### Report Endpoints

#### Sales Report

```
GET /api/reports/sales?from=2025-01-01&to=2025-12-31&group_by=month
Authorization: Bearer <token>
Permission: reports_view

Response (200):
{
  "success": true,
  "data": {
    "summary": {
      "total_sales": 500000.00,
      "total_tax": 75000.00,
      "total_discount": 10000.00,
      "net_sales": 565000.00,
      "invoice_count": 150
    },
    "breakdown": [
      {
        "period": "2025-01",
        "sales": 40000.00,
        "invoice_count": 12
      }
    ]
  }
}
```

#### Inventory Report

```
GET /api/reports/inventory?warehouse_id=1
Authorization: Bearer <token>
Permission: reports_view

Response (200):
{
  "success": true,
  "data": {
    "summary": {
      "total_value": 1000000.00,
      "total_products": 500,
      "low_stock_products": 15,
      "out_of_stock_products": 3
    },
    "categories": [
      {
        "category": "إلكترونيات",
        "product_count": 50,
        "total_value": 500000.00
      }
    ]
  }
}
```

---

## Webhook Events

### Event Types

| Event | Description |
|-------|-------------|
| `invoice.created` | New invoice created |
| `invoice.paid` | Invoice fully paid |
| `stock.low` | Stock below minimum |
| `stock.out` | Stock depleted |
| `user.login` | User logged in |

### Webhook Payload

```json
{
  "event": "invoice.created",
  "timestamp": "2025-12-01T12:00:00Z",
  "data": {
    "id": 50,
    "invoice_number": "INV-2025-050",
    "total": 1255.00
  }
}
```

---

## SDK Examples

### Python

```python
import requests

BASE_URL = "https://api.store.example.com/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "password": "password"
})
tokens = response.json()["data"]

# Use API
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
products = requests.get(f"{BASE_URL}/products", headers=headers)
```

### JavaScript

```javascript
const BASE_URL = 'https://api.store.example.com/api';

// Login
const loginResponse = await fetch(`${BASE_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'password' })
});
const { data: tokens } = await loginResponse.json();

// Use API
const products = await fetch(`${BASE_URL}/products`, {
  headers: { 'Authorization': `Bearer ${tokens.access_token}` }
});
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-01 | Initial API documentation |

---

**OpenAPI Spec:** `/api/docs`  
**Swagger UI:** `/api/docs`  
**Support:** api-support@company.com
