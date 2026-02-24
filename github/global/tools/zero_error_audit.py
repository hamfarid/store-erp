#!/usr/bin/env python3
"""
Module: zero_error_audit.py
Description: Comprehensive audit tool to ensure the project adheres to the Zero Error policy.
Checks for syntax errors, version mismatches, empty files, and missing docstrings.
"""
import os
import re
import json
import yaml
import ast
import sys
from pathlib import Path

# Configuration
ROOT_DIR = Path(os.getcwd())
TARGET_VERSION = "v26.0 Diamond 32"
# Obfuscate forbidden versions to prevent self-detection
FORBIDDEN_VERSIONS = ["v" + "15.9", "v" + "40", "Diamond " + "30", "Diamond " + "31", "v" + "25"]
REQUIRED_FILES = ["README_FINAL_ZERO_ERROR.md", "setup_project.py", "requirements.txt"]

# Report Data
report = {
    "syntax_errors": [],
    "version_mismatches": [],
    "empty_files": [],
    "missing_docstrings": [],
    "missing_required_files": []
}

def check_python_syntax(file_path):
    """
    Checks Python files for syntax errors using the ast module.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source)
        return True
    except SyntaxError as e:
        report["syntax_errors"].append(f"{file_path}: {e}")
        return False
    except Exception as e:
        report["syntax_errors"].append(f"{file_path}: {e}")
        return False

def check_json_syntax(file_path):
    """
    Checks JSON files for syntax errors.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        report["syntax_errors"].append(f"{file_path}: {e}")
        return False

def check_yaml_syntax(file_path):
    """
    Checks YAML files for syntax errors.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            list(yaml.safe_load_all(f))
        return True
    except yaml.YAMLError as e:
        report["syntax_errors"].append(f"{file_path}: {e}")
        return False

def check_version_mismatch(file_path):
    """
    Checks files for forbidden version strings.
    """
    # Skip checking this file itself to avoid false positives
    if os.path.basename(file_path) == "zero_error_audit.py":
        return

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        for version in FORBIDDEN_VERSIONS:
            if version in content:
                report["version_mismatches"].append(f"{file_path}: Found '{version}'")
                break
    except Exception as e:
        pass

def check_empty_file(file_path):
    """
    Checks if a file is empty.
    """
    if os.path.getsize(file_path) == 0:
        report["empty_files"].append(str(file_path))

def check_docstrings(file_path):
    """
    Checks Python files for missing module, class, and function docstrings.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        
        # Check module docstring
        if not ast.get_docstring(tree):
            report["missing_docstrings"].append(f"{file_path}: Module docstring missing")
            
        # Check function/class docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    # Skip __init__ if class has docstring (optional preference)
                    if node.name == "__init__":
                        continue
                    report["missing_docstrings"].append(f"{file_path}: {node.name} docstring missing")
    except Exception:
        pass

def main():
    """
    Main execution function for the audit tool.
    """
    print(f"🔍 Starting Zero Error Audit on {ROOT_DIR}...")
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip hidden directories and venv
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != "venv" and d != "__pycache__"]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # 1. Check Empty Files
            check_empty_file(file_path)
            
            # 2. Check Syntax & Docstrings
            if file.endswith(".py"):
                check_python_syntax(file_path)
                check_docstrings(file_path)
                check_version_mismatch(file_path)
            elif file.endswith(".json"):
                check_json_syntax(file_path)
                check_version_mismatch(file_path)
            elif file.endswith((".yaml", ".yml")):
                check_yaml_syntax(file_path)
                check_version_mismatch(file_path)
            elif file.endswith((".md", ".txt")):
                check_version_mismatch(file_path)

    # 3. Check Required Files
    for req_file in REQUIRED_FILES:
        if not os.path.exists(os.path.join(ROOT_DIR, req_file)):
            report["missing_required_files"].append(req_file)

    # Save Report
    with open("AUDIT_REPORT.json", "w") as f:
        json.dump(report, f, indent=4)
        
    print("✅ Audit Complete. Report saved to AUDIT_REPORT.json")
    
    # Print Summary
    print("\n📊 Summary:")
    print(f"Syntax Errors: {len(report['syntax_errors'])}")
    print(f"Version Mismatches: {len(report['version_mismatches'])}")
    print(f"Empty Files: {len(report['empty_files'])}")
    print(f"Missing Docstrings: {len(report['missing_docstrings'])}")
    print(f"Missing Required Files: {len(report['missing_required_files'])}")

if __name__ == "__main__":
    main()
