#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
فاحص تكامل النظام الشامل
- فحص العلاقات بين قواعد البيانات
- فحص تكامل الواجهات
- فحص عمل الأزرار والوظائف
- فحص APIs والاتصالات
"""

import sqlite3
import requests
import json
import os
from pathlib import Path
from datetime import datetime


class SystemIntegrationChecker:
    def __init__(self):
        self.backend_url = 'http://localhost:8007'
        self.databases = [
            'integrated_system.db',
            'comprehensive_inventory.db',
            'inventory_system.db'
        ]
        self.frontend_files = [
            'integrated_admin_dashboard.html',
            'comprehensive_admin_panel.html',
            'frontend_backend_integration_test.html',
            'reports_demo.html'
        ]
        self.results = {
            'database_relations': {},
            'api_endpoints': {},
            'frontend_integration': {},
            'button_functionality': {},
            'overall_status': 'unknown'
        }

    def check_database_relations(self):
        """فحص العلاقات في قواعد البيانات"""
        print("🔍 فحص العلاقات في قواعد البيانات...")

        for db_name in self.databases:
            if os.path.exists(db_name):
                try:
                    conn = sqlite3.connect(db_name)
                    conn.row_factory = sqlite3.Row

                    # الحصول على قائمة الجداول
                    tables = conn.execute("""
                        SELECT name FROM sqlite_master
                        WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    """).fetchall()

                    table_info = {}
                    foreign_keys = {}

                    for table in tables:
                        table_name = table['name']

                        # معلومات الأعمدة
                        columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
                        table_info[table_name] = {
                            'columns': len(columns),
                            'column_names': [col['name'] for col in columns]
                        }

                        # العلاقات الخارجية
                        fks = conn.execute(f"PRAGMA foreign_key_list({table_name})").fetchall()
                        if fks:
                            foreign_keys[table_name] = [
                                {
                                    'column': fk['from'],
                                    'references': f"{fk['table']}.{fk['to']}"
                                } for fk in fks
                            ]

                        # عدد السجلات
                        count = conn.execute(f"SELECT COUNT(*) as count FROM {table_name}").fetchone()
                        table_info[table_name]['record_count'] = count['count']

                    self.results['database_relations'][db_name] = {
                        'status': 'connected',
                        'tables': table_info,
                        'foreign_keys': foreign_keys,
                        'total_tables': len(tables)
                    }

                    conn.close()
                    print(f"✅ {db_name}: {len(tables)} جدول، {len(foreign_keys)} علاقة خارجية")

                except Exception as e:
                    self.results['database_relations'][db_name] = {
                        'status': 'error',
                        'error': str(e)
                    }
                    print(f"❌ {db_name}: خطأ - {e}")
            else:
                self.results['database_relations'][db_name] = {
                    'status': 'not_found'
                }
                print(f"⚠️ {db_name}: غير موجود")

    def check_api_endpoints(self):
        """فحص نقاط النهاية للـ APIs"""
        print("\n🌐 فحص APIs...")

        endpoints = [
            ('GET', '/api/health', 'فحص حالة النظام'),
            ('POST', '/api/auth/login', 'تسجيل الدخول'),
            ('GET', '/api/products/integrated', 'المنتجات المتكاملة'),
            ('GET', '/api/batches/integrated', 'اللوطات المتكاملة'),
            ('GET', '/api/reports/financial/integrated', 'التقارير المالية'),
            ('POST', '/api/export/integrated', 'تصدير البيانات'),
            ('GET', '/api/import-export/logs/integrated', 'سجلات الاستيراد/التصدير'),
            ('GET', '/api/settings/company', 'إعدادات الشركة'),
            ('GET', '/api/settings/system', 'إعدادات النظام'),
            ('GET', '/api/roles', 'الأدوار'),
        ]

        for method, endpoint, description in endpoints:
            try:
                if method == 'GET':
                    response = requests.get(f"{self.backend_url}{endpoint}",
                                            timeout=5)
                elif method == 'POST':
                    if endpoint == '/api/auth/login':
                        response = requests.post(
                            f"{self.backend_url}{endpoint}",
                            json={'username': 'admin', 'password': 'admin123'},
                            timeout=5
                        )
                    else:
                        response = requests.post(f"{self.backend_url}{endpoint}",
                                                 timeout=5)

                self.results['api_endpoints'][endpoint] = {
                    'status': 'working' if response.status_code < 500 else 'error',
                    'status_code': response.status_code,
                    'description': description
                }

                status_icon = "✅" if response.status_code < 500 else "❌"
                print(f"{status_icon} {method} {endpoint}: {response.status_code} - {description}")

            except requests.exceptions.ConnectionError:
                self.results['api_endpoints'][endpoint] = {
                    'status': 'connection_error',
                    'description': description
                }
                print(f"🔌 {method} {endpoint}: خطأ اتصال - {description}")
            except Exception as e:
                self.results['api_endpoints'][endpoint] = {
                    'status': 'error',
                    'error': str(e),
                    'description': description
                }
                print(f"❌ {method} {endpoint}: خطأ - {e}")

    def check_frontend_integration(self):
        """فحص تكامل الواجهات الأمامية"""
        print("\n🎨 فحص تكامل الواجهات...")

        for file_name in self.frontend_files:
            if os.path.exists(file_name):
                try:
                    with open(file_name, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # فحص وجود عناصر مهمة
                    checks = {
                        'backend_url': 'BACKEND_URL' in content,
                        'api_calls': 'fetch(' in content,
                        'arabic_support': 'dir="rtl"' in content,
                        'error_handling': 'catch(' in content,
                        'loading_states': 'loading' in content.lower(),
                        'button_handlers': 'onclick=' in content,
                        'form_elements': '<input' in content or '<select' in content,
                        'result_display': 'result' in content.lower()
                    }

                    working_features = sum(checks.values())
                    total_features = len(checks)

                    self.results['frontend_integration'][file_name] = {
                        'status': 'good' if working_features >= total_features * 0.8 else 'needs_improvement',
                        'features': checks,
                        'score': f"{working_features}/{total_features}"
                    }

                    status_icon = "✅" if working_features >= total_features * 0.8 else "⚠️"
                    print(f"{status_icon} {file_name}: {working_features}/{total_features} ميزة تعمل")

                except Exception as e:
                    self.results['frontend_integration'][file_name] = {
                        'status': 'error',
                        'error': str(e)
                    }
                    print(f"❌ {file_name}: خطأ - {e}")
            else:
                self.results['frontend_integration'][file_name] = {
                    'status': 'not_found'
                }
                print(f"⚠️ {file_name}: غير موجود")

    def check_button_functionality(self):
        """فحص وظائف الأزرار"""
        print("\n🔘 فحص وظائف الأزرار...")

        # فحص الأزرار في الواجهة الرئيسية
        main_dashboard = 'integrated_admin_dashboard.html'
        if os.path.exists(main_dashboard):
            try:
                with open(main_dashboard, 'r', encoding='utf-8') as f:
                    content = f.read()

                # البحث عن الأزرار ووظائفها
                button_functions = [
                    'checkSystemHealth',
                    'loginAsAdmin',
                    'loadIntegratedProducts',
                    'loadIntegratedBatches',
                    'loadFinancialReports',
                    'exportData',
                    'loadImportExportLogs',
                    'updateUserPermissions',
                    'loadCompanySettings',
                    'saveCompanySettings',
                    'loadSystemSettings',
                    'saveSystemSettings'
                ]

                button_status = {}
                for func in button_functions:
                    # فحص وجود تعريف الدالة
                    function_defined = f"function {func}(" in content or f"async function {func}(" in content
                    # فحص وجود استدعاء الدالة في onclick
                    function_called = "onclick=\"{func}(" in content or f"onclick='{func}(" in content

                    button_status[func] = {
                        'defined': function_defined,
                        'called': function_called,
                        'status': 'working' if function_defined and function_called else 'incomplete'
                    }

                working_buttons = sum(1 for btn in button_status.values() if btn['status'] == 'working')
                total_buttons = len(button_functions)

                self.results['button_functionality'] = {
                    'buttons': button_status,
                    'working_count': working_buttons,
                    'total_count': total_buttons,
                    'score': f"{working_buttons}/{total_buttons}"
                }

                print(f"✅ الأزرار: {working_buttons}/{total_buttons} يعمل بشكل صحيح")

                # عرض تفاصيل الأزرار غير العاملة
                for func, status in button_status.items():
                    if status['status'] != 'working':
                        issue = "غير معرف" if not status['defined'] else "غير مستدعى"
                        print(f"⚠️ {func}: {issue}")

            except Exception as e:
                self.results['button_functionality'] = {
                    'status': 'error',
                    'error': str(e)
                }
                print(f"❌ خطأ في فحص الأزرار: {e}")

    def generate_report(self):
        """إنشاء تقرير شامل"""
        print("\n📋 إنشاء التقرير الشامل...")

        # حساب النتيجة الإجمالية
        scores = []

        # نتيجة قواعد البيانات
        db_working = sum(1 for db in self.results['database_relations'].values()
                         if db.get('status') == 'connected')
        db_total = len(self.results['database_relations'])
        if db_total > 0:
            scores.append(db_working / db_total)

        # نتيجة APIs
        api_working = sum(1 for api in self.results['api_endpoints'].values()
                          if api.get('status') == 'working')
        api_total = len(self.results['api_endpoints'])
        if api_total > 0:
            scores.append(api_working / api_total)

        # نتيجة الواجهات
        frontend_working = sum(1 for fe in self.results['frontend_integration'].values()
                               if fe.get('status') == 'good')
        frontend_total = len(self.results['frontend_integration'])
        if frontend_total > 0:
            scores.append(frontend_working / frontend_total)

        # نتيجة الأزرار
        if 'working_count' in self.results['button_functionality']:
            button_score = (self.results['button_functionality']['working_count'] /
                            self.results['button_functionality']['total_count'])
            scores.append(button_score)

        # النتيجة الإجمالية
        overall_score = sum(scores) / len(scores) if scores else 0

        if overall_score >= 0.9:
            self.results['overall_status'] = 'excellent'
            status_icon = "🎉"
            status_text = "ممتاز"
        elif overall_score >= 0.7:
            self.results['overall_status'] = 'good'
            status_icon = "✅"
            status_text = "جيد"
        elif overall_score >= 0.5:
            self.results['overall_status'] = 'fair'
            status_icon = "⚠️"
            status_text = "مقبول"
        else:
            self.results['overall_status'] = 'poor'
            status_icon = "❌"
            status_text = "يحتاج تحسين"

        # إنشاء التقرير
        report = """
# 📊 تقرير فحص تكامل النظام الشامل

## {status_icon} النتيجة الإجمالية: {status_text} ({overall_score:.1%})

### 🗄️ قواعد البيانات: {db_working}/{db_total}
### 🌐 APIs: {api_working}/{api_total}
### 🎨 الواجهات: {frontend_working}/{frontend_total}
### 🔘 الأزرار: {self.results['button_functionality'].get('score', 'غير محدد')}

## 📋 التفاصيل:

### قواعد البيانات:
"""

        for db_name, db_info in self.results['database_relations'].items():
            if db_info.get('status') == 'connected':
                report += f"✅ {db_name}: {db_info.get('total_tables', 0)} جدول\n"
            else:
                report += f"❌ {db_name}: {db_info.get('status', 'خطأ')}\n"

        report += "\n### APIs:\n"
        for endpoint, api_info in self.results['api_endpoints'].items():
            status_icon = "✅" if api_info.get('status') == 'working' else "❌"
            report += f"{status_icon} {endpoint}: {api_info.get('description', '')}\n"

        report += "\n### الواجهات:\n"
        for file_name, fe_info in self.results['frontend_integration'].items():
            status_icon = "✅" if fe_info.get('status') == 'good' else "⚠️"
            score = fe_info.get('score', 'غير محدد')
            report += f"{status_icon} {file_name}: {score}\n"

        report += f"\n📅 تاريخ الفحص: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        # حفظ التقرير
        with open('system_integration_report.md', 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n{status_icon} النتيجة الإجمالية: {status_text} ({overall_score:.1%})")
        print("📄 تم حفظ التقرير في: system_integration_report.md")

        return self.results

    def run_full_check(self):
        """تشغيل الفحص الشامل"""
        print("🚀 بدء فحص تكامل النظام الشامل...")
        print("=" * 60)

        self.check_database_relations()
        self.check_api_endpoints()
        self.check_frontend_integration()
        self.check_button_functionality()

        print("\n" + "=" * 60)
        return self.generate_report()


if __name__ == '__main__':
    checker = SystemIntegrationChecker()
    results = checker.run_full_check()

    # عرض ملخص سريع
    print("\n🎯 ملخص سريع:")
    print(f"   • قواعد البيانات: {len([db for db in results['database_relations'].values() if db.get('status') == 'connected'])} متصلة")
    print(f"   • APIs: {len([api for api in results['api_endpoints'].values() if api.get('status') == 'working'])} تعمل")
    print(f"   • الواجهات: {len([fe for fe in results['frontend_integration'].values() if fe.get('status') == 'good'])} جيدة")
    print(f"   • الحالة العامة: {results['overall_status']}")
