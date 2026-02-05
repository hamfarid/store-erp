# FILE: .github/CONTRIBUTING.md | PURPOSE: Contribution guidelines | OWNER: Maintainers | LAST-AUDITED: 2026-02-05

# 🤝 دليل المساهمة في Gaara ERP

شكراً لاهتمامك بالمساهمة في مشروع Gaara ERP! 🎉

## 📋 جدول المحتويات

- [قواعد السلوك](#-قواعد-السلوك)
- [كيف أساهم؟](#-كيف-أساهم)
- [إعداد بيئة التطوير](#-إعداد-بيئة-التطوير)
- [سير العمل](#-سير-العمل)
- [معايير الكود](#-معايير-الكود)
- [رسائل الالتزام](#-رسائل-الالتزام)

---

## 📜 قواعد السلوك

نلتزم بتوفير بيئة ترحيبية وشاملة للجميع. نرجو منك:

- ✅ استخدام لغة مهذبة ومحترمة
- ✅ احترام وجهات النظر المختلفة
- ✅ قبول النقد البناء بروح رياضية
- ✅ التركيز على ما هو أفضل للمشروع والمجتمع

---

## 💡 كيف أساهم؟

### 🐛 الإبلاغ عن الأخطاء

1. تأكد من عدم وجود تقرير مشابه في [Issues](../../issues)
2. استخدم قالب "تقرير خطأ"
3. قدم أكبر قدر من التفاصيل

### ✨ اقتراح ميزات

1. افتح Issue جديد باستخدام قالب "طلب ميزة"
2. اشرح الفائدة من الميزة
3. قدم أمثلة على الاستخدام

### 💻 المساهمة بالكود

1. Fork المستودع
2. أنشئ فرع للميزة/الإصلاح
3. اكتب اختبارات للكود الجديد
4. تأكد من اجتياز جميع الاختبارات
5. أنشئ Pull Request

---

## 🔧 إعداد بيئة التطوير

### المتطلبات

- Python 3.11+
- Node.js 18+ (للأدوات)
- Git
- Docker (اختياري)

### خطوات الإعداد

```bash
# 1. استنساخ المستودع
git clone https://github.com/hamfarid/gaara_erp.git
cd gaara_erp

# 2. إنشاء البيئة الافتراضية
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# أو
.venv\Scripts\activate     # Windows

# 3. تثبيت المتطلبات
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. تثبيت أدوات Git hooks
npm install
npx husky install

# 5. إعداد قاعدة البيانات
cd gaara_erp
python manage.py migrate
python manage.py createsuperuser

# 6. تشغيل الخادم
python manage.py runserver
```

---

## 🔄 سير العمل

### 1. إنشاء فرع جديد

```bash
# تحديث develop
git checkout develop
git pull origin develop

# إنشاء فرع الميزة
git checkout -b feature/my-new-feature

# أو فرع إصلاح
git checkout -b fix/bug-description
```

### 2. العمل على التغييرات

```bash
# إجراء التغييرات
# ...

# فحص الكود
black gaara_erp/
flake8 gaara_erp/

# تشغيل الاختبارات
pytest
```

### 3. الالتزام

```bash
git add .
git commit -m "feat(module): add new feature"
```

### 4. رفع الفرع

```bash
git push origin feature/my-new-feature
```

### 5. إنشاء Pull Request

- اذهب إلى GitHub
- أنشئ Pull Request من فرعك إلى `develop`
- املأ القالب بالكامل
- انتظر المراجعة

---

## 📝 معايير الكود

### Python

- نتبع [PEP 8](https://pep8.org/)
- نستخدم [Black](https://black.readthedocs.io/) للتنسيق
- نستخدم [isort](https://pycqa.github.io/isort/) لترتيب الاستيرادات
- نستخدم [flake8](https://flake8.pycqa.org/) للفحص

```bash
# تنسيق الكود
black gaara_erp/
isort gaara_erp/

# فحص الكود
flake8 gaara_erp/
```

### التوثيق

- كل دالة/صف يجب أن يحتوي على docstring
- استخدم Google style للـ docstrings

```python
def calculate_total(items: list[Item], tax_rate: float = 0.15) -> Decimal:
    """
    حساب المجموع الكلي مع الضريبة.
    
    Args:
        items: قائمة العناصر للحساب
        tax_rate: نسبة الضريبة (افتراضي 15%)
    
    Returns:
        المجموع الكلي شاملاً الضريبة
    
    Raises:
        ValueError: إذا كانت قائمة العناصر فارغة
    """
    ...
```

---

## 💬 رسائل الالتزام

نتبع [Conventional Commits](https://www.conventionalcommits.org/):

### الصيغة

```
<type>(<scope>): <subject>

<body>

<footer>
```

### الأنواع

| النوع | الوصف |
|-------|-------|
| `feat` | ميزة جديدة |
| `fix` | إصلاح خطأ |
| `docs` | تحديث التوثيق |
| `style` | تنسيق الكود |
| `refactor` | إعادة هيكلة |
| `perf` | تحسين الأداء |
| `test` | اختبارات |
| `build` | تغييرات البناء |
| `ci` | تغييرات CI/CD |
| `chore` | مهام صيانة |

### أمثلة

```bash
# ميزة جديدة
git commit -m "feat(auth): add two-factor authentication"

# إصلاح خطأ
git commit -m "fix(invoice): resolve Arabic number formatting"

# تغيير كاسر
git commit -m "feat(api)!: change response format

BREAKING CHANGE: API responses now use new envelope format"
```

---

## 🏷️ التسميات (Labels)

| التسمية | الوصف |
|---------|-------|
| `bug` | خطأ يحتاج إصلاح |
| `enhancement` | طلب ميزة جديدة |
| `documentation` | تحسين التوثيق |
| `good first issue` | مناسب للمساهمين الجدد |
| `help wanted` | يحتاج مساعدة |
| `priority: high` | أولوية عالية |
| `priority: low` | أولوية منخفضة |

---

## ❓ أسئلة؟

- افتح [Discussion](../../discussions) للأسئلة العامة
- افتح [Issue](../../issues) للمشاكل التقنية

---

**شكراً لمساهمتك! 🙏**
