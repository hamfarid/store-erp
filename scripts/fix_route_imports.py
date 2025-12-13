#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix missing imports in route files
Adds success_response, error_response, ErrorCodes imports to all route files
"""

import re
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent
routes_dir = project_root / "backend" / "src" / "routes"

# Import statement to add
IMPORT_STATEMENT = """
# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes
)
"""

def has_error_envelope_imports(content: str) -> bool:
    """Check if file already has error envelope imports"""
    # Check for actual import statement, not just usage
    return 'from src.middleware.error_envelope_middleware import' in content or \
           'from middleware.error_envelope_middleware import' in content or \
           'from ..middleware.error_envelope_middleware import' in content

def add_imports_after_flask(content: str) -> str:
    """Add imports after Flask imports"""
    # Find Flask import line
    flask_import_pattern = r'(from flask import [^\n]+\n)'
    
    match = re.search(flask_import_pattern, content)
    if not match:
        # No Flask import found, add at top after docstring
        if content.startswith('"""') or content.startswith("'''"):
            # Find end of docstring
            if content.startswith('"""'):
                end_idx = content.find('"""', 3) + 3
            else:
                end_idx = content.find("'''", 3) + 3
            
            return content[:end_idx] + "\n" + IMPORT_STATEMENT + content[end_idx:]
        else:
            # Add at very top
            return IMPORT_STATEMENT + "\n" + content
    
    # Insert after Flask import
    insert_pos = match.end()
    return content[:insert_pos] + IMPORT_STATEMENT + content[insert_pos:]

def fix_route_file(filepath: Path) -> tuple[bool, str]:
    """Fix a single route file"""
    try:
        # Read file
        content = filepath.read_text(encoding='utf-8')
        
        # Check if already has imports
        if has_error_envelope_imports(content):
            return False, f"⏭️  {filepath.name}: Already has imports"
        
        # Add imports
        new_content = add_imports_after_flask(content)
        
        # Write back
        filepath.write_text(new_content, encoding='utf-8')
        
        return True, f"✅ {filepath.name}: Added imports"
        
    except Exception as e:
        return False, f"❌ {filepath.name}: Error - {str(e)}"

def main():
    """Main function"""
    print("=" * 80)
    print("Fix Route Imports - Add error_envelope_middleware imports")
    print("=" * 80)
    print()
    
    # Find all route files
    route_files = list(routes_dir.glob("*.py"))
    
    # Exclude files
    exclude_files = {
        '__init__.py',
        'auth_routes.py',  # Already has imports
        'mfa_routes.py',   # Already has imports
    }
    
    route_files = [f for f in route_files if f.name not in exclude_files]
    
    print(f"Found {len(route_files)} route files to fix:")
    for f in route_files:
        print(f"  - {f.name}")
    print()
    
    # Fix each file
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for filepath in route_files:
        success, message = fix_route_file(filepath)
        print(message)
        
        if success:
            fixed_count += 1
        elif "Already has" in message:
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

