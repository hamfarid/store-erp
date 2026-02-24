#!/usr/bin/env python3
"""
Genesis Tool: The starting point for all new projects.
This script initializes the project structure and sets up the environment.
"""
import os
import sys
import subprocess

def main():
    print("Genesis: Initializing Global System Project...")
    
    # Check for required files
    required_files = ["AGENTS.md", "CLAUDE.md", "BOOTSTRAP.md"]
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        print(f"Error: Missing critical files: {missing}")
        sys.exit(1)
        
    print("Genesis: Core files verified.")
    
    # Run setup script if available
    if os.path.exists("setup_project.py"):
        print("Genesis: Running setup_project.py...")
        subprocess.run([sys.executable, "setup_project.py"])
    else:
        print("Genesis: setup_project.py not found. Skipping setup.")
        
    print("Genesis: Initialization complete.")

if __name__ == "__main__":
    main()
