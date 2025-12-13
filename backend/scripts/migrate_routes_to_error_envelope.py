# FILE: backend/scripts/migrate_routes_to_error_envelope.py | PURPOSE: P0.2.4 - Auto-migrate routes to error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

"""
P0.2.4: Automated Migration Script for Error Envelope
Converts all route files to use unified error envelope format
"""

import re
import sys
from pathlib import Path

# Add backend/src to path
backend_dir = Path(__file__).parent.parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))


def add_error_envelope_imports(content: str) -> str:
    """Add error envelope imports to file if not present"""
    if "error_envelope_middleware" in content:
        return content  # Already has imports

    # Find the import section (after docstring, before blueprint creation)
    import_pattern = r"(from flask import.*?\n)"

    error_envelope_imports = """
# P0.2.4: Import error envelope helpers
try:
    from ..middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes
    )
except ImportError:
    from middleware.error_envelope_middleware import (
        success_response,
        error_response,
        ErrorCodes
    )

"""

    # Insert after Flask imports
    content = re.sub(import_pattern, r"\1" + error_envelope_imports, content, count=1)
    return content


def migrate_success_responses(content: str) -> str:
    """Convert jsonify success responses to success_response()"""

    # Pattern 1: jsonify({'success': True, 'data': ..., 'message': ...})
    pattern1 = r"jsonify\(\s*\{\s*['\"]success['\"]:\s*True,\s*['\"]data['\"]:\s*([^,}]+),\s*['\"]message['\"]:\s*(['\"][^'\"]+['\"])\s*\}\s*\)"
    replacement1 = r"success_response(data=\1, message=\2, status_code=200)"
    content = re.sub(pattern1, replacement1, content)

    # Pattern 2: jsonify({'success': True, 'message': ...})
    pattern2 = r"jsonify\(\s*\{\s*['\"]success['\"]:\s*True,\s*['\"]message['\"]:\s*(['\"][^'\"]+['\"])\s*\}\s*\)"
    replacement2 = r"success_response(message=\1, status_code=200)"
    content = re.sub(pattern2, replacement2, content)

    # Pattern 3: jsonify({'success': True, 'data': ...})
    pattern3 = r"jsonify\(\s*\{\s*['\"]success['\"]:\s*True,\s*['\"]data['\"]:\s*([^}]+)\s*\}\s*\)"
    replacement3 = r"success_response(data=\1, message='Success', status_code=200)"
    content = re.sub(pattern3, replacement3, content)

    return content


def migrate_error_responses(content: str) -> str:
    """Convert jsonify error responses to error_response()"""

    # Pattern 1: jsonify({'success': False, 'error': ..., 'message': ...}), 400
    pattern1 = r"jsonify\(\s*\{\s*['\"]success['\"]:\s*False,\s*['\"]error['\"]:\s*([^,}]+),\s*['\"]message['\"]:\s*(['\"][^'\"]+['\"])\s*\}\s*\),\s*(\d+)"
    replacement1 = r"error_response(message=\2, code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=\3)"
    content = re.sub(pattern1, replacement1, content)

    # Pattern 2: jsonify({'success': False, 'message': ...}), 400
    pattern2 = r"jsonify\(\s*\{\s*['\"]success['\"]:\s*False,\s*['\"]message['\"]:\s*(['\"][^'\"]+['\"])\s*\}\s*\),\s*(\d+)"

    def get_error_code(match):
        status_code = match.group(2)
        code_map = {
            "400": "ErrorCodes.VAL_INVALID_FORMAT",
            "401": "ErrorCodes.AUTH_INVALID_CREDENTIALS",
            "403": "ErrorCodes.AUTH_INSUFFICIENT_PERMISSIONS",
            "404": "ErrorCodes.DB_NOT_FOUND",
            "500": "ErrorCodes.SYS_INTERNAL_ERROR",
        }
        code = code_map.get(status_code, "ErrorCodes.SYS_INTERNAL_ERROR")
        return f"error_response(message={match.group(1)}, code={code}, status_code={status_code})"

    content = re.sub(pattern2, get_error_code, content)

    # Pattern 3: jsonify({'success': False, 'error': ...}), 500
    pattern3 = r"jsonify\(\s*\{\s*['\"]success['\"]:\s*False,\s*['\"]error['\"]:\s*([^}]+)\s*\}\s*\),\s*(\d+)"
    replacement3 = r"error_response(message=\1, code=ErrorCodes.SYS_INTERNAL_ERROR, status_code=\2)"
    content = re.sub(pattern3, replacement3, content)

    return content


def add_file_header(content: str, filename: str) -> str:
    """Add file header if not present"""
    if content.startswith("# FILE:"):
        return content  # Already has header

    header = f"""# FILE: backend/src/routes/{filename} | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

"""
    return header + content


def migrate_route_file(filepath: Path) -> tuple[bool, str]:
    """
    Migrate a single route file to use error envelope

    Returns:
        (success, message)
    """
    try:
        # Read file
        content = filepath.read_text(encoding="utf-8")
        original_content = content

        # Add file header
        content = add_file_header(content, filepath.name)

        # Add imports
        content = add_error_envelope_imports(content)

        # Migrate responses
        content = migrate_success_responses(content)
        content = migrate_error_responses(content)

        # Check if any changes were made
        if content == original_content:
            return True, f"✅ {filepath.name}: Already migrated or no changes needed"

        # Write back
        filepath.write_text(content, encoding="utf-8")

        return True, f"✅ {filepath.name}: Migrated successfully"

    except Exception as e:
        return False, f"❌ {filepath.name}: Error - {str(e)}"


def main():
    """Main migration function"""
    print("=" * 80)
    print("P0.2.4: Automated Route Migration to Error Envelope")
    print("=" * 80)
    print()

    # Find all route files
    routes_dir = src_dir / "routes"
    route_files = list(routes_dir.glob("*.py"))

    # Exclude already migrated files
    exclude_files = {"__init__.py", "auth_routes.py", "mfa_routes.py"}
    route_files = [f for f in route_files if f.name not in exclude_files]

    print(f"Found {len(route_files)} route files to migrate:")
    for f in route_files:
        print(f"  - {f.name}")
    print()

    # Migrate each file
    results = []
    for filepath in route_files:
        success, message = migrate_route_file(filepath)
        results.append((success, message))
        print(message)

    print()
    print("=" * 80)
    print("Migration Summary")
    print("=" * 80)

    successful = sum(1 for s, _ in results if s)
    failed = len(results) - successful

    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")

    if failed > 0:
        print()
        print("Failed files:")
        for success, message in results:
            if not success:
                print(f"  {message}")

    print()
    print("=" * 80)
    print("Next Steps:")
    print("=" * 80)
    print("1. Review migrated files for correctness")
    print("2. Run tests: pytest backend/tests/ -v")
    print("3. Test endpoints manually")
    print("4. Update P0_Implementation_Status.md")
    print()

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
