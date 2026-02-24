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
hashlib, ast, os, sys

### 📤 Exports
def hash_function(), def scan_project()

### 💡 Example
```python
# Example usage for code_dna.py
# from code_dna import def hash_function()
```
"""

#!/usr/bin/env python3
"""
Module: code_dna.py

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
- hashlib
    - ast
    - os
    - sys

### 📤 Exports
- Function: hash_function
    - Function: scan_project

### 💡 Examples
```python
    # Example usage
    from code_dna import hash_function
    result = hash_function()
    print(result)
    ```
"""


"""
Code DNA (Global System Ultimate)
Fingerprints functions to detect duplicates across projects.
"""

import hashlib
import ast
import os
import sys

def hash_function(node):
    """Hashes the AST of a function (ignoring comments/formatting)."""
    code_str = ast.dump(node)
    return hashlib.md5(code_str.encode()).hexdigest()

def scan_project(path):
    fingerprints = {}
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    try:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                h = hash_function(node)
                                fingerprints[h] = f"{filepath}::{node.name}"
                    except:
                        pass
    return fingerprints

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 code_dna.py <project_path>")
        sys.exit(1)
        
    dna = scan_project(sys.argv[1])
    print(f"🧬 Found {len(dna)} unique functions.")
    # In a real system, we'd compare this against the Global Vector DB