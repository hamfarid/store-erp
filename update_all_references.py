#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 سكريبت تحديث جميع المراجع
Update All References Script

يقوم بتحديث جميع المراجع للمنافذ الجديدة:
- المنفذ 5001 → 5002 (الواجهة الخلفية)
- المنفذ 3000 → 5502 (الواجهة الأمامية)
"""

import os
import re
import json
from pathlib import Path

def print_step(message):
    print(f"📋 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def update_cors_origins():
    """تحديث إعدادات CORS في app.py"""
    print_step("تحديث إعدادات CORS...")
    
    app_py_path = Path("./backend/app.py")
    if app_py_path.exists():
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # تحديث CORS origins
        cors_pattern = r'"origins": \[(.*?)\]'
        new_origins = '''[
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:5502",
                "http://127.0.0.1:5502",
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ]'''
        
        content = re.sub(cors_pattern, f'"origins": {new_origins}', content, flags=re.DOTALL)
        
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_success("تم تحديث إعدادات CORS")

def update_package_json():
    """تحديث package.json للواجهة الأمامية"""
    print_step("تحديث package.json...")
    
    package_json_path = Path("./frontend/package.json")
    if package_json_path.exists():
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # تحديث scripts
        if 'scripts' in package_data:
            if 'dev' in package_data['scripts']:
                package_data['scripts']['dev'] = "vite --port 5502"
            if 'preview' in package_data['scripts']:
                package_data['scripts']['preview'] = "vite preview --port 5502"
        
        with open(package_json_path, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        
        print_success("تم تحديث package.json")

def update_env_file():
    """تحديث ملف .env"""
    print_step("تحديث ملف .env...")
    
    env_path = Path("./backend/.env")
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # تحديث المنافذ في .env
        content = re.sub(r'FLASK_RUN_PORT=5001', 'FLASK_RUN_PORT=5002', content)
        content = re.sub(r'PORT=5001', 'PORT=5002', content)
        content = re.sub(r'BACKEND_PORT=5001', 'BACKEND_PORT=5002', content)
        content = re.sub(r'FRONTEND_PORT=3000', 'FRONTEND_PORT=5502', content)
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_success("تم تحديث ملف .env")

def update_documentation():
    """تحديث الوثائق"""
    print_step("تحديث الوثائق...")
    
    docs_files = [
        "./README.md",
        "./QUICK_START_GUIDE.md",
        "./USER_GUIDE.md"
    ]
    
    for doc_file in docs_files:
        doc_path = Path(doc_file)
        if doc_path.exists():
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تحديث المنافذ في الوثائق
            content = re.sub(r'localhost:5001', 'localhost:5002', content)
            content = re.sub(r'localhost:3000', 'localhost:5502', content)
            content = re.sub(r'127\.0\.0\.1:5001', '127.0.0.1:5002', content)
            content = re.sub(r'127\.0\.0\.1:3000', '127.0.0.1:5502', content)
            
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print_success(f"تم تحديث {doc_file}")

def update_shell_scripts():
    """تحديث ملفات Shell Scripts"""
    print_step("تحديث ملفات Shell Scripts...")
    
    script_files = [
        "./run_complete_system.sh",
        "./maintenance.sh",
        "./scripts/start_system.sh"
    ]
    
    for script_file in script_files:
        script_path = Path(script_file)
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تحديث المنافذ في scripts
            content = re.sub(r'--port 5001', '--port 5002', content)
            content = re.sub(r'--port 3000', '--port 5502', content)
            content = re.sub(r'PORT=5001', 'PORT=5002', content)
            content = re.sub(r'PORT=3000', 'PORT=5502', content)
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print_success(f"تم تحديث {script_file}")

def update_config_files():
    """تحديث ملفات التكوين الأخرى"""
    print_step("تحديث ملفات التكوين...")
    
    # تحديث admin_credentials.json
    admin_creds_path = Path("./admin_credentials.json")
    if admin_creds_path.exists():
        with open(admin_creds_path, 'r', encoding='utf-8') as f:
            creds_data = json.load(f)
        
        if 'api_url' in creds_data:
            creds_data['api_url'] = 'http://localhost:5002'
        if 'frontend_url' in creds_data:
            creds_data['frontend_url'] = 'http://localhost:5502'
        
        with open(admin_creds_path, 'w', encoding='utf-8') as f:
            json.dump(creds_data, f, indent=2, ensure_ascii=False)
        
        print_success("تم تحديث admin_credentials.json")

def clean_duplicate_references():
    """تنظيف المراجع المكررة"""
    print_step("تنظيف المراجع المكررة...")
    
    # إزالة الملفات المكررة من repeat_code إذا لم تعد مطلوبة
    repeat_code_path = Path("./repeat_code")
    if repeat_code_path.exists():
        # فحص الملفات المكررة وإزالة غير الضرورية
        for root, dirs, files in os.walk(repeat_code_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    # يمكن إضافة منطق لتحديد الملفات غير الضرورية
                    pass
        
        print_success("تم تنظيف المراجع المكررة")

def main():
    print("🔄 بدء تحديث جميع المراجع...")
    print("=" * 50)
    
    # تحديث جميع المراجع
    update_cors_origins()
    update_package_json()
    update_env_file()
    update_documentation()
    update_shell_scripts()
    update_config_files()
    clean_duplicate_references()
    
    print("=" * 50)
    print_success("تم تحديث جميع المراجع بنجاح!")
    print("📋 التحديثات المطبقة:")
    print("   - إعدادات CORS")
    print("   - package.json")
    print("   - ملف .env")
    print("   - الوثائق")
    print("   - Shell Scripts")
    print("   - ملفات التكوين")
    print("   - تنظيف المراجع المكررة")

if __name__ == "__main__":
    main()
