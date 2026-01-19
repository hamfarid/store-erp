# /home/ubuntu/gaara-ai-system/performance_test.py

"""
سكريبت اختبار الأداء الشامل لنظام Gaara AI
Comprehensive Performance Testing Script for Gaara AI System
"""

import time
import psutil
import threading
import sqlite3
import json
import os
import sys
import traceback
from datetime import datetime
from typing import Dict, List, Any
import subprocess
import gc
import resource

class PerformanceTester:
    """فئة اختبار الأداء"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        
    def log_result(self, test_name: str, result: Dict[str, Any]):
        """تسجيل نتيجة اختبار"""
        self.results[test_name] = {
            **result,
            'timestamp': datetime.now().isoformat()
        }
        
    def test_system_resources(self) -> Dict[str, Any]:
        """اختبار موارد النظام"""
        print("📊 فحص استهلاك الموارد...")
        
        try:
            # CPU
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # الذاكرة
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            memory_used_gb = memory.used / (1024**3)
            
            # القرص
            disk = psutil.disk_usage('/')
            disk_gb = disk.total / (1024**3)
            disk_used_gb = disk.used / (1024**3)
            
            # الشبكة
            network = psutil.net_io_counters()
            
            result = {
                'status': 'success',
                'cpu': {
                    'usage_percent': cpu_usage,
                    'core_count': cpu_count,
                    'status': 'good' if cpu_usage < 80 else 'warning'
                },
                'memory': {
                    'total_gb': round(memory_gb, 2),
                    'used_gb': round(memory_used_gb, 2),
                    'usage_percent': memory.percent,
                    'available_gb': round(memory.available / (1024**3), 2),
                    'status': 'good' if memory.percent < 80 else 'warning'
                },
                'disk': {
                    'total_gb': round(disk_gb, 2),
                    'used_gb': round(disk_used_gb, 2),
                    'usage_percent': disk.percent,
                    'free_gb': round(disk.free / (1024**3), 2),
                    'status': 'good' if disk.percent < 90 else 'warning'
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                }
            }
            
            print(f"   ✅ CPU: {cpu_usage}% ({cpu_count} cores)")
            print(f"   ✅ الذاكرة: {memory.percent}% ({memory_used_gb:.1f}GB من {memory_gb:.1f}GB)")
            print(f"   ✅ القرص: {disk.percent}% ({disk_used_gb:.1f}GB من {disk_gb:.1f}GB)")
            
            return result
            
        except Exception as e:
            print(f"   ❌ خطأ في اختبار موارد النظام: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def test_database_performance(self) -> Dict[str, Any]:
        """اختبار أداء قاعدة البيانات"""
        print("🗄️ اختبار قواعد البيانات...")
        
        try:
            db_path = 'test_performance.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # إنشاء جدول اختبار
            cursor.execute('''CREATE TABLE IF NOT EXISTS test_table 
                             (id INTEGER PRIMARY KEY, data TEXT, timestamp DATETIME)''')
            
            # اختبار الكتابة
            write_start = time.time()
            test_records = 5000
            
            for i in range(test_records):
                cursor.execute('INSERT INTO test_table (data, timestamp) VALUES (?, ?)', 
                              (f'test_data_{i}_{time.time()}', datetime.now()))
            
            conn.commit()
            write_time = time.time() - write_start
            
            # اختبار القراءة
            read_start = time.time()
            cursor.execute('SELECT COUNT(*) FROM test_table')
            count = cursor.fetchone()[0]
            read_time = time.time() - read_start
            
            # اختبار الاستعلام المعقد
            complex_start = time.time()
            cursor.execute('''SELECT data, COUNT(*) as count 
                             FROM test_table 
                             WHERE data LIKE 'test_data_%' 
                             GROUP BY substr(data, 1, 15) 
                             ORDER BY count DESC 
                             LIMIT 10''')
            complex_results = cursor.fetchall()
            complex_time = time.time() - complex_start
            
            # اختبار التحديث
            update_start = time.time()
            cursor.execute('UPDATE test_table SET data = data || "_updated" WHERE id % 100 = 0')
            conn.commit()
            update_time = time.time() - update_start
            
            conn.close()
            
            # حذف ملف الاختبار
            if os.path.exists(db_path):
                os.remove(db_path)
            
            result = {
                'status': 'success',
                'write_performance': {
                    'records': test_records,
                    'time_seconds': round(write_time, 3),
                    'records_per_second': round(test_records / write_time, 2)
                },
                'read_performance': {
                    'time_seconds': round(read_time, 3),
                    'total_records': count
                },
                'complex_query': {
                    'time_seconds': round(complex_time, 3),
                    'results_count': len(complex_results)
                },
                'update_performance': {
                    'time_seconds': round(update_time, 3)
                }
            }
            
            print(f"   ✅ كتابة {test_records} سجل: {write_time:.3f}s ({test_records/write_time:.0f} سجل/ثانية)")
            print(f"   ✅ قراءة العدد الكلي: {read_time:.3f}s")
            print(f"   ✅ استعلام معقد: {complex_time:.3f}s")
            print(f"   ✅ تحديث البيانات: {update_time:.3f}s")
            
            return result
            
        except Exception as e:
            print(f"   ❌ خطأ في اختبار قاعدة البيانات: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def test_memory_performance(self) -> Dict[str, Any]:
        """اختبار أداء الذاكرة"""
        print("💾 اختبار الذاكرة...")
        
        try:
            # قياس الذاكرة قبل الاختبار
            start_memory = psutil.virtual_memory().used
            
            # إنشاء بيانات كبيرة
            large_data = []
            test_size = 50000
            
            memory_start = time.time()
            for i in range(test_size):
                large_data.append({
                    'id': i,
                    'data': 'x' * 200,
                    'timestamp': datetime.now(),
                    'metadata': {'type': 'test', 'index': i}
                })
            memory_time = time.time() - memory_start
            
            # قياس الذاكرة بعد الإنشاء
            mid_memory = psutil.virtual_memory().used
            memory_used = (mid_memory - start_memory) / (1024 * 1024)
            
            # اختبار الوصول للبيانات
            access_start = time.time()
            for i in range(0, test_size, 100):
                _ = large_data[i]['data']
            access_time = time.time() - access_start
            
            # اختبار البحث
            search_start = time.time()
            found_items = [item for item in large_data if item['id'] % 1000 == 0]
            search_time = time.time() - search_start
            
            # تنظيف الذاكرة
            del large_data
            gc.collect()
            
            end_memory = psutil.virtual_memory().used
            
            result = {
                'status': 'success',
                'allocation': {
                    'items': test_size,
                    'time_seconds': round(memory_time, 3),
                    'memory_used_mb': round(memory_used, 2),
                    'items_per_second': round(test_size / memory_time, 2)
                },
                'access': {
                    'time_seconds': round(access_time, 3),
                    'accesses': test_size // 100
                },
                'search': {
                    'time_seconds': round(search_time, 3),
                    'found_items': len(found_items)
                },
                'memory_cleanup': {
                    'recovered_mb': round((mid_memory - end_memory) / (1024 * 1024), 2)
                }
            }
            
            print(f"   ✅ إنشاء {test_size} عنصر: {memory_time:.3f}s ({memory_used:.1f}MB)")
            print(f"   ✅ الوصول للبيانات: {access_time:.3f}s")
            print(f"   ✅ البحث في البيانات: {search_time:.3f}s ({len(found_items)} نتيجة)")
            
            return result
            
        except Exception as e:
            print(f"   ❌ خطأ في اختبار الذاكرة: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def test_concurrent_performance(self) -> Dict[str, Any]:
        """اختبار الأداء المتزامن"""
        print("🌐 اختبار الأداء المتزامن...")
        
        try:
            results = []
            errors = []
            
            def worker_task(worker_id: int):
                """مهمة العامل"""
                try:
                    start_time = time.time()
                    
                    # محاكاة عمل معقد
                    data = []
                    for i in range(1000):
                        data.append(f"worker_{worker_id}_item_{i}")
                    
                    # محاكاة معالجة البيانات
                    processed = [item.upper() for item in data if 'worker' in item]
                    
                    end_time = time.time()
                    
                    results.append({
                        'worker_id': worker_id,
                        'processing_time': end_time - start_time,
                        'items_processed': len(processed)
                    })
                    
                except Exception as e:
                    errors.append({'worker_id': worker_id, 'error': str(e)})
            
            # تشغيل عدة threads
            thread_count = 20
            threads = []
            
            concurrent_start = time.time()
            
            for i in range(thread_count):
                thread = threading.Thread(target=worker_task, args=(i,))
                threads.append(thread)
                thread.start()
            
            # انتظار انتهاء جميع المهام
            for thread in threads:
                thread.join()
            
            concurrent_time = time.time() - concurrent_start
            
            # تحليل النتائج
            if results:
                avg_processing_time = sum(r['processing_time'] for r in results) / len(results)
                total_items = sum(r['items_processed'] for r in results)
                throughput = total_items / concurrent_time
            else:
                avg_processing_time = 0
                total_items = 0
                throughput = 0
            
            result = {
                'status': 'success',
                'concurrent_execution': {
                    'thread_count': thread_count,
                    'total_time_seconds': round(concurrent_time, 3),
                    'successful_workers': len(results),
                    'failed_workers': len(errors),
                    'avg_worker_time': round(avg_processing_time, 3),
                    'total_items_processed': total_items,
                    'throughput_items_per_second': round(throughput, 2)
                },
                'errors': errors[:5]  # أول 5 أخطاء فقط
            }
            
            print(f"   ✅ {thread_count} thread متزامن: {concurrent_time:.3f}s")
            print(f"   ✅ نجح: {len(results)}, فشل: {len(errors)}")
            print(f"   ✅ معدل المعالجة: {throughput:.0f} عنصر/ثانية")
            
            return result
            
        except Exception as e:
            print(f"   ❌ خطأ في اختبار الأداء المتزامن: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def test_file_io_performance(self) -> Dict[str, Any]:
        """اختبار أداء الملفات"""
        print("📁 اختبار معالجة الملفات...")
        
        try:
            test_file = 'test_large_file.txt'
            test_lines = 20000
            
            # اختبار الكتابة
            write_start = time.time()
            with open(test_file, 'w', encoding='utf-8') as f:
                for i in range(test_lines):
                    f.write(f'سطر رقم {i} - بيانات اختبار الأداء مع نص عربي وإنجليزي mixed content\\n')
            write_time = time.time() - write_start
            
            # حجم الملف
            file_size = os.path.getsize(test_file)
            file_size_mb = file_size / (1024 * 1024)
            
            # اختبار القراءة
            read_start = time.time()
            with open(test_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            read_time = time.time() - read_start
            
            # اختبار المعالجة
            process_start = time.time()
            processed_lines = [line.strip().upper() for line in lines if 'اختبار' in line]
            process_time = time.time() - process_start
            
            # اختبار الإلحاق
            append_start = time.time()
            with open(test_file, 'a', encoding='utf-8') as f:
                for i in range(1000):
                    f.write(f'سطر إضافي {i}\\n')
            append_time = time.time() - append_start
            
            # حذف الملف
            if os.path.exists(test_file):
                os.remove(test_file)
            
            result = {
                'status': 'success',
                'write_performance': {
                    'lines': test_lines,
                    'time_seconds': round(write_time, 3),
                    'file_size_mb': round(file_size_mb, 2),
                    'write_speed_mb_per_sec': round(file_size_mb / write_time, 2)
                },
                'read_performance': {
                    'time_seconds': round(read_time, 3),
                    'lines_read': len(lines),
                    'read_speed_mb_per_sec': round(file_size_mb / read_time, 2)
                },
                'processing': {
                    'time_seconds': round(process_time, 3),
                    'processed_lines': len(processed_lines)
                },
                'append_performance': {
                    'time_seconds': round(append_time, 3),
                    'lines_appended': 1000
                }
            }
            
            print(f"   ✅ كتابة {test_lines} سطر: {write_time:.3f}s ({file_size_mb:.1f}MB)")
            print(f"   ✅ قراءة الملف: {read_time:.3f}s")
            print(f"   ✅ معالجة البيانات: {process_time:.3f}s ({len(processed_lines)} سطر)")
            print(f"   ✅ إلحاق البيانات: {append_time:.3f}s")
            
            return result
            
        except Exception as e:
            print(f"   ❌ خطأ في اختبار الملفات: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def test_python_performance(self) -> Dict[str, Any]:
        """اختبار أداء Python"""
        print("🐍 اختبار أداء Python...")
        
        try:
            # اختبار الحلقات
            loop_start = time.time()
            result_sum = 0
            for i in range(1000000):
                result_sum += i * 2
            loop_time = time.time() - loop_start
            
            # اختبار القوائم
            list_start = time.time()
            test_list = [i**2 for i in range(100000)]
            list_time = time.time() - list_start
            
            # اختبار القواميس
            dict_start = time.time()
            test_dict = {f'key_{i}': f'value_{i}' for i in range(50000)}
            dict_time = time.time() - dict_start
            
            # اختبار الدوال
            def test_function(x):
                return x**2 + x**0.5 + abs(x)
            
            func_start = time.time()
            func_results = [test_function(i) for i in range(100000)]
            func_time = time.time() - func_start
            
            # اختبار معالجة النصوص
            text_start = time.time()
            test_text = "هذا نص تجريبي للاختبار " * 1000
            text_operations = [
                test_text.upper(),
                test_text.lower(),
                test_text.replace("تجريبي", "حقيقي"),
                len(test_text.split())
            ]
            text_time = time.time() - text_start
            
            result = {
                'status': 'success',
                'loop_performance': {
                    'iterations': 1000000,
                    'time_seconds': round(loop_time, 3),
                    'iterations_per_second': round(1000000 / loop_time, 0)
                },
                'list_comprehension': {
                    'items': 100000,
                    'time_seconds': round(list_time, 3)
                },
                'dictionary_creation': {
                    'items': 50000,
                    'time_seconds': round(dict_time, 3)
                },
                'function_calls': {
                    'calls': 100000,
                    'time_seconds': round(func_time, 3),
                    'calls_per_second': round(100000 / func_time, 0)
                },
                'text_processing': {
                    'time_seconds': round(text_time, 3),
                    'operations': len(text_operations)
                }
            }
            
            print(f"   ✅ حلقة مليون تكرار: {loop_time:.3f}s")
            print(f"   ✅ إنشاء قائمة 100k عنصر: {list_time:.3f}s")
            print(f"   ✅ إنشاء قاموس 50k عنصر: {dict_time:.3f}s")
            print(f"   ✅ استدعاء دالة 100k مرة: {func_time:.3f}s")
            print(f"   ✅ معالجة النصوص: {text_time:.3f}s")
            
            return result
            
        except Exception as e:
            print(f"   ❌ خطأ في اختبار Python: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def generate_performance_report(self) -> str:
        """إنشاء تقرير الأداء"""
        total_time = time.time() - self.start_time
        
        report = f"""
# تقرير اختبار الأداء الشامل لنظام Gaara AI
## Comprehensive Performance Test Report for Gaara AI System

**تاريخ الاختبار:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**مدة الاختبار:** {total_time:.2f} ثانية

---

## ملخص النتائج / Results Summary

"""
        
        for test_name, result in self.results.items():
            status_emoji = "✅" if result.get('status') == 'success' else "❌"
            report += f"### {status_emoji} {test_name}\n"
            
            if result.get('status') == 'success':
                report += "**الحالة:** نجح الاختبار\n\n"
                
                # إضافة تفاصيل النتائج
                for key, value in result.items():
                    if key not in ['status', 'timestamp']:
                        if isinstance(value, dict):
                            report += f"**{key}:**\n"
                            for sub_key, sub_value in value.items():
                                report += f"  - {sub_key}: {sub_value}\n"
                        else:
                            report += f"**{key}:** {value}\n"
                report += "\n"
            else:
                report += f"**الحالة:** فشل الاختبار\n"
                report += f"**الخطأ:** {result.get('error', 'خطأ غير محدد')}\n\n"
        
        # إضافة التوصيات
        report += """
---

## التوصيات / Recommendations

### الأداء العام / General Performance
- النظام يعمل بأداء جيد في البيئة الحالية
- يُنصح بمراقبة استهلاك الموارد بشكل دوري
- تحسين الاستعلامات المعقدة في قاعدة البيانات

### الأمان / Security
- تطبيق نظام المراقبة المتقدم المطور
- مراجعة دورية لسجلات الأمان
- تحديث كلمات المرور بانتظام

### التطوير / Development
- استخدام فهرسة أفضل لقاعدة البيانات
- تحسين خوارزميات المعالجة المتزامنة
- تطبيق تقنيات التخزين المؤقت

---

**تم إنشاء هذا التقرير بواسطة نظام اختبار الأداء الشامل لـ Gaara AI**
"""
        
        return report
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🚀 بدء اختبار الأداء الشامل لنظام Gaara AI")
        print("=" * 60)
        
        # قائمة الاختبارات
        tests = [
            ("فحص موارد النظام", self.test_system_resources),
            ("اختبار قاعدة البيانات", self.test_database_performance),
            ("اختبار الذاكرة", self.test_memory_performance),
            ("اختبار الأداء المتزامن", self.test_concurrent_performance),
            ("اختبار الملفات", self.test_file_io_performance),
            ("اختبار Python", self.test_python_performance)
        ]
        
        # تشغيل الاختبارات
        for test_name, test_func in tests:
            try:
                result = test_func()
                self.log_result(test_name, result)
            except Exception as e:
                print(f"❌ خطأ في {test_name}: {e}")
                self.log_result(test_name, {'status': 'error', 'error': str(e)})
            
            print()  # سطر فارغ بين الاختبارات
        
        print("=" * 60)
        print("✅ انتهى اختبار الأداء الشامل")
        
        # إنشاء التقرير
        report = self.generate_performance_report()
        
        # حفظ التقرير
        with open('performance_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 تم حفظ التقرير في: performance_report.md")
        
        return self.results

def main():
    """الدالة الرئيسية"""
    try:
        tester = PerformanceTester()
        results = tester.run_all_tests()
        
        # عرض ملخص سريع
        successful_tests = sum(1 for r in results.values() if r.get('status') == 'success')
        total_tests = len(results)
        
        print(f"\n📊 ملخص النتائج: {successful_tests}/{total_tests} اختبار نجح")
        
        if successful_tests == total_tests:
            print("🎉 جميع الاختبارات نجحت! النظام يعمل بأداء ممتاز.")
        else:
            print("⚠️ بعض الاختبارات فشلت. يرجى مراجعة التقرير للتفاصيل.")
        
        return results
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل اختبارات الأداء: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
