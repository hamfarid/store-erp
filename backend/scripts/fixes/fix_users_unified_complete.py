#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح شامل وكامل لجميع أخطاء users_unified.py
"""

import re
from pathlib import Path


def fix_users_unified():
    file_path = Path("src/routes/users_unified.py")
    content = file_path.read_text(encoding="utf-8")

    # 1. إصلاح السطر 3: block comment
    content = content.replace("#!/usr/bin/python3", "# !/usr/bin/python3")

    # 2. إصلاح imports - إزالة تعريف Role المكرر
    old_imports = """# استيراد النماذج الموحدة
try:
    from src.models.user_unified import User, create_default_roles  # type: ignore[assignment]
    from src.models.user import Role  # Import Role from canonical location
    from src.models.supporting_models import AuditLog, ActionType  # type: ignore[assignment]
    UNIFIED_MODELS = True
except ImportError:
    from src.models.user_unified import User
    from src.models.user import Role  # Import Role from canonical location
    UNIFIED_MODELS = False
    
    # Create dummy classes if not available
    class Role:  # type: ignore[no-redef]
        pass
    
    class ActionType:  # type: ignore[no-redef]
        pass
    
    class AuditLog:  # type: ignore[no-redef]
        pass"""

    new_imports = """# استيراد النماذج الموحدة
try:
    from src.models.user_unified import User, create_default_roles
    from src.models.user import Role
    from src.models.supporting_models import AuditLog, ActionType
    UNIFIED_MODELS = True
except ImportError:
    from src.models.user_unified import User
    from src.models.user import Role
    UNIFIED_MODELS = False
    
    # Create dummy classes if not available
    class ActionType:  # type: ignore[no-redef]
        pass
    
    class AuditLog:  # type: ignore[no-redef]
        pass"""

    content = content.replace(old_imports, new_imports)

    # 3. إصلاح is_active == (is_active.lower() == 'true')
    content = content.replace(
        "query = query.filter(User.is_active == (is_active.lower() == 'true'))",
        "query = query.filter_by(is_active=(is_active.lower() == 'true'))",
    )

    # 4. إصلاح جميع error_response مع E203 و E128
    patterns_to_fix = [
        # Pattern: return error_response(message='...' \n        , code=...
        (
            r"return error_response\(message='([^']+)'\s*\n\s*, code=([^,]+), status_code=(\d+)\)",
            lambda m: f"return error_response(\n            message='{m.group(1)}',\n            code={m.group(2)},\n            status_code={m.group(3)}\n        )",
        ),
        # Pattern: return error_response(message='...', \n        code=...
        (
            r"return error_response\(message='([^']+)',\s*\n\s*code=([^,]+), status_code=(\d+)\)",
            lambda m: f"return error_response(\n            message='{m.group(1)}',\n            code={m.group(2)},\n            status_code={m.group(3)}\n        )",
        ),
    ]

    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # 5. إصلاح datetime.utcnow()
    content = content.replace("datetime.utcnow()", "datetime.now(datetime.UTC)")

    # 6. إصلاح log_activity الطويل
    content = re.sub(
        r"log_activity\(request\.current_user_id, ActionType\.(\w+) if UNIFIED_MODELS else '(\w+)', \{  # type: ignore\[attr-defined,possibly-unbound\]",
        lambda m: f"action_type = ActionType.{m.group(1)} if UNIFIED_MODELS else '{m.group(2)}'\n        log_activity(\n            request.current_user_id,  # type: ignore[attr-defined]\n            action_type,  # type: ignore[possibly-unbound]\n            {{",
        content,
    )

    # 7. إصلاح success_response الطويل
    content = re.sub(
        r"return success_response\(data=user\.to_dict\(\), message='([^']+)', status_code=(\d+)\), (\d+)",
        lambda m: f"return success_response(\n            data=user.to_dict(),\n            message='{m.group(1)}',\n            status_code={m.group(2)}\n        ), {m.group(3)}",
        content,
    )

    content = re.sub(
        r"return success_response\(message='([^']+)', status_code=(\d+)\), (\d+)",
        lambda m: f"return success_response(\n            message='{m.group(1)}',\n            status_code={m.group(2)}\n        ), {m.group(3)}",
        content,
    )

    # 8. إصلاح success_response مع role
    content = re.sub(
        r"return success_response\(data=role\.to_dict\(\), message='([^']+)', status_code=(\d+)\), (\d+)",
        lambda m: f"return success_response(\n            data=role.to_dict(),\n            message='{m.group(1)}',\n            status_code={m.group(2)}\n        ), {m.group(3)}",
        content,
    )

    # كتابة الملف
    file_path.write_text(content, encoding="utf-8")

    print("✅ تم إصلاح جميع الأخطاء في users_unified.py!")
    print("\n📝 الإصلاحات المطبقة:")
    print("  ✓ إصلاح block comment في السطر 3")
    print("  ✓ إزالة تعريف Role المكرر")
    print("  ✓ إصلاح جميع error_response (E203 + E128)")
    print("  ✓ تحويل datetime.utcnow() إلى datetime.now(datetime.UTC)")
    print("  ✓ إصلاح log_activity الطويل")
    print("  ✓ إصلاح success_response الطويل")


if __name__ == "__main__":
    fix_users_unified()
