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
os, ast, json, datetime

### 📤 Exports
def analyze_file(), def generate_workflows()

### 💡 Example
```python
# Example usage for generate_workflows.py
# from generate_workflows import def analyze_file()
```
"""

#!/usr/bin/env python3
"""
Module: generate_workflows.py

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
    - datetime

### 📤 Exports
- Function: analyze_file
    - Function: generate_workflows

### 💡 Examples
```python
    # Example usage
    from generate_workflows import analyze_file
    result = analyze_file()
    print(result)
    ```
"""


"""
Workflow Generator (Global System Ultimate)
Analyzes Python files to extract function definitions and imports, creating a workflow registry.
"""

import os
import ast
import json
import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW_REGISTRY = os.path.join(ROOT_DIR, "MEMORY", "WORKFLOW_REGISTRY.json")

def analyze_file(file_path):
    with open(file_path, 'r') as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return None

    functions = []
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [a.arg for a in node.args.args],
                "docstring": ast.get_docstring(node) or "No description"
            })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")

    return {
        "functions": functions,
        "imports": list(set(imports))
    }

def generate_workflows():
    registry = {}
    
    print("🧠 Analyzing code structure...")
    
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ROOT_DIR)
                
                analysis = analyze_file(full_path)
                if analysis:
                    registry[rel_path] = analysis
                    
    # Save to Memory
    os.makedirs(os.path.join(ROOT_DIR, "MEMORY"), exist_ok=True)
    with open(WORKFLOW_REGISTRY, 'w') as f:
        json.dump({"generated_at": str(datetime.datetime.now()), "modules": registry}, f, indent=2)
        
    print(f"✅ Workflow Registry updated: {WORKFLOW_REGISTRY}")

if __name__ == "__main__":
    generate_workflows()