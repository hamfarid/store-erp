# Environment Configuration Guide

This document describes all environment variables required for Gaara ERP v12.

## Quick Start

Create a `.env` file in the project root with the following variables:

```bash
# Copy this to .env and fill in your values
# NEVER commit .env to version control!

# ===========================================
# REQUIRED - Application Settings
# ===========================================
SECRET_KEY=your-super-secret-key-minimum-50-characters-here
DEBUG=False
APP_MODE=prod  # dev | test | prod
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# ===========================================
# REQUIRED - Database Configuration
# ===========================================
DATABASE_URL=postgresql://username:password@localhost:5432/gaara_erp

# ===========================================
# REQUIRED - Redis Cache & Celery
# ===========================================
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ===========================================
# REQUIRED FOR AI FEATURES
# ===========================================
OPENAI_API_KEY=sk-your-openai-api-key-here

# ===========================================
# REQUIRED FOR AGRICULTURAL AI
# ===========================================
PYBROPS_API_KEY=your-pybrops-api-key-here

# ===========================================
# SECURITY SETTINGS (Production)
# ===========================================
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# ===========================================
# EMAIL CONFIGURATION
# ===========================================
EMAIL_HOST=smtp.yourdomain.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# ===========================================
# ADMIN CREDENTIALS (Initial Setup Only)
# ===========================================
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=change-this-secure-password

# ===========================================
# OPTIONAL - External Services
# ===========================================
# AWS_ACCESS_KEY_ID=your-aws-access-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret-key
# AWS_S3_BUCKET_NAME=your-bucket-name

# SENTRY_DSN=https://your-sentry-dsn

# ===========================================
# LOGGING
# ===========================================
LOG_LEVEL=INFO
```

## Variable Reference

### Application Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | None | Django secret key (min 50 chars) |
| `DEBUG` | No | False | Enable debug mode |
| `APP_MODE` | No | prod | Application mode (dev/test/prod) |
| `ALLOWED_HOSTS` | Yes | None | Comma-separated allowed hosts |

### Database

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | None | PostgreSQL connection URL |

### Redis & Celery

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REDIS_URL` | Yes | None | Redis connection URL for caching |
| `CELERY_BROKER_URL` | Yes | None | Celery broker URL |
| `CELERY_RESULT_BACKEND` | No | None | Celery result backend |

### AI Services

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | For AI | None | OpenAI API key |
| `PYBROPS_API_KEY` | For Agri AI | None | PyBrOpS API key |

### Security

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECURE_SSL_REDIRECT` | Prod | True | Redirect HTTP to HTTPS |
| `SESSION_COOKIE_SECURE` | Prod | True | Secure session cookies |
| `CSRF_COOKIE_SECURE` | Prod | True | Secure CSRF cookies |
| `SECURE_HSTS_SECONDS` | Prod | 31536000 | HSTS header duration |

## Development vs Production

### Development
```bash
DEBUG=True
APP_MODE=dev
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Production
```bash
DEBUG=False
APP_MODE=prod
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Validation

Run Django check to validate your configuration:

```bash
python manage.py check --deploy
```

