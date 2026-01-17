#!/usr/bin/env python3
"""
Environment Configuration Validator for Gaara ERP v12
======================================================

This script validates that all required environment variables are set
and meet security requirements.

Usage:
    python scripts/validate_env.py
    python scripts/validate_env.py --strict  # Production mode
    python scripts/validate_env.py --env-file .env.production
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import List, Tuple, Dict


# Configuration
REQUIRED_VARS = [
    'SECRET_KEY',
    'JWT_SECRET_KEY',
    'JWT_REFRESH_SECRET_KEY',
    'DATABASE_URL',
]

RECOMMENDED_VARS = [
    'REDIS_URL',
    'CELERY_BROKER_URL',
    'FLASK_ENV',
]

MIN_SECRET_LENGTH = 32
WEAK_SECRET_PATTERNS = [
    'change_me',
    'changeme',
    'password',
    '12345',
    'secret',
    'test',
    'dev',
    'demo',
]


class ValidationResult:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.passed = 0
        self.failed = 0


def load_env_file(env_file: str = '.env') -> Dict[str, str]:
    """Load environment variables from .env file."""
    env_vars = {}
    env_path = Path(env_file)
    
    if not env_path.exists():
        return env_vars
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars


def validate_secret_strength(value: str, var_name: str) -> List[str]:
    """Validate secret strength and return list of issues."""
    issues = []
    
    # Check length
    if len(value) < MIN_SECRET_LENGTH:
        issues.append(f"Too short ({len(value)} chars, need {MIN_SECRET_LENGTH}+)")
    
    # Check for weak patterns
    value_lower = value.lower()
    for pattern in WEAK_SECRET_PATTERNS:
        if pattern in value_lower:
            issues.append(f"Contains weak pattern: '{pattern}'")
    
    # Check entropy (simple heuristic)
    unique_chars = len(set(value))
    if unique_chars < 10:
        issues.append(f"Low entropy (only {unique_chars} unique characters)")
    
    # Check if it's all same character
    if len(set(value)) == 1:
        issues.append("All characters are the same")
    
    # Check if it's sequential
    if len(value) >= 8:
        if value[:8] == "12345678" or value[:8] == "abcdefgh":
            issues.append("Contains sequential pattern")
    
    return issues


def validate_environment(env_vars: Dict[str, str], strict: bool = False) -> ValidationResult:
    """Validate environment configuration."""
    result = ValidationResult()
    
    print("=" * 80)
    print("🔍 GAARA ERP v12 - Environment Validation")
    print("=" * 80)
    print(f"Mode: {'STRICT (Production)' if strict else 'NORMAL (Development)'}")
    print(f"Variables loaded: {len(env_vars)}")
    print("=" * 80)
    print()
    
    # Check required variables
    print("📋 Checking REQUIRED variables...")
    print("-" * 80)
    
    for var in REQUIRED_VARS:
        value = env_vars.get(var) or os.getenv(var)
        
        if not value:
            result.errors.append(f"Missing required variable: {var}")
            result.failed += 1
            print(f"❌ {var}: MISSING")
        else:
            # Validate secrets
            if 'KEY' in var or 'SECRET' in var:
                issues = validate_secret_strength(value, var)
                if issues:
                    for issue in issues:
                        result.warnings.append(f"{var}: {issue}")
                    print(f"⚠️  {var}: SET but {', '.join(issues)}")
                else:
                    result.passed += 1
                    print(f"✅ {var}: VALID ({len(value)} chars)")
            else:
                result.passed += 1
                # Mask sensitive values
                display_value = value[:10] + "..." if len(value) > 10 else value
                print(f"✅ {var}: SET ({display_value})")
    
    print()
    
    # Check recommended variables
    print("📋 Checking RECOMMENDED variables...")
    print("-" * 80)
    
    for var in RECOMMENDED_VARS:
        value = env_vars.get(var) or os.getenv(var)
        
        if not value:
            result.warnings.append(f"Missing recommended variable: {var}")
            print(f"⚠️  {var}: NOT SET (recommended)")
        else:
            result.info.append(f"{var} is set")
            print(f"✅ {var}: SET")
    
    print()
    
    # Production-specific checks
    if strict:
        print("🔒 STRICT MODE: Production Security Checks...")
        print("-" * 80)
        
        # DEBUG must be False
        debug = env_vars.get('DEBUG') or os.getenv('DEBUG', 'True')
        if debug.lower() in ['true', '1', 'yes']:
            result.errors.append("DEBUG must be False in production")
            print("❌ DEBUG: Must be False in production")
        else:
            print("✅ DEBUG: False (correct for production)")
        
        # FLASK_ENV must be production
        flask_env = env_vars.get('FLASK_ENV') or os.getenv('FLASK_ENV', 'development')
        if flask_env != 'production':
            result.errors.append("FLASK_ENV must be 'production'")
            print(f"❌ FLASK_ENV: '{flask_env}' (should be 'production')")
        else:
            print("✅ FLASK_ENV: production")
        
        # Database should be PostgreSQL
        db_url = env_vars.get('DATABASE_URL') or os.getenv('DATABASE_URL', '')
        if 'sqlite' in db_url.lower():
            result.warnings.append("Using SQLite in production (PostgreSQL recommended)")
            print("⚠️  DATABASE_URL: SQLite (PostgreSQL recommended for production)")
        elif 'postgresql' in db_url.lower():
            print("✅ DATABASE_URL: PostgreSQL")
        
        # SESSION_COOKIE_SECURE should be True
        secure_cookie = env_vars.get('SESSION_COOKIE_SECURE') or os.getenv('SESSION_COOKIE_SECURE', 'False')
        if secure_cookie.lower() not in ['true', '1', 'yes']:
            result.warnings.append("SESSION_COOKIE_SECURE should be True in production")
            print("⚠️  SESSION_COOKIE_SECURE: Should be True for HTTPS")
        else:
            print("✅ SESSION_COOKIE_SECURE: True")
        
        # API docs should be disabled
        api_docs = env_vars.get('ENABLE_API_DOCS') or os.getenv('ENABLE_API_DOCS', 'True')
        if api_docs.lower() in ['true', '1', 'yes']:
            result.warnings.append("API docs should be disabled in production")
            print("⚠️  ENABLE_API_DOCS: Should be False in production")
        
        print()
    
    # Summary
    print("=" * 80)
    print("📊 VALIDATION SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {result.passed}")
    print(f"❌ Errors: {len(result.errors)}")
    print(f"⚠️  Warnings: {len(result.warnings)}")
    print()
    
    if result.errors:
        print("❌ ERRORS:")
        for error in result.errors:
            print(f"   - {error}")
        print()
    
    if result.warnings:
        print("⚠️  WARNINGS:")
        for warning in result.warnings:
            print(f"   - {warning}")
        print()
    
    # Determine overall result
    if result.errors:
        print("=" * 80)
        print("❌ VALIDATION FAILED")
        print("=" * 80)
        print("Fix all errors before deploying to production.")
        print()
        return result
    
    if strict and result.warnings:
        print("=" * 80)
        print("⚠️  VALIDATION PASSED WITH WARNINGS")
        print("=" * 80)
        print("Review warnings before deploying to production.")
        print()
        return result
    
    print("=" * 80)
    print("✅ VALIDATION PASSED")
    print("=" * 80)
    print("Environment configuration is valid!")
    print()
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Validate Gaara ERP v12 environment configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate default .env file (development mode)
  python scripts/validate_env.py
  
  # Validate with strict production checks
  python scripts/validate_env.py --strict
  
  # Validate specific .env file
  python scripts/validate_env.py --env-file .env.production --strict
        """
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Enable strict validation for production'
    )
    
    parser.add_argument(
        '--env-file',
        default='.env',
        help='Path to .env file (default: .env)'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    env_vars = load_env_file(args.env_file)
    
    if not env_vars and not os.getenv('SECRET_KEY'):
        print(f"⚠️  Warning: No .env file found at '{args.env_file}'", file=sys.stderr)
        print("   Checking system environment variables...", file=sys.stderr)
        print()
    
    # Validate
    result = validate_environment(env_vars, strict=args.strict)
    
    # Exit with appropriate code
    if result.errors:
        sys.exit(1)
    elif args.strict and result.warnings:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
