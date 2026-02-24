# OOP Fundamentals — ملخص البرمجة الكائنية (v26.0.2 Diamond 32)

> مرجع سريع لمفاهيم OOP الأساسية باللغة العربية

## ايه هي الـ OOP؟
Object Oriented Programming — طريقة في البرمجة تخلي الكود سهل الاستخدام وأقدر أستخدمه أكتر من مرة بدون تكرار.

## المبادئ الأساسية الأربعة

### 1. Encapsulation (التغليف)
أسلوب لإخفاء البيانات الأساسية في الكلاس وجعل الكلاسات الأخرى قادرة على التعامل معها فقط من خلال دوال يقوم بإنشائها المبرمج.

### 2. Inheritance (الوراثة)
عملية إنشاء كلاس جديد بناءً على كلاس سابق لإعادة استخدام أكواد مكتوبة سابقاً. الفئة الأصلية تسمى Parent والمشتقة Son/Child.

### 3. Polymorphism (تعدد الأشكال)
الكائن يمكن أن يتخذ أكتر من شكل — مجموعة كائنات ترث من أب واحد لكن كل منهم يعدل الخصائص بشكل مختلف.

### 4. Abstraction (التجريد)
إخفاء تفاصيل التنفيذ لتسهيل التعامل مع الأشياء ببساطة.

## Overloading vs Overriding
- **Overloading**: نفس الاسم، عدد/نوع بارامترات مختلف
- **Overriding**: نفس التوقيع بالكامل لكن محتوى مختلف في الـ Subclass

## Constructor (المُنشئ)
دالة خاصة تُستدعى عند إنشاء كائن. أنواعه: Parameterized و Parameterless.
- لا يكون final/synchronized/abstract/static
- يمكن أن يكون private (لن نستطيع إنشاء كائن من الكلاس)
- **Copy Constructor**: إنشاء كائن جديد من كائن قديم

## Constructor vs Methods
| Constructor | Methods |
|-------------|---------|
| تهيئة الـ object، لا يرجع قيم | وصف المتغيرات وترجع قيم |

## Destructor (المُدمر)
تعطيل الذاكرة المخصصة للكائنات. يعرّف بنفس اسم الكلاس مسبوقاً بـ (~).

## Constructor vs Destructor
| Constructor | Destructor |
|-------------|------------|
| توليد الكائنات | تدمير أماكن الكائنات |
| يستخدم معاملات | لا يستخدم معاملات |
| واحد أو أكثر في الكلاس | واحد فقط |

## Interface vs Abstract Class
- **Interface**: كل الدوال مجردة (Full abstract)، لا implementation
- **Abstract Class**: يمكن أن يحوي دوال بتنفيذ افتراضي

## Diamond Problem
مشكلة التوريث المتعدد — تكرار الأوامر عند وراثة نفس الأصل من مسارين.

## مفاهيم إضافية
- **Static vs Const**: Static باسم الكلاس بدون كائن، Const قيمة ثابتة لا تتغير
- **Extend vs Implementation**: Extend توريث، Implementation تنفيذ interface
- **Getter/Setter**: Getter ترجع قيم، Setter تستقبل قيم
- **Class vs Object**: Class نموذج (blueprint)، Object نسخة (instance)
- **Pure Virtual Function**: دالة في الكلاس الأب فقط للـ overriding
- **Static Method**: تُنادى من اسم الكلاس `ClassName.methodName()`
- **Event vs Delegate**: Event الحدث، Delegate ربط الدالة بالحدث
- **Applet**: برنامج Java قابل للتضمين في HTML

### مثال Java: فحص الأعداد الأولية
```java
public static boolean isPrime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i < Math.sqrt(n); i++)
        if (n % i == 0) return false;
    return true;
}
```
