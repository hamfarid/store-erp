#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def check_environment():
    print("🔍 Checking environment...")
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required.")
        sys.exit(1)
    print("✅ Python version ok.")

    # Check for required tools
    tools = ["git", "docker", "node"]
    for tool in tools:
        if not shutil.which(tool):
            print(f"⚠️ Warning: {tool} not found.")
        else:
            print(f"✅ {tool} found.")

def install_dependencies():
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        sys.exit(1)

def setup_directories():
    print("📂 Setting up directories...")
    dirs = ["logs", "data", "models", "archive"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✅ Created {d}/")

def main():
    print("🚀 Starting Project Setup (v24.0.0)...")
    check_environment()
    setup_directories()
    if os.path.exists("requirements.txt"):
        install_dependencies()
    else:
        print("⚠️ requirements.txt not found, skipping dependency installation.")
    
    print("\n✅ Setup Complete! You are ready to go.")
    print("Run 'python3 tools/verify_system_v40.3.py' to verify the installation.")

if __name__ == "__main__":
    main()
