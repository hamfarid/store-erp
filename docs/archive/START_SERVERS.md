# 🚀 تشغيل الخوادم - Start Servers

## ⚠️ المشكلة مصلحة الآن!

تم إصلاح مشكلة MIME type في `vite.config.js`

---

## 📋 الأوامر الصحيحة

### 1️⃣ أوقف جميع العمليات
اضغط `Ctrl+C` في أي Terminal مفتوح

---

### 2️⃣ Terminal 1 - Backend

**افتح Terminal جديد واكتب:**

```powershell
cd D:\APPS_AI\store\store_v1.6\backend
python app.py
```

**انتظر حتى ترى:**
```
* Running on http://127.0.0.1:5002
```

✅ Backend جاهز!

---

### 3️⃣ Terminal 2 - Frontend

**افتح Terminal جديد آخر واكتب:**

```powershell
cd D:\APPS_AI\store\store_v1.6\frontend
npm run dev
```

**انتظر حتى ترى:**
```
Local: http://localhost:5502/
```

✅ Frontend جاهز!

---

## 🌐 افتح المتصفح

```
http://localhost:5502
```

أو

```
http://localhost:5503
```

(حسب المنفذ الذي يظهر في Terminal)

---

## 🔐 بيانات الدخول

- **Username:** admin
- **Password:** u-fZEk2jsOQN3bwvFrj93A

---

## ✅ يجب أن يعمل الآن بدون أخطاء MIME!

---

## 🔧 إذا استمرت المشكلة

### نظف Cache:
```powershell
cd D:\APPS_AI\store\store_v1.6\frontend
npm cache clean --force
rm -rf node_modules
npm install
npm run dev
```

---

## 📊 ما تم إصلاحه:

1. ✅ إزالة `Content-Type` header من `vite.config.js`
2. ✅ حذف ملف `_headers` الذي كان يسبب مشاكل
3. ✅ CORS مصلح في Backend
4. ✅ كلمة المرور محدّثة في Login

---

## 🎯 النتيجة المتوقعة:

- ✅ لا أخطاء MIME type
- ✅ لا أخطاء CORS
- ✅ Login يعمل
- ✅ جميع الصفحات تعمل

---

**جرب الآن وأخبرني بالنتيجة!** 🚀

