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
os, sys, time, subprocess, json, shutil, rag_engine, container_manager, socket

### 📤 Exports
def clear_screen(), def print_header(), def get_docker_status(), def get_rag_status(), def show_dashboard(), def main()

### 💡 Example
```python
# Example usage for mission_control.py
# from mission_control import def clear_screen()
```
"""

#!/usr/bin/env python3
"""
Module: mission_control.py

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
    - time
    - subprocess
    - json
    - shutil
    - rag_engine.RAGEngine
    - container_manager.get_system_resources
    - socket

### 📤 Exports
- Function: clear_screen
    - Function: print_header
    - Function: get_docker_status
    - Function: get_rag_status
    - Function: show_dashboard
    - Function: main

### 💡 Examples
```python
    # Example usage
    from mission_control import clear_screen
    result = clear_screen()
    print(result)
    ```
"""


"""
Mission Control (Global System Ultimate Swarm Intelligence)
The Unified Dashboard for Global AI System.
Manages Docker, RAG, MCP, and System Health from a single TUI.
"""

import os
import sys
import time
import subprocess
import json
import shutil

# Import Tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from rag_engine import RAGEngine
    from container_manager import get_system_resources
except ImportError:
    pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   🌌 GLOBAL AI SYSTEM - MISSION CONTROL (Global System Ultimate Sentient)     ║")
    print("╚══════════════════════════════════════════════════════════════╝")

def get_docker_status():
    try:
        output = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}"], text=True)
        containers = output.strip().split('\n')
        return [c for c in containers if c]
    except:
        return []

def get_rag_status():
    try:
        # Simple check if port 8000 is open
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', 8000)) == 0:
                return "✅ Online (ChromaDB Active)"
        return "❌ Offline"
    except:
        return "❓ Unknown"

def show_dashboard():
    clear_screen()
    print_header()
    
    # System Stats
    try:
        # Mocking resource check if module missing
        if 'get_system_resources' in globals():
            res = get_system_resources()
            mem = res.get("ram_gb", 0)
            cpu = res.get("cpu_cores", 0)
            print(f"\n📊 SYSTEM RESOURCES: CPU: {cpu} Cores | RAM: {int(mem)}GB")
        else:
            print("\n📊 SYSTEM RESOURCES: (Module not loaded)")
    except:
        pass

    # Docker Status
    containers = get_docker_status()
    print(f"\n🐳 ACTIVE CONTAINERS ({len(containers)}):")
    if containers:
        for c in containers:
            print(f"   - {c}")
    else:
        print("   (No containers running)")

    # RAG Status
    print(f"\n🧠 RAG ENGINE: {get_rag_status()}")

    # Menu
    print("\n🎮 COMMANDS:")
    print("   1. [S]tart Global Infrastructure (Genesis)")
    print("   2. [T]une Containers (Auto-Tune)")
    print("   3. [M]anage MCP Tools")
    print("   4. [V]iew System Log")
    print("   5. [Q]uit")

def main():
    while True:
        show_dashboard()
        choice = input("\n👉 Select Command: ").strip().lower()
        
        if choice in ['q', 'quit', '5']:
            print("👋 Exiting Mission Control.")
            break
        elif choice in ['s', 'start', '1']:
            print("\n🚀 Starting Infrastructure...")
            os.system("python3 global/genesis.py")
            input("\nPress Enter to continue...")
        elif choice in ['t', 'tune', '2']:
            print("\n⚖️  Auto-Tuning...")
            os.system("python3 global/tools/auto_tune.py")
            input("\nPress Enter to continue...")
        elif choice in ['m', 'mcp', '3']:
            os.system("python3 global/tools/mcp_manager.py list")
            input("\nPress Enter to continue...")
        elif choice in ['v', 'view', '4']:
            os.system("tail -n 20 global/system_log.md")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()