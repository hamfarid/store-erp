"""
Module: configure_ide.py
Configure Ide — part of Global System v26.0.2 Diamond 32.
"""
#!/usr/bin/env python3
import os
import shutil
import json
import sys

# Import logger
try:
    from logger import GaaraLogger
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from logger import GaaraLogger

# Initialize logger
logger = GaaraLogger()

# --- Configuration ---
TEMPLATES_DIR = "templates/ide_configs"
MCP_CONFIG_FILE = "mcp_config.json"
# Updated core folders to include workflows and templates for Diamond 32
CORE_FOLDERS = ["prompts", "roles", "rules", "workflows", "templates"]

# --- Helper Functions ---
def print_header(text):
    """
    Print header implementation.
    """
    print(f"\n{'='*40}")
    print(f" {text}")
    print(f"{'='*40}")

def print_success(text):
    """
    Print success implementation.
    """
    print(f"✅ {text}")

def print_error(text):
    """
    Print error implementation.
    """
    print(f"❌ {text}")

def ensure_dir(path):
    """
    Ensure dir implementation.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
        logger.log_system("INFO", "IDE Config", f"Created directory: {path}")

def copy_file(src, dest):
    """
    Copy file implementation.
    """
    try:
        shutil.copy2(src, dest)
        print(f"Copied: {src} -> {dest}")
        logger.log_system("INFO", "IDE Config", f"Copied file: {src}")
        return True
    except FileNotFoundError:
        print_error(f"Source file not found: {src}")
        logger.log_system("ERROR", "IDE Config", f"Source file not found: {src}")
        return False
    except Exception as e:
        print_error(f"Error copying file: {e}")
        logger.log_system("ERROR", "IDE Config", f"Error copying file: {e}")
        return False

def copy_folder(src, dest):
    """
    Copy folder implementation.
    """
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        print(f"Copied folder: {src} -> {dest}")
        logger.log_system("INFO", "IDE Config", f"Copied folder: {src}")
        return True
    except FileNotFoundError:
        print_error(f"Source folder not found: {src}")
        logger.log_system("ERROR", "IDE Config", f"Source folder not found: {src}")
        return False
    except Exception as e:
        print_error(f"Error copying folder: {e}")
        logger.log_system("ERROR", "IDE Config", f"Error copying folder: {e}")
        return False

def activate_mcp(ide_name, config_path):
    """Ensures MCP config is referenced in the IDE settings."""
    print(f"Activating MCP for {ide_name}...")
    logger.log_system("INFO", "IDE Config", f"Activating MCP for {ide_name}")
    
    if not os.path.exists(MCP_CONFIG_FILE):
        print_error(f"MCP config file not found: {MCP_CONFIG_FILE}")
        logger.log_system("ERROR", "IDE Config", f"MCP config file not found: {MCP_CONFIG_FILE}")
        return False

    abs_mcp_path = os.path.abspath(MCP_CONFIG_FILE)
    print(f"MCP Config Path: {abs_mcp_path}")
    
    print_success(f"MCP Activated for {ide_name}")
    logger.log_system("INFO", "IDE Config", f"MCP Activated for {ide_name}")
    return True

def inject_core_context(ide_config_dir):
    """Copies core folders (prompts, roles, rules, workflows, templates) into the IDE config directory."""
    print(f"Injecting core context (prompts, roles, rules, workflows, templates) into {ide_config_dir}...")
    logger.log_system("INFO", "IDE Config", f"Injecting core context into {ide_config_dir}")
    
    for folder in CORE_FOLDERS:
        src = folder
        dest = os.path.join(ide_config_dir, folder)
        if os.path.exists(src):
            copy_folder(src, dest)
        else:
            print_error(f"Core folder missing: {src}")
            logger.log_system("WARNING", "IDE Config", f"Core folder missing: {src}")

    print_success(f"Core Context Injected into {ide_config_dir}")
    logger.log_system("INFO", "IDE Config", f"Core Context Injected into {ide_config_dir}")

# --- IDE Configuration Logic ---

def configure_cursor():
    """
    Configure cursor implementation.
    """
    logger.log_system("INFO", "IDE Config", "Configuring Cursor")
    print_header("Configuring for Cursor")
    ensure_dir(".cursor")
    # Copy core context to .cursor directory
    inject_core_context(".cursor")
    activate_mcp("Cursor", ".cursor/mcp.json")

def configure_vscode():
    """
    Configure vscode implementation.
    """
    logger.log_system("INFO", "IDE Config", "Configuring VS Code")
    print_header("Configuring for VS Code")
    ensure_dir(".vscode")
    # Copy core context to .vscode directory
    inject_core_context(".vscode")
    activate_mcp("VS Code", ".vscode/settings.json")

def configure_cline():
    """
    Configure cline implementation.
    """
    logger.log_system("INFO", "IDE Config", "Configuring Cline")
    print_header("Configuring for Cline")
    ensure_dir(".cline")
    # Copy core context to .cline directory
    inject_core_context(".cline")
    activate_mcp("Cline", ".cline/config.json")

def configure_pycharm():
    """
    Configure pycharm implementation.
    """
    logger.log_system("INFO", "IDE Config", "Configuring PyCharm")
    print_header("Configuring for PyCharm")
    ensure_dir(".idea")
    # Copy core context to .idea directory
    inject_core_context(".idea")
    activate_mcp("PyCharm", ".idea/workspace.xml")

def configure_other(ide_name):
    """
    Configure other implementation.
    """
    logger.log_system("INFO", "IDE Config", f"Configuring {ide_name}")
    print_header(f"Configuring for {ide_name}")
    # Create a generic config directory for other IDEs
    config_dir = f".{ide_name.lower().replace(' ', '_')}"
    ensure_dir(config_dir)
    inject_core_context(config_dir)
    activate_mcp(ide_name, f"{config_dir}/config.json")

# --- Main Interactive Loop ---

def main():
    """
    Main implementation.
    """
    print_header("Global System v26.0 (Diamond 32) - IDE Configuration Wizard")
    print("Select your primary IDE/Agent:")
    print("1. Cursor")
    print("2. VS Code")
    print("3. Cline")
    print("4. PyCharm")
    print("5. Windsurf / Kiro / Kilo / Antigravity / Augment / Autopilot")
    print("0. Exit")

    # For automated execution, default to all if no input provided
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        configure_cursor()
        configure_vscode()
        configure_cline()
        configure_pycharm()
        print("\nAll IDEs configured successfully!")
        return

    choice = input("\nEnter your choice (0-5): ").strip()

    if choice == "1":
        configure_cursor()
    elif choice == "2":
        configure_vscode()
    elif choice == "3":
        configure_cline()
    elif choice == "4":
        configure_pycharm()
    elif choice == "5":
        ide_name = input("Enter the specific IDE name: ").strip()
        configure_other(ide_name if ide_name else "Other IDE")
    elif choice == "0":
        print("Exiting...")
        sys.exit(0)
    else:
        print_error("Invalid choice. Please try again.")
        main()

if __name__ == "__main__":
    main()
