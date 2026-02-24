# 🔐 دليل إعدادات البيئة - Environment Configuration Guide

## 📋 نظرة عامة

جميع الإعدادات الحساسة والقابلة للتخصيص موجودة في ملف `.env` لتجنب الـ hardcoding وتحسين الأمان.

---

## 🔑 المتغيرات الرئيسية

### 👤 معلومات المدير الافتراضي

```env
# اسم المستخدم
DEFAULT_ADMIN_USERNAME=admin

# البريد الإلكتروني
DEFAULT_ADMIN_EMAIL=hady.m.farid@gmail.com

# الاسم الكامل
DEFAULT_ADMIN_FULLNAME=مدير النظام الرئيسي

# كلمة المرور
ADMIN_PASSWORD=u-fZEk2jsOQN3bwvFrj93A

# الدور
DEFAULT_ADMIN_ROLE=admin

# القسم
DEFAULT_ADMIN_DEPARTMENT=إدارة النظام
```

### 🌐 إعدادات الخادم

```env
# عنوان الخادم
HOST=0.0.0.0

# منفذ Backend
PORT=5002

# منفذ Frontend
FRONTEND_PORT=5502
```

### 🔐 مفاتيح الأمان

```env
# مفتاح Flask السري
SECRET_KEY=e15085f24c5d7dd1f60b95d26310022350105c26dd3af48a1130c347e32cfa3a

# مفتاح JWT
JWT_SECRET_KEY=849c4a304f1d276f5a09549baa2b92e76ed575d4388afd30f60c6ae3eea1f9a5

# مفتاح التشفير
ENCRYPTION_KEY=ce8525174c4af33fcac6a79b5a9a1378c961f8ff1498a2f8a988a03428630207
```

### 🗄️ قاعدة البيانات

```env
# رابط قاعدة البيانات
DATABASE_URL=sqlite:///instance/inventory.db

# إعدادات SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS=False
DB_POOL_SIZE=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

### 📧 البريد الإلكتروني

```env
# خادم SMTP
MAIL_SERVER=smtp.gaaraholding.com
MAIL_PORT=587
MAIL_USE_TLS=True

# بيانات الاعتماد
MAIL_USERNAME=hady.m.farid@gaaraholding.com
MAIL_PASSWORD=HaRrMa123!@#
MAIL_DEFAULT_SENDER=hady.m.farid@gaaraholding.com
```

---

## 🔧 كيفية الاستخدام

### 1. في Python (Backend):

```python
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# قراءة المتغيرات
admin_username = os.getenv('DEFAULT_ADMIN_USERNAME', 'admin')
admin_email = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@system.com')
admin_password = os.getenv('ADMIN_PASSWORD')
port = os.getenv('PORT', '5002')
```

### 2. في JavaScript (Frontend):

```javascript
// في ملف .env في مجلد frontend
VITE_API_URL=http://localhost:5002
VITE_APP_NAME=نظام إدارة المتجر

// في الكود
const apiUrl = import.meta.env.VITE_API_URL;
const appName = import.meta.env.VITE_APP_NAME;
```

---

## 📝 أمثلة الاستخدام

### مثال 1: إنشاء مستخدم admin

```python
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

# قراءة الإعدادات من .env
username = os.getenv('DEFAULT_ADMIN_USERNAME')
email = os.getenv('DEFAULT_ADMIN_EMAIL')
password = os.getenv('ADMIN_PASSWORD')
fullname = os.getenv('DEFAULT_ADMIN_FULLNAME')

# تشفير كلمة المرور
password_hash = bcrypt.hashpw(
    password.encode('utf-8'), 
    bcrypt.gensalt()
).decode('utf-8')

# إنشاء المستخدم
user = User(
    username=username,
    email=email,
    password_hash=password_hash,
    full_name=fullname
)
```

### مثال 2: تكوين الخادم

```python
import os
from dotenv import load_dotenv

load_dotenv()

# قراءة إعدادات الخادم
host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', 5002))
debug = os.getenv('FLASK_DEBUG', 'False') == 'True'

# تشغيل الخادم
app.run(host=host, port=port, debug=debug)
```

### مثال 3: إعدادات البريد الإلكتروني

```python
import os
from dotenv import load_dotenv

load_dotenv()

# قراءة إعدادات البريد
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
```

---

## 🔒 أفضل الممارسات الأمنية

### 1. لا تشارك ملف `.env`
```bash
# أضف .env إلى .gitignore
echo ".env" >> .gitignore
```

### 2. استخدم `.env.example` للتوثيق
```env
# .env.example (بدون قيم حساسة)
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_EMAIL=your-email@example.com
ADMIN_PASSWORD=your-secure-password
SECRET_KEY=your-secret-key
```

### 3. غيّر المفاتيح في الإنتاج
```bash
# توليد مفتاح سري جديد
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. استخدم قيم افتراضية آمنة
```python
# دائماً استخدم قيمة افتراضية
port = int(os.getenv('PORT', 5002))
debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
```

---

## 🔄 تحديث الإعدادات

### 1. تحديث كلمة مرور Admin:
```env
# في .env
ADMIN_PASSWORD=new-secure-password-here
```

```bash
# أعد إنشاء قاعدة البيانات
python simple_recreate_db.py
```

### 2. تحديث منفذ الخادم:
```env
# في .env
PORT=8000
FRONTEND_PORT=3000
```

```bash
# أعد تشغيل الخادم
python app.py
```

### 3. تحديث إعدادات البريد:
```env
# في .env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## 📊 المتغيرات المستخدمة في السكريبتات

### `simple_recreate_db.py`:
- ✅ `DEFAULT_ADMIN_USERNAME`
- ✅ `DEFAULT_ADMIN_EMAIL`
- ✅ `DEFAULT_ADMIN_FULLNAME`
- ✅ `ADMIN_PASSWORD`
- ✅ `DEFAULT_ADMIN_ROLE`
- ✅ `PORT`
- ✅ `FRONTEND_PORT`

### `app.py`:
- ✅ `SECRET_KEY`
- ✅ `JWT_SECRET_KEY`
- ✅ `DATABASE_URL`
- ✅ `HOST`
- ✅ `PORT`
- ✅ `FLASK_DEBUG`
- ✅ `FLASK_ENV`

### `database.py`:
- ✅ `DATABASE_URL`
- ✅ `SQLALCHEMY_TRACK_MODIFICATIONS`
- ✅ `DB_POOL_SIZE`
- ✅ `DB_POOL_TIMEOUT`

---

## ⚠️ ملاحظات مهمة

### 1. ترتيب الأولوية:
```
1. متغيرات البيئة (Environment Variables)
2. ملف .env
3. القيم الافتراضية في الكود
```

### 2. إعادة التحميل:
```python
# إذا غيّرت .env أثناء التشغيل
from dotenv import load_dotenv
load_dotenv(override=True)  # إعادة تحميل مع الكتابة فوق القيم القديمة
```

### 3. التحقق من المتغيرات:
```python
import os

# التحقق من وجود متغير
if not os.getenv('SECRET_KEY'):
    raise ValueError("SECRET_KEY is not set in .env file")
```

---

## 🔍 استكشاف الأخطاء

### خطأ: "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### خطأ: "متغير البيئة غير موجود"
```python
# تحقق من اسم المتغير
print(os.getenv('ADMIN_PASSWORD'))  # None إذا لم يكن موجوداً

# استخدم قيمة افتراضية
password = os.getenv('ADMIN_PASSWORD', 'default-password')
```

### خطأ: "ملف .env غير موجود"
```bash
# تأكد من وجود الملف
ls -la .env

# أو في Windows
dir .env
```

---

## 📖 المراجع

- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [12-Factor App: Config](https://12factor.net/config)
- [Environment Variables Best Practices](https://www.twilio.com/blog/environment-variables-python)

---

<div align="center">

# ✅ جميع الإعدادات في .env

**لا hardcoding • أكثر أماناً • سهل التخصيص**

</div>

