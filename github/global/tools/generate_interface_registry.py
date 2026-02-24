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
os, ast, re

### 📤 Exports
def analyze_file(), def generate_registry()

### 💡 Example
```python
# Example usage for generate_interface_registry.py
# from generate_interface_registry import def analyze_file()
```
"""

#!/usr/bin/env python3
"""
Module: generate_interface_registry.py

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
    - re

### 📤 Exports
- Function: analyze_file
    - Function: generate_registry

### 💡 Examples
```python
    # Example usage
    from generate_interface_registry import analyze_file
    result = analyze_file()
    print(result)
    ```
"""


"""
Interface Registry Generator (Global System v26 Diamond 32)
Scans all Python modules and generates a single Markdown reference table.
"""

import os
import ast
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(ROOT_DIR, "docs", "MODULE_INTERFACES.md")

def analyze_file(file_path):
    """
    Analyze file implementation.
    """
    with open(file_path, 'r') as f:
        try:
            content = f.read()
            tree = ast.parse(content)
        except:
            return None

    imports = []
    exports = []
    workflow = "Standard Execution"

    # Extract Docstring Workflow if present
    docstring = ast.get_docstring(tree)
    if docstring:
        match = re.search(r'### 🔄 Workflow\n(.*?)(###|$)', docstring, re.DOTALL)
        if match:
            workflow = match.group(1).strip().replace('\n', '<br>')

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")
        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):
                exports.append(f"func: {node.name}")
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                exports.append(f"class: {node.name}")

    return {
        "imports": imports[:5], # Limit to top 5 for readability
        "exports": exports[:5],
        "workflow": workflow
    }

def generate_registry():
    """
    Generate registry implementation.
    """
    print("🔍 Scanning modules for Interface Registry...")
    
    content = "# 📚 Unified Module Interface Registry (Global System v26 Diamond 32)\n\n"
    content += "| Module | Imports (Inputs) | Exports (Outputs) | Workflow |\n"
    content += "|---|---|---|---|\n"
    
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ROOT_DIR)
                
                data = analyze_file(full_path)
                if data:
                    imps = "<br>".join(data['imports']) or "None"
                    exps = "<br>".join(data['exports']) or "None"
                    wf = data['workflow']
                    
                    content += f"| `{rel_path}` | {imps} | {exps} | {wf} |\n"

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(content)
        
    print(f"✅ Registry Generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_registry()
