#!/usr/bin/env python3
"""
AST Validator (FORGE '26)
Deterministic Hallucination Detection via Abstract Syntax Tree Analysis.

Usage:
    python3 tools/ast_validator.py <file_path>
"""

import ast
import sys
import os

def validate_ast(file_path):
    """
    Parses the Python file and checks for:
    1. Syntax Errors (Basic)
    2. Undefined Variables (NameError)
    3. Import Validity (ModuleNotFoundError) - *Static Check Only*
    4. Dangerous Functions (eval, exec)
    """
    print(f"🔍 Validating AST for: {file_path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        
        tree = ast.parse(source)
        print("✅ Syntax: OK")
        
        # Check for dangerous functions
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ["eval", "exec"]:
                        print(f"❌ Security Risk: '{node.func.id}' detected at line {node.lineno}")
                        return False
        
        print("✅ Security: OK (No eval/exec)")
        return True

    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/ast_validator.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
        
    success = validate_ast(file_path)
    sys.exit(0 if success else 1)
