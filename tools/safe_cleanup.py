#!/usr/bin/env python3
"""
Safe Cleanup Tool - Moves unused files to unneeded/ directory
"""
import json
import os
import shutil
from pathlib import Path
import sys

def move_to_unneeded(file_path, base_dir, unneeded_dir):
    """Move a file to the unneeded directory, preserving structure"""
    try:
        # Get relative path from base_dir
        rel_path = os.path.relpath(file_path, base_dir)
        
        # Create destination path
        dest_path = os.path.join(unneeded_dir, rel_path)
        dest_dir = os.path.dirname(dest_path)
        
        # Create destination directory if it doesn't exist
        os.makedirs(dest_dir, exist_ok=True)
        
        # Move the file
        shutil.move(file_path, dest_path)
        return True, dest_path
    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) < 3:
        print("Usage: python safe_cleanup.py <analysis_file> <base_dir> [--execute]")
        print("Example: python safe_cleanup.py backend_analysis_new.json backend --execute")
        sys.exit(1)
    
    analysis_file = sys.argv[1]
    base_dir = sys.argv[2]
    execute = "--execute" in sys.argv
    
    # Load analysis
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    unused_files = analysis.get('unused_files', [])
    
    print(f"\n{'='*60}")
    print(f"SAFE CLEANUP TOOL")
    print(f"{'='*60}")
    print(f"Base directory: {base_dir}")
    print(f"Unused files: {len(unused_files)}")
    print(f"Mode: {'EXECUTE' if execute else 'DRY RUN'}")
    print(f"{'='*60}\n")
    
    if not execute:
        print("🔍 DRY RUN - No files will be moved")
        print("\nFiles that would be moved to unneeded/:\n")
        for file in unused_files[:20]:  # Show first 20
            print(f"  - {file}")
        if len(unused_files) > 20:
            print(f"  ... and {len(unused_files) - 20} more files")
        print(f"\nTo execute, run with --execute flag")
        return
    
    # Execute mode
    unneeded_dir = os.path.join(base_dir, 'unneeded')
    os.makedirs(unneeded_dir, exist_ok=True)
    
    moved = 0
    failed = 0
    errors = []
    
    print("🗂️  Moving files to unneeded/...\n")
    
    for file in unused_files:
        file_path = os.path.join(base_dir, file)
        
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file}")
            failed += 1
            errors.append(f"Not found: {file}")
            continue
        
        success, result = move_to_unneeded(file_path, base_dir, unneeded_dir)
        
        if success:
            print(f"✅ Moved: {file}")
            moved += 1
        else:
            print(f"❌ Failed: {file} - {result}")
            failed += 1
            errors.append(f"{file}: {result}")
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"Total files: {len(unused_files)}")
    print(f"Moved: {moved}")
    print(f"Failed: {failed}")
    print(f"{'='*60}\n")
    
    if errors:
        print("❌ Errors:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    # Save report
    report = {
        'total': len(unused_files),
        'moved': moved,
        'failed': failed,
        'errors': errors
    }
    
    report_file = f"{base_dir}_cleanup_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Report saved to: {report_file}")

if __name__ == '__main__':
    main()

