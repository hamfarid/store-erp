# Secrets Manager - Usage Guide

## Overview

The Secrets Manager provides secure secret retrieval with caching, fallback to `.env`, and integration with AWS Secrets Manager.

## Quick Start

### Development (Local)

```python
from src.utils.secrets_manager import get_secret

# Secrets are read from .env in development mode
db_url = get_secret('database-url')  # Reads DATABASE_URL from .env
jwt_secret = get_secret('jwt-secret')  # Reads JWT_SECRET from .env
```

### Production (AWS)

```python
from src.utils.secrets_manager import get_secret

# Secrets are read from AWS Secrets Manager in production
db_url = get_secret('database-url')  # Reads from gaara-store/production/database-url
jwt_secret = get_secret('jwt-secret')  # Reads from gaara-store/production/jwt-secret
```

## Configuration

### Environment Variables

```bash
# Required
ENVIRONMENT=development  # or staging, production

# AWS Configuration (production only)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...  # For local dev only; use IAM roles in production
AWS_SECRET_ACCESS_KEY=...  # For local dev only

# Optional
SECRET_CACHE_TTL=300  # Cache TTL in seconds (default: 5 minutes)
```

### Secret Naming Convention

**AWS Secrets Manager**:
- Format: `gaara-store/{environment}/{secret-name}`
- Examples:
  - `gaara-store/production/database-url`
  - `gaara-store/production/jwt-secret`
  - `gaara-store/staging/redis-url`

**Environment Variables** (.env):
- Format: `{SECRET_NAME}` (uppercase, underscores)
- Examples:
  - `DATABASE_URL`
  - `JWT_SECRET`
  - `REDIS_URL`

## API Reference

### `get_secret(secret_name, default=None, force_refresh=False)`

Retrieve a secret with caching and fallback.

**Parameters**:
- `secret_name` (str): Name of the secret (without environment prefix)
- `default` (str, optional): Default value if secret not found
- `force_refresh` (bool): Bypass cache and fetch fresh value

**Returns**: Secret value as string

**Raises**:
- `SecretNotFoundError`: If secret not found and no default provided
- `SecretsManagerError`: If AWS API call fails

**Examples**:

```python
# Basic usage
db_url = get_secret('database-url')

# With default value
smtp_pass = get_secret('smtp-password', default='')

# Force refresh (bypass cache)
jwt_secret = get_secret('jwt-secret', force_refresh=True)

# Error handling
try:
    api_key = get_secret('api-key')
except SecretNotFoundError:
    print("Secret not found")
except SecretsManagerError as e:
    print(f"AWS error: {e}")
```

### `clear_cache(secret_name=None)`

Clear secret cache.

**Parameters**:
- `secret_name` (str, optional): Specific secret to clear, or None to clear all

**Examples**:

```python
from src.utils.secrets_manager import clear_cache

# Clear specific secret
clear_cache('database-url')

# Clear all secrets
clear_cache()
```

### `get_cache_stats()`

Get cache statistics for monitoring.

**Returns**: Dictionary with cache stats

**Example**:

```python
from src.utils.secrets_manager import get_cache_stats

stats = get_cache_stats()
print(f"Cached secrets: {stats['cached_secrets']}")
print(f"Secrets: {stats['secrets']}")
print(f"Cache TTL: {stats['cache_ttl']}")
print(f"Environment: {stats['environment']}")
print(f"boto3 available: {stats['boto3_available']}")
```

## AWS Setup

### 1. Install boto3

```bash
pip install boto3
```

### 2. Create KMS Key

```bash
aws kms create-key \
  --description "Gaara Store encryption key" \
  --key-usage ENCRYPT_DECRYPT \
  --origin AWS_KMS

# Note the KeyId from the response
```

### 3. Create Secrets

```bash
# Database URL
aws secretsmanager create-secret \
  --name gaara-store/production/database-url \
  --secret-string "postgresql://user:pass@host:5432/dbname" \
  --kms-key-id <key-id>

# JWT Secret
aws secretsmanager create-secret \
  --name gaara-store/production/jwt-secret \
  --secret-string "your-jwt-secret-key" \
  --kms-key-id <key-id>

# Redis URL
aws secretsmanager create-secret \
  --name gaara-store/production/redis-url \
  --secret-string "redis://localhost:6379/0" \
  --kms-key-id <key-id>
```

### 4. Create IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:*:secret:gaara-store/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:us-east-1:*:key/<key-id>"
    }
  ]
}
```

### 5. Attach Policy to IAM User/Role

```bash
aws iam attach-user-policy \
  --user-name gaara-store-app \
  --policy-arn arn:aws:iam::aws:policy/custom/GaaraStoreSecretsAccess
```

## Migration Guide

### Step 1: Identify Secrets

Current secrets in `.env`:
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `REDIS_URL` (if enabled)
- `MAIL_PASSWORD` (if enabled)
- `SENTRY_DSN` (if enabled)

### Step 2: Create Secrets in AWS

```bash
# For each secret
aws secretsmanager create-secret \
  --name gaara-store/production/{secret-name} \
  --secret-string "{secret-value}" \
  --kms-key-id <key-id>
```

### Step 3: Update Application Code

**Before**:
```python
import os
db_url = os.getenv('DATABASE_URL')
```

**After**:
```python
from src.utils.secrets_manager import get_secret
db_url = get_secret('database-url')
```

### Step 4: Test in Staging

```bash
# Set environment
export ENVIRONMENT=staging
export AWS_REGION=us-east-1

# Run tests
python -m pytest backend/tests/test_secrets_manager.py -v
```

### Step 5: Deploy to Production

```bash
# Set environment
export ENVIRONMENT=production
export AWS_REGION=us-east-1

# Deploy (use IAM role, not access keys)
# Application will automatically use AWS Secrets Manager
```

## Caching Behavior

### Cache TTL

- Default: 5 minutes (300 seconds)
- Configurable via `SECRET_CACHE_TTL` environment variable
- Reduces AWS API calls and improves performance

### Cache Invalidation

```python
# Manual invalidation
clear_cache('database-url')

# Force refresh on next access
db_url = get_secret('database-url', force_refresh=True)
```

### Cache Statistics

```python
stats = get_cache_stats()
# {
#   'cached_secrets': 3,
#   'secrets': ['database-url', 'jwt-secret', 'redis-url'],
#   'cache_ttl': 300,
#   'environment': 'production',
#   'boto3_available': True
# }
```

## Security Best Practices

### 1. Never Log Secrets

```python
# ❌ BAD
logger.info(f"Database URL: {db_url}")

# ✅ GOOD
logger.info("Database connection established")
```

Secrets are automatically redacted in logs by the secrets manager.

### 2. Use IAM Roles in Production

```bash
# ❌ BAD - Using access keys in production
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...

# ✅ GOOD - Using IAM role
# No credentials needed; role attached to EC2/ECS/Lambda
```

### 3. Rotate Secrets Regularly

```bash
# Enable automatic rotation (for RDS)
aws secretsmanager rotate-secret \
  --secret-id gaara-store/production/database-url \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:*:function:SecretsManagerRotation \
  --rotation-rules AutomaticallyAfterDays=30
```

### 4. Use Least Privilege

Only grant `GetSecretValue` and `DescribeSecret` permissions, not `PutSecretValue` or `DeleteSecret`.

## Troubleshooting

### Secret Not Found

```python
SecretNotFoundError: Secret 'database-url' not found in AWS or .env
```

**Solutions**:
1. Check secret exists in AWS: `aws secretsmanager describe-secret --secret-id gaara-store/production/database-url`
2. Check environment variable: `echo $DATABASE_URL`
3. Verify `ENVIRONMENT` is set correctly

### AWS Credentials Error

```python
SecretsManagerError: Failed to create Secrets Manager client
```

**Solutions**:
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify IAM permissions
3. Check `AWS_REGION` is set

### boto3 Not Installed

```python
SecretsManagerError: boto3 is not installed
```

**Solution**:
```bash
pip install boto3
```

## Testing

### Unit Tests

```bash
# Run all secrets manager tests
python -m pytest backend/tests/test_secrets_manager.py -v

# Run specific test
python -m pytest backend/tests/test_secrets_manager.py::TestCaching::test_secret_cached_on_first_access -v
```

### Integration Tests (AWS)

```bash
# Enable AWS integration tests
export SKIP_AWS_TESTS=false
export ENVIRONMENT=production
export AWS_REGION=us-east-1

# Run tests
python -m pytest backend/tests/test_secrets_manager.py::TestAWSIntegration -v
```

## Monitoring

### CloudWatch Metrics

Monitor secret access in CloudWatch:
- `SecretAccess` - Number of secret retrievals
- `CacheHitRate` - Percentage of cache hits
- `FailedAccess` - Number of failed retrievals

### Alerts

Set up alerts for:
- Failed secret access > 5% of requests
- Cache hit rate < 80%
- Unusual access patterns

## Support

For issues or questions:
- Documentation: `/docs/Security.md`, `/docs/Env.md`
- Tests: `backend/tests/test_secrets_manager.py`
- Code: `backend/src/utils/secrets_manager.py`

