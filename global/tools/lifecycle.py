#!/usr/bin/env python3
"""
Lifecycle Maestro - The ONLY entry point for project lifecycle management.
Based on Global Professional Core Prompt v33.2 (The Adoption Edition)

Usage:
    python3 global/tools/lifecycle.py "<Project Name>" "<Description>"

This tool:
    1. Auto-detects if this is a New Project (Genesis) or Existing Project (Adoption)
    2. Generates Constitution, Plan, and Tasks
    3. Initializes the Librarian file registry
    4. Creates .spec.md files for implementation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Project root detection
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def detect_project_mode() -> str:
    """
    Detect if this is a new project (Genesis) or existing project (Adoption).
    
    Returns:
        'genesis' for new projects
        'adoption' for existing projects
    """
    indicators = [
        PROJECT_ROOT / 'backend' / 'app.py',
        PROJECT_ROOT / 'frontend' / 'package.json',
        PROJECT_ROOT / 'docs' / 'TODO.md',
        PROJECT_ROOT / '.memory' / 'file_registry.json',
    ]
    
    existing_count = sum(1 for f in indicators if f.exists())
    
    if existing_count >= 2:
        return 'adoption'
    return 'genesis'


def load_file_registry() -> dict:
    """Load the file registry from .memory/file_registry.json."""
    registry_path = PROJECT_ROOT / '.memory' / 'file_registry.json'
    
    if registry_path.exists():
        with open(registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {
        '_metadata': {
            'version': '1.0.0',
            'created': get_timestamp(),
            'project': '',
            'description': ''
        },
        'directories': {},
        'files': {},
        'rules': {
            'never_delete': [],
            'always_update': [],
            'verify_before_create': True
        },
        'spec_files': {},
        'audit_log': []
    }


def save_file_registry(registry: dict) -> None:
    """Save the file registry to .memory/file_registry.json."""
    registry_path = PROJECT_ROOT / '.memory' / 'file_registry.json'
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    print(f"✅ File registry saved to {registry_path}")


def scan_project_structure() -> dict:
    """Scan the project structure and return directory/file information."""
    structure = {
        'directories': [],
        'files': [],
        'stats': {
            'total_dirs': 0,
            'total_files': 0,
            'by_extension': {}
        }
    }
    
    ignore_patterns = {
        '.git', '__pycache__', 'node_modules', '.venv', 'venv',
        'dist', 'build', '.next', '.cache', 'htmlcov', '.pytest_cache'
    }
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_patterns]
        
        rel_path = Path(root).relative_to(PROJECT_ROOT)
        structure['directories'].append(str(rel_path))
        structure['stats']['total_dirs'] += 1
        
        for file in files:
            file_path = Path(root) / file
            rel_file_path = file_path.relative_to(PROJECT_ROOT)
            structure['files'].append(str(rel_file_path))
            structure['stats']['total_files'] += 1
            
            # Count by extension
            ext = file_path.suffix.lower() or 'no_extension'
            structure['stats']['by_extension'][ext] = \
                structure['stats']['by_extension'].get(ext, 0) + 1
    
    return structure


def generate_constitution(project_name: str, description: str, mode: str) -> str:
    """Generate the project constitution document."""
    constitution = f"""# Project Constitution
## {project_name}

**Generated:** {get_timestamp()}
**Mode:** {mode.upper()}
**Description:** {description}

---

## 1. Project Identity

- **Name:** {project_name}
- **Type:** Store Management System (Inventory & ERP)
- **Status:** {'Active Development (Adoption)' if mode == 'adoption' else 'New Project (Genesis)'}

---

## 2. Core Principles

### 2.1 Code Quality
- Clean code over clever code
- Simple over complex
- Explicit over implicit
- Tested over untested

### 2.2 Architecture
- Separation of concerns
- Single responsibility
- DRY (Don't Repeat Yourself)
- SOLID principles

### 2.3 Security
- Defense in depth
- Principle of least privilege
- Input validation everywhere
- Secure by default

---

## 3. Technology Stack

### Backend
- Python 3.x with Flask
- SQLAlchemy ORM
- JWT Authentication
- PostgreSQL/SQLite database

### Frontend
- React with Vite
- TailwindCSS
- Radix UI / shadcn/ui components
- RTL support (Arabic)

### DevOps
- Docker & Docker Compose
- GitHub Actions CI/CD
- Nginx reverse proxy

---

## 4. Critical Rules

1. **Never delete from TODO.md** - Only mark with [x]
2. **Verify before create** - Check file registry first
3. **Use absolute paths** - No relative path confusion
4. **Atomic updates** - Documentation with code
5. **Respect legacy** - Don't delete existing without authorization

---

## 5. Success Criteria

- Minimum 95% project completion
- Zero critical security vulnerabilities
- 80%+ test coverage
- All P0 tasks complete

---

**This Constitution is the supreme law of this project.**
"""
    return constitution


def generate_plan(project_name: str, mode: str, structure: dict) -> str:
    """Generate the project plan document."""
    plan = f"""# Project Plan
## {project_name}

**Generated:** {get_timestamp()}
**Mode:** {mode.upper()}

---

## Current State Analysis

- **Total Directories:** {structure['stats']['total_dirs']}
- **Total Files:** {structure['stats']['total_files']}
- **Top Extensions:**
"""
    
    # Add top 10 extensions
    sorted_ext = sorted(
        structure['stats']['by_extension'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    for ext, count in sorted_ext:
        plan += f"  - {ext}: {count} files\n"
    
    plan += f"""
---

## Phase Plan

### Phase 1: Initialization & Analysis ✅
- [x] Detect project mode ({mode})
- [x] Initialize file registry
- [x] Scan project structure
- [x] Generate constitution

### Phase 2: Planning
- [ ] Review existing TODO.md
- [ ] Identify gaps and missing components
- [ ] Update task list with priorities

### Phase 3: Implementation
- [ ] Complete P0 (Critical) tasks
- [ ] Complete P1 (High Priority) tasks
- [ ] Complete P2 (Medium Priority) tasks

### Phase 4: Quality Assurance
- [ ] Run all tests
- [ ] Security audit
- [ ] Performance optimization

### Phase 5: Documentation
- [ ] Update all documentation
- [ ] Create deployment guide
- [ ] Final verification

---

## Next Steps

1. Read `docs/TODO.md` for current task status
2. Check `docs/INCOMPLETE_TASKS.md` for remaining work
3. Use `global/tools/librarian.py` to manage files
4. Create `.spec.md` files before implementation

---

**Remember:** Think before you act. Plan before you code.
"""
    return plan


def initialize_lifecycle(project_name: str, description: str) -> None:
    """Main lifecycle initialization function."""
    print("=" * 60)
    print("🚀 LIFECYCLE MAESTRO - Initializing...")
    print("=" * 60)
    
    # Step 1: Detect mode
    mode = detect_project_mode()
    print(f"\n📋 Project Mode: {mode.upper()}")
    
    # Step 2: Scan project structure
    print("\n🔍 Scanning project structure...")
    structure = scan_project_structure()
    print(f"   Found {structure['stats']['total_dirs']} directories")
    print(f"   Found {structure['stats']['total_files']} files")
    
    # Step 3: Load/update file registry
    print("\n📚 Updating file registry...")
    registry = load_file_registry()
    registry['_metadata']['project'] = project_name
    registry['_metadata']['description'] = description
    registry['_metadata']['updated'] = get_timestamp()
    
    # Add audit log entry
    registry['audit_log'].append({
        'timestamp': get_timestamp(),
        'action': 'lifecycle_init',
        'mode': mode,
        'description': f'Lifecycle initialized for {project_name}'
    })
    
    save_file_registry(registry)
    
    # Step 4: Generate constitution
    print("\n📜 Generating constitution...")
    constitution = generate_constitution(project_name, description, mode)
    constitution_path = PROJECT_ROOT / 'docs' / 'CONSTITUTION.md'
    constitution_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(constitution_path, 'w', encoding='utf-8') as f:
        f.write(constitution)
    print(f"   Saved to {constitution_path}")
    
    # Step 5: Generate plan
    print("\n📝 Generating plan...")
    plan = generate_plan(project_name, mode, structure)
    plan_path = PROJECT_ROOT / 'docs' / 'PROJECT_PLAN.md'
    
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(plan)
    print(f"   Saved to {plan_path}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ LIFECYCLE INITIALIZATION COMPLETE")
    print("=" * 60)
    print(f"""
Next Steps:
1. Read docs/CONSTITUTION.md for project principles
2. Read docs/PROJECT_PLAN.md for execution plan
3. Check docs/TODO.md for current tasks
4. Use global/tools/librarian.py to manage files
5. Create .spec.md files before writing implementation code
""")


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python3 lifecycle.py \"<Project Name>\" \"<Description>\"")
        print("Example: python3 lifecycle.py \"Store ERP\" \"Inventory management system\"")
        sys.exit(1)
    
    project_name = sys.argv[1]
    description = sys.argv[2]
    
    initialize_lifecycle(project_name, description)


if __name__ == '__main__':
    main()
