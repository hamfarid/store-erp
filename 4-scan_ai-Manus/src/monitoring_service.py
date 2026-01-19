# File: /home/ubuntu/clean_project/src/monitoring_service.py
"""
مسار الملف: /home/ubuntu/clean_project/src/monitoring_service.py

خدمة مراقبة النظام والأداء
تتضمن مراقبة الخادم، قاعدة البيانات، والذاكرة
"""

import psutil
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass
import json
import os

@dataclass
class SystemMetrics:
    """مقاييس النظام"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, int]
    process_count: int
    uptime: float

@dataclass
class DatabaseMetrics:
    """مقاييس قاعدة البيانات"""
    timestamp: datetime
    connection_count: int
    query_count: int
    avg_query_time: float
    database_size: int
    table_count: int

@dataclass
class ApplicationMetrics:
    """مقاييس التطبيق"""
    timestamp: datetime
    active_users: int
    total_requests: int
    avg_response_time: float
    error_count: int
    diagnosis_count: int

class MonitoringService:
    """خدمة مراقبة النظام"""
    
    def __init__(self, log_file: str = "monitoring.log"):
        self.log_file = log_file
        self.setup_logging()
        self.metrics_history: List[SystemMetrics] = []
        self.db_metrics_history: List[DatabaseMetrics] = []
        self.app_metrics_history: List[ApplicationMetrics] = []
        self.alerts_config = self.load_alerts_config()
        
    def setup_logging(self):
        """إعداد نظام السجلات"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def load_alerts_config(self) -> Dict[str, Any]:
        """تحميل إعدادات التنبيهات"""
        default_config = {
            "cpu_threshold": 80.0,
            "memory_threshold": 85.0,
            "disk_threshold": 90.0,
            "response_time_threshold": 2.0,
            "error_rate_threshold": 5.0
        }
        
        config_file = "monitoring_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"فشل في تحميل إعدادات المراقبة: {e}")
        
        return default_config
    
    def collect_system_metrics(self) -> SystemMetrics:
        """جمع مقاييس النظام"""
        try:
            # معلومات المعالج
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # معلومات الذاكرة
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # معلومات القرص
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # معلومات الشبكة
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            # عدد العمليات
            process_count = len(psutil.pids())
            
            # وقت التشغيل
            uptime = time.time() - psutil.boot_time()
            
            metrics = SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                network_io=network_io,
                process_count=process_count,
                uptime=uptime
            )
            
            self.metrics_history.append(metrics)
            self.check_system_alerts(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"خطأ في جمع مقاييس النظام: {e}")
            raise
    
    def collect_database_metrics(self) -> DatabaseMetrics:
        """جمع مقاييس قاعدة البيانات"""
        try:
            # محاكاة مقاييس قاعدة البيانات (يمكن ربطها بقاعدة بيانات حقيقية)
            metrics = DatabaseMetrics(
                timestamp=datetime.now(),
                connection_count=self.get_db_connection_count(),
                query_count=self.get_db_query_count(),
                avg_query_time=self.get_avg_query_time(),
                database_size=self.get_database_size(),
                table_count=self.get_table_count()
            )
            
            self.db_metrics_history.append(metrics)
            return metrics
            
        except Exception as e:
            self.logger.error(f"خطأ في جمع مقاييس قاعدة البيانات: {e}")
            raise
    
    def collect_application_metrics(self) -> ApplicationMetrics:
        """جمع مقاييس التطبيق"""
        try:
            metrics = ApplicationMetrics(
                timestamp=datetime.now(),
                active_users=self.get_active_users_count(),
                total_requests=self.get_total_requests(),
                avg_response_time=self.get_avg_response_time(),
                error_count=self.get_error_count(),
                diagnosis_count=self.get_diagnosis_count()
            )
            
            self.app_metrics_history.append(metrics)
            self.check_application_alerts(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"خطأ في جمع مقاييس التطبيق: {e}")
            raise
    
    def check_system_alerts(self, metrics: SystemMetrics):
        """فحص تنبيهات النظام"""
        alerts = []
        
        if metrics.cpu_percent > self.alerts_config["cpu_threshold"]:
            alerts.append(f"استخدام المعالج عالي: {metrics.cpu_percent:.1f}%")
        
        if metrics.memory_percent > self.alerts_config["memory_threshold"]:
            alerts.append(f"استخدام الذاكرة عالي: {metrics.memory_percent:.1f}%")
        
        if metrics.disk_percent > self.alerts_config["disk_threshold"]:
            alerts.append(f"مساحة القرص منخفضة: {metrics.disk_percent:.1f}%")
        
        for alert in alerts:
            self.logger.warning(f"تنبيه النظام: {alert}")
            self.send_alert(alert, "system")
    
    def check_application_alerts(self, metrics: ApplicationMetrics):
        """فحص تنبيهات التطبيق"""
        alerts = []
        
        if metrics.avg_response_time > self.alerts_config["response_time_threshold"]:
            alerts.append(f"وقت الاستجابة بطيء: {metrics.avg_response_time:.2f}s")
        
        # حساب معدل الأخطاء
        if metrics.total_requests > 0:
            error_rate = (metrics.error_count / metrics.total_requests) * 100
            if error_rate > self.alerts_config["error_rate_threshold"]:
                alerts.append(f"معدل الأخطاء عالي: {error_rate:.1f}%")
        
        for alert in alerts:
            self.logger.warning(f"تنبيه التطبيق: {alert}")
            self.send_alert(alert, "application")
    
    def send_alert(self, message: str, alert_type: str):
        """إرسال تنبيه"""
        # يمكن تطوير هذه الدالة لإرسال تنبيهات عبر البريد الإلكتروني أو Slack
        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "message": message,
            "severity": "warning"
        }
        
        # حفظ التنبيه في ملف
        alerts_file = "alerts.json"
        try:
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r', encoding='utf-8') as f:
                    alerts = json.load(f)
            else:
                alerts = []
            
            alerts.append(alert_data)
            
            # الاحتفاظ بآخر 100 تنبيه فقط
            if len(alerts) > 100:
                alerts = alerts[-100:]
            
            with open(alerts_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"فشل في حفظ التنبيه: {e}")
    
    def get_system_health_score(self) -> float:
        """حساب نقاط صحة النظام"""
        if not self.metrics_history:
            return 0.0
        
        latest_metrics = self.metrics_history[-1]
        
        # حساب النقاط بناءً على المقاييس
        cpu_score = max(0, 100 - latest_metrics.cpu_percent)
        memory_score = max(0, 100 - latest_metrics.memory_percent)
        disk_score = max(0, 100 - latest_metrics.disk_percent)
        
        # متوسط النقاط
        health_score = (cpu_score + memory_score + disk_score) / 3
        return min(100, max(0, health_score))
    
    def get_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """إنشاء تقرير الأداء"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # تصفية المقاييس حسب الوقت
        recent_metrics = [m for m in self.metrics_history if m.timestamp > cutoff_time]
        recent_app_metrics = [m for m in self.app_metrics_history if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {"error": "لا توجد بيانات كافية"}
        
        # حساب الإحصائيات
        avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        avg_disk = sum(m.disk_percent for m in recent_metrics) / len(recent_metrics)
        
        max_cpu = max(m.cpu_percent for m in recent_metrics)
        max_memory = max(m.memory_percent for m in recent_metrics)
        
        report = {
            "period": f"آخر {hours} ساعة",
            "system_metrics": {
                "avg_cpu_percent": round(avg_cpu, 2),
                "avg_memory_percent": round(avg_memory, 2),
                "avg_disk_percent": round(avg_disk, 2),
                "max_cpu_percent": round(max_cpu, 2),
                "max_memory_percent": round(max_memory, 2)
            },
            "health_score": round(self.get_system_health_score(), 2),
            "data_points": len(recent_metrics)
        }
        
        if recent_app_metrics:
            total_requests = sum(m.total_requests for m in recent_app_metrics)
            total_errors = sum(m.error_count for m in recent_app_metrics)
            avg_response_time = sum(m.avg_response_time for m in recent_app_metrics) / len(recent_app_metrics)
            
            report["application_metrics"] = {
                "total_requests": total_requests,
                "total_errors": total_errors,
                "error_rate": round((total_errors / max(total_requests, 1)) * 100, 2),
                "avg_response_time": round(avg_response_time, 3)
            }
        
        return report
    
    def cleanup_old_data(self, days: int = 7):
        """تنظيف البيانات القديمة"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        self.metrics_history = [m for m in self.metrics_history if m.timestamp > cutoff_time]
        self.db_metrics_history = [m for m in self.db_metrics_history if m.timestamp > cutoff_time]
        self.app_metrics_history = [m for m in self.app_metrics_history if m.timestamp > cutoff_time]
        
        self.logger.info(f"تم تنظيف البيانات الأقدم من {days} أيام")
    
    # دوال مساعدة لجمع البيانات (يمكن ربطها بالنظام الفعلي)
    def get_db_connection_count(self) -> int:
        """الحصول على عدد اتصالات قاعدة البيانات"""
        # محاكاة - يمكن ربطها بقاعدة البيانات الفعلية
        return 5
    
    def get_db_query_count(self) -> int:
        """الحصول على عدد استعلامات قاعدة البيانات"""
        return 150
    
    def get_avg_query_time(self) -> float:
        """الحصول على متوسط وقت الاستعلام"""
        return 0.05
    
    def get_database_size(self) -> int:
        """الحصول على حجم قاعدة البيانات بالبايت"""
        return 1024 * 1024 * 50  # 50 MB
    
    def get_table_count(self) -> int:
        """الحصول على عدد الجداول"""
        return 8
    
    def get_active_users_count(self) -> int:
        """الحصول على عدد المستخدمين النشطين"""
        return 12
    
    def get_total_requests(self) -> int:
        """الحصول على إجمالي الطلبات"""
        return 1500
    
    def get_avg_response_time(self) -> float:
        """الحصول على متوسط وقت الاستجابة"""
        return 0.25
    
    def get_error_count(self) -> int:
        """الحصول على عدد الأخطاء"""
        return 5
    
    def get_diagnosis_count(self) -> int:
        """الحصول على عدد التشخيصات"""
        return 45

# مثيل عام للخدمة
monitoring_service = MonitoringService()

def start_monitoring(interval: int = 60):
    """بدء مراقبة النظام"""
    import threading
    import time
    
    def monitor_loop():
        while True:
            try:
                monitoring_service.collect_system_metrics()
                monitoring_service.collect_database_metrics()
                monitoring_service.collect_application_metrics()
                
                # تنظيف البيانات القديمة كل 24 ساعة
                if len(monitoring_service.metrics_history) % 1440 == 0:  # 24 * 60
                    monitoring_service.cleanup_old_data()
                
            except Exception as e:
                monitoring_service.logger.error(f"خطأ في حلقة المراقبة: {e}")
            
            time.sleep(interval)
    
    # تشغيل المراقبة في خيط منفصل
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    
    monitoring_service.logger.info("تم بدء خدمة المراقبة")
    return monitor_thread

if __name__ == "__main__":
    # اختبار الخدمة
    print("بدء اختبار خدمة المراقبة...")
    
    # جمع المقاييس
    system_metrics = monitoring_service.collect_system_metrics()
    print(f"مقاييس النظام: CPU {system_metrics.cpu_percent}%, Memory {system_metrics.memory_percent}%")
    
    # إنشاء تقرير
    report = monitoring_service.get_performance_report(1)
    print(f"تقرير الأداء: {json.dumps(report, ensure_ascii=False, indent=2)}")
    
    print("انتهى اختبار خدمة المراقبة")

