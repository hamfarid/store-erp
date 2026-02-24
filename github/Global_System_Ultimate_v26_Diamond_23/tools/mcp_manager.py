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
sys, os, json, argparse, shutil

### 📤 Exports
def load_config(), def save_config(), def list_servers(), def add_server(), def remove_server(), def scan_for_servers(), def main()

### 💡 Example
```python
# Example usage for mcp_manager.py
# from mcp_manager import def load_config()
```
"""

#!/usr/bin/env python3
"""
Module: mcp_manager.py

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
- sys
    - os
    - json
    - argparse
    - shutil

### 📤 Exports
- Function: load_config
    - Function: save_config
    - Function: list_servers
    - Function: add_server
    - Function: remove_server
    - Function: scan_for_servers
    - Function: main

### 💡 Examples
```python
    # Example usage
    from mcp_manager import load_config
    result = load_config()
    print(result)
    ```
"""


"""
MCP Manager (Global System Ultimate)
Dynamic Registry for Model Context Protocol servers.
Allows adding/removing tools on the fly.
"""

import sys
import os
import json
import argparse
import shutil

# --- CONFIGURATION ---
GLOBAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_CONFIG_FILE = os.path.join(GLOBAL_DIR, "mcp_config.json")

def load_config():
    if os.path.exists(MCP_CONFIG_FILE):
        with open(MCP_CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"mcpServers": {}}

def save_config(config):
    with open(MCP_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ MCP Config updated: {MCP_CONFIG_FILE}")

def list_servers():
    config = load_config()
    servers = config.get("mcpServers", {})
    print("\n🔌 Active MCP Servers:")
    print("=====================")
    if not servers:
        print("   (No servers configured)")
    for name, details in servers.items():
        cmd = details.get("command", "unknown")
        args = " ".join(details.get("args", []))
        print(f"   - {name}: {cmd} {args}")
    print("")

def add_server(name, command, args):
    config = load_config()
    config.setdefault("mcpServers", {})
    
    config["mcpServers"][name] = {
        "command": command,
        "args": args
    }
    save_config(config)
    print(f"✅ Added server '{name}'")

def remove_server(name):
    config = load_config()
    if name in config.get("mcpServers", {}):
        del config["mcpServers"][name]
        save_config(config)
        print(f"✅ Removed server '{name}'")
    else:
        print(f"❌ Server '{name}' not found.")

def scan_for_servers():
    """Scans for common MCP servers installed via npm/pip."""
    print("🔍 Scanning for available MCP servers...")
    
    common_servers = {
        "filesystem": {"cmd": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home"]},
        "github": {"cmd": "npx", "args": ["-y", "@modelcontextprotocol/server-github"]},
        "postgres": {"cmd": "npx", "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/db"]},
        "brave-search": {"cmd": "npx", "args": ["-y", "@modelcontextprotocol/server-brave-search"]}
    }
    
    found = []
    # Heuristic: Check if npm is available
    if shutil.which("npm"):
        print("   - npm detected. Assuming npx-based servers are available.")
        for name, details in common_servers.items():
            found.append((name, details))
    
    if not found:
        print("   (No new servers detected)")
        return

    print("\nFound potential servers:")
    for i, (name, details) in enumerate(found):
        print(f"   {i+1}. {name}")
    
    choice = input("\nEnter number to install (or 'all', 'n'): ").strip()
    if choice == 'n':
        return
    elif choice == 'all':
        for name, details in found:
            add_server(name, details['cmd'], details['args'])
    elif choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(found):
            name, details = found[idx]
            add_server(name, details['cmd'], details['args'])

def main():
    parser = argparse.ArgumentParser(description="MCP Manager")
    parser.add_argument("action", choices=["list", "add", "remove", "scan"], help="Action to perform")
    parser.add_argument("--name", help="Server name")
    parser.add_argument("--cmd", help="Command to run server")
    parser.add_argument("--args", nargs="+", help="Arguments for command")
    
    args = parser.parse_args()
    
    if args.action == "list":
        list_servers()
    elif args.action == "scan":
        scan_for_servers()
    elif args.action == "add":
        if not args.name or not args.cmd:
            print("❌ Error: --name and --cmd required for 'add'")
            sys.exit(1)
        add_server(args.name, args.cmd, args.args or [])
    elif args.action == "remove":
        if not args.name:
            print("❌ Error: --name required for 'remove'")
            sys.exit(1)
        remove_server(args.name)

if __name__ == "__main__":
    main()