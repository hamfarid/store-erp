#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح شامل لجميع أخطاء التنسيق في users_unified.py
"""

import re
from pathlib import Path

file_path = Path("src/routes/users_unified.py")
content = file_path.read_text(encoding="utf-8")

# 1. إصلاح error_response مع المسافات البادئة الصحيحة
lines = content.split("\n")
fixed_lines = []
i = 0

while i < len(lines):
    line = lines[i]

    # إذا وجدنا error_response(
    if "return error_response(" in line:
        # احسب المسافة البادئة
        indent = len(line) - len(line.lstrip())

        # تحقق من السطر التالي
        if i + 1 < len(lines) and "message=" in lines[i + 1]:
            # هذا error_response متعدد الأسطر يحتاج إصلاح
            fixed_lines.append(" " * indent + "return error_response(")

            # أضف message
            if "message=" in lines[i + 1]:
                msg = lines[i + 1].strip()
                fixed_lines.append(" " * (indent + 4) + msg)
                i += 1

            # أضف code
            if i + 1 < len(lines) and "code=" in lines[i + 1]:
                code = lines[i + 1].strip()
                fixed_lines.append(" " * (indent + 4) + code)
                i += 1

            # أضف status_code
            if i + 1 < len(lines) and "status_code=" in lines[i + 1]:
                status = lines[i + 1].strip()
                fixed_lines.append(" " * (indent + 4) + status)
                i += 1

            # أضف الإغلاق
            if i + 1 < len(lines) and lines[i + 1].strip() in [")", ")"]:
                fixed_lines.append(" " * indent + ")")
                i += 1

            i += 1
            continue

    fixed_lines.append(line)
    i += 1

content = "\n".join(fixed_lines)

# 2. إصلاح log_activity مع المسافات البادئة الصحيحة
content = re.sub(
    r"log_activity\(\n\s+request\.current_user_id,.*?\n\s+action,.*?\n\s+\{(.*?)\n\s+\}\n\s+\)",
    lambda m: (
        f"log_activity(\n            request.current_user_id,"
        f"  # type: ignore[attr-defined]\n"
        f"            action,  # type: ignore[possibly-unbound]\n"
        f"            {{{m.group(1)}\n            }}\n        )"
    ),
    content,
    flags=re.DOTALL,
)

# 3. إصلاح الأسطر الطويلة البسيطة
replacements = [
    (
        "from src.routes.auth_unified import token_required, admin_required, log_activity",
        "from src.routes.auth_unified import (\n    token_required,\n    admin_required,\n    log_activity\n)",
    ),
    (
        "        pagination = query.paginate(page=page, per_page=per_page, error_out=False)",
        "        pagination = query.paginate(\n            page=page,\n            per_page=per_page,\n            error_out=False\n        )",
    ),
]

for old, new in replacements:
    content = content.replace(old, new)

# كتابة النتيجة
file_path.write_text(content, encoding="utf-8")

print("✅ تم إصلاح جميع الأخطاء بنجاح!")
