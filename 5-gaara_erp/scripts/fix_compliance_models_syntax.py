#!/usr/bin/env python3
# FILE: scripts/fix_compliance_models_syntax.py | PURPOSE: Fix syntax errors in compliance models | OWNER: Architecture Team | LAST-AUDITED: 2025-11-18

"""
Fix Compliance Models Syntax Errors

The compliance/models.py file has multiple syntax errors where Meta classes
were incorrectly inserted into choice tuples. This script fixes all of them.

Usage:
    python scripts/fix_compliance_models_syntax.py
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'
FILE_PATH = PROJECT_ROOT / 'services_modules' / 'compliance' / 'models.py'

def fix_compliance_models():
    """Fix all syntax errors in compliance/models.py"""
    
    print("="*80)
    print("FIXING COMPLIANCE MODELS SYNTAX ERRORS")
    print("="*80)
    print()
    
    # Read the file
    content = FILE_PATH.read_text(encoding='utf-8')
    
    # Backup original
    backup_path = FILE_PATH.with_suffix('.py.bak2')
    backup_path.write_text(content, encoding='utf-8')
    print(f"✓ Backup created: {backup_path}")
    
    # Pattern to find broken choice tuples with Meta class inserted
    # Matches: ('key', _('value')),\n    class Meta:\n        app_label = 'compliance'\n  ('key2', _('value2')),
    pattern = r"\('([^']+)',\s*_\('([^']+)'\)\),\s*\n\s*class Meta:\s*\n\s*app_label = 'compliance'\s*\n\s*\('([^']+)',\s*_\('([^']+)'\)\),"
    
    # Find all matches
    matches = list(re.finditer(pattern, content, re.MULTILINE))
    print(f"Found {len(matches)} broken choice tuples\n")
    
    # Fix each match
    for i, match in enumerate(matches, 1):
        old_text = match.group(0)
        # Reconstruct without the Meta class
        new_text = f"('{match.group(1)}', _('{match.group(2)}')),\n        ('{match.group(3)}', _('{match.group(4)}')),"
        content = content.replace(old_text, new_text, 1)
        print(f"Fix {i}: Removed Meta class from choice tuple")
    
    # Write fixed content
    FILE_PATH.write_text(content, encoding='utf-8')
    print(f"\n✓ Fixed {len(matches)} syntax errors")
    print(f"✓ File saved: {FILE_PATH}")
    
    return len(matches)


if __name__ == "__main__":
    try:
        fixes = fix_compliance_models()
        print("\n" + "="*80)
        print(f"✓ SUCCESS: Fixed {fixes} syntax errors in compliance/models.py")
        print("="*80)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

