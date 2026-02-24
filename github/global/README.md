# Global System v26.0 Diamond 33 (Final v15) 💎

**The Ultimate AI Engineering Framework for Automated Project Creation & Management**

This system is designed to be the "brain" of your AI development workflow. It automates project setup, enforces strict anti-hallucination rules, manages long-term memory via Vector DB/MCP, and now includes **Full Platform Automation** for VS Code, Cursor, and Antigravity.

---

## 🚀 New in v15: Full Platform Automation
The `ai_project_creator.py` wizard now automatically configures your IDE:

### 1. VS Code (Claude Dev / Cline)
- **Auto-Config**: Generates `.vscode/settings.json` optimized for Python/AI.
- **MCP Integration**: Creates `vscode_mcp_config.json` linking Memory & Code Reviewer tools.
- **Prompts Injection**: Copies all roles to `.vscode/prompts/` for easy access.
- **System Instructions**: Generates `CLAUDE_DEV_INSTRUCTIONS.md` for the AI assistant.

### 2. Cursor AI
- **Rules Engine**: Creates `.cursor/rules/` and populates it with role definitions.
- **Auto-Rules**: Generates `.cursorrules` to enforce Memory & Truth Guardian roles.
- **Context Awareness**: Configures Cursor to use local tools automatically.

### 3. Antigravity
- **Path Configuration**: Generates `antigravity.json` pointing to the correct tool paths.

---

## 🧠 Core Features

### 1. Memory & RAG (Retrieval-Augmented Generation)
- **Local Vector DB**: Uses ChromaDB to store and retrieve project context.
- **Memory MCP Server**: A standardized protocol for AI models to read/write memories.
- **Zero Hallucination**: Strict verification steps before answering.

### 2. Automated Code Reviewer (MCP)
- **"Code Rabbit" Style**: An MCP tool that reviews code, finds bugs, and suggests optimizations.
- **Security Checks**: Scans for common vulnerabilities.

### 3. The "Maestro" Wizard (`ai_project_creator.py`)
- Interactive CLI to create new projects or upgrade existing ones.
- Downloads the latest Global System tools automatically.
- Sets up environments, installs dependencies, and configures IDEs.

---

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.10+
- Git

### Quick Start
1. **Download the System**:
   Clone this repository or download the ZIP.

2. **Run the Wizard**:
   ```bash
   python3 ai_project_creator.py
   ```

3. **Follow the Prompts**:
   - Select **(N)ew** or **(E)xisting** project.
   - Enable **RAG** and **Memory MCP** (Recommended).
   - Select your **IDE** (VS Code, Cursor, Antigravity).

4. **Start Coding**:
   The system will prepare your environment. Open your IDE and start working!

---

## 📂 Directory Structure

```
Global_System/
├── ai_project_creator.py       # Main Wizard
├── setup_project.py            # Project Setup Script
├── tools/
│   ├── memory_mcp_server.py    # Memory MCP Server
│   ├── code_reviewer_mcp.py    # Code Reviewer MCP
│   ├── setup_local_rag.py      # RAG Setup
│   └── verify_hallucinations.py # Fact Checker
├── roles/                      # AI Persona Definitions (Truth Guardian, etc.)
├── prompts/                    # System Prompts
├── rules/                      # Operational Rules
├── docs/                       # Documentation
│   ├── README_VSCODE.md        # VS Code Guide
│   └── README_CURSOR.md        # Cursor Guide
└── ...
```

---

## 🛡️ Anti-Hallucination Protocol
1. **Verify**: The AI must verify every claim using `verify_hallucinations.py` or the Memory MCP.
2. **Cite**: All answers must cite sources from the Vector DB.
3. **Refuse**: If unsure, the AI must refuse to answer rather than guess.

---

## 🤝 Contributing
This is a private system for high-performance AI engineering. Updates are managed via the `ai_project_creator.py` script.

**Version**: v15.0 (Diamond 33)
**Date**: Feb 2026
