# دليل الاستخدام السريع / Quick Usage Guide

**Version:** 10.2.0 (Project-Specific Memory & MCP)  
**Date:** November 5, 2025

---

## 🚀 البدء السريع / Quick Start

### الأمر الأساسي / Basic Command

```
Initialize Memory and MCP for project: [project-name]
```

**مثال / Example:**
```
Initialize Memory and MCP for project: store-erp
```

---

## 📂 البنية / Structure

### ما يتم إنشاؤه / What Gets Created

```
C:\Users\hadym\.global\
├── memory\
│   └── store-erp\              ✅ ذاكرة Store ERP فقط
│       ├── decisions.md
│       ├── architecture.md
│       ├── preferences.md
│       └── context.md
│
└── mcp\
    └── store-erp\              ✅ MCP لـ Store ERP فقط
        ├── config.json
        ├── tools.json
        └── connections.json
```

---

## 💬 الأوامر الأساسية / Basic Commands

### 1. البدء بمشروع جديد
```
Initialize Memory and MCP for project: my-project
```

### 2. حفظ قرار
```
Save to memory: We decided to use PostgreSQL for the database
```
↓ يُحفظ في:
```
~/.global/memory/my-project/decisions.md
```

### 3. استدعاء قرار
```
What did we decide about the database?
```
↓ يقرأ من:
```
~/.global/memory/my-project/decisions.md
```

### 4. التبديل بين المشاريع
```
Switch to project: another-project
```

---

## 🎯 أمثلة عملية / Practical Examples

### مثال 1: Store ERP

```
# البدء
Initialize Memory and MCP for project: store-erp

# حفظ قرار
Save to memory: Using JWT for authentication

# استدعاء
What did we decide about authentication?

# النتيجة
"We decided to use JWT for authentication"
```

### مثال 2: عدة مشاريع

```
# مشروع 1
Initialize Memory and MCP for project: store-erp
Save to memory: Store ERP uses PostgreSQL

# مشروع 2
Switch to project: personal-site
Save to memory: Personal site uses SQLite

# مشروع 3
Switch to project: gaara-erp-v12
Save to memory: Gaara ERP uses MySQL

# كل مشروع منفصل!
```

---

## 📊 المقارنة / Comparison

| الجانب | القديم | الجديد |
|--------|--------|--------|
| **الأمر** | `Initialize Memory and MCP` | `Initialize Memory and MCP for project: name` |
| **البنية** | `~/.global/memory/` | `~/.global/memory/[project-name]/` |
| **الاختلاط** | ❌ يحدث | ✅ لا يحدث |
| **التنظيم** | ❌ صعب | ✅ سهل |

---

## ⚠️ ملاحظات مهمة / Important Notes

### 1. اسم المشروع
```
✅ الصحيح:
- store-erp
- gaara-erp-v12
- personal-site

❌ الخطأ:
- Store ERP (مسافات)
- StoreERP (حروف كبيرة)
```

### 2. كل مشروع منفصل
```
✅ الصحيح:
~/.global/memory/store-erp/      # Store ERP فقط
~/.global/memory/gaara-erp-v12/  # Gaara ERP فقط

❌ الخطأ:
~/.global/memory/                # كل المشاريع مختلطة
```

### 3. Environment Separation
```
✅ الصحيح:
YOUR tools:    ~/.global/memory/store-erp/
USER project:  D:\APPS_AI\store\Store\

❌ الخطأ:
خلط الأدوات مع المشروع
```

---

## 🔧 استكشاف الأخطاء / Troubleshooting

### المشكلة: لم يحدد اسم المشروع

**الحل:**
```
STOP. You must specify project name.

Use: Initialize Memory and MCP for project: [project-name]

Example: Initialize Memory and MCP for project: store-erp
```

### المشكلة: اختلاط المشاريع

**الحل:**
```
CRITICAL: Projects are mixing!

Each project MUST have its own directory:
- ~/.global/memory/[project-name]/
- ~/.global/mcp/[project-name]/

Fix this immediately.
```

---

## 📚 الموارد / Resources

### التوثيق الكامل
- **البنية الجديدة:** `NEW_STRUCTURE.md`
- **دليل الخطوات:** `STEP_BY_STEP_GUIDE.md`
- **سجل التغييرات:** `CHANGELOG_v10.2.0.md`

### GitHub
- **Repository:** https://github.com/hamfarid/global
- **Version:** 10.2.0

---

## ✅ الخلاصة / Summary

### الأمر الجديد:
```
Initialize Memory and MCP for project: [project-name]
```

### الفوائد:
1. ✅ لا اختلاط بين المشاريع
2. ✅ تنظيم أفضل
3. ✅ سهولة الصيانة
4. ✅ دعم عدة مشاريع

### البدء:
```
Initialize Memory and MCP for project: your-project-name
```

---

**الإصدار:** 10.2.0  
**الحالة:** ✅ Production Ready

🚀 **Happy Coding!** 🚀

