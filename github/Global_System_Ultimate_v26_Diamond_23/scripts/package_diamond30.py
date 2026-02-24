#!/usr/bin/env python3
import os
import shutil
import zipfile
from pathlib import Path
import datetime

# Import logger
try:
    from logger import logger
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from logger import logger

def package_system():
    """
    Packages the Global System v26 Diamond 30 files into a structured directory and zip archive.
    Verifies file integrity and completeness.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"Global_System_v26_Diamond_30_{timestamp}"
    package_dir = Path(f"/home/ubuntu/{package_name}")
    
    print(f"Packaging system into {package_dir}...")
    logger.log_system("INFO", "Packager", f"Packaging started: {package_name}")

    # Define source directories and files
    sources = {
        "roles": Path("/home/ubuntu/roles"),
        "rules": Path("/home/ubuntu/rules"),
        "prompts": Path("/home/ubuntu/prompts"),
        "workflows": Path("/home/ubuntu/workflows"),
        "templates": Path("/home/ubuntu/templates"),
        "scripts": Path("/home/ubuntu/scripts"),
        "logs": Path("/home/ubuntu/logs"), # Include logs directory
    }

    # Create package directory
    package_dir.mkdir(parents=True, exist_ok=True)

    # Copy directories
    for name, src_path in sources.items():
        if src_path.exists():
            dest_path = package_dir / name
            shutil.copytree(src_path, dest_path)
            print(f"Copied {name} to {dest_path}")
            logger.log_system("INFO", "Packager", f"Copied directory: {name}")
        else:
            print(f"Warning: Source {src_path} not found.")
            logger.log_system("WARNING", "Packager", f"Source directory not found: {src_path}")

    # Create a comprehensive README for the package
    readme_content = """# Global System v26 Diamond 30

## Overview
This package contains the complete set of roles, rules, prompts, workflows, and tools for the Global System v26 Diamond 30, integrated with the latest financial and architectural requirements.

## Contents

### 1. Roles (`/roles`)
- **Financial_Analyst_Agent.md**: Expert agent for financial analysis and prediction.
- **System_Architect_Agent.md**: Expert agent for system design and infrastructure.
- **Machine_Learning_Engineer_Agent.md**: Expert agent for ML operations.

### 2. Rules (`/rules`)
- **financial_precision.md**: Strict guidelines for financial data handling and reporting.
- **data_handling.md**: Comprehensive rules for data acquisition, processing, and storage.
- **security_protocols.md**: Security standards and practices.

### 3. Prompts (`/prompts`)
- **GLOBAL_PROFESSIONAL_CORE_PROMPT.md**: The master prompt defining the system's identity and core directives.
- **communication_scripts.md**: Standardized scripts for user interactions.

### 4. Workflows (`/workflows`)
- **prediction_lifecycle.md**: End-to-end workflow for financial predictions.
- **incident_response.md**: Workflow for handling security incidents.

### 5. Templates (`/templates`)
- **solution_tradeoff_log.md**: Template for documenting architectural decisions and trade-offs.
- **incident_report.md**: Template for reporting incidents.

### 6. Scripts (`/scripts`)
- **configure_ide.py**: Script to configure VS Code, Cursor, and Cline with the new system context.
- **setup_project.py**: Script to initialize a new project with the Diamond 30 structure.
- **logger.py**: Programmatic logging module.

### 7. Logs (`/logs`)
- **system_log.md**: System-level event log.
- **ai_log.md**: AI activity log.
- **learning_log.md**: Model learning log.
- **user_log.md**: User interaction log.

## Installation & Usage

1. **Extract the Package**:
   Unzip the archive to your desired location.

2. **Initialize a Project**:
   Run the setup script to create a new project structure:
   ```bash
   python3 scripts/setup_project.py
   ```

3. **Configure IDE**:
   Run the configuration script to set up your development environment:
   ```bash
   python3 scripts/configure_ide.py
   ```

4. **Deploy Agents**:
   Use the role definitions in `/roles` to configure your AI agents.

5. **Follow Workflows**:
   Refer to `/workflows` for operational procedures.

## Version Information
- **Version**: v26.0 Diamond 30
- **Date**: {}
""".format(datetime.datetime.now().strftime("%Y-%m-%d"))

    with open(package_dir / "README.md", "w") as f:
        f.write(readme_content)
    print("Created README.md")
    logger.log_system("INFO", "Packager", "Created README.md")

    # Create Zip Archive
    zip_filename = f"/home/ubuntu/{package_name}.zip"
    print(f"Creating zip archive: {zip_filename}")
    logger.log_system("INFO", "Packager", f"Creating zip archive: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    # Verify Zip File Size
    zip_size = os.path.getsize(zip_filename)
    print(f"Package successfully created at {zip_filename} (Size: {zip_size} bytes)")
    logger.log_system("INFO", "Packager", f"Package created successfully. Size: {zip_size} bytes")
    
    return zip_filename

if __name__ == "__main__":
    package_system()
