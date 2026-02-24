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
os, shutil, argparse

### 📤 Exports
def cleanup()

### 💡 Example
```python
# Example usage for file_cleanup.py
# from file_cleanup import def cleanup()
```
"""

#!/usr/bin/env python3
"""
Module: file_cleanup.py

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
    - shutil
    - argparse

### 📤 Exports
- Function: cleanup

### 💡 Examples
```python
    # Example usage
    from file_cleanup import cleanup
    result = cleanup()
    print(result)
    ```
"""


"""
Aggressive File Cleanup Tool (Global System Ultimate)
Removes temporary files, caches, build artifacts, and legacy v3x files.
"""

import os
import shutil
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Standard Cleanup Targets
TARGETS = [
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".coverage",
    "htmlcov",
    "dist",
    "build",
    "*.egg-info"
]

# Legacy Files to Remove
LEGACY_FILES = [
    "todo_v39.md",
    "v38_roadmap_and_evaluation.md",
    "GAP_ANALYSIS_REPORT_Global System Ultimate.md",
    "VSCODE_STARTUP_PROMPT_Global System Ultimate.md",
    "IRONCLAD_WORKFLOW_Global System Ultimate.md",
    "00_MASTER_Global System Ultimate.md",
    "00_MASTER_Global System Ultimate.md",
    "GLOBAL_PROFESSIONAL_CORE_PROMPT_Global System Ultimate.md"
]

def cleanup(aggressive=False):
    print(f"🧹 Starting cleanup in: {ROOT_DIR}")
    
    deleted_count = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # Remove directories
        for d in dirs:
            if d in TARGETS or (d == "__pycache__") or (d == ".pytest_cache"):
                path = os.path.join(root, d)
                try:
                    shutil.rmtree(path)
                    print(f"   Deleted dir: {path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"   ❌ Failed to delete {path}: {e}")
        
        # Remove files
        for f in files:
            # Check for standard targets
            if f == ".DS_Store" or f.endswith((".pyc", ".pyo", ".pyd", ".tmp", ".bak")):
                path = os.path.join(root, f)
                try:
                    os.remove(path)
                    print(f"   Deleted file: {path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"   ❌ Failed to delete {path}: {e}")
            
            # Check for legacy files
            if f in LEGACY_FILES:
                path = os.path.join(root, f)
                try:
                    os.remove(path)
                    print(f"   🗑️  Removed legacy file: {path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"   ⚠️  Failed to remove {path}: {e}")

    print(f"✨ Cleanup complete. Removed {deleted_count} items.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup project artifacts")
    parser.add_argument("--aggressive", action="store_true", help="Perform deep cleaning")
    args = parser.parse_args()
    
    cleanup(args.aggressive)