# 📋 استراتيجية التفريع والإصدار - Store ERP

## نظرة عامة

يستخدم مشروع **Store ERP** استراتيجية **GitHub Flow** المُحسّنة، وهي استراتيجية بسيطة وفعّالة مصممة للفرق الصغيرة التي تنشر بشكل متكرر.

---

## 🔄 استراتيجية GitHub Flow

### هيكل الفروع الأساسي

```
main (الإنتاج)
  ↑
  ├── feature/* (ميزات جديدة)
  ├── bugfix/*  (إصلاحات)
  ├── hotfix/*  (إصلاحات طارئة)
  └── develop   (فرع التطوير - اختياري)
```

### أنواع الفروع

| نوع الفرع | الغرض | من | إلى |
|-----------|-------|-----|-----|
| `main` | الشيفرة في الإنتاج | - | PR → release |
| `feature/*` | ميزات جديدة | main | PR → main |
| `bugfix/*` | إصلاحات عادية | main | PR → main |
| `hotfix/*` | إصلاحات طارئة | main | PR → main |
| `develop` | فرع تطوير (اختياري) | main | PR → main |

---

## 🚀 سير العمل الكامل

### 1️⃣ إنشاء ميزة جديدة

```bash
# 1. تحديث main الحالي
git checkout main
git pull origin main

# 2. إنشاء فرع الميزة
git checkout -b feature/user-authentication

# 3. العمل والالتزام
git add .
git commit -m "feat: add user authentication system"

# 4. دفع الفرع
git push -u origin feature/user-authentication
```

**صيغة الـ Commit:**
```
feat: add user authentication
fix: resolve login validation error
docs: update README
refactor: improve database queries
test: add unit tests for auth
```

### 2️⃣ فتح طلب السحب (Pull Request)

**عند فتح PR:**
1. ملء نموذج PR المُعدّ مسبقاً
2. انتظار فحوصات CI (اختبارات، linting)
3. طلب المراجعة (إن لزم الأمر)
4. معالجة التعليقات والتحديثات

**قالب PR التلقائي:** ([.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md))

### 3️⃣ مراجعة والموافقة

- ✅ جميع اختبارات CI تمر
- ✅ لا توجد ملاحظات
- ✅ موافقة من مالك الكود (CODEOWNERS)

### 4️⃣ دمج في main

```bash
# الخيار 1: دمج مباشر من GitHub
# اضغط "Squash and merge" أو "Merge"

# الخيار 2: دمج محلي
git checkout main
git pull origin main
git merge --no-ff feature/user-authentication
git push origin main

# 5. حذف الفرع
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

---

## 🚨 الإصلاحات الطارئة (Hotfix)

### الحالات التي تتطلب Hotfix

- خطأ حرج يؤثر على المستخدمين
- ثغرة أمنية
- مشكلة في الأداء

### سير عمل Hotfix

```bash
# 1. إنشاء فرع من آخر إصدار
git checkout -b hotfix/v1.0.1 main

# 2. إصلاح المشكلة وعمل commit
git add .
git commit -m "fix: إصلاح critical database timeout issue

BREAKING CHANGE: none
Fixes #123"

# 3. دفع الفرع
git push origin hotfix/v1.0.1

# 4. فتح PR وحل المشكلة
# (اتبع نفس خطوات الـ feature إلى هنا)

# 5. دمج في main
git checkout main
git merge --no-ff hotfix/v1.0.1
git push origin main

# 6. إنشاء علامة إصدار
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git push origin v1.0.1

# 7. دمج في develop (مهم جداً!)
git checkout develop
git merge --no-ff hotfix/v1.0.1
git push origin develop

# 8. حذف الفرع
git branch -d hotfix/v1.0.1
git push origin --delete hotfix/v1.0.1
```

---

## 📦 الإصدارات والإصدار الدلالي

### الإصدار الدلالي (Semantic Versioning)

تنسيق: **MAJOR.MINOR.PATCH** (مثال: 1.2.3)

```
1.2.3
│ │ └─ PATCH: إصلاحات أخطاء (1.2.4)
│ └─── MINOR: ميزات جديدة (1.3.0)
└───── MAJOR: تغييرات كاسرة (2.0.0)
```

### أنواع الإصدارات

| الإصدار | الحالات | مثال |
|--------|--------|------|
| MAJOR | تغييرات كاسرة | إزالة API، تغيير بنية البيانات |
| MINOR | ميزات جديدة متوافقة | إضافة endpoint جديد |
| PATCH | إصلاحات أخطاء | إصلاح خطأ في التحقق |

### مثال على الإصدار

```bash
# 1. التأكد من أن main محدّث وجميع الاختبارات تمر
git checkout main
git pull origin main
npm test  # أو pytest

# 2. تشغيل سير عمل الإصدار
# انتقل إلى GitHub Actions → Release → Run workflow
# اختر:
#   - Release type: patch/minor/major
#   - Target branch: main

# 3. يتم التالي تلقائياً:
#   ✅ حساب النسخة الجديدة
#   ✅ تشغيل جميع الاختبارات
#   ✅ تحديث CHANGELOG
#   ✅ إنشاء Git tag (v1.2.3)
#   ✅ إنشاء GitHub Release
#   ✅ النشر التلقائي للإنتاج
```

---

## 🔐 قواعد حماية الفروع

### Checks المطلوبة قبل دمج PR

```yaml
قبل دمج في main يجب:
✅ تمرير جميع CI checks
✅ لا توجد conflicts
✅ الفرع محدّث مع main
✅ CODEOWNERS يوافق
```

### إعدادات GitHub (قريباً)

في Settings → Branches → Branch protection rules:

1. **Pattern:** `main`
2. **قواعد الحماية:**
   - ✅ Require pull request reviews (1 approval)
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Restrict who can push

---

## 📝 Conventional Commits

صيغة الالتزام الموحّدة:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### أنواع الـ Commits

```bash
# Feature (ميزة)
git commit -m "feat(auth): add JWT token validation"

# Fix (إصلاح)
git commit -m "fix(database): resolve connection timeout"

# Docs (توثيق)
git commit -m "docs: update API documentation"

# Refactor (إعادة هيكلة)
git commit -m "refactor(core): improve performance"

# Test (اختبارات)
git commit -m "test: add unit tests for parser"

# Breaking change (تغيير كاسر)
git commit -m "feat!: change API response format

BREAKING CHANGE: API now returns JSON instead of XML"
```

---

## 🔄 GitHub Actions Workflows

### الـ Workflows المتوفرة

#### 1. CI Pipeline (`github-flow-ci.yml`)

**يعمل على:**
- كل push إلى أي فرع
- كل pull request

**الخطوات:**
```
Lint Backend → Lint Frontend
                    ↓
              Test Backend → Build Backend
              
Build Frontend ← (متوازي)

CI Status Check (ملخص نهائي)
```

#### 2. Hotfix (`hotfix.yml`)

**يعمل على:** تشغيل يدوي فقط

**الخطوات:**
```
Validate Hotfix
      ↓
Deploy to Staging (اختياري)
      ↓
Deploy to Production
      ↓
Create Release Tag
      ↓
Notify Teams
```

#### 3. Release (`release.yml`)

**يعمل على:** تشغيل يدوي فقط

**الخطوات:**
```
Calculate Version
      ↓
Run Final Tests
      ↓
Update CHANGELOG
      ↓
Create Release
      ↓
Deploy (if main)
```

---

## 📊 مثال عملي كامل

### السيناريو: إضافة نظام دفع جديد

```bash
# 1. البداية
git checkout main
git pull origin main

# 2. إنشاء فرع الميزة
git checkout -b feature/payment-gateway

# 3. التطوير
# ... عمل على الملفات ...

# 4. الالتزام
git add .
git commit -m "feat(payments): add Stripe payment integration

- Implement Stripe API integration
- Add payment processing endpoints
- Add error handling and logging

Closes #42"

# 5. دفع الفرع
git push -u origin feature/payment-gateway

# 6. فتح PR على GitHub
# - URL: https://github.com/hamfarid/store-erp/pull/new/feature/payment-gateway
# - الوصف: ملء النموذج التلقائي
# - انتظار الفحوصات

# 7. بعد الموافقة، دمج من GitHub
# ("Squash and merge" أو "Create a merge commit")

# 8. حذف الفرع محلياً (اختياري)
git checkout main
git pull origin main
git branch -d feature/payment-gateway
```

---

## 📚 موارد إضافية

### الملفات المهمة

- [CODEOWNERS](.github/CODEOWNERS) - تحديد مسؤولي الكود
- [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) - نموذج PR
- [Workflows](.github/workflows/) - أتمتة CI/CD

### الأوامر المفيدة

```bash
# عرض الفروع المحلية
git branch

# عرض جميع الفروع (محلي + بعيد)
git branch -a

# حذف فرع محلي
git branch -d feature/my-feature

# حذف فرع بعيد
git push origin --delete feature/my-feature

# عرض آخر التزامات
git log --oneline -n 10

# عرض الفروع بتاريخ آخر تعديل
git branch -v

# البحث عن commits بحسب الرسالة
git log --all --grep="payment"
```

---

## 🎯 أفضل الممارسات

### ✅ يجب

- ✅ استخدم فروع منفصلة لكل ميزة
- ✅ اجعل الـ commits صغيرة وملفتة للنظر
- ✅ اكتب رسائل commits واضحة
- ✅ اختبر قبل فتح PR
- ✅ اطلب مراجعة من الزملاء
- ✅ حدّث الفرع قبل الدمج
- ✅ اترك تعليقات مفيدة في PR

### ❌ لا تفعل

- ❌ لا تعمل مباشرة على main
- ❌ لا تدمج بدون اختبارات
- ❌ لا تترك فروع قديمة معلقة
- ❌ لا تكتب commits برسائل غير واضحة
- ❌ لا تتجاهل تعليقات المراجعة

---

## 📞 الدعم والمساعدة

**لديك سؤال أو مشكلة؟**

1. تحقق من هذه الوثيقة أولاً
2. ابحث في GitHub Issues
3. اطلب المساعدة من الفريق
4. افتح GitHub Discussion

---

## 📅 ملخص التواريخ المهمة

- **تاريخ الإنشاء:** 5 فبراير 2026
- **آخر تحديث:** 5 فبراير 2026
- **النسخة:** 1.0.0

---

**آخر تحديث:** فبراير 2026  
**الحالة:** ✅ نشط وجاهز للاستخدام
