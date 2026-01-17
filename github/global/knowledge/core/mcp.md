# Knowledge Item: MCP (Model Context Protocol)

> **Role:** Helper tool for senior technical lead  
> **NOT part of user's project!**

---

## Use this when

- ✅ Starting ANY new task (check available tools first!)
- ✅ Need to interact with external services (GitHub, databases, browsers)
- ✅ Automating repetitive tasks
- ✅ Need specialized capabilities beyond base AI
- ✅ Integrating with third-party APIs
- ✅ Browser automation required
- ✅ File system operations needed
- ✅ Database queries required

## Don't use this when

- ❌ Simple text generation
- ❌ Basic calculations
- ❌ When no MCP servers are configured
- ❌ For user's project business logic (that goes in their code!)

## Purpose

**Single clear purpose:**  
Provide senior technical lead with access to external tools and services to enhance capabilities beyond base AI functionality.

## Decision Rule

**Always choose the best solution:**
- If MCP tool exists for the task → Use it (it's optimized!)
- If no MCP tool → Implement manually
- If task is repetitive → Check if MCP can automate it

**Never choose the easy way:**
- ❌ Don't skip checking MCP servers (you might miss a perfect tool!)
- ✅ Always check first, even if you think you can do it manually

## Location & Environment

### MCP Configuration Location
```
~/.global/mcp/              # MCP configuration (NOT in project!)
├── config.json             # MCP servers configuration
├── servers/                # Installed MCP servers
└── logs/                   # MCP operation logs
```

### User's Project Location
```
~/user-project/             # User's actual project
├── src/                    # Project source code
├── api/                    # Project API (uses MCP as tool)
└── integrations/           # Project integrations (may use MCP)
```

### Critical Separation
```
MCP System:     ~/.global/mcp/  (Helper tool for YOU)
Project Code:   ~/user-project/  (User's application)

MCP is a TOOL you use, not part of user's project!
```

## Example Usage

### Good Example ✅
```python
# ALWAYS start by checking available MCP tools
# 1. List MCP servers
servers = mcp.list_servers()
# Output: ['playwright', 'github', 'cloudflare', 'sentry']

# 2. Check tools for specific server
tools = mcp.list_tools(server='playwright')
# Output: ['browser_navigate', 'browser_click', 'browser_screenshot']

# 3. Use MCP tool to help with user's project
result = mcp.call_tool(
    server='github',
    tool='create_issue',
    args={
        'repo': 'user/their-project',  # User's project
        'title': 'Bug: Login fails',
        'body': '...'
    }
)

# 4. Save to memory that we used MCP
memory.save({
    "type": "tool_usage",
    "mcp_server": "github",
    "tool": "create_issue",
    "purpose": "Track bug in user's project"
})
```

### Bad Example ❌
```python
# DON'T: Skipping MCP check
# Just implementing manually without checking if MCP can help
def scrape_website_manually():  # WRONG!
    # ... 100 lines of code ...
    pass

# Should have checked: mcp.list_tools(server='playwright')
# Playwright MCP can do this in 3 lines!

# DON'T: Confusing MCP with user's project
# MCP is YOUR tool, not part of their application
# Don't put MCP config in user's project folder!
```

## Available MCP Servers

### Configured Servers
1. **playwright** - Browser automation
2. **github** - Git operations
3. **cloudflare** - Cloudflare services
4. **sentry** - Error monitoring
5. **serena** - Code analysis

### When to Use Each

**Use playwright when:**
- Need to automate browser interactions
- Testing user's web application
- Scraping web data
- Taking screenshots

**Use github when:**
- Managing user's repository
- Creating issues/PRs
- Reading code from repos
- Git operations

**Use cloudflare when:**
- Managing DNS
- CDN operations
- Worker deployments

**Use sentry when:**
- Analyzing errors in user's app
- Setting up monitoring
- Reviewing error reports

**Use serena when:**
- Analyzing user's codebase
- Finding code patterns
- Semantic search in code

## MCP Operations

### Check Available Tools
```python
# Always do this FIRST!
all_servers = mcp.list_servers()

for server in all_servers:
    tools = mcp.list_tools(server=server)
    print(f"{server}: {tools}")
```

### Call a Tool
```python
result = mcp.call_tool(
    server='server_name',
    tool='tool_name',
    args={
        'param1': 'value1',
        'param2': 'value2'
    }
)
```

### Handle Errors
```python
try:
    result = mcp.call_tool(...)
except MCPError as e:
    # Save error to memory
    memory.save({
        "type": "mcp_error",
        "server": "...",
        "error": str(e),
        "attempted_solution": "..."
    })
```

## Integration with Other Tools

### With Memory
```python
# 1. Check MCP
tools = mcp.list_tools(server='github')

# 2. Save what you're doing
memory.save({
    "type": "mcp_usage",
    "server": "github",
    "purpose": "Clone user's repository for analysis"
})

# 3. Use MCP
mcp.call_tool(server='github', tool='clone_repo', args={...})

# 4. Save result
memory.save({
    "type": "mcp_result",
    "success": True,
    "output": "Repository cloned successfully"
})
```

### With Thinking Framework
```python
# Thinking framework considers MCP capabilities
decision = thinking_framework.analyze({
    "problem": "Need to test user's web app",
    "available_tools": mcp.list_servers(),  # Include MCP in analysis
    "constraints": [...]
})

# Decision might be: "Use playwright MCP for automation"
```

## Quality Gates

### Before Using MCP
- [ ] Did I check if MCP server is available?
- [ ] Did I list available tools?
- [ ] Is this the right tool for the job?
- [ ] Am I using it for user's project (good) not confusing it as part of their project (bad)?

### After Using MCP
- [ ] Did I save the operation to memory?
- [ ] Did I handle errors properly?
- [ ] Did I verify the result?

## Common Mistakes

### Mistake 1: Not Checking MCP First
```
❌ WRONG: Implementing manually without checking MCP
✅ RIGHT: Always check mcp.list_servers() first!
```

### Mistake 2: Confusing MCP with User's Project
```
❌ WRONG: "User's project uses MCP" (No! YOU use MCP to help with their project)
✅ RIGHT: "I use MCP to automate tasks for user's project"
```

### Mistake 3: Wrong Location
```
❌ WRONG: MCP config in ~/user-project/.mcp/
✅ RIGHT: MCP config in ~/.global/mcp/
```

### Mistake 4: Skipping Error Handling
```
❌ WRONG: mcp.call_tool(...) without try/catch
✅ RIGHT: Always handle MCP errors and save to memory
```

## Decision Matrix

| Task | Manual | MCP | Best Choice |
|------|--------|-----|-------------|
| Browser automation | Hard, 100+ lines | Easy, 3 lines | **MCP (playwright)** |
| Git operations | Possible | Easy | **MCP (github)** |
| Simple calculation | Easy | Overkill | **Manual** |
| Web scraping | Hard | Easy | **MCP (playwright)** |
| Text generation | Easy | N/A | **Manual** |

**Rule:** If MCP can do it easier and better → Use MCP!

## Related Knowledge Items

- **Memory System** - Save MCP usage (see `knowledge/core/memory.md`)
- **Thinking Framework** - Consider MCP in decisions (see `knowledge/core/thinking.md`)
- **Environment Separation** - Keep MCP separate (see `knowledge/core/environment.md`)
- **Browser Automation** - Uses playwright MCP (see `knowledge/technical/browser.md`)

---

## Summary

**MCP is a helper tool for YOU (the senior technical lead).**

- Check it FIRST before any task
- Use it to enhance your capabilities
- It's YOUR tool, not part of user's project
- **DON'T confuse it with user's application!**

**Location:** `~/.global/mcp/` (NOT in user's project!)  
**Purpose:** Give YOU superpowers  
**Rule:** Always check MCP first, use it when it's better

