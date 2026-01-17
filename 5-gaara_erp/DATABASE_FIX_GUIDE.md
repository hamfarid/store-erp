# 🔧 دليل إصلاح قاعدة البيانات - Database Fix Guide

<div align="center">

![Error](https://img.shields.io/badge/الخطأ-sqlite3.OperationalError-red.svg?style=for-the-badge)
![Fix](https://img.shields.io/badge/الحل-إعادة_إنشاء_DB-success.svg?style=for-the-badge)

**المشكلة:** `no such column: users.password_hash`  
**السبب:** قاعدة البيانات قديمة ولا تحتوي على العمود الجديد

</div>

---

## ❌ الأخطاء المحتملة

### 1. خطأ password_hash:
```
❌ خطأ في إنشاء البيانات الأساسية: (sqlite3.OperationalError)
no such column: users.password_hash
```

### 2. خطأ Foreign Key:
```
❌ خطأ في إنشاء قاعدة البيانات: Foreign key associated with
column 'products.supplier_id' could not find table 'suppliers'
```

---

## 🔍 السبب

قاعدة البيانات القديمة تستخدم عمود `password` بدلاً من `password_hash`.  
النموذج الجديد (`User`) يبحث عن `password_hash` ولا يجده.

---

## ✅ الحل السريع (موصى به)

### الخطوة 1: أوقف Backend (إذا كان يعمل)
```powershell
# اضغط Ctrl+C في Terminal الذي يشغل Backend
```

### الخطوة 2: شغّل السكريبت المبسط (موصى به)
```powershell
cd D:\APPS_AI\store\store_v1.6\backend
python simple_recreate_db.py
```

**ماذا يفعل السكريبت:**
1. ✅ ينسخ قاعدة البيانات القديمة احتياطياً
2. ✅ يحذف قواعد البيانات القديمة
3. ✅ ينشئ قاعدة بيانات جديدة باستخدام SQL مباشرة
4. ✅ ينشئ الأدوار الافتراضية (admin, manager, user)
5. ✅ ينشئ مستخدم admin
6. ✅ ينشئ جميع الجداول بالترتيب الصحيح

**البديل (إذا فشل السكريبت المبسط):**
```powershell
python recreate_database.py
```

### الخطوة 3: شغّل Backend
```powershell
python app.py
```

### الخطوة 4: تحقق من النجاح
يجب أن ترى:
```
✅ Database initialized successfully
✅ Error handlers registered successfully
✅ Registered blueprint: temp_api_bp
✅ Registered blueprint: status_bp
 * Running on http://127.0.0.1:5002
```

---

## 🔧 الحل اليدوي (إذا فشل السكريبت)

### الخطوة 1: نسخ احتياطي يدوي
```powershell
cd D:\APPS_AI\store\store_v1.6\backend

# إنشاء مجلد النسخ الاحتياطية
mkdir database_archive\manual_backup_$(Get-Date -Format "yyyyMMdd_HHmmss")

# نسخ قواعد البيانات
copy instance\inventory.db database_archive\manual_backup_*\
copy instance\inventory_encrypted.db database_archive\manual_backup_*\
```

### الخطوة 2: حذف قواعد البيانات القديمة
```powershell
# حذف جميع ملفات قاعدة البيانات
del instance\inventory.db
del instance\inventory.db-shm
del instance\inventory.db-wal
del instance\inventory_encrypted.db
del instance\inventory_encrypted.db-shm
del instance\inventory_encrypted.db-wal
del inventory_system.db
del inventory_system.db-shm
del inventory_system.db-wal
```

### الخطوة 3: إنشاء قاعدة بيانات جديدة
```powershell
python
```

ثم في Python:
```python
from app import app, db
from src.models.user_unified import User, Role, create_default_roles
import bcrypt

with app.app_context():
    # إنشاء الجداول
    db.create_all()
    print("✅ تم إنشاء الجداول")
    
    # إنشاء الأدوار
    create_default_roles()
    print("✅ تم إنشاء الأدوار")
    
    # إنشاء admin
    admin_role = Role.query.filter_by(name='admin').first()
    password = 'u-fZEk2jsOQN3bwvFrj93A'
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    admin_user = User(
        username='admin',
        email='admin@system.com',
        password_hash=password_hash,
        full_name='مدير النظام',
        role_id=admin_role.id if admin_role else None,
        role='admin',
        is_active=True,
        is_superuser=True,
        permissions='*'
    )
    
    db.session.add(admin_user)
    db.session.commit()
    print("✅ تم إنشاء admin")

exit()
```

### الخطوة 4: شغّل Backend
```powershell
python app.py
```

---

## 📊 التحقق من قاعدة البيانات

### فحص الجداول:
```powershell
python
```

```python
from app import app, db
from src.models.user_unified import User

with app.app_context():
    # عدد المستخدمين
    user_count = User.query.count()
    print(f"عدد المستخدمين: {user_count}")
    
    # المستخدم admin
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print(f"✅ admin موجود")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.role}")
        print(f"   Active: {admin.is_active}")
    else:
        print("❌ admin غير موجود")

exit()
```

---

## ⚠️ ملاحظات مهمة

### 1. النسخ الاحتياطية:
- ✅ يتم حفظ النسخ الاحتياطية في `database_archive/`
- ✅ يمكنك استرجاع البيانات القديمة إذا احتجتها

### 2. البيانات القديمة:
- ❌ سيتم فقدان جميع البيانات القديمة
- ✅ إذا كنت تريد الاحتفاظ بالبيانات، استخدم migration script

### 3. بيانات الدخول الجديدة:
```
Username: admin
Password: u-fZEk2jsOQN3bwvFrj93A
```

---

## 🔄 استرجاع النسخة الاحتياطية

إذا أردت استرجاع قاعدة البيانات القديمة:

```powershell
cd D:\APPS_AI\store\store_v1.6\backend

# ابحث عن آخر نسخة احتياطية
dir database_archive

# انسخ النسخة الاحتياطية
copy database_archive\backup_YYYYMMDD_HHMMSS\inventory.db instance\
copy database_archive\backup_YYYYMMDD_HHMMSS\inventory_encrypted.db instance\
```

---

## 🚀 بعد الإصلاح

### 1. شغّل Backend:
```powershell
cd D:\APPS_AI\store\store_v1.6\backend
python app.py
```

### 2. شغّل Frontend:
```powershell
cd D:\APPS_AI\store\store_v1.6\frontend
npm run dev
```

### 3. افتح المتصفح:
```
http://localhost:5502
```

### 4. سجل الدخول:
```
Username: admin
Password: u-fZEk2jsOQN3bwvFrj93A
```

---

## 📖 الملفات المرجعية

1. ✅ [DATABASE_FIX_GUIDE.md](./DATABASE_FIX_GUIDE.md) - هذا الملف
2. ✅ [backend/recreate_database.py](./backend/recreate_database.py) - سكريبت الإصلاح
3. ✅ [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md) - دليل التثبيت

---

<div align="center">

# ✅ الحل جاهز!

**سكريبت تلقائي**

**نسخ احتياطي آمن**

**قاعدة بيانات جديدة**

---

⭐ **شغّل السكريبت الآن!**

```powershell
cd backend
python recreate_database.py
```

</div>

