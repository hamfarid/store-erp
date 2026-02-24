# Secrets Setup Guide

**Date**: 2025-10-27  
**Purpose**: Step-by-step guide for setting up AWS Secrets Manager

---

## QUICK START

### Development (Using .env)
```bash
# No setup needed - use .env file
cp templates/.env.example .env
# Edit .env with your secrets
```

### Production (Using AWS Secrets Manager)
```bash
# 1. Install AWS CLI
pip install boto3

# 2. Configure AWS credentials
aws configure

# 3. Create KMS key
aws kms create-key --description "Gaara Store Encryption Key"

# 4. Create secrets
./scripts/setup_secrets.sh
```

---

## DETAILED SETUP

### Step 1: Create KMS Key

```bash
# Create KMS key
KMS_KEY=$(aws kms create-key \
  --description "Gaara Store Encryption Key" \
  --region us-east-1 \
  --query 'KeyMetadata.KeyId' \
  --output text)

echo "KMS Key ID: $KMS_KEY"

# Create alias for easy reference
aws kms create-alias \
  --alias-name alias/gaara-store \
  --target-key-id $KMS_KEY
```

### Step 2: Create Secrets

```bash
# Database URL
aws secretsmanager create-secret \
  --name gaara/database-url \
  --secret-string "postgresql://user:pass@localhost/gaara" \
  --kms-key-id alias/gaara-store

# JWT Secrets
aws secretsmanager create-secret \
  --name gaara/jwt-secret \
  --secret-string "your-jwt-secret-key-here" \
  --kms-key-id alias/gaara-store

aws secretsmanager create-secret \
  --name gaara/jwt-refresh-secret \
  --secret-string "your-jwt-refresh-secret-here" \
  --kms-key-id alias/gaara-store

# Encryption Key
aws secretsmanager create-secret \
  --name gaara/encryption-key \
  --secret-string "your-encryption-key-here" \
  --kms-key-id alias/gaara-store

# API Keys
aws secretsmanager create-secret \
  --name gaara/sendgrid-api-key \
  --secret-string "your-sendgrid-key" \
  --kms-key-id alias/gaara-store

aws secretsmanager create-secret \
  --name gaara/stripe-api-key \
  --secret-string "your-stripe-key" \
  --kms-key-id alias/gaara-store
```

### Step 3: Set IAM Permissions

Create IAM policy for application:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadSecrets",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:*:*:secret:gaara/*"
    },
    {
      "Sid": "DecryptSecrets",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:*:*:key/*",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": "secretsmanager.us-east-1.amazonaws.com"
        }
      }
    }
  ]
}
```

### Step 4: Configure Application

```bash
# Set environment variables
export ENVIRONMENT=production
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
```

### Step 5: Test Integration

```bash
# Test secret retrieval
python -c "
from src.services.secrets_adapter import get_secrets_adapter
adapter = get_secrets_adapter()
secret = adapter.get_secret('gaara/database-url')
print('✅ Successfully retrieved secret')
"
```

---

## ENVIRONMENT VARIABLES

### Development (.env)
```
ENVIRONMENT=development
GAARA_DATABASE_URL=postgresql://...
GAARA_JWT_SECRET=your-secret
GAARA_JWT_REFRESH_SECRET=your-refresh-secret
GAARA_ENCRYPTION_KEY=your-encryption-key
GAARA_SENDGRID_API_KEY=your-sendgrid-key
GAARA_STRIPE_API_KEY=your-stripe-key
```

### Production (.env.production)
```
ENVIRONMENT=production
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

---

## DOCKER DEPLOYMENT

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN pip install boto3 flask sqlalchemy

# Copy application
COPY . /app
WORKDIR /app

# Set environment
ENV ENVIRONMENT=production
ENV AWS_REGION=us-east-1

# Run application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      ENVIRONMENT: production
      AWS_REGION: us-east-1
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
    ports:
      - "5000:5000"
```

---

## KUBERNETES DEPLOYMENT

### Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gaara-aws-credentials
  namespace: default
type: Opaque
data:
  AWS_ACCESS_KEY_ID: <base64-encoded>
  AWS_SECRET_ACCESS_KEY: <base64-encoded>
```

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gaara-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: gaara-store:latest
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: AWS_REGION
          value: "us-east-1"
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: gaara-aws-credentials
              key: AWS_ACCESS_KEY_ID
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: gaara-aws-credentials
              key: AWS_SECRET_ACCESS_KEY
```

---

## MONITORING & AUDIT

### CloudTrail Logging
```bash
aws cloudtrail create-trail \
  --name gaara-secrets-trail \
  --s3-bucket-name gaara-audit-logs \
  --is-multi-region-trail
```

### View Audit Logs
```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=gaara/database-url \
  --max-results 10
```

---

## TROUBLESHOOTING

### Secret Not Found
```bash
# List all secrets
aws secretsmanager list-secrets --filters Key=name,Values=gaara

# Describe specific secret
aws secretsmanager describe-secret --secret-id gaara/database-url
```

### Permission Denied
```bash
# Check IAM permissions
aws iam get-user-policy --user-name your-user --policy-name your-policy

# Check KMS key permissions
aws kms describe-key --key-id alias/gaara-store
```

### Connection Issues
```bash
# Test AWS connectivity
aws sts get-caller-identity

# Test Secrets Manager access
aws secretsmanager get-secret-value --secret-id gaara/database-url
```

---

## BEST PRACTICES

1. ✅ Never commit secrets to git
2. ✅ Use separate KMS keys per environment
3. ✅ Enable CloudTrail logging
4. ✅ Rotate secrets regularly
5. ✅ Use IAM roles instead of access keys
6. ✅ Monitor secret access
7. ✅ Use VPC endpoints for Secrets Manager
8. ✅ Enable MFA for secret deletion

---

**Status**: Setup Guide Complete  
**Next**: Deploy to production

