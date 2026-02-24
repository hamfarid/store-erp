import os
import shutil
import sys
from unittest.mock import patch
import ai_project_creator

# Mock user inputs: 
# 1. New Project (N)
# 2. Project Name (test_vscode_proj)
# 3. Use RAG (n) - skipping for speed
# 4. Use Memory MCP (n) - skipping for speed
# 5. Use Code Reviewer (n) - skipping for speed
# 6. Platform: VS Code (1)

inputs = iter(["N", "test_vscode_proj", "n", "n", "n", "1"])

def mock_input(prompt, default=None):
    try:
        val = next(inputs)
        print(f"[Mock Input] {prompt} -> {val}")
        return val
    except StopIteration:
        return default

# Mock run_command to avoid git clone and setup_project execution
def mock_run_command(command, cwd=None, check=True, shell=True):
    print(f"[Mock Command] {command}")
    # Simulate git clone by creating a dummy folder structure in the temp directory
    if "git clone" in command:
        target_dir = command.split()[-1]
        os.makedirs(target_dir, exist_ok=True)
        # Create dummy roles in the temp directory so they get copied to project_path
        os.makedirs(os.path.join(target_dir, "roles"), exist_ok=True)
        with open(os.path.join(target_dir, "roles", "role1.md"), "w") as f: f.write("Role 1")
        return True
    return True

# Patch functions
ai_project_creator.get_input = mock_input
ai_project_creator.run_command = mock_run_command

# Run main
try:
    ai_project_creator.main()
except SystemExit:
    pass

# Verify VS Code specific files
project_path = os.path.join(os.getcwd(), "test_vscode_proj")
vscode_dir = os.path.join(project_path, ".vscode")
prompts_dir = os.path.join(vscode_dir, "prompts")
settings_file = os.path.join(vscode_dir, "settings.json")
mcp_config = os.path.join(project_path, "vscode_mcp_config.json")
instructions = os.path.join(project_path, "CLAUDE_DEV_INSTRUCTIONS.md")

print("\n--- Verification Results ---")
if os.path.exists(vscode_dir): print("✅ .vscode directory created")
else: print("❌ .vscode directory MISSING")

if os.path.exists(prompts_dir): print("✅ .vscode/prompts directory created")
else: print("❌ .vscode/prompts directory MISSING")

if os.path.exists(os.path.join(prompts_dir, "role1.md")): print("✅ Roles copied to prompts")
else: print("❌ Roles NOT copied")

if os.path.exists(settings_file): print("✅ settings.json created")
else: print("❌ settings.json MISSING")

if os.path.exists(mcp_config): print("✅ vscode_mcp_config.json created")
else: print("❌ vscode_mcp_config.json MISSING")

if os.path.exists(instructions): print("✅ CLAUDE_DEV_INSTRUCTIONS.md created")
else: print("❌ CLAUDE_DEV_INSTRUCTIONS.md MISSING")

# Cleanup
# shutil.rmtree(project_path)
