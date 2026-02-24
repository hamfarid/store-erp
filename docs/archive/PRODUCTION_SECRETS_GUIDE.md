# Production Secrets & Configuration Guide

## Overview

This guide explains how to configure secrets and environment variables for production deployment on GitHub Actions.

## GitHub Secrets Management

### Setting Up GitHub Secrets

1. **Navigate to Repository Settings**
   - Go to `Settings` → `Secrets and variables` → `Actions`
   
2. **Add New Secret**
   - Click "New repository secret"
   - Enter secret name and value
   - Click "Add secret"

3. **Secret Naming Convention**
   - Use UPPERCASE with UNDERSCORES
   - Prefix with environment: `PROD_`, `STAGING_`, `DEV_`
   - Example: `PROD_DATABASE_URL`

## Required Secrets by Environment

### Production Backend Secrets

```yaml
PROD_DATABASE_URL:
  Description: PostgreSQL connection string
  Format: postgresql://username:password@host:port/database
  Sensitivity: CRITICAL
  
PROD_SECRET_KEY:
  Description: Flask secret key for session management
  Format: Random 32+ character string
  Generate: python -c 'import secrets; print(secrets.token_hex(32))'
  Sensitivity: CRITICAL

PROD_JWT_SECRET:
  Description: JWT token signing secret
  Format: Random 32+ character string
  Generate: python -c 'import secrets; print(secrets.token_hex(32))'
  Sensitivity: CRITICAL

PROD_MAIL_SERVER:
  Description: SMTP server for email notifications
  Example: smtp.gmail.com
  Sensitivity: MEDIUM

PROD_MAIL_PORT:
  Description: SMTP port
  Example: 587
  Sensitivity: LOW

PROD_MAIL_USERNAME:
  Description: Email service username
  Sensitivity: CRITICAL

PROD_MAIL_PASSWORD:
  Description: Email service password/app-password
  Sensitivity: CRITICAL

PROD_AWS_ACCESS_KEY_ID:
  Description: AWS access key for S3/storage (if used)
  Sensitivity: CRITICAL

PROD_AWS_SECRET_ACCESS_KEY:
  Description: AWS secret access key
  Sensitivity: CRITICAL

PROD_AWS_S3_BUCKET:
  Description: S3 bucket name for file storage
  Example: my-store-production
  Sensitivity: MEDIUM

PROD_SENTRY_DSN:
  Description: Sentry error tracking URL (optional)
  Format: https://key@sentry.io/project-id
  Sensitivity: MEDIUM

PROD_LOG_LEVEL:
  Description: Logging level
  Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
  Default: INFO
  Sensitivity: LOW

PROD_API_CORS_ORIGINS:
  Description: Comma-separated list of allowed CORS origins
  Example: https://production.com,https://app.production.com
  Sensitivity: LOW
```

### Production Frontend Secrets

```yaml
PROD_API_URL:
  Description: Backend API endpoint URL
  Example: https://api.production.com
  Sensitivity: LOW

PROD_APP_URL:
  Description: Frontend application URL
  Example: https://production.com
  Sensitivity: LOW

PROD_AUTH_DOMAIN:
  Description: Authentication domain (OAuth/SAML)
  Sensitivity: MEDIUM

PROD_STRIPE_PUBLIC_KEY:
  Description: Stripe publishable key (if using payments)
  Sensitivity: LOW (public key)

PROD_SENTRY_DSN_FRONTEND:
  Description: Frontend error tracking
  Sensitivity: MEDIUM

PROD_ANALYTICS_KEY:
  Description: Analytics tracking key (Google Analytics, etc.)
  Sensitivity: LOW
```

### Docker Registry Secrets

```yaml
REGISTRY_USERNAME:
  Description: GitHub Container Registry username
  Example: hamfarid
  Sensitivity: CRITICAL

REGISTRY_PASSWORD:
  Description: GitHub Container Registry PAT token
  Note: Use GitHub personal access token with 'write:packages' scope
  Sensitivity: CRITICAL

DOCKER_REGISTRY:
  Description: Container registry URL
  Default: ghcr.io
  Sensitivity: LOW
```

### Deployment Secrets

```yaml
DEPLOY_SSH_KEY:
  Description: SSH private key for production server deployment
  Format: RSA/Ed25519 private key
  Sensitivity: CRITICAL

DEPLOY_SSH_HOST:
  Description: Production server hostname/IP
  Sensitivity: CRITICAL

DEPLOY_SSH_USER:
  Description: SSH user for deployment
  Example: deploy
  Sensitivity: HIGH

PROD_DEPLOY_TOKEN:
  Description: Token for deployment services
  Sensitivity: CRITICAL
```

## How to Generate Secure Secrets

### Python (for Backend Secrets)

```python
import secrets
import string

# Generate random string
def generate_secret(length=32):
    return secrets.token_urlsafe(length)

# For database password
def generate_password(length=24):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

# Examples
print("Secret Key:", generate_secret(32))
print("JWT Secret:", generate_secret(32))
print("DB Password:", generate_password(24))
```

### OpenSSL

```bash
# Generate random hex string
openssl rand -hex 32

# Generate base64 encoded secret
openssl rand -base64 32
```

### Using GitHub Secrets in Workflows

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy backend
        env:
          DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
          SECRET_KEY: ${{ secrets.PROD_SECRET_KEY }}
          JWT_SECRET: ${{ secrets.PROD_JWT_SECRET }}
          MAIL_SERVER: ${{ secrets.PROD_MAIL_SERVER }}
          MAIL_USERNAME: ${{ secrets.PROD_MAIL_USERNAME }}
          MAIL_PASSWORD: ${{ secrets.PROD_MAIL_PASSWORD }}
          AWS_ACCESS_KEY_ID: ${{ secrets.PROD_AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.PROD_AWS_SECRET_ACCESS_KEY }}
        run: |
          docker compose -f docker-compose.prod.yml up -d backend
      
      - name: Deploy frontend
        env:
          REACT_APP_API_URL: ${{ secrets.PROD_API_URL }}
          REACT_APP_SENTRY_DSN: ${{ secrets.PROD_SENTRY_DSN_FRONTEND }}
        run: |
          docker compose -f docker-compose.prod.yml up -d frontend
```

## Environment Files

### `.env.production` (DO NOT commit to git)

```bash
# Backend Configuration
FLASK_ENV=production
FLASK_APP=backend/app.py
FLASK_DEBUG=False

# Database
SQLALCHEMY_DATABASE_URI=${PROD_DATABASE_URL}
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=False

# Security
SECRET_KEY=${PROD_SECRET_KEY}
JWT_SECRET_KEY=${PROD_JWT_SECRET}
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Email
MAIL_SERVER=${PROD_MAIL_SERVER}
MAIL_PORT=${PROD_MAIL_PORT:-587}
MAIL_USE_TLS=True
MAIL_USERNAME=${PROD_MAIL_USERNAME}
MAIL_PASSWORD=${PROD_MAIL_PASSWORD}

# AWS (optional)
AWS_ACCESS_KEY_ID=${PROD_AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${PROD_AWS_SECRET_ACCESS_KEY}
AWS_S3_BUCKET=${PROD_AWS_S3_BUCKET}

# Logging
LOG_LEVEL=${PROD_LOG_LEVEL:-INFO}
LOG_FILE=/var/log/app/app.log

# Error Tracking
SENTRY_DSN=${PROD_SENTRY_DSN}
```

### `.env.production.local` (Machine-specific, DO NOT commit)

```bash
# Machine-specific settings
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=<generate-secure-password>
REDIS_PASSWORD=<generate-secure-password>
```

## Security Best Practices

### DO's ✅

- [x] Use GitHub Secrets for all sensitive data
- [x] Rotate secrets regularly (at least every 90 days)
- [x] Use strong, randomly generated secrets (32+ characters)
- [x] Document secret purposes (not values)
- [x] Audit secret access in GitHub logs
- [x] Use separate secrets for each environment
- [x] Use principle of least privilege for service accounts
- [x] Enable GitHub organization-level secret management
- [x] Use encrypted containers for secrets
- [x] Review workflow access to secrets

### DON'Ts ❌

- [x] NEVER commit secrets to git
- [x] NEVER log or print secrets
- [x] NEVER share secrets via email/chat
- [x] NEVER use default/weak passwords
- [x] NEVER reuse secrets across environments
- [x] NEVER hardcode secrets in Docker images
- [x] NEVER expose secrets in public logs
- [x] NEVER use plain text for storage
- [x] NEVER grant unnecessary secret access

## Secret Rotation

### Monthly Secret Rotation Procedure

```bash
#!/bin/bash
# Script to help rotate secrets (requires manual updates in GitHub)

SECRETS_TO_ROTATE=(
  "PROD_SECRET_KEY"
  "PROD_JWT_SECRET"
  "PROD_MAIL_PASSWORD"
  "PROD_AWS_SECRET_ACCESS_KEY"
  "DEPLOY_SSH_KEY"
)

for secret in "${SECRETS_TO_ROTATE[@]}"; do
  echo "❗ Update $secret in GitHub Secrets"
  echo "  1. Go to Settings → Secrets and variables → Actions"
  echo "  2. Find $secret"
  echo "  3. Click 'Update secret'"
  echo "  4. Generate new value: python -c 'import secrets; print(secrets.token_hex(32))'"
  echo "  5. Update and confirm"
  echo ""
done
```

### Post-Rotation Tasks

1. Update dependent systems
2. Test with new secrets
3. Monitor for issues
4. Document rotation date
5. Notify team of changes

## Monitoring Secret Usage

### GitHub Audit Log Queries

```bash
# View secret access logs
# Settings → Audit log → Filter by "secret"

# Expected queries:
- Repository secret accessed by workflow
- Repository secret updated
- Organization secret accessed
```

## Troubleshooting

### Secret Not Available in Workflow

```yaml
# Problem: Secret appears undefined in workflow

# Solution: Ensure proper access
- Check secret exists in Settings → Secrets
- Verify secret name matches exactly (case-sensitive)
- Check workflow has proper permissions
- Ensure secret scope (repository vs organization)
```

### Secret Leaked Accidentally

1. **Immediately Rotate** the exposed secret
2. **Revoke** any credentials (API keys, tokens, etc.)
3. **Scan** for usage in logs and commits
4. **Notify** relevant teams
5. **Generate** new credentials
6. **Update** GitHub Secrets
7. **Monitor** for unauthorized access

## References

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Security Best Practices](https://docs.github.com/en/organizations/managing-organization-access-to-your-repositories/roles-in-an-organization)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

Last Updated: January 31, 2026
Maintained By: DevOps Team
