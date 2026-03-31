# MCP Configuration & Auto-Generation (v24.0)

## 1. The "Auto-Config" Protocol
The system can automatically generate `mcp_config.json` based on project needs.

### Detection Logic
*   **Postgres Detected?** -> Add `postgres` server.
*   **Filesystem Access Needed?** -> Add `filesystem` server.
*   **GitHub Repo?** -> Add `github` server.

### Generation Command
When initializing a project, run:
```bash
# Conceptual command - implemented via AI logic
generate_mcp_config --detect
```

## 2. Standard MCP Servers (v24.0)
1.  **Context7 (Exa):** For external search & docs.
2.  **Playwright:** For E2E testing.
3.  **Postgres:** For database inspection.
4.  **Filesystem:** For safe file operations.

## 3. Usage Rule
*   **Always check `mcp_config.json`** at the start of a session.
*   If a tool is missing, suggest adding the corresponding server to the user.
