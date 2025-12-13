# Scripts - سكريبتات الدمج والتكامل

## نظرة عامة / Overview

هذا المجلد يحتوي على جميع السكريبتات اللازمة لدمج Global Guidelines في المشاريع القائمة.

This directory contains all scripts needed to integrate Global Guidelines into existing projects.

---

## السكريبتات الرئيسية / Main Scripts

### 1. integrate.sh ⭐
**الاستخدام الأساسي** - دمج Global Guidelines في مشروع قائم

```bash
# Remote installation (recommended)
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# Or local
./integrate.sh
```

**ما يفعله:**
- ✅ ينشئ مجلد `.global/`
- ✅ يحمل جميع الملفات من GitHub
- ✅ يحدث `.gitignore`
- ✅ ينشئ shortcuts
- ✅ لا يؤثر على Git الخاص بك

---

### 2. configure.sh
**اختيار المكونات** - حدد ما تريد استخدامه

```bash
.global/scripts/configure.sh
```

**الخيارات:**
1. config/definitions - Type definitions
2. tools/ - Development tools
3. templates/ - Project templates
4. examples/ - Code examples
5. scripts/ - Helper scripts
6. flows/ - Workflow documentation

**مثال تفاعلي:**
```
Select components to integrate:
Enter numbers separated by spaces (e.g., 1 2 5)
Or press ENTER for default (1 2 5 6):
> 1 2 5

✓ Configuration saved!

Selected components:
[✓] config/definitions - Type definitions
[✓] tools/ - Development tools
[ ] templates/ - Project templates
[ ] examples/ - Code examples
[✓] scripts/ - Helper scripts
[ ] flows/ - Workflow docs
```

---

### 3. apply.sh
**تطبيق المكونات** - نسخ الملفات للمشروع

```bash
# Apply all configured components
.global/scripts/apply.sh

# Apply specific component only
.global/scripts/apply.sh --only config
.global/scripts/apply.sh --only tools

# Create backup before applying
.global/scripts/apply.sh --backup
```

**ما يفعله:**
- ✅ ينسخ `config/definitions/` إلى مشروعك
- ✅ ينسخ `tools/` إلى مشروعك
- ✅ ينشئ `__init__.py` files
- ✅ يحفظ نسخة احتياطية (مع `--backup`)

---

### 4. update.sh
**تحديث Global Guidelines** - احصل على أحدث إصدار

```bash
# Update to latest version
.global/scripts/update.sh

# Update to specific version
.global/scripts/update.sh --version 3.7.0
```

**ما يفعله:**
- ✅ يحمل أحدث إصدار
- ✅ يحفظ `config.json` الخاص بك
- ✅ يعرض changelog
- ✅ يحدث جميع الملفات

---

### 5. uninstall.sh
**إزالة Global Guidelines** - حذف كامل أو جزئي

```bash
# Remove .global/ only (keep applied files)
.global/scripts/uninstall.sh

# Full removal (including applied files)
.global/scripts/uninstall.sh --full
```

**ما يفعله:**
- ✅ يحذف `.global/` directory
- ✅ ينظف `.gitignore`
- ✅ يحذف shortcuts
- ✅ (مع `--full`) يحذف الملفات المطبقة

---

## سير العمل الكامل / Complete Workflow

### Scenario 1: مشروع جديد تماماً

```bash
# 1. Clone Global Guidelines
git clone https://github.com/hamfarid/global.git my-project
cd my-project

# 2. Remove .git to start fresh
rm -rf .git
git init

# 3. Start developing
# ... follow DEVELOPMENT_FLOW.md
```

---

### Scenario 2: مشروع قائم (الأكثر شيوعاً)

```bash
# 1. Navigate to your project
cd /path/to/existing-project

# 2. Integrate Global Guidelines
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# 3. Configure components
.global/scripts/configure.sh
# Select: 1 2 5 (config, tools, scripts)

# 4. Apply to project
.global/scripts/apply.sh --backup

# 5. Verify
ls -la config/definitions/
ls -la tools/

# 6. Start using
python tools/analyze_dependencies.py .
cat .global/GLOBAL_GUIDELINES_v3.7.txt
```

---

### Scenario 3: تحديث Global Guidelines

```bash
# 1. Check current version
cat .global/VERSION

# 2. Update
.global/scripts/update.sh

# 3. Re-apply if needed
.global/scripts/apply.sh

# 4. Verify
cat .global/CHANGELOG.md
```

---

### Scenario 4: إزالة Global Guidelines

```bash
# Option A: Remove .global/ only (keep applied files)
.global/scripts/uninstall.sh

# Option B: Full removal
.global/scripts/uninstall.sh --full

# Verify
ls -la .global/  # Should not exist
```

---

## السكريبتات المساعدة / Helper Scripts

### backup.sh
نسخ احتياطي للمشروع

```bash
scripts/backup.sh
```

### fix_line_length.sh
إصلاح السطور الطويلة

```bash
scripts/fix_line_length.sh
```

### remove_unused.sh
إزالة الاستيرادات غير المستخدمة

```bash
scripts/remove_unused.sh
```

---

## الاستخدام المتقدم / Advanced Usage

### 1. تخصيص التثبيت

```bash
# Edit integrate.sh before running
vim scripts/integrate.sh

# Change GLOBAL_DIR
GLOBAL_DIR=".my-custom-dir"

# Change VERSION
VERSION="3.6.0"
```

### 2. Automation في CI/CD

```yaml
# .github/workflows/setup.yml
steps:
  - name: Install Global Guidelines
    run: |
      curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash
      .global/scripts/configure.sh <<< "1 2 5"
      .global/scripts/apply.sh
```

### 3. Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Run quality checks
python .global/tools/analyze_dependencies.py .
python .global/tools/detect_code_duplication.py .

# If checks fail, prevent commit
if [ $? -ne 0 ]; then
    echo "Quality checks failed"
    exit 1
fi
```

---

## Troubleshooting / حل المشاكل

### Issue 1: integrate.sh يفشل

```bash
# Check prerequisites
which curl
which git

# Run with debug
bash -x scripts/integrate.sh
```

### Issue 2: Permission denied

```bash
# Make scripts executable
chmod +x .global/scripts/*.sh

# Or run with bash
bash .global/scripts/integrate.sh
```

### Issue 3: Files already exist

```bash
# Use --backup flag
.global/scripts/apply.sh --backup

# Or remove existing files first
rm -rf config/definitions tools/
.global/scripts/apply.sh
```

### Issue 4: Update fails

```bash
# Remove and reinstall
rm -rf .global/
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash
```

---

## Best Practices / أفضل الممارسات

### 1. استخدم --backup دائماً

```bash
# Always create backup before applying
.global/scripts/apply.sh --backup
```

### 2. اختبر في branch منفصل

```bash
# Create test branch
git checkout -b test-global-integration

# Integrate
curl -sSL ... | bash
.global/scripts/configure.sh
.global/scripts/apply.sh

# Test
# ... run tests

# If OK, merge to main
git checkout main
git merge test-global-integration
```

### 3. وثق التخصيصات

```markdown
# في README.md

## Global Guidelines Integration

We use [Global Guidelines](https://github.com/hamfarid/global) v3.7.0

### Customizations:
- Using only config and tools components
- Modified config/definitions/custom.py for our needs
- Added project-specific tools in tools/custom/
```

### 4. حدّث بانتظام

```bash
# Monthly update
.global/scripts/update.sh

# Check changelog
cat .global/CHANGELOG.md

# Re-apply if needed
.global/scripts/apply.sh
```

---

## FAQ / الأسئلة الشائعة

### Q1: هل يمكن تشغيل integrate.sh أكثر من مرة؟

**A:** نعم! سيسألك إذا كنت تريد إعادة التثبيت.

### Q2: ماذا لو كان لدي ملفات config/ موجودة؟

**A:** استخدم `--backup` flag. أو اختر components محددة فقط.

### Q3: كيف أعرف الإصدار المثبت؟

**A:** `cat .global/VERSION`

### Q4: هل يمكن استخدام جزء من الأدوات فقط؟

**A:** نعم! استخدم `configure.sh` لاختيار المكونات.

### Q5: كيف أحذف كل شيء؟

**A:** `.global/scripts/uninstall.sh --full`

---

## Examples / أمثلة

### Example 1: Django Project

```bash
cd my-django-project/

# Integrate
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# Configure (config + tools)
.global/scripts/configure.sh <<< "1 2"

# Apply
.global/scripts/apply.sh --backup

# Use in models.py
from config.definitions import Status, UserRole

class User(models.Model):
    role = models.CharField(choices=[(r.value, r.name) for r in UserRole])
    status = models.CharField(choices=[(s.value, s.name) for s in Status])
```

### Example 2: Flask Project

```bash
cd my-flask-app/

# Integrate
./integrate.sh

# Configure (all components)
.global/scripts/configure.sh <<< "1 2 3 4 5 6"

# Apply
.global/scripts/apply.sh

# Use in app.py
from config.definitions import APIResponse

@app.route('/api/data')
def get_data():
    return APIResponse(success=True, data={"items": []})
```

### Example 3: FastAPI Project

```bash
cd my-fastapi-service/

# Integrate
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# Configure
.global/scripts/configure.sh

# Apply with backup
.global/scripts/apply.sh --backup

# Analyze dependencies
python .global/tools/analyze_dependencies.py app/

# Detect duplication
python .global/tools/detect_code_duplication.py app/
```

---

## References / المراجع

- [Integration Flow](../flows/INTEGRATION_FLOW.md)
- [Development Flow](../flows/DEVELOPMENT_FLOW.md)
- [Global Guidelines](../GLOBAL_GUIDELINES_v3.7.txt)
- [Quick Start](../QUICK_START.md)

---

**Last Updated:** 2025-11-02  
**Version:** 1.0.0  
**Status:** ✅ Active

