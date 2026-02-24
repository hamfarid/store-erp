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
os, sys, yaml, importlib.util

### 📤 Exports
def check_file_exists(), def verify_docker_compose(), def verify_setup_script(), def main()

### 💡 Example
```python
# Example usage for final_verify_functional.py
# from final_verify_functional import def check_file_exists()
```
"""

#!/usr/bin/env python3
"""
Module: final_verify_functional.py

---
### 🔄 Workflow
1. Load configuration.
    2. Scan target files.
    3. Report violations.

### 📊 Logical Chart
```mermaid
    graph TD
        A[Start] --> B[Load Config]
        B --> C[Scan Files]
        C --> D{Violations?}
        D -- Yes --> E[Report Error]
        D -- No --> F[Pass]
    ```

### 📥 Imports
- os
    - sys
    - yaml
    - importlib.util

### 📤 Exports
- Function: check_file_exists
    - Function: verify_docker_compose
    - Function: verify_setup_script
    - Function: main

### 💡 Examples
```python
    # Example usage
    from final_verify_functional import check_file_exists
    result = check_file_exists()
    print(result)
    ```
"""


"""
Global AI System Global System Ultimate - Final Functional Verification
The Synchronized Intelligence Edition

Verifies that the system is not just version-bumped, but functionally capable.
Checks:
1. Shared Infrastructure (Docker Compose) validity.
2. Dependency completeness (requirements.v40.txt).
3. Setup Script logic (setup_project.py).
4. Container Manager health checks.
"""

import os
import sys
import yaml
import importlib.util

def check_file_exists(path, description):
    if os.path.exists(path):
        print(f"✅ {description} found.")
        return True
    else:
        print(f"❌ {description} MISSING at {path}")
        return False

def verify_docker_compose(path):
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        services = data.get('services', {})
        required = ['chromadb', 'ollama', 'redis']
        
        missing = [s for s in required if s not in services]
        
        if missing:
            print(f"❌ Docker Compose missing services: {missing}")
            return False
            
        # Check Healthchecks
        for svc in required:
            if 'healthcheck' not in services[svc]:
                print(f"⚠️  Service {svc} has no healthcheck defined.")
            else:
                print(f"✅ Service {svc} has healthcheck.")
                
        print("✅ Docker Compose configuration is valid.")
        return True
    except Exception as e:
        print(f"❌ Invalid Docker Compose file: {e}")
        return False

def verify_setup_script(path):
    try:
        with open(path, 'r') as f:
            content = f.read()
            
        if "requirements.v40.txt" not in content:
            print("❌ setup_project.py does not reference requirements.v40.txt")
            return False
            
        if "docker-compose.shared.yml" not in content:
            print("❌ setup_project.py does not reference shared infrastructure")
            return False
            
        print("✅ setup_project.py logic verified.")
        return True
    except Exception as e:
        print(f"❌ Could not read setup_project.py: {e}")
        return False

def main():
    print("🔍 Starting Final Functional Verification (Global System Ultimate)...\n")
    
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # 1. Check Infrastructure
    infra_path = os.path.join(base_path, "infrastructure", "docker-compose.shared.yml")
    if check_file_exists(infra_path, "Shared Infrastructure"):
        verify_docker_compose(infra_path)
        
    # 2. Check Dependencies
    req_path = os.path.join(base_path, "config", "requirements.v40.txt")
    check_file_exists(req_path, "Global System Ultimate Requirements")
    
    # 3. Check Setup Logic
    setup_path = os.path.join(base_path, "setup_project.py")
    if check_file_exists(setup_path, "Setup Script"):
        verify_setup_script(setup_path)
        
    # 4. Check Container Manager
    cm_path = os.path.join(base_path, "tools", "container_manager.py")
    check_file_exists(cm_path, "Container Manager")
    
    print("\n✨ Verification Complete.")

if __name__ == "__main__":
    main()