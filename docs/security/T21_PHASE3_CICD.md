# T21 Phase 3: CI/CD Integration

**Status:** ✅ Complete  
**Date:** 2025-11-07  
**Phase:** CI/CD Integration  

---

## 📋 Overview

Phase 3 integrates Vault with GitHub Actions CI/CD pipelines, enabling automated testing, secret rotation, and security scanning.

### What Was Done

1. ✅ Created `vault-integration.yml` workflow
2. ✅ Created `vault-secret-rotation.yml` workflow
3. ✅ Updated `backend-tests.yml` to support Vault
4. ✅ Documented CI/CD integration

---

## 🔧 Workflows Created

### 1. Vault Integration Tests (`vault-integration.yml`)

**Purpose:** Test Vault integration in CI/CD environment

**Triggers:**
- Push to Vault-related files
- Pull requests affecting Vault code
- Daily schedule (2 AM UTC)

**Jobs:**

#### Job 1: vault-tests
- Runs Vault container as service
- Configures Vault with test secrets
- Runs `test_vault.py` (19 tests)
- Runs `test_vault_integration.py` (11 tests)
- Tests secret rotation script
- Uploads coverage to Codecov
- Enforces 90% coverage threshold

#### Job 2: vault-security-scan
- Scans Vault client with Bandit
- Scans rotation script
- Checks for hardcoded secrets
- Uploads security scan results

#### Job 3: vault-performance
- Benchmarks Vault client performance
- Asserts average lookup < 50ms
- Asserts max lookup < 200ms
- Validates caching effectiveness

**Example Run:**
```yaml
- name: Run Vault client tests
  env:
    VAULT_ADDR: http://localhost:8200
    VAULT_TOKEN: ci-vault-token
  run: |
    cd backend
    pytest tests/test_vault.py -v --cov=src.vault_client
```

---

### 2. Vault Secret Rotation (`vault-secret-rotation.yml`)

**Purpose:** Automate secret rotation every 90 days

**Triggers:**
- Schedule: Quarterly (every 90 days at 3 AM UTC)
- Manual dispatch with options:
  - Environment: development/staging/production
  - Dry run: true/false

**Jobs:**

#### Job 1: rotate-secrets
- Validates Vault connection
- Backs up current secrets
- Rotates secrets (if not dry run)
- Verifies new secrets
- Uploads backup as artifact (90-day retention)
- Notifies on success/failure

#### Job 2: verify-rotation
- Tests application with new secrets
- Runs all Vault tests
- Verifies application startup
- Only runs if rotation succeeded

#### Job 3: create-rotation-report
- Creates detailed rotation report
- Includes status, details, next rotation date
- Uploads report (365-day retention)

**Manual Trigger:**
```bash
# Via GitHub UI: Actions → Vault Secret Rotation → Run workflow
# Select environment and dry run option
```

**Scheduled Run:**
```yaml
schedule:
  - cron: '0 3 1 */3 *'  # Every 90 days
```

---

### 3. Backend Tests Update (`backend-tests.yml`)

**Changes:**
- Added Vault dependencies installation
- Added VAULT_ADDR environment variable
- Vault will fallback to env vars in CI

**Before:**
```yaml
- name: Install dependencies
  run: |
    pip install -r backend/requirements.txt
```

**After:**
```yaml
- name: Install dependencies
  run: |
    pip install -r backend/requirements.txt
    pip install -r backend/requirements-vault.txt
```

---

## 🔐 GitHub Secrets Required

### For Production Workflows

Add these secrets in GitHub repository settings:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `VAULT_ADDR` | Vault server URL | `https://vault.example.com` |
| `VAULT_TOKEN` | Vault authentication token | `hvs.CAESIJ...` |

**How to Add:**
1. Go to repository Settings
2. Secrets and variables → Actions
3. New repository secret
4. Add `VAULT_ADDR` and `VAULT_TOKEN`

### For Development/Testing

CI workflows use ephemeral Vault container with:
- Token: `ci-vault-token`
- Address: `http://localhost:8200`

---

## 🧪 Testing

### Local Testing

#### Test Vault Integration Workflow
```bash
# Install act (GitHub Actions local runner)
choco install act

# Run vault-integration workflow locally
act -j vault-tests

# Run with secrets
act -j vault-tests -s VAULT_ADDR=http://localhost:8200 -s VAULT_TOKEN=dev-root-token-change-me
```

#### Test Secret Rotation
```bash
# Dry run
python scripts/rotate_secrets.py --dry-run

# Actual rotation (development)
python scripts/rotate_secrets.py --environment development --rotate
```

### CI Testing

#### Trigger Workflows
```bash
# Push to trigger vault-integration.yml
git add .github/workflows/vault-integration.yml
git commit -m "feat: Add Vault integration workflow"
git push

# Manual trigger for secret rotation
# Go to Actions → Vault Secret Rotation → Run workflow
```

---

## 📊 Monitoring

### Workflow Status

Monitor workflows in GitHub Actions:
- **Vault Integration Tests:** Daily at 2 AM UTC
- **Secret Rotation:** Quarterly (every 90 days)

### Metrics Tracked

| Metric | Threshold | Action if Failed |
|--------|-----------|------------------|
| Test Coverage | ≥90% | Workflow fails |
| Vault Lookup Time | <50ms avg | Performance test fails |
| Max Lookup Time | <200ms | Performance test fails |
| Security Scan | No high/critical | Review and fix |

### Artifacts

| Artifact | Retention | Purpose |
|----------|-----------|---------|
| Coverage Reports | 30 days | Track test coverage |
| Security Scans | 90 days | Security audit trail |
| Secret Backups | 90 days | Disaster recovery |
| Rotation Reports | 365 days | Compliance audit |

---

## 🚨 Alerts & Notifications

### Workflow Failures

GitHub will notify via:
- Email to workflow author
- GitHub notifications
- Status checks on PRs

### Secret Rotation

Notifications include:
- ✅ Success: Backup artifact ID, next rotation date
- ❌ Failure: Error details, restore instructions

---

## 🔄 Secret Rotation Process

### Automated (Every 90 Days)

```
Scheduled Trigger (3 AM UTC)
    ↓
Validate Vault Connection
    ↓
Backup Current Secrets
    ↓
Generate New Secrets
    ↓
Update Vault
    ↓
Verify New Secrets
    ↓
Test Application
    ↓
Create Report
    ↓
Upload Artifacts
```

### Manual (On Demand)

```
GitHub Actions UI
    ↓
Select Environment
    ↓
Choose Dry Run (optional)
    ↓
Run Workflow
    ↓
Review Results
    ↓
Download Backup (if needed)
```

---

## 🛠️ Troubleshooting

### Workflow Fails: Vault Connection

**Error:** `Vault authentication failed`

**Solution:**
```bash
# Check secrets are set
gh secret list

# Update Vault token
gh secret set VAULT_TOKEN

# Verify Vault is accessible
curl -H "X-Vault-Token: $VAULT_TOKEN" $VAULT_ADDR/v1/sys/health
```

### Workflow Fails: Tests

**Error:** `pytest failed with exit code 1`

**Solution:**
```bash
# Run tests locally
cd backend
pytest tests/test_vault*.py -v

# Check Vault is running
docker ps | grep vault

# Check secrets exist
docker exec store-vault vault kv get secret/store-erp/development/flask
```

### Secret Rotation Fails

**Error:** `Secret rotation failed`

**Solution:**
```bash
# Download backup artifact from failed run
# Restore secrets manually
docker exec store-vault vault kv put secret/store-erp/development/flask @backup.json

# Verify restore
docker exec store-vault vault kv get secret/store-erp/development/flask
```

---

## 📈 Performance Benchmarks

### CI/CD Workflow Times

| Workflow | Duration | Frequency |
|----------|----------|-----------|
| Vault Integration Tests | ~3-5 min | On push + daily |
| Secret Rotation | ~2-3 min | Quarterly |
| Backend Tests (with Vault) | ~5-7 min | On push |

### Resource Usage

| Resource | Usage |
|----------|-------|
| Vault Container | ~100MB RAM |
| Python Dependencies | ~50MB disk |
| Test Artifacts | ~5MB per run |

---

## 🎯 Next Steps

### Phase 4: Production Deployment

1. Deploy Vault in production environment
2. Configure production secrets
3. Update production workflows
4. Enable audit logging
5. Set up monitoring and alerts

### Future Enhancements

1. **Multi-environment support**
   - Separate workflows for dev/staging/prod
   - Environment-specific rotation schedules

2. **Advanced monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - PagerDuty integration

3. **Compliance**
   - Audit log analysis
   - Compliance reports
   - SOC 2 documentation

---

## 📚 References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Vault CI/CD Integration](https://www.vaultproject.io/docs/platform/k8s/injector)
- [T21 Implementation Guide](./T21_IMPLEMENTATION_GUIDE.md)
- [T21 Phase 2 Integration](./T21_PHASE2_INTEGRATION.md)

---

**✅ Phase 3 Complete! Ready for Production Deployment (Phase 4)**

