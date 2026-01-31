# تقرير حالة حاويات Scraper و ML
**التاريخ:** 2026-01-23  
**المشاريع:** Project 2 (gold-price-predictor) و Project 4 (scan_ai-Manus)

## 📊 ملخص شامل

### حاويات Scraper

#### Project 2 (gold-price-predictor):
| الخدمة | النوع | الحالة | الملاحظات |
|--------|------|--------|-----------|
| **scraper service** | Service (في worker) | ⚠️ غير منفصلة | موجودة كخدمة داخل `ml-platform-worker` |
| **NewsScraper** | Python Class | ✅ موجودة | في `ml-services/services/scraper/main.py` |
| **scraper container** | Docker Container | ❌ غير موجودة | ليست حاوية منفصلة |

**الوظيفة:**
- ✅ Scraping الأخبار من SerpAPI, RSS, NewsAPI
- ✅ Caching مع Redis
- ✅ Rate limiting
- ✅ موجودة في `ml-platform-worker` container

#### Project 4 (scan_ai-Manus):
| الخدمة | النوع | الحالة | الملاحظات |
|--------|------|--------|-----------|
| **image_crawler** | Docker Container | ✅ **running** | `scan_ai-Manus-ai` (Port: 4601) |
| **ImageCrawler** | Python Service | ✅ موجودة | في `image_crawler/crawler.py` |
| **ImageAnalyzer** | Python Service | ✅ موجودة | تحليل الصور |

**الوظيفة:**
- ✅ Crawling صور أمراض النباتات
- ✅ تحليل الصور
- ✅ Knowledge base management
- ✅ ✅ **الحاوية تعمل:** `scan_ai-Manus-ai` (healthy)

### حاويات ML

#### Project 2 (gold-price-predictor):
| الحاوية | الحالة | Port | Health | الملاحظات |
|---------|--------|------|--------|-----------|
| **gold-price-predictor-ml** | ❌ **غير موجودة** | 2101 | - | موجودة في docker-compose لكن غير مشغلة |
| **ml-platform-mlflow** | ✅ running | 5000 | ✅ healthy | MLflow tracking server |
| **ml-platform-worker** | ⚠️ غير موجودة | - | - | Worker service (يحتوي scraper) |

**التعلم/التدريب:**
- ⚠️ **لا يوجد تدريب تلقائي** - الكود موجود لكن placeholder
- ✅ يوجد `train_model_job` في Celery tasks
- ⚠️ Training module غير مطبق بالكامل (commented out)
- ✅ يوجد drift detection لكن placeholder

**الكود:**
```python
# في tasks.py:
@celery_app.task(name="predictor.train_model")
def train_model_job(...):
    # Training would happen here
    # result = train_model(asset_symbol, model_type, config)  # Commented
    result = {...}  # Placeholder
```

#### Project 4 (scan_ai-Manus):
| الحاوية | الحالة | Port | Health | الملاحظات |
|---------|--------|------|--------|-----------|
| **scan_ai-Manus-ml** | ✅ **running** | 4101 | ✅ healthy | ML service للـ disease diagnosis |
| **scan_ai-Manus-ai** | ✅ **running** | 4601 | ✅ healthy | Image crawler service |

**التعلم/التدريب:**
- ⚠️ **لا يوجد تدريب تلقائي** - يستخدم نماذج pre-trained
- ✅ يستخدم YOLOv5 (pre-trained) للكشف
- ✅ يستخدم Confidence Calibrator (fit method موجود)
- ⚠️ لا يوجد scheduled training أو auto-retraining

**الكود:**
```python
# في ml_service/main.py:
# لا يوجد training endpoints
# يستخدم YOLO pre-trained models

# في confidence_calibrator.py:
calibrator.fit(val_logits, val_labels)  # Calibration فقط
```

## 🔍 تفاصيل الحاويات

### 1. scan_ai-Manus-ml (✅ تعمل)
- **الحالة:** ✅ running - healthy
- **Port:** 4101
- **الوظيفة:** Disease diagnosis using YOLO
- **التعلم:** ⚠️ لا يوجد - يستخدم pre-trained models
- **Health Check:** ✅ `http://localhost:4101/health` → 200 OK

### 2. scan_ai-Manus-ai (✅ تعمل)
- **الحالة:** ✅ running - healthy  
- **Port:** 4601
- **الوظيفة:** Image crawling و analysis
- **التعلم:** ⚠️ لا يوجد - crawler فقط
- **Health Check:** ✅ `http://localhost:4601/health` → 200 OK

### 3. gold-price-predictor-ml (❌ غير موجودة)
- **الحالة:** ❌ غير مشغلة
- **Port:** 2101 (محدد في docker-compose)
- **السبب:** الحاوية غير مشغلة رغم وجودها في docker-compose.yml
- **الإجراء المطلوب:** تشغيل الحاوية

### 4. ml-platform-worker (⚠️ غير موجودة)
- **الحالة:** ⚠️ غير موجودة كحاوية منفصلة
- **الوظيفة:** يحتوي على scraper service
- **الموقع:** `ml-services/services/worker/`
- **Scraper:** موجود في `ml-services/services/scraper/`

## 📝 تحليل التعلم/التدريب

### Project 2 (gold-price-predictor):
| الميزة | الحالة | التفاصيل |
|--------|--------|----------|
| **Training Jobs** | ⚠️ Placeholder | `train_model_job` موجود لكن غير مطبق |
| **Auto Retraining** | ⚠️ Placeholder | `retrain_model_job` موجود لكن غير مطبق |
| **Drift Detection** | ⚠️ Placeholder | `detect_drift_job` موجود لكن placeholder |
| **Scheduled Training** | ❌ غير موجود | لا يوجد cron jobs أو scheduled tasks |
| **Continuous Learning** | ❌ غير موجود | لا يوجد online learning |

### Project 4 (scan_ai-Manus):
| الميزة | الحالة | التفاصيل |
|--------|--------|----------|
| **Training** | ❌ غير موجود | يستخدم pre-trained YOLOv5 فقط |
| **Calibration** | ✅ موجود | `confidence_calibrator.fit()` |
| **Auto Retraining** | ❌ غير موجود | لا يوجد scheduled training |
| **Continuous Learning** | ❌ غير موجود | لا يوجد online learning |
| **Model Updates** | ❌ غير موجود | لا يوجد mechanism لتحديث النماذج |

## 🔧 الإصلاحات المطلوبة

### 1. ✅ scan_ai-Manus-ml و scan_ai-Manus-ai
- **الحالة:** ✅ تعملان بشكل صحيح
- **لا حاجة لإصلاح**

### 2. ❌ gold-price-predictor-ml
- **المشكلة:** الحاوية غير مشغلة
- **الإصلاح:** تشغيل الحاوية من docker-compose

```bash
cd 2-gold-price-predictor
docker-compose up -d ml
```

### 3. ⚠️ ML Learning/Training
- **المشكلة:** لا يوجد تدريب تلقائي في أي من المشروعين
- **التوصية:** 
  - Project 2: تطبيق training module في `train_model_job`
  - Project 4: إضافة scheduled training للـ YOLO models

## 📊 النتيجة النهائية

### Scraper Containers:
- ✅ **scan_ai-Manus-ai** (image crawler) → ✅ تعمل
- ⚠️ **gold-price-predictor scraper** → موجودة كخدمة في worker (غير منفصلة)

### ML Containers:
- ✅ **scan_ai-Manus-ml** → ✅ تعمل (healthy)
- ✅ **scan_ai-Manus-ai** → ✅ تعمل (healthy)
- ❌ **gold-price-predictor-ml** → ❌ غير مشغلة
- ✅ **ml-platform-mlflow** → ✅ تعمل (healthy)

### ML Learning Status:
- ⚠️ **لا يوجد تدريب تلقائي** في أي من المشروعين
- ⚠️ **لا يوجد continuous learning**
- ✅ **Pre-trained models** مستخدمة في scan_ai-Manus
- ⚠️ **Training code** موجود لكن placeholder في gold-price-predictor

---

**ملاحظة:** يجب تشغيل `gold-price-predictor-ml` وإضافة training functionality إذا كان مطلوباً.
