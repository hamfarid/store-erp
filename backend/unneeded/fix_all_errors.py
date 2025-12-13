#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح جميع أخطاء التنسيق في users_unified.py
"""

import re
from pathlib import Path

file_path = Path("src/routes/users_unified.py")

# قراءة المحتوى
content = file_path.read_text(encoding="utf-8")

# 1. إصلاح error_response مع الفواصل
pattern = (
    r"error_response\(message='([^']+)'\s*\n\s*" r", code=([^,]+), status_code=(\d+)\)"
)


def fix_error_response(match):
    msg, code, status = match.groups()
    return (
        f"error_response(\n            message='{msg}',\n"
        f"            code={code},\n"
        f"            status_code={status}\n        )"
    )


content = re.sub(pattern, fix_error_response, content, flags=re.MULTILINE)

# 2. إصلاح datetime.utcnow()
content = content.replace("datetime.utcnow()", "datetime.now(datetime.UTC)")

# 3. إصلاح success_response الطويل
pattern2 = r"success_response\(message='([^']+)', status_code=(\d+)\), (\d+)"


def fix_success_response(match):
    msg, status, code = match.groups()
    return (
        f"success_response(\n            message='{msg}',\n"
        f"            status_code={status}\n        ), {code}"
    )


content = re.sub(pattern2, fix_success_response, content)

# 4. إصلاح log_activity الطويل
pattern3 = (
    r"log_activity\(request\.current_user_id, "
    r"ActionType\.(\w+) if UNIFIED_MODELS else '(\w+)', \{"
    r"  # type: ignore\[attr-defined,possibly-unbound\]"
)


def fix_log_activity(match):
    action1, action2 = match.groups()
    return (
        f"action = ActionType.{action1} if UNIFIED_MODELS "
        f"else '{action2}'\n        log_activity(\n"
        f"            request.current_user_id,"
        f"  # type: ignore[attr-defined]\n"
        f"            action,  # type: ignore[possibly-unbound]\n"
        f"            {{"
    )


content = re.sub(pattern3, fix_log_activity, content)

# كتابة المحتوى
file_path.write_text(content, encoding="utf-8")

print("✅ تم إصلاح جميع الأخطاء!")
print("📝 المعدلات:")
print("  - error_response: تنسيق صحيح")
print("  - datetime.utcnow() -> datetime.now(datetime.UTC)")
print("  - success_response: تنسيق متعدد الأسطر")
print("  - log_activity: تنسيق محسّن")
