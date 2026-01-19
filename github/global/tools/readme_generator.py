#!/usr/bin/env python3
import os
import json

# --- CONFIGURATION ---
MEMORY_DIR = ".memory"
INDEX_FILE = os.path.join(MEMORY_DIR, "code_structure.json")
README_FILE = "README.md"

def log(message):
    print(f"[ReadmeGen] {message}")

def generate_readme(project_name):
    """Generates a comprehensive README.md from the code index."""
    
    if not os.path.exists(INDEX_FILE):
        log(f"Index file not found: {INDEX_FILE}. Run code_indexer.py first.")
        return

    with open(INDEX_FILE, "r") as f:
        index = json.load(f)
        
    content = f"# {project_name}\n\n"
    content += "## Project Structure\n\n"
    content += "This project is automatically documented by the Global System v34.0.\n\n"
    
    # Group by directory
    tree = {}
    for file_path, data in index["files"].items():
        directory = os.path.dirname(file_path)
        if directory not in tree:
            tree[directory] = []
        tree[directory].append((os.path.basename(file_path), data))
        
    # Generate Markdown
    for directory, files in sorted(tree.items()):
        content += f"### 📂 `{directory}/`\n"
        for filename, data in sorted(files, key=lambda x: x[0]):
            content += f"*   **`{filename}`**\n"
            
            # Classes
            if data["classes"]:
                for cls in data["classes"]:
                    doc = cls["docstring"].split('\n')[0] if cls["docstring"] else "No description."
                    content += f"    *   `class {cls['name']}`: {doc}\n"
                    
            # Functions
            if data["functions"]:
                for func in data["functions"]:
                    doc = func["docstring"].split('\n')[0] if func["docstring"] else "No description."
                    content += f"    *   `def {func['name']}`: {doc}\n"
            
            content += "\n"

    with open(README_FILE, "w") as f:
        f.write(content)
        
    log(f"Generated {README_FILE}")

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "Project Documentation"
    generate_readme(name)
