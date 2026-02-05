# ⚙️ إعداد GitHub Secrets للـ Workflows

## 📋 نظرة عامة

لكي تعمل GitHub Actions Workflows بشكل صحيح، يجب إعداد Secrets معينة في إعدادات المستودع.

---

## 🔐 الـ Secrets المطلوبة

### 1️⃣ لـ Deploy to Staging

| Secret | الوصف | مثال |
|--------|-------|------|
| `STAGING_HOST` | اسم الخادم أو IP | `staging.example.com` |
| `STAGING_USER` | اسم المستخدم SSH | `deploy` |
| `STAGING_SSH_KEY` | مفتاح SSH الخاص | `-----BEGIN OPENSSH PRIVATE KEY-----...` |

### 2️⃣ لـ Deploy to Production

| Secret | الوصف | مثال |
|--------|-------|------|
| `PRODUCTION_HOST` | اسم الخادم أو IP | `example.com` |
| `PRODUCTION_USER` | اسم المستخدم SSH | `deploy` |
| `PRODUCTION_SSH_KEY` | مفتاح SSH الخاص | `-----BEGIN OPENSSH PRIVATE KEY-----...` |

### 3️⃣ للإخطارات (اختياري)

| Secret | الوصف | مثال |
|--------|-------|------|
| `SLACK_WEBHOOK_URL` | Slack Webhook URL | `https://hooks.slack.com/services/...` |

---

## 🚀 كيفية إضافة Secrets

### الطريقة 1: عبر GitHub Web UI

1. انتقل إلى: **Settings → Secrets and variables → Actions**
2. اضغط **New repository secret**
3. أدخل الاسم والقيمة
4. اضغط **Add secret**

### الطريقة 2: عبر GitHub CLI

```bash
# إضافة secret واحد
gh secret set STAGING_HOST -b "staging.example.com"
gh secret set STAGING_USER -b "deploy"
gh secret set STAGING_SSH_KEY < ~/.ssh/staging_key

# إضافة متعددة
gh secret set PRODUCTION_HOST -b "example.com"
gh secret set PRODUCTION_USER -b "deploy"
gh secret set PRODUCTION_SSH_KEY < ~/.ssh/production_key
gh secret set SLACK_WEBHOOK_URL -b "https://hooks.slack.com/services/..."
```

### الطريقة 3: عبر GitHub API

```bash
# إضافة secret
curl -X PUT \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/hamfarid/store-erp/actions/secrets/STAGING_HOST \
  -d '{"encrypted_value":"YOUR_ENCRYPTED_VALUE"}'
```

---

## 🔒 الأمان: كيفية إعداد مفاتيح SSH

### إنشاء مفتاح SSH للـ Staging

```bash
# إنشاء مفتاح جديد
ssh-keygen -t ed25519 -C "github-staging-deploy" -f ~/.ssh/staging_key -N ""

# عرض المفتاح العام (أضفه إلى الخادم)
cat ~/.ssh/staging_key.pub

# عرض المفتاح الخاص (استخدمه في GitHub Secret)
cat ~/.ssh/staging_key
```

### إضافة المفتاح العام إلى الخادم

```bash
# على الخادم (staging)
cat ~/.ssh/staging_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### التحقق من الاتصال

```bash
ssh -i ~/.ssh/staging_key deploy@staging.example.com "echo 'Connection OK'"
```

---

## ✅ التحقق من الإعداد

### اختبار الـ Workflow

1. انتقل إلى: **Actions**
2. اختر **CD - Deploy** من القائمة
3. اضغط **Run workflow**
4. اختر:
   - Branch: `main`
   - Environment: `staging` أو `production`
5. اضغط **Run workflow**

### التحقق من السجلات

```bash
# عرض سجل الـ workflow
gh run list --workflow=cd-deploy.yml

# عرض تفاصيل run محدد
gh run view RUN_ID --log
```

---

## 🐛 استكشاف الأخطاء

### خطأ: "Cannot find secret"

```
Error: Secrets.STAGING_HOST is not defined
```

**الحل:** تأكد من إضافة الـ secret بالاسم الصحيح (حساس لحالة الأحرف)

### خطأ: "Permission denied"

```
Permission denied (publickey).
```

**الحل:** 
- تحقق من المفتاح الخاص في الـ secret
- تحقق من المفتاح العام على الخادم

### خطأ: "Host key verification failed"

```
Host key verification failed.
```

**الحل:** أضف الخادم إلى `known_hosts`:

```bash
ssh-keyscan -t ed25519 staging.example.com >> ~/.ssh/known_hosts
```

---

## 📚 الموارد

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [SSH Key Management](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/learn-github-actions)

---

## 🎯 ملخص الإعداد

```
✅ إنشاء مفاتيح SSH (staging + production)
✅ إضافة المفاتيح العامة إلى الخوادم
✅ إضافة الـ Secrets في GitHub Settings
✅ اختبار الاتصال SSH يدوياً
✅ تشغيل Workflow الاختبار
✅ مراجعة السجلات والتحقق من النجاح
```

---

**الحالة:** 📝 توثيق الإعداد  
**آخر تحديث:** 5 فبراير 2026  
**الإصدار:** 1.0.0
