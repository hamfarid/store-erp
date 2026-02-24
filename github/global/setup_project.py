#!/usr/bin/env python3
"""
Module: setup_project.py
Description: Initializes the project structure, installs dependencies, and runs initial audits.
Supports Global System v26.0 Diamond 33 standards.
Includes setup for Local RAG and Memory MCP.
"""
import os
import sys
import subprocess
import shutil

def check_environment():
    """
    Checks if the current environment meets the minimum requirements (Python 3.8+, Git, Docker, Node).
    """
    print("🔍 Checking environment...")
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required.")
        sys.exit(1)
    print("✅ Python version ok.")

    # Check for required tools
    tools = ["git", "docker", "node"]
    for tool in tools:
        if shutil.which(tool):
            print(f"✅ {tool} found.")
        else:
            print(f"⚠️ Warning: {tool} not found.")

def install_dependencies():
    """
    Installs Python dependencies from requirements.txt using pip.
    """
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        # Don't exit, allow setup to continue
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")

def setup_directories():
    """
    Creates the standard directory structure for the project, including Core and Speckit folders.
    """
    print("📂 Setting up directories...")
    
    # Core System Directories
    core_dirs = [
        "logs", 
        "data", 
        "models", 
        "archive", 
        "tools", 
        "rules", 
        "workflows",
        "docs",         # Documentation
        "examples",     # Example projects/code
        "tests",        # Unit/Integration tests
        "infrastructure" # Infrastructure configs
    ]
    
    # Speckit & AI Agent Directories (Crucial for System Operation)
    speckit_dirs = [
        "plans",        # Speckit planning files
        "specs",        # Technical specifications
        "prompts",      # AI prompts and instructions
        "memory-bank",  # Context memory storage
        "meta_rules",   # High-level governing rules
        "roles",        # AI role definitions
        "knowledge",    # Knowledge base
        "templates"     # Project templates
    ]
    
    all_dirs = core_dirs + speckit_dirs
    
    for d in all_dirs:
        os.makedirs(d, exist_ok=True)
        # print(f"✅ Created/Verified {d}/") # Reduce noise

def setup_rag_and_mcp():
    """
    Sets up the Local RAG and Memory MCP system.
    """
    print("🧠 Setting up Local RAG & Memory MCP...")
    
    # Check if RAG script exists
    rag_script = "tools/setup_local_rag.py"
    if os.path.exists(rag_script):
        print("✅ RAG script found.")
        # Create .vector_db directory
        os.makedirs(".vector_db", exist_ok=True)
        print("✅ Created .vector_db directory.")
        
        # Create start_memory.sh script
        with open("start_memory.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("# Start Memory MCP Server\n")
            f.write("echo 'Starting Memory MCP Server...'\n")
            f.write("python3 tools/memory_mcp_server.py\n")
        os.chmod("start_memory.sh", 0o755)
        print("✅ Created start_memory.sh script.")
        
    else:
        print("⚠️ Warning: RAG script not found.")

def main():
    """
    Main entry point for the project setup script.
    """
    print("🚀 Starting Project Setup (Global System v26.0 Diamond 33)...")
    check_environment()
    setup_directories()
    
    if os.path.exists("requirements.txt"):
        install_dependencies()
    else:
        print("⚠️ requirements.txt not found, skipping dependency installation.")
    
    setup_rag_and_mcp()
    
    print("\n✅ Setup Complete! You are ready to go.")
    print("👉 To start the Memory MCP Server, run: ./start_memory.sh")
    
    # Run the correct verification tool
    audit_tool = "tools/zero_error_audit.py"
    if os.path.exists(audit_tool):
        print(f"🔍 Running initial audit with {audit_tool}...")
        subprocess.run([sys.executable, audit_tool])
    else:
        print(f"⚠️ Warning: Audit tool '{audit_tool}' not found.")

if __name__ == "__main__":
    main()
