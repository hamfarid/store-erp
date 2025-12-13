#!/usr/bin/env python3
"""
Path & Import Tracing and Correction Tool

This script analyzes a project's codebase, identifies broken paths and imports,
and automatically corrects them.

Usage:
    python3 fix_paths.py --project-root /path/to/project
"""

import os
import re
import json
import argparse
from pathlib import Path


def get_project_structure(root):
    """Generate a tree structure of the project."""
    structure = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
        
        level = dirpath.replace(root, '').count(os.sep)
        indent = '  ' * level
        structure.append(f"{indent}{os.path.basename(dirpath)}/")
        
        sub_indent = '  ' * (level + 1)
        for filename in filenames:
            structure.append(f"{sub_indent}{filename}")
    
    return '\n'.join(structure)


def extract_paths(root):
    """Extract all paths and imports from the project."""
    results = []
    
    # File extensions to scan
    extensions = ['.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.html', '.json', '.vue']
    
    # Patterns to match
    patterns = [
        (r'import\s+.*?\s+from\s+["\']([^"\']+)["\']', 'import'),
        (r'require\(["\']([^"\']+)["\']\)', 'require'),
        (r'src=["\']([^"\']+)["\']', 'src'),
        (r'href=["\']([^"\']+)["\']', 'href'),
        (r'url\(["\']?([^"\')\s]+)["\']?\)', 'url'),
    ]
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
        
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                filepath = os.path.join(dirpath, filename)
                relative_filepath = os.path.relpath(filepath, root)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    for line_num, line in enumerate(lines, 1):
                        for pattern, path_type in patterns:
                            matches = re.finditer(pattern, line)
                            for match in matches:
                                path = match.group(1)
                                
                                # Skip external URLs and data URIs
                                if path.startswith(('http://', 'https://', 'data:', '//')):
                                    continue
                                
                                results.append({
                                    'file': relative_filepath,
                                    'line': line_num,
                                    'path': path,
                                    'type': path_type
                                })
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
    
    return results


def validate_paths(root, paths):
    """Validate each extracted path."""
    for entry in paths:
        file_dir = os.path.dirname(os.path.join(root, entry['file']))
        path = entry['path']
        
        # Handle absolute paths from root
        if path.startswith('/'):
            resolved_path = os.path.join(root, path.lstrip('/'))
        else:
            resolved_path = os.path.normpath(os.path.join(file_dir, path))
        
        # Check if file exists (with or without extension)
        exists = False
        if os.path.exists(resolved_path):
            exists = True
        else:
            # Try adding common extensions
            for ext in ['', '.js', '.jsx', '.ts', '.tsx', '.json', '.css', '.scss']:
                if os.path.exists(resolved_path + ext):
                    resolved_path = resolved_path + ext
                    exists = True
                    break
        
        entry['resolved_path'] = resolved_path
        entry['status'] = 'ok' if exists else 'broken'
    
    return paths


def find_correct_path(root, broken_entry):
    """Find the correct path for a broken import."""
    filename = os.path.basename(broken_entry['path'])
    
    # Search for the file in the entire project
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
        
        for found_file in filenames:
            if found_file == filename or found_file.startswith(filename + '.'):
                found_path = os.path.join(dirpath, found_file)
                
                # Calculate relative path from the original file
                original_file_dir = os.path.dirname(os.path.join(root, broken_entry['file']))
                relative_path = os.path.relpath(found_path, original_file_dir)
                
                # Remove extension if original path didn't have one
                if not os.path.splitext(broken_entry['path'])[1]:
                    relative_path = os.path.splitext(relative_path)[0]
                
                return relative_path
    
    return None


def generate_corrections(root, paths):
    """Generate corrections for broken paths."""
    corrections = []
    
    for entry in paths:
        if entry['status'] == 'broken':
            new_path = find_correct_path(root, entry)
            
            if new_path:
                corrections.append({
                    'file': entry['file'],
                    'line': entry['line'],
                    'old_path': entry['path'],
                    'new_path': new_path,
                    'status': 'correction_proposed'
                })
            else:
                corrections.append({
                    'file': entry['file'],
                    'line': entry['line'],
                    'old_path': entry['path'],
                    'new_path': None,
                    'status': 'file_not_found'
                })
    
    return corrections


def apply_corrections(root, corrections):
    """Apply the proposed corrections to the files."""
    files_to_update = {}
    
    # Group corrections by file
    for correction in corrections:
        if correction['status'] == 'correction_proposed':
            filepath = os.path.join(root, correction['file'])
            if filepath not in files_to_update:
                files_to_update[filepath] = []
            files_to_update[filepath].append(correction)
    
    # Apply corrections file by file
    for filepath, file_corrections in files_to_update.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for correction in file_corrections:
            # Replace old path with new path
            content = content.replace(f'"{correction["old_path"]}"', f'"{correction["new_path"]}"')
            content = content.replace(f"'{correction['old_path']}'", f"'{correction['new_path']}'")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated: {os.path.relpath(filepath, root)}")


def main():
    parser = argparse.ArgumentParser(description='Fix broken paths and imports in a project')
    parser.add_argument('--project-root', required=True, help='Root directory of the project')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically apply fixes without confirmation')
    args = parser.parse_args()
    
    root = os.path.abspath(args.project_root)
    docs_dir = os.path.join(root, 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    print(f"🔍 Analyzing project at: {root}\n")
    
    # Phase 1: Analysis
    print("📁 Phase 1: Generating project structure...")
    structure = get_project_structure(root)
    with open(os.path.join(docs_dir, 'PROJECT_STRUCTURE.md'), 'w') as f:
        f.write(f"# Project Structure\n\n```\n{structure}\n```\n")
    print(f"✅ Created: docs/PROJECT_STRUCTURE.md\n")
    
    print("🔍 Extracting all paths and imports...")
    paths = extract_paths(root)
    print(f"✅ Found {len(paths)} paths/imports\n")
    
    print("✔️  Validating paths...")
    paths = validate_paths(root, paths)
    broken_count = sum(1 for p in paths if p['status'] == 'broken')
    print(f"✅ Validation complete: {broken_count} broken paths found\n")
    
    with open(os.path.join(docs_dir, 'Path_Analysis.json'), 'w') as f:
        json.dump(paths, f, indent=2)
    print(f"✅ Created: docs/Path_Analysis.json\n")
    
    if broken_count == 0:
        print("🎉 No broken paths found! Project is clean.")
        return
    
    # Phase 2: Correction
    print("🔧 Phase 2: Generating corrections...")
    corrections = generate_corrections(root, paths)
    
    with open(os.path.join(docs_dir, 'Path_Corrections.json'), 'w') as f:
        json.dump(corrections, f, indent=2)
    print(f"✅ Created: docs/Path_Corrections.json\n")
    
    fixable = sum(1 for c in corrections if c['status'] == 'correction_proposed')
    unfixable = sum(1 for c in corrections if c['status'] == 'file_not_found')
    
    print(f"📊 Summary:")
    print(f"   - Fixable: {fixable}")
    print(f"   - Unfixable (file not found): {unfixable}\n")
    
    if fixable > 0:
        if not args.auto_fix:
            confirm = input(f"Apply {fixable} corrections? (yes/no): ")
            if confirm.lower() != 'yes':
                print("❌ Corrections not applied.")
                return
        
        print("\n🔧 Applying corrections...")
        apply_corrections(root, corrections)
        print(f"\n✅ {fixable} corrections applied!\n")
        
        # Phase 3: Verification
        print("🔍 Phase 3: Re-running analysis for verification...")
        paths = extract_paths(root)
        paths = validate_paths(root, paths)
        broken_count = sum(1 for p in paths if p['status'] == 'broken')
        
        with open(os.path.join(docs_dir, 'Path_Analysis_After_Fix.json'), 'w') as f:
            json.dump(paths, f, indent=2)
        
        print(f"✅ Verification complete: {broken_count} broken paths remaining\n")
        
        if broken_count == 0:
            print("🎉 All paths fixed successfully!")
        else:
            print(f"⚠️  {broken_count} paths could not be fixed automatically.")
            print("   Review docs/Path_Analysis_After_Fix.json for details.")


if __name__ == '__main__':
    main()

