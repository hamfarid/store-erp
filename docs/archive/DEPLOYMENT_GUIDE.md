# 🚀 Deployment Guide - Store ERP v2.0.0

**Version:** 2.0.0  
**Status:** Production Ready  
**Last Updated:** January 16, 2026

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Development Setup](#development-setup)
4. [Production Deployment](#production-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Configuration](#configuration)
7. [SSL/HTTPS Setup](#sslhttps-setup)
8. [Monitoring](#monitoring)
9. [Troubleshooting](#troubleshooting)

---

## 📦 Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Storage | 20 GB | 50+ GB SSD |
| OS | Ubuntu 20.04+ / Windows Server 2019+ | Ubuntu 22.04 LTS |

### Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend |
| Node.js | 20+ | Frontend build |
| PostgreSQL | 14+ | Database (production) |
| Nginx | 1.24+ | Reverse proxy |
| Docker | 24+ | Containerization (optional) |

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/your-repo/store-erp.git
cd store-erp

# Create Docker network
docker network create Ai_project

# Start all services
docker-compose up -d

# Access application
# Frontend: http://localhost
# API: http://localhost:6001/api
```

### Option 2: Script Deployment

```bash
# Windows
.\scripts\deploy.ps1 -Environment dev

# Linux/Mac
./scripts/deploy.sh dev
```

---

## 🛠️ Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example.txt .env
# Edit .env with your settings

# Initialize database
flask db upgrade

# Create admin user
python create_admin.py

# Start development server
python app.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp env.example.txt .env.local
# Edit .env.local with your settings

# Start development server
npm run dev
```

### Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:6501 |
| Backend API | http://localhost:6001/api |
| API Health | http://localhost:6001/api/health |

### Default Credentials

```
Username: admin
Password: admin123
```

⚠️ **Change these credentials immediately in production!**

---

## 🏭 Production Deployment

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.11 python3.11-venv nginx postgresql redis-server

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Database Setup

```bash
# Create PostgreSQL database
sudo -u postgres psql

CREATE DATABASE store_db;
CREATE USER store_user WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE store_db TO store_user;
\q
```

### 3. Application Setup

```bash
# Clone repository
cd /opt
sudo git clone https://github.com/your-repo/store-erp.git
sudo chown -R www-data:www-data store-erp
cd store-erp

# Backend setup
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Configure environment
cp env.example.txt .env
nano .env  # Edit with production settings

# Run migrations
flask db upgrade

# Frontend build
cd ../frontend
npm ci
npm run build
```

### 4. Systemd Services

Create backend service:

```bash
sudo nano /etc/systemd/system/store-backend.service
```

```ini
[Unit]
Description=Store ERP Backend
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/store-erp/backend
Environment="PATH=/opt/store-erp/backend/venv/bin"
ExecStart=/opt/store-erp/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /var/log/store-erp/access.log \
    --error-logfile /var/log/store-erp/error.log \
    wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo mkdir -p /var/log/store-erp
sudo chown www-data:www-data /var/log/store-erp
sudo systemctl enable store-backend
sudo systemctl start store-backend
```

### 5. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/store-erp
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    # Frontend
    location / {
        root /opt/store-erp/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check
    location /health {
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/store-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🐳 Docker Deployment

### docker-compose.yml

```yaml
version: '3.8'

services:
  database:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: store_db
      POSTGRES_USER: store_user
      POSTGRES_PASSWORD: secure-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://store_user:secure-password@database:5432/store_db
      - SECRET_KEY=your-secret-key
      - JWT_SECRET_KEY=your-jwt-secret
    depends_on:
      - database
    restart: unless-stopped

  frontend:
    build: ./frontend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/store.conf:/etc/nginx/conf.d/default.conf
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
```

### Deploy

```bash
# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## ⚙️ Configuration

### Backend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FLASK_ENV` | Yes | `development` or `production` |
| `SECRET_KEY` | Yes | Random secret key |
| `JWT_SECRET_KEY` | Yes | JWT signing key |
| `DATABASE_URL` | Yes | Database connection string |
| `CORS_ORIGINS` | Yes | Allowed CORS origins |
| `REDIS_URL` | No | Redis connection string |

### Frontend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_BASE` | Yes | Backend API URL |
| `VITE_APP_NAME` | No | Application name |
| `VITE_ENABLE_2FA` | No | Enable 2FA feature |

---

## 🔒 SSL/HTTPS Setup

### Using Certbot

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### Manual SSL

1. Obtain SSL certificate
2. Update Nginx configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/your-cert.crt;
    ssl_certificate_key /etc/ssl/private/your-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # ... rest of config
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}
```

---

## 📊 Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:6001/api/health

# Nginx health
curl http://localhost/health
```

### Logs

| Service | Log Location |
|---------|--------------|
| Backend | `/var/log/store-erp/` or Docker logs |
| Nginx | `/var/log/nginx/store_*.log` |
| System | `journalctl -u store-backend` |

### Backup Script

```bash
#!/bin/bash
# /opt/store-erp/scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/store-erp"

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U store_user store_db > $BACKUP_DIR/db_$DATE.sql

# Keep last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

---

## 🔧 Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Check logs
sudo journalctl -u store-backend -f

# Check database connection
psql -U store_user -d store_db -c "SELECT 1"
```

#### Frontend not loading
```bash
# Check Nginx config
sudo nginx -t

# Check if build exists
ls -la /opt/store-erp/frontend/dist/
```

#### API returns 502
```bash
# Check if backend is running
sudo systemctl status store-backend

# Check port binding
ss -tlnp | grep 5000
```

#### Database migration errors
```bash
# Reset migrations
cd backend
flask db downgrade base
flask db upgrade
```

---

## 📞 Support

- Documentation: `./docs/`
- Issues: GitHub Issues
- Email: support@store-erp.com

---

*Deployment Guide - Store ERP v2.0.0*
