#!/usr/bin/env python3
"""
Backup creation script for the Store ERP project.
Excludes unnecessary files like node_modules, __pycache__, .venv, etc.
Creates timestamped ZIP archives with comprehensive reporting.
"""

import os
import zipfile
import shutil
import datetime
import sys
from pathlib import Path
from typing import List, Tuple

# Directories and files to exclude from backup
EXCLUDE_PATTERNS = {
    'directories': [
        '__pycache__',
        '.pytest_cache',
        'node_modules',
        '.venv',
        'venv',
        'env',
        '.git',
        '.github',
        'dist',
        'build',
        '.egg-info',
        '.tox',
        '.coverage',
        'htmlcov',
        '.vscode',
        '.idea',
        'coverage',
        '.next',
        'out',
    ],
    'files': [
        '.env',
        '.env.local',
        '.env.*.local',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.DS_Store',
        'Thumbs.db',
        '*.log',
        '.coverage',
        'coverage.xml',
        '.pytest_cache',
    ]
}

def should_exclude(path: str, rel_path: str) -> bool:
    """Check if a path should be excluded from backup."""
    path_parts = rel_path.replace('\\', '/').split('/')
    
    # Check directory names
    for part in path_parts[:-1]:  # All but last (which is filename)
        if part in EXCLUDE_PATTERNS['directories']:
            return True
    
    # Check filename patterns
    filename = path_parts[-1] if path_parts else ''
    if filename in EXCLUDE_PATTERNS['files']:
        return True
    
    # Check file extensions
    for pattern in EXCLUDE_PATTERNS['files']:
        if pattern.startswith('*') and filename.endswith(pattern[1:]):
            return True
    
    return False

def create_backup(project_root: str = '.', backup_dir: str = 'backups') -> Tuple[str, int, int]:
    """
    Create a backup zip file of the project.
    
    Args:
        project_root: Root directory of the project
        backup_dir: Directory to store backups
    
    Returns:
        Tuple of (backup_path, file_count, total_size_mb)
    """
    # Create backup directory if it doesn't exist
    backup_path_obj = Path(backup_dir)
    backup_path_obj.mkdir(exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'backup_{timestamp}.zip'
    backup_filepath = backup_path_obj / backup_filename
    
    # Track statistics
    file_count = 0
    excluded_count = 0
    total_size = 0
    
    print(f"\n🔄 Creating backup: {backup_filename}")
    print(f"📁 Project root: {project_root}")
    print(f"💾 Backup directory: {backup_dir}")
    print("-" * 60)
    
    try:
        with zipfile.ZipFile(backup_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_root):
                # Filter directories to skip excluded ones
                dirs[:] = [d for d in dirs if not should_exclude(root, d)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, project_root)
                    
                    if should_exclude(file_path, rel_path):
                        excluded_count += 1
                        continue
                    
                    try:
                        zipf.write(file_path, arcname=rel_path)
                        file_count += 1
                        file_size = os.path.getsize(file_path)
                        total_size += file_size
                    except Exception as e:
                        print(f"⚠️  Error adding {rel_path}: {e}")
        
        total_size_mb = total_size / (1024 * 1024)
        
        print(f"\n✅ Backup completed successfully!")
        print(f"📦 Backup file: {backup_filepath}")
        print(f"📊 Statistics:")
        print(f"  - Files included: {file_count}")
        print(f"  - Files excluded: {excluded_count}")
        print(f"  - Total size: {total_size_mb:.2f} MB")
        print(f"  - Compressed size: {backup_filepath.stat().st_size / (1024 * 1024):.2f} MB")
        print("-" * 60)
        
        return str(backup_filepath), file_count, int(total_size_mb)
    
    except Exception as e:
        print(f"\n❌ Error creating backup: {e}")
        sys.exit(1)

def create_backup_manifest(backup_filepath: str, file_count: int, size_mb: int):
    """Create a manifest file documenting the backup."""
    manifest_path = Path(backup_filepath).with_suffix('.txt')
    timestamp = datetime.datetime.now().isoformat()
    
    manifest_content = f"""BACKUP MANIFEST
{'=' * 60}
Created: {timestamp}
Backup File: {Path(backup_filepath).name}
Total Files: {file_count}
Total Size: {size_mb} MB

EXCLUDED PATTERNS:
Directories:
{chr(10).join(f'  - {d}' for d in EXCLUDE_PATTERNS['directories'])}

File Patterns:
{chr(10).join(f'  - {f}' for f in EXCLUDE_PATTERNS['files'])}

PURPOSE:
- Development backups for recovery
- Database backup before migrations
- Version control for major changes

RESTORE INSTRUCTIONS:
1. Extract the ZIP file to a temporary directory
2. Compare with current project structure
3. Copy necessary files back to project
4. Update .env and configuration files as needed
5. Run: pip install -r backend/requirements.txt
6. Run: npm install (in frontend directory)
7. Test the application before deploying

SECURITY NOTE:
- This backup does not include .env files (for security)
- Sensitive credentials must be restored manually
- Store backups in a secure location
{'=' * 60}
"""
    
    with open(manifest_path, 'w') as f:
        f.write(manifest_content)
    
    print(f"📋 Manifest created: {manifest_path}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Create a backup of the Store ERP project'
    )
    parser.add_argument(
        '--root',
        default='.',
        help='Project root directory (default: current directory)'
    )
    parser.add_argument(
        '--backup-dir',
        default='backups',
        help='Directory to store backups (default: backups)'
    )
    parser.add_argument(
        '--manifest',
        action='store_true',
        help='Create a manifest file with backup information'
    )
    
    args = parser.parse_args()
    
    backup_path, file_count, size_mb = create_backup(args.root, args.backup_dir)
    
    if args.manifest:
        create_backup_manifest(backup_path, file_count, size_mb)
    
    print(f"\n✨ Backup process complete!")
