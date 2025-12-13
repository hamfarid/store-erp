#!/usr/bin/env python3
"""
Script to validate Python syntax for all Python files
"""

import ast
import sys
from pathlib import Path


def validate_python_file(file_path):
    """Validate Python syntax for a single file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to parse the file
        ast.parse(content)
        return True, None

    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def main():
    """Main function to validate all Python files"""
    backend_dir = Path(__file__).parent

    # Files that were fixed
    files_to_check = [
        "check_database.py",
        "fix_formatting.py",
        "flask_server.py",
        "init_db.py",
        "src/database_encryption.py",
        "src/encryption_manager.py",
        "src/https_server.py",
        "src/routes/company_settings.py",
        "src/routes/dashboard.py",
        "src/routes/financial_reports_advanced.py",
        "src/routes/import_export_advanced.py",
        "src/routes/reports.py",
        "src/routes/sales_advanced.py",
        "src/routes/region_warehouse.py",
        "src/app_integrated.py",
        "src/config/production.py",
    ]

    print("🔍 Validating Python syntax...")

    all_valid = True

    for file_name in files_to_check:
        file_path = backend_dir / file_name

        if file_path.exists():
            is_valid, error = validate_python_file(file_path)

            if is_valid:
                print(f"✅ {file_name} - Syntax OK")
            else:
                print(f"❌ {file_name} - {error}")
                all_valid = False
        else:
            print(f"⚠️  {file_name} - File not found")

    if all_valid:
        print("\n🎉 All Python files have valid syntax!")
    else:
        print("\n❌ Some files have syntax errors!")
        sys.exit(1)


if __name__ == "__main__":
    main()
