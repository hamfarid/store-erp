#!/usr/bin/env python3
"""
Fix admin.py inline User class conflict
This script removes the mock User class and uses the real one from models
"""

import re
from pathlib import Path


def fix_admin_py():
    """Fix admin.py to import User from models instead of defining inline"""

    admin_file = Path("src/routes/admin.py")

    if not admin_file.exists():
        print(f"❌ File not found: {admin_file}")
        return False

    content = admin_file.read_text(encoding="utf-8")

    # Check if inline User class exists
    if "class User:" not in content:
        print("✅ No inline User class found - already fixed or not present")
        return True

    print("🔍 Found inline User class (mock) - replacing with real import")

    # Find the inline User class definition (lines 80-100+)
    # Pattern: from "class User:" to the end of the class
    user_class_pattern = r"class User:.*?(?=\n(?:class|def|\Z))"

    # Check if import already exists
    has_import = "from src.models.user import User" in content

    if not has_import:
        # Add import after other imports
        # Find last import line
        import_pattern = r"(from src\..*import.*\n)"
        imports = list(re.finditer(import_pattern, content))

        if imports:
            last_import = imports[-1]
            insert_pos = last_import.end()
            content = (
                content[:insert_pos]
                + "from src.models.user import User\n"
                + content[insert_pos:]
            )
            print("✅ Added: from src.models.user import User")
        else:
            print("⚠️  Could not find import section")
            return False
    else:
        print("✅ Import already exists")

    # Remove the inline User class definition
    # This is a mock class that conflicts with the real User model
    content_before = content
    content = re.sub(user_class_pattern, "", content, flags=re.DOTALL)

    if content != content_before:
        print("✅ Removed inline User class definition")
    else:
        print("⚠️  Could not remove inline User class")
        return False

    # Write back
    admin_file.write_text(content, encoding="utf-8")
    print(f"✅ Fixed {admin_file}")

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Fix Admin.py Inline User Class Conflict")
    print("=" * 60)

    success = fix_admin_py()

    print("\n" + "=" * 60)
    if success:
        print("✅ SUCCESS - admin.py fixed")
        print("\nNext steps:")
        print("1. Test import: python -c 'from src.routes import admin'")
        print("2. Review diff: git diff backend/src/routes/admin.py")
        print("3. Commit: git commit -am 'fix: Remove inline User class in admin.py'")
    else:
        print("❌ FAILED - manual fix required")
        print("\nManual steps:")
        print("1. Open: backend/src/routes/admin.py")
        print("2. Add import: from src.models.user import User")
        print("3. Remove: class User: definition (lines ~80-100)")
    print("=" * 60)
