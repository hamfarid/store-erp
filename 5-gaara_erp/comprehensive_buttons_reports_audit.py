#!/usr/bin/env python3
"""
فحص شامل للأزرار والتقارير والمكتبات
Comprehensive Audit for Buttons, Reports, and Libraries
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime

class ComprehensiveAudit:
    def __init__(self):
        self.base_path = Path(".")
        self.frontend_path = self.base_path / "frontend"
        self.backend_path = self.base_path / "backend"
        self.results = {
            'buttons': {},
            'reports': {},
            'libraries': {},
            'summary': {}
        }
        
    def audit_buttons(self):
        """فحص شامل للأزرار"""
        print("🔘 فحص الأزرار في الواجهة الأمامية...")
        
        buttons_data = {
            'total_buttons': 0,
            'connected_buttons': 0,
            'disconnected_buttons': 0,
            'button_types': {},
            'button_functions': [],
            'missing_handlers': []
        }
        
        # البحث عن جميع الأزرار
        frontend_files = list(self.frontend_path.glob("**/*.jsx")) + list(self.frontend_path.glob("**/*.js"))
        
        for file_path in frontend_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن الأزرار
                button_patterns = [
                    r'<button[^>]*onClick\s*=\s*{([^}]+)}',
                    r'<Button[^>]*onClick\s*=\s*{([^}]+)}',
                    r'onClick\s*=\s*{([^}]+)}',
                    r'onSubmit\s*=\s*{([^}]+)}',
                    r'onPress\s*=\s*{([^}]+)}'
                ]
                
                for pattern in button_patterns:
                    matches = re.findall(pattern, content)
                    buttons_data['total_buttons'] += len(matches)
                    
                    for match in matches:
                        if match.strip() and match.strip() != '':
                            buttons_data['connected_buttons'] += 1
                            buttons_data['button_functions'].append({
                                'file': str(file_path.relative_to(self.frontend_path)),
                                'handler': match.strip()[:50]
                            })
                        else:
                            buttons_data['disconnected_buttons'] += 1
                            buttons_data['missing_handlers'].append(str(file_path.relative_to(self.frontend_path)))
                
                # تحليل أنواع الأزرار
                button_types = re.findall(r'type\s*=\s*["\']([^"\']+)["\']', content)
                for btn_type in button_types:
                    buttons_data['button_types'][btn_type] = buttons_data['button_types'].get(btn_type, 0) + 1
                    
            except Exception as e:
                print(f"خطأ في قراءة {file_path}: {e}")
        
        self.results['buttons'] = buttons_data
        
    def audit_reports(self):
        """فحص شامل للتقارير"""
        print("📊 فحص التقارير في النظام...")
        
        reports_data = {
            'frontend_reports': [],
            'backend_reports': [],
            'report_endpoints': [],
            'report_components': [],
            'export_functions': []
        }
        
        # فحص تقارير الواجهة الأمامية
        frontend_files = list(self.frontend_path.glob("**/*report*.jsx")) + list(self.frontend_path.glob("**/*Report*.jsx"))
        for file_path in frontend_files:
            reports_data['frontend_reports'].append({
                'file': str(file_path.relative_to(self.frontend_path)),
                'size': file_path.stat().st_size
            })
        
        # فحص تقارير الواجهة الخلفية
        backend_files = list(self.backend_path.glob("**/*report*.py")) + list(self.backend_path.glob("**/*Report*.py"))
        for file_path in backend_files:
            if '__pycache__' not in str(file_path):
                reports_data['backend_reports'].append({
                    'file': str(file_path.relative_to(self.backend_path)),
                    'size': file_path.stat().st_size
                })
        
        # البحث عن نقاط نهاية التقارير
        backend_route_files = list(self.backend_path.glob("src/routes/*.py"))
        for file_path in backend_route_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن نقاط نهاية التقارير
                report_endpoints = re.findall(r'@.*\.route\(["\']([^"\']*report[^"\']*)["\']', content, re.IGNORECASE)
                for endpoint in report_endpoints:
                    reports_data['report_endpoints'].append({
                        'file': str(file_path.relative_to(self.backend_path)),
                        'endpoint': endpoint
                    })
                
            except Exception as e:
                print(f"خطأ في قراءة {file_path}: {e}")
        
        # البحث عن مكونات التقارير في الواجهة الأمامية
        frontend_component_files = list(self.frontend_path.glob("src/components/*.jsx"))
        for file_path in frontend_component_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'report' in content.lower() or 'Report' in content:
                    reports_data['report_components'].append({
                        'file': str(file_path.relative_to(self.frontend_path)),
                        'size': file_path.stat().st_size
                    })
                
                # البحث عن وظائف التصدير
                export_functions = re.findall(r'(export[A-Za-z]*|download[A-Za-z]*|print[A-Za-z]*)\s*[=:]', content)
                if export_functions:
                    reports_data['export_functions'].extend([{
                        'file': str(file_path.relative_to(self.frontend_path)),
                        'function': func
                    } for func in export_functions])
                    
            except Exception as e:
                print(f"خطأ في قراءة {file_path}: {e}")
        
        self.results['reports'] = reports_data
        
    def audit_libraries(self):
        """فحص شامل للمكتبات"""
        print("📚 فحص المكتبات والتبعيات...")
        
        libraries_data = {
            'frontend_dependencies': {},
            'backend_dependencies': {},
            'unused_imports': [],
            'missing_dependencies': [],
            'version_conflicts': []
        }
        
        # فحص مكتبات الواجهة الأمامية
        package_json_path = self.frontend_path / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                
                libraries_data['frontend_dependencies'] = {
                    'dependencies': package_data.get('dependencies', {}),
                    'devDependencies': package_data.get('devDependencies', {}),
                    'total_count': len(package_data.get('dependencies', {})) + len(package_data.get('devDependencies', {}))
                }
                
            except Exception as e:
                print(f"خطأ في قراءة package.json: {e}")
        
        # فحص مكتبات الواجهة الخلفية
        requirements_files = [
            self.backend_path / "requirements.txt",
            self.backend_path / "requirements_clean.txt"
        ]
        
        for req_file in requirements_files:
            if req_file.exists():
                try:
                    with open(req_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # استخراج المكتبات
                    dependencies = []
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            dependencies.append(line)
                    
                    libraries_data['backend_dependencies'][req_file.name] = {
                        'dependencies': dependencies,
                        'count': len(dependencies)
                    }
                    
                except Exception as e:
                    print(f"خطأ في قراءة {req_file}: {e}")
        
        # فحص الاستيرادات المستخدمة
        used_imports = set()
        
        # فحص الواجهة الأمامية
        frontend_files = list(self.frontend_path.glob("**/*.jsx")) + list(self.frontend_path.glob("**/*.js"))
        for file_path in frontend_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # البحث عن الاستيرادات
                imports = re.findall(r'import\s+.*?\s+from\s+["\']([^"\']+)["\']', content)
                used_imports.update(imports)
                
            except Exception as e:
                continue
        
        # فحص الواجهة الخلفية
        backend_files = list(self.backend_path.glob("**/*.py"))
        for file_path in backend_files:
            if '__pycache__' not in str(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # البحث عن الاستيرادات
                    imports = re.findall(r'(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
                    used_imports.update(imports)
                    
                except Exception as e:
                    continue
        
        libraries_data['used_imports'] = list(used_imports)
        libraries_data['used_imports_count'] = len(used_imports)
        
        self.results['libraries'] = libraries_data
        
    def generate_summary(self):
        """إنشاء ملخص شامل"""
        print("📋 إنشاء الملخص الشامل...")
        
        summary = {
            'audit_date': datetime.now().isoformat(),
            'buttons_summary': {
                'total': self.results['buttons'].get('total_buttons', 0),
                'connected': self.results['buttons'].get('connected_buttons', 0),
                'disconnected': self.results['buttons'].get('disconnected_buttons', 0),
                'connection_rate': 0
            },
            'reports_summary': {
                'frontend_files': len(self.results['reports'].get('frontend_reports', [])),
                'backend_files': len(self.results['reports'].get('backend_reports', [])),
                'endpoints': len(self.results['reports'].get('report_endpoints', [])),
                'components': len(self.results['reports'].get('report_components', []))
            },
            'libraries_summary': {
                'frontend_deps': self.results['libraries'].get('frontend_dependencies', {}).get('total_count', 0),
                'backend_deps': sum([data.get('count', 0) for data in self.results['libraries'].get('backend_dependencies', {}).values()]),
                'used_imports': self.results['libraries'].get('used_imports_count', 0)
            }
        }
        
        # حساب معدل ربط الأزرار
        total_buttons = summary['buttons_summary']['total']
        connected_buttons = summary['buttons_summary']['connected']
        if total_buttons > 0:
            summary['buttons_summary']['connection_rate'] = round((connected_buttons / total_buttons) * 100, 2)
        
        self.results['summary'] = summary
        
    def run_audit(self):
        """تشغيل الفحص الشامل"""
        print("🚀 بدء الفحص الشامل للأزرار والتقارير والمكتبات...")
        print("=" * 70)
        
        self.audit_buttons()
        self.audit_reports()
        self.audit_libraries()
        self.generate_summary()
        
        print("=" * 70)
        print("✅ تم الانتهاء من الفحص الشامل!")
        
        # حفظ النتائج
        results_file = "comprehensive_audit_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # طباعة الملخص
        self.print_summary()
        
        return self.results
    
    def print_summary(self):
        """طباعة ملخص النتائج"""
        summary = self.results['summary']
        
        print(f"\n📊 ملخص النتائج:")
        print(f"تاريخ الفحص: {summary['audit_date']}")
        
        print(f"\n🔘 الأزرار:")
        print(f"  إجمالي الأزرار: {summary['buttons_summary']['total']}")
        print(f"  الأزرار المربوطة: {summary['buttons_summary']['connected']}")
        print(f"  الأزرار غير المربوطة: {summary['buttons_summary']['disconnected']}")
        print(f"  معدل الربط: {summary['buttons_summary']['connection_rate']}%")
        
        print(f"\n📊 التقارير:")
        print(f"  ملفات تقارير الواجهة الأمامية: {summary['reports_summary']['frontend_files']}")
        print(f"  ملفات تقارير الواجهة الخلفية: {summary['reports_summary']['backend_files']}")
        print(f"  نقاط نهاية التقارير: {summary['reports_summary']['endpoints']}")
        print(f"  مكونات التقارير: {summary['reports_summary']['components']}")
        
        print(f"\n📚 المكتبات:")
        print(f"  مكتبات الواجهة الأمامية: {summary['libraries_summary']['frontend_deps']}")
        print(f"  مكتبات الواجهة الخلفية: {summary['libraries_summary']['backend_deps']}")
        print(f"  الاستيرادات المستخدمة: {summary['libraries_summary']['used_imports']}")

if __name__ == "__main__":
    auditor = ComprehensiveAudit()
    results = auditor.run_audit()
    
    print(f"\n🎉 الفحص الشامل مكتمل!")
    print(f"تم حفظ النتائج في: comprehensive_audit_results.json")
