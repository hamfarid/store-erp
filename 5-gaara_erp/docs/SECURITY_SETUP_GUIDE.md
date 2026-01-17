# FILE: docs/SECURITY_SETUP_GUIDE.md | PURPOSE: Security setup guide for deployment | OWNER: Security Team | RELATED: P0_Security_FINAL_VERIFICATION_REPORT.md | LAST-AUDITED: 2025-11-20

# Gaara ERP v12 - Security Setup Guide

**Purpose**: Step-by-step guide for deploying Gaara ERP v12 with all security features enabled  
**Audience**: DevOps Engineers, System Administrators  
**Last Updated**: 2025-11-20

---

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ Python 3.11+
- ✅ PostgreSQL 14+ (or SQLite for development)
- ✅ Redis 6+ (for caching and rate limiting)
- ✅ SSL/TLS certificate (for HTTPS)
- ✅ Environment variable management (e.g., `.env` file or secrets manager)

---

## 🔐 Step 1: Environment Variables Setup

Create a `.env` file in the project root with the following **required** variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-min-50-chars
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
POSTGRES_DB=gaara_erp
POSTGRES_USER=gaara_user
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# JWT Settings (already configured in settings/security.py)
# ACCESS_TOKEN_LIFETIME=15 minutes (hardcoded)
# REFRESH_TOKEN_LIFETIME=7 days (hardcoded)

# CORS Settings
CORS_ALLOWED_ORIGINS=https://app.yourdomain.com,https://admin.yourdomain.com

# Redis (for caching and rate limiting)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Email (for password reset, notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Security Settings (Production)
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

**⚠️ CRITICAL**: Never commit `.env` to version control!

---

## 🔒 Step 2: Generate Secure SECRET_KEY

```bash
# Generate a secure SECRET_KEY (50+ characters)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and set it as `SECRET_KEY` in your `.env` file.

---

## 🛡️ Step 3: Database Setup

### PostgreSQL (Production)

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE gaara_erp;
CREATE USER gaara_user WITH PASSWORD 'your-secure-password-here';
ALTER ROLE gaara_user SET client_encoding TO 'utf8';
ALTER ROLE gaara_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gaara_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE gaara_erp TO gaara_user;
\q
```

### Run Migrations

```bash
# Apply all migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## 🔐 Step 4: SSL/TLS Certificate Setup

### Option 1: Let's Encrypt (Free)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 2: Custom Certificate

Place your certificate files in `/etc/ssl/`:
- `/etc/ssl/certs/yourdomain.crt`
- `/etc/ssl/private/yourdomain.key`

---

## 🚀 Step 5: Deploy with Gunicorn + Nginx

### Install Gunicorn

```bash
pip install gunicorn
```

### Create Gunicorn Service

Create `/etc/systemd/system/gaara-erp.service`:

```ini
[Unit]
Description=Gaara ERP Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/gaara_erp
Environment="PATH=/var/www/gaara_erp/venv/bin"
ExecStart=/var/www/gaara_erp/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/www/gaara_erp/gaara_erp.sock \
    gaara_erp.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Configure Nginx

Create `/etc/nginx/sites-available/gaara-erp`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers (additional to Django middleware)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;

    location / {
        proxy_pass http://unix:/var/www/gaara_erp/gaara_erp.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/gaara_erp/staticfiles/;
    }

    location /media/ {
        alias /var/www/gaara_erp/media/;
    }
}
```

### Enable and Start Services

```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/gaara-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Enable and start Gunicorn
sudo systemctl enable gaara-erp
sudo systemctl start gaara-erp
sudo systemctl status gaara-erp
```

---

## 🔍 Step 6: Verify Security Features

### 1. Check HTTPS Enforcement

```bash
curl -I http://yourdomain.com
# Should return 301 redirect to https://
```

### 2. Check Security Headers

```bash
curl -I https://yourdomain.com
# Should include:
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# Content-Security-Policy: ...
```

### 3. Check Health Endpoints

```bash
curl https://yourdomain.com/health/
# Should return: {"status": "healthy", "checks": {...}}

curl https://yourdomain.com/health/detailed/
# Should return detailed component status
```

### 4. Test Rate Limiting

```bash
# Send 10 rapid requests
for i in {1..10}; do curl https://yourdomain.com/api/users/; done
# After 5 requests, should return 429 Too Many Requests
```

### 5. Test Account Lockout

```bash
# Try 6 failed login attempts
for i in {1..6}; do
  curl -X POST https://yourdomain.com/api/auth/login/ \
    -H "Content-Type: application/json" \
    -d '{"username": "test", "password": "wrong"}'
done
# 6th attempt should return: {"code": "ACCOUNT_LOCKED"}
```

---

## 📊 Step 7: Monitoring Setup

### 1. Check Logs

```bash
# View structured JSON logs
tail -f /var/www/gaara_erp/logs/info.log
tail -f /var/www/gaara_erp/logs/error.log
tail -f /var/www/gaara_erp/logs/security.log
```

### 2. Set Up Log Rotation

Create `/etc/logrotate.d/gaara-erp`:

```
/var/www/gaara_erp/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload gaara-erp
    endscript
}
```

### 3. Monitor Health Endpoints

Set up monitoring (e.g., Prometheus, Grafana) to poll:
- `https://yourdomain.com/health/` every 30 seconds
- Alert if status != "healthy"

---

## 🔐 Step 8: Secret Scanning (CI/CD)

### GitHub Actions

The project includes `.github/workflows/security-scan.yml` which:
- ✅ Runs on every push to main/develop/staging
- ✅ Runs on every pull request
- ✅ Runs daily at 2 AM UTC
- ✅ Scans for hardcoded secrets using `detect-secrets`

### Manual Scan

```bash
# Install detect-secrets
pip install detect-secrets==1.5.0

# Scan for secrets
detect-secrets scan --baseline .secrets.baseline

# Audit results
detect-secrets audit .secrets.baseline
```

---

## ✅ Step 9: Production Checklist

Before going live, verify:

- [ ] `.env` file configured with all required variables
- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is 50+ characters and unique
- [ ] Database is PostgreSQL (not SQLite)
- [ ] Redis is running and accessible
- [ ] SSL/TLS certificate is valid
- [ ] HTTPS is enforced (HTTP redirects to HTTPS)
- [ ] All security headers are present
- [ ] CORS is whitelist-only (not wildcard)
- [ ] Health endpoints return 200 OK
- [ ] Logs are being written to `/logs/`
- [ ] Log rotation is configured
- [ ] Monitoring is set up
- [ ] Secret scanning is enabled in CI/CD
- [ ] Backups are automated

---

## 🆘 Troubleshooting

### Issue: 500 Internal Server Error

**Solution**: Check error logs
```bash
tail -f /var/www/gaara_erp/logs/error.log
```

### Issue: CSRF Verification Failed

**Solution**: Ensure `CSRF_COOKIE_SECURE=True` and you're using HTTPS

### Issue: Rate Limit Not Working

**Solution**: Verify Redis is running
```bash
redis-cli ping
# Should return: PONG
```

### Issue: Account Lockout Not Working

**Solution**: Check User model has `is_account_locked()` method
```bash
python manage.py shell
>>> from core_modules.users.models import User
>>> user = User.objects.first()
>>> hasattr(user, 'is_account_locked')
# Should return: True
```

---

## 📚 Additional Resources

- **Full Verification Report**: `docs/P0_Security_FINAL_VERIFICATION_REPORT.md`
- **Executive Summary**: `docs/EXECUTIVE_SUMMARY_FINAL.md`
- **Permission Model**: `docs/Permissions_Model.md`
- **Secret Scanning Guide**: `docs/Secret_Scanning_Guide.md`

---

**For support, contact the Security Team.**

**Status**: ✅ **Production Ready**  
**Last Updated**: 2025-11-20

