# Environment Configuration

**Last Updated:** 2025-11-04  
**Owner:** DevOps/Backend  
**Status:** ✅ Current

---

## Overview

Complete environment variable documentation with validation schema.

## Environment Files

- **Development:** `.env` (local, not committed)
- **Staging:** `.env.staging` (CI/CD secret)
- **Production:** `.env.production` (KMS/Vault)
- **Example:** `templates/.env.example` (template)

## Core Configuration

### Application

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `ENVIRONMENT` | string | `development` | Yes | Environment name (development, staging, production) |
| `FLASK_ENV` | string | `development` | Yes | Flask environment |
| `FLASK_DEBUG` | boolean | `0` | No | Enable Flask debug mode (dev only) |
| `SECRET_KEY` | string | - | Yes | Flask secret key (min 32 chars) |
| `APP_NAME` | string | `Store` | No | Application name |
| `APP_VERSION` | string | `1.0.0` | No | Application version |

### Database

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `DATABASE_URL` | string | `sqlite:///inventory.db` | Yes | Database connection URL |
| `DB_HOST` | string | `localhost` | No | Database host |
| `DB_PORT` | integer | `5432` | No | Database port |
| `DB_NAME` | string | `inventory` | No | Database name |
| `DB_USER` | string | - | No | Database user |
| `DB_PASSWORD` | string | - | No | Database password (use KMS/Vault in prod) |
| `DB_POOL_SIZE` | integer | `10` | No | Connection pool size |
| `DB_POOL_RECYCLE` | integer | `3600` | No | Connection recycle time (seconds) |

### API Configuration

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `API_BASE_URL` | string | `http://localhost:5001` | Yes | Backend API base URL |
| `API_PORT` | integer | `5001` | No | Backend API port |
| `API_HOST` | string | `0.0.0.0` | No | Backend API host |
| `VITE_API_BASE_URL` | string | - | No | Frontend API base URL (Vite env var) |

### Frontend Configuration

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `VITE_API_BASE_URL` | string | - | No | Frontend API base URL |
| `VITE_APP_NAME` | string | `Store` | No | Frontend app name |
| `VITE_APP_VERSION` | string | `1.0.0` | No | Frontend app version |

### Security

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `JWT_SECRET` | string | - | Yes | JWT signing secret (min 32 chars) |
| `JWT_ALGORITHM` | string | `HS256` | No | JWT algorithm (HS256, RS256) |
| `JWT_ACCESS_TTL` | integer | `900` | No | JWT access token TTL (seconds, default 15m) |
| `JWT_REFRESH_TTL` | integer | `604800` | No | JWT refresh token TTL (seconds, default 7d) |
| `SESSION_COOKIE_SECURE` | boolean | `true` (prod) | No | Secure cookie flag |
| `SESSION_COOKIE_HTTPONLY` | boolean | `true` | No | HttpOnly cookie flag |
| `SESSION_COOKIE_SAMESITE` | string | `Strict` (prod) | No | SameSite cookie attribute |
| `CORS_ORIGINS` | string | `http://localhost:3000` | No | CORS allowed origins (comma-separated) |
| `CSRF_ENABLED` | boolean | `true` | No | Enable CSRF protection |

### Authentication

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `MFA_ENABLED` | boolean | `true` | No | Enable MFA (TOTP) |
| `MFA_ISSUER` | string | `Store` | No | MFA issuer name |
| `LOGIN_LOCKOUT_ATTEMPTS` | integer | `5` | No | Failed login attempts before lockout |
| `LOGIN_LOCKOUT_DURATION` | integer | `900` | No | Lockout duration (seconds, default 15m) |
| `PASSWORD_MIN_LENGTH` | integer | `8` | No | Minimum password length |
| `PASSWORD_REQUIRE_UPPERCASE` | boolean | `true` | No | Require uppercase in password |
| `PASSWORD_REQUIRE_NUMBERS` | boolean | `true` | No | Require numbers in password |
| `PASSWORD_REQUIRE_SPECIAL` | boolean | `true` | No | Require special chars in password |

### Logging

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `LOG_LEVEL` | string | `INFO` | No | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FORMAT` | string | `json` | No | Log format (json, text) |
| `LOG_FILE` | string | - | No | Log file path (optional) |

### External Services

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `SMTP_HOST` | string | - | No | Email SMTP host |
| `SMTP_PORT` | integer | `587` | No | Email SMTP port |
| `SMTP_USER` | string | - | No | Email SMTP user |
| `SMTP_PASSWORD` | string | - | No | Email SMTP password (use KMS/Vault in prod) |
| `SMTP_FROM` | string | - | No | Email from address |

### RAG Configuration

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `RAG_ENABLED` | boolean | `true` | No | Enable RAG service |
| `RAG_MODEL` | string | `all-MiniLM-L6-v2` | No | RAG embedding model |
| `RAG_CACHE_TTL` | integer | `3600` | No | RAG cache TTL (seconds) |
| `RAG_TOP_K` | integer | `5` | No | RAG top-k results |

## Environment-Specific Values

### Development

```bash
ENVIRONMENT=development
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///inventory.db
API_BASE_URL=http://localhost:5001
VITE_API_BASE_URL=http://localhost:5001
SESSION_COOKIE_SECURE=0
SESSION_COOKIE_SAMESITE=Lax
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=DEBUG
```

### Staging

```bash
ENVIRONMENT=staging
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=postgresql://user:pass@db.staging.internal:5432/inventory
API_BASE_URL=https://api.staging.example.com
VITE_API_BASE_URL=https://api.staging.example.com
SESSION_COOKIE_SECURE=1
SESSION_COOKIE_SAMESITE=Strict
CORS_ORIGINS=https://staging.example.com
LOG_LEVEL=INFO
```

### Production

```bash
ENVIRONMENT=production
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=postgresql://user:pass@db.prod.internal:5432/inventory
API_BASE_URL=https://api.example.com
VITE_API_BASE_URL=https://api.example.com
SESSION_COOKIE_SECURE=1
SESSION_COOKIE_SAMESITE=Strict
CORS_ORIGINS=https://example.com
LOG_LEVEL=WARNING
```

## Secrets Management

### Development
- Store in `.env` (local, not committed)
- Use `.env.example` as template

### Staging & Production
- **Use KMS/Vault** (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault)
- Never commit secrets to repository
- Rotate secrets every 90 days
- Audit all secret access

### Secret Rotation
- JWT_SECRET: Every 90 days
- DB_PASSWORD: Every 90 days
- SMTP_PASSWORD: Every 90 days
- API keys: Every 30 days

## Validation

### Schema

```python
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    ENVIRONMENT: str
    SECRET_KEY: str  # min 32 chars
    JWT_SECRET: str  # min 32 chars
    DATABASE_URL: str
    API_BASE_URL: str
    
    @validator('SECRET_KEY', 'JWT_SECRET')
    def validate_secret_length(cls, v):
        if len(v) < 32:
            raise ValueError('Secret must be at least 32 characters')
        return v
    
    @validator('ENVIRONMENT')
    def validate_environment(cls, v):
        if v not in ['development', 'staging', 'production']:
            raise ValueError('Invalid environment')
        return v
    
    class Config:
        env_file = '.env'
```

### Validation Script

```bash
# Validate environment variables
python scripts/validate_env.py
```

## Best Practices

1. **Never commit secrets** to repository
2. **Use `.env.example`** as template with placeholder values
3. **Rotate secrets** regularly (every 90 days)
4. **Use KMS/Vault** for production secrets
5. **Audit secret access** in production
6. **Use strong secrets** (min 32 characters, random)
7. **Separate secrets** by environment
8. **Document all variables** in this file
9. **Validate on startup** to catch missing vars
10. **Use environment-specific configs** for different deployments

---

**Next Steps:**
- [ ] Implement KMS/Vault integration for prod
- [ ] Create secret rotation automation
- [ ] Add environment validation script
- [ ] Document secret access audit logs

