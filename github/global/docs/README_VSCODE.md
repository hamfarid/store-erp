# VS Code (Claude Dev / Cline) Setup Guide - Global System v26

## 🚀 Automated Setup (Recommended)
The easiest way to set up VS Code is using the **AI Project Creator Wizard**:

1. Run the wizard:
   ```bash
   python3 ai_project_creator.py
   ```
2. Select **VS Code** when asked for your platform.
3. The wizard will automatically:
   - Create `.vscode/settings.json`
   - Generate `vscode_mcp_config.json`
   - Copy roles to `.vscode/prompts/`
   - Create `CLAUDE_DEV_INSTRUCTIONS.md`

---

## ⚙️ Manual Configuration (If needed)

### 1. Install Extensions
- **Claude Dev** (or Cline)
- **Python** (Microsoft)
- **Pylance**

### 2. Configure MCP Servers
Copy the content of `vscode_mcp_config.json` into your Claude Dev settings:
1. Open Claude Dev settings.
2. Go to **MCP Servers**.
3. Paste the JSON configuration.

### 3. Set Custom Instructions
Copy the content of `CLAUDE_DEV_INSTRUCTIONS.md` into the **Custom Instructions** field in Claude Dev. This ensures the AI follows the Global System rules (Truth Guardian, Memory Guardian).

### 4. Usage
- **Memory**: Ask "What do you remember about this project?" to query the Vector DB.
- **Code Review**: Ask "Review this file" to trigger the Code Reviewer MCP.
- **Roles**: The AI will automatically adopt roles defined in `.vscode/prompts/`.
