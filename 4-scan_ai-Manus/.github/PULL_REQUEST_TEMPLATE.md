## وصف التغييرات | Description
<!-- قدم وصفاً موجزاً للتغييرات التي أجريتها -->


## نوع التغيير | Change Type
- [ ] 🐛 إصلاح خطأ (Bug fix)
- [ ] ✨ ميزة جديدة (New feature)
- [ ] 💥 تغيير كاسر (Breaking change)
- [ ] 📝 تحديث التوثيق (Documentation update)
- [ ] 🔧 تحسين الأداء (Performance improvement)
- [ ] ♻️ إعادة هيكلة الكود (Code refactoring)
- [ ] 🔒 إصلاح أمني (Security fix)
- [ ] 🎨 تحسين واجهة المستخدم (UI/UX improvement)

## المشاكل المرتبطة | Related Issues
<!-- اربط المشاكل ذات الصلة باستخدام الكلمات المفتاحية -->
Closes #
Relates to #

## التغييرات المُنفذة | Changes Made
<!-- قائمة بالتغييرات الرئيسية -->
- 
- 
- 

## لقطات الشاشة | Screenshots
<!-- إذا كانت التغييرات تؤثر على الواجهة، أضف لقطات شاشة -->
| قبل | بعد |
|-----|-----|
|     |     |

## الاختبارات | Testing
### Backend
- [ ] اختبارات الوحدة تمر بنجاح (Unit tests pass)
- [ ] اختبارات التكامل تمر بنجاح (Integration tests pass)
- [ ] لا توجد تحذيرات جديدة من flake8/black

### Frontend
- [ ] اختبارات الوحدة تمر بنجاح (Unit tests pass)
- [ ] لا توجد أخطاء ESLint جديدة
- [ ] تم اختبار الواجهة يدوياً

### عام | General
- [ ] تم اختبار التغييرات محلياً
- [ ] تم اختبار Docker build بنجاح

## قائمة التحقق | Checklist
### جودة الكود | Code Quality
- [ ] الكود يتبع إرشادات المشروع (Code follows project guidelines)
- [ ] راجعت الكود ذاتياً (I have self-reviewed the code)
- [ ] أضفت التعليقات اللازمة للكود المعقد (Added comments for complex code)
- [ ] لا توجد أخطاء إملائية (No typos)

### التوثيق | Documentation
- [ ] حدّثت README إذا لزم الأمر (Updated README if needed)
- [ ] أضفت/حدّثت docstrings للدوال الجديدة
- [ ] حدّثت API documentation إذا تغيرت الـ endpoints

### الأمان | Security
- [ ] لا توجد بيانات حساسة مكشوفة (No sensitive data exposed)
- [ ] تم التحقق من صحة المدخلات (Input validation added)
- [ ] لا توجد ثغرات SQL injection أو XSS

### قاعدة البيانات | Database
- [ ] أضفت migration files إذا تغير الـ schema
- [ ] التغييرات متوافقة مع البيانات الموجودة (Backward compatible)

## ملاحظات للمراجعين | Notes for Reviewers
<!-- أي معلومات إضافية تساعد المراجعين -->


## قائمة النشر | Deployment Checklist
<!-- للتغييرات التي تتطلب إعدادات خاصة عند النشر -->
- [ ] متغيرات بيئة جديدة مطلوبة (New environment variables needed)
- [ ] تحديث قاعدة البيانات مطلوب (Database migration needed)
- [ ] تغيير في إعدادات الخادم (Server configuration changes)
- [ ] لا حاجة لإعدادات خاصة (No special requirements)

### متغيرات البيئة الجديدة | New Environment Variables
<!-- إذا أضفت متغيرات بيئة جديدة، اذكرها هنا -->
```
VARIABLE_NAME=description
```

---
### تذكير | Reminder
- 🔴 تأكد من أن جميع الاختبارات تمر قبل طلب المراجعة
- 🔴 اطلب مراجعة من شخصين على الأقل للتغييرات الكبيرة
- 🔴 لا تدمج PR حتى تحصل على الموافقات المطلوبة
