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
os, json, sys, datetime

### 📤 Exports
def log(), def generate_readme()

### 💡 Example
```python
# Example usage for readme_generator.py
# from readme_generator import def log()
```
"""

#!/usr/bin/env python3
"""
Module: readme_generator.py

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
    - sys
    - datetime.datetime

### 📤 Exports
- Function: log
    - Function: generate_readme

### 💡 Examples
```python
    # Example usage
    from readme_generator import log
    result = log()
    print(result)
    ```
"""


import os
import json
import sys
from datetime import datetime

# --- CONFIGURATION ---
MEMORY_DIR = ".memory"
REGISTRY_FILE = os.path.join(MEMORY_DIR, "file_registry.json")
README_FILE = "README.md"

def log(message):
    print(f"[ReadmeGen] {message}")

def generate_readme(project_name):
    """Generates a comprehensive README.md from the File Registry."""
    
    if not os.path.exists(REGISTRY_FILE):
        log(f"Registry not found: {REGISTRY_FILE}. Run code_indexer.py first.")
        return

    with open(REGISTRY_FILE, "r") as f:
        registry = json.load(f)
        
    content = f"# {project_name}\n\n"
    content += f"![Powered by Speckit](https://img.shields.io/badge/Powered_by-Speckit_Global System Ultimate-blue)\n"
    content += f"![Sentinel Protected](https://img.shields.io/badge/Security-Sentinel_Protected-green)\n\n"
    
    content += "## 🧠 Autonomous Engineering System\n"
    content += "This project is managed by the **Singularity System Global System Ultimate**.\n"
    content += "*   **Architect:** Speckit Global System Ultimate\n"
    content += "*   **Guard:** Sentinel Global System Ultimate\n\n"
    
    content += "## 📂 Project Structure (Auto-Generated)\n\n"
    
    # Sort files by path
    sorted_files = sorted(registry.keys())
    for file_path in sorted_files:
        # Skip hidden files and meta files
        if file_path.startswith(".") or file_path == README_FILE:
            continue
            
        data = registry[file_path]
        desc = ""
        if "definitions" in data and "classes" in data["definitions"]:
            classes = [c["name"] for c in data["definitions"]["classes"]]
            if classes:
                desc = f" (Contains: {', '.join(classes)})"
        
        content += f"*   `{file_path}`{desc}\n"
            
    content += "\n## 🚀 Getting Started\n"
    content += "1.  **Initialize:** `python3 global/setup_project.py`\n"
    content += "2.  **Analyze:** `python3 global/tools/speckit.py analyze`\n"
    content += "3.  **Verify:** `python3 global/tools/speckit.py verify`\n"

    with open(README_FILE, "w") as f:
        f.write(content)
        
    log(f"Generated {README_FILE}")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Project Documentation"
    generate_readme(name)