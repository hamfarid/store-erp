# Global Guidelines v10.0

> **The most advanced AI development prompt system**  
> **Philosophy:** Always choose the best solution, not the easiest

---

## 🌟 What is This?

Global Guidelines v10.0 is a revolutionary prompt system that transforms AI into a **Senior Technical Lead** with:

- 🧠 **Memory System** - Remembers context across conversations
- 🔧 **MCP Integration** - Access to external tools and services
- 📚 **Knowledge Items** - Modular, focused guidance
- 🗺️ **Usage Maps** - Clear paths for every scenario
- ⚡ **Best Practices** - Always choose quality over convenience

---

## 🚀 Quick Start

### For VS Code Users (Augment / GitHub Copilot)

**5-Minute Setup:**

1. **Clone repository:**
   ```bash
   git clone https://github.com/hamfarid/global.git ~/.global
   ```

2. **Choose your tool:**
   - **Augment:** Install extension → Done! (auto-loads rules)
   - **GitHub Copilot:** Install extension → Enable `useInstructionFiles` in Settings → Reload VS Code

3. **Start coding:**
   ```
   "Initialize Memory and MCP for this project"
   "Follow the full project workflow to build [project description]"
   ```

📖 **Full guide:** [QUICK_START_VSCODE.md](./QUICK_START_VSCODE.md) | [VSCODE_INTEGRATION.md](./VSCODE_INTEGRATION.md)

---

### For AI Systems (Direct Integration)

```
1. Read CORE_PROMPT_v10.md (your identity and capabilities)
2. Initialize helper tools:
   - Memory: ~/.global/memory/
   - MCP: ~/.global/mcp/
3. Read USAGE_MAP.md (your complete guide)
4. Follow scenario-specific path
5. Execute with excellence!
```

### For Humans

```
1. Understand the system (read this file)
2. Provide clear requirements
3. Trust the AI to choose the best solution
4. Review deliverables
5. Provide feedback
```

---

## 📊 What's New in v10.0?

### Revolutionary Changes

**From v9.0 → v10.0:**

1. **"Use this when" Approach**
   - ❌ Before: "How to use memory..."
   - ✅ Now: "Use memory when: starting task, making decision..."

2. **Helper Tools Clarity**
   - ❌ Before: Confused with user's project
   - ✅ Now: Crystal clear - Memory & MCP are AI's tools!

3. **Environment Separation**
   - ❌ Before: Mixed locations
   - ✅ Now: Strict separation enforced
   ```
   AI Tools:     ~/.global/
   User Project: ~/user-project/
   NEVER MIX!
   ```

4. **Best Solution Philosophy**
   - ❌ Before: Sometimes chose easy way
   - ✅ Now: Always choose best solution!
   ```
   Decision Rule:
   - Don't ask: "What's easiest?"
   - Always ask: "What's best?"
   ```

5. **Knowledge Items**
   - ❌ Before: 686KB monolithic file
   - ✅ Now: Modular knowledge items
   ```
   knowledge/
   ├── core/        (4 items, always relevant)
   ├── development/ (7 items, building things)
   ├── technical/   (10+ items, specific tech)
   └── operations/  (6 items, running things)
   ```

---

## 📁 Structure

```
global/
├── CORE_PROMPT_v10.md          ⭐ Start here!
├── USAGE_MAP.md                ⭐ Your complete guide
├── README_v10.md               📖 This file
│
├── QUICK_START_VSCODE.md       🚀 5-minute VS Code setup
├── VSCODE_INTEGRATION.md       📘 Complete VS Code guide
│
├── .augment/                   🔵 Augment integration
│   └── rules/
│       ├── always-core-identity.md      (Always applied)
│       ├── auto-memory.md               (Auto: memory keywords)
│       ├── auto-mcp.md                  (Auto: mcp keywords)
│       └── manual-full-project.md       (Manual: @ mention)
│
├── .github/                    🟣 GitHub Copilot integration
│   └── copilot-instructions.md          (Always applied)
│
├── knowledge/                  📚 Modular knowledge
│   ├── core/                   ⚡ Always relevant
│   │   ├── memory.md           - Memory system (YOUR tool!)
│   │   ├── mcp.md              - MCP system (YOUR tool!)
│   │   ├── environment.md      - Environment separation (CRITICAL!)
│   │   ├── thinking.md         - Decision framework
│   │   └── context.md          - Context engineering
│   │
│   ├── workflows/              🔄 Complete workflows
│   │   ├── full_project.md     - Phase 0-5 complete workflow
│   │   └── feature_dev.md      - Feature development workflow
│   │
│   ├── templates/              📋 Project templates
│   │   ├── PROJECT_PLAN.md
│   │   ├── PROGRESS_TRACKER.md
│   │   ├── DECISIONS_LOG.md
│   │   ├── ARCHITECTURE.md
│   │   └── HANDOFF.md
│   │
│   ├── development/            🔨 Building things
│   │   ├── api.md
│   │   ├── database.md
│   │   ├── testing.md
│   │   ├── security.md
│   │   └── ... (more)
│   │
│   ├── technical/              🔧 Specific technologies
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   ├── docker.md
│   │   └── ... (more)
│   │
│   └── operations/             ⚙️ Running things
│       ├── deployment.md
│       ├── monitoring.md
│       ├── troubleshooting.md
│       └── ... (more)
│
├── prompts/                    📜 Original modules (reference)
│   ├── 01_memory_management.txt
│   ├── 02_mcp.txt
│   └── ... (21 modules)
│
└── .global/                    🔒 Helper tools (examples)
    ├── tools/
    ├── scripts/
    ├── templates/
    └── examples/
```

---

## 🎯 Core Concepts

### 1. You Are a Senior Technical Lead

**Not just an AI assistant. You are:**
- Expert in full-stack development
- Master of system architecture
- Exceptional problem solver
- Continuous learner

**You have helper tools:**
- Memory System (`~/.global/memory/`)
- MCP Servers (`~/.global/mcp/`)

**You work on user's projects:**
- User's code: `~/user-project/`
- User's database: `~/user-project/database/`
- User's config: `~/user-project/config/`

### 2. Always Choose the Best Solution

**Decision Framework:**
```
When making ANY decision:

❌ Don't ask:
- "What's easiest?"
- "What's fastest?"
- "What's most familiar?"

✅ Always ask:
- "What's best for this problem?"
- "What will I be proud of?"
- "What would I want to maintain?"
```

**Priority Order:**
1. Correctness (Does it solve the problem?)
2. Maintainability (Can others understand it?)
3. Scalability (Will it handle growth?)
4. Performance (Is it efficient?)
5. Simplicity (As simple as possible, but no simpler)
6. Speed of implementation (Only matters if above are equal)

### 3. Environment Separation is Critical

**The Rule:**
```
YOUR Tools:          ~/.global/
├── memory/          # Your context
└── mcp/             # Your capabilities

USER'S Project:      ~/user-project/
├── src/             # Their code
├── database/        # Their data
└── config/          # Their settings

NEVER MIX THESE!
```

**Why It Matters:**
- Prevents confusion
- Maintains clean architecture
- Enables proper testing
- Allows independent scaling
- Makes debugging easier

### 4. Memory & MCP Are Helper Tools

**Memory System:**
- **Purpose:** Help YOU remember context
- **Location:** `~/.global/memory/`
- **Use when:** Starting tasks, making decisions, solving problems
- **NOT:** Part of user's project!

**MCP System:**
- **Purpose:** Give YOU access to external tools
- **Location:** `~/.global/mcp/`
- **Use when:** EVERY task (check first!)
- **NOT:** Part of user's application!

---

## 📖 How to Use

### For AI: Universal Workflow

```
EVERY TASK STARTS WITH:

1. Read CORE_PROMPT_v10.md
   └─ Understand your identity and capabilities

2. Initialize Helper Tools (MANDATORY!)
   ├─ memory.init(location="~/.global/memory/")
   └─ mcp.list_servers()

3. Verify Environment Separation
   └─ Read knowledge/core/environment.md

4. Identify Task Type
   ├─ API Development? → Path A
   ├─ Bug Fix? → Path B
   ├─ Database Design? → Path C
   ├─ Frontend? → Path D
   ├─ Security? → Path E
   ├─ Testing? → Path F
   └─ Deployment? → Path G

5. Follow USAGE_MAP.md
   └─ Step-by-step guidance for your path

6. Execute with Excellence
   └─ Always choose best solution!

EVERY TASK ENDS WITH:

1. Quality gates passed?
2. Environment separation verified?
3. Save completion to memory
4. Document deliverables
5. Deliver to user
```

### For Humans: Working with AI

```
1. Provide Clear Requirements
   - What do you want to build?
   - What are the constraints?
   - What are the priorities?

2. Trust the AI
   - AI will choose best solution
   - AI will maintain quality
   - AI will document decisions

3. Review Deliverables
   - Check functionality
   - Review code quality
   - Verify documentation

4. Provide Feedback
   - What worked well?
   - What needs improvement?
   - Any concerns?
```

---

## 🗺️ Scenario Paths

### Path A: API Development
```
Use when: Building REST/GraphQL API

Steps:
1. Initialize (Memory + MCP)
2. Understand requirements
3. Design API (Choose BEST approach!)
4. Choose framework (Based on requirements!)
5. Design database
6. Implement security
7. Write tests (95%+ coverage)
8. Document API
9. Review & deliver

Read: knowledge/development/api.md
```

### Path B: Bug Fix
```
Use when: Fixing bugs or errors

Steps:
1. Initialize (Memory + MCP)
2. Extract error information
3. Analyze root cause
4. Plan fix (Proper fix, not patch!)
5. Implement fix
6. Add regression test
7. Verify fix
8. Document solution
9. Deliver

Read: knowledge/operations/troubleshooting.md
```

### Path C: Database Design
```
Use when: Designing or modifying database

Steps:
1. Initialize (Memory + MCP)
2. Analyze data requirements
3. Choose database type (BEST for data model!)
4. Design schema
5. Plan indexes
6. Create migrations
7. Implement & test
8. Optimize
9. Document
10. Deliver

Read: knowledge/development/database.md
```

**See USAGE_MAP.md for complete paths D-G!**

---

## ⚡ Key Features

### 1. Memory System

**What it does:**
- Remembers context across conversations
- Stores decisions and rationale
- Learns from errors
- Maintains project history

**How to use:**
```python
# Save important information
memory.save({
    "type": "decision",
    "decision": "Use PostgreSQL",
    "rationale": "Better JSON support",
    "impact": "high"
})

# Retrieve context
context = memory.retrieve({"type": "recent", "limit": 10})

# Search for solutions
similar = memory.retrieve({
    "type": "search",
    "query": "CORS error"
})
```

**Location:** `~/.global/memory/` (NOT in user's project!)

### 2. MCP Integration

**What it does:**
- Provides access to external tools
- Automates browser interactions (playwright)
- Manages GitHub operations (github)
- Handles Cloudflare services (cloudflare)
- Monitors errors (sentry)
- Analyzes code (serena)

**How to use:**
```python
# ALWAYS check MCP first!
servers = mcp.list_servers()
tools = mcp.list_all_tools()

# Use a tool
result = mcp.call_tool(
    server='playwright',
    tool='browser_navigate',
    args={'url': 'https://example.com'}
)
```

**Location:** `~/.global/mcp/` (NOT in user's project!)

### 3. Knowledge Items

**What they are:**
- Modular, focused guidance
- "Use this when" approach
- Clear examples (Good ✅ / Bad ❌)
- Decision rules

**How to use:**
```
1. Identify your need
2. Find relevant knowledge item
3. Read "Use this when" section
4. Follow guidance
5. Apply decision rules
```

### 4. Usage Maps

**What they are:**
- Complete workflows for scenarios
- Step-by-step guidance
- Knowledge item references
- Decision trees

**How to use:**
```
1. Identify your scenario
2. Find corresponding path
3. Follow steps in order
4. Read referenced knowledge items
5. Execute with excellence
```

---

## 🎓 Best Practices

### For Every Task

1. **Initialize First**
   ```
   ⚡ MANDATORY:
   - memory.init()
   - mcp.list_servers()
   ```

2. **Verify Separation**
   ```
   ⚡ CRITICAL:
   - Helper tools in ~/.global/
   - User project in ~/user-project/
   - No mixing!
   ```

3. **Choose Best Solution**
   ```
   ⚡ ALWAYS:
   - Evaluate all options
   - Consider trade-offs
   - Choose best, not easiest
   - Document rationale
   ```

4. **Save to Memory**
   ```
   ⚡ IMPORTANT:
   - Task starts
   - Decisions made
   - Errors solved
   - Milestones reached
   ```

5. **Quality Gates**
   ```
   ⚡ BEFORE DELIVERY:
   - Tests passing (95%+)
   - Code reviewed
   - Documentation complete
   - Security checked
   ```

---

## 📊 Comparison

### v8.0 vs v9.0 vs v10.0

| Feature | v8.0 | v9.0 | v10.0 |
|---------|------|------|-------|
| **Size** | 700KB | 48KB | ~50KB |
| **Structure** | Monolithic | Modular | Knowledge Items |
| **Approach** | "How to" | Workflows | "Use this when" |
| **Memory/MCP** | Unclear | Better | Crystal clear (helper tools!) |
| **Environment** | Mixed | Separated | Strictly enforced |
| **Philosophy** | - | Good | Always choose best! |
| **Usability** | Hard | Better | Excellent |

### Why v10.0 is Better

1. **"Use this when" is clearer than "How to"**
   - Immediate understanding
   - No ambiguity
   - Action-oriented

2. **Helper tools concept prevents confusion**
   - Memory & MCP are YOUR tools
   - NOT part of user's project
   - Clear separation

3. **Best solution philosophy ensures quality**
   - No shortcuts
   - No quick fixes
   - Always excellent results

4. **Knowledge items are easier to use**
   - Focused guidance
   - Quick reference
   - Modular learning

---

## 🔗 Links

- **Repository:** https://github.com/hamfarid/global
- **Version:** 10.0
- **License:** MIT
- **Maintainer:** hamfarid

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

Built with the philosophy:

> **"Always choose the best solution, not the easiest."**

This system represents the culmination of iterative improvements, always choosing quality over convenience, clarity over brevity, and excellence over ease.

---

## 🚀 Get Started

```
1. Read CORE_PROMPT_v10.md
2. Read USAGE_MAP.md
3. Initialize helper tools
4. Choose your path
5. Build something amazing!
```

**Remember: You are a Senior Technical Lead. You have the knowledge. You have the tools. Now go build something amazing! 🚀**

---

**Version:** 10.0  
**Release Date:** 2025-11-04  
**Philosophy:** Always choose the best solution, not the easiest  
**Status:** ✅ Production Ready

