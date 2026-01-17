# Knowledge Item: Memory System

> **Role:** Helper tool for senior technical lead  
> **NOT part of user's project!**

---

## Use this when

- ✅ Starting a new task or project
- ✅ Making an important technical decision
- ✅ Switching between project phases
- ✅ Encountering a complex error
- ✅ Completing a major milestone
- ✅ Need to remember context from previous conversation
- ✅ Summarizing long discussions
- ✅ Tracking project evolution

## Don't use this when

- ❌ Doing simple calculations
- ❌ Answering one-time questions
- ❌ Storing temporary variables
- ❌ Managing user's project database
- ❌ Replacing proper project documentation

## Purpose

**Single clear purpose:**  
Enable senior technical lead to maintain context, remember decisions, and learn from experience across long conversations and multiple sessions.

## Decision Rule

**Always choose the best solution:**
- If task is complex (>3 steps) → Save to memory
- If decision impacts architecture → Save to memory  
- If error took >2 attempts → Save solution to memory
- If simple one-off task → Skip memory (don't waste resources)

**Never choose the easy way:**
- ❌ Don't skip memory to save time
- ✅ Invest time now, save time later

## Location & Environment

### Memory System Location
```
~/.global/memory/          # Memory system (NOT in project!)
├── context.db             # SQLite database
├── summaries/             # Conversation summaries
└── decisions/             # Decision logs
```

### User's Project Location
```
~/user-project/            # User's actual project
├── src/                   # Project source code
├── database/              # Project database
│   └── app.db            # Project data (separate!)
└── docs/                  # Project documentation
```

### Critical Separation
```
Memory System:  ~/.global/memory/context.db
Project DB:     ~/user-project/database/app.db

These are COMPLETELY SEPARATE!
Never confuse them!
```

## Example Usage

### Good Example ✅
```python
# At task start
memory.save({
    "type": "task_start",
    "project_path": "~/user-project",  # Note: project is separate
    "description": "Build REST API for user management",
    "requirements": [...]
})

# When making architectural decision
memory.save({
    "type": "decision",
    "decision": "Use PostgreSQL instead of MySQL",
    "rationale": "Better JSON support, required for our use case",
    "alternatives_considered": ["MySQL", "MongoDB"],
    "impact": "high"
})

# When solving complex error
memory.save({
    "type": "solution",
    "error": "CORS policy blocking API calls",
    "attempts": 3,
    "solution": "Added CORS middleware with specific origins",
    "lesson": "Always configure CORS before frontend integration"
})
```

### Bad Example ❌
```python
# DON'T: Storing user's project data in memory system
memory.save({
    "type": "user_data",  # WRONG!
    "user_id": 123,
    "email": "user@example.com"
})
# This belongs in user's project database, not memory!

# DON'T: Using memory for temporary calculations
memory.save({
    "type": "calculation",
    "result": 2 + 2
})
# This is wasteful, just calculate it
```

## What to Save

### Always Save
- Task objectives and requirements
- Architectural decisions and rationale
- Complex error solutions (>2 attempts)
- Phase completions and handoffs
- Important discoveries or insights

### Sometimes Save
- Medium complexity decisions
- Useful patterns or approaches
- Configuration choices

### Never Save
- Temporary calculations
- One-time queries
- User's project data (goes in their DB!)
- Passwords or secrets
- Obvious information

## Memory Operations

### Save
```python
memory.save({
    "type": "decision|solution|task_start|milestone",
    "content": {...},
    "timestamp": "auto",
    "project": "~/user-project"  # Always note project path
})
```

### Retrieve
```python
# Get recent context
context = memory.retrieve({
    "type": "recent",
    "limit": 10
})

# Search for similar issues
similar = memory.retrieve({
    "type": "search",
    "query": "CORS error",
    "category": "solution"
})
```

### Summarize
```python
# Summarize conversation
summary = memory.summarize({
    "from": "task_start",
    "to": "now",
    "focus": "key_decisions"
})
```

## Integration with Other Tools

### With MCP
```python
# Memory and MCP work together
# 1. Check MCP for available tools
mcp_tools = mcp.list_tools()

# 2. Save which tools we're using
memory.save({
    "type": "tools_selected",
    "mcp_servers": ["playwright", "github"],
    "rationale": "Need browser automation and git operations"
})
```

### With Thinking Framework
```python
# Thinking framework uses memory
# 1. Retrieve past decisions
past_decisions = memory.retrieve({"type": "decision"})

# 2. Apply thinking framework
decision = thinking_framework.analyze({
    "problem": "...",
    "context": past_decisions
})

# 3. Save new decision
memory.save({"type": "decision", "content": decision})
```

## Quality Gates

### Before Saving
- [ ] Is this important for future reference?
- [ ] Will this help maintain context?
- [ ] Is this a learning opportunity?
- [ ] Does this belong in memory (not project DB)?

### After Saving
- [ ] Can I retrieve this later?
- [ ] Is the information clear and useful?
- [ ] Did I separate memory from project data?

## Common Mistakes

### Mistake 1: Confusing Memory with Project Database
```
❌ WRONG: Storing user's app data in memory
✅ RIGHT: Memory = context for AI, Project DB = user's data
```

### Mistake 2: Over-using Memory
```
❌ WRONG: Saving every single step
✅ RIGHT: Save important decisions and learnings
```

### Mistake 3: Under-using Memory
```
❌ WRONG: Never saving anything
✅ RIGHT: Save at key milestones and decisions
```

### Mistake 4: Wrong Location
```
❌ WRONG: Memory in ~/user-project/.memory/
✅ RIGHT: Memory in ~/.global/memory/
```

## Related Knowledge Items

- **MCP System** - Another helper tool (see `knowledge/core/mcp.md`)
- **Thinking Framework** - Uses memory for decisions (see `knowledge/core/thinking.md`)
- **Context Engineering** - Builds on memory (see `knowledge/core/context.md`)
- **Environment Separation** - Critical concept (see `knowledge/core/environment.md`)

---

## Summary

**Memory is a helper tool for YOU (the senior technical lead).**

- Use it to remember context
- Use it to learn from experience
- Use it to maintain consistency
- **DON'T confuse it with user's project!**

**Location:** `~/.global/memory/` (NOT in user's project!)  
**Purpose:** Help YOU work better  
**Rule:** Always choose the best solution, not the easiest

