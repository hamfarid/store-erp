# T21: KMS/Vault Integration - Implementation Guide

**Status:** 🔄 In Progress  
**Date:** 2025-11-06  
**Phase:** P1 - Requirements & Analysis  
**Estimated Time:** 3-4 hours

---

## 📋 Overview

This guide covers the complete implementation of HashiCorp Vault integration for the Store ERP system. Vault provides centralized secret management with:

- ✅ Secure secret storage
- ✅ Secret rotation
- ✅ Audit logging
- ✅ Access control
- ✅ Multiple environments support

---

## 🎯 Objectives

1. ✅ Set up HashiCorp Vault with Docker
2. ✅ Create Vault client module for Python
3. ✅ Implement secret retrieval with caching
4. ✅ Implement secret rotation
5. ✅ Integrate with application configuration
6. ✅ Update CI/CD workflows
7. ✅ Create comprehensive tests
8. ✅ Document procedures

---

## 📁 Files Created

### Core Implementation
- ✅ `backend/src/vault_client.py` - Vault client module (300 lines)
- ✅ `backend/tests/test_vault.py` - Comprehensive tests (300 lines)
- ✅ `scripts/rotate_secrets.py` - Secret rotation script (300 lines)
- ✅ `backend/requirements-vault.txt` - Dependencies

### Configuration
- ✅ `docker-compose.vault.yml` - Vault Docker setup
- ✅ `docs/security/T21_KMS_VAULT_PLAN.md` - Architecture plan

---

## 🚀 Implementation Steps

### Step 1: Install Dependencies

```bash
# Install hvac client
pip install hvac==2.1.0

# Or use requirements file
pip install -r backend/requirements-vault.txt
```

### Step 2: Start Vault with Docker

```powershell
# Option 1: Using setup script
.\scripts\setup_vault.ps1

# Option 2: Manual Docker Compose
docker-compose -f docker-compose.vault.yml up -d

# Verify Vault is running
curl http://127.0.0.1:8200/v1/sys/health
```

### Step 3: Initialize Vault

```bash
# Access Vault CLI
docker exec -it store-vault vault status

# Initialize (if needed)
docker exec -it store-vault vault operator init

# Unseal (if needed)
docker exec -it store-vault vault operator unseal
```

### Step 4: Create Secrets

```bash
# Enable KV v2 secrets engine
docker exec store-vault vault secrets enable -version=2 -path=secret kv

# Create Flask secrets
docker exec store-vault vault kv put secret/store-erp/development/flask \
  secret_key="dev-secret-key-change-me" \
  jwt_secret="dev-jwt-secret-change-me"

# Create database secrets
docker exec store-vault vault kv put secret/store-erp/development/database \
  host="localhost" \
  port="5432" \
  username="store_user" \
  password="dev-password-change-me" \
  database="store_db"

# Create production secrets
docker exec store-vault vault kv put secret/store-erp/production/flask \
  secret_key="prod-secret-key-change-me" \
  jwt_secret="prod-jwt-secret-change-me"
```

### Step 5: Create AppRole for CI/CD

```bash
# Enable AppRole auth method
docker exec store-vault vault auth enable approle

# Create role for CI/CD
docker exec store-vault vault write auth/approle/role/store-ci \
  token_ttl=1h \
  token_max_ttl=4h \
  policies="store-policy"

# Get role ID
docker exec store-vault vault read auth/approle/role/store-ci/role-id

# Generate secret ID
docker exec store-vault vault write -f auth/approle/role/store-ci/secret-id
```

### Step 6: Create Vault Policy

```bash
# Create policy file
cat > /tmp/store-policy.hcl << 'EOF'
# Read secrets
path "secret/data/store-erp/*" {
  capabilities = ["read", "list"]
}

# Rotate secrets
path "secret/data/store-erp/*" {
  capabilities = ["create", "update"]
}

# Audit logs
path "sys/audit" {
  capabilities = ["read"]
}
EOF

# Write policy
docker exec -i store-vault vault policy write store-policy - < /tmp/store-policy.hcl
```

### Step 7: Test Vault Client

```python
from src.vault_client import VaultClient

# Initialize client
vault = VaultClient(
    vault_url='http://127.0.0.1:8200',
    vault_token='dev-root-token-change-me',
    environment='development'
)

# Get secret
flask_config = vault.get_secret('flask')
print(f"Flask config: {flask_config}")

# Get specific field
secret_key = vault.get_secret('flask', field='secret_key')
print(f"Secret key: {secret_key}")

# Check health
health = vault.health_check()
print(f"Vault health: {health}")
```

### Step 8: Run Tests

```bash
# Run all Vault tests
pytest backend/tests/test_vault.py -v

# Run with coverage
pytest backend/tests/test_vault.py --cov=src.vault_client

# Run integration tests (requires Vault running)
pytest backend/tests/test_vault.py -v -m integration
```

### Step 9: Rotate Secrets

```bash
# Rotate all secrets
python scripts/rotate_secrets.py --all

# Rotate specific secret
python scripts/rotate_secrets.py --secret flask

# List backups
python scripts/rotate_secrets.py --list-backups

# Restore from backup
python scripts/rotate_secrets.py --restore backups/secrets/flask_20251106_120000.json
```

### Step 10: Update Application Configuration

```python
# In backend/src/config.py
from vault_client import get_secret

class Config:
    """Base configuration."""
    
    # Get secrets from Vault with fallback to env vars
    SECRET_KEY = get_secret(
        'flask',
        field='secret_key',
        fallback_env='SECRET_KEY'
    )
    
    JWT_SECRET_KEY = get_secret(
        'flask',
        field='jwt_secret',
        fallback_env='JWT_SECRET_KEY'
    )
    
    # Database configuration
    db_config = get_secret('database', fallback_env='DATABASE_URL')
    if db_config:
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{db_config['username']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
```

---

## 🔐 Security Best Practices

### 1. Token Management
```bash
# Use short-lived tokens
export VAULT_TOKEN="your-token"

# Revoke token when done
vault token revoke $VAULT_TOKEN
```

### 2. Audit Logging
```bash
# Enable audit logging
docker exec store-vault vault audit enable file file_path=/vault/logs/audit.log

# View audit logs
docker exec store-vault tail -f /vault/logs/audit.log
```

### 3. Secret Rotation Schedule
```bash
# Add to crontab for automatic rotation
0 2 * * 0 python /path/to/scripts/rotate_secrets.py --all
```

### 4. Backup Secrets
```bash
# Backup all secrets
docker exec store-vault vault kv list secret/store-erp/development > backup.txt

# Backup to file
docker exec store-vault vault kv get -format=json secret/store-erp/development/flask > flask_backup.json
```

---

## 📊 Vault Client API

### Basic Usage

```python
from src.vault_client import get_secret, get_vault_client

# Get entire secret
flask_config = get_secret('flask')

# Get specific field
secret_key = get_secret('flask', field='secret_key')

# With fallback
secret_key = get_secret(
    'flask',
    field='secret_key',
    fallback_env='SECRET_KEY'
)

# Get client instance
vault = get_vault_client()

# Set secret
vault.set_secret('flask', {
    'secret_key': 'new-key',
    'jwt_secret': 'new-jwt'
})

# Rotate secret
vault.rotate_secret('flask', 'secret_key', 'rotated-key')

# Health check
health = vault.health_check()
```

### Advanced Usage

```python
# Custom client
vault = VaultClient(
    vault_url='http://vault.example.com:8200',
    vault_token='your-token',
    environment='production',
    cache_ttl=600  # 10 minutes
)

# Disable caching
secret = vault.get_secret('flask', use_cache=False)

# Clear cache
vault.clear_cache()

# Check health
health = vault.health_check()
if health['authenticated']:
    print("Vault is ready!")
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest backend/tests/test_vault.py::TestVaultClientInitialization -v
pytest backend/tests/test_vault.py::TestSecretRetrieval -v
pytest backend/tests/test_vault.py::TestSecretRotation -v
```

### Integration Tests
```bash
# Requires Vault running
pytest backend/tests/test_vault.py -v -m integration
```

### Manual Testing
```bash
# Test client initialization
python -c "from src.vault_client import VaultClient; v = VaultClient(); print(v.health_check())"

# Test secret retrieval
python -c "from src.vault_client import get_secret; print(get_secret('flask'))"
```

---

## 🐛 Troubleshooting

### Issue: Connection Refused
```
Error: Connection refused at http://127.0.0.1:8200
```

**Solution:**
```bash
# Check if Vault is running
docker ps | grep vault

# Start Vault
docker-compose -f docker-compose.vault.yml up -d

# Check logs
docker logs store-vault
```

### Issue: Authentication Failed
```
Error: Vault authentication failed - invalid token
```

**Solution:**
```bash
# Check token
echo $VAULT_TOKEN

# Get new token
docker exec store-vault vault token create

# Set token
export VAULT_TOKEN="new-token"
```

### Issue: Secret Not Found
```
Error: Secret not found in Vault
```

**Solution:**
```bash
# List available secrets
docker exec store-vault vault kv list secret/store-erp/development

# Create secret if missing
docker exec store-vault vault kv put secret/store-erp/development/flask \
  secret_key="test-key"
```

---

## 📈 Monitoring

### Health Checks
```bash
# Check Vault health
curl http://127.0.0.1:8200/v1/sys/health

# Check client health
python -c "from src.vault_client import get_vault_client; print(get_vault_client().health_check())"
```

### Audit Logs
```bash
# View recent audit logs
docker exec store-vault tail -f /vault/logs/audit.log

# Search for specific events
docker exec store-vault grep "secret_key" /vault/logs/audit.log
```

---

## ✅ Checklist

- [ ] Install hvac library
- [ ] Start Vault with Docker
- [ ] Initialize Vault
- [ ] Create secrets
- [ ] Create AppRole for CI/CD
- [ ] Create Vault policy
- [ ] Test Vault client
- [ ] Run all tests
- [ ] Update application config
- [ ] Update CI/CD workflows
- [ ] Document procedures
- [ ] Set up secret rotation schedule
- [ ] Enable audit logging
- [ ] Create backup strategy

---

## 📚 References

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [hvac Python Client](https://hvac.readthedocs.io/)
- [Vault KV Secrets Engine](https://www.vaultproject.io/docs/secrets/kv)
- [Vault AppRole Auth](https://www.vaultproject.io/docs/auth/approle)

---

## 🎉 Next Steps

1. ✅ Complete all implementation steps above
2. ✅ Run comprehensive tests
3. ✅ Update CI/CD workflows to use Vault
4. ✅ Deploy to staging environment
5. ✅ Monitor and validate
6. ✅ Deploy to production

---

**Status:** 🔄 In Progress  
**Last Updated:** 2025-11-06  
**Next Review:** After implementation completion

