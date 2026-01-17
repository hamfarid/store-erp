#!/usr/bin/env python3
# FILE: scripts/fix_all_meta_insertions.py | PURPOSE: Fix ALL Meta class insertions | OWNER: Architecture Team | LAST-AUDITED: 2025-11-18

"""
Fix ALL Meta Class Insertions in compliance/models.py

This script finds and removes ALL incorrectly inserted Meta classes
that break the code structure.

Usage:
    python scripts/fix_all_meta_insertions.py
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'
FILE_PATH = PROJECT_ROOT / 'services_modules' / 'compliance' / 'models.py'

def fix_all_meta_insertions():
    """Remove ALL incorrectly inserted Meta classes"""
    
    print("="*80)
    print("FIXING ALL META CLASS INSERTIONS")
    print("="*80)
    print()
    
    # Read the file
    content = FILE_PATH.read_text(encoding='utf-8')
    original_content = content
    
    # Backup
    backup_path = FILE_PATH.with_suffix('.py.bak_final')
    backup_path.write_text(content, encoding='utf-8')
    print(f"✓ Backup created: {backup_path}\n")
    
    # Pattern 1: Meta class inserted in middle of code
    # Matches any line ending with incomplete code + Meta class + continuation
    pattern1 = r"([^\n]+)\n\s+class Meta:\s*\n\s+app_label = 'compliance'\s*\n([^\n]+)"
    
    fixes = 0
    while True:
        match = re.search(pattern1, content, re.MULTILINE)
        if not match:
            break
        
        # Reconstruct without Meta class
        line1 = match.group(1).rstrip()
        line2 = match.group(2).lstrip()
        
        # Join the lines
        new_text = f"{line1}{line2}"
        
        old_text = match.group(0)
        content = content.replace(old_text, new_text, 1)
        fixes += 1
        print(f"Fix {fixes}: Removed Meta class insertion")
    
    # Write fixed content
    if content != original_content:
        FILE_PATH.write_text(content, encoding='utf-8')
        print(f"\n✓ Fixed {fixes} Meta class insertions")
        print(f"✓ File saved: {FILE_PATH}")
    else:
        print("\n✓ No Meta class insertions found")
    
    return fixes


if __name__ == "__main__":
    try:
        fixes = fix_all_meta_insertions()
        print("\n" + "="*80)
        if fixes > 0:
            print(f"✓ SUCCESS: Fixed {fixes} Meta class insertions")
        else:
            print("✓ File is clean")
        print("="*80)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

