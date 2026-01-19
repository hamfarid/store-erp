#!/usr/bin/env python3
"""
Speckit v32.0 - The Dynamic Planning Engine
Integrated with Anti-Amnesia & Librarian Protocols.
"""
import os
import json
import sys

# --- Configuration ---
MEMORY_DIR = ".memory"
FILE_REGISTRY = os.path.join(MEMORY_DIR, "file_registry.json")
TODO_FILE = "todo.md"

def load_registry():
    """Loads the Librarian's File Registry."""
    if not os.path.exists(FILE_REGISTRY):
        return {}
    with open(FILE_REGISTRY, 'r') as f:
        return json.load(f)

def scan_project(root_dir):
    """Scans the project for existing files (Reality Check)."""
    existing_files = set()
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            existing_files.add(full_path)
    return existing_files

def generate_plan(goal, existing_files):
    """Generates a plan based on the goal and reality."""
    plan = []
    plan.append(f"# Project Plan: {goal}")
    plan.append("## 1. Analysis")
    
    if not existing_files:
        plan.append("- [ ] Initialize Project Structure (Greenfield)")
    else:
        plan.append(f"- [ ] Analyze {len(existing_files)} existing files (Brownfield)")

    plan.append("## 2. Execution")
    plan.append("- [ ] Create 'project_memory.md'")
    plan.append("- [ ] Setup 'global/rules' (v32.0)")
    
    return "\n".join(plan)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 speckit.py <project_goal>")
        sys.exit(1)

    goal = sys.argv[1]
    root_dir = os.getcwd()
    
    print(f"🚀 Speckit v32.0 Initializing for: {goal}")
    
    # 1. Librarian Check
    registry = load_registry()
    print(f"📚 Registry loaded: {len(registry)} files known.")
    
    # 2. Reality Check
    real_files = scan_project(root_dir)
    print(f"🔍 Reality check: {len(real_files)} files found on disk.")
    
    # 3. Generate Plan
    plan_content = generate_plan(goal, real_files)
    
    # 4. Write Plan
    with open(TODO_FILE, 'w') as f:
        f.write(plan_content)
    
    print(f"✅ Plan generated in '{TODO_FILE}'. Ready to execute.")

if __name__ == "__main__":
    main()
