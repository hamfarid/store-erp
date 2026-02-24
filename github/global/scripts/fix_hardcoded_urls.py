#!/usr/bin/env python3
"""
Fix Hardcoded URLs in Frontend Components
Replaces hardcoded API URLs with environment variables
"""

import re
import os
from pathlib import Path

# Files to fix
FILES_TO_FIX = [
    'frontend/src/components/AccountingSystem.jsx',
    'frontend/src/components/LotManagement.jsx',
    'frontend/src/components/StockMovements.jsx',
    'frontend/src/components/WarehousesManagement.jsx',
    'frontend/src/components/CurrencyManagement.jsx',
    'frontend/src/components/ProfitLossReport.jsx',
    'frontend/src/components/PurchaseInvoiceManagement.jsx',
]

# URL patterns to replace
URL_PATTERNS = [
    (r"'http://172\.16\.16\.27:5005/", "API_BASE_URL + '/"),
    (r'"http://172\.16\.16\.27:5005/', 'API_BASE_URL + "/'),
    (r"'http://localhost:5005/api/", "API_BASE_URL + '/"),
    (r'"http://localhost:5005/api/', 'API_BASE_URL + "/'),
]

def add_import_if_missing(content):
    """Add API import if not present"""
    if 'from \'../utils/api\'' in content or 'from "../utils/api"' in content:
        return content
    
    # Find the last import statement
    import_pattern = r'(import .+ from .+[\'"];?\n)'
    imports = list(re.finditer(import_pattern, content))
    
    if imports:
        last_import = imports[-1]
        insert_pos = last_import.end()
        new_import = "import { API_BASE_URL } from '../utils/api';\n"
        content = content[:insert_pos] + new_import + content[insert_pos:]
    
    return content

def fix_file(filepath):
    """Fix hardcoded URLs in a single file"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # Replace URL patterns
    for pattern, replacement in URL_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes_made += len(matches)
    
    if changes_made > 0:
        # Add import if needed
        content = add_import_if_missing(content)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed {filepath}: {changes_made} URLs replaced")
        return True
    else:
        print(f"⏭️  Skipped {filepath}: No hardcoded URLs found")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Hardcoded URLs in Frontend Components\n")
    
    fixed_count = 0
    total_count = len(FILES_TO_FIX)
    
    for filepath in FILES_TO_FIX:
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Total files: {total_count}")
    print(f"   Fixed: {fixed_count}")
    print(f"   Skipped: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ Successfully fixed {fixed_count} files!")
        print(f"\n📝 Next steps:")
        print(f"   1. Review the changes")
        print(f"   2. Test all components")
        print(f"   3. Commit the changes")
    else:
        print(f"\n⏭️  No files needed fixing")

if __name__ == '__main__':
    main()

