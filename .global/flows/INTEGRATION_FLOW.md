# Integration Flow - سير عمل الدمج

## نظرة عامة / Overview

دليل شامل لدمج Global Guidelines في المشاريع القائمة **بدون التأثير على مستودع Git الأصلي**.

Comprehensive guide for integrating Global Guidelines into existing projects **without affecting the original Git repository**.

---

## الفلسفة / Philosophy

### المبادئ الأساسية:

1. **عدم التدخل** - لا تغيير في `.git/` الأصلي
2. **الاستقلالية** - التثبيت في مجلد منفصل `.global/`
3. **المرونة** - اختيار ما تحتاجه فقط
4. **القابلية للإزالة** - سهولة الحذف الكامل

---

## طرق الدمج / Integration Methods

### Method 1: Standalone Installation (موصى به)

**الاستخدام:** للمشاريع القائمة التي لا تريد تغيير Git

```bash
# التحميل والتثبيت التلقائي
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# أو التحميل اليدوي
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh -o integrate.sh
chmod +x integrate.sh
./integrate.sh
```

**ما يحدث:**
```
your-project/
├── .git/              # لا يتغير! ✅
├── .global/           # مجلد جديد منفصل
│   ├── guidelines/    # البرومبت
│   ├── tools/         # الأدوات
│   ├── templates/     # القوالب
│   ├── scripts/       # السكريبتات
│   └── examples/      # الأمثلة
├── .gitignore         # يُحدث لتجاهل .global/
└── (ملفات مشروعك)
```

---

### Method 2: Git Submodule

**الاستخدام:** إذا كنت تريد تتبع الإصدارات

```bash
# إضافة كـ submodule
git submodule add https://github.com/hamfarid/global.git .global

# تحديث
git submodule update --remote .global

# Clone مع submodules
git clone --recurse-submodules <your-repo>
```

**الإيجابيات:**
- ✅ تتبع الإصدارات
- ✅ سهولة التحديث
- ✅ مدمج مع Git

**السلبيات:**
- ❌ يضيف complexity
- ❌ يتطلب فهم submodules

---

### Method 3: Manual Download

**الاستخدام:** للتحكم الكامل

```bash
# تحميل ZIP
curl -L https://github.com/hamfarid/global/archive/refs/heads/main.zip -o global.zip
unzip global.zip -d .global
rm global.zip
mv .global/global-main/* .global/
rm -rf .global/global-main
```

---

## خطوات الدمج التفصيلية / Detailed Integration Steps

### Step 1: التحضير / Preparation

```bash
# 1. الانتقال لمشروعك
cd /path/to/your/project

# 2. التأكد من حالة Git نظيفة
git status

# 3. إنشاء branch للتجربة (اختياري)
git checkout -b integrate-global-guidelines
```

---

### Step 2: التثبيت / Installation

```bash
# تشغيل script الدمج
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# أو إذا حملته يدوياً
./integrate.sh
```

**Script يقوم بـ:**
1. ✅ إنشاء `.global/` directory
2. ✅ تحميل جميع الملفات
3. ✅ إعداد البنية
4. ✅ تحديث `.gitignore`
5. ✅ إنشاء shortcuts

---

### Step 3: التكوين / Configuration

```bash
# 1. اختيار ما تحتاجه
.global/scripts/configure.sh

# سيسألك:
# - Do you want to use config/definitions? [Y/n]
# - Do you want to use tools? [Y/n]
# - Do you want to use templates? [Y/n]
# - Do you want to use examples? [Y/n]
```

**مثال تفاعلي:**
```
🔧 Global Guidelines Configuration
====================================

Select components to integrate:

[✓] 1. config/definitions (Type definitions)
[✓] 2. tools/ (Development tools)
[ ] 3. templates/ (Project templates)
[ ] 4. examples/ (Code examples)
[✓] 5. scripts/ (Helper scripts)

Press SPACE to toggle, ENTER to confirm
```

---

### Step 4: التطبيق / Application

```bash
# تطبيق المكونات المختارة
.global/scripts/apply.sh

# أو تطبيق مكون محدد
.global/scripts/apply.sh --only config
.global/scripts/apply.sh --only tools
```

**ما يحدث:**
```
Applying config/definitions...
  ✅ Created config/
  ✅ Created config/definitions/
  ✅ Copied common.py
  ✅ Copied core.py
  ✅ Copied custom.py
  ✅ Created __init__.py

Applying tools...
  ✅ Created tools/
  ✅ Copied analyze_dependencies.py
  ✅ Copied detect_code_duplication.py
  ✅ Copied smart_merge.py
  ✅ Copied update_imports.py

Done! ✨
```

---

### Step 5: التحقق / Verification

```bash
# فحص البنية
tree -L 2 -I 'venv|__pycache__'

# اختبار الأدوات
python .global/tools/analyze_dependencies.py .

# قراءة البرومبت
cat .global/guidelines/GLOBAL_GUIDELINES_v3.7.txt | less
```

---

## الاستخدام اليومي / Daily Usage

### 1. الوصول للبرومبت

```bash
# قراءة البرومبت
cat .global/guidelines/GLOBAL_GUIDELINES_v3.7.txt

# البحث في البرومبت
grep -n "keyword" .global/guidelines/GLOBAL_GUIDELINES_v3.7.txt

# نسخ للمشروع
cp .global/guidelines/GLOBAL_GUIDELINES_v3.7.txt docs/GUIDELINES.txt
```

### 2. استخدام الأدوات

```bash
# تحليل الاعتماديات
python .global/tools/analyze_dependencies.py .

# كشف التكرار
python .global/tools/detect_code_duplication.py .

# دمج ذكي
python .global/tools/smart_merge.py --config merge.json

# تحديث الاستيرادات
python .global/tools/update_imports.py old new .
```

### 3. استخدام Templates

```bash
# نسخ template
cp .global/templates/config/definitions/common.py config/definitions/

# تطبيق template كامل
.global/scripts/apply_template.sh api-server
```

---

## التحديث / Updates

### تحديث Global Guidelines

```bash
# Method 1: Standalone
.global/scripts/update.sh

# Method 2: Submodule
git submodule update --remote .global

# Method 3: Manual
cd .global
git pull origin main
cd ..
```

### التحقق من الإصدار

```bash
# عرض الإصدار الحالي
cat .global/VERSION

# عرض التغييرات
cat .global/CHANGELOG.md

# مقارنة الإصدارات
.global/scripts/compare_versions.sh
```

---

## الإزالة / Removal

### إزالة كاملة

```bash
# حذف .global/ فقط
rm -rf .global/

# حذف الملفات المطبقة أيضاً
.global/scripts/uninstall.sh --full

# تنظيف .gitignore
# (احذف السطور المتعلقة بـ .global/)
```

### إزالة جزئية

```bash
# إزالة مكون محدد
.global/scripts/remove.sh --component tools

# الاحتفاظ بالبرومبت فقط
.global/scripts/remove.sh --keep-guidelines
```

---

## أمثلة عملية / Practical Examples

### Example 1: مشروع Django قائم

```bash
# 1. الانتقال للمشروع
cd /path/to/django-project

# 2. التثبيت
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# 3. اختيار المكونات
.global/scripts/configure.sh
# Select: config, tools, scripts

# 4. التطبيق
.global/scripts/apply.sh

# 5. استخدام config/definitions
# في models.py
from config.definitions import Status, UserRole

class User(models.Model):
    role = models.CharField(
        max_length=20,
        choices=[(r.value, r.name) for r in UserRole]
    )
    status = models.CharField(
        max_length=20,
        choices=[(s.value, s.name) for s in Status]
    )
```

---

### Example 2: مشروع Flask قائم

```bash
# 1. التثبيت
cd /path/to/flask-project
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# 2. استخدام الأدوات
python .global/tools/analyze_dependencies.py app/

# 3. تطبيق البنية
mkdir -p config/definitions
cp .global/templates/config/definitions/*.py config/definitions/

# 4. استخدام في الكود
# في app/__init__.py
from config.definitions import APIResponse, ErrorResponse

@app.route('/api/data')
def get_data():
    return APIResponse(
        success=True,
        message="Data retrieved",
        data={"items": []}
    )
```

---

### Example 3: مشروع FastAPI قائم

```bash
# 1. التثبيت
cd /path/to/fastapi-project
./integrate.sh

# 2. دمج config/definitions مع Pydantic
# في app/models.py
from pydantic import BaseModel
from config.definitions import Status, UserRole

class UserCreate(BaseModel):
    username: str
    role: UserRole
    status: Status = Status.ACTIVE

# 3. استخدام الأدوات
python .global/tools/detect_code_duplication.py app/
```

---

## Best Practices / أفضل الممارسات

### 1. إدارة .gitignore

```gitignore
# .gitignore

# Global Guidelines (standalone installation)
.global/

# OR if using submodule, don't ignore it
# .global/ is tracked by Git as submodule
```

### 2. التوثيق

```markdown
# في README.md

## Development Setup

This project uses [Global Guidelines](https://github.com/hamfarid/global) for development standards.

### Installation

```bash
# Install Global Guidelines
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# Configure
.global/scripts/configure.sh

# Apply
.global/scripts/apply.sh
```

### 3. CI/CD Integration

```yaml
# .github/workflows/ci.yml

jobs:
  test:
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Global Guidelines
        run: |
          curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash
      
      - name: Run quality checks
        run: |
          python .global/tools/analyze_dependencies.py .
          python .global/tools/detect_code_duplication.py .
```

---

## Troubleshooting / حل المشاكل

### Issue 1: Script لا يعمل

```bash
# تأكد من الصلاحيات
chmod +x integrate.sh
chmod +x .global/scripts/*.sh

# تشغيل مع bash صريح
bash integrate.sh
```

### Issue 2: تعارض الملفات

```bash
# نسخ احتياطي قبل التطبيق
.global/scripts/apply.sh --backup

# استرجاع إذا حدث خطأ
.global/scripts/restore_backup.sh
```

### Issue 3: مشاكل الاستيراد

```python
# إضافة .global/ للـ Python path
import sys
sys.path.insert(0, '.global')

# أو في .env
export PYTHONPATH="${PYTHONPATH}:${PWD}/.global"
```

---

## FAQ / الأسئلة الشائعة

### Q1: هل سيؤثر على Git الخاص بي؟

**A:** لا! التثبيت في `.global/` منفصل تماماً. فقط `.gitignore` يُحدث لتجاهله.

### Q2: كيف أحدث Global Guidelines؟

**A:** استخدم `.global/scripts/update.sh` أو `git submodule update --remote .global`

### Q3: هل يمكن استخدام جزء فقط؟

**A:** نعم! استخدم `.global/scripts/configure.sh` لاختيار المكونات.

### Q4: كيف أزيله بالكامل؟

**A:** `rm -rf .global/` أو `.global/scripts/uninstall.sh --full`

### Q5: هل يعمل مع monorepos؟

**A:** نعم! ثبته في الـ root أو في كل package منفصل.

---

## Checklist / قائمة التحقق

### قبل الدمج:
- [ ] نسخة احتياطية من المشروع
- [ ] Git status نظيف
- [ ] فهم طريقة الدمج المختارة

### بعد الدمج:
- [ ] `.global/` موجود ويعمل
- [ ] `.gitignore` محدث
- [ ] الأدوات تعمل بشكل صحيح
- [ ] الفريق على علم بالتغييرات
- [ ] التوثيق محدث

### الصيانة الدورية:
- [ ] تحديث Global Guidelines شهرياً
- [ ] مراجعة التغييرات الجديدة
- [ ] تطبيق best practices الجديدة

---

## References / المراجع

- [Development Flow](./DEVELOPMENT_FLOW.md)
- [Global Guidelines](../GLOBAL_GUIDELINES_v3.7.txt)
- [Integration Script](../scripts/integrate.sh)
- [Quick Start](../QUICK_START.md)

---

**Last Updated:** 2025-11-02  
**Version:** 1.0.0  
**Status:** ✅ Active

