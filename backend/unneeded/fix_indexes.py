#!/usr/bin/env python
"""Fix duplicate index definitions in models"""
import re
import os

# Files to fix
model_files = [
    "src/models/enhanced_models.py",
    "src/models/category.py",
    "src/models/invoice.py",
    "src/models/models.py",
    "src/models/refresh_token.py",
    "src/models/supplier.py",
    "src/models/sales_engineer.py",
]

pattern = r"(db\.Column\([^)]*unique=True[^)]*),\s*index=True"
replacement = r"\1"

print("Fixing duplicate index definitions...")
for file_path in model_files:
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Count matches
        matches = len(re.findall(pattern, content))
        if matches > 0:
            print(f"\n{file_path}:")
            print(f"  Found {matches} duplicate index definitions")

            # Replace
            new_content = re.sub(pattern, replacement, content)

            # Write back
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"  ✅ Fixed")
        else:
            print(f"{file_path}: No duplicates found")
    else:
        print(f"❌ File not found: {full_path}")

print("\n✅ All files processed")
