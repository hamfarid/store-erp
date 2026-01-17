#!/usr/bin/env python3
"""
Generate Secure Secrets for Gaara ERP v12
==========================================

This script generates cryptographically secure random secrets for use in .env files.

Usage:
    python scripts/generate_secrets.py
    python scripts/generate_secrets.py --length 64
    python scripts/generate_secrets.py --format env > .env.secrets
"""

import secrets
import string
import argparse
import sys
from datetime import datetime


def generate_secret(length=32):
    """Generate a cryptographically secure random secret."""
    return secrets.token_hex(length)


def generate_password(length=16):
    """Generate a strong password with mixed characters."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_uuid():
    """Generate a UUID v4."""
    return secrets.token_urlsafe(22)


def print_secrets(format_type='human', length=32):
    """Print generated secrets in specified format."""
    
    secrets_data = {
        'SECRET_KEY': generate_secret(length),
        'JWT_SECRET_KEY': generate_secret(length),
        'JWT_REFRESH_SECRET_KEY': generate_secret(length),
    }
    
    if format_type == 'human':
        print("=" * 80)
        print("🔐 GAARA ERP v12 - Generated Secrets")
        print("=" * 80)
        print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Secret length: {length} bytes ({length * 2} hex characters)")
        print("\n⚠️  SECURITY WARNING:")
        print("   - NEVER commit these secrets to version control")
        print("   - Use different secrets for dev/staging/production")
        print("   - Store production secrets in KMS/Vault")
        print("   - Rotate secrets periodically")
        print("\n" + "=" * 80)
        print("\nCopy these values to your .env file:")
        print("=" * 80)
        print()
        
        for key, value in secrets_data.items():
            print(f"{key}={value}")
        
        print()
        print("=" * 80)
        print("\n📋 Additional Random Values:")
        print("=" * 80)
        print(f"\nStrong Password (16 chars): {generate_password(16)}")
        print(f"UUID: {generate_uuid()}")
        print(f"32-byte hex: {secrets.token_hex(32)}")
        print(f"Base64 (32 bytes): {secrets.token_urlsafe(32)}")
        print()
        
    elif format_type == 'env':
        print("# Generated secrets for .env file")
        print(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        for key, value in secrets_data.items():
            print(f"{key}={value}")
        print()
        
    elif format_type == 'json':
        import json
        secrets_data['_generated'] = datetime.now().isoformat()
        secrets_data['_length'] = length
        print(json.dumps(secrets_data, indent=2))
        
    elif format_type == 'python':
        print("# Generated secrets for Python configuration")
        print(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        for key, value in secrets_data.items():
            print(f"{key} = '{value}'")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Generate secure secrets for Gaara ERP v12',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate secrets with default length (32 bytes)
  python scripts/generate_secrets.py
  
  # Generate longer secrets (64 bytes)
  python scripts/generate_secrets.py --length 64
  
  # Generate in .env format and save to file
  python scripts/generate_secrets.py --format env > .env.secrets
  
  # Generate in JSON format
  python scripts/generate_secrets.py --format json
        """
    )
    
    parser.add_argument(
        '--length',
        type=int,
        default=32,
        help='Length of secrets in bytes (default: 32)'
    )
    
    parser.add_argument(
        '--format',
        choices=['human', 'env', 'json', 'python'],
        default='human',
        help='Output format (default: human)'
    )
    
    args = parser.parse_args()
    
    # Validate length
    if args.length < 16:
        print("❌ Error: Secret length must be at least 16 bytes", file=sys.stderr)
        sys.exit(1)
    
    if args.length > 128:
        print("⚠️  Warning: Secret length > 128 bytes is excessive", file=sys.stderr)
    
    # Generate and print secrets
    print_secrets(args.format, args.length)


if __name__ == '__main__':
    main()
