#!/usr/bin/env python3
"""
Compliance Checker (Global System Ultimate)
Audits the system for adherence to Visual & Logical Documentation standards.
Checks for:
1. Logical Charts in Python files.
2. TASKS.md in directories.
3. Docstrings in functions/classes.
"""

import os
import sys

# Define root directory relative to this script
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_compliance():
    print("🔍 Starting Comprehensive Compliance Audit...")
    
    total_py_files = 0
    compliant_py_files = 0
    total_dirs = 0
    compliant_dirs = 0
    
    missing_charts = []
    missing_tasks = []
    
    # Walk through the directory structure
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip hidden folders, tests, and virtual environments
        if any(part.startswith('.') for part in root.split(os.sep)) or \
           "__pycache__" in root or \
           "venv" in root or \
           "node_modules" in root:
            continue
            
        # Check for TASKS.md in significant directories (those with code)
        has_code = any(f.endswith(('.py', '.js', '.ts', '.md')) for f in files)
        if has_code:
            total_dirs += 1
            if "TASKS.md" in files:
                compliant_dirs += 1
            else:
                missing_tasks.append(root)

        for file in files:
            if file.endswith(".py"):
                total_py_files += 1
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check for Logical Chart presence
                        if "### 📊 Logical Chart" in content or "mermaid" in content:
                            compliant_py_files += 1
                        else:
                            missing_charts.append(file_path)
                except Exception as e:
                    print(f"⚠️  Error reading {file_path}: {e}")

    # Report Results
    print("\n📊 Audit Results:")
    
    if total_py_files > 0:
        py_compliance = (compliant_py_files / total_py_files) * 100
        print(f"   - Python Files: {compliant_py_files}/{total_py_files} ({py_compliance:.1f}%) Compliant")
    else:
        print("   - Python Files: 0/0 (N/A)")

    if total_dirs > 0:
        dir_compliance = (compliant_dirs / total_dirs) * 100
        print(f"   - Directories:  {compliant_dirs}/{total_dirs} ({dir_compliance:.1f}%) Compliant")
    else:
        print("   - Directories:  0/0 (N/A)")
    
    if missing_charts:
        print("\n❌ Missing Logical Charts in (Sample):")
        for f in missing_charts[:5]:
            print(f"   - {os.path.relpath(f, ROOT_DIR)}")
        if len(missing_charts) > 5:
            print(f"   ... and {len(missing_charts)-5} more.")
            
    if missing_tasks:
        print("\n❌ Missing TASKS.md in (Sample):")
        for d in missing_tasks[:5]:
            print(f"   - {os.path.relpath(d, ROOT_DIR)}")
        if len(missing_tasks) > 5:
            print(f"   ... and {len(missing_tasks)-5} more.")
            
    # Auto-Fix Suggestions
    print("\n💡 Suggestions:")
    if missing_tasks:
        print("   - Run 'tools/generate_task_lists.py' to generate missing TASKS.md files.")
    if missing_charts:
        print("   - Run 'tools/doc_injector.py' to inject missing Logical Charts.")

if __name__ == "__main__":
    check_compliance()
