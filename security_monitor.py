#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 مراقبة أمنية مستمرة
Continuous Security Monitoring
"""

import os
import json
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


class SecurityMonitor:
    """مراقب الأمان المستمر"""
    
    def __init__(self):
        self.db_path = "backend/instance/inventory.db"
        self.log_file = "logs/security_monitor.log"
        self.alerts = []
        
    def log_event(self, level, message):
        """تسجيل حدث أمني"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        # إنشاء مجلد السجلات إذا لم يكن موجوداً
        Path("logs").mkdir(exist_ok=True)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"{level}: {message}")
        
    def check_failed_logins(self):
        """فحص محاولات تسجيل الدخول الفاشلة"""
        try:
            if not Path(self.db_path).exists():
                return
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # فحص محاولات تسجيل الدخول في آخر ساعة
            one_hour_ago = datetime.now() - timedelta(hours=1)
            
            cursor.execute("""
                SELECT COUNT(*) FROM login_attempts 
                WHERE success = 0 AND timestamp > ?
            """, (one_hour_ago.isoformat(),))
            
            failed_count = cursor.fetchone()[0]
            
            if failed_count > 10:
                self.log_event("ALERT", f"عدد كبير من محاولات تسجيل الدخول الفاشلة: {failed_count}")
                self.alerts.append({
                    "type": "failed_logins",
                    "count": failed_count,
                    "timestamp": datetime.now().isoformat()
                })
                
            conn.close()
            
        except Exception as e:
            self.log_event("ERROR", f"خطأ في فحص محاولات تسجيل الدخول: {e}")
            
    def check_file_integrity(self):
        """فحص سلامة الملفات الحساسة"""
        sensitive_files = [
            "backend/.env",
            "backend/instance/inventory.db",
            "backend/src/security_middleware.py"
        ]
        
        for file_path in sensitive_files:
            if Path(file_path).exists():
                # فحص صلاحيات الملف
                stat = os.stat(file_path)
                permissions = oct(stat.st_mode)[-3:]
                
                if permissions != "600":
                    self.log_event("WARNING", f"صلاحيات غير آمنة للملف: {file_path} ({permissions})")
                    
                # فحص حجم الملف (للكشف عن التلاعب)
                size = stat.st_size
                if size == 0:
                    self.log_event("ALERT", f"ملف فارغ مشبوه: {file_path}")
                    
            else:
                self.log_event("ALERT", f"ملف حساس مفقود: {file_path}")
                
    def check_disk_space(self):
        """فحص مساحة القرص"""
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            
            free_percent = (free / total) * 100
            
            if free_percent < 10:
                self.log_event("ALERT", f"مساحة القرص منخفضة: {free_percent:.1f}%")
            elif free_percent < 20:
                self.log_event("WARNING", f"مساحة القرص تحتاج مراقبة: {free_percent:.1f}%")
                
        except Exception as e:
            self.log_event("ERROR", f"خطأ في فحص مساحة القرص: {e}")
            
    def check_process_health(self):
        """فحص صحة العمليات"""
        try:
            # فحص إذا كان الخادم يعمل
            import psutil
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if 'python' in proc.info['name'] and 'app.py' in ' '.join(proc.info['cmdline'] or []):
                    self.log_event("INFO", f"الخادم يعمل بشكل طبيعي: PID {proc.info['pid']}")
                    return
                    
            self.log_event("ALERT", "الخادم غير متاح!")
            
        except ImportError:
            self.log_event("INFO", "psutil غير متاح - تخطي فحص العمليات")
        except Exception as e:
            self.log_event("ERROR", f"خطأ في فحص العمليات: {e}")
            
    def generate_security_report(self):
        """توليد تقرير أمني"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "alerts": self.alerts,
            "status": "healthy" if not self.alerts else "needs_attention",
            "recommendations": []
        }
        
        if self.alerts:
            report["recommendations"] = [
                "مراجعة السجلات الأمنية فوراً",
                "التحقق من محاولات تسجيل الدخول المشبوهة",
                "فحص سلامة الملفات الحساسة",
                "التأكد من تحديث النظام"
            ]
            
        with open('security_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        return report
        
    def run_monitoring_cycle(self):
        """تشغيل دورة مراقبة واحدة"""
        self.log_event("INFO", "بدء دورة المراقبة الأمنية")
        
        self.check_failed_logins()
        self.check_file_integrity()
        self.check_disk_space()
        self.check_process_health()
        
        report = self.generate_security_report()
        
        self.log_event("INFO", f"انتهاء دورة المراقبة - الحالة: {report['status']}")
        
        return report
        
    def run_continuous_monitoring(self, interval=300):
        """تشغيل المراقبة المستمرة"""
        self.log_event("INFO", f"بدء المراقبة المستمرة - فترة: {interval} ثانية")
        
        try:
            while True:
                self.run_monitoring_cycle()
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log_event("INFO", "تم إيقاف المراقبة بواسطة المستخدم")
        except Exception as e:
            self.log_event("ERROR", f"خطأ في المراقبة المستمرة: {e}")


if __name__ == "__main__":
    import sys
    
    monitor = SecurityMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        # مراقبة مستمرة
        monitor.run_continuous_monitoring()
    else:
        # دورة واحدة فقط
        report = monitor.run_monitoring_cycle()
        print(f"\nتقرير الأمان: {report['status']}")
        if report['alerts']:
            print(f"عدد التنبيهات: {len(report['alerts'])}")
