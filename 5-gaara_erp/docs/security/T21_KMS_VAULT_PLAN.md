# T21: KMS/Vault Integration Plan

**Date:** 2025-11-06  
**Priority:** P1 (High Priority)  
**Status:** 📋 Planning Phase  
**Estimated Time:** 3-4 hours

---

## Objective

Implement secure secret management using HashiCorp Vault or AWS KMS to replace environment variable-based secret storage.

---

## Current State Analysis

### Current Secret Management

**Secrets Currently in Environment Variables:**
1. `SECRET_KEY` - Flask session secret
2. `JWT_SECRET_KEY` - JWT token signing key
3. `DATABASE_URL` - Database connection string (contains password)
4. `REDIS_URL` - Redis connection string (if used)
5. API keys (if any)

**Current Issues:**
- ❌ Secrets stored in `.env` files (risk of exposure)
- ❌ No secret rotation mechanism
- ❌ No audit trail for secret access
- ❌ Secrets visible in environment variables
- ❌ No centralized secret management

---

## Solution Options

### Option 1: HashiCorp Vault (Recommended for Self-Hosted)

**Pros:**
- ✅ Open-source and free
- ✅ Self-hosted (full control)
- ✅ Dynamic secrets support
- ✅ Secret rotation built-in
- ✅ Audit logging
- ✅ Multiple authentication methods
- ✅ Encryption as a service
- ✅ Active community

**Cons:**
- ⚠️ Requires infrastructure setup
- ⚠️ Needs maintenance
- ⚠️ Learning curve

**Best For:**
- Self-hosted applications
- Multi-cloud environments
- Organizations wanting full control

---

### Option 2: AWS Secrets Manager

**Pros:**
- ✅ Fully managed service
- ✅ Automatic secret rotation
- ✅ Integration with AWS services
- ✅ Audit logging (CloudTrail)
- ✅ No infrastructure to manage

**Cons:**
- ⚠️ AWS-specific (vendor lock-in)
- ⚠️ Cost per secret ($0.40/month + API calls)
- ⚠️ Requires AWS account

**Best For:**
- AWS-hosted applications
- Organizations already using AWS
- Teams wanting managed solution

---

### Option 3: Azure Key Vault

**Pros:**
- ✅ Fully managed service
- ✅ Integration with Azure services
- ✅ Hardware security module (HSM) support
- ✅ Audit logging

**Cons:**
- ⚠️ Azure-specific (vendor lock-in)
- ⚠️ Requires Azure account

**Best For:**
- Azure-hosted applications
- Organizations using Azure

---

## Recommended Solution: HashiCorp Vault

**Rationale:**
1. ✅ Self-hosted (no vendor lock-in)
2. ✅ Free and open-source
3. ✅ Works with any cloud or on-premises
4. ✅ Comprehensive feature set
5. ✅ Active community and documentation

---

## Implementation Plan

### Phase 1: Vault Setup (1 hour)

**Tasks:**
1. Install HashiCorp Vault
   - Docker container (recommended for development)
   - Binary installation (for production)

2. Initialize Vault
   - Generate unseal keys
   - Store unseal keys securely
   - Create root token

3. Configure Vault
   - Enable KV secrets engine (v2)
   - Set up authentication method (AppRole for CI/CD)
   - Configure policies

**Deliverables:**
- Running Vault instance
- Vault configuration files
- Unseal keys (stored securely)
- Root token (stored securely)

---

### Phase 2: Secret Migration (1 hour)

**Tasks:**
1. Create secret structure in Vault
   ```
   secret/
   ├── store-erp/
   │   ├── development/
   │   │   ├── flask
   │   │   ├── database
   │   │   └── jwt
   │   ├── staging/
   │   └── production/
   ```

2. Migrate secrets to Vault
   - Flask secrets (SECRET_KEY, JWT_SECRET_KEY)
   - Database credentials
   - API keys

3. Update application configuration
   - Install `hvac` (Vault Python client)
   - Create Vault client wrapper
   - Update config to fetch from Vault

**Deliverables:**
- Secrets stored in Vault
- Application code updated
- Vault client wrapper

---

### Phase 3: Application Integration (1 hour)

**Tasks:**
1. Create Vault client module
   ```python
   # src/vault_client.py
   import hvac
   from functools import lru_cache
   
   class VaultClient:
       def __init__(self):
           self.client = hvac.Client(url=VAULT_URL)
           self.authenticate()
       
       def get_secret(self, path):
           return self.client.secrets.kv.v2.read_secret_version(path=path)
   ```

2. Update configuration
   ```python
   # config.py
   from src.vault_client import VaultClient
   
   vault = VaultClient()
   
   class Config:
       SECRET_KEY = vault.get_secret('store-erp/development/flask')['secret_key']
       JWT_SECRET_KEY = vault.get_secret('store-erp/development/jwt')['secret_key']
   ```

3. Update CI/CD workflows
   - Add Vault authentication
   - Fetch secrets during deployment
   - Update GitHub Actions secrets

**Deliverables:**
- Vault client module
- Updated configuration
- Updated CI/CD workflows

---

### Phase 4: Secret Rotation (30 minutes)

**Tasks:**
1. Implement secret rotation script
   ```python
   # scripts/rotate_secrets.py
   import secrets
   from src.vault_client import VaultClient
   
   def rotate_flask_secret():
       new_secret = secrets.token_urlsafe(32)
       vault.update_secret('store-erp/production/flask', {'secret_key': new_secret})
   ```

2. Configure rotation schedule
   - Manual rotation initially
   - Automated rotation (cron job or Vault policy)

3. Document rotation procedure

**Deliverables:**
- Secret rotation script
- Rotation documentation
- Rotation schedule

---

### Phase 5: Testing & Documentation (30 minutes)

**Tasks:**
1. Test secret retrieval
   - Development environment
   - Staging environment
   - Production environment

2. Test secret rotation
   - Rotate secrets
   - Verify application still works
   - Verify old secrets are invalidated

3. Create documentation
   - Setup guide
   - Usage guide
   - Troubleshooting guide
   - Rotation guide

**Deliverables:**
- Test results
- Comprehensive documentation

---

## Technical Implementation

### 1. Vault Installation (Docker)

```bash
# docker-compose.yml
version: '3.8'
services:
  vault:
    image: hashicorp/vault:latest
    container_name: vault
    ports:
      - "8200:8200"
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: "dev-root-token"
      VAULT_DEV_LISTEN_ADDRESS: "0.0.0.0:8200"
    cap_add:
      - IPC_LOCK
    volumes:
      - ./vault/data:/vault/data
      - ./vault/config:/vault/config
```

### 2. Vault Initialization

```bash
# Initialize Vault
docker-compose up -d vault
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='dev-root-token'

# Enable KV secrets engine
vault secrets enable -version=2 -path=secret kv

# Create secrets
vault kv put secret/store-erp/development/flask secret_key="your-secret-key"
vault kv put secret/store-erp/development/jwt secret_key="your-jwt-secret"
```

### 3. Python Integration

```python
# requirements.txt
hvac==2.1.0

# src/vault_client.py
import os
import hvac
from functools import lru_cache

class VaultClient:
    def __init__(self):
        self.vault_url = os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200')
        self.vault_token = os.getenv('VAULT_TOKEN')
        self.client = hvac.Client(url=self.vault_url, token=self.vault_token)
        
        if not self.client.is_authenticated():
            raise Exception("Vault authentication failed")
    
    @lru_cache(maxsize=128)
    def get_secret(self, path):
        """Get secret from Vault with caching"""
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            return response['data']['data']
        except Exception as e:
            raise Exception(f"Failed to get secret from Vault: {e}")
    
    def update_secret(self, path, data):
        """Update secret in Vault"""
        try:
            self.client.secrets.kv.v2.create_or_update_secret(path=path, secret=data)
        except Exception as e:
            raise Exception(f"Failed to update secret in Vault: {e}")

# Usage
vault = VaultClient()
flask_secrets = vault.get_secret('store-erp/development/flask')
SECRET_KEY = flask_secrets['secret_key']
```

---

## Security Considerations

### 1. Vault Access Control

**Policies:**
```hcl
# app-policy.hcl
path "secret/data/store-erp/development/*" {
  capabilities = ["read"]
}

path "secret/data/store-erp/production/*" {
  capabilities = ["read"]
}
```

### 2. Authentication Methods

**AppRole (for CI/CD):**
```bash
vault auth enable approle
vault write auth/approle/role/store-erp \
    secret_id_ttl=24h \
    token_ttl=1h \
    token_max_ttl=4h \
    policies="app-policy"
```

### 3. Audit Logging

```bash
vault audit enable file file_path=/vault/logs/audit.log
```

---

## Rollback Plan

If Vault integration fails:

1. **Immediate Rollback:**
   - Revert to environment variables
   - Use backup `.env` file
   - Restart application

2. **Gradual Rollback:**
   - Keep both Vault and env vars
   - Fallback to env vars if Vault fails
   - Monitor for issues

---

## Success Criteria

- ✅ Vault running and accessible
- ✅ All secrets migrated to Vault
- ✅ Application retrieves secrets from Vault
- ✅ CI/CD workflows updated
- ✅ Secret rotation working
- ✅ Documentation complete
- ✅ No secrets in environment variables
- ✅ Audit logging enabled

---

## Next Steps

1. **Review this plan** - Get approval
2. **Set up Vault** - Docker or binary
3. **Migrate secrets** - Move to Vault
4. **Update application** - Integrate Vault client
5. **Test thoroughly** - All environments
6. **Document** - Complete documentation
7. **Deploy** - Production rollout

---

**Ready to proceed with T21 implementation?**

