#!/usr/bin/env python3
"""
سكريبت لإصلاح جميع أخطاء التنسيق في users_unified.py
"""

import re

file_path = "src/routes/users_unified.py"

# قراءة المحتوى
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# إصلاح error_response مع الفواصل على أسطر منفصلة
patterns = [
    # Pattern 1: error_response مع whitespace before comma
    (
        r"error_response\(message='([^']+)'\s*\n\s*,\s*code=([^,]+),\s*status_code=(\d+)\)",
        lambda m: f"error_response(\n            message='{m.group(1)}',\n            code={m.group(2)},\n            status_code={m.group(3)}\n        )",
    ),
    # Pattern 2: تعديل الأسطر الطويلة
    (
        r"User\.query\.filter\(User\.email == data\['email'\], User\.id != user_id\)\.first\(\)",
        "User.query.filter(\n                User.email == data['email'],\n                User.id != user_id\n            ).first()",
    ),
    # Pattern 3: إصلاح datetime.utcnow()
    (r"datetime\.utcnow\(\)", "datetime.now(datetime.UTC)"),
]

for pattern, replacement in patterns:
    if callable(replacement):
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    else:
        content = re.sub(pattern, replacement, content)

# كتابة المحتوى المعدّل
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ تم إصلاح جميع الأخطاء بنجاح!")
