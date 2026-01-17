# 🔧 PORT CONFIGURATION & DEPLOYMENT ARCHITECTURE
# تكوين المنافذ وهندسة النشر - Gaara ERP v12

**Document Date:** January 15, 2026  
**Status:** ✅ **Architecture Clarified**  
**Purpose:** Define port assignments and deployment architecture for Gaara ERP v12

---

## 🎯 EXECUTIVE SUMMARY

Gaara ERP v12 uses a **dual-backend microservices architecture**:
- **Django Core** (Primary): Full ERP system with 80+ modules
- **Flask Inventory** (Supplementary): Specialized inventory/warehouse management API

This document clarifies the port configuration, Nginx routing, and deployment architecture to eliminate confusion and ensure proper setup.

---

## 🏗️ ARCHITECTURE OVERVIEW

```
                        Internet
                           │
                           ▼
                    ┌──────────────┐
                    │  Nginx Proxy │
                    │   Port 80    │
                    │  (Reverse)   │
                    └──────────────┘
                           │
           ┌───────────────┴────────────────┐
           │                                │
           ▼                                ▼
    Path: /erp/*                     Path: /erp/api/*
           │                                │
           ▼                                ▼
┌─────────────────────┐          ┌──────────────────────┐
│  Frontend (React)   │          │   Backend APIs       │
│  Container: gaara_  │          │   (Django + Flask)   │
│  frontend           │          │                      │
│  Internal: 80       │          │   Django: 8000       │
│  External: 5501     │          │   Flask:  5001       │
└─────────────────────┘          └──────────────────────┘
           │                                │
           │                                ▼
           │                       ┌────────────────┐
           │                       │   PostgreSQL   │
           │                       │   Port: 5432   │
           │                       │   (Internal)   │
           │                       │   10502 (Ext)  │
           │                       └────────────────┘
           │                                │
           │                                ▼
           │                       ┌────────────────┐
           │                       │     Redis      │
           │                       │   Port: 6379   │
           │                       │   (Internal)   │
           │                       │   6375 (Ext)   │
           │                       └────────────────┘
           │
           └──────────────────────────┐
                                      ▼
                            ┌─────────────────┐
                            │   ML Service    │
                            │   Port: 5101    │
                            │                 │
                            │   AI Service    │
                            │   Port: 5601    │
                            └─────────────────┘
```

---

## 📊 PORT ASSIGNMENT TABLE

### **Production Port Assignments**

| Service | Container Name | Internal Port | External Port | Purpose |
|---------|---------------|---------------|---------------|---------|
| **Nginx** | nginx | 80, 443 | 80, 443 | Reverse proxy |
| **Django Backend** | gaara_django | 8000 | 8000 | Django ERP API |
| **Flask Backend** | gaara_backend | 5001 | 5001 | Flask Inventory API |
| **Frontend** | gaara_frontend | 80 | 5501 | React UI (dev: 5505) |
| **ML Service** | gaara_ml | 5101 | 5101 | Machine Learning API |
| **AI Service** | gaara_ai | 5601 | 5601 | AI Agents API |
| **PostgreSQL** | gaara_postgres | 5432 | 10502 | Primary database |
| **Redis** | gaara_redis | 6379 | 6375 | Cache & message queue |

### **Development Port Assignments**

| Service | Port | Purpose | Access URL |
|---------|------|---------|------------|
| **Django Dev Server** | 8000 | Django development | http://localhost:8000 |
| **Flask Dev Server** | 5001 | Flask development | http://localhost:5001 |
| **Frontend Dev (Vite)** | 5505 | React development | http://localhost:5505 |
| **ML Dev** | 5101 | ML development | http://localhost:5101 |
| **AI Dev** | 5601 | AI development | http://localhost:5601 |
| **PostgreSQL** | 5432 | Database (local) | localhost:5432 |
| **Redis** | 6379 | Cache (local) | localhost:6379 |

---

## 🔀 NGINX ROUTING CONFIGURATION

### **Primary Configuration (Path-Based Routing)**

**Location:** `D:\Ai_Project\nginx\conf.d\default.conf`

```nginx
# Main server block
server {
    listen 80;
    server_name localhost;
    client_max_body_size 100M;

    # Health check
    location /health {
        access_log off;
        return 200 "Healthy\n";
        add_header Content-Type text/plain;
    }

    # ==========================================
    # Gaara ERP - Frontend
    # ==========================================
    location /erp/ {
        set $erp_frontend gaara_frontend:80;
        rewrite ^/erp/(.*) /$1 break;
        
        proxy_pass http://$erp_frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # ==========================================
    # Gaara ERP - Backend API (Django Primary)
    # ==========================================
    location /erp/api/ {
        set $erp_backend gaara_django:8000;
        rewrite ^/erp/api/(.*) /api/$1 break;
        
        proxy_pass http://$erp_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # ==========================================
    # Gaara ERP - Flask Inventory API
    # ==========================================
    location /erp/inventory/api/ {
        set $erp_flask gaara_backend:5001;
        rewrite ^/erp/inventory/api/(.*) /api/$1 break;
        
        proxy_pass http://$erp_flask;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🐳 DOCKER COMPOSE CONFIGURATION

### **Production Deployment**

**File:** `docker-compose.prod.yml`

```yaml
version: '3.8'

services:
  # ==========================================
  # Django Backend (Primary ERP)
  # ==========================================
  gaara_django:
    build:
      context: ./gaara_erp
      dockerfile: Dockerfile.prod
    container_name: gaara_django
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=gaara_erp.settings.prod
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@gaara_postgres:5432/${POSTGRES_DB}
      - REDIS_URL=redis://gaara_redis:6379/0
    depends_on:
      - gaara_postgres
      - gaara_redis
    volumes:
      - ./gaara_erp/media:/app/media
      - ./gaara_erp/staticfiles:/app/staticfiles
    networks:
      - gaara_network
    restart: unless-stopped

  # ==========================================
  # Flask Backend (Inventory API)
  # ==========================================
  gaara_backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: gaara_backend
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${FLASK_SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DATABASE_URL=${FLASK_DATABASE_URL}
    depends_on:
      - gaara_postgres
      - gaara_redis
    networks:
      - gaara_network
    restart: unless-stopped

  # ==========================================
  # Frontend (React)
  # ==========================================
  gaara_frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: gaara_frontend
    ports:
      - "5501:80"
    environment:
      - REACT_APP_API_URL=/erp/api
      - REACT_APP_INVENTORY_API_URL=/erp/inventory/api
    networks:
      - gaara_network
    restart: unless-stopped

  # ==========================================
  # ML Service
  # ==========================================
  gaara_ml:
    build:
      context: ./ml_service
      dockerfile: Dockerfile
    container_name: gaara_ml
    ports:
      - "5101:5101"
    environment:
      - MODEL_PATH=/app/models
    volumes:
      - ./ml_service/models:/app/models
    networks:
      - gaara_network
    restart: unless-stopped

  # ==========================================
  # AI Service
  # ==========================================
  gaara_ai:
    build:
      context: ./ai_service
      dockerfile: Dockerfile
    container_name: gaara_ai
    ports:
      - "5601:5601"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AI_MODEL=gpt-4
    networks:
      - gaara_network
    restart: unless-stopped

  # ==========================================
  # PostgreSQL Database
  # ==========================================
  gaara_postgres:
    image: postgres:15-alpine
    container_name: gaara_postgres
    ports:
      - "10502:5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/backups:/backups
    networks:
      - gaara_network
    restart: unless-stopped

  # ==========================================
  # Redis Cache & Queue
  # ==========================================
  gaara_redis:
    image: redis:7-alpine
    container_name: gaara_redis
    ports:
      - "6375:6379"
    volumes:
      - redis_data:/data
    networks:
      - gaara_network
    restart: unless-stopped
    command: redis-server --appendonly yes

  # ==========================================
  # Nginx Reverse Proxy
  # ==========================================
  nginx:
    image: nginx:alpine
    container_name: gaara_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
      - ./gaara_erp/staticfiles:/static
      - ./gaara_erp/media:/media
    depends_on:
      - gaara_django
      - gaara_backend
      - gaara_frontend
    networks:
      - gaara_network
    restart: unless-stopped

networks:
  gaara_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

---

## 🔐 ENVIRONMENT VARIABLES

### **Required Environment Variables**

Create `.env` file in project root:

```bash
# ==========================================
# Django Configuration
# ==========================================
SECRET_KEY=your-super-secret-django-key-change-in-production
DJANGO_SETTINGS_MODULE=gaara_erp.settings.prod
DEBUG=False
ALLOWED_HOSTS=app.gaara-erp.com,admin.gaara-erp.com

# ==========================================
# Flask Configuration
# ==========================================
FLASK_SECRET_KEY=your-flask-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_REFRESH_SECRET_KEY=your-jwt-refresh-secret-key-change-in-production
FLASK_ENV=production

# ==========================================
# Database Configuration
# ==========================================
POSTGRES_DB=gaara_erp_prod
POSTGRES_USER=gaara_admin
POSTGRES_PASSWORD=your-super-strong-password-here
DATABASE_URL=postgresql://gaara_admin:your-password@gaara_postgres:5432/gaara_erp_prod
FLASK_DATABASE_URL=postgresql://gaara_admin:your-password@gaara_postgres:5432/gaara_erp_inventory

# ==========================================
# Redis Configuration
# ==========================================
REDIS_URL=redis://gaara_redis:6379/0

# ==========================================
# AI/ML Configuration
# ==========================================
OPENAI_API_KEY=sk-your-openai-api-key-here
PYBROPS_API_KEY=your-pybrops-api-key-here

# ==========================================
# External APIs
# ==========================================
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1

# ==========================================
# Application Configuration
# ==========================================
APP_VERSION=1.0.0
APP_MODE=prod
LOG_LEVEL=INFO
```

---

## 🚀 DEPLOYMENT INSTRUCTIONS

### **Method 1: Docker Compose (Recommended)**

#### **Step 1: Prepare Environment**

```bash
# Clone repository
cd D:\Ai_Project\5-gaara_erp

# Create production environment file
cp .env.example .env

# Edit .env with production values
notepad .env

# Generate secret keys
python backend/scripts/generate_secrets.py
```

#### **Step 2: Build Images**

```bash
# Build all production images
docker-compose -f docker-compose.prod.yml build

# Or build individually
docker-compose -f docker-compose.prod.yml build gaara_django
docker-compose -f docker-compose.prod.yml build gaara_backend
docker-compose -f docker-compose.prod.yml build gaara_frontend
```

#### **Step 3: Start Services**

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Or start individually
docker-compose -f docker-compose.prod.yml up -d gaara_postgres
docker-compose -f docker-compose.prod.yml up -d gaara_redis
docker-compose -f docker-compose.prod.yml up -d gaara_django
docker-compose -f docker-compose.prod.yml up -d gaara_backend
docker-compose -f docker-compose.prod.yml up -d gaara_frontend
docker-compose -f docker-compose.prod.yml up -d nginx
```

#### **Step 4: Run Migrations**

```bash
# Django migrations
docker-compose -f docker-compose.prod.yml exec gaara_django python manage.py migrate

# Flask migrations (if using Alembic)
docker-compose -f docker-compose.prod.yml exec gaara_backend flask db upgrade
```

#### **Step 5: Create Superuser**

```bash
# Django superuser
docker-compose -f docker-compose.prod.yml exec gaara_django python manage.py createsuperuser
```

#### **Step 6: Collect Static Files**

```bash
# Django static files
docker-compose -f docker-compose.prod.yml exec gaara_django python manage.py collectstatic --noinput
```

#### **Step 7: Verify Deployment**

```bash
# Check all containers are running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Test health endpoint
curl http://localhost/health

# Test Django API
curl http://localhost/erp/api/

# Test Flask API
curl http://localhost/erp/inventory/api/

# Test Frontend
curl http://localhost/erp/
```

---

### **Method 2: Manual Deployment (No Docker)**

#### **Step 1: PostgreSQL Setup**

```bash
# Install PostgreSQL (if not installed)
# Windows: Download from https://www.postgresql.org/download/windows/

# Create database
psql -U postgres
CREATE DATABASE gaara_erp_prod;
CREATE DATABASE gaara_erp_inventory;
CREATE USER gaara_admin WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE gaara_erp_prod TO gaara_admin;
GRANT ALL PRIVILEGES ON DATABASE gaara_erp_inventory TO gaara_admin;
\q
```

#### **Step 2: Redis Setup**

```bash
# Install Redis (if not installed)
# Windows: Download from https://github.com/microsoftarchive/redis/releases

# Start Redis
redis-server
```

#### **Step 3: Django Backend**

```bash
cd D:\Ai_Project\5-gaara_erp\gaara_erp

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
$env:DJANGO_SETTINGS_MODULE="gaara_erp.settings.prod"
$env:SECRET_KEY="your-secret-key"
$env:DATABASE_URL="postgresql://gaara_admin:password@localhost:5432/gaara_erp_prod"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Start Django (use Gunicorn for production)
pip install gunicorn
gunicorn gaara_erp.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

#### **Step 4: Flask Backend**

```bash
cd D:\Ai_Project\5-gaara_erp\backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
$env:FLASK_ENV="production"
$env:SECRET_KEY="your-flask-secret"
$env:JWT_SECRET_KEY="your-jwt-secret"
$env:DATABASE_URL="postgresql://gaara_admin:password@localhost:5432/gaara_erp_inventory"

# Start Flask (use Gunicorn for production)
pip install gunicorn
gunicorn src.unified_server:app --bind 0.0.0.0:5001 --workers 4
```

#### **Step 5: Frontend**

```bash
cd D:\Ai_Project\5-gaara_erp\frontend

# Install dependencies
npm install

# Build production bundle
npm run build

# Serve with a static file server (or Nginx)
npm install -g serve
serve -s dist -l 5501
```

#### **Step 6: Nginx Setup**

```nginx
# Copy Nginx configuration
copy D:\Ai_Project\nginx\conf.d\default.conf C:\nginx\conf\

# Test configuration
nginx -t

# Start Nginx
nginx

# Or reload if already running
nginx -s reload
```

---

## 🔍 VERIFICATION & TESTING

### **Health Checks**

```bash
# Nginx health
curl http://localhost/health

# Django health
curl http://localhost/erp/api/health/

# Flask health
curl http://localhost/erp/inventory/api/health

# PostgreSQL
psql -h localhost -p 10502 -U gaara_admin -d gaara_erp_prod -c "SELECT 1"

# Redis
redis-cli -p 6375 ping
```

### **API Testing**

```bash
# Django API - List users (requires auth)
curl http://localhost/erp/api/users/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Flask API - List products
curl http://localhost/erp/inventory/api/products/

# Test CORS
curl http://localhost/erp/api/ \
  -H "Origin: http://localhost:5505" \
  -H "Access-Control-Request-Method: GET" \
  -X OPTIONS -v
```

### **Load Testing**

```bash
# Install Apache Bench
# Windows: Download from Apache Lounge

# Test Django API
ab -n 1000 -c 10 http://localhost/erp/api/health/

# Test Flask API
ab -n 1000 -c 10 http://localhost/erp/inventory/api/health

# Test Frontend
ab -n 1000 -c 10 http://localhost/erp/
```

---

## 🛠️ TROUBLESHOOTING

### **Issue 1: Container Won't Start**

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs gaara_django
docker-compose -f docker-compose.prod.yml logs gaara_backend

# Check environment variables
docker-compose -f docker-compose.prod.yml exec gaara_django env

# Rebuild container
docker-compose -f docker-compose.prod.yml build --no-cache gaara_django
docker-compose -f docker-compose.prod.yml up -d gaara_django
```

### **Issue 2: Database Connection Failed**

```bash
# Check PostgreSQL is running
docker-compose -f docker-compose.prod.yml ps gaara_postgres

# Check connection from Django container
docker-compose -f docker-compose.prod.yml exec gaara_django \
  psql -h gaara_postgres -U gaara_admin -d gaara_erp_prod

# Check DATABASE_URL environment variable
docker-compose -f docker-compose.prod.yml exec gaara_django \
  python -c "import os; print(os.environ.get('DATABASE_URL'))"
```

### **Issue 3: Nginx 502 Bad Gateway**

```bash
# Check backend containers are running
docker-compose -f docker-compose.prod.yml ps

# Check backend logs
docker-compose -f docker-compose.prod.yml logs gaara_django
docker-compose -f docker-compose.prod.yml logs gaara_backend

# Test backend directly (without Nginx)
curl http://localhost:8000/api/health/
curl http://localhost:5001/api/health

# Check Nginx error log
docker-compose -f docker-compose.prod.yml logs nginx

# Restart Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### **Issue 4: CORS Errors**

```bash
# Check CORS settings in Django
# File: gaara_erp/gaara_erp/settings/base.py
# CORS_ALLOWED_ORIGINS should include your frontend URL

# Test CORS headers
curl -H "Origin: http://localhost:5505" \
  -H "Access-Control-Request-Method: GET" \
  -X OPTIONS -v \
  http://localhost/erp/api/

# Should return:
# Access-Control-Allow-Origin: http://localhost:5505
# Access-Control-Allow-Methods: GET, POST, ...
```

### **Issue 5: Static Files Not Loading**

```bash
# Collect static files again
docker-compose -f docker-compose.prod.yml exec gaara_django \
  python manage.py collectstatic --noinput

# Check static files volume
docker-compose -f docker-compose.prod.yml exec nginx ls -la /static

# Check Nginx configuration for static file serving
docker-compose -f docker-compose.prod.yml exec nginx \
  cat /etc/nginx/conf.d/default.conf
```

---

## 📊 MONITORING & LOGS

### **Log Locations**

| Service | Log Location (Container) | Access Method |
|---------|-------------------------|---------------|
| Django | `/app/logs/` | `docker logs gaara_django` |
| Flask | `/app/logs/` | `docker logs gaara_backend` |
| Nginx | `/var/log/nginx/` | `docker logs nginx` |
| PostgreSQL | `/var/log/postgresql/` | `docker logs gaara_postgres` |
| Redis | `/data/` | `docker logs gaara_redis` |

### **View Logs**

```bash
# Real-time logs
docker-compose -f docker-compose.prod.yml logs -f

# Specific service logs
docker-compose -f docker-compose.prod.yml logs -f gaara_django

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 gaara_django

# Since timestamp
docker-compose -f docker-compose.prod.yml logs --since 2026-01-15T10:00:00
```

### **Performance Monitoring**

```bash
# Container stats
docker stats

# Specific container
docker stats gaara_django

# Database queries (Django)
docker-compose -f docker-compose.prod.yml exec gaara_django \
  python manage.py shell
>>> from django.db import connection
>>> print(connection.queries)

# Redis stats
docker-compose -f docker-compose.prod.yml exec gaara_redis redis-cli info stats
```

---

## ✅ POST-DEPLOYMENT CHECKLIST

### **Security:**
- [ ] All SECRET_KEY values are unique and strong
- [ ] Environment variables are not committed to Git
- [ ] HTTPS/SSL certificates are installed
- [ ] Firewall rules are configured
- [ ] Database passwords are strong
- [ ] DEBUG=False in production

### **Configuration:**
- [ ] All services start successfully
- [ ] Health checks pass
- [ ] API endpoints are accessible
- [ ] Frontend loads correctly
- [ ] Database migrations applied
- [ ] Static files collected and served

### **Testing:**
- [ ] Login/authentication works
- [ ] API requests succeed
- [ ] Database reads/writes work
- [ ] Redis caching works
- [ ] Email notifications work (if configured)

### **Monitoring:**
- [ ] Log aggregation configured
- [ ] Error tracking set up (Sentry)
- [ ] Performance monitoring active
- [ ] Backup jobs scheduled
- [ ] Health check monitoring active

### **Documentation:**
- [ ] Deployment runbook created
- [ ] API documentation published
- [ ] User manual available
- [ ] Admin guide available

---

## 🎬 CONCLUSION

This document provides:
- ✅ Clear port assignments for all services
- ✅ Nginx routing configuration
- ✅ Docker Compose production setup
- ✅ Deployment instructions (Docker & Manual)
- ✅ Health check procedures
- ✅ Troubleshooting guide
- ✅ Post-deployment checklist

**Key Decisions Made:**
1. **Django (8000)** is the PRIMARY backend API
2. **Flask (5001)** is the SUPPLEMENTARY inventory API
3. **Path-based routing** via Nginx is the STANDARD approach
4. **PostgreSQL** is the REQUIRED production database (no SQLite3)

**Next Steps:**
1. Set up production environment variables
2. Build Docker images
3. Deploy to staging environment
4. Run smoke tests
5. Deploy to production

---

*Document Generated: January 15, 2026*  
*Version: 1.0.0*  
*Classification: DEPLOYMENT ARCHITECTURE*  
*Owner: DevOps Team*

---

**🚀 Ready for deployment once PostgreSQL is set up and test coverage reaches 80%+**
