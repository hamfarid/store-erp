# دليل استخدام Docker - Gaara Scan AI
**Path:** /home/ubuntu/gaara_scan_ai/DOCKER_GUIDE.md  
**الإصدار:** v4.3.1  
**التاريخ:** 13 ديسمبر 2025

---

## المحتويات

1. [نظرة عامة](#نظرة-عامة)
2. [المتطلبات](#المتطلبات)
3. [البنية الأساسية](#البنية-الأساسية)
4. [التثبيت والتشغيل](#التثبيت-والتشغيل)
5. [إدارة الحاويات](#إدارة-الحاويات)
6. [استكشاف الأخطاء](#استكشاف-الأخطاء)

---

## نظرة عامة

يستخدم مشروع Gaara Scan AI نظام Docker لتوفير بيئة تطوير وإنتاج موحدة ومعزولة. يتكون النظام من **4 خدمات رئيسية**:

| الخدمة | الوصف | المنفذ |
|---|---|---|
| **database** | PostgreSQL 16 | 5432 |
| **redis** | Redis 7 (Cache & Sessions) | 6379 |
| **backend** | FastAPI Backend | 1005 |
| **frontend** | React + Vite + Nginx | 1505 |

---

## المتطلبات

### البرامج المطلوبة

```bash
# Docker
docker --version  # يجب أن يكون >= 20.10

# Docker Compose
docker compose version  # يجب أن يكون >= 2.0
```

### متطلبات النظام

- **RAM:** 4 GB كحد أدنى (8 GB موصى به)
- **Storage:** 10 GB مساحة حرة
- **CPU:** معالج ثنائي النواة كحد أدنى

---

## البنية الأساسية

### هيكل الملفات

```
gaara_scan_ai/
├── docker-compose.yml          # الملف الرئيسي للإنتاج
├── .dockerignore               # ملفات مستبعدة من البناء
├── .env                        # متغيرات البيئة
├── backend/
│   └── Dockerfile             # صورة Backend
├── frontend/
│   └── Dockerfile             # صورة Frontend
├── docker/                     # ملفات Docker إضافية
│   ├── docker-compose.yml     # نسخة موسعة مع خدمات إضافية
│   ├── postgres/
│   ├── redis/
│   └── nginx/
└── data/                       # بيانات دائمة (Volumes)
    ├── postgres/
    ├── redis/
    ├── uploads/
    ├── results/
    ├── logs/
    ├── backups/
    └── models/
```

### الشبكات (Networks)

```yaml
gaara_network:
  subnet: 172.20.0.0/16
  gateway: 172.20.0.1
```

### الأحجام (Volumes)

| Volume | المسار | الوصف |
|---|---|---|
| `postgres_data` | `./data/postgres` | بيانات قاعدة البيانات |
| `redis_data` | `./data/redis` | بيانات Redis |
| `backend_uploads` | `./data/uploads` | ملفات المستخدمين |
| `backend_results` | `./data/results` | نتائج التشخيص |
| `backend_logs` | `./data/logs/backend` | سجلات Backend |
| `frontend_logs` | `./data/logs/frontend` | سجلات Frontend |
| `backend_backups` | `./data/backups` | النسخ الاحتياطية |
| `ai_models` | `./data/models` | نماذج الذكاء الاصطناعي |

---

## التثبيت والتشغيل

### 1. إعداد البيئة

```bash
# نسخ ملف البيئة
cp .env.example .env

# تعديل المتغيرات حسب الحاجة
nano .env
```

### 2. إنشاء المجلدات المطلوبة

```bash
# إنشاء جميع المجلدات
mkdir -p data/{postgres,redis,uploads,results,logs/{backend,frontend},backups,models}

# تعيين الصلاحيات
chmod -R 755 data/
```

### 3. بناء الصور (Build)

```bash
# بناء جميع الصور
docker compose build

# بناء صورة محددة
docker compose build backend
docker compose build frontend
```

### 4. تشغيل الخدمات

```bash
# تشغيل جميع الخدمات
docker compose up -d

# تشغيل خدمة محددة
docker compose up -d database
docker compose up -d backend

# عرض السجلات
docker compose logs -f backend
docker compose logs -f frontend
```

### 5. التحقق من الحالة

```bash
# عرض حالة الحاويات
docker compose ps

# فحص صحة الخدمات
docker compose exec backend curl http://localhost:1005/api/v1/health
docker compose exec frontend wget -O- http://localhost/health
```

---

## إدارة الحاويات

### الأوامر الأساسية

```bash
# إيقاف الخدمات
docker compose stop

# إعادة تشغيل الخدمات
docker compose restart

# إيقاف وحذف الحاويات
docker compose down

# إيقاف وحذف الحاويات والأحجام
docker compose down -v

# عرض استخدام الموارد
docker stats
```

### الوصول إلى الحاويات

```bash
# الدخول إلى Backend
docker compose exec backend bash

# الدخول إلى قاعدة البيانات
docker compose exec database psql -U gaara_user -d gaara_scan_ai

# الدخول إلى Redis
docker compose exec redis redis-cli
```

### النسخ الاحتياطي

```bash
# نسخ احتياطي لقاعدة البيانات
docker compose exec database pg_dump -U gaara_user gaara_scan_ai > backup.sql

# استعادة النسخة الاحتياطية
docker compose exec -T database psql -U gaara_user gaara_scan_ai < backup.sql
```

---

## استكشاف الأخطاء

### المشكلة: الحاوية لا تبدأ

```bash
# عرض السجلات
docker compose logs backend

# فحص الحالة
docker compose ps

# إعادة بناء الصورة
docker compose build --no-cache backend
docker compose up -d backend
```

### المشكلة: خطأ في الاتصال بقاعدة البيانات

```bash
# التحقق من تشغيل قاعدة البيانات
docker compose ps database

# فحص الاتصال
docker compose exec backend python -c "import psycopg2; psycopg2.connect('postgresql://gaara_user:gaara_secure_2024@database:5432/gaara_scan_ai')"
```

### المشكلة: نفاد المساحة

```bash
# حذف الصور غير المستخدمة
docker image prune -a

# حذف الأحجام غير المستخدمة
docker volume prune

# حذف كل شيء غير مستخدم
docker system prune -a --volumes
```

### المشكلة: بطء الأداء

```bash
# زيادة الموارد المخصصة
# تعديل docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 2G  # زيادة الذاكرة
      cpus: '2'   # زيادة المعالجات
```

---

## متغيرات البيئة الهامة

### قاعدة البيانات

```bash
POSTGRES_DB=gaara_scan_ai
POSTGRES_USER=gaara_user
POSTGRES_PASSWORD=gaara_secure_2024
DB_PORT=5432
```

### Backend

```bash
APP_PORT=1005
WORKERS=4
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
```

### Frontend

```bash
FRONTEND_PORT=1505
REACT_APP_API_URL=http://localhost:1005/api
```

### Redis

```bash
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
```

---

## الأمان

### أفضل الممارسات

1. **تغيير كلمات المرور الافتراضية**
   ```bash
   # في ملف .env
   POSTGRES_PASSWORD=your_strong_password
   SECRET_KEY=your_secret_key
   JWT_SECRET=your_jwt_secret
   ```

2. **استخدام HTTPS في الإنتاج**
   - تكوين شهادات SSL/TLS
   - استخدام Nginx كـ Reverse Proxy

3. **تقييد الوصول للمنافذ**
   ```yaml
   ports:
     - "127.0.0.1:5432:5432"  # فقط localhost
   ```

4. **تحديث الصور بانتظام**
   ```bash
   docker compose pull
   docker compose up -d
   ```

---

## الإنتاج (Production)

### التحضير للإنتاج

1. **تعيين المتغيرات الصحيحة**
   ```bash
   ENVIRONMENT=production
   DEBUG=false
   ```

2. **استخدام Docker Secrets**
   ```yaml
   secrets:
     db_password:
       file: ./secrets/db_password.txt
   ```

3. **تفعيل المراقبة**
   - استخدام Prometheus + Grafana
   - تكوين التنبيهات

4. **النسخ الاحتياطي التلقائي**
   - جدولة النسخ الاحتياطية
   - تخزين النسخ في مكان آمن

---

## الخلاصة

نظام Docker في Gaara Scan AI مصمم ليكون:

- ✅ **سهل الاستخدام**: أوامر بسيطة للبدء
- ✅ **قابل للتوسع**: إضافة خدمات جديدة بسهولة
- ✅ **آمن**: أفضل الممارسات الأمنية مطبقة
- ✅ **موثوق**: Health checks ومراقبة مستمرة

للمزيد من المساعدة، راجع التوثيق الرسمي لـ [Docker](https://docs.docker.com/) و [Docker Compose](https://docs.docker.com/compose/).
