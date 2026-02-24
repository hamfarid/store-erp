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
os, sys, subprocess, datetime

### 📤 Exports
def log(), def run_speckit(), def run_container_check(), def run_upgrade(), def main()

### 💡 Example
```python
# Example usage for lifecycle.py
# from lifecycle import def log()
```
"""

#!/usr/bin/env python3
"""
Module: lifecycle.py

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
    - datetime.datetime

### 📤 Exports
- Function: log
    - Function: run_speckit
    - Function: run_container_check
    - Function: run_upgrade
    - Function: main

### 💡 Examples
```python
    # Example usage
    from lifecycle import log
    result = log()
    print(result)
    ```
"""


import os
import sys
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
GLOBAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(GLOBAL_ROOT, "tools")
SCRIPTS_DIR = os.path.join(GLOBAL_ROOT, "scripts")

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def run_speckit(command):
    """Executes a Speckit command."""
    tool_path = os.path.join(TOOLS_DIR, "speckit.py")
    cmd = [sys.executable, tool_path, command]
    log(f"Running: speckit.py {command}", "EXEC")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        log(f"Speckit {command} FAILED. Halting Lifecycle.", "CRITICAL")
        sys.exit(1)

def run_container_check(project_path):
    """Executes the Container Manager check."""
    tool_path = os.path.join(TOOLS_DIR, "container_manager.py")
    
    # Check if project has container files
    has_docker = os.path.exists(os.path.join(project_path, "docker-compose.yml"))
    
    if has_docker:
        log("🐳 Container Environment Detected. Initiating Pre-Flight Checks...", "CONTAINER")
        cmd = [sys.executable, tool_path, project_path]
        try:
            subprocess.run(cmd, check=True)
            log("✅ Container Pre-Flight Checks Passed.", "CONTAINER")
        except subprocess.CalledProcessError:
            log("❌ Container Checks FAILED. Fix port conflicts or missing files.", "CRITICAL")
            sys.exit(1)
    else:
        log("ℹ️ No Container Environment Detected. Skipping checks.", "CONTAINER")

def run_upgrade():
    """Executes the upgrade script."""
    script_path = os.path.join(SCRIPTS_DIR, "upgrade_to_v37.sh")
    if os.path.exists(script_path):
        log(f"Running: upgrade_to_v37.sh", "EXEC")
        subprocess.run(["bash", script_path], check=True)
    else:
        log("Upgrade script not found. Skipping.", "WARN")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 lifecycle.py <project_path> [command]")
        print("Commands: start (default), upgrade")
        sys.exit(1)

    project_path = os.path.abspath(sys.argv[1])
    project_name = os.path.basename(project_path)
    command = sys.argv[2] if len(sys.argv) > 2 else "start"
    
    log(f"Starting Singularity Lifecycle Global System Ultimate for: {project_name}", "INIT")
    
    if command == "upgrade":
        log("Phase 0: Upgrade Protocol Initiated", "PHASE")
        run_upgrade()
        log("Upgrade Complete. Verifying System Integrity...", "PHASE")
        run_speckit("verify")
        return

    # Standard Lifecycle (Speckit Global System Ultimate Compliant)
    # 1. Analyze (Context & Registry)
    log("Phase 1: Analysis (Librarian Protocol)", "PHASE")
    run_speckit("analyze")
    
    # 1.5 Container Pre-Flight (NEW)
    run_container_check(project_path)
    
    # 2. Plan (Blueprint)
    log("Phase 2: Planning (Shadow Architect)", "PHASE")
    run_speckit("plan")
    
    # 3. Tasks (Breakdown)
    log("Phase 3: Task Generation", "PHASE")
    run_speckit("tasks")
    
    # 4. Implement (Execution)
    log("Phase 4: Implementation", "PHASE")
    run_speckit("implement")
    
    # 5. Verify (Sentinel)
    log("Phase 5: Verification (Sentinel Guard)", "PHASE")
    run_speckit("verify")

    log("Lifecycle Complete. System is Stable.", "SUCCESS")

if __name__ == "__main__":
    main()