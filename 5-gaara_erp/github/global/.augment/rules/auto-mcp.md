---
type: agent_requested
description: Model Context Protocol usage guidelines
---

# MCP System

## Use MCP When

- ✅ Starting any task (check available tools)
- ✅ Need external capabilities
- ✅ Need to integrate with services
- ✅ Need to access databases
- ✅ Need to use APIs
- ✅ Need specialized tools

## Don't Use MCP When

- ❌ Built-in capabilities are sufficient
- ❌ Simple text processing
- ❌ Basic code generation
- ❌ Standard file operations

## MCP Location

**Project-Specific Structure:**

```
YOUR MCP (helper tool):
  ~/.global/mcp/[project-name]/

Example:
  ~/.global/mcp/store-erp/
  ~/.global/mcp/gaara-erp-v12/
  ~/.global/mcp/personal-site/

NOT in user's project:
  ~/user-project/  ❌
```

**Each project has its own MCP directory to prevent mixing!**

## Initialization

**ALWAYS do this at task start:**

```
1. Initialize MCP for project:
   "Initialize MCP for project: [project-name]"
   → Creates ~/.global/mcp/[project-name]/

2. mcp.list_servers()

3. Review available tools

4. Plan which tools to use

5. Save tool list to memory:
   "Save to memory: Available MCP tools"
   → Saves to ~/.global/memory/[project-name]/
```

## Available MCP Servers

Check these servers:
- **cloudflare** - D1, R2, KV, Workers
- **playwright** - Browser automation
- **sentry** - Error monitoring
- **serena** - Semantic code retrieval

## How to Use

```
1. Check available servers
2. Identify needed capabilities
3. Use appropriate tools
4. Document usage
5. Save results to memory
```

## Best Practices

- Always check available tools first
- Use the right tool for the job
- Don't reinvent what tools provide
- Document tool usage
- Handle errors gracefully
- Save tool outputs to memory

## Integration with Memory

```
1. List MCP servers
2. Save to memory
3. Use tools as needed
4. Save results to memory
5. Reference when needed
```

## Project-Specific Files

**Each project directory contains:**
```
~/.global/mcp/[project-name]/
├── config.json          # MCP configuration
├── tools.json           # Available tools
└── connections.json     # External connections
```

## Critical Rules

- ❌ NEVER mix projects in the same directory
- ✅ ALWAYS use project-specific subdirectories
- ✅ ALWAYS specify project name when initializing
- ✅ Each project has completely separate MCP

## Remember

MCP is YOUR helper tool. It gives YOU capabilities. It's not part of the user's project.

**Each project has its own MCP to prevent mixing!**

