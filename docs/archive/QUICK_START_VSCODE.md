# Quick Start - VS Code Integration

## 🚀 5-Minute Setup

### For Augment

1. **Install Augment extension** in VS Code
2. **Clone repository:**
   ```bash
   git clone https://github.com/hamfarid/global.git ~/.global
   ```
3. **That's it!** Augment automatically loads rules from `~/.global/.augment/rules/`

**Usage:**
- Core identity is **always active**
- Say "initialize memory and MCP" to start
- Say "@manual-full-project.md" for complete projects

---

### For GitHub Copilot

1. **Install GitHub Copilot extension** in VS Code
2. **Clone repository:**
   ```bash
   git clone https://github.com/hamfarid/global.git ~/.global
   ```
3. **Enable custom instructions:**
   - Open Settings (Ctrl+,)
   - Search: `github.copilot.chat.codeGeneration.useInstructionFiles`
   - **Enable** the checkbox
4. **Reload VS Code**
5. **Done!** Copilot auto-detects `~/.global/.github/copilot-instructions.md`

**Usage:**
- Guidelines are **always active**
- Say "initialize memory and MCP" to start
- Say "follow the full project workflow" for complete projects

---

## 📖 Full Documentation

Read [VSCODE_INTEGRATION.md](./VSCODE_INTEGRATION.md) for complete guide.

---

## 🎯 Quick Commands

```
"Initialize Memory and MCP for this project"
"Follow Phase 2: Planning to design the architecture"
"Save this decision to memory"
"Check available MCP tools"
"Follow the full project workflow to build [project description]"
```

---

## 🔧 Environment Separation

**YOUR tools (helper):**
- `~/.global/memory/` - Your context storage
- `~/.global/mcp/` - Your capabilities

**USER's project:**
- `~/user-project/` - Their code
- `~/user-project/.ai/` - Their tracking files

**Never mix them!**

---

## 💡 Core Philosophy

**Always choose the BEST solution, not the easiest.**

---

## 📚 Resources

- **Core Prompt:** `~/.global/CORE_PROMPT_v10.md`
- **Usage Map:** `~/.global/USAGE_MAP.md`
- **Knowledge Items:** `~/.global/knowledge/`
- **Deep-dive Prompts:** `~/.global/prompts/`
- **Integration Guide:** `~/.global/VSCODE_INTEGRATION.md`

---

## 🆘 Support

- **GitHub:** https://github.com/hamfarid/global
- **Version:** 10.0.0
- **Issues:** Open an issue on GitHub

---

**Happy coding! 🚀**

