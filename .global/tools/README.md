# Advanced Development Tools

This directory contains powerful tools for managing code quality, detecting duplication, and maintaining a clean codebase.

## 🛠️ Tools Overview

### 1. analyze_dependencies.py
**Comprehensive Dependency Analysis Tool**

Scans the entire project and generates a detailed dependency table.

**Features:**
- Extracts all imports from Python files
- Builds dependency graph
- Detects circular dependencies
- Generates Markdown and JSON reports

**Usage:**
```bash
python tools/analyze_dependencies.py . docs/Dependencies_Report.md
```

**Output:**
- `docs/Dependencies_Report.md` - Human-readable report
- `docs/Dependencies_Report.json` - Machine-readable data

---

### 2. detect_code_duplication.py
**AST-Based Code Duplication Detector**

Detects duplicate code by analyzing the Abstract Syntax Tree (AST), not just names.

**Features:**
- Semantic code comparison
- Configurable similarity threshold (default 80%)
- Detects exact and similar duplicates
- Generates detailed reports

**Usage:**
```bash
# Scan entire project
python tools/detect_code_duplication.py . docs/Duplication_Report.md

# Custom threshold (90%)
python tools/detect_code_duplication.py . docs/Duplication_Report.md --threshold 0.9
```

**Output:**
- `docs/Duplication_Report.md` - Human-readable report
- `docs/Duplication_Report.json` - Machine-readable data for smart_merge.py

---

### 3. smart_merge.py
**Intelligent Code Merge Tool**

Automatically merges duplicate code blocks detected by `detect_code_duplication.py`.

**Features:**
- Automatic backup before merge
- Dry-run mode for safety
- Smart merge strategies
- Updates all imports automatically
- Rollback capability

**Usage:**
```bash
# Dry run (no changes)
python tools/smart_merge.py docs/Duplication_Report.json --dry-run

# Execute merge
python tools/smart_merge.py docs/Duplication_Report.json

# Custom backup directory
python tools/smart_merge.py docs/Duplication_Report.json --backup-dir ./my_backups
```

**Workflow:**
1. Run `detect_code_duplication.py` to find duplicates
2. Review `Duplication_Report.json`
3. Run `smart_merge.py` with `--dry-run` to preview
4. Run `smart_merge.py` to execute merge
5. Run tests to verify: `pytest tests/`
6. If issues, rollback using backup

---

### 4. update_imports.py
**Import Statement Update Tool**

Updates import statements across the entire project when modules are moved, renamed, or merged.

**Features:**
- AST-based import detection
- Supports all import styles (import, from...import, as)
- Circular dependency detection
- Dry-run mode
- Comprehensive reporting

**Usage:**
```bash
# Rename module
python tools/update_imports.py models.user models.user_unified

# Move module
python tools/update_imports.py utils.helpers core.utils.helpers

# Dry run
python tools/update_imports.py models.old models.new --dry-run

# Custom project root
python tools/update_imports.py models.old models.new --project-root /path/to/project
```

**Output:**
- `docs/Import_Update_Report.md` - Comprehensive report with dependency graph

---

## 📋 Recommended Workflow

### Initial Setup
```bash
# 1. Analyze dependencies
python tools/analyze_dependencies.py . docs/Dependencies_Report.md

# 2. Detect duplications
python tools/detect_code_duplication.py . docs/Duplication_Report.md
```

### Code Cleanup
```bash
# 3. Preview merge (dry run)
python tools/smart_merge.py docs/Duplication_Report.json --dry-run

# 4. Execute merge
python tools/smart_merge.py docs/Duplication_Report.json

# 5. Run tests
pytest tests/

# 6. If OK, commit; if not, rollback
```

### Module Refactoring
```bash
# 7. Update imports after renaming/moving modules
python tools/update_imports.py old.module new.module --dry-run
python tools/update_imports.py old.module new.module

# 8. Re-analyze dependencies
python tools/analyze_dependencies.py . docs/Dependencies_Report.md
```

---

## ⚠️ Important Notes

1. **Always backup before using smart_merge.py** (automatic, but verify)
2. **Always run tests after merging** to ensure nothing broke
3. **Use --dry-run first** to preview changes
4. **Review reports carefully** before taking action
5. **Circular dependencies** should be resolved manually

---

## 📊 Reports Generated

All tools generate reports in `docs/`:

- `Dependencies_Report.md` - Dependency analysis
- `Dependencies_Report.json` - Dependency data
- `Duplication_Report.md` - Duplication analysis
- `Duplication_Report.json` - Duplication data
- `Merge_Report.json` - Merge operations log
- `Import_Update_Report.md` - Import update log

---

## 🔧 Requirements

All tools require Python 3.7+ and use only standard library modules:
- `ast` - Abstract Syntax Tree parsing
- `pathlib` - Path operations
- `json` - JSON handling
- `dataclasses` - Data structures

No external dependencies needed!

---

## 📝 License

Part of the Gaara ERP Global Guidelines project.
