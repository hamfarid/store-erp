#!/usr/bin/env python3
# FILE: scripts/fix_all_compliance_syntax.py | PURPOSE: Fix ALL syntax errors in compliance models | OWNER: Architecture Team | LAST-AUDITED: 2025-11-18

"""
Fix ALL Compliance Models Syntax Errors

The compliance/models.py file has multiple broken class definitions where
Meta classes were incorrectly inserted, breaking the class name.

Pattern: class Compli\n    class Meta:\n        app_label = 'compliance'\nanceAudit(models.Model):
Should be: class ComplianceAudit(models.Model):

Usage:
    python scripts/fix_all_compliance_syntax.py
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'
FILE_PATH = PROJECT_ROOT / 'services_modules' / 'compliance' / 'models.py'

def fix_all_compliance_syntax():
    """Fix ALL broken class definitions in compliance/models.py"""
    
    print("="*80)
    print("FIXING ALL COMPLIANCE MODELS SYNTAX ERRORS")
    print("="*80)
    print()
    
    # Read the file
    content = FILE_PATH.read_text(encoding='utf-8')
    
    # Backup original
    backup_path = FILE_PATH.with_suffix('.py.bak3')
    backup_path.write_text(content, encoding='utf-8')
    print(f"✓ Backup created: {backup_path}")
    
    # Pattern to find broken class definitions
    # Matches: class Compli\n    class Meta:\n        app_label = 'compliance'\nanceXXX(models.Model):
    pattern = r"class ([A-Z][a-z]+)\n\s+class Meta:\s*\n\s+app_label = 'compliance'\s*\n([a-z]+[A-Z][a-zA-Z]*)\(models\.Model\):"
    
    # Find all matches
    matches = list(re.finditer(pattern, content, re.MULTILINE))
    print(f"Found {len(matches)} broken class definitions\n")
    
    # Fix each match
    for i, match in enumerate(matches, 1):
        old_text = match.group(0)
        # Reconstruct the class name
        class_name = match.group(1) + match.group(2)
        new_text = f"class {class_name}(models.Model):"
        content = content.replace(old_text, new_text, 1)
        print(f"Fix {i}: {class_name}")
    
    # Write fixed content
    FILE_PATH.write_text(content, encoding='utf-8')
    print(f"\n✓ Fixed {len(matches)} broken class definitions")
    print(f"✓ File saved: {FILE_PATH}")
    
    return len(matches)


if __name__ == "__main__":
    try:
        fixes = fix_all_compliance_syntax()
        print("\n" + "="*80)
        print(f"✓ SUCCESS: Fixed {fixes} broken class definitions")
        print("="*80)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

