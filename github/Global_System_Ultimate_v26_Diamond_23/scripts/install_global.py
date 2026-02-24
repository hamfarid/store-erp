#!/usr/bin/env python3
"""
Module: install_global.py
Purpose: Download and integrate the 'global' system into a new project.
Usage: python3 install_global.py
"""

import os
import sys
import shutil
import subprocess
import json

# Configuration
REPO_URL = "https://github.com/hamfarid/global.git"
TARGET_DIR = "global"
TEMP_DIR = "_global_temp"

def print_step(msg):
    print(f"\n🚀 INSTALLER: {msg}")
    print("="*50)

def run_command(cmd, check=True):
    try:
        subprocess.run(cmd, shell=True, check=check)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(e)
        return False

def main():
    print_step("Starting Global System Installation")

    # 1. Check Git
    if not shutil.which("git"):
        print("❌ Git is not installed. Please install Git first.")
        sys.exit(1)

    # 2. Clone Repository
    print_step(f"Cloning {REPO_URL}...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    
    if not run_command(f"git clone {REPO_URL} {TEMP_DIR}"):
        print("❌ Failed to clone repository.")
        sys.exit(1)

    # 3. Install/Update Global Directory
    print_step(f"Installing to ./{TARGET_DIR}...")
    
    if os.path.exists(TARGET_DIR):
        print(f"⚠️  Directory '{TARGET_DIR}' already exists.")
        choice = input("Overwrite? (y/n): ").lower()
        if choice != 'y':
            print("Installation aborted.")
            shutil.rmtree(TEMP_DIR)
            sys.exit(0)
        shutil.rmtree(TARGET_DIR)

    # Move from temp to target
    shutil.move(TEMP_DIR, TARGET_DIR)
    
    # Remove .git folder from the copy to avoid submodule issues (unless desired)
    # For now, we keep it as a submodule or just a folder. Let's remove .git to treat it as a library.
    shutil.rmtree(os.path.join(TARGET_DIR, ".git"), ignore_errors=True)

    print(f"✅ Installed 'global' system to ./{TARGET_DIR}")

    # 4. Run Genesis
    print_step("Running Genesis Initialization...")
    genesis_script = os.path.join(TARGET_DIR, "genesis.py")
    if os.path.exists(genesis_script):
        run_command(f"python3 {genesis_script}")
    else:
        print("⚠️  genesis.py not found. Skipping initialization.")

    print_step("Installation Complete!")
    print("👉 You can now use the global system tools.")
    print(f"   Try: python3 {TARGET_DIR}/tools/preflight_check.py")

if __name__ == "__main__":
    main()
