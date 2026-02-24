#!/usr/bin/env python3
"""
Execute Cleanup - Safely delete files with backup
Part of PROMPT 84: PROJECT ANALYSIS & CLEANUP
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class CleanupExecutor:
    def __init__(self, cleanup_plan_file: str, backup_dir: str, root_dir: str, dry_run: bool = True):
        self.plan_file = Path(cleanup_plan_file)
        self.backup_dir = Path(backup_dir)
        self.root_dir = Path(root_dir)  # Root directory (backend or frontend)
        self.dry_run = dry_run

        with open(self.plan_file, 'r', encoding='utf-8') as f:
            self.plan = json.load(f)

        # Create backup directory
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.deleted_files = []
        self.failed_files = []
    
    def backup_file(self, file_path: Path) -> bool:
        """Backup a file before deletion"""
        try:
            # Create same directory structure in backup
            rel_path = file_path.relative_to(file_path.parents[len(file_path.parents) - 2])
            backup_path = self.backup_dir / rel_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(file_path, backup_path)
            return True
        except Exception as e:
            print(f"  ❌ Failed to backup {file_path}: {e}")
            return False
    
    def delete_file(self, file_path: Path) -> bool:
        """Delete a file"""
        try:
            if self.dry_run:
                print(f"  [DRY RUN] Would delete: {file_path}")
                return True
            else:
                file_path.unlink()
                print(f"  ✅ Deleted: {file_path}")
                return True
        except Exception as e:
            print(f"  ❌ Failed to delete {file_path}: {e}")
            return False
    
    def execute_high_confidence(self):
        """Execute high confidence deletions"""
        print("\n🗑️  Executing HIGH CONFIDENCE deletions...")
        print("=" * 60)

        files = self.plan['high_confidence']['files']
        print(f"Files to delete: {len(files)}")

        for file_rel in files:
            # Use root_dir to resolve relative paths
            file_path = self.root_dir / file_rel

            if not file_path.exists():
                print(f"  ⚠️  File not found: {file_rel}")
                continue
            
            # Backup
            if self.backup_file(file_path):
                # Delete
                if self.delete_file(file_path):
                    self.deleted_files.append(str(file_path))
                else:
                    self.failed_files.append(str(file_path))
            else:
                self.failed_files.append(str(file_path))
    
    def execute_medium_confidence(self):
        """Execute medium confidence deletions (duplicates)"""
        print("\n🗑️  Executing MEDIUM CONFIDENCE deletions (duplicates)...")
        print("=" * 60)

        files = self.plan['medium_confidence']['files']
        print(f"Duplicate files to delete: {len(files)}")

        for file_rel in files:
            # Use root_dir to resolve relative paths
            file_path = self.root_dir / file_rel

            if not file_path.exists():
                print(f"  ⚠️  File not found: {file_rel}")
                continue
            
            # Backup
            if self.backup_file(file_path):
                # Delete
                if self.delete_file(file_path):
                    self.deleted_files.append(str(file_path))
                else:
                    self.failed_files.append(str(file_path))
            else:
                self.failed_files.append(str(file_path))
    
    def generate_report(self) -> dict:
        """Generate cleanup report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'backup_directory': str(self.backup_dir),
            'deleted_files': self.deleted_files,
            'failed_files': self.failed_files,
            'summary': {
                'total_deleted': len(self.deleted_files),
                'total_failed': len(self.failed_files)
            }
        }

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print("Usage: python execute_cleanup.py <cleanup_plan.json> <backup_dir> <root_dir> [--execute]")
        print("\nExample: python execute_cleanup.py backend_cleanup_plan.json backup/ ../backend/")
        print("\nBy default, runs in DRY RUN mode. Use --execute to actually delete files.")
        sys.exit(1)

    dry_run = '--execute' not in sys.argv

    executor = CleanupExecutor(sys.argv[1], sys.argv[2], sys.argv[3], dry_run=dry_run)
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be deleted")
        print("=" * 60)
    else:
        print("\n🚨 EXECUTE MODE - Files will be DELETED")
        print("=" * 60)
    
    executor.execute_high_confidence()
    executor.execute_medium_confidence()
    
    # Generate report
    report = executor.generate_report()
    
    # Save report
    report_file = Path(sys.argv[2]) / 'cleanup_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Summary:")
    print(f"  Deleted: {report['summary']['total_deleted']}")
    print(f"  Failed: {report['summary']['total_failed']}")
    print(f"\n📄 Report saved to: {report_file}")

