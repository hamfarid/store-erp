#!/usr/bin/env python3
"""
Backup Script for Gaara ERP Project
Creates timestamped ZIP archives excluding unnecessary files
"""

import os
import zipfile
from datetime import datetime
from pathlib import Path
import sys

# Directories and patterns to exclude
EXCLUDE_PATTERNS = [
    'node_modules',
    '__pycache__',
    '.venv',
    'venv',
    '.pytest_cache',
    '.mypy_cache',
    '.git',
    'env',
    '.env',
    'dist',
    'build',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.Python',
    'pip-log.txt',
    'pip-delete-this-directory.txt',
    '.coverage',
    'htmlcov',
    '.tox',
    '.nox',
    'coverage.xml',
    '*.cover',
    '.hypothesis',
    '.DS_Store',
    'Thumbs.db',
    '*.log',
    '*.sqlite',
    '*.sqlite3',
    '*.db',
    'migrations/__pycache__',
    '.idea',
    '.vscode',
    '*.swp',
    '*.swo',
    '*~',
    '.backup',
    '*.backup',
    '*.zip',
    '*.tar.gz',
    '*.tar',
]

def should_exclude(file_path, exclude_patterns):
    """Check if file should be excluded based on patterns"""
    path_str = str(file_path)

    for pattern in exclude_patterns:
        if pattern.startswith('*.'):
            # File extension pattern
            if path_str.endswith(pattern[1:]):
                return True
        else:
            # Directory or file name pattern
            if pattern in path_str:
                return True

    return False

def get_file_size(file_path):
    """Get human-readable file size"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def create_backup(source_dir='.', backup_dir='../backups'):
    """Create a backup ZIP file of the project"""

    # Create timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    backup_name = f'gaara-erp-backup-{timestamp}.zip'

    # Ensure backup directory exists
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)

    backup_file = backup_path / backup_name

    print(f"Creating backup: {backup_file}")
    print(f"Source directory: {os.path.abspath(source_dir)}")
    print(f"Excluding patterns: {', '.join(EXCLUDE_PATTERNS[:5])}... (and more)")
    print("-" * 60)

    file_count = 0
    excluded_count = 0
    total_size = 0

    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d, EXCLUDE_PATTERNS)]

            for file in files:
                file_path = Path(root) / file

                if should_exclude(file_path, EXCLUDE_PATTERNS):
                    excluded_count += 1
                    continue

                try:
                    # Add file to ZIP with relative path
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)
                    file_count += 1
                    total_size += os.path.getsize(file_path)

                    if file_count % 100 == 0:
                        print(f"Processed {file_count} files...", end='\r')

                except Exception as e:
                    print(f"\nWarning: Could not add {file_path}: {e}")

    backup_size = get_file_size(backup_file)

    print(f"\n{'-' * 60}")
    print(f"✅ Backup created successfully!")
    print(f"📦 Backup file: {backup_file}")
    print(f"📊 Files included: {file_count:,}")
    print(f"🚫 Files excluded: {excluded_count:,}")
    print(f"💾 Backup size: {backup_size}")
    print(f"📏 Original size: {get_file_size(total_size)}")
    print(f"🕐 Timestamp: {timestamp}")

    return str(backup_file)

if __name__ == '__main__':
    try:
        source = sys.argv[1] if len(sys.argv) > 1 else '.'
        backup_location = sys.argv[2] if len(sys.argv) > 2 else '../backups'

        backup_file = create_backup(source, backup_location)
        print(f"\n✨ Backup complete: {backup_file}")

    except KeyboardInterrupt:
        print("\n❌ Backup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error creating backup: {e}")
        sys.exit(1)
