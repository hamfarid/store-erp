#!/usr/bin/env python3
"""
Automated Environment Setup for Gaara ERP v12
==============================================

This script automatically sets up environment configuration files
with secure, randomly generated secrets.

Usage:
    python scripts/setup_env.py                    # Development setup
    python scripts/setup_env.py --environment staging
    python scripts/setup_env.py --environment production
"""

import os
import sys
import secrets
import argparse
from pathlib import Path
from datetime import datetime


def generate_secret(length=32):
    """Generate cryptographically secure random secret."""
    return secrets.token_hex(length)


def create_development_env():
    """Create development .env file with secure defaults."""
    env_content = f"""# =============================================================================
# GAARA ERP v12 - Development Environment (Auto-Generated)
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# =============================================================================

# =============================================================================
# 🔴 REQUIRED - Auto-Generated Secrets
# =============================================================================

SECRET_KEY={generate_secret(32)}
JWT_SECRET_KEY={generate_secret(32)}
JWT_REFRESH_SECRET_KEY={generate_secret(32)}
DATABASE_URL=sqlite:///instance/gaara_erp_dev.db

# =============================================================================
# 🟠 RECOMMENDED - Development Defaults
# =============================================================================

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
FLASK_ENV=development
DEBUG=True

# =============================================================================
# 🔒 SECURITY - Development Settings
# =============================================================================

JWT_ACCESS_TOKEN_EXPIRES_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7
RATELIMIT_ENABLED=True
RATELIMIT_DEFAULT=60 per minute
CORS_ORIGINS=http://localhost:5501,http://localhost:3000

# =============================================================================
# 🌐 PORTS - Development
# =============================================================================

BACKEND_PORT=5001
FRONTEND_PORT=5501
ML_PORT=5101
AI_PORT=5601

# =============================================================================
# 🤖 AI SERVICES (OPTIONAL) - Add your keys here
# =============================================================================

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
PYBROPS_API_KEY=

# =============================================================================
# 📧 EMAIL (OPTIONAL) - Add your SMTP settings
# =============================================================================

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=
MAIL_PASSWORD=

# =============================================================================
# 📊 LOGGING - Development
# =============================================================================

LOG_LEVEL=DEBUG
LOG_FILE=logs/gaara_erp_dev.log

# =============================================================================
# 🔧 FEATURES - Development
# =============================================================================

ENABLE_MFA=False
ENABLE_API_DOCS=True
ENABLE_SWAGGER=True
ENABLE_AUDIT_LOGGING=True

# =============================================================================
# END OF DEVELOPMENT CONFIGURATION
# =============================================================================
"""
    return env_content


def create_production_env():
    """Create production .env template with placeholders."""
    env_content = f"""# =============================================================================
# GAARA ERP v12 - Production Environment Template
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# =============================================================================
#
# ⚠️ CRITICAL: Replace all CHANGE_ME values before deployment ⚠️
#
# Production secrets should be loaded from Vault/KMS, not this file.
# This file serves as a template and should not contain real production secrets.
#
# =============================================================================

# =============================================================================
# 🔴 REQUIRED - MUST BE SET
# =============================================================================

SECRET_KEY=CHANGE_ME_PROD_SECRET_{generate_secret(16)}
JWT_SECRET_KEY=CHANGE_ME_PROD_JWT_{generate_secret(16)}
JWT_REFRESH_SECRET_KEY=CHANGE_ME_PROD_REFRESH_{generate_secret(16)}
DATABASE_URL=postgresql://gaara_prod:CHANGE_ME@db-prod:10502/gaara_erp_prod

# =============================================================================
# 🟠 PRODUCTION REQUIRED
# =============================================================================

REDIS_URL=redis://redis-prod:6375/0
CELERY_BROKER_URL=redis://redis-prod:6375/0
FLASK_ENV=production
DEBUG=False

# =============================================================================
# 🔒 PRODUCTION SECURITY
# =============================================================================

JWT_ACCESS_TOKEN_EXPIRES_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7
RATELIMIT_ENABLED=True
RATELIMIT_DEFAULT=30 per minute
CORS_ORIGINS=https://erp.company.com
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# =============================================================================
# 🤖 AI SERVICES - Production Keys
# =============================================================================

OPENAI_API_KEY=CHANGE_ME
ANTHROPIC_API_KEY=CHANGE_ME
PYBROPS_API_KEY=CHANGE_ME

# =============================================================================
# 📊 PRODUCTION MONITORING
# =============================================================================

LOG_LEVEL=WARNING
SENTRY_DSN=CHANGE_ME
PROMETHEUS_ENABLED=True

# =============================================================================
# 🔧 PRODUCTION FEATURES
# =============================================================================

ENABLE_MFA=True
ENABLE_API_DOCS=False
ENABLE_SWAGGER=False
ENABLE_AUDIT_LOGGING=True

# =============================================================================
# END OF PRODUCTION TEMPLATE
# =============================================================================
"""
    return env_content


def setup_frontend_env(environment='development'):
    """Create frontend .env file."""
    if environment == 'development':
        api_url = 'http://localhost:5001'
        app_env = 'development'
        enable_mfa = 'false'
        sentry_dsn = ''
    elif environment == 'staging':
        api_url = 'https://staging-api.gaara-erp.com'
        app_env = 'staging'
        enable_mfa = 'true'
        sentry_dsn = 'https://staging@sentry.io/project'
    else:  # production
        api_url = 'https://api.gaara-erp.com'
        app_env = 'production'
        enable_mfa = 'true'
        sentry_dsn = 'CHANGE_ME_PROD_SENTRY_DSN'
    
    env_content = f"""# =============================================================================
# GAARA ERP v12 - Frontend {environment.title()} Environment
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# =============================================================================

VITE_API_BASE_URL={api_url}
VITE_APP_ENV={app_env}
VITE_APP_TITLE=Gaara ERP v12
VITE_DEFAULT_LANGUAGE=ar
VITE_DEFAULT_CURRENCY=SAR
VITE_ENABLE_MFA={enable_mfa}
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_RTL=true
VITE_ENABLE_PWA={('true' if environment == 'production' else 'false')}
VITE_SESSION_TIMEOUT=30
VITE_IDLE_TIMEOUT=15
VITE_SENTRY_DSN={sentry_dsn}
"""
    return env_content


def main():
    parser = argparse.ArgumentParser(
        description='Automated environment setup for Gaara ERP v12',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--environment',
        choices=['development', 'staging', 'production'],
        default='development',
        help='Environment to set up (default: development)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing .env file'
    )
    
    parser.add_argument(
        '--backend-only',
        action='store_true',
        help='Set up backend only'
    )
    
    parser.add_argument(
        '--frontend-only',
        action='store_true',
        help='Set up frontend only'
    )
    
    args = parser.parse_args()
    
    backend_dir = Path('.').resolve()
    frontend_dir = backend_dir.parent / 'frontend'
    
    print("=" * 80)
    print("🚀 GAARA ERP v12 - Automated Environment Setup")
    print("=" * 80)
    print(f"Environment: {args.environment.upper()}")
    print(f"Backend: {backend_dir}")
    print(f"Frontend: {frontend_dir}")
    print("=" * 80)
    print()
    
    # Setup backend
    if not args.frontend_only:
        backend_env = backend_dir / '.env'
        
        if backend_env.exists() and not args.force:
            print(f"⚠️  Backend .env already exists: {backend_env}")
            print("   Use --force to overwrite")
        else:
            if args.environment == 'development':
                content = create_development_env()
            else:
                content = create_production_env()
            
            backend_env.write_text(content, encoding='utf-8')
            print(f"✅ Created backend .env: {backend_env}")
            print(f"   ({len(content.splitlines())} lines)")
    
    # Setup frontend
    if not args.backend_only and frontend_dir.exists():
        frontend_env = frontend_dir / '.env'
        
        if frontend_env.exists() and not args.force:
            print(f"⚠️  Frontend .env already exists: {frontend_env}")
            print("   Use --force to overwrite")
        else:
            content = setup_frontend_env(args.environment)
            frontend_env.write_text(content, encoding='utf-8')
            print(f"✅ Created frontend .env: {frontend_env}")
            print(f"   ({len(content.splitlines())} lines)")
    
    print()
    print("=" * 80)
    print("✅ SETUP COMPLETE")
    print("=" * 80)
    print()
    
    # Next steps
    print("📋 Next Steps:")
    print()
    
    if args.environment == 'development':
        print("1. Edit .env files to add optional API keys (OpenAI, etc.)")
        print("2. Run validation: python scripts/validate_env.py")
        print("3. Start backend: python src/main.py")
        print("4. Start frontend: cd ../frontend && npm run dev")
    else:
        print("1. Replace all CHANGE_ME values in .env files")
        print("2. Configure secrets in Vault/KMS")
        print("3. Run strict validation: python scripts/validate_env.py --strict")
        print("4. Review ENVIRONMENT_SETUP_GUIDE.md")
        print("5. Complete production deployment checklist")
    
    print()


if __name__ == '__main__':
    main()
