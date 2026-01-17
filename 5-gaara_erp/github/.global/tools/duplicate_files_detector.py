#!/usr/bin/env python3
"""
Duplicate Files Detector
Detects files with similar names (excluding .md files)

Usage:
    python duplicate_files_detector.py /path/to/project
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict
import hashlib
import json

class DuplicateFilesDetector:
    def __init__(self, project_path: str, exclude_extensions: List[str] = None):
        self.project_path = Path(project_path)
        self.exclude_extensions = exclude_extensions or ['.md', '.txt', '.log']
        self.exclude_dirs = {
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            'dist', 'build', '.next', '.cache', 'coverage'
        }
        self.similar_files = defaultdict(list)
        self.duplicate_files = defaultdict(list)
        
    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        # Skip by extension
        if file_path.suffix.lower() in self.exclude_extensions:
            return True
        
        # Skip by directory
        for part in file_path.parts:
            if part in self.exclude_dirs:
                return True
        
        return False
    
    def normalize_filename(self, filename: str) -> str:
        """Normalize filename for comparison"""
        # Remove extension
        name = Path(filename).stem
        
        # Remove version numbers (v1, v2, _v1, -v2, etc.)
        name = re.sub(r'[_-]?v\d+', '', name, flags=re.IGNORECASE)
        
        # Remove copy indicators (copy, Copy, COPY, (1), (2), etc.)
        name = re.sub(r'[_-]?copy\d*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\(\d+\)', '', name)
        
        # Remove trailing numbers
        name = re.sub(r'[_-]?\d+$', '', name)
        
        # Convert to lowercase
        name = name.lower()
        
        # Remove special characters
        name = re.sub(r'[^a-z0-9]', '', name)
        
        return name
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def find_similar_names(self) -> Dict[str, List[Path]]:
        """Find files with similar names"""
        print("🔍 Scanning for files with similar names...")
        
        name_groups = defaultdict(list)
        
        for file_path in self.project_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            if self.should_skip_file(file_path):
                continue
            
            normalized = self.normalize_filename(file_path.name)
            if normalized:  # Only add if normalized name is not empty
                name_groups[normalized].append(file_path)
        
        # Filter to only groups with multiple files
        similar_files = {
            name: files for name, files in name_groups.items()
            if len(files) > 1
        }
        
        return similar_files
    
    def find_exact_duplicates(self) -> Dict[str, List[Path]]:
        """Find files with identical content (by hash)"""
        print("🔍 Scanning for files with identical content...")
        
        hash_groups = defaultdict(list)
        
        for file_path in self.project_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            if self.should_skip_file(file_path):
                continue
            
            file_hash = self.calculate_file_hash(file_path)
            if file_hash:
                hash_groups[file_hash].append(file_path)
        
        # Filter to only groups with multiple files
        duplicate_files = {
            file_hash: files for file_hash, files in hash_groups.items()
            if len(files) > 1
        }
        
        return duplicate_files
    
    def generate_report(self) -> Dict:
        """Generate comprehensive report"""
        print("\n" + "="*80)
        print("DUPLICATE FILES DETECTION REPORT")
        print("="*80)
        
        similar_files = self.find_similar_names()
        duplicate_files = self.find_exact_duplicates()
        
        report = {
            'project_path': str(self.project_path),
            'similar_names': {},
            'exact_duplicates': {},
            'summary': {
                'similar_name_groups': len(similar_files),
                'similar_name_files': sum(len(files) for files in similar_files.values()),
                'exact_duplicate_groups': len(duplicate_files),
                'exact_duplicate_files': sum(len(files) for files in duplicate_files.values()),
            }
        }
        
        # Process similar names
        for normalized_name, files in similar_files.items():
            report['similar_names'][normalized_name] = [str(f) for f in files]
        
        # Process exact duplicates
        for file_hash, files in duplicate_files.items():
            # Use first file's name as key
            key = files[0].name
            report['exact_duplicates'][key] = [str(f) for f in files]
        
        return report
    
    def print_report(self):
        """Print report to console"""
        report = self.generate_report()
        
        print(f"\nProject: {report['project_path']}")
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")
        print(f"Similar Name Groups: {report['summary']['similar_name_groups']}")
        print(f"Similar Name Files: {report['summary']['similar_name_files']}")
        print(f"Exact Duplicate Groups: {report['summary']['exact_duplicate_groups']}")
        print(f"Exact Duplicate Files: {report['summary']['exact_duplicate_files']}")
        
        # Print similar names
        if report['similar_names']:
            print(f"\n{'='*80}")
            print("FILES WITH SIMILAR NAMES")
            print(f"{'='*80}")
            
            for normalized_name, files in sorted(report['similar_names'].items()):
                print(f"\n📁 Group: {normalized_name}")
                print(f"   Files ({len(files)}):")
                for file_path in files:
                    print(f"   - {file_path}")
        
        # Print exact duplicates
        if report['exact_duplicates']:
            print(f"\n{'='*80}")
            print("FILES WITH IDENTICAL CONTENT")
            print(f"{'='*80}")
            
            for key, files in sorted(report['exact_duplicates'].items()):
                print(f"\n📄 Group: {key}")
                print(f"   Files ({len(files)}):")
                for file_path in files:
                    print(f"   - {file_path}")
        
        # Final verdict
        print(f"\n{'='*80}")
        total_issues = (
            report['summary']['similar_name_groups'] +
            report['summary']['exact_duplicate_groups']
        )
        
        if total_issues == 0:
            print("✅ No duplicate or similar files found!")
        else:
            print(f"⚠️  Found {total_issues} groups of duplicate/similar files")
            print("   Run the deduplication tool to merge them.")
        
        print(f"{'='*80}\n")
        
        return report
    
    def save_report(self, output_file: str = None):
        """Save report to JSON file"""
        if output_file is None:
            output_file = self.project_path / 'docs' / 'duplicate_files_report.json'
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = self.generate_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Report saved to: {output_path}")
        
        return output_path

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python duplicate_files_detector.py /path/to/project")
        print("\nExample:")
        print("  python duplicate_files_detector.py /home/user/my-project")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)
    
    detector = DuplicateFilesDetector(project_path)
    detector.print_report()
    detector.save_report()

if __name__ == '__main__':
    main()

