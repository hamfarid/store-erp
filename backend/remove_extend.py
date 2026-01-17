#!/usr/bin/env python
"""Remove extend_existing from all models"""
import re
import os
import glob

pattern = r",\s*'extend_existing':\s*True"

print("Removing 'extend_existing' from models...")
model_files = glob.glob("src/models/*.py")

for file_path in model_files:
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "extend_existing" in content:
            print(f"\n{file_path}:")
            print("  Removing 'extend_existing'...")

            # Remove extend_existing
            new_content = re.sub(pattern, "", content)

            # Write back
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print("  ✅ Done")

print("\n✅ All files processed")
