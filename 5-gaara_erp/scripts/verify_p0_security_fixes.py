#!/usr/bin/env python3
# FILE: scripts/verify_p0_security_fixes.py | PURPOSE: Verify all P0 security fixes | OWNER: Security Team | LAST-AUDITED: 2025-11-18

"""
P0 Security Fixes Verification Script

This script verifies that all P0 security fixes have been properly implemented:
1. No hardcoded secrets
2. JWT configuration consolidated (15 min access, 7 day refresh)
3. Account lockout logic active (5 attempts, 15 min lock)
4. HTTPS enforced in production
5. All security middleware active

Usage:
    python scripts/verify_p0_security_fixes.py
"""

import os
import sys
import re
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def check_hardcoded_secrets():
    """Check for hardcoded secrets in codebase."""
    print("\n" + "="*80)
    print("FIX #1: Checking for hardcoded secrets...")
    print("="*80)
    
    patterns = [
        (r'"secret_key"', 'Hardcoded "secret_key" found'),
        (r'SECRET_KEY\s*=\s*["\'][^"\']+["\']', 'Hardcoded SECRET_KEY with default value'),
        (r'password\s*=\s*["\']admin["\']', 'Hardcoded admin password'),
    ]
    
    issues = []
    for root, dirs, files in os.walk(PROJECT_ROOT / 'gaara_erp'):
        # Skip migrations, __pycache__, etc.
        dirs[:] = [d for d in dirs if d not in ['migrations', '__pycache__', '.git', 'node_modules']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = Path(root) / file
                try:
                    content = filepath.read_text(encoding='utf-8')
                    for pattern, message in patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            # Exclude .env.example and comments
                            if '.env.example' not in str(filepath) and not re.search(r'#.*' + pattern, content):
                                issues.append(f"{filepath}: {message}")
                except Exception as e:
                    pass
    
    if issues:
        print(f"{RED}✗ FAILED: Found {len(issues)} hardcoded secrets{RESET}")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"{GREEN}✓ PASSED: No hardcoded secrets found{RESET}")
        return True


def check_jwt_configuration():
    """Check JWT configuration is consolidated and correct."""
    print("\n" + "="*80)
    print("FIX #2: Checking JWT configuration...")
    print("="*80)
    
    security_file = PROJECT_ROOT / 'gaara_erp' / 'gaara_erp' / 'settings' / 'security.py'
    
    if not security_file.exists():
        print(f"{RED}✗ FAILED: security.py not found{RESET}")
        return False
    
    content = security_file.read_text(encoding='utf-8')
    
    checks = [
        (r"'ACCESS_TOKEN_LIFETIME':\s*timedelta\(minutes=15\)", "15-minute access token"),
        (r"'REFRESH_TOKEN_LIFETIME':\s*timedelta\(days=7\)", "7-day refresh token"),
        (r"'ROTATE_REFRESH_TOKENS':\s*True", "Refresh token rotation enabled"),
        (r"'BLACKLIST_AFTER_ROTATION':\s*True", "Token blacklisting enabled"),
    ]
    
    passed = True
    for pattern, description in checks:
        if re.search(pattern, content):
            print(f"{GREEN}✓ {description}{RESET}")
        else:
            print(f"{RED}✗ {description} NOT FOUND{RESET}")
            passed = False
    
    return passed


def check_account_lockout():
    """Check account lockout logic is implemented."""
    print("\n" + "="*80)
    print("FIX #3: Checking account lockout logic...")
    print("="*80)
    
    models_file = PROJECT_ROOT / 'gaara_erp' / 'core_modules' / 'users' / 'models.py'
    
    if not models_file.exists():
        print(f"{RED}✗ FAILED: users/models.py not found{RESET}")
        return False
    
    content = models_file.read_text(encoding='utf-8')
    
    checks = [
        (r'failed_login_attempts\s*=\s*models\.PositiveIntegerField', "failed_login_attempts field"),
        (r'account_locked_until\s*=\s*models\.DateTimeField', "account_locked_until field"),
        (r'def lock_account\(self,\s*duration_minutes=15\)', "lock_account method (15 min default)"),
        (r'def is_account_locked\(self\)', "is_account_locked method"),
        (r'def increment_failed_login\(self\)', "increment_failed_login method"),
        (r'if self\.failed_login_attempts >= 5:', "5 failed attempts threshold"),
    ]
    
    passed = True
    for pattern, description in checks:
        if re.search(pattern, content):
            print(f"{GREEN}✓ {description}{RESET}")
        else:
            print(f"{RED}✗ {description} NOT FOUND{RESET}")
            passed = False
    
    return passed


def check_https_enforcement():
    """Check HTTPS is enforced in production."""
    print("\n" + "="*80)
    print("FIX #4: Checking HTTPS enforcement...")
    print("="*80)
    
    prod_file = PROJECT_ROOT / 'gaara_erp' / 'gaara_erp' / 'settings' / 'prod.py'
    
    if not prod_file.exists():
        print(f"{RED}✗ FAILED: prod.py not found{RESET}")
        return False
    
    content = prod_file.read_text(encoding='utf-8')
    
    checks = [
        (r'SECURE_SSL_REDIRECT\s*=\s*True', "HTTPS redirect enabled"),
        (r'SESSION_COOKIE_SECURE\s*=\s*True', "Secure session cookies"),
        (r'CSRF_COOKIE_SECURE\s*=\s*True', "Secure CSRF cookies"),
        (r'SECURE_HSTS_SECONDS\s*=\s*31536000', "HSTS enabled (1 year)"),
    ]
    
    passed = True
    for pattern, description in checks:
        if re.search(pattern, content):
            print(f"{GREEN}✓ {description}{RESET}")
        else:
            print(f"{RED}✗ {description} NOT FOUND{RESET}")
            passed = False
    
    return passed


def check_middleware_configuration():
    """Check all security middleware is active."""
    print("\n" + "="*80)
    print("FIX #5: Checking middleware configuration...")
    print("="*80)
    
    base_file = PROJECT_ROOT / 'gaara_erp' / 'gaara_erp' / 'settings' / 'base.py'
    
    if not base_file.exists():
        print(f"{RED}✗ FAILED: base.py not found{RESET}")
        return False
    
    content = base_file.read_text(encoding='utf-8')
    
    middleware_checks = [
        ('django.middleware.security.SecurityMiddleware', "Django SecurityMiddleware"),
        ('gaara_erp.middleware.security_headers.SecurityHeadersMiddleware', "SecurityHeadersMiddleware"),
        ('django.middleware.csrf.CsrfViewMiddleware', "CSRF middleware"),
        ('core_modules.security.middleware.SecurityMiddleware', "Custom SecurityMiddleware"),
        ('core_modules.security.middleware.RateLimitMiddleware', "RateLimitMiddleware"),
    ]
    
    passed = True
    for middleware, description in middleware_checks:
        if middleware in content:
            print(f"{GREEN}✓ {description}{RESET}")
        else:
            print(f"{RED}✗ {description} NOT FOUND{RESET}")
            passed = False
    
    return passed


def main():
    """Run all verification checks."""
    print("\n" + "="*80)
    print("P0 SECURITY FIXES VERIFICATION")
    print("="*80)
    print(f"Project: Gaara ERP v12")
    print(f"Date: 2025-11-18")
    print("="*80)
    
    results = {
        "Fix #1: Remove Hardcoded Secrets": check_hardcoded_secrets(),
        "Fix #2: Consolidate JWT Configuration": check_jwt_configuration(),
        "Fix #3: Account Lockout Logic": check_account_lockout(),
        "Fix #4: Force HTTPS in Production": check_https_enforcement(),
        "Fix #5: Verify Middleware Configuration": check_middleware_configuration(),
    }
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    passed = sum(results.values())
    total = len(results)
    
    for fix, result in results.items():
        status = f"{GREEN}✓ PASSED{RESET}" if result else f"{RED}✗ FAILED{RESET}"
        print(f"{fix}: {status}")
    
    print("="*80)
    print(f"Total: {passed}/{total} fixes verified")
    
    if passed == total:
        print(f"{GREEN}✓ ALL P0 SECURITY FIXES VERIFIED{RESET}")
        return 0
    else:
        print(f"{RED}✗ SOME FIXES FAILED VERIFICATION{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

