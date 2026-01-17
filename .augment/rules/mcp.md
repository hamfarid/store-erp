# 🔧 MCP (Model Context Protocol) Rules

## Purpose

MCP provides access to external tools and services. Using MCP means you don't have to manually do what tools can do automatically.

---

## ⚡ Mandatory Activation

**ALWAYS check MCP tools at the START of EVERY task!**

This is NOT optional. This is REQUIRED.

---

## 📋 When to Check MCP

### **Always:**
1. **At task start** - Check available servers and tools
2. **Before manual work** - See if a tool can do it
3. **When integrating services** - Use MCP connectors
4. **When accessing data** - Use MCP data sources
5. **Throughout the task** - Leverage available tools

---

## 🔧 How to Use MCP

### **1. Check Available Servers**
```bash
# List all configured MCP servers
manus-mcp-cli tool list --server <server_name>
```

### **2. List Tools from Each Server**
```bash
# For each server, list its tools
manus-mcp-cli tool list --server cloudflare
manus-mcp-cli tool list --server playwright
manus-mcp-cli tool list --server sentry
manus-mcp-cli tool list --server serena
```

### **3. Call Tools**
```bash
# Call a tool with JSON arguments
manus-mcp-cli tool call <tool_name> \
  --server <server_name> \
  --input '<json_args>'
```

---

## 🛠️ Available MCP Servers

### **1. Cloudflare**
```
Server: cloudflare
Purpose: Cloudflare Workers, D1, R2, KV
Tools: Database operations, object storage, key-value store
```

**Use for:**
- Database queries (D1)
- File storage (R2)
- Cache operations (KV)
- Worker bindings

### **2. Playwright**
```
Server: playwright
Purpose: Browser automation
Tools: Web scraping, testing, screenshots
```

**Use for:**
- Automated testing
- Web scraping
- Screenshot capture
- Browser interactions

**Important:** Call `browser_install` tool first to install browser!

### **3. Sentry**
```
Server: sentry
Purpose: Error monitoring and tracking
Tools: Error reports, performance analysis, issue tracking
```

**Use for:**
- Error monitoring
- Performance analysis
- Issue tracking
- Stack trace analysis

### **4. Serena**
```
Server: serena
Purpose: Semantic code retrieval and editing
Tools: Code search, code editing, project onboarding
```

**Use for:**
- Semantic code search
- Code editing
- Project understanding
- Code navigation

**Important:** Check if project onboarding was performed first!

---

## 📋 MCP Workflow

### **Step 1: Check Availability**
```
At task start:
1. List all MCP servers
2. Check what tools are available
3. Plan which tools to use
```

### **Step 2: Use Tools**
```
During task:
1. Before manual work, check if MCP tool can do it
2. Call appropriate tools
3. Use tool outputs
4. Don't reinvent what tools provide
```

### **Step 3: Handle Errors**
```
If tool fails:
1. Check error message
2. Verify input format
3. Check server status
4. Retry with corrected input
```

---

## 🎯 Common Use Cases

### **Use Case 1: Database Operations**
```bash
# Instead of manually writing SQL
# Use Cloudflare D1 MCP tools

manus-mcp-cli tool call d1_query \
  --server cloudflare \
  --input '{"query": "SELECT * FROM users WHERE active = true"}'
```

### **Use Case 2: Browser Automation**
```bash
# Instead of manually testing in browser
# Use Playwright MCP tools

# First, install browser
manus-mcp-cli tool call browser_install \
  --server playwright \
  --input '{"browser": "chrome"}'

# Then, automate
manus-mcp-cli tool call navigate \
  --server playwright \
  --input '{"url": "https://example.com"}'
```

### **Use Case 3: Error Monitoring**
```bash
# Instead of manually checking logs
# Use Sentry MCP tools

manus-mcp-cli tool call get_issues \
  --server sentry \
  --input '{"project": "my-project", "status": "unresolved"}'
```

### **Use Case 4: Code Search**
```bash
# Instead of manually searching code
# Use Serena MCP tools

# First, check onboarding
manus-mcp-cli tool call check_onboarding \
  --server serena \
  --input '{"project_path": "/path/to/project"}'

# Then, search
manus-mcp-cli tool call semantic_search \
  --server serena \
  --input '{"query": "authentication logic"}'
```

---

## ⚠️ Critical Rules

### **DO:**
- ✅ Check MCP servers at task start
- ✅ List available tools before starting
- ✅ Use MCP tools instead of manual work
- ✅ Read tool documentation
- ✅ Provide correct JSON input
- ✅ Handle tool errors gracefully

### **DON'T:**
- ❌ Skip MCP check
- ❌ Manually do what tools can do
- ❌ Ignore available tools
- ❌ Use incorrect input format
- ❌ Give up after one tool failure
- ❌ Forget to install prerequisites (e.g., browser)

---

## 🔄 MCP Integration Workflow

### **Phase 1: Discovery**
```
Task Start
    ↓
Check MCP Servers
    ↓
List Available Tools
    ↓
Plan Tool Usage
```

### **Phase 2: Usage**
```
Need to Do Something
    ↓
Check if MCP Tool Exists
    ↓
Yes: Use MCP Tool
No: Do Manually
    ↓
Continue
```

### **Phase 3: Error Handling**
```
Tool Call Failed
    ↓
Check Error Message
    ↓
Fix Input/Prerequisites
    ↓
Retry
    ↓
Success or Fallback to Manual
```

---

## 💡 Best Practices

### **1. Always Check First**
```
❌ Bad:  Start working without checking MCP
✅ Good: "Let me check available MCP tools first..."
         [Lists tools]
         "I can use Cloudflare D1 for database operations"
```

### **2. Use Tools Appropriately**
```
❌ Bad:  Write SQL queries manually when D1 tool available
✅ Good: Use D1 MCP tool for database operations
```

### **3. Handle Prerequisites**
```
❌ Bad:  Call playwright tools without installing browser
✅ Good: "First, I'll install the browser..."
         [Calls browser_install]
         "Now I can use playwright tools"
```

### **4. Provide Correct Input**
```
❌ Bad:  manus-mcp-cli tool call query --input "SELECT * FROM users"
✅ Good: manus-mcp-cli tool call query --input '{"query": "SELECT * FROM users"}'
```

---

## 🎓 Examples

### **Example 1: Database Query**
```bash
# Task: Get all active users

# ❌ Bad: Write SQL manually
# ✅ Good: Use MCP

manus-mcp-cli tool call d1_query \
  --server cloudflare \
  --input '{
    "database": "prod_db",
    "query": "SELECT id, name, email FROM users WHERE active = true"
  }'
```

### **Example 2: Web Testing**
```bash
# Task: Test login flow

# ❌ Bad: Manually test in browser
# ✅ Good: Use MCP

# Install browser first
manus-mcp-cli tool call browser_install \
  --server playwright \
  --input '{"browser": "chrome"}'

# Navigate to login page
manus-mcp-cli tool call navigate \
  --server playwright \
  --input '{"url": "https://myapp.com/login"}'

# Fill form
manus-mcp-cli tool call fill_form \
  --server playwright \
  --input '{
    "selector": "#login-form",
    "data": {
      "username": "test@example.com",
      "password": "testpass123"
    }
  }'

# Submit
manus-mcp-cli tool call click \
  --server playwright \
  --input '{"selector": "#submit-btn"}'
```

### **Example 3: Error Monitoring**
```bash
# Task: Check recent errors

# ❌ Bad: Manually check logs
# ✅ Good: Use MCP

manus-mcp-cli tool call get_issues \
  --server sentry \
  --input '{
    "project": "my-app",
    "status": "unresolved",
    "limit": 10,
    "sort": "date"
  }'
```

### **Example 4: Code Search**
```bash
# Task: Find authentication code

# ❌ Bad: Manually grep through files
# ✅ Good: Use MCP

# Check onboarding first
manus-mcp-cli tool call check_onboarding \
  --server serena \
  --input '{"project_path": "/home/ubuntu/my-project"}'

# Search semantically
manus-mcp-cli tool call semantic_search \
  --server serena \
  --input '{
    "query": "user authentication and login logic",
    "limit": 5
  }'
```

---

## 🚀 Quick Start

**For every task:**

1. **Check MCP Servers**
   ```
   "Let me check available MCP tools..."
   [List servers and tools]
   ```

2. **Plan Tool Usage**
   ```
   "I can use:
   - Cloudflare D1 for database
   - Playwright for testing
   - Sentry for monitoring"
   ```

3. **Use Tools Throughout**
   ```
   Instead of manual work:
   - Use MCP tools
   - Leverage automation
   - Save time and effort
   ```

---

## ⚡ Remember

**MCP is NOT optional!**

Without MCP:
- ❌ You do everything manually
- ❌ You waste time
- ❌ You miss available tools
- ❌ You reinvent the wheel

With MCP:
- ✅ You leverage existing tools
- ✅ You save time
- ✅ You use automation
- ✅ You work smarter

**Always check MCP. Always use available tools.**

---

*MCP is your toolbox. Use it, and you'll work 10x faster.*

