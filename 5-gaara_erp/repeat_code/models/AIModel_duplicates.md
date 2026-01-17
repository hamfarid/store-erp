# نماذج AIModel المكررة

تم العثور على نموذج AIModel مكرر في 5 ملفات مختلفة:

## الملفات المكررة:
1. `./ai_modules/ai_models/models.py` - النموذج الأساسي (يجب الاحتفاظ به)
2. `./ai_modules/intelligent_assistant/models.py` - مكرر
3. `./core_modules/ai_permissions/models.py` - مكرر
4. `./integration_modules/ai_services/models.py` - مكرر
5. `./integration_modules/ai_ui/models.py` - مكرر

## الحل المقترح:
1. الاحتفاظ بالنموذج الأساسي في `ai_modules.ai_models.models.AIModel`
2. استبدال المراجع في الملفات الأخرى بـ:
   ```python
   from ai_modules.ai_models.models import AIModel
   ```

## النموذج الأساسي المحتفظ به:
```python
class AIModel(models.Model):
    """نموذج للنماذج الذكية"""
    
    MODEL_TYPE_CHOICES = [
        ("llm", _("نموذج لغوي كبير")),
        ("vision", _("رؤية حاسوبية")),
        ("nlp", _("معالجة اللغة الطبيعية")),
        ("speech", _("معالجة الكلام")),
        ("recommendation", _("نظام توصيات")),
        ("classification", _("تصنيف")),
        ("regression", _("انحدار")),
        ("clustering", _("تجميع")),
        ("custom", _("مخصص")),
    ]
    
    # ... باقي الحقول
```

## الإجراءات المطلوبة:
- [ ] حذف النماذج المكررة من الملفات الأخرى
- [ ] إضافة استيراد من النموذج الأساسي
- [ ] تحديث المراجع في admin.py و serializers.py
- [ ] تحديث الترحيلات إذا لزم الأمر
