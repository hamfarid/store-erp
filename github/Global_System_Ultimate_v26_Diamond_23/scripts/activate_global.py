#!/usr/bin/env python3
"""
Module: activate_global.py
Purpose: Activate the Global System Ultimate in a new project by deploying rules, configuring MCP, and bootstrapping.
Usage: python3 activate_global.py
"""

import os
import sys
import shutil
import subprocess
import json

# Configuration
# Path Structure: ProjectRoot/GitHub/global_system/scripts/activate_global.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GLOBAL_DIR = os.path.dirname(SCRIPT_DIR) # global_system/
GITHUB_DIR = os.path.dirname(GLOBAL_DIR) # GitHub/
PROJECT_ROOT = os.path.dirname(GITHUB_DIR) # ProjectRoot/

def print_step(msg):
    print(f"\n🚀 ACTIVATION: {msg}")
    print("="*50)

def run_command(cmd, shell=False, check=True):
    try:
        subprocess.run(cmd, shell=shell, check=check)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(e)
        return False

def deploy_rules():
    print_step("Deploying AI Rules & Prompts")
    
    # Map source files in global_system/ to destination in ProjectRoot
    # We use symlinks where possible to keep 'global_system' as the single source of truth
    
    rules_map = {
        "AGENTS.md": "AGENTS.md",
        ".cursorrules": ".cursorrules",
        ".clinerules": ".clinerules",
        ".windsurfrules": ".windsurfrules",
        "AI_HANDBOOK.md": "AI_HANDBOOK.md",
        "AI_CONTEXT_ROUTER.md": "AI_CONTEXT_ROUTER.md",
        "BOOTSTRAP.md": "BOOTSTRAP.md",
        "CLAUDE.md": "CLAUDE.md"
    }

    for src_name, dest_name in rules_map.items():
        src_path = os.path.join(GLOBAL_DIR, src_name)
        dest_path = os.path.join(PROJECT_ROOT, dest_name)
        
        if not os.path.exists(src_path):
            print(f"⚠️  Source not found: {src_name} (Skipping)")
            continue

        if os.path.exists(dest_path):
            print(f"ℹ️  Destination exists: {dest_name}")
            if os.path.islink(dest_path):
                print(f"   -> Already linked.")
                continue
            else:
                backup_name = f"{dest_name}.bak"
                print(f"   -> Backing up existing file to {backup_name}")
                shutil.move(dest_path, os.path.join(PROJECT_ROOT, backup_name))

        # Create Symlink (or copy if windows/failed)
        try:
            # Use relative path for symlink to be portable
            rel_src = os.path.relpath(src_path, PROJECT_ROOT)
            os.symlink(rel_src, dest_path)
            print(f"✅ Linked: {dest_name} -> {rel_src}")
        except OSError:
            print(f"⚠️  Symlink failed. Copying instead: {dest_name}")
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)

def configure_mcp():
    print_step("Configuring MCP (Model Context Protocol)")
    
    # 1. Install Node Dependencies
    print("📦 Installing MCP Servers...")
    package_json = os.path.join(GLOBAL_DIR, "package.json")
    if os.path.exists(package_json):
        # Install in global_system/ directory
        subprocess.run(["npm", "install"], cwd=GLOBAL_DIR, check=False)
    else:
        print("⚠️  global_system/package.json not found. Skipping npm install.")

    # 2. Deploy Config
    # We generate mcp_config.json in ProjectRoot
    
    src_config = os.path.join(GLOBAL_DIR, "mcp_config.json")
    dest_config = os.path.join(PROJECT_ROOT, "mcp_config.json")
    
    if os.path.exists(src_config):
        if not os.path.exists(dest_config):
            shutil.copy2(src_config, dest_config)
            print(f"✅ Copied MCP Config to Project Root: {dest_config}")
            print("👉 NOTE: You may need to manually add this to your IDE settings (Cursor/VS Code).")
        else:
            print(f"ℹ️  MCP Config already exists at {dest_config}")
    else:
        print("⚠️  Source mcp_config.json not found. Run genesis.py first?")

def bootstrap_system():
    print_step("Bootstrapping System (Genesis Global System Ultimate)")
    
    genesis_script = os.path.join(GLOBAL_DIR, "tools", "genesis.py")
    if os.path.exists(genesis_script):
        print("🚀 Running Genesis...")
        # Run genesis from the ProjectRoot context
        subprocess.run([sys.executable, genesis_script], cwd=PROJECT_ROOT)
    else:
        print(f"❌ genesis.py not found at {genesis_script}!")

def main():
    print_step("ACTIVATING Global System Ultimate")
    print(f"Global Dir: {GLOBAL_DIR}")
    print(f"Project Root: {PROJECT_ROOT}")
    
    deploy_rules()
    configure_mcp()
    bootstrap_system()
    
    print_step("ACTIVATION COMPLETE")
    print("✅ The Global System Ultimate is now active in this project.")
    print("👉 Next: Run 'python3 GitHub/global_system/tools/preflight_check.py' to verify.")

if __name__ == "__main__":
    main()
