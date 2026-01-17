#!/usr/bin/env python3
"""
Speckit Bridge - GitHub Tool Wrapper for Spec Files
Based on Global Professional Core Prompt v33.2

This tool creates and manages .spec.md files for implementation:
1. Create spec files before writing code
2. Validate implementations against specs
3. Track spec file status

Usage:
    python3 global/tools/speckit_bridge.py create <feature_name>
    python3 global/tools/speckit_bridge.py validate <spec_path>
    python3 global/tools/speckit_bridge.py list
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Project root detection
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
SPECS_DIR = PROJECT_ROOT / 'specs'


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def create_spec(feature_name: str, spec_type: str = 'feature') -> Path:
    """
    Create a new spec file for a feature.
    
    Args:
        feature_name: Name of the feature (e.g., 'user-authentication')
        spec_type: Type of spec ('feature', 'api', 'component', 'migration')
    
    Returns:
        Path to the created spec file
    """
    # Normalize feature name
    feature_slug = feature_name.lower().replace(' ', '-').replace('_', '-')
    
    # Determine spec directory
    type_dirs = {
        'feature': SPECS_DIR / 'features',
        'api': SPECS_DIR / 'api',
        'component': SPECS_DIR / 'components',
        'migration': SPECS_DIR / 'migrations'
    }
    
    spec_dir = type_dirs.get(spec_type, SPECS_DIR / 'features')
    spec_dir.mkdir(parents=True, exist_ok=True)
    
    spec_path = spec_dir / f'{feature_slug}.spec.md'
    
    # Generate spec template
    spec_content = f"""# Specification: {feature_name}

**Created:** {get_timestamp()}
**Type:** {spec_type}
**Status:** Draft
**Author:** AI Agent

---

## 1. Overview

### 1.1 Purpose
<!-- Describe what this feature/component does -->

### 1.2 Scope
<!-- Define what is in scope and out of scope -->

### 1.3 Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## 2. Requirements

### 2.1 Functional Requirements
| ID | Description | Priority |
|----|-------------|----------|
| FR-001 | | P0 |
| FR-002 | | P1 |

### 2.2 Non-Functional Requirements
| ID | Description | Metric |
|----|-------------|--------|
| NFR-001 | Performance | Response time < 200ms |
| NFR-002 | Security | No critical vulnerabilities |

---

## 3. Technical Design

### 3.1 Architecture
<!-- Describe the technical architecture -->

### 3.2 Data Model
<!-- Describe data structures and schemas -->

### 3.3 API Endpoints
<!-- List API endpoints if applicable -->

### 3.4 Dependencies
- Dependency 1
- Dependency 2

---

## 4. Implementation Plan

### 4.1 Files to Create/Modify
| File | Action | Description |
|------|--------|-------------|
| | Create | |
| | Modify | |

### 4.2 Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### 4.3 Estimated Effort
- Backend: X hours
- Frontend: X hours
- Testing: X hours
- Total: X hours

---

## 5. Testing Strategy

### 5.1 Unit Tests
- Test case 1
- Test case 2

### 5.2 Integration Tests
- Test case 1
- Test case 2

### 5.3 E2E Tests
- Test case 1

---

## 6. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| | | |

---

## 7. Checklist

- [ ] Spec reviewed and approved
- [ ] Implementation complete
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Deployed to staging
- [ ] Deployed to production

---

## 8. Change Log

| Date | Author | Description |
|------|--------|-------------|
| {get_timestamp()[:10]} | AI Agent | Initial spec created |

---

**Remember:** No code without spec. This spec must be completed before implementation begins.
"""
    
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ Spec created: {spec_path}")
    print(f"   Type: {spec_type}")
    print(f"   Feature: {feature_name}")
    
    # Update file registry
    update_registry_with_spec(spec_path, feature_name, spec_type)
    
    return spec_path


def update_registry_with_spec(spec_path: Path, feature_name: str, spec_type: str) -> None:
    """Update the file registry with the new spec file."""
    registry_path = PROJECT_ROOT / '.memory' / 'file_registry.json'
    
    if registry_path.exists():
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    else:
        registry = {'spec_files': {}}
    
    # Add spec to registry
    if spec_type not in registry.get('spec_files', {}):
        registry['spec_files'][spec_type] = []
    
    rel_path = str(spec_path.relative_to(PROJECT_ROOT)).replace('\\', '/')
    
    if rel_path not in registry['spec_files'][spec_type]:
        registry['spec_files'][spec_type].append(rel_path)
    
    # Save registry
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def validate_spec(spec_path: str) -> bool:
    """
    Validate that a spec file is complete.
    
    Returns True if valid, False otherwise.
    """
    path = Path(spec_path)
    
    if not path.exists():
        # Try relative to project root
        path = PROJECT_ROOT / spec_path
    
    if not path.exists():
        print(f"❌ Spec file not found: {spec_path}")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required sections
    required_sections = [
        '## 1. Overview',
        '## 2. Requirements',
        '## 3. Technical Design',
        '## 4. Implementation Plan',
        '## 5. Testing Strategy'
    ]
    
    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)
    
    # Check for placeholders
    has_placeholders = '<!-- ' in content and ' -->' in content
    
    # Check for unchecked items
    unchecked_count = content.count('- [ ]')
    checked_count = content.count('- [x]')
    
    print(f"📋 Spec Validation: {path.name}")
    print("=" * 50)
    
    if missing:
        print(f"❌ Missing sections:")
        for section in missing:
            print(f"   • {section}")
    else:
        print("✅ All required sections present")
    
    if has_placeholders:
        print("⚠️ Has unfilled placeholders (<!-- ... -->)")
    
    print(f"📊 Checklist: {checked_count}/{checked_count + unchecked_count} complete")
    
    is_valid = len(missing) == 0 and not has_placeholders
    print(f"\n{'✅ VALID' if is_valid else '❌ NEEDS WORK'}")
    
    return is_valid


def list_specs() -> None:
    """List all spec files in the project."""
    print("📚 Spec Files")
    print("=" * 50)
    
    if not SPECS_DIR.exists():
        print("No specs directory found. Create specs with:")
        print("  python3 speckit_bridge.py create <feature_name>")
        return
    
    total = 0
    for spec_type_dir in SPECS_DIR.iterdir():
        if spec_type_dir.is_dir():
            specs = list(spec_type_dir.glob('*.spec.md'))
            if specs:
                print(f"\n📁 {spec_type_dir.name.upper()}")
                for spec in specs:
                    print(f"   • {spec.name}")
                    total += 1
    
    # Also check root specs dir
    root_specs = list(SPECS_DIR.glob('*.spec.md'))
    if root_specs:
        print(f"\n📁 ROOT")
        for spec in root_specs:
            print(f"   • {spec.name}")
            total += 1
    
    print(f"\n{'=' * 50}")
    print(f"Total spec files: {total}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Speckit Bridge - Spec File Manager")
        print("=" * 50)
        print("\nUsage:")
        print("  python3 speckit_bridge.py create <feature_name> [type]")
        print("  python3 speckit_bridge.py validate <spec_path>")
        print("  python3 speckit_bridge.py list")
        print("\nTypes: feature, api, component, migration")
        print("\nExample:")
        print("  python3 speckit_bridge.py create user-authentication feature")
        print("  python3 speckit_bridge.py validate specs/features/user-auth.spec.md")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'create' and len(sys.argv) >= 3:
        feature_name = sys.argv[2]
        spec_type = sys.argv[3] if len(sys.argv) >= 4 else 'feature'
        create_spec(feature_name, spec_type)
    
    elif command == 'validate' and len(sys.argv) >= 3:
        validate_spec(sys.argv[2])
    
    elif command == 'list':
        list_specs()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
