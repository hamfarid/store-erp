#!/usr/bin/env python3
# FILE: scripts/fix_invalid_model_references.py | PURPOSE: Fix invalid Django model references | OWNER: Architecture Team | LAST-AUDITED: 2025-11-18

"""
Fix Invalid Django Model References

Django model references in ForeignKey, ManyToManyField, OneToOneField must be in format:
"app_label.ModelName"

NOT:
"module.submodule.ModelName"

This script finds and fixes all invalid references.

Usage:
    python scripts/fix_invalid_model_references.py
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'

# Pattern to match invalid model references
# Matches: "module.submodule.ModelName" (3+ parts with capital letter at end)
INVALID_PATTERN = re.compile(r'"([a-z_]+\.[a-z_]+\.[A-Z][a-zA-Z]+)"')

# Known app labels and their module paths
APP_LABEL_MAP = {
    'business_modules.accounting': 'accounting',
    'business_modules.inventory': 'inventory',
    'business_modules.sales': 'sales',
    'business_modules.purchasing': 'purchasing',
    'business_modules.contacts': 'contacts',
    'business_modules.production': 'production',
    'business_modules.pos': 'pos',
    'business_modules.assets': 'assets',
    'services_modules.accounting': 'accounting',  # May conflict, need to check
    'services_modules.hr': 'hr',
    'services_modules.projects': 'projects',
    'core_modules.users': 'users',
    'core_modules.core': 'core',
    'core_modules.organization': 'organization',
    'core_modules.companies': 'companies',
}


def fix_model_reference(match_text):
    """Convert invalid model reference to valid format."""
    # Extract the full reference
    full_ref = match_text.group(1)
    parts = full_ref.split('.')
    
    if len(parts) < 3:
        return match_text.group(0)  # Already valid
    
    # Try to find app label
    model_name = parts[-1]  # Last part is always the model name
    module_path = '.'.join(parts[:-1])  # Everything except model name
    
    # Check if we have a mapping
    if module_path in APP_LABEL_MAP:
        app_label = APP_LABEL_MAP[module_path]
        return f'"{app_label}.{model_name}"'
    
    # If no mapping, use the second-to-last part as app label
    # e.g., "business_modules.accounting.Expense" -> "accounting.Expense"
    app_label = parts[-2]
    return f'"{app_label}.{model_name}"'


def scan_and_fix_file(file_path):
    """Scan a Python file and fix invalid model references."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Find all matches
        matches = list(INVALID_PATTERN.finditer(content))
        
        if not matches:
            return 0
        
        # Fix each match
        fixed_content = INVALID_PATTERN.sub(fix_model_reference, content)
        
        if fixed_content != original_content:
            # Backup original
            backup_path = file_path.with_suffix('.py.bak')
            backup_path.write_text(original_content, encoding='utf-8')
            
            # Write fixed content
            file_path.write_text(fixed_content, encoding='utf-8')
            
            print(f"✓ Fixed {len(matches)} references in: {file_path.relative_to(PROJECT_ROOT)}")
            for match in matches:
                old_ref = match.group(1)
                new_ref = fix_model_reference(match).strip('"')
                print(f"    {old_ref} → {new_ref}")
            
            return len(matches)
        
        return 0
        
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return 0


def main():
    """Scan all Python files and fix invalid model references."""
    print("="*80)
    print("FIXING INVALID DJANGO MODEL REFERENCES")
    print("="*80)
    print()
    
    total_files = 0
    total_fixes = 0
    
    # Scan all Python files
    for py_file in PROJECT_ROOT.rglob('*.py'):
        # Skip migrations
        if 'migrations' in py_file.parts:
            continue
        
        # Skip __pycache__
        if '__pycache__' in py_file.parts:
            continue
        
        fixes = scan_and_fix_file(py_file)
        if fixes > 0:
            total_files += 1
            total_fixes += fixes
    
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Files fixed: {total_files}")
    print(f"Total references fixed: {total_fixes}")
    
    if total_fixes > 0:
        print("\n✓ All invalid model references have been fixed!")
        print("✓ Original files backed up with .bak extension")
    else:
        print("\n✓ No invalid model references found!")


if __name__ == "__main__":
    main()

