#!/usr/bin/env python3
"""
Version Agnostic Script (Global System v26 Diamond 32)
Removes specific version numbers (vXX.XX) and replaces them with "Global System v26 Diamond 32".
"""

import os
import re

# Configuration
# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Target the parent directory (global_system/)
TARGET_DIR = os.path.dirname(SCRIPT_DIR)

# Patterns to find and replace
VERSION_PATTERNS = [
    (r"v\d+\.\d+(\.\d+)?", "Global System v26 Diamond 32"),          # Matches Global System v26 Diamond 32, Global System v26 Diamond 32
    (r"Global System v\d+\.\d+", "Global System v26 Diamond 32"),    # Matches Global System Global System v26 Diamond 32
    (r"Bootstrap v\d+\.\d+", "Bootstrap Global System v26 Diamond 32"),        # Matches Bootstrap Global System v26 Diamond 32
    (r"Global System v26 Diamond 32", "Global System v26 Diamond 32"),            # Legacy branding
    (r"Global System v26 Diamond 32", "Global System v26 Diamond 32")                       # Legacy branding
]

def remove_versions(directory):
    """
    Remove versions implementation.
    """
    print(f"🧹 Removing version numbers and legacy branding from {directory}...")
    count = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip .git and other hidden folders
        if ".git" in dirs: dirs.remove(".git")
        if "__pycache__" in dirs: dirs.remove("__pycache__")
            
        for file in files:
            if file.endswith((".py", ".md", ".json", ".sh", ".txt", ".yaml", ".yml")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    new_content = content
                    for pattern, replacement in VERSION_PATTERNS:
                        # Use re.IGNORECASE for branding
                        flags = re.IGNORECASE if "Global System v26 Diamond 32" in pattern else 0
                        new_content = re.sub(pattern, replacement, new_content, flags=flags)
                    
                    # Avoid double replacement "Global System v26 Diamond 32"
                    new_content = new_content.replace("Global System v26 Diamond 32", "Global System v26 Diamond 32")
                    
                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"✅ Updated: {file}")
                        count += 1
                except Exception as e:
                    print(f"⚠️  Skipped {file}: {e}")
                    
    print(f"✨ Completed. Updated {count} files.")

if __name__ == "__main__":
    remove_versions(TARGET_DIR)
