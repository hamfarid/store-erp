# API Documentation - Store Management System v1.5

**Base URL**: `http://localhost:5002`  
**API Version**: 1.5  
**Last Updated**: 2025-11-17

---

## Table of Contents

1. [Authentication](#authentication)
2. [Products & Inventory](#products--inventory)
3. [Categories](#categories)
4. [Customers & Suppliers](#customers--suppliers)
5. [Invoices](#invoices)
6. [Accounting](#accounting)
7. [Users & Roles](#users--roles)
8. [Dashboard & Reports](#dashboard--reports)
9. [Error Handling](#error-handling)
10. [Response Envelope](#response-envelope)

---

## Authentication

All protected endpoints require JWT Bearer token authentication.

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Administrator"
    }
  },
  "message": "تم تسجيل الدخول بنجاح"
}
```

### Logout

```http
POST /api/auth/logout
Authorization: Bearer <token>
```

### Refresh Token

```http
POST /api/auth/refresh
Authorization: Bearer <token>
```

---

## Products & Inventory

### List All Products

```http
GET /api/products
Authorization: Bearer <token>
```

**Query Parameters**:
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 10)
- `search` (string): Search term
- `category_id` (int): Filter by category
- `is_active` (boolean): Filter by active status

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Product Name",
      "name_en": "Product Name EN",
      "sku": "SKU001",
      "barcode": "1234567890",
      "category_id": 1,
      "cost_price": 10.00,
      "sale_price": 15.00,
      "current_stock": 100,
      "min_quantity": 10,
      "is_active": true,
      "created_at": "2025-11-17T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 2,
    "pages": 1
  }
}
```

### Get Single Product

```http
GET /api/products/:id
Authorization: Bearer <token>
```

**Response (200 OK)**: Single product object

### Create Product

```http
POST /api/products
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Product",
  "name_en": "New Product EN",
  "sku": "SKU002",
  "barcode": "0987654321",
  "category_id": 1,
  "cost_price": 20.00,
  "sale_price": 30.00,
  "min_quantity": 5,
  "is_active": true
}
```

**Response (201 Created)**: Created product object

### Update Product

```http
PUT /api/products/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Product",
  "sale_price": 35.00
}
```

**Response (200 OK)**: Updated product object

### Delete Product

```http
DELETE /api/products/:id
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Product deleted successfully"
}
```

### Product Statistics

```http
GET /api/products/stats
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "total_products": 100,
    "active_products": 95,
    "inactive_products": 5,
    "low_stock_products": 10,
    "out_of_stock_products": 3,
    "total_stock": 5000,
    "total_inventory_value": 150000.00
  }
}
```

### Low Stock Products

```http
GET /api/products/low-stock
Authorization: Bearer <token>
```

### Out of Stock Products

```http
GET /api/products/out-of-stock
Authorization: Bearer <token>
```

### Search Products

```http
GET /api/products/search?q=laptop
Authorization: Bearer <token>
```

**Query Parameters**:
- `q` (string, required): Search query
- `limit` (int): Maximum results (default: 10)

### Update Stock

```http
POST /api/products/:id/update-stock
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantity": 50,
  "reason": "Stock adjustment"
}
```

### Export Products

```http
GET /api/products/export?format=json
Authorization: Bearer <token>
```

**Query Parameters**:
- `format` (string): Export format (json, csv)

---

## Categories

### List Categories

```http
GET /api/categories
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Electronics",
      "name_en": "Electronics",
      "description": "Electronic devices",
      "parent_id": null,
      "is_active": true
    }
  ]
}
```

### Get Category

```http
GET /api/categories/:id
Authorization: Bearer <token>
```

### Create Category

```http
POST /api/categories
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Category",
  "name_en": "New Category EN",
  "description": "Category description",
  "parent_id": null,
  "is_active": true
}
```

### Update Category

```http
PUT /api/categories/:id
Authorization: Bearer <token>
```

### Delete Category

```http
DELETE /api/categories/:id
Authorization: Bearer <token>
```

---

## Customers & Suppliers

### List Customers

```http
GET /api/customers
Authorization: Bearer <token>
```

**Query Parameters**:
- `page`, `per_page`, `search`, `is_active`

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Customer Name",
      "phone": "+1234567890",
      "email": "customer@example.com",
      "address": "123 Main St",
      "balance": 1000.00,
      "is_active": true
    }
  ]
}
```

### Get Customer

```http
GET /api/customers/:id
Authorization: Bearer <token>
```

### Create Customer

```http
POST /api/customers
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Customer",
  "phone": "+1234567890",
  "email": "newcustomer@example.com",
  "address": "456 Elm St",
  "is_active": true
}
```

### Update Customer

```http
PUT /api/customers/:id
Authorization: Bearer <token>
```

### Delete Customer

```http
DELETE /api/customers/:id
Authorization: Bearer <token>
```

### Customer Statistics

```http
GET /api/customers/stats
Authorization: Bearer <token>
```

### Search Customers

```http
GET /api/customers/search?q=john
Authorization: Bearer <token>
```

### Export Customers

```http
GET /api/customers/export?format=csv
Authorization: Bearer <token>
```

### Suppliers

All customer endpoints have equivalent supplier endpoints:
- `GET /api/suppliers`
- `GET /api/suppliers/:id`
- `POST /api/suppliers`
- `PUT /api/suppliers/:id`
- `DELETE /api/suppliers/:id`
- `GET /api/suppliers/stats`
- `GET /api/suppliers/search`
- `GET /api/suppliers/export`

---

## Invoices

### List Invoices

```http
GET /api/invoices?invoice_type=sales
Authorization: Bearer <token>
```

**Query Parameters**:
- `invoice_type` (string): sales, purchase, return
- `status` (string): draft, confirmed, cancelled
- `page`, `per_page`, `search`

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "invoice_number": "INV-2025-001",
      "invoice_type": "sales",
      "customer_id": 1,
      "invoice_date": "2025-11-17",
      "total_amount": 500.00,
      "status": "confirmed",
      "items": [
        {
          "product_id": 1,
          "quantity": 2,
          "unit_price": 250.00,
          "total": 500.00
        }
      ]
    }
  ]
}
```

### Get Invoice

```http
GET /api/invoices/:id
Authorization: Bearer <token>
```

### Create Invoice

```http
POST /api/invoices
Authorization: Bearer <token>
Content-Type: application/json

{
  "invoice_type": "sales",
  "customer_id": 1,
  "invoice_date": "2025-11-17",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 250.00
    }
  ],
  "notes": "Invoice notes"
}
```

**Response (201 Created)**: Created invoice object

### Update Invoice

```http
PUT /api/invoices/:id
Authorization: Bearer <token>
```

### Delete Invoice

```http
DELETE /api/invoices/:id
Authorization: Bearer <token>
```

### Confirm Invoice

```http
POST /api/invoices/:id/confirm
Authorization: Bearer <token>
```

### Cancel Invoice

```http
POST /api/invoices/:id/cancel
Authorization: Bearer <token>
```

### Add Payment

```http
POST /api/invoices/:id/payments
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 250.00,
  "payment_method": "cash",
  "payment_date": "2025-11-17"
}
```

### Invoice Statistics

```http
GET /api/invoices/stats
Authorization: Bearer <token>
```

### Search Invoices

```http
GET /api/invoices/search?q=INV-001
Authorization: Bearer <token>
```

### Export Invoices

```http
GET /api/invoices/export?format=pdf
Authorization: Bearer <token>
```

---

## Accounting

### Currencies

#### List Currencies

```http
GET /api/accounting/currencies
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "US Dollar",
      "name_en": "US Dollar",
      "code": "USD",
      "symbol": "$",
      "exchange_rate": 1.0,
      "is_default": true,
      "is_active": true
    }
  ]
}
```

#### Create Currency

```http
POST /api/accounting/currencies
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Euro",
  "name_en": "Euro",
  "code": "EUR",
  "symbol": "€",
  "exchange_rate": 0.85,
  "is_active": true
}
```

#### Update Currency

```http
PUT /api/accounting/currencies/:id
Authorization: Bearer <token>
```

#### Delete Currency

```http
DELETE /api/accounting/currencies/:id
Authorization: Bearer <token>
```

### Cash Boxes (Treasuries)

#### List Cash Boxes

```http
GET /api/accounting/cash-boxes
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Main Cash Box",
      "code": "CASH01",
      "currency_id": 1,
      "current_balance": 10000.00,
      "opening_balance": 5000.00,
      "is_main": true,
      "status": "active"
    }
  ]
}
```

#### Create Cash Box

```http
POST /api/accounting/cash-boxes
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Branch Cash Box",
  "code": "CASH02",
  "currency_id": 1,
  "opening_balance": 2000.00,
  "description": "Branch office cash box"
}
```

#### Update Cash Box

```http
PUT /api/accounting/cash-boxes/:id
Authorization: Bearer <token>
```

#### Delete Cash Box

```http
DELETE /api/accounting/cash-boxes/:id
Authorization: Bearer <token>
```

#### Cash Box Transactions

```http
GET /api/accounting/cash-boxes/:id/transactions
Authorization: Bearer <token>
```

#### Add Transaction

```http
POST /api/accounting/cash-boxes/:id/transactions
Authorization: Bearer <token>
Content-Type: application/json

{
  "transaction_type": "deposit",
  "amount": 500.00,
  "description": "Daily sales deposit",
  "currency_id": 1
}
```

### Vouchers

#### List Vouchers

```http
GET /api/accounting/vouchers
Authorization: Bearer <token>
```

**Query Parameters**:
- `voucher_type` (string): payment, receipt
- `status` (string): draft, approved, rejected
- `start_date`, `end_date`

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "voucher_number": "PAY-2025-001",
      "voucher_type": "payment",
      "amount": 1000.00,
      "beneficiary": "Supplier Name",
      "description": "Payment for invoice INV-001",
      "status": "approved",
      "created_at": "2025-11-17T10:00:00Z"
    }
  ]
}
```

#### Create Voucher

```http
POST /api/accounting/vouchers
Authorization: Bearer <token>
Content-Type: application/json

{
  "voucher_type": "payment",
  "amount": 1000.00,
  "beneficiary": "Supplier Name",
  "description": "Payment description",
  "treasury_id": 1,
  "currency_id": 1
}
```

#### Update Voucher Status

```http
PUT /api/accounting/vouchers/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "approved"
}
```

### Profit & Loss Report

```http
GET /api/accounting/profit-loss?start_date=2025-01-01&end_date=2025-12-31
Authorization: Bearer <token>
```

**Query Parameters**:
- `start_date` (date, required): Report start date
- `end_date` (date, required): Report end date
- `period` (string): monthly, yearly, custom

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "period": {
      "start_date": "2025-01-01",
      "end_date": "2025-12-31"
    },
    "revenue": {
      "sales": 150000.00,
      "other_income": 5000.00,
      "total": 155000.00
    },
    "expenses": {
      "cost_of_goods_sold": 80000.00,
      "operating_expenses": 40000.00,
      "other_expenses": 5000.00,
      "total": 125000.00
    },
    "net_profit": 30000.00,
    "profit_margin": 19.35
  }
}
```

---

## Users & Roles

### List Users

```http
GET /api/users
Authorization: Bearer <token>
```

**Requires**: Admin role

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Administrator",
      "role": "admin",
      "is_active": true,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

### Get Current User

```http
GET /api/users/me
Authorization: Bearer <token>
```

**Response (200 OK)**: Current user object from JWT token

### Get User

```http
GET /api/users/:id
Authorization: Bearer <token>
```

### Create User

```http
POST /api/users
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "SecureP@ssw0rd",
  "full_name": "New User",
  "role_id": 2,
  "is_active": true
}
```

### Update User

```http
PUT /api/users/:id
Authorization: Bearer <token>
```

### Delete User

```http
DELETE /api/users/:id
Authorization: Bearer <token>
```

### Roles

#### List Roles

```http
GET /api/roles
Authorization: Bearer <token>
```

#### Get Role

```http
GET /api/roles/:id
Authorization: Bearer <token>
```

#### Create Role

```http
POST /api/roles
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Manager",
  "description": "Store Manager Role",
  "permissions": ["read_products", "write_products", "read_invoices"]
}
```

#### Update Role

```http
PUT /api/roles/:id
Authorization: Bearer <token>
```

#### Delete Role

```http
DELETE /api/roles/:id
Authorization: Bearer <token>
```

---

## Dashboard & Reports

### Dashboard Statistics

```http
GET /api/dashboard/stats
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "products": {
      "total": 100,
      "active": 95,
      "low_stock": 10
    },
    "invoices": {
      "today": 15,
      "this_month": 450,
      "total_value": 125000.00
    },
    "customers": {
      "total": 250,
      "active": 240
    },
    "revenue": {
      "today": 5000.00,
      "this_month": 150000.00
    }
  }
}
```

### Available Reports

```http
GET /api/reports
Authorization: Bearer <token>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": "stock_valuation",
      "name": "Stock Valuation Report",
      "name_en": "Stock Valuation Report",
      "endpoint": "/stock-valuation",
      "method": "GET",
      "description": "Comprehensive stock valuation report"
    },
    {
      "id": "sales",
      "name": "Sales Report",
      "name_en": "Sales Report",
      "endpoint": "/sales-report",
      "method": "GET",
      "description": "Sales report by period"
    }
  ]
}
```

### Stock Valuation Report

```http
GET /stock-valuation
Authorization: Bearer <token>
```

### Low Stock Report

```http
GET /low-stock
Authorization: Bearer <token>
```

### Inventory Report

```http
GET /inventory-report
Authorization: Bearer <token>
```

### Stock Movements Report

```http
GET /stock-movements-report
Authorization: Bearer <token>
```

### Sales Report

```http
GET /sales-report?start_date=2025-01-01&end_date=2025-12-31
Authorization: Bearer <token>
```

### Purchases Report

```http
GET /purchases-report?start_date=2025-01-01&end_date=2025-12-31
Authorization: Bearer <token>
```

---

## Error Handling

### Error Response Format (P0.2.4 Envelope)

All errors follow a consistent response format:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error details"
  },
  "timestamp": "2025-11-17T10:00:00Z"
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate entry)
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
- `501 Not Implemented`: Feature not implemented

### Common Error Codes

- `AUTH_INVALID_CREDENTIALS`: Invalid username or password
- `AUTH_INVALID_TOKEN`: JWT token invalid or expired
- `AUTH_INSUFFICIENT_PERMISSIONS`: User lacks required permissions
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `VALIDATION_ERROR`: Request data validation failed
- `DUPLICATE_ENTRY`: Resource with same identifier exists
- `INTERNAL_ERROR`: Unexpected server error

### Example Error Response

```json
{
  "success": false,
  "error": "Validation Error",
  "message": "Invalid request data",
  "code": "VALIDATION_ERROR",
  "details": {
    "name": "Name is required",
    "email": "Invalid email format"
  },
  "timestamp": "2025-11-17T10:00:00Z"
}
```

---

## Response Envelope

### Success Response Format (P0.2.4)

All successful responses follow this format:

```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation completed successfully",
  "timestamp": "2025-11-17T10:00:00Z",
  "metadata": {
    "pagination": { /* if applicable */ },
    "filters": { /* if applicable */ }
  }
}
```

### Pagination

Paginated responses include:

```json
{
  "success": true,
  "data": [ /* items */ ],
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

## Rate Limiting

- **Rate Limit**: 100 requests per minute per IP
- **Burst**: Up to 20 requests in 1 second
- **Headers**:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Time when limit resets

---

## Authentication Headers

All protected endpoints require:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## API Versioning

Current API version: **v1.5**

Future versions will be accessed via URL path:
- `/api/v1/...`
- `/api/v2/...`

---

## Postman Collection

Import the provided Postman collection for easy testing:

📦 **File**: `postman/Store_Management_API.postman_collection.json`

---

## Support

- **Documentation**: `/docs` (Swagger UI)
- **GitHub**: https://github.com/hamfarid/store
- **Issues**: https://github.com/hamfarid/store/issues

---

**Last Updated**: November 17, 2025  
**API Version**: 1.5.0
