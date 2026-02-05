"""
Create backup ZIP file excluding unnecessary directories and files.
"""
import os
import zipfile
from datetime import datetime
from pathlib import Path

# Directories and patterns to exclude
EXCLUDE_DIRS = {
    'node_modules',
    '__pycache__',
    '.pytest_cache',
    'pytest_cache',
    '.env',
    '.venv',
    'venv',
    'env',
    '.git',
    '.vscode',
    '.idea',
    'htmlcov',
    '.coverage',
    'dist',
    'build',
    '*.egg-info',
    '.mypy_cache',
    '.ruff_cache',
    '.tox',
    'venvsource',
}

EXCLUDE_EXTENSIONS = {
    '.pyc',
    '.pyo',
    '.pyd',
    '.so',
    '.dll',
    '.dylib',
    '.egg',
    '.log',
}

def should_exclude(path: Path, base_path: Path) -> bool:
    """Check if path should be excluded from backup."""
    relative_path = str(path.relative_to(base_path))
    
    # Check if any excluded directory is in the path
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in relative_path.split(os.sep):
            return True
    
    # Check file extension
    if path.suffix in EXCLUDE_EXTENSIONS:
        return True
    
    return False

def create_backup(source_dir: str, output_dir: str = None):
    """Create backup ZIP file."""
    source_path = Path(source_dir).resolve()
    
    if output_dir is None:
        output_dir = source_path.parent
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"gaara_scan_ai_backup_{timestamp}.zip"
    backup_path = Path(output_dir) / backup_name
    
    print(f"Creating backup: {backup_path}")
    print(f"Source directory: {source_path}")
    print(f"\nExcluding: {', '.join(EXCLUDE_DIRS)}")
    print(f"Excluding extensions: {', '.join(EXCLUDE_EXTENSIONS)}\n")
    
    file_count = 0
    excluded_count = 0
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            root_path = Path(root)
            
            # Filter directories to exclude
            dirs[:] = [
                d for d in dirs 
                if not should_exclude(root_path / d, source_path)
            ]
            
            for file in files:
                file_path = root_path / file
                
                if should_exclude(file_path, source_path):
                    excluded_count += 1
                    continue
                
                # Add file to zip
                arcname = file_path.relative_to(source_path)
                zipf.write(file_path, arcname)
                file_count += 1
                
                if file_count % 100 == 0:
                    print(f"Processed {file_count} files...", end='\r')
    
    # Get backup size
    backup_size = backup_path.stat().st_size
    size_mb = backup_size / (1024 * 1024)
    
    print(f"\n\n✅ Backup created successfully!")
    print(f"📁 Location: {backup_path}")
    print(f"📊 Files included: {file_count:,}")
    print(f"🚫 Files excluded: {excluded_count:,}")
    print(f"💾 Size: {size_mb:.2f} MB")
    
    return backup_path

if __name__ == "__main__":
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create backup
    backup_path = create_backup(current_dir)
    
    print(f"\n🎉 Backup complete: {backup_path.name}")
