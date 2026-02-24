#!/bin/bash

# ============================================
# V26 Diamond 10 → Diamond 11: Fix Script
# ============================================
# Run from inside Global_System_Ultimate_v26_Diamond/
# 
# This script:
# 1. Deletes 19 short duplicate role files (replaced by longer ROLE-prefixed versions)
# 2. Deletes 2 duplicate rules files (replaced by RULES-prefixed versions)
# 
# The replacement files and reference fixes are provided separately
# in the v26_d10_fixes package — copy them BEFORE running this script.

echo "=== V26 Diamond 10 → 11: Cleanup Script ==="
echo ""

# —————————————————
# STEP 1: Delete 19 short duplicate ROLE files
# These are all replaced by longer ROLE-prefixed versions
# —————————————————

echo "Deleting 19 short duplicate role files..."

SHORT_ROLES=(
"roles/01-architect.md"
"roles/02-developer.md"
"roles/03-reviewer.md"
"roles/04-qa.md"
"roles/api-designer.md"
"roles/backend-specialist.md"
"roles/code-reviewer.md"
"roles/data-scientist.md"
"roles/database-architect.md"
"roles/devops-engineer.md"
"roles/documentation-writer.md"
"roles/frontend-specialist.md"
"roles/qa.md"
"roles/reviewer.md"
"roles/security-auditor.md"
"roles/security-engineer.md"
"roles/00_swarm_intelligence.md"
"roles/big-data-architect.md"
"roles/performance-engineer.md"
)

for f in "${SHORT_ROLES[@]}"; do
  if [ -f "$f" ]; then
    rm "$f"
    echo "  ✅ Deleted: $f"
  else
    echo "  ⚠️  Not found: $f"
  fi
done

# —————————————————
# STEP 2: Delete 2 duplicate rules files
# Keeping the RULES-prefixed versions (consistent with rules/ml/)
# —————————————————

echo ""
echo "Deleting 2 duplicate rules files..."

DUP_RULES=(
"rules/big-data-security.md"
"rules/context-engineering.md"
)

for f in "${DUP_RULES[@]}"; do
  if [ -f "$f" ]; then
    rm "$f"
    echo "  ✅ Deleted: $f"
  else
    echo "  ⚠️  Not found: $f"
  fi
done

echo ""
echo "=== Cleanup Complete ==="
echo ""
echo "Summary:"
echo "  - 19 short role duplicates removed"
echo "  - 2 short rules duplicates removed"
echo "  - Total files removed: 21"
echo ""
echo "Remaining roles/ should have $(ls roles/*.md 2>/dev/null | wc -l) files (expected: ~27)"
echo ""
