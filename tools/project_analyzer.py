#!/usr/bin/env python3
"""
Project Analyzer - Analyzes the entire codebase for dependencies, usage, and duplicates
Part of PROMPT 84: PROJECT ANALYSIS & CLEANUP
"""

import os
import json
import ast
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import re

class ProjectAnalyzer:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.dependency_map = defaultdict(lambda: {"imports": [], "exports": [], "used_by": []})
        self.file_hashes = {}
        self.file_contents = {}
        self.duplicate_files = defaultdict(list)
        self.similar_files = []
        self.unused_files = set()
        self.all_files = set()
        
        # Directories to skip
        self.skip_dirs = {
            'node_modules', '.venv', 'venv', '__pycache__', '.git', 
            'dist', 'build', '.next', 'coverage', 'playwright-report',
            '.pytest_cache', 'htmlcov', 'instance'
        }
        
        # File extensions to analyze
        self.python_exts = {'.py'}
        self.js_exts = {'.js', '.jsx', '.ts', '.tsx'}
        self.all_exts = self.python_exts | self.js_exts
    
    def should_skip(self, path: Path) -> bool:
        """Check if path should be skipped"""
        parts = path.parts
        return any(skip_dir in parts for skip_dir in self.skip_dirs)
    
    def get_file_hash(self, filepath: Path) -> str:
        """Get MD5 hash of file content"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def get_file_content(self, filepath: Path) -> str:
        """Read file content"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""
    
    def analyze_python_file(self, filepath: Path) -> Dict:
        """Analyze Python file for imports and exports"""
        content = self.get_file_content(filepath)
        if not content:
            return {"imports": [], "exports": []}
        
        imports = []
        exports = []
        
        try:
            tree = ast.parse(content)
            
            # Find imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # Find exports (functions, classes)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not node.name.startswith('_'):
                        exports.append(node.name)
        
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
        
        return {"imports": imports, "exports": exports}
    
    def analyze_js_file(self, filepath: Path) -> Dict:
        """Analyze JavaScript/TypeScript file for imports and exports"""
        content = self.get_file_content(filepath)
        if not content:
            return {"imports": [], "exports": []}
        
        imports = []
        exports = []
        
        # Find imports
        import_patterns = [
            r"import\s+.*?\s+from\s+['\"](.+?)['\"]",
            r"require\(['\"](.+?)['\"]\)",
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)
        
        # Find exports
        export_patterns = [
            r"export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)",
            r"export\s+\{([^}]+)\}",
        ]
        
        for pattern in export_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if '{' not in match:
                    exports.append(match.strip())
                else:
                    # Handle named exports
                    names = [n.strip().split(' as ')[0] for n in match.split(',')]
                    exports.extend(names)
        
        return {"imports": imports, "exports": exports}
    
    def analyze_file(self, filepath: Path):
        """Analyze a single file"""
        rel_path = str(filepath.relative_to(self.root_dir))
        self.all_files.add(rel_path)
        
        # Get file hash for duplicate detection
        file_hash = self.get_file_hash(filepath)
        if file_hash:
            self.file_hashes[rel_path] = file_hash
            self.duplicate_files[file_hash].append(rel_path)
        
        # Store content for similarity analysis
        content = self.get_file_content(filepath)
        self.file_contents[rel_path] = content
        
        # Analyze dependencies
        if filepath.suffix in self.python_exts:
            analysis = self.analyze_python_file(filepath)
        elif filepath.suffix in self.js_exts:
            analysis = self.analyze_js_file(filepath)
        else:
            return
        
        self.dependency_map[rel_path]["imports"] = analysis["imports"]
        self.dependency_map[rel_path]["exports"] = analysis["exports"]
    
    def scan_directory(self):
        """Scan entire directory tree"""
        print(f"🔍 Scanning directory: {self.root_dir}")
        
        for root, dirs, files in os.walk(self.root_dir):
            # Remove skip directories from dirs list
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            root_path = Path(root)
            if self.should_skip(root_path):
                continue
            
            for file in files:
                filepath = root_path / file
                if filepath.suffix in self.all_exts:
                    self.analyze_file(filepath)
        
        print(f"✅ Found {len(self.all_files)} files to analyze")

    def build_usage_graph(self):
        """Build reverse dependency graph (who uses what)"""
        print("🔗 Building usage graph...")

        for file_path, data in self.dependency_map.items():
            for imported in data["imports"]:
                # Find files that export this import
                for other_file, other_data in self.dependency_map.items():
                    if file_path != other_file:
                        # Check if imported module matches file path or exports
                        if imported in other_data["exports"] or imported in other_file:
                            self.dependency_map[other_file]["used_by"].append(file_path)

        print("✅ Usage graph built")

    def find_unused_files(self):
        """Find files that are not imported by anyone"""
        print("🔍 Finding unused files...")

        for file_path, data in self.dependency_map.items():
            # Skip entry points
            if any(entry in file_path for entry in ['app.py', 'run.py', 'main.py', 'index.js', 'App.jsx']):
                continue

            # If no one uses this file and it's not a test file
            if not data["used_by"] and 'test' not in file_path.lower():
                self.unused_files.add(file_path)

        print(f"✅ Found {len(self.unused_files)} potentially unused files")

    def find_duplicates(self):
        """Find exact duplicate files"""
        print("🔍 Finding duplicate files...")

        exact_duplicates = {
            hash_val: files
            for hash_val, files in self.duplicate_files.items()
            if len(files) > 1
        }

        print(f"✅ Found {len(exact_duplicates)} sets of duplicate files")
        return exact_duplicates

    def calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two files (simple line-based)"""
        lines1 = set(content1.split('\n'))
        lines2 = set(content2.split('\n'))

        if not lines1 or not lines2:
            return 0.0

        intersection = len(lines1 & lines2)
        union = len(lines1 | lines2)

        return intersection / union if union > 0 else 0.0

    def find_similar_files(self, threshold: float = 0.8):
        """Find files with high similarity (but not exact duplicates)"""
        print(f"🔍 Finding similar files (threshold: {threshold})...")

        files = list(self.file_contents.keys())
        similar_pairs = []

        for i, file1 in enumerate(files):
            for file2 in files[i+1:]:
                # Skip if exact duplicates
                if self.file_hashes.get(file1) == self.file_hashes.get(file2):
                    continue

                similarity = self.calculate_similarity(
                    self.file_contents[file1],
                    self.file_contents[file2]
                )

                if similarity >= threshold:
                    similar_pairs.append((file1, file2, similarity))

        self.similar_files = sorted(similar_pairs, key=lambda x: x[2], reverse=True)
        print(f"✅ Found {len(self.similar_files)} pairs of similar files")

    def generate_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        print("📊 Generating report...")

        duplicates = self.find_duplicates()

        report = {
            "summary": {
                "total_files": len(self.all_files),
                "total_dependencies": sum(len(d["imports"]) for d in self.dependency_map.values()),
                "unused_files": len(self.unused_files),
                "duplicate_sets": len(duplicates),
                "similar_pairs": len(self.similar_files),
            },
            "unused_files": sorted(list(self.unused_files)),
            "duplicates": {
                hash_val: files
                for hash_val, files in duplicates.items()
            },
            "similar_files": [
                {"file1": f1, "file2": f2, "similarity": f"{sim:.2%}"}
                for f1, f2, sim in self.similar_files[:20]  # Top 20
            ],
            "dependency_map": dict(self.dependency_map),
        }

        print("✅ Report generated")
        return report

    def save_report(self, output_file: str):
        """Save report to JSON file"""
        report = self.generate_report()

        output_path = self.root_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"💾 Report saved to: {output_path}")
        return report


def main():
    """Main entry point"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else "project_analysis.json"

    analyzer = ProjectAnalyzer(root_dir)

    # Run analysis
    analyzer.scan_directory()
    analyzer.build_usage_graph()
    analyzer.find_unused_files()
    analyzer.find_similar_files(threshold=0.8)

    # Generate and save report
    report = analyzer.save_report(output_file)

    # Print summary
    print("\n" + "="*60)
    print("📊 ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total Files: {report['summary']['total_files']}")
    print(f"Total Dependencies: {report['summary']['total_dependencies']}")
    print(f"Unused Files: {report['summary']['unused_files']}")
    print(f"Duplicate Sets: {report['summary']['duplicate_sets']}")
    print(f"Similar Pairs: {report['summary']['similar_pairs']}")
    print("="*60)


if __name__ == "__main__":
    main()

