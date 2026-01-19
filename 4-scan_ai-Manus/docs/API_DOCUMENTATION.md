# API Documentation - Gaara AI Platform

**Version:** 2.0.0  
**Base URL:** `http://localhost:5000/api` (Development)  
**Production URL:** `https://api.gaara-ai.com/api`  
**Last Updated:** 2025-01-18

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Common Patterns](#common-patterns)
4. [API Endpoints](#api-endpoints)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)

---

## 1. Overview

### 1.1 API Characteristics

- **Protocol:** REST over HTTPS
- **Format:** JSON
- **Authentication:** JWT Bearer tokens
- **Versioning:** URL-based (`/api/v1/`)
- **Total Endpoints:** 85+

### 1.2 Base Response Format

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2025-01-18T00:00:00Z"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... }
  },
  "timestamp": "2025-01-18T00:00:00Z"
}
```

---

## 2. Authentication

### 2.1 Login

**Endpoint:** `POST /api/auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johndoe",
      "role": "user"
    }
  }
}
```

### 2.2 Register

**Endpoint:** `POST /api/auth/register`

**Request:**
```json
{
  "username": "johndoe",
  "email": "user@example.com",
  "password": "securePassword123",
  "full_name": "John Doe"
}
```

**Response:** Same as login

### 2.3 Refresh Token

**Endpoint:** `POST /api/auth/refresh`

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "new_access_token",
    "expires_in": 900
  }
}
```

### 2.4 Logout

**Endpoint:** `POST /api/auth/logout`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## 3. Common Patterns

### 3.1 Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page` (default: 1)
- `per_page` (default: 20, max: 100)

**Response:**
```json
{
  "success": true,
  "data": [ ... ],
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

### 3.2 Filtering

**Query Parameters:**
- `search` - Full-text search
- `filter[field]` - Filter by field value
- `sort` - Sort field (prefix with `-` for descending)

**Example:**
```
GET /api/farms?search=organic&filter[area]=gt:100&sort=-created_at
```

### 3.3 Including Related Data

**Query Parameter:**
- `include` - Comma-separated list of relations

**Example:**
```
GET /api/farms/1?include=crops,sensors
```

---

## 4. API Endpoints

### 4.1 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login` | User login | No |
| POST | `/api/auth/register` | User registration | No |
| POST | `/api/auth/logout` | User logout | Yes |
| POST | `/api/auth/refresh` | Refresh access token | Yes (Refresh) |
| POST | `/api/auth/forgot-password` | Request password reset | No |
| POST | `/api/auth/reset-password` | Reset password | No |
| POST | `/api/auth/verify-email` | Verify email address | No |
| GET | `/api/auth/me` | Get current user | Yes |

### 4.2 Farm Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/farms` | List all farms | Yes |
| GET | `/api/farms/:id` | Get farm details | Yes |
| POST | `/api/farms` | Create new farm | Yes |
| PUT | `/api/farms/:id` | Update farm | Yes |
| DELETE | `/api/farms/:id` | Delete farm | Yes |
| GET | `/api/farms/:id/crops` | Get farm crops | Yes |
| GET | `/api/farms/:id/sensors` | Get farm sensors | Yes |
| GET | `/api/farms/export` | Export farms to CSV | Yes |

**Example: Create Farm**

**Request:**
```json
POST /api/farms
{
  "name": "Green Valley Farm",
  "location": "California, USA",
  "area": 250.5,
  "owner_id": 1,
  "company_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 10,
    "name": "Green Valley Farm",
    "location": "California, USA",
    "area": 250.5,
    "owner_id": 1,
    "company_id": 1,
    "created_at": "2025-01-18T00:00:00Z"
  }
}
```

### 4.3 Plant Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/plants` | List all plants | Yes |
| GET | `/api/plants/:id` | Get plant details | Yes |
| POST | `/api/plants` | Create new plant | Yes |
| PUT | `/api/plants/:id` | Update plant | Yes |
| DELETE | `/api/plants/:id` | Delete plant | Yes |
| GET | `/api/plants/:id/diseases` | Get plant diseases | Yes |

### 4.4 Disease Diagnosis Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/diagnosis` | Submit image for diagnosis | Yes |
| GET | `/api/diagnosis` | List diagnosis history | Yes |
| GET | `/api/diagnosis/:id` | Get diagnosis details | Yes |
| DELETE | `/api/diagnosis/:id` | Delete diagnosis | Yes |

**Example: Submit Diagnosis**

**Request:**
```json
POST /api/diagnosis
Content-Type: multipart/form-data

{
  "image": <file>,
  "plant_id": 5,
  "farm_id": 10
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 100,
    "image_url": "/uploads/diagnosis/image_100.jpg",
    "result": {
      "disease": "Leaf Blight",
      "confidence": 0.94,
      "severity": "moderate",
      "treatment": "Apply fungicide..."
    },
    "plant_id": 5,
    "farm_id": 10,
    "created_at": "2025-01-18T00:00:00Z"
  }
}
```

### 4.5 User Management Endpoints (Admin)

| Method | Endpoint | Description | Auth Required | Permission |
|--------|----------|-------------|---------------|------------|
| GET | `/api/users` | List all users | Yes | ADMIN |
| GET | `/api/users/:id` | Get user details | Yes | ADMIN |
| POST | `/api/users` | Create new user | Yes | ADMIN |
| PUT | `/api/users/:id` | Update user | Yes | ADMIN |
| DELETE | `/api/users/:id` | Delete user | Yes | ADMIN |
| PUT | `/api/users/:id/permissions` | Update user permissions | Yes | ADMIN |

### 4.6 Dashboard & Analytics Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/dashboard/stats` | Get dashboard statistics | Yes |
| GET | `/api/analytics/farms` | Farm analytics | Yes |
| GET | `/api/analytics/crops` | Crop analytics | Yes |
| GET | `/api/analytics/diseases` | Disease analytics | Yes |

---

## 5. Error Handling

### 5.1 HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### 5.2 Error Codes

| Code | Description |
|------|-------------|
| `AUTH_INVALID_CREDENTIALS` | Invalid email or password |
| `AUTH_TOKEN_EXPIRED` | Access token has expired |
| `AUTH_TOKEN_INVALID` | Invalid or malformed token |
| `VALIDATION_ERROR` | Input validation failed |
| `RESOURCE_NOT_FOUND` | Requested resource not found |
| `PERMISSION_DENIED` | Insufficient permissions |
| `RATE_LIMIT_EXCEEDED` | Too many requests |

---

## 6. Rate Limiting

**Limits:**
- **Anonymous:** 100 requests/hour
- **Authenticated:** 1000 requests/hour
- **Admin:** 5000 requests/hour

**Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642550400
```

---

**For complete interactive API documentation, visit:** `http://localhost:5000/docs` (Swagger UI)

