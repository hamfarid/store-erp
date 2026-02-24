# 🔌 API Connection Documentation

**Version:** 2.0.0  
**Last Updated:** 2026-01-17

---

## 📋 Overview

This document describes how the frontend connects to the backend API in Store ERP.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     React Pages                          │   │
│  │  (Dashboard, POS, Products, Lots, Reports, Settings)    │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │                  Services Layer                          │   │
│  │  authService | productService | lotService | ...         │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │                    API Client                            │   │
│  │  - Token Management                                      │   │
│  │  - Request/Response Handling                             │   │
│  │  - Error Handling                                        │   │
│  │  - Auto Token Refresh                                    │   │
│  └────────────────────────┬────────────────────────────────┘   │
└───────────────────────────│────────────────────────────────────┘
                            │ HTTP/HTTPS
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                         NGINX                                  │
│  - Reverse Proxy                                               │
│  - Rate Limiting                                               │
│  - SSL Termination                                             │
│  - Load Balancing                                              │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────┐
│                         BACKEND                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   Flask Application                      │  │
│  │  - Routes (95+)                                          │  │
│  │  - Services (36+)                                        │  │
│  │  - Middleware (10+)                                      │  │
│  └────────────────────────┬────────────────────────────────┘  │
│                           │                                    │
│  ┌────────────────────────▼────────────────────────────────┐  │
│  │                   SQLAlchemy ORM                         │  │
│  │  - Models (70+)                                          │  │
│  │  - Migrations                                            │  │
│  └────────────────────────┬────────────────────────────────┘  │
│                           │                                    │
│  ┌────────────────────────▼────────────────────────────────┐  │
│  │                     Database                             │  │
│  │  SQLite (Dev) / PostgreSQL (Prod)                        │  │
│  └─────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Environment Variables

#### Frontend (.env)
```env
# API Configuration
VITE_API_BASE=http://localhost:6001
VITE_API_TIMEOUT=30000

# Feature Flags
VITE_ENABLE_2FA=true
VITE_ENABLE_DEBUG=false
```

#### Backend (.env)
```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///instance/inventory.db
# Or for production:
# DATABASE_URL=postgresql://user:pass@host:5432/store_erp

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=604800

# CORS
CORS_ORIGINS=http://localhost:6501,http://localhost:5173
```

### Port Configuration (`config/ports.json`)
```json
{
  "services": {
    "backend": {
      "port": 6001,
      "url": "http://localhost:6001"
    },
    "frontend": {
      "port": 6501,
      "url": "http://localhost:6501"
    }
  }
}
```

---

## 📡 API Client

### Location
`frontend/src/services/apiClient.js`

### Features
- ✅ Automatic token management
- ✅ Token refresh on 401
- ✅ Request/response interceptors
- ✅ Error handling
- ✅ File upload support
- ✅ Batch requests
- ✅ Health checks

### Usage Example

```javascript
import apiClient from './services/apiClient';

// GET request
const products = await apiClient.get('/api/products', { 
  page: 1, 
  limit: 10 
});

// POST request
const newProduct = await apiClient.post('/api/products', {
  name: 'Product Name',
  sku: 'SKU-001',
  price: 100
});

// PUT request
const updated = await apiClient.put('/api/products/1', {
  name: 'Updated Name'
});

// DELETE request
await apiClient.delete('/api/products/1');

// File upload
await apiClient.uploadFile('/api/products/1/image', file);

// Download file
await apiClient.downloadFile('/api/reports/export', 'report.xlsx');
```

---

## 🔐 Authentication Flow

### Login
```
1. User enters credentials
2. POST /api/auth/login { username, password }
3. Backend validates credentials
4. Returns { access_token, refresh_token, user }
5. Frontend stores tokens in localStorage
6. All subsequent requests include Authorization header
```

### Token Refresh
```
1. API request returns 401
2. apiClient automatically calls /api/auth/refresh
3. New tokens received and stored
4. Original request retried with new token
5. If refresh fails → redirect to login
```

### 2FA Flow
```
1. Login returns { requires_2fa: true }
2. Frontend shows 2FA input
3. POST /api/auth/2fa/verify { code }
4. Returns tokens on success
```

---

## 📚 Service Layer

### Available Services

| Service | File | Purpose |
|---------|------|---------|
| `authService` | `authService.js` | Authentication, 2FA, sessions |
| `userService` | `userService.js` | User & role management |
| `productService` | `productService.js` | Product CRUD |
| `categoryService` | `categoryService.js` | Category management |
| `lotService` | `lotService.js` | Lot/batch management |
| `warehouseService` | `warehouseService.js` | Warehouse operations |
| `invoiceService` | `invoiceService.js` | Invoice management |
| `posService` | `posService.js` | POS operations |
| `reportsService` | `reportsService.js` | Report generation |
| `settingsService` | `settingsService.js` | System settings |
| `customerService` | `customerService.js` | Customer management |
| `purchaseService` | `purchaseService.js` | Purchase orders |

### Usage in Components

```jsx
import { productService, lotService } from '../services';

const ProductList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const data = await productService.getProducts({ 
          is_active: true 
        });
        setProducts(data.items);
      } catch (error) {
        toast.error('Failed to load products');
      }
    };
    loadProducts();
  }, []);

  return (/* JSX */);
};
```

---

## 🔄 Request/Response Format

### Request Headers
```http
GET /api/products HTTP/1.1
Host: localhost:6001
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json
Accept: application/json
```

### Success Response
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "pages": 10
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "name": "Name is required"
    }
  }
}
```

---

## 🚨 Error Handling

### HTTP Status Codes

| Code | Meaning | Handling |
|------|---------|----------|
| 200 | Success | Return data |
| 201 | Created | Return created resource |
| 400 | Bad Request | Show validation errors |
| 401 | Unauthorized | Refresh token or redirect to login |
| 403 | Forbidden | Show permission error |
| 404 | Not Found | Show not found message |
| 422 | Validation Error | Show field errors |
| 429 | Rate Limited | Show retry message |
| 500 | Server Error | Show generic error |

### Error Handler Example

```javascript
try {
  await productService.createProduct(data);
  toast.success('Product created!');
} catch (error) {
  if (error.response?.status === 422) {
    // Validation error
    setErrors(error.response.data.details);
  } else if (error.response?.status === 403) {
    toast.error('You do not have permission');
  } else {
    toast.error(error.message || 'An error occurred');
  }
}
```

---

## 🔒 CORS Configuration

### Backend (Flask)
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:6501",
            "http://localhost:5173"
        ],
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
```

### Nginx
```nginx
location /api/ {
    add_header 'Access-Control-Allow-Origin' '$http_origin' always;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, PATCH, DELETE, OPTIONS' always;
    add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;
    
    if ($request_method = 'OPTIONS') {
        return 204;
    }
    
    proxy_pass http://backend:6001;
}
```

---

## 🧪 Testing API Connections

### Health Check
```bash
curl http://localhost:6001/api/health
```

### Test Authentication
```bash
# Login
curl -X POST http://localhost:6001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# With token
curl http://localhost:6001/api/products \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Frontend Health Check
```javascript
import { healthCheckServices } from './services';

const status = await healthCheckServices();
console.log(status);
// { status: 'healthy', data: {...} }
```

---

## 📊 API Endpoints Summary

| Category | Endpoints | Count |
|----------|-----------|-------|
| Auth | `/api/auth/*` | 12 |
| Users | `/api/users/*` | 15 |
| Products | `/api/products/*` | 10 |
| Categories | `/api/categories/*` | 8 |
| Lots | `/api/lots/*` | 12 |
| Warehouses | `/api/warehouses/*` | 10 |
| Invoices | `/api/invoices/*` | 15 |
| POS | `/api/pos/*` | 8 |
| Reports | `/api/reports/*` | 12 |
| Settings | `/api/settings/*` | 10 |
| **Total** | | **100+** |

---

*API Connection Documentation - Store ERP v2.0.0*
