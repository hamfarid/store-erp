# 🌿 دليل استراتيجيات التفريع وسير العمل | Git Branching Strategy Guide

دليل شامل لاستراتيجيات التفريع وسير العمل في مشروع **Gaara Scan AI**.

---

## 📋 جدول المحتويات

1. [نظرة عامة على الاستراتيجية](#-نظرة-عامة-على-الاستراتيجية)
2. [أنواع الفروع](#-أنواع-الفروع)
3. [سير العمل اليومي](#-سير-العمل-اليومي)
4. [إنشاء الإصدارات](#-إنشاء-الإصدارات)
5. [الإصلاحات الطارئة](#-الإصلاحات-الطارئة-hotfix)
6. [اتفاقيات الالتزامات](#-اتفاقيات-الالتزامات)
7. [قواعد حماية الفروع](#-قواعد-حماية-الفروع)
8. [أوامر Git الشائعة](#-أوامر-git-الشائعة)

---

## 🎯 نظرة عامة على الاستراتيجية

نستخدم استراتيجية **GitFlow المُعدّلة** التي تجمع بين:
- هيكلية GitFlow للإصدارات المنظمة
- سرعة GitHub Flow للتطوير اليومي
- مبادئ Trunk-Based للدمج المتكرر

```
main ─────●─────────●─────────●─────────● (إنتاج)
          │         ↑         ↑         ↑
          │    release/v1.0   │    hotfix/v1.0.1
          │         │         │         │
develop ──●─────────●─────────●─────────● (تطوير)
          │         │         │
     feature/auth   │    feature/search
                    │
               feature/profile
```

---

## 🌳 أنواع الفروع

### 1. `main` - فرع الإنتاج
```bash
# ⚠️ لا يتم الدفع إليه مباشرة أبداً
# يُحدّث فقط عبر:
# - دمج release/* 
# - دمج hotfix/*
```

**الحماية:**
- ✅ يتطلب 2 مراجعات
- ✅ يتطلب نجاح CI
- ✅ يتطلب مراجعة Code Owners
- ❌ لا يُسمح بالدفع المباشر

### 2. `develop` - فرع التطوير
```bash
# فرع التكامل الرئيسي
git checkout develop
git pull origin develop
```

**الحماية:**
- ✅ يتطلب 1 مراجعة
- ✅ يتطلب نجاح CI

### 3. `feature/*` - فروع الميزات
```bash
# إنشاء فرع ميزة جديدة
git checkout develop
git pull origin develop
git checkout -b feature/user-authentication

# العمل والالتزام
git add .
git commit -m "feat: add login form component"

# رفع الفرع
git push -u origin feature/user-authentication
```

**اتفاقيات التسمية:**
- `feature/user-auth` - ميزة المصادقة
- `feature/disease-detection` - ميزة تشخيص الأمراض
- `feature/123-add-search` - ميزة مرتبطة بـ issue #123

### 4. `release/*` - فروع الإصدار
```bash
# إنشاء فرع إصدار
git checkout develop
git checkout -b release/v1.2.0

# إصلاحات الإصدار فقط
git commit -m "fix: correct validation message"

# عند الانتهاء - يتم الدمج في main و develop
```

**اتفاقيات التسمية:**
- `release/v1.2.0` - بالإصدار
- `release/2026-02` - بالتاريخ
- `release/sprint-42` - بالسبرينت

### 5. `hotfix/*` - الإصلاحات الطارئة
```bash
# إنشاء hotfix من main
git checkout main
git pull origin main
git checkout -b hotfix/v1.0.1

# إصلاح طارئ
git commit -m "fix: critical database connection issue"
```

---

## 💻 سير العمل اليومي

### إضافة ميزة جديدة

```bash
# 1. تأكد أنك على develop محدّث
git checkout develop
git pull origin develop

# 2. أنشئ فرع الميزة
git checkout -b feature/add-crop-management

# 3. اعمل على الميزة مع التزامات صغيرة
git add .
git commit -m "feat: add crop model"
git commit -m "feat: add crop API endpoints"
git commit -m "test: add crop service tests"

# 4. ارفع الفرع
git push -u origin feature/add-crop-management

# 5. أنشئ Pull Request إلى develop
# من GitHub أو:
gh pr create --base develop --title "feat: Add crop management" --body "..."

# 6. بعد المراجعة والموافقة، ادمج
# (يُفضل Squash and Merge للتاريخ النظيف)

# 7. احذف الفرع
git checkout develop
git pull origin develop
git branch -d feature/add-crop-management
```

### مراجعة Pull Request

```bash
# جلب فرع PR للمراجعة المحلية
git fetch origin pull/123/head:pr-123
git checkout pr-123

# اختبار محلي
cd backend && pytest tests/
cd ../frontend && npm test

# إضافة تعليق على PR
gh pr review 123 --comment --body "يبدو جيداً، لكن يرجى..."

# الموافقة
gh pr review 123 --approve

# طلب تغييرات
gh pr review 123 --request-changes --body "يرجى إصلاح..."
```

---

## 📦 إنشاء الإصدارات

### الإصدار العادي

```bash
# 1. تأكد أن develop جاهز
git checkout develop
git pull origin develop

# 2. أنشئ فرع الإصدار
git checkout -b release/v1.2.0

# 3. حدّث رقم الإصدار
# في backend/src/core/config.py
# في frontend/package.json

# 4. إصلاحات أخيرة فقط (لا ميزات جديدة)
git commit -m "fix: typo in error message"
git commit -m "chore: update version to 1.2.0"

# 5. ارفع فرع الإصدار
git push -u origin release/v1.2.0

# 6. أنشئ PR إلى main
gh pr create --base main --title "Release v1.2.0"

# 7. بعد الموافقة والدمج، أنشئ العلامة
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release v1.2.0 - وصف التغييرات"
git push origin v1.2.0

# 8. ادمج في develop أيضاً
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop

# 9. احذف فرع الإصدار
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

### الإصدار الآلي (semantic-release)

```bash
# الإصدار يتم تلقائياً عند الدمج في main
# بناءً على صيغة الالتزامات:

# PATCH (1.0.x)
git commit -m "fix: resolve login issue"

# MINOR (1.x.0)
git commit -m "feat: add search functionality"

# MAJOR (x.0.0)
git commit -m "feat!: redesign API"
# أو
git commit -m "feat: update config format

BREAKING CHANGE: configuration now uses YAML"
```

---

## 🚨 الإصلاحات الطارئة (Hotfix)

### متى نستخدم Hotfix؟
- ❗ خطأ حرج يؤثر على المستخدمين
- 🔒 ثغرة أمنية
- 💾 مشكلة في البيانات

### خطوات Hotfix

```bash
# 1. أنشئ فرع من main
git checkout main
git pull origin main
git checkout -b hotfix/v1.0.1

# 2. أصلح المشكلة
git add .
git commit -m "fix: critical database timeout

- زيادة timeout الاتصال
- إضافة retry logic
- تحسين معالجة الأخطاء

Fixes #456"

# 3. اختبر محلياً
cd backend && pytest tests/
npm test

# 4. ارفع الفرع
git push -u origin hotfix/v1.0.1

# 5. أنشئ PR إلى main (مستعجل)
gh pr create --base main --title "🚨 Hotfix: Critical DB fix" --label "hotfix,urgent"

# 6. بعد المراجعة السريعة والموافقة

# 7. ادمج في main
git checkout main
git merge --no-ff hotfix/v1.0.1
git push origin main

# 8. أنشئ العلامة
git tag -a v1.0.1 -m "Hotfix v1.0.1 - إصلاح طارئ"
git push origin v1.0.1

# 9. ⚠️ مهم: ادمج في develop
git checkout develop
git pull origin develop
git merge --no-ff hotfix/v1.0.1
git push origin develop

# 10. احذف فرع الإصلاح
git branch -d hotfix/v1.0.1
git push origin --delete hotfix/v1.0.1
```

---

## 📝 اتفاقيات الالتزامات

نتبع معيار [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### أنواع الالتزامات

| النوع | الوصف | الإصدار |
|-------|-------|---------|
| `feat` | ميزة جديدة | MINOR |
| `fix` | إصلاح خطأ | PATCH |
| `docs` | توثيق فقط | - |
| `style` | تنسيق (لا يؤثر على الكود) | - |
| `refactor` | إعادة هيكلة | - |
| `perf` | تحسين أداء | PATCH |
| `test` | إضافة اختبارات | - |
| `chore` | صيانة عامة | - |
| `ci` | تغييرات CI/CD | - |

### أمثلة

```bash
# ميزة جديدة
git commit -m "feat(auth): add two-factor authentication"

# إصلاح خطأ
git commit -m "fix(api): resolve null pointer in user service"

# إصلاح مع نطاق
git commit -m "fix(frontend): correct RTL text alignment in Arabic"

# تغيير كاسر
git commit -m "feat(api)!: change response format to JSON:API

BREAKING CHANGE: All API responses now follow JSON:API spec.
Migration guide: https://..."

# إصلاح مرتبط بـ issue
git commit -m "fix(database): resolve connection timeout

Increases connection pool size and adds retry logic.

Fixes #123
Refs #456"
```

---

## 🛡️ قواعد حماية الفروع

### إعداد الحماية في GitHub

1. اذهب إلى **Settings → Branches → Add rule**
2. طبق الإعدادات التالية:

#### main (الإنتاج)
- ✅ Require pull request before merging
  - Required approvals: **2**
  - ✅ Dismiss stale approvals
  - ✅ Require Code Owner review
- ✅ Require status checks
  - ✅ Require up to date
  - Checks: `Lint Code`, `Test Backend`, `Test Frontend`, `Security Scan`
- ✅ Require conversation resolution
- ❌ Allow force pushes
- ❌ Allow deletions

#### develop (التطوير)
- ✅ Require pull request (1 approval)
- ✅ Require status checks

#### release/* و hotfix/*
- ✅ Require pull request (1 approval)
- ✅ Allow deletions (بعد الدمج)

---

## ⌨️ أوامر Git الشائعة

### التحديث والمزامنة

```bash
# تحديث جميع الفروع
git fetch --all --prune

# تحديث develop
git checkout develop && git pull origin develop

# تحديث main
git checkout main && git pull origin main

# عرض الفروع المدمجة
git branch --merged develop
```

### العلامات (Tags)

```bash
# عرض جميع العلامات
git tag -l "v*"

# إنشاء علامة موضحة
git tag -a v1.0.0 -m "Release v1.0.0"

# رفع علامة
git push origin v1.0.0

# رفع جميع العلامات
git push origin --tags

# حذف علامة محلية
git tag -d v1.0.0

# حذف علامة من الخادم
git push origin --delete v1.0.0
```

### Cherry-pick

```bash
# نقل التزام واحد
git cherry-pick abc123

# نقل مع مرجع
git cherry-pick -x abc123

# نقل عدة التزامات
git cherry-pick abc123 def456 ghi789

# التعامل مع التعارضات
git status
# حل التعارضات...
git add .
git cherry-pick --continue

# إلغاء
git cherry-pick --abort
```

### تنظيف

```bash
# حذف الفروع المدمجة محلياً
git branch --merged | grep -v "main\|develop" | xargs git branch -d

# حذف الفروع البعيدة المحذوفة
git fetch --prune

# عرض الفروع القديمة
git for-each-ref --sort=-committerdate refs/heads/ --format='%(committerdate:short) %(refname:short)'
```

---

## 🔗 الملفات ذات الصلة

- [CODEOWNERS](../.github/CODEOWNERS) - مالكو الكود
- [PR Template](../.github/PULL_REQUEST_TEMPLATE.md) - قالب طلب السحب
- [CI Workflow](../.github/workflows/ci.yml) - سير عمل CI
- [Release Workflow](../.github/workflows/release.yml) - سير عمل الإصدار
- [Hotfix Workflow](../.github/workflows/hotfix.yml) - سير عمل الإصلاحات

---

## 📞 المساعدة

للأسئلة أو المشاكل:
1. راجع [FAQ](./FAQ.md)
2. افتح [Issue](https://github.com/your-org/gaara-scan-ai/issues/new)
3. تواصل مع فريق DevOps

---

*آخر تحديث: 2026-02-05*
