#!/usr/bin/env python3
# FILE: scripts/update_version.py | PURPOSE: Update version in project files | OWNER: DevOps Team | LAST-AUDITED: 2026-02-05
"""
سكربت تحديث رقم الإصدار في جميع ملفات المشروع.
يُستخدم من قبل semantic-release لتحديث الإصدار تلقائياً.
"""

import sys
import re
import json
from pathlib import Path


def update_version_py(version: str, file_path: Path) -> bool:
    """تحديث __version__.py"""
    content = f'''# FILE: {file_path.relative_to(Path.cwd())} | PURPOSE: Version information | OWNER: DevOps Team | LAST-AUDITED: 2026-02-05
"""
معلومات الإصدار - Gaara ERP
يتم تحديث هذا الملف تلقائياً بواسطة semantic-release
"""

__version__ = "{version}"
__version_info__ = tuple(map(int, "{version}".replace("-", ".").split(".")[:3]))

VERSION = __version__
'''

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    print(f"✅ تم تحديث {file_path}")
    return True


def update_pyproject_toml(version: str, file_path: Path) -> bool:
    """تحديث pyproject.toml"""
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding="utf-8")

    # تحديث version في [project] أو [tool.poetry]
    patterns = [
        (r'(version\s*=\s*")[^"]*(")', rf'\g<1>{version}\g<2>'),
        (r"(version\s*=\s*')[^']*(')", rf"\g<1>{version}\g<2>"),
    ]

    updated = False
    for pattern, replacement in patterns:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            updated = True
            break

    if updated:
        file_path.write_text(content, encoding="utf-8")
        print(f"✅ تم تحديث {file_path}")

    return updated


def update_package_json(version: str, file_path: Path) -> bool:
    """تحديث package.json"""
    if not file_path.exists():
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["version"] = version

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        print(f"✅ تم تحديث {file_path}")
        return True
    except (json.JSONDecodeError, KeyError):
        return False


def update_init_py(version: str, file_path: Path) -> bool:
    """تحديث __init__.py"""
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding="utf-8")

    # تحديث __version__
    patterns = [
        (r'(__version__\s*=\s*")[^"]*(")', rf'\g<1>{version}\g<2>'),
        (r"(__version__\s*=\s*')[^']*(')", rf"\g<1>{version}\g<2>"),
    ]

    updated = False
    for pattern, replacement in patterns:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            updated = True
            break

    if updated:
        file_path.write_text(content, encoding="utf-8")
        print(f"✅ تم تحديث {file_path}")

    return updated


def main():
    if len(sys.argv) < 2:
        print("❌ الاستخدام: python update_version.py <version>")
        print("   مثال: python update_version.py 1.2.3")
        sys.exit(1)

    version = sys.argv[1].lstrip("v")  # إزالة 'v' إذا كان موجوداً

    print(f"📦 تحديث الإصدار إلى: {version}")
    print("-" * 40)

    root = Path.cwd()
    updates = []

    # 1. تحديث/إنشاء __version__.py
    version_py = root / "gaara_erp" / "__version__.py"
    if update_version_py(version, version_py):
        updates.append(str(version_py))

    # 2. تحديث pyproject.toml
    pyproject = root / "pyproject.toml"
    if update_pyproject_toml(version, pyproject):
        updates.append(str(pyproject))

    # 3. تحديث package.json (إذا كان موجوداً)
    package_json = root / "package.json"
    if update_package_json(version, package_json):
        updates.append(str(package_json))

    # 4. تحديث __init__.py
    init_py = root / "gaara_erp" / "__init__.py"
    if update_init_py(version, init_py):
        updates.append(str(init_py))

    print("-" * 40)

    if updates:
        print(f"✅ تم تحديث {len(updates)} ملف(ات)")
    else:
        print("⚠️ لم يتم تحديث أي ملفات")

    return 0


if __name__ == "__main__":
    sys.exit(main())
