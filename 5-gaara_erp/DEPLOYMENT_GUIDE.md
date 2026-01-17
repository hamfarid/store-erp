# 🚀 دليل النشر - نظام Gaara ERP

## 📋 **دليل النشر الشامل للإنتاج**

هذا الدليل يوضح كيفية نشر نظام Gaara ERP في بيئة الإنتاج بطريقة آمنة وفعالة.

---

## 🎯 **متطلبات النشر**

### **متطلبات الخادم**
- **نظام التشغيل:** Ubuntu 20.04 LTS أو أحدث / CentOS 8+ / Windows Server 2019+
- **المعالج:** 4 أنوية على الأقل
- **الذاكرة:** 8 جيجابايت RAM كحد أدنى (16 جيجابايت مُوصى به)
- **التخزين:** 50 جيجابايت مساحة فارغة (SSD مُوصى به)
- **الشبكة:** اتصال إنترنت مستقر

### **البرامج المطلوبة**
- **Python:** 3.11 أو أحدث
- **PostgreSQL:** 13 أو أحدث
- **Redis:** 6.0 أو أحدث
- **Nginx:** 1.18 أو أحدث
- **Node.js:** 18 LTS أو أحدث
- **Git:** أحدث إصدار

---

## 🔧 **إعداد البيئة**

### **1. تحديث النظام**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### **2. تثبيت Python 3.11**
```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# CentOS/RHEL
sudo yum install python311 python311-devel -y
```

### **3. تثبيت PostgreSQL**
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib -y

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib -y
sudo postgresql-setup initdb
```

### **4. تثبيت Redis**
```bash
# Ubuntu/Debian
sudo apt install redis-server -y

# CentOS/RHEL
sudo yum install redis -y
```

### **5. تثبيت Nginx**
```bash
# Ubuntu/Debian
sudo apt install nginx -y

# CentOS/RHEL
sudo yum install nginx -y
```

---

## 📁 **إعداد المشروع**

### **1. استنساخ المشروع**
```bash
cd /opt
sudo git clone https://github.com/your-repo/gaara_erp_v5.git
sudo chown -R $USER:$USER gaara_erp_v5
cd gaara_erp_v5
```

### **2. إنشاء البيئة الافتراضية**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### **3. تثبيت التبعيات**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **4. إعداد متغيرات البيئة**
```bash
# إنشاء ملف .env
cp .env.example .env

# تعديل الملف
nano .env
```

**محتوى ملف .env:**
```env
# Django Settings
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,localhost

# Database Settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=gaara_erp_prod
DB_USER=gaara_user
DB_PASSWORD=secure_password_here
DB_HOST=localhost
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://127.0.0.1:6379/1

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Company Settings
COMPANY_NAME=اسم شركتك
SUPPORT_EMAIL=support@your-domain.com

# AI Settings (اختياري)
OPENAI_API_KEY=your-openai-api-key
AI_FEATURES_ENABLED=True

# Backup Settings
BACKUP_ENABLED=True
BACKUP_RETENTION_DAYS=30
```

---

## 🗄️ **إعداد قاعدة البيانات**

### **1. إنشاء قاعدة البيانات**
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE gaara_erp_prod;
CREATE USER gaara_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE gaara_erp_prod TO gaara_user;
ALTER USER gaara_user CREATEDB;
\q
```

### **2. تطبيق الترحيلات**
```bash
cd gaara_erp
python manage.py migrate --settings=gaara_erp.production_settings
```

### **3. إنشاء مستخدم إداري**
```bash
python manage.py createsuperuser --settings=gaara_erp.production_settings
```

### **4. جمع الملفات الثابتة**
```bash
python manage.py collectstatic --noinput --settings=gaara_erp.production_settings
```

---

## 🌐 **إعداد Nginx**

### **1. إنشاء ملف التكوين**
```bash
sudo nano /etc/nginx/sites-available/gaara_erp
```

**محتوى الملف:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Static Files
    location /static/ {
        alias /opt/gaara_erp_v5/gaara_erp/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media Files
    location /media/ {
        alias /opt/gaara_erp_v5/gaara_erp/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Django Application
    location / {
        proxy_pass http://127.0.0.1:9551;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Frontend (if serving separately)
    location /app/ {
        proxy_pass http://127.0.0.1:5173/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **2. تفعيل التكوين**
```bash
sudo ln -s /etc/nginx/sites-available/gaara_erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 **إعداد Systemd Services**

### **1. خدمة Django**
```bash
sudo nano /etc/systemd/system/gaara-erp.service
```

**محتوى الملف:**
```ini
[Unit]
Description=Gaara ERP Django Application
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/gaara_erp_v5/gaara_erp
Environment=PATH=/opt/gaara_erp_v5/.venv/bin
Environment=DJANGO_SETTINGS_MODULE=gaara_erp.production_settings
ExecStart=/opt/gaara_erp_v5/.venv/bin/python manage.py runserver 127.0.0.1:9551
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### **2. خدمة Celery (للمهام الخلفية)**
```bash
sudo nano /etc/systemd/system/gaara-erp-celery.service
```

**محتوى الملف:**
```ini
[Unit]
Description=Gaara ERP Celery Worker
After=network.target redis.service

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/gaara_erp_v5/gaara_erp
Environment=PATH=/opt/gaara_erp_v5/.venv/bin
Environment=DJANGO_SETTINGS_MODULE=gaara_erp.production_settings
ExecStart=/opt/gaara_erp_v5/.venv/bin/celery -A gaara_erp worker --loglevel=info
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### **3. تفعيل الخدمات**
```bash
sudo systemctl daemon-reload
sudo systemctl enable gaara-erp
sudo systemctl enable gaara-erp-celery
sudo systemctl start gaara-erp
sudo systemctl start gaara-erp-celery
```

---

## 🔒 **الأمان والحماية**

### **1. إعداد Firewall**
```bash
# Ubuntu/Debian
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### **2. تأمين PostgreSQL**
```bash
sudo nano /etc/postgresql/13/main/postgresql.conf
```

```conf
# تعديل الإعدادات
listen_addresses = 'localhost'
max_connections = 100
shared_buffers = 256MB
```

### **3. تأمين Redis**
```bash
sudo nano /etc/redis/redis.conf
```

```conf
# تعديل الإعدادات
bind 127.0.0.1
requirepass your_redis_password
```

---

## 📊 **المراقبة والسجلات**

### **1. إعداد السجلات**
```bash
sudo mkdir -p /var/log/gaara_erp
sudo chown www-data:www-data /var/log/gaara_erp
```

### **2. مراقبة الخدمات**
```bash
# فحص حالة الخدمات
sudo systemctl status gaara-erp
sudo systemctl status gaara-erp-celery
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis

# مراقبة السجلات
sudo journalctl -u gaara-erp -f
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 💾 **النسخ الاحتياطي**

### **1. سكريبت النسخ الاحتياطي**
```bash
sudo nano /opt/gaara_erp_v5/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/gaara_erp"
DATE=$(date +%Y%m%d_%H%M%S)

# إنشاء مجلد النسخ الاحتياطي
mkdir -p $BACKUP_DIR

# نسخة احتياطية من قاعدة البيانات
pg_dump -U gaara_user -h localhost gaara_erp_prod > $BACKUP_DIR/db_backup_$DATE.sql

# نسخة احتياطية من الملفات
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz /opt/gaara_erp_v5/gaara_erp/media

# حذف النسخ القديمة (أكثر من 30 يوم)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### **2. جدولة النسخ الاحتياطي**
```bash
sudo crontab -e
```

```cron
# نسخة احتياطية يومية في الساعة 2:00 صباحاً
0 2 * * * /opt/gaara_erp_v5/backup.sh
```

---

## 🚀 **بدء التشغيل**

### **1. استخدام سكريبت البدء**
```bash
# للإنتاج
python start_system.py --production --port 9551

# للتطوير
python start_system.py
```

### **2. التحقق من التشغيل**
- تصفح الموقع: https://your-domain.com
- لوحة الإدارة: https://your-domain.com/admin
- API: https://your-domain.com/api

---

## 🔧 **استكشاف الأخطاء**

### **مشاكل شائعة وحلولها**

#### **خطأ في الاتصال بقاعدة البيانات**
```bash
# فحص حالة PostgreSQL
sudo systemctl status postgresql

# إعادة تشغيل الخدمة
sudo systemctl restart postgresql
```

#### **خطأ في الملفات الثابتة**
```bash
# إعادة جمع الملفات الثابتة
python manage.py collectstatic --clear --noinput
```

#### **خطأ في الصلاحيات**
```bash
# إصلاح صلاحيات الملفات
sudo chown -R www-data:www-data /opt/gaara_erp_v5
sudo chmod -R 755 /opt/gaara_erp_v5
```

---

## 📞 **الدعم والصيانة**

### **صيانة دورية**
- **يومياً:** مراقبة السجلات والأداء
- **أسبوعياً:** فحص النسخ الاحتياطي
- **شهرياً:** تحديث النظام والحزم
- **ربع سنوياً:** مراجعة الأمان والأداء

### **التواصل للدعم**
- **البريد الإلكتروني:** support@gaara-erp.com
- **الهاتف:** +966-XX-XXX-XXXX
- **الدعم الفني:** متاح 24/7

---

*دليل النشر - نظام Gaara ERP*  
*الإصدار 1.0 - ديسمبر 2024*  
*جميع الحقوق محفوظة*
