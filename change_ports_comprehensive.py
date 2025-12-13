#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 سكريبت تغيير المنافذ الشامل
Comprehensive Port Change Script

يقوم بتغيير:
- المنفذ 5001 إلى 5002 (الواجهة الخلفية)
- المنفذ 3000 إلى 5502 (الواجهة الأمامية)
"""

import os
import re
import shutil
from pathlib import Path

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def change_ports_in_file(file_path):
    """تغيير المنافذ في ملف واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # تغيير المنافذ
        content = re.sub(r'\b5001\b', '5002', content)
        content = re.sub(r'\b3000\b', '5502', content)
        content = re.sub(r'\b3004\b', '5502', content)
        
        # تغييرات خاصة للروابط
        content = re.sub(r'localhost:5001', 'localhost:5002', content)
        content = re.sub(r'localhost:3000', 'localhost:5502', content)
        content = re.sub(r'localhost:3004', 'localhost:5502', content)
        content = re.sub(r'127\.0\.0\.1:5001', '127.0.0.1:5002', content)
        content = re.sub(r'127\.0\.0\.1:3000', '127.0.0.1:5502', content)
        content = re.sub(r'127\.0\.0\.1:3004', '127.0.0.1:5502', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print_warning(f"خطأ في معالجة {file_path}: {e}")
        return False

def main():
    print("🔧 بدء تغيير المنافذ الشامل...")
    print("=" * 50)
    
    base_path = Path("./system_backup_clean/store_v1.5_folder")

    # قائمة الملفات المستهدفة (تجاهل node_modules)
    target_files = [
        # Backend files
        base_path / "backend/app.py",
        base_path / "backend/.env",
        base_path / "backend/create_admin_user.py",
        
        # Frontend files
        base_path / "frontend/vite.config.js",
        base_path / "frontend/src/config/api.js",
        
        # Root files
        base_path / "run_complete_system.sh",
        base_path / "maintenance.sh",
        base_path / "QUICK_START_GUIDE.md",
    ]
    
    changed_files = 0
    
    for file_path in target_files:
        if file_path.exists():
            print_step(f"معالجة {file_path}")
            if change_ports_in_file(file_path):
                changed_files += 1
                print_success(f"تم تحديث {file_path}")
            else:
                print(f"   لا توجد تغييرات في {file_path}")
        else:
            print_warning(f"الملف غير موجود: {file_path}")
    
    print("=" * 50)
    print_success(f"تم تحديث {changed_files} ملف بنجاح!")
    print("📋 التغييرات المطبقة:")
    print("   - المنفذ 5001 → 5002 (الواجهة الخلفية)")
    print("   - المنفذ 3000 → 5502 (الواجهة الأمامية)")

if __name__ == "__main__":
    main()

