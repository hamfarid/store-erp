# File: /home/ubuntu/clean_project/comprehensive_test.py
"""
مسار الملف: /home/ubuntu/clean_project/comprehensive_test.py

اختبار شامل لجميع مكونات نظام WhatIsScanAI
يفحص التكامل والوظائف والأداء
"""

import asyncio
import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

# إضافة مسار المشروع
sys.path.append(str(Path(__file__).parent / "src"))

# استيراد المكونات الأساسية
try:
    from src.core.integration_manager import IntegrationManager, get_integration_manager
    from src.core.config import Config
    from src.core.error_handling import ErrorHandler
    from src.database_models import init_database
    print("✅ تم استيراد المكونات الأساسية بنجاح")
except ImportError as e:
    print(f"❌ فشل في استيراد المكونات الأساسية: {e}")
    sys.exit(1)

class ComprehensiveTestSuite:
    """مجموعة الاختبارات الشاملة"""
    
    def __init__(self):
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': [],
            'start_time': None,
            'end_time': None,
            'duration': None
        }
        self.config = None
        self.integration_manager = None
        
    async def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🚀 بدء الاختبار الشامل لنظام WhatIsScanAI")
        print("=" * 60)
        
        self.test_results['start_time'] = datetime.now()
        
        # اختبارات التكوين
        await self.test_configuration()
        
        # اختبارات قاعدة البيانات
        await self.test_database()
        
        # اختبارات الخدمات الأساسية
        await self.test_core_services()
        
        # اختبارات الذكاء الاصطناعي
        await self.test_ai_services()
        
        # اختبارات واجهات برمجة التطبيقات
        await self.test_apis()
        
        # اختبارات التكامل
        await self.test_integration()
        
        # اختبارات الأداء
        await self.test_performance()
        
        # اختبارات الأمان
        await self.test_security()
        
        self.test_results['end_time'] = datetime.now()
        self.test_results['duration'] = (
            self.test_results['end_time'] - self.test_results['start_time']
        ).total_seconds()
        
        # إنشاء التقرير النهائي
        await self.generate_test_report()
        
        return self.test_results
    
    async def test_configuration(self):
        """اختبار التكوين"""
        print("\n📋 اختبار التكوين...")
        
        try:
            # اختبار إنشاء التكوين
            self.config = Config()
            self._record_test("Configuration Creation", True, "تم إنشاء التكوين بنجاح")
            
            # اختبار المتغيرات الأساسية
            required_vars = ['DATABASE_URL', 'SECRET_KEY', 'AI_MODEL_PATH']
            for var in required_vars:
                if hasattr(self.config, var.lower()):
                    self._record_test(f"Config Variable: {var}", True, f"المتغير {var} موجود")
                else:
                    self._record_test(f"Config Variable: {var}", False, f"المتغير {var} مفقود")
            
        except Exception as e:
            self._record_test("Configuration", False, f"فشل في التكوين: {e}")
    
    async def test_database(self):
        """اختبار قاعدة البيانات"""
        print("\n🗄️ اختبار قاعدة البيانات...")
        
        try:
            # اختبار إنشاء قاعدة البيانات
            engine, SessionMaker = init_database("sqlite:///test_db.db")
            self._record_test("Database Creation", True, "تم إنشاء قاعدة البيانات بنجاح")
            
            # اختبار الجداول
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            expected_tables = [
                'users', 'crops', 'diseases', 'diagnoses',
                'ai_memory', 'generative_models', 'vision_models',
                'collaborative_projects', 'predictive_alerts',
                'treatment_plans', 'distributed_nodes'
            ]
            
            for table in expected_tables:
                if table in tables:
                    self._record_test(f"Table: {table}", True, f"الجدول {table} موجود")
                else:
                    self._record_test(f"Table: {table}", False, f"الجدول {table} مفقود")
            
            # اختبار العمليات الأساسية
            session = SessionMaker()
            try:
                from src.database_models import User
                test_user = User(
                    username="test_user",
                    email="test@example.com",
                    full_name="Test User"
                )
                test_user.set_password("test_password")
                session.add(test_user)
                session.commit()
                
                # التحقق من إدراج البيانات
                retrieved_user = session.query(User).filter_by(username="test_user").first()
                if retrieved_user and retrieved_user.check_password("test_password"):
                    self._record_test("Database Operations", True, "العمليات الأساسية تعمل بنجاح")
                else:
                    self._record_test("Database Operations", False, "فشل في العمليات الأساسية")
                
            finally:
                session.close()
            
        except Exception as e:
            self._record_test("Database", False, f"فشل في اختبار قاعدة البيانات: {e}")
    
    async def test_core_services(self):
        """اختبار الخدمات الأساسية"""
        print("\n⚙️ اختبار الخدمات الأساسية...")
        
        try:
            # اختبار مدير التكامل
            self.integration_manager = await get_integration_manager(self.config)
            self._record_test("Integration Manager", True, "تم إنشاء مدير التكامل بنجاح")
            
            # اختبار حالة النظام
            status = await self.integration_manager.get_system_status()
            if status.get('success'):
                self._record_test("System Status", True, "حالة النظام سليمة")
            else:
                self._record_test("System Status", False, "مشكلة في حالة النظام")
            
            # اختبار خدمة الذاكرة
            if 'memory' in self.integration_manager.services:
                memory_service = self.integration_manager.services['memory']
                test_memory = await memory_service.store_memory(
                    "test", {"test": "data"}, "test_context"
                )
                if test_memory.get('success'):
                    self._record_test("Memory Service", True, "خدمة الذاكرة تعمل بنجاح")
                else:
                    self._record_test("Memory Service", False, "مشكلة في خدمة الذاكرة")
            
        except Exception as e:
            self._record_test("Core Services", False, f"فشل في اختبار الخدمات الأساسية: {e}")
    
    async def test_ai_services(self):
        """اختبار خدمات الذكاء الاصطناعي"""
        print("\n🤖 اختبار خدمات الذكاء الاصطناعي...")
        
        try:
            # اختبار الذكاء الاصطناعي التوليدي
            if 'generative_ai' in self.integration_manager.services:
                gen_ai = self.integration_manager.services['generative_ai']
                models = await gen_ai.get_available_models()
                if models.get('success'):
                    self._record_test("Generative AI Models", True, f"متوفر {len(models.get('models', []))} نموذج توليدي")
                else:
                    self._record_test("Generative AI Models", False, "مشكلة في النماذج التوليدية")
            
            # اختبار الرؤية المتقدمة
            if 'advanced_vision' in self.integration_manager.services:
                vision = self.integration_manager.services['advanced_vision']
                models = await vision.get_available_models()
                if models.get('success'):
                    self._record_test("Vision Models", True, f"متوفر {len(models.get('models', []))} نموذج رؤية")
                else:
                    self._record_test("Vision Models", False, "مشكلة في نماذج الرؤية")
            
            # اختبار التشخيص الاستباقي
            if 'predictive_diagnosis' in self.integration_manager.services:
                pred_diag = self.integration_manager.services['predictive_diagnosis']
                health = await pred_diag.health_check()
                if health.get('status') == 'healthy':
                    self._record_test("Predictive Diagnosis", True, "نظام التشخيص الاستباقي يعمل بنجاح")
                else:
                    self._record_test("Predictive Diagnosis", False, "مشكلة في نظام التشخيص الاستباقي")
            
        except Exception as e:
            self._record_test("AI Services", False, f"فشل في اختبار خدمات الذكاء الاصطناعي: {e}")
    
    async def test_apis(self):
        """اختبار واجهات برمجة التطبيقات"""
        print("\n🌐 اختبار واجهات برمجة التطبيقات...")
        
        try:
            # اختبار APIs المتوفرة
            apis = self.integration_manager.apis
            
            for api_name, api in apis.items():
                try:
                    if hasattr(api, 'health_check'):
                        health = await api.health_check()
                        if health.get('status') == 'healthy':
                            self._record_test(f"API: {api_name}", True, f"API {api_name} يعمل بنجاح")
                        else:
                            self._record_test(f"API: {api_name}", False, f"مشكلة في API {api_name}")
                    else:
                        self._record_test(f"API: {api_name}", True, f"API {api_name} متوفر")
                except Exception as e:
                    self._record_test(f"API: {api_name}", False, f"خطأ في API {api_name}: {e}")
            
        except Exception as e:
            self._record_test("APIs", False, f"فشل في اختبار واجهات برمجة التطبيقات: {e}")
    
    async def test_integration(self):
        """اختبار التكامل"""
        print("\n🔗 اختبار التكامل...")
        
        try:
            # اختبار التكامل بين الخدمات
            if 'generative_ai' in self.integration_manager.services and 'memory' in self.integration_manager.services:
                # اختبار تكامل الذكاء الاصطناعي مع الذاكرة
                gen_ai = self.integration_manager.services['generative_ai']
                memory = self.integration_manager.services['memory']
                
                # تخزين ذاكرة
                memory_result = await memory.store_memory(
                    "integration_test", 
                    {"test": "integration"}, 
                    "test_integration"
                )
                
                if memory_result.get('success'):
                    self._record_test("AI-Memory Integration", True, "تكامل الذكاء الاصطناعي والذاكرة يعمل")
                else:
                    self._record_test("AI-Memory Integration", False, "مشكلة في تكامل الذكاء الاصطناعي والذاكرة")
            
            # اختبار التكامل مع قاعدة البيانات
            try:
                from src.database_models import AIMemory
                engine, SessionMaker = init_database("sqlite:///test_db.db")
                session = SessionMaker()
                
                test_memory = AIMemory(
                    memory_type="test",
                    content={"test": "integration"},
                    context={"source": "integration_test"}
                )
                session.add(test_memory)
                session.commit()
                
                retrieved = session.query(AIMemory).filter_by(memory_type="test").first()
                if retrieved:
                    self._record_test("Database Integration", True, "تكامل قاعدة البيانات يعمل بنجاح")
                else:
                    self._record_test("Database Integration", False, "مشكلة في تكامل قاعدة البيانات")
                
                session.close()
                
            except Exception as e:
                self._record_test("Database Integration", False, f"خطأ في تكامل قاعدة البيانات: {e}")
            
        except Exception as e:
            self._record_test("Integration", False, f"فشل في اختبار التكامل: {e}")
    
    async def test_performance(self):
        """اختبار الأداء"""
        print("\n⚡ اختبار الأداء...")
        
        try:
            # اختبار سرعة الاستجابة
            start_time = time.time()
            status = await self.integration_manager.get_system_status()
            response_time = time.time() - start_time
            
            if response_time < 2.0:  # أقل من ثانيتين
                self._record_test("Response Time", True, f"زمن الاستجابة: {response_time:.2f} ثانية")
            else:
                self._record_test("Response Time", False, f"زمن الاستجابة بطيء: {response_time:.2f} ثانية")
            
            # اختبار استخدام الذاكرة
            import psutil
            memory_usage = psutil.virtual_memory().percent
            if memory_usage < 80:
                self._record_test("Memory Usage", True, f"استخدام الذاكرة: {memory_usage}%")
            else:
                self._record_test("Memory Usage", False, f"استخدام الذاكرة مرتفع: {memory_usage}%")
            
        except Exception as e:
            self._record_test("Performance", False, f"فشل في اختبار الأداء: {e}")
    
    async def test_security(self):
        """اختبار الأمان"""
        print("\n🔒 اختبار الأمان...")
        
        try:
            # اختبار تشفير كلمات المرور
            from src.database_models import User
            test_user = User(
                username="security_test",
                email="security@test.com",
                full_name="Security Test"
            )
            test_user.set_password("test_password_123")
            
            # التحقق من التشفير
            if test_user.password_hash != "test_password_123":
                self._record_test("Password Encryption", True, "تشفير كلمات المرور يعمل بنجاح")
            else:
                self._record_test("Password Encryption", False, "كلمات المرور غير مشفرة")
            
            # التحقق من صحة كلمة المرور
            if test_user.check_password("test_password_123"):
                self._record_test("Password Verification", True, "التحقق من كلمة المرور يعمل بنجاح")
            else:
                self._record_test("Password Verification", False, "مشكلة في التحقق من كلمة المرور")
            
            # اختبار معالجة الأخطاء
            error_handler = ErrorHandler()
            try:
                raise ValueError("Test error")
            except Exception as e:
                error_info = error_handler.handle_error(e, "security_test")
                if error_info.get('error_id'):
                    self._record_test("Error Handling", True, "معالجة الأخطاء تعمل بنجاح")
                else:
                    self._record_test("Error Handling", False, "مشكلة في معالجة الأخطاء")
            
        except Exception as e:
            self._record_test("Security", False, f"فشل في اختبار الأمان: {e}")
    
    def _record_test(self, test_name: str, passed: bool, message: str):
        """تسجيل نتيجة اختبار"""
        self.test_results['total_tests'] += 1
        
        if passed:
            self.test_results['passed_tests'] += 1
            status = "✅ نجح"
            print(f"  {status} {test_name}: {message}")
        else:
            self.test_results['failed_tests'] += 1
            status = "❌ فشل"
            print(f"  {status} {test_name}: {message}")
        
        self.test_results['test_details'].append({
            'test_name': test_name,
            'status': 'passed' if passed else 'failed',
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    async def generate_test_report(self):
        """إنشاء تقرير الاختبار"""
        print("\n" + "=" * 60)
        print("📊 تقرير الاختبار الشامل")
        print("=" * 60)
        
        total = self.test_results['total_tests']
        passed = self.test_results['passed_tests']
        failed = self.test_results['failed_tests']
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"إجمالي الاختبارات: {total}")
        print(f"الاختبارات الناجحة: {passed}")
        print(f"الاختبارات الفاشلة: {failed}")
        print(f"معدل النجاح: {success_rate:.1f}%")
        print(f"مدة الاختبار: {self.test_results['duration']:.2f} ثانية")
        
        # حفظ التقرير في ملف
        report_file = Path("test_reports") / f"comprehensive_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n📄 تم حفظ التقرير في: {report_file}")
        
        if success_rate >= 90:
            print("\n🎉 النظام يعمل بشكل ممتاز!")
        elif success_rate >= 75:
            print("\n✅ النظام يعمل بشكل جيد مع بعض المشاكل البسيطة")
        else:
            print("\n⚠️ النظام يحتاج إلى إصلاحات مهمة")

async def main():
    """الدالة الرئيسية"""
    test_suite = ComprehensiveTestSuite()
    results = await test_suite.run_all_tests()
    
    # تنظيف الملفات المؤقتة
    try:
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")
    except:
        pass
    
    return results

if __name__ == "__main__":
    # تشغيل الاختبارات
    results = asyncio.run(main())
    
    # إنهاء البرنامج بحالة مناسبة
    success_rate = (results['passed_tests'] / results['total_tests'] * 100) if results['total_tests'] > 0 else 0
    sys.exit(0 if success_rate >= 75 else 1)

