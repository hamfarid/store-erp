# -*- markdown -*-
# FILE: docs/DEPLOYMENT_AND_MAINTENANCE_GUIDE.md | PURPOSE: Comprehensive Deployment and Maintenance Guide | OWNER: DevOps | RELATED: docker-compose.prod.yml | LAST-AUDITED: 2025-10-21

# دليل النشر والصيانة الشامل - نظام إدارة المخزون العربي

## 🚀 مقدمة

هذا الدليل يوفر جميع الخطوات اللازمة لنشر وصيانة وتحديث نظام إدارة المخزون العربي في بيئة الإنتاج. تم تصميم هذا الدليل ليكون مرجعاً شاملاً للمطورين ومسؤولي النظام.

## 📋 المتطلبات الأساسية

- **خادم Linux:** (موصى به: Ubuntu 22.04 أو أحدث)
- **Docker:** (الإصدار 20.10.0 أو أحدث)
- **Docker Compose:** (الإصدار 2.0.0 أو أحدث)
- **Git:** (الإصدار 2.34.1 أو أحدث)
- **نطاق (Domain):** مسجل وموجه إلى عنوان IP الخاص بالخادم
- **شهادة SSL:** (موصى به: Let's Encrypt)

## ⚙️ خطوات النشر للإنتاج

### 1. إعداد الخادم

1.  **تحديث النظام:**

    ```bash
    sudo apt-get update && sudo apt-get upgrade -y
    ```

2.  **تثبيت Docker و Docker Compose:**

    ```bash
    # تثبيت Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh

    # إضافة المستخدم إلى مجموعة Docker
    sudo usermod -aG docker $USER
    newgrp docker

    # تثبيت Docker Compose
    sudo apt-get install docker-compose-plugin -y
    ```

3.  **تثبيت Git:**

    ```bash
    sudo apt-get install git -y
    ```

### 2. استنساخ المشروع

```bash
# استنساخ المستودع
git clone https://github.com/hamfarid/Store.git

# الدخول إلى مجلد المشروع
cd Store
```

### 3. إعداد متغيرات البيئة

1.  **نسخ ملف البيئة:**

    ```bash
    cp .env.example .env.production
    ```

2.  **تعديل ملف البيئة:**

    ```bash
    nano .env.production
    ```

    - **تغيير جميع كلمات المرور والمفاتيح السرية** إلى قيم قوية وعشوائية.
    - **إعداد معلومات قاعدة البيانات** (DB_PASSWORD).
    - **إعداد معلومات Redis** (REDIS_PASSWORD).
    - **إعداد مفاتيح الأمان** (SECRET_KEY, JWT_SECRET_KEY, SECURITY_PASSWORD_SALT).
    - **إعداد معلومات البريد الإلكتروني** (MAIL_USERNAME, MAIL_PASSWORD).
    - **إعداد معلومات Grafana** (GRAFANA_PASSWORD).
    - **إعداد النطاق** (ALLOWED_HOSTS, CORS_ORIGINS).

### 4. إعداد شهادة SSL (Let's Encrypt)

1.  **تثبيت Certbot:**

    ```bash
    sudo apt-get install certbot python3-certbot-nginx -y
    ```

2.  **الحصول على شهادة SSL:**

    ```bash
    sudo certbot --nginx -d your-domain.com -d www.your-domain.com
    ```

    - اتبع التعليمات التي تظهر على الشاشة.
    - سيقوم Certbot بتكوين Nginx تلقائياً لاستخدام شهادة SSL.

### 5. بناء وتشغيل النظام

1.  **بناء وتشغيل الحاويات:**

    ```bash
    docker-compose -f docker-compose.prod.yml up --build -d
    ```

2.  **التحقق من حالة الحاويات:**

    ```bash
    docker-compose -f docker-compose.prod.yml ps
    ```

    - يجب أن تكون جميع الحاويات في حالة `running` و `healthy`.

### 6. تهيئة قاعدة البيانات

1.  **إنشاء الجداول:**

    ```bash
    docker-compose -f docker-compose.prod.yml exec backend flask db upgrade
    ```

2.  **إنشاء المستخدم المسؤول الأول:**

    ```bash
    docker-compose -f docker-compose.prod.yml exec backend flask create-admin
    ```

    - اتبع التعليمات لإدخال معلومات المستخدم المسؤول.

### 7. الوصول إلى النظام

- **الواجهة الأمامية:** `https://your-domain.com`
- **لوحة المراقبة Grafana:** `http://localhost:3000` (أو عبر SSH tunnel)
- **Prometheus:** `http://localhost:9090` (أو عبر SSH tunnel)

## 🔧 الصيانة والتحديثات

### تحديث النظام

1.  **سحب آخر التحديثات من Git:**

    ```bash
    git pull origin main
    ```

2.  **إعادة بناء وتشغيل الحاويات:**

    ```bash
    docker-compose -f docker-compose.prod.yml up --build -d
    ```

3.  **تطبيق تحديثات قاعدة البيانات (إذا لزم الأمر):**

    ```bash
    docker-compose -f docker-compose.prod.yml exec backend flask db upgrade
    ```

### النسخ الاحتياطية

- **النسخ الاحتياطية التلقائية:** يتم تشغيلها يومياً في الساعة 2 صباحاً (قابلة للتكوين في `.env.production`).
- **مجلد النسخ الاحتياطية:** `/app/backups` داخل حاوية الواجهة الخلفية.
- **تقارير النسخ الاحتياطية:** يتم إرسالها عبر البريد الإلكتروني.

**لإنشاء نسخة احتياطية يدوياً:**

```bash
docker-compose -f docker-compose.prod.yml exec backend python scripts/backup_system.py
```

### استعادة النظام

1.  **إيقاف النظام:**

    ```bash
    docker-compose -f docker-compose.prod.yml down
    ```

2.  **استعادة قاعدة البيانات:**

    ```bash
    # استخراج النسخة الاحتياطية
    gunzip -c /path/to/backup/database_YYYYMMDD_HHMMSS.sql.gz > database.sql

    # استعادة قاعدة البيانات
    docker-compose -f docker-compose.prod.yml run --rm database pg_restore -U store_user -d store_production < database.sql
    ```

3.  **استعادة الملفات:**

    ```bash
    # استخراج النسخة الاحتياطية
    tar -xzf /path/to/backup/files_YYYYMMDD_HHMMSS.tar.gz -C /path/to/project
    ```

4.  **إعادة تشغيل النظام:**

    ```bash
    docker-compose -f docker-compose.prod.yml up -d
    ```

### مراقبة السجلات

- **سجلات الواجهة الخلفية:**

  ```bash
  docker-compose -f docker-compose.prod.yml logs -f backend
  ```

- **سجلات الواجهة الأمامية (Nginx):**

  ```bash
  docker-compose -f docker-compose.prod.yml logs -f frontend
  ```

- **سجلات Nginx Reverse Proxy:**

  ```bash
  docker-compose -f docker-compose.prod.yml logs -f nginx
  ```

### حل المشاكل الشائعة

- **مشكلة في الصلاحيات:**

  ```bash
  sudo chown -R $USER:$USER .
  ```

- **مشكلة في الاتصال بقاعدة البيانات:**
  - تأكد من صحة معلومات قاعدة البيانات في `.env.production`.
  - تأكد من أن حاوية قاعدة البيانات تعمل بشكل صحيح.

- **مشكلة في شهادة SSL:**

  ```bash
  sudo certbot renew --dry-run
  ```

## 🛡️ الأمان

- **تحديث النظام والتبعيات بانتظام.**
- **استخدام كلمات مرور قوية ومعقدة.**
- **مراقبة السجلات والتنبيهات بانتظام.**
- **تقييد الوصول إلى الخادم والمنافذ.**
- **إجراء نسخ احتياطية منتظمة وتخزينها في مكان آمن.**

## 📞 الدعم

للحصول على الدعم الفني، يرجى إنشاء issue في مستودع GitHub:

[https://github.com/hamfarid/Store/issues](https://github.com/hamfarid/Store/issues)

---

**تم إنشاؤه بواسطة Manus AI** | **آخر تحديث:** 2025-10-21
