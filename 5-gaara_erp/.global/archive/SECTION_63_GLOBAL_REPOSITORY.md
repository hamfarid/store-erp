# Section 63: GLOBAL REPOSITORY STRUCTURE & TOOLS
# القسم 63: بنية مستودع Global والأدوات

================================================================================
## 63. GLOBAL REPOSITORY STRUCTURE & TOOLS
================================================================================

## Overview / نظرة عامة

مستودع **Global Guidelines** هو مستودع شامل يحتوي على:
- البرومبت الرئيسي (هذا الملف)
- أدوات تطوير احترافية
- أمثلة عملية
- قوالب جاهزة
- سكريبتات للتكامل
- وثائق سير العمل

The **Global Guidelines** repository is a comprehensive repository containing:
- Main prompt (this file)
- Professional development tools
- Practical examples
- Ready-made templates
- Integration scripts
- Workflow documentation

**Repository URL:** https://github.com/hamfarid/global

---

## Repository Structure / بنية المستودع

```
global/
├── GLOBAL_GUIDELINES_v3.7.txt          # البرومبت الرئيسي (هذا الملف)
├── GLOBAL_GUIDELINES_FINAL.txt         # نسخة نهائية
├── VERSION                              # الإصدار الحالي
│
├── tools/                               # أدوات التطوير ⚙️
│   ├── analyze_dependencies.py          # تحليل الاعتماديات
│   ├── detect_code_duplication.py       # كشف التكرار
│   ├── smart_merge.py                   # دمج ذكي
│   ├── update_imports.py                # تحديث الاستيرادات
│   └── README.md                        # دليل الأدوات
│
├── templates/                           # القوالب 📋
│   └── config/
│       ├── ports.py                     # Ports pattern
│       └── definitions/
│           ├── __init__.py
│           ├── common.py                # تعريفات عامة
│           ├── core.py                  # تعريفات أساسية
│           └── custom.py                # تعريفات مخصصة
│
├── examples/                            # الأمثلة 💡
│   ├── simple-api/                      # مثال API بسيط
│   ├── code-samples/                    # عينات كود
│   └── init_py_patterns/                # أنماط __init__.py
│       ├── 01_central_registry/
│       ├── 02_lazy_loading/
│       └── 03_plugin_system/
│
├── scripts/                             # سكريبتات التكامل 🔧
│   ├── integrate.sh                     # تثبيت رئيسي
│   ├── configure.sh                     # تكوين
│   ├── apply.sh                         # تطبيق
│   ├── update.sh                        # تحديث
│   ├── uninstall.sh                     # إزالة
│   └── README.md                        # دليل السكريبتات
│
├── flows/                               # سير العمل 📚
│   ├── DEVELOPMENT_FLOW.md              # سير عمل التطوير
│   ├── INTEGRATION_FLOW.md              # سير عمل الدمج
│   ├── DEPLOYMENT_FLOW.md               # سير عمل النشر
│   └── README.md                        # دليل Flows
│
└── docs/                                # الوثائق 📖
    ├── INIT_PY_BEST_PRACTICES.md        # أفضل ممارسات __init__.py
    ├── OSF_FRAMEWORK.md                 # إطار OSF
    ├── QUICK_START.md                   # البدء السريع
    └── CHANGELOG.md                     # سجل التغييرات
```

---

## 1. Tools / الأدوات ⚙️

### 1.1 analyze_dependencies.py

**الوظيفة:** تحليل شامل للاعتماديات في المشروع

**الاستخدام:**
```bash
python tools/analyze_dependencies.py /path/to/project
```

**الميزات:**
- ✅ اكتشاف الاعتماديات المباشرة وغير المباشرة
- ✅ كشف الاعتماديات الدائرية (Circular Dependencies)
- ✅ تحليل عمق الاعتماديات
- ✅ إنشاء رسم بياني للاعتماديات
- ✅ تقرير مفصل بالمشاكل

**مثال الإخراج:**
```
=== Dependency Analysis Report ===

Total modules analyzed: 45
Direct dependencies: 123
Indirect dependencies: 67

⚠️ Circular Dependencies Found:
  - module_a → module_b → module_c → module_a
  - service_x → service_y → service_x

Recommendations:
  1. Break circular dependency between module_a and module_c
  2. Consider using dependency injection for service_x
```

**الخيارات:**
```bash
# تحليل مع رسم بياني
python tools/analyze_dependencies.py . --graph deps.png

# تحليل مع تقرير JSON
python tools/analyze_dependencies.py . --format json > report.json

# تحليل مع عمق محدد
python tools/analyze_dependencies.py . --max-depth 3
```

---

### 1.2 detect_code_duplication.py

**الوظيفة:** كشف التكرار في الكود

**الاستخدام:**
```bash
python tools/detect_code_duplication.py /path/to/project
```

**الميزات:**
- ✅ كشف الكود المكرر (>= 5 أسطر)
- ✅ حساب نسبة التشابه
- ✅ تحديد الملفات والأسطر المكررة
- ✅ اقتراحات للدمج
- ✅ تقرير مفصل

**مثال الإخراج:**
```
=== Code Duplication Report ===

Total files scanned: 45
Duplications found: 12
Average similarity: 87%

Duplication #1 (95% similar):
  File 1: src/services/user_service.py (lines 45-62)
  File 2: src/services/admin_service.py (lines 78-95)
  
  Suggestion: Extract to common function in src/utils/auth.py

Duplication #2 (89% similar):
  File 1: src/models/user.py (lines 12-25)
  File 2: src/models/admin.py (lines 15-28)
  
  Suggestion: Create base model in src/models/base.py
```

**الخيارات:**
```bash
# تحديد حد التشابه
python tools/detect_code_duplication.py . --threshold 0.85

# تحديد الحد الأدنى لعدد الأسطر
python tools/detect_code_duplication.py . --min-lines 10

# تجاهل ملفات معينة
python tools/detect_code_duplication.py . --ignore tests/,migrations/
```

---

### 1.3 smart_merge.py

**الوظيفة:** دمج ذكي للملفات مع حل التعارضات

**الاستخدام:**
```bash
python tools/smart_merge.py --config merge_config.json
```

**الميزات:**
- ✅ دمج تلقائي للملفات
- ✅ كشف التعارضات
- ✅ حل ذكي للتعارضات
- ✅ نسخ احتياطي تلقائي
- ✅ Rollback عند الفشل

**ملف التكوين (merge_config.json):**
```json
{
  "source": "feature_branch/",
  "target": "main_branch/",
  "strategy": "smart",
  "backup": true,
  "auto_resolve": true,
  "conflict_resolution": {
    "imports": "merge",
    "functions": "prefer_target",
    "classes": "prefer_source"
  }
}
```

**مثال الإخراج:**
```
=== Smart Merge Report ===

Files to merge: 15
Conflicts detected: 3
Auto-resolved: 2
Manual intervention needed: 1

✅ Merged successfully:
  - src/models/user.py
  - src/services/auth.py
  - src/utils/helpers.py

⚠️ Conflicts (auto-resolved):
  - src/config/settings.py (imports merged)
  - src/api/routes.py (functions merged)

❌ Manual intervention needed:
  - src/core/engine.py (conflicting logic)
    Please review and resolve manually
```

**الخيارات:**
```bash
# تشغيل تجريبي (dry run)
python tools/smart_merge.py --config merge_config.json --dry-run

# تجاهل النسخ الاحتياطي
python tools/smart_merge.py --config merge_config.json --no-backup

# وضع تفاعلي
python tools/smart_merge.py --config merge_config.json --interactive
```

---

### 1.4 update_imports.py

**الوظيفة:** تحديث الاستيرادات تلقائياً عند إعادة التسمية

**الاستخدام:**
```bash
python tools/update_imports.py old_module new_module /path/to/project
```

**الميزات:**
- ✅ تحديث جميع الاستيرادات تلقائياً
- ✅ دعم الاستيرادات المختلفة (from, import, as)
- ✅ تحديث docstrings
- ✅ نسخ احتياطي قبل التحديث
- ✅ تقرير مفصل بالتغييرات

**أمثلة:**
```bash
# تحديث اسم module
python tools/update_imports.py old_auth new_auth .

# تحديث اسم package
python tools/update_imports.py src.old_pkg src.new_pkg .

# تحديث مع نسخ احتياطي
python tools/update_imports.py old new . --backup
```

**مثال الإخراج:**
```
=== Import Update Report ===

Files scanned: 45
Files updated: 12
Imports updated: 34

Updated files:
  ✅ src/services/user_service.py (3 imports)
  ✅ src/api/routes.py (5 imports)
  ✅ src/models/user.py (2 imports)
  ...

Backup created at: .backup_20251102_120000/
```

**التحديثات المدعومة:**
```python
# Before
from old_module import func
import old_module
import old_module as om
from old_module.sub import Class

# After
from new_module import func
import new_module
import new_module as om
from new_module.sub import Class
```

---

## 2. Templates / القوالب 📋

### 2.1 config/ports.py

**الوصف:** نمط Ports & Adapters (Hexagonal Architecture)

**الاستخدام:**
```python
from config.ports import (
    UserRepositoryPort,
    EmailServicePort,
    PaymentGatewayPort
)

# Implement adapters
class PostgresUserRepository(UserRepositoryPort):
    def get_user(self, user_id: int) -> User:
        # Implementation
        pass
```

**الميزات:**
- ✅ فصل المنطق عن التفاصيل
- ✅ سهولة الاختبار (Mocking)
- ✅ قابلية التبديل (Swappable implementations)

---

### 2.2 config/definitions/

#### common.py
**التعريفات العامة المشتركة:**
```python
from config.definitions import (
    Status,           # ACTIVE, INACTIVE, PENDING, DELETED
    UserRole,         # ADMIN, USER, GUEST, MODERATOR
    Environment,      # DEV, STAGING, PROD
    APIResponse,      # استجابة API موحدة
    ErrorResponse     # استجابة خطأ موحدة
)
```

#### core.py
**التعريفات الأساسية للنماذج:**
```python
from config.definitions import (
    BaseModel,        # نموذج أساسي
    TimestampMixin,   # created_at, updated_at
    SoftDeleteMixin,  # deleted_at, is_deleted
    AuditMixin        # created_by, updated_by
)
```

#### custom.py
**تعريفات مخصصة للمشروع:**
```python
from config.definitions import (
    ProjectStatus,    # PLANNING, IN_PROGRESS, COMPLETED
    Priority,         # LOW, MEDIUM, HIGH, CRITICAL
    TaskType          # BUG, FEATURE, ENHANCEMENT
)
```

---

## 3. Examples / الأمثلة 💡

### 3.1 simple-api/

**الوصف:** مثال كامل لـ API بسيط باستخدام FastAPI

**المحتوى:**
```
simple-api/
├── main.py              # نقطة الدخول
├── models.py            # النماذج
├── routes.py            # المسارات
├── config.py            # التكوين
└── README.md            # الدليل
```

**الاستخدام:**
```bash
cd examples/simple-api/
pip install -r requirements.txt
uvicorn main:app --reload
```

**الميزات:**
- ✅ استخدام config/definitions
- ✅ Ports & Adapters pattern
- ✅ Error handling موحد
- ✅ Logging شامل
- ✅ Tests كاملة

---

### 3.2 code-samples/

**الوصف:** عينات كود لأنماط شائعة

**الأمثلة المتوفرة:**
- `log_activity_example.py` - تسجيل النشاطات
- `error_handling_example.py` - معالجة الأخطاء
- `async_example.py` - البرمجة غير المتزامنة
- `database_example.py` - عمليات قاعدة البيانات

---

### 3.3 init_py_patterns/

**الوصف:** 3 أنماط كاملة لملفات `__init__.py`

#### Pattern 1: Central Registry
```python
# من 01_central_registry/__init__.py
from .status_types import Status, UserRole
from .response_types import APIResponse, ErrorResponse
from .model_mixins import TimestampMixin, AuditMixin

__all__ = [
    'Status', 'UserRole',
    'APIResponse', 'ErrorResponse',
    'TimestampMixin', 'AuditMixin'
]
```

#### Pattern 2: Lazy Loading
```python
# من 02_lazy_loading/__init__.py
def __getattr__(name):
    if name == 'Analyzer':
        from .analyzer import Analyzer
        return Analyzer
    raise AttributeError(f"module has no attribute '{name}'")
```

#### Pattern 3: Plugin System
```python
# من 03_plugin_system/__init__.py
def discover_plugins():
    # Auto-discover plugins
    pass

def get_plugin(name):
    # Get plugin by name
    pass
```

---

## 4. Scripts / السكريبتات 🔧

### 4.1 integrate.sh ⭐⭐⭐

**الوظيفة:** تثبيت Global Guidelines في مشروع قائم

**الاستخدام:**
```bash
# Remote installation
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# Local installation
./scripts/integrate.sh
```

**ما يفعله:**
1. ينشئ `.global/` directory
2. يحمل جميع الملفات من GitHub
3. يحدث `.gitignore`
4. ينشئ shortcuts
5. يجعل السكريبتات قابلة للتنفيذ

**لا يؤثر على:**
- `.git/` directory
- ملفات المشروع الموجودة
- Git history

---

### 4.2 configure.sh

**الوظيفة:** اختيار المكونات المطلوبة

**الاستخدام:**
```bash
.global/scripts/configure.sh
```

**المكونات:**
1. config/definitions
2. tools/
3. templates/
4. examples/
5. scripts/
6. flows/

---

### 4.3 apply.sh

**الوظيفة:** تطبيق المكونات على المشروع

**الاستخدام:**
```bash
# تطبيق الكل
.global/scripts/apply.sh

# تطبيق مكون محدد
.global/scripts/apply.sh --only config

# مع نسخ احتياطي
.global/scripts/apply.sh --backup
```

---

### 4.4 update.sh

**الوظيفة:** تحديث Global Guidelines

**الاستخدام:**
```bash
# آخر إصدار
.global/scripts/update.sh

# إصدار محدد
.global/scripts/update.sh --version 3.7.0
```

---

### 4.5 uninstall.sh

**الوظيفة:** إزالة Global Guidelines

**الاستخدام:**
```bash
# إزالة .global/ فقط
.global/scripts/uninstall.sh

# إزالة كاملة
.global/scripts/uninstall.sh --full
```

---

## 5. Flows / سير العمل 📚

### 5.1 DEVELOPMENT_FLOW.md

**المحتوى:**
- 7 مراحل للتطوير
- من التهيئة إلى النشر
- Best practices لكل مرحلة
- أمثلة CI/CD

---

### 5.2 INTEGRATION_FLOW.md ⭐

**المحتوى:**
- 3 طرق للدمج
- خطوات تفصيلية
- أمثلة لـ Django, Flask, FastAPI
- FAQ شامل

**الأهم للمشاريع القائمة!**

---

### 5.3 DEPLOYMENT_FLOW.md

**المحتوى:**
- 3 استراتيجيات نشر
- Docker & Kubernetes
- CI/CD pipelines
- Monitoring & Rollback

---

## 6. How to Use in Augment / كيفية الاستخدام في Augment

### الطريقة الموصى بها:

```bash
# 1. نسخ البرومبت إلى Augment
cp GLOBAL_GUIDELINES_v3.7.txt /path/to/augment/prompts/

# 2. نسخ الأدوات
cp -r tools/ /path/to/augment/tools/

# 3. نسخ الأمثلة
cp -r examples/ /path/to/augment/examples/

# 4. نسخ Templates
cp -r templates/ /path/to/augment/templates/

# 5. في Augment، أشر إلى:
# - البرومبت: prompts/GLOBAL_GUIDELINES_v3.7.txt
# - الأدوات: tools/
# - الأمثلة: examples/
```

### في Augment Configuration:

```yaml
# augment.yml
prompts:
  - path: prompts/GLOBAL_GUIDELINES_v3.7.txt
    name: "Global Guidelines"
    version: "3.7.0"

tools:
  - path: tools/analyze_dependencies.py
    name: "Dependency Analyzer"
  - path: tools/detect_code_duplication.py
    name: "Duplication Detector"
  - path: tools/smart_merge.py
    name: "Smart Merge"
  - path: tools/update_imports.py
    name: "Import Updater"

examples:
  - path: examples/simple-api/
  - path: examples/code-samples/
  - path: examples/init_py_patterns/

templates:
  - path: templates/config/
```

---

## 7. Best Practices / أفضل الممارسات

### عند استخدام الأدوات:

1. **analyze_dependencies.py**
   - شغله دورياً (أسبوعياً)
   - راقب الاعتماديات الدائرية
   - احفظ التقارير للمقارنة

2. **detect_code_duplication.py**
   - شغله قبل كل merge
   - استهدف < 5% تكرار
   - استخدم الاقتراحات للدمج

3. **smart_merge.py**
   - استخدم dry-run أولاً
   - احفظ نسخة احتياطية دائماً
   - راجع التعارضات يدوياً

4. **update_imports.py**
   - اختبر في branch منفصل
   - راجع التغييرات قبل commit
   - احفظ نسخة احتياطية

---

### عند استخدام Templates:

1. **لا تعدل Templates مباشرة**
   - انسخها لمشروعك أولاً
   - عدل النسخة في مشروعك

2. **حافظ على التحديثات**
   - راجع templates عند التحديث
   - دمج التحسينات الجديدة

---

### عند استخدام Examples:

1. **استخدمها كمرجع**
   - لا تنسخها كما هي
   - افهم المفاهيم وطبقها

2. **تعلم من الأنماط**
   - كل مثال يوضح نمط معين
   - طبق النمط المناسب لحالتك

---

## 8. Integration with AI Tools / التكامل مع أدوات AI

### مع Augment:

```python
# في Augment، يمكنك:
# 1. تحميل البرومبت كـ system prompt
# 2. الإشارة للأدوات عند الحاجة
# 3. استخدام الأمثلة كـ context

# مثال:
augment.load_prompt("GLOBAL_GUIDELINES_v3.7.txt")
augment.add_tool("tools/analyze_dependencies.py")
augment.add_context("examples/simple-api/")
```

### مع GitHub Copilot:

```python
# في .github/copilot-instructions.md
# أضف:
"""
Use Global Guidelines from:
- Prompt: GLOBAL_GUIDELINES_v3.7.txt
- Tools: tools/
- Examples: examples/
- Templates: templates/
"""
```

### مع Cursor:

```json
// في .cursor/settings.json
{
  "cursor.rules": [
    "Follow GLOBAL_GUIDELINES_v3.7.txt",
    "Use tools/ for analysis",
    "Reference examples/ for patterns"
  ]
}
```

---

## 9. Troubleshooting / حل المشاكل

### Issue 1: الأدوات لا تعمل

```bash
# تأكد من Python version
python --version  # يجب أن يكون >= 3.8

# ثبت المتطلبات
pip install -r requirements.txt

# شغل مع verbose
python tools/analyze_dependencies.py . --verbose
```

### Issue 2: Templates لا تعمل

```bash
# تأكد من البنية
ls -la templates/config/definitions/

# تأكد من __init__.py
cat templates/config/definitions/__init__.py
```

### Issue 3: Examples لا تشتغل

```bash
# تأكد من المتطلبات
cd examples/simple-api/
pip install -r requirements.txt

# شغل مع debug
python main.py --debug
```

---

## 10. References / المراجع

### الوثائق الرئيسية:
- [GLOBAL_GUIDELINES_v3.7.txt](../GLOBAL_GUIDELINES_v3.7.txt)
- [INIT_PY_BEST_PRACTICES.md](../INIT_PY_BEST_PRACTICES.md)
- [OSF_FRAMEWORK.md](../OSF_FRAMEWORK.md)

### Workflows:
- [DEVELOPMENT_FLOW.md](../flows/DEVELOPMENT_FLOW.md)
- [INTEGRATION_FLOW.md](../flows/INTEGRATION_FLOW.md)
- [DEPLOYMENT_FLOW.md](../flows/DEPLOYMENT_FLOW.md)

### Tools Documentation:
- [tools/README.md](../tools/README.md)

### Scripts Documentation:
- [scripts/README.md](../scripts/README.md)

---

## Summary / الملخص

مستودع Global Guidelines يوفر:

✅ **4 أدوات احترافية** للتحليل والصيانة  
✅ **قوالب جاهزة** لـ config/definitions  
✅ **3 أمثلة كاملة** لأنماط مختلفة  
✅ **5 سكريبتات** للتكامل السلس  
✅ **3 workflows** شاملة  
✅ **توثيق شامل** لكل شيء

**للاستخدام في Augment:**
1. انسخ البرومبت
2. انسخ الأدوات
3. انسخ الأمثلة
4. أشر إليها في التكوين
5. ابدأ العمل!

---

**Last Updated:** 2025-11-02  
**Version:** 3.9.0  
**Status:** ✅ Active

================================================================================
END OF SECTION 63
================================================================================

