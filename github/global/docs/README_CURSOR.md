# Cursor AI Setup Guide - Global System v26

## 🚀 Automated Setup (Recommended)
The **AI Project Creator Wizard** makes setting up Cursor effortless:

1. Run the wizard:
   ```bash
   python3 ai_project_creator.py
   ```
2. Select **Cursor** when asked for your platform.
3. The wizard will automatically:
   - Create `.cursor/rules/` directory.
   - Copy all role definitions (Truth Guardian, Memory Guardian, etc.) into `.cursor/rules/`.
   - Generate `.cursorrules` file with strict anti-hallucination protocols.

---

## 🧠 How It Works
Cursor AI (v0.40+) supports a `.cursorrules` file and a `.cursor/rules/` folder for defining AI behavior.

### 1. Role Injection
The wizard injects specialized roles into `.cursor/rules/`. When you mention a role (e.g., "Act as Truth Guardian"), Cursor will automatically load the corresponding rule file.

### 2. Anti-Hallucination
The `.cursorrules` file enforces a strict protocol:
- **Verify**: Before answering, the AI must check its internal knowledge or use the `memory` tool.
- **Cite**: It must cite sources from the project context.
- **Refuse**: It will refuse to guess if information is missing.

### 3. Tool Integration
Cursor will automatically detect the local tools provided by the Global System:
- `tools/verify_hallucinations.py`: For fact-checking.
- `tools/code_reviewer_mcp.py`: For code auditing.

---

## ⚙️ Manual Configuration (If needed)
If you prefer manual setup:
1. Create a `.cursor/rules/` folder in your project root.
2. Copy all markdown files from `roles/` into `.cursor/rules/`.
3. Create a `.cursorrules` file in the root with the following content:

```markdown
# Cursor AI Rules (Global System v26)

## Core Behavior
- You are part of the Global System v26.
- You MUST check `.cursor/rules/` for specific role definitions.
- You MUST use the `memory` tool (if available) to verify context.

## Roles
- **Truth Guardian**: Verify all factual claims.
- **Memory Guardian**: Manage project context.

## Tools
- Use `tools/verify_hallucinations.py` for fact-checking.
```
