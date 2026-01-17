#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Analyzer - Comprehensive codebase analysis tool
Analyzes dependencies, detects duplicates, and identifies unused files
"""

import os
import json
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import hashlib
from difflib import SequenceMatcher


class ProjectAnalyzer:
    """Comprehensive project analysis tool"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.dependencies: Dict[str, Dict] = {}
        self.file_hashes: Dict[str, str] = {}
        self.file_contents: Dict[str, str] = {}
        self.imports_map: Dict[str, List[str]] = defaultdict(list)
        self.exports_map: Dict[str, List[str]] = defaultdict(list)
        self.usage_map: Dict[str, Set[str]] = defaultdict(set)
        self.duplicates: List[Tuple[str, str, float]] = []
        
        # Patterns for duplicate detection
        self.duplicate_patterns = [
            r'fix|clean|unified|enhanced|advanced|simple|smorest',
            r'_v\d+|_backup|_old|_new|_copy',
            r'test_.*_copy|.*_temp|.*_tmp'
        ]
        
        # Directories to skip
        self.skip_dirs = {
            'node_modules', '.venv', 'venv', '__pycache__',
            '.git', '.pytest_cache', 'dist', 'build',
            'coverage', '.next', 'out', 'global', 'unneeded',
            '.github', 'monitoring', 'postman', 'tmp', 'ui'
        }
        
        # File extensions to analyze
        self.analyze_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx',
            '.json', '.yml', '.yaml', '.md'
        }

    def analyze(self, stages: List[int] = None):
        """Run complete project analysis in stages
        
        Args:
            stages: List of stage numbers to run (1-5), or None for all
        """
        if stages is None:
            stages = [1, 2, 3, 4, 5]
        
        print("🔍 Starting comprehensive project analysis...")
        print(f"   Running stages: {stages}")
        
        if 1 in stages:
            print("\n📂 Phase 1: Scanning files...")
            self._scan_files()
            self._save_progress('stage1_files')
        
        if 2 in stages:
            print("\n🔗 Phase 2: Analyzing dependencies...")
            self._load_progress('stage1_files')
            self._analyze_dependencies()
            self._save_progress('stage2_deps')
        
        if 3 in stages:
            print("\n🔎 Phase 3: Detecting duplicates...")
            self._load_progress('stage2_deps')
            self._detect_duplicates()
            self._save_progress('stage3_dups')
        
        if 4 in stages:
            print("\n📊 Phase 4: Analyzing usage...")
            self._load_progress('stage3_dups')
            self._analyze_usage()
            self._save_progress('stage4_usage')
        
        if 5 in stages:
            print("\n💾 Phase 5: Generating reports...")
            self._load_progress('stage4_usage')
            self._generate_reports()
        
        print("\n✅ Analysis complete!")
    
    def _save_progress(self, stage_name: str):
        """Save progress to temp file"""
        progress_file = self.root_dir / f'.analysis_{stage_name}.json'
        data = {
            'file_contents': self.file_contents,
            'file_hashes': self.file_hashes,
            'dependencies': self.dependencies,
            'imports_map': {k: list(v) for k, v in self.imports_map.items()},
            'exports_map': {k: list(v) for k, v in self.exports_map.items()},
            'usage_map': {k: list(v) for k, v in self.usage_map.items()},
            'duplicates': self.duplicates
        }
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"  💾 Progress saved to {progress_file.name}")
    
    def _load_progress(self, stage_name: str):
        """Load progress from temp file"""
        progress_file = self.root_dir / f'.analysis_{stage_name}.json'
        if not progress_file.exists():
            return
        
        with open(progress_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.file_contents = data.get('file_contents', {})
        self.file_hashes = data.get('file_hashes', {})
        self.dependencies = data.get('dependencies', {})
        self.imports_map = defaultdict(list, {k: v for k, v in data.get('imports_map', {}).items()})
        self.exports_map = defaultdict(list, {k: v for k, v in data.get('exports_map', {}).items()})
        self.usage_map = defaultdict(set, {k: set(v) for k, v in data.get('usage_map', {}).items()})
        self.duplicates = data.get('duplicates', [])
        print(f"  📂 Loaded progress from {progress_file.name}")

    def _scan_files(self):
        """Scan all files in the project"""
        file_count = 0
        for root, dirs, files in os.walk(self.root_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            root_path = Path(root)
            for file in files:
                file_path = root_path / file
                ext = file_path.suffix.lower()
                
                if ext in self.analyze_extensions:
                    try:
                        rel_path = str(file_path.relative_to(self.root_dir))
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        self.file_contents[rel_path] = content
                        self.file_hashes[rel_path] = self._hash_content(
                            content
                        )
                        
                        file_count += 1
                        if file_count % 10 == 0:
                            print(f"  📄 Scanned {file_count} files...")
                    except Exception as e:
                        print(f"  ⚠️  Error reading {file_path}: {e}")
        
        print(f"  ✅ Total files scanned: {file_count}")

    def _hash_content(self, content: str) -> str:
        """Generate hash of normalized content"""
        # Normalize whitespace and comments for better duplicate detection
        normalized = re.sub(r'\s+', ' ', content)
        normalized = re.sub(r'#.*?$', '', normalized, flags=re.MULTILINE)
        normalized = re.sub(r'//.*?$', '', normalized, flags=re.MULTILINE)
        return hashlib.md5(normalized.encode()).hexdigest()

    def _analyze_dependencies(self):
        """Analyze imports and exports for all files"""
        total = len(self.file_contents)
        print(f"  🔍 Analyzing {total} files for dependencies...")
        
        analyzed = 0
        for rel_path, content in self.file_contents.items():
            ext = Path(rel_path).suffix.lower()
            
            try:
                if ext == '.py':
                    self._analyze_python_file(rel_path, content)
                elif ext in {'.js', '.jsx', '.ts', '.tsx'}:
                    self._analyze_javascript_file(rel_path, content)
            except Exception as e:
                print(f"  ⚠️  Error analyzing {rel_path}: {e}")
            
            analyzed += 1
            if analyzed % 50 == 0:
                print(f"  📊 Progress: {analyzed}/{total} files analyzed...")
        
        print(f"  ✅ Total dependencies found: {len(self.dependencies)}")

    def _analyze_python_file(self, rel_path: str, content: str):
        """Analyze Python file for imports and exports"""
        try:
            tree = ast.parse(content)
            imports = []
            exports = []
            
            for node in ast.walk(tree):
                # Imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                
                # Exports (functions, classes)
                elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    exports.append(node.name)
            
            self.imports_map[rel_path] = imports
            self.exports_map[rel_path] = exports
            
            self.dependencies[rel_path] = {
                'type': 'python',
                'imports': imports,
                'exports': exports
            }
        except SyntaxError:
            pass

    def _analyze_javascript_file(self, rel_path: str, content: str):
        """Analyze JavaScript/TypeScript file for imports and exports"""
        imports = []
        exports = []
        
        # Match import statements
        import_patterns = [
            r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]',
            r'import\s+[\'"](.+?)[\'"]',
            r'require\([\'"](.+?)[\'"]\)'
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                imports.append(match.group(1))
        
        # Match export statements
        export_patterns = [
            r'export\s+(?:default\s+)?(?:class|function)\s+(\w+)',
            r'export\s+const\s+(\w+)',
            r'export\s+\{([^}]+)\}'
        ]
        
        for pattern in export_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                exported = match.group(1)
                if '{' not in exported:
                    exports.append(exported)
                else:
                    # Parse multiple exports
                    names = re.findall(r'\w+', exported)
                    exports.extend(names)
        
        self.imports_map[rel_path] = imports
        self.exports_map[rel_path] = exports
        
        self.dependencies[rel_path] = {
            'type': 'javascript',
            'imports': imports,
            'exports': exports
        }

    def _detect_duplicates(self):
        """Detect duplicate and similar files with progress tracking"""
        files = list(self.file_contents.keys())
        total = len(files)
        print(f"  🔍 Comparing {total} files for duplicates...")
        
        # Load processed files to avoid re-checking
        processed_file = self.root_dir / '.analysis_processed_files.json'
        processed = set()
        if processed_file.exists():
            try:
                with open(processed_file, 'r') as f:
                    processed = set(json.load(f))
                print(f"  📂 Loaded {len(processed)} already processed files")
            except Exception:
                pass
        
        checked = 0
        skipped = 0
        last_progress = 0
        
        for i, file1 in enumerate(files):
            # Skip if already processed
            if file1 in processed:
                skipped += 1
                continue
            
            # Only check files with similar names first (optimization)
            candidates = []
            for file2 in files[i+1:]:
                if file2 in processed:
                    continue
                if self._names_similar(file1, file2):
                    candidates.append(file2)
            
            # Also check same extension files with identical hashes
            ext1 = Path(file1).suffix
            file1_size = len(self.file_contents.get(file1, ''))
            
            for file2 in files[i+1:]:
                if file2 in processed or file2 in candidates:
                    continue
                
                # Quick size check - skip if sizes differ too much
                file2_size = len(self.file_contents.get(file2, ''))
                size_ratio = max(file1_size, file2_size) / max(1, min(file1_size, file2_size))
                if size_ratio > 1.2:
                    continue
                
                if (Path(file2).suffix == ext1 and 
                    self.file_hashes[file1] == self.file_hashes[file2]):
                    candidates.append(file2)
            
            # Check content similarity only for candidates (only if hashes match or names very similar)
            for file2 in candidates:
                try:
                    # Only do expensive content comparison if hashes match or names are very similar
                    if self.file_hashes[file1] == self.file_hashes[file2]:
                        # Identical files - skip content comparison
                        self.duplicates.append((file1, file2, 1.0))
                        print(f"  🔄 Found identical: {Path(file1).name} = {Path(file2).name}")
                    elif self._names_similar(file1, file2):
                        # Names similar - do quick check
                        similarity = self._content_similarity(file1, file2)
                        if similarity > 0.8:
                            self.duplicates.append((file1, file2, similarity))
                            print(f"  🔄 Found similar: {Path(file1).name} ≈ {Path(file2).name} ({similarity:.1%})")
                except Exception:
                    continue
            
            # Mark as processed
            processed.add(file1)
            checked += 1
            
            # Show progress bar every file
            progress_pct = int((checked / (total - skipped)) * 100) if total > skipped else 0
            bar_length = 40
            filled = int(bar_length * checked / (total - skipped)) if total > skipped else 0
            bar = '█' * filled + '░' * (bar_length - filled)
            
            if progress_pct >= last_progress + 1 or checked % 10 == 0:
                msg = f"\r  [{bar}] {progress_pct}% | {checked}/{total - skipped} | Dups: {len(self.duplicates)}"
                print(msg, end='', flush=True)
                last_progress = progress_pct
            
            # Save progress every 10 files
            if checked % 10 == 0:
                with open(processed_file, 'w') as f:
                    json.dump(list(processed), f)
        
        print(f"\n  ✅ Completed: {checked} checked, {skipped} skipped, {len(self.duplicates)} duplicates")
        
        # Final save
        with open(processed_file, 'w') as f:
            json.dump(list(processed), f)
        
        print(f"  ✅ Duplicate detection complete: {len(self.duplicates)} pairs found")

    def _names_similar(self, file1: str, file2: str) -> bool:
        """Check if file names suggest duplication"""
        name1 = Path(file1).stem.lower()
        name2 = Path(file2).stem.lower()
        
        # Check for duplicate patterns
        for pattern in self.duplicate_patterns:
            if (re.search(pattern, name1) and re.search(pattern, name2)):
                base1 = re.sub(pattern, '', name1)
                base2 = re.sub(pattern, '', name2)
                if base1 == base2:
                    return True
        
        return False

    def _content_similarity(self, file1: str, file2: str) -> float:
        """Calculate content similarity between two files"""
        content1 = self.file_contents[file1]
        content2 = self.file_contents[file2]
        
        # Normalize content
        norm1 = re.sub(r'\s+', ' ', content1).strip()
        norm2 = re.sub(r'\s+', ' ', content2).strip()
        
        return SequenceMatcher(None, norm1, norm2).ratio()

    def _analyze_usage(self):
        """Determine which files are actively used"""
        total = len(self.imports_map)
        print(f"  🔍 Analyzing usage for {total} files...")
        
        analyzed = 0
        # Build usage graph
        for file, imports in self.imports_map.items():
            for imp in imports:
                # Try to resolve import to actual file
                resolved = self._resolve_import(file, imp)
                if resolved:
                    self.usage_map[resolved].add(file)
            
            analyzed += 1
            if analyzed % 50 == 0:
                print(f"  📊 Progress: {analyzed}/{total} files analyzed...")
        
        # Identify unused files
        unused = []
        for file in self.file_contents.keys():
            # Skip special files
            if any(x in file.lower() for x in [
                'readme', 'license', 'changelog',
                'package.json', 'setup.py', '__init__'
            ]):
                continue
            
            # Check if file is imported anywhere
            if file not in self.usage_map or not self.usage_map[file]:
                # Check if it's an entry point
                if not self._is_entry_point(file):
                    unused.append(file)
        
        used_count = len(self.file_contents) - len(unused)
        print(f"  ✅ Used files: {used_count}/{len(self.file_contents)}")
        print(f"  🗑️  Unused files: {len(unused)}")
        
        return unused

    def _resolve_import(self, from_file: str, import_path: str) -> str:
        """Try to resolve import to actual file path"""
        from_dir = Path(from_file).parent
        
        # Handle relative imports
        if import_path.startswith('.'):
            # Python relative import
            import_path = import_path.replace('.', '/')
            resolved = from_dir / import_path
        elif '/' in import_path or '\\' in import_path:
            # Already a path
            resolved = self.root_dir / import_path
        else:
            # Try to find in project
            for file in self.file_contents.keys():
                if import_path in file:
                    return file
            return None
        
        # Try different extensions
        for ext in self.analyze_extensions:
            candidate = resolved.with_suffix(ext)
            rel = str(candidate.relative_to(self.root_dir))
            if rel in self.file_contents:
                return rel
        
        return None

    def _is_entry_point(self, file: str) -> bool:
        """Check if file is an entry point"""
        entry_patterns = [
            r'main\.py$', r'app\.py$', r'index\.[jt]sx?$',
            r'server\.[jt]s$', r'setup\.py$',
            r'manage\.py$', r'wsgi\.py$'
        ]
        
        return any(re.search(p, file) for p in entry_patterns)

    def _generate_reports(self):
        """Generate JSON reports"""
        docs_dir = self.root_dir / 'docs'
        docs_dir.mkdir(exist_ok=True)
        
        # Dependency map
        dep_map_path = docs_dir / 'dependency_map.json'
        with open(dep_map_path, 'w', encoding='utf-8') as f:
            json.dump({
                'files': list(self.file_contents.keys()),
                'dependencies': self.dependencies,
                'imports': dict(self.imports_map),
                'exports': dict(self.exports_map)
            }, f, indent=2)
        print(f"  📝 Created: {dep_map_path}")
        
        # File usage
        unused = [
            f for f in self.file_contents.keys()
            if f not in self.usage_map and not self._is_entry_point(f)
        ]
        
        usage_path = docs_dir / 'file_usage.json'
        with open(usage_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total_files': len(self.file_contents),
                'used_files': len(self.usage_map),
                'unused_files': len(unused),
                'unused': unused,
                'usage_map': {k: list(v) for k, v in self.usage_map.items()}
            }, f, indent=2)
        print(f"  ✅ Created: {usage_path}")
        
        # Duplicate files
        print("  ⏳ Writing duplicates report...")
        dup_path = docs_dir / 'duplicate_files.json'
        with open(dup_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total_duplicates': len(self.duplicates),
                'duplicates': [
                    {
                        'file1': d[0],
                        'file2': d[1],
                        'similarity': f"{d[2]:.2%}"
                    }
                    for d in self.duplicates
                ]
            }, f, indent=2)
        print(f"  ✅ Created: {dup_path}")
        
        # Summary report
        print("  ⏳ Writing summary report...")
        summary_path = docs_dir / 'analysis_summary.md'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_summary())
        print(f"  ✅ Created: {summary_path}")
        
        print("\n📊 Report Summary:")
        print(f"  • Total files: {len(self.file_contents)}")
        print(f"  • Dependencies: {len(self.dependencies)}")
        print(f"  • Duplicates found: {len(self.duplicates)}")
        unused = [f for f in self.file_contents.keys() if f not in self.usage_map and not self._is_entry_point(f)]
        print(f"  • Unused files: {len(unused)}")

    def _generate_summary(self) -> str:
        """Generate markdown summary report"""
        unused = [
            f for f in self.file_contents.keys()
            if f not in self.usage_map and not self._is_entry_point(f)
        ]
        
        return f"""# Project Analysis Summary

## Overview

- **Total Files Analyzed**: {len(self.file_contents)}
- **Total Dependencies**: {len(self.dependencies)}
- **Duplicate Files Found**: {len(self.duplicates)}
- **Unused Files**: {len(unused)}

## Duplicates Detected

{self._format_duplicates()}

## Unused Files

{self._format_unused(unused)}

## Recommendations

1. Review and merge duplicate files
2. Move unused files to `unneeded/` directory
3. Consolidate helper scripts to `tools/` directory
4. Update imports after cleanup

---

*Generated by ProjectAnalyzer*
"""

    def _format_duplicates(self) -> str:
        """Format duplicates for markdown"""
        if not self.duplicates:
            return "*No duplicates found*"
        
        lines = []
        for file1, file2, sim in self.duplicates:
            lines.append(f"- `{file1}` ≈ `{file2}` ({sim:.1%})")
        return '\n'.join(lines)

    def _format_unused(self, unused: List[str]) -> str:
        """Format unused files for markdown"""
        if not unused:
            return "*All files are in use*"
        
        return '\n'.join(f"- `{f}`" for f in unused[:50])


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze project codebase in stages'
    )
    parser.add_argument(
        '--stages',
        type=str,
        default='all',
        help='Stages to run: "all" or comma-separated numbers (e.g., "1,2,3")'
    )
    
    args = parser.parse_args()
    
    # Parse stages
    if args.stages.lower() == 'all':
        stages = None
    else:
        try:
            stages = [int(s.strip()) for s in args.stages.split(',')]
        except ValueError:
            print("❌ Error: Invalid stage numbers. Use 'all' or numbers 1-5")
            return
    
    root = Path(__file__).parent
    analyzer = ProjectAnalyzer(str(root))
    analyzer.analyze(stages=stages)


if __name__ == '__main__':
    main()
