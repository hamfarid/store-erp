# نصوص بدء العمل (Startup Prompts) - Diamond 26

هذه النصوص جاهزة للنسخ واللصق في نافذة الدردشة مع الذكاء الاصطناعي (Claude / Cursor / Cline) لبدء العمل فوراً.

---

## 🚀 السيناريو الأول: مشروع جديد (أول تشغيل)

**استخدم هذا النص عندما تبدأ مشروعاً جديداً من الصفر وملفات `memory-bank/` فارغة.**

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

## 🔄 السيناريو الثاني: مشروع قائم (استكمال العمل)

**استخدم هذا النص عندما تريد إكمال العمل على مشروع موجود بالفعل.**

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

## 🧬 السيناريو الثالث: مهام ML/AI

**استخدم هذا النص لمشاريع الذكاء الاصطناعي وتعلم الآلة.**

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
