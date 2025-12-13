#!/usr/bin/env python3
"""
أداة إعادة تنسيق ملفات HTML
تقوم بإعادة تنسيق الملفات المضغوطة وجعلها قابلة للقراءة
"""

import re
from pathlib import Path


def format_html_content(content):
    """إعادة تنسيق محتوى HTML"""

    # إزالة التعليقات المتتالية
    content = re.sub(r'<!--[^>]*--><!--[^>]*-->', '<!-- تعليق -->', content)

    # إضافة أسطر جديدة بعد العناصر الرئيسية
    content = re.sub(r'><', '>\n<', content)
    content = re.sub(r'<!DOCTYPE html>', '<!DOCTYPE html>\n', content)
    content = re.sub(r'<html([^>]*)>', r'<html\1>\n', content)
    content = re.sub(r'<head>', '<head>\n    ', content)
    content = re.sub(r'</head>', '\n</head>', content)
    content = re.sub(r'<body>', '<body>\n', content)
    content = re.sub(r'</body>', '\n</body>', content)
    content = re.sub(r'</html>', '\n</html>', content)

    # تنسيق العناصر الأساسية
    content = re.sub(r'<meta([^>]*)>', r'    <meta\1>', content)
    content = re.sub(r'<title>', '    <title>', content)
    content = re.sub(r'<link([^>]*)>', r'    <link\1>', content)
    content = re.sub(r'<style>', '    <style>', content)
    content = re.sub(r'</style>', '    </style>', content)

    # تنسيق العناصر الهيكلية
    content = re.sub(r'<nav([^>]*)>', r'<nav\1>\n    ', content)
    content = re.sub(r'</nav>', '\n</nav>', content)
    content = re.sub(r'<div([^>]*)>', r'<div\1>\n        ', content)
    content = re.sub(r'</div>', '\n    </div>', content)

    # تنظيف المسافات الزائدة
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r'^\s+$', '', content, flags=re.MULTILINE)

    return content


def format_html_file(file_path):
    """إعادة تنسيق ملف HTML واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # التحقق من أن الملف مضغوط (أقل من 10 أسطر)
        line_count = len(content.split('\n'))
        if line_count < 10:
            formatted_content = format_html_content(content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            print(f"✅ تم تنسيق: {file_path}")
            return True
        else:
            print(f"ℹ️  لا يحتاج تنسيق: {file_path}")
            return False

    except Exception as e:
        print(f"❌ خطأ في تنسيق {file_path}: {e}")
        return False


def main():
    """الدالة الرئيسية"""
    static_dir = Path("src/static")

    if not static_dir.exists():
        print("❌ مجلد src/static غير موجود")
        return

    html_files = list(static_dir.glob("*.html"))

    if not html_files:
        print("❌ لا توجد ملفات HTML في مجلد src/static")
        return

    print(f"📝 بدء تنسيق {len(html_files)} ملف HTML...")

    formatted_count = 0
    for html_file in html_files:
        if format_html_file(html_file):
            formatted_count += 1

    print(f"\n🎉 تم الانتهاء! تم تنسيق {formatted_count} "
          f"من {len(html_files)} ملف")
    print()  # Add a blank line after the output


if __name__ == "__main__":
    main()
