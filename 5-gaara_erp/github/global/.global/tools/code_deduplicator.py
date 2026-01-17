#!/usr/bin/env python3
"""
Code Deduplicator
Deep code analysis and file merging tool with progress bar

Usage:
    python code_deduplicator.py /path/to/project
"""

import os
import re
import ast
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict
import json
from datetime import datetime
import difflib

class ProgressBar:
    """Simple progress bar for console"""
    def __init__(self, total: int, prefix: str = '', length: int = 50):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.current = 0
    
    def update(self, current: int = None):
        """Update progress bar"""
        if current is not None:
            self.current = current
        else:
            self.current += 1
        
        percent = self.current / self.total if self.total > 0 else 0
        filled = int(self.length * percent)
        bar = '█' * filled + '-' * (self.length - filled)
        
        print(f'\r{self.prefix} |{bar}| {percent*100:.1f}% ({self.current}/{self.total})', end='', flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete

class CodeAnalyzer:
    """Analyze code files for similarity"""
    
    @staticmethod
    def extract_functions(code: str, language: str) -> Set[str]:
        """Extract function signatures from code"""
        functions = set()
        
        if language == 'python':
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.add(node.name)
                    elif isinstance(node, ast.ClassDef):
                        functions.add(node.name)
            except:
                pass
        
        elif language in ['javascript', 'typescript']:
            # Extract function names
            patterns = [
                r'function\s+(\w+)',
                r'const\s+(\w+)\s*=\s*(?:async\s*)?\(',
                r'let\s+(\w+)\s*=\s*(?:async\s*)?\(',
                r'var\s+(\w+)\s*=\s*(?:async\s*)?\(',
                r'(\w+)\s*:\s*(?:async\s*)?function',
                r'class\s+(\w+)',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, code)
                functions.update(matches)
        
        return functions
    
    @staticmethod
    def normalize_code(code: str) -> str:
        """Normalize code for comparison"""
        # Remove comments
        code = re.sub(r'//.*?\n', '\n', code)  # Single line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Multi-line comments
        code = re.sub(r'#.*?\n', '\n', code)  # Python comments
        
        # Remove whitespace
        code = re.sub(r'\s+', ' ', code)
        
        # Remove strings (to focus on logic)
        code = re.sub(r'"[^"]*"', '""', code)
        code = re.sub(r"'[^']*'", "''", code)
        
        return code.strip()
    
    @staticmethod
    def calculate_similarity(code1: str, code2: str) -> float:
        """Calculate similarity between two code snippets"""
        normalized1 = CodeAnalyzer.normalize_code(code1)
        normalized2 = CodeAnalyzer.normalize_code(code2)
        
        # Use SequenceMatcher for similarity
        matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
        return matcher.ratio()

class CodeDeduplicator:
    def __init__(self, project_path: str, similarity_threshold: float = 0.85):
        self.project_path = Path(project_path)
        self.similarity_threshold = similarity_threshold
        self.exclude_extensions = ['.md', '.txt', '.log', '.json', '.xml', '.yml', '.yaml']
        self.exclude_dirs = {
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            'dist', 'build', '.next', '.cache', 'coverage', 'logs'
        }
        self.language_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
        }
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'project_path': str(project_path),
            'duplicate_groups': [],
            'merged_files': [],
            'summary': {
                'total_files_scanned': 0,
                'duplicate_groups_found': 0,
                'files_merged': 0,
                'space_saved_bytes': 0
            }
        }
    
    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        if file_path.suffix.lower() in self.exclude_extensions:
            return True
        
        for part in file_path.parts:
            if part in self.exclude_dirs:
                return True
        
        return False
    
    def get_language(self, file_path: Path) -> str:
        """Get programming language from file extension"""
        return self.language_extensions.get(file_path.suffix.lower(), 'unknown')
    
    def read_file(self, file_path: Path) -> str:
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"\n⚠️  Error reading {file_path}: {e}")
            return ""
    
    def find_duplicate_groups(self) -> List[List[Path]]:
        """Find groups of duplicate/similar files"""
        print("\n🔍 Scanning for duplicate files...")
        
        # Collect all files
        all_files = []
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and not self.should_skip_file(file_path):
                all_files.append(file_path)
        
        self.report['summary']['total_files_scanned'] = len(all_files)
        
        if not all_files:
            print("No files to scan.")
            return []
        
        print(f"Found {len(all_files)} files to analyze")
        
        # Group files by size first (optimization)
        size_groups = defaultdict(list)
        for file_path in all_files:
            try:
                size = file_path.stat().st_size
                size_groups[size].append(file_path)
            except:
                pass
        
        # Find duplicates within each size group
        duplicate_groups = []
        processed_files = set()
        
        progress = ProgressBar(len(all_files), prefix='Analyzing files')
        
        for size, files in size_groups.items():
            if len(files) < 2:
                progress.update(progress.current + len(files))
                continue
            
            # Compare files in this size group
            for i, file1 in enumerate(files):
                if file1 in processed_files:
                    progress.update()
                    continue
                
                group = [file1]
                content1 = self.read_file(file1)
                
                if not content1:
                    progress.update()
                    continue
                
                for file2 in files[i+1:]:
                    if file2 in processed_files:
                        continue
                    
                    content2 = self.read_file(file2)
                    
                    if not content2:
                        continue
                    
                    # Calculate similarity
                    similarity = CodeAnalyzer.calculate_similarity(content1, content2)
                    
                    if similarity >= self.similarity_threshold:
                        group.append(file2)
                        processed_files.add(file2)
                
                if len(group) > 1:
                    duplicate_groups.append(group)
                    processed_files.add(file1)
                
                progress.update()
        
        self.report['summary']['duplicate_groups_found'] = len(duplicate_groups)
        
        return duplicate_groups
    
    def merge_files(self, file_group: List[Path], keep_index: int = 0) -> Dict:
        """Merge duplicate files, keeping one and removing others"""
        if len(file_group) < 2:
            return {'success': False, 'message': 'Not enough files to merge'}
        
        # File to keep
        keep_file = file_group[keep_index]
        
        # Files to remove
        remove_files = [f for i, f in enumerate(file_group) if i != keep_index]
        
        # Create backup directory
        backup_dir = self.project_path / '.global' / 'backups' / 'duplicates' / datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        removed_files = []
        space_saved = 0
        
        for file_path in remove_files:
            try:
                # Backup file before removing
                backup_path = backup_dir / file_path.name
                import shutil
                shutil.copy2(file_path, backup_path)
                
                # Get file size
                size = file_path.stat().st_size
                
                # Remove file
                file_path.unlink()
                
                removed_files.append(str(file_path))
                space_saved += size
                
            except Exception as e:
                print(f"\n⚠️  Error removing {file_path}: {e}")
        
        result = {
            'success': True,
            'kept_file': str(keep_file),
            'removed_files': removed_files,
            'space_saved_bytes': space_saved,
            'backup_dir': str(backup_dir)
        }
        
        self.report['merged_files'].append(result)
        self.report['summary']['files_merged'] += len(removed_files)
        self.report['summary']['space_saved_bytes'] += space_saved
        
        return result
    
    def auto_merge_duplicates(self, duplicate_groups: List[List[Path]]) -> None:
        """Automatically merge all duplicate groups"""
        if not duplicate_groups:
            print("\n✅ No duplicate groups to merge")
            return
        
        print(f"\n🔧 Merging {len(duplicate_groups)} duplicate groups...")
        
        progress = ProgressBar(len(duplicate_groups), prefix='Merging files')
        
        for group in duplicate_groups:
            # Keep the file with the shortest path (usually the original)
            sorted_group = sorted(group, key=lambda x: len(str(x)))
            
            result = self.merge_files(sorted_group, keep_index=0)
            
            if result['success']:
                print(f"\n✅ Merged {len(result['removed_files'])} files into {result['kept_file']}")
            
            progress.update()
    
    def generate_report(self) -> Dict:
        """Generate final report"""
        return self.report
    
    def save_report(self, output_file: str = None):
        """Save report to JSON file"""
        if output_file is None:
            output_file = self.project_path / 'docs' / 'deduplication_report.json'
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Report saved to: {output_path}")
        
        return output_path
    
    def print_summary(self):
        """Print summary of operations"""
        print("\n" + "="*80)
        print("DEDUPLICATION SUMMARY")
        print("="*80)
        print(f"Total Files Scanned: {self.report['summary']['total_files_scanned']}")
        print(f"Duplicate Groups Found: {self.report['summary']['duplicate_groups_found']}")
        print(f"Files Merged: {self.report['summary']['files_merged']}")
        
        space_saved_mb = self.report['summary']['space_saved_bytes'] / (1024 * 1024)
        print(f"Space Saved: {space_saved_mb:.2f} MB")
        print("="*80 + "\n")
    
    def run(self, auto_merge: bool = False):
        """Run the complete deduplication process"""
        print("\n" + "="*80)
        print("CODE DEDUPLICATION TOOL")
        print("="*80)
        print(f"Project: {self.project_path}")
        print(f"Similarity Threshold: {self.similarity_threshold * 100}%")
        print(f"Auto Merge: {'Yes' if auto_merge else 'No'}")
        
        # Find duplicates
        duplicate_groups = self.find_duplicate_groups()
        
        # Store duplicate groups in report
        for group in duplicate_groups:
            self.report['duplicate_groups'].append([str(f) for f in group])
        
        if not duplicate_groups:
            print("\n✅ No duplicate files found!")
            self.save_report()
            return
        
        # Print found duplicates
        print(f"\n📋 Found {len(duplicate_groups)} groups of duplicate files:")
        for i, group in enumerate(duplicate_groups, 1):
            print(f"\nGroup {i}:")
            for file_path in group:
                print(f"  - {file_path}")
        
        # Merge if requested
        if auto_merge:
            self.auto_merge_duplicates(duplicate_groups)
        
        # Print summary
        self.print_summary()
        
        # Save report
        self.save_report()

def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Code Deduplication Tool')
    parser.add_argument('project_path', help='Path to project directory')
    parser.add_argument('--auto-merge', action='store_true', help='Automatically merge duplicate files')
    parser.add_argument('--threshold', type=float, default=0.85, help='Similarity threshold (0.0-1.0)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.project_path):
        print(f"❌ Error: Project path does not exist: {args.project_path}")
        sys.exit(1)
    
    deduplicator = CodeDeduplicator(args.project_path, similarity_threshold=args.threshold)
    deduplicator.run(auto_merge=args.auto_merge)

if __name__ == '__main__':
    main()

