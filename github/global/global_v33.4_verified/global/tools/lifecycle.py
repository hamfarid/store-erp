#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
GLOBAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = ".memory"
CONSTITUTION_FILE = os.path.join(MEMORY_DIR, "project_constitution.md")
PLAN_FILE = os.path.join(MEMORY_DIR, "project_plan.md")
REGISTRY_FILE = os.path.join(MEMORY_DIR, "file_registry.json")
SPECKIT_BRIDGE = os.path.join(GLOBAL_ROOT, "tools", "speckit_bridge.py")
HELPERS_DIR = os.path.join(GLOBAL_ROOT, "helpers")

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def ensure_memory_dir():
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
        log(f"Created memory directory: {MEMORY_DIR}")

def get_system_dna():
    """Retrieves the System's DNA (Roles, Rules, Helpers) to inject into Constitution."""
    dna = "\n## 4. System DNA (The Unified Roles)\n"
    dna += "The following roles are MANDATORY for this project. The AI must adopt these personas:\n"
    dna += "*   **The Architect:** Responsible for high-level design, `project_plan.md`, and ensuring alignment with the Mission.\n"
    dna += "*   **The Librarian:** Responsible for maintaining `file_registry.json`, verifying paths, and preventing duplicate files.\n"
    dna += "*   **The Shadow:** Responsible for 'Red Teaming' every plan in `thinking.md` before execution.\n"
    dna += "*   **The Builder:** Responsible for writing code using **Absolute Paths Only** and following Spec-Driven Development.\n"
    dna += "*   **The QA Engineer:** Responsible for writing tests *before* or *immediately after* code, and maintaining `global/errors/`.\n"
    
    dna += "\n## 5. Mandatory Templates & Helpers\n"
    dna += "The following templates from `global/helpers/` MUST be used:\n"
    
    if os.path.exists(HELPERS_DIR):
        for f_name in os.listdir(HELPERS_DIR):
            dna += f"*   `{f_name}`: Use for standardizing output.\n"
    else:
        dna += "*   (No templates found in global/helpers/)\n"
        
    dna += "\n## 6. The Speckit Integration\n"
    dna += "*   All tasks must be generated via `speckit_bridge.py`.\n"
    dna += "*   Specs must reference the Roles defined above.\n"
            
    return dna

def is_existing_project(target_path):
    """Check if the directory contains files other than the system files."""
    if not os.path.exists(target_path):
        return False
    
    # List of system files/dirs to ignore when checking for existence
    system_items = {'.memory', 'global', 'todo.md', 'system_log.md', 'global_v33.1_lifecycle.zip', 'global_v33.2_adoption.zip', 'global_v33.3_unified.zip', 'global_v33.4_verified.zip'}
    
    try:
        items = os.listdir(target_path)
        # If there are items not in the system_items set, it's an existing project
        for item in items:
            if item not in system_items:
                return True
    except FileNotFoundError:
        return False
    
    return False

def adopt_project(project_name, description):
    """Perform Adoption Protocol for existing projects."""
    log(f"⚠️  EXISTING PROJECT DETECTED: {project_name}", "ADOPTION")
    log("Initiating Adoption Protocol v33.3 (Unified DNA)...", "ADOPTION")
    
    ensure_memory_dir()
    
    # 1. Reverse Engineer Constitution with DNA
    if not os.path.exists(CONSTITUTION_FILE):
        log("Reverse engineering Constitution from existing code...", "ADOPTION")
        constitution_content = f"""# Project Constitution: {project_name}
**Status:** Adopted (Brownfield)
**Adoption Date:** {datetime.now().strftime("%Y-%m-%d")}

## 1. Mission
{description}

## 2. Legacy Analysis
This project was adopted by the Global System v33.3.
The goal is to refactor and align it with the Global Standards without breaking existing functionality.

## 3. Core Values (Enforced)
*   **Stability:** Do not break what works.
*   **Gradual Migration:** Refactor module by module.
*   **Anti-Amnesia:** Register all existing files immediately.
"""
        constitution_content += get_system_dna()
        
        with open(CONSTITUTION_FILE, "w") as f:
            f.write(constitution_content)
        log("Constitution created with System DNA.", "SUCCESS")
    
    # 2. Register Existing Files (Librarian Protocol)
    log("Scanning existing files for Librarian Registry...", "ADOPTION")
    registry = {}
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, "r") as f:
                registry = json.load(f)
        except json.JSONDecodeError:
            log("Warning: Existing registry file is corrupt. Rebuilding.", "WARNING")

    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        if ".memory" in dirs:
            dirs.remove(".memory")
        if "global" in dirs:
            dirs.remove("global")
            
        for file in files:
            file_path = os.path.join(root, file)
            abs_path = os.path.abspath(file_path)
            if file not in registry:
                registry[file] = {
                    "path": abs_path,
                    "created_at": datetime.now().isoformat(),
                    "description": "Legacy file registered during adoption."
                }
    
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=4)
    log(f"Registered {len(registry)} existing files.", "SUCCESS")

    # 3. Initialize Speckit (if not present)
    log("Initializing Speckit for Adoption...", "ADOPTION")
    subprocess.run([sys.executable, SPECKIT_BRIDGE, "init", project_name], check=False)
    
    log("✅ ADOPTION COMPLETE. The system is now in control.", "SUCCESS")

def create_new_project(project_name, description):
    """Perform Genesis Protocol for new projects."""
    log(f"✨ NEW PROJECT DETECTED: {project_name}", "GENESIS")
    
    ensure_memory_dir()
    
    # 1. Create Constitution with DNA
    constitution_content = f"""# Project Constitution: {project_name}
**Status:** New (Greenfield)
**Creation Date:** {datetime.now().strftime("%Y-%m-%d")}

## 1. Mission
{description}

## 2. Core Values
*   **Spec-First:** No code without specs.
*   **Zero-Hallucination:** Verify everything.
*   **Atomic Tasks:** Small, testable steps.
"""
    constitution_content += get_system_dna()

    with open(CONSTITUTION_FILE, "w") as f:
        f.write(constitution_content)
    log("Constitution drafted with System DNA.", "SUCCESS")
    
    # 2. Initialize Speckit
    log("Calling Speckit Bridge...", "GENESIS")
    subprocess.run([sys.executable, SPECKIT_BRIDGE, "init", project_name], check=True)
    
    # 3. Initialize Registry
    with open(REGISTRY_FILE, "w") as f:
        json.dump({}, f)
    log("Librarian Registry initialized.", "SUCCESS")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 lifecycle.py <project_name> <description>")
        sys.exit(1)
        
    project_name = sys.argv[1]
    description = sys.argv[2]
    
    current_dir = os.getcwd()
    
    if is_existing_project(current_dir):
        adopt_project(project_name, description)
    else:
        create_new_project(project_name, description)

if __name__ == "__main__":
    main()
