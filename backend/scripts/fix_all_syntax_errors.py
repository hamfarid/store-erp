# FILE: backend/scripts/fix_all_syntax_errors.py | PURPOSE: Fix all syntax errors in route files | OWNER: Backend | RELATED: routes/*.py | LAST-AUDITED: 2025-10-25

"""
Fix all syntax errors in route files caused by migration script
"""

import re
from pathlib import Path
import sys

# Path to routes directory
routes_dir = Path(__file__).parent.parent / "src" / "routes"

# Find all Python files
route_files = list(routes_dir.glob("*.py"))

print(f"Found {len(route_files)} route files")
print()

fixed_count = 0
error_count = 0

for route_file in route_files:
    try:
        # Read file
        content = route_file.read_text(encoding="utf-8")
        original_content = content

        # Fix pattern 1: return success_response(data=X,\n            'key': value\n        , message=...)
        # This is invalid syntax - positional args after keyword args
        pattern1 = r"return success_response\(data=([^,\n]+),\s*\n\s*'([^']+)':\s*([^,\n]+)\s*\n\s*,\s*message='([^']+)',\s*status_code=(\d+)\)"

        def fix_pattern1(match):
            data_var = match.group(1)
            key = match.group(2)
            value = match.group(3)
            message = match.group(4)
            status = match.group(5)

            return f"""return success_response(
            data={{
                '{key}': {value}
            }},
            message='{message}',
            status_code={status}
        )"""

        content = re.sub(pattern1, fix_pattern1, content)

        # Fix pattern 2: return success_response(data=X\n        , message=...)
        pattern2 = r"return success_response\(data=([^\n]+)\s*\n\s*,\s*message='([^']+)',\s*status_code=(\d+)\)"

        def fix_pattern2(match):
            data_expr = match.group(1)
            message = match.group(2)
            status = match.group(3)

            return f"""return success_response(
            data={data_expr},
            message='{message}',
            status_code={status}
        )"""

        content = re.sub(pattern2, fix_pattern2, content)

        # Fix pattern 3: Unclosed parentheses in success_response
        # Look for success_response( followed by data= but with mismatched parens
        pattern3 = r"return success_response\(data=\{([^}]+)\}\s*\n\s*\}\)"

        def fix_pattern3(match):
            data_content = match.group(1)
            return f"""return success_response(
            data={{{data_content}}},
            message='Success',
            status_code=200
        )"""

        content = re.sub(pattern3, fix_pattern3, content)

        # Check if file was modified
        if content != original_content:
            # Write back
            route_file.write_text(content, encoding="utf-8")
            print(f"✅ Fixed: {route_file.name}")
            fixed_count += 1
        else:
            print(f"⏭️  Skipped: {route_file.name} (no changes needed)")

    except Exception as e:
        print(f"❌ Error in {route_file.name}: {e}")
        error_count += 1

print()
print("=" * 80)
print(f"✅ Fixed: {fixed_count} files")
print(f"⏭️  Skipped: {len(route_files) - fixed_count - error_count} files")
print(f"❌ Errors: {error_count} files")
print("=" * 80)

sys.exit(0 if error_count == 0 else 1)
