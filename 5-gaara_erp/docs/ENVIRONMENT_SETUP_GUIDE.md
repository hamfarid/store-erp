# 🔐 Environment Configuration Guide
# دليل إعداد بيئة النظام

**Project:** Gaara ERP v12  
**Version:** 1.0.0  
**Date:** January 15, 2026

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Backend Configuration](#backend-configuration)
3. [Frontend Configuration](#frontend-configuration)
4. [Environment-Specific Setup](#environment-specific-setup)
5. [Security Best Practices](#security-best-practices)
6. [Validation & Testing](#validation--testing)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Navigate to backend
cd D:\Ai_Project\5-gaara_erp\backend

# Generate secure secrets
python scripts/generate_secrets.py --format env > .env.secrets

# Copy template and add generated secrets
cp config/env.template .env
# Then copy secrets from .env.secrets to .env

# Validate configuration
python scripts/validate_env.py

# Frontend setup
cd ../frontend
cp config/env.template .env
# Edit VITE_API_BASE_URL if needed
```

### Option 2: Manual Setup

```bash
# Backend
cd backend
cp config/env.template .env
# Edit .env manually

# Frontend
cd frontend
cp config/env.template .env
# Edit .env manually
```

---

## 🔧 Backend Configuration

### File Location
**Development:** `backend/.env`  
**Production:** `backend/.env.production`  
**Template:** `backend/config/env.template`

### Required Variables

#### 1. SECRET_KEY
```bash
# Flask session encryption key
# MUST be 32+ random characters
# Generate with:
python -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(32)}')"

SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

**Purpose:**
- Flask session cookie encryption
- CSRF token signing
- General security operations

**Security:**
- ❌ DO NOT use: "secret", "password", "changeme"
- ❌ DO NOT use: short keys (<32 chars)
- ❌ DO NOT reuse: between environments
- ✅ DO use: `secrets.token_hex(32)` or equivalent
- ✅ DO rotate: every 90 days in production

---

#### 2. JWT_SECRET_KEY
```bash
# JWT access token signing key
# MUST be 32+ random characters, DIFFERENT from SECRET_KEY
JWT_SECRET_KEY=b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1
```

**Purpose:**
- Signs JWT access tokens (short-lived)
- Validates token authenticity
- Prevents token tampering

---

#### 3. JWT_REFRESH_SECRET_KEY
```bash
# JWT refresh token signing key
# MUST be 32+ random characters, DIFFERENT from other keys
JWT_REFRESH_SECRET_KEY=c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a1b2
```

**Purpose:**
- Signs JWT refresh tokens (long-lived)
- Enables token refresh without re-login
- Separate key allows independent rotation

---

#### 4. DATABASE_URL
```bash
# Development
DATABASE_URL=sqlite:///instance/gaara_erp.db

# Production (PostgreSQL)
DATABASE_URL=postgresql://gaara_user:secure_password@localhost:10502/gaara_erp_prod
```

**Format:**
- SQLite: `sqlite:///path/to/database.db`
- PostgreSQL: `postgresql://user:password@host:port/database`
- MySQL: `mysql://user:password@host:port/database`

---

### Recommended Variables

#### Redis Configuration
```bash
# Redis for caching, sessions, and Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
```

#### Environment Settings
```bash
FLASK_ENV=development  # or production, staging
DEBUG=True             # False in production
LOG_LEVEL=INFO         # WARNING in production
```

---

### Optional AI Service Keys

```bash
# OpenAI (ChatGPT, GPT-4)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# PyBrops (Agricultural AI)
PYBROPS_API_KEY=pybrops-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Where to Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- PyBrops: Contact PyBrops support

---

## 🎨 Frontend Configuration

### File Location
**Development:** `frontend/.env`  
**Production:** `frontend/.env.production`  
**Template:** `frontend/config/env.template`

### Required Variables

#### VITE_API_BASE_URL
```bash
# Development
VITE_API_BASE_URL=http://localhost:5001

# Production (HTTPS required)
VITE_API_BASE_URL=https://api.gaara-erp.com
```

**Important:**
- Must match backend URL
- Production MUST use HTTPS
- No trailing slash
- Include port if non-standard

---

### Recommended Variables

```bash
# Application Settings
VITE_APP_ENV=development
VITE_APP_TITLE=Gaara ERP v12
VITE_DEFAULT_LANGUAGE=ar
VITE_DEFAULT_CURRENCY=SAR

# Features
VITE_ENABLE_MFA=true
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_RTL=true
VITE_ENABLE_PWA=false

# Security
VITE_SESSION_TIMEOUT=30
VITE_IDLE_TIMEOUT=15
```

---

## 🌍 Environment-Specific Setup

### Development Environment

**Backend `.env`:**
```bash
SECRET_KEY=dev-secret-key-for-local-testing-only
JWT_SECRET_KEY=dev-jwt-key-for-local-testing-only
JWT_REFRESH_SECRET_KEY=dev-jwt-refresh-key-for-local-testing-only
DATABASE_URL=sqlite:///instance/gaara_erp_dev.db
REDIS_URL=redis://localhost:6379/0
FLASK_ENV=development
DEBUG=True
LOG_LEVEL=DEBUG
```

**Frontend `.env`:**
```bash
VITE_API_BASE_URL=http://localhost:5001
VITE_APP_ENV=development
VITE_ENABLE_MFA=false
```

**Characteristics:**
- ✅ SQLite database (fast, no setup)
- ✅ Debug mode enabled (detailed errors)
- ✅ Verbose logging
- ✅ Hot reload enabled
- ✅ API docs enabled

---

### Staging Environment

**Backend `.env.staging`:**
```bash
SECRET_KEY=staging-secret-key-32-chars-random-value
JWT_SECRET_KEY=staging-jwt-key-32-chars-random-value
JWT_REFRESH_SECRET_KEY=staging-jwt-refresh-32-chars-random
DATABASE_URL=postgresql://gaara_staging:password@localhost:10502/gaara_erp_staging
REDIS_URL=redis://localhost:6375/0
FLASK_ENV=staging
DEBUG=False
LOG_LEVEL=INFO
```

**Frontend `.env.staging`:**
```bash
VITE_API_BASE_URL=https://staging-api.gaara-erp.com
VITE_APP_ENV=staging
VITE_ENABLE_MFA=true
VITE_SENTRY_DSN=https://staging@sentry.io/project
```

**Characteristics:**
- ✅ PostgreSQL database (production-like)
- ✅ Debug disabled
- ✅ Moderate logging
- ✅ HTTPS enabled
- ✅ MFA enabled
- ✅ Sentry error tracking

---

### Production Environment

**Backend `.env.production`:**
```bash
# Load from KMS/Vault in production
SECRET_KEY=${VAULT:secret/gaara_erp/secret_key}
JWT_SECRET_KEY=${VAULT:secret/gaara_erp/jwt_secret}
JWT_REFRESH_SECRET_KEY=${VAULT:secret/gaara_erp/jwt_refresh}
DATABASE_URL=postgresql://gaara_prod:${VAULT:secret/gaara_erp/db_password}@db-prod:10502/gaara_erp
REDIS_URL=redis://redis-prod:6375/0
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=WARNING
```

**Frontend `.env.production`:**
```bash
VITE_API_BASE_URL=https://api.gaara-erp.com
VITE_APP_ENV=production
VITE_ENABLE_MFA=true
VITE_ENABLE_PWA=true
VITE_SENTRY_DSN=https://prod@sentry.io/project
VITE_GA_TRACKING_ID=UA-XXXXXXXXX-X
```

**Characteristics:**
- ✅ PostgreSQL cluster (high availability)
- ✅ Debug completely disabled
- ✅ Minimal logging (WARNING+)
- ✅ HTTPS enforced
- ✅ MFA required
- ✅ Secrets from Vault/KMS
- ✅ Full monitoring (Sentry, GA)
- ✅ PWA enabled

---

## 🔒 Security Best Practices

### 1. Secret Generation

**DO:**
```bash
# ✅ Use cryptographically secure random generation
python scripts/generate_secrets.py

# ✅ Or use Python secrets module
python -c "import secrets; print(secrets.token_hex(32))"

# ✅ Or use OpenSSL
openssl rand -hex 32
```

**DON'T:**
```bash
# ❌ Never use weak secrets
SECRET_KEY=password123
SECRET_KEY=changeme
SECRET_KEY=secret

# ❌ Never use same secret across environments
SECRET_KEY=my-universal-key  # Used in dev AND prod

# ❌ Never use short secrets
SECRET_KEY=abc123  # Too short
```

---

### 2. Secret Storage

**Development:**
- Store in `.env` file (local only)
- Add `.env` to `.gitignore`
- Use weak/simple secrets (faster dev)

**Staging:**
- Store in `.env.staging` file (server only)
- Use moderate-strength secrets
- Rotate quarterly

**Production:**
- ✅ **Store in KMS/Vault** (HashiCorp Vault, AWS Secrets Manager)
- ✅ Load secrets at runtime
- ✅ Rotate monthly
- ✅ Audit secret access
- ❌ NEVER store in `.env` file
- ❌ NEVER commit to version control
- ❌ NEVER send via email/chat

---

### 3. Secret Rotation

**Rotation Schedule:**
- Development: No rotation needed
- Staging: Every 90 days
- Production: Every 30 days

**Rotation Process:**
1. Generate new secret
2. Add to Vault/KMS with new version
3. Deploy with old + new secret (grace period)
4. Update application to use new secret
5. Remove old secret after grace period
6. Verify all services working

---

### 4. Access Control

**Who Needs Access:**
- Development Secrets: All developers
- Staging Secrets: DevOps + QA team
- Production Secrets: DevOps team ONLY (2-3 people max)

**Access Methods:**
- Development: Local `.env` file
- Staging: CI/CD variables
- Production: Vault/KMS with IAM roles

---

## ✅ Validation & Testing

### Validate Environment Configuration

```bash
# Development validation
cd backend
python scripts/validate_env.py

# Production validation (strict mode)
python scripts/validate_env.py --strict --env-file .env.production
```

### Test Secret Strength

```bash
# Check if secrets meet minimum requirements
python scripts/validate_env.py

# Output shows:
# ✅ SECRET_KEY: VALID (64 chars)
# ❌ JWT_SECRET_KEY: Too short (20 chars, need 32+)
```

### Generate Test Secrets

```bash
# Generate with default length (32 bytes = 64 hex chars)
python scripts/generate_secrets.py

# Generate longer secrets
python scripts/generate_secrets.py --length 64

# Generate in different formats
python scripts/generate_secrets.py --format env
python scripts/generate_secrets.py --format json
python scripts/generate_secrets.py --format python
```

---

## 🐳 Docker Environment Setup

### Using docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    env_file:
      - .env
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379/0
    
  frontend:
    env_file:
      - .env
    environment:
      - VITE_API_BASE_URL=http://backend:5001
```

### Using .env in Docker

```bash
# Copy template
docker cp config/env.template backend-container:/app/.env

# Or mount as volume
volumes:
  - ./.env:/app/.env:ro  # Read-only for security
```

---

## 🔧 Troubleshooting

### Issue: "SECRET_KEY not set" Error

**Cause:** `.env` file not loaded or SECRET_KEY missing

**Solutions:**
1. Check `.env` file exists in backend root
2. Verify SECRET_KEY is set (not empty)
3. Check file is not in `.gitignore`
4. Restart application after changes

```bash
# Verify .env file
cd backend
cat .env | grep SECRET_KEY

# Should output: SECRET_KEY=your-secret-here
```

---

### Issue: "JWT token verification failed"

**Cause:** JWT_SECRET_KEY mismatch or changed

**Solutions:**
1. Verify JWT_SECRET_KEY is correct
2. Check if key was rotated
3. Clear old tokens from clients
4. Re-login to get new token

```bash
# Clear tokens from localStorage
# In browser console:
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
```

---

### Issue: "Cannot connect to database"

**Cause:** Invalid DATABASE_URL

**Solutions:**
1. Check DATABASE_URL format
2. Verify database is running
3. Check credentials
4. Check network connectivity

```bash
# Test PostgreSQL connection
psql "${DATABASE_URL}"

# Test SQLite file exists
ls -lh instance/gaara_erp.db
```

---

### Issue: "Frontend can't reach backend"

**Cause:** VITE_API_BASE_URL incorrect

**Solutions:**
1. Check backend is running: `curl http://localhost:5001/api/health`
2. Verify VITE_API_BASE_URL matches backend port
3. Check CORS configuration
4. Verify firewall rules

```bash
# Test backend health
curl http://localhost:5001/api/health

# Check CORS
curl -H "Origin: http://localhost:5501" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS http://localhost:5001/api/health -v
```

---

## 📊 Environment Variables Reference

### Complete Variable List

#### Backend (Python/Flask)

| Category | Variable | Required | Default |
|----------|----------|----------|---------|
| **Security** | SECRET_KEY | ✅ | None |
| **Security** | JWT_SECRET_KEY | ✅ | None |
| **Security** | JWT_REFRESH_SECRET_KEY | ✅ | None |
| **Database** | DATABASE_URL | ✅ | None |
| **Cache** | REDIS_URL | ⚠️ | redis://localhost:6379/0 |
| **Queue** | CELERY_BROKER_URL | ⚠️ | redis://localhost:6379/0 |
| **App** | FLASK_ENV | ⚠️ | development |
| **App** | DEBUG | ⚠️ | True |
| **AI** | OPENAI_API_KEY | ➖ | None |
| **AI** | ANTHROPIC_API_KEY | ➖ | None |
| **AI** | PYBROPS_API_KEY | ➖ | None |
| **Email** | MAIL_SERVER | ➖ | None |
| **Email** | MAIL_USERNAME | ➖ | None |
| **Email** | MAIL_PASSWORD | ➖ | None |
| **Telegram** | TELEGRAM_BOT_TOKEN | ➖ | None |
| **Monitoring** | SENTRY_DSN | ➖ | None |
| **Ports** | BACKEND_PORT | ➖ | 5001 |

**Legend:**
- ✅ Required (app won't start)
- ⚠️ Recommended (functionality affected)
- ➖ Optional (feature-specific)

---

#### Frontend (React/Vite)

| Category | Variable | Required | Default |
|----------|----------|----------|---------|
| **API** | VITE_API_BASE_URL | ✅ | None |
| **App** | VITE_APP_ENV | ⚠️ | development |
| **App** | VITE_APP_TITLE | ➖ | Gaara ERP v12 |
| **Locale** | VITE_DEFAULT_LANGUAGE | ➖ | ar |
| **Locale** | VITE_DEFAULT_CURRENCY | ➖ | SAR |
| **Features** | VITE_ENABLE_MFA | ➖ | false |
| **Features** | VITE_ENABLE_PWA | ➖ | false |
| **Analytics** | VITE_GA_TRACKING_ID | ➖ | None |
| **Monitoring** | VITE_SENTRY_DSN | ➖ | None |
| **Security** | VITE_SESSION_TIMEOUT | ➖ | 30 |

---

## 🛠️ Helper Scripts

### 1. Generate Secrets

**Location:** `backend/scripts/generate_secrets.py`

```bash
# Basic usage (human-readable)
python scripts/generate_secrets.py

# Output in .env format
python scripts/generate_secrets.py --format env > .env.secrets

# Generate longer secrets (64 bytes)
python scripts/generate_secrets.py --length 64

# JSON format (for programmatic use)
python scripts/generate_secrets.py --format json
```

**Features:**
- Cryptographically secure random generation
- Multiple output formats
- Includes password generator
- UUID generator

---

### 2. Validate Environment

**Location:** `backend/scripts/validate_env.py`

```bash
# Basic validation (development)
python scripts/validate_env.py

# Strict validation (production)
python scripts/validate_env.py --strict

# Validate specific file
python scripts/validate_env.py --env-file .env.production --strict
```

**Checks:**
- ✅ All required variables present
- ✅ Secret length >= 32 characters
- ✅ No weak patterns (password, changeme, etc.)
- ✅ Production-specific rules (DEBUG=False, etc.)
- ✅ Database URL format
- ✅ Secret entropy

**Exit Codes:**
- `0` - All checks passed
- `1` - Errors found (missing required vars)
- `2` - Warnings in strict mode

---

## 📚 Examples

### Complete Development Setup

```bash
# Backend
cd backend

# Generate secrets
python scripts/generate_secrets.py --format env > .env.secrets

# Create .env from template
cp config/env.template .env

# Append generated secrets
cat .env.secrets >> .env

# Edit .env to set DATABASE_URL and other settings
nano .env

# Validate
python scripts/validate_env.py

# Frontend
cd ../frontend
cp config/env.template .env
# Edit VITE_API_BASE_URL if needed

# Start services
cd ../backend
python src/main.py  # Backend on 5001

cd ../frontend
npm run dev  # Frontend on 5501
```

---

### Complete Production Setup

```bash
# 1. Set up Vault/KMS
vault kv put secret/gaara_erp/prod \
  secret_key="$(python scripts/generate_secrets.py --format env | grep SECRET_KEY)" \
  jwt_secret="$(python scripts/generate_secrets.py --format env | grep JWT_SECRET_KEY)"

# 2. Configure backend to load from Vault
# (See Vault integration guide)

# 3. Create production .env with Vault references
cp config/env.production.template .env.production

# 4. Validate strictly
python scripts/validate_env.py --env-file .env.production --strict

# 5. Deploy with secrets from Vault
```

---

## 🚨 Production Deployment Checklist

### Pre-Deployment

- [ ] All required variables configured
- [ ] All secrets stored in Vault/KMS
- [ ] Validation passed with `--strict` mode
- [ ] DEBUG=False
- [ ] FLASK_ENV=production
- [ ] PostgreSQL database configured
- [ ] Redis configured
- [ ] HTTPS certificates installed
- [ ] CORS origins configured correctly
- [ ] SESSION_COOKIE_SECURE=True
- [ ] API docs disabled
- [ ] Monitoring configured (Sentry)
- [ ] Logging configured
- [ ] Backup strategy in place

### Post-Deployment

- [ ] Health check passes: `curl https://api.company.com/api/health`
- [ ] Login works
- [ ] JWT tokens issued correctly
- [ ] Permissions enforced
- [ ] MFA works (if enabled)
- [ ] Email notifications work (if configured)
- [ ] Celery tasks executing
- [ ] Redis caching working
- [ ] Logs being written
- [ ] Sentry receiving errors
- [ ] Prometheus metrics available

---

## 📖 Additional Resources

### Documentation
- [ENV_CONFIGURATION.md](./ENV_CONFIGURATION.md) - Detailed variable reference
- [SECURITY_GUIDE.md](./SECURITY_GUIDE.md) - Security best practices
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Deployment instructions

### External Resources
- Flask Configuration: https://flask.palletsprojects.com/en/latest/config/
- Vite Env Variables: https://vitejs.dev/guide/env-and-mode.html
- HashiCorp Vault: https://www.vaultproject.io/
- AWS Secrets Manager: https://aws.amazon.com/secrets-manager/

---

## 💡 Pro Tips

1. **Use .envrc with direnv**
```bash
# Install direnv
# Create .envrc
echo "dotenv" > .envrc
direnv allow
# Automatically loads .env when entering directory
```

2. **Environment-specific npm scripts**
```json
{
  "scripts": {
    "dev": "vite --mode development",
    "build:staging": "vite build --mode staging",
    "build:prod": "vite build --mode production"
  }
}
```

3. **Secret rotation script**
```bash
# Automate secret rotation
python scripts/rotate_secrets.py --environment production
```

4. **Health check with env validation**
```bash
# Add to startup script
python scripts/validate_env.py --strict || exit 1
python src/main.py
```

---

**Status:** ✅ **COMPLETE GUIDE**  
**Last Updated:** January 15, 2026  
**Version:** 1.0.0

---

*For questions or issues, contact: devops@gaara-erp.com*
