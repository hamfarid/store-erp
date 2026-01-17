#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة إصلاح أخطاء Flake8 تلقائياً
"""

import os
import re
import sys

def fix_flake8_errors(file_path):
    """إصلاح أخطاء Flake8 في ملف"""
    print(f"🔧 إصلاح أخطاء Flake8 في: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # إصلاح E304: blank lines found after function decorator
            if (i > 0 and
                lines[i-1].strip().startswith('@') and
                line.strip() == '' and
                i + 1 < len(lines) and
                lines[i+1].strip().startswith('def ')):
                # تخطي السطر الفارغ بعد decorator
                i += 1
                continue

            # إصلاح E303: too many blank lines
            if line.strip() == '':
                # عد الأسطر الفارغة المتتالية
                empty_count = 0
                j = i
                while j < len(lines) and lines[j].strip() == '':
                    empty_count += 1
                    j += 1

                # السماح بحد أقصى سطرين فارغين
                if empty_count > 2:
                    # إضافة سطرين فارغين فقط
                    fixed_lines.append('\n')
                    fixed_lines.append('\n')
                    i = j
                    continue
                else:
                    fixed_lines.append(line)

            # إصلاح الأسطر الطويلة (E501)
            elif len(line.rstrip()) > 79:
                # محاولة تقسيم الأسطر الطويلة
                stripped = line.rstrip()
                indent = len(line) - len(line.lstrip())

                # إذا كان السطر يحتوي على 'and' أو 'or'
                if ' and ' in stripped or ' or ' in stripped:
                    # تقسيم عند العوامل المنطقية
                    if ' and ' in stripped:
                        parts = stripped.split(' and ')
                        operator = ' and'
                    else:
                        parts = stripped.split(' or ')
                        operator = ' or'

                    if len(parts) == 2:
                        fixed_lines.append(' ' * indent + parts[0] + operator + '\n')
                        fixed_lines.append(' ' * (indent + 8) + parts[1] + '\n')
                        i += 1
                        continue

                # إذا كان السطر يحتوي على قاموس أو قائمة
                elif '{' in stripped and '}' in stripped:
                    # تقسيم عند الفواصل
                    if ', ' in stripped:
                        # محاولة تقسيم القاموس
                        before_brace = stripped[:stripped.find('{')]
                        after_brace = stripped[stripped.find('}'):]
                        dict_content = stripped[stripped.find('{')+1:stripped.find('}')]

                        if len(dict_content) > 40:
                            items = dict_content.split(', ')
                            fixed_lines.append(' ' * indent + before_brace + '{\n')
                            for item in items:
                                fixed_lines.append(' ' * (indent + 4) + item + ',
                                    \n')
                            fixed_lines.append(' ' * indent + '}' + after_brace + '\n')
                            i += 1
                            continue

                # إضافة السطر كما هو إذا لم نتمكن من إصلاحه
                fixed_lines.append(line)

            else:
                fixed_lines.append(line)

            i += 1

        # كتابة الملف المُصحح
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)

        print("  ✅ تم إصلاح الملف بنجاح")
        return True

    except Exception as e:
        print(f"  ❌ خطأ في إصلاح الملف: {str(e)}")
        return False

def fix_specific_decorators(file_path):
    """إصلاح مشاكل decorators المحددة"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # إصلاح الأنماط الشائعة
        patterns = [
            # إزالة الأسطر الفارغة بعد decorators
            (r'(@\w+.*\n)\n+(\s*def\s+)', r'\1\2'),
            (r'(@app\.route.*\n)\n+(\s*def\s+)', r'\1\2'),
            (r'(@wraps.*\n)\n+(\s*def\s+)', r'\1\2'),
            (r'(@login_required\n)\n+(\s*def\s+)', r'\1\2'),
            (r'(@staticmethod\n)\n+(\s*def\s+)', r'\1\2'),

            # إصلاح الأسطر الفارغة الزائدة
            (r'\n\n\n+', r'\n\n'),
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        # كتابة المحتوى المُصحح
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"خطأ في إصلاح decorators: {str(e)}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔧 أداة إصلاح أخطاء Flake8")
    print("=" * 40)

    # الملفات المراد إصلاحها
    files_to_fix = [
        'complete_inventory_system/backend/src/app_integrated.py',
        'complete_inventory_system/backend/src/auth.py'
    ]

    success_count = 0

    for file_path in files_to_fix:
        if os.path.exists(file_path):
            # إصلاح decorators أولاً
            fix_specific_decorators(file_path)

            # ثم إصلاح باقي المشاكل
            if fix_flake8_errors(file_path):
                success_count += 1
        else:
            print(f"❌ الملف غير موجود: {file_path}")

    print("\n" + "=" * 40)
    print("📊 النتائج:")
    print(f"✅ ملفات مُصلحة: {success_count}")
    print(f"📁 إجمالي الملفات: {len(files_to_fix)}")

    if success_count == len(files_to_fix):
        print("🎉 تم إصلاح جميع الملفات بنجاح!")
    else:
        print("⚠️ بعض الملفات تحتاج إلى مراجعة يدوية")

if __name__ == "__main__":
    main()
