# 🗣️ ماذا تقول للذكاء الاصطناعي: دليل الأوامر (Diamond 26)

**الإصدار:** 26.0.0 (Diamond 26)
**تاريخ التحديث:** 2026-02-17

---

## 🎯 القاعدة الأساسية

اكتب المطلوب بكلامك مباشرة. لا تستخدم أقواس فارغة أو قوالب جاهزة.
كلما كان وصفك واضحاً ومحدداً، كانت النتيجة أفضل.

---

## 🚀 1. أول تشغيل — مشروع جديد من الصفر

عند بدء مشروع جديد، ملفات `memory-bank/` تكون فارغة.
لذلك نطلب من الـ AI أن **يملأها** (لا أن يقرأها).

**انسخ والصق، ثم عدّل الجزء الأخير حسب مشروعك:**

```markdown
أنت تعمل الآن تحت إطار Global System v26 Diamond 32 v26.0 Diamond.

هذا أول تشغيل لمشروع جديد. ملفات memory-bank/ فارغة وستملؤها أنت.

أولاً اقرأ قواعد النظام:
1. @AGENTS.md
2. @CLAUDE.md
3. @BOOTSTRAP.md
4. @rules/00-iron-rules.md
5. @prompts/GLOBAL_PROFESSIONAL_CORE_PROMPT.md

ثانياً ابدأ كـ Architect واملأ ملفات memory-bank/ بالمعلومات التالية:

المشروع: [اسم المشروع]
التقنيات: [التقنيات المستخدمة]
الهدف: [وصف الهدف]

الملفات التي يجب أن تملأها:
- memory-bank/projectBrief.md — اسم المشروع وأهدافه ومعايير النجاح
- memory-bank/techContext.md — التقنيات المختارة وأسبابها
- memory-bank/systemPatterns.md — الأنماط المعمارية (Repository, Service Layer, etc.)
- memory-bank/activeContext.md — الحالة الحالية (مرحلة التخطيط)

بعد ملء الملفات، قدّم لي خطة العمل قبل أي كود.
```

---

## 🔄 2. مشروع قائم — memory-bank فيه بيانات

عند الاستمرار في مشروع قائم، ملفات `memory-bank/` تحتوي على سياق المشروع.
لذلك نطلب من الـ AI أن **يقرأها** أولاً ثم ينفّذ المهمة.

**انسخ والصق، ثم عدّل السطر الأخير فقط:**

```markdown
أنت تعمل الآن تحت إطار Global System v26 Diamond 32 v26.0 Diamond.

هذا مشروع قائم. اقرأ الملفات بالترتيب:
1. @AGENTS.md و @CLAUDE.md و @rules/00-iron-rules.md
2. @memory-bank/activeContext.md
3. @memory-bank/projectBrief.md
4. @memory-bank/techContext.md
5. @memory-bank/systemPatterns.md
6. @errors/DONT_MAKE_THESE_ERRORS_AGAIN.md

بعد القراءة، أخبرني بما فهمته عن حالة المشروع، ثم نفّذ المطلوب:

[اكتب طلبك هنا]
```

---

## 🧬 3. مهام ML/AI

نفس مشروع قائم لكن أضف قراءة ملفات ML:

```markdown
أنت تعمل الآن تحت إطار Global System v26 Diamond 32 v26.0 Diamond.

هذا مشروع ML قائم. اقرأ الملفات بالترتيب:
1. @AGENTS.md و @CLAUDE.md و @rules/00-iron-rules.md
2. @memory-bank/activeContext.md و @memory-bank/projectBrief.md
3. @rules/ml/ بالكامل
4. @errors/ml/ بالكامل
5. @workflows/ml/ML_MULTI_VIEW_WORKFLOW.md

بعد القراءة، أخبرني بما فهمته عن حالة المشروع، ثم نفّذ المطلوب:

[اكتب طلبك هنا]
```

---

## ⚡ 4. أوامر أثناء العمل

| الأمر | ماذا يفعل |
| :--- | :--- |
| **كمّل** | يكمل من حيث وقف |
| **راجع الكود** | يبدأ مراجعة كـ Reviewer |
| **اعمل الاختبارات** | يشغّل الاختبارات كـ QA |
| **ارجع للخطة** | يعود لـ activeContext.md ويلتزم بالترتيب |
| `/checkpoint` | يحفظ الحالة الحالية في memory-bank/activeContext.md |
| `/refresh` | يعيد تحميل السياق من memory-bank/ |
| `/compact` | يضغط نافذة السياق عند امتلائها |

---

## 🧠 5. حفظ معلومات في الذاكرة

> "لقد قررنا استخدام PostgreSQL كقاعدة بيانات. سجّل هذا القرار ومبرراته في memory-bank/."

> "واجهنا خطأ في الاتصال بالـ API. احفظ تفاصيل الخطأ والحل في errors/ لتجنب تكراره."

> "أضف متطلب جديد: يجب أن يدعم النظام الدفع عبر Stripe. حدّث memory-bank/projectBrief.md."

---

## 📌 ملاحظات

- رمز **@** قبل اسم الملف يعني "اقرأ هذا الملف" في Cursor و Claude Code
- في **Claude.ai (الويب)**: ارفع المجلد كاملاً أو الملفات المطلوبة مع الرسالة
- في **Cursor**: ضع مجلد Global_System_Ultimate_v26_Diamond في جذر مشروعك
- **الفرق بين أول مرة والمرات التالية**: أول مرة الـ AI **يملأ** memory-bank/. بعدها **يقرأها** ويكمل
- **القاعدة الذهبية**: اكتب المطلوب بكلامك مباشرة — كلما كنت واضحاً كانت النتيجة أفضل
