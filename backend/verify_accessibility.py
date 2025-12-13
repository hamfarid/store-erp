#!/usr/bin/env python3
"""
أداة التحقق من إصلاح مشاكل Accessibility
تتحقق من وجود جميع الخصائص المطلوبة
"""

import re
from pathlib import Path


def check_accessibility_issues(file_path):
    """فحص مشاكل Accessibility في ملف HTML"""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        issues = []

        # فحص الأزرار بدون aria-label أو title
        button_pattern = r"<button[^>]*(?!.*aria-label)(?!.*title)[^>]*>"
        buttons_without_labels = re.findall(
            button_pattern,
            content,
            re.IGNORECASE,
        )

        # استثناء الأزرار التي تحتوي على نص واضح
        problematic_buttons = []
        for button in buttons_without_labels:
            if "navbar-toggler" in button or "btn-close" in button:
                problematic_buttons.append(button)

        if problematic_buttons:
            issues.append(f"أزرار بدون aria-label أو title: {len(problematic_buttons)}")

        # فحص عناصر select بدون aria-label أو title
        select_pattern = r"<select[^>]*(?!.*aria-label)(?!.*title)[^>]*>"
        selects_without_labels = re.findall(
            select_pattern,
            content,
            re.IGNORECASE,
        )

        if selects_without_labels:
            issues.append(
                f"عناصر select بدون aria-label أو title: {len(selects_without_labels)}"
            )

        # فحص حقول input بدون aria-label أو placeholder أو title
        input_pattern = r'<input[^>]*type="(?:text|number|email)"[^>]*(?!.*aria-label)(?!.*placeholder)(?!.*title)[^>]*>'
        inputs_without_labels = re.findall(
            input_pattern,
            content,
            re.IGNORECASE,
        )

        if inputs_without_labels:
            issues.append(f"حقول input بدون تسميات: {len(inputs_without_labels)}")

        return issues

    except Exception as e:
        return [f"خطأ في فحص الملف: {e}"]


def verify_all_files():
    """التحقق من جميع ملفات HTML"""

    static_dir = Path("src/static")

    if not static_dir.exists():
        print("❌ مجلد src/static غير موجود")
        return

    html_files = list(static_dir.glob("*.html"))

    if not html_files:
        print("❌ لا توجد ملفات HTML في مجلد src/static")
        return

    print(f"🔍 فحص {len(html_files)} ملف HTML...")
    print("=" * 60)

    total_issues = 0
    files_with_issues = 0

    for html_file in html_files:
        issues = check_accessibility_issues(html_file)

        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"❌ {html_file.name}:")
            for issue in issues:
                print(f"   • {issue}")
        else:
            print(f"✅ {html_file.name}: لا توجد مشاكل")

    print("=" * 60)

    if total_issues == 0:
        print("🎉 ممتاز! جميع الملفات متوافقة مع معايير Accessibility")
    else:
        print(f"⚠️  تم العثور على {total_issues} مشكلة في {files_with_issues} ملف")
        print("💡 يُنصح بتشغيل أداة الإصلاح مرة أخرى")


def check_specific_elements():
    """فحص عناصر محددة في currencies.html"""

    file_path = Path("src/static/currencies.html")

    if not file_path.exists():
        print("❌ ملف currencies.html غير موجود")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        print("\n🔍 فحص تفصيلي لملف currencies.html:")
        print("-" * 40)

        # عد العناصر المختلفة
        aria_labels = len(re.findall(r'aria-label="[^"]*"', content))
        titles = len(re.findall(r'title="[^"]*"', content))
        placeholders = len(re.findall(r'placeholder="[^"]*"', content))

        print(f"✅ عدد aria-label: {aria_labels}")
        print(f"✅ عدد title: {titles}")
        print(f"✅ عدد placeholder: {placeholders}")

        # فحص عناصر محددة
        navbar_togglers = len(re.findall(r"navbar-toggler[^>]*aria-label", content))
        btn_closes = len(re.findall(r"btn-close[^>]*aria-label", content))
        selects_with_labels = len(re.findall(r"<select[^>]*aria-label", content))
        inputs_with_labels = len(
            re.findall(r"<input[^>]*(?:aria-label|placeholder)", content)
        )

        print(f"✅ أزرار navbar-toggler مع تسميات: {navbar_togglers}")
        print(f"✅ أزرار btn-close مع تسميات: {btn_closes}")
        print(f"✅ عناصر select مع تسميات: {selects_with_labels}")
        print(f"✅ حقول input مع تسميات: {inputs_with_labels}")

    except Exception as e:
        print(f"❌ خطأ في فحص currencies.html: {e}")


if __name__ == "__main__":
    verify_all_files()
    check_specific_elements()
