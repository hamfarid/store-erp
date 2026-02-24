# 📦 Global System Installation Guide

This guide explains how to install and activate the **Global AI System (Global System v26 Diamond 32)** in any new project.

---

## 1. Prerequisites

Ensure you have the following installed on your machine:
*   **Python 3.11+**
*   **Node.js 20+** (for MCP)
*   **Git**

---

## 2. Installation Steps

### Step 1: Prepare Project Structure
1.  Go to your new project's root directory (e.g., `MyNewApp/`).
2.  Create a folder named `GitHub`.
3.  Copy the `global_system` folder (from the downloaded zip) into `GitHub`.

**Your structure should look like this:**
```
MyNewApp/
├── (Your project files...)
└── GitHub/
    └── global_system/
        ├── scripts/
        ├── tools/
        ├── config/
        └── ...
```

### Step 2: Activate the System
Open your terminal in the project root (`MyNewApp/`) and run:

```bash
python3 GitHub/global_system/scripts/activate_global.py
```

**What this script does:**
1.  **Deploys Rules**: Links `.cursorrules`, `AGENTS.md`, etc., to your project root.
2.  **Configures MCP**: Sets up `mcp_config.json` for your IDE.
3.  **BooBootstraps Memory: Creates the memory-bank/ folder structure..
4.  **Installs Deps**: Installs necessary Python and Node.js packages.

### Step 3: Verify Installation
Run the preflight check to ensure everything is working:

```bash
python3 GitHub/global_system/tools/preflight_check.py
```

If you see **"ALL SYSTEMS GO"**, you are ready to start!

---

## 3. Next Steps

*   **Read the Handbook**: Open `GitHub/global_system/AI_HANDBOOK.md`.
*   **Start a Task**: Use the workflow defined in `GitHub/global_system/TASKS/UNIVERSAL_LIFECYCLE.md`.
*   **Create a Checkpoint**: Before writing code, run:
    ```bash
    python3 GitHub/global_system/tools/checkpoint_manager.py create --name "init"
    ```

---

## ❓ Troubleshooting

**Issue: "Module not found"**
*   Ensure you ran `activate_global.py`.
*   Try installing dependencies manually: `pip3 install -r GitHub/global_system/config/requirements.txt`

**Issue: "MCP Connection Failed"**
*   Check `mcp_config.json` in your project root.
*   Ensure `npm install` ran successfully in `GitHub/global_system/`.
