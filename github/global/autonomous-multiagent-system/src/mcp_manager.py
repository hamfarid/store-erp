"""
MCP Manager for Autonomous Multi-Agent System

Manages Model Context Protocol (MCP) tools and connections.
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class MCPManager:
    """Manages MCP tools and connections for a specific project"""
    
    def __init__(self, project_name: str):
        """
        Initialize MCP Manager
        
        Args:
            project_name: Name of the project
        """
        self.project_name = project_name
        self.base_path = Path.home() / ".global" / "mcp" / project_name
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Available MCP servers
        self.available_servers = [
            "cloudflare",
            "playwright",
            "sentry",
            "serena"
        ]
        
        # Initialize MCP files
        self._initialize_mcp()
    
    def _initialize_mcp(self):
        """Initialize MCP configuration files"""
        config_file = self.base_path / "config.json"
        if not config_file.exists():
            config = {
                "project": self.project_name,
                "created": datetime.now().isoformat(),
                "servers": {
                    "sentry": {"enabled": True, "description": "Error monitoring"},
                    "playwright": {"enabled": False, "description": "Browser automation"},
                    "cloudflare": {"enabled": False, "description": "D1, R2, KV"},
                    "serena": {"enabled": False, "description": "Code retrieval"}
                }
            }
            config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
        
        tools_file = self.base_path / "tools.json"
        if not tools_file.exists():
            tools = {
                "available_tools": [],
                "last_updated": datetime.now().isoformat()
            }
            tools_file.write_text(json.dumps(tools, indent=2), encoding='utf-8')
        
        connections_file = self.base_path / "connections.json"
        if not connections_file.exists():
            connections = {
                "active_connections": [],
                "last_updated": datetime.now().isoformat()
            }
            connections_file.write_text(json.dumps(connections, indent=2), encoding='utf-8')
    
    def list_tools(self, server: str) -> List[Dict[str, Any]]:
        """
        List available tools for a specific MCP server
        
        Args:
            server: MCP server name
            
        Returns:
            List of available tools
        """
        try:
            cmd = ["manus-mcp-cli", "tool", "list", "--server", server]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            tools = json.loads(result.stdout)
            
            # Update tools cache
            self._update_tools_cache(server, tools)
            
            return tools
        except subprocess.CalledProcessError as e:
            print(f"Error listing tools for {server}: {e.stderr}")
            return []
        except json.JSONDecodeError:
            print(f"Error parsing tools list for {server}")
            return []
    
    def call_tool(self, server: str, tool_name: str, args: Dict[str, Any]) -> Optional[Any]:
        """
        Call an MCP tool
        
        Args:
            server: MCP server name
            tool_name: Tool name
            args: Tool arguments
            
        Returns:
            Tool result
        """
        try:
            cmd = [
                "manus-mcp-cli", "tool", "call", tool_name,
                "--server", server,
                "--input", json.dumps(args)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Log the call
            self._log_tool_call(server, tool_name, args, "success")
            
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error calling tool {tool_name} on {server}: {e.stderr}")
            self._log_tool_call(server, tool_name, args, "error", e.stderr)
            return None
        except json.JSONDecodeError:
            print(f"Error parsing tool result for {tool_name}")
            return None
    
    def _update_tools_cache(self, server: str, tools: List[Dict[str, Any]]):
        """Update tools cache"""
        tools_file = self.base_path / "tools.json"
        cache = json.loads(tools_file.read_text(encoding='utf-8'))
        
        # Update cache
        cache[server] = {
            "tools": tools,
            "last_updated": datetime.now().isoformat()
        }
        cache["last_updated"] = datetime.now().isoformat()
        
        tools_file.write_text(json.dumps(cache, indent=2), encoding='utf-8')
    
    def _log_tool_call(self, server: str, tool_name: str, args: Dict[str, Any], 
                      status: str, error: str = None):
        """Log tool call"""
        log_file = self.base_path / "tool_calls.log"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "server": server,
            "tool": tool_name,
            "args": args,
            "status": status,
            "error": error
        }
        
        # Append to log
        if log_file.exists():
            logs = json.loads(log_file.read_text(encoding='utf-8'))
        else:
            logs = []
        
        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')
    
    def enable_server(self, server: str):
        """Enable an MCP server"""
        config_file = self.base_path / "config.json"
        config = json.loads(config_file.read_text(encoding='utf-8'))
        
        if server in config["servers"]:
            config["servers"][server]["enabled"] = True
            config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
            print(f"Enabled MCP server: {server}")
        else:
            print(f"Unknown MCP server: {server}")
    
    def disable_server(self, server: str):
        """Disable an MCP server"""
        config_file = self.base_path / "config.json"
        config = json.loads(config_file.read_text(encoding='utf-8'))
        
        if server in config["servers"]:
            config["servers"][server]["enabled"] = False
            config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
            print(f"Disabled MCP server: {server}")
        else:
            print(f"Unknown MCP server: {server}")
    
    def get_enabled_servers(self) -> List[str]:
        """Get list of enabled MCP servers"""
        config_file = self.base_path / "config.json"
        config = json.loads(config_file.read_text(encoding='utf-8'))
        
        return [
            server for server, info in config["servers"].items()
            if info["enabled"]
        ]
    
    def __repr__(self):
        return f"MCPManager(project='{self.project_name}', path='{self.base_path}')"


if __name__ == "__main__":
    # Test
    mcp = MCPManager("test-project")
    print(f"Enabled servers: {mcp.get_enabled_servers()}")
    mcp.enable_server("playwright")
    print(f"Enabled servers: {mcp.get_enabled_servers()}")

