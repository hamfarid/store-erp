# AWS Setup Guide - Gaara Store System

**Purpose**: Step-by-step guide for setting up AWS KMS and Secrets Manager  
**Owner**: DevOps Team  
**Last Updated**: 2025-10-25  
**Status**: Production Ready

---

## 📋 Prerequisites

- [ ] AWS Account (or approval to create one)
- [ ] AWS CLI installed (`aws --version`)
- [ ] IAM permissions to create KMS keys and secrets
- [ ] Budget approval (~$10-15/month)
- [ ] Python 3.11+ with boto3 installed

---

## 🎯 Overview

This guide will help you:
1. Create AWS account and IAM user
2. Create KMS key for envelope encryption
3. Create secrets in Secrets Manager
4. Configure application to use AWS secrets
5. Test the integration
6. Enable automatic rotation

**Estimated Time**: 30-45 minutes

---

## 📝 Step 1: AWS Account Setup

### 1.1 Create AWS Account (if needed)

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the registration process
4. Add payment method (free tier available)
5. Verify email and phone

### 1.2 Create IAM User for Application

```bash
# Login to AWS Console
# Navigate to: IAM > Users > Add User

# User details:
Name: gaara-store-app
Access type: Programmatic access (API keys)

# Permissions:
Attach policies:
- SecretsManagerReadWrite
- AWSKeyManagementServicePowerUser

# Save credentials:
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

**⚠️ IMPORTANT**: Save these credentials securely. You'll need them later.

---

## 🔐 Step 2: Create KMS Key

### 2.1 Create KMS Key via Console

```bash
# Navigate to: KMS > Customer managed keys > Create key

# Step 1: Configure key
Key type: Symmetric
Key usage: Encrypt and decrypt
Advanced options: KMS (default)

# Step 2: Add labels
Alias: gaara-store-production
Description: Master key for Gaara Store envelope encryption

# Step 3: Define key administrative permissions
Key administrators: Your IAM user

# Step 4: Define key usage permissions
Key users: gaara-store-app (IAM user created above)

# Step 5: Review and create
```

### 2.2 Create KMS Key via CLI

```bash
# Create key
aws kms create-key \
  --description "Gaara Store Production Master Key" \
  --key-usage ENCRYPT_DECRYPT \
  --origin AWS_KMS

# Output: Save the KeyId (e.g., arn:aws:kms:us-east-1:123456789012:key/abc-123)

# Create alias
aws kms create-alias \
  --alias-name alias/gaara-store-production \
  --target-key-id <KeyId from above>

# Verify
aws kms describe-key --key-id alias/gaara-store-production
```

### 2.3 Save KMS Key ID

```bash
# Add to .env (for reference only, not committed)
KMS_KEY_ID=alias/gaara-store-production
# or
KMS_KEY_ID=arn:aws:kms:us-east-1:123456789012:key/abc-123
```

---

## 🔑 Step 3: Create Secrets in Secrets Manager

### 3.1 Secret Naming Convention

Format: `gaara-store/{environment}/{secret-name}`

Examples:
- `gaara-store/production/secret-key`
- `gaara-store/production/jwt-secret`
- `gaara-store/production/database-url`

### 3.2 Create Secrets via Console

```bash
# Navigate to: Secrets Manager > Store a new secret

# For each secret:

1. Secret type: Other type of secret
2. Key/value pairs:
   - Key: (leave default or use "value")
   - Value: <paste secret value>
3. Encryption key: gaara-store-production (KMS key created above)
4. Secret name: gaara-store/production/secret-key
5. Description: Flask secret key for session management
6. Rotation: Disable (for now)
7. Review and store
```

### 3.3 Create Secrets via CLI

```bash
# 1. SECRET_KEY
aws secretsmanager create-secret \
  --name gaara-store/production/secret-key \
  --description "Flask secret key" \
  --kms-key-id alias/gaara-store-production \
  --secret-string "e15085f24c5d7dd1f60b95d26310022350105c26dd3af48a1130c347e32cfa3a"

# 2. JWT_SECRET_KEY
aws secretsmanager create-secret \
  --name gaara-store/production/jwt-secret \
  --description "JWT secret key" \
  --kms-key-id alias/gaara-store-production \
  --secret-string "849c4a304f1d276f5a09549baa2b92e76ed575d4388afd30f60c6ae3eea1f9a5"

# 3. ENCRYPTION_KEY
aws secretsmanager create-secret \
  --name gaara-store/production/encryption-key \
  --description "Fallback encryption key" \
  --kms-key-id alias/gaara-store-production \
  --secret-string "ce8525174c4af33fcac6a79b5a9a1378c961f8ff1498a2f8a988a03428630207"

# 4. DATABASE_URL
aws secretsmanager create-secret \
  --name gaara-store/production/database-url \
  --description "Database connection string" \
  --kms-key-id alias/gaara-store-production \
  --secret-string "postgresql://user:pass@host:5432/gaara_store"

# 5. REDIS_PASSWORD
aws secretsmanager create-secret \
  --name gaara-store/production/redis-password \
  --description "Redis password" \
  --kms-key-id alias/gaara-store-production \
  --secret-string "bwvFrj93A"

# 6. MAIL_PASSWORD
aws secretsmanager create-secret \
  --name gaara-store/production/mail-password \
  --description "SMTP password" \
  --kms-key-id alias/gaara-store-production \
  --secret-string "HaRrMa123!@#"

# 7. SENTRY_DSN (if using Sentry)
aws secretsmanager create-secret \
  --name gaara-store/production/sentry-dsn \
  --description "Sentry DSN for error tracking" \
  --kms-key-id alias/gaara-store-production \
  --secret-string "https://..."
```

### 3.4 Verify Secrets

```bash
# List all secrets
aws secretsmanager list-secrets --filters Key=name,Values=gaara-store/

# Get a specific secret (test)
aws secretsmanager get-secret-value \
  --secret-id gaara-store/production/secret-key \
  --query SecretString \
  --output text
```

---

## ⚙️ Step 4: Configure Application

### 4.1 Install boto3

```bash
pip install boto3
```

### 4.2 Update .env for Production

```bash
# Environment
ENVIRONMENT=production

# AWS Configuration
AWS_REGION=us-east-1
KMS_KEY_ID=alias/gaara-store-production

# AWS Credentials (use IAM role in production, not env vars)
# AWS_ACCESS_KEY_ID=AKIA...
# AWS_SECRET_ACCESS_KEY=...

# Secret Cache TTL
SECRET_CACHE_TTL=300
```

### 4.3 Update Application Code

See `backend/src/utils/README_SECRETS.md` for detailed migration guide.

**Example**:

```python
# Before (reading from .env)
import os
db_url = os.getenv('DATABASE_URL')

# After (reading from Secrets Manager)
from src.utils.secrets_manager import get_secret
db_url = get_secret('database-url')
```

---

## 🧪 Step 5: Test Integration

### 5.1 Test Secrets Manager

```bash
# Run secrets manager tests
python -m pytest backend/tests/test_secrets_manager.py -v

# Run with AWS integration tests (requires AWS credentials)
SKIP_AWS_TESTS=false python -m pytest backend/tests/test_secrets_manager.py -v
```

### 5.2 Test Encryption

```bash
# Run encryption tests
python -m pytest backend/tests/test_encryption.py -v
```

### 5.3 Manual Test

```python
# Test script: test_aws_secrets.py
from src.utils.secrets_manager import get_secret

# Test reading a secret
secret_key = get_secret('secret-key')
print(f"✅ Successfully retrieved secret (length: {len(secret_key)})")

# Test caching
secret_key_2 = get_secret('secret-key')
assert secret_key == secret_key_2
print("✅ Cache working correctly")
```

---

## 🔄 Step 6: Enable Automatic Rotation (Optional)

### 6.1 Enable Rotation for RDS Credentials

```bash
# For RDS database credentials
aws secretsmanager rotate-secret \
  --secret-id gaara-store/production/database-url \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:SecretsManagerRDSRotation \
  --rotation-rules AutomaticallyAfterDays=30
```

### 6.2 Create Custom Rotation Lambda (Advanced)

See AWS documentation: https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html

---

## 💰 Cost Estimation

### Monthly Costs (Approximate)

| Service | Usage | Cost |
|---------|-------|------|
| **KMS** | 1 key + 10,000 API calls | $1.00 + $0.03 = $1.03 |
| **Secrets Manager** | 7 secrets | 7 × $0.40 = $2.80 |
| **Secrets Manager API** | ~100,000 calls | $0.05 |
| **Data Transfer** | Minimal | $0.00 |
| **Total** | | **~$3.88/month** |

**Note**: Actual costs may vary. Enable billing alerts.

---

## 🔒 Security Best Practices

1. **Never commit AWS credentials** to git
2. **Use IAM roles** in production (not access keys)
3. **Enable CloudTrail** for audit logging
4. **Set up billing alerts** ($5, $10, $20 thresholds)
5. **Rotate secrets** every 90 days
6. **Use least-privilege IAM policies**
7. **Enable MFA** for AWS console access
8. **Monitor CloudWatch** for anomalous access

---

## 🚨 Troubleshooting

### Issue: "AccessDeniedException"

**Solution**: Check IAM permissions for KMS and Secrets Manager

```bash
# Verify IAM user permissions
aws iam list-attached-user-policies --user-name gaara-store-app
```

### Issue: "Secret not found"

**Solution**: Verify secret name and region

```bash
# List secrets in current region
aws secretsmanager list-secrets

# Check AWS_REGION in .env
echo $AWS_REGION
```

### Issue: "KMS key not found"

**Solution**: Verify KMS key ID and alias

```bash
# List KMS keys
aws kms list-keys

# Describe key
aws kms describe-key --key-id alias/gaara-store-production
```

---

## ✅ Checklist

- [ ] AWS account created
- [ ] IAM user created with correct permissions
- [ ] KMS key created (`alias/gaara-store-production`)
- [ ] 7 secrets created in Secrets Manager
- [ ] boto3 installed
- [ ] .env updated with AWS configuration
- [ ] Application code updated to use `get_secret()`
- [ ] Tests passing (93/93)
- [ ] Manual test successful
- [ ] CloudWatch monitoring configured
- [ ] Billing alerts enabled

---

## 📚 References

- [AWS KMS Documentation](https://docs.aws.amazon.com/kms/)
- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Gaara Store Secrets Manager Guide](../backend/src/utils/README_SECRETS.md)

---

**Next Steps**: After completing this guide, proceed to `docs/P1_KMS_Vault_Plan.md` Phase 3.

