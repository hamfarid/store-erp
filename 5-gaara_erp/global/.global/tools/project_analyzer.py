#!/usr/bin/env python3
"""
Project Analyzer - Comprehensive codebase analysis tool.

This tool reads the ENTIRE content of every file in the project and generates:
1. dependency_map.json - Complete import/export graph
2. file_usage.json - Used vs. unused files
3. duplicate_files.json - Duplicate and similar files
"""

import os
import json
import hashlib
import ast
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

# Configuration
PROJECT_ROOT = Path.cwd()
OUTPUT_DIR = PROJECT_ROOT / "docs"
IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".next", "dist", "build", "unneeded"}
CODE_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".py", ".css", ".scss"}

class ProjectAnalyzer:
    def __init__(self):
        self.files = []
        self.dependency_map = {}
        self.file_usage = {}
        self.duplicate_files = []
        self.file_hashes = {}
        
    def analyze(self):
        """Run complete analysis."""
        print("🔍 Starting project analysis...")
        self._scan_files()
        self._analyze_dependencies()
        self._detect_duplicates()
        self._analyze_usage()
        self._generate_reports()
        print("✅ Analysis complete!")
        
    def _scan_files(self):
        """Scan all files in the project."""
        print("📂 Scanning files...")
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in CODE_EXTENSIONS:
                    self.files.append(file_path)
                    
        print(f"   Found {len(self.files)} code files")
        
    def _analyze_dependencies(self):
        """Analyze imports and exports in all files."""
        print("🔗 Analyzing dependencies...")
        
        for file_path in self.files:
            try:
                content = file_path.read_text(encoding='utf-8')
                imports = self._extract_imports(content, file_path.suffix)
                exports = self._extract_exports(content, file_path.suffix)
                
                rel_path = str(file_path.relative_to(PROJECT_ROOT))
                self.dependency_map[rel_path] = {
                    "imports": imports,
                    "exports": exports
                }
            except Exception as e:
                print(f"   ⚠️  Error analyzing {file_path}: {e}")
                
    def _extract_imports(self, content, extension):
        """Extract import statements."""
        imports = []
        
        if extension in {".js", ".jsx", ".ts", ".tsx"}:
            # JavaScript/TypeScript imports
            patterns = [
                r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
                r'require\([\'"](.+?)[\'"]\)',
            ]
            for pattern in patterns:
                imports.extend(re.findall(pattern, content))
                
        elif extension == ".py":
            # Python imports
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
            except:
                pass
                
        return imports
        
    def _extract_exports(self, content, extension):
        """Extract export statements."""
        exports = []
        
        if extension in {".js", ".jsx", ".ts", ".tsx"}:
            # JavaScript/TypeScript exports
            patterns = [
                r'export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)',
                r'export\s+\{([^}]+)\}',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if ',' in match:
                        exports.extend([e.strip() for e in match.split(',')])
                    else:
                        exports.append(match)
                        
        return exports
        
    def _detect_duplicates(self):
        """Detect duplicate and similar files."""
        print("🔎 Detecting duplicates...")
        
        # Group files by content hash
        hash_groups = defaultdict(list)
        
        for file_path in self.files:
            try:
                content = file_path.read_text(encoding='utf-8')
                content_hash = hashlib.md5(content.encode()).hexdigest()
                hash_groups[content_hash].append(str(file_path.relative_to(PROJECT_ROOT)))
                self.file_hashes[str(file_path.relative_to(PROJECT_ROOT))] = content_hash
            except:
                pass
                
        # Find exact duplicates
        for file_group in hash_groups.values():
            if len(file_group) > 1:
                self.duplicate_files.append({
                    "type": "exact",
                    "files": file_group
                })
                
        # Find similar files (by name)
        similar_names = defaultdict(list)
        for file_path in self.files:
            # Extract base name without suffixes like _fixed, _clean, etc.
            name = file_path.stem
            base_name = re.sub(r'[_-](fix|fixed|clean|enhanced|simple|unified|v\d+)$', '', name, flags=re.IGNORECASE)
            similar_names[base_name.lower()].append(str(file_path.relative_to(PROJECT_ROOT)))
            
        for base_name, file_group in similar_names.items():
            if len(file_group) > 1:
                self.duplicate_files.append({
                    "type": "similar_name",
                    "base_name": base_name,
                    "files": file_group
                })
                
    def _analyze_usage(self):
        """Analyze which files are used and which are not."""
        print("📊 Analyzing usage...")
        
        # Build a set of all imported files
        imported_files = set()
        for file_info in self.dependency_map.values():
            for imp in file_info["imports"]:
                # Normalize import path
                if imp.startswith('.'):
                    imported_files.add(imp)
                    
        # Mark files as used or unused
        for rel_path in self.dependency_map.keys():
            is_used = any(imp in rel_path for imp in imported_files)
            self.file_usage[rel_path] = {
                "used": is_used,
                "imported_by": [f for f, info in self.dependency_map.items() if any(imp in rel_path for imp in info["imports"])]
            }
            
    def _generate_reports(self):
        """Generate JSON reports."""
        print("📄 Generating reports...")
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        # Dependency map
        with open(OUTPUT_DIR / "dependency_map.json", "w") as f:
            json.dump(self.dependency_map, f, indent=2)
            
        # File usage
        with open(OUTPUT_DIR / "file_usage.json", "w") as f:
            json.dump(self.file_usage, f, indent=2)
            
        # Duplicate files
        with open(OUTPUT_DIR / "duplicate_files.json", "w") as f:
            json.dump(self.duplicate_files, f, indent=2)
            
        print(f"   Reports saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    analyzer = ProjectAnalyzer()
    analyzer.analyze()

