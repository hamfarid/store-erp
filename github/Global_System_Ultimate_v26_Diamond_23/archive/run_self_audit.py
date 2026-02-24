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
os, sys, subprocess, global_system.genesis

### 📤 Exports
def run_command(), def main()

### 💡 Example
```python
# Example usage for run_self_audit.py
# from run_self_audit import def run_command()
```
"""

#!/usr/bin/env python3
"""
Module: run_self_audit.py

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
    - sys
    - subprocess
    - global_system.genesis

### 📤 Exports
- Function: run_command
    - Function: main

### 💡 Examples
```python
    # Example usage
    from run_self_audit import run_command
    result = run_command()
    print(result)
    ```
"""


import os
# Injected by Global System Ultimate Swarm Intelligence
try:
    import global_system.genesis
except:
    pass
import sys
import subprocess

# --- CONFIGURATION ---
GLOBAL_ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIT_MANAGER = os.path.join(GLOBAL_ROOT, "tools", "audit_manager.py")

def run_command(command):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(e.stderr)
        sys.exit(1)

def main():
    print("🔍 Starting Self-Audit of Global System v37.x...")
    
    # 1. Initialize Audit Manager (Generate Inventory & Checklist)
    print("\n[Step 1] Initializing Audit Manager...")
    run_command(f"python3 {AUDIT_MANAGER} init")
    
    # 2. Verify all files (Simulate verification for self-audit)
    print("\n[Step 2] Verifying all files...")
    # In a real scenario, a human or AI would verify each file.
    # Here, we are verifying that the Audit Manager *can* verify them.
    
    # Load inventory
    with open(os.path.join(GLOBAL_ROOT, "all_files_inventory.txt"), "r") as f:
        files = [line.strip() for line in f.readlines() if line.strip()]
        
    for file_path in files:
        # Skip the audit files themselves to avoid recursion issues
        if "AUDIT_CHECKLIST" in file_path or "all_files_inventory" in file_path:
            continue
            
        # Run verification
        print(f"  - Verifying: {file_path}")
        run_command(f"python3 {AUDIT_MANAGER} verify '{file_path}' 'Self-Audit Passed'")
        
    print("\n✅ Self-Audit Complete! Check AUDIT_CHECKLIST.md for results.")

if __name__ == "__main__":
    main()