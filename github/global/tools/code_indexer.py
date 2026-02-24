"""
### 📊 Logical Chart (Create -> Verify -> Execute)
```mermaid
flowchart TD
    Start([Start]) --> Order[1. Order Requirements]
    Order --> Create[2. Create Artifacts]
    Create --> Verify{3. Verify Success?}
    Verify -- No --> Rollback[Rollback/Fix]
    Rollback --> Create
    Verify -- Yes --> Execute[4. Execute/Deploy]
    Execute --> End([End])
```

### 🔄 Workflow
1.  **Order**: Define prerequisites and inputs.
2.  **Create**: Generate the output (file, data, resource).
3.  **Verify**: Check if the output meets standards (Syntax, Logic, Compliance).
4.  **Execute**: Apply the change or return the result.

### 📥 Imports
os, ast, json, sys, datetime

### 📤 Exports
def log(), def get_definitions(), def update_registry(), def index_project()

### 💡 Example
```python
# Example usage for code_indexer.py
# from code_indexer import def log()
```
"""

#!/usr/bin/env python3
"""
Module: code_indexer.py

---
### 🔄 Workflow
1. Initialize module.
    2. Process inputs.
    3. Return results.

### 📊 Logical Chart
```mermaid
    graph TD
        A[Start] --> B{Process}
        B -->|Success| C[End]
    ```

### 📥 Imports
- os
    - ast
    - json
    - sys
    - datetime.datetime

### 📤 Exports
- Function: log
    - Function: get_definitions
    - Function: update_registry
    - Function: index_project

### 💡 Examples
```python
    # Example usage
    from code_indexer import log
    result = log()
    print(result)
    ```
"""


import os
import ast
import json
import sys
from datetime import datetime

# --- CONFIGURATION ---
MEMORY_DIR = ".memory"
REGISTRY_FILE = os.path.join(MEMORY_DIR, "file_registry.json")
IGNORE_DIRS = {".git", "__pycache__", "venv", "node_modules", ".memory", "global"}

def log(message):
    """
    Log implementation.
    """
    print(f"[Indexer] {message}")

def get_definitions(file_path):
    """Extracts classes, functions, imports, and docstrings."""
    definitions = {"classes": [], "functions": [], "imports": []}
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
                if not isinstance(node.parent, ast.ClassDef) if hasattr(node, 'parent') else True:
                    definitions["functions"].append({
                        "name": node.name,
                        "lineno": node.lineno,
                        "docstring": ast.get_docstring(node)
                    })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    definitions["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ""
                for alias in node.names:
                    definitions["imports"].append(f"{module}.{alias.name}")

    except Exception as e:
        # Non-fatal for non-Python files or syntax errors
        pass
        
    return definitions

def update_registry(index_data):
    """Updates the file_registry.json file."""
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)

    registry = {}
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, 'r') as f:
                registry = json.load(f)
        except json.JSONDecodeError:
            pass

    # Merge new data
    for path, data in index_data.items():
        registry[path] = {
            "last_indexed": datetime.now().isoformat(),
            "definitions": data
        }

    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    log(f"Updated {REGISTRY_FILE}")

def index_project(root_dir):
    """Scans the project and builds the index."""
    index_data = {}
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_dir)
            
            if file.endswith(".py"):
                defs = get_definitions(full_path)
                index_data[rel_path] = defs
                log(f"Indexed: {rel_path}")
            else:
                # Basic indexing for non-Python files
                index_data[rel_path] = {"type": "file"}

    update_registry(index_data)

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    index_project(root)
