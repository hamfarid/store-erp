# Quick Reference: Memory & MCP Systems

**Status:** ✅ Initialized and Ready  
**Date:** 2025-11-05

---

## 📁 Locations

### Helper Tools (AI's Tools)
```
C:\Users\hadym\.global\
├── memory\              # AI memory system
│   ├── conversations\
│   ├── knowledge\
│   ├── preferences\
│   ├── state\
│   ├── checkpoints\
│   ├── decisions\
│   └── summaries\
└── mcp\                 # MCP system
    ├── servers\
    ├── logs\
    └── config\
        └── mcp_config.json
```

### Your Project
```
D:\APPS_AI\store\Store\
├── backend\             # Flask backend
├── frontend\            # React frontend
└── global\              # Project tracking (different!)
```

---

## 🔧 Quick Commands

### Check Memory System
```powershell
# View memory directory
dir $env:USERPROFILE\.global\memory

# View current state
type $env:USERPROFILE\.global\memory\state\current_state.json

# View project context
type $env:USERPROFILE\.global\memory\state\store_project_context.json

# View decisions
dir $env:USERPROFILE\.global\memory\decisions
```

### Check MCP System
```powershell
# View MCP configuration
type $env:USERPROFILE\.global\mcp\config\mcp_config.json

# View MCP directory
dir $env:USERPROFILE\.global\mcp
```

---

## 🎯 MCP Servers

### Active Servers
- ✅ **Sentry** - Error monitoring (gaara-group org)

### Available Servers (Enable as needed)
- ⚪ **Cloudflare** - Workers, D1, R2, KV
- ⚪ **Playwright** - Browser automation
- ⚪ **GitHub** - Repository management

### Enable a Server
Edit `C:\Users\hadym\.global\mcp\config\mcp_config.json`:
```json
{
  "playwright": {
    "enabled": true,  // Change false to true
    ...
  }
}
```

---

## 💡 Common Tasks

### Save a Decision to Memory
```python
import json
from pathlib import Path
from datetime import datetime

memory_dir = Path.home() / '.global' / 'memory'
decision = {
    "timestamp": datetime.now().isoformat(),
    "type": "decision",
    "decision": "Your decision here",
    "rationale": "Why you made this decision",
    "impact": "high/medium/low"
}

file_path = memory_dir / 'decisions' / f'decision_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
file_path.write_text(json.dumps(decision, indent=2))
```

### Check Current State
```python
import json
from pathlib import Path

memory_dir = Path.home() / '.global' / 'memory'
state_file = memory_dir / 'state' / 'current_state.json'

with open(state_file) as f:
    state = json.load(f)
    print(json.dumps(state, indent=2))
```

### Use Sentry MCP
The Sentry MCP is already active! You can:
- Monitor errors in Store project
- Track performance issues
- Analyze user impact
- Get detailed stack traces

---

## 📋 Best Practices

### DO ✅
- Save important decisions to memory
- Check MCP servers before starting tasks
- Maintain environment separation
- Use memory for context retention
- Track progress in state files

### DON'T ❌
- Mix helper tools with project code
- Store project data in memory system
- Skip memory for important decisions
- Forget to check available MCP tools

---

## 🚀 Next Steps

1. **Start using memory:**
   - Save decisions as you make them
   - Track progress in state files
   - Create checkpoints at milestones

2. **Leverage Sentry MCP:**
   - Monitor Store project errors
   - Track performance metrics
   - Analyze production issues

3. **Enable more MCP servers:**
   - Playwright for testing
   - GitHub for repo management
   - Cloudflare if using their services

4. **Maintain separation:**
   - Helper tools: `~/.global/`
   - Project code: `~/Store/`
   - Never mix!

---

## 📚 Full Documentation

- **Detailed Report:** `MEMORY_MCP_INITIALIZATION_REPORT.md`
- **Memory Guide:** `global/knowledge/core/memory.md`
- **MCP Guide:** `global/knowledge/core/mcp.md`
- **Environment Guide:** `global/knowledge/core/environment.md`

---

**Everything is ready! Start working with full context! 🎉**

