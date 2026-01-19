#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف: /home/ubuntu/gaara_ai_FINAL_INTEGRATED_SYSTEM_20250708_040611/test_complete_integration.py
سكريبت اختبار التكامل الشامل والمتقدم لنظام Gaara AI
الإصدار: 2.0.0
تم الإنشاء: 2025-01-08
المطور: Gaara Group & Manus AI
"""

import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path
from datetime import datetime
import logging

# إعداد نظام السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integration_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GaaraIntegrationTester:
    """فئة اختبار التكامل الشامل لنظام Gaara AI"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.backend_dir = self.base_dir / "gaara_ai_integrated" / "backend"
        self.frontend_dir = self.base_dir / "gaara_ai_integrated" / "frontend"
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
        
    def log_test(self, test_name, status, message="", details=None):
        """تسجيل نتيجة اختبار"""
        self.test_results['tests'][test_name] = {
            'status': status,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results['summary']['total'] += 1
        if status == 'PASS':
            self.test_results['summary']['passed'] += 1
            logger.info(f"✅ {test_name}: {message}")
        elif status == 'FAIL':
            self.test_results['summary']['failed'] += 1
            logger.error(f"❌ {test_name}: {message}")
        elif status == 'WARN':
            self.test_results['summary']['warnings'] += 1
            logger.warning(f"⚠️ {test_name}: {message}")
    
    def test_file_structure(self):
        """اختبار هيكل الملفات"""
        logger.info("🔍 اختبار هيكل الملفات...")
        
        # الملفات الأساسية المطلوبة
        required_files = [
            # الواجهة الخلفية
            "gaara_ai_integrated/backend/main_api.py",
            "gaara_ai_integrated/backend/models.py",
            "gaara_ai_integrated/backend/routes_complete.py",
            "gaara_ai_integrated/backend/permissions_complete.py",
            "gaara_ai_integrated/backend/utils.py",
            "gaara_ai_integrated/backend/requirements.txt",
            "gaara_ai_integrated/backend/Dockerfile",
            
            # الواجهة الأمامية
            "gaara_ai_integrated/frontend/package.json",
            "gaara_ai_integrated/frontend/src/App.jsx",
            "gaara_ai_integrated/frontend/src/main.jsx",
            "gaara_ai_integrated/frontend/src/services/ApiServiceComplete.js",
            "gaara_ai_integrated/frontend/src/components/Router/AppRouter.jsx",
            "gaara_ai_integrated/frontend/Dockerfile",
            "gaara_ai_integrated/frontend/nginx.conf",
            
            # ملفات Docker
            "docker-compose.yml",
            ".env.example",
            
            # ملفات التوثيق
            "README.md",
            "docs/README.md"
        ]
        
        missing_files = []
        existing_files = []
        
        for file_path in required_files:
            full_path = self.base_dir / file_path
            if full_path.exists():
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        if missing_files:
            self.log_test(
                "file_structure",
                "WARN",
                f"بعض الملفات مفقودة: {len(missing_files)} ملف",
                {"missing_files": missing_files, "existing_files": existing_files}
            )
        else:
            self.log_test(
                "file_structure",
                "PASS",
                f"جميع الملفات الأساسية موجودة: {len(existing_files)} ملف"
            )
    
    def test_python_syntax(self):
        """اختبار صحة بناء الجملة في ملفات Python"""
        logger.info("🐍 اختبار صحة بناء الجملة في ملفات Python...")
        
        python_files = list(self.backend_dir.glob("**/*.py"))
        syntax_errors = []
        valid_files = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), py_file, 'exec')
                valid_files.append(str(py_file.relative_to(self.base_dir)))
            except SyntaxError as e:
                syntax_errors.append({
                    'file': str(py_file.relative_to(self.base_dir)),
                    'error': str(e),
                    'line': e.lineno
                })
            except Exception as e:
                syntax_errors.append({
                    'file': str(py_file.relative_to(self.base_dir)),
                    'error': str(e),
                    'line': 'unknown'
                })
        
        if syntax_errors:
            self.log_test(
                "python_syntax",
                "FAIL",
                f"أخطاء في بناء الجملة: {len(syntax_errors)} ملف",
                {"syntax_errors": syntax_errors, "valid_files": valid_files}
            )
        else:
            self.log_test(
                "python_syntax",
                "PASS",
                f"جميع ملفات Python صحيحة: {len(valid_files)} ملف"
            )
    
    def test_javascript_syntax(self):
        """اختبار صحة بناء الجملة في ملفات JavaScript/JSX"""
        logger.info("📜 اختبار صحة بناء الجملة في ملفات JavaScript/JSX...")
        
        js_files = []
        js_files.extend(list(self.frontend_dir.glob("**/*.js")))
        js_files.extend(list(self.frontend_dir.glob("**/*.jsx")))
        
        # فلترة ملفات node_modules
        js_files = [f for f in js_files if 'node_modules' not in str(f)]
        
        syntax_errors = []
        valid_files = []
        
        for js_file in js_files:
            try:
                # فحص أساسي للملف
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # فحص الأقواس المتوازنة
                brackets = {'(': ')', '[': ']', '{': '}'}
                stack = []
                
                for char in content:
                    if char in brackets:
                        stack.append(brackets[char])
                    elif char in brackets.values():
                        if not stack or stack.pop() != char:
                            raise SyntaxError(f"Unmatched bracket: {char}")
                
                if stack:
                    raise SyntaxError(f"Unclosed brackets: {stack}")
                
                valid_files.append(str(js_file.relative_to(self.base_dir)))
                
            except Exception as e:
                syntax_errors.append({
                    'file': str(js_file.relative_to(self.base_dir)),
                    'error': str(e)
                })
        
        if syntax_errors:
            self.log_test(
                "javascript_syntax",
                "WARN",
                f"تحذيرات في ملفات JavaScript: {len(syntax_errors)} ملف",
                {"syntax_errors": syntax_errors, "valid_files": valid_files}
            )
        else:
            self.log_test(
                "javascript_syntax",
                "PASS",
                f"جميع ملفات JavaScript صحيحة: {len(valid_files)} ملف"
            )
    
    def test_dependencies(self):
        """اختبار التبعيات والمكتبات"""
        logger.info("📦 اختبار التبعيات والمكتبات...")
        
        # فحص requirements.txt للواجهة الخلفية
        requirements_file = self.backend_dir / "requirements.txt"
        if requirements_file.exists():
            try:
                with open(requirements_file, 'r') as f:
                    requirements = f.read().strip().split('\n')
                    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]
                
                self.log_test(
                    "backend_dependencies",
                    "PASS",
                    f"ملف requirements.txt موجود مع {len(requirements)} تبعية",
                    {"dependencies": requirements}
                )
            except Exception as e:
                self.log_test(
                    "backend_dependencies",
                    "FAIL",
                    f"خطأ في قراءة requirements.txt: {str(e)}"
                )
        else:
            self.log_test(
                "backend_dependencies",
                "FAIL",
                "ملف requirements.txt غير موجود"
            )
        
        # فحص package.json للواجهة الأمامية
        package_file = self.frontend_dir / "package.json"
        if package_file.exists():
            try:
                with open(package_file, 'r') as f:
                    package_data = json.load(f)
                
                dependencies = package_data.get('dependencies', {})
                dev_dependencies = package_data.get('devDependencies', {})
                
                self.log_test(
                    "frontend_dependencies",
                    "PASS",
                    f"ملف package.json موجود مع {len(dependencies)} تبعية و {len(dev_dependencies)} تبعية تطوير",
                    {
                        "dependencies": list(dependencies.keys()),
                        "devDependencies": list(dev_dependencies.keys())
                    }
                )
            except Exception as e:
                self.log_test(
                    "frontend_dependencies",
                    "FAIL",
                    f"خطأ في قراءة package.json: {str(e)}"
                )
        else:
            self.log_test(
                "frontend_dependencies",
                "FAIL",
                "ملف package.json غير موجود"
            )
    
    def test_docker_configuration(self):
        """اختبار تكوين Docker"""
        logger.info("🐳 اختبار تكوين Docker...")
        
        # فحص docker-compose.yml
        docker_compose_file = self.base_dir / "docker-compose.yml"
        if docker_compose_file.exists():
            try:
                with open(docker_compose_file, 'r') as f:
                    content = f.read()
                
                # فحص وجود الخدمات الأساسية
                required_services = ['backend', 'frontend', 'database']
                found_services = []
                
                for service in required_services:
                    if service in content:
                        found_services.append(service)
                
                self.log_test(
                    "docker_compose",
                    "PASS",
                    f"ملف docker-compose.yml موجود مع {len(found_services)} خدمة",
                    {"found_services": found_services}
                )
            except Exception as e:
                self.log_test(
                    "docker_compose",
                    "FAIL",
                    f"خطأ في قراءة docker-compose.yml: {str(e)}"
                )
        else:
            self.log_test(
                "docker_compose",
                "FAIL",
                "ملف docker-compose.yml غير موجود"
            )
        
        # فحص Dockerfile للواجهة الخلفية
        backend_dockerfile = self.backend_dir / "Dockerfile"
        if backend_dockerfile.exists():
            self.log_test(
                "backend_dockerfile",
                "PASS",
                "Dockerfile للواجهة الخلفية موجود"
            )
        else:
            self.log_test(
                "backend_dockerfile",
                "FAIL",
                "Dockerfile للواجهة الخلفية غير موجود"
            )
        
        # فحص Dockerfile للواجهة الأمامية
        frontend_dockerfile = self.frontend_dir / "Dockerfile"
        if frontend_dockerfile.exists():
            self.log_test(
                "frontend_dockerfile",
                "PASS",
                "Dockerfile للواجهة الأمامية موجود"
            )
        else:
            self.log_test(
                "frontend_dockerfile",
                "FAIL",
                "Dockerfile للواجهة الأمامية غير موجود"
            )
    
    def test_api_routes(self):
        """اختبار مسارات API"""
        logger.info("🛣️ اختبار مسارات API...")
        
        routes_file = self.backend_dir / "routes_complete.py"
        if routes_file.exists():
            try:
                with open(routes_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن مسارات API
                import re
                route_patterns = [
                    r"@app\.route\(['\"]([^'\"]+)['\"]",
                    r"@bp\.route\(['\"]([^'\"]+)['\"]",
                    r"@api\.route\(['\"]([^'\"]+)['\"]"
                ]
                
                found_routes = []
                for pattern in route_patterns:
                    matches = re.findall(pattern, content)
                    found_routes.extend(matches)
                
                # إزالة التكرارات
                found_routes = list(set(found_routes))
                
                self.log_test(
                    "api_routes",
                    "PASS",
                    f"تم العثور على {len(found_routes)} مسار API",
                    {"routes": found_routes}
                )
            except Exception as e:
                self.log_test(
                    "api_routes",
                    "FAIL",
                    f"خطأ في فحص مسارات API: {str(e)}"
                )
        else:
            self.log_test(
                "api_routes",
                "FAIL",
                "ملف routes_complete.py غير موجود"
            )
    
    def test_frontend_components(self):
        """اختبار مكونات الواجهة الأمامية"""
        logger.info("⚛️ اختبار مكونات الواجهة الأمامية...")
        
        # البحث عن مكونات React
        src_dir = self.frontend_dir / "src"
        if src_dir.exists():
            jsx_files = list(src_dir.glob("**/*.jsx"))
            js_files = list(src_dir.glob("**/*.js"))
            
            # فلترة ملفات node_modules
            jsx_files = [f for f in jsx_files if 'node_modules' not in str(f)]
            js_files = [f for f in js_files if 'node_modules' not in str(f)]
            
            components = []
            pages = []
            
            for file in jsx_files + js_files:
                relative_path = str(file.relative_to(src_dir))
                if 'components' in relative_path:
                    components.append(relative_path)
                elif 'pages' in relative_path:
                    pages.append(relative_path)
            
            self.log_test(
                "frontend_components",
                "PASS",
                f"تم العثور على {len(components)} مكون و {len(pages)} صفحة",
                {"components": components, "pages": pages}
            )
        else:
            self.log_test(
                "frontend_components",
                "FAIL",
                "مجلد src للواجهة الأمامية غير موجود"
            )
    
    def test_routing_configuration(self):
        """اختبار تكوين التوجيه"""
        logger.info("🧭 اختبار تكوين التوجيه...")
        
        router_file = self.frontend_dir / "src" / "components" / "Router" / "AppRouter.jsx"
        if router_file.exists():
            try:
                with open(router_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن المسارات
                import re
                route_patterns = [
                    r"path:\s*['\"]([^'\"]+)['\"]",
                    r"<Route\s+path=['\"]([^'\"]+)['\"]"
                ]
                
                found_routes = []
                for pattern in route_patterns:
                    matches = re.findall(pattern, content)
                    found_routes.extend(matches)
                
                # إزالة التكرارات
                found_routes = list(set(found_routes))
                
                self.log_test(
                    "routing_configuration",
                    "PASS",
                    f"تم العثور على {len(found_routes)} مسار في التوجيه",
                    {"routes": found_routes}
                )
            except Exception as e:
                self.log_test(
                    "routing_configuration",
                    "FAIL",
                    f"خطأ في فحص تكوين التوجيه: {str(e)}"
                )
        else:
            self.log_test(
                "routing_configuration",
                "FAIL",
                "ملف AppRouter.jsx غير موجود"
            )
    
    def test_permissions_system(self):
        """اختبار نظام الصلاحيات"""
        logger.info("🔐 اختبار نظام الصلاحيات...")
        
        permissions_file = self.backend_dir / "permissions_complete.py"
        if permissions_file.exists():
            try:
                with open(permissions_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن الصلاحيات والأدوار
                permission_indicators = [
                    'PermissionType',
                    'Module',
                    'DefaultRole',
                    'require_permission',
                    'require_role'
                ]
                
                found_indicators = []
                for indicator in permission_indicators:
                    if indicator in content:
                        found_indicators.append(indicator)
                
                self.log_test(
                    "permissions_system",
                    "PASS",
                    f"نظام الصلاحيات مكتمل مع {len(found_indicators)} مكون",
                    {"components": found_indicators}
                )
            except Exception as e:
                self.log_test(
                    "permissions_system",
                    "FAIL",
                    f"خطأ في فحص نظام الصلاحيات: {str(e)}"
                )
        else:
            self.log_test(
                "permissions_system",
                "FAIL",
                "ملف permissions_complete.py غير موجود"
            )
    
    def test_api_service_integration(self):
        """اختبار تكامل خدمة API"""
        logger.info("🔗 اختبار تكامل خدمة API...")
        
        api_service_file = self.frontend_dir / "src" / "services" / "ApiServiceComplete.js"
        if api_service_file.exists():
            try:
                with open(api_service_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن الطرق والخدمات
                import re
                method_pattern = r"async\s+(\w+)\s*\("
                methods = re.findall(method_pattern, content)
                
                # تصنيف الطرق
                auth_methods = [m for m in methods if 'login' in m.lower() or 'auth' in m.lower() or 'register' in m.lower()]
                crud_methods = [m for m in methods if any(op in m.lower() for op in ['get', 'create', 'update', 'delete'])]
                
                self.log_test(
                    "api_service_integration",
                    "PASS",
                    f"خدمة API مكتملة مع {len(methods)} طريقة",
                    {
                        "total_methods": len(methods),
                        "auth_methods": len(auth_methods),
                        "crud_methods": len(crud_methods),
                        "methods": methods[:20]  # أول 20 طريقة فقط
                    }
                )
            except Exception as e:
                self.log_test(
                    "api_service_integration",
                    "FAIL",
                    f"خطأ في فحص خدمة API: {str(e)}"
                )
        else:
            self.log_test(
                "api_service_integration",
                "FAIL",
                "ملف ApiServiceComplete.js غير موجود"
            )
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        logger.info("📊 إنشاء تقرير شامل...")
        
        # حفظ النتائج في ملف JSON
        report_file = self.base_dir / "integration_test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        # إنشاء تقرير نصي
        report_text = f"""
# تقرير اختبار التكامل الشامل لنظام Gaara AI
التاريخ: {self.test_results['timestamp']}

## ملخص النتائج
- إجمالي الاختبارات: {self.test_results['summary']['total']}
- نجح: {self.test_results['summary']['passed']} ✅
- فشل: {self.test_results['summary']['failed']} ❌
- تحذيرات: {self.test_results['summary']['warnings']} ⚠️

## تفاصيل الاختبارات
"""
        
        for test_name, result in self.test_results['tests'].items():
            status_icon = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "⚠️"
            report_text += f"\n### {test_name} {status_icon}\n"
            report_text += f"الحالة: {result['status']}\n"
            report_text += f"الرسالة: {result['message']}\n"
            if result['details']:
                report_text += f"التفاصيل: {json.dumps(result['details'], ensure_ascii=False, indent=2)}\n"
        
        # حفظ التقرير النصي
        report_text_file = self.base_dir / "integration_test_report.md"
        with open(report_text_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        logger.info(f"📄 تم حفظ التقرير في: {report_file}")
        logger.info(f"📄 تم حفظ التقرير النصي في: {report_text_file}")
        
        return self.test_results
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        logger.info("🚀 بدء اختبار التكامل الشامل لنظام Gaara AI")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        try:
            # تشغيل جميع الاختبارات
            self.test_file_structure()
            self.test_python_syntax()
            self.test_javascript_syntax()
            self.test_dependencies()
            self.test_docker_configuration()
            self.test_api_routes()
            self.test_frontend_components()
            self.test_routing_configuration()
            self.test_permissions_system()
            self.test_api_service_integration()
            
        except Exception as e:
            logger.error(f"خطأ أثناء تشغيل الاختبارات: {str(e)}")
            self.log_test("general_error", "FAIL", str(e))
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info("=" * 60)
        logger.info(f"⏱️ مدة الاختبار: {duration:.2f} ثانية")
        
        # إنشاء التقرير
        results = self.generate_report()
        
        # طباعة الملخص النهائي
        summary = results['summary']
        logger.info(f"📊 ملخص النتائج:")
        logger.info(f"   إجمالي: {summary['total']}")
        logger.info(f"   نجح: {summary['passed']} ✅")
        logger.info(f"   فشل: {summary['failed']} ❌")
        logger.info(f"   تحذيرات: {summary['warnings']} ⚠️")
        
        success_rate = (summary['passed'] / summary['total']) * 100 if summary['total'] > 0 else 0
        logger.info(f"   معدل النجاح: {success_rate:.1f}%")
        
        if summary['failed'] == 0:
            logger.info("🎉 جميع الاختبارات نجحت!")
        else:
            logger.warning(f"⚠️ هناك {summary['failed']} اختبار فاشل يحتاج إلى إصلاح")
        
        return results

def main():
    """الدالة الرئيسية"""
    print("🌱 نظام Gaara AI - اختبار التكامل الشامل")
    print("=" * 50)
    
    tester = GaaraIntegrationTester()
    results = tester.run_all_tests()
    
    # إرجاع كود الخروج المناسب
    if results['summary']['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()

