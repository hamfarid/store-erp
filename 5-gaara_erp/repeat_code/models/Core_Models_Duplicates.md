# النماذج الأساسية المكررة

## نموذج Currency (مكرر 3 مرات):

### الملفات المكررة:
1. `core_modules/core/models.py` - النموذج الأساسي (يجب الاحتفاظ به)
2. `business_modules/accounting/models.py` - مكرر
3. `core_modules/organization/models.py` - مكرر

### النموذج الأساسي المحتفظ به:
```python
class Currency(TimestampedModel):
    """Represents a currency."""
    name = models.CharField(_("Name"), max_length=100)
    code = models.CharField(_("Code"), max_length=3, unique=True, help_text=_("ISO 4217 currency code"))
    symbol = models.CharField(_("Symbol"), max_length=5)
    exchange_rate = models.DecimalField(
        _("Exchange Rate"), max_digits=12, decimal_places=6, default=Decimal("1.0")
    )
    is_base_currency = models.BooleanField(_("Is Base Currency"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)
```

## نموذج Country (مكرر 2 مرات):

### الملفات المكررة:
1. `core_modules/core/models.py` - النموذج الأساسي (يجب الاحتفاظ به)
2. `core_modules/organization/models.py` - مكرر

## نموذج Company (مكرر 2 مرات):

### الملفات المكررة:
1. `core_modules/core/models.py` - النموذج الأساسي (يجب الاحتفاظ به)
2. `core_modules/organization/models.py` - مكرر

## نموذج Branch (مكرر 2 مرات):

### الملفات المكررة:
1. `core_modules/core/models.py` - النموذج الأساسي (يجب الاحتفاظ به)
2. `core_modules/organization/models.py` - مكرر

## نموذج Department (مكرر 3 مرات):

### الملفات المكررة:
1. `core_modules/core/models.py` - النموذج الأساسي (يجب الاحتفاظ به)
2. `core_modules/organization/models.py` - مكرر
3. `services_modules/hr/models.py` - مكرر

## الحل المقترح:
1. الاحتفاظ بجميع النماذج الأساسية في `core_modules.core.models`
2. استبدال المراجع في الملفات الأخرى بـ:
   ```python
   from core_modules.core.models import Currency, Country, Company, Branch, Department
   ```

## الإجراءات المطلوبة:
- [ ] حذف النماذج المكررة من organization/models.py
- [ ] حذف النماذج المكررة من accounting/models.py
- [ ] حذف النماذج المكررة من hr/models.py
- [ ] إضافة استيرادات من core.models
- [ ] تحديث المراجع في admin.py و serializers.py
- [ ] تحديث الترحيلات إذا لزم الأمر
