# 🔐 Branch Protection Rules Configuration

## غرض هذا الملف

يوضح هذا الملف كيفية إعداد قواعد حماية الفروع على GitHub لضمان جودة الكود والعمليات الآمنة.

---

## إعدادات Branch Protection لـ `main`

### 📋 القواعد المطلوبة

#### 1. **Require pull request reviews before merging**

- ✅ **Enabled**
- **عدد الموافقات:** 1 (أو أكثر حسب حجم الفريق)
- **Dismiss stale pull request reviews:** ✅ مفعّل
- **Require review from Code Owners:** ✅ مفعّل
- **Require last push approval:** ✅ مفعّل

#### 2. **Require status checks to pass before merging**

- ✅ **Enabled**
- **Required checks:**
  - `CI / Lint Backend (Python)`
  - `CI / Lint Frontend (JavaScript)`
  - `CI / Test Backend`
  - `CI / Build Backend`
  - `CI / Build Frontend`
- **Require branches to be up to date:** ✅ مفعّل

#### 3. **Require code owner reviews**

- ✅ **Enabled**
- **File:** `.github/CODEOWNERS`

#### 4. **Allow force pushes**

- ❌ **Disabled** (لا نسمح بـ force push)

#### 5. **Allow deletions**

- ❌ **Disabled** (لا نسمح بحذف main)

#### 6. **Require conversation resolution before merging**

- ✅ **Enabled** (يجب حل جميع التعليقات)

#### 7. **Require linear history**

- ✅ **Enabled** (سجل نظيف بدون merge commits غير ضرورية)

#### 8. **Require signed commits**

- ❌ **Optional** (موصى به للأمان العالي)

---

## إعدادات Branch Protection لـ `develop` (اختياري)

### القواعس الأساسية فقط

- ✅ Require pull request reviews (1 approval)
- ✅ Require status checks
- ❌ Require conversation resolution
- ❌ Require linear history

---

## كيفية تطبيق القواعس على GitHub

### الطريقة اليدوية

1. **انتقل إلى:** Settings → Branches
2. **اضغط:** "Add rule"
3. **Branch name pattern:** `main`
4. **فعّل الإعدادات أعلاه:**

   ```
   ☑️ Require a pull request before merging
      ☑️ Require approvals (Count: 1)
      ☑️ Dismiss stale pull request reviews
      ☑️ Require review from Code Owners
      ☑️ Require last push approval
   
   ☑️ Require status checks to pass before merging
      ☑️ Require branches to be up to date before merging
      - Select required checks: (CI jobs)
   
   ☑️ Include administrators
   ☑️ Require conversation resolution before merging
   ☑️ Require linear history
   ☑️ Restrict who can push to matching branches
   ```

### الطريقة البرمجية (Terraform)

```hcl
resource "github_branch_protection" "main" {
  repository_id = github_repository.store_erp.node_id
  pattern       = "main"
  
  enforce_admins = true
  allows_deletions = false
  allows_force_pushes = false
  require_conversation_resolution = true
  require_linear_history = true
  
  required_status_checks {
    strict = true
    contexts = [
      "CI / Lint Backend (Python)",
      "CI / Lint Frontend (JavaScript)",
      "CI / Test Backend",
      "CI / Build Backend",
      "CI / Build Frontend",
    ]
  }
  
  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = true
    required_approving_review_count = 1
    require_last_push_approval      = true
  }
}
```

### الطريقة عبر GitHub CLI

```bash
# عرض الإعدادات الحالية
gh api repos/hamfarid/store-erp/branches/main/protection

# تحديث الإعدادات
gh api repos/hamfarid/store-erp/branches/main/protection \
  --input protect-main.json
```

---

## ملف إعدادات JSON (`protect-main.json`)

```json
{
  "enforce_admins": true,
  "allow_deletions": false,
  "allow_force_pushes": false,
  "require_conversation_resolution": true,
  "require_linear_history": true,
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "CI / Lint Backend (Python)",
      "CI / Lint Frontend (JavaScript)",
      "CI / Test Backend",
      "CI / Build Backend",
      "CI / Build Frontend"
    ]
  },
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1,
    "require_last_push_approval": true
  },
  "restrictions": {
    "users": [],
    "teams": [],
    "apps": []
  }
}
```

---

## ✅ التحقق من الإعدادات

للتأكد من تطبيق القواعس بشكل صحيح:

```bash
# عرض الإعدادات
gh api repos/hamfarid/store-erp/branches/main/protection --pretty

# اختبار PR:
# 1. حاول دمج PR بدون موافقات ❌ يجب أن يفشل
# 2. حاول دمج PR بدون CI تمرير ❌ يجب أن يفشل
# 3. حاول force push ❌ يجب أن يفشل
```

---

## 🎯 النتائج المتوقعة

بعد تطبيق القواعس:

### ✅ يمكنك

- فتح PRs من أي فرع
- دمج PRs **بعد** الموافقة و CI
- رؤية قائمة كاملة من الفحوصات المطلوبة

### ❌ لا يمكنك

- دمج PR بدون موافقة
- دمج PR بدون CI تمرير
- حذف main
- Force push إلى main
- تجاهل تعليقات المراجعة

---

## 📊 مثال من الواقع

### محاولة دمج PR بدون موافقة

```
❌ This branch cannot be merged
├─ Require status checks to pass before merging
│  └─ All checks must pass
├─ Require pull request reviews before merging
│  └─ Requires 1 approving review
└─ Require conversation resolution
   └─ All conversations must be resolved
```

---

## 📝 ملاحظات مهمة

1. **الموافقات:** يجب أن يكون الموافق **مختلفاً** عن كاتب الـ PR
2. **CI Checks:** يجب تحديدها بنفس الأسماء في GitHub Actions
3. **Admins:** قد يتجاوزون القواعس (استخدم بحذر!)
4. **المراجعة:** استخدم "Request changes" لرفض PR

---

## 🔄 تطبيق على `develop` (اختياري)

إذا كان لديك فرع `develop`:

```json
{
  "enforce_admins": false,
  "allow_deletions": false,
  "allow_force_pushes": false,
  "require_conversation_resolution": false,
  "require_linear_history": false,
  "required_status_checks": {
    "strict": true,
    "contexts": ["CI / Test Backend"]
  },
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  }
}
```

---

## 📞 الدعم

**هل تواجه مشاكل؟**

- تحقق من أسماء CI checks مطابقة تماماً
- تأكد من أن CODEOWNERS موجود
- راجع إعدادات Branch Protection الحالية

---

**آخر تحديث:** فبراير 2026  
**الحالة:** ✅ جاهز للتطبيق
