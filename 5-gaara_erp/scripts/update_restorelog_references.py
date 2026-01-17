#!/usr/bin/env python3
# FILE: scripts/update_restorelog_references.py
# PURPOSE: Update all RestoreLog references from database_management to system_backups
# OWNER: Architecture Team
# LAST-AUDITED: 2025-11-18

"""
Update RestoreLog References Script

This script updates all references to database_management.RestoreLog
to use system_backups.RestoreLog instead.

Usage:
    python scripts/update_restorelog_references.py [--dry-run]
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'

# Files to update
FILES_TO_UPDATE = [
    'admin_modules/database_management/serializers.py',
    'admin_modules/reports/serializers.py',
]

def update_file(file_path: Path, dry_run: bool = False):
    """Update RestoreLog imports in a file"""
    
    if not file_path.exists():
        print(f"⏭️  Skipping {file_path} (not found)")
        return False
    
    # Read file
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Backup
    if not dry_run:
        backup_path = file_path.with_suffix('.py.bak_restorelog')
        backup_path.write_text(content, encoding='utf-8')
    
    # Pattern 1: from .models import ... RestoreLog ...
    # Replace with import from system_backups
    pattern1 = r'from \.models import (.*)RestoreLog(.*)'
    
    def replace_import(match):
        before = match.group(1)
        after = match.group(2)
        
        # Keep other imports from .models
        other_imports = []
        if before.strip():
            other_imports.extend([x.strip() for x in before.split(',') if x.strip()])
        if after.strip():
            other_imports.extend([x.strip() for x in after.split(',') if x.strip()])
        
        # Remove empty strings
        other_imports = [x for x in other_imports if x]
        
        # Build new import statements
        new_imports = []
        if other_imports:
            new_imports.append(f"from .models import {', '.join(other_imports)}")
        new_imports.append("from admin_modules.system_backups.models import RestoreLog")
        
        return '\n'.join(new_imports)
    
    content = re.sub(pattern1, replace_import, content)
    
    # Check if changes were made
    if content != original_content:
        if dry_run:
            print(f"✏️  Would update: {file_path}")
            print(f"   Changes:")
            # Show diff
            original_lines = original_content.split('\n')
            new_lines = content.split('\n')
            for i, (old, new) in enumerate(zip(original_lines, new_lines), 1):
                if old != new:
                    print(f"   Line {i}:")
                    print(f"     - {old}")
                    print(f"     + {new}")
        else:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ Updated: {file_path}")
        return True
    else:
        print(f"⏭️  No changes needed: {file_path}")
        return False


def main(dry_run: bool = False):
    """Main function"""
    
    print("="*80)
    print("UPDATING RESTORELOG REFERENCES")
    print("="*80)
    print()
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print()
    
    updated = 0
    skipped = 0
    
    for file_rel_path in FILES_TO_UPDATE:
        file_path = PROJECT_ROOT / file_rel_path
        if update_file(file_path, dry_run):
            updated += 1
        else:
            skipped += 1
    
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Updated: {updated} files")
    print(f"⏭️  Skipped: {skipped} files")
    
    if not dry_run and updated > 0:
        print()
        print("📝 Next steps:")
        print("   1. Run: python manage.py check")
        print("   2. Update admin.py files")
        print("   3. Update tests")
        print("   4. Run tests")
    
    print("="*80)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Update RestoreLog references')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    
    args = parser.parse_args()
    
    main(dry_run=args.dry_run)

