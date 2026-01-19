# 🚀 Production Deployment Guide

**Version:** 1.0.0  
**Last Updated:** 2025-11-18  
**Target:** Production Environment  
**Status:** ✅ Production Ready

---

## 📋 Overview

This guide covers deploying the Gaara AI application to a production environment with best practices for security, performance, and reliability.

**Deployment Options:**
1. Docker + Docker Compose (Recommended)
2. Traditional Server (Ubuntu/Debian)
3. Cloud Platforms (AWS, GCP, Azure)

---

## 🎯 Prerequisites

### Required Software
- Python 3.11+
- PostgreSQL 15+
- Node.js 18+ (for frontend)
- Nginx (reverse proxy)
- SSL Certificate (Let's Encrypt recommended)

### Required Accounts
- Domain name
- Cloud provider account (optional)
- Email service (SMTP)
- Storage service (S3, GCS, or local)

---

## 🐳 Option 1: Docker Deployment (Recommended)

### Step 1: Prepare Environment

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: gaara_postgres
    restart: always
    environment:
      POSTGRES_DB: gaara_scan_ai
      POSTGRES_USER: gaara_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - gaara_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U gaara_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: gaara_backend
    restart: always
    environment:
      - DATABASE_URL=postgresql://gaara_user:${POSTGRES_PASSWORD}@postgres:5432/gaara_scan_ai
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET=${JWT_SECRET}
      - DEBUG=False
      - ALLOWED_ORIGINS=${ALLOWED_ORIGINS}
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    networks:
      - gaara_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    container_name: gaara_frontend
    restart: always
    environment:
      - VITE_API_URL=${API_URL}
    networks:
      - gaara_network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: gaara_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - backend
      - frontend
    networks:
      - gaara_network

volumes:
  postgres_data:

networks:
  gaara_network:
    driver: bridge
```

### Step 2: Create Backend Dockerfile

Create `backend/Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 gaara && chown -R gaara:gaara /app
USER gaara

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Step 3: Create Frontend Dockerfile

Create `frontend/Dockerfile.prod`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Step 4: Create Nginx Configuration

Create `nginx/nginx.conf`:

```nginx
upstream backend {
    server backend:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Frontend
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # File uploads
    location /uploads {
        alias /app/uploads;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Health check
    location /health {
        proxy_pass http://backend/health;
        access_log off;
    }
}
```

### Step 5: Create Environment File

Create `.env.prod`:

```env
# Database
POSTGRES_PASSWORD=your_secure_password_here

# Application
SECRET_KEY=your_secret_key_min_32_chars_here
JWT_SECRET=your_jwt_secret_min_32_chars_here
DEBUG=False

# CORS
ALLOWED_ORIGINS=https://your-domain.com

# API
API_URL=https://your-domain.com/api

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Storage (Optional)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=gaara-uploads
AWS_REGION=us-east-1
```

### Step 6: Deploy

```bash
# 1. Clone repository
git clone https://github.com/your-org/gaara-ai.git
cd gaara-ai

# 2. Copy environment file
cp .env.prod .env

# 3. Edit .env with your values
nano .env

# 4. Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# 5. Run database migrations
docker-compose exec backend alembic upgrade head

# 6. Create admin user
docker-compose exec backend python scripts/create_admin.py

# 7. Check logs
docker-compose logs -f

# 8. Verify deployment
curl https://your-domain.com/health
```

---

## 🖥️ Option 2: Traditional Server Deployment

### Step 1: Prepare Server (Ubuntu 22.04)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib nginx certbot python3-certbot-nginx \
    git curl

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Step 2: Setup PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE gaara_scan_ai;
CREATE USER gaara_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE gaara_scan_ai TO gaara_user;
\q
```

### Step 3: Deploy Backend

```bash
# Create application directory
sudo mkdir -p /var/www/gaara-ai
sudo chown $USER:$USER /var/www/gaara-ai
cd /var/www/gaara-ai

# Clone repository
git clone https://github.com/your-org/gaara-ai.git .

# Setup Python virtual environment
cd backend
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
# Add your configuration

# Run migrations
alembic upgrade head

# Test application
gunicorn src.main:app --bind 0.0.0.0:8000 --workers 4
```

### Step 4: Create Systemd Service

Create `/etc/systemd/system/gaara-backend.service`:

```ini
[Unit]
Description=Gaara AI Backend
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/gaara-ai/backend
Environment="PATH=/var/www/gaara-ai/backend/venv/bin"
ExecStart=/var/www/gaara-ai/backend/venv/bin/gunicorn \
    src.main:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --access-logfile /var/log/gaara/access.log \
    --error-logfile /var/log/gaara/error.log

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
# Create log directory
sudo mkdir -p /var/log/gaara
sudo chown www-data:www-data /var/log/gaara

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable gaara-backend
sudo systemctl start gaara-backend
sudo systemctl status gaara-backend
```

### Step 5: Deploy Frontend

```bash
cd /var/www/gaara-ai/frontend

# Install dependencies
npm ci

# Build for production
npm run build

# Copy to nginx directory
sudo cp -r dist/* /var/www/html/
```

### Step 6: Configure Nginx

Create `/etc/nginx/sites-available/gaara-ai`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and get SSL:

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/gaara-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

---

## ☁️ Option 3: Cloud Platform Deployment

### AWS Deployment

**Services Used:**
- EC2 (Application server)
- RDS (PostgreSQL database)
- S3 (File storage)
- CloudFront (CDN)
- Route 53 (DNS)
- Certificate Manager (SSL)

**Quick Deploy:**
```bash
# Use AWS Elastic Beanstalk
eb init gaara-ai --platform python-3.11
eb create gaara-production
eb deploy
```

### Google Cloud Platform

**Services Used:**
- Cloud Run (Backend)
- Cloud SQL (PostgreSQL)
- Cloud Storage (Files)
- Cloud CDN
- Cloud Load Balancing

### Azure

**Services Used:**
- App Service (Backend)
- Azure Database for PostgreSQL
- Blob Storage (Files)
- Azure CDN
- Application Gateway

---

## 🔒 Security Checklist

- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY and JWT_SECRET
- [ ] Enable HTTPS (SSL certificate)
- [ ] Configure firewall (allow only 80, 443, 22)
- [ ] Disable DEBUG mode
- [ ] Set up database backups
- [ ] Configure log rotation
- [ ] Enable fail2ban
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Configure rate limiting
- [ ] Enable CORS only for your domain
- [ ] Set up intrusion detection
- [ ] Regular security updates

---

## 📊 Monitoring & Logging

### Application Logs

```bash
# View backend logs
docker-compose logs -f backend

# Or on traditional server
sudo journalctl -u gaara-backend -f
```

### Database Monitoring

```bash
# PostgreSQL stats
docker-compose exec postgres psql -U gaara_user -d gaara_scan_ai -c "SELECT * FROM pg_stat_activity;"
```

### Performance Monitoring

Install Prometheus and Grafana:

```yaml
# Add to docker-compose.prod.yml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 🔄 Backup & Recovery

### Automated Backups

Create `/etc/cron.daily/gaara-backup`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/gaara"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
docker-compose exec -T postgres pg_dump -U gaara_user gaara_scan_ai | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Files backup
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /var/www/gaara-ai/uploads

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete
```

Make executable:
```bash
sudo chmod +x /etc/cron.daily/gaara-backup
```

### Recovery

```bash
# Restore database
gunzip < db_backup.sql.gz | docker-compose exec -T postgres psql -U gaara_user gaara_scan_ai

# Restore files
tar -xzf uploads_backup.tar.gz -C /var/www/gaara-ai/
```

---

## 🚀 Scaling

### Horizontal Scaling

```yaml
# docker-compose.prod.yml
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

### Load Balancing

Use Nginx upstream:

```nginx
upstream backend {
    least_conn;
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

---

## 📞 Support

**Documentation:** https://docs.gaara-ai.com  
**Issues:** https://github.com/your-org/gaara-ai/issues  
**Email:** support@gaara-ai.com

---

**Generated by:** Autonomous AI Agent  
**Framework:** GLOBAL_PROFESSIONAL_CORE_PROMPT v16.0  
**Status:** ✅ Production Ready

---

