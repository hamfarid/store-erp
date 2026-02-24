#!/usr/bin/env python3
"""
Librarian - File Registry Manager
Based on Global Professional Core Prompt v33.2

This tool manages the .memory/file_registry.json and provides:
1. File existence checks (verify before create)
2. File registration
3. File search capabilities
4. Audit logging

Usage:
    python3 global/tools/librarian.py check <file_path>
    python3 global/tools/librarian.py register <file_path> <purpose>
    python3 global/tools/librarian.py search <pattern>
    python3 global/tools/librarian.py list
    python3 global/tools/librarian.py audit
"""

import json
import os
import sys
import fnmatch
from datetime import datetime
from pathlib import Path
from typing import Optional

# Project root detection
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
REGISTRY_PATH = PROJECT_ROOT / '.memory' / 'file_registry.json'


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def load_registry() -> dict:
    """Load the file registry."""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Create initial registry if doesn't exist
    return {
        '_metadata': {
            'version': '1.0.0',
            'created': get_timestamp(),
            'updated': get_timestamp(),
            'project': 'Store Management System'
        },
        'directories': {},
        'files': {
            'core': {},
            'configuration': {},
            'documentation': {},
            'memory': {}
        },
        'rules': {
            'never_delete': [
                'docs/TODO.md',
                'docs/COMPLETE_TASKS.md',
                'docs/INCOMPLETE_TASKS.md'
            ],
            'always_update': [],
            'verify_before_create': True
        },
        'spec_files': {},
        'audit_log': []
    }


def save_registry(registry: dict) -> None:
    """Save the file registry."""
    registry['_metadata']['updated'] = get_timestamp()
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def check_file(file_path: str) -> bool:
    """
    Check if a file exists in the project and registry.
    Returns True if file exists, False otherwise.
    """
    registry = load_registry()
    
    # Normalize path
    if os.path.isabs(file_path):
        abs_path = Path(file_path)
        try:
            rel_path = abs_path.relative_to(PROJECT_ROOT)
        except ValueError:
            rel_path = abs_path
    else:
        rel_path = Path(file_path)
        abs_path = PROJECT_ROOT / rel_path
    
    rel_path_str = str(rel_path).replace('\\', '/')
    
    # Check physical existence
    physical_exists = abs_path.exists()
    
    # Check registry
    registry_exists = False
    for category in registry.get('files', {}).values():
        if isinstance(category, dict) and rel_path_str in category:
            registry_exists = True
            break
    
    print(f"📁 File: {rel_path_str}")
    print(f"   Physical: {'✅ EXISTS' if physical_exists else '❌ NOT FOUND'}")
    print(f"   Registry: {'✅ REGISTERED' if registry_exists else '⚠️ NOT REGISTERED'}")
    
    return physical_exists


def register_file(file_path: str, purpose: str, category: str = 'core') -> None:
    """Register a file in the registry."""
    registry = load_registry()
    
    # Normalize path
    if os.path.isabs(file_path):
        abs_path = Path(file_path)
        try:
            rel_path = abs_path.relative_to(PROJECT_ROOT)
        except ValueError:
            rel_path = abs_path
    else:
        rel_path = Path(file_path)
        abs_path = PROJECT_ROOT / rel_path
    
    rel_path_str = str(rel_path).replace('\\', '/')
    
    # Determine file type from extension
    ext = abs_path.suffix.lower()
    type_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'jsx',
        '.ts': 'typescript',
        '.tsx': 'tsx',
        '.json': 'json',
        '.md': 'markdown',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.sql': 'sql',
        '.css': 'css',
        '.html': 'html'
    }
    file_type = type_map.get(ext, 'unknown')
    
    # Ensure category exists
    if category not in registry['files']:
        registry['files'][category] = {}
    
    # Register file
    registry['files'][category][rel_path_str] = {
        'type': file_type,
        'purpose': purpose,
        'status': 'active',
        'registered': get_timestamp()
    }
    
    # Add audit log
    registry['audit_log'].append({
        'timestamp': get_timestamp(),
        'action': 'file_registered',
        'file': rel_path_str,
        'purpose': purpose
    })
    
    save_registry(registry)
    print(f"✅ Registered: {rel_path_str}")
    print(f"   Category: {category}")
    print(f"   Type: {file_type}")
    print(f"   Purpose: {purpose}")


def search_files(pattern: str) -> list:
    """Search for files matching a pattern."""
    registry = load_registry()
    matches = []
    
    for category, files in registry.get('files', {}).items():
        if isinstance(files, dict):
            for file_path, info in files.items():
                if fnmatch.fnmatch(file_path.lower(), f'*{pattern.lower()}*'):
                    matches.append({
                        'path': file_path,
                        'category': category,
                        'info': info
                    })
    
    print(f"🔍 Search: *{pattern}*")
    print(f"   Found: {len(matches)} files")
    
    for match in matches:
        print(f"\n   📄 {match['path']}")
        print(f"      Category: {match['category']}")
        print(f"      Purpose: {match['info'].get('purpose', 'N/A')}")
    
    return matches


def list_files() -> None:
    """List all registered files."""
    registry = load_registry()
    
    print("📚 File Registry Contents")
    print("=" * 60)
    
    total = 0
    for category, files in registry.get('files', {}).items():
        if isinstance(files, dict) and files:
            print(f"\n📁 {category.upper()}")
            for file_path, info in files.items():
                print(f"   • {file_path}")
                if isinstance(info, dict):
                    print(f"     Purpose: {info.get('purpose', 'N/A')}")
                total += 1
    
    print(f"\n{'=' * 60}")
    print(f"Total registered files: {total}")


def show_audit_log(limit: int = 20) -> None:
    """Show recent audit log entries."""
    registry = load_registry()
    audit_log = registry.get('audit_log', [])
    
    print("📋 Audit Log (Recent)")
    print("=" * 60)
    
    for entry in audit_log[-limit:]:
        print(f"\n⏰ {entry.get('timestamp', 'N/A')}")
        print(f"   Action: {entry.get('action', 'N/A')}")
        if 'file' in entry:
            print(f"   File: {entry['file']}")
        if 'description' in entry:
            print(f"   Description: {entry['description']}")


def verify_oath() -> None:
    """Display the Anti-Hallucination Verification Oath."""
    oath = """
╔══════════════════════════════════════════════════════════════╗
║              VERIFICATION OATH (Anti-Hallucination)          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Before every import or file reference, I swear to:          ║
║                                                              ║
║  1. CHECK if the file exists in the file registry            ║
║  2. VERIFY the file exists on disk                           ║
║  3. READ the file to understand its contents                 ║
║  4. NEVER assume a file exists without verification          ║
║  5. NEVER hallucinate imports or file paths                  ║
║                                                              ║
║  I will use: librarian.py check <file_path>                  ║
║  Before every implementation.                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(oath)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 librarian.py check <file_path>")
        print("  python3 librarian.py register <file_path> <purpose> [category]")
        print("  python3 librarian.py search <pattern>")
        print("  python3 librarian.py list")
        print("  python3 librarian.py audit")
        print("  python3 librarian.py oath")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'check' and len(sys.argv) >= 3:
        check_file(sys.argv[2])
    
    elif command == 'register' and len(sys.argv) >= 4:
        category = sys.argv[4] if len(sys.argv) >= 5 else 'core'
        register_file(sys.argv[2], sys.argv[3], category)
    
    elif command == 'search' and len(sys.argv) >= 3:
        search_files(sys.argv[2])
    
    elif command == 'list':
        list_files()
    
    elif command == 'audit':
        show_audit_log()
    
    elif command == 'oath':
        verify_oath()
    
    else:
        print(f"Unknown command or missing arguments: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
