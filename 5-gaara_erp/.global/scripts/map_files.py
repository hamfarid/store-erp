#!/usr/bin/env python3
"""
File: scripts/map_files.py
Generate comprehensive file map for the project
"""

import os
import ast
from datetime import datetime
from typing import Dict


def analyze_python_file(file_path: str) -> Dict:
    """Analyze a Python file and extract metadata"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)

        classes = []
        functions = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # Skip private functions
                    functions.append(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(ast.unparse(node))

        stats = os.stat(file_path)

        return {
            'classes': classes,
            'functions': functions,
            'imports': imports[:5],  # First 5 imports
            'size': stats.st_size,
            'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d'),
        }
    except Exception as e:
        return {'error': str(e)}


def generate_file_map(
        root_dir: str = '.',
        output_file: str = 'docs/File_Map.md'):
    """Generate complete file map"""

    # Create docs directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(
            f"# File Map - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(
            "This file provides a comprehensive map of all files in the project.\n\n")
        f.write("---\n\n")

        # Scan directories
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip common directories
            dirnames[:] = [d for d in dirnames if d not in [
                '.git', '__pycache__', 'node_modules', '.venv', 'venv',
                'dist', 'build', '.next', 'coverage'
            ]]

            if not filenames:
                continue

            rel_dir = os.path.relpath(dirpath, root_dir)
            if rel_dir == '.':
                rel_dir = 'Root'

            f.write(f"## {rel_dir}\n\n")

            for filename in sorted(filenames):
                file_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(file_path, root_dir)

                f.write(f"### `{rel_path}`\n\n")

                # Analyze Python files
                if filename.endswith('.py'):
                    info = analyze_python_file(file_path)

                    if 'error' not in info:
                        if info['classes']:
                            f.write(
                                f"**Classes:** {', '.join(info['classes'])}\n\n")
                        if info['functions']:
                            f.write(
                                f"**Functions:** {', '.join(info['functions'][:10])}\n\n")
                        if info['imports']:
                            f.write(f"**Key Imports:**\n")
                            for imp in info['imports']:
                                f.write(f"- `{imp}`\n")
                            f.write("\n")
                        f.write(
                            f"**Size:** {info['size']:,} bytes | **Modified:** {info['modified']}\n\n")
                    else:
                        f.write(f"*Error analyzing file: {info['error']}*\n\n")

                # Basic info for other files
                else:
                    stats = os.stat(file_path)
                    f.write(
                        f"**Size:** {stats.st_size:,} bytes | **Modified:** {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d')}\n\n")

                f.write("---\n\n")

    print(f"✅ File map generated: {output_file}")


if __name__ == '__main__':
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    output = sys.argv[2] if len(sys.argv) > 2 else 'docs/File_Map.md'

    generate_file_map(root, output)
