"""
Module: upload_to_github.py
Upload To Github — part of Global System v26.0.2 Diamond 32.
"""
#!/usr/bin/env python3
import os
import subprocess
import sys

def run_command(command, error_message):
    """
    Run command implementation.
    """
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error: {error_message}")
        sys.exit(1)

def main():
    """
    Main implementation.
    """
    print("🚀 Global System v26 Diamond 32 GAARA AI - GitHub Upload Helper")
    print("===============================================================")
    try:
        subprocess.check_call(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ Error: Git is not installed. Please install Git first.")
        sys.exit(1)
    repo_url = input("🔗 Please enter your new GitHub repository URL (e.g., https://github.com/username/global.git): ").strip()
    if not repo_url:
        print("❌ Error: Repository URL is required.")
        sys.exit(1)
    confirm = input(f"⚠️  Are you sure you want to initialize a new git repo and push to {repo_url}? (y/n): ").lower()
    if confirm != 'y':
        print("🚫 Operation cancelled.")
        sys.exit(0)
    print("\n📦 Initializing Git repository...")
    if os.path.exists(".git"):
        print("ℹ️  .git directory already exists. Skipping init.")
    else:
        run_command("git init", "Failed to initialize git repository.")
        run_command("git branch -M main", "Failed to rename branch to main.")
    print("➕ Adding files...")
    run_command("git add .", "Failed to add files.")
    print("💾 Committing files...")
    commit_message = "Initial commit: Global System v26 Diamond 32 GAARA AI"
    try:
        subprocess.check_call(f'git commit -m "{commit_message}"', shell=True)
    except subprocess.CalledProcessError:
        print("ℹ️  Nothing to commit (working tree clean).")
    print("🔗 Adding remote origin...")
    try:
        subprocess.check_call(f"git remote add origin {repo_url}", shell=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("ℹ️  Remote origin already exists. Updating URL...")
        run_command(f"git remote set-url origin {repo_url}", "Failed to set remote URL.")
    print("⬆️  Pushing to GitHub...")
    run_command("git push -u origin main", "Failed to push to GitHub. Please check your credentials and repository URL.")
    print("\n✅ Success! Your system has been uploaded to GitHub.")

if __name__ == "__main__":
    main()
