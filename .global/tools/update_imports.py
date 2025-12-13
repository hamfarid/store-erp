#!/usr/bin/env python3
"""
File: tools/update_imports.py
Path: /home/ubuntu/global/tools/update_imports.py

Import Statement Update Tool

This tool updates import statements across the entire project when
modules are moved, renamed, or merged. It uses AST parsing for
accurate detection and modification of imports.

Features:
- AST-based import detection
- Support for all import styles (import, from...import, as)
- Circular dependency detection
- Dry-run mode for safety
- Comprehensive reporting

Usage:
    python update_imports.py <old_module> <new_module> [--dry-run] [--project-root .]

Examples:
    # Rename module
    python update_imports.py models.user models.user_unified

    # Move module
    python update_imports.py utils.helpers core.utils.helpers

    # Dry run
    python update_imports.py models.old models.new --dry-run

Author: Gaara ERP Team
Date: 2025-01-15
Version: 1.0.0
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ImportInfo:
    """Information about an import statement."""
    file_path: str
    line_number: int
    import_type: str  # 'import', 'from_import'
    module: str
    names: List[str]
    alias: str = None

    def __str__(self) -> str:
        """String representation."""
        if self.import_type == 'import':
            base = f"import {self.module}"
            if self.alias:
                base += f" as {self.alias}"
        else:  # from_import
            names_str = ', '.join(self.names)
            base = f"from {self.module} import {names_str}"

        return f"{self.file_path}:{self.line_number}: {base}"


class ImportVisitor(ast.NodeVisitor):
    """AST visitor to extract import information."""

    def __init__(self, file_path: str):
        """Initialize visitor."""
        self.file_path = file_path
        self.imports: List[ImportInfo] = []

    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statement."""
        for alias in node.names:
            import_info = ImportInfo(
                file_path=self.file_path,
                line_number=node.lineno,
                import_type='import',
                module=alias.name,
                names=[],
                alias=alias.asname
            )
            self.imports.append(import_info)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from...import statement."""
        if node.module:  # Skip relative imports without module
            names = [alias.name for alias in node.names]
            import_info = ImportInfo(
                file_path=self.file_path,
                line_number=node.lineno,
                import_type='from_import',
                module=node.module,
                names=names
            )
            self.imports.append(import_info)

        self.generic_visit(node)


class ImportUpdater:
    """Updates import statements across the project."""

    def __init__(self, project_root: str = '.', dry_run: bool = False):
        """Initialize updater."""
        self.project_root = Path(project_root).resolve()
        self.dry_run = dry_run
        self.all_imports: List[ImportInfo] = []
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)

    def scan_project(self) -> None:
        """Scan all Python files in the project."""
        print(f"🔍 Scanning project: {self.project_root}")

        py_files = list(self.project_root.rglob('*.py'))

        # Filter out virtual environments and caches
        py_files = [
            f for f in py_files if not any(
                part in f.parts for part in [
                    '__pycache__',
                    '.venv',
                    'venv',
                    'env'])]

        print(f"📊 Found {len(py_files)} Python files")

        for py_file in py_files:
            self._scan_file(py_file)

        print(f"📦 Extracted {len(self.all_imports)} import statements")

    def _scan_file(self, file_path: Path) -> None:
        """Scan a single Python file for imports."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))
            visitor = ImportVisitor(str(file_path))
            visitor.visit(tree)

            self.all_imports.extend(visitor.imports)

            # Build dependency graph
            file_module = self._file_to_module(file_path)
            for imp in visitor.imports:
                self.dependency_graph[file_module].add(imp.module)

        except SyntaxError as e:
            print(f"⚠️  Syntax error in {file_path}: {e}")
        except Exception as e:
            print(f"⚠️  Error scanning {file_path}: {e}")

    def _file_to_module(self, file_path: Path) -> str:
        """Convert file path to module name."""
        try:
            rel_path = file_path.relative_to(self.project_root)
            module_path = str(rel_path.with_suffix('')).replace(os.sep, '.')
            return module_path
        except ValueError:
            return str(file_path)

    def find_affected_imports(
            self,
            old_module: str,
            new_module: str) -> List[ImportInfo]:
        """
        Find all imports that need to be updated.

        Args:
            old_module: Old module name (e.g., 'models.user')
            new_module: New module name (e.g., 'models.user_unified')

        Returns:
            List of ImportInfo objects that need updating
        """
        affected = []

        for imp in self.all_imports:
            # Check exact match
            if imp.module == old_module:
                affected.append(imp)
            # Check if it's a submodule
            elif imp.module.startswith(old_module + '.'):
                affected.append(imp)

        return affected

    def update_imports(self, old_module: str, new_module: str) -> None:
        """
        Update all imports from old_module to new_module.

        Args:
            old_module: Old module name
            new_module: New module name
        """
        affected = self.find_affected_imports(old_module, new_module)

        if not affected:
            print(f"✅ No imports found for '{old_module}'")
            return

        print(f"📝 Found {len(affected)} imports to update")

        # Group by file
        files_to_update: Dict[str, List[ImportInfo]] = defaultdict(list)
        for imp in affected:
            files_to_update[imp.file_path].append(imp)

        print(f"📁 Updating {len(files_to_update)} files")

        for file_path, imports in files_to_update.items():
            self._update_file(file_path, imports, old_module, new_module)

    def _update_file(self, file_path: str, imports: List[ImportInfo],
                     old_module: str, new_module: str) -> None:
        """Update imports in a single file."""
        if self.dry_run:
            print(f"\n🔍 DRY RUN - Would update: {file_path}")
            for imp in imports:
                old_str = str(imp)
                new_module_full = imp.module.replace(old_module, new_module, 1)
                print(f"  - {imp.module} → {new_module_full}")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Sort imports by line number (descending) to avoid line number
            # shifts
            imports_sorted = sorted(
                imports, key=lambda x: x.line_number, reverse=True)

            for imp in imports_sorted:
                line_idx = imp.line_number - 1
                old_line = lines[line_idx]

                # Replace old module with new module
                new_module_full = imp.module.replace(old_module, new_module, 1)
                new_line = old_line.replace(imp.module, new_module_full)

                lines[line_idx] = new_line

            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            print(f"✅ Updated: {file_path} ({len(imports)} imports)")

        except Exception as e:
            print(f"⚠️  Error updating {file_path}: {e}")

    def detect_circular_dependencies(self) -> List[Tuple[str, str]]:
        """
        Detect circular dependencies in the project.

        Returns:
            List of (module1, module2) tuples representing circular deps
        """
        circular = []

        for module, deps in self.dependency_graph.items():
            for dep in deps:
                # Check if dep also depends on module
                if module in self.dependency_graph.get(dep, set()):
                    # Avoid duplicates
                    if (dep, module) not in circular:
                        circular.append((module, dep))

        return circular

    def generate_report(
            self,
            output_file: str = 'docs/Import_Update_Report.md') -> None:
        """Generate comprehensive import report."""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Import Update Report\n\n")
            f.write(f"**Project:** {self.project_root}\n\n")
            f.write(f"**Total Imports:** {len(self.all_imports)}\n\n")

            # Group by module
            imports_by_module: Dict[str, List[ImportInfo]] = defaultdict(list)
            for imp in self.all_imports:
                imports_by_module[imp.module].append(imp)

            f.write("## Imports by Module\n\n")
            for module in sorted(imports_by_module.keys()):
                imports = imports_by_module[module]
                f.write(f"### {module} ({len(imports)} imports)\n\n")

                for imp in imports[:10]:  # Limit to first 10
                    f.write(f"- {imp.file_path}:{imp.line_number}\n")

                if len(imports) > 10:
                    f.write(f"- ... and {len(imports) - 10} more\n")

                f.write("\n")

            # Circular dependencies
            circular = self.detect_circular_dependencies()
            if circular:
                f.write("## ⚠️  Circular Dependencies\n\n")
                for mod1, mod2 in circular:
                    f.write(f"- {mod1} ↔ {mod2}\n")
                f.write("\n")

            # Dependency graph
            f.write("## Dependency Graph\n\n")
            f.write("```\n")
            for module, deps in sorted(self.dependency_graph.items()):
                if deps:
                    f.write(f"{module}:\n")
                    for dep in sorted(deps):
                        f.write(f"  → {dep}\n")
            f.write("```\n")

        print(f"📄 Report generated: {output_file}")


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print(
            "Usage: python update_imports.py <old_module> <new_module> [--dry-run] [--project-root .]")
        print("\nExamples:")
        print("  python update_imports.py models.user models.user_unified")
        print("  python update_imports.py utils.helpers core.utils.helpers --dry-run")
        sys.exit(1)

    old_module = sys.argv[1]
    new_module = sys.argv[2]
    dry_run = '--dry-run' in sys.argv
    project_root = '.'

    # Parse optional arguments
    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == '--project-root' and i + 1 < len(sys.argv):
            project_root = sys.argv[i + 1]

    print(f"🔄 Updating imports: {old_module} → {new_module}")
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")

    # Create updater
    updater = ImportUpdater(project_root=project_root, dry_run=dry_run)

    # Scan project
    updater.scan_project()

    # Update imports
    updater.update_imports(old_module, new_module)

    # Generate report
    if not dry_run:
        updater.generate_report()

    # Check for circular dependencies
    circular = updater.detect_circular_dependencies()
    if circular:
        print(
            f"\n⚠️  Warning: {len(circular)} circular dependencies detected!")
        print("   See Import_Update_Report.md for details")

    print("\n✅ Import update complete!")


if __name__ == '__main__':
    main()
