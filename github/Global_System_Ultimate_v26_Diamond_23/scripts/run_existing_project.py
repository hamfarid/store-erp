#!/usr/bin/env python3
"""
Module: run_existing_project.py
Purpose: Analyze, Upgrade, and Run an existing project according to Global System v26 Diamond 15 standards.
Usage: python3 scripts/run_existing_project.py [project_path]
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

# --- Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
GLOBAL_ROOT = SCRIPT_DIR.parent
REQUIRED_FILES = [
    "AGENTS.md",
    "BOOTSTRAP.md",
    "mcp_config.json",
    "prompts/00_MASTER.md"
]

def print_header(msg):
    print(f"\n💎 {msg}")
    print("="*60)

def analyze_project(project_path):
    """Analyze the target project structure and tech stack."""
    print_header(f"Analyzing Project: {project_path}")
    
    stats = {
        "type": "Unknown",
        "missing_files": [],
        "has_git": (project_path / ".git").exists(),
        "has_venv": (project_path / "venv").exists() or (project_path / ".venv").exists(),
        "has_node_modules": (project_path / "node_modules").exists()
    }

    # Detect Type
    if (project_path / "package.json").exists() and (project_path / "requirements.txt").exists():
        stats["type"] = "Hybrid (Python + Node.js)"
    elif (project_path / "package.json").exists():
        stats["type"] = "Node.js"
    elif (project_path / "requirements.txt").exists() or (project_path / "pyproject.toml").exists():
        stats["type"] = "Python"
    
    # Check Compliance
    for f in REQUIRED_FILES:
        if not (project_path / f).exists():
            stats["missing_files"].append(f)
            
    print(f"  🔹 Type: {stats['type']}")
    print(f"  🔹 Git Initialized: {'Yes' if stats['has_git'] else 'No'}")
    print(f"  🔹 Missing Governance Files: {len(stats['missing_files'])}")
    
    return stats

def upgrade_project(project_path, stats):
    """Upgrade the project to Diamond 15 standards."""
    print_header("Upgrading Project to Diamond 15 Standards")
    
    # 1. Copy Missing Governance Files
    if stats["missing_files"]:
        print("  📦 Injecting Governance Files...")
        for f in stats["missing_files"]:
            src = GLOBAL_ROOT / f
            dest = project_path / f
            
            if not src.exists():
                print(f"    ⚠️  Source not found: {f}")
                continue
                
            # Ensure parent dir exists
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            if src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dest)
            print(f"    ✅ Installed: {f}")

    # 2. Update .gitignore
    gitignore_path = project_path / ".gitignore"
    if not gitignore_path.exists():
        print("  📄 Creating .gitignore...")
        gitignore_path.write_text("venv/\n__pycache__/\nnode_modules/\n.env\n.DS_Store\n")
    
    # 3. Create Virtual Environment (if Python)
    if "Python" in stats["type"] and not stats["has_venv"]:
        print("  🐍 Creating Python Virtual Environment...")
        subprocess.run([sys.executable, "-m", "venv", str(project_path / "venv")], check=True)
        print("    ✅ venv created.")

def run_project(project_path, stats):
    """Attempt to run the project based on its type."""
    print_header("Launching Project 🚀")
    
    if stats["type"] == "Node.js":
        print("  👉 Detected Node.js. Running 'npm start'...")
        subprocess.run(["npm", "start"], cwd=project_path)
        
    elif stats["type"] == "Python":
        print("  👉 Detected Python.")
        if (project_path / "main.py").exists():
            print("  ▶️  Running main.py...")
            subprocess.run([sys.executable, "main.py"], cwd=project_path)
        elif (project_path / "app.py").exists():
            print("  ▶️  Running app.py...")
            subprocess.run([sys.executable, "app.py"], cwd=project_path)
        else:
            print("  ⚠️  No entry point (main.py/app.py) found.")
            
    elif stats["type"] == "Hybrid":
        print("  👉 Hybrid Project. Please specify which part to run (Backend/Frontend).")

def main():
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1]).resolve()
    else:
        target_dir = Path.cwd()
        
    if not target_dir.exists():
        print(f"❌ Error: Directory {target_dir} does not exist.")
        sys.exit(1)
        
    stats = analyze_project(target_dir)
    
    print("\nOptions:")
    print("  1. Upgrade Project (Inject Global System Files)")
    print("  2. Run Project")
    print("  3. Both (Upgrade & Run)")
    print("  4. Exit")
    
    choice = input("\nSelect an option (1-4): ").strip()
    
    if choice == "1":
        upgrade_project(target_dir, stats)
    elif choice == "2":
        run_project(target_dir, stats)
    elif choice == "3":
        upgrade_project(target_dir, stats)
        run_project(target_dir, stats)
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
