#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح المسافات البادئة في error_response
"""

from pathlib import Path
import re


def fix_indentation():
    file_path = Path("src/routes/users_unified.py")
    content = file_path.read_text(encoding="utf-8")

    # إصلاح error_response مع مسافات بادئة خاطئة
    # Pattern: return error_response(\n            message=... (بدون مسافات إضافية)

    lines = content.split("\n")
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # إذا وجدنا error_response(
        if "return error_response(" in line and i + 1 < len(lines):
            # احسب المسافة البادئة الأساسية
            base_indent = len(line) - len(line.lstrip())

            # أضف السطر الأول
            fixed_lines.append(line)
            i += 1

            # تحقق من الأسطر التالية
            params = []
            while i < len(lines):
                next_line = lines[i]
                stripped = next_line.strip()

                # إذا كان السطر يحتوي على معامل
                if stripped.startswith(("message=", "code=", "status_code=")):
                    params.append(stripped)
                    i += 1
                elif stripped == ")":
                    # نهاية error_response
                    # أضف جميع المعاملات بالمسافات الصحيحة
                    for param in params:
                        fixed_lines.append(" " * (base_indent + 4) + param)
                    fixed_lines.append(" " * base_indent + ")")
                    i += 1
                    break
                else:
                    # سطر آخر، توقف
                    break
        else:
            fixed_lines.append(line)
            i += 1

    content = "\n".join(fixed_lines)

    # إصلاح السطر 3
    content = content.replace("#!/usr/bin/env python3", "# !/usr/bin/env python3")

    # إزالة الأسطر الفارغة مع مسافات
    content = re.sub(r"^\s+$", "", content, flags=re.MULTILINE)

    # إصلاح السطر الأول الطويل
    if content.startswith("# FILE: backend/src/routes"):
        first_line_end = content.index("\n")
        first_line = content[:first_line_end]
        rest = content[first_line_end:]

        # تقسيم السطر الأول
        new_first = """# FILE: backend/src/routes/users_unified.py
# PURPOSE: Routes with P0.2.4 error envelope
# OWNER: Backend
# RELATED: middleware/error_envelope_middleware.py
# LAST-AUDITED: 2025-10-25"""

        content = new_first + rest

    file_path.write_text(content, encoding="utf-8")

    print("✅ تم إصلاح المسافات البادئة!")


if __name__ == "__main__":
    fix_indentation()
