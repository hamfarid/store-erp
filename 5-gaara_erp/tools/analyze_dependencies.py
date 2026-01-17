#!/usr/bin/env python3
"""
File: /scripts/analyze_dependencies.py
Purpose: Comprehensive dependency analysis and table generation

Features:
- Scan all Python files in project
- Extract all imports (absolute, relative, from X import Y)
- Build dependency graph
- Calculate dependency levels
- Generate markdown table
- Detect circular dependencies
- Identify orphan files

Usage:
    python analyze_dependencies.py <project_root> [--output docs/]
"""

import os
import ast
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque


class DependencyAnalyzer:
    """Analyze Python project dependencies comprehensively."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.files: Dict[str, Path] = {}  # module_name -> file_path
        self.imports: Dict[str, Set[str]] = defaultdict(set)  # file -> imports
        self.imported_by: Dict[str, Set[str]] = defaultdict(
            set)  # file -> imported_by
        self.dependency_levels: Dict[str, int] = {}
        self.circular_deps: List[List[str]] = []
        self.orphan_files: Set[str] = set()

    def scan_project(self):
        """Scan project for all Python files."""
        print(f"Scanning project: {self.project_root}")

        for py_file in self.project_root.rglob("*.py"):
            if self._should_skip(py_file):
                continue

            rel_path = py_file.relative_to(self.project_root)
            module_name = str(rel_path).replace(os.sep, ".").replace(".py", "")
            self.files[module_name] = py_file

        print(f"Found {len(self.files)} Python files")

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_dirs = {'.git', '__pycache__', 'venv', '.venv', 'env',
                     'node_modules', 'build', 'dist', '.tox'}

        return any(part in skip_dirs for part in file_path.parts)

    def analyze_imports(self):
        """Analyze imports in all files."""
        print("Analyzing imports...")

        for module_name, file_path in self.files.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=str(file_path))

                imports = self._extract_imports(tree, module_name)
                self.imports[module_name] = imports

                # Build reverse mapping
                for imported in imports:
                    self.imported_by[imported].add(module_name)

            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")

        print(f"Analyzed imports in {len(self.imports)} files")

    def _extract_imports(self, tree: ast.AST, current_module: str) -> Set[str]:
        """Extract all imports from AST."""
        imports = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Handle relative imports
                    if node.level > 0:
                        base = ".".join(
                            current_module.split(".")[
                                :-node.level])
                        if node.module:
                            module = f"{base}.{node.module}"
                        else:
                            module = base
                    else:
                        module = node.module

                    imports.add(module)

        return imports

    def calculate_dependency_levels(self):
        """Calculate dependency level for each file (BFS from leaves)."""
        print("Calculating dependency levels...")

        # Find leaf nodes (no imports from project)
        leaves = []
        for module in self.files.keys():
            project_imports = [imp for imp in self.imports[module]
                               if imp in self.files]
            if not project_imports:
                leaves.append(module)
                self.dependency_levels[module] = 0

        # BFS from leaves
        queue = deque(leaves)
        visited = set(leaves)

        while queue:
            current = queue.popleft()
            current_level = self.dependency_levels[current]

            # Update files that import current
            for importer in self.imported_by[current]:
                if importer not in visited:
                    self.dependency_levels[importer] = max(
                        self.dependency_levels.get(importer, 0),
                        current_level + 1
                    )

                    # Check if all dependencies processed
                    deps = [imp for imp in self.imports[importer]
                            if imp in self.files]
                    if all(dep in visited for dep in deps):
                        visited.add(importer)
                        queue.append(importer)

        print(f"Calculated levels for {len(self.dependency_levels)} files")

    def detect_circular_dependencies(self):
        """Detect circular dependencies using DFS."""
        print("Detecting circular dependencies...")

        visited = set()
        rec_stack = set()

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.imports.get(node, []):
                if neighbor not in self.files:
                    continue

                if neighbor not in visited:
                    if dfs(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if cycle not in self.circular_deps:
                        self.circular_deps.append(cycle)
                    return True

            path.pop()
            rec_stack.remove(node)
            return False

        for module in self.files.keys():
            if module not in visited:
                dfs(module, [])

        print(f"Found {len(self.circular_deps)} circular dependencies")

    def identify_orphan_files(self):
        """Identify files not imported by anyone."""
        print("Identifying orphan files...")

        for module in self.files.keys():
            if not self.imported_by[module]:
                self.orphan_files.add(module)

        print(f"Found {len(self.orphan_files)} orphan files")

    def generate_dependency_table(self, output_dir: str):
        """Generate comprehensive dependency table in Markdown."""
        output_path = Path(output_dir) / "Dependency_Table.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Dependency Table\n\n")
            f.write(f"**Project:** {self.project_root.name}\n")
            f.write(f"**Total Files:** {len(self.files)}\n")
            f.write(f"**Circular Dependencies:** {len(self.circular_deps)}\n")
            f.write(f"**Orphan Files:** {len(self.orphan_files)}\n\n")

            f.write("---\n\n")
            f.write("## Dependency Table\n\n")
            f.write(
                "| Module | Path | Imports From | Imported By | Dependency Level |\n")
            f.write(
                "|--------|------|--------------|-------------|------------------|\n")

            # Sort by dependency level (ascending)
            sorted_modules = sorted(
                self.files.keys(),
                key=lambda m: (self.dependency_levels.get(m, 999), m)
            )

            for module in sorted_modules:
                path = str(self.files[module].relative_to(self.project_root))

                # Get project imports only
                imports = [
                    imp for imp in self.imports[module] if imp in self.files]
                imports_str = ", ".join(sorted(imports)[:5])
                if len(imports) > 5:
                    imports_str += f", ... (+{len(imports)-5})"
                if not imports_str:
                    imports_str = "-"

                # Get importers
                importers = list(self.imported_by[module])
                importers_str = ", ".join(sorted(importers)[:5])
                if len(importers) > 5:
                    importers_str += f", ... (+{len(importers)-5})"
                if not importers_str:
                    importers_str = "-"

                level = self.dependency_levels.get(module, "?")

                f.write(
                    f"| `{module}` | `{path}` | {imports_str} | {importers_str} | {level} |\n")

        print(f"Generated dependency table: {output_path}")
        return output_path

    def generate_dependency_graph(self, output_dir: str):
        """Generate dependency graph in JSON format."""
        output_path = Path(output_dir) / "Dependency_Graph.json"

        graph = {
            "nodes": [
                {
                    "id": module,
                    "path": str(self.files[module].relative_to(self.project_root)),
                    "level": self.dependency_levels.get(module, None),
                    "is_orphan": module in self.orphan_files
                }
                for module in self.files.keys()
            ],
            "edges": [
                {"from": module, "to": imp}
                for module in self.files.keys()
                for imp in self.imports[module]
                if imp in self.files
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2)

        print(f"Generated dependency graph: {output_path}")
        return output_path

    def generate_circular_dependencies_report(self, output_dir: str):
        """Generate circular dependencies report."""
        output_path = Path(output_dir) / "Circular_Dependencies.md"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Circular Dependencies Report\n\n")

            if not self.circular_deps:
                f.write("✅ **No circular dependencies found!**\n")
            else:
                f.write(
                    f"⚠️ **Found {len(self.circular_deps)} circular dependencies:**\n\n")

                for i, cycle in enumerate(self.circular_deps, 1):
                    f.write(f"## Cycle {i}\n\n")
                    f.write("```\n")
                    f.write(" → ".join(cycle))
                    f.write("\n```\n\n")

        print(f"Generated circular dependencies report: {output_path}")
        return output_path

    def generate_orphan_files_report(self, output_dir: str):
        """Generate orphan files report."""
        output_path = Path(output_dir) / "Orphan_Files.md"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Orphan Files Report\n\n")
            f.write("Files that are not imported by any other file.\n\n")

            if not self.orphan_files:
                f.write("✅ **No orphan files found!**\n")
            else:
                f.write(
                    f"⚠️ **Found {len(self.orphan_files)} orphan files:**\n\n")

                for module in sorted(self.orphan_files):
                    path = str(
                        self.files[module].relative_to(
                            self.project_root))
                    f.write(f"- `{module}` (`{path}`)\n")

        print(f"Generated orphan files report: {output_path}")
        return output_path

    def run_full_analysis(self, output_dir: str = "docs"):
        """Run complete dependency analysis."""
        self.scan_project()
        self.analyze_imports()
        self.calculate_dependency_levels()
        self.detect_circular_dependencies()
        self.identify_orphan_files()

        self.generate_dependency_table(output_dir)
        self.generate_dependency_graph(output_dir)
        self.generate_circular_dependencies_report(output_dir)
        self.generate_orphan_files_report(output_dir)

        print("\n✅ Dependency analysis complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive Python project dependency analysis"
    )
    parser.add_argument(
        "project_root",
        help="Root directory of the project to analyze"
    )
    parser.add_argument(
        "--output",
        default="docs",
        help="Output directory for reports (default: docs)"
    )

    args = parser.parse_args()

    analyzer = DependencyAnalyzer(args.project_root)
    analyzer.run_full_analysis(args.output)


if __name__ == "__main__":
    main()
