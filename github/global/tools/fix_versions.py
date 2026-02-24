"""
Module: fix_versions.py
Fix Versions — part of Global System v26.0.2 Diamond 32.
"""
#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path

# Configuration
ROOT_DIR = Path(__file__).parent.parent
TARGET_VERSION = "v26.0 Diamond 32"
TARGET_VERSION_SHORT = "v26.0"
REPLACEMENTS = {
    "v26.0": TARGET_VERSION_SHORT,
    "v26.0": TARGET_VERSION_SHORT,
    "Diamond 32": "Diamond 32",
    "Diamond 32": "Diamond 32",
    "v26.0": TARGET_VERSION_SHORT,
    "Global System v26 Diamond 32": "Global System v26 Diamond 32",
    "requirements.txt": "requirements.txt" # Unify requirements file name
}

DIRECTORIES_TO_REMOVE = [
    "audit_v35.9",
    "prompts/archive/v26.0",
    "archive"
]

def replace_in_file(file_path):
    """
    Replace in file implementation.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        original_content = content
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
            
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
    except Exception as e:
        print(f"❌ Failed to update {file_path}: {e}")

def cleanup_directories():
    """
    Cleanup directories implementation.
    """
    for dir_name in DIRECTORIES_TO_REMOVE:
        dir_path = ROOT_DIR / dir_name
        if dir_path.exists():
            print(f"🗑️ Removing directory: {dir_path}")
            shutil.rmtree(dir_path)

def rename_files():
    """
    Rename files implementation.
    """
    # Rename requirements.txt to requirements.txt if it exists
    old_req = ROOT_DIR / "config/requirements.txt"
    new_req = ROOT_DIR / "requirements.txt"
    
    if old_req.exists():
        if new_req.exists():
            # Merge content if both exist
            with open(old_req, "r") as f1, open(new_req, "r") as f2:
                content = f1.read() + "\n" + f2.read()
            with open(new_req, "w") as f:
                f.write(content)
            os.remove(old_req)
            print(f"✅ Merged and renamed requirements.txt to requirements.txt")
        else:
            shutil.move(old_req, new_req)
            print(f"✅ Renamed requirements.txt to requirements.txt")

def main():
    """
    Main implementation.
    """
    print(f"🚀 Starting Version Fix on {ROOT_DIR}...")
    
    # 1. Replace Content
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            file_path = Path(root) / file
            if file.endswith((".py", ".md", ".txt", ".json", ".yaml", ".yml")):
                replace_in_file(file_path)

    # 2. Cleanup
    cleanup_directories()
    
    # 3. Rename Files
    rename_files()
    
    print("✨ Version Fix Complete.")

if __name__ == "__main__":
    main()
