=================================================================================
PROMPT 86: DUPLICATE FILES DETECTION & DEDUPLICATION
=================================================================================

**Version:** Latest  
**Type:** Code Quality & Optimization  
**Priority:** HIGH  
**Phase:** Maintenance (Phase 5)

**Objective:** Detect and merge duplicate/similar files to reduce code redundancy and improve maintainability.

---

## 🎯 PURPOSE

This prompt ensures that:
1. ✅ No duplicate files exist in the project
2. ✅ Similar files are detected and merged
3. ✅ Code redundancy is minimized
4. ✅ Project structure is clean and organized

**Benefits:**
- Reduced codebase size
- Easier maintenance
- Fewer bugs from inconsistent duplicates
- Better code organization

---

## 🛠️ AVAILABLE TOOLS

### Tool 1: Duplicate Files Detector

**File:** `.global/tools/duplicate_files_detector.py`

**Purpose:** Detect files with similar names or identical content

**Usage:**
```bash
python .global/tools/duplicate_files_detector.py /path/to/project
```

**Features:**
- Finds files with similar names (ignoring version numbers, "copy", etc.)
- Finds files with identical content (by hash)
- Excludes .md, .txt, .log files
- Generates JSON report

**Output:**
- Console report with all duplicate groups
- JSON file: `docs/duplicate_files_report.json`

---

### Tool 2: Code Deduplicator

**File:** `.global/tools/code_deduplicator.py`

**Purpose:** Deep code analysis and automatic file merging

**Usage:**
```bash
# Detect only (no merging)
python .global/tools/code_deduplicator.py /path/to/project

# Detect and auto-merge
python .global/tools/code_deduplicator.py /path/to/project --auto-merge

# Custom similarity threshold
python .global/tools/code_deduplicator.py /path/to/project --threshold 0.90
```

**Features:**
- Deep code similarity analysis
- Normalizes code (removes comments, whitespace, strings)
- Calculates similarity percentage
- Progress bar for each file
- Automatic merging with backup
- Keeps file with shortest path (usually the original)

**Parameters:**
- `--auto-merge`: Automatically merge duplicate files
- `--threshold`: Similarity threshold (0.0-1.0, default: 0.85)

**Output:**
- Console report with progress bar
- JSON file: `docs/deduplication_report.json`
- Backup directory: `.global/backups/duplicates/{timestamp}/`

---

## 📋 WORKFLOW

### Step 1: Initial Detection

**Run the detector first:**
```bash
cd /path/to/project
python ../.global/tools/duplicate_files_detector.py .
```

**Review the report:**
- Check `docs/duplicate_files_report.json`
- Identify groups of similar/duplicate files
- Decide which files to merge

---

### Step 2: Deep Analysis

**Run the deduplicator (detection only):**
```bash
python ../.global/tools/code_deduplicator.py . --threshold 0.85
```

**Review the results:**
- Check which files are similar (>85% similarity)
- Verify that files should actually be merged
- Look for false positives

---

### Step 3: Manual Review

**For each duplicate group:**

1. **Open all files in the group**
2. **Compare them manually**
3. **Check for differences:**
   - Are they truly duplicates?
   - Do they serve different purposes?
   - Is one more complete than the other?

4. **Decide:**
   - ✅ Merge if truly duplicate
   - ❌ Keep separate if different purposes
   - 🔄 Refactor if similar but not identical

---

### Step 4: Automatic Merging

**If confident, run auto-merge:**
```bash
python ../.global/tools/code_deduplicator.py . --auto-merge --threshold 0.95
```

**What happens:**
- Files with >95% similarity are merged
- The file with the shortest path is kept
- Other files are backed up to `.global/backups/duplicates/`
- Duplicate files are deleted
- Report is generated

---

### Step 5: Verification

**After merging:**

1. **Check the backup:**
   ```bash
   ls -la .global/backups/duplicates/
   ```

2. **Review the report:**
   ```bash
   cat docs/deduplication_report.json
   ```

3. **Test the project:**
   - Run tests
   - Build the project
   - Verify functionality

4. **Commit changes:**
   ```bash
   git add -A
   git commit -m "Remove duplicate files"
   git push
   ```

---

## 🚨 IMPORTANT RULES

### Files to NEVER Merge

**DO NOT merge these files even if similar:**
- Configuration files (`.env`, `config.js`, etc.)
- Test files (even if testing similar functionality)
- Migration files (each migration is unique)
- API route files (even if similar structure)
- Component files with similar structure but different data

### Safe to Merge

**These are usually safe to merge:**
- Exact duplicates (100% identical)
- Copy files (file_copy.js, file (1).js, etc.)
- Old versions (file_v1.js, file_old.js, etc.)
- Backup files (file_backup.js, file.bak, etc.)

---

## 📊 EXAMPLE SCENARIOS

### Scenario 1: Exact Duplicates

**Found:**
```
Group: UserController
  - backend/controllers/UserController.js
  - backend/controllers/UserController_copy.js
  - backend/controllers/UserController_backup.js
```

**Action:**
✅ Safe to merge - Keep `UserController.js`, remove others

---

### Scenario 2: Version Files

**Found:**
```
Group: api
  - services/api_v1.js
  - services/api_v2.js
  - services/api_latest.js
```

**Action:**
⚠️ Manual review needed - Check if all versions are still used

---

### Scenario 3: Similar Structure

**Found:**
```
Group: ProductController
  - controllers/ProductController.js (95% similar)
  - controllers/CategoryController.js (95% similar)
```

**Action:**
❌ DO NOT merge - Similar structure but different entities

---

### Scenario 4: Test Files

**Found:**
```
Group: test
  - tests/user.test.js (90% similar)
  - tests/product.test.js (90% similar)
```

**Action:**
❌ DO NOT merge - Test files should remain separate

---

## 📝 MANDATORY DOCUMENTATION

### After Running Deduplication

**You MUST create:** `docs/DEDUPLICATION_LOG.md`

**Template:**
```markdown
# Deduplication Log

## Date: {date}

### Summary
- Files Scanned: {count}
- Duplicate Groups Found: {count}
- Files Merged: {count}
- Space Saved: {size} MB

### Merged Files

#### Group 1: {name}
- **Kept:** {file_path}
- **Removed:**
  - {file_path_1}
  - {file_path_2}
- **Reason:** {reason}
- **Backup:** {backup_path}

#### Group 2: {name}
...

### Skipped Files

#### Group 1: {name}
- **Files:**
  - {file_path_1}
  - {file_path_2}
- **Reason:** {reason for not merging}

### Verification
- [ ] Tests passed
- [ ] Build successful
- [ ] Functionality verified
- [ ] Changes committed

### Notes
{any additional notes}
```

---

## 🔍 VERIFICATION CHECKLIST

**Before merging:**
- [ ] Ran duplicate detector
- [ ] Reviewed all duplicate groups
- [ ] Manually checked each group
- [ ] Identified safe-to-merge files
- [ ] Backed up project

**After merging:**
- [ ] Verified backup exists
- [ ] Ran all tests
- [ ] Built project successfully
- [ ] Checked functionality
- [ ] Created deduplication log
- [ ] Committed changes

---

## ⚙️ CONFIGURATION

### Similarity Thresholds

**Recommended thresholds:**
- **0.95-1.0:** Very safe - Only near-identical files
- **0.85-0.95:** Safe - Similar files with minor differences
- **0.70-0.85:** Risky - Significant differences, manual review required
- **<0.70:** Unsafe - Too different, do not merge

**Default:** 0.85 (85% similarity)

### Excluded Extensions

**By default, these are excluded:**
- `.md` - Markdown documentation
- `.txt` - Text files
- `.log` - Log files
- `.json` - JSON data files
- `.xml` - XML files
- `.yml`, `.yaml` - YAML files

**To include them, modify the tool's `exclude_extensions` list.**

### Excluded Directories

**By default, these are excluded:**
- `node_modules/` - Node.js dependencies
- `.git/` - Git repository
- `__pycache__/` - Python cache
- `.venv/`, `venv/` - Virtual environments
- `dist/`, `build/` - Build outputs
- `.next/` - Next.js cache
- `.cache/` - Cache directories
- `coverage/` - Test coverage
- `logs/` - Log files

---

## 🚀 AUTOMATION

### Add to Pre-commit Hook

**File:** `.git/hooks/pre-commit`

```bash
#!/bin/bash

# Run duplicate detection
python .global/tools/duplicate_files_detector.py .

# Check if duplicates found
if [ -f "docs/duplicate_files_report.json" ]; then
    duplicates=$(jq '.summary.exact_duplicate_groups' docs/duplicate_files_report.json)
    
    if [ "$duplicates" -gt 0 ]; then
        echo "⚠️  Warning: $duplicates duplicate file groups detected"
        echo "   Run deduplication tool before committing"
        exit 1
    fi
fi
```

### Add to CI/CD Pipeline

**File:** `.github/workflows/check-duplicates.yml`

```yaml
name: Check for Duplicate Files

on: [push, pull_request]

jobs:
  check-duplicates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Run duplicate detector
        run: |
          python .global/tools/duplicate_files_detector.py .
      
      - name: Check results
        run: |
          duplicates=$(jq '.summary.exact_duplicate_groups' docs/duplicate_files_report.json)
          if [ "$duplicates" -gt 0 ]; then
            echo "❌ Found $duplicates duplicate file groups"
            exit 1
          fi
          echo "✅ No duplicates found"
```

---

## ✅ SUCCESS CRITERIA

**This prompt is complete when:**

1. ✅ All duplicate files are detected
2. ✅ Safe duplicates are merged
3. ✅ Risky duplicates are manually reviewed
4. ✅ Deduplication log is created
5. ✅ Tests pass after merging
6. ✅ Changes are committed

**This is a RECOMMENDED practice for code quality.**

---

**END OF PROMPT 86: DUPLICATE FILES DETECTION & DEDUPLICATION**

