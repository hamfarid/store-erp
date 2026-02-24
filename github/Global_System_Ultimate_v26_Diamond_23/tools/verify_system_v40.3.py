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
json, os, sys, pathlib

### 📤 Exports
def verify_mcp_config(), def verify_requirements()

### 💡 Example
```python
# Example usage for verify_system_Global System Ultimate.py
# from verify_system_Global System Ultimate import def verify_mcp_config()
```
"""

import json
import os
import sys
from pathlib import Path

def verify_mcp_config():
    config_path = Path("mcp_config.json")
    if not config_path.exists():
        print("❌ mcp_config.json not found!")
        return False
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        servers = config.get("mcpServers", {})
        required_servers = [
            "sequential-thinking",
            "sequentialthinking-tools",
            "context7",
            "serena",
            "memory",
            "filesystem",
            "postgres",
            "github",
            "brave-search",
            "sentry",
            "playwright"
        ]
        
        missing = [s for s in required_servers if s not in servers]
        
        if missing:
            print(f"❌ Missing MCP servers: {', '.join(missing)}")
            return False
            
        # Verify specific configs
        if servers["postgres"]["args"][2] != "postgresql://user:password@localhost/Global System Ultimate_erp":
            print("❌ Postgres connection string mismatch")
            return False
            
        if servers["sequentialthinking-tools"]["env"]["MAX_HISTORY_SIZE"] != "1000":
            print("❌ Sequential Thinking MAX_HISTORY_SIZE mismatch")
            return False
            
        print("✅ MCP Configuration Verified")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying MCP config: {e}")
        return False

def verify_requirements():
    req_path = Path("config/requirements.v40.txt")
    if not req_path.exists():
        print("❌ requirements.v40.txt not found!")
        return False
        
    with open(req_path) as f:
        content = f.read()
        
    required_packages = [
        "mcp>=0.1.0",
        "fastmcp>=0.1.0",
        "uv>=0.1.0",
        "camoufox[geoip]",
        "redis",
        "passlib"
    ]
    
    missing = [p for p in required_packages if p.split('[')[0].split('>')[0] not in content]
    
    if missing:
        print(f"❌ Missing requirements: {', '.join(missing)}")
        return False
        
    print("✅ Requirements Verified")
    return True

if __name__ == "__main__":
    print("🔍 Starting System Verification Global System Ultimate...")
    mcp_ok = verify_mcp_config()
    req_ok = verify_requirements()
    
    if mcp_ok and req_ok:
        print("\n✨ SYSTEM VERIFICATION PASSED ✨")
        sys.exit(0)
    else:
        print("\n💀 SYSTEM VERIFICATION FAILED 💀")
        sys.exit(1)