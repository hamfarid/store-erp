# Gaara ERP - API Documentation

## 🌐 Base URL

- **Development**: `http://localhost:8000/api`
- **Production**: `https://yourdomain.com/api`

## 🔐 Authentication

All protected endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### Register

```http
POST /api/auth/users/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "أحمد",
  "last_name": "محمد"
}
```

#### Login

```http
POST /api/auth/jwt/create/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token

```http
POST /api/auth/jwt/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout

```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
```

## 📊 Core Endpoints

### Health Check

```http
GET /health/
GET /health/detailed/
```

### Countries

```http
GET /api/countries/
GET /api/countries/{id}/
```

### Companies

```http
GET /api/companies/
GET /api/companies/{id}/
POST /api/companies/
PUT /api/companies/{id}/
DELETE /api/companies/{id}/
```

### Currencies

```http
GET /api/currencies/
GET /api/currencies/{id}/
```

## 📦 Inventory Module

Base Path: `/api/inventory/`

### Products

```http
GET    /api/inventory/products/              # List products
GET    /api/inventory/products/{id}/         # Get product
POST   /api/inventory/products/              # Create product
PUT    /api/inventory/products/{id}/         # Update product
PATCH  /api/inventory/products/{id}/         # Partial update
DELETE /api/inventory/products/{id}/         # Delete product
```

**Query Parameters:**

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `search`: Search term
- `category`: Filter by category
- `warehouse`: Filter by warehouse

**Example:**

```http
GET /api/inventory/products/?page=1&limit=20&search=بذور&category=بذور
```

### Warehouses

```http
GET    /api/inventory/warehouses/
GET    /api/inventory/warehouses/{id}/
POST   /api/inventory/warehouses/
PUT    /api/inventory/warehouses/{id}/
DELETE /api/inventory/warehouses/{id}/
```

### Stock Movements

```http
GET    /api/inventory/movements/
POST   /api/inventory/movements/
GET    /api/inventory/movements/{id}/
```

**Query Parameters:**

- `type`: Movement type (in, out, transfer, adjustment)
- `product`: Filter by product ID
- `warehouse`: Filter by warehouse ID
- `dateFrom`: Start date (YYYY-MM-DD)
- `dateTo`: End date (YYYY-MM-DD)

### Stock Levels

```http
GET  /api/inventory/warehouses/{warehouse_id}/stock/
PATCH /api/inventory/warehouses/{warehouse_id}/stock/{product_id}/
```

### Reports

```http
GET /api/inventory/reports/summary/
GET /api/inventory/reports/low-stock/
GET /api/inventory/reports/valuation/
```

## 💰 Sales Module

Base Path: `/api/sales/`

### Customers

```http
GET    /api/sales/customers/
GET    /api/sales/customers/{id}/
POST   /api/sales/customers/
PUT    /api/sales/customers/{id}/
DELETE /api/sales/customers/{id}/
```

**Query Parameters:**

- `page`: Page number
- `limit`: Items per page
- `search`: Search term
- `status`: Filter by status

### Orders

```http
GET    /api/sales/orders/
GET    /api/sales/orders/{id}/
POST   /api/sales/orders/
PUT    /api/sales/orders/{id}/
POST   /api/sales/orders/{id}/cancel/
POST   /api/sales/orders/{id}/fulfill/
```

**Query Parameters:**

- `status`: Order status (pending, confirmed, processing, shipped, delivered, cancelled)
- `customer`: Filter by customer ID
- `dateFrom`: Start date
- `dateTo`: End date

### Invoices

```http
GET    /api/sales/invoices/
GET    /api/sales/invoices/{id}/
POST   /api/sales/invoices/
PUT    /api/sales/invoices/{id}/
POST   /api/sales/invoices/{id}/send/
POST   /api/sales/invoices/{id}/pay/
```

### Reports

```http
GET /api/sales/reports/summary/
GET /api/sales/customers/{id}/report/
GET /api/sales/reports/top-products/
GET /api/sales/reports/trend/
```

## 📊 Accounting Module

Base Path: `/api/accounting/`

### Chart of Accounts

```http
GET    /api/accounting/accounts/
GET    /api/accounting/accounts/{id}/
POST   /api/accounting/accounts/
PUT    /api/accounting/accounts/{id}/
DELETE /api/accounting/accounts/{id}/
```

### Journal Entries

```http
GET    /api/accounting/journal-entries/
GET    /api/accounting/journal-entries/{id}/
POST   /api/accounting/journal-entries/
PUT    /api/accounting/journal-entries/{id}/
DELETE /api/accounting/journal-entries/{id}/
POST   /api/accounting/journal-entries/{id}/approve/
```

**Query Parameters:**

- `dateFrom`: Start date
- `dateTo`: End date
- `account`: Filter by account ID

### Financial Reports

```http
GET /api/accounting/reports/balance-sheet/
GET /api/accounting/reports/income-statement/
GET /api/accounting/reports/cash-flow/
GET /api/accounting/reports/trial-balance/
GET /api/accounting/accounts/{id}/ledger/
```

## 👥 User Management

Base Path: `/api/users/` (Admin only)

### Users

```http
GET    /api/users/
GET    /api/users/{id}/
POST   /api/users/
PUT    /api/users/{id}/
DELETE /api/users/{id}/
PATCH  /api/users/{id}/status/
POST   /api/users/{id}/reset-password/
POST   /api/users/{id}/roles/
DELETE /api/users/{id}/roles/{role_id}/
GET    /api/users/{id}/permissions/
GET    /api/users/{id}/activity/
```

**Query Parameters:**

- `page`: Page number
- `limit`: Items per page
- `search`: Search term
- `role`: Filter by role (admin, manager, accountant, user)
- `status`: Filter by status (active, inactive)

### Bulk Operations

```http
POST /api/users/bulk-delete/
POST /api/users/bulk-update/
```

## 🔌 IoT Module

Base Path: `/api/iot/`

### Devices

```http
GET    /api/iot/devices/
GET    /api/iot/devices/{id}/
POST   /api/iot/devices/
PUT    /api/iot/devices/{id}/
DELETE /api/iot/devices/{id}/
PATCH  /api/iot/devices/{id}/status/
GET    /api/iot/devices/{id}/status/
GET    /api/iot/devices/{id}/analytics/
```

### Sensors

```http
GET /api/iot/sensors/
GET /api/iot/devices/{device_id}/sensors/
GET /api/iot/sensors/{id}/
GET /api/iot/sensors/{id}/readings/
GET /api/iot/sensors/{id}/analytics/
```

**Query Parameters for Readings:**

- `startDate`: Start date (ISO 8601)
- `endDate`: End date (ISO 8601)
- `limit`: Number of readings (default: 100)

### Alerts

```http
GET    /api/iot/alerts/
GET    /api/iot/alerts/{id}/
POST   /api/iot/alerts/{id}/acknowledge/
POST   /api/iot/alerts/{id}/resolve/
```

**Query Parameters:**

- `status`: Alert status (active, acknowledged, resolved)
- `severity`: Alert severity (low, medium, high, critical)
- `device`: Filter by device ID

## 📈 Dashboard

Base Path: `/api/dashboard/`

### Statistics

```http
GET /api/dashboard/stats/
GET /api/dashboard/sales-chart/
GET /api/dashboard/revenue-chart/
GET /api/dashboard/recent-activities/
GET /api/dashboard/low-stock-alerts/
GET /api/dashboard/pending-orders/
GET /api/dashboard/top-products/
GET /api/dashboard/customer-growth/
GET /api/dashboard/iot-status/
GET /api/dashboard/ai-predictions/
```

## 🔒 Error Responses

### Standard Error Format

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

### HTTP Status Codes

- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Validation Errors

```json
{
  "errors": {
    "field_name": ["Error message 1", "Error message 2"]
  }
}
```

## 📝 Pagination

All list endpoints support pagination:

**Query Parameters:**

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

**Response Format:**

```json
{
  "count": 150,
  "next": "http://api.example.com/api/resource/?page=2",
  "previous": null,
  "results": [...]
}
```

## 🔍 Filtering & Search

Most endpoints support filtering and search:

**Common Query Parameters:**

- `search`: Full-text search
- `ordering`: Sort field (prefix with `-` for descending)
- `page`: Page number
- `limit`: Items per page

**Example:**

```http
GET /api/inventory/products/?search=بذور&ordering=-created_at&page=1&limit=20
```

## 📅 Date Formats

All dates should be in ISO 8601 format:

- Date: `YYYY-MM-DD`
- DateTime: `YYYY-MM-DDTHH:mm:ssZ`
- Example: `2025-01-15T10:30:00Z`

## 🌍 Language & Localization

- Default language: Arabic (ar)
- All responses include Arabic labels
- Dates formatted according to locale
- Currency: SAR (ر.س)

## 🔄 Rate Limiting

- **Authenticated**: 1000 requests/hour
- **Unauthenticated**: 100 requests/hour
- Headers included in response:
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

## 📚 Additional Resources

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **Health Check**: `http://localhost:8000/health/`

---

**Last Updated**: 2025-01-15  
**API Version**: 1.0.0
