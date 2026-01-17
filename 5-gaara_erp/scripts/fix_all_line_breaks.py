#!/usr/bin/env python3
# FILE: scripts/fix_all_line_breaks.py | PURPOSE: Fix ALL missing line breaks | OWNER: Architecture Team | LAST-AUDITED: 2025-11-18

"""
Fix ALL Missing Line Breaks in compliance/models.py

After removing Meta class insertions, many lines were joined without proper line breaks.
This script finds and fixes ALL instances.

Pattern: )class Meta:  or  )verbose_name  or similar

Usage:
    python scripts/fix_all_line_breaks.py
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'
FILE_PATH = PROJECT_ROOT / 'services_modules' / 'compliance' / 'models.py'

def fix_all_line_breaks():
    """Fix ALL missing line breaks"""
    
    print("="*80)
    print("FIXING ALL MISSING LINE BREAKS")
    print("="*80)
    print()
    
    # Read the file
    content = FILE_PATH.read_text(encoding='utf-8')
    original_content = content
    
    # Backup
    backup_path = FILE_PATH.with_suffix('.py.bak_linebreaks')
    backup_path.write_text(content, encoding='utf-8')
    print(f"✓ Backup created: {backup_path}\n")
    
    fixes = 0
    
    # Pattern 1: )class Meta:
    pattern1 = r'\)class Meta:'
    matches1 = re.findall(pattern1, content)
    if matches1:
        content = re.sub(pattern1, r')\n\n    class Meta:', content)
        fixes += len(matches1)
        print(f"Fix {fixes}: Added line breaks before 'class Meta:' ({len(matches1)} instances)")
    
    # Pattern 2: )verbose_name
    pattern2 = r'\)verbose_name'
    matches2 = re.findall(pattern2, content)
    if matches2:
        content = re.sub(pattern2, r')\n\n    class Meta:\n        app_label = \'compliance\'\n        verbose_name', content)
        fixes += len(matches2)
        print(f"Fix {fixes}: Added line breaks before 'verbose_name' ({len(matches2)} instances)")
    
    # Pattern 3: )ordering
    pattern3 = r'\)ordering'
    matches3 = re.findall(pattern3, content)
    if matches3:
        content = re.sub(pattern3, r')\n\n    class Meta:\n        app_label = \'compliance\'\n        ordering', content)
        fixes += len(matches3)
        print(f"Fix {fixes}: Added line breaks before 'ordering' ({len(matches3)} instances)")
    
    # Pattern 4: )def
    pattern4 = r'\)def '
    matches4 = re.findall(pattern4, content)
    if matches4:
        content = re.sub(pattern4, r')\n\n    def ', content)
        fixes += len(matches4)
        print(f"Fix {fixes}: Added line breaks before 'def' ({len(matches4)} instances)")
    
    # Write fixed content
    if content != original_content:
        FILE_PATH.write_text(content, encoding='utf-8')
        print(f"\n✓ Fixed {fixes} missing line breaks")
        print(f"✓ File saved: {FILE_PATH}")
    else:
        print("\n✓ No missing line breaks found")
    
    return fixes


if __name__ == "__main__":
    try:
        fixes = fix_all_line_breaks()
        print("\n" + "="*80)
        if fixes > 0:
            print(f"✓ SUCCESS: Fixed {fixes} missing line breaks")
        else:
            print("✓ File is clean")
        print("="*80)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

