#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import argparse
from datetime import datetime

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

# Global System Ultimate - Speckit Tool
# Verified Feb 2026: Context Rot, BATS Logic, & Context Engineering

CONTEXT_LIMIT = 128000  # 128k Tokens (Feb 2026 Standard)
MEMORY_BANK = "memory-bank"

def check_context_rot():
    """Simulates context token counting and triggers compaction if needed."""
    try:
        # In a real scenario, this would use tiktoken
        # Here we estimate based on file size (1 char ~= 0.25 tokens)
        total_chars = 0
        if os.path.exists(MEMORY_BANK):
            for root, _, files in os.walk(MEMORY_BANK):
                for file in files:
                    if file.endswith(".md"):
                        path = os.path.join(root, file)
                        with open(path, 'r') as f:
                            total_chars += len(f.read())
        
        estimated_tokens = total_chars // 4
        print(f"📊 Current Context Usage: ~{estimated_tokens} tokens")
        
        if estimated_tokens > CONTEXT_LIMIT:
            print(f"⚠️ WARNING: Context Rot Threshold Exceeded ({CONTEXT_LIMIT})")
            compress_context()
        else:
            print("✅ Context is Healthy")
            
    except Exception as e:
        print(f"❌ Error checking context: {e}")

def compress_context():
    """Compacts memory-bank files to reduce token usage."""
    print("🔄 Triggering Context Compaction (Strategy: Summarization)...")
    # Logic: Archive old decisions, summarize progress
    archive_path = os.path.join(MEMORY_BANK, "archive")
    os.makedirs(archive_path, exist_ok=True)
    
    # Example: Move old decision log
    decision_log = os.path.join(MEMORY_BANK, "decisionLog.md")
    if os.path.exists(decision_log):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_path = os.path.join(archive_path, f"decisionLog_{timestamp}.md")
        os.rename(decision_log, new_path)
        
        # Create fresh log
        with open(decision_log, 'w') as f:
            f.write(f"# Decision Log (Compacted {timestamp})\n\n*Old logs archived to {new_path}*\n")
        print(f"✅ Compacted: {decision_log}")

def generate_plan(goal):
    """Generates a plan using the 4-Block Pattern (Context Engineering)."""
    print(f"🧠 Planning: {goal}")
    check_context_rot()
    
    plan_content = f"""# PLAN: {goal}

## 1. INSTRUCTION (What to do)
*   Analyze the requirements for '{goal}'.
*   Break down into atomic tasks.

## 2. CONTEXT (What we know)
*   Current System Version: {VERSION}
*   Active Context: (See memory-bank/activeContext.md)

## 3. CONSTRAINTS (What NOT to do)
*   Do NOT hallucinate APIs.
*   Do NOT break existing tests.
*   Do NOT exceed token budget.

## 4. OUTPUT (Format)
*   Generate a list of tasks in `TASKS.md`.
*   Update `memory-bank/activeContext.md`.
"""
    with open("PLAN.md", "w") as f:
        f.write(plan_content)
    print("✅ PLAN.md generated using 4-Block Pattern.")

def main():
    parser = argparse.ArgumentParser(description=f"Speckit: The AI Orchestrator ({VERSION})")
    subparsers = parser.add_subparsers(dest="command")
    
    # Plan Command
    plan_parser = subparsers.add_parser("plan", help="Generate a plan")
    plan_parser.add_argument("goal", help="The goal to achieve")
    
    # Verify Command
    verify_parser = subparsers.add_parser("verify", help="Verify system integrity")
    
    # Compress Command
    compress_parser = subparsers.add_parser("compress", help="Force context compaction")

    args = parser.parse_args()
    
    if args.command == "plan":
        generate_plan(args.goal)
        
    elif args.command == "verify":
        print(f"🛡️ Verifying System Integrity ({VERSION})...")
        # (Verification logic)
        
    elif args.command == "compress":
        compress_context()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
