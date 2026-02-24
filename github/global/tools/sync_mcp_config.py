#!/usr/bin/env python3
"""
Sync MCP Config Tool - Global System v26 Diamond 32
Synchronizes MCP configurations between .vscode/mcp.json and .cursor/mcp.json.
"""

import json
import os
import sys
from pathlib import Path

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

def load_json(path):
    """
    Load json implementation.
    """
    if not path.exists():
        return {}
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {path}")
        return {}

def save_json(path, data):
    """
    Save json implementation.
    """
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved: {path}")
    except Exception as e:
        print(f"❌ Error saving {path}: {e}")

def sync_configs():
    """
    Sync configs implementation.
    """
    print(f"🔄 Syncing MCP Configs ({VERSION})...")
    root_dir = Path(__file__).parent.parent
    vscode_config_path = root_dir / ".vscode" / "mcp.json"
    cursor_config_path = root_dir / ".cursor" / "mcp.json"
    
    print(f"   VS Code: {vscode_config_path}")
    print(f"   Cursor:  {cursor_config_path}")

    vscode_data = load_json(vscode_config_path)
    cursor_data = load_json(cursor_config_path)

    # Merge logic: Union of servers, preferring VS Code if conflict (arbitrary choice, can be changed)
    merged_servers = {}
    
    if "mcpServers" in vscode_data:
        merged_servers.update(vscode_data["mcpServers"])
    
    if "mcpServers" in cursor_data:
        # Only add if not present or update? Let's do a smart merge
        for server, config in cursor_data["mcpServers"].items():
            if server not in merged_servers:
                merged_servers[server] = config
            else:
                # Conflict? For now, keep existing (VS Code priority)
                pass

    final_config = {"mcpServers": merged_servers}

    # Save back to both
    save_json(vscode_config_path, final_config)
    save_json(cursor_config_path, final_config)
    
    print("✨ Sync Complete!")

if __name__ == "__main__":
    sync_configs()
