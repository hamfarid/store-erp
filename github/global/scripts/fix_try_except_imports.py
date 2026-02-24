#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix imports that were incorrectly placed inside try blocks
"""

import re
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent
routes_dir = project_root / "backend" / "src" / "routes"

# Files to fix
FILES_TO_FIX = [
    'batch_management.py',
    'batch_reports.py',
    'excel_import.py',
    'excel_import_clean.py',
    'lot_management.py',
    'security_system.py',
]

def fix_file(filepath: Path) -> tuple[bool, str]:
    """Fix a single file"""
    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content
        
        # Pattern: try:\n    from flask import ...\n\n# P0.2.4: Import error envelope helpers\nfrom src.middleware...
        # This is WRONG - the import is inside the try block
        
        # Find the pattern
        pattern = r'(try:\s*\n\s*from flask import[^\n]+\n)\s*\n# P0\.2\.4: Import error envelope helpers\nfrom src\.middleware\.error_envelope_middleware import \(\s*\n\s*success_response,\s*\n\s*error_response,\s*\n\s*ErrorCodes\s*\n\)\s*\n(except ImportError:)'
        
        # Replacement: move the import AFTER the except block
        def replace_func(match):
            try_block = match.group(1)
            except_line = match.group(2)
            
            return f'''{try_block}{except_line}
    # Fallback when Flask is not available
    class Blueprint:
        def __init__(self, *args, **kwargs):
            pass

        def route(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

    def jsonify(data):
        return {{"data": data}}

    class request:
        args = {{}}

# P0.2.4: Import error envelope helpers
try:
    from src.middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes
    )
except ImportError:
    # Fallback when middleware is not available
    def success_response(data=None, message='Success', code='SUCCESS', status_code=200):
        return {{"success": True, "data": data, "message": message}}, status_code
    
    def error_response(message, code=None, details=None, status_code=400):
        return {{"success": False, "message": message, "code": code}}, status_code
    
    class ErrorCodes:
        SYS_INTERNAL_ERROR = 'SYS_001'
'''
        
        content = re.sub(pattern, replace_func, content, flags=re.MULTILINE)
        
        if content != original_content:
            filepath.write_text(content, encoding='utf-8')
            return True, f"✅ {filepath.name}: Fixed"
        else:
            return False, f"⏭️  {filepath.name}: No changes needed"
            
    except Exception as e:
        return False, f"❌ {filepath.name}: Error - {str(e)}"

def main():
    """Main function"""
    print("=" * 80)
    print("Fix Try/Except Import Issues")
    print("=" * 80)
    print()
    
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for filename in FILES_TO_FIX:
        filepath = routes_dir / filename
        if not filepath.exists():
            print(f"⚠️  {filename}: File not found")
            error_count += 1
            continue
        
        success, message = fix_file(filepath)
        print(message)
        
        if success:
            fixed_count += 1
        elif "No changes" in message:
            skipped_count += 1
        else:
            error_count += 1
    
    print()
    print("=" * 80)
    print(f"Summary:")
    print(f"  ✅ Fixed: {fixed_count}")
    print(f"  ⏭️  Skipped: {skipped_count}")
    print(f"  ❌ Errors: {error_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()

