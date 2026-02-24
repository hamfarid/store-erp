import os
import shutil
import sys
import json
import time
from unittest.mock import patch, MagicMock
import ai_project_creator

# Setup mock project structure
project_name = "test_v5_proj"
project_path = os.path.join(os.getcwd(), project_name)

if os.path.exists(project_path):
    shutil.rmtree(project_path)
os.makedirs(project_path)

print(f"✅ Created mock project at: {project_path}")

# Test Project Config
print("\n--- Testing Project Config ---")
cfg = ai_project_creator.ProjectConfig(project_path)
if cfg.save_defaults(project_path):
    print("✅ Config file created")
else:
    print("❌ Config file creation failed")

if cfg.get("default_platform") == "1":
    print("✅ Config loaded correctly")
else:
    print("❌ Config load failed")

# Test Plugin System
print("\n--- Testing Plugin System ---")
pm = ai_project_creator.PluginManager(project_path)
if pm.ensure_dir():
    print("✅ Plugins directory created")
else:
    print("❌ Plugins directory creation failed")

# Create a dummy plugin
plugin_code = """
PLUGIN_NAME = "test_plugin"
PLUGIN_VERSION = "0.1"
def on_task_added(task, **kwargs):
    return f"Task {task['title']} added!"
"""
with open(os.path.join(project_path, "plugins", "test_plugin.py"), "w") as f:
    f.write(plugin_code)

pm = ai_project_creator.PluginManager(project_path) # Reload to find plugin
if len(pm.plugins) >= 1:
    print(f"✅ Plugin loaded: {pm.plugins[0]['name']}")
else:
    print("❌ Plugin load failed")

# Test Task Manager (Enhanced)
print("\n--- Testing Task Manager (Enhanced) ---")
tm = ai_project_creator.TaskManager(project_path)

# Add Tasks with Dependencies
t1 = tm.add_task("Core Task", "critical")
t2 = tm.add_task("Dependent Task", "high", depends_on=[t1["id"]])
print(f"Added Task 1: {t1['title']} (ID: {t1['id']})")
print(f"Added Task 2: {t2['title']} (ID: {t2['id']}) - Depends on: {t2['depends_on']}")

# Try to complete dependent task (should fail)
if not tm.complete_task(t2["id"]):
    print("✅ Dependency check working (prevented completion)")
else:
    print("❌ Dependency check failed (allowed completion)")

# Complete core task then dependent task
tm.complete_task(t1["id"])
if tm.complete_task(t2["id"]):
    print("✅ Dependency resolution working")
else:
    print("❌ Dependency resolution failed")

# Test Export
print("\n--- Testing Export ---")
tm.export_tasks("csv")
print("✅ Export function called")

# Test Snapshot (Mocking file operations)
print("\n--- Testing Snapshot ---")
# Create some files
with open(os.path.join(project_path, "file1.txt"), "w") as f: f.write("content1")
snap_path = ai_project_creator.create_snapshot(project_path)
if os.path.exists(snap_path):
    print(f"✅ Snapshot created at {snap_path}")
else:
    print("❌ Snapshot creation failed")

# Modify file
with open(os.path.join(project_path, "file1.txt"), "w") as f: f.write("modified")

# Rollback (Mocking input)
print("\n--- Testing Rollback ---")
with patch('builtins.input', side_effect=['1', 'y']):
    if ai_project_creator.rollback_snapshot(project_path):
        with open(os.path.join(project_path, "file1.txt"), "r") as f:
            if f.read() == "content1":
                print("✅ Rollback successful (content restored)")
            else:
                print("❌ Rollback failed (content mismatch)")
    else:
        print("❌ Rollback function returned False")

print("\n--- Test Complete ---")
