# إدارة المنافذ - Port Management Guide

## المشكلة الشائعة: EADDRINUSE

عندما تحصل على خطأ `EADDRINUSE: address already in use`، هذا يعني أن منفذ معين مستخدم بالفعل من قبل عملية أخرى.

---

## الحل السريع

### Windows PowerShell:

```powershell
# 1. ابحث عن العملية التي تستخدم المنفذ
netstat -ano | findstr :9323

# 2. أوقف العملية (استبدل PID برقم العملية)
Stop-Process -Id <PID> -Force

# 3. تحقق من أن المنفذ أصبح متاحاً
netstat -ano | findstr :9323
```

### استخدام سكريبت Port Manager:

```powershell
# فحص المنفذ
.\scripts\port-manager.ps1 -Port 9323

# إيقاف العملية التي تستخدم المنفذ
.\scripts\port-manager.ps1 -Port 9323 -Kill
```

---

## المنافذ المستخدمة في المشروع

### Backend:
- **8000** - Flask Backend Server
- **5432** - PostgreSQL Database
- **6379** - Redis Cache

### Frontend:
- **5505** - Vite Dev Server
- **3000** - Alternative Frontend Port

### Monitoring:
- **9323** - Prometheus Docker Exporter
- **9090** - Prometheus Server

---

## منع تعارض المنافذ

### 1. تحقق من المنافذ قبل البدء:

```powershell
# فحص جميع المنافذ المستخدمة
netstat -ano | findstr "LISTENING"
```

### 2. استخدم متغيرات البيئة:

```bash
# .env
BACKEND_PORT=8000
FRONTEND_PORT=5505
DATABASE_PORT=5432
```

### 3. استخدم سكريبت Port Manager:

```powershell
# فحص جميع المنافذ المهمة
.\scripts\port-manager.ps1 -Port 8000
.\scripts\port-manager.ps1 -Port 5505
.\scripts\port-manager.ps1 -Port 9323
```

---

## حلول بديلة

### 1. تغيير المنفذ:

إذا كان المنفذ مستخدم ولا يمكن إيقافه، غيّر المنفذ في إعدادات التطبيق:

```javascript
// frontend/vite.config.js
export default {
  server: {
    port: 5506  // بدلاً من 5505
  }
}
```

```python
# backend/main.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)  # بدلاً من 8000
```

### 2. إيقاف جميع عمليات Node.js:

```powershell
# إيقاف جميع عمليات Node.js
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
```

### 3. إعادة تشغيل النظام:

في الحالات القصوى، يمكن إعادة تشغيل النظام لتحرير جميع المنافذ.

---

## نصائح

1. ✅ **تحقق دائماً** من المنافذ قبل بدء الخوادم
2. ✅ **استخدم سكريبت Port Manager** لإدارة المنافذ بسهولة
3. ✅ **وثّق المنافذ** في ملف `.env` أو `config/ports.json`
4. ✅ **استخدم منافذ مختلفة** لكل خدمة
5. ✅ **أوقف الخوادم بشكل صحيح** قبل إعادة التشغيل

---

## الأوامر المفيدة

```powershell
# عرض جميع المنافذ المستخدمة
netstat -ano | findstr "LISTENING"

# البحث عن منفذ معين
netstat -ano | findstr :9323

# عرض معلومات العملية
Get-Process -Id <PID>

# إيقاف عملية معينة
Stop-Process -Id <PID> -Force

# إيقاف جميع عمليات Node.js
Get-Process node | Stop-Process -Force
```

---

## المراجع

- [Port Manager Script](../scripts/port-manager.ps1)
- [Prometheus Config](../monitoring/prometheus.yml)

