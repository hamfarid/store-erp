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
os, json, datetime

### 📤 Exports
def generate_inventory()

### 💡 Example
```python
# Example usage for generate_inventory.py
# from generate_inventory import def generate_inventory()
```
"""

#!/usr/bin/env python3
"""
Module: generate_inventory.py

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
    - json
    - datetime

### 📤 Exports
- Function: generate_inventory

### 💡 Examples
```python
    # Example usage
    from generate_inventory import generate_inventory
    result = generate_inventory()
    print(result)
    ```
"""


"""
Inventory Generator (Global System Ultimate)
Creates a comprehensive map of all files and folders in the project.
"""

import os
import json
import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_FILE = os.path.join(ROOT_DIR, "INVENTORY.md")
JSON_INVENTORY = os.path.join(ROOT_DIR, "MEMORY", "FILE_MAP.json")

IGNORE_DIRS = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'env'}

def generate_inventory():
    inventory = []
    file_tree = {}
    
    print(f"🔍 Scanning project from: {ROOT_DIR}")
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Filter ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        rel_path = os.path.relpath(root, ROOT_DIR)
        if rel_path == ".":
            rel_path = ""
            
        for file in files:
            if file in {'.DS_Store'}:
                continue
                
            full_path = os.path.join(root, file)
            rel_file_path = os.path.join(rel_path, file)
            
            # Get file stats
            stats = os.stat(full_path)
            size_kb = stats.st_size / 1024
            mod_time = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            entry = {
                "path": rel_file_path,
                "size_kb": round(size_kb, 2),
                "last_modified": mod_time,
                "type": os.path.splitext(file)[1]
            }
            
            inventory.append(entry)
            
            # Build tree structure
            parts = rel_file_path.split(os.sep)
            current_level = file_tree
            for part in parts[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            current_level[parts[-1]] = "FILE"

    # Write Markdown Inventory
    with open(INVENTORY_FILE, 'w') as f:
        f.write(f"# 📦 Project Inventory (Generated: {datetime.datetime.now()})\n\n")
        f.write("| File Path | Size (KB) | Last Modified | Type |\n")
        f.write("|---|---|---|---|\n")
        for item in sorted(inventory, key=lambda x: x['path']):
            f.write(f"| `{item['path']}` | {item['size_kb']} | {item['last_modified']} | {item['type']} |\n")
            
    # Write JSON Memory
    os.makedirs(os.path.join(ROOT_DIR, "MEMORY"), exist_ok=True)
    with open(JSON_INVENTORY, 'w') as f:
        json.dump({"generated_at": str(datetime.datetime.now()), "files": inventory, "tree": file_tree}, f, indent=2)
        
    print(f"✅ Inventory generated: {INVENTORY_FILE}")
    print(f"✅ Memory updated: {JSON_INVENTORY}")

if __name__ == "__main__":
    generate_inventory()