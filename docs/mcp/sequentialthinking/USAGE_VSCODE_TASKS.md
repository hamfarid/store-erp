# Reusing MCP SequentialThinking tasks in any new project

These tasks call PowerShell scripts under `scripts/` to build/run the MCP `sequentialthinking` Docker image. To use them in a different project:

1. Copy the two scripts into the new project (include `scripts/` in repo):
   - `scripts/mcp_build_sequentialthinking.ps1`
   - `scripts/mcp_run_sequentialthinking.ps1`

2. Merge the tasks into the new project’s `.vscode/tasks.json`:
   - Use `docs/mcp/sequentialthinking/vscode_tasks_template.json` as a reference.
   - If `.vscode/tasks.json` doesn’t exist yet, you can copy the whole file; otherwise, paste the two task objects into the existing `tasks` array.

3. Run tasks from VS Code Command Palette:
   - `Tasks: Run Task` → `MCP: Build sequentialthinking image`
   - `Tasks: Run Task` → `MCP: Run sequentialthinking image`

Notes
- The build script clones the official MCP repo into `D:\APPS_AI\servers` by default and checks out tag `2025.4.6`. Override with parameters if needed: `-BaseDir`, `-RepoName`, `-Tag`.
- Ensure `git` and `docker` are installed and available on PATH on the machine where you run these tasks.

