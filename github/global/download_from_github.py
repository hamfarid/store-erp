"""
Module: download_from_github.py
Download From Github — part of Global System v26.0.2 Diamond 32.
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
    print("🚀 Global System v26 Diamond 32 GAARA AI - GitHub Download Helper")
    print("=================================================================")
    try:
        subprocess.check_call(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ Error: Git is not installed. Please install Git first.")
        sys.exit(1)
    repo_url = input("🔗 Please enter the GitHub repository URL (e.g., https://github.com/username/global.git): ").strip()
    if not repo_url:
        print("❌ Error: Repository URL is required.")
        sys.exit(1)
    dest_dir = input("📂 Enter destination directory (leave empty for current directory): ").strip()
    if not dest_dir:
        dest_dir = "."
    confirm = input(f"⚠️  Are you sure you want to clone {repo_url} into {dest_dir}? (y/n): ").lower()
    if confirm != 'y':
        print("🚫 Operation cancelled.")
        sys.exit(0)
    print("\n📦 Cloning repository...")
    try:
        subprocess.check_call(f"git clone {repo_url} {dest_dir}", shell=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to clone repository. Please check the URL and your permissions.")
        sys.exit(1)
    print("\n✅ Repository cloned successfully.")
    run_setup = input("⚙️  Do you want to run the setup script now? (y/n): ").lower()
    if run_setup == 'y':
        setup_script = os.path.join(dest_dir, "setup_project.py")
        if os.path.exists(setup_script):
            print("\n🚀 Running setup script...")
            original_cwd = os.getcwd()
            os.chdir(dest_dir)
            try:
                subprocess.check_call([sys.executable, "setup_project.py"])
            except subprocess.CalledProcessError:
                print("❌ Setup script failed.")
            finally:
                os.chdir(original_cwd)
        else:
            print("⚠️  setup_project.py not found in the cloned repository.")
    print("\n✨ Done! You can now start using the Global System.")

if __name__ == "__main__":
    main()
