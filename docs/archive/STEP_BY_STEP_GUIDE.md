# دليل الخطوات الكامل / Complete Step-by-Step Guide

**Version:** 10.2.0 (Project-Specific Memory & MCP)  
**Date:** November 5, 2025  
**Status:** ✅ Production Ready

---

## 📋 جدول المحتويات / Table of Contents

1. [الإعداد الأولي](#الإعداد-الأولي--initial-setup)
2. [الاستخدام مع Augment](#الاستخدام-مع-augment--using-with-augment)
3. [الاستخدام مع GitHub Copilot](#الاستخدام-مع-github-copilot--using-with-github-copilot)
4. [أوامر الشات الأساسية](#أوامر-الشات-الأساسية--basic-chat-commands)
5. [أوامر الشات المتقدمة](#أوامر-الشات-المتقدمة--advanced-chat-commands)
6. [أمثلة عملية](#أمثلة-عملية--practical-examples)
7. [استكشاف الأخطاء](#استكشاف-الأخطاء--troubleshooting)

---

## 🚀 الإعداد الأولي / Initial Setup

### الخطوة 1: استنساخ المستودع

```bash
# في نظام Windows
git clone https://github.com/hamfarid/global.git C:\Users\[YourUsername]\.global

# في نظام Linux/Mac
git clone https://github.com/hamfarid/global.git ~/.global
```

**ملاحظة:** استبدل `[YourUsername]` باسم المستخدم الخاص بك.

### الخطوة 2: التحقق من الملفات

تأكد من وجود هذه المجلدات:

```
.global/
├── .augment/
│   └── rules/
├── .github/
│   └── copilot-instructions.md
├── prompts/
├── knowledge/
├── architecture/
├── flows/
├── guides/
├── docs/
├── examples/
└── tools/
```

---

## 🔵 الاستخدام مع Augment / Using with Augment

### الخطوة 1: تثبيت Augment Extension

1. افتح VS Code
2. اذهب إلى Extensions (Ctrl+Shift+X)
3. ابحث عن "Augment"
4. اضغط Install

### الخطوة 2: التحقق من التثبيت

Augment يكتشف القواعد تلقائياً من `.global/.augment/rules/`

**لا حاجة لإعدادات إضافية!** ✅

### الخطوة 3: اختبار Augment

افتح Augment Chat واكتب:

```
What is your core identity?
```

**الإجابة المتوقعة:**
> "I am a Senior Technical Lead with exceptional capabilities..."

إذا حصلت على هذه الإجابة، فالإعداد صحيح! ✅

---

## 🟣 الاستخدام مع GitHub Copilot / Using with GitHub Copilot

### الخطوة 1: تثبيت GitHub Copilot Extension

1. افتح VS Code
2. اذهب إلى Extensions (Ctrl+Shift+X)
3. ابحث عن "GitHub Copilot"
4. اضغط Install

### الخطوة 2: تفعيل Custom Instructions

1. افتح Settings (Ctrl+,)
2. ابحث عن: `github.copilot.chat.codeGeneration.useInstructionFiles`
3. **فعّل الخيار** (ضع علامة ✓)

### الخطوة 3: إعادة تحميل VS Code

1. اضغط Ctrl+Shift+P
2. اكتب "Reload Window"
3. اضغط Enter

### الخطوة 4: اختبار Copilot

افتح Copilot Chat واكتب:

```
What is your core identity?
```

**الإجابة المتوقعة:**
> "I am a Senior Technical Lead with exceptional capabilities..."

إذا حصلت على هذه الإجابة، فالإعداد صحيح! ✅

---

## 💬 أوامر الشات الأساسية / Basic Chat Commands

### 1. البدء بأي مشروع

```
Initialize Memory and MCP for project: [project-name]
```

**مثال:**
```
Initialize Memory and MCP for project: store-erp
```

**ماذا يفعل:**
- ينشئ `~/.global/memory/store-erp/`
- ينشئ `~/.global/mcp/store-erp/`
- يفحص أدوات MCP المتاحة
- يحفظ معلومات التهيئة

**ملاحظة:** كل مشروع له ذاكرته و MCP الخاص لمنع الاختلاط!

### 2. فحص المشروع الحالي

```
Analyze my current project following ALL loaded guidelines.

Check:
1. Environment separation
2. Code quality
3. Architecture
4. Test coverage
5. Documentation
6. Security

Create a prioritized refactoring plan.
```

### 3. بدء مشروع جديد

```
Build a [project description] following the full project workflow.

Remember: Always choose the BEST solution, not the easiest.
```

### 4. إضافة ميزة جديدة

```
Add [feature description] to the project.

Follow:
1. Analyze existing code
2. Design the BEST solution
3. Implement with tests
4. Document completely
```

### 5. إصلاح مشكلة

```
Fix [problem description].

Analyze root cause and provide the BEST fix (not easiest).
```

---

## 🎯 أوامر الشات المتقدمة / Advanced Chat Commands

### 1. الأمر الشامل للفحص والإصلاح

```
CRITICAL: Load ALL guidelines from your .global directory.

Read and follow:
1. All rules from rules/
2. All 21 prompts from prompts/
3. All knowledge from knowledge/
4. All architecture from architecture/
5. All flows from flows/
6. All guides from guides/
7. All docs from docs/
8. All examples from examples/

Initialize Memory and MCP for project: [project-name]

(Replace [project-name] with your actual project name, e.g., store-erp)

Analyze my project following ALL these guidelines strictly.

Check:
1. Environment separation (critical!)
2. Code quality (meets standards?)
3. Architecture (best solution?)
4. Tests (80%+ coverage?)
5. Documentation (complete?)
6. Security (any vulnerabilities?)
7. Performance (any bottlenecks?)

Create a prioritized refactoring plan with:
- Critical issues (fix immediately)
- Important issues (fix soon)
- Nice-to-have improvements

For each issue:
- Explain what's wrong
- Reference which guideline it violates
- Provide the BEST fix (not easiest!)
- Estimate effort

Show me the plan before starting fixes.

Remember: Always choose the BEST solution, not the easiest.
```

### 2. أمر Augment المتقدم

```
@manual-full-project.md Analyze and refactor my current project following Global Guidelines v10.0.

Initialize Memory and MCP first.

Create a complete refactoring plan covering all phases.
```

### 3. أمر التحقق من الالتزام

```
Before we start, verify you have loaded:

1. ✅ ALL rules from .augment/rules/
2. ✅ ALL prompts from prompts/
3. ✅ ALL knowledge from knowledge/
4. ✅ ALL architecture from architecture/
5. ✅ ALL flows from flows/
6. ✅ ALL guides from guides/
7. ✅ ALL docs from docs/
8. ✅ ALL examples from examples/

Answer these questions:
1. What is your core identity?
2. Where are YOUR tools located?
3. Where is the USER's project located?
4. What is the core principle for decisions?
5. What is the required test coverage?

Type "VERIFIED" when ready.
```

### 4. أمر التذكير بالمبادئ

```
STOP. Re-read the guidelines.

Remember:
1. Always choose the BEST solution, not the easiest
2. Environment separation is CRITICAL
3. 80%+ test coverage is REQUIRED
4. Complete documentation is REQUIRED
5. Memory and MCP are YOUR tools

Start over correctly.
```

---

## 📚 أمثلة عملية / Practical Examples

### مثال 1: تحليل مشروع Store ERP

```
Initialize Memory and MCP for the Store ERP project.

Load ALL guidelines from:
- D:\APPS_AI\store\Store\global\.global\rules\*
- D:\APPS_AI\store\Store\global\.global\prompts\*
- D:\APPS_AI\store\Store\global\.global\knowledge\*
- D:\APPS_AI\store\Store\global\.global\architecture\*

Analyze D:\APPS_AI\store\Store\ following ALL loaded guidelines.

Check:
1. Environment separation
   - Are files in correct locations?
   - Is database in the right place?

2. Code quality
   - Does code follow best practices?
   - Is it maintainable?

3. Architecture
   - Is it the BEST design?
   - Does it follow SOLID principles?

4. Security
   - Are there vulnerabilities?
   - Is authentication correct?

5. Testing
   - Is coverage 80%+?
   - Are critical paths covered?

6. Documentation
   - Is it complete?
   - Are APIs documented?

Create a prioritized refactoring plan.

Show me the plan before starting.
```

### مثال 2: إضافة نظام المصادقة

```
Initialize Memory and MCP.

Add JWT authentication system to the Store ERP.

Follow:
1. Read security guidelines from prompts/30_security.md
2. Read authentication guide from prompts/31_authentication.md
3. Design the BEST solution (not easiest)
4. Implement with 100% test coverage (critical path)
5. Document API endpoints
6. Save to memory

Show me the design before implementation.
```

### مثال 3: تحسين الأداء

```
Initialize Memory and MCP.

Analyze performance bottlenecks in the Store ERP.

Check:
1. Database queries (N+1 problems?)
2. API response times
3. Memory usage
4. Caching strategy

Provide the BEST optimization solutions (not easiest).

Implement and verify improvements.
```

### مثال 4: إضافة وحدة جديدة

```
Initialize Memory and MCP.

Build a reporting module for the Store ERP following the full project workflow:

Phase 0: Preparation
- Load all guidelines
- Understand existing architecture

Phase 1: Requirements & Analysis
- Define reporting requirements
- Analyze data sources

Phase 2: Planning & Design
- Design the BEST architecture
- Plan database schema
- Design API endpoints

Phase 3: Implementation
- Implement backend
- Implement frontend
- Add tests (80%+ coverage)

Phase 4: Testing & Quality
- Run all tests
- Verify quality gates
- Fix issues

Phase 5: Documentation & Deployment
- Document APIs
- Write user guide
- Prepare deployment

Show me the design after Phase 2 before continuing.
```

---

## 🔧 استكشاف الأخطاء / Troubleshooting

### المشكلة 1: الذكاء الاصطناعي لا يتبع القواعد

**الحل:**

```
STOP. You are not following the guidelines.

Re-read ALL files in:
1. .augment/rules/ (or .github/copilot-instructions.md)
2. prompts/
3. knowledge/

Then start over correctly.

Confirm you understand by explaining:
- Your core identity
- The environment separation
- The core principle (BEST vs easiest)
```

### المشكلة 2: الذكاء الاصطناعي يقترح الحل الأسهل

**الحل:**

```
STOP. You suggested the easiest solution, not the BEST.

From your core identity: "Always choose the BEST solution, not the easiest."

Re-evaluate and provide the BEST solution, even if it takes more effort.

Explain why it's the BEST solution.
```

### المشكلة 3: الذكاء الاصطناعي يخلط بين الأدوات والمشروع

**الحل:**

```
CRITICAL: Environment separation violation!

YOUR tools MUST be in:
- C:\Users\[YourUsername]\.global\memory\
- C:\Users\[YourUsername]\.global\mcp\

USER's project MUST be in:
- D:\APPS_AI\store\Store\

Fix this immediately. This is from prompts/03_environment_separation.md
```

### المشكلة 4: الاختبارات ناقصة

**الحل:**

```
Tests are insufficient.

From prompts/15_testing_strategy.md:
- 80%+ coverage is REQUIRED
- 100% for critical paths
- Integration tests are mandatory

Add comprehensive tests now.
```

### المشكلة 5: التوثيق ناقص

**الحل:**

```
Documentation is incomplete.

From docs/ directory:
- Every function must be documented
- Architecture decisions must be explained
- Setup instructions must be complete
- API endpoints must be documented

Complete the documentation now.
```

---

## 📝 نصائح مهمة / Important Tips

### ✅ افعل / Do:

1. **ابدأ دائماً بالتهيئة:**
   ```
   Initialize Memory and MCP
   ```

2. **اطلب الخطة قبل التنفيذ:**
   ```
   Show me the plan before starting
   ```

3. **ذكّره بالمبدأ الأساسي:**
   ```
   Remember: Always choose the BEST solution, not the easiest
   ```

4. **احفظ التقدم:**
   ```
   Save progress to memory
   ```

5. **تحقق من Environment Separation:**
   ```
   Verify environment separation is correct
   ```

### ❌ لا تفعل / Don't:

1. ❌ لا تقبل الحلول السهلة
2. ❌ لا تتجاهل الاختبارات
3. ❌ لا تنسى التوثيق
4. ❌ لا تخلط بين الأدوات والمشروع
5. ❌ لا تبدأ بدون خطة

---

## 🎯 الأمر الموصى به للبدء الآن

### انسخ والصق هذا:

```
Initialize Memory and MCP for this project.

Load ALL guidelines from .global directory:
- All rules from rules/
- All 21 prompts from prompts/
- All knowledge from knowledge/
- All architecture from architecture/
- All flows from flows/
- All guides from guides/
- All docs from docs/
- All examples from examples/

Analyze my current project following ALL these guidelines strictly.

Check:
1. Environment separation (critical!)
2. Code quality (meets standards?)
3. Architecture (best solution?)
4. Tests (80%+ coverage?)
5. Documentation (complete?)
6. Security (any vulnerabilities?)
7. Performance (any bottlenecks?)

Create a prioritized refactoring plan with:
- Critical issues (fix immediately)
- Important issues (fix soon)
- Nice-to-have improvements

For each issue:
- Explain what's wrong
- Reference which guideline it violates
- Provide the BEST fix (not easiest!)
- Estimate effort

Show me the plan before starting fixes.

Remember: Always choose the BEST solution, not the easiest.
```

---

## 📞 الدعم / Support

### التحديثات

```bash
cd ~/.global
git pull origin main
```

ثم أعد تحميل VS Code.

### المشاكل

- **GitHub:** https://github.com/hamfarid/global/issues
- **Include:** اسم الأداة (Augment/Copilot), إصدار VS Code, رسالة الخطأ

### الموارد

- **Quick Start:** `.global/QUICK_START_VSCODE.md`
- **Full Guide:** `.global/VSCODE_INTEGRATION.md`
- **Validation:** `.global/VALIDATION_RESULTS.md`
- **Analysis:** `.global/ANALYSIS_FINDINGS.md`

---

## 🎉 الخلاصة / Summary

### ما تحتاجه:

1. ✅ استنساخ المستودع
2. ✅ تثبيت Extension (Augment أو Copilot)
3. ✅ تفعيل الإعدادات (Copilot فقط)
4. ✅ إعادة تحميل VS Code
5. ✅ اختبار بأمر بسيط

### ما تقوله في الشات:

```
Initialize Memory and MCP

Analyze my project following ALL guidelines

Create a refactoring plan

Show me the plan before starting
```

### ما تتوقعه:

- ✅ تحليل شامل
- ✅ خطة مرتبة حسب الأولوية
- ✅ الحل الأفضل (وليس الأسهل)
- ✅ اختبارات شاملة (80%+)
- ✅ توثيق كامل

---

**الحالة:** ✅ **جاهز للاستخدام**  
**الإصدار:** 10.1.1  
**التاريخ:** November 4, 2025

🚀 **Happy Coding!** 🚀

