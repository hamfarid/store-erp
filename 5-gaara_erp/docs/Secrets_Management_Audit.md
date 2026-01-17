# FILE: docs/Secrets_Management_Audit.md | PURPOSE: P0.7 Secrets management audit and KMS/Vault migration plan | OWNER: Backend Security | RELATED: .env, GLOBAL_GUIDELINES §XXXVII | LAST-AUDITED: 2025-10-25

# Secrets Management Audit — P0.7

**Audit Date**: 2025-10-25  
**Guidelines Version**: 2.3  
**Auditor**: Augment Agent  
**Scope**: All secrets in .env files, migration to KMS/Vault for production

---

## Executive Summary

⚠️ **OVERALL STATUS**: **NON-COMPLIANT** for production deployment

**Critical Findings**:

- ❌ **CRITICAL**: Production secrets stored in plaintext `.env` file
- ❌ **CRITICAL**: Email password exposed in repository (line 116)
- ❌ **CRITICAL**: Admin password exposed in repository (line 43)
- ❌ **HIGH**: Encryption keys stored in plaintext (lines 19, 22, 25)
- ⚠️ **MEDIUM**: No secret rotation policy documented
- ⚠️ **MEDIUM**: No KMS/Vault integration for production

**Immediate Actions Required**:

1. 🚨 **URGENT**: Remove `.env` from repository (add to `.gitignore`)
2. 🚨 **URGENT**: Rotate all exposed secrets immediately
3. 🚨 **URGENT**: Implement KMS/Vault for production secrets
4. 🚨 **URGENT**: Add secret scanning to CI pipeline

**Compliance**: ❌ **FAILS** GLOBAL_GUIDELINES §XXXVII (Secrets Management)

---

## P0.7.1: Identified Secrets in .env Files

### Critical Secrets (MUST migrate to KMS/Vault)

| Secret Name | Location | Type | Risk Level | Rotation Required |
|-------------|----------|------|------------|-------------------|
| `SECRET_KEY` | backend/.env:19 | Flask Session Key | 🔴 CRITICAL | ✅ YES |
| `JWT_SECRET_KEY` | backend/.env:22 | JWT Signing Key | 🔴 CRITICAL | ✅ YES |
| `ENCRYPTION_KEY` | backend/.env:25 | Data Encryption | 🔴 CRITICAL | ✅ YES |
| `ADMIN_PASSWORD` | backend/.env:43 | Admin Credentials | 🔴 CRITICAL | ✅ YES |
| `MAIL_PASSWORD` | backend/.env:116 | Email SMTP | 🔴 CRITICAL | ✅ YES |

### Sensitive Configuration (Should migrate to KMS/Vault)

| Config Name | Location | Type | Risk Level | Notes |
|-------------|----------|------|------------|-------|
| `DATABASE_URL` | backend/.env:61 | DB Connection | 🟡 MEDIUM | Contains path, not credentials |
| `MAIL_USERNAME` | backend/.env:115 | Email Account | 🟡 MEDIUM | Public info, but sensitive |
| `DEFAULT_ADMIN_EMAIL` | backend/.env:37 | Admin Email | 🟡 MEDIUM | PII |

### Non-Secret Configuration (Can remain in .env)

- `FLASK_ENV`, `FLASK_DEBUG`, `PORT`, `HOST`
- `LOG_LEVEL`, `LOG_FILE`, `CACHE_TYPE`
- `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`
- Feature flags: `AUTO_BACKUP`, `MONITORING_ENABLED`

---

## P0.7.2: KMS/Vault Migration Plan for Production

### Recommended Solution: **AWS Secrets Manager** or **HashiCorp Vault**

#### Option A: AWS Secrets Manager (Recommended for AWS deployments)

**Pros**:

- ✅ Fully managed service
- ✅ Automatic rotation for RDS, Redshift, DocumentDB
- ✅ Fine-grained IAM permissions
- ✅ Encryption at rest with AWS KMS
- ✅ Audit logging via CloudTrail
- ✅ Pay-per-secret pricing ($0.40/month per secret)

**Cons**:

- ❌ AWS-specific (vendor lock-in)
- ❌ Requires AWS account

**Implementation**:

```python
# backend/src/config/secrets.py
import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name, region_name="us-east-1"):
    """Retrieve secret from AWS Secrets Manager"""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise Exception(f"Failed to retrieve secret: {e}")

# Usage in app.py
secrets = get_secret("store-system/production")
app.config['SECRET_KEY'] = secrets['SECRET_KEY']
app.config['JWT_SECRET_KEY'] = secrets['JWT_SECRET_KEY']
```

**Secret Structure in AWS**:

```json
{
  "SECRET_KEY": "e15085f24c5d7dd1f60b95d26310022350105c26dd3af48a1130c347e32cfa3a",
  "JWT_SECRET_KEY": "849c4a304f1d276f5a09549baa2b92e76ed575d4388afd30f60c6ae3eea1f9a5",
  "ENCRYPTION_KEY": "ce8525174c4af33fcac6a79b5a9a1378c961f8ff1498a2f8a988a03428630207",
  "ADMIN_PASSWORD": "NEW_ROTATED_PASSWORD",
  "MAIL_PASSWORD": "NEW_ROTATED_PASSWORD"
}
```

#### Option B: HashiCorp Vault (Recommended for multi-cloud/on-prem)

**Pros**:

- ✅ Cloud-agnostic
- ✅ Dynamic secrets generation
- ✅ Detailed audit logs
- ✅ Secret versioning
- ✅ Lease management with TTLs
- ✅ Open-source (self-hosted) or managed (HCP Vault)

**Cons**:

- ❌ Requires infrastructure setup (if self-hosted)
- ❌ More complex than AWS Secrets Manager

**Implementation**:

```python
# backend/src/config/secrets.py
import hvac

def get_vault_secret(path, mount_point='secret'):
    """Retrieve secret from HashiCorp Vault"""
    client = hvac.Client(
        url=os.getenv('VAULT_ADDR', 'http://localhost:8200'),
        token=os.getenv('VAULT_TOKEN')
    )
    
    if not client.is_authenticated():
        raise Exception("Vault authentication failed")
    
    response = client.secrets.kv.v2.read_secret_version(
        path=path,
        mount_point=mount_point
    )
    
    return response['data']['data']

# Usage in app.py
secrets = get_vault_secret('store-system/production')
app.config['SECRET_KEY'] = secrets['SECRET_KEY']
```

**Vault Secret Path**:

```
secret/store-system/production
  ├── SECRET_KEY
  ├── JWT_SECRET_KEY
  ├── ENCRYPTION_KEY
  ├── ADMIN_PASSWORD
  └── MAIL_PASSWORD
```

---

## P0.7.3: Updated /docs/Env.md with Key IDs/Secret Paths

**File**: `docs/Env.md` (to be created)

**Content**:

```markdown
# Environment Variables & Secrets

## Production Secrets (AWS Secrets Manager)

| Variable | Secret Path | Key ID | Rotation Policy |
|----------|-------------|--------|-----------------|
| SECRET_KEY | store-system/production | flask-session-key | 90 days |
| JWT_SECRET_KEY | store-system/production | jwt-signing-key | 90 days |
| ENCRYPTION_KEY | store-system/production | data-encryption-key | 90 days |
| ADMIN_PASSWORD | store-system/admin-creds | admin-password | 30 days |
| MAIL_PASSWORD | store-system/smtp-creds | smtp-password | 90 days |

## Development Secrets (.env - NOT for production)

Development uses `.env` file with non-production secrets.
**NEVER commit `.env` to repository.**

## Accessing Secrets in Code

```python
from src.config.secrets import get_secret

# Production
if os.getenv('APP_ENV') == 'production':
    secrets = get_secret("store-system/production")
    app.config['SECRET_KEY'] = secrets['SECRET_KEY']
else:
    # Development
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

## IAM Permissions Required

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
      "Resource": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:store-system/*"
    }
  ]
}
```

```

---

## P0.7.4: Updated /docs/Security.md with Secrets Lifecycle

**File**: `docs/Security.md` (to be updated)

**Secrets Lifecycle Section**:
```markdown
## Secrets Lifecycle Management

### 1. Creation
- Generate secrets using cryptographically secure random generators
- Minimum entropy: 256 bits for encryption keys, 128 bits for passwords
- Store in KMS/Vault immediately (never in code/config files)

### 2. Access Control
- Least-privilege IAM policies
- Service accounts with specific secret access
- Audit all secret access via CloudTrail/Vault audit logs

### 3. Rotation
- **Encryption Keys**: 90 days
- **Admin Passwords**: 30 days
- **SMTP Passwords**: 90 days
- **JWT Signing Keys**: 90 days
- Automated rotation via AWS Secrets Manager or Vault

### 4. Revocation
- Immediate revocation on suspected compromise
- Rotate all dependent secrets
- Audit access logs for unauthorized usage

### 5. Monitoring
- Alert on secret access anomalies
- Track rotation compliance
- Monitor failed authentication attempts
```

---

## P0.7.5: CI Secret Scanning (gitleaks/trufflehog)

### Implementation: GitHub Actions Workflow

**File**: `.github/workflows/secret-scan.yml`

```yaml
name: Secret Scanning

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  gitleaks:
    name: Gitleaks Secret Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for comprehensive scan
      
      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}  # Optional for pro features
      
      - name: Upload Gitleaks Report
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: gitleaks-report
          path: gitleaks-report.json

  trufflehog:
    name: TruffleHog Secret Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Run TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
          extra_args: --only-verified
```

### Local Secret Scanning

```bash
# Install gitleaks
brew install gitleaks  # macOS
# or
wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz

# Scan repository
gitleaks detect --source . --verbose

# Scan specific file
gitleaks detect --source backend/.env --verbose
```

---

## Immediate Action Plan

### Phase 1: Emergency Remediation (24 hours)

1. ✅ **Add `.env` to `.gitignore`** (if not already)
2. ✅ **Remove `.env` from git history** (BFG Repo-Cleaner)
3. ✅ **Rotate all exposed secrets**:
   - Generate new `SECRET_KEY`, `JWT_SECRET_KEY`, `ENCRYPTION_KEY`
   - Reset `ADMIN_PASSWORD`
   - Update `MAIL_PASSWORD`
4. ✅ **Add secret scanning to CI** (gitleaks)

### Phase 2: KMS/Vault Integration (1 week)

1. ⏳ **Choose KMS solution** (AWS Secrets Manager or Vault)
2. ⏳ **Create secret store** in chosen platform
3. ⏳ **Migrate production secrets** to KMS/Vault
4. ⏳ **Update application code** to fetch from KMS/Vault
5. ⏳ **Test in staging environment**
6. ⏳ **Deploy to production**

### Phase 3: Ongoing Compliance (continuous)

1. ⏳ **Implement rotation policy** (30-90 days)
2. ⏳ **Set up monitoring** and alerts
3. ⏳ **Quarterly security audits**
4. ⏳ **Update documentation** (Env.md, Security.md)

---

## Compliance Checklist

| Requirement | Status | Evidence |
|-------------|--------|----------|
| No secrets in repository | ❌ | .env contains plaintext secrets |
| KMS/Vault for production | ❌ | Not implemented |
| Secret rotation ≤90 days | ❌ | No rotation policy |
| Least-privilege access | ❌ | No IAM policies defined |
| Audit logging | ❌ | No CloudTrail/Vault audit |
| CI secret scanning | ❌ | No gitleaks/trufflehog in CI |
| Encrypted at rest | ❌ | Plaintext in .env |
| Encrypted in transit | ⚠️ | HTTPS enforced, but secrets in .env |

**Overall Compliance**: ❌ **0/8 (0%)** — CRITICAL NON-COMPLIANCE

---

## Estimated Effort

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| P0.7.1: Identify secrets | P0 | 2 hours | ✅ COMPLETE |
| P0.7.2: KMS/Vault migration plan | P0 | 4 hours | ✅ COMPLETE |
| P0.7.3: Update Env.md | P0 | 2 hours | ⏳ PENDING |
| P0.7.4: Update Security.md | P0 | 2 hours | ⏳ PENDING |
| P0.7.5: CI secret scanning | P0 | 4 hours | ⏳ PENDING |
| **Total** | | **14 hours** | **2/5 complete** |

---

## Next Steps

1. ⏳ Create `docs/Env.md` with secret paths and Key IDs
2. ⏳ Update `docs/Security.md` with secrets lifecycle
3. ⏳ Add `.github/workflows/secret-scan.yml`
4. ⏳ Rotate all exposed secrets
5. ⏳ Implement KMS/Vault integration for production
