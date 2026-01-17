# ملفات التكوين والإعدادات الكاملة - Gaara ERP v12

## نظرة عامة
توثيق شامل لجميع ملفات التكوين والإعدادات في نظام Gaara ERP v12.

## 1. ملفات الإعدادات الرئيسية (Django Settings)

### 1.1 `gaara_erp/settings/base.py`
```python
# gaara_erp/settings/base.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-...")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition

INSTALLED_APPS = [
    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party Apps
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "drf_yasg",

    # Core Modules
    "core_modules.users",
    "core_modules.permissions",
    "core_modules.system_settings",

    # Business Modules
    "business_modules.accounting",
    "business_modules.inventory",
    "business_modules.sales",
    "business_modules.purchasing",

    # Agricultural Modules
    "agricultural_modules.farms",
    "agricultural_modules.plant_diagnosis",
    "agricultural_modules.production",

    # AI Modules
    "ai_modules.intelligent_assistant",
    "ai_modules.ai_memory",
    "ai_modules.ai_models",

    # Integration Modules
    "integration_modules.ai",
    "integration_modules.ai_agriculture",

    # Service Modules
    "services_modules.hr",
    "services_modules.projects",

    # Admin Modules
    "admin_modules.custom_admin",
    "admin_modules.system_monitoring",

    # Security Module
    "security",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gaara_erp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gaara_erp.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "gaara_erp"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Riyadh"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = "users.User"

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# Simple JWT
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True # For development only
# CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

# Celery
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

### 1.2 `gaara_erp/settings/prod.py` (للإنتاج)
```python
# gaara_erp/settings/prod.py

from .base import *

DEBUG = False

# Security Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://app.gaara-erp.com",
    "https://www.gaara-erp.com",
]

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
```

### 1.3 `gaara_erp/settings_enhanced_security.py`
```python
# gaara_erp/settings_enhanced_security.py

from .settings.base import *

# Enhanced Security Settings

# Content Security Policy (CSP)
MIDDLEWARE.insert(2, "csp.middleware.CSPMiddleware")
CSP_DEFAULT_SRC = ("'self'", "api.gaara-erp.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "www.google-analytics.com")
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com")

# HTTP Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Password Policy
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "pwned_passwords_django.validators.PwnedPasswordsValidator",
    },
]

# Rate Limiting
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = [
    "rest_framework.throttling.AnonRateThrottle",
    "rest_framework.throttling.UserRateThrottle",
]
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "100/day",
    "user": "1000/day",
    "login": "10/hour",
}
```

## 2. ملفات Docker

### 2.1 `Dockerfile.enhanced`
```dockerfile
# Dockerfile.enhanced

# --- Build Stage ---
FROM python:3.11-slim-buster AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev

COPY requirements_enhanced_security.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements_enhanced_security.txt

# --- Final Stage ---
FROM python:3.11-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
COPY requirements_enhanced_security.txt .
RUN pip install --no-cache-dir /wheels/*

COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]
```

### 2.2 `docker-compose.enhanced.yml`
```yaml
# docker-compose.enhanced.yml

version: "3.8"

services:
  db:
    image: postgres:14-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build:
      context: .
      dockerfile: Dockerfile.enhanced
    command: gunicorn gaara_erp.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }

  celery_worker:
    build:
      context: .
      dockerfile: Dockerfile.enhanced
    command: celery -A gaara_erp worker -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - redis

  celery_beat:
    build:
      context: .
      dockerfile: Dockerfile.enhanced
    command: celery -A gaara_erp beat -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - redis

volumes:
  postgres_data:
```

### 2.3 `docker/entrypoint.sh`
```bash
#!/bin/sh

# Wait for the database to be ready
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER
do
  echo "Waiting for database..."
  sleep 2
done

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --settings=gaara_erp.settings_enhanced_security

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=gaara_erp.settings_enhanced_security

# Start the server
echo "Starting server..."
exec "$@"
```

## 3. ملفات المتطلبات (Requirements Files)

### 3.1 `requirements.txt` (الأساسي)
```
Django>=4.2,<5.0
djangorestframework>=3.14,<3.15
djangorestframework-simplejwt>=5.3,<5.4
django-filter>=23.3,<24.0
django-cors-headers>=4.2,<4.3
psycopg2-binary>=2.9,<3.0
gunicorn>=21.2,<22.0
celery>=5.3,<5.4
redis>=5.0,<5.1
django-redis>=5.3,<5.4
drf-yasg>=1.21,<1.22
```

### 3.2 `requirements_enhanced_security.txt`
```
# Includes all from requirements.txt
-r requirements.txt

# Security Libraries
argon2-cffi>=23.1,<24.0
django-csp>=3.7,<3.8
pwned-passwords-django>=1.4,<1.5
bleach>=6.0,<6.1

# MFA Libraries
pyotp>=2.9,<3.0
qrcode>=7.4,<7.5

# Encryption
cryptography>=41.0,<42.0
```

## 4. ملفات التكوين الأخرى

### 4.1 `.env.example`
```
# Environment variables for Gaara ERP

# General
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=gaara_erp
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432

# Redis / Celery
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# AI Services
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
```

### 4.2 `pytest.ini`
```ini
[pytest]
DJANGO_SETTINGS_MODULE = gaara_erp.settings.test
python_files = tests.py test_*.py *_tests.py
addopts = -p no:warnings
```

### 4.3 `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class

# Environment
.env

# Django
*.log
local_settings.py
db.sqlite3

# Static & Media
/staticfiles/
/media/

# IDE
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db
```

---

**تاريخ التوثيق**: نوفمبر 2025  
**إصدار النظام**: Gaara ERP v12 Enhanced Security Edition  
**حالة التوثيق**: شامل ومحدث
