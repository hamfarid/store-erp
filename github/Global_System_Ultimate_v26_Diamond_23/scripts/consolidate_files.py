import os
import json
from pathlib import Path

def consolidate_files():
    """
    Identifies and lists all relevant project files from the root directory and subdirectories,
    excluding system files and temporary directories.
    """
    root_dir = Path(".")
    
    # Define directories to include
    include_dirs = [
        "roles",
        "rules",
        "prompts",
        "workflows",
        "examples",
        "docs",
        "templates",
        "tools",
        "scripts",
        "logs"
    ]
    
    # Define files to include from root
    include_files = [
        "README.md",
        "BOOTSTRAP.md",
        "todo.md"
    ]
    
    print("Scanning for project files...")
    
    found_files = []
    
    # Scan directories
    for dir_name in include_dirs:
        dir_path = root_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            for file_path in dir_path.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith("."):
                    found_files.append(str(file_path))
    
    # Scan root files
    for file_name in include_files:
        file_path = root_dir / file_name
        if file_path.exists() and file_path.is_file():
            found_files.append(str(file_path))
            
    print(f"Found {len(found_files)} relevant project files.")
    
    # Save the list of files
    with open("project_file_list.json", "w") as f:
        json.dump(found_files, f, indent=4)
            
    print("File list saved to project_file_list.json")

if __name__ == "__main__":
    consolidate_files()
