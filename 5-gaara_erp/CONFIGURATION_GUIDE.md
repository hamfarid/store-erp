# Gaara ERP - Configuration Guide

## 📋 Overview

This guide explains all configuration options available in Gaara ERP and how to customize them for your environment.

## 🔧 Configuration Files

### Core Configuration

Located in `gaara_erp/config/`:

1. **`logging_config.py`** - Logging configuration
2. **`cache_config.py`** - Redis caching and sessions
3. **`performance_config.py`** - Performance optimizations
4. **`rate_limiting.py`** - API rate limiting
5. **`api_versioning.py`** - API versioning and documentation
6. **`websocket_config.py`** - WebSocket/real-time configuration
7. **`email_config.py`** - Email service configuration
8. **`storage_config.py`** - File storage (local/S3)
9. **`error_tracking.py`** - Sentry error tracking

## 🔐 Environment Variables

### Required Variables

```bash
# Database
POSTGRES_DB=gaara_erp
POSTGRES_USER=gaara_admin
POSTGRES_PASSWORD=your_secure_password

# Django
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
DEBUG=false
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Redis
REDIS_URL=redis://redis:6379/0
```

### Optional Variables

```bash
# API Configuration
API_THROTTLE_USER=1000/hour
API_THROTTLE_ANON=100/hour
API_PAGE_SIZE=20

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# AWS S3 (for file storage)
USE_S3=true
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1

# Error Tracking
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# Monitoring
GRAFANA_PASSWORD=admin
```

## 📊 Logging Configuration

### Log Levels

Set via environment variable:
```bash
DJANGO_LOG_LEVEL=INFO      # Django logs
GAARA_LOG_LEVEL=INFO       # Application logs
DB_LOG_LEVEL=WARNING       # Database query logs
```

### Log Files

- `logs/gaara_erp.log` - General application logs
- `logs/errors.log` - Error logs only
- `logs/api.log` - API request logs (JSON format)

### Customization

Edit `gaara_erp/config/logging_config.py` to:
- Change log formats
- Add new handlers
- Configure log rotation
- Set custom log levels

## 💾 Caching Configuration

### Cache Backends

1. **Default Cache** - General purpose caching
2. **Session Cache** - User sessions
3. **API Cache** - API response caching

### Cache Timeouts

Configured in `gaara_erp/config/cache_config.py`:
- Default: 5 minutes
- User profile: 10 minutes
- Dashboard stats: 5 minutes
- Product list: 10 minutes

### Redis Configuration

```bash
REDIS_URL=redis://host:port/db_number
```

## ⚡ Performance Configuration

### Database

- Connection pooling: 10 minutes
- Query timeout: 30 seconds
- Connection max age: 600 seconds

### Gunicorn Workers

Automatically calculated: `(2 × CPU cores) + 1`

Override:
```bash
GUNICORN_WORKERS=4
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=120
```

### File Upload Limits

- Max memory size: 10 MB
- Max number of fields: 1000

## 🚦 Rate Limiting

### Default Limits

- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour
- Login: 5 requests/minute
- Register: 3 requests/hour

### Customization

Edit `gaara_erp/config/rate_limiting.py` or set environment variables:
```bash
API_THROTTLE_USER=2000/hour
API_THROTTLE_ANON=200/hour
```

## 📧 Email Configuration

### Development (Console)

```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production (SMTP)

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

### Email Templates

Located in `templates/emails/`:
- `welcome.html`
- `password_reset.html`
- `order_confirmation.html`
- `invoice.html`
- `notification.html`

## 📁 File Storage

### Local Storage (Default)

Files stored in `media/` directory.

### AWS S3 (Production)

```bash
USE_S3=true
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

### Allowed File Types

- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Documents: `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.csv`

### File Size Limits

- Images: 5 MB
- Documents: 10 MB
- General: 10 MB

## 🔍 Error Tracking

### Sentry Integration

```bash
SENTRY_DSN=https://your-dsn@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1
ENVIRONMENT=production
```

### Features

- Automatic error capture
- Performance monitoring
- Release tracking
- User context

## 🔌 WebSocket Configuration

### Real-time Features

Enabled by default:
- IoT monitoring
- Notifications
- Dashboard updates
- Inventory alerts

### Configuration

```bash
WEBSOCKET_ALLOWED_ORIGINS=http://localhost:5173,http://yourdomain.com
```

## 🧪 Development Tools

### Setup Script

```bash
./scripts/setup-dev.sh
```

Automatically:
- Checks prerequisites
- Creates .env file
- Starts services
- Initializes database
- Seeds data
- Creates superuser

### Generate Secret Keys

```bash
./scripts/generate-secret-key.sh
```

Generates:
- SECRET_KEY
- ENCRYPTION_KEY
- JWT_SECRET_KEY

### Cleanup Script

```bash
./scripts/clean.sh
```

Removes:
- Containers
- Volumes (optional)
- Build cache
- Python/Node cache
- Logs

## 📝 Configuration Best Practices

### Development

1. Use console email backend
2. Enable DEBUG mode
3. Use local file storage
4. Disable rate limiting (or set high limits)
5. Enable detailed logging

### Production

1. Use SMTP email backend
2. Disable DEBUG mode
3. Use S3 for file storage
4. Configure proper rate limits
5. Set up error tracking (Sentry)
6. Enable SSL/TLS
7. Configure proper CORS
8. Set up monitoring

## 🔄 Configuration Updates

After changing configuration:

```bash
# Restart services
docker-compose restart backend

# Or rebuild
docker-compose build backend
docker-compose up -d backend
```

## 📚 Additional Resources

- [Django Settings Documentation](https://docs.djangoproject.com/en/stable/ref/settings/)
- [Django REST Framework Settings](https://www.django-rest-framework.org/api-guide/settings/)
- [Redis Configuration](https://redis.io/docs/management/config/)
- [AWS S3 Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)

---

**Last Updated**: 2025-01-15  
**Version**: 1.0.0
