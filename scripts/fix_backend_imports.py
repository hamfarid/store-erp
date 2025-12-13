#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Backend Import Paths

This script automatically fixes incorrect import paths in backend route files.

Fixes:
1. src.models.category -> src.models.inventory
2. src.models.user_unified -> src.models.user
3. src.models.supporting_models -> correct locations

Usage:
    python scripts/fix_backend_imports.py
"""

import os
import re
from pathlib import Path

# Define import replacements
REPLACEMENTS = {
    # Category imports
    'from src.models.category import Category': 'from src.models.inventory import Category',
    
    # User imports
    'from src.models.user_unified import User': 'from src.models.user import User',
    'from src.models.user_unified import User, Role': 'from src.models.user import User, Role',
    'from src.models.user_unified import User, Role, create_default_roles': 'from src.models.user import User, Role, create_default_roles',
    
    # Supporting models - StockMovement
    'from src.models.supporting_models import StockMovement': 'from src.models.inventory import StockMovement',
    'from src.models.supporting_models import (StockMovement': 'from src.models.inventory import (StockMovement',
    
    # Supporting models - Payment
    'from src.models.supporting_models import Payment': 'from src.models.invoice_unified import Payment',
    
    # Supporting models - ActionType, AuditLog (these might not exist, keep as fallback)
    'from src.models.supporting_models import ActionType': '# from src.models.supporting_models import ActionType  # TODO: Verify this model exists',
    'from src.models.supporting_models import AuditLog': '# from src.models.supporting_models import AuditLog  # TODO: Verify this model exists',
}

# Complex multi-line replacements
COMPLEX_REPLACEMENTS = [
    # Replace supporting_models imports with correct locations
    {
        'pattern': r'from src\.models\.supporting_models import \(\s*ActionType,\s*AuditLog,?\s*\)',
        'replacement': '# from src.models.supporting_models import (ActionType, AuditLog)  # TODO: Verify these models exist'
    },
    {
        'pattern': r'from src\.models\.supporting_models import ActionType, AuditLog',
        'replacement': '# from src.models.supporting_models import ActionType, AuditLog  # TODO: Verify these models exist'
    },
]

def fix_file(filepath):
    """Fix imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # Apply simple replacements
        for old, new in REPLACEMENTS.items():
            if old in content:
                content = content.replace(old, new)
                modified = True
                print(f'  ✅ Replaced: {old}')
        
        # Apply complex regex replacements
        for replacement in COMPLEX_REPLACEMENTS:
            pattern = replacement['pattern']
            new_text = replacement['replacement']
            if re.search(pattern, content):
                content = re.sub(pattern, new_text, content)
                modified = True
                print(f'  ✅ Replaced pattern: {pattern}')
        
        # Write back if modified
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f'  ❌ Error: {e}')
        return False

def main():
    """Main function"""
    print('🔧 Fixing Backend Import Paths')
    print('=' * 60)
    
    # Get all Python files in routes directory
    routes_dir = Path('backend/src/routes')
    if not routes_dir.exists():
        print(f'❌ Routes directory not found: {routes_dir}')
        return
    
    python_files = list(routes_dir.glob('*.py'))
    print(f'📁 Found {len(python_files)} Python files in routes/')
    print()
    
    fixed_count = 0
    
    for filepath in python_files:
        # Skip __init__.py and backup files
        if filepath.name == '__init__.py' or '.backup' in filepath.name:
            continue
        
        print(f'📄 Processing: {filepath.name}')
        
        if fix_file(filepath):
            fixed_count += 1
            print(f'  ✅ Fixed!')
        else:
            print(f'  ⏭️  No changes needed')
        
        print()
    
    print('=' * 60)
    print(f'🎉 Import Fix Complete!')
    print(f'📊 Files fixed: {fixed_count}/{len(python_files)}')
    print()
    print('Next steps:')
    print('1. Install reportlab: pip install reportlab')
    print('2. Restart backend server: python backend/app.py')
    print('3. Verify no warnings appear')
    print('=' * 60)

if __name__ == '__main__':
    main()

