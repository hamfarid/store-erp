# Flows - سير العمل

## نظرة عامة / Overview

هذا المجلد يحتوي على جميع ملفات سير العمل (Flows) للمشاريع المبنية باستخدام Global Guidelines.

This directory contains all workflow files (Flows) for projects built using Global Guidelines.

---

## الملفات المتوفرة / Available Files

### 1. [DEVELOPMENT_FLOW.md](./DEVELOPMENT_FLOW.md)
**سير عمل التطوير الكامل**

يغطي:
- ✅ Project Initialization
- ✅ Development Setup
- ✅ Development Workflow
- ✅ Quality Assurance
- ✅ Documentation
- ✅ Testing
- ✅ Deployment Preparation

**متى تستخدمه:** عند بدء مشروع جديد أو تطوير features جديدة

---

### 2. [INTEGRATION_FLOW.md](./INTEGRATION_FLOW.md)
**دمج Global Guidelines في مشاريع قائمة**

يغطي:
- ✅ طرق الدمج المختلفة
- ✅ التثبيت بدون تأثير على Git
- ✅ التكوين والتطبيق
- ✅ الاستخدام اليومي
- ✅ التحديث والإزالة

**متى تستخدمه:** عند دمج Global Guidelines في مشروع قائم

---

### 3. [DEPLOYMENT_FLOW.md](./DEPLOYMENT_FLOW.md)
**نشر المشاريع إلى الإنتاج**

يغطي:
- ✅ Pre-deployment Checklist
- ✅ Deployment Strategies
- ✅ Docker & Kubernetes
- ✅ CI/CD Pipelines
- ✅ Monitoring & Rollback

**متى تستخدمه:** عند نشر المشروع إلى staging أو production

---

## مسار العمل الكامل / Complete Workflow

```
┌─────────────────────────────────────────────────────────┐
│                   1. Start New Project                   │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  DEVELOPMENT_FLOW.md                           │    │
│  │  - Initialize project                          │    │
│  │  - Setup development environment               │    │
│  │  - Develop features                            │    │
│  │  - Quality assurance                           │    │
│  │  - Documentation                               │    │
│  │  - Testing                                     │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              2. Integrate into Existing Project          │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  INTEGRATION_FLOW.md                           │    │
│  │  - Choose integration method                   │    │
│  │  - Install without affecting Git               │    │
│  │  - Configure components                        │    │
│  │  - Apply to project                            │    │
│  │  - Daily usage                                 │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   3. Deploy to Production                │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  DEPLOYMENT_FLOW.md                            │    │
│  │  - Pre-deployment checks                       │    │
│  │  - Choose deployment strategy                  │    │
│  │  - Build & deploy                              │    │
│  │  - Monitor & verify                            │    │
│  │  - Rollback if needed                          │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Start / البدء السريع

### Scenario 1: مشروع جديد

```bash
# 1. Clone Global Guidelines
git clone https://github.com/hamfarid/global.git
cd global

# 2. اتبع DEVELOPMENT_FLOW.md
cat flows/DEVELOPMENT_FLOW.md

# 3. ابدأ التطوير
# ... follow the steps in DEVELOPMENT_FLOW.md
```

---

### Scenario 2: مشروع قائم

```bash
# 1. انتقل لمشروعك
cd /path/to/your/project

# 2. ادمج Global Guidelines
curl -sSL https://raw.githubusercontent.com/hamfarid/global/main/scripts/integrate.sh | bash

# 3. اتبع INTEGRATION_FLOW.md
cat .global/flows/INTEGRATION_FLOW.md

# 4. طبق المكونات
.global/scripts/configure.sh
.global/scripts/apply.sh
```

---

### Scenario 3: نشر للإنتاج

```bash
# 1. اتبع DEPLOYMENT_FLOW.md
cat .global/flows/DEPLOYMENT_FLOW.md

# 2. Pre-deployment checks
pytest --cov=.
flake8 .
mypy .

# 3. Deploy
# ... follow the steps in DEPLOYMENT_FLOW.md
```

---

## مقارنة الـ Flows / Flows Comparison

| Flow | الهدف | المدة المتوقعة | التعقيد |
|------|-------|----------------|---------|
| **Development** | تطوير features جديدة | أيام-أسابيع | ⭐⭐⭐ |
| **Integration** | دمج في مشروع قائم | ساعات | ⭐⭐ |
| **Deployment** | نشر للإنتاج | ساعات | ⭐⭐⭐⭐ |

---

## Best Practices / أفضل الممارسات

### 1. اتبع الترتيب

```
Development → Integration → Deployment
```

لا تقفز مباشرة للـ deployment بدون اتباع development flow.

### 2. استخدم Checklists

كل flow يحتوي على checklists - استخدمها!

```markdown
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3
```

### 3. وثق الانحرافات

إذا انحرفت عن الـ flow، وثق السبب:

```markdown
## Deviations from Standard Flow

### Why we skipped step X
- Reason 1
- Reason 2

### Why we added step Y
- Reason 1
- Reason 2
```

### 4. شارك مع الفريق

تأكد أن الفريق كله يفهم الـ flows:

```bash
# أضف للـ README
cat >> README.md << EOF

## Development Workflow

We follow the Global Guidelines flows:
- Development: .global/flows/DEVELOPMENT_FLOW.md
- Integration: .global/flows/INTEGRATION_FLOW.md
- Deployment: .global/flows/DEPLOYMENT_FLOW.md
EOF
```

---

## Customization / التخصيص

### إنشاء Flow مخصص

```bash
# انسخ flow موجود
cp flows/DEVELOPMENT_FLOW.md flows/CUSTOM_FLOW.md

# عدّل حسب احتياجاتك
vim flows/CUSTOM_FLOW.md

# شارك مع الفريق
git add flows/CUSTOM_FLOW.md
git commit -m "docs: add custom flow for X"
```

### دمج Flows متعددة

يمكنك دمج خطوات من flows مختلفة:

```markdown
# CUSTOM_COMBINED_FLOW.md

## Phase 1: Setup
(من INTEGRATION_FLOW.md)

## Phase 2: Development
(من DEVELOPMENT_FLOW.md)

## Phase 3: Deployment
(من DEPLOYMENT_FLOW.md)
```

---

## Troubleshooting / حل المشاكل

### Issue: Flow غير واضح

**الحل:**
1. اقرأ الأمثلة في كل flow
2. راجع الـ FAQ في نهاية كل flow
3. افتح issue على GitHub

### Issue: Flow لا يناسب مشروعي

**الحل:**
1. خذ ما يناسبك فقط
2. خصص flow لمشروعك
3. وثق التخصيصات
4. شارك مع المجتمع

### Issue: خطوة معينة لا تعمل

**الحل:**
1. راجع الـ Troubleshooting section في الـ flow
2. تحقق من الـ prerequisites
3. اطلب المساعدة من الفريق

---

## Contributing / المساهمة

### تحسين Flow موجود

```bash
# 1. Fork the repo
# 2. Create branch
git checkout -b improve-development-flow

# 3. Make changes
vim flows/DEVELOPMENT_FLOW.md

# 4. Commit
git commit -m "docs: improve development flow clarity"

# 5. Push and create PR
git push origin improve-development-flow
```

### إضافة Flow جديد

```bash
# 1. Create new flow
vim flows/NEW_FLOW.md

# 2. Follow template structure
# - Overview
# - Phases
# - Best Practices
# - Examples
# - Troubleshooting

# 3. Update this README
vim flows/README.md

# 4. Submit PR
```

---

## Templates / القوالب

### Flow Template

```markdown
# FLOW_NAME - عنوان بالعربية

## نظرة عامة / Overview
...

## المراحل / Phases

### Phase 1: Name
...

### Phase 2: Name
...

## Best Practices / أفضل الممارسات
...

## Examples / أمثلة
...

## Troubleshooting / حل المشاكل
...

## References / المراجع
...
```

---

## Resources / الموارد

### Documentation
- [Global Guidelines](../GLOBAL_GUIDELINES_v3.7.txt)
- [Quick Start](../QUICK_START.md)
- [Contributing](../CONTRIBUTING.md)

### Tools
- [analyze_dependencies.py](../tools/analyze_dependencies.py)
- [detect_code_duplication.py](../tools/detect_code_duplication.py)
- [smart_merge.py](../tools/smart_merge.py)
- [update_imports.py](../tools/update_imports.py)

### Examples
- [Code Samples](../examples/code-samples/)
- [Simple API](../examples/simple-api/)
- [Init Patterns](../examples/init_py_patterns/)

---

## Feedback / التغذية الراجعة

هل لديك اقتراحات لتحسين الـ flows؟

- 📧 Email: [your-email]
- 🐛 Issues: https://github.com/hamfarid/global/issues
- 💬 Discussions: https://github.com/hamfarid/global/discussions

---

**Last Updated:** 2025-11-02  
**Version:** 1.0.0  
**Status:** ✅ Active

