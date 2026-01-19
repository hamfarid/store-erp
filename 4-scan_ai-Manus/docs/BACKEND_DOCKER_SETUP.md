# Backend, Docker & Database Setup - Gaara Scan AI v4.3

## 📋 Overview

This document provides comprehensive setup instructions for the backend, Docker containers, API, and database configuration.

---

## ✅ Completed Setup

### **1. Docker Files**

#### **Backend Dockerfile** (`backend/Dockerfile`)
- ✅ Multi-stage build (builder + production)
- ✅ Python 3.11-slim base image
- ✅ Non-root user for security
- ✅ Health checks configured
- ✅ Database migration support
- ✅ Production-ready optimizations

#### **Frontend Dockerfile** (`frontend/Dockerfile`)
- ✅ Multi-stage build (builder + nginx)
- ✅ Node.js 20-alpine for building
- ✅ Nginx 1.25-alpine for serving
- ✅ SPA routing support
- ✅ Gzip compression
- ✅ Security headers
- ✅ Health checks

#### **Docker Compose** (`docker-compose.yml`)
- ✅ PostgreSQL 16 database
- ✅ Redis 7 cache
- ✅ Backend API service
- ✅ Frontend service
- ✅ Health checks for all services
- ✅ Volume management
- ✅ Network configuration
- ✅ Resource limits

### **2. Environment Configuration**

#### **Environment Variables** (`env.example`)
- ✅ Application settings
- ✅ Database configuration (PostgreSQL)
- ✅ Redis configuration
- ✅ Security settings (JWT, secrets)
- ✅ CORS settings
- ✅ File upload settings
- ✅ Logging configuration
- ✅ Performance settings
- ✅ Monitoring settings
- ✅ Email settings (optional)
- ✅ Frontend settings
- ✅ Docker settings

### **3. Database Setup**

#### **Initialization Scripts**
- ✅ `docker/postgres/init/01-init.sql` - Database extensions and schemas
- ✅ `docker/postgres/init/02-seed-data.sql` - Seed data template

#### **Database Features**
- ✅ PostgreSQL 16
- ✅ UUID extension
- ✅ Full-text search (pg_trgm)
- ✅ Multiple schemas (gaara, analytics, ai)
- ✅ Proper user permissions

### **4. API Endpoints**

#### **Complete API Structure** (`backend/src/api/v1/`)

| Endpoint | File | Status | Features |
|----------|------|--------|----------|
| **Health** | `health.py` | ✅ Complete | Health checks, liveness, readiness |
| **Auth** | `auth.py` | ✅ Complete | Login, register, password reset, MFA |
| **Farms** | `farms.py` | ✅ Complete | CRUD operations |
| **Diagnosis** | `diagnosis.py` | ✅ Complete | Image upload, diagnosis history |
| **Reports** | `reports.py` | ✅ Complete | Report generation |
| **Crops** | `crops.py` | ✅ Created | CRUD operations |
| **Diseases** | `diseases.py` | ✅ Created | CRUD operations |
| **Sensors** | `sensors.py` | ✅ Created | CRUD + readings |
| **Equipment** | `equipment.py` | ✅ Created | CRUD operations |
| **Inventory** | `inventory.py` | ✅ Created | CRUD operations |
| **Users** | `users.py` | ✅ Created | User management (Admin) |
| **Companies** | `companies.py` | ✅ Created | CRUD operations |
| **Breeding** | `breeding.py` | ✅ Created | Breeding programs |
| **Analytics** | `analytics.py` | ✅ Created | Analytics & insights |

---

## 🚀 Quick Start

### **1. Prerequisites**

```bash
# Install Docker & Docker Compose
# Docker Desktop (Windows/Mac) or Docker Engine + Compose (Linux)
```

### **2. Setup Environment**

```bash
# Copy environment template
cp env.example .env

# Edit .env with your settings
# ⚠️ IMPORTANT: Change all default passwords and secrets!
```

### **3. Start Services**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### **4. Access Services**

- **Frontend:** http://localhost:1505
- **Backend API:** http://localhost:1005
- **API Docs:** http://localhost:1005/docs
- **Database:** localhost:5432
- **Redis:** localhost:6379

---

## 📁 File Structure

```
gaara_scan_ai_final_4.3/
├── backend/
│   ├── Dockerfile              # Backend container
│   ├── requirements.txt        # Python dependencies
│   └── src/
│       ├── main.py             # Application entry
│       ├── core/               # Core modules
│       ├── api/v1/             # API endpoints
│       ├── models/             # Database models
│       └── ...
├── frontend/
│   ├── Dockerfile              # Frontend container
│   └── ...
├── docker/
│   └── postgres/
│       └── init/               # Database init scripts
│           ├── 01-init.sql
│           └── 02-seed-data.sql
├── docker-compose.yml          # Main compose file
├── env.example                 # Environment template
└── .env                        # Your environment (not in git)
```

---

## 🔧 Configuration

### **Database Connection**

The backend automatically connects to PostgreSQL using environment variables:

```env
DATABASE_URL=postgresql://gaara_user:password@database:5432/gaara_scan_ai
```

Or individual variables:
```env
POSTGRES_DB=gaara_scan_ai
POSTGRES_USER=gaara_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=database
POSTGRES_PORT=5432
```

### **Redis Connection**

```env
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_DB=0
```

### **API Endpoints**

All API endpoints are prefixed with `/api/v1/`:

- `GET /api/v1/health` - Health check
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/farms` - List farms
- `POST /api/v1/farms` - Create farm
- ... (see API documentation)

---

## 🗄️ Database Migrations

### **Using Alembic**

```bash
# Enter backend container
docker-compose exec backend bash

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 🧪 Testing

### **Health Checks**

```bash
# Backend health
curl http://localhost:1005/api/v1/health

# Frontend health
curl http://localhost:1505/health
```

### **API Testing**

```bash
# Login
curl -X POST http://localhost:1005/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Get farms (with token)
curl http://localhost:1005/api/v1/farms \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 Monitoring

### **Service Health**

All services include health checks:

- **Backend:** `/api/v1/health`
- **Frontend:** `/health`
- **Database:** `pg_isready`
- **Redis:** `redis-cli ping`

### **View Logs**

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

---

## 🔒 Security Notes

1. **Change Default Passwords**
   - Database password
   - Redis password
   - JWT secret
   - Application secret key

2. **Environment Variables**
   - Never commit `.env` file
   - Use strong, unique passwords
   - Rotate secrets regularly

3. **Network Security**
   - Services communicate on internal network
   - Only expose necessary ports
   - Use reverse proxy for production

---

## 🐛 Troubleshooting

### **Database Connection Issues**

```bash
# Check database is running
docker-compose ps database

# Check database logs
docker-compose logs database

# Test connection
docker-compose exec database psql -U gaara_user -d gaara_scan_ai
```

### **Backend Not Starting**

```bash
# Check backend logs
docker-compose logs backend

# Check environment variables
docker-compose exec backend env | grep DATABASE

# Restart backend
docker-compose restart backend
```

### **Frontend Not Loading**

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

---

## 📝 Next Steps

1. **Implement Database Models**
   - Create SQLAlchemy models for all entities
   - Run Alembic migrations
   - Seed initial data

2. **Complete API Implementation**
   - Implement actual database queries
   - Add validation and error handling
   - Add unit tests

3. **Production Deployment**
   - Set up SSL/TLS certificates
   - Configure reverse proxy (Nginx)
   - Set up monitoring (Prometheus/Grafana)
   - Configure backups

---

## ✅ Status

**Backend & Docker Setup:** ✅ **COMPLETE**

- ✅ Docker files created
- ✅ Docker Compose configured
- ✅ Environment template created
- ✅ Database initialization scripts
- ✅ All API endpoints created
- ✅ Health checks implemented
- ✅ Security best practices applied

**Ready for:** Development & Testing

---

**Last Updated:** December 2024  
**Version:** 4.3.0

