#!/usr/bin/env python3
"""
File: tools/detect_code_duplication.py
Path: /home/ubuntu/global/tools/detect_code_duplication.py

AST-Based Code Duplication Detection Tool

This tool detects code duplication by analyzing the Abstract Syntax Tree (AST)
of Python files, comparing function and class structures semantically rather
than by name.

Features:
- AST-based semantic analysis
- Configurable similarity threshold (default 80%)
- Detailed similarity reports
- Multiple output formats (Markdown, JSON)
- CI/CD integration ready

Usage:
    python detect_code_duplication.py <project_root> [--threshold 80] [--output report.md]

Author: Gaara ERP Team
Date: 2025-01-15
Version: 1.0.0
"""

import ast
import os
import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Set, Any
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class CodeBlock:
    """Represents a code block (function or class)."""
    file_path: str
    name: str
    type: str  # 'function' or 'class'
    start_line: int
    end_line: int
    ast_hash: str
    structure_hash: str
    code: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class DuplicationMatch:
    """Represents a duplication match between two code blocks."""
    block1: CodeBlock
    block2: CodeBlock
    similarity: float
    match_type: str  # 'exact', 'high', 'medium'

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'block1': self.block1.to_dict(),
            'block2': self.block2.to_dict(),
            'similarity': self.similarity,
            'match_type': self.match_type
        }


class ASTHasher:
    """Computes hashes for AST nodes."""

    @staticmethod
    def hash_ast(node: ast.AST, include_names: bool = True) -> str:
        """
        Compute hash of AST node.

        Args:
            node: AST node to hash
            include_names: Include variable/function names in hash

        Returns:
            SHA256 hash of the AST structure
        """
        def serialize_node(n: ast.AST) -> str:
            """Serialize AST node to string."""
            if isinstance(n, ast.AST):
                fields = []
                for field, value in ast.iter_fields(n):
                    # Skip names if requested (for structure comparison)
                    if not include_names and field in ('name', 'id', 'arg'):
                        continue
                    fields.append(f"{field}:{serialize_node(value)}")
                return f"{n.__class__.__name__}({','.join(fields)})"
            elif isinstance(n, list):
                return f"[{','.join(serialize_node(item) for item in n)}]"
            else:
                return str(n)

        serialized = serialize_node(node)
        return hashlib.sha256(serialized.encode()).hexdigest()

    @staticmethod
    def hash_structure(node: ast.AST) -> str:
        """
        Compute hash of AST structure (ignoring names).

        This allows detecting similar code with different variable names.
        """
        return ASTHasher.hash_ast(node, include_names=False)


class CodeBlockExtractor:
    """Extracts code blocks (functions and classes) from Python files."""

    def __init__(self, file_path: str):
        """Initialize extractor with file path."""
        self.file_path = file_path
        self.blocks: List[CodeBlock] = []

    def extract(self) -> List[CodeBlock]:
        """Extract all code blocks from the file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source, filename=self.file_path)
            self._visit_node(tree, source)
            return self.blocks

        except SyntaxError as e:
            print(
                f"⚠️  Syntax error in {self.file_path}: {e}",
                file=sys.stderr)
            return []
        except Exception as e:
            print(
                f"⚠️  Error processing {self.file_path}: {e}",
                file=sys.stderr)
            return []

    def _visit_node(self, node: ast.AST, source: str, parent_name: str = ""):
        """Visit AST node and extract code blocks."""
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._extract_function(child, source, parent_name)
            elif isinstance(child, ast.ClassDef):
                self._extract_class(child, source, parent_name)
                # Recursively visit class methods
                self._visit_node(child, source, child.name)
            else:
                # Continue visiting other nodes
                self._visit_node(child, source, parent_name)

    def _extract_function(
            self,
            node: ast.FunctionDef,
            source: str,
            parent_name: str):
        """Extract function as code block."""
        full_name = f"{parent_name}.{node.name}" if parent_name else node.name
        code = self._get_node_source(node, source)

        block = CodeBlock(
            file_path=self.file_path,
            name=full_name,
            type='function',
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
            ast_hash=ASTHasher.hash_ast(node),
            structure_hash=ASTHasher.hash_structure(node),
            code=code
        )
        self.blocks.append(block)

    def _extract_class(
            self,
            node: ast.ClassDef,
            source: str,
            parent_name: str):
        """Extract class as code block."""
        full_name = f"{parent_name}.{node.name}" if parent_name else node.name
        code = self._get_node_source(node, source)

        block = CodeBlock(
            file_path=self.file_path,
            name=full_name,
            type='class',
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
            ast_hash=ASTHasher.hash_ast(node),
            structure_hash=ASTHasher.hash_structure(node),
            code=code
        )
        self.blocks.append(block)

    def _get_node_source(self, node: ast.AST, source: str) -> str:
        """Get source code for AST node."""
        try:
            lines = source.splitlines()
            start = node.lineno - 1
            end = node.end_lineno if node.end_lineno else node.lineno
            return '\n'.join(lines[start:end])
        except BaseException:
            return ""


class DuplicationDetector:
    """Detects code duplication using AST analysis."""

    def __init__(self, threshold: float = 0.80):
        """
        Initialize detector.

        Args:
            threshold: Similarity threshold (0.0-1.0)
        """
        self.threshold = threshold
        self.blocks: List[CodeBlock] = []
        self.matches: List[DuplicationMatch] = []

    def scan_directory(self, root_dir: str) -> None:
        """Scan directory for Python files and extract code blocks."""
        root_path = Path(root_dir).resolve()

        for py_file in root_path.rglob('*.py'):
            # Skip common non-source directories
            if any(part in py_file.parts for part in [
                '__pycache__', '.venv', 'venv', 'env',
                'node_modules', '.git', 'build', 'dist'
            ]):
                continue

            extractor = CodeBlockExtractor(str(py_file))
            self.blocks.extend(extractor.extract())

    def detect_duplications(self) -> List[DuplicationMatch]:
        """Detect duplications among extracted code blocks."""
        # Group by structure hash for efficiency
        structure_groups = defaultdict(list)
        for block in self.blocks:
            structure_groups[block.structure_hash].append(block)

        # Find duplications within each group
        for structure_hash, group in structure_groups.items():
            if len(group) < 2:
                continue

            # Compare all pairs in the group
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    block1, block2 = group[i], group[j]

                    # Skip if same file and overlapping lines
                    if (block1.file_path == block2.file_path and
                            self._lines_overlap(block1, block2)):
                        continue

                    similarity = self._calculate_similarity(block1, block2)

                    if similarity >= self.threshold:
                        match_type = self._get_match_type(similarity)
                        match = DuplicationMatch(
                            block1=block1,
                            block2=block2,
                            similarity=similarity,
                            match_type=match_type
                        )
                        self.matches.append(match)

        # Sort by similarity (highest first)
        self.matches.sort(key=lambda m: m.similarity, reverse=True)
        return self.matches

    def _lines_overlap(self, block1: CodeBlock, block2: CodeBlock) -> bool:
        """Check if two blocks have overlapping line ranges."""
        return not (block1.end_line < block2.start_line or
                    block2.end_line < block1.start_line)

    def _calculate_similarity(
            self,
            block1: CodeBlock,
            block2: CodeBlock) -> float:
        """
        Calculate similarity between two code blocks.

        Uses structure hash for primary comparison.
        """
        # If structure hashes match, they're very similar
        if block1.structure_hash == block2.structure_hash:
            # Check if AST hashes also match (exact duplicate)
            if block1.ast_hash == block2.ast_hash:
                return 1.0
            else:
                return 0.95  # Same structure, different names

        # For different structures, use a simple metric
        # (In production, you might want more sophisticated comparison)
        return 0.0

    def _get_match_type(self, similarity: float) -> str:
        """Determine match type based on similarity score."""
        if similarity >= 0.95:
            return 'exact'
        elif similarity >= 0.85:
            return 'high'
        else:
            return 'medium'


class ReportGenerator:
    """Generates duplication reports in various formats."""

    @staticmethod
    def generate_markdown(
            matches: List[DuplicationMatch],
            output_file: str) -> None:
        """Generate Markdown report."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Code Duplication Report\n\n")
            f.write(f"**Total Duplications Found:** {len(matches)}\n\n")

            if not matches:
                f.write("✅ No code duplications detected!\n")
                return

            # Group by match type
            exact = [m for m in matches if m.match_type == 'exact']
            high = [m for m in matches if m.match_type == 'high']
            medium = [m for m in matches if m.match_type == 'medium']

            f.write("## Summary\n\n")
            f.write(f"- **Exact Matches:** {len(exact)}\n")
            f.write(f"- **High Similarity:** {len(high)}\n")
            f.write(f"- **Medium Similarity:** {len(medium)}\n\n")

            f.write("---\n\n")

            # Detailed matches
            for idx, match in enumerate(matches, 1):
                f.write(f"## Duplication #{idx}\n\n")
                f.write(
                    f"**Similarity:** {match.similarity*100:.1f}% ({match.match_type})\n\n")

                f.write("### Block 1\n")
                f.write(f"- **File:** `{match.block1.file_path}`\n")
                f.write(f"- **Name:** `{match.block1.name}`\n")
                f.write(f"- **Type:** {match.block1.type}\n")
                f.write(
                    f"- **Lines:** {match.block1.start_line}-{match.block1.end_line}\n\n")

                f.write("### Block 2\n")
                f.write(f"- **File:** `{match.block2.file_path}`\n")
                f.write(f"- **Name:** `{match.block2.name}`\n")
                f.write(f"- **Type:** {match.block2.type}\n")
                f.write(
                    f"- **Lines:** {match.block2.start_line}-{match.block2.end_line}\n\n")

                f.write("---\n\n")

    @staticmethod
    def generate_json(
            matches: List[DuplicationMatch],
            output_file: str) -> None:
        """Generate JSON report."""
        data = {
            'total_duplications': len(matches),
            'matches': [m.to_dict() for m in matches]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(
            "Usage: python detect_code_duplication.py <project_root> [--threshold 80] [--output report.md]")
        sys.exit(1)

    project_root = sys.argv[1]
    threshold = 0.80
    output_file = "docs/Code_Duplication_Report.md"

    # Parse optional arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--threshold' and i + 1 < len(sys.argv):
            threshold = float(sys.argv[i + 1]) / 100.0
        elif arg == '--output' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]

    print(f"🔍 Scanning {project_root} for code duplications...")
    print(f"📊 Similarity threshold: {threshold*100:.0f}%")

    # Detect duplications
    detector = DuplicationDetector(threshold=threshold)
    detector.scan_directory(project_root)

    print(f"📦 Found {len(detector.blocks)} code blocks")

    matches = detector.detect_duplications()

    print(f"🎯 Found {len(matches)} duplications")

    # Generate reports
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)

    ReportGenerator.generate_markdown(matches, output_file)
    print(f"✅ Markdown report: {output_file}")

    json_file = output_file.replace('.md', '.json')
    ReportGenerator.generate_json(matches, json_file)
    print(f"✅ JSON report: {json_file}")

    # Exit with error code if duplications found
    if matches:
        print("\n⚠️  Code duplications detected! Consider refactoring.")
        sys.exit(1)
    else:
        print("\n✅ No code duplications detected!")
        sys.exit(0)


if __name__ == '__main__':
    main()
