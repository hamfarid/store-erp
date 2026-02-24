# Deployment Guide - Store Management System v1.5

Complete guide for deploying the Store Management System to production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Database Configuration](#database-configuration)
6. [Security Hardening](#security-hardening)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup & Recovery](#backup--recovery)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum**:
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB SSD
- OS: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+

**Recommended**:
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+ SSD
- OS: Ubuntu 22.04 LTS

### Software Requirements

- **Python**: 3.11+
- **Node.js**: 18+ LTS
- **PostgreSQL**: 14+ (or MySQL 8+, SQLite for dev)
- **Nginx**: 1.18+ (reverse proxy)
- **Redis**: 7+ (caching, optional)
- **SSL Certificate**: Let's Encrypt or commercial

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/hamfarid/store.git
cd store
```

### 2. Create Environment Files

#### Backend (.env)

Create `backend/.env`:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=<generate-strong-secret-key-here>
DEBUG=False

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/storedb
# Or for MySQL:
# DATABASE_URL=mysql://username:password@localhost:3306/storedb
# Or for SQLite (development only):
# DATABASE_URL=sqlite:///instance/inventory.db

# JWT Configuration
JWT_SECRET_KEY=<generate-another-strong-secret-key>
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour
JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 days

# CORS Configuration
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Upload Configuration
UPLOAD_FOLDER=/var/www/store/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Redis (optional, for caching)
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/store/app.log
```

#### Frontend (.env.production)

Create `frontend/.env.production`:

```env
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_NAME=Store Management System
VITE_APP_VERSION=1.5.0
VITE_ENABLE_ANALYTICS=true
```

### 3. Generate Secret Keys

```bash
# Python method
python3 -c "import secrets; print(secrets.token_urlsafe(64))"

# OpenSSL method
openssl rand -base64 64
```

---

## Backend Deployment

### Option A: Production WSGI Server (Gunicorn - Recommended)

#### 1. Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install gunicorn  # Production server
```

#### 2. Create Gunicorn Configuration

Create `backend/gunicorn_config.py`:

```python
import multiprocessing

# Server socket
bind = "127.0.0.1:5002"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 5

# Logging
accesslog = "/var/log/store/gunicorn_access.log"
errorlog = "/var/log/store/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "store_backend"

# Server mechanics
daemon = False
pidfile = "/var/run/store/gunicorn.pid"
user = "www-data"
group = "www-data"

# SSL (if terminating SSL at application level)
# keyfile = "/etc/ssl/private/store.key"
# certfile = "/etc/ssl/certs/store.crt"
```

#### 3. Create Systemd Service

Create `/etc/systemd/system/store-backend.service`:

```ini
[Unit]
Description=Store Management System Backend
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/store/backend
Environment="PATH=/var/www/store/backend/venv/bin"
Environment="PYTHONPATH=/var/www/store"
ExecStart=/var/www/store/backend/venv/bin/gunicorn \
    --config /var/www/store/backend/gunicorn_config.py \
    app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

#### 4. Start Service

```bash
# Create required directories
sudo mkdir -p /var/log/store /var/run/store
sudo chown www-data:www-data /var/log/store /var/run/store

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable store-backend
sudo systemctl start store-backend
sudo systemctl status store-backend

# View logs
sudo journalctl -u store-backend -f
```

### Option B: Docker Deployment

#### Backend Dockerfile

Already exists at `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV FLASK_APP=app.py

EXPOSE 5002

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "4", "app:app"]
```

#### Docker Compose (Production)

Use `docker-compose.prod.yml`:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Frontend Deployment

### 1. Build for Production

```bash
cd frontend
npm install
npm run build
```

This creates optimized static files in `frontend/dist/`.

### 2. Option A: Nginx Static Hosting (Recommended)

#### Nginx Configuration

Create `/etc/nginx/sites-available/store`:

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Frontend (Static Files)
    root /var/www/store/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API Proxy (Backend)
    location /api/ {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;

    # Logs
    access_log /var/log/nginx/store_access.log;
    error_log /var/log/nginx/store_error.log;
}
```

#### Enable Site

```bash
# Copy frontend build files
sudo cp -r frontend/dist/* /var/www/store/frontend/dist/

# Enable nginx site
sudo ln -s /etc/nginx/sites-available/store /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Option B: Node.js/PM2 (Alternative)

```bash
cd frontend
npm install -g pm2
pm2 start npm --name "store-frontend" -- run preview
pm2 save
pm2 startup
```

---

## Database Configuration

### PostgreSQL Setup

#### 1. Install PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### 2. Create Database and User

```bash
sudo -u postgres psql

CREATE DATABASE storedb;
CREATE USER storeuser WITH ENCRYPTED PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE storedb TO storeuser;
\q
```

#### 3. Configure PostgreSQL

Edit `/etc/postgresql/14/main/postgresql.conf`:

```conf
listen_addresses = 'localhost'
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
```

Edit `/etc/postgresql/14/main/pg_hba.conf`:

```conf
local   storedb    storeuser                md5
host    storedb    storeuser    127.0.0.1/32    md5
```

#### 4. Restart PostgreSQL

```bash
sudo systemctl restart postgresql
```

#### 5. Initialize Database

```bash
cd backend
source venv/bin/activate
export DATABASE_URL=postgresql://storeuser:secure_password_here@localhost:5432/storedb
python database_setup.py
```

### Database Migrations

If you make schema changes:

```bash
# Using Alembic (if configured)
alembic upgrade head

# Or run custom migration script
python database_migration_script.py
```

---

## Security Hardening

### 1. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (should be automatic)
sudo certbot renew --dry-run
```

### 3. Application Security

- **Change default passwords** in `backend/database_setup.py`
- **Rotate secret keys** regularly
- **Enable rate limiting** in Flask (Flask-Limiter)
- **Implement CSRF protection** (Flask-WTF)
- **Use prepared statements** (already implemented with SQLAlchemy)
- **Sanitize user input** (validate all inputs)
- **Keep dependencies updated**: `pip list --outdated`

### 4. Server Hardening

```bash
# Disable root SSH login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl reload sshd

# Install fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## Monitoring & Logging

### 1. Application Logs

**Backend logs**:
- Location: `/var/log/store/app.log`
- Gunicorn logs: `/var/log/store/gunicorn_*.log`
- Systemd logs: `sudo journalctl -u store-backend`

**Nginx logs**:
- Access: `/var/log/nginx/store_access.log`
- Error: `/var/log/nginx/store_error.log`

### 2. Log Rotation

Create `/etc/logrotate.d/store`:

```conf
/var/log/store/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    sharedscripts
    postrotate
        systemctl reload store-backend > /dev/null 2>&1 || true
    endscript
}
```

### 3. Monitoring Tools

#### Option A: Simple Health Check Script

Create `/opt/store/health_check.sh`:

```bash
#!/bin/bash

# Check backend
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/api/status)
if [ "$BACKEND_STATUS" != "200" ]; then
    echo "Backend is down! Status: $BACKEND_STATUS"
    systemctl restart store-backend
fi

# Check database
psql -U storeuser -d storedb -c "SELECT 1" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Database connection failed!"
fi

# Check disk space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 85 ]; then
    echo "Warning: Disk usage at ${DISK_USAGE}%"
fi
```

Add to crontab:

```bash
*/5 * * * * /opt/store/health_check.sh >> /var/log/store/health_check.log 2>&1
```

#### Option B: Prometheus + Grafana

Install Flask-Prometheus metrics:

```bash
pip install prometheus-flask-exporter
```

Add to `backend/app.py`:

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
```

Configure Prometheus to scrape `http://localhost:5002/metrics`.

---

## Backup & Recovery

### 1. Database Backup

#### Automated PostgreSQL Backup

Create `/opt/store/backup_db.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/store"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/storedb_$DATE.sql.gz"

mkdir -p $BACKUP_DIR

pg_dump -U storeuser storedb | gzip > $BACKUP_FILE

# Keep only last 30 days
find $BACKUP_DIR -name "storedb_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE"
```

Add to crontab (daily at 2 AM):

```bash
0 2 * * * /opt/store/backup_db.sh >> /var/log/store/backup.log 2>&1
```

#### Manual Backup

```bash
# Backup
pg_dump -U storeuser storedb > storedb_backup.sql

# Restore
psql -U storeuser storedb < storedb_backup.sql
```

### 2. Application Files Backup

```bash
# Backup uploads, configs, logs
tar -czf /var/backups/store/app_files_$(date +%Y%m%d).tar.gz \
    /var/www/store/backend/.env \
    /var/www/store/uploads \
    /var/log/store
```

### 3. Off-site Backup (Recommended)

Use rsync to copy to remote server:

```bash
rsync -avz /var/backups/store/ user@backup-server:/backups/store/
```

Or use cloud storage (AWS S3, Google Cloud Storage):

```bash
# Install AWS CLI
pip install awscli

# Sync to S3
aws s3 sync /var/backups/store/ s3://your-bucket/store-backups/
```

---

## Troubleshooting

### Backend Won't Start

```bash
# Check service status
sudo systemctl status store-backend

# Check logs
sudo journalctl -u store-backend -n 100

# Check Python syntax
cd backend
source venv/bin/activate
python -m py_compile app.py

# Check database connection
python -c "from src.database import db; print('DB OK')"
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U storeuser -h localhost -d storedb

# Check PostgreSQL service
sudo systemctl status postgresql

# Check pg_hba.conf authentication
sudo tail /var/log/postgresql/postgresql-14-main.log
```

### Nginx 502 Bad Gateway

```bash
# Check if backend is running
curl http://localhost:5002/api/status

# Check Nginx error logs
sudo tail -f /var/log/nginx/store_error.log

# Test Nginx configuration
sudo nginx -t
```

### High Memory Usage

```bash
# Check processes
ps aux --sort=-%mem | head

# Reduce Gunicorn workers
# Edit gunicorn_config.py: workers = 2

# Restart service
sudo systemctl restart store-backend
```

### Slow Database Queries

```bash
# Enable slow query logging in PostgreSQL
# Edit postgresql.conf:
log_min_duration_statement = 1000  # Log queries > 1s

# Analyze query performance
sudo -u postgres psql storedb
EXPLAIN ANALYZE SELECT * FROM products;

# Add indexes if needed
CREATE INDEX idx_products_sku ON products(sku);
```

---

## Performance Optimization

### 1. Enable Caching (Redis)

```bash
# Install Redis
sudo apt install redis-server

# Configure Flask-Caching
pip install flask-caching redis
```

Add to `backend/app.py`:

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@cache.memoize(timeout=300)
def expensive_query():
    return Product.query.all()
```

### 2. Database Connection Pooling

Already configured in SQLAlchemy, but can be tuned:

```python
# In src/database.py
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
```

### 3. Static File CDN

For better performance, serve static files from CDN:

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    # Or point to CDN
    # return 301 https://cdn.yourdomain.com$request_uri;
}
```

---

## Maintenance

### Regular Tasks

- **Daily**: Check logs, verify backups
- **Weekly**: Review security updates, check disk space
- **Monthly**: Review access logs, update dependencies
- **Quarterly**: Security audit, performance review

### Updates

```bash
# Update backend dependencies
cd backend
source venv/bin/activate
pip list --outdated
pip install --upgrade <package>

# Update frontend dependencies
cd frontend
npm outdated
npm update

# Rebuild frontend
npm run build
sudo cp -r dist/* /var/www/store/frontend/dist/

# Restart services
sudo systemctl restart store-backend
sudo systemctl reload nginx
```

---

## Support & Resources

- **GitHub**: https://github.com/hamfarid/store
- **Documentation**: `/docs`
- **Issues**: https://github.com/hamfarid/store/issues

---

**Last Updated**: November 17, 2025  
**Version**: 1.5.0
