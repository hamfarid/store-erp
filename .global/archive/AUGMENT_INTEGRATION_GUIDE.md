# Augment Integration Guide
# دليل التكامل مع Augment

## نظرة عامة / Overview

هذا الدليل يشرح كيفية دمج **Global Guidelines v3.9.0** مع **Augment** بشكل كامل.

This guide explains how to fully integrate **Global Guidelines v3.9.0** with **Augment**.

---

## المتطلبات / Prerequisites

- ✅ Augment مثبت ومفعل
- ✅ نسخة من Global Guidelines (v3.9.0)
- ✅ مساحة كافية (~5MB)

---

## الطريقة 1: التثبيت السريع (موصى به) ⭐

### الخطوة 1: تحميل النسخة الاحتياطية

```bash
# إذا كان لديك الملف المضغوط
tar -xzf global_final_backup_v3.9.0.tar.gz -C /tmp/global-temp/

# أو استنساخ من GitHub
git clone https://github.com/hamfarid/global.git /tmp/global-temp/
```

---

### الخطوة 2: نسخ الملفات إلى Augment

```bash
# إنشاء مجلدات Augment
mkdir -p ~/augment/prompts/
mkdir -p ~/augment/tools/
mkdir -p ~/augment/examples/
mkdir -p ~/augment/templates/

# نسخ البرومبت
cp /tmp/global-temp/GLOBAL_GUIDELINES_v3.9.txt ~/augment/prompts/

# نسخ الأدوات
cp -r /tmp/global-temp/tools/* ~/augment/tools/

# نسخ الأمثلة
cp -r /tmp/global-temp/examples/* ~/augment/examples/

# نسخ Templates
cp -r /tmp/global-temp/templates/* ~/augment/templates/

echo "✅ Files copied successfully!"
```

---

### الخطوة 3: تكوين Augment

قم بإنشاء ملف `~/augment/augment.yml`:

```yaml
# Augment Configuration for Global Guidelines v3.9.0

version: "1.0"

prompts:
  - path: prompts/GLOBAL_GUIDELINES_v3.9.txt
    name: "Global Guidelines"
    version: "3.9.0"
    description: "Comprehensive development guidelines and patterns"
    enabled: true
    priority: 1

tools:
  - path: tools/analyze_dependencies.py
    name: "Dependency Analyzer"
    description: "Analyze project dependencies and detect circular dependencies"
    enabled: true
    
  - path: tools/detect_code_duplication.py
    name: "Duplication Detector"
    description: "Detect code duplication and suggest refactoring"
    enabled: true
    
  - path: tools/smart_merge.py
    name: "Smart Merge"
    description: "Intelligently merge files with conflict resolution"
    enabled: true
    
  - path: tools/update_imports.py
    name: "Import Updater"
    description: "Update imports after module renaming"
    enabled: true

examples:
  - path: examples/simple-api/
    name: "Simple API Example"
    description: "Complete FastAPI example"
    
  - path: examples/code-samples/
    name: "Code Samples"
    description: "Common patterns and examples"
    
  - path: examples/init_py_patterns/
    name: "__init__.py Patterns"
    description: "Three __init__.py patterns"

templates:
  - path: templates/config/
    name: "Config Templates"
    description: "Configuration templates (ports, definitions)"

settings:
  auto_load_prompt: true
  tool_timeout: 300
  max_context_length: 10000
```

---

### الخطوة 4: التحقق من التثبيت

```bash
# التحقق من البرومبت
cat ~/augment/prompts/GLOBAL_GUIDELINES_v3.9.txt | head -20

# التحقق من الأدوات
ls -la ~/augment/tools/

# التحقق من الأمثلة
ls -la ~/augment/examples/

# التحقق من التكوين
cat ~/augment/augment.yml
```

---

### الخطوة 5: تشغيل Augment

```bash
# تشغيل Augment
augment start

# أو إذا كان لديك واجهة ويب
augment serve --port 8080
```

---

## الطريقة 2: التثبيت اليدوي (تفصيلي)

### الخطوة 1: إنشاء بنية المجلدات

```bash
cd ~/augment/

# إنشاء البنية
mkdir -p prompts/global/
mkdir -p tools/global/
mkdir -p examples/global/
mkdir -p templates/global/
mkdir -p docs/global/
```

---

### الخطوة 2: نسخ البرومبت

```bash
# نسخ البرومبت الرئيسي
cp /tmp/global-temp/GLOBAL_GUIDELINES_v3.9.txt ~/augment/prompts/global/

# نسخ القسم 63 منفصل (للمرجع)
cp /tmp/global-temp/SECTION_63_GLOBAL_REPOSITORY.md ~/augment/docs/global/

# نسخ الإصدارات السابقة (اختياري)
cp /tmp/global-temp/GLOBAL_GUIDELINES_v3.7.txt ~/augment/prompts/global/
cp /tmp/global-temp/GLOBAL_GUIDELINES_v3.6.txt ~/augment/prompts/global/
```

---

### الخطوة 3: نسخ الأدوات

```bash
# نسخ كل أداة
cp /tmp/global-temp/tools/analyze_dependencies.py ~/augment/tools/global/
cp /tmp/global-temp/tools/detect_code_duplication.py ~/augment/tools/global/
cp /tmp/global-temp/tools/smart_merge.py ~/augment/tools/global/
cp /tmp/global-temp/tools/update_imports.py ~/augment/tools/global/

# نسخ README
cp /tmp/global-temp/tools/README.md ~/augment/tools/global/

# جعل الأدوات قابلة للتنفيذ
chmod +x ~/augment/tools/global/*.py
```

---

### الخطوة 4: نسخ الأمثلة

```bash
# نسخ جميع الأمثلة
cp -r /tmp/global-temp/examples/* ~/augment/examples/global/

# التحقق
ls -la ~/augment/examples/global/
```

---

### الخطوة 5: نسخ Templates

```bash
# نسخ جميع Templates
cp -r /tmp/global-temp/templates/* ~/augment/templates/global/

# التحقق
ls -la ~/augment/templates/global/
```

---

### الخطوة 6: نسخ الوثائق

```bash
# نسخ الوثائق المهمة
cp /tmp/global-temp/INIT_PY_BEST_PRACTICES.md ~/augment/docs/global/
cp /tmp/global-temp/OSF_FRAMEWORK.md ~/augment/docs/global/
cp /tmp/global-temp/QUICK_START.md ~/augment/docs/global/

# نسخ Flows
mkdir -p ~/augment/docs/global/flows/
cp /tmp/global-temp/flows/* ~/augment/docs/global/flows/

# نسخ Changelogs
cp /tmp/global-temp/CHANGELOG_v3.9.0.md ~/augment/docs/global/
```

---

## استخدام Augment مع Global Guidelines

### 1. تحميل البرومبت

```python
# في Augment
import augment

# تحميل البرومبت
augment.load_prompt("prompts/GLOBAL_GUIDELINES_v3.9.txt")

# أو تحميل قسم محدد
augment.load_section("prompts/GLOBAL_GUIDELINES_v3.9.txt", section=63)
```

---

### 2. استخدام الأدوات

#### تحليل الاعتماديات

```python
# في Augment
result = augment.run_tool(
    "tools/global/analyze_dependencies.py",
    args=["./my-project/"]
)

print(result)
```

#### كشف التكرار

```python
# في Augment
result = augment.run_tool(
    "tools/global/detect_code_duplication.py",
    args=["./my-project/", "--threshold", "0.85"]
)

print(result)
```

#### دمج ذكي

```python
# في Augment
result = augment.run_tool(
    "tools/global/smart_merge.py",
    args=["--config", "merge_config.json"]
)

print(result)
```

#### تحديث الاستيرادات

```python
# في Augment
result = augment.run_tool(
    "tools/global/update_imports.py",
    args=["old_module", "new_module", "./my-project/"]
)

print(result)
```

---

### 3. استخدام الأمثلة

```python
# في Augment
# الإشارة إلى مثال
augment.add_context("examples/global/simple-api/")

# أو قراءة مثال محدد
example = augment.read_file("examples/global/simple-api/main.py")
print(example)
```

---

### 4. استخدام Templates

```python
# في Augment
# نسخ template
template = augment.read_file("templates/global/config/ports.py")

# استخدام في المشروع
augment.create_file("my-project/config/ports.py", template)
```

---

## التكوين المتقدم

### 1. تخصيص البرومبت

قم بإنشاء `~/augment/prompts/custom_prompt.txt`:

```
# تضمين Global Guidelines
{{include: prompts/GLOBAL_GUIDELINES_v3.9.txt}}

# إضافات مخصصة
## Project-Specific Rules

1. Always use TypeScript
2. Follow our custom naming conventions
3. Use our internal libraries

## Custom Patterns

...
```

---

### 2. تخصيص الأدوات

قم بإنشاء `~/augment/tools/custom/`:

```bash
mkdir -p ~/augment/tools/custom/

# إنشاء أداة مخصصة تستخدم Global tools
cat > ~/augment/tools/custom/my_analyzer.py << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '../global/')

from analyze_dependencies import analyze
from detect_code_duplication import detect

def my_custom_analysis(project_path):
    # استخدام أدوات Global
    deps = analyze(project_path)
    dupes = detect(project_path)
    
    # تحليل مخصص
    return {
        'dependencies': deps,
        'duplications': dupes,
        'custom_metric': calculate_custom_metric()
    }

if __name__ == '__main__':
    result = my_custom_analysis(sys.argv[1])
    print(result)
EOF

chmod +x ~/augment/tools/custom/my_analyzer.py
```

---

### 3. Workflows مخصصة

قم بإنشاء `~/augment/workflows/`:

```bash
mkdir -p ~/augment/workflows/

cat > ~/augment/workflows/code_review.yml << 'EOF'
name: Code Review Workflow
description: Automated code review using Global Guidelines

steps:
  - name: Load Guidelines
    action: load_prompt
    prompt: prompts/GLOBAL_GUIDELINES_v3.9.txt
    
  - name: Analyze Dependencies
    action: run_tool
    tool: tools/global/analyze_dependencies.py
    args: ["${PROJECT_PATH}"]
    
  - name: Detect Duplication
    action: run_tool
    tool: tools/global/detect_code_duplication.py
    args: ["${PROJECT_PATH}", "--threshold", "0.85"]
    
  - name: Generate Report
    action: generate_report
    template: templates/code_review_report.md
    
  - name: Send Notification
    action: notify
    channel: slack
    message: "Code review complete"
EOF
```

---

## أمثلة الاستخدام

### مثال 1: مراجعة كود تلقائية

```python
# في Augment
import augment

# تحميل البرومبت
augment.load_prompt("prompts/GLOBAL_GUIDELINES_v3.9.txt")

# تحليل المشروع
project_path = "./my-django-project/"

# تشغيل الأدوات
deps_result = augment.run_tool(
    "tools/global/analyze_dependencies.py",
    args=[project_path]
)

dupes_result = augment.run_tool(
    "tools/global/detect_code_duplication.py",
    args=[project_path]
)

# إنشاء تقرير
report = augment.generate_report({
    'dependencies': deps_result,
    'duplications': dupes_result
})

print(report)
```

---

### مثال 2: إنشاء مشروع جديد

```python
# في Augment
import augment

# تحميل البرومبت
augment.load_prompt("prompts/GLOBAL_GUIDELINES_v3.9.txt")

# إنشاء بنية المشروع
project_name = "my-new-api"
augment.create_project(project_name, template="examples/global/simple-api/")

# نسخ config definitions
augment.copy_template(
    "templates/global/config/definitions/",
    f"{project_name}/config/definitions/"
)

# إنشاء ملفات أساسية
augment.create_file(
    f"{project_name}/main.py",
    template="examples/global/simple-api/main.py"
)

print(f"✅ Project {project_name} created!")
```

---

### مثال 3: Refactoring تلقائي

```python
# في Augment
import augment

# تحميل البرومبت
augment.load_prompt("prompts/GLOBAL_GUIDELINES_v3.9.txt")

project_path = "./legacy-project/"

# 1. كشف التكرار
dupes = augment.run_tool(
    "tools/global/detect_code_duplication.py",
    args=[project_path]
)

# 2. اقتراح refactoring
suggestions = augment.suggest_refactoring(dupes)

# 3. تطبيق refactoring
for suggestion in suggestions:
    augment.apply_refactoring(suggestion)

# 4. تحديث الاستيرادات
augment.run_tool(
    "tools/global/update_imports.py",
    args=["old_module", "new_module", project_path]
)

print("✅ Refactoring complete!")
```

---

## Troubleshooting / حل المشاكل

### Issue 1: البرومبت لا يتحمل

```bash
# تحقق من المسار
ls -la ~/augment/prompts/GLOBAL_GUIDELINES_v3.9.txt

# تحقق من الأذونات
chmod 644 ~/augment/prompts/GLOBAL_GUIDELINES_v3.9.txt

# تحقق من المحتوى
head -20 ~/augment/prompts/GLOBAL_GUIDELINES_v3.9.txt
```

---

### Issue 2: الأدوات لا تعمل

```bash
# تحقق من Python
python3 --version  # يجب أن يكون >= 3.8

# تحقق من المتطلبات
pip3 install -r ~/augment/tools/global/requirements.txt

# جعل الأدوات قابلة للتنفيذ
chmod +x ~/augment/tools/global/*.py

# اختبار أداة
python3 ~/augment/tools/global/analyze_dependencies.py --help
```

---

### Issue 3: Augment لا يجد الملفات

```bash
# تحقق من augment.yml
cat ~/augment/augment.yml

# تحقق من المسارات النسبية
cd ~/augment/
ls -la prompts/
ls -la tools/
ls -la examples/
```

---

### Issue 4: الأمثلة لا تعمل

```bash
# تحقق من نسخ الأمثلة
ls -la ~/augment/examples/global/simple-api/

# تحقق من المتطلبات
cd ~/augment/examples/global/simple-api/
pip3 install -r requirements.txt

# اختبار المثال
python3 main.py
```

---

## Best Practices / أفضل الممارسات

### 1. تنظيم الملفات

```
~/augment/
├── prompts/
│   └── global/
│       ├── GLOBAL_GUIDELINES_v3.9.txt    # البرومبت الرئيسي
│       └── older-versions/                # إصدارات قديمة
│
├── tools/
│   ├── global/                            # أدوات Global
│   └── custom/                            # أدواتك المخصصة
│
├── examples/
│   ├── global/                            # أمثلة Global
│   └── my-examples/                       # أمثلتك
│
├── templates/
│   ├── global/                            # Templates Global
│   └── my-templates/                      # Templates مخصصة
│
└── docs/
    └── global/                            # وثائق Global
```

---

### 2. التحديثات

```bash
# عند صدور إصدار جديد
cd /tmp/
git clone https://github.com/hamfarid/global.git

# نسخ الإصدار الجديد
cp /tmp/global/GLOBAL_GUIDELINES_v*.txt ~/augment/prompts/global/

# تحديث الأدوات
cp -r /tmp/global/tools/* ~/augment/tools/global/

# تحديث augment.yml
vim ~/augment/augment.yml  # تحديث رقم الإصدار
```

---

### 3. النسخ الاحتياطي

```bash
# نسخ احتياطي دوري لتكوين Augment
tar -czf ~/augment-backup-$(date +%Y%m%d).tar.gz ~/augment/

# حفظ في مكان آمن
mv ~/augment-backup-*.tar.gz ~/backups/
```

---

### 4. المشاركة مع الفريق

```bash
# إنشاء حزمة للفريق
cd ~/augment/
tar -czf augment-global-setup.tar.gz \
  prompts/global/ \
  tools/global/ \
  examples/global/ \
  templates/global/ \
  augment.yml

# مشاركة مع الفريق
# يمكنهم فك الضغط واستخدامها مباشرة
```

---

## FAQ / الأسئلة الشائعة

### Q1: هل يمكن استخدام جزء من البرومبت فقط؟

**A:** نعم! يمكنك:
```python
# تحميل قسم محدد
augment.load_section("prompts/GLOBAL_GUIDELINES_v3.9.txt", section=63)

# أو استخراج أقسام محددة
augment.extract_sections([1, 5, 10, 63])
```

---

### Q2: كيف أحدث إلى إصدار جديد؟

**A:** 
```bash
# حمل الإصدار الجديد
git clone https://github.com/hamfarid/global.git /tmp/global-new/

# نسخ الملفات الجديدة
cp /tmp/global-new/GLOBAL_GUIDELINES_v*.txt ~/augment/prompts/global/

# تحديث التكوين
vim ~/augment/augment.yml
```

---

### Q3: هل يمكن تخصيص الأدوات؟

**A:** نعم! انظر قسم "التكوين المتقدم" أعلاه.

---

### Q4: كيف أشارك التكوين مع الفريق؟

**A:** 
```bash
# إنشاء حزمة
tar -czf augment-setup.tar.gz ~/augment/

# مشاركة الحزمة
# الفريق يفك الضغط ويستخدم
```

---

## Resources / المصادر

### الوثائق الرسمية:
- [Global Guidelines Repository](https://github.com/hamfarid/global)
- [Section 63: Repository Structure](https://github.com/hamfarid/global#section-63)
- [Tools Documentation](https://github.com/hamfarid/global/tree/main/tools)

### الأمثلة:
- [Simple API Example](https://github.com/hamfarid/global/tree/main/examples/simple-api)
- [__init__.py Patterns](https://github.com/hamfarid/global/tree/main/examples/init_py_patterns)

### Workflows:
- [Integration Flow](https://github.com/hamfarid/global/blob/main/flows/INTEGRATION_FLOW.md)
- [Development Flow](https://github.com/hamfarid/global/blob/main/flows/DEVELOPMENT_FLOW.md)

---

## Support / الدعم

### Need Help?

- **GitHub Issues:** https://github.com/hamfarid/global/issues
- **Discussions:** https://github.com/hamfarid/global/discussions
- **Email:** [your-email]

---

## Summary / الملخص

### ما تم إنجازه:

✅ **نسخ البرومبت** (9,277 سطر)  
✅ **نسخ 4 أدوات** احترافية  
✅ **نسخ 3 فئات أمثلة**  
✅ **نسخ Templates** جاهزة  
✅ **تكوين Augment** كامل  
✅ **أمثلة استخدام** شاملة

### الآن يمكنك:

1. ✅ استخدام البرومبت في Augment
2. ✅ تشغيل الأدوات من Augment
3. ✅ الإشارة إلى الأمثلة
4. ✅ استخدام Templates
5. ✅ إنشاء workflows مخصصة

---

**Version:** 3.9.0  
**Last Updated:** 2025-11-02  
**Status:** ✅ Complete  
**Recommended:** Yes ⭐⭐⭐

**Happy Coding with Augment! 🚀**

