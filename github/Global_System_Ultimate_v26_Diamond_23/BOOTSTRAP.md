# Global System v26.0 (Diamond 30) - Bootstrap Guide

## 1. Initial Setup
1.  **Clone the Repository:**
    ```bash
    git clone <repo_url>
    cd <project_name>
    ```

2.  **Run the IDE Configuration Wizard:**
    This step is crucial for setting up your development environment correctly.
    ```bash
    python3 scripts/configure_ide.py
    ```
    Follow the on-screen instructions to select your IDE (Cursor, VS Code, Cline, etc.). This will:
    - Copy the necessary configuration files (e.g., `.cursorrules`, `.vscode/settings.json`).
    - Activate MCP (Model Context Protocol) integration.
    - Optimize the environment for your chosen tool.

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the System:**
    ```bash
    python3 scripts/speckit.py init
    ```

## 2. Verification
- Check that the configuration files for your IDE have been created.
- Verify that `mcp_config.json` is present and correctly configured.
- Run `python3 scripts/audit_system.py` to ensure system integrity.

## 3. Start Developing
- Use `speckit.py` for task management.
- Refer to `GLOBAL_PROFESSIONAL_CORE_PROMPT.md` for core principles.
