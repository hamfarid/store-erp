# PATH AND IMPORT TRACING PROMPT

**FILE**: github/global/prompts/13_path_and_import_tracing.md | **PURPOSE**: Analyze and fix all paths and imports | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Overview

This prompt guides you through analyzing and fixing all file paths, imports, and module references in the codebase.

## Why This Matters

Broken imports and incorrect paths are the #1 cause of runtime errors. This systematic approach ensures:
- All imports resolve correctly
- All file paths are valid
- All module references are accurate
- No circular dependencies exist

## Pre-Execution Checklist

- [ ] Memory system is active
- [ ] Logging is configured
- [ ] Project structure is known
- [ ] Language/framework identified

## Step 1: Identify Import System

Determine the import system used:

### JavaScript/TypeScript
- ES6 modules: `import { X } from './path'`
- CommonJS: `const X = require('./path')`
- Path aliases: `@/components/Button`

### Python
- Absolute imports: `from package.module import Class`
- Relative imports: `from .module import Class`
- Package imports: `import package`

### Other Languages
- Go: `import "github.com/user/repo/package"`
- Rust: `use crate::module::Item;`
- Java: `import com.example.package.Class;`

## Step 2: Map All Files

Create a complete file map:

```bash
# List all source files
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.venv/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*"
```

## Step 3: Extract All Imports

For each file, extract all import statements:

### Python Example
```python
import re
import ast

def extract_imports(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    'type': 'import',
                    'module': alias.name,
                    'line': node.lineno
                })
        elif isinstance(node, ast.ImportFrom):
            imports.append({
                'type': 'from',
                'module': node.module,
                'names': [alias.name for alias in node.names],
                'level': node.level,  # For relative imports
                'line': node.lineno
            })
    
    return imports
```

### TypeScript Example
```typescript
import * as ts from 'typescript';

function extractImports(filePath: string) {
    const sourceFile = ts.createSourceFile(
        filePath,
        fs.readFileSync(filePath, 'utf8'),
        ts.ScriptTarget.Latest,
        true
    );
    
    const imports: any[] = [];
    
    function visit(node: ts.Node) {
        if (ts.isImportDeclaration(node)) {
            imports.push({
                type: 'import',
                module: (node.moduleSpecifier as ts.StringLiteral).text,
                line: sourceFile.getLineAndCharacterOfPosition(node.getStart()).line
            });
        }
        ts.forEachChild(node, visit);
    }
    
    visit(sourceFile);
    return imports;
}
```

## Step 4: Verify Each Import

For each import, verify:

1. **File Exists**: Does the imported file exist?
2. **Export Exists**: Does the file export the imported symbol?
3. **Path Correct**: Is the relative/absolute path correct?
4. **Extension**: Is the file extension correct (or omitted correctly)?

### Verification Script (Python)

```python
import os
from pathlib import Path

def verify_import(file_path, import_info):
    """Verify a single import statement"""
    
    # Get the directory of the importing file
    file_dir = Path(file_path).parent
    
    # Handle relative imports
    if import_info['type'] == 'from' and import_info['level'] > 0:
        # Go up 'level' directories
        target_dir = file_dir
        for _ in range(import_info['level']):
            target_dir = target_dir.parent
        
        # Construct the module path
        module_parts = import_info['module'].split('.') if import_info['module'] else []
        target_path = target_dir / '/'.join(module_parts)
    else:
        # Absolute import - search in sys.path or project root
        module_parts = import_info['module'].split('.')
        # Try to find in project
        target_path = Path('.') / '/'.join(module_parts)
    
    # Check if file exists (try .py, __init__.py)
    possible_paths = [
        target_path.with_suffix('.py'),
        target_path / '__init__.py'
    ]
    
    for path in possible_paths:
        if path.exists():
            return {
                'valid': True,
                'resolved_path': str(path)
            }
    
    return {
        'valid': False,
        'error': f"Module not found: {import_info['module']}",
        'file': file_path,
        'line': import_info['line']
    }
```

## Step 5: Detect Circular Dependencies

Create a dependency graph and detect cycles:

```python
from collections import defaultdict

def build_dependency_graph(all_imports):
    """Build a directed graph of dependencies"""
    graph = defaultdict(set)
    
    for file_path, imports in all_imports.items():
        for imp in imports:
            if imp['resolved_path']:
                graph[file_path].add(imp['resolved_path'])
    
    return graph

def detect_cycles(graph):
    """Detect circular dependencies using DFS"""
    visited = set()
    rec_stack = set()
    cycles = []
    
    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path.copy())
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
        
        rec_stack.remove(node)
    
    for node in graph:
        if node not in visited:
            dfs(node, [])
    
    return cycles
```

## Step 6: Generate Report

Create `docs/IMPORT_ANALYSIS.md`:

```markdown
# Import Analysis Report

**Generated**: [Date]

## Summary

- **Total Files**: [Count]
- **Total Imports**: [Count]
- **Valid Imports**: [Count]
- **Broken Imports**: [Count]
- **Circular Dependencies**: [Count]

## Broken Imports

### Critical (P0)

1. **File**: `backend/services/auth.py`
   - **Line**: 5
   - **Import**: `from models.user import User`
   - **Error**: Module not found
   - **Fix**: Change to `from backend.models.user import User`

[Repeat for all broken imports]

## Circular Dependencies

### Cycle 1
```
backend/models/user.py
  → backend/services/auth.py
  → backend/models/session.py
  → backend/models/user.py
```

**Recommendation**: Extract shared types to a separate file

[Repeat for all cycles]

## Path Aliases

### Configured Aliases
- `@/` → `src/`
- `@components/` → `src/components/`
- `@utils/` → `src/utils/`

### Usage
- [File] uses [@/components/Button]

## Recommendations

1. **Fix all broken imports** (P0)
2. **Resolve circular dependencies** (P0)
3. **Standardize import style** (P1)
4. **Use path aliases consistently** (P2)

---

**Next Steps**: Fix all P0 issues before proceeding
```

## Step 7: Auto-Fix Imports

For each broken import, attempt to auto-fix:

```python
def fix_import(file_path, import_info, correct_path):
    """Automatically fix a broken import"""
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Replace the broken import line
    old_line = lines[import_info['line'] - 1]
    new_line = old_line.replace(import_info['module'], correct_path)
    lines[import_info['line'] - 1] = new_line
    
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"Fixed import in {file_path}:{import_info['line']}")
```

## Step 8: Verify Fixes

After fixing, run the verification again to ensure all imports are valid.

## Step 9: Log Actions

Log all fixes to `logs/info.log`

## Step 10: Save to Memory

Save the analysis report to `.memory/learnings/import_analysis_[date].md`

---

**Completion Criteria**:
- [ ] All files scanned
- [ ] All imports extracted
- [ ] All imports verified
- [ ] Broken imports identified
- [ ] Circular dependencies detected
- [ ] Report generated
- [ ] Auto-fixes applied (where possible)
- [ ] Verification re-run
- [ ] Actions logged

