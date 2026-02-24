#!/usr/bin/env python3
"""
فحص شامل ومتقدم لنظام إدارة المتجر
Comprehensive System Audit for Store Management System
"""

import os
import json
import sqlite3
import subprocess
import time
from datetime import datetime
from pathlib import Path

class ComprehensiveSystemAudit:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.backend_path = self.base_path / "backend"
        self.frontend_path = self.base_path / "frontend"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "backend": {},
            "frontend": {},
            "database": {},
            "api": {},
            "security": {},
            "reports": {},
            "integration": {},
            "performance": {},
            "summary": {}
        }
    
    def audit_backend(self):
        """فحص الواجهة الخلفية"""
        print("🔍 فحص الواجهة الخلفية...")
        
        # فحص ملفات Python
        py_files = list(self.backend_path.rglob("*.py"))
        self.results["backend"]["python_files"] = len(py_files)
        
        # فحص النماذج
        models_path = self.backend_path / "src" / "models"
        if models_path.exists():
            model_files = list(models_path.glob("*.py"))
            self.results["backend"]["models"] = len(model_files)
        
        # فحص المسارات
        routes_path = self.backend_path / "src" / "routes"
        if routes_path.exists():
            route_files = list(routes_path.glob("*.py"))
            self.results["backend"]["routes"] = len(route_files)
        
        # فحص نقاط النهاية
        try:
            result = subprocess.run(
                ["grep", "-r", "@.*route", str(routes_path)],
                capture_output=True, text=True
            )
            endpoints = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["backend"]["endpoints"] = endpoints
        except:
            self.results["backend"]["endpoints"] = 0
        
        # فحص Blueprints
        try:
            result = subprocess.run(
                ["grep", "-r", "Blueprint", str(routes_path)],
                capture_output=True, text=True
            )
            blueprints = len([line for line in result.stdout.split('\n') if 'Blueprint(' in line])
            self.results["backend"]["blueprints"] = blueprints
        except:
            self.results["backend"]["blueprints"] = 0
    
    def audit_frontend(self):
        """فحص الواجهة الأمامية"""
        print("🎨 فحص الواجهة الأمامية...")
        
        # فحص ملفات React
        jsx_files = list(self.frontend_path.rglob("*.jsx"))
        js_files = list(self.frontend_path.rglob("*.js"))
        self.results["frontend"]["jsx_files"] = len(jsx_files)
        self.results["frontend"]["js_files"] = len(js_files)
        
        # فحص المكونات
        components_path = self.frontend_path / "src" / "components"
        if components_path.exists():
            components = list(components_path.rglob("*.jsx"))
            self.results["frontend"]["components"] = len(components)
        
        # فحص الصفحات
        pages_path = self.frontend_path / "src" / "pages"
        if pages_path.exists():
            pages = list(pages_path.glob("*.jsx"))
            self.results["frontend"]["pages"] = len(pages)
        
        # فحص CSS
        css_files = list(self.frontend_path.rglob("*.css"))
        self.results["frontend"]["css_files"] = len(css_files)
        
        # فحص الأزرار
        try:
            result = subprocess.run(
                ["grep", "-r", "<button\\|onClick", str(self.frontend_path / "src")],
                capture_output=True, text=True
            )
            buttons = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["frontend"]["buttons"] = buttons
        except:
            self.results["frontend"]["buttons"] = 0
        
        # فحص المسارات
        try:
            result = subprocess.run(
                ["grep", "-r", "Route.*path\\|<Route", str(self.frontend_path / "src")],
                capture_output=True, text=True
            )
            routes = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["frontend"]["routes"] = routes
        except:
            self.results["frontend"]["routes"] = 0
    
    def audit_database(self):
        """فحص قواعد البيانات"""
        print("🗄️ فحص قواعد البيانات...")
        
        # فحص ملفات قاعدة البيانات
        db_files = list(self.backend_path.rglob("*.db"))
        self.results["database"]["db_files"] = len(db_files)
        
        # فحص الجداول في قاعدة البيانات الرئيسية
        main_db = self.backend_path / "instance" / "inventory.db"
        if main_db.exists():
            try:
                conn = sqlite3.connect(str(main_db))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                self.results["database"]["tables"] = len(tables)
                self.results["database"]["table_names"] = [table[0] for table in tables]
                conn.close()
            except Exception as e:
                self.results["database"]["error"] = str(e)
        
        # فحص النماذج المعرفة
        try:
            result = subprocess.run(
                ["grep", "-r", "class.*db\\.Model\\|class.*Model", str(self.backend_path / "src" / "models")],
                capture_output=True, text=True
            )
            models = len([line for line in result.stdout.split('\n') if 'class' in line and 'Model' in line])
            self.results["database"]["defined_models"] = models
        except:
            self.results["database"]["defined_models"] = 0
    
    def audit_api(self):
        """فحص API والاتصالات"""
        print("🌐 فحص API والاتصالات...")
        
        # فحص استدعاءات API في الواجهة الأمامية
        try:
            result = subprocess.run(
                ["grep", "-r", "localhost:5001\\|/api/", str(self.frontend_path / "src")],
                capture_output=True, text=True
            )
            api_calls = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["api"]["frontend_api_calls"] = api_calls
        except:
            self.results["api"]["frontend_api_calls"] = 0
        
        # اختبار الاتصال بالخادم
        try:
            # تشغيل الخادم في الخلفية
            server_process = subprocess.Popen(
                ["python", "app.py"],
                cwd=str(self.backend_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # انتظار قصير للخادم
            time.sleep(3)
            
            # اختبار الاتصال
            result = subprocess.run(
                ["curl", "-s", "http://localhost:5001/api/health"],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0 and result.stdout:
                self.results["api"]["server_status"] = "running"
                try:
                    health_data = json.loads(result.stdout)
                    self.results["api"]["health_check"] = health_data
                except:
                    self.results["api"]["health_check"] = "response_received"
            else:
                self.results["api"]["server_status"] = "not_responding"
            
            # إيقاف الخادم
            server_process.terminate()
            server_process.wait(timeout=5)
            
        except Exception as e:
            self.results["api"]["server_error"] = str(e)
    
    def audit_security(self):
        """فحص الأمان"""
        print("🔒 فحص الأمان...")
        
        # فحص مراجع الأمان
        try:
            result = subprocess.run(
                ["grep", "-r", "JWT\\|jwt\\|token", str(self.backend_path / "src")],
                capture_output=True, text=True
            )
            security_refs = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["security"]["jwt_references"] = security_refs
        except:
            self.results["security"]["jwt_references"] = 0
        
        # فحص التشفير
        try:
            result = subprocess.run(
                ["grep", "-r", "encrypt\\|hash\\|bcrypt", str(self.backend_path / "src")],
                capture_output=True, text=True
            )
            encryption_refs = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["security"]["encryption_references"] = encryption_refs
        except:
            self.results["security"]["encryption_references"] = 0
        
        # فحص كلمات المرور المكشوفة
        try:
            result = subprocess.run(
                ["grep", "-r", "password.*=", str(self.backend_path)],
                capture_output=True, text=True
            )
            password_refs = len([line for line in result.stdout.split('\n') if 'password' in line.lower() and '=' in line])
            self.results["security"]["password_references"] = password_refs
        except:
            self.results["security"]["password_references"] = 0
    
    def audit_reports(self):
        """فحص التقارير والطباعة"""
        print("📊 فحص التقارير والطباعة...")
        
        # فحص ملفات التقارير
        report_files = list(self.backend_path.rglob("*report*")) + list(self.backend_path.rglob("*Report*"))
        self.results["reports"]["report_files"] = len(report_files)
        
        # فحص وظائف الطباعة والتصدير
        try:
            result = subprocess.run(
                ["grep", "-r", "print\\|pdf\\|export", str(self.backend_path / "src" / "routes")],
                capture_output=True, text=True
            )
            export_functions = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["reports"]["export_functions"] = export_functions
        except:
            self.results["reports"]["export_functions"] = 0
        
        # فحص Excel
        try:
            result = subprocess.run(
                ["grep", "-r", "excel\\|xlsx\\|openpyxl", str(self.backend_path / "src")],
                capture_output=True, text=True
            )
            excel_refs = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["reports"]["excel_references"] = excel_refs
        except:
            self.results["reports"]["excel_references"] = 0
    
    def audit_integration(self):
        """فحص التكامل بين المكونات"""
        print("🔗 فحص التكامل...")
        
        # فحص ربط الأزرار بـ API
        try:
            result = subprocess.run(
                ["grep", "-r", "onClick.*fetch\\|onClick.*api", str(self.frontend_path / "src")],
                capture_output=True, text=True
            )
            connected_buttons = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["integration"]["api_connected_buttons"] = connected_buttons
        except:
            self.results["integration"]["api_connected_buttons"] = 0
        
        # فحص النماذج
        try:
            result = subprocess.run(
                ["grep", "-r", "<form\\|onSubmit", str(self.frontend_path / "src")],
                capture_output=True, text=True
            )
            forms = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["integration"]["forms"] = forms
        except:
            self.results["integration"]["forms"] = 0
        
        # فحص الروابط
        try:
            result = subprocess.run(
                ["grep", "-r", "<Link\\|href", str(self.frontend_path / "src")],
                capture_output=True, text=True
            )
            links = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["integration"]["links"] = links
        except:
            self.results["integration"]["links"] = 0
    
    def audit_performance(self):
        """فحص الأداء"""
        print("⚡ فحص الأداء...")
        
        # فحص حجم الملفات
        total_size = sum(f.stat().st_size for f in self.base_path.rglob('*') if f.is_file())
        self.results["performance"]["total_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        # فحص Tailwind CSS
        try:
            result = subprocess.run(
                ["grep", "-r", "bg-\\|text-\\|p-\\|m-", str(self.frontend_path / "src")],
                capture_output=True, text=True
            )
            tailwind_classes = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["performance"]["tailwind_classes"] = tailwind_classes
        except:
            self.results["performance"]["tailwind_classes"] = 0
        
        # فحص lazy loading
        try:
            result = subprocess.run(
                ["grep", "-r", "lazy\\|Suspense", str(self.frontend_path / "src")],
                capture_output=True, text=True
            )
            lazy_refs = len(result.stdout.split('\n')) if result.stdout else 0
            self.results["performance"]["lazy_loading_refs"] = lazy_refs
        except:
            self.results["performance"]["lazy_loading_refs"] = 0
    
    def calculate_summary(self):
        """حساب الملخص والنقاط"""
        print("📋 حساب الملخص...")
        
        # حساب النقاط
        backend_score = min(100, (
            (self.results["backend"].get("python_files", 0) / 200 * 20) +
            (self.results["backend"].get("endpoints", 0) / 500 * 30) +
            (self.results["backend"].get("blueprints", 0) / 10 * 25) +
            (self.results["backend"].get("models", 0) / 50 * 25)
        ))
        
        frontend_score = min(100, (
            (self.results["frontend"].get("components", 0) / 100 * 30) +
            (self.results["frontend"].get("pages", 0) / 30 * 20) +
            (self.results["frontend"].get("buttons", 0) / 1000 * 25) +
            (self.results["frontend"].get("routes", 0) / 100 * 25)
        ))
        
        database_score = min(100, (
            (self.results["database"].get("tables", 0) / 50 * 40) +
            (self.results["database"].get("defined_models", 0) / 100 * 60)
        ))
        
        api_score = 100 if self.results["api"].get("server_status") == "running" else 50
        
        security_score = min(100, (
            (self.results["security"].get("jwt_references", 0) / 200 * 40) +
            (self.results["security"].get("encryption_references", 0) / 300 * 60)
        ))
        
        integration_score = min(100, (
            (self.results["integration"].get("forms", 0) / 50 * 30) +
            (self.results["integration"].get("links", 0) / 100 * 30) +
            (self.results["integration"].get("api_connected_buttons", 0) / 10 * 40)
        ))
        
        overall_score = (backend_score + frontend_score + database_score + api_score + security_score + integration_score) / 6
        
        self.results["summary"] = {
            "backend_score": round(backend_score, 1),
            "frontend_score": round(frontend_score, 1),
            "database_score": round(database_score, 1),
            "api_score": round(api_score, 1),
            "security_score": round(security_score, 1),
            "integration_score": round(integration_score, 1),
            "overall_score": round(overall_score, 1),
            "grade": self.get_grade(overall_score)
        }
    
    def get_grade(self, score):
        """تحديد التقدير"""
        if score >= 95: return "ممتاز+"
        elif score >= 90: return "ممتاز"
        elif score >= 85: return "جيد جداً+"
        elif score >= 80: return "جيد جداً"
        elif score >= 75: return "جيد+"
        elif score >= 70: return "جيد"
        elif score >= 65: return "مقبول+"
        elif score >= 60: return "مقبول"
        else: return "ضعيف"
    
    def run_audit(self):
        """تشغيل الفحص الشامل"""
        print("🚀 بدء الفحص الشامل للنظام...")
        print("=" * 50)
        
        self.audit_backend()
        self.audit_frontend()
        self.audit_database()
        self.audit_api()
        self.audit_security()
        self.audit_reports()
        self.audit_integration()
        self.audit_performance()
        self.calculate_summary()
        
        print("=" * 50)
        print("✅ تم الانتهاء من الفحص الشامل!")
        
        return self.results
    
    def save_results(self, filename="comprehensive_audit_results.json"):
        """حفظ النتائج"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"💾 تم حفظ النتائج في: {filename}")

if __name__ == "__main__":
    auditor = ComprehensiveSystemAudit()
    results = auditor.run_audit()
    auditor.save_results()
    
    # طباعة الملخص
    summary = results["summary"]
    print(f"\n📊 الملخص النهائي:")
    print(f"الواجهة الخلفية: {summary['backend_score']}/100")
    print(f"الواجهة الأمامية: {summary['frontend_score']}/100")
    print(f"قاعدة البيانات: {summary['database_score']}/100")
    print(f"API: {summary['api_score']}/100")
    print(f"الأمان: {summary['security_score']}/100")
    print(f"التكامل: {summary['integration_score']}/100")
    print(f"النقاط الإجمالية: {summary['overall_score']}/100")
    print(f"التقدير: {summary['grade']}")
