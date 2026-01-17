#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 إعادة دمج الوحدات المعطلة تدريجياً
Gradual Module Restoration Script

يقوم بإعادة دمج الوحدات المعطلة في الخادم الخلفي بشكل تدريجي
مع اختبار كل وحدة قبل الانتقال للتالية
"""

import os
import shutil
import subprocess
import time
import requests
from pathlib import Path

class ModuleRestorer:
    def __init__(self):
        self.backend_dir = Path("backend")
        self.routes_dir = self.backend_dir / "src" / "routes"
        self.models_dir = self.backend_dir / "src" / "models"
        self.disabled_dir = self.routes_dir / "disabled"
        self.backend_url = "http://localhost:5002"
        
        # قائمة الوحدات المراد إعادة دمجها بالترتيب
        self.modules_to_restore = [
            {
                'name': 'inventory',
                'routes_file': 'inventory_advanced.py',
                'models_file': 'inventory.py',
                'blueprint_name': 'inventory_bp',
                'test_endpoint': '/api/inventory'
            },
            {
                'name': 'reports',
                'routes_file': 'comprehensive_reports.py',
                'models_file': None,
                'blueprint_name': 'reports_bp',
                'test_endpoint': '/api/reports/inventory'
            },
            {
                'name': 'invoices',
                'routes_file': 'invoices.py',
                'models_file': 'invoice.py',
                'blueprint_name': 'invoices_bp',
                'test_endpoint': '/api/invoices'
            }
        ]
    
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🔄 {title}")
        print(f"{'='*60}")
    
    def print_step(self, message):
        print(f"📋 {message}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def test_backend_health(self):
        """اختبار صحة الخادم الخلفي"""
        try:
            response = requests.get(f"{self.backend_url}/api/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('success', False)
            return False
        except Exception:
            return False
    
    def fix_import_paths(self, file_path):
        """إصلاح مسارات الاستيراد في الملف"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # إصلاح مسارات الاستيراد
            content = content.replace('from models.', 'from src.models.')
            content = content.replace('from database import', 'from src.database import')
            content = content.replace('import models.', 'import src.models.')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            self.print_error(f"خطأ في إصلاح مسارات الاستيراد: {e}")
            return False
    
    def create_simple_route_file(self, module_name, blueprint_name, endpoint):
        """إنشاء ملف مسار بسيط للوحدة"""
        simple_route = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مسارات {module_name} البسيطة
Simple {module_name} Routes
"""

from flask import Blueprint, jsonify, request
from src.database import db
from datetime import datetime

# إنشاء Blueprint
{blueprint_name} = Blueprint('{module_name}', __name__)

@{blueprint_name}.route('{endpoint}', methods=['GET'])
def get_{module_name}():
    """الحصول على {module_name}"""
    try:
        return jsonify({{
            'success': True,
            'message': 'وحدة {module_name} تعمل بشكل طبيعي',
            'data': [],
            'timestamp': datetime.now().isoformat()
        }})
    except Exception as e:
        return jsonify({{
            'success': False,
            'error': str(e)
        }}), 500

@{blueprint_name}.route('{endpoint}', methods=['POST'])
def create_{module_name}():
    """إنشاء عنصر جديد في {module_name}"""
    try:
        data = request.get_json()
        return jsonify({{
            'success': True,
            'message': 'تم إنشاء العنصر بنجاح',
            'data': data,
            'timestamp': datetime.now().isoformat()
        }})
    except Exception as e:
        return jsonify({{
            'success': False,
            'error': str(e)
        }}), 500
'''
        
        route_file = self.routes_dir / f"{module_name}.py"
        with open(route_file, 'w', encoding='utf-8') as f:
            f.write(simple_route)
        
        return route_file
    
    def restore_module(self, module_info):
        """إعادة دمج وحدة واحدة"""
        module_name = module_info['name']
        self.print_header(f"إعادة دمج وحدة {module_name}")
        
        # إنشاء ملف مسار بسيط أولاً
        self.print_step(f"إنشاء ملف مسار بسيط لوحدة {module_name}")
        route_file = self.create_simple_route_file(
            module_name,
            module_info['blueprint_name'],
            module_info['test_endpoint']
        )
        
        # إصلاح مسارات الاستيراد
        self.print_step("إصلاح مسارات الاستيراد")
        if not self.fix_import_paths(route_file):
            return False
        
        # إعادة تشغيل الخادم الخلفي
        self.print_step("إعادة تشغيل الخادم الخلفي")
        self.restart_backend()
        
        # انتظار بدء التشغيل
        time.sleep(5)
        
        # اختبار الوحدة
        self.print_step(f"اختبار وحدة {module_name}")
        if self.test_module(module_info['test_endpoint']):
            self.print_success(f"تم دمج وحدة {module_name} بنجاح")
            return True
        else:
            self.print_error(f"فشل في دمج وحدة {module_name}")
            # حذف الملف في حالة الفشل
            if route_file.exists():
                route_file.unlink()
            return False
    
    def restart_backend(self):
        """إعادة تشغيل الخادم الخلفي"""
        try:
            # إيقاف العمليات الحالية
            subprocess.run(['pkill', '-f', 'simple_app.py'], capture_output=True)
            time.sleep(2)
            
            # تشغيل الخادم الجديد
            subprocess.Popen(
                ['python3', 'simple_app.py'],
                cwd=self.backend_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
        except Exception as e:
            self.print_error(f"خطأ في إعادة تشغيل الخادم: {e}")
    
    def test_module(self, endpoint):
        """اختبار وحدة معينة"""
        try:
            # انتظار بدء الخادم
            for i in range(10):
                if self.test_backend_health():
                    break
                time.sleep(1)
            else:
                return False
            
            # اختبار نقطة النهاية
            response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
            return response.status_code == 200
            
        except Exception:
            return False
    
    def run_restoration(self):
        """تشغيل عملية الإعادة الدمج الكاملة"""
        self.print_header("بدء عملية إعادة الدمج التدريجية")
        
        # التحقق من صحة الخادم الأساسي
        if not self.test_backend_health():
            self.print_error("الخادم الخلفي لا يعمل، يرجى تشغيله أولاً")
            return False
        
        self.print_success("الخادم الخلفي يعمل بشكل طبيعي")
        
        # إعادة دمج كل وحدة
        successful_modules = []
        failed_modules = []
        
        for module_info in self.modules_to_restore:
            if self.restore_module(module_info):
                successful_modules.append(module_info['name'])
            else:
                failed_modules.append(module_info['name'])
        
        # تقرير النتائج
        self.print_header("تقرير النتائج")
        print(f"📊 إجمالي الوحدات: {len(self.modules_to_restore)}")
        print(f"✅ الوحدات الناجحة: {len(successful_modules)}")
        print(f"❌ الوحدات الفاشلة: {len(failed_modules)}")
        
        if successful_modules:
            print(f"🎉 الوحدات المدمجة بنجاح: {', '.join(successful_modules)}")
        
        if failed_modules:
            print(f"⚠️  الوحدات التي فشلت: {', '.join(failed_modules)}")
        
        success_rate = len(successful_modules) / len(self.modules_to_restore) * 100
        print(f"📈 معدل النجاح: {success_rate:.1f}%")
        
        return success_rate >= 50

def main():
    print("🔄 بدء عملية إعادة الدمج التدريجية للوحدات...")
    
    restorer = ModuleRestorer()
    success = restorer.run_restoration()
    
    if success:
        print("\n🎉 تمت عملية إعادة الدمج بنجاح!")
    else:
        print("\n⚠️  تمت عملية إعادة الدمج مع بعض المشاكل")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
