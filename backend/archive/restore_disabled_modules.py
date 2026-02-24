#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 إعادة دمج الوحدات المعطلة
Restore Disabled Modules

هذا السكريبت يقوم بإعادة دمج الوحدات المعطلة بشكل تدريجي وآمن
"""

import os
import shutil
import subprocess

def restore_module(module_name):
    """إعادة دمج وحدة واحدة"""
    print(f"🔄 إعادة دمج وحدة {module_name}...")
    
    disabled_path = f"backend/src/routes/disabled/{module_name}.py"
    active_path = f"backend/src/routes/{module_name}.py"
    
    try:
        if os.path.exists(disabled_path):
            # نسخ الملف من disabled إلى routes
            shutil.copy2(disabled_path, active_path)
            print(f"✅ تم نسخ {module_name}.py إلى مجلد routes")
            
            # إضافة الوحدة إلى الخادم الخلفي
            add_module_to_backend(module_name)
            
            return True
        else:
            print(f"❌ الملف {disabled_path} غير موجود")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في إعادة دمج وحدة {module_name}: {e}")
        return False

def add_module_to_backend(module_name):
    """إضافة الوحدة إلى الخادم الخلفي"""
    backend_file = "backend/enhanced_simple_app.py"
    
    try:
        # قراءة محتوى الملف
        with open(backend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # إضافة استيراد الوحدة
        import_line = f"from src.routes.{module_name} import {module_name}_bp"
        if import_line not in content:
            # البحث عن مكان الاستيرادات
            if "from src.routes" in content:
                # إضافة بعد آخر استيراد من src.routes
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("from src.routes") and i < len(lines) - 1:
                        if not lines[i + 1].startswith("from src.routes"):
                            lines.insert(i + 1, import_line)
                            break
                content = '\n'.join(lines)
            else:
                # إضافة في بداية الملف بعد الاستيرادات الأساسية
                content = content.replace("import sqlite3", f"import sqlite3\n{import_line}")
        
        # إضافة تسجيل المخطط
        register_line = f"app.register_blueprint({module_name}_bp)"
        if register_line not in content:
            # البحث عن مكان تسجيل المخططات
            if "app.register_blueprint" in content:
                # إضافة بعد آخر تسجيل مخطط
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "app.register_blueprint" in line:
                        lines.insert(i + 1, register_line)
                        break
                content = '\n'.join(lines)
            else:
                # إضافة قبل تشغيل الخادم
                content = content.replace("if __name__ == '__main__':", 
                                        f"{register_line}\n\nif __name__ == '__main__':")
        
        # كتابة المحتوى المحدث
        with open(backend_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ تم إضافة وحدة {module_name} إلى الخادم الخلفي")
        
    except Exception as e:
        print(f"❌ خطأ في إضافة وحدة {module_name} إلى الخادم: {e}")

def test_module_endpoints(module_name):
    """اختبار نقاط نهاية الوحدة"""
    print(f"🧪 اختبار نقاط نهاية وحدة {module_name}...")
    
    import requests
    
    # تحديد نقاط النهاية حسب الوحدة
    endpoints = {
        'categories': ['/api/categories'],
        'warehouses': ['/api/warehouses'],
        'inventory': ['/api/inventory', '/api/products'],
        'users': ['/api/users'],
        'reports': ['/api/reports/dashboard']
    }
    
    module_endpoints = endpoints.get(module_name, [])
    
    success_count = 0
    total_count = len(module_endpoints)
    
    for endpoint in module_endpoints:
        try:
            response = requests.get(f'http://localhost:5002{endpoint}', timeout=5)
            if response.status_code in [200, 401]:  # 401 مقبول للنقاط المحمية
                print(f"   ✅ {endpoint}: {response.status_code}")
                success_count += 1
            else:
                print(f"   ❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint}: خطأ في الاتصال - {e}")
    
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0
    print(f"   معدل النجاح: {success_rate:.1f}% ({success_count}/{total_count})")
    
    return success_rate >= 50  # نعتبر النجاح إذا كان 50% أو أكثر

def restart_backend():
    """إعادة تشغيل الخادم الخلفي"""
    print("🔄 إعادة تشغيل الخادم الخلفي...")
    
    try:
        # إيقاف العمليات الحالية
        subprocess.run(['pkill', '-f', 'enhanced_simple_app.py'], 
                      capture_output=True, text=True)
        
        # انتظار قصير
        import time
        time.sleep(2)
        
        # تشغيل الخادم الجديد
        subprocess.Popen(['python3', 'enhanced_simple_app.py'], 
                        cwd='backend', 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # انتظار حتى يبدأ الخادم
        time.sleep(5)
        
        print("✅ تم إعادة تشغيل الخادم الخلفي")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إعادة تشغيل الخادم: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔄 بدء إعادة دمج الوحدات المعطلة")
    print("=" * 60)
    
    # ترتيب الوحدات حسب الأولوية (الأقل اعتماداً أولاً)
    modules_order = ['categories', 'warehouses', 'users', 'inventory', 'reports']
    
    restored_modules = []
    failed_modules = []
    
    for module_name in modules_order:
        print(f"\n📦 معالجة وحدة: {module_name}")
        print("-" * 40)
        
        if restore_module(module_name):
            # إعادة تشغيل الخادم
            if restart_backend():
                # اختبار الوحدة
                if test_module_endpoints(module_name):
                    restored_modules.append(module_name)
                    print(f"✅ تم دمج وحدة {module_name} بنجاح")
                else:
                    failed_modules.append(module_name)
                    print(f"⚠️ تم دمج وحدة {module_name} لكن بعض النقاط لا تعمل")
            else:
                failed_modules.append(module_name)
                print(f"❌ فشل في إعادة تشغيل الخادم بعد دمج {module_name}")
        else:
            failed_modules.append(module_name)
            print(f"❌ فشل في دمج وحدة {module_name}")
    
    # تقرير النتائج
    print("\n" + "=" * 60)
    print("📊 تقرير إعادة الدمج:")
    print(f"✅ الوحدات المدمجة بنجاح: {len(restored_modules)}")
    for module in restored_modules:
        print(f"   - {module}")
    
    print(f"❌ الوحدات الفاشلة: {len(failed_modules)}")
    for module in failed_modules:
        print(f"   - {module}")
    
    success_rate = len(restored_modules) / len(modules_order) * 100
    print(f"\n🎯 معدل النجاح الإجمالي: {success_rate:.1f}%")

if __name__ == "__main__":
    main()
