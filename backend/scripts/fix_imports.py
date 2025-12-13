#!/usr/bin/env python3
"""
Fix Import Patterns in Backend Routes
Standardizes all imports to use src. prefix
"""
import os
import re
from pathlib import Path
from typing import Tuple


def fix_database_import(content: str) -> Tuple[str, bool]:
    """Fix: from database import db -> from src.database import db"""
    pattern = r"^from database import db"
    replacement = "from src.database import db"
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    changed = new_content != content
    return new_content, changed


def fix_model_imports(content: str) -> Tuple[str, bool]:
    """Fix: from models.X import Y -> from src.models.X import Y"""
    pattern = r"^from models\.(\w+) import"
    replacement = r"from src.models.\1 import"
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    changed = new_content != content
    return new_content, changed


def fix_auth_imports(content: str) -> Tuple[str, bool]:
    """Fix: from auth import X -> from src.auth import X"""
    pattern = r"^from auth import"
    replacement = "from src.auth import"
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    changed = new_content != content
    return new_content, changed


def fix_file(file_path: Path) -> dict:
    """Apply all import fixes to a single file"""
    results = {
        "file": file_path.name,
        "database_fixed": False,
        "models_fixed": False,
        "auth_fixed": False,
        "total_changes": 0,
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Apply fixes
        content, db_changed = fix_database_import(content)
        results["database_fixed"] = db_changed

        content, model_changed = fix_model_imports(content)
        results["models_fixed"] = model_changed

        content, auth_changed = fix_auth_imports(content)
        results["auth_fixed"] = auth_changed

        # Count total changes
        if content != original_content:
            results["total_changes"] = sum([db_changed, model_changed, auth_changed])

            # Write back
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(
                f"✅ Fixed {file_path.name} ({results['total_changes']} change types)"
            )
            if db_changed:
                print(f"   - Database import")
            if model_changed:
                print(f"   - Model imports")
            if auth_changed:
                print(f"   - Auth imports")

    except Exception as e:
        print(f"❌ Error fixing {file_path.name}: {e}")
        results["error"] = str(e)

    return results


def main():
    """Main execution"""
    print("=" * 60)
    print("Import Pattern Fixer - Backend Routes")
    print("=" * 60)
    print()

    # Get routes directory
    routes_dir = Path(__file__).parent.parent / "src" / "routes"

    if not routes_dir.exists():
        print(f"❌ Routes directory not found: {routes_dir}")
        return

    print(f"📂 Scanning: {routes_dir}")
    print()

    # Process all Python files
    py_files = list(routes_dir.glob("*.py"))
    results = []

    for py_file in sorted(py_files):
        if py_file.name == "__init__.py":
            continue
        result = fix_file(py_file)
        results.append(result)

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    fixed_files = [r for r in results if r["total_changes"] > 0]
    unchanged_files = [r for r in results if r["total_changes"] == 0]
    error_files = [r for r in results if "error" in r]

    print(f"Total files scanned: {len(results)}")
    print(f"✅ Files fixed: {len(fixed_files)}")
    print(f"✔️  Files already correct: {len(unchanged_files)}")
    print(f"❌ Files with errors: {len(error_files)}")
    print()

    if fixed_files:
        print("Files modified:")
        for r in fixed_files:
            print(f"  - {r['file']}")

    if error_files:
        print()
        print("Files with errors:")
        for r in error_files:
            print(f"  - {r['file']}: {r.get('error', 'Unknown error')}")

    print()
    print("✅ Import fix completed!")
    print()
    print("Next steps:")
    print("1. Test application startup: python app.py")
    print(
        "2. Run import tests: python -c 'import sys; sys.path.insert(0, \"src\"); from src.routes import invoices_unified'"
    )
    print(
        "3. Commit changes: git add -A && git commit -m 'fix: Standardize imports to use src. prefix'"
    )


if __name__ == "__main__":
    main()
