# 🔗 Integration Guide - Store ERP v2.0.0

**Phase 4: Integration**
**Generated:** 2026-01-16
**Status:** In Progress

---

## 📋 Overview

This guide covers the integration of all Store ERP components:
- Backend API (Flask) → Port 6001
- Frontend (React/Vite) → Port 6501
- Database (PostgreSQL/SQLite)
- Redis Cache
- Nginx Reverse Proxy

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────────────┐
                    │              NGINX (Port 80)            │
                    │         Reverse Proxy + SSL             │
                    └─────────────────┬───────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│   Frontend    │           │    Backend    │           │  ML/AI APIs   │
│  React/Vite   │           │    Flask      │           │   Optional    │
│  Port: 6501   │           │  Port: 6001   │           │ 6101 / 6601   │
└───────────────┘           └───────┬───────┘           └───────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌───────────┐   ┌───────────┐   ┌───────────┐
            │PostgreSQL │   │   Redis   │   │   Files   │
            │  :5432    │   │   :6379   │   │  Uploads  │
            └───────────┘   └───────────┘   └───────────┘
```

---

## 🚀 Quick Start

### Development Mode

```bash
# 1. Start Backend
cd backend
pip install -r requirements.txt
python app.py
# Running on http://localhost:6001

# 2. Start Frontend (new terminal)
cd frontend
npm install
npm run dev
# Running on http://localhost:6501
```

### Docker Mode

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## ⚙️ Configuration Files

### Frontend Environment (`frontend/env.example.txt`)

```env
# Copy to .env.local for development
VITE_API_BASE=http://localhost:6001
VITE_APP_NAME=Store ERP
VITE_ENABLE_2FA=true
VITE_ENABLE_DARK_MODE=true
```

### Backend Environment (`backend/env.example.txt`)

```env
# Copy to .env
FLASK_ENV=development
DATABASE_URL=sqlite:///instance/store.db
JWT_SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:6501
PORT=6001
```

### Vite Proxy Configuration

The frontend uses Vite's proxy feature to forward API requests:

```javascript
// vite.config.js
server: {
  port: 6501,
  proxy: {
    '/api': {
      target: 'http://localhost:6001',
      changeOrigin: true
    }
  }
}
```

---

## 🔌 API Integration

### API Client Usage

```javascript
import apiClient from '@/services/apiClient';

// GET request
const products = await apiClient.get('/api/products');

// POST request
const newProduct = await apiClient.post('/api/products', {
  name: 'Product Name',
  price: 100
});

// With authentication (automatic)
// Token is automatically included from localStorage
```

### API Endpoints Summary

| Module | Base Path | Methods |
|--------|-----------|---------|
| Auth | `/api/auth` | login, logout, refresh, register |
| Products | `/api/products` | CRUD |
| Categories | `/api/categories` | CRUD |
| Customers | `/api/customers` | CRUD |
| Suppliers | `/api/suppliers` | CRUD |
| Invoices | `/api/invoices` | CRUD + print |
| Lots | `/api/lots` | CRUD + expire check |
| Reports | `/api/reports` | generate, export |
| Settings | `/api/settings` | get, update |
| Users | `/api/users` | CRUD + roles |

---

## 🐳 Docker Integration

### Services

| Service | Container | Port | Health Check |
|---------|-----------|------|--------------|
| Backend | store_backend | 6001:5000 | `/api/health` |
| Frontend | store_frontend | 6501:80 | `/` |
| Database | store_database | 12502:5432 | pg_isready |
| Redis | store_redis | 6376:6379 | redis-cli ping |
| Nginx | store_nginx | 80:80 | `/health` |

### Docker Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart a service
docker-compose restart backend

# Stop all
docker-compose down

# Remove volumes (CAUTION: deletes data)
docker-compose down -v
```

---

## 🌐 Nginx Configuration

### Key Features

- Reverse proxy for backend API
- Static file serving for frontend
- Rate limiting for API endpoints
- Stricter rate limiting for login
- CORS headers
- Gzip compression
- Security headers
- WebSocket support

### Routes

| Path | Destination | Notes |
|------|-------------|-------|
| `/` | Frontend (static) | React SPA |
| `/api/*` | Backend | API proxy |
| `/ws/*` | Backend | WebSocket |
| `/ml/*` | ML Service | Optional |
| `/ai/*` | AI Service | Optional |
| `/health` | Nginx | Health check |

---

## 🔒 Security Integration

### Authentication Flow

```
1. User submits credentials → /api/auth/login
2. Backend validates → Returns JWT tokens
3. Frontend stores tokens in localStorage
4. API requests include Authorization header
5. Token expiry → Auto refresh using refresh_token
6. Logout → Clear tokens, redirect to login
```

### CORS Configuration

Backend allows requests from:
- `http://localhost:6501` (development)
- `http://localhost:5173` (Vite default)
- Production domain (configurable)

### Security Headers (Nginx)

```nginx
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
```

---

## 🧪 Testing Integration

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=src
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# E2E tests with Playwright
cd e2e
npm test
```

---

## 📊 Monitoring

### Health Endpoints

| Endpoint | Service | Response |
|----------|---------|----------|
| `GET /api/health` | Backend | `{"status": "healthy"}` |
| `GET /health` | Nginx | `healthy` |
| `GET /` | Frontend | HTML page |

### Logs Location

| Service | Log Path |
|---------|----------|
| Backend | `backend/logs/app.log` |
| Frontend | Browser console |
| Nginx | `/var/log/nginx/store_*.log` |
| Docker | `docker-compose logs` |

---

## 🔧 Troubleshooting

### Common Issues

#### CORS Error
```
Check CORS_ORIGINS in backend .env
Ensure frontend origin is listed
```

#### API Connection Failed
```
1. Check backend is running on port 6001
2. Verify VITE_API_BASE in frontend .env
3. Check Vite proxy configuration
```

#### Database Connection Error
```
1. Check DATABASE_URL
2. Verify database service is running
3. Run migrations: flask db upgrade
```

#### Docker Network Error
```
# Create the network if not exists
docker network create Ai_project

# Restart containers
docker-compose down && docker-compose up -d
```

---

## 📝 Checklist

### Pre-Deployment

- [ ] Environment files configured
- [ ] Database migrations applied
- [ ] JWT secrets set (not defaults)
- [ ] CORS origins configured
- [ ] SSL certificates ready (production)
- [ ] Docker network created
- [ ] All tests passing

### Post-Deployment

- [ ] Health endpoints responding
- [ ] Login/logout working
- [ ] API requests proxied correctly
- [ ] Static assets loading
- [ ] Logs accessible
- [ ] Backups configured

---

## 📈 Performance Tips

1. **Enable Redis caching** for session and API responses
2. **Use CDN** for static assets in production
3. **Enable Gzip** compression (already in Nginx config)
4. **Set proper cache headers** for static files
5. **Use connection pooling** for database
6. **Monitor with** health checks and logging

---

*Integration by Store ERP v2.0.0 - Phoenix Rising*
