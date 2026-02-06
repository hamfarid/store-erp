# GitHub Environments Setup Guide

هذا الدليل يشرح كيفية إعداد بيئات GitHub المطلوبة لتشغيل سير العمل بنجاح.

---

## 📋 البيئات المطلوبة

### 1. **Staging Environment** (بيئة التطوير)
**الموقع:** Settings → Environments → New environment → "staging"

#### متغيرات البيئة (Environment variables)
```
STAGING_HOST=staging.example.com
STAGING_USER=deploy
VITE_API_URL=https://staging-api.example.com
```

#### الأسرار (Secrets)
```
STAGING_SSH_KEY=-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----

STAGING_API_KEY=sk_staging_...
STAGING_DB_URL=postgresql://user:pass@staging-db:5432/gaara_scan
```

#### قواعد الحماية
- ✅ Required reviewers: **1**
- Deployment branches: Select non-default branches
- Require environment-specific secrets

---

### 2. **Production Environment** (بيئة الإنتاج)
**الموقع:** Settings → Environments → New environment → "production"

#### متغيرات البيئة
```
PRODUCTION_HOST=api.example.com
PRODUCTION_USER=deploy
VITE_API_URL=https://api.example.com
```

#### الأسرار
```
PRODUCTION_SSH_KEY=-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----

PRODUCTION_API_KEY=sk_live_...
PRODUCTION_DB_URL=postgresql://user:pass@prod-db:5432/gaara_scan
PROD_BACKUP_BUCKET=s3://gaara-backups/prod
```

#### قواعد الحماية (STRICT)
- ✅ Required reviewers: **2** (من أعضاء مختلفين)
- ✅ Deployment branches: main only
- ✅ Require custom deployment branches / tags
- ✅ Require environment-specific secrets
- ⏰ Deployment timeout: 30 minutes

---

## 🔐 الأسرار المطلوبة

### على مستوى المستودع (Repository secrets)
يمكن إضافتها عند الحاجة إذا كانت مشتركة بين البيئات:

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
GITHUB_TOKEN=ghp_...  (automatically provided)
```

### الأسرار الخاصة بكل بيئة
تُضاف في Settings → Environments → [environment] → Secrets

---

## 🛠️ خطوات الإعداد اليدوي

### الخطوة 1: إنشاء البيئات
```bash
# اذهب إلى: https://github.com/[owner]/[repo]/settings/environments

# انقر على "New environment"
# أدخل الاسم: "staging"
# انقر Create environment
# كرر لـ "production"
```

### الخطوة 2: إضافة متغيرات البيئة
```
Settings → Environments → [environment name] → Environment variables
+ Add variable
```

### الخطوة 3: إضافة الأسرار
```
Settings → Environments → [environment name] → Secrets
+ New repository secret
```

### الخطوة 4: تكوين قواعل الحماية
```
Settings → Environments → [environment name] → Deployment protection rules
```

---

## 📝 قالب الأسرار (Template)

### SSH Private Key Generation
```bash
# إنشاء مفتاح SSH
ssh-keygen -t ed25519 -f deploy_key -C "github-actions@gaara-scan.ai"

# عرض المفتاح الخاص (للإضافة في GitHub)
cat deploy_key

# عرض المفتاح العام (للإضافة في السيرفر)
cat deploy_key.pub
```

### إضافة المفتاح العام إلى السيرفر
```bash
# على السيرفر (staging/production)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cat >> ~/.ssh/authorized_keys << 'EOF'
[paste deploy_key.pub content]
EOF
chmod 600 ~/.ssh/authorized_keys
```

---

## ✅ التحقق من الإعداد

### اختبار الاتصال
```bash
# من terminal locally
ssh -i deploy_key deploy@staging.example.com "echo 'Connection OK'"
ssh -i deploy_key deploy@prod.example.com "echo 'Connection OK'"
```

### تشغيل عملية اختبار
```bash
# اذهب إلى: Actions → [Workflow] → Run workflow
# اختر البيئة: staging
# انقر Run workflow
```

---

## 🔄 استراتيجية التطوير والنشر

| البيئة | متى | من | الفروع |
|-------|-----|----|----|
| **Staging** | تلقائي | feature/* → develop | release/*, develop |
| **Production** | يدويّ | main | main, tags |
| **Hotfix** | طارئ | hotfix/* | main |

---

## 🚨 حالات الطوارئ

### إذا فشل النشر
1. راجع سجل المهام في GitHub Actions
2. تحقق من الأسرار والمتغيرات
3. تحقق من اتصال الشبكة
4. أعد محاولة النشر

### إذا انقطعت الخدمة
```bash
# Rollback السريع (من Staging فقط لأول مرة)
git revert [commit-hash]
git push origin develop

# للإنتاج: استخدم hotfix/*
git checkout -b hotfix/rollback
# اعكس التغييرات
git push origin hotfix/rollback
```

---

## 📞 الدعم والمساعدة

- **مراجع:**
  - [GitHub Environments Documentation](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
  - [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

- **الملفات ذات الصلة:**
  - [Git Workflow Guide](./GIT_WORKFLOW_GUIDE.md)
  - [Branch Protection Rules](./branch-protection.tf)

---

*آخر تحديث: 2026-02-05*
