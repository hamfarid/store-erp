# FILE: scripts/fix_hardcoded_passwords.py | PURPOSE: Replace hardcoded passwords with env vars | OWNER: Security Team | RELATED: SECRETS_MANAGEMENT.md | LAST-AUDITED: 2025-12-19
"""
Hardcoded Password Replacement Script
=====================================

CRITICAL SECURITY FIX per GLOBAL_PROFESSIONAL_CORE_PROMPT P0 constraints.

This script:
1. Scans Python files for hardcoded passwords
2. Replaces with environment variable lookups
3. Creates backup of original files
4. Generates report of changes

Usage:
    python scripts/fix_hardcoded_passwords.py --scan        # Scan only
    python scripts/fix_hardcoded_passwords.py --fix         # Apply fixes
    python scripts/fix_hardcoded_passwords.py --fix --dry   # Dry run
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict

# Patterns to detect hardcoded passwords
HARDCODED_PATTERNS = [
    # Direct password assignments
    (r"password\s*=\s*['\"]admin123['\"]",
     "password=os.getenv('TEST_ADMIN_PASSWORD', 'CHANGE_ME_IN_PRODUCTION')"),

    (r"'password':\s*['\"]admin123['\"]",
     "'password': os.getenv('TEST_ADMIN_PASSWORD', 'CHANGE_ME_IN_PRODUCTION')"),

    (r'"password":\s*"admin123"',
     '"password": os.getenv("TEST_ADMIN_PASSWORD", "CHANGE_ME_IN_PRODUCTION")'),

    # set_password calls
    (r"\.set_password\(['\"]admin123['\"]\)",
     ".set_password(os.getenv('ADMIN_PASSWORD', generate_secure_password()))"),

    # generate_password_hash calls
    (r"generate_password_hash\(['\"]admin123['\"]\)",
     "generate_password_hash(os.getenv('ADMIN_PASSWORD', generate_secure_password()))"),

    # SQL INSERT with password
    (r"VALUES\s*\([^)]*['\"]admin123['\"][^)]*\)",
     "# WARNING: Hardcoded password removed - use environment variable"),
]

# Files/directories to skip
SKIP_DIRS = {
    '.venv', 'venv', 'node_modules', '.git', '__pycache__',
    '.mypy_cache', '.pytest_cache', 'dist', 'build',
    'unneeded', 'archive', 'backup'
}

SKIP_FILES = {
    'fix_hardcoded_passwords.py',  # Don't modify self
    'test_password.py',  # Test files that intentionally use weak passwords for testing
    'test_pwd2.py',
}


def find_python_files(root_dir: Path) -> List[Path]:
    """Find all Python files to scan."""
    python_files = []

    for path in root_dir.rglob('*.py'):
        # Skip directories
        if any(skip_dir in path.parts for skip_dir in SKIP_DIRS):
            continue
        # Skip specific files
        if path.name in SKIP_FILES:
            continue
        python_files.append(path)

    return python_files


def scan_file(filepath: Path) -> List[Tuple[int, str, str]]:
    """
    Scan a file for hardcoded passwords.

    Returns:
        List of (line_number, original_line, matched_pattern)
    """
    findings = []

    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            # Check patterns
            for pattern, replacement in HARDCODED_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append((i, line.strip(), pattern))
                    break

    except Exception as e:
        print(f"Error scanning {filepath}: {e}")

    return findings


def fix_file(filepath: Path, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Fix hardcoded passwords in a file.

    Returns:
        Tuple of (was_modified, number_of_fixes)
    """
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        original_content = content
        fix_count = 0

        # Add import if we're making changes and os not imported
        needs_os_import = False

        for pattern, replacement in HARDCODED_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                fix_count += 1
                if 'os.getenv' in replacement:
                    needs_os_import = True

        if fix_count > 0:
            # Add os import if needed
            if needs_os_import and 'import os' not in content:
                # Add after other imports or at top
                if 'import ' in content:
                    content = re.sub(
                        r'(import [^\n]+\n)',
                        r'\1import os\n',
                        content,
                        count=1
                    )
                else:
                    content = 'import os\n\n' + content

            if not dry_run:
                # Backup original
                backup_path = filepath.with_suffix('.py.bak')
                shutil.copy2(filepath, backup_path)

                # Write fixed content
                filepath.write_text(content, encoding='utf-8')

            return True, fix_count

        return False, 0

    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False, 0


def generate_report(findings: Dict[Path, List], output_path: Path):
    """Generate a report of findings."""
    report = []
    report.append("# Hardcoded Password Audit Report")
    report.append(f"\nGenerated: {datetime.now().isoformat()}")
    report.append(f"\nTotal files scanned: {len(findings)}")

    files_with_issues = {k: v for k, v in findings.items() if v}
    report.append(f"Files with issues: {len(files_with_issues)}")

    total_issues = sum(len(v) for v in files_with_issues.values())
    report.append(f"Total issues found: {total_issues}\n")

    report.append("## Findings\n")

    for filepath, issues in sorted(files_with_issues.items()):
        rel_path = filepath.relative_to(Path.cwd()) if filepath.is_relative_to(Path.cwd()) else filepath
        report.append(f"### {rel_path}\n")

        for line_num, line, pattern in issues:
            report.append(f"- **Line {line_num}**: `{line[:80]}...`")

        report.append("")

    output_path.write_text('\n'.join(report), encoding='utf-8')
    print(f"\nReport saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Fix hardcoded passwords in Python files')
    parser.add_argument('--scan', action='store_true', help='Scan for hardcoded passwords')
    parser.add_argument('--fix', action='store_true', help='Apply fixes')
    parser.add_argument('--dry', action='store_true', help='Dry run (no changes)')
    parser.add_argument('--root', type=str, default='.', help='Root directory to scan')
    parser.add_argument('--report', type=str, default='docs/hardcoded_passwords_report.md',
                       help='Report output path')

    args = parser.parse_args()

    if not args.scan and not args.fix:
        parser.print_help()
        return

    root_dir = Path(args.root).resolve()
    print(f"Scanning directory: {root_dir}")

    python_files = find_python_files(root_dir)
    print(f"Found {len(python_files)} Python files to scan")

    findings = {}

    for filepath in python_files:
        file_findings = scan_file(filepath)
        findings[filepath] = file_findings

        if file_findings:
            rel_path = filepath.relative_to(root_dir)
            print(f"\n⚠️  {rel_path}: {len(file_findings)} issue(s)")
            for line_num, line, pattern in file_findings:
                print(f"   Line {line_num}: {line[:60]}...")

    # Generate report
    generate_report(findings, Path(args.report))

    # Apply fixes if requested
    if args.fix:
        print("\n" + "="*60)
        if args.dry:
            print("DRY RUN - No changes will be made")
        else:
            print("APPLYING FIXES")
        print("="*60)

        total_fixed = 0
        files_fixed = 0

        for filepath, file_findings in findings.items():
            if file_findings:
                modified, count = fix_file(filepath, dry_run=args.dry)
                if modified:
                    files_fixed += 1
                    total_fixed += count
                    rel_path = filepath.relative_to(root_dir)
                    status = "(dry run)" if args.dry else "✅"
                    print(f"{status} Fixed {count} issue(s) in {rel_path}")

        print(f"\n{'Would fix' if args.dry else 'Fixed'} {total_fixed} issues in {files_fixed} files")

    # Summary
    files_with_issues = sum(1 for v in findings.values() if v)
    total_issues = sum(len(v) for v in findings.values())

    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_issues} hardcoded passwords in {files_with_issues} files")
    print(f"{'='*60}")

    if total_issues > 0:
        print("\n⚠️  SECURITY RISK: Hardcoded passwords found!")
        print("   Run with --fix to apply automatic fixes")
        print("   Run with --fix --dry for a dry run first")
        sys.exit(1)
    else:
        print("\n✅ No hardcoded passwords found!")
        sys.exit(0)


if __name__ == '__main__':
    main()
