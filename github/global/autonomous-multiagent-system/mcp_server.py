#!/usr/bin/env python3
"""
MCP Server for Autonomous Multi-Agent System

This MCP server exposes the autonomous multi-agent orchestrator as a tool
that can be used by MCP-compatible clients (like Augment, Claude Desktop, etc.).

Usage:
    python mcp_server.py

Configuration (add to MCP config):
    {
      "mcpServers": {
        "autonomous-builder": {
          "command": "python",
          "args": ["/home/ubuntu/.global/autonomous-multiagent-system/mcp_server.py"]
        }
      }
    }
"""

import sys
import os
import json
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("Error: mcp package not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

from orchestrator import AutonomousOrchestrator


# Create server instance
server = Server("autonomous-builder")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="build_project",
            description=(
                "Build a complete software project autonomously using multiple AI agents. "
                "The system uses Gemini (Lead Agent) for design and coding, Claude (Reviewer Agent) "
                "for code review and testing, and optionally ChatGPT (Consultant Agent) for "
                "architectural consultation on complex projects. Returns complete code, tests, "
                "and documentation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "requirement": {
                        "type": "string",
                        "description": (
                            "What to build. Be specific and clear. "
                            "Examples: 'Build a REST API for user authentication with JWT', "
                            "'Create a CLI tool for file encryption', "
                            "'Build a web scraper for product prices'"
                        )
                    },
                    "project_name": {
                        "type": "string",
                        "description": (
                            "Project name (lowercase, hyphens, no spaces). "
                            "Examples: 'user-auth-api', 'file-encryptor', 'price-scraper'"
                        )
                    },
                    "consult_on_architecture": {
                        "type": "boolean",
                        "description": (
                            "Whether to consult ChatGPT on architecture (for complex projects only). "
                            "Use TRUE only for: microservices, distributed systems, complex architectures. "
                            "Use FALSE for: simple APIs, CRUD apps, CLI tools, standard web apps. "
                            "Default: false"
                        ),
                        "default": False
                    }
                },
                "required": ["requirement", "project_name"]
            }
        ),
        Tool(
            name="get_project_info",
            description=(
                "Get information about a previously built project. "
                "Returns the saved context, decisions, architecture, code, tests, and documentation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Project name to retrieve information for"
                    }
                },
                "required": ["project_name"]
            }
        ),
        Tool(
            name="list_projects",
            description=(
                "List all projects that have been built using the autonomous system. "
                "Returns project names and basic information."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "build_project":
        return await build_project(arguments)
    elif name == "get_project_info":
        return await get_project_info(arguments)
    elif name == "list_projects":
        return await list_projects(arguments)
    else:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]


async def build_project(arguments: dict) -> list[TextContent]:
    """Build a project autonomously"""
    
    requirement = arguments.get("requirement")
    project_name = arguments.get("project_name")
    consult = arguments.get("consult_on_architecture", False)
    
    if not requirement or not project_name:
        return [TextContent(
            type="text",
            text="Error: Both 'requirement' and 'project_name' are required"
        )]
    
    # Check API keys
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
    
    if not os.getenv("GEMINI_API_KEY"):
        return [TextContent(
            type="text",
            text=(
                "Error: GEMINI_API_KEY not found. "
                "Please configure API keys in ~/.global/autonomous-multiagent-system/.env"
            )
        )]
    
    # Create orchestrator
    try:
        orchestrator = AutonomousOrchestrator(project_name)
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error initializing orchestrator: {str(e)}"
        )]
    
    # Run orchestrator
    try:
        result = orchestrator.run(
            requirement=requirement,
            consult_on_architecture=consult
        )
        
        if result["success"]:
            data = result["result"]
            
            # Format response
            response = f"""✅ Project built successfully!

📋 **Project Information**
- Name: {project_name}
- Requirement: {requirement}
- Agents Used: Lead (Gemini), Reviewer (Claude){', Consultant (ChatGPT)' if consult else ''}

"""
            
            if "architecture" in data:
                response += f"""🏗️ **Architecture**
{data['architecture']}

"""
            
            response += f"""📝 **Generated Code**
```
{data.get('code', 'No code generated')}
```

🧪 **Generated Tests**
```
{data.get('tests', 'No tests generated')}
```

📖 **Documentation**
{data.get('documentation', 'No documentation generated')}

💾 **Files Location**
The project files are saved in:
- Memory: ~/.global/memory/{project_name}/
- Code: ~/.global/memory/{project_name}/code.md
- Tests: ~/.global/memory/{project_name}/tests.md
- Docs: ~/.global/memory/{project_name}/documentation.md

🚀 **Next Steps**
1. Review the generated code
2. Run the tests to verify functionality
3. Customize as needed for your specific use case
4. Deploy when ready!
"""
            
            return [TextContent(type="text", text=response)]
        else:
            error_msg = result.get("error", "Unknown error")
            details = result.get("details", "")
            return [TextContent(
                type="text",
                text=f"❌ Project build failed!\n\nError: {error_msg}\n\nDetails: {details}"
            )]
            
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Unexpected error: {str(e)}"
        )]


async def get_project_info(arguments: dict) -> list[TextContent]:
    """Get information about a project"""
    
    project_name = arguments.get("project_name")
    
    if not project_name:
        return [TextContent(
            type="text",
            text="Error: 'project_name' is required"
        )]
    
    # Check if project exists
    memory_path = Path.home() / ".global" / "memory" / project_name
    
    if not memory_path.exists():
        return [TextContent(
            type="text",
            text=f"❌ Project '{project_name}' not found. No memory exists for this project."
        )]
    
    # Load project files
    files = {
        "context": memory_path / "context.md",
        "decisions": memory_path / "decisions.md",
        "architecture": memory_path / "architecture.md",
        "code": memory_path / "code.md",
        "tests": memory_path / "tests.md",
        "documentation": memory_path / "documentation.md"
    }
    
    response = f"📁 **Project: {project_name}**\n\n"
    
    for name, path in files.items():
        if path.exists():
            content = path.read_text()
            response += f"**{name.upper()}**\n```\n{content}\n```\n\n"
        else:
            response += f"**{name.upper()}**\n_Not available_\n\n"
    
    return [TextContent(type="text", text=response)]


async def list_projects(arguments: dict) -> list[TextContent]:
    """List all projects"""
    
    memory_path = Path.home() / ".global" / "memory"
    
    if not memory_path.exists():
        return [TextContent(
            type="text",
            text="No projects found. The memory directory doesn't exist yet."
        )]
    
    projects = [d for d in memory_path.iterdir() if d.is_dir()]
    
    if not projects:
        return [TextContent(
            type="text",
            text="No projects found. Build your first project with the 'build_project' tool!"
        )]
    
    response = f"📚 **Found {len(projects)} project(s):**\n\n"
    
    for project in sorted(projects):
        project_name = project.name
        context_file = project / "context.md"
        
        if context_file.exists():
            # Try to extract requirement from context
            content = context_file.read_text()
            lines = content.split('\n')
            requirement = "No description available"
            for line in lines:
                if line.startswith("Requirement:"):
                    requirement = line.replace("Requirement:", "").strip()
                    break
            
            response += f"- **{project_name}**: {requirement}\n"
        else:
            response += f"- **{project_name}**: _No context available_\n"
    
    response += "\nUse 'get_project_info' tool to view details of a specific project."
    
    return [TextContent(type="text", text=response)]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

