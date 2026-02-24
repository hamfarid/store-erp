# GitHub Copilot Custom Instructions Research

## Source
- URL: https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- Date: November 4, 2025

## Key Findings

### Types of Instructions Files

VS Code supports **3 types** of Markdown-based instructions files:

1. **`.github/copilot-instructions.md`** file
   - Automatically applies to **all chat requests** in the workspace
   - Stored in the root of the workspace
   - Compatible with Visual Studio and GitHub.com

2. **`.instructions.md`** files (multiple files)
   - Created for **specific tasks or files**
   - Use `applyTo` frontmatter to define which files the instructions apply to
   - Can be workspace-specific or user-specific (stored in VS Code profile)

3. **`AGENTS.md`** file (experimental)
   - Useful if you work with multiple AI agents
   - Automatically applies to all chat requests in the workspace
   - Stored in the root of the workspace

### File Locations

**Workspace instructions files:**
- `.github/copilot-instructions.md` - stored in workspace root
- `.github/instructions/` folder - for workspace-specific .instructions.md files
- `AGENTS.md` - stored in workspace root

**User instructions files:**
- Stored in the current VS Code profile
- Available across multiple workspaces

### How to Use `.github/copilot-instructions.md`

1. **Enable the setting:**
   - `github.copilot.chat.codeGeneration.useInstructionFiles` setting

2. **Create the file:**
   - Create `.github/copilot-instructions.md` at the root of your workspace
   - If needed, create `.github` directory first

3. **Write instructions:**
   - Use natural language
   - Use Markdown format
   - Whitespace between instructions is ignored
   - Can be written as single paragraph, each on new line, or separated by blank lines

4. **Reference context:**
   - Can use Markdown links to reference files or URLs

### `.instructions.md` Files Format

**File extension:** `.instructions.md`

**Structure:**
- **Header (optional):** YAML frontmatter
  - `description`: Description shown on hover in Chat view
  - `applyTo`: Glob pattern for automatic application (use `**` for all files), relative to the workspace root

**Example:**
```markdown
---
description: React component guidelines
applyTo: src/**/*.tsx
---

# React Component Guidelines

- Use functional components with hooks
- Implement proper TypeScript interfaces for props
```

**Usage:**
- Instructions files are used when **creating or modifying files**
- Typically **not applied for read operations**
- Can manually attach via **Add Context > Instructions** in Chat view

### Important Notes

**Custom instructions are NOT taken into account for:**
- Code completions as you type in the editor

**They only apply to:**
- Chat requests
- Code generation via Chat

### Settings Configuration

**Setting name:** `github.copilot.chat.codeGeneration.useInstructionFiles`

**Must be enabled** to use `.github/copilot-instructions.md` file.

### Compatibility

- **VS Code:** Full support
- **Visual Studio:** Supports `.github/copilot-instructions.md`
- **GitHub.com:** Supports `.github/copilot-instructions.md`

---

## CRITICAL FINDINGS

### ✅ CORRECT: Our Implementation

1. **File location:** `.github/copilot-instructions.md` ✅
2. **File format:** Markdown ✅
3. **Natural language instructions** ✅

### ❌ INCORRECT/MISSING: Our Implementation

1. **Settings configuration:** We didn't mention that users need to enable `github.copilot.chat.codeGeneration.useInstructionFiles` setting ❌
2. **Alternative file types:** We didn't mention `.instructions.md` files or `AGENTS.md` ❌
3. **Limitations:** We didn't mention that instructions don't apply to code completions ❌

### ✅ CORRECT: Our Documentation

1. **Setup instructions:** We correctly showed how to configure settings.json ✅
2. **File path:** We correctly used `.github/copilot-instructions.md` ✅
3. **Content format:** We correctly used natural language in Markdown ✅

---

## Comparison with Augment

| Feature | Augment | GitHub Copilot |
|---------|---------|----------------|
| **File location** | `.augment/rules/` | `.github/copilot-instructions.md` |
| **Multiple files** | Yes (multiple rule files) | Yes (multiple .instructions.md files) |
| **File format** | Markdown with YAML frontmatter | Markdown (with optional YAML for .instructions.md) |
| **Types** | Always, Auto (agent_requested), Manual | Single file (all), Multiple files (applyTo), AGENTS.md |
| **Frontmatter** | Required for type specification | Optional (only for .instructions.md with applyTo) |
| **Auto-detection** | Yes (agent_requested with description) | Yes (.instructions.md with applyTo glob pattern) |
| **Settings required** | No (auto-discovers) | Yes (must enable useInstructionFiles) |
| **Applies to** | Agent and Chat only | Chat only (not code completions) |

---

## Next Steps

1. Update documentation to mention the required setting
2. Add information about .instructions.md files as alternative
3. Clarify that instructions don't apply to code completions
4. Update examples to match official documentation

