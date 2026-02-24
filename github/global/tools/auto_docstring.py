"""
Module: auto_docstring.py
Auto Docstring — part of Global System v26.0.2 Diamond 32.
"""
#!/usr/bin/env python3
import os
import ast
from pathlib import Path

# Configuration
ROOT_DIR = Path(__file__).parent.parent

def add_docstrings_to_file(file_path):
    """
    Add docstrings to file implementation.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        
        tree = ast.parse(source)
        lines = source.splitlines()
        modified = False
        
        # Collect nodes that need docstrings (reverse order to keep line numbers valid)
        nodes_to_doc = []
        
        # Check module docstring
        if not ast.get_docstring(tree):
            nodes_to_doc.append((0, f'"""\nModule: {file_path.name}\nAuto Docstring — part of Global System v26.0.2 Diamond 32.\n"""'))

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    # Calculate indentation
                    line_idx = node.lineno - 1
                    indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
                    indent_str = " " * (indent + 4)
                    
                    docstring = f'{indent_str}"""\n{indent_str}Implementation for {node.name}.\n{indent_str}"""'
                    
                    # Find insertion point (after def line)
                    insert_line = node.lineno
                    nodes_to_doc.append((insert_line, docstring))

        # Apply changes in reverse order
        nodes_to_doc.sort(key=lambda x: x[0], reverse=True)
        
        for line_num, docstring in nodes_to_doc:
            lines.insert(line_num, docstring)
            modified = True
            
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            print(f"✅ Added docstrings to: {file_path}")
            
    except Exception as e:
        print(f"❌ Failed to process {file_path}: {e}")

def main():
    """
    Main implementation.
    """
    print(f"📝 Starting Auto-Docstring on {ROOT_DIR}...")
    
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                add_docstrings_to_file(file_path)
                
    print("✨ Auto-Docstring Complete.")

if __name__ == "__main__":
    main()
