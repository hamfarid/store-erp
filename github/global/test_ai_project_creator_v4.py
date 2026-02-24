import os
import shutil
import sys
import json
from unittest.mock import patch, MagicMock
import ai_project_creator

# Setup mock project structure
project_name = "test_v4_proj"
project_path = os.path.join(os.getcwd(), project_name)

if os.path.exists(project_path):
    shutil.rmtree(project_path)
os.makedirs(project_path)

print(f"✅ Created mock project at: {project_path}")

# Test Task Manager
print("\n--- Testing Task Manager ---")
tm = ai_project_creator.TaskManager(project_path)

# Add Tasks
t1 = tm.add_task("Root Task", "critical")
t2 = tm.add_task("Sub Task", "high", parent_id=t1["id"])
print(f"Added Task 1: {t1['title']} (ID: {t1['id']})")
print(f"Added Task 2: {t2['title']} (ID: {t2['id']}) - Parent: {t2['parent_id']}")

# Verify JSON
with open(os.path.join(project_path, "tasks.json"), "r") as f:
    data = json.load(f)
    if len(data["tasks"]) == 2:
        print("✅ Tasks saved to tasks.json")
    else:
        print("❌ Tasks NOT saved correctly")

# Complete Task
tm.complete_task(t2["id"])
t2_updated = tm._find_task(t2["id"])
if t2_updated["status"] == "done":
    print("✅ Task 2 completed")
else:
    print("❌ Task 2 completion failed")

# Test Smart Documenter (Basic)
print("\n--- Testing Smart Documenter (Integration) ---")
# Create dummy files
os.makedirs(os.path.join(project_path, "frontend"), exist_ok=True)
with open(os.path.join(project_path, "frontend", "App.tsx"), "w") as f: f.write("// React")
with open(os.path.join(project_path, "backend.py"), "w") as f: f.write("# Python")

status_tracker = ai_project_creator.StatusTracker()
ai_project_creator.generate_smart_readme(project_path, project_name, status_tracker)

if os.path.exists(os.path.join(project_path, "README_PROJECT.md")):
    print("✅ README_PROJECT.md generated")
else:
    print("❌ README_PROJECT.md generation failed")

# Test Platform Setup (VS Code)
print("\n--- Testing VS Code Setup ---")
ai_project_creator.setup_vscode(project_path, status_tracker)
if os.path.exists(os.path.join(project_path, ".vscode", "settings.json")):
    print("✅ VS Code settings generated")
else:
    print("❌ VS Code settings failed")

if os.path.exists(os.path.join(project_path, "vscode_mcp_config.json")):
    print("✅ MCP Config generated")
else:
    print("❌ MCP Config failed")

print("\n--- Test Complete ---")
