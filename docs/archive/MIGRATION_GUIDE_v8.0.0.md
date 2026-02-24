# Migration Guide v7.x → v8.0.0

**From:** v7.2.0 (or any v7.x)  
**To:** v8.0.0  
**Type:** Breaking Changes (Module Numbers)

---

## 🚨 Breaking Changes

**All module numbers have changed!**

This is necessary to improve AI performance from 60-70% context retention to 95%+.

---

## 📋 Quick Reference

### Module Number Mapping

| v7.x | v8.0.0 | Module Name |
|------|--------|-------------|
| 01 | 10 | Requirements |
| 02 | 11 | Analysis |
| 03 | 12 | Planning |
| 10 | 20 | Backend |
| 11 | 21 | Frontend |
| 12 | 22 | Database |
| 13 | 23 | API |
| 14 | 24 | Blueprint |
| 15 | 02 | MCP |
| 16 | 03 | MCP Integration |
| 17 | 04 | Thinking Framework |
| 18 | 06 | Task AI |
| 19 | 05 | Context Engineering |
| 20 | 30 | Security |
| 21 | 31 | Authentication |
| 30 | 40 | Quality |
| 31 | 41 | Testing |
| 40 | 50 | Deployment |
| 50 | 60 | Templates |
| 60 | 01 | Memory Management |

---

## 🔧 Step-by-Step Migration

### Step 1: Backup

```bash
# Backup your current setup
cp -r /path/to/global /path/to/global_v7_backup
```

### Step 2: Update

```bash
# Pull latest version
cd /path/to/global
git fetch origin
git checkout v8.0.0
```

### Step 3: Update References

**In your code:**
```bash
# Find all references to old module numbers
grep -r "prompts/[0-9][0-9]_" .

# Update manually or use sed
sed -i 's/prompts\/60_memory/prompts\/01_memory/g' **/*.sh
sed -i 's/prompts\/15_mcp/prompts\/02_mcp/g' **/*.sh
# ... etc
```

**In your documentation:**
```bash
# Update markdown files
find . -name "*.md" -exec sed -i 's/Module 60/Module 01/g' {} \;
find . -name "*.md" -exec sed -i 's/Module 15/Module 02/g' {} \;
# ... etc
```

### Step 4: Test

```bash
# Run tests if available
python3 tools/test_suite.py

# Verify your workflows
./your_workflow.sh
```

### Step 5: Update Documentation

Update any project-specific documentation that references module numbers.

---

## 💡 Tips

### Use Module Names, Not Numbers

**Instead of:**
```bash
source prompts/01_requirements.txt  # Will break in v8.0.0!
```

**Do this:**
```bash
source prompts/$(ls prompts/*requirements.txt)  # Works in any version
```

### Use Variables

```bash
# Define once
REQUIREMENTS_MODULE="prompts/10_requirements.txt"  # v8.0.0
MCP_MODULE="prompts/02_mcp.txt"  # v8.0.0

# Use everywhere
source $REQUIREMENTS_MODULE
source $MCP_MODULE
```

---

## ✅ Verification

After migration:

```bash
# Check module count
ls prompts/*.txt | wc -l
# Should be: 21

# Check for old references
grep -r "60_memory" .
grep -r "15_mcp" .
# Should find nothing (except in backups)

# Verify new structure
ls -1 prompts/*.txt
# Should show new numbering
```

---

## 🆘 Troubleshooting

### "Module not found"

**Problem:** Script can't find module 60, 15, etc.

**Solution:** Update module numbers in your script (see mapping table above).

### "Duplicate modules"

**Problem:** Both old and new numbered modules exist.

**Solution:**
```bash
# Clean and re-clone
rm -rf prompts
git checkout prompts/
```

### "Tests failing"

**Problem:** Test suite references old module numbers.

**Solution:** Update test suite or use latest version from v8.0.0.

---

## 📞 Support

If you encounter issues:

1. Check this migration guide
2. Review CHANGELOG_v8.0.0.md
3. Check GitHub issues: https://github.com/hamfarid/global/issues
4. Create new issue if needed

---

**Good luck with the migration! 🚀**

The improvements in AI performance are worth it!
