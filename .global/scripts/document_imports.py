#!/usr/bin/env python3
"""
File: scripts/document_imports.py
Generate import/export documentation
"""

import ast
import sys
from pathlib import Path
from datetime import datetime


def analyze_file(filepath: Path) -> dict:
    """Analyze Python file for imports and exports"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
    except Exception as e:
        print(f"Warning: Could not parse {filepath}: {e}")
        return {}

    imports = []
    exports = []
    functions = []
    classes = []

    for node in ast.walk(tree):
        # Imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                if alias.name == '*':
                    imports.append(f"{module}.*")
                else:
                    imports.append(f"{module}.{alias.name}")

        # Exports (__all__)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == '__all__':
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant):
                                exports.append(elt.value)

        # Functions
        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):
                functions.append(node.name)

        # Classes
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith('_'):
                classes.append(node.name)

    return {
        'imports': sorted(set(imports)),
        'exports': sorted(set(exports)),
        'functions': sorted(set(functions)),
        'classes': sorted(set(classes))
    }


def generate_documentation(root_dir: str, output_file: str):
    """Generate import/export documentation"""

    modules = {}

    print(f"Analyzing Python files in {root_dir}...")

    for filepath in Path(root_dir).rglob('*.py'):
        # Skip virtual environments and migrations
        if any(
            part in filepath.parts for part in [
                'venv',
                '.venv',
                'migrations',
                'node_modules',
                '__pycache__']):
            continue

        rel_path = filepath.relative_to(root_dir)
        analysis = analyze_file(filepath)

        if analysis:
            modules[str(rel_path)] = analysis

    print(f"Found {len(modules)} modules")

    # Write documentation
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Import/Export Documentation\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        f.write(f"**Total Modules:** {len(modules)}\n\n")
        f.write("---\n\n")

        for module, data in sorted(modules.items()):
            f.write(f"## `{module}`\n\n")

            # Exports
            if data.get('exports'):
                f.write("### 📤 Exports (`__all__`)\n\n")
                for exp in data['exports']:
                    f.write(f"- `{exp}`\n")
                f.write("\n")

            # Classes
            if data.get('classes'):
                f.write("### 🏛️ Classes\n\n")
                for cls in data['classes']:
                    f.write(f"- `{cls}`\n")
                f.write("\n")

            # Functions
            if data.get('functions'):
                f.write("### ⚙️ Functions\n\n")
                for func in data['functions']:
                    f.write(f"- `{func}()`\n")
                f.write("\n")

            # Imports
            if data.get('imports'):
                f.write("### 📥 Imports\n\n")
                for imp in data['imports']:
                    f.write(f"- `{imp}`\n")
                f.write("\n")

            f.write("---\n\n")

    print(f"✅ Documentation generated: {output_file}")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    output = sys.argv[2] if len(sys.argv) > 2 else "docs/Imports_Exports.md"

    generate_documentation(root, output)
