#!/usr/bin/env python
"""
Fix missing app_label declarations in Django models across the codebase.
This script scans for models without app_label in their Meta class and adds them.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAARA_ERP = ROOT / "gaara_erp"


def get_app_label_from_path(file_path: Path) -> str:
    """Extract app label from file path."""
    parts = file_path.relative_to(GAARA_ERP).parts

    # Handle different module structures
    if len(parts) >= 2:
        if parts[0].endswith('_modules'):
            # e.g., core_modules/companies/models.py -> companies
            return parts[1]
        else:
            # e.g., some_app/models.py -> some_app
            return parts[0]

    return parts[0] if parts else "unknown"


def fix_model_app_labels(file_path: Path):
    """Fix missing app_label in models for a single file."""
    if not file_path.exists() or not file_path.name.endswith('.py'):
        return False

    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    # Skip if not a models file
    if 'models.Model' not in content and 'from django.db import models' not in content:
        return False

    app_label = get_app_label_from_path(file_path)

    # Find all model classes and their Meta classes
    model_pattern = re.compile(
        r'class\s+(\w+)\s*\([^)]*models\.Model[^)]*\):\s*\n(.*?)(?=\nclass|\nfrom|\n\n|\Z)',
        re.DOTALL | re.MULTILINE
    )

    changes_made = False

    for match in model_pattern.finditer(content):
        model_name = match.group(1)
        model_body = match.group(2)

        # Check if Meta class exists
        meta_pattern = re.compile(r'(\s+)class Meta:\s*\n(.*?)(?=\n\s{0,4}\S|\Z)', re.DOTALL)
        meta_match = meta_pattern.search(model_body)

        if meta_match:
            indent = meta_match.group(1)
            meta_content = meta_match.group(2)

            # Check if app_label already exists
            if 'app_label' not in meta_content:
                # Add app_label as first line in Meta
                new_meta_content = f"{indent}    app_label = '{app_label}'\n{meta_content}"
                new_meta = f"{indent}class Meta:\n{new_meta_content}"
                content = content.replace(meta_match.group(0), new_meta)
                changes_made = True
                print(f"Added app_label to {model_name} in {file_path}")
        else:
            # No Meta class exists, add one
            # Find the end of the model class (before methods or next class)
            method_pattern = re.compile(r'\n(\s+)def\s+')
            method_match = method_pattern.search(model_body)

            if method_match:
                # Insert Meta before first method
                insert_pos = match.start(2) + method_match.start(1)
                meta_indent = method_match.group(1)
            else:
                # Insert at end of model body
                insert_pos = match.end(2)
                meta_indent = "    "

            new_meta = f"\n{meta_indent}class Meta:\n{meta_indent}    app_label = '{app_label}'\n"
            content = content[:insert_pos] + new_meta + content[insert_pos:]
            changes_made = True
            print(f"Added Meta class with app_label to {model_name} in {file_path}")

    if changes_made:
        try:
            file_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False

    return False


def main():
    """Process all model files in the codebase."""
    fixed_count = 0

    # Find all Python files that might contain models
    for root, dirs, files in os.walk(GAARA_ERP):
        # Skip migrations, __pycache__, .venv
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'migrations']

        for file in files:
            if file.endswith('.py') and ('model' in file.lower() or file == '__init__.py'):
                file_path = Path(root) / file
                if fix_model_app_labels(file_path):
                    fixed_count += 1

    print(f"\nFixed app_label in {fixed_count} files.")


if __name__ == "__main__":
    main()
