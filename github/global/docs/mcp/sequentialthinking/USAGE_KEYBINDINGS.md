# Reusing MCP keybindings in any new project

To use the same keyboard shortcuts to build/run the MCP `sequentialthinking` image:

1. Copy the two scripts into the new project (if not already):
   - `scripts/mcp_build_sequentialthinking.ps1`
   - `scripts/mcp_run_sequentialthinking.ps1`

2. Ensure the tasks exist in `.vscode/tasks.json` (see `vscode_tasks_template.json`).

3. Merge these keybindings into `.vscode/keybindings.json` in the new project:

```json
[
  { "key": "ctrl+alt+m", "command": "workbench.action.tasks.runTask", "args": "MCP: Build sequentialthinking image", "when": "editorTextFocus" },
  { "key": "ctrl+alt+n", "command": "workbench.action.tasks.runTask", "args": "MCP: Run sequentialthinking image", "when": "editorTextFocus" }
]
```

4. Reload VS Code, then use the shortcuts:
   - Ctrl+Alt+M: Build the Docker image
   - Ctrl+Alt+N: Run the Docker image

Notes
- The tasks must have labels that exactly match the `args` above.
- You can change the key combinations if they conflict in your environment.

