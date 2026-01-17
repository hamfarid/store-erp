"""
نظام المراقبة المتقدم
Advanced Monitoring System
"""

import time
import psutil
import threading
from datetime import datetime, timedelta
from collections import defaultdict, deque


class SystemMonitor:
    """نظام مراقبة الأداء المتقدم"""

    def __init__(self):
        self.metrics = defaultdict(deque)
        self.alerts = []
        self.is_monitoring = False
        self.monitor_thread = None

    def start_monitoring(self):
        """بدء المراقبة"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()

    def stop_monitoring(self):
        """إيقاف المراقبة"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()

    def _monitor_loop(self):
        """حلقة المراقبة الرئيسية"""
        while self.is_monitoring:
            try:
                # جمع المقاييس
                self._collect_system_metrics()
                self._check_alerts()
                time.sleep(30)  # مراقبة كل 30 ثانية
            except Exception as e:
                print(f"خطأ في المراقبة: {e}")
                time.sleep(60)

    def _collect_system_metrics(self):
        """جمع مقاييس النظام"""
        timestamp = datetime.now()

        # مقاييس المعالج
        cpu_percent = psutil.cpu_percent(interval=1)
        self.metrics["cpu"].append((timestamp, cpu_percent))

        # مقاييس الذاكرة
        memory = psutil.virtual_memory()
        self.metrics["memory_percent"].append((timestamp, memory.percent))
        self.metrics["memory_used"].append((timestamp, memory.used))

        # مقاييس القرص
        disk = psutil.disk_usage("/")
        self.metrics["disk_percent"].append((timestamp, disk.percent))

        # مقاييس الشبكة
        network = psutil.net_io_counters()
        self.metrics["network_sent"].append((timestamp, network.bytes_sent))
        self.metrics["network_recv"].append((timestamp, network.bytes_recv))

        # الحفاظ على آخر 100 قراءة فقط
        for metric_name in self.metrics:
            if len(self.metrics[metric_name]) > 100:
                self.metrics[metric_name].popleft()

    def _check_alerts(self):
        """فحص التنبيهات"""
        current_time = datetime.now()

        # تنبيه استخدام المعالج العالي
        if self.metrics["cpu"] and self.metrics["cpu"][-1][1] > 80:
            self.alerts.append(
                {
                    "type": "HIGH_CPU",
                    "message": f'استخدام المعالج عالي: {self.metrics["cpu"][-1][1]:.1f}%',
                    "timestamp": current_time,
                    "severity": "warning",
                }
            )

        # تنبيه استخدام الذاكرة العالي
        if (
            self.metrics["memory_percent"]
            and self.metrics["memory_percent"][-1][1] > 85
        ):
            self.alerts.append(
                {
                    "type": "HIGH_MEMORY",
                    "message": f'استخدام الذاكرة عالي: {self.metrics["memory_percent"][-1][1]:.1f}%',
                    "timestamp": current_time,
                    "severity": "warning",
                }
            )

        # تنبيه مساحة القرص المنخفضة
        if self.metrics["disk_percent"] and self.metrics["disk_percent"][-1][1] > 90:
            self.alerts.append(
                {
                    "type": "LOW_DISK_SPACE",
                    "message": f'مساحة القرص منخفضة: {self.metrics["disk_percent"][-1][1]:.1f}%',
                    "timestamp": current_time,
                    "severity": "critical",
                }
            )

        # الحفاظ على آخر 50 تنبيه
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-50:]

    def get_current_status(self):
        """الحصول على حالة النظام الحالية"""
        if not self.metrics["cpu"]:
            return {"status": "no_data", "message": "لا توجد بيانات مراقبة"}

        latest_cpu = self.metrics["cpu"][-1][1] if self.metrics["cpu"] else 0
        latest_memory = (
            self.metrics["memory_percent"][-1][1]
            if self.metrics["memory_percent"]
            else 0
        )
        latest_disk = (
            self.metrics["disk_percent"][-1][1] if self.metrics["disk_percent"] else 0
        )

        # تحديد حالة النظام
        if latest_cpu > 80 or latest_memory > 85 or latest_disk > 90:
            status = "critical"
        elif latest_cpu > 60 or latest_memory > 70 or latest_disk > 80:
            status = "warning"
        else:
            status = "healthy"

        return {
            "status": status,
            "cpu_percent": latest_cpu,
            "memory_percent": latest_memory,
            "disk_percent": latest_disk,
            "active_alerts": len(
                [
                    a
                    for a in self.alerts
                    if (datetime.now() - a["timestamp"]).seconds < 300
                ]
            ),
            "uptime": time.time() - psutil.boot_time(),
        }

    def get_performance_report(self):
        """تقرير الأداء المفصل"""
        if not self.metrics["cpu"]:
            return {"error": "لا توجد بيانات كافية"}

        # حساب المتوسطات
        cpu_avg = sum(m[1] for m in self.metrics["cpu"]) / len(self.metrics["cpu"])
        memory_avg = sum(m[1] for m in self.metrics["memory_percent"]) / len(
            self.metrics["memory_percent"]
        )

        # حساب الذروات
        cpu_max = max(m[1] for m in self.metrics["cpu"])
        memory_max = max(m[1] for m in self.metrics["memory_percent"])

        return {
            "period": f'آخر {len(self.metrics["cpu"])} قراءة',
            "cpu": {
                "average": cpu_avg,
                "maximum": cpu_max,
                "current": self.metrics["cpu"][-1][1],
            },
            "memory": {
                "average": memory_avg,
                "maximum": memory_max,
                "current": self.metrics["memory_percent"][-1][1],
            },
            "alerts_summary": {
                "total": len(self.alerts),
                "recent": len(
                    [
                        a
                        for a in self.alerts
                        if (datetime.now() - a["timestamp"]).seconds < 3600
                    ]
                ),
            },
        }


# إنشاء instance عام
system_monitor = SystemMonitor()

# بدء المراقبة تلقائياً
system_monitor.start_monitoring()
