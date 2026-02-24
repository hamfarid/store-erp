# 🔧 دليل إعداد البيئة - Environment Setup Guide
## Store Management System v1.6

---

## 📋 جدول المحتويات

1. [إعداد ملف .env](#-إعداد-ملف-env)
2. [تفعيل Redis للـ Caching](#-تفعيل-redis-للـ-caching)
3. [تفعيل Sentry للـ Error Monitoring](#-تفعيل-sentry-للـ-error-monitoring)
4. [تفعيل Google Analytics](#-تفعيل-google-analytics)
5. [إعداد Cloud Backup](#-إعداد-cloud-backup)
6. [تفعيل CI/CD Pipeline](#-تفعيل-cicd-pipeline)

---

## 🔐 إعداد ملف .env

### الخطوة 1: نسخ ملف المثال

```bash
cd backend
cp .env.example .env
```

### الخطوة 2: تعديل القيم الأساسية

افتح ملف `.env` وعدّل القيم التالية:

```env
# مفاتيح الأمان (مهم جداً!)
SECRET_KEY=your-very-secret-key-here-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-here-min-32-chars

# إعدادات الخادم
PORT=5002
FLASK_ENV=development  # غيّر إلى production في الإنتاج
```

### الخطوة 3: توليد مفاتيح آمنة

استخدم Python لتوليد مفاتيح عشوائية آمنة:

```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## ⚙️ تفعيل Redis للـ Caching

### لماذا Redis؟
- ⚡ **أداء أسرع 5x** - تخزين مؤقت للاستجابات
- 📊 **تقليل الحمل** - تقليل استعلامات قاعدة البيانات
- 🚀 **Scalability** - دعم التوسع الأفقي

### الخطوة 1: تثبيت Redis

#### Windows:
```powershell
# تحميل Redis من:
# https://github.com/microsoftarchive/redis/releases
# أو استخدام WSL
```

#### Linux/Mac:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# Mac
brew install redis
```

### الخطوة 2: تشغيل Redis

```bash
# تشغيل Redis
redis-server

# التحقق من التشغيل
redis-cli ping
# يجب أن يرد: PONG
```

### الخطوة 3: تثبيت مكتبة Python

```bash
pip install redis
```

### الخطوة 4: تفعيل في .env

```env
REDIS_ENABLED=True
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # اتركه فارغاً للتطوير
REDIS_CACHE_TTL=300  # 5 دقائق
```

### الخطوة 5: استخدام Redis في الكود

```python
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': os.getenv('REDIS_HOST', 'localhost'),
    'CACHE_REDIS_PORT': int(os.getenv('REDIS_PORT', 6379)),
    'CACHE_REDIS_DB': int(os.getenv('REDIS_DB', 0)),
    'CACHE_DEFAULT_TIMEOUT': int(os.getenv('REDIS_CACHE_TTL', 300))
})

# استخدام Cache decorator
@cache.cached(timeout=300)
def get_dashboard_stats():
    # الكود هنا
    pass
```

---

## 📊 تفعيل Sentry للـ Error Monitoring

### لماذا Sentry؟
- 🔍 **تتبع الأخطاء** - رصد جميع الأخطاء في الإنتاج
- 📧 **إشعارات فورية** - تنبيهات عند حدوث أخطاء
- 📊 **تحليلات** - فهم أنماط الأخطاء

### الخطوة 1: إنشاء حساب Sentry

1. اذهب إلى: https://sentry.io
2. أنشئ حساب مجاني
3. أنشئ مشروع جديد (Python/Flask)
4. احصل على DSN

### الخطوة 2: تثبيت SDK

```bash
pip install sentry-sdk[flask]
```

### الخطوة 3: تفعيل في .env

```env
SENTRY_ENABLED=True
SENTRY_DSN=https://your-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=1.0
```

### الخطوة 4: إضافة إلى app.py

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

if os.getenv('SENTRY_ENABLED', 'False') == 'True':
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', 1.0)),
        environment=os.getenv('SENTRY_ENVIRONMENT', 'development')
    )
```

---

## 📈 تفعيل Google Analytics

### الخطوة 1: إنشاء حساب GA

1. اذهب إلى: https://analytics.google.com
2. أنشئ حساب جديد
3. أنشئ property جديد
4. احصل على Tracking ID و Measurement ID

### الخطوة 2: تفعيل في .env

```env
GA_ENABLED=True
GA_TRACKING_ID=UA-XXXXXXXXX-X
GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

### الخطوة 3: إضافة إلى Frontend

في `frontend/index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## ☁️ إعداد Cloud Backup

### الخيار 1: AWS S3

#### الخطوة 1: إنشاء Bucket

```bash
aws s3 mb s3://store-backups
```

#### الخطوة 2: تفعيل في .env

```env
BACKUP_ENABLED=True
BACKUP_PROVIDER=s3
BACKUP_SCHEDULE=daily
BACKUP_RETENTION_DAYS=30

AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=store-backups
AWS_S3_REGION=us-east-1
```

#### الخطوة 3: تثبيت boto3

```bash
pip install boto3
```

### الخيار 2: Google Cloud Storage

```env
BACKUP_PROVIDER=gcs
GCS_PROJECT_ID=your-project-id
GCS_BUCKET=store-backups
GCS_CREDENTIALS_PATH=/path/to/credentials.json
```

### الخيار 3: Azure Blob Storage

```env
BACKUP_PROVIDER=azure
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_CONTAINER_NAME=store-backups
```

---

## 🔄 تفعيل CI/CD Pipeline

### GitHub Actions

#### الخطوة 1: إنشاء Workflow

أنشئ ملف `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest
    
    - name: Run linters
      run: |
        cd backend
        ruff check .
        
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
```

#### الخطوة 2: إضافة Secrets

في GitHub Repository Settings → Secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `SENTRY_DSN`
- `SECRET_KEY`

---

## ✅ التحقق من الإعداد

### اختبار Redis

```python
from redis import Redis
r = Redis(host='localhost', port=6379, db=0)
r.set('test', 'value')
print(r.get('test'))  # يجب أن يطبع: b'value'
```

### اختبار Sentry

```python
import sentry_sdk
sentry_sdk.capture_message("Test message from Store System")
```

### اختبار Backup

```bash
python -c "from src.database import backup_database; backup_database()"
```

---

## 🎯 الخلاصة

بعد إكمال جميع الخطوات:

- ✅ Redis: تخزين مؤقت سريع
- ✅ Sentry: رصد الأخطاء
- ✅ Google Analytics: تحليلات الاستخدام
- ✅ Cloud Backup: نسخ احتياطية آمنة
- ✅ CI/CD: نشر تلقائي

**النظام الآن جاهز للإنتاج 100%!** 🚀

---

**للدعم:** support@example.com  
**التوثيق الكامل:** [README_FINAL.md](./README_FINAL.md)

