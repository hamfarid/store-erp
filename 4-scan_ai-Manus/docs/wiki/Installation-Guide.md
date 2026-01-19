# 🚀 دليل التثبيت - Gaara AI Installation Guide

هذا الدليل يوضح كيفية تثبيت وإعداد نظام Gaara AI للزراعة الذكية بطرق مختلفة حسب احتياجاتك.

## 📋 المتطلبات الأساسية

قبل البدء في التثبيت، تأكد من توفر المتطلبات التالية على نظامك:

### متطلبات النظام
- **نظام التشغيل**: Ubuntu 20.04+, CentOS 8+, Windows 10+, macOS 10.15+
- **الذاكرة**: 4 GB RAM كحد أدنى (8 GB مُوصى به)
- **التخزين**: 10 GB مساحة فارغة كحد أدنى
- **المعالج**: معالج ثنائي النواة أو أفضل
- **الشبكة**: اتصال إنترنت مستقر

### البرامج المطلوبة

#### للتشغيل بـ Docker (الطريقة المُوصى بها)
- **Docker**: الإصدار 20.0 أو أحدث
- **Docker Compose**: الإصدار 2.0 أو أحدث
- **Git**: لاستنساخ المشروع

#### للتشغيل اليدوي
- **Python**: الإصدار 3.8 أو أحدث (3.11 مُوصى به)
- **Node.js**: الإصدار 16.0 أو أحدث (18.0 مُوصى به)
- **npm**: يأتي مع Node.js
- **Git**: لاستنساخ المشروع

## 🐳 الطريقة الأولى: التثبيت باستخدام Docker

هذه هي الطريقة الأسهل والأكثر موثوقية لتشغيل النظام.

### الخطوة 1: تثبيت Docker و Docker Compose

#### على Ubuntu/Debian
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# إضافة المستخدم الحالي لمجموعة docker
sudo usermod -aG docker $USER

# تثبيت Docker Compose
sudo apt install docker-compose-plugin -y

# إعادة تسجيل الدخول أو تشغيل
newgrp docker
```

#### على CentOS/RHEL
```bash
# تثبيت Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# تشغيل Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

#### على Windows
1. تحميل Docker Desktop من [الموقع الرسمي](https://www.docker.com/products/docker-desktop)
2. تثبيت البرنامج واتباع التعليمات
3. إعادة تشغيل الكمبيوتر

#### على macOS
```bash
# باستخدام Homebrew
brew install --cask docker
```

### الخطوة 2: استنساخ المشروع
```bash
# استنساخ المستودع
git clone https://github.com/hamfarid/gaara-ai-system.git
cd gaara-ai-system

# التحقق من محتويات المشروع
ls -la
```

### الخطوة 3: إعداد متغيرات البيئة
```bash
# نسخ ملف البيئة النموذجي
cp .env.example .env

# تحرير ملف البيئة (استخدم محرر النصوص المفضل لديك)
nano .env
# أو
vim .env
# أو
code .env
```

### الخطوة 4: تشغيل النظام
```bash
# تشغيل النظام في الخلفية
docker-compose up -d

# مراقبة السجلات
docker-compose logs -f

# التحقق من حالة الحاويات
docker-compose ps
```

### الخطوة 5: الوصول للنظام
بعد التشغيل الناجح، يمكنك الوصول للنظام عبر:

- **الواجهة الأمامية**: http://localhost:3000
- **الواجهة الخلفية**: http://localhost:5000
- **توثيق API**: http://localhost:5000/docs

## 🛠️ الطريقة الثانية: التثبيت اليدوي

إذا كنت تفضل التحكم الكامل أو تريد التطوير على النظام.

### الخطوة 1: تثبيت Python و Node.js

#### على Ubuntu/Debian
```bash
# تثبيت Python 3.11
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip -y

# تثبيت Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# التحقق من الإصدارات
python3.11 --version
node --version
npm --version
```

#### على Windows
1. تحميل Python من [python.org](https://www.python.org/downloads/)
2. تحميل Node.js من [nodejs.org](https://nodejs.org/)
3. تثبيت البرامج واتباع التعليمات

#### على macOS
```bash
# باستخدام Homebrew
brew install python@3.11 node@18

# التحقق من الإصدارات
python3.11 --version
node --version
```

### الخطوة 2: استنساخ وإعداد المشروع
```bash
# استنساخ المشروع
git clone https://github.com/hamfarid/gaara-ai-system.git
cd gaara-ai-system

# إعداد متغيرات البيئة
cp .env.example .env
```

### الخطوة 3: إعداد الواجهة الخلفية
```bash
# الانتقال لمجلد الواجهة الخلفية
cd gaara_ai_integrated/backend

# إنشاء بيئة افتراضية
python3.11 -m venv venv

# تفعيل البيئة الافتراضية
# على Linux/macOS
source venv/bin/activate
# على Windows
# venv\Scripts\activate

# تثبيت التبعيات
pip install --upgrade pip
pip install -r requirements.txt

# إعداد قاعدة البيانات
python -c "from main_api import create_tables; create_tables()"

# تشغيل الخادم
python main_api.py
```

### الخطوة 4: إعداد الواجهة الأمامية
```bash
# فتح terminal جديد والانتقال لمجلد الواجهة الأمامية
cd gaara_ai_integrated/frontend

# تثبيت التبعيات
npm install

# تشغيل الخادم التطويري
npm run dev
```

## ⚙️ الإعدادات المتقدمة

### إعداد قاعدة البيانات PostgreSQL

إذا كنت تريد استخدام PostgreSQL بدلاً من SQLite:

```bash
# تثبيت PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# إنشاء قاعدة بيانات ومستخدم
sudo -u postgres psql
CREATE DATABASE gaara_ai;
CREATE USER gaara_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE gaara_ai TO gaara_user;
\q

# تحديث ملف .env
DATABASE_URL=postgresql://gaara_user:your_password@localhost/gaara_ai
```

### إعداد Redis للكاش

```bash
# تثبيت Redis
sudo apt install redis-server -y

# تشغيل Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# تحديث ملف .env
REDIS_URL=redis://localhost:6379/0
```

### إعداد Nginx للإنتاج

```bash
# تثبيت Nginx
sudo apt install nginx -y

# إنشاء ملف تكوين
sudo nano /etc/nginx/sites-available/gaara-ai

# محتوى ملف التكوين
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# تفعيل التكوين
sudo ln -s /etc/nginx/sites-available/gaara-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔧 استكشاف الأخطاء

### مشاكل شائعة وحلولها

#### خطأ في الاتصال بقاعدة البيانات
```bash
# التحقق من حالة قاعدة البيانات
sudo systemctl status postgresql

# إعادة تشغيل الخدمة
sudo systemctl restart postgresql
```

#### خطأ في منافذ الشبكة
```bash
# التحقق من المنافذ المستخدمة
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :5000

# إيقاف العمليات المتضاربة
sudo kill -9 PID_NUMBER
```

#### مشاكل الذاكرة
```bash
# مراقبة استخدام الذاكرة
free -h
htop

# تنظيف الذاكرة
sudo sysctl vm.drop_caches=3
```

## ✅ التحقق من التثبيت

بعد التثبيت، تأكد من أن النظام يعمل بشكل صحيح:

### اختبار الواجهة الخلفية
```bash
# اختبار API الصحة
curl http://localhost:5000/health

# اختبار تسجيل الدخول
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### اختبار الواجهة الأمامية
1. افتح المتصفح وانتقل إلى http://localhost:3000
2. تأكد من ظهور صفحة تسجيل الدخول
3. سجل الدخول باستخدام: admin / admin123
4. تأكد من ظهور لوحة التحكم

### اختبار التكامل
```bash
# تشغيل اختبارات التكامل
python test_complete_integration.py
```

## 📚 الخطوات التالية

بعد التثبيت الناجح:

1. **اقرأ دليل المستخدم**: [End-User-Guide](End-User-Guide)
2. **تعرف على الميزات**: [AI-Diagnosis-System](AI-Diagnosis-System)
3. **إعداد المزرعة الأولى**: [Farm-Management](Farm-Management)
4. **تكوين أجهزة الاستشعار**: [IoT-System](IoT-System)

## 🆘 الحصول على المساعدة

إذا واجهت أي مشاكل:

1. راجع [استكشاف الأخطاء](Troubleshooting)
2. ابحث في [Issues](https://github.com/hamfarid/gaara-ai-system/issues)
3. اطرح سؤالاً في [Discussions](https://github.com/hamfarid/gaara-ai-system/discussions)
4. اتصل بالدعم الفني: support@gaara-ai.com

---

**🌱 مبروك! لقد أصبح نظام Gaara AI جاهزاً للاستخدام! 🌱**

