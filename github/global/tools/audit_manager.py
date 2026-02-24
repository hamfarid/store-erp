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
os, sys, datetime

### 📤 Exports
def generate_inventory(), def load_inventory(), def create_checklist(), def verify_file(), def log_audit(), def main()

### 💡 Example
```python
# Example usage for audit_manager.py
# from audit_manager import def generate_inventory()
```
"""

#!/usr/bin/env python3
"""
Module: audit_manager.py

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
    - datetime

### 📤 Exports
- Function: generate_inventory
    - Function: load_inventory
    - Function: create_checklist
    - Function: verify_file
    - Function: log_audit
    - Function: main

### 💡 Examples
```python
    # Example usage
    from audit_manager import generate_inventory
    result = generate_inventory()
    print(result)
    ```
"""


import os
import sys
import datetime

# --- Configuration ---
# Determine the root directory of the project (one level up from tools/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_FILE = os.path.join(PROJECT_ROOT, "AUDIT_CHECKLIST.md")
INVENTORY_FILE = os.path.join(PROJECT_ROOT, "all_files_inventory.txt")
LOG_FILE = os.path.join(PROJECT_ROOT, "system_log.md")

def generate_inventory():
    """Generates the inventory file dynamically."""
    print(f"🔍 Generating inventory for {PROJECT_ROOT}...")
    inventory = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if ".git" in dirs:
            dirs.remove(".git")  # Skip .git directory
        for file in files:
            # Skip the inventory and checklist files themselves to avoid loops
            if file in ["all_files_inventory.txt", "AUDIT_CHECKLIST.md", "system_log.md"]:
                continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, PROJECT_ROOT)
            inventory.append(rel_path)
            
    with open(INVENTORY_FILE, 'w') as f:
        for item in sorted(inventory):
            f.write(f"{item}\n")
    print(f"✅ Inventory generated: {INVENTORY_FILE}")
    return inventory

def load_inventory():
    """Loads the list of all files in the project."""
    if not os.path.exists(INVENTORY_FILE):
        return generate_inventory()
    
    with open(INVENTORY_FILE, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def create_checklist(files):
    """Creates or updates the AUDIT_CHECKLIST.md file."""
    header = "# 🛡️ Global System Audit Checklist\n\n"
    header += "**Status:** LIVING DOCUMENT\n"
    header += "**Protocol:** Every file MUST be checked before release.\n\n"
    
    existing_checks = {}
    if os.path.exists(AUDIT_FILE):
        with open(AUDIT_FILE, 'r') as f:
            for line in f:
                if line.startswith("- [x]"):
                    try:
                        path = line.split("`")[1]
                        existing_checks[path] = line.strip()
                    except IndexError:
                        pass # Ignore malformed lines

    content = header
    for file_path in sorted(files):
        if file_path in existing_checks:
            content += f"{existing_checks[file_path]}\n"
        else:
            content += f"- [ ] `{file_path}`\n"
    
    with open(AUDIT_FILE, 'w') as f:
        f.write(content)
    print(f"✅ Checklist updated: {AUDIT_FILE}")

def verify_file(file_path, notes="Verified"):
    """Marks a file as verified in the checklist."""
    if not os.path.exists(AUDIT_FILE):
        print(f"❌ Error: {AUDIT_FILE} not found. Run --init first.")
        return

    with open(AUDIT_FILE, 'r') as f:
        lines = f.readlines()

    new_lines = []
    found = False
    for line in lines:
        if f"`{file_path}`" in line:
            new_lines.append(f"- [x] `{file_path}` ({notes})\n")
            found = True
        else:
            new_lines.append(line)
    
    if found:
        with open(AUDIT_FILE, 'w') as f:
            f.writelines(new_lines)
        print(f"✅ Verified: {file_path}")
        log_audit(file_path, notes)
    else:
        print(f"⚠️ Warning: File '{file_path}' not found in checklist.")

def log_audit(file_path, notes):
    """Logs the audit action to system_log.md."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"| {timestamp} | AUDIT | Verified {file_path}: {notes} |\n"
    
    with open(LOG_FILE, 'a') as f:
        f.write(entry)

def main():
    """
    Main implementation.
    """
    if len(sys.argv) < 2:
        print("Usage: python3 audit_manager.py [init|verify <file> <notes>]")
        return

    command = sys.argv[1]
    
    if command == "init":
        files = load_inventory()
        create_checklist(files)
    elif command == "verify":
        if len(sys.argv) < 3:
            print("Usage: python3 audit_manager.py verify <file_path> [notes]")
            return
        file_path = sys.argv[2]
        notes = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "Verified"
        verify_file(file_path, notes)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
