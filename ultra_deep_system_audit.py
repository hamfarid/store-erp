#!/usr/bin/env python3
"""
فحص شامل ومتعمق جداً لنظام إدارة المتجر
Ultra Deep System Audit for Store Management System
"""

import os
import json
import sqlite3
import subprocess
import time
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class UltraDeepSystemAudit:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.backend_path = self.base_path / "backend"
        self.frontend_path = self.base_path / "frontend"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "backend_detailed": {},
            "frontend_detailed": {},
            "database_detailed": {},
            "api_detailed": {},
            "security_detailed": {},
            "integration_detailed": {},
            "ui_ux_detailed": {},
            "performance_detailed": {},
            "issues_found": [],
            "recommendations": [],
            "summary_detailed": {}
        }
    
    def audit_backend_detailed(self):
        """فحص مفصل للواجهة الخلفية"""
        print("🔍 فحص مفصل للواجهة الخلفية...")
        
        backend_data = {}
        
        # فحص ملفات Python
        py_files = list(self.backend_path.rglob("*.py"))
        backend_data["total_python_files"] = len(py_files)
        
        # فحص الأخطاء النحوية
        syntax_errors = []
        for py_file in py_files:
            try:
                result = subprocess.run(
                    ["python", "-m", "py_compile", str(py_file)],
                    capture_output=True, text=True, cwd=str(self.backend_path)
                )
                if result.returncode != 0:
                    syntax_errors.append({
                        "file": str(py_file.relative_to(self.backend_path)),
                        "error": result.stderr
                    })
            except Exception as e:
                syntax_errors.append({
                    "file": str(py_file.relative_to(self.backend_path)),
                    "error": str(e)
                })
        
        backend_data["syntax_errors"] = syntax_errors
        backend_data["syntax_error_count"] = len(syntax_errors)
        
        # فحص نقاط النهاية API
        api_endpoints = []
        routes_path = self.backend_path / "src" / "routes"
        if routes_path.exists():
            for route_file in routes_path.glob("*.py"):
                try:
                    with open(route_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # البحث عن نقاط النهاية
                        endpoints = re.findall(r'@.*\.route\([\'"]([^\'"]+)[\'"].*methods=\[([^\]]+)\]', content)
                        for endpoint, methods in endpoints:
                            api_endpoints.append({
                                "file": route_file.name,
                                "endpoint": endpoint,
                                "methods": methods.replace("'", "").replace('"', '').split(', ')
                            })
                except Exception as e:
                    self.results["issues_found"].append(f"خطأ في قراءة {route_file}: {e}")
        
        backend_data["api_endpoints"] = api_endpoints
        backend_data["api_endpoints_count"] = len(api_endpoints)
        
        # فحص النماذج
        models_info = []
        models_path = self.backend_path / "src" / "models"
        if models_path.exists():
            for model_file in models_path.glob("*.py"):
                try:
                    with open(model_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # البحث عن تعريفات النماذج
                        models = re.findall(r'class\s+(\w+)\s*\([^)]*Model[^)]*\):', content)
                        for model in models:
                            models_info.append({
                                "file": model_file.name,
                                "model_name": model
                            })
                except Exception as e:
                    self.results["issues_found"].append(f"خطأ في قراءة {model_file}: {e}")
        
        backend_data["models"] = models_info
        backend_data["models_count"] = len(models_info)
        
        # فحص الاستيرادات
        import_issues = []
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # البحث عن استيرادات مكسورة
                    imports = re.findall(r'from\s+([^\s]+)\s+import\s+([^\n]+)', content)
                    for module, items in imports:
                        if 'models.partners' in module and ('Customer' in items or 'Supplier' in items):
                            import_issues.append({
                                "file": str(py_file.relative_to(self.backend_path)),
                                "issue": f"استيراد مكسور: from {module} import {items}"
                            })
            except Exception as e:
                continue
        
        backend_data["import_issues"] = import_issues
        backend_data["import_issues_count"] = len(import_issues)
        
        self.results["backend_detailed"] = backend_data
    
    def audit_frontend_detailed(self):
        """فحص مفصل للواجهة الأمامية"""
        print("🎨 فحص مفصل للواجهة الأمامية...")
        
        frontend_data = {}
        
        # فحص ملفات React
        jsx_files = list(self.frontend_path.rglob("*.jsx"))
        js_files = list(self.frontend_path.rglob("*.js"))
        
        frontend_data["jsx_files_count"] = len(jsx_files)
        frontend_data["js_files_count"] = len(js_files)
        
        # فحص المكونات
        components_analysis = []
        components_path = self.frontend_path / "src" / "components"
        if components_path.exists():
            for component_file in components_path.rglob("*.jsx"):
                try:
                    with open(component_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # تحليل المكون
                        analysis = {
                            "file": str(component_file.relative_to(self.frontend_path)),
                            "size_kb": round(len(content) / 1024, 2),
                            "has_export": "export" in content,
                            "has_styling": "className" in content or "style=" in content,
                            "has_state": "useState" in content or "state" in content,
                            "has_effects": "useEffect" in content,
                            "api_calls": len(re.findall(r'fetch\(|axios\.|api\.', content)),
                            "button_count": len(re.findall(r'<button|onClick', content)),
                            "form_count": len(re.findall(r'<form|onSubmit', content)),
                            "has_error_handling": "try" in content and "catch" in content,
                            "console_logs": len(re.findall(r'console\.log', content))
                        }
                        
                        components_analysis.append(analysis)
                        
                        # فحص المشاكل
                        if analysis["size_kb"] > 50:
                            self.results["issues_found"].append(f"مكون كبير: {analysis['file']} ({analysis['size_kb']} KB)")
                        
                        if analysis["console_logs"] > 0:
                            self.results["issues_found"].append(f"console.log موجود في: {analysis['file']} ({analysis['console_logs']} مرة)")
                        
                        if not analysis["has_styling"]:
                            self.results["issues_found"].append(f"مكون بدون تصميم: {analysis['file']}")
                
                except Exception as e:
                    self.results["issues_found"].append(f"خطأ في تحليل {component_file}: {e}")
        
        frontend_data["components_analysis"] = components_analysis
        frontend_data["components_count"] = len(components_analysis)
        
        # فحص الصفحات
        pages_analysis = []
        pages_path = self.frontend_path / "src" / "pages"
        if pages_path.exists():
            for page_file in pages_path.glob("*.jsx"):
                try:
                    with open(page_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        analysis = {
                            "file": page_file.name,
                            "size_kb": round(len(content) / 1024, 2),
                            "has_routing": "useNavigate" in content or "Link" in content,
                            "has_api_integration": "fetch" in content or "api" in content,
                            "has_form": "<form" in content or "onSubmit" in content,
                            "has_loading_state": "loading" in content or "Loading" in content,
                            "has_error_handling": "error" in content and ("Error" in content or "catch" in content)
                        }
                        
                        pages_analysis.append(analysis)
                
                except Exception as e:
                    self.results["issues_found"].append(f"خطأ في تحليل {page_file}: {e}")
        
        frontend_data["pages_analysis"] = pages_analysis
        frontend_data["pages_count"] = len(pages_analysis)
        
        # فحص التصميم
        styling_analysis = {
            "tailwind_classes": 0,
            "responsive_classes": 0,
            "custom_css_files": 0
        }
        
        for jsx_file in jsx_files:
            try:
                with open(jsx_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    styling_analysis["tailwind_classes"] += len(re.findall(r'bg-|text-|p-|m-|w-|h-', content))
                    styling_analysis["responsive_classes"] += len(re.findall(r'sm:|md:|lg:|xl:', content))
            except:
                continue
        
        css_files = list(self.frontend_path.rglob("*.css"))
        styling_analysis["custom_css_files"] = len(css_files)
        
        frontend_data["styling_analysis"] = styling_analysis
        
        self.results["frontend_detailed"] = frontend_data
    
    def audit_database_detailed(self):
        """فحص مفصل لقاعدة البيانات"""
        print("🗄️ فحص مفصل لقاعدة البيانات...")
        
        database_data = {}
        
        # فحص ملفات قاعدة البيانات
        db_files = list(self.backend_path.rglob("*.db"))
        database_data["db_files"] = [str(f.relative_to(self.backend_path)) for f in db_files]
        database_data["db_files_count"] = len(db_files)
        
        # فحص قاعدة البيانات الرئيسية
        main_db = self.backend_path / "instance" / "inventory.db"
        if main_db.exists():
            try:
                conn = sqlite3.connect(str(main_db))
                cursor = conn.cursor()
                
                # فحص الجداول
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [table[0] for table in cursor.fetchall()]
                database_data["tables"] = tables
                database_data["tables_count"] = len(tables)
                
                # فحص بنية كل جدول
                tables_structure = {}
                for table in tables:
                    cursor.execute(f"PRAGMA table_info({table});")
                    columns = cursor.fetchall()
                    
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    row_count = cursor.fetchone()[0]
                    
                    tables_structure[table] = {
                        "columns": len(columns),
                        "column_details": [{"name": col[1], "type": col[2], "not_null": col[3]} for col in columns],
                        "row_count": row_count
                    }
                
                database_data["tables_structure"] = tables_structure
                
                # فحص الفهارس
                cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
                indexes = [idx[0] for idx in cursor.fetchall()]
                database_data["indexes"] = indexes
                database_data["indexes_count"] = len(indexes)
                
                # فحص حجم قاعدة البيانات
                database_data["size_mb"] = round(main_db.stat().st_size / (1024 * 1024), 2)
                
                conn.close()
                
            except Exception as e:
                self.results["issues_found"].append(f"خطأ في فحص قاعدة البيانات: {e}")
                database_data["error"] = str(e)
        
        self.results["database_detailed"] = database_data
    
    def audit_api_detailed(self):
        """فحص مفصل للـ API"""
        print("🌐 فحص مفصل للـ API...")
        
        api_data = {}
        
        # اختبار تشغيل الخادم
        try:
            # تشغيل الخادم في الخلفية
            server_process = subprocess.Popen(
                ["python", "app.py"],
                cwd=str(self.backend_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # انتظار قصير للخادم
            time.sleep(5)
            
            # اختبار نقاط النهاية المختلفة
            test_endpoints = [
                "/api/health",
                "/api/products",
                "/api/customers", 
                "/api/suppliers",
                "/api/users",
                "/api/categories",
                "/api/warehouses",
                "/api/inventory",
                "/api/reports",
                "/api/auth/login"
            ]
            
            endpoint_results = []
            for endpoint in test_endpoints:
                try:
                    result = subprocess.run(
                        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"http://localhost:5001{endpoint}"],
                        capture_output=True, text=True, timeout=5
                    )
                    
                    status_code = result.stdout.strip() if result.stdout else "فشل"
                    endpoint_results.append({
                        "endpoint": endpoint,
                        "status_code": status_code,
                        "working": status_code in ["200", "201", "401", "403"]  # حتى 401/403 تعني أن النقطة تعمل
                    })
                    
                except Exception as e:
                    endpoint_results.append({
                        "endpoint": endpoint,
                        "status_code": "خطأ",
                        "working": False,
                        "error": str(e)
                    })
            
            api_data["endpoint_tests"] = endpoint_results
            api_data["working_endpoints"] = len([e for e in endpoint_results if e["working"]])
            api_data["total_tested_endpoints"] = len(endpoint_results)
            
            # إيقاف الخادم
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except:
                server_process.kill()
            
        except Exception as e:
            api_data["server_error"] = str(e)
            self.results["issues_found"].append(f"خطأ في اختبار الخادم: {e}")
        
        # فحص استدعاءات API في الواجهة الأمامية
        frontend_api_calls = []
        if self.frontend_path.exists():
            for jsx_file in self.frontend_path.rglob("*.jsx"):
                try:
                    with open(jsx_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # البحث عن استدعاءات API
                        api_calls = re.findall(r'fetch\([\'"]([^\'"]+)[\'"]|axios\.[a-z]+\([\'"]([^\'"]+)[\'"]', content)
                        for call in api_calls:
                            url = call[0] or call[1]
                            if url and ('/api/' in url or 'localhost:5001' in url):
                                frontend_api_calls.append({
                                    "file": str(jsx_file.relative_to(self.frontend_path)),
                                    "api_call": url
                                })
                
                except Exception as e:
                    continue
        
        api_data["frontend_api_calls"] = frontend_api_calls
        api_data["frontend_api_calls_count"] = len(frontend_api_calls)
        
        self.results["api_detailed"] = api_data
    
    def audit_security_detailed(self):
        """فحص مفصل للأمان"""
        print("🔒 فحص مفصل للأمان...")
        
        security_data = {}
        
        # فحص مراجع الأمان في الكود
        security_patterns = {
            "jwt": r'jwt|JWT|token',
            "password": r'password|Password|passwd',
            "encryption": r'encrypt|decrypt|hash|bcrypt|crypto',
            "session": r'session|Session',
            "auth": r'auth|Auth|login|logout',
            "permission": r'permission|Permission|role|Role'
        }
        
        security_findings = {}
        
        for pattern_name, pattern in security_patterns.items():
            findings = []
            
            # فحص الواجهة الخلفية
            for py_file in self.backend_path.rglob("*.py"):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            findings.append({
                                "file": str(py_file.relative_to(self.backend_path)),
                                "matches": len(matches),
                                "type": "backend"
                            })
                except:
                    continue
            
            # فحص الواجهة الأمامية
            for jsx_file in self.frontend_path.rglob("*.jsx"):
                try:
                    with open(jsx_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            findings.append({
                                "file": str(jsx_file.relative_to(self.frontend_path)),
                                "matches": len(matches),
                                "type": "frontend"
                            })
                except:
                    continue
            
            security_findings[pattern_name] = {
                "total_matches": sum(f["matches"] for f in findings),
                "files_count": len(findings),
                "details": findings
            }
        
        security_data["security_patterns"] = security_findings
        
        # فحص كلمات المرور المكشوفة
        exposed_secrets = []
        for py_file in self.backend_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # البحث عن كلمات مرور ثابتة
                    if re.search(r'password\s*=\s*[\'"][^\'"]{3,}[\'"]', content, re.IGNORECASE):
                        exposed_secrets.append({
                            "file": str(py_file.relative_to(self.backend_path)),
                            "type": "hardcoded_password"
                        })
                    
                    # البحث عن مفاتيح API مكشوفة
                    if re.search(r'api[_-]?key\s*=\s*[\'"][^\'"]{10,}[\'"]', content, re.IGNORECASE):
                        exposed_secrets.append({
                            "file": str(py_file.relative_to(self.backend_path)),
                            "type": "exposed_api_key"
                        })
            except:
                continue
        
        security_data["exposed_secrets"] = exposed_secrets
        security_data["exposed_secrets_count"] = len(exposed_secrets)
        
        if exposed_secrets:
            for secret in exposed_secrets:
                self.results["issues_found"].append(f"أمان: {secret['type']} في {secret['file']}")
        
        self.results["security_detailed"] = security_data
    
    def audit_integration_detailed(self):
        """فحص مفصل للتكامل"""
        print("🔗 فحص مفصل للتكامل...")
        
        integration_data = {}
        
        # فحص ربط الأزرار بالوظائف
        button_analysis = []
        for jsx_file in self.frontend_path.rglob("*.jsx"):
            try:
                with open(jsx_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # البحث عن الأزرار
                    buttons = re.findall(r'<button[^>]*onClick\s*=\s*{([^}]+)}', content)
                    for button in buttons:
                        button_type = "unknown"
                        if "handle" in button.lower():
                            button_type = "handler_function"
                        elif "=>" in button:
                            button_type = "arrow_function"
                        elif "fetch" in button or "api" in button:
                            button_type = "api_call"
                        elif "{}" in button or "undefined" in button:
                            button_type = "empty_handler"
                        
                        button_analysis.append({
                            "file": str(jsx_file.relative_to(self.frontend_path)),
                            "handler": button.strip(),
                            "type": button_type
                        })
            except:
                continue
        
        integration_data["button_analysis"] = button_analysis
        integration_data["total_buttons"] = len(button_analysis)
        integration_data["empty_handlers"] = len([b for b in button_analysis if b["type"] == "empty_handler"])
        integration_data["api_connected_buttons"] = len([b for b in button_analysis if b["type"] == "api_call"])
        
        # فحص النماذج
        form_analysis = []
        for jsx_file in self.frontend_path.rglob("*.jsx"):
            try:
                with open(jsx_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # البحث عن النماذج
                    forms = re.findall(r'<form[^>]*onSubmit\s*=\s*{([^}]+)}', content)
                    for form in forms:
                        form_analysis.append({
                            "file": str(jsx_file.relative_to(self.frontend_path)),
                            "handler": form.strip(),
                            "has_validation": "validate" in content.lower() or "error" in content.lower()
                        })
            except:
                continue
        
        integration_data["form_analysis"] = form_analysis
        integration_data["total_forms"] = len(form_analysis)
        integration_data["forms_with_validation"] = len([f for f in form_analysis if f["has_validation"]])
        
        # إضافة مشاكل التكامل
        if integration_data["empty_handlers"] > 0:
            self.results["issues_found"].append(f"تكامل: {integration_data['empty_handlers']} زر بدون وظيفة")
        
        if integration_data["forms_with_validation"] < integration_data["total_forms"]:
            missing_validation = integration_data["total_forms"] - integration_data["forms_with_validation"]
            self.results["issues_found"].append(f"تكامل: {missing_validation} نموذج بدون تحقق")
        
        self.results["integration_detailed"] = integration_data
    
    def generate_recommendations(self):
        """إنشاء التوصيات"""
        print("💡 إنشاء التوصيات...")
        
        recommendations = []
        
        # توصيات الواجهة الخلفية
        if self.results["backend_detailed"].get("syntax_error_count", 0) > 0:
            recommendations.append({
                "priority": "عالية",
                "category": "واجهة خلفية",
                "issue": f"{self.results['backend_detailed']['syntax_error_count']} خطأ نحوي",
                "solution": "إصلاح الأخطاء النحوية في ملفات Python"
            })
        
        if self.results["backend_detailed"].get("import_issues_count", 0) > 0:
            recommendations.append({
                "priority": "متوسطة",
                "category": "واجهة خلفية", 
                "issue": f"{self.results['backend_detailed']['import_issues_count']} مشكلة استيراد",
                "solution": "تحديث الاستيرادات لتتوافق مع البنية الجديدة"
            })
        
        # توصيات الواجهة الأمامية
        large_components = [c for c in self.results["frontend_detailed"].get("components_analysis", []) if c.get("size_kb", 0) > 50]
        if large_components:
            recommendations.append({
                "priority": "متوسطة",
                "category": "واجهة أمامية",
                "issue": f"{len(large_components)} مكون كبير الحجم",
                "solution": "تقسيم المكونات الكبيرة إلى مكونات أصغر"
            })
        
        # توصيات التكامل
        if self.results["integration_detailed"].get("empty_handlers", 0) > 0:
            recommendations.append({
                "priority": "عالية",
                "category": "تكامل",
                "issue": f"{self.results['integration_detailed']['empty_handlers']} زر بدون وظيفة",
                "solution": "ربط الأزرار بوظائف مناسبة"
            })
        
        # توصيات الأمان
        if self.results["security_detailed"].get("exposed_secrets_count", 0) > 0:
            recommendations.append({
                "priority": "عالية جداً",
                "category": "أمان",
                "issue": f"{self.results['security_detailed']['exposed_secrets_count']} معلومة حساسة مكشوفة",
                "solution": "نقل المعلومات الحساسة إلى متغيرات البيئة"
            })
        
        # توصيات الأداء
        if self.results["frontend_detailed"]["styling_analysis"].get("tailwind_classes", 0) > 10000:
            recommendations.append({
                "priority": "منخفضة",
                "category": "أداء",
                "issue": "استخدام مكثف لـ Tailwind CSS",
                "solution": "تحسين استخدام Tailwind وإزالة الفئات غير المستخدمة"
            })
        
        self.results["recommendations"] = recommendations
    
    def calculate_detailed_summary(self):
        """حساب الملخص المفصل"""
        print("📊 حساب الملخص المفصل...")
        
        # حساب النقاط المفصلة
        backend_score = 100
        if self.results["backend_detailed"].get("syntax_error_count", 0) > 0:
            backend_score -= self.results["backend_detailed"]["syntax_error_count"] * 5
        if self.results["backend_detailed"].get("import_issues_count", 0) > 0:
            backend_score -= self.results["backend_detailed"]["import_issues_count"] * 2
        backend_score = max(0, backend_score)
        
        frontend_score = 100
        components_with_issues = len([c for c in self.results["frontend_detailed"].get("components_analysis", []) 
                                    if not c.get("has_styling", True) or c.get("console_logs", 0) > 0])
        frontend_score -= components_with_issues * 2
        frontend_score = max(0, frontend_score)
        
        api_score = 100
        if "api_detailed" in self.results and "endpoint_tests" in self.results["api_detailed"]:
            working = self.results["api_detailed"]["working_endpoints"]
            total = self.results["api_detailed"]["total_tested_endpoints"]
            if total > 0:
                api_score = (working / total) * 100
        
        security_score = 100
        if self.results["security_detailed"].get("exposed_secrets_count", 0) > 0:
            security_score -= self.results["security_detailed"]["exposed_secrets_count"] * 20
        security_score = max(0, security_score)
        
        integration_score = 100
        if self.results["integration_detailed"].get("empty_handlers", 0) > 0:
            integration_score -= self.results["integration_detailed"]["empty_handlers"] * 5
        if self.results["integration_detailed"].get("total_forms", 0) > 0:
            validation_ratio = self.results["integration_detailed"]["forms_with_validation"] / self.results["integration_detailed"]["total_forms"]
            integration_score = integration_score * validation_ratio
        integration_score = max(0, integration_score)
        
        overall_score = (backend_score + frontend_score + api_score + security_score + integration_score) / 5
        
        self.results["summary_detailed"] = {
            "backend_score": round(backend_score, 1),
            "frontend_score": round(frontend_score, 1),
            "api_score": round(api_score, 1),
            "security_score": round(security_score, 1),
            "integration_score": round(integration_score, 1),
            "overall_score": round(overall_score, 1),
            "grade": self.get_grade(overall_score),
            "total_issues": len(self.results["issues_found"]),
            "total_recommendations": len(self.results["recommendations"]),
            "critical_issues": len([r for r in self.results["recommendations"] if r["priority"] in ["عالية جداً", "عالية"]])
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
    
    def run_ultra_deep_audit(self):
        """تشغيل الفحص المتعمق جداً"""
        print("🚀 بدء الفحص المتعمق جداً للنظام...")
        print("=" * 60)
        
        self.audit_backend_detailed()
        self.audit_frontend_detailed()
        self.audit_database_detailed()
        self.audit_api_detailed()
        self.audit_security_detailed()
        self.audit_integration_detailed()
        self.generate_recommendations()
        self.calculate_detailed_summary()
        
        print("=" * 60)
        print("✅ تم الانتهاء من الفحص المتعمق جداً!")
        
        return self.results
    
    def save_results(self, filename="ultra_deep_audit_results.json"):
        """حفظ النتائج"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"💾 تم حفظ النتائج في: {filename}")

if __name__ == "__main__":
    auditor = UltraDeepSystemAudit()
    results = auditor.run_ultra_deep_audit()
    auditor.save_results()
    
    # طباعة الملخص المفصل
    summary = results["summary_detailed"]
    print(f"\n📊 الملخص المفصل:")
    print(f"الواجهة الخلفية: {summary['backend_score']}/100")
    print(f"الواجهة الأمامية: {summary['frontend_score']}/100")
    print(f"API: {summary['api_score']}/100")
    print(f"الأمان: {summary['security_score']}/100")
    print(f"التكامل: {summary['integration_score']}/100")
    print(f"النقاط الإجمالية: {summary['overall_score']}/100")
    print(f"التقدير: {summary['grade']}")
    print(f"المشاكل المكتشفة: {summary['total_issues']}")
    print(f"التوصيات: {summary['total_recommendations']}")
    print(f"المشاكل الحرجة: {summary['critical_issues']}")
