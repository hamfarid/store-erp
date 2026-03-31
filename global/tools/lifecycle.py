#!/usr/bin/env python3
import os
import sys
import subprocess
import json
from datetime import datetime

# --- CONFIGURATION ---
GLOBAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(GLOBAL_ROOT, "tools")
PROMPTS_DIR = os.path.join(GLOBAL_ROOT, "prompts", "speckit")
MEMORY_DIR = ".memory"

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def run_tool(tool_name, args=[]):
    """Executes a python tool from global/tools/."""
    tool_path = os.path.join(TOOLS_DIR, tool_name)
    cmd = [sys.executable, tool_path] + args
    log(f"Running: {tool_name} {' '.join(args)}", "EXEC")
    subprocess.run(cmd, check=True)

def print_instruction(step_name, prompt_file):
    """Prints the instruction for the AI to follow."""
    prompt_path = os.path.join(PROMPTS_DIR, prompt_file)
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as f:
            content = f.read()
        print(f"\n{'='*40}\nSTEP: {step_name}\n{'='*40}\n")
        print(content)
        print(f"\n{'='*40}\n")
    else:
        log(f"Prompt file not found: {prompt_path}", "ERROR")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 lifecycle.py <project_name> <mission_description>")
        sys.exit(1)

    project_name = sys.argv[1]
    mission = sys.argv[2]
    
    log(f"Starting Lifecycle v34.0 for: {project_name}", "INIT")
    
    # 1. Index & Readme (Reverse Engineering / Initialization)
    log("Phase 1: Reality Check", "PHASE")
    run_tool("code_indexer.py", ["."])
    run_tool("readme_generator.py", [project_name])
    
    # 2. Constitution
    log("Phase 2: Constitution", "PHASE")
    print_instruction("CONSTITUTION", "constitution.md")
    input("Press Enter after AI generates CONSTITUTION.md...")
    
    # 3. Specify
    log("Phase 3: Specification", "PHASE")
    print_instruction("SPECIFY", "specify.md")
    input("Press Enter after AI generates the Spec Draft...")
    
    # 4. Clarify
    log("Phase 4: Clarification", "PHASE")
    print_instruction("CLARIFY", "clarify.md")
    input("Press Enter after AI clarifies requirements...")
    
    # 5. Plan
    log("Phase 5: Technical Planning", "PHASE")
    print_instruction("PLAN", "plan.md")
    input("Press Enter after AI updates Spec with Technical Plan...")
    
    # 6. Tasks
    log("Phase 6: Task Generation", "PHASE")
    print_instruction("TASKS", "tasks.md")
    input("Press Enter after AI generates todo.md...")
    
    # 7. Analyze
    log("Phase 7: Analysis", "PHASE")
    print_instruction("ANALYZE", "analyze.md")
    input("Press Enter after AI verifies consistency...")
    
    # 8. Implement Loop
    log("Phase 8: Implementation Loop", "PHASE")
    print("The AI will now enter the Implementation Loop.")
    print("For each task:")
    print("1. Read /speckit.implement instruction.")
    print("2. Write Code.")
    print("3. Run Tests.")
    print("4. Run 'python3 global/tools/code_indexer.py .'")
    
    print_instruction("IMPLEMENT", "implement.md")

if __name__ == "__main__":
    main()
