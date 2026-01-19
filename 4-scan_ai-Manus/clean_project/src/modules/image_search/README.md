# /home/ubuntu/image_search_integration/README.md
# مديول البحث عن صور الإصابات والآفات النباتية

## نظرة عامة

مديول البحث عن صور الإصابات والآفات النباتية هو جزء من نظام Gaara ERP، ويوفر وظائف للبحث عن صور الأمراض النباتية والآفات الزراعية والمحاصيل من الإنترنت، وتنزيلها وتخزينها في النظام. يتيح المديول للمستخدمين البحث عن الصور باستخدام استعلامات نصية، أو البحث عن صور مرتبطة بأمراض أو آفات أو محاصيل محددة موجودة في قاعدة البيانات.

## المكونات الرئيسية

### 1. عميل البحث (Search Client)

يوفر واجهة للتفاعل مع واجهات برمجة تطبيقات البحث عن الصور على الإنترنت. يدعم البحث العام عن الصور، والبحث المتخصص عن صور الأمراض والآفات والمحاصيل.

**الملف:** `search_client.py`

### 2. جامع الصور (Image Collector)

يستخدم عميل البحث لتنزيل الصور من الإنترنت، مع التحقق من صحتها وتنظيف أسماء الملفات وتخزينها في النظام.

**الملف:** `image_collector.py`

### 3. مدير التخزين (Storage Manager)

يدير تخزين الصور في النظام، بما في ذلك تنظيم الصور في مجلدات حسب الفئة والتاريخ، وتوليد أسماء ملفات فريدة.

**الملف:** `storage.py`

### 4. واجهة برمجة التطبيقات (API)

توفر نقاط نهاية RESTful للتفاعل مع وظائف البحث عن الصور وجمعها وتخزينها.

**الملف:** `api.py`

### 5. مخططات البيانات (Schemas)

تحدد هياكل البيانات المستخدمة في طلبات واستجابات واجهة برمجة التطبيقات.

**الملف:** `schemas.py`

### 6. نماذج البيانات (Models)

تحدد نماذج قاعدة البيانات لتخزين البيانات الوصفية للصور والعلاقات مع الكيانات الأخرى مثل الأمراض والآفات والمحاصيل.

**الملف:** `models.py`

### 7. واجهة المستخدم (Frontend)

توفر واجهة مستخدم تفاعلية للبحث عن الصور وعرضها وتنزيلها.

**الملف:** `frontend/image_search.vue`

## متطلبات التثبيت

### المتطلبات الأساسية

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pillow
- Requests
- Vue.js (للواجهة الأمامية)

### تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

## الإعداد

### 1. إعداد متغيرات البيئة

قم بإنشاء ملف `.env` في المجلد الجذر للمشروع وأضف المتغيرات التالية:

```
IMAGE_SEARCH_API_KEY=your_api_key_here
IMAGE_SEARCH_ENGINE_ID=your_engine_id_here
IMAGE_SEARCH_API_ENDPOINT=https://www.googleapis.com/customsearch/v1
```

### 2. إعداد مجلدات التخزين

تأكد من وجود المجلدات التالية وأن لديها أذونات الكتابة المناسبة:

```bash
mkdir -p /data/images/plant_images/diseases
mkdir -p /data/images/plant_images/pests
mkdir -p /data/images/plant_images/crops
mkdir -p /data/images/plant_images/uploads
```

## الاستخدام

### البحث عن الصور

```python
from search_client import search_client

# البحث العام عن الصور
image_urls = search_client.search_images("wheat leaf rust", count=10)

# البحث عن صور مرض محدد
image_urls = search_client.search_images_by_disease("leaf rust", count=10)

# البحث عن صور آفة محددة
image_urls = search_client.search_images_by_pest("aphid", count=10)

# البحث عن صور محصول محدد
image_urls = search_client.search_images_by_crop("wheat", condition="healthy", count=10)
```

### جمع وتنزيل الصور

```python
from image_collector import ImageCollector

collector = ImageCollector({
    "download_path": "/tmp/images/web_search_collected",
    "min_download_delay_seconds": 0.5,
    "max_download_delay_seconds": 2.0
})

# جمع صور بناءً على كلمات مفتاحية
collected_images = collector.collect_images_by_keywords(
    keywords=["wheat leaf rust", "wheat disease"],
    max_images_per_keyword=10
)

# جمع صور لمرض محدد
collected_images = collector.collect_images_by_disease("leaf rust", max_images=20)

# جمع صور لآفة محددة
collected_images = collector.collect_images_by_pest("aphid", max_images=20)

# جمع صور لمحصول محدد
collected_images = collector.collect_images_by_crop("wheat", condition="healthy", max_images=20)
```

### تخزين الصور

```python
from storage import ImageStorage

storage = ImageStorage({
    "base_storage_path": "/data/images/plant_images"
})

# تخزين صورة
stored_path = storage.store_image("/path/to/image.jpg", category="diseases")

# حذف صورة
success = storage.delete_image(stored_path)

# نقل صورة إلى فئة مختلفة
new_path = storage.move_image(stored_path, new_category="pests")

# الحصول على عنوان URL للصورة
image_url = storage.get_image_url(stored_path, base_url="http://example.com")
```

## واجهة برمجة التطبيقات (API)

### نقاط النهاية الرئيسية

- `POST /api/image-search/search`: البحث عن صور باستخدام استعلام نصي
- `POST /api/image-search/collect`: جمع وتنزيل صور بناءً على كلمات مفتاحية
- `POST /api/image-search/search/disease`: البحث عن صور لمرض محدد
- `POST /api/image-search/search/pest`: البحث عن صور لآفة محددة
- `POST /api/image-search/search/crop`: البحث عن صور لمحصول محدد
- `POST /api/image-search/upload`: رفع صورة جديدة إلى النظام

## الاختبارات

لتشغيل اختبارات الوحدة:

```bash
cd tests
python -m unittest discover
```

## المساهمة

1. قم بعمل fork للمشروع
2. قم بإنشاء فرع للميزة الجديدة (`git checkout -b feature/amazing-feature`)
3. قم بعمل commit للتغييرات (`git commit -m 'Add some amazing feature'`)
4. قم بدفع الفرع (`git push origin feature/amazing-feature`)
5. قم بفتح طلب سحب (Pull Request)

## الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف LICENSE للتفاصيل.

## الاعتمادات

- [Google Custom Search API](https://developers.google.com/custom-search/v1/overview)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pillow](https://python-pillow.org/)
- [Vue.js](https://vuejs.org/)
