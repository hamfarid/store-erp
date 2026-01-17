# Gaara ERP - Environment Configuration Guide

Generated: 2025-12-02

## Required Environment Variables

### Core Settings (REQUIRED)
```bash
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
APP_MODE=dev  # dev | test | prod
APP_VERSION=12.0.0
ENVIRONMENT=development  # development | staging | production
```

### Database Configuration
```bash
# SQLite (default for development)
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL (recommended for production)
POSTGRES_DB=gaara
POSTGRES_USER=gaara
POSTGRES_PASSWORD=your-secure-password
```

### Allowed Hosts & CORS
```bash
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3505,http://127.0.0.1:3505,http://localhost:9551,http://127.0.0.1:9551
CSRF_TRUSTED_ORIGINS=http://localhost:3505,http://127.0.0.1:3505
```

### Redis & Celery
```bash
REDIS_URL=redis://127.0.0.1:9651/1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Email Configuration
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@gaara-erp.com
```

### AI & ML Configuration (REQUIRED for AI features)
```bash
OPENAI_API_KEY=your-openai-api-key

# ML Service
ML_HOST=127.0.0.1
ML_PORT=12056
ML_SERVICE_URL=http://127.0.0.1:12056
ML_ENABLED=True

# RAG Configuration
RAG_ENABLED=True
RAG_CHUNK_SIZE=500
RAG_TOP_K=5

# AI Memory
AI_MEMORY_ENABLED=True
AI_MAX_MEMORIES=1000
```

### Security Settings
```bash
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
TWO_FACTOR_AUTH_ENABLED=True
API_RATE_LIMIT=1000/hour
LOGIN_RATE_LIMIT=5/minute
ENCRYPTION_KEY=your-encryption-key-32-chars-min
```

### Secrets Manager (Production)
```bash
SECRETS_BACKEND=env  # env | vault | aws | azure | gcp

# HashiCorp Vault
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=your-vault-token

# AWS Secrets Manager
AWS_SECRETS_REGION=us-east-1
AWS_SECRET_NAME=gaara-erp/production
```

## Port Configuration

| Service | Port |
|---------|------|
| Frontend | 3505 |
| Backend | 9551 |
| Redis | 9651 |
| SQL | 3605 |
| ML Service | 12056 |

## Creating .env File

1. Create `.env` file in project root:
```bash
cp docs/ENV_CONFIG.md .env
# Edit and keep only the KEY=value lines
```

2. Or use this minimal setup:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
APP_MODE=dev
ALLOWED_HOSTS=localhost,127.0.0.1
```

