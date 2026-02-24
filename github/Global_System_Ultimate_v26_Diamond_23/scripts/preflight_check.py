#!/usr/bin/env python3
import os
import sys

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

# Preflight Check Script
# Checks if the environment is ready for a new project.

REQUIRED_TOOLS = ["uv", "pnpm", "git", "docker"]
REQUIRED_FILES = ["AGENTS.md", "knowledge/core/project_lifecycle.md"]

def check_tool(tool):
    return os.system(f"which {tool} > /dev/null 2>&1") == 0

def check_file(path):
    return os.path.exists(path)

def main():
    print(f"🚀 Running Preflight Check ({VERSION})...")
    
    all_ok = True
    
    print("\n🛠️  Checking Tools:")
    for tool in REQUIRED_TOOLS:
        if check_tool(tool):
            print(f"✅ {tool} found")
        else:
            print(f"❌ {tool} MISSING")
            all_ok = False
            
    print("\n📄 Checking Core Files:")
    for f in REQUIRED_FILES:
        if check_file(f):
            print(f"✅ {f} found")
        else:
            print(f"❌ {f} MISSING")
            all_ok = False
            
    if all_ok:
        print("\n✅ System Ready for Takeoff!")
        sys.exit(0)
    else:
        print("\n❌ System Checks Failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
