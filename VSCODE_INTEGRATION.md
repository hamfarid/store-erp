# VS Code Integration Guide - Global Guidelines v10.0

## نظرة عامة / Overview

هذا الدليل يشرح كيفية استخدام Global Guidelines مع Augment و GitHub Copilot في VS Code.

This guide explains how to use Global Guidelines with Augment and GitHub Copilot in VS Code.

---

## المتطلبات / Requirements

### For Augment
- VS Code installed
- Augment extension installed from VS Code marketplace
- Augment account (free or paid)

### For GitHub Copilot
- VS Code installed
- GitHub Copilot extension installed
- GitHub Copilot subscription (paid)

---

## التثبيت / Installation

### Step 1: Clone the Repository

```bash
# Clone to your home directory
cd ~
git clone https://github.com/hamfarid/global.git ~/.global

# Or if already cloned, pull latest changes
cd ~/.global
git pull origin main
```

### Step 2: Verify Structure

```bash
cd ~/.global
ls -la

# You should see:
# .augment/              # Augment rules
# .github/               # GitHub Copilot instructions
# knowledge/             # Knowledge items
# prompts/               # Deep-dive prompts
# CORE_PROMPT_v10.md     # Core identity
# USAGE_MAP.md           # Navigation guide
# VSCODE_INTEGRATION.md  # This file
```

---

## استخدام Augment / Using Augment

### How Augment Works

Augment uses a **rules system** with three types:
1. **Always rules** - Applied to every conversation
2. **Auto rules** - Applied when keywords detected
3. **Manual rules** - Applied when @ mentioned

### Rules Location

```
~/.global/.augment/rules/
├── always-core-identity.md    # Always applied
├── auto-memory.md             # Auto: memory, context, remember
├── auto-mcp.md                # Auto: mcp, tools, capabilities
└── manual-full-project.md     # Manual: @ mention
```

### Usage in VS Code

#### 1. Core Identity (Always Active)

The `always-core-identity.md` is **always applied** to every conversation. It defines:
- Who you are (Senior Technical Lead)
- Your helper tools (Memory, MCP)
- Environment separation
- Core philosophy (best solution, not easiest)
- Quality standards

**You don't need to do anything** - it's always active!

#### 2. Memory System (Auto)

When you mention keywords like "memory", "context", "remember", "save", "recall", the `auto-memory.md` rule is automatically applied.

**Example:**
```
"Save this decision to memory"
"Remember the project context"
"What do we have in memory?"
```

#### 3. MCP System (Auto)

When you mention keywords like "mcp", "tools", "capabilities", "servers", "integration", the `auto-mcp.md` rule is automatically applied.

**Example:**
```
"Check available MCP tools"
"Use MCP to access database"
"What MCP servers are available?"
```

#### 4. Full Project Workflow (Manual)

For complete projects, **@ mention** the full project workflow:

**Example:**
```
@manual-full-project.md I need to build a complete e-commerce platform
```

This loads the complete project lifecycle workflow (Phase 0-5).

### Best Practices with Augment

1. **Start with initialization:**
   ```
   "Initialize Memory and MCP for this project"
   ```

2. **For complete projects:**
   ```
   @manual-full-project.md Build a task management app with React and Node.js
   ```

3. **For specific features:**
   ```
   "Add authentication to the existing app" (auto rules will apply)
   ```

4. **Save important decisions:**
   ```
   "Save this architecture decision to memory"
   ```

---

## استخدام GitHub Copilot / Using GitHub Copilot

### How GitHub Copilot Works

GitHub Copilot uses a **single instructions file** that is always applied to all conversations.

### Instructions Location

```
~/.global/.github/copilot-instructions.md
```

### Setup in VS Code

#### Step 1: Enable Custom Instructions

1. Open VS Code Settings (Ctrl+, or Cmd+,)
2. Search for: `github.copilot.chat.codeGeneration.useInstructionFiles`
3. **Enable** the checkbox (check it)

#### Step 2: Reload VS Code

1. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)
2. Type "Reload Window" and press Enter

#### Step 3: Verify

Copilot will automatically detect and use `~/.global/.github/copilot-instructions.md`

**That's it!** No need to edit settings.json manually.

#### Alternative: Settings JSON (Advanced)

If you prefer to edit settings.json directly:

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true
}
```

### Usage in VS Code

Once configured, GitHub Copilot will **always** use the Global Guidelines in all conversations.

**Example conversations:**

```
"Initialize Memory and MCP for this project"
"Build a REST API with Express and PostgreSQL"
"Add authentication with JWT"
"Save this decision to memory"
"Check available MCP tools"
```

### Best Practices with GitHub Copilot

1. **Always start with initialization:**
   ```
   "Initialize Memory and MCP for this new project"
   ```

2. **Reference the workflow explicitly:**
   ```
   "Follow the full project workflow to build an e-commerce platform"
   ```

3. **Be specific about phases:**
   ```
   "We're in Phase 2: Planning. Help me design the architecture."
   ```

4. **Save to memory regularly:**
   ```
   "Save this architecture decision to memory"
   ```

---

## الفرق بين Augment و GitHub Copilot / Differences

| Feature | Augment | GitHub Copilot |
|---------|---------|----------------|
| **Rules System** | 3 types (Always, Auto, Manual) | Single instructions file |
| **Activation** | Always + Auto-detect + @ mention | Always applied |
| **Flexibility** | High (modular rules) | Medium (single file) |
| **File Location** | `~/.global/.augment/rules/` | `~/.global/.github/copilot-instructions.md` |
| **Best For** | Complex projects with phases | General coding assistance |

---

## سير العمل الموصى به / Recommended Workflow

### For Complete Projects (Both Tools)

```
1. Initialize
   "Initialize Memory and MCP for this project"

2. Plan
   "Follow Phase 2: Planning to design the architecture"
   
3. Build
   "Follow Phase 3: Build to implement features"
   
4. Finalize
   "Follow Phase 4: Finalize to complete testing and documentation"
   
5. Deliver
   "Follow Phase 5: Deliver to deploy and handoff"
```

### For Feature Development (Both Tools)

```
1. Initialize
   "Initialize Memory and MCP"

2. Understand
   "Read the existing codebase and understand the architecture"
   
3. Plan
   "Design the new feature following best practices"
   
4. Implement
   "Implement the feature with tests and documentation"
   
5. Deliver
   "Verify quality gates and deliver"
```

---

## القيود المهمة / Important Limitations

### Augment Rules

**Rules apply to:**
- ✅ Agent (AI coding assistant)
- ✅ Chat (conversations)

**Rules do NOT apply to:**
- ❌ Completions (autocomplete as you type)
- ❌ Instructions (Ctrl+I inline edits)
- ❌ Next Edit (suggested edits)

### GitHub Copilot Instructions

**Instructions apply to:**
- ✅ Chat requests
- ✅ Code generation via Chat

**Instructions do NOT apply to:**
- ❌ Code completions (autocomplete as you type in editor)

### Why This Matters

- **For complex tasks:** Use Chat/Agent (instructions apply)
- **For quick autocomplete:** Instructions won't affect it (by design)
- **For best results:** Always use Chat for important decisions

---

## الأسئلة الشائعة / FAQ

### Q: Which tool should I use?

**A:** Both tools work with Global Guidelines:
- **Augment:** Better for complex projects with multiple phases (modular rules)
- **GitHub Copilot:** Better for general coding assistance (simpler setup)

### Q: Can I use both tools together?

**A:** Yes! Both tools can coexist. Configure both and use whichever you prefer.

### Q: How do I update the guidelines?

**A:**
```bash
cd ~/.global
git pull origin main
```

Then reload VS Code.

### Q: Where are my helper tools?

**A:**
- **Memory:** `~/.global/memory/` (YOUR tool, not the project)
- **MCP:** `~/.global/mcp/` (YOUR tool, not the project)

### Q: Where is my project?

**A:**
- **Project:** `~/user-project/` (USER's code)
- **Tracking:** `~/user-project/.ai/` (USER's tracking files)

**Never mix them!**

### Q: How do I verify environment separation?

**A:** Ask the AI:
```
"Show me the environment separation. Where are my helper tools and where is the user's project?"
```

The AI should clearly distinguish:
- `~/.global/` - YOUR tools
- `~/user-project/` - USER's project

### Q: What if the AI doesn't follow the guidelines?

**A:**
1. **For Augment:** Verify rules are in `~/.global/.augment/rules/`
2. **For GitHub Copilot:** Verify `useInstructionFiles` is enabled in Settings
3. Reload VS Code
4. Explicitly remind the AI:
   ```
   "Follow the Global Guidelines. Initialize Memory and MCP first."
   ```

### Q: How do I access deep-dive prompts?

**A:** The `prompts/` folder contains 21 detailed modules (800KB) for complex scenarios:
```
~/.global/prompts/
├── 01_core_identity.md
├── 02_thinking_framework.md
├── 03_environment_separation.md
├── ...
└── 21_quality_gates.md
```

Reference them when needed:
```
"Read ~/.global/prompts/05_architecture_design.md for architecture guidance"
```

---

## الدعم / Support

### Documentation
- **Core Prompt:** `~/.global/CORE_PROMPT_v10.md`
- **Usage Map:** `~/.global/USAGE_MAP.md`
- **README:** `~/.global/README_v10.md`
- **Knowledge Items:** `~/.global/knowledge/`
- **Deep-dive Prompts:** `~/.global/prompts/`

### Repository
- **GitHub:** https://github.com/hamfarid/global
- **Version:** 10.0.0

### Issues
- Open an issue on GitHub
- Include: tool (Augment/Copilot), VS Code version, error message

---

## الخلاصة / Summary

✅ **Augment:** Modular rules system (Always, Auto, Manual)  
✅ **GitHub Copilot:** Single instructions file (always applied)  
✅ **Both:** Support complete Global Guidelines v10.0  
✅ **Location:** `~/.global/` (YOUR tools, not the project)  
✅ **Philosophy:** Always choose the best solution, not the easiest  
✅ **Workflow:** Initialize → Plan → Build → Finalize → Deliver  
✅ **Quality:** 95%+ coverage, best practices, complete documentation  

**Happy coding! 🚀**

