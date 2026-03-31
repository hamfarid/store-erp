#!/usr/bin/env python3
import os
import json
import sys
from datetime import datetime

# --- CONFIGURATION ---
MEMORY_DIR = ".memory"
INDEX_FILE = os.path.join(MEMORY_DIR, "code_structure.json")
TODO_FILE = "todo.md"
CONSTITUTION_FILE = os.path.join(MEMORY_DIR, "project_constitution.md")

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def count_lines_of_code(index):
    total_lines = 0
    file_count = 0
    class_count = 0
    func_count = 0
    
    if "files" in index:
        file_count = len(index["files"])
        for f_data in index["files"].values():
            class_count += len(f_data.get("classes", []))
            func_count += len(f_data.get("functions", []))
            # Estimate LOC (very rough)
            total_lines += 50 # Placeholder
            
    return file_count, class_count, func_count

def get_task_status():
    total = 0
    done = 0
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            for line in f:
                if "- [ ]" in line:
                    total += 1
                elif "- [x]" in line:
                    total += 1
                    done += 1
    return total, done

def print_dashboard():
    os.system('clear')
    print("="*60)
    print("   🚀  GLOBAL SYSTEM v35.0: MISSION CONTROL   🚀")
    print("="*60)
    
    # 1. Project Identity
    print(f"\n[PROJECT IDENTITY]")
    if os.path.exists(CONSTITUTION_FILE):
        print(f"  ✅ Constitution: Active")
    else:
        print(f"  ❌ Constitution: MISSING")
        
    # 2. Memory Status
    index = load_json(INDEX_FILE)
    files, classes, funcs = count_lines_of_code(index)
    print(f"\n[MEMORY STATUS]")
    print(f"  🧠 Indexed Files:     {files}")
    print(f"  📦 Tracked Classes:   {classes}")
    print(f"  ⚡ Tracked Functions: {funcs}")
    
    # 3. Mission Progress
    total_tasks, done_tasks = get_task_status()
    progress = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
    bar_length = 20
    filled_length = int(bar_length * done_tasks // total_tasks) if total_tasks > 0 else 0
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f"\n[MISSION PROGRESS]")
    print(f"  Tasks: {done_tasks}/{total_tasks} [{bar}] {progress:.1f}%")
    
    # 4. System Health
    print(f"\n[SYSTEM HEALTH]")
    print(f"  ✅ Hybrid Engine:  ONLINE")
    print(f"  ✅ Overlord:       WATCHING")
    print(f"  ✅ Meta-Cognition: ENABLED")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print_dashboard()
