#!/usr/bin/env python3
"""
أداة تنسيق خاصة لملف currencies.html
تقوم بإعادة تنسيق الملف المضغوط وجعله قابل للقراءة
"""

import re


def format_currencies_html():
    """إعادة تنسيق ملف currencies.html"""

    file_path = "src/static/currencies.html"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # إعادة تنسيق HTML
        content = format_html_structure(content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ تم تنسيق {file_path} بنجاح")

    except Exception as e:
        print(f"❌ خطأ في تنسيق {file_path}: {e}")


def format_html_structure(content):
    """إعادة تنسيق بنية HTML"""

    # إزالة التعليقات المتتالية وإضافة أسطر جديدة
    content = re.sub(r'<!--[^>]*-->', '\n<!-- تعليق -->\n', content)

    # تنسيق العناصر الأساسية
    content = re.sub(r'<!DOCTYPE html>', '<!DOCTYPE html>\n', content)
    content = re.sub(r'<html([^>]*)>', r'<html\1>\n', content)
    content = re.sub(r'<head>', '<head>\n', content)
    content = re.sub(r'</head>', '\n</head>\n', content)
    content = re.sub(r'<body>', '<body>\n', content)
    content = re.sub(r'</body>', '\n</body>\n', content)
    content = re.sub(r'</html>', '\n</html>', content)

    # تنسيق meta tags
    content = re.sub(r'<meta([^>]*)>', r'\n    <meta\1>', content)
    content = re.sub(r'<title>', '\n    <title>', content)
    content = re.sub(r'</title>', '</title>\n', content)
    content = re.sub(r'<link([^>]*)>', r'\n    <link\1>', content)

    # تنسيق style
    content = re.sub(r'<style>', '\n    <style>\n', content)
    content = re.sub(r'</style>', '\n    </style>\n', content)

    # تنسيق العناصر الهيكلية
    content = re.sub(r'<nav([^>]*)>', r'\n<nav\1>\n', content)
    content = re.sub(r'</nav>', '\n</nav>\n', content)

    content = re.sub(r'<div([^>]*)>', r'\n<div\1>\n', content)
    content = re.sub(r'</div>', '\n</div>\n', content)

    content = re.sub(r'<form([^>]*)>', r'\n<form\1>\n', content)
    content = re.sub(r'</form>', '\n</form>\n', content)

    content = re.sub(r'<table([^>]*)>', r'\n<table\1>\n', content)
    content = re.sub(r'</table>', '\n</table>\n', content)

    content = re.sub(r'<script([^>]*)>', r'\n<script\1>\n', content)
    content = re.sub(r'</script>', '\n</script>\n', content)

    # تنظيف المسافات الزائدة
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r'^\s+$', '', content, flags=re.MULTILINE)

    # إضافة مسافات للعناصر المتداخلة
    lines = content.split('\n')
    formatted_lines = []
    indent_level = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # تقليل المسافة للعناصر المغلقة
        if line.startswith('</') and not line.startswith('<!--'):
            indent_level = max(0, indent_level - 1)

        # إضافة المسافات
        formatted_lines.append('    ' * indent_level + line)

        # زيادة المسافة للعناصر المفتوحة
        if (line.startswith('<') and not line.startswith('</') and
            not line.startswith('<!--') and not line.endswith('/>')):
            # تحقق من أن العنصر لا ينتهي في نفس السطر
            tag_name = line.split()[0][1:].split('>')[0]
            if f'</{tag_name}>' not in line:
                indent_level += 1

    return '\n'.join(formatted_lines)


if __name__ == "__main__":
    format_currencies_html()
