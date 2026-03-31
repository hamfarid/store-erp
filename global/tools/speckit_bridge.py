#!/usr/bin/env python3
import os
import sys
import subprocess
import json
from datetime import datetime

# --- CONFIGURATION ---
GLOBAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = ".memory"
REGISTRY_FILE = os.path.join(MEMORY_DIR, "file_registry.json")
HELPERS_DIR = os.path.join(GLOBAL_ROOT, "helpers")
REAL_CLI = "specify"

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def check_librarian_registry(file_path):
    """Checks if a file exists in the Librarian Registry."""
    if not os.path.exists(REGISTRY_FILE):
        return False
    
    with open(REGISTRY_FILE, "r") as f:
        registry = json.load(f)
    
    return os.path.basename(file_path) in registry

def load_template(template_name):
    """Loads a template from global/helpers/."""
    template_path = os.path.join(HELPERS_DIR, template_name)
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            return f.read()
    return ""

def init_project(project_name):
    """Initialize a new Speckit project with System Templates."""
    log(f"Initializing Speckit for: {project_name}", "SPECKIT")
    
    # 1. Run real specify init
    try:
        subprocess.run([REAL_CLI, "init"], check=False)
    except FileNotFoundError:
        log(f"'{REAL_CLI}' command not found. Please install spec-kit.", "ERROR")
        # Continue anyway to generate our structure
    
    # 2. Inject System Templates into the Spec
    spec_template = load_template("Task_List_Template.md") # Using Task List as a base for Specs
    
    if not os.path.exists("specs"):
        os.makedirs("specs")
        
    initial_spec = os.path.join("specs", "00_initial_project.spec.md")
    
    content = f"""# Spec: {project_name} Initialization
**Role:** The Architect
**Date:** {datetime.now().strftime("%Y-%m-%d")}

## 1. Overview
(Auto-generated from System Template)
{spec_template}

## 2. Requirements
*   [ ] Setup Project Structure
*   [ ] Initialize Git
*   [ ] Create Virtual Environment
"""
    with open(initial_spec, "w") as f:
        f.write(content)
        
    log(f"Created initial spec with System Template: {initial_spec}", "SUCCESS")

def generate_tasks_from_spec(spec_file):
    """Reads a .spec.md file and generates tasks in todo.md using the Task List Template."""
    log(f"Generating tasks from {spec_file}...", "SPECKIT")
    
    if not os.path.exists(spec_file):
        log(f"Spec file not found: {spec_file}", "ERROR")
        return

    # Load Task List Template
    task_template = load_template("Task_List_Template.md")
    
    with open(spec_file, "r") as f:
        spec_content = f.read()
        
    # Simple parsing logic (can be enhanced)
    tasks = []
    for line in spec_content.splitlines():
        if line.strip().startswith("* [ ]"):
            task_name = line.replace("* [ ]", "").strip()
            tasks.append(task_name)
            
    # Append to todo.md
    todo_file = "todo.md"
    mode = "a" if os.path.exists(todo_file) else "w"
    
    with open(todo_file, mode) as f:
        if mode == "w":
            f.write(f"# Project Tasks\n\n{task_template}\n\n")
        
        f.write(f"\n## From Spec: {os.path.basename(spec_file)}\n")
        for task in tasks:
            f.write(f"- [ ] {task}\n")
            
    log(f"Added {len(tasks)} tasks to todo.md", "SUCCESS")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 speckit_bridge.py <command> [args]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "init":
        project_name = sys.argv[2] if len(sys.argv) > 2 else "NewProject"
        init_project(project_name)
    elif command == "generate":
        spec_file = sys.argv[2]
        generate_tasks_from_spec(spec_file)
    else:
        # Pass through to real specify CLI
        try:
            subprocess.run([REAL_CLI] + sys.argv[1:])
        except FileNotFoundError:
             log(f"'{REAL_CLI}' command not found. Please install spec-kit.", "ERROR")

if __name__ == "__main__":
    main()
