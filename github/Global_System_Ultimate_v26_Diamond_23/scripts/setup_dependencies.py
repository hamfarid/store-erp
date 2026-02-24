#!/usr/bin/env python3
"""
Module: setup_dependencies.py
Purpose: Install ONLY the necessary dependencies (Python & Node.js) for the Global System to run.
Usage: python3 setup_dependencies.py
"""

import os
import sys
import shutil
import subprocess
import platform

# Configuration
GLOBAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIREMENTS_FILE = os.path.join(GLOBAL_DIR, "config", "requirements.v40.txt")

def print_step(msg):
    print(f"\n🚀 SETUP: {msg}")
    print("="*50)

def check_command(cmd):
    return shutil.which(cmd) is not None

def run_command(cmd, shell=False, check=True):
    try:
        subprocess.run(cmd, shell=shell, check=check)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(e)
        return False

def main():
    print_step("Initializing Dependency Setup")
    
    # 1. System Check
    print_step("Checking System Tools")
    tools = ["git", "docker", "node", "npm", "python3"]
    missing = []
    for tool in tools:
        if check_command(tool):
            print(f"✅ {tool} found.")
        else:
            print(f"❌ {tool} NOT found.")
            missing.append(tool)
    
    if missing:
        print("\n⚠️  WARNING: Some core tools are missing. The system may not function correctly.")
        print(f"Missing: {', '.join(missing)}")
        input("Press Enter to continue anyway, or Ctrl+C to abort...")

    # 2. Python Dependencies
    print_step("Installing Python Libraries")
    if os.path.exists(REQUIREMENTS_FILE):
        print(f"📦 Installing from {REQUIREMENTS_FILE}...")
        # Check for 'uv' for faster install
        if check_command("uv"):
            print("⚡ Using 'uv' for fast installation...")
            run_command(f"uv pip install --system -r {REQUIREMENTS_FILE}", shell=True)
        else:
            print("🐢 Using 'pip' for installation...")
            run_command(f"pip3 install -r {REQUIREMENTS_FILE}", shell=True)
    else:
        print(f"⚠️  Requirements file not found at {REQUIREMENTS_FILE}")
        print("Skipping Python dependency installation.")

    # 3. Node.js Dependencies (for MCP)
    print_step("Installing Node.js Packages (MCP)")
    # We assume package.json is in the root or we install globally/locally as needed.
    # For now, let's install the core MCP servers if package.json exists.
    package_json = os.path.join(GLOBAL_DIR, "package.json")
    if os.path.exists(package_json):
        print("📦 Installing npm packages from package.json...")
        run_command("npm install", shell=True)
    else:
        print("⚠️  package.json not found. Installing core MCP servers manually...")
        mcp_packages = [
            "@modelcontextprotocol/server-filesystem",
            "@modelcontextprotocol/server-github",
            "@modelcontextprotocol/server-memory"
        ]
        run_command(f"npm install {' '.join(mcp_packages)}", shell=True)

    print_step("Setup Complete!")
    print("✅ All dependencies should now be installed.")
    print("👉 You can now run 'python3 tools/preflight_check.py' to verify the system.")

if __name__ == "__main__":
    main()
