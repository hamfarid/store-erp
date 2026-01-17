# KMS/Vault Integration Design

**Date**: 2025-10-27  
**Status**: Design Phase  
**Purpose**: Secure secrets management for production deployment

---

## 1. OVERVIEW

This document outlines the integration of AWS KMS (Key Management Service) or HashiCorp Vault for secure secrets management in the Gaara Store application.

### Goals
- ✅ Eliminate secrets from .env files in production
- ✅ Centralized secrets management
- ✅ Automatic key rotation
- ✅ Audit logging for all secret access
- ✅ Fine-grained IAM permissions

---

## 2. ARCHITECTURE OPTIONS

### Option A: AWS KMS + Secrets Manager (Recommended)
**Pros**:
- Native AWS integration
- Automatic rotation
- Audit logging via CloudTrail
- Cost-effective
- No additional infrastructure

**Cons**:
- AWS-specific
- Requires IAM setup

**Cost**: ~$1/month for Secrets Manager + KMS usage

### Option B: HashiCorp Vault
**Pros**:
- Cloud-agnostic
- Self-hosted option
- Advanced policy engine
- Multi-cloud support

**Cons**:
- Additional infrastructure
- More complex setup
- Higher operational overhead

**Cost**: $0 (self-hosted) or $500+/month (managed)

### Recommendation
**AWS KMS + Secrets Manager** for production (simpler, cost-effective)

---

## 3. AWS KMS INTEGRATION DESIGN

### 3.1 Architecture

```
Application
    ↓
SecretsAdapter (Python)
    ↓
AWS Secrets Manager
    ↓
AWS KMS (Encryption)
    ↓
CloudTrail (Audit)
```

### 3.2 Secrets to Migrate

```
DATABASE_URL
JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY
ENCRYPTION_KEY
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
SENDGRID_API_KEY
STRIPE_API_KEY
OAUTH_CLIENT_SECRET
```

### 3.3 Implementation Steps

#### Step 1: Create KMS Key
```bash
aws kms create-key \
  --description "Gaara Store Encryption Key" \
  --region us-east-1
```

#### Step 2: Create Secrets in Secrets Manager
```bash
aws secretsmanager create-secret \
  --name gaara/prod/database-url \
  --secret-string "postgresql://..." \
  --kms-key-id arn:aws:kms:...
```

#### Step 3: Set IAM Permissions
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
      "Resource": "arn:aws:secretsmanager:*:*:secret:gaara/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey"
      ],
      "Resource": "arn:aws:kms:*:*:key/*"
    }
  ]
}
```

---

## 4. PYTHON ADAPTER IMPLEMENTATION

### 4.1 SecretsAdapter Class

```python
# backend/src/services/secrets_adapter.py

import boto3
import json
from typing import Dict, Any, Optional
from functools import lru_cache

class SecretsAdapter:
    """Adapter for AWS Secrets Manager"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)
        self.cache: Dict[str, Any] = {}
    
    @lru_cache(maxsize=128)
    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """Retrieve secret from AWS Secrets Manager"""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            
            if 'SecretString' in response:
                return json.loads(response['SecretString'])
            else:
                return {'value': response['SecretBinary']}
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve secret {secret_name}: {str(e)}")
    
    def get_secret_value(self, secret_name: str, key: Optional[str] = None) -> str:
        """Get a specific secret value"""
        secret = self.get_secret(secret_name)
        
        if key:
            return secret.get(key, '')
        return secret.get('value', '')
    
    def rotate_secret(self, secret_name: str) -> bool:
        """Trigger secret rotation"""
        try:
            self.client.rotate_secret(SecretId=secret_name)
            self.cache.pop(secret_name, None)  # Clear cache
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to rotate secret {secret_name}: {str(e)}")
```

### 4.2 Integration with Flask

```python
# backend/app.py

from src.services.secrets_adapter import SecretsAdapter

def create_app():
    app = Flask(__name__)
    
    # Initialize secrets adapter
    secrets = SecretsAdapter(region='us-east-1')
    
    # Load secrets from AWS Secrets Manager
    if os.getenv('ENVIRONMENT') == 'production':
        db_secret = secrets.get_secret('gaara/prod/database')
        app.config['SQLALCHEMY_DATABASE_URI'] = db_secret['url']
        app.config['JWT_SECRET_KEY'] = secrets.get_secret_value('gaara/prod/jwt-secret')
    else:
        # Use .env for development
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    return app
```

---

## 5. DEPLOYMENT CONFIGURATION

### 5.1 Environment Variables

```bash
# .env.production
ENVIRONMENT=production
AWS_REGION=us-east-1
SECRETS_MANAGER_PREFIX=gaara/prod
```

### 5.2 Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install AWS CLI
RUN pip install boto3

# Copy application
COPY . /app
WORKDIR /app

# Set environment
ENV ENVIRONMENT=production
ENV AWS_REGION=us-east-1

# Run application
CMD ["python", "-m", "flask", "run"]
```

### 5.3 Kubernetes Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gaara-aws-credentials
type: Opaque
data:
  AWS_ACCESS_KEY_ID: <base64-encoded>
  AWS_SECRET_ACCESS_KEY: <base64-encoded>
```

---

## 6. MONITORING & AUDIT

### 6.1 CloudTrail Logging

```bash
aws cloudtrail create-trail \
  --name gaara-secrets-trail \
  --s3-bucket-name gaara-audit-logs
```

### 6.2 Metrics to Monitor

- Secret access frequency
- Failed access attempts
- Key rotation events
- Unauthorized access attempts

### 6.3 Alerts

```python
# CloudWatch Alarms
- Alert on >10 failed secret retrievals in 5 minutes
- Alert on unauthorized KMS key usage
- Alert on secret rotation failures
```

---

## 7. MIGRATION PLAN

### Phase 1: Setup (1 hour)
- Create KMS key
- Create Secrets Manager secrets
- Set IAM permissions

### Phase 2: Development (2 hours)
- Implement SecretsAdapter
- Test with local AWS credentials
- Update Flask app

### Phase 3: Staging (1 hour)
- Deploy to staging environment
- Verify secret retrieval
- Test rotation

### Phase 4: Production (1 hour)
- Deploy to production
- Monitor for errors
- Verify audit logs

---

## 8. ROLLBACK PLAN

If issues occur:
1. Revert to .env-based secrets
2. Disable KMS integration
3. Investigate CloudTrail logs
4. Fix and redeploy

---

## 9. COST ESTIMATION

```
AWS Secrets Manager: $0.40/secret/month
AWS KMS: $1.00/month (first 20,000 requests free)
CloudTrail: $2.00/month

Total: ~$5-10/month
```

---

## 10. NEXT STEPS

1. ✅ Design document (this file)
2. ⏳ Implement SecretsAdapter
3. ⏳ Create AWS resources
4. ⏳ Test integration
5. ⏳ Deploy to production

---

**Status**: Design Phase Complete  
**Next**: Implementation Phase

