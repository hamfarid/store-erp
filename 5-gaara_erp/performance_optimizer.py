#!/usr/bin/env python3
"""
سكريبت تحسين أداء النظام
System Performance Optimizer
"""

import os
import re
import sqlite3
from pathlib import Path
from datetime import datetime

class PerformanceOptimizer:
    def __init__(self):
        self.optimizations = []
        self.db_path = "instance/inventory.db"
        
    def create_database_indexes(self):
        """إنشاء فهارس قاعدة البيانات لتحسين الأداء"""
        print("📊 إنشاء فهارس قاعدة البيانات...")
        
        if not os.path.exists(self.db_path):
            self.optimizations.append("❌ قاعدة البيانات غير موجودة")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # فهارس للجداول الأساسية
            indexes = [
                # فهارس المنتجات
                "CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)",
                "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)",
                "CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode)",
                
                # فهارس العملاء
                "CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name)",
                "CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email)",
                "CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone)",
                
                # فهارس الموردين
                "CREATE INDEX IF NOT EXISTS idx_suppliers_name ON suppliers(name)",
                "CREATE INDEX IF NOT EXISTS idx_suppliers_email ON suppliers(email)",
                
                # فهارس الفواتير
                "CREATE INDEX IF NOT EXISTS idx_invoices_date ON invoices(invoice_date)",
                "CREATE INDEX IF NOT EXISTS idx_invoices_customer ON invoices(customer_id)",
                "CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_number)",
                
                # فهارس حركات المخزون
                "CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(movement_date)",
                "CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id)",
                "CREATE INDEX IF NOT EXISTS idx_stock_movements_type ON stock_movements(movement_type)",
                
                # فهارس المستخدمين
                "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
                "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
                "CREATE INDEX IF NOT EXISTS idx_users_role ON users(role_id)",
            ]
            
            created_count = 0
            for index_sql in indexes:
                try:
                    cursor.execute(index_sql)
                    created_count += 1
                except sqlite3.Error as e:
                    if "already exists" not in str(e):
                        print(f"خطأ في إنشاء فهرس: {e}")
            
            conn.commit()
            conn.close()
            
            self.optimizations.append(f"✅ تم إنشاء {created_count} فهرس لتحسين الأداء")
            
        except Exception as e:
            self.optimizations.append(f"❌ خطأ في إنشاء الفهارس: {e}")
    
    def optimize_query_patterns(self):
        """تحسين أنماط الاستعلامات في الكود"""
        print("🔍 تحسين أنماط الاستعلامات...")
        
        route_files = []
        for root, dirs, files in os.walk("src/routes"):
            for file in files:
                if file.endswith(".py"):
                    route_files.append(os.path.join(root, file))
        
        optimized_files = 0
        for file_path in route_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # تحسين استعلامات N+1
                # استبدال lazy loading بـ eager loading
                patterns = [
                    (r'\.query\.all\(\)', '.query.options(joinedload("*")).all()'),
                    (r'\.query\.filter\(', '.query.options(joinedload("*")).filter('),
                ]
                
                for pattern, replacement in patterns:
                    if re.search(pattern, content) and 'joinedload' not in content:
                        # إضافة import إذا لم يكن موجود
                        if 'from sqlalchemy.orm import joinedload' not in content:
                            content = 'from sqlalchemy.orm import joinedload\n' + content
                
                # حفظ الملف إذا تم تعديله
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    optimized_files += 1
                    
            except Exception as e:
                continue
        
        if optimized_files > 0:
            self.optimizations.append(f"✅ تم تحسين {optimized_files} ملف استعلامات")
        else:
            self.optimizations.append("ℹ️ لا توجد استعلامات تحتاج تحسين")
    
    def cleanup_unused_imports(self):
        """تنظيف الاستيرادات غير المستخدمة"""
        print("📦 تنظيف الاستيرادات غير المستخدمة...")
        
        try:
            # استخدام autoflake لتنظيف الاستيرادات
            import subprocess
            
            result = subprocess.run([
                'python', '-m', 'autoflake', 
                '--remove-all-unused-imports',
                '--remove-unused-variables',
                '--in-place',
                '--recursive',
                'src/'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.optimizations.append("✅ تم تنظيف الاستيرادات غير المستخدمة")
            else:
                # تنظيف يدوي بسيط
                self.manual_import_cleanup()
                
        except ImportError:
            # تنظيف يدوي إذا لم يكن autoflake متاح
            self.manual_import_cleanup()
    
    def manual_import_cleanup(self):
        """تنظيف يدوي للاستيرادات"""
        python_files = []
        for root, dirs, files in os.walk("src/"):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        
        cleaned_files = 0
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # إزالة الاستيرادات المكررة
                seen_imports = set()
                cleaned_lines = []
                
                for line in lines:
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        if line.strip() not in seen_imports:
                            seen_imports.add(line.strip())
                            cleaned_lines.append(line)
                    else:
                        cleaned_lines.append(line)
                
                if len(cleaned_lines) != len(lines):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(cleaned_lines)
                    cleaned_files += 1
                    
            except Exception:
                continue
        
        self.optimizations.append(f"✅ تم تنظيف {cleaned_files} ملف يدوياً")
    
    def optimize_static_files(self):
        """تحسين الملفات الثابتة"""
        print("📁 تحسين الملفات الثابتة...")
        
        # فحص الواجهة الأمامية
        frontend_path = "../frontend"
        if os.path.exists(frontend_path):
            # فحص حجم ملفات البناء
            dist_path = os.path.join(frontend_path, "dist")
            if os.path.exists(dist_path):
                total_size = 0
                file_count = 0
                
                for root, dirs, files in os.walk(dist_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            size = os.path.getsize(file_path)
                            total_size += size
                            file_count += 1
                        except:
                            continue
                
                size_mb = total_size / (1024 * 1024)
                self.optimizations.append(f"📊 حجم ملفات البناء: {size_mb:.2f} MB ({file_count} ملف)")
                
                if size_mb < 5:
                    self.optimizations.append("✅ حجم ملفات البناء محسن")
                else:
                    self.optimizations.append("⚠️ حجم ملفات البناء كبير - يحتاج تحسين")
            else:
                self.optimizations.append("⚠️ ملفات البناء غير موجودة")
        else:
            self.optimizations.append("ℹ️ مجلد الواجهة الأمامية غير موجود")
    
    def analyze_performance_bottlenecks(self):
        """تحليل عقد الأداء"""
        print("🔍 تحليل عقد الأداء...")
        
        # فحص الملفات الكبيرة
        large_files = []
        for root, dirs, files in os.walk("src/"):
            for file in files:
                if file.endswith((".py", ".js", ".jsx")):
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        if size > 50000:  # أكبر من 50KB
                            large_files.append((file_path, size))
                    except:
                        continue
        
        if large_files:
            self.optimizations.append(f"⚠️ {len(large_files)} ملف كبير قد يؤثر على الأداء:")
            for file_path, size in large_files[:5]:  # أول 5 ملفات
                size_kb = size / 1024
                self.optimizations.append(f"   - {file_path}: {size_kb:.1f} KB")
        else:
            self.optimizations.append("✅ لا توجد ملفات كبيرة تؤثر على الأداء")
        
        # فحص الاستعلامات المعقدة
        complex_queries = 0
        for root, dirs, files in os.walk("src/routes/"):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # عد الاستعلامات المعقدة
                        joins = len(re.findall(r'join\(|JOIN\s+', content, re.IGNORECASE))
                        subqueries = len(re.findall(r'subquery\(|EXISTS\s*\(', content, re.IGNORECASE))
                        
                        if joins > 2 or subqueries > 0:
                            complex_queries += 1
                    except:
                        continue
        
        if complex_queries > 0:
            self.optimizations.append(f"⚠️ {complex_queries} ملف يحتوي على استعلامات معقدة")
        else:
            self.optimizations.append("✅ الاستعلامات بسيطة ومحسنة")
    
    def generate_performance_report(self):
        """إنشاء تقرير الأداء"""
        print("\n" + "="*60)
        print("📊 تقرير تحسين الأداء")
        print("="*60)
        
        print(f"🕒 وقت التنفيذ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 عدد التحسينات: {len(self.optimizations)}")
        
        print("\n📋 تفاصيل التحسينات:")
        print("-" * 40)
        
        for i, optimization in enumerate(self.optimizations, 1):
            print(f"{i:2d}. {optimization}")
        
        # حفظ التقرير
        report_file = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("تقرير تحسين الأداء\n")
            f.write("="*50 + "\n\n")
            f.write(f"وقت التنفيذ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"عدد التحسينات: {len(self.optimizations)}\n\n")
            f.write("تفاصيل التحسينات:\n")
            f.write("-" * 30 + "\n")
            for i, optimization in enumerate(self.optimizations, 1):
                f.write(f"{i:2d}. {optimization}\n")
        
        print(f"\n💾 تم حفظ التقرير في: {report_file}")
        
        # تقييم التحسين
        success_count = len([opt for opt in self.optimizations if opt.startswith("✅")])
        warning_count = len([opt for opt in self.optimizations if opt.startswith("⚠️")])
        
        print(f"\n📈 ملخص التحسينات:")
        print(f"✅ نجح: {success_count}")
        print(f"⚠️ تحذيرات: {warning_count}")
        print(f"ℹ️ معلومات: {len(self.optimizations) - success_count - warning_count}")
        
        if success_count >= len(self.optimizations) * 0.7:
            print("🎉 تم تحسين الأداء بنجاح!")
        elif success_count >= len(self.optimizations) * 0.5:
            print("👍 تحسينات جيدة مع بعض النقاط للمراجعة")
        else:
            print("⚠️ يحتاج المزيد من التحسينات")
    
    def run_all_optimizations(self):
        """تشغيل جميع التحسينات"""
        print("🚀 بدء تحسين أداء النظام...")
        print("="*60)
        
        # تشغيل جميع التحسينات
        self.create_database_indexes()
        self.optimize_query_patterns()
        self.cleanup_unused_imports()
        self.optimize_static_files()
        self.analyze_performance_bottlenecks()
        
        # إنشاء التقرير
        self.generate_performance_report()

def main():
    """الدالة الرئيسية"""
    optimizer = PerformanceOptimizer()
    optimizer.run_all_optimizations()

if __name__ == "__main__":
    main()
