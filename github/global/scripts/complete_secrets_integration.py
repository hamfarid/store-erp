# FILE: scripts/complete_secrets_integration.py | PURPOSE: Complete secrets manager integration for remaining modules | OWNER: Security Team | RELATED: docs/Secrets_Migration_Guide.md | LAST-AUDITED: 2025-10-25

"""
Complete Secrets Manager Integration Script

This script completes the integration of AWS Secrets Manager for remaining modules:
- backend/src/config/production.py - MAIL_PASSWORD
- Any other files using sensitive environment variables

Usage:
    python scripts/complete_secrets_integration.py
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Base directory
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = BASE_DIR / "backend"


def backup_file(filepath: Path) -> Path:
    """Create backup of file before modification"""
    backup_path = filepath.with_suffix(filepath.suffix + '.backup_secrets')
    if not backup_path.exists():
        backup_path.write_text(filepath.read_text(encoding='utf-8'), encoding='utf-8')
        print(f"  ✅ Backup created: {backup_path.name}")
    return backup_path


def update_production_config() -> Tuple[bool, str]:
    """Update backend/src/config/production.py to use secrets manager"""
    filepath = BACKEND_DIR / "src" / "config" / "production.py"
    
    if not filepath.exists():
        return False, f"❌ File not found: {filepath}"
    
    print(f"\n📝 Updating: {filepath.relative_to(BASE_DIR)}")
    
    # Backup
    backup_file(filepath)
    
    # Read content
    content = filepath.read_text(encoding='utf-8')
    
    # Check if already updated
    if 'from src.utils.secrets_manager import get_secret' in content:
        return True, f"✅ {filepath.name}: Already integrated with secrets manager"
    
    # Add import at the top (after existing imports)
    import_pattern = r'(import os\n)'
    import_replacement = r'\1\n# P1.1: Import secrets manager for production secrets\ntry:\n    from src.utils.secrets_manager import get_secret\n    SECRETS_MANAGER_AVAILABLE = True\nexcept ImportError:\n    SECRETS_MANAGER_AVAILABLE = False\n    get_secret = None  # type: ignore\n'
    
    if re.search(import_pattern, content):
        content = re.sub(import_pattern, import_replacement, content, count=1)
    else:
        # Add at the beginning
        content = import_replacement + '\n' + content
    
    # Update MAIL_PASSWORD usage
    mail_password_pattern = r"MAIL_PASSWORD = os\.environ\.get\('MAIL_PASSWORD'\)"
    mail_password_replacement = """# P1.1: Get MAIL_PASSWORD from secrets manager in production
    environment = os.environ.get('ENVIRONMENT', 'development')
    
    if environment == 'production' and SECRETS_MANAGER_AVAILABLE:
        try:
            MAIL_PASSWORD = get_secret('mail-password')
            print("✅ Using MAIL_PASSWORD from AWS Secrets Manager")
        except Exception as e:
            print(f"⚠️  Failed to get MAIL_PASSWORD from Secrets Manager: {e}")
            print("⚠️  Falling back to .env MAIL_PASSWORD")
            MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    else:
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')"""
    
    if re.search(mail_password_pattern, content):
        content = re.sub(mail_password_pattern, mail_password_replacement, content)
    
    # Write updated content
    filepath.write_text(content, encoding='utf-8')
    
    return True, f"✅ {filepath.name}: Updated with secrets manager integration"


def search_for_remaining_secrets() -> List[Tuple[Path, str, int]]:
    """Search for remaining os.getenv() calls with potential secrets"""
    
    print("\n🔍 Searching for remaining secrets in codebase...")
    
    # Patterns to search for
    secret_patterns = [
        r"os\.getenv\(['\"]REDIS_PASSWORD['\"]\)",
        r"os\.getenv\(['\"]SENTRY_DSN['\"]\)",
        r"os\.getenv\(['\"]API_KEY['\"]\)",
        r"os\.getenv\(['\"].*_SECRET['\"]\)",
        r"os\.getenv\(['\"].*_PASSWORD['\"]\)",
        r"os\.getenv\(['\"].*_TOKEN['\"]\)",
    ]
    
    findings = []
    
    # Search in backend/src
    for py_file in (BACKEND_DIR / "src").rglob("*.py"):
        # Skip already integrated files
        if py_file.name in ['database.py', 'auth.py', 'secrets_manager.py', 'encryption.py']:
            continue
        
        try:
            content = py_file.read_text(encoding='utf-8')
            
            for pattern in secret_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    # Get line number
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append((py_file, match.group(), line_num))
        except Exception:
            continue
    
    return findings


def generate_integration_report(findings: List[Tuple[Path, str, int]]) -> str:
    """Generate report of remaining secrets to integrate"""
    
    if not findings:
        return "\n✅ No remaining secrets found that need integration!"
    
    report = "\n📊 Remaining Secrets to Integrate:\n"
    report += "=" * 80 + "\n\n"
    
    # Group by file
    by_file = {}
    for filepath, secret, line_num in findings:
        rel_path = filepath.relative_to(BASE_DIR)
        if rel_path not in by_file:
            by_file[rel_path] = []
        by_file[rel_path].append((secret, line_num))
    
    for filepath, secrets in sorted(by_file.items()):
        report += f"📁 {filepath}\n"
        for secret, line_num in secrets:
            report += f"   Line {line_num}: {secret}\n"
        report += "\n"
    
    report += f"Total: {len(findings)} secrets found in {len(by_file)} files\n"
    report += "=" * 80 + "\n"
    
    return report


def main():
    """Main function"""
    print("=" * 80)
    print("P1.1: Complete Secrets Manager Integration")
    print("=" * 80)
    
    results = []
    
    # 1. Update production.py
    print("\n📝 Step 1: Update production.py")
    success, message = update_production_config()
    results.append((success, message))
    print(message)
    
    # 2. Search for remaining secrets
    print("\n🔍 Step 2: Search for remaining secrets")
    findings = search_for_remaining_secrets()
    report = generate_integration_report(findings)
    print(report)
    
    # 3. Summary
    print("\n" + "=" * 80)
    print("📊 Summary")
    print("=" * 80)
    
    successful = sum(1 for success, _ in results if success)
    total = len(results)
    
    print(f"\n✅ Successfully updated: {successful}/{total} files")
    
    if findings:
        print(f"⚠️  Found {len(findings)} remaining secrets to integrate manually")
        print("\n💡 Next Steps:")
        print("   1. Review the findings above")
        print("   2. Update each file following the pattern in docs/Secrets_Migration_Guide.md")
        print("   3. Test in development environment")
        print("   4. Deploy to production")
    else:
        print("\n🎉 All secrets integrated successfully!")
    
    print("\n" + "=" * 80)
    
    # Save report to file
    report_path = BASE_DIR / "docs" / "Remaining_Secrets_Report.md"

    status = 'Complete' if not findings else 'Pending'
    findings_text = report if findings else '✅ No remaining secrets found!'
    next_steps = '1. Review findings above\n2. Update files manually\n3. Test in development\n4. Deploy to production' if findings else '✅ All secrets integrated! Proceed with AWS setup.'

    report_content = f"""# Remaining Secrets Integration Report

**Generated**: 2025-10-25
**Status**: {status}

## Summary

- **Files Updated**: {successful}/{total}
- **Remaining Secrets**: {len(findings)}

## Findings

{findings_text}

## Next Steps

{next_steps}

---

**See**: docs/Secrets_Migration_Guide.md for migration patterns
"""
    
    report_path.write_text(report_content, encoding='utf-8')
    print(f"\n📄 Report saved to: {report_path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()

