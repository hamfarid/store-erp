#!/usr/bin/env python3
"""
Fix double /api prefix in all frontend files
"""
import os
import re
from pathlib import Path

def fix_api_prefix(file_path):
    """Remove /api prefix from apiClient and ApiService calls"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Pattern 1: apiClient.get('/api/...'), apiClient.post('/api/...'), etc.
        pattern1 = r"apiClient\.(get|post|put|delete|patch)\('/api/"
        replacement1 = r"apiClient.\1('/"
        content = re.sub(pattern1, replacement1, content)

        # Pattern 2: ApiService.get('/api/...'), ApiService.post('/api/...'), etc.
        pattern2 = r"ApiService\.(get|post|put|delete|patch)\('/api/"
        replacement2 = r"ApiService.\1('/"
        content = re.sub(pattern2, replacement2, content)

        # Pattern 3: fetch('/api/...') - but keep full URL if it starts with http
        # Only fix relative paths that start with '/api/'
        pattern3 = r"fetch\(\s*['\"]\/api\/"
        replacement3 = r"fetch('/"
        content = re.sub(pattern3, replacement3, content)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    frontend_src = Path('frontend/src')
    files_fixed = 0

    # Process all .js and .jsx files
    for ext in ['*.js', '*.jsx']:
        for file_path in frontend_src.rglob(ext):
            if fix_api_prefix(file_path):
                print(f"✅ Fixed: {file_path}")
                files_fixed += 1

    print(f"\n🎉 Total files fixed: {files_fixed}")

if __name__ == '__main__':
    main()

