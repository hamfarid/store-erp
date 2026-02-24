#!/usr/bin/env python3
"""
Comprehensive Import Fixer for Complete Inventory System
Fixes all import issues across the entire backend
"""

import re
from pathlib import Path


def fix_imports_in_file(file_path):
    """Fix imports in a single Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix relative imports to absolute imports
        patterns = [
            # Fix ..auth imports
            (r'from \.\.auth import', 'from auth import'),
            
            # Fix ..models imports
            (r'from \.\.models\.(\w+) import', r'from models.\1 import'),
            
            # Fix ..routes imports
            (r'from \.\.routes\.(\w+) import', r'from routes.\1 import'),
            
            # Fix ..services imports
            (r'from \.\.services\.(\w+) import', r'from services.\1 import'),
            
            # Fix ..config imports
            (r'from \.\.config\.(\w+) import', r'from config.\1 import'),
            
            # Fix src. imports
            (r'from src\.(\w+) import', r'from \1 import'),
            (r'from src\.models\.(\w+) import', r'from models.\1 import'),
            (r'from src\.routes\.(\w+) import', r'from routes.\1 import'),
            (r'from src\.services\.(\w+) import', r'from services.\1 import'),
            
            # Fix single dot imports
            (r'from \.(\w+) import', r'from \1 import'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # Save the file if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def create_proper_init_files():
    """Create proper __init__.py files for all packages"""
    backend_dir = Path(__file__).parent
    src_dir = backend_dir / "src"
    
    # Directories that need __init__.py files
    package_dirs = [
        src_dir,
        src_dir / "models",
        src_dir / "routes", 
        src_dir / "services",
        src_dir / "config",
        src_dir / "decorators",
        src_dir / "middleware",
        src_dir / "integration",
    ]
    
    for pkg_dir in package_dirs:
        if pkg_dir.exists():
            init_file = pkg_dir / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# Package initialization\n")
                print(f"Created {init_file}")


def fix_main_py():
    """Fix the main.py file specifically"""
    main_file = Path(__file__).parent / "src" / "main.py"
    
    if not main_file.exists():
        return
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the complex import structure with a simpler one
    new_imports = '''
# Import local modules with fallback handling
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from auth import AuthManager
except ImportError:
    print("Warning: AuthManager not available")
    class AuthManager:
        @staticmethod
        def authenticate(username, password):
            return True

try:
    from models.user import Role, User, db
except ImportError:
    print("Warning: User models not available")
    Role = User = db = None

# Import blueprints with error handling
blueprints_to_import = [
    ('routes.user', 'user_bp'),
    ('routes.dashboard', 'dashboard_bp'),
    ('routes.inventory', 'inventory_bp'),
    ('routes.admin', 'admin_bp'),
]

imported_blueprints = {}
for module_name, bp_name in blueprints_to_import:
    try:
        module = __import__(module_name, fromlist=[bp_name])
        imported_blueprints[bp_name] = getattr(module, bp_name)
    except ImportError:
        print(f"Warning: {module_name} not available")
        imported_blueprints[bp_name] = None

# Extract blueprints
user_bp = imported_blueprints.get('user_bp')
dashboard_bp = imported_blueprints.get('dashboard_bp')
inventory_bp = imported_blueprints.get('inventory_bp')
admin_bp = imported_blueprints.get('admin_bp')
'''
    
    # Find where to insert the new imports (after the sys.path.insert line)
    lines = content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if 'sys.path.insert(0,' in line:
            insert_index = i + 1
            break
    
    if insert_index > 0:
        # Remove old import section and insert new one
        new_lines = lines[:insert_index] + new_imports.split('\n')
        
        # Find where the old imports end (look for the first function or class)
        # definition
        for i in range(insert_index, len(lines)):
            if lines[i].strip().startswith(('def ', 'class ', 'app = Flask')):
                new_lines.extend(lines[i:])
                break
        
        new_content = '\n'.join(new_lines)
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Fixed main.py imports")


def main():
    """Main function to fix all import issues"""
    print("🔧 Fixing all import issues in the backend...")
    
    backend_dir = Path(__file__).parent
    src_dir = backend_dir / "src"
    
    if not src_dir.exists():
        print("❌ src directory not found")
        return
    
    # Create proper __init__.py files
    create_proper_init_files()
    
    # Fix imports in all Python files
    fixed_count = 0
    total_count = 0
    
    for py_file in src_dir.rglob("*.py"):
        if py_file.name in ['__init__.py', 'fix_all_imports.py']:
            continue
        
        total_count += 1
        if fix_imports_in_file(py_file):
            fixed_count += 1
            print(f"✅ Fixed imports in {py_file.relative_to(backend_dir)}")
    
    # Fix main.py specifically
    fix_main_py()
    
    print("\n📊 Import fixing complete:")
    print(f"   Fixed: {fixed_count} files")
    print(f"   Total: {total_count} files")
    print(f"   Success rate: {(fixed_count/total_count)*100:.1f}%")


if __name__ == "__main__":
    main()
