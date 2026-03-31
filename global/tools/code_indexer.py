#!/usr/bin/env python3
import os
import ast
import json
from datetime import datetime

# --- CONFIGURATION ---
MEMORY_DIR = ".memory"
INDEX_FILE = os.path.join(MEMORY_DIR, "code_structure.json")
IGNORE_DIRS = {".git", "__pycache__", "venv", "node_modules", ".memory", "global"}

def log(message):
    print(f"[Indexer] {message}")

def get_definitions(file_path):
    """Extracts classes and functions from a Python file."""
    definitions = {"classes": [], "functions": []}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
            
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                definitions["classes"].append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "methods": methods,
                    "docstring": ast.get_docstring(node)
                })
            elif isinstance(node, ast.FunctionDef):
                # Only top-level functions (not methods)
                if not isinstance(node.parent, ast.ClassDef) if hasattr(node, 'parent') else True:
                     definitions["functions"].append({
                        "name": node.name,
                        "lineno": node.lineno,
                        "docstring": ast.get_docstring(node)
                    })
    except Exception as e:
        log(f"Error parsing {file_path}: {e}")
        
    return definitions

def index_project(root_dir):
    """Scans the project and builds the index."""
    index = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files": {}
    }
    
    for root, dirs, files in os.walk(root_dir):
        # Filter ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                
                defs = get_definitions(full_path)
                if defs["classes"] or defs["functions"]:
                    index["files"][rel_path] = defs
                    log(f"Indexed: {rel_path}")

    # Ensure memory dir exists
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
        
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
        
    log(f"Index saved to {INDEX_FILE}")

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    index_project(root)
