#!/usr/bin/env python3
"""
Checkpoint Manager (Global System Ultimate)
Provides a safe mechanism to create, list, and restore project checkpoints using Git branches.
Includes retention policy to prevent branch bloat.
"""

import sys
import os
import subprocess
import datetime
import argparse

RETENTION_LIMIT = 5  # Keep only the last 5 checkpoints
# Tiered Retention Policy (Future Implementation):
# - Keep all checkpoints from the last 24 hours.
# - Keep one checkpoint per hour for the last 7 days.
# - Keep one checkpoint per day for the last 30 days.

def run_command(command):
    try:
        result = subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def ensure_git_repo():
    """Ensures the current directory is a git repository."""
    if not os.path.exists(".git"):
        print("⚠️  Not a git repository. Initializing...")
        run_command("git init")
        run_command("git add .")
        run_command("git commit -m 'Initial commit by Checkpoint Manager'")

def enforce_retention_policy():
    """Deletes old checkpoints if they exceed the limit."""
    success, output = run_command("git branch --list 'checkpoint/*'")
    if not success or not output:
        return

    branches = [b.strip().replace('* ', '') for b in output.split('\n') if b.strip()]
    # Sort by creation time (assuming timestamp in name: checkpoint/YYYYMMDD_HHMMSS_name)
    branches.sort()

    if len(branches) > RETENTION_LIMIT:
        to_delete = branches[:-RETENTION_LIMIT]
        print(f"🧹 Cleaning up {len(to_delete)} old checkpoints...")
        for branch in to_delete:
            run_command(f"git branch -D {branch}")
            print(f"   - Deleted: {branch}")

def create_checkpoint(name):
    """Creates a new git branch as a checkpoint."""
    ensure_git_repo()
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize name
    safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_'))
    branch_name = f"checkpoint/{timestamp}_{safe_name}"
    
    print(f"Creating checkpoint: {branch_name}...")
    
    # 1. Commit any pending changes first (Safety)
    status, _ = run_command("git status --porcelain")
    if status:
        print("   -> Committing pending changes...")
        run_command("git add .")
        run_command(f"git commit -m 'Auto-save before checkpoint {name}'")
    
    # 2. Create Branch
    success, output = run_command(f"git branch {branch_name}")
    
    if success:
        print(f"✅ Checkpoint '{name}' created successfully.")
        print(f"   -> Branch: {branch_name}")
        enforce_retention_policy()
        return True
    else:
        print(f"❌ Failed to create checkpoint: {output}")
        return False

def restore_checkpoint(name):
    """Restores the state to a specific checkpoint."""
    ensure_git_repo()
    
    # Find the branch
    success, output = run_command("git branch --list 'checkpoint/*'")
    if not success:
        print("❌ Failed to list checkpoints.")
        return False
        
    branches = [b.strip().replace('* ', '') for b in output.split('\n') if b.strip()]
    
    target_branch = None
    # Exact match first
    if name in branches:
        target_branch = name
    else:
        # Partial match
        matches = [b for b in branches if name in b]
        if len(matches) == 1:
            target_branch = matches[0]
        elif len(matches) > 1:
            print(f"❌ Ambiguous checkpoint name '{name}'. Matches: {matches}")
            return False
            
    if not target_branch:
        print(f"❌ Checkpoint '{name}' not found.")
        return False
        
    print(f"Restoring checkpoint: {target_branch}...")
    
    # Checkout
    # Force checkout to overwrite local changes if necessary (Safety warning?)
    success, output = run_command(f"git checkout {target_branch}")
    
    if success:
        print(f"✅ Restored to checkpoint '{target_branch}'.")
        return True
    else:
        print(f"❌ Failed to restore: {output}")
        return False

def list_checkpoints():
    """Lists all available checkpoints."""
    ensure_git_repo()
    success, output = run_command("git branch --list 'checkpoint/*'")
    if success and output:
        print("Available Checkpoints:")
        branches = [b.strip().replace('* ', '') for b in output.split('\n') if b.strip()]
        branches.sort()
        for branch in branches:
            print(f"  - {branch.replace('checkpoint/', '')}")
    else:
        print("No checkpoints found.")

def main():
    parser = argparse.ArgumentParser(description="Checkpoint Manager (Global System Ultimate)")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")
    
    create_parser = subparsers.add_parser("create", help="Create a new checkpoint")
    create_parser.add_argument("name", help="Name of the checkpoint")
    
    restore_parser = subparsers.add_parser("restore", help="Restore a checkpoint")
    restore_parser.add_argument("name", help="Name of the checkpoint to restore")
    
    subparsers.add_parser("list", help="List all checkpoints")
    
    args = parser.parse_args()
    
    if args.action == "create":
        create_checkpoint(args.name)
    elif args.action == "restore":
        restore_checkpoint(args.name)
    elif args.action == "list":
        list_checkpoints()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
