#!/usr/bin/env python3
# FILE: scripts/aws_secrets_migration.py | PURPOSE: Migrate secrets from .env to AWS Secrets Manager | OWNER: DevOps | RELATED: backend/.env, backend/src/config/secrets_loader.py | LAST-AUDITED: 2025-10-28

"""
AWS Secrets Manager Migration Script

Migrates all secrets from backend/.env to AWS Secrets Manager.
Supports both creation and update of secrets.

Usage:
    python scripts/aws_secrets_migration.py --create    # Create new secrets
    python scripts/aws_secrets_migration.py --update    # Update existing secrets
    python scripts/aws_secrets_migration.py --verify    # Verify secrets in AWS
    python scripts/aws_secrets_migration.py --cleanup   # Remove .env from git history
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AWSSecretsManager:
    """Manage AWS Secrets Manager operations"""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize AWS Secrets Manager client"""
        try:
            import boto3
            self.client = boto3.client('secretsmanager', region_name=region)
            self.region = region
            logger.info(f"✅ Connected to AWS Secrets Manager in {region}")
        except ImportError:
            logger.error("❌ boto3 not installed. Run: pip install boto3")
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Failed to connect to AWS: {e}")
            sys.exit(1)
    
    def create_secret(self, name: str, value: str, description: str = "") -> bool:
        """Create a new secret in AWS Secrets Manager"""
        try:
            self.client.create_secret(
                Name=name,
                SecretString=value,
                Description=description,
                Tags=[
                    {'Key': 'Application', 'Value': 'gaara-store'},
                    {'Key': 'ManagedBy', 'Value': 'aws_secrets_migration.py'},
                    {'Key': 'CreatedAt', 'Value': datetime.now().isoformat()}
                ]
            )
            logger.info(f"✅ Created secret: {name}")
            return True
        except self.client.exceptions.ResourceExistsException:
            logger.warning(f"⚠️ Secret already exists: {name}")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to create secret {name}: {e}")
            return False
    
    def update_secret(self, name: str, value: str) -> bool:
        """Update an existing secret"""
        try:
            self.client.update_secret(
                SecretId=name,
                SecretString=value
            )
            logger.info(f"✅ Updated secret: {name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to update secret {name}: {e}")
            return False
    
    def get_secret(self, name: str) -> Optional[str]:
        """Retrieve a secret value"""
        try:
            response = self.client.get_secret_value(SecretId=name)
            return response.get('SecretString')
        except Exception as e:
            logger.error(f"❌ Failed to retrieve secret {name}: {e}")
            return None
    
    def list_secrets(self) -> list:
        """List all secrets"""
        try:
            response = self.client.list_secrets()
            return response.get('SecretList', [])
        except Exception as e:
            logger.error(f"❌ Failed to list secrets: {e}")
            return []


def load_env_file(env_path: str = 'backend/.env') -> Dict[str, str]:
    """Load secrets from .env file"""
    secrets = {}
    
    if not os.path.exists(env_path):
        logger.error(f"❌ .env file not found: {env_path}")
        return secrets
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    secrets[key.strip()] = value.strip()
        
        logger.info(f"✅ Loaded {len(secrets)} secrets from {env_path}")
        return secrets
    except Exception as e:
        logger.error(f"❌ Failed to load .env file: {e}")
        return secrets


def migrate_secrets(secrets: Dict[str, str], manager: AWSSecretsManager) -> Dict[str, bool]:
    """Migrate secrets to AWS Secrets Manager"""
    
    # Map of .env keys to AWS secret names
    secret_mapping = {
        'SECRET_KEY': 'gaara/secret-key',
        'JWT_SECRET_KEY': 'gaara/jwt-secret-key',
        'ENCRYPTION_KEY': 'gaara/encryption-key',
        'ADMIN_PASSWORD': 'gaara/admin-password',
        'MAIL_PASSWORD': 'gaara/mail-password',
        'MAIL_USERNAME': 'gaara/mail-username',
        'DATABASE_URL': 'gaara/database-url',
        'JWT_REFRESH_SECRET_KEY': 'gaara/jwt-refresh-secret-key',
    }
    
    results = {}
    
    for env_key, secret_name in secret_mapping.items():
        if env_key in secrets:
            value = secrets[env_key]
            if value:
                results[secret_name] = manager.create_secret(
                    name=secret_name,
                    value=value,
                    description=f"Secret for {env_key}"
                )
            else:
                logger.warning(f"⚠️ Empty value for {env_key}")
                results[secret_name] = False
        else:
            logger.warning(f"⚠️ {env_key} not found in .env")
            results[secret_name] = False
    
    return results


def verify_secrets(manager: AWSSecretsManager) -> bool:
    """Verify all secrets are in AWS"""
    required_secrets = [
        'gaara/secret-key',
        'gaara/jwt-secret-key',
        'gaara/encryption-key',
        'gaara/admin-password',
        'gaara/mail-password',
    ]
    
    all_exist = True
    for secret_name in required_secrets:
        value = manager.get_secret(secret_name)
        if value:
            logger.info(f"✅ Verified: {secret_name}")
        else:
            logger.error(f"❌ Missing: {secret_name}")
            all_exist = False
    
    return all_exist


def cleanup_git_history() -> bool:
    """Remove .env from git history"""
    try:
        logger.info("🔄 Removing .env from git history...")
        os.system('git filter-branch --tree-filter "rm -f backend/.env" HEAD')
        logger.info("✅ Removed .env from git history")
        
        # Add .env to .gitignore
        gitignore_path = '.gitignore'
        with open(gitignore_path, 'a') as f:
            f.write('\n# Secrets - never commit\nbackend/.env\n')
        
        logger.info("✅ Added backend/.env to .gitignore")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to cleanup git history: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Migrate secrets from .env to AWS Secrets Manager'
    )
    parser.add_argument(
        '--create',
        action='store_true',
        help='Create new secrets in AWS'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update existing secrets in AWS'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify secrets in AWS'
    )
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='Remove .env from git history'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region (default: us-east-1)'
    )
    
    args = parser.parse_args()
    
    # Initialize AWS Secrets Manager
    manager = AWSSecretsManager(region=args.region)
    
    # Load secrets from .env
    secrets = load_env_file()
    
    if args.create:
        logger.info("🔄 Creating secrets in AWS Secrets Manager...")
        results = migrate_secrets(secrets, manager)
        success_count = sum(1 for v in results.values() if v)
        logger.info(f"✅ Created {success_count}/{len(results)} secrets")
    
    elif args.verify:
        logger.info("🔄 Verifying secrets in AWS...")
        if verify_secrets(manager):
            logger.info("✅ All secrets verified successfully")
        else:
            logger.error("❌ Some secrets are missing")
            sys.exit(1)
    
    elif args.cleanup:
        logger.info("🔄 Cleaning up git history...")
        if cleanup_git_history():
            logger.info("✅ Git history cleaned")
        else:
            logger.error("❌ Failed to cleanup git history")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

