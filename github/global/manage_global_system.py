#!/usr/bin/env python3
"""
Module: manage_global_system.py
Description: Interactive CLI tool for managing the Global System v26.0 Diamond 33.
Allows users to download/inject the system into projects or upload changes to GitHub.
Includes support for Local RAG, Memory MCP, and Hallucination Verification.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configuration
# Default repo URL - can be overridden by user input
DEFAULT_REPO_URL = "https://github.com/hamfarid/global.git"
TEMP_DIR = "temp_global_system"
TARGET_DIRS = [
    "tools",
    "rules",
    "workflows",
    "memory-bank",
    "meta_rules",
    "plans",
    "specs",
    "prompts",
    "roles",
    "templates",
    "scripts",
    "docs",
    "examples",
    "knowledge",
    "data",
    "models",
    "logs",
    "tests",
    "infrastructure" # Added infrastructure
]
TARGET_FILES = [
    "setup_project.py",
    "requirements.txt",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "docker-compose.yml",
    "setup_rag.sh", # Added RAG setup script
    "start_mcp.sh", # Added MCP start script
    "verify_hallucinations.sh" # Added Hallucination Verification script
]

class Colors:
    """
    ANSI color codes for terminal output.
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(msg):
    """
    Prints a step message in blue.
    """
    print(f"{Colors.BLUE}▸ {msg}{Colors.ENDC}")

def print_success(msg):
    """
    Prints a success message in green.
    """
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def print_warning(msg):
    """
    Prints a warning message in yellow.
    """
    print(f"{Colors.WARNING}⚠️  {msg}{Colors.ENDC}")

def print_error(msg):
    """
    Prints an error message in red.
    """
    print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")

def get_user_input(prompt, default=None):
    """
    Gets user input with an optional default value.
    """
    if default:
        user_input = input(f"{Colors.BOLD}{prompt} [{default}]: {Colors.ENDC}")
        return user_input.strip() or default
    else:
        return input(f"{Colors.BOLD}{prompt}: {Colors.ENDC}").strip()

def run_command(command, cwd=None, check=True):
    """
    Runs a shell command and returns the output.
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {command}")
        print_error(e.stderr)
        if check:
            sys.exit(1)
        return None

def inject_system(repo_url):
    """
    Clones the Global System repository and injects files into the current project.
    """
    print_step(f"Cloning Global System from {repo_url}...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    
    # Try to clone
    try:
        run_command(f"git clone {repo_url} {TEMP_DIR}")
        print_success("Repository cloned successfully.")
    except Exception:
        print_warning("Git clone failed. Checking for local simulation source...")
        if os.path.exists("github_upload_temp"):
            shutil.copytree("github_upload_temp", TEMP_DIR)
            print_success("Repository cloned from local simulation source.")
        else:
            print_error("Failed to clone repository and no local source found.")
            return

    print_step("Injecting system files into current project...")
    
    for item in TARGET_DIRS:
        src = os.path.join(TEMP_DIR, item)
        dst = item
        if os.path.exists(src):
            if os.path.exists(dst):
                print_warning(f"Directory '{dst}' already exists. Merging...")
                run_command(f"cp -r {src}/* {dst}/", check=False)
            else:
                shutil.copytree(src, dst)
                print_success(f"Installed directory: {dst}")
        else:
            # Optional directories might not exist
            pass

    for item in TARGET_FILES:
        src = os.path.join(TEMP_DIR, item)
        dst = item
        if os.path.exists(src):
            if os.path.exists(dst):
                print_warning(f"File '{dst}' already exists. Backing up to '{dst}.bak'...")
                shutil.move(dst, f"{dst}.bak")
            shutil.copy2(src, dst)
            print_success(f"Installed file: {dst}")

    print_step("Cleaning up temporary files...")
    shutil.rmtree(TEMP_DIR)
    
    # Make scripts executable
    print_step("Setting permissions...")
    run_command("chmod +x setup_project.py setup_rag.sh start_mcp.sh verify_hallucinations.sh", check=False)

    # Run Setup
    print_step("Running System Setup...")
    if os.path.exists("setup_project.py"):
        subprocess.run([sys.executable, "setup_project.py"])
    
    # Run Audit
    print_step("Running Initial System Audit...")
    if os.path.exists("tools/zero_error_audit.py"):
        subprocess.run([sys.executable, "tools/zero_error_audit.py"])

    print_success("Injection Complete!")

def upload_system(repo_url):
    """
    Initializes a git repository (if needed) and pushes the current project to GitHub.
    """
    print_step("Preparing to upload project to GitHub...")
    
    if not os.path.exists(".git"):
        print_step("Initializing Git repository...")
        run_command("git init")
        run_command("git branch -M main")
    
    # Check remote
    remotes = run_command("git remote -v", check=False)
    if "origin" not in remotes:
        run_command(f"git remote add origin {repo_url}")
        print_success(f"Added remote origin: {repo_url}")
    else:
        print_warning("Remote 'origin' already exists. Skipping addition.")

    print_step("Adding files...")
    run_command("git add .")
    
    commit_msg = get_user_input("Enter commit message", "Update Global System")
    run_command(f"git commit -m '{commit_msg}'", check=False)
    
    print_step(f"Pushing to {repo_url}...")
    try:
        run_command("git push -u origin main")
        print_success("Upload Complete!")
    except Exception:
        print_error("Push failed. Please check your Git credentials and permissions.")

def main():
    """
    Main entry point for the interactive management tool.
    """
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║   Global System Management Tool v26.0 Diamond 33     ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

    print("Please choose an operation:")
    print(f"1. {Colors.GREEN}📥 Download/Inject{Colors.ENDC} (Pull system tools from GitHub to this project)")
    print(f"2. {Colors.BLUE}📤 Upload{Colors.ENDC} (Push this project/system to GitHub)")
    print(f"3. {Colors.WARNING}❌ Skip{Colors.ENDC} (Do nothing, just exit)")
    
    choice = get_user_input("Enter choice (1/2/3)", "1")

    if choice == "1":
        repo_url = get_user_input("Enter GitHub Repository URL", DEFAULT_REPO_URL)
        inject_system(repo_url)
    elif choice == "2":
        repo_url = get_user_input("Enter GitHub Repository URL", DEFAULT_REPO_URL)
        upload_system(repo_url)
    elif choice == "3":
        print("Exiting...")
        sys.exit(0)
    else:
        print_error("Invalid choice!")
        sys.exit(1)

if __name__ == "__main__":
    main()
