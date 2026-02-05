# 🚀 دليل سريع - GitHub Flow في Store ERP

## ⚡ الأوامر الأساسية

### ✨ ميزة جديدة

```bash
git checkout main && git pull
git checkout -b feature/description-here
# ... اعمل ...
git add . && git commit -m "feat: your feature"
git push -u origin feature/description-here
# افتح PR على GitHub
```

### 🐛 إصلاح خطأ

```bash
git checkout main && git pull
git checkout -b bugfix/description-here
# ... اصلح ...
git add . && git commit -m "fix: your fix"
git push -u origin bugfix/description-here
# افتح PR على GitHub
```

### 🚨 إصلاح طارئ (Hotfix)

```bash
git checkout main && git pull
git checkout -b hotfix/v1.0.1
# ... اصلح المشكلة الحرجة ...
git add . && git commit -m "fix: critical issue"
git push -u origin hotfix/v1.0.1

# ثم:
git checkout main && git merge --no-ff hotfix/v1.0.1
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git push origin main v1.0.1

git checkout develop && git merge --no-ff hotfix/v1.0.1
git push origin develop

git branch -d hotfix/v1.0.1
git push origin --delete hotfix/v1.0.1
```

---

## 📋 قائمة التحقق قبل فتح PR

- [ ] اختبرت الكود محلياً
- [ ] رسالة الـ commit واضحة (feat/fix/docs)
- [ ] لا توجد ملفات غير مرادة (.env, node_modules)
- [ ] آخر version من main
- [ ] جميع الاختبارات تمر

---

## 🔑 قواعد التسمية

### الفروع
```
feature/user-authentication      ✅ جيد
bugfix/login-validation-error    ✅ جيد
hotfix/v1.0.1                    ✅ جيد
Feature-user-authentication      ❌ استخدم - بدلاً من _
feature/user_auth123             ❌ استخدم - بدلاً من _
```

### الـ Commits
```
feat: add payment system        ✅ جيد
fix: resolve timeout error      ✅ جيد
docs: update README             ✅ جيد
add payment system              ❌ لا تبدأ برسالة عادية
feat : add payment              ❌ بدون مسافة قبل :
```

---

## ⏱️ الجداول الزمنية المتوقعة

| المرحلة | الزمن | النقاط |
|--------|------|--------|
| التطوير | ساعات إلى أيام | اختبر محلياً |
| PR Review | دقائق إلى ساعات | تفاعل مع التعليقات |
| CI Tests | 5-10 دقائق | لا تدمج بدون CI ✅ |
| Merge | فوري | حذف الفرع تلقائياً |
| Deploy | دقائق | تراقب Slack/Teams |

---

## 🎓 التعلم الإضافي

للمزيد من التفاصيل، اقرأ [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md)

---

**الالتزام بهذا الدليل يضمن جودة الكود والعمل الفعّال للفريق! 🎯**
