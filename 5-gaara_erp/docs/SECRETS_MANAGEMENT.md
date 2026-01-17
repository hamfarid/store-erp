# Secrets Management Guide - Gaara ERP

**Created**: 2025-12-01
**Purpose**: Guide for migrating secrets from environment variables to centralized secret managers

---

## Overview

This document outlines the recommended approach for managing secrets in Gaara ERP across different deployment environments.

## Current Secret Types

| Secret | Environment Variable | Usage |
|--------|---------------------|-------|
| Django Secret Key | `SECRET_KEY` / `DJANGO_SECRET_KEY` | Session signing, CSRF tokens |
| Database Password | `DB_PASSWORD` | PostgreSQL authentication |
| OpenAI API Key | `OPENAI_API_KEY` | AI features integration |
| Langfuse Keys | `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY` | AI monitoring |
| Flask Secret Key | `FLASK_SECRET_KEY` | API server sessions |

---

## Recommended Secret Managers

### Option 1: HashiCorp Vault (Self-Hosted / Cloud)

**Best for**: On-premise deployments, multi-cloud environments

```python
# settings/secrets_vault.py
import hvac

def get_vault_client():
    """Initialize Vault client."""
    client = hvac.Client(
        url=os.environ.get('VAULT_ADDR', 'http://127.0.0.1:8200'),
        token=os.environ.get('VAULT_TOKEN')
    )
    return client

def get_secret(path: str, key: str) -> str:
    """Retrieve secret from Vault."""
    client = get_vault_client()
    secret = client.secrets.kv.v2.read_secret_version(path=path)
    return secret['data']['data'][key]

# Usage in settings
SECRET_KEY = get_secret('gaara-erp/django', 'secret_key')
```

**Setup Requirements**:
```bash
# Install Vault client
pip install hvac

# Set environment variables (only these, not actual secrets!)
export VAULT_ADDR=https://vault.example.com
export VAULT_TOKEN=s.xxxxxxxxxxxx
```

### Option 2: AWS Secrets Manager

**Best for**: AWS-hosted deployments

```python
# settings/secrets_aws.py
import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name: str, region_name: str = "us-east-1") -> dict:
    """Retrieve secret from AWS Secrets Manager."""
    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise e

# Usage in settings
secrets = get_secret('gaara-erp/production')
SECRET_KEY = secrets['django_secret_key']
DB_PASSWORD = secrets['db_password']
```

**Setup Requirements**:
```bash
# Install AWS SDK
pip install boto3

# Configure AWS credentials (use IAM roles in production)
export AWS_ACCESS_KEY_ID=xxxx
export AWS_SECRET_ACCESS_KEY=xxxx
```

### Option 3: Azure Key Vault

**Best for**: Azure-hosted deployments

```python
# settings/secrets_azure.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_azure_secret(vault_url: str, secret_name: str) -> str:
    """Retrieve secret from Azure Key Vault."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value

# Usage in settings
VAULT_URL = os.environ.get('AZURE_VAULT_URL')
SECRET_KEY = get_azure_secret(VAULT_URL, 'django-secret-key')
```

**Setup Requirements**:
```bash
# Install Azure SDK
pip install azure-identity azure-keyvault-secrets

# Configure Azure credentials
export AZURE_VAULT_URL=https://gaara-erp-vault.vault.azure.net/
```

### Option 4: Google Secret Manager

**Best for**: GCP-hosted deployments

```python
# settings/secrets_gcp.py
from google.cloud import secretmanager

def get_gcp_secret(project_id: str, secret_id: str, version: str = "latest") -> str:
    """Retrieve secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage in settings
PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
SECRET_KEY = get_gcp_secret(PROJECT_ID, 'django-secret-key')
```

---

## Recommended Environment Configuration

### Development Environment
```bash
# .env.development (gitignored)
SECRET_KEY=dev-random-key-generated-by-django
DB_PASSWORD=local_dev_password
OPENAI_API_KEY=sk-test-key
```

### Production Environment
```bash
# .env.production (minimal - only vault connection info)
VAULT_ADDR=https://vault.production.example.com
VAULT_ROLE_ID=xxxx
VAULT_SECRET_ID=xxxx
# OR for AWS
AWS_SECRETS_REGION=us-east-1
AWS_SECRETS_NAME=gaara-erp/production
```

---

## Migration Checklist

- [ ] Choose secret manager based on cloud provider
- [ ] Install required SDK packages
- [ ] Create secrets in chosen manager
- [ ] Update settings.py to use secret manager client
- [ ] Remove secrets from .env files
- [ ] Update deployment scripts
- [ ] Test secret rotation capability
- [ ] Document recovery procedures

---

## Security Best Practices

1. **Never commit secrets** - Use `.gitignore` for all `.env` files
2. **Rotate secrets regularly** - Automate rotation where possible
3. **Use IAM roles** - Avoid long-lived access keys
4. **Audit access** - Enable logging on secret access
5. **Encrypt in transit** - Use TLS for all secret manager connections
6. **Least privilege** - Grant minimum required permissions

---

## Emergency Procedures

### If secrets are leaked:
1. **Immediately** rotate all potentially exposed secrets
2. Revoke any exposed API keys
3. Review access logs for unauthorized usage
4. Update all deployment environments
5. Notify security team and document incident

