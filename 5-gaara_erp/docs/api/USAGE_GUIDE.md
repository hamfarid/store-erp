# Store ERP API - Usage Guide

**Version:** 1.0.0  
**Base URL:** `http://localhost:5001`  
**Documentation:** `/api/docs` (Swagger UI)  
**OpenAPI Spec:** `/api/openapi.json`

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [Common Patterns](#common-patterns)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Pagination](#pagination)
7. [Examples](#examples)

---

## 🚀 Quick Start

### 1. Start the Server

```bash
cd backend
python src/main.py
```

Server will start on `http://localhost:5001`

### 2. Access Documentation

Open your browser and navigate to:
- **Swagger UI:** http://localhost:5001/api/docs
- **OpenAPI JSON:** http://localhost:5001/api/openapi.json

### 3. Import Postman Collection

1. Open Postman
2. Click **Import**
3. Select `postman/Store_API.postman_collection.json`
4. Collection will be imported with all endpoints

---

## 🔐 Authentication

### Overview

The API uses **JWT (JSON Web Tokens)** for authentication.

**Token Types:**
- **Access Token:** Short-lived (15 minutes), used for API requests
- **Refresh Token:** Long-lived (7 days), used to get new access tokens

### Login Flow

#### 1. Login

```bash
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
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "is_active": true
    },
    "expires_in": 900
  }
}
```

#### 2. Use Access Token

Include the access token in the `Authorization` header:

```bash
GET /api/products
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 3. Refresh Token (when access token expires)

```bash
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 900
  }
}
```

#### 4. Logout

```bash
POST /api/auth/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🔄 Common Patterns

### Success Response Format

All successful responses follow this format:

```json
{
  "success": true,
  "data": {
    // Response data here
  }
}
```

### List Response Format

List endpoints return paginated data:

```json
{
  "success": true,
  "data": {
    "items": [
      // Array of items
    ],
    "pagination": {
      "page": 1,
      "pages": 5,
      "per_page": 10,
      "total": 42
    }
  }
}
```

### Error Response Format

All errors follow this format:

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "status_code": 400,
  "timestamp": "2025-11-07T10:30:00Z",
  "path": "/api/products",
  "details": [
    {
      "field": "name",
      "message": "Field is required",
      "value": null
    }
  ]
}
```

---

## ❌ Error Handling

### HTTP Status Codes

| Code | Meaning | When It Happens |
|------|---------|-----------------|
| **200** | OK | Request successful |
| **201** | Created | Resource created successfully |
| **400** | Bad Request | Validation errors in request |
| **401** | Unauthorized | Authentication required or token invalid |
| **403** | Forbidden | User doesn't have permission |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Duplicate resource (e.g., barcode already exists) |
| **422** | Unprocessable Entity | Business logic error (e.g., insufficient stock) |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Internal Server Error | Server error occurred |
| **503** | Service Unavailable | Service temporarily unavailable |

### Common Errors

#### 400 Bad Request - Validation Error

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Validation failed for one or more fields",
  "status_code": 400,
  "timestamp": "2025-11-07T10:30:00Z",
  "path": "/api/products",
  "details": [
    {
      "field": "name",
      "message": "Field is required",
      "value": null
    },
    {
      "field": "selling_price",
      "message": "Must be greater than 0",
      "value": -10
    }
  ]
}
```

#### 401 Unauthorized - Token Expired

```json
{
  "error": "TOKEN_EXPIRED",
  "message": "Access token has expired. Please refresh your token.",
  "status_code": 401,
  "timestamp": "2025-11-07T10:30:00Z",
  "path": "/api/products"
}
```

**Solution:** Use refresh token to get new access token

#### 404 Not Found

```json
{
  "error": "NOT_FOUND",
  "message": "Product with ID 999 not found",
  "status_code": 404,
  "timestamp": "2025-11-07T10:30:00Z",
  "path": "/api/products/999"
}
```

#### 409 Conflict - Duplicate Resource

```json
{
  "error": "CONFLICT",
  "message": "Product with barcode '1234567890' already exists",
  "status_code": 409,
  "timestamp": "2025-11-07T10:30:00Z",
  "path": "/api/products",
  "details": [
    {
      "field": "barcode",
      "message": "Must be unique",
      "value": "1234567890"
    }
  ]
}
```

---

## ⏱️ Rate Limiting

### Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/auth/login` | 5 requests | 1 minute |
| All other endpoints | 100 requests | 1 minute |

### Rate Limit Headers

Response includes rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699356000
```

### Rate Limit Exceeded

```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Please try again later.",
  "status_code": 429,
  "timestamp": "2025-11-07T10:30:00Z",
  "path": "/api/auth/login",
  "retry_after": 60
}
```

**Solution:** Wait for `retry_after` seconds before retrying

---

## 📄 Pagination

### Query Parameters

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | integer | 1 | - | Page number |
| `per_page` | integer | 10 | 100 | Items per page |

### Example Request

```bash
GET /api/products?page=2&per_page=20
Authorization: Bearer {token}
```

### Example Response

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 21,
        "name": "Product 21",
        // ... more fields
      }
      // ... 19 more items
    ],
    "pagination": {
      "page": 2,
      "pages": 5,
      "per_page": 20,
      "total": 95
    }
  }
}
```

---

## 💡 Examples

### Example 1: Complete Product Workflow

```bash
# 1. Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Save access_token from response

# 2. List products
curl -X GET http://localhost:5001/api/products?page=1&per_page=10 \
  -H "Authorization: Bearer {access_token}"

# 3. Create product
curl -X POST http://localhost:5001/api/products \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Dell XPS 15",
    "barcode": "1234567890123",
    "cost_price": 4500.00,
    "selling_price": 5999.00
  }'

# 4. Get product details
curl -X GET http://localhost:5001/api/products/1 \
  -H "Authorization: Bearer {access_token}"
```

### Example 2: Error Handling

```python
import requests

# Login
response = requests.post(
    'http://localhost:5001/api/auth/login',
    json={'username': 'admin', 'password': 'admin123'}
)

if response.status_code == 200:
    data = response.json()
    access_token = data['data']['access_token']
    print(f'✅ Login successful')
else:
    error = response.json()
    print(f'❌ Login failed: {error["message"]}')
    exit(1)

# Create product with error handling
headers = {'Authorization': f'Bearer {access_token}'}
product_data = {
    'name': 'Test Product',
    'cost_price': 100.00,
    'selling_price': 150.00
}

response = requests.post(
    'http://localhost:5001/api/products',
    headers=headers,
    json=product_data
)

if response.status_code == 201:
    product = response.json()['data']
    print(f'✅ Product created: {product["id"]}')
elif response.status_code == 400:
    error = response.json()
    print(f'❌ Validation error:')
    for detail in error.get('details', []):
        print(f'  - {detail["field"]}: {detail["message"]}')
elif response.status_code == 409:
    error = response.json()
    print(f'❌ Conflict: {error["message"]}')
else:
    print(f'❌ Unexpected error: {response.status_code}')
```

---

## 📚 Additional Resources

- **Swagger UI:** http://localhost:5001/api/docs
- **OpenAPI Spec:** http://localhost:5001/api/openapi.json
- **Postman Collection:** `postman/Store_API.postman_collection.json`
- **Error Schemas:** `backend/src/schemas/error_schemas.py`

---

**Last Updated:** 2025-11-07  
**Version:** 1.0.0  
**Part of:** T23 - API Documentation Enhancement

