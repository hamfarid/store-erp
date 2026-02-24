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
os, sys, ast

### 📤 Exports
def analyze_python_file(), def generate_readme()

### 💡 Example
```python
# Example usage for doc_updater.py
# from doc_updater import def analyze_python_file()
```
"""

#!/usr/bin/env python3
"""
Module: doc_updater.py

---
### 🔄 Workflow
1. Identify target files.
    2. Apply changes.
    3. Verify updates.

### 📊 Logical Chart
```mermaid
    graph TD
        A[Start] --> B[Find Files]
        B --> C[Apply Update]
        C --> D[Verify]
        D --> E[End]
    ```

### 📥 Imports
- os
    - sys
    - ast

### 📤 Exports
- Function: analyze_python_file
    - Function: generate_readme

### 💡 Examples
```python
    # Example usage
    from doc_updater import analyze_python_file
    result = analyze_python_file()
    print(result)
    ```
"""


"""
Doc Updater (Global System Ultimate)
Self-Updating Documentation Tool.
Reads code structure and updates README.md automatically.
"""

import os
import sys
import ast

def analyze_python_file(filepath):
    """Extracts docstrings and classes from a Python file."""
    with open(filepath, 'r') as f:
        try:
            tree = ast.parse(f.read())
        except:
            return None
            
    docstring = ast.get_docstring(tree)
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    return {
        "doc": docstring,
        "classes": classes,
        "functions": functions
    }

def generate_readme(project_path):
    """Generates a README based on code analysis."""
    readme_path = os.path.join(project_path, "README.md")
    
    content = ["# Project Documentation (Auto-Generated)\n"]
    content.append(f"> Last Updated: {os.popen('date').read().strip()}\n")
    
    content.append("## 📂 Modules\n")
    
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, project_path)
                
                info = analyze_python_file(filepath)
                if info:
                    content.append(f"### `{relpath}`")
                    if info['doc']:
                        content.append(f"{info['doc']}\n")
                    
                    if info['classes']:
                        content.append(f"- **Classes**: {', '.join(info['classes'])}")
                    if info['functions']:
                        content.append(f"- **Functions**: {', '.join(info['functions'])}")
                    content.append("\n")

    with open(readme_path, "w") as f:
        f.write("\n".join(content))
    
    print(f"✅ Updated {readme_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 doc_updater.py <project_path>")
    else:
        generate_readme(sys.argv[1])