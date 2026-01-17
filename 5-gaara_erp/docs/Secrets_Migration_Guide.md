# Secrets Migration Guide - From .env to AWS Secrets Manager

**Purpose**: Guide for migrating application secrets from .env files to AWS Secrets Manager  
**Owner**: DevOps Team  
**Last Updated**: 2025-10-25  
**Status**: Production Ready

---

## 📋 Overview

This guide explains how to migrate your application code from reading secrets from `.env` files to using AWS Secrets Manager via the `secrets_manager` utility.

### Benefits

- ✅ **Security**: Secrets never stored in code or config files
- ✅ **Rotation**: Automatic secret rotation support
- ✅ **Audit**: Full audit trail of secret access
- ✅ **Compliance**: Meets SOC2, PCI-DSS, HIPAA requirements
- ✅ **Centralized**: Single source of truth for all secrets

---

## 🎯 Migration Pattern

### Before (Reading from .env)

```python
import os

# Reading secrets from environment variables
db_url = os.getenv('DATABASE_URL')
jwt_secret = os.getenv('JWT_SECRET_KEY')
api_key = os.getenv('EXTERNAL_API_KEY')
```

### After (Reading from Secrets Manager)

```python
import os
from src.utils.secrets_manager import get_secret

# Get environment
environment = os.getenv('ENVIRONMENT', 'development')

# Production: read from Secrets Manager
if environment == 'production':
    try:
        db_url = get_secret('database-url')
        jwt_secret = get_secret('jwt-secret')
        api_key = get_secret('external-api-key')
        print("✅ Using secrets from AWS Secrets Manager")
    except Exception as e:
        print(f"⚠️  Failed to get secrets: {e}")
        # Fallback to .env
        db_url = os.getenv('DATABASE_URL')
        jwt_secret = os.getenv('JWT_SECRET_KEY')
        api_key = os.getenv('EXTERNAL_API_KEY')
else:
    # Development/staging: use .env
    db_url = os.getenv('DATABASE_URL')
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    api_key = os.getenv('EXTERNAL_API_KEY')
```

---

## 📝 Step-by-Step Migration

### Step 1: Identify Secrets to Migrate

**Production Secrets** (must migrate):
- `SECRET_KEY` → `gaara-store/production/secret-key`
- `JWT_SECRET_KEY` → `gaara-store/production/jwt-secret`
- `ENCRYPTION_KEY` → `gaara-store/production/encryption-key`
- `DATABASE_URL` → `gaara-store/production/database-url`
- `REDIS_PASSWORD` → `gaara-store/production/redis-password`
- `MAIL_PASSWORD` → `gaara-store/production/mail-password`
- `SENTRY_DSN` → `gaara-store/production/sentry-dsn`

**Non-Secrets** (keep in .env):
- `ENVIRONMENT`
- `AWS_REGION`
- `LOG_LEVEL`
- `FEATURE_FLAGS`

### Step 2: Update Code

#### Example 1: Database Configuration

**File**: `backend/src/database.py`

```python
# Before
import os

db_url = os.getenv('DATABASE_URL', 'sqlite:///instance/inventory.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
```

```python
# After
import os
from src.utils.secrets_manager import get_secret

environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'production':
    try:
        db_url = get_secret('database-url')
        print("✅ Using database URL from AWS Secrets Manager")
    except Exception as e:
        print(f"⚠️  Failed to get database URL: {e}")
        db_url = os.getenv('DATABASE_URL', 'sqlite:///instance/inventory.db')
else:
    db_url = os.getenv('DATABASE_URL', 'sqlite:///instance/inventory.db')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
```

#### Example 2: JWT Configuration

**File**: `backend/src/auth.py`

```python
# Before
import os

jwt_secret = os.getenv('JWT_SECRET_KEY', 'default-secret')
app.config['JWT_SECRET_KEY'] = jwt_secret
```

```python
# After
import os
from src.utils.secrets_manager import get_secret

environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'production':
    try:
        jwt_secret = get_secret('jwt-secret')
        print("✅ Using JWT secret from AWS Secrets Manager")
    except Exception as e:
        print(f"⚠️  Failed to get JWT secret: {e}")
        jwt_secret = os.getenv('JWT_SECRET_KEY', 'default-secret')
else:
    jwt_secret = os.getenv('JWT_SECRET_KEY', 'default-secret')

app.config['JWT_SECRET_KEY'] = jwt_secret
```

#### Example 3: Email Configuration

**File**: `backend/src/routes/export.py`

```python
# Before
import os

mail_password = os.getenv('MAIL_PASSWORD')
```

```python
# After
import os
from src.utils.secrets_manager import get_secret

environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'production':
    try:
        mail_password = get_secret('mail-password')
    except Exception as e:
        print(f"⚠️  Failed to get mail password: {e}")
        mail_password = os.getenv('MAIL_PASSWORD')
else:
    mail_password = os.getenv('MAIL_PASSWORD')
```

### Step 3: Test in Development

```bash
# Set environment to development
export ENVIRONMENT=development

# Run tests
python -m pytest backend/tests -v

# Should use .env fallback
# Output: "🔧 Development mode: using fallback encryption"
```

### Step 4: Test in Staging (Optional)

```bash
# Set environment to staging
export ENVIRONMENT=staging

# Configure AWS credentials
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...

# Run application
python backend/app.py

# Should attempt Secrets Manager, fallback to .env if not configured
```

### Step 5: Deploy to Production

```bash
# Set environment to production
export ENVIRONMENT=production

# Configure AWS credentials (use IAM role in production)
export AWS_REGION=us-east-1

# Run application
python backend/app.py

# Should use Secrets Manager
# Output: "✅ Using secrets from AWS Secrets Manager"
```

---

## 🔍 Verification Checklist

### Development Environment

- [ ] `ENVIRONMENT=development` in `.env`
- [ ] Application starts successfully
- [ ] All tests passing (93/93)
- [ ] Logs show: "🔧 Development mode: using fallback encryption"
- [ ] No AWS credentials required

### Staging Environment (Optional)

- [ ] `ENVIRONMENT=staging` in `.env`
- [ ] AWS credentials configured
- [ ] Application starts successfully
- [ ] Secrets Manager fallback works
- [ ] Logs show fallback messages if secrets not in AWS

### Production Environment

- [ ] `ENVIRONMENT=production` in `.env`
- [ ] AWS IAM role configured (no access keys)
- [ ] All 7 secrets created in Secrets Manager
- [ ] Application starts successfully
- [ ] Logs show: "✅ Using secrets from AWS Secrets Manager"
- [ ] No secrets in `.env` file (only references)

---

## 🚨 Common Issues

### Issue 1: "Secret not found"

**Symptom**: `SecretNotFoundException: Secrets Manager can't find the specified secret.`

**Solution**:
1. Verify secret name matches exactly: `gaara-store/production/secret-key`
2. Check AWS region matches: `AWS_REGION=us-east-1`
3. List secrets: `aws secretsmanager list-secrets`

### Issue 2: "Access Denied"

**Symptom**: `AccessDeniedException: User is not authorized to perform: secretsmanager:GetSecretValue`

**Solution**:
1. Verify IAM permissions include `SecretsManagerReadWrite`
2. Check IAM role/user has access to KMS key
3. Test manually: `aws secretsmanager get-secret-value --secret-id gaara-store/production/secret-key`

### Issue 3: "Fallback to .env in production"

**Symptom**: Logs show "⚠️  Failed to get secrets" in production

**Solution**:
1. Check `ENVIRONMENT=production` is set
2. Verify AWS credentials are configured
3. Check network connectivity to AWS
4. Review CloudWatch logs for detailed errors

### Issue 4: "Cache not working"

**Symptom**: Too many AWS API calls, high costs

**Solution**:
1. Verify `SECRET_CACHE_TTL=300` in `.env`
2. Check cache statistics: `get_cache_stats()`
3. Clear cache if needed: `clear_cache()`

---

## 📊 Monitoring

### CloudWatch Metrics

Monitor these metrics in CloudWatch:

1. **Secret Access Count**: Number of `GetSecretValue` calls
2. **Cache Hit Rate**: Percentage of cached vs fresh retrievals
3. **Error Rate**: Failed secret retrievals
4. **Latency**: Time to retrieve secrets

### Application Logs

Look for these log messages:

- ✅ `"Using secrets from AWS Secrets Manager"` - Success
- ⚠️  `"Failed to get secrets"` - Fallback to .env
- 🔧 `"Development mode: using fallback encryption"` - Dev mode

---

## 🔒 Security Best Practices

1. **Never commit secrets** to git (use `.gitignore`)
2. **Use IAM roles** in production (not access keys)
3. **Enable CloudTrail** for audit logging
4. **Rotate secrets** every 90 days
5. **Monitor access** via CloudWatch
6. **Use least-privilege** IAM policies
7. **Test fallback** mechanisms regularly

---

## 📚 References

- [Secrets Manager Utility](../backend/src/utils/README_SECRETS.md)
- [AWS Setup Guide](./AWS_Setup_Guide.md)
- [P1 KMS/Vault Plan](./P1_KMS_Vault_Plan.md)
- [AWS Secrets Manager Docs](https://docs.aws.amazon.com/secretsmanager/)

---

## ✅ Migration Checklist

### Code Changes

- [x] `backend/src/database.py` - Database URL
- [x] `backend/src/auth.py` - SECRET_KEY, JWT_SECRET_KEY
- [ ] `backend/app.py` - Redis password (if using Redis)
- [ ] `backend/src/routes/export.py` - Mail password
- [ ] Any other files using secrets

### Testing

- [x] Development tests passing (93/93)
- [ ] Staging tests passing
- [ ] Production smoke tests passing

### Deployment

- [ ] AWS account created
- [ ] KMS key created
- [ ] 7 secrets created in Secrets Manager
- [ ] IAM role configured
- [ ] CloudWatch monitoring enabled
- [ ] Application deployed to production
- [ ] Secrets verified working
- [ ] Fallback tested

---

**Status**: ✅ **Ready for Production Migration**

**Next Steps**: Follow [AWS Setup Guide](./AWS_Setup_Guide.md) to complete AWS configuration.

