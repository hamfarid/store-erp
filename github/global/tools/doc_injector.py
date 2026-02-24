#!/usr/bin/env python3
"""
Doc Injector Global System v26 Diamond 32 (Fix Formatting)
Injects documentation and logical charts that enforce the Create -> Verify -> Execute pattern.
"""

import os
import ast

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Double braces {{ }} for literal braces in f-string/format
TEMPLATE = '''"""
### 📊 Logical Chart (Create -> Verify -> Execute)
```mermaid
flowchart TD
    Start([Start]) --> Order[1. Order Requirements]
    Order --> Create[2. Create Artifacts]
    Create --> Verify{{3. Verify Success?}}
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
{imports}

### 📤 Exports
{exports}

### 💡 Example
```python
{example}
```
"""
'''

def get_imports_exports(file_path):
    """
    Get imports exports implementation.
    """
    with open(file_path, "r") as f:
        try:
            tree = ast.parse(f.read())
        except:
            return "Error parsing imports", "Error parsing exports"
            
    imports = []
    exports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(f"{node.module}")
        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):
                exports.append(f"def {node.name}()")
        elif isinstance(node, ast.ClassDef):
            exports.append(f"class {node.name}")
            
    return ", ".join(imports) or "None", ", ".join(exports) or "None"

def inject_docs():
    """
    Inject docs implementation.
    """
    print("💉 Injecting 'Create-Verify-Execute' Documentation...")
    
    for root, _, files in os.walk(ROOT_DIR):
        if ".git" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file.endswith(".py") and file != "doc_injector.py":
                file_path = os.path.join(root, file)
                imports, exports = get_imports_exports(file_path)
                
                example = f"# Example usage for {file}\n# from {file.replace('.py', '')} import {exports.split(', ')[0] if exports != 'None' else '*'}"
                
                docstring = TEMPLATE.format(imports=imports, exports=exports, example=example)
                
                try:
                    with open(file_path, "r") as f:
                        content = f.read()
                    
                    # Remove old docstring if exists (simple heuristic)
                    if content.strip().startswith('"""') or content.strip().startswith("'''"):
                        end_quote = '"""' if content.strip().startswith('"""') else "'''"
                        parts = content.split(end_quote, 2)
                        if len(parts) >= 3:
                            content = parts[2].strip()
                        else:
                            # Fallback if split fails
                            pass
                    
                    new_content = docstring + "\n" + content
                    
                    # Verify Syntax before saving
                    ast.parse(new_content)
                    
                    with open(file_path, "w") as f:
                        f.write(new_content)
                        
                    print(f"✅ Injected: {file}")
                    
                except Exception as e:
                    print(f"❌ Failed: {file} - {e}")

if __name__ == "__main__":
    inject_docs()
