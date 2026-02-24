#!/usr/bin/env python3
"""
Completeness Checker
Verifies that all functions in a module have type hints and docstrings.

Usage:
    python3 tools/completeness_checker.py <file_path>
"""

import ast
import sys
import os

def get_version():
    try:
        with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "UNKNOWN"

VERSION = get_version()

def check_completeness(file_path):
    print(f"🔍 Checking Completeness for: {file_path} (System v{VERSION})")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check Docstring
                if not ast.get_docstring(node):
                    issues.append(f"Function '{node.name}' missing docstring (Line {node.lineno})")
                
                # Check Return Type Hint
                if node.returns is None and node.name != "__init__":
                    issues.append(f"Function '{node.name}' missing return type hint (Line {node.lineno})")
                
                # Check Argument Type Hints
                for arg in node.args.args:
                    if arg.annotation is None and arg.arg != "self":
                        issues.append(f"Argument '{arg.arg}' in '{node.name}' missing type hint (Line {node.lineno})")

        if issues:
            print(f"❌ Found {len(issues)} completeness issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ Completeness: 100% (All functions typed & documented)")
            return True

    except Exception as e:
        print(f"❌ Error parsing file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/completeness_checker.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
        
    success = check_completeness(file_path)
    sys.exit(0 if success else 1)
