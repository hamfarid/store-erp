#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 سكريبت البحث عن الكود المكرر
Duplicate Code Detection Script

يبحث عن:
- الدوال المكررة
- الفئات المكررة  
- الملفات المتشابهة
- الكود المنسوخ
"""

import os
import hashlib
import difflib
from pathlib import Path
from collections import defaultdict
import ast
import re

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_error(message):
    print(f"❌ {message}")

def get_file_hash(file_path):
    """حساب hash للملف"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def get_function_signatures(file_path):
    """استخراج توقيعات الدوال من ملف Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # استخراج اسم الدالة والمعاملات
                args = [arg.arg for arg in node.args.args]
                signature = f"{node.name}({', '.join(args)})"
                
                # استخراج جسم الدالة (أول 3 أسطر)
                body_lines = []
                for stmt in node.body[:3]:
                    if hasattr(stmt, 'lineno'):
                        line_content = content.split('\n')[stmt.lineno-1].strip()
                        if line_content and not line_content.startswith('#'):
                            body_lines.append(line_content)
                
                functions.append({
                    'name': node.name,
                    'signature': signature,
                    'body_preview': ' | '.join(body_lines),
                    'line': node.lineno
                })
        
        return functions
    except:
        return []

def get_class_signatures(file_path):
    """استخراج توقيعات الفئات من ملف Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # استخراج الفئات الأساسية
                bases = [base.id if hasattr(base, 'id') else str(base) for base in node.bases]
                
                # استخراج الطرق
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                
                classes.append({
                    'name': node.name,
                    'bases': bases,
                    'methods': methods[:5],  # أول 5 طرق
                    'line': node.lineno
                })
        
        return classes
    except:
        return []

def find_similar_files():
    """البحث عن الملفات المتشابهة"""
    print_step("البحث عن الملفات المتشابهة...")
    
    file_hashes = defaultdict(list)
    similar_files = []
    
    # جمع جميع ملفات Python
    for root, dirs, files in os.walk('.'):
        # تجاهل المجلدات غير المرغوبة
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)
                if file_hash:
                    file_hashes[file_hash].append(file_path)
    
    # العثور على الملفات المتطابقة
    for file_hash, paths in file_hashes.items():
        if len(paths) > 1:
            similar_files.append(paths)
    
    return similar_files

def find_duplicate_functions():
    """البحث عن الدوال المكررة"""
    print_step("البحث عن الدوال المكررة...")
    
    function_signatures = defaultdict(list)
    duplicate_functions = []
    
    # جمع جميع الدوال
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                functions = get_function_signatures(file_path)
                
                for func in functions:
                    key = f"{func['name']}_{func['body_preview']}"
                    function_signatures[key].append({
                        'file': file_path,
                        'function': func
                    })
    
    # العثور على الدوال المكررة
    for signature, occurrences in function_signatures.items():
        if len(occurrences) > 1:
            duplicate_functions.append({
                'signature': signature,
                'occurrences': occurrences
            })
    
    return duplicate_functions

def find_duplicate_classes():
    """البحث عن الفئات المكررة"""
    print_step("البحث عن الفئات المكررة...")
    
    class_signatures = defaultdict(list)
    duplicate_classes = []
    
    # جمع جميع الفئات
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                classes = get_class_signatures(file_path)
                
                for cls in classes:
                    key = f"{cls['name']}_{','.join(cls['methods'])}"
                    class_signatures[key].append({
                        'file': file_path,
                        'class': cls
                    })
    
    # العثور على الفئات المكررة
    for signature, occurrences in class_signatures.items():
        if len(occurrences) > 1:
            duplicate_classes.append({
                'signature': signature,
                'occurrences': occurrences
            })
    
    return duplicate_classes

def create_repeat_code_folder():
    """إنشاء مجلد repeat_code"""
    repeat_folder = Path('./repeat_code')
    repeat_folder.mkdir(exist_ok=True)
    return repeat_folder

def move_duplicate_files(similar_files, repeat_folder):
    """نقل الملفات المكررة"""
    moved_files = []
    
    for file_group in similar_files:
        if len(file_group) > 1:
            # الاحتفاظ بالملف الأول، نقل الباقي
            original_file = file_group[0]
            
            for duplicate_file in file_group[1:]:
                try:
                    # إنشاء مسار الوجهة
                    relative_path = Path(duplicate_file).relative_to('.')
                    dest_path = repeat_folder / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # نقل الملف
                    import shutil
                    shutil.move(duplicate_file, dest_path)
                    moved_files.append({
                        'original': original_file,
                        'moved': str(dest_path),
                        'source': duplicate_file
                    })
                    
                except Exception as e:
                    print_warning(f"فشل نقل {duplicate_file}: {e}")
    
    return moved_files

def generate_report(similar_files, duplicate_functions, duplicate_classes, moved_files):
    """إنشاء تقرير شامل"""
    report = []
    
    report.append("# 🔍 تقرير الكود المكرر - Duplicate Code Report")
    report.append("=" * 60)
    report.append("")
    
    # الملفات المتشابهة
    report.append("## 📁 الملفات المتطابقة تماماً")
    if similar_files:
        for i, file_group in enumerate(similar_files, 1):
            report.append(f"\n### المجموعة {i}:")
            for file_path in file_group:
                report.append(f"- {file_path}")
    else:
        report.append("✅ لا توجد ملفات متطابقة تماماً")
    
    report.append("")
    
    # الدوال المكررة
    report.append("## 🔧 الدوال المكررة")
    if duplicate_functions:
        for i, dup in enumerate(duplicate_functions, 1):
            report.append(f"\n### الدالة المكررة {i}:")
            report.append(f"**التوقيع:** {dup['signature']}")
            report.append("**المواقع:**")
            for occ in dup['occurrences']:
                report.append(f"- {occ['file']} (السطر {occ['function']['line']})")
    else:
        report.append("✅ لا توجد دوال مكررة")
    
    report.append("")
    
    # الفئات المكررة
    report.append("## 📦 الفئات المكررة")
    if duplicate_classes:
        for i, dup in enumerate(duplicate_classes, 1):
            report.append(f"\n### الفئة المكررة {i}:")
            report.append(f"**التوقيع:** {dup['signature']}")
            report.append("**المواقع:**")
            for occ in dup['occurrences']:
                report.append(f"- {occ['file']} (السطر {occ['class']['line']})")
    else:
        report.append("✅ لا توجد فئات مكررة")
    
    report.append("")
    
    # الملفات المنقولة
    report.append("## 📦 الملفات المنقولة إلى repeat_code")
    if moved_files:
        for moved in moved_files:
            report.append(f"- **الأصلي:** {moved['original']}")
            report.append(f"  **المنقول:** {moved['moved']}")
            report.append(f"  **المصدر:** {moved['source']}")
            report.append("")
    else:
        report.append("✅ لم يتم نقل أي ملفات")
    
    # إحصائيات
    report.append("")
    report.append("## 📊 الإحصائيات")
    report.append(f"- **الملفات المتطابقة:** {len(similar_files)} مجموعة")
    report.append(f"- **الدوال المكررة:** {len(duplicate_functions)} دالة")
    report.append(f"- **الفئات المكررة:** {len(duplicate_classes)} فئة")
    report.append(f"- **الملفات المنقولة:** {len(moved_files)} ملف")
    
    return "\n".join(report)

def main():
    print("🔍 بدء البحث عن الكود المكرر...")
    print("=" * 50)
    
    # البحث عن التكرارات
    similar_files = find_similar_files()
    duplicate_functions = find_duplicate_functions()
    duplicate_classes = find_duplicate_classes()
    
    # إنشاء مجلد repeat_code
    repeat_folder = create_repeat_code_folder()
    print_success(f"تم إنشاء مجلد: {repeat_folder}")
    
    # نقل الملفات المكررة
    moved_files = move_duplicate_files(similar_files, repeat_folder)
    
    # إنشاء التقرير
    report = generate_report(similar_files, duplicate_functions, duplicate_classes, moved_files)
    
    # حفظ التقرير
    with open('duplicate_code_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("=" * 50)
    print_success("تم إكمال البحث عن الكود المكرر!")
    print(f"📊 النتائج:")
    print(f"   - الملفات المتطابقة: {len(similar_files)} مجموعة")
    print(f"   - الدوال المكررة: {len(duplicate_functions)} دالة")
    print(f"   - الفئات المكررة: {len(duplicate_classes)} فئة")
    print(f"   - الملفات المنقولة: {len(moved_files)} ملف")
    print(f"📄 التقرير محفوظ في: duplicate_code_report.md")

if __name__ == "__main__":
    main()
