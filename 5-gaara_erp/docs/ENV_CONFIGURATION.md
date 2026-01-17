# 🔐 GAARA ERP v12 - Environment Configuration
# إعدادات البيئة لنظام قعرة

**Version:** 1.0.0
**Created:** 2026-01-15

---

## Quick Setup

```bash
# Create .env file in backend directory
cd D:\Ai_Project\5-gaara_erp\backend

# Generate secret keys
python -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(32)}')"
python -c "import secrets; print(f'JWT_SECRET_KEY={secrets.token_hex(32)}')"
```

---

## 🔴 REQUIRED Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session encryption (32+ chars) | `a1b2c3d4...` |
| `JWT_SECRET_KEY` | JWT token signing (32+ chars) | `e5f6g7h8...` |
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@localhost:5432/gaara_erp` |

---

## 🟠 RECOMMENDED Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Celery message broker | `redis://localhost:6379/0` |
| `FLASK_ENV` | Environment mode | `development` |
| `DEBUG` | Debug mode | `True` |

---

## 🟢 OPTIONAL Variables

### AI Services
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_AI_API_KEY=...
PYBROPS_API_KEY=...
```

### Email Configuration
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=your-app-password
```

### Telegram Notifications
```bash
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=your-chat-id
```

---

## 🔒 Security Configuration

### JWT Settings (Standardized)
```bash
# Access Token: 15 minutes (900 seconds)
JWT_ACCESS_TOKEN_EXPIRES=900

# Refresh Token: 7 days (604800 seconds)
JWT_REFRESH_TOKEN_EXPIRES=604800
```

### Rate Limiting
```bash
RATELIMIT_ENABLED=True
RATELIMIT_DEFAULT=60 per minute
```

### CORS
```bash
CORS_ORIGINS=http://localhost:5501,http://localhost:3000
```

---

## 🐳 Port Configuration (Docker)

| Service | Port | Variable |
|---------|------|----------|
| Backend API | 5001 | `BACKEND_PORT` |
| Frontend | 5501 | `FRONTEND_PORT` |
| ML Service | 5101 | `ML_PORT` |
| AI Service | 5601 | `AI_PORT` |
| PostgreSQL | 10502 | `POSTGRES_PORT` |
| Redis | 6375 | `REDIS_PORT` |

---

## 📋 Complete .env Template

```bash
# =============================================================================
# GAARA ERP v12 - Environment Configuration
# =============================================================================

# REQUIRED
SECRET_KEY=your-secret-key-here-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-here-min-32-chars
DATABASE_URL=sqlite:///instance/gaara_erp.db

# RECOMMENDED
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
FLASK_ENV=development
DEBUG=True

# SECURITY
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=604800
RATELIMIT_ENABLED=True

# PORTS
BACKEND_PORT=5001
FRONTEND_PORT=5501

# OPTIONAL AI
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# LOGGING
LOG_LEVEL=INFO
```

---

## ⚠️ Security Warnings

1. **NEVER commit `.env` to version control**
2. **Use strong secrets** (32+ characters, random)
3. **Rotate secrets** periodically
4. **Use different secrets** for development/production
5. **Store production secrets** in KMS/Vault

---

## 🔧 Validation Script

```python
# scripts/validate_env.py
import os
import sys

REQUIRED = ['SECRET_KEY', 'JWT_SECRET_KEY', 'DATABASE_URL']
MIN_KEY_LENGTH = 32

def validate():
    errors = []
    
    for var in REQUIRED:
        value = os.getenv(var)
        if not value:
            errors.append(f"Missing required: {var}")
        elif 'KEY' in var and len(value) < MIN_KEY_LENGTH:
            errors.append(f"{var} too short ({len(value)} chars, need {MIN_KEY_LENGTH})")
    
    if errors:
        print("❌ Environment validation failed:")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)
    
    print("✅ Environment configuration valid")

if __name__ == '__main__':
    validate()
```

---

**END OF ENVIRONMENT CONFIGURATION**
