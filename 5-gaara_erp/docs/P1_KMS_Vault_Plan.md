# FILE: docs/P1_KMS_Vault_Plan.md | PURPOSE: KMS/Vault Integration Plan | OWNER: Security Team | RELATED: docs/Security.md, docs/Env.md | LAST-AUDITED: 2025-10-25

# P1 - KMS/Vault Integration Plan

**Priority**: P1 - High Priority  
**Status**: Planning  
**Owner**: Security Team  
**Estimated Effort**: 2-3 days

---

## Executive Summary

Implement production-grade secrets management using either **AWS KMS + Secrets Manager** OR **HashiCorp Vault** to replace current `.env` file-based secrets storage. This is a **MANDATORY** requirement per GLOBAL_GUIDELINES v2.3 Section XXXVII.

### Goals

1. ✅ Eliminate secrets from `.env` files in production
2. ✅ Implement envelope encryption for PII/sensitive data
3. ✅ Enable automatic secret rotation (≤90 days)
4. ✅ Provide audit logging for all secret access
5. ✅ Support multiple environments (dev/staging/prod)

---

## Decision: AWS vs Vault

### Option 1: AWS KMS + Secrets Manager

**Pros**:
- ✅ Fully managed service (no infrastructure to maintain)
- ✅ Native integration with AWS services (RDS, S3, etc.)
- ✅ Automatic rotation for RDS/DocumentDB credentials
- ✅ Fine-grained IAM policies
- ✅ Compliance certifications (SOC, PCI-DSS, HIPAA)
- ✅ Pay-per-use pricing (no upfront costs)

**Cons**:
- ❌ Vendor lock-in to AWS
- ❌ Requires AWS account and credentials
- ❌ Higher cost at scale (vs self-hosted Vault)

**Cost Estimate**:
- KMS: $1/month per key + $0.03 per 10,000 requests
- Secrets Manager: $0.40/month per secret + $0.05 per 10,000 API calls
- **Total for ~20 secrets**: ~$10-15/month

### Option 2: HashiCorp Vault

**Pros**:
- ✅ Cloud-agnostic (works anywhere)
- ✅ Advanced features (dynamic secrets, PKI, SSH)
- ✅ Open source (self-hosted option)
- ✅ Multi-cloud support
- ✅ Extensive plugin ecosystem

**Cons**:
- ❌ Requires infrastructure setup and maintenance
- ❌ High availability setup is complex
- ❌ Unsealing process adds operational overhead
- ❌ Self-hosted requires security expertise

**Cost Estimate**:
- Self-hosted: Infrastructure costs only (~$50-100/month for HA setup)
- HCP Vault: $0.03/hour per cluster (~$22/month) + $0.03/hour per node

---

## Recommendation: AWS KMS + Secrets Manager

**Rationale**:
1. **Simplicity**: Fully managed, no infrastructure to maintain
2. **Security**: Battle-tested, compliance-certified
3. **Cost**: Affordable for small-medium scale
4. **Integration**: Easy integration with Python (boto3)
5. **Time-to-value**: Can be implemented in 1-2 days

**OSF Score**: 0.85
- Security: 0.95 (excellent)
- Correctness: 0.90 (proven)
- Reliability: 0.95 (AWS SLA)
- Maintainability: 0.85 (managed service)
- Performance: 0.75 (network latency)
- Speed: 0.70 (API calls add latency)

---

## Implementation Plan

### Phase 1: Setup AWS Resources (Day 1)

**Tasks**:
1. Create AWS account (if not exists)
2. Create IAM user with minimal permissions:
   - `kms:Decrypt`, `kms:Encrypt`, `kms:GenerateDataKey`
   - `secretsmanager:GetSecretValue`, `secretsmanager:DescribeSecret`
3. Create KMS key for envelope encryption
4. Create secrets in Secrets Manager:
   - `gaara-store/prod/database-url`
   - `gaara-store/prod/jwt-secret`
   - `gaara-store/prod/redis-url`
   - `gaara-store/prod/smtp-password`
   - etc.
5. Tag secrets with environment and owner

**Deliverables**:
- AWS account configured
- KMS key created (ARN documented)
- Secrets created and populated
- IAM credentials for app (access key + secret)

### Phase 2: Implement Secrets Manager Adapter (Day 1-2)

**File**: `backend/src/utils/secrets_manager.py`

**Features**:
- Singleton pattern for connection pooling
- Caching with TTL (default: 5 minutes)
- Automatic retry with exponential backoff
- Fallback to `.env` for local development
- Type-safe secret retrieval
- Audit logging

**Interface**:
```python
from src.utils.secrets_manager import get_secret

# Get secret (cached)
db_url = get_secret('database-url')

# Force refresh
jwt_secret = get_secret('jwt-secret', force_refresh=True)

# Get with default
smtp_pass = get_secret('smtp-password', default='')
```

**Deliverables**:
- `backend/src/utils/secrets_manager.py` implemented
- Unit tests for secrets manager
- Integration tests with AWS (mocked)

### Phase 3: Update Application Config (Day 2)

**Files to Update**:
1. `backend/src/database.py` - Use `get_secret('database-url')`
2. `backend/src/auth.py` - Use `get_secret('jwt-secret')`
3. `backend/app.py` - Use `get_secret('redis-url')`
4. `backend/src/routes/export.py` - Use `get_secret('smtp-password')`

**Environment Variables** (only for AWS credentials):
```bash
# .env (local dev only)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
ENVIRONMENT=development  # or staging, production

# Production (injected by deployment)
AWS_REGION=us-east-1
# Use IAM role instead of access keys
ENVIRONMENT=production
```

**Deliverables**:
- All secret references updated
- `.env.example` updated with AWS vars
- Documentation in `/docs/Env.md`

### Phase 4: Implement Envelope Encryption (Day 2-3)

**File**: `backend/src/utils/encryption.py`

**Use Cases**:
- Encrypt PII fields in database (email, phone, address)
- Encrypt backup files
- Encrypt sensitive logs

**Interface**:
```python
from src.utils.encryption import encrypt_field, decrypt_field

# Encrypt PII
encrypted_email = encrypt_field(user.email, context={'user_id': user.id})

# Decrypt PII
email = decrypt_field(encrypted_email, context={'user_id': user.id})
```

**Implementation**:
- Use KMS `GenerateDataKey` for envelope encryption
- Store encrypted data key with ciphertext
- Include context for additional security
- Automatic key rotation support

**Deliverables**:
- `backend/src/utils/encryption.py` implemented
- Migration script for existing PII
- Tests for encryption/decryption

### Phase 5: Secret Rotation (Day 3)

**Automated Rotation**:
- Enable automatic rotation for RDS credentials (30 days)
- Manual rotation for JWT secret (90 days)
- Rotation alerts via CloudWatch

**Rotation Process**:
1. Secrets Manager creates new secret version
2. Lambda function updates database password
3. Application automatically picks up new secret (cache TTL)
4. Old secret version deprecated after grace period

**Deliverables**:
- Rotation enabled for database credentials
- Rotation runbook in `/docs/Runbook.md`
- Alerts configured

### Phase 6: Audit & Monitoring (Day 3)

**CloudWatch Logs**:
- Log all secret access (who, when, which secret)
- Alert on anomalous access patterns
- Dashboard for secret usage metrics

**Metrics**:
- Secret access count by environment
- Cache hit rate
- Failed access attempts
- Rotation status

**Deliverables**:
- CloudWatch dashboard created
- Alerts configured
- Audit log retention policy (90 days)

---

## Testing Strategy

### Unit Tests

```python
# tests/test_secrets_manager.py
def test_get_secret_cached():
    """Test secret caching"""
    secret1 = get_secret('test-secret')
    secret2 = get_secret('test-secret')
    assert secret1 == secret2
    # Verify only 1 AWS API call made

def test_get_secret_force_refresh():
    """Test force refresh bypasses cache"""
    secret1 = get_secret('test-secret')
    secret2 = get_secret('test-secret', force_refresh=True)
    # Verify 2 AWS API calls made

def test_fallback_to_env():
    """Test fallback to .env in development"""
    os.environ['ENVIRONMENT'] = 'development'
    secret = get_secret('test-secret')
    assert secret == os.getenv('TEST_SECRET')
```

### Integration Tests

```python
# tests/test_secrets_integration.py
@pytest.mark.integration
def test_database_connection_with_kms():
    """Test database connection using KMS secret"""
    db_url = get_secret('database-url')
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        assert result.scalar() == 1
```

### Security Tests

```python
# tests/test_secrets_security.py
def test_secrets_not_logged():
    """Ensure secrets are redacted in logs"""
    with capture_logs() as logs:
        secret = get_secret('jwt-secret')
        assert secret not in logs

def test_secrets_not_in_error_messages():
    """Ensure secrets are redacted in exceptions"""
    try:
        raise ValueError(f"Invalid secret: {get_secret('test')}")
    except ValueError as e:
        assert '[REDACTED]' in str(e)
```

---

## Rollout Plan

### Week 1: Development Environment

1. Implement secrets manager adapter
2. Update config to use adapter
3. Test locally with AWS credentials
4. Document setup in `/docs/Env.md`

### Week 2: Staging Environment

1. Create staging secrets in AWS
2. Deploy to staging
3. Run full test suite
4. Monitor for issues

### Week 3: Production Environment

1. Create production secrets in AWS
2. Enable rotation for database credentials
3. Deploy to production (blue-green)
4. Monitor metrics and logs
5. Verify rotation works

---

## Rollback Plan

**If issues occur**:
1. Revert to previous deployment (using `.env` secrets)
2. Investigate root cause
3. Fix and redeploy

**Rollback Triggers**:
- Secret access failures > 5% of requests
- Database connection failures
- Application crashes related to secrets
- Performance degradation > 20%

---

## Documentation Updates

**Files to Update**:
1. `/docs/Env.md` - Add AWS setup instructions
2. `/docs/Security.md` - Document KMS usage
3. `/docs/Runbook.md` - Add secret rotation procedures
4. `/docs/Threat_Model.md` - Update with KMS controls
5. `README.md` - Update deployment instructions

---

## Success Criteria

- [ ] All production secrets stored in AWS Secrets Manager
- [ ] No secrets in `.env` files (except AWS credentials for local dev)
- [ ] Envelope encryption implemented for PII
- [ ] Automatic rotation enabled for database credentials
- [ ] Audit logging configured and monitored
- [ ] Documentation complete
- [ ] All tests passing
- [ ] Zero downtime deployment

---

## Next Steps

1. **Get approval** for AWS account creation and budget
2. **Install boto3**: `pip install boto3`
3. **Create AWS resources** (KMS key, secrets)
4. **Implement secrets manager adapter**
5. **Update application config**
6. **Test and deploy**

---

**Created**: 2025-10-25  
**Owner**: Security Team  
**Approver**: Tech Lead  
**Target Completion**: 2025-10-28

