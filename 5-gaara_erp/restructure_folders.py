#!/usr/bin/env python3
"""
مُعيد هيكلة المجلدات - تنظيف وتوحيد هيكل المشروع
Folder Restructuring Script - Clean and unify project structure
"""

import os
import shutil
import sys
from pathlib import Path
import json
from datetime import datetime


def create_backup_info():
    """إنشاء ملف معلومات النسخة الاحتياطية"""
    backup_info = {
        "restructure_date": datetime.now().isoformat(),
        "original_structure": "complete_inventory_system/complete_inventory_system (nested)",
        "new_structure": "complete_inventory_system (single level)",
        "moved_to_unneeded": [],
        "consolidated_files": [],
        "removed_duplicates": []
    }
    return backup_info


def move_to_unneeded(source_path, unneeded_dir, backup_info):
    """نقل ملف أو مجلد إلى مجلد unneeded"""
    if not os.path.exists(source_path):
        return False
    
    source_name = os.path.basename(source_path)
    target_path = os.path.join(unneeded_dir, source_name)
    
    # إذا كان الهدف موجود، أضف timestamp
    if os.path.exists(target_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(source_name)
        target_path = os.path.join(unneeded_dir, f"{name}_{timestamp}{ext}")
    
    try:
        if os.path.isdir(source_path):
            shutil.move(source_path, target_path)
        else:
            shutil.move(source_path, target_path)
        
        backup_info["moved_to_unneeded"].append({
            "source": source_path,
            "target": target_path,
            "type": "directory" if os.path.isdir(target_path) else "file"
        })
        print(f"✅ Moved to unneeded: {source_path} -> {target_path}")
        return True
    except Exception as e:
        print(f"❌ Error moving {source_path}: {e}")
        return False


def consolidate_nested_structure(root_dir):
    """دمج الهيكل المتداخل"""
    backup_info = create_backup_info()
    
    # المسارات
    main_dir = Path(root_dir)
    nested_dir = main_dir / "complete_inventory_system"
    unneeded_dir = main_dir / "unneeded"
    
    # التأكد من وجود مجلد unneeded
    unneeded_dir.mkdir(exist_ok=True)
    
    print("🔧 بدء إعادة هيكلة المجلدات...")
    print(f"📁 المجلد الرئيسي: {main_dir}")
    print(f"📁 المجلد المتداخل: {nested_dir}")
    print(f"📁 مجلد الملفات غير المطلوبة: {unneeded_dir}")
    
    if not nested_dir.exists():
        print("ℹ️ لا يوجد مجلد متداخل للدمج")
        return backup_info
    
    # نقل محتويات المجلد المتداخل
    if nested_dir.exists():
        print("\n📦 دمج محتويات المجلد المتداخل...")
        
        for item in nested_dir.iterdir():
            item_name = item.name
            target_path = main_dir / item_name
            
            if target_path.exists():
                print(f"⚠️ يوجد تضارب: {item_name}")
                # نقل النسخة المتداخلة إلى unneeded
                conflict_name = f"nested_{item_name}"
                move_to_unneeded(str(item), str(unneeded_dir), backup_info)
            else:
                # نقل إلى المجلد الرئيسي
                try:
                    shutil.move(str(item), str(target_path))
                    backup_info["consolidated_files"].append({
                        "source": str(item),
                        "target": str(target_path)
                    })
                    print(f"✅ تم نقل: {item_name}")
                except Exception as e:
                    print(f"❌ خطأ في نقل {item_name}: {e}")
        
        # حذف المجلد المتداخل الفارغ
        try:
            nested_dir.rmdir()
            print("✅ تم حذف المجلد المتداخل الفارغ")
        except Exception as e:
            print(f"⚠️ لم يتم حذف المجلد المتداخل: {e}")
    
    return backup_info


def move_unneeded_files(root_dir, backup_info):
    """نقل الملفات غير المطلوبة إلى مجلد unneeded"""
    main_dir = Path(root_dir)
    unneeded_dir = main_dir / "unneeded"
    
    # قائمة الملفات والمجلدات المراد نقلها
    files_to_move = [
        # ملفات Python للإصلاح والتحليل
        "fix_*.py",
        "python_auto_fixer.py",
        "python_files_checker_and_fixer.py",
        "comprehensive_error_fixer.py",
        "system_cleanup_analyzer.py",
        "system_error_fixer.py",
        "systematic_system_fixer.py",
        "master_system_fixer.py",
        "final_*.py",
        "ultimate_*.py",
        "quick_*.py",
        "gap_analysis_and_fix.py",
        "install_and_setup.py",
        
        # ملفات التقارير المتعددة
        "*_REPORT.md",
        "*_STATUS*.md",
        "*_FINAL*.md",
        "*_COMPREHENSIVE*.md",
        "*_ULTIMATE*.md",
        "*_ABSOLUTE*.md",
        "BUTTONS_FIX_REPORT.md",
        "MOCKDB_FIX_REPORT.md",
        "ERROR_FIXES_*.md",
        
        # ملفات JSON للتقارير
        "*.json",
        "button_*.json",
        "system_*.json",
        "comprehensive_*.json",
        "systematic_*.json",
        
        # مجلدات __pycache__
        "__pycache__",
        
        # ملفات اختبار
        "*test*.py",
        "*test*.js",
        "*test*.html",
        
        # ملفات مؤقتة
        "*.pyc",
        "*.log",
        
        # مجلدات قديمة
        "inventory",  # المجلد القديم
        "flask_session",
        "exports",
        "uploads",
        "logs",
        "instance",
    ]
    
    print("\n🧹 نقل الملفات غير المطلوبة...")
    
    import glob
    
    for pattern in files_to_move:
        matches = list(main_dir.glob(pattern))
        for match in matches:
            if match.name != "unneeded" and not str(match).startswith(str(unneeded_dir)):
                move_to_unneeded(str(match), str(unneeded_dir), backup_info)
    
    return backup_info


def clean_duplicate_documentation(root_dir, backup_info):
    """تنظيف الوثائق المكررة"""
    main_dir = Path(root_dir)
    unneeded_dir = main_dir / "unneeded"
    
    print("\n📚 تنظيف الوثائق المكررة...")
    
    # الاحتفاظ بالملفات الأساسية فقط
    keep_docs = [
        "README.md",
        "QUICK_START.md", 
        "USER_GUIDE.md",
        "TECHNICAL_DOCUMENTATION.md",
        "API_DOCUMENTATION.md"
    ]
    
    # نقل باقي ملفات .md
    for md_file in main_dir.glob("*.md"):
        if md_file.name not in keep_docs:
            move_to_unneeded(str(md_file), str(unneeded_dir), backup_info)
    
    return backup_info


def save_backup_info(root_dir, backup_info):
    """حفظ معلومات النسخة الاحتياطية"""
    backup_file = Path(root_dir) / "unneeded" / "restructure_backup_info.json"
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        print(f"✅ تم حفظ معلومات النسخة الاحتياطية: {backup_file}")
    except Exception as e:
        print(f"❌ خطأ في حفظ معلومات النسخة الاحتياطية: {e}")


def main():
    """الدالة الرئيسية"""
    # الحصول على المجلد الحالي
    current_dir = os.getcwd()
    
    print("🚀 بدء إعادة هيكلة نظام إدارة المخزون")
    print(f"📍 المجلد الحالي: {current_dir}")
    
    # التأكد من أننا في المجلد الصحيح
    if not os.path.basename(current_dir) == "complete_inventory_system":
        print("❌ يجب تشغيل هذا السكريبت من داخل مجلد complete_inventory_system")
        sys.exit(1)
    
    # إنشاء معلومات النسخة الاحتياطية
    backup_info = create_backup_info()
    
    try:
        # 1. دمج الهيكل المتداخل
        backup_info = consolidate_nested_structure(current_dir)
        
        # 2. نقل الملفات غير المطلوبة
        backup_info = move_unneeded_files(current_dir, backup_info)
        
        # 3. تنظيف الوثائق المكررة
        backup_info = clean_duplicate_documentation(current_dir, backup_info)
        
        # 4. حفظ معلومات النسخة الاحتياطية
        save_backup_info(current_dir, backup_info)
        
        print("\n🎉 تمت إعادة الهيكلة بنجاح!")
        print("\n📋 ملخص العملية:")
        print(f"   📁 ملفات تم نقلها إلى unneeded: {len(backup_info['moved_to_unneeded'])}")
        print(f"   🔄 ملفات تم دمجها: {len(backup_info['consolidated_files'])}")
        print(f"   🗑️ ملفات مكررة تم إزالتها: {len(backup_info['removed_duplicates'])}")
        
        print("\n✅ الهيكل النهائي:")
        print("   📁 complete_inventory_system/")
        print("   ├── 📁 backend/")
        print("   ├── 📁 frontend/")
        print("   ├── 📁 unneeded/")
        print("   ├── 📄 README.md")
        print("   └── 📄 ملفات أساسية أخرى")
        
    except Exception as e:
        print(f"❌ خطأ في إعادة الهيكلة: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
