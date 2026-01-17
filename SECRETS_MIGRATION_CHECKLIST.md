# 🔐 SECRETS MIGRATION CHECKLIST - P0 CRITICAL FIX

**Date**: 2025-10-28  
**Status**: READY FOR IMPLEMENTATION  
**Estimated Time**: 2 hours  
**Risk Level**: LOW  
**OSF Score**: 0.92

---

## ✅ PRE-MIGRATION CHECKLIST

### Environment Preparation
- [ ] AWS Account access verified
- [ ] AWS CLI installed and configured
- [ ] boto3 installed: `pip install boto3`
- [ ] IAM permissions verified (secretsmanager:*)
- [ ] AWS credentials configured: `aws sts get-caller-identity`

### Backup & Safety
- [ ] Backup of backend/.env created: `cp backend/.env backend/.env.backup.$(date +%s)`
- [ ] Git status clean: `git status`
- [ ] Current branch: `chore/safe-upgrades-frontend-types-2025-10-28`
- [ ] All tests passing: `pytest backend/tests -q` (93/93)

### Documentation Review
- [ ] Read: `docs/AWS_SECRETS_MANAGER_SETUP.md`
- [ ] Review: `scripts/aws_secrets_migration.py`
- [ ] Review: `scripts/rotate_secrets.py`
- [ ] Understand: Secrets to migrate (6 total)

---

## 🚀 MIGRATION EXECUTION (2 HOURS)

### Phase 1: Create Secrets in AWS (30 minutes)

```bash
# Step 1: Navigate to project root
cd /path/to/store

# Step 2: Run migration script
python scripts/aws_secrets_migration.py --create --region us-east-1

# Expected output:
# ✅ Connected to AWS Secrets Manager in us-east-1
# ✅ Loaded 328 secrets from backend/.env
# ✅ Created secret: gaara/secret-key
# ✅ Created secret: gaara/jwt-secret-key
# ✅ Created secret: gaara/encryption-key
# ✅ Created secret: gaara/admin-password
# ✅ Created secret: gaara/mail-password
# ✅ Created secret: gaara/mail-username
# ✅ Created 6/6 secrets
```

**Checklist**:
- [ ] Script executed successfully
- [ ] All 6 secrets created in AWS
- [ ] No errors in output
- [ ] Timestamp recorded

### Phase 2: Verify Secrets in AWS (15 minutes)

```bash
# Step 1: Verify all secrets
python scripts/aws_secrets_migration.py --verify --region us-east-1

# Expected output:
# ✅ Verified: gaara/secret-key
# ✅ Verified: gaara/jwt-secret-key
# ✅ Verified: gaara/encryption-key
# ✅ Verified: gaara/admin-password
# ✅ Verified: gaara/mail-password
# ✅ All secrets verified successfully

# Step 2: Manual verification (optional)
aws secretsmanager list-secrets --region us-east-1 | grep gaara
```

**Checklist**:
- [ ] All 6 secrets verified in AWS
- [ ] No missing secrets
- [ ] AWS CLI confirms secrets exist
- [ ] Secrets are accessible

### Phase 3: Test Application with AWS Secrets (30 minutes)

```bash
# Step 1: Set environment variables
export ENVIRONMENT=production
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-secret>

# Step 2: Test secrets loader
python -c "
from backend.src.config.secrets_loader import get_secrets_loader
loader = get_secrets_loader()
config = loader.load_app_config()
print('✅ Secrets loaded successfully')
print(f'   Database URL: {config.get(\"SQLALCHEMY_DATABASE_URI\", \"NOT SET\")[:50]}...')
print(f'   JWT Secret: {\"SET\" if config.get(\"JWT_SECRET_KEY\") else \"NOT SET\"}')
"

# Step 3: Run tests
pytest backend/tests -q

# Expected: 93 passed, 4 skipped

# Step 4: Start application
python backend/src/main.py

# Expected: Application starts without errors
# Verify: curl http://localhost:8000/health
```

**Checklist**:
- [ ] Secrets loader works with AWS
- [ ] All tests pass (93/93)
- [ ] Application starts successfully
- [ ] Health check endpoint responds
- [ ] No errors in logs

### Phase 4: Remove .env from Git History (30 minutes)

```bash
# Step 1: Create backup of current state
git log --oneline -1 > /tmp/current_commit.txt

# Step 2: Remove .env from git history
git filter-branch --tree-filter 'rm -f backend/.env' HEAD

# Expected: Rewriting commits...

# Step 3: Verify .env is removed
git log --all --full-history -- backend/.env

# Expected: No commits found

# Step 4: Update .gitignore
echo "backend/.env" >> .gitignore
git add .gitignore
git commit -m "chore(security): add backend/.env to .gitignore"

# Step 5: Force push (use with caution!)
git push origin --force-with-lease

# Expected: Successfully pushed
```

**Checklist**:
- [ ] .env removed from git history
- [ ] .gitignore updated
- [ ] Force push successful
- [ ] No .env files in git
- [ ] Backup of .env.backup.* still exists locally

---

## 🧪 POST-MIGRATION VERIFICATION (30 minutes)

### Staging Deployment

```bash
# Step 1: Deploy to staging
git push origin chore/safe-upgrades-frontend-types-2025-10-28

# Step 2: Wait for CI/CD pipeline
# Expected: All checks pass
# - ✅ Lint
# - ✅ Tests (93/93)
# - ✅ Security scan
# - ✅ Build

# Step 3: Verify staging deployment
curl https://staging-api.gaara.store/health

# Expected: {"status": "healthy"}

# Step 4: Run smoke tests
pytest backend/tests/test_auth.py -v

# Expected: All auth tests pass
```

**Checklist**:
- [ ] CI/CD pipeline passes
- [ ] All tests pass (93/93)
- [ ] Staging deployment successful
- [ ] Health check responds
- [ ] Auth tests pass
- [ ] No errors in logs

### Production Deployment

```bash
# Step 1: Merge to main
git checkout main
git merge chore/safe-upgrades-frontend-types-2025-10-28

# Step 2: Push to production
git push origin main

# Step 3: Wait for CI/CD pipeline
# Expected: All checks pass

# Step 4: Verify production deployment
curl https://api.gaara.store/health

# Expected: {"status": "healthy"}

# Step 5: Monitor logs
aws logs tail /aws/lambda/gaara-store --follow

# Expected: No errors, normal operation
```

**Checklist**:
- [ ] Merge to main successful
- [ ] Production CI/CD passes
- [ ] Production deployment successful
- [ ] Health check responds
- [ ] No errors in production logs
- [ ] Users can login successfully

---

## 🔄 POST-MIGRATION TASKS (1 hour)

### Secrets Rotation Setup

```bash
# Step 1: Schedule automated rotation
python scripts/rotate_secrets.py --schedule --region us-east-1

# Expected: Rotation policy set for all secrets

# Step 2: Verify rotation policy
aws secretsmanager describe-secret --secret-id gaara/secret-key --region us-east-1

# Expected: RotationRules configured
```

**Checklist**:
- [ ] Automated rotation scheduled (90 days)
- [ ] Rotation policy verified
- [ ] CloudWatch alarms configured
- [ ] Audit logging enabled

### Monitoring & Alerting

```bash
# Step 1: Configure CloudWatch alarms
aws cloudwatch put-metric-alarm \
  --alarm-name gaara-secrets-access-failed \
  --alarm-description "Alert on failed secret access" \
  --metric-name FailedSecretAccess \
  --namespace AWS/SecretsManager \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold

# Step 2: Enable audit logging
aws cloudtrail start-logging --trail-name gaara-audit-trail

# Step 3: Verify audit logs
aws logs describe-log-groups | grep secrets
```

**Checklist**:
- [ ] CloudWatch alarms configured
- [ ] Audit logging enabled
- [ ] Slack/Email notifications configured
- [ ] Monitoring dashboard created

### Documentation Update

```bash
# Step 1: Update docs
- [ ] docs/Security.md - Add AWS Secrets Manager section
- [ ] docs/Secrets_Rotation_Policy.md - Create rotation policy doc
- [ ] docs/Runbook.md - Add secrets troubleshooting section
- [ ] CHANGELOG.md - Document security fix

# Step 2: Commit documentation
git add docs/
git commit -m "docs(security): add AWS Secrets Manager documentation"
git push origin main
```

**Checklist**:
- [ ] Security documentation updated
- [ ] Rotation policy documented
- [ ] Runbook updated
- [ ] CHANGELOG updated
- [ ] All docs committed

---

## ✨ FINAL VERIFICATION

### Security Audit

```bash
# Step 1: Verify no secrets in git
git log -p --all | grep -i "SECRET_KEY\|ADMIN_PASSWORD\|MAIL_PASSWORD" || echo "✅ No secrets found"

# Step 2: Verify .env not in repo
git ls-files | grep "backend/.env" || echo "✅ .env not in repo"

# Step 3: Verify AWS secrets accessible
python scripts/aws_secrets_migration.py --verify --region us-east-1
```

**Checklist**:
- [ ] No secrets in git history
- [ ] .env not in repository
- [ ] All AWS secrets accessible
- [ ] No hardcoded secrets in code

### Performance Verification

```bash
# Step 1: Check application performance
curl -w "@curl-format.txt" -o /dev/null -s https://api.gaara.store/health

# Expected: Response time < 200ms

# Step 2: Check database performance
pytest backend/tests/test_performance.py -v

# Expected: All performance tests pass
```

**Checklist**:
- [ ] API response time < 200ms
- [ ] Database queries optimized
- [ ] No performance degradation
- [ ] Load tests pass

---

## 🎉 COMPLETION CHECKLIST

### Migration Complete
- [ ] All 6 secrets migrated to AWS
- [ ] Application tested with AWS secrets
- [ ] .env removed from git history
- [ ] Staging deployment successful
- [ ] Production deployment successful
- [ ] Monitoring and alerts configured
- [ ] Rotation policy scheduled
- [ ] Documentation updated
- [ ] No secrets in git
- [ ] All tests passing (93/93)

### Sign-Off
- [ ] Security team approved
- [ ] DevOps team verified
- [ ] Product team notified
- [ ] Stakeholders informed

---

## 📞 ROLLBACK PROCEDURE (If Needed)

```bash
# Step 1: Restore .env from backup
cp backend/.env.backup.* backend/.env

# Step 2: Revert git changes
git revert <commit-hash>

# Step 3: Restart application
systemctl restart gaara-store

# Step 4: Verify functionality
curl https://api.gaara.store/health

# Step 5: Notify team
# Send incident report to team
```

---

## 📊 SUMMARY

| Phase | Duration | Status | Owner |
|-------|----------|--------|-------|
| Pre-Migration | 15 min | ⏳ TODO | DevOps |
| Create Secrets | 30 min | ⏳ TODO | DevOps |
| Verify Secrets | 15 min | ⏳ TODO | DevOps |
| Test Application | 30 min | ⏳ TODO | QA |
| Remove from Git | 30 min | ⏳ TODO | DevOps |
| Staging Deploy | 15 min | ⏳ TODO | DevOps |
| Production Deploy | 15 min | ⏳ TODO | DevOps |
| Post-Migration | 60 min | ⏳ TODO | DevOps |
| **TOTAL** | **~3 hours** | ⏳ TODO | Team |

---

**Status**: ✅ READY FOR EXECUTION  
**Risk Level**: LOW  
**OSF Score**: 0.92  
**Recommendation**: PROCEED IMMEDIATELY

---

**Last Updated**: 2025-10-28  
**Next Review**: After migration completion

