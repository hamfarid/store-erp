"""
Module: setup_project.py
Setup Project — part of Global System v26.0.2 Diamond 32.
"""
#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path

# Import the logger
try:
    from logger import GaaraLogger
except ImportError:
    # Fallback if logger is not yet in the path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from logger import GaaraLogger

def setup_project():
    """
    Sets up a new project with the standard Global System folder structure
    and includes essential templates and configurations.
    """
    # Initialize logger
    logger = GaaraLogger()
    
    print("Initializing new project with Global System v26 Diamond 32 structure...")
    logger.log_system("INFO", "Setup Script", "Project initialization started", "Diamond 32")

    # Define standard directories
    directories = [
        "prompts",
        "roles",
        "rules",
        "workflows",
        "templates",
        "scripts",
        "docs",
        "examples",
        "tools",
        "knowledge",
        "errors",
        "data/raw",
        "data/processed",
        "models/trained",
        "models/deployed",
        "logs",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        ".vscode",
        ".cursor",
        ".cline",
        ".idea"
    ]

    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
        logger.log_system("INFO", "Setup Script", f"Created directory: {directory}")

    # Copy essential files from the system root to the new project
    # Assuming the script is run from the system root or the system files are available
    system_root = Path(".")
    
    # Files to copy
    files_to_copy = {
        "BOOTSTRAP.md": "BOOTSTRAP.md",
        "prompts/GLOBAL_PROFESSIONAL_CORE_PROMPT.md": "prompts/GLOBAL_PROFESSIONAL_CORE_PROMPT.md",
        "prompts/communication_scripts.md": "prompts/communication_scripts.md",
        "templates/solution_tradeoff_log.md": "templates/solution_tradeoff_log.md",
        "templates/incident_report.md": "templates/incident_report.md",
        "scripts/configure_ide.py": "scripts/configure_ide.py",
        "scripts/logger.py": "scripts/logger.py", # Copy the logger itself
        "rules/financial_precision.md": "rules/financial_precision.md",
        "rules/data_handling.md": "rules/data_handling.md",
        "rules/security_protocols.md": "rules/security_protocols.md",
        "roles/Financial_Analyst_Agent.md": "roles/Financial_Analyst_Agent.md",
        "roles/System_Architect_Agent.md": "roles/System_Architect_Agent.md",
        "roles/Machine_Learning_Engineer_Agent.md": "roles/Machine_Learning_Engineer_Agent.md",
        "workflows/prediction_lifecycle.md": "workflows/prediction_lifecycle.md",
        "workflows/incident_response.md": "workflows/incident_response.md",
    }

    for src, dest in files_to_copy.items():
        src_path = system_root / src
        dest_path = Path(dest)
        
        if src_path.exists():
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src} to {dest}")
            logger.log_system("INFO", "Setup Script", f"Copied file: {src}")
        else:
            print(f"Warning: Source file {src} not found. Skipping.")
            logger.log_system("WARNING", "Setup Script", f"Source file not found: {src}")

    # Create a README.md for the new project
    readme_content = """# New Project

This project was initialized using the Global System v26 Diamond 32 framework.

## Structure
- **prompts/**: Core system prompts and communication scripts.
- **roles/**: Agent role definitions.
- **rules/**: System rules and guidelines.
- **workflows/**: Operational workflows.
- **templates/**: Project templates (e.g., Solution Trade-off Log).
- **scripts/**: Utility scripts.
- **docs/**: Documentation.
- **examples/**: Example implementations.
- **tools/**: System tools.
- **data/**: Raw and processed data storage.
- **models/**: Trained and deployed ML models.
- **logs/**: System logs.
- **tests/**: Unit, integration, and E2E tests.

## Getting Started
1. Run `python3 scripts/configure_ide.py` to set up your IDE.
2. Review `BOOTSTRAP.md` for initialization instructions.
3. Use `templates/solution_tradeoff_log.md` for documenting architectural decisions.
"""
    with open("README.md", "w") as f:
        f.write(readme_content)
    print("Created README.md")
    logger.log_system("INFO", "Setup Script", "Created README.md")

    print("\nProject setup completed successfully!")
    logger.log_system("INFO", "Setup Script", "Project setup completed successfully")

if __name__ == "__main__":
    setup_project()
