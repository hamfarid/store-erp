# 🔐 Production Secrets Configuration Guide

## Required GitHub Secrets

Configure these secrets in: **Settings → Secrets and variables → Actions**

### Database Secrets
```
PROD_DB_HOST               # PostgreSQL host (e.g., db.example.com)
PROD_DB_PORT               # PostgreSQL port (default: 5432)
PROD_DB_NAME               # Database name
PROD_DB_USER               # Database username
PROD_DB_PASSWORD           # Database password (strong password required)
PROD_DATABASE_URL          # Full connection string (optional, overrides above)
```

### Redis Secrets
```
PROD_REDIS_HOST            # Redis host
PROD_REDIS_PORT            # Redis port (default: 6379)
PROD_REDIS_PASSWORD        # Redis password
```

### Application Secrets
```
SECRET_KEY                 # Django/Flask secret key (generate with: openssl rand -hex 32)
JWT_SECRET_KEY             # JWT signing key (generate with: openssl rand -hex 32)
ENCRYPTION_KEY             # Data encryption key (if used)
```

### AWS Secrets (for backups)
```
AWS_ACCESS_KEY_ID          # AWS access key
AWS_SECRET_ACCESS_KEY      # AWS secret key
AWS_REGION                 # AWS region (e.g., us-east-1)
BACKUP_S3_BUCKET           # S3 bucket for backups
```

### Deployment Secrets
```
KUBE_CONFIG                # Base64 encoded Kubernetes config (kubectl config view --raw | base64)
DEPLOY_SSH_KEY             # SSH private key for server access
DEPLOY_HOST                # Production server IP/domain
DEPLOY_USER                # Deployment user
```

### Monitoring & Alerts
```
SLACK_WEBHOOK_URL          # Slack webhook for notifications
ALERT_EMAIL                # Email for critical alerts
PAGERDUTY_WEBHOOK_URL      # PagerDuty integration (optional)
```

### Email Configuration
```
SMTP_HOST                  # SMTP server
SMTP_PORT                  # SMTP port (587 or 465)
SMTP_USERNAME              # SMTP username
SMTP_PASSWORD              # SMTP password
SMTP_FROM                  # From email address
EMAIL_USERNAME             # Email username for notifications
EMAIL_PASSWORD             # Email password for notifications
```

### External Services
```
PROD_BACKEND_URL           # Backend API URL (e.g., https://api.example.com)
PROD_FRONTEND_URL          # Frontend URL (e.g., https://example.com)
```

### Optional: Code Quality Services
```
CODECOV_TOKEN              # Codecov token for coverage reports
SONAR_TOKEN                # SonarCloud token for code quality
```

### Optional: Grafana
```
GRAFANA_ADMIN_USER         # Grafana admin username
GRAFANA_ADMIN_PASSWORD     # Grafana admin password
```

---

## How to Add Secrets

### Via GitHub UI:
1. Go to: https://github.com/hamfarid/gaara-Scan-system/settings/secrets/actions
2. Click "New repository secret"
3. Enter name and value
4. Click "Add secret"

### Via GitHub CLI:
```bash
# Single secret
gh secret set SECRET_NAME

# From file
gh secret set SECRET_NAME < secret.txt

# From stdin
echo "secret_value" | gh secret set SECRET_NAME
```

---

## Secret Generation Commands

### Generate Random Secrets
```bash
# 32-character hex string
openssl rand -hex 32

# Base64 encoded (64 characters)
openssl rand -base64 32

# UUID
uuidgen

# Strong password
openssl rand -base64 48 | tr -d "=+/" | cut -c1-32
```

### Encode Kubernetes Config
```bash
# Get and encode kubeconfig
kubectl config view --raw | base64 -w 0
```

### Generate SSH Key Pair
```bash
# Generate key
ssh-keygen -t ed25519 -C "deploy@gaara-scan-system" -f deploy_key

# Add public key to server's authorized_keys
cat deploy_key.pub

# Set private key as secret (paste entire content)
cat deploy_key
```

---

## Environment-Specific Secrets

### Development
- Use `.env` file locally
- Never commit to git
- Add to `.gitignore`

### Staging
- Use GitHub Environments
- Settings → Environments → staging
- Configure protection rules

### Production
- Use GitHub Environments
- Settings → Environments → production
- Require reviewers
- Enable deployment branches

---

## Secret Rotation Schedule

| Secret Type | Rotation Frequency | Last Rotated |
|-------------|-------------------|--------------|
| Database Passwords | Every 90 days | - |
| API Keys | Every 180 days | - |
| JWT Secrets | Every 365 days | - |
| SSH Keys | Every 365 days | - |
| SSL Certificates | Auto-renewed | - |

---

## Security Best Practices

### DO ✅
- Use strong, unique passwords
- Enable 2FA on all accounts
- Rotate secrets regularly
- Use GitHub Environments for prod
- Encrypt sensitive data at rest
- Monitor secret access logs
- Use dedicated service accounts
- Implement least privilege access

### DON'T ❌
- Commit secrets to git
- Share secrets via email/chat
- Use default passwords
- Reuse passwords across services
- Store secrets in code comments
- Use weak encryption
- Give broad access permissions
- Skip secret rotation

---

## Troubleshooting

### Secret Not Working
1. Check secret name matches exactly (case-sensitive)
2. Verify secret value has no extra spaces
3. Check environment scoping
4. Review workflow permissions

### Access Denied
1. Verify GITHUB_TOKEN permissions
2. Check repository settings
3. Review branch protection rules

### Workflow Fails with Secret Error
1. Confirm secret exists
2. Check spelling in workflow file
3. Verify secret is not empty
4. Review workflow logs

---

## Audit Log

Keep track of secret changes:

```bash
# View audit log
gh api /repos/hamfarid/gaara-Scan-system/actions/secrets

# List all secrets
gh secret list
```

---

## Emergency Procedures

### If Secret Compromised:
1. **Immediately** rotate the secret
2. Update in GitHub Secrets
3. Trigger redeployment
4. Review access logs
5. Document incident
6. Notify security team

### Rollback with New Secrets:
```bash
# Update secrets first
gh secret set NEW_SECRET_NAME

# Then rollback
gh workflow run rollback.yml
```

---

## Backup Secrets (Encrypted)

Store encrypted backup:
```bash
# Export to encrypted file
gh secret list | gpg --encrypt --recipient your@email.com > secrets.gpg

# Restore from backup
gpg --decrypt secrets.gpg
```

---

**⚠️ IMPORTANT:** Never share this document with actual secret values. This is a template only.

**Last Updated:** 2026-01-31
