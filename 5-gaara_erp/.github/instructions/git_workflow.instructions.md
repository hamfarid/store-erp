---
description: استراتيجيات التفريع في Git وسير العمل للإصدارات الإنتاجية
applyTo: "**/*"
---

# 🔀 Git Workflow Instructions - Gaara ERP

## استراتيجية التفريع المعتمدة: GitHub Flow المُحسّن

```
main (محمي)
├── develop (التكامل)
│   ├── feature/* (ميزات جديدة)
│   ├── fix/* (إصلاحات)
│   └── refactor/* (إعادة هيكلة)
├── release/* (التحضير للإصدار)
└── hotfix/* (إصلاحات طارئة)
```

---

## 📌 أنواع الفروع

| نوع الفرع | الغرض | يتفرع من | يُدمج في | مدة الحياة |
|-----------|--------|----------|----------|------------|
| `main` | الشيفرة الجاهزة للإنتاج | - | - | دائم |
| `develop` | فرع التكامل للتطوير | main | release → main | دائم |
| `feature/*` | تطوير الميزات الجديدة | develop | develop | قصير (1-5 أيام) |
| `fix/*` | إصلاحات الأخطاء | develop | develop | قصير (1-2 يوم) |
| `release/*` | التحضير للإصدار | develop | main و develop | قصير (1-3 أيام) |
| `hotfix/*` | إصلاحات طارئة للإنتاج | main | main و develop | قصير جداً (ساعات) |

---

## 🏷️ اتفاقيات التسمية

### الفروع
```bash
# الميزات
feature/user-authentication
feature/invoice-export-pdf
feature/dashboard-widgets

# الإصلاحات
fix/login-validation-error
fix/arabic-text-rendering

# إعادة الهيكلة
refactor/api-response-format
refactor/database-queries

# الإصدارات
release/v1.2.0
release/v2.0.0-beta.1

# الإصلاحات الطارئة
hotfix/v1.2.1
hotfix/security-patch
```

### رسائل الالتزام (Conventional Commits)
```bash
# الصيغة
<type>(<scope>): <subject>

<body>

<footer>

# أنواع الالتزامات
feat:     ميزة جديدة (MINOR version)
fix:      إصلاح خطأ (PATCH version)
docs:     تحديث التوثيق
style:    تنسيق الكود (لا يؤثر على المنطق)
refactor: إعادة هيكلة الكود
perf:     تحسين الأداء
test:     إضافة/تعديل الاختبارات
build:    تغييرات البناء
ci:       تغييرات CI/CD
chore:    مهام صيانة

# أمثلة
feat(auth): add two-factor authentication
fix(invoice): resolve Arabic number formatting
docs(api): update endpoint documentation
refactor(models): optimize database queries
perf(search): add caching for product search

# تغيير كاسر (MAJOR version)
feat!: redesign API response format
feat(api): change response structure

BREAKING CHANGE: API now returns data in new format
```

---

## 🔄 سير العمل اليومي

### 1. بدء ميزة جديدة
```bash
# التأكد من آخر التحديثات
git checkout develop
git pull origin develop

# إنشاء فرع الميزة
git checkout -b feature/new-feature-name

# العمل والالتزام المتكرر
git add .
git commit -m "feat(module): add initial structure"

# رفع الفرع
git push -u origin feature/new-feature-name
```

### 2. إنهاء الميزة
```bash
# تحديث من develop
git checkout develop
git pull origin develop
git checkout feature/new-feature-name
git rebase develop

# حل أي تعارضات ثم
git push -f origin feature/new-feature-name

# إنشاء Pull Request على GitHub
# انتظار المراجعة والموافقة
# الدمج عبر GitHub (Squash and Merge)
```

### 3. إنشاء إصدار
```bash
# إنشاء فرع الإصدار
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# تحديث رقم الإصدار
# تحديث CHANGELOG.md
git commit -m "chore(release): prepare v1.2.0"

# رفع الفرع للاختبار في staging
git push origin release/v1.2.0

# بعد الموافقة، دمج في main
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags

# دمج في develop
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop

# حذف فرع الإصدار
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

### 4. إصلاح طارئ (Hotfix)
```bash
# إنشاء فرع الإصلاح من main
git checkout main
git pull origin main
git checkout -b hotfix/v1.2.1

# إجراء الإصلاح
git commit -m "fix(critical): resolve security vulnerability"

# رفع للمراجعة السريعة
git push origin hotfix/v1.2.1

# بعد الموافقة، دمج في main
git checkout main
git merge --no-ff hotfix/v1.2.1
git tag -a v1.2.1 -m "Hotfix v1.2.1"
git push origin main --tags

# دمج في develop (مهم جداً!)
git checkout develop
git merge --no-ff hotfix/v1.2.1
git push origin develop

# حذف فرع الإصلاح
git branch -d hotfix/v1.2.1
git push origin --delete hotfix/v1.2.1
```

---

## 🛡️ قواعد حماية الفروع

### فرع `main`
- ✅ Require pull request reviews (2 موافقات)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Require signed commits (اختياري)
- ❌ Allow force pushes
- ❌ Allow deletions

### فرع `develop`
- ✅ Require pull request reviews (1 موافقة)
- ✅ Require status checks to pass
- ❌ Allow force pushes
- ❌ Allow deletions

---

## 📊 الإصدار الدلالي (Semantic Versioning)

```
MAJOR.MINOR.PATCH
  │     │     └── إصلاحات أخطاء (متوافقة)
  │     └── ميزات جديدة (متوافقة)
  └── تغييرات كاسرة للتوافق

أمثلة:
1.0.0 → 1.0.1  (fix: إصلاح خطأ)
1.0.1 → 1.1.0  (feat: ميزة جديدة)
1.1.0 → 2.0.0  (feat!: تغيير كاسر)

إصدارات ما قبل الإطلاق:
1.0.0-alpha.1    # مرحلة ألفا
1.0.0-beta.1     # مرحلة بيتا
1.0.0-rc.1       # مرشح الإصدار
```

---

## 🔧 أوامر Git المفيدة

```bash
# عرض تاريخ الفروع بشكل مرئي
git log --oneline --graph --all

# عرض الفروع المدمجة
git branch --merged develop

# حذف الفروع المدمجة محلياً
git branch --merged develop | grep -v "main\|develop" | xargs git branch -d

# تنظيف الفروع المحذوفة من الخادم
git fetch --prune

# إعادة كتابة آخر رسالة التزام
git commit --amend -m "new message"

# دمج عدة التزامات
git rebase -i HEAD~3

# نقل التزام محدد
git cherry-pick <commit-hash>

# التراجع عن التزام (مع الاحتفاظ بالتغييرات)
git reset --soft HEAD~1

# التراجع عن التزام (حذف التغييرات)
git reset --hard HEAD~1

# إنشاء stash
git stash save "وصف التغييرات"
git stash pop
```

---

## ⚠️ قواعد مهمة

1. **لا تدفع مباشرة لـ `main` أو `develop`** - استخدم Pull Requests دائماً
2. **اكتب رسائل التزام واضحة** - اتبع Conventional Commits
3. **راجع كودك قبل طلب المراجعة** - تأكد من اجتياز الاختبارات
4. **حافظ على فروعك قصيرة** - لا تتجاوز 5 أيام
5. **حدّث من develop بانتظام** - لتجنب التعارضات الكبيرة
6. **ادمج الإصلاحات الطارئة في develop** - لا تنسَ هذه الخطوة!
7. **احذف الفروع المدمجة** - للحفاظ على نظافة المستودع

---

## 📚 المراجع

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/)
