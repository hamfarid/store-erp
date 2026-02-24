#!/usr/bin/env python3
"""
Secret Rotation Script for Vault

This script rotates application secrets in HashiCorp Vault.
It supports:
- Rotating Flask secret key
- Rotating JWT secret
- Rotating database credentials
- Logging all rotations
- Backup of old secrets

Usage:
    python rotate_secrets.py --secret flask --field secret_key
    python rotate_secrets.py --all
    python rotate_secrets.py --backup

Author: Store ERP Team
Date: 2025-11-06
Part of: T21 - KMS/Vault Integration
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import secrets
import string

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from src.vault_client import VaultClient
    VAULT_AVAILABLE = True
except ImportError:
    VAULT_AVAILABLE = False
    print("ERROR: Vault client not available. Install hvac: pip install hvac==2.1.0")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/secret_rotation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SecretRotator:
    """Manages secret rotation in Vault."""
    
    def __init__(self, vault_url: Optional[str] = None, vault_token: Optional[str] = None):
        """Initialize secret rotator."""
        self.vault = VaultClient(vault_url=vault_url, vault_token=vault_token)
        self.backup_dir = Path('backups/secrets')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.vault.authenticated:
            logger.error("Vault not authenticated - cannot proceed")
            raise RuntimeError("Vault authentication failed")
    
    def generate_secret(self, length: int = 32) -> str:
        """
        Generate a cryptographically secure random secret.
        
        Args:
            length: Length of secret (default: 32)
        
        Returns:
            Random secret string
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def backup_secret(self, path: str, data: Dict[str, Any]) -> str:
        """
        Backup secret before rotation.
        
        Args:
            path: Secret path
            data: Secret data
        
        Returns:
            Backup file path
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f"{path.replace('/', '_')}_{timestamp}.json"
        
        backup_data = {
            'path': path,
            'timestamp': timestamp,
            'data': data
        }
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        logger.info(f"Backed up secret to: {backup_file}")
        return str(backup_file)
    
    def rotate_flask_secret(self) -> bool:
        """Rotate Flask secret key."""
        logger.info("Rotating Flask secret key...")
        
        try:
            # Get current secret
            current = self.vault.get_secret('flask', use_cache=False)
            if not current:
                logger.error("Flask secret not found in Vault")
                return False
            
            # Backup current secret
            self.backup_secret('flask', current)
            
            # Generate new secret
            new_secret = self.generate_secret(32)
            
            # Rotate
            success = self.vault.rotate_secret('flask', 'secret_key', new_secret)
            
            if success:
                logger.info("✅ Flask secret key rotated successfully")
                logger.info(f"   New secret: {new_secret[:8]}...***")
                return True
            else:
                logger.error("Failed to rotate Flask secret key")
                return False
        
        except Exception as e:
            logger.error(f"Error rotating Flask secret: {e}")
            return False
    
    def rotate_jwt_secret(self) -> bool:
        """Rotate JWT secret."""
        logger.info("Rotating JWT secret...")
        
        try:
            # Get current secret
            current = self.vault.get_secret('jwt', use_cache=False)
            if not current:
                logger.error("JWT secret not found in Vault")
                return False
            
            # Backup current secret
            self.backup_secret('jwt', current)
            
            # Generate new secret
            new_secret = self.generate_secret(32)
            
            # Rotate
            success = self.vault.rotate_secret('jwt', 'secret_key', new_secret)
            
            if success:
                logger.info("✅ JWT secret rotated successfully")
                logger.info(f"   New secret: {new_secret[:8]}...***")
                return True
            else:
                logger.error("Failed to rotate JWT secret")
                return False
        
        except Exception as e:
            logger.error(f"Error rotating JWT secret: {e}")
            return False
    
    def rotate_database_password(self) -> bool:
        """Rotate database password."""
        logger.info("Rotating database password...")
        
        try:
            # Get current credentials
            current = self.vault.get_secret('database', use_cache=False)
            if not current:
                logger.error("Database credentials not found in Vault")
                return False
            
            # Backup current credentials
            self.backup_secret('database', current)
            
            # Generate new password
            new_password = self.generate_secret(24)
            
            # Rotate
            success = self.vault.rotate_secret('database', 'password', new_password)
            
            if success:
                logger.info("✅ Database password rotated successfully")
                logger.info(f"   New password: {new_password[:8]}...***")
                logger.warning("⚠️  Remember to update database user password!")
                return True
            else:
                logger.error("Failed to rotate database password")
                return False
        
        except Exception as e:
            logger.error(f"Error rotating database password: {e}")
            return False
    
    def rotate_all_secrets(self) -> bool:
        """Rotate all secrets."""
        logger.info("=" * 60)
        logger.info("Starting full secret rotation...")
        logger.info("=" * 60)
        
        results = {
            'flask': self.rotate_flask_secret(),
            'jwt': self.rotate_jwt_secret(),
            'database': self.rotate_database_password()
        }
        
        logger.info("=" * 60)
        logger.info("Secret rotation summary:")
        for secret, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            logger.info(f"  {secret}: {status}")
        logger.info("=" * 60)
        
        return all(results.values())
    
    def list_backups(self) -> None:
        """List all secret backups."""
        logger.info("Secret backups:")
        
        if not self.backup_dir.exists():
            logger.info("  No backups found")
            return
        
        backups = sorted(self.backup_dir.glob('*.json'))
        for backup in backups:
            logger.info(f"  - {backup.name}")
    
    def restore_secret(self, backup_file: str) -> bool:
        """
        Restore secret from backup.
        
        Args:
            backup_file: Path to backup file
        
        Returns:
            True if successful
        """
        logger.info(f"Restoring secret from: {backup_file}")
        
        try:
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            path = backup_data['path']
            data = backup_data['data']
            
            success = self.vault.set_secret(path, data)
            
            if success:
                logger.info(f"✅ Secret restored: {path}")
                return True
            else:
                logger.error(f"Failed to restore secret: {path}")
                return False
        
        except Exception as e:
            logger.error(f"Error restoring secret: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Rotate application secrets in Vault'
    )
    
    parser.add_argument(
        '--secret',
        choices=['flask', 'jwt', 'database'],
        help='Specific secret to rotate'
    )
    parser.add_argument(
        '--field',
        help='Specific field to rotate (e.g., secret_key, password)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Rotate all secrets'
    )
    parser.add_argument(
        '--list-backups',
        action='store_true',
        help='List all secret backups'
    )
    parser.add_argument(
        '--restore',
        help='Restore secret from backup file'
    )
    parser.add_argument(
        '--vault-url',
        default=os.getenv('VAULT_ADDR'),
        help='Vault server URL'
    )
    parser.add_argument(
        '--vault-token',
        default=os.getenv('VAULT_TOKEN'),
        help='Vault authentication token'
    )
    
    args = parser.parse_args()
    
    try:
        rotator = SecretRotator(args.vault_url, args.vault_token)
        
        if args.list_backups:
            rotator.list_backups()
        elif args.restore:
            rotator.restore_secret(args.restore)
        elif args.all:
            rotator.rotate_all_secrets()
        elif args.secret:
            if args.secret == 'flask':
                rotator.rotate_flask_secret()
            elif args.secret == 'jwt':
                rotator.rotate_jwt_secret()
            elif args.secret == 'database':
                rotator.rotate_database_password()
        else:
            parser.print_help()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

