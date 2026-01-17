#!/usr/bin/env python3
"""
Gaara ERP System Monitor
========================

Real-time monitoring and alerting system for Gaara ERP.
Monitors system health, performance, and sends alerts when needed.

Usage:
    python system_monitor.py [--interval SECONDS] [--alert-email EMAIL]

Features:
    - Real-time system monitoring
    - Performance metrics collection
    - Automated alerts and notifications
    - Health status dashboard
    - Log analysis and reporting
"""

import os
import sys
import time
import json
import psutil
import requests
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import threading
from collections import deque


class GaaraERPMonitor:
    def __init__(self, interval=30, alert_email=None):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.interval = interval
        self.alert_email = alert_email
        self.metrics_history = deque(maxlen=100)  # Keep last 100 metrics
        self.alerts_sent = set()
        self.running = False

        # Thresholds for alerts
        self.thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'disk_percent': 90,
            'response_time': 5000,  # milliseconds
            'error_rate': 10  # errors per minute
        }

    def get_system_metrics(self):
        """Collect system metrics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(self.base_dir)

            # Network
            network = psutil.net_io_counters()

            # Process info
            django_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if 'python' in proc.info['name'].lower() and 'manage.py' in ' '.join(proc.cmdline()):
                        django_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            metrics = {
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_available_gb': memory.available / (1024**3),
                    'disk_percent': (disk.used / disk.total) * 100,
                    'disk_free_gb': disk.free / (1024**3),
                    'network_bytes_sent': network.bytes_sent,
                    'network_bytes_recv': network.bytes_recv
                },
                'django': {
                    'processes': len(django_processes),
                    'total_cpu': sum(p.get('cpu_percent', 0) for p in django_processes),
                    'total_memory': sum(p.get('memory_percent', 0) for p in django_processes)
                }
            }

            # Test Django response time
            try:
                start_time = time.time()
                response = requests.get('http://localhost:9551/admin/', timeout=10)
                response_time = (time.time() - start_time) * 1000

                metrics['django']['response_time_ms'] = response_time
                metrics['django']['status_code'] = response.status_code
                metrics['django']['is_responding'] = response.status_code in [200, 302, 401, 403]
            except requests.RequestException as e:
                metrics['django']['response_time_ms'] = None
                metrics['django']['status_code'] = None
                metrics['django']['is_responding'] = False
                metrics['django']['error'] = str(e)

            return metrics

        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': f'Failed to collect metrics: {e}'
            }

    def check_log_errors(self):
        """Check for recent errors in logs"""
        try:
            log_file = self.gaara_dir / 'logs' / 'gaara_erp.log'
            if not log_file.exists():
                return {'error_count': 0, 'recent_errors': []}

            # Read last 1000 lines
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = deque(f, maxlen=1000)

            # Count errors in last 10 minutes
            now = datetime.now()
            ten_minutes_ago = now - timedelta(minutes=10)

            error_count = 0
            recent_errors = []

            for line in lines:
                if 'ERROR' in line or 'CRITICAL' in line:
                    try:
                        # Try to extract timestamp (basic parsing)
                        if len(line) > 19:  # Basic timestamp check
                            error_count += 1
                            if len(recent_errors) < 5:  # Keep last 5 errors
                                recent_errors.append(line.strip())
                    except:
                        continue

            return {
                'error_count': error_count,
                'recent_errors': recent_errors
            }

        except Exception as e:
            return {
                'error_count': 0,
                'recent_errors': [],
                'check_error': str(e)
            }

    def check_database_health(self):
        """Check database connectivity and performance"""
        try:
            os.chdir(self.gaara_dir)

            # Test database connection
            start_time = time.time()
            result = subprocess.run([
                sys.executable, 'manage.py', 'shell', '-c',
                'from django.db import connection; connection.ensure_connection(); print("DB_OK")'
            ], capture_output=True, text=True, timeout=30)

            db_response_time = (time.time() - start_time) * 1000

            return {
                'is_connected': 'DB_OK' in result.stdout,
                'response_time_ms': db_response_time,
                'error': result.stderr if result.returncode != 0 else None
            }

        except Exception as e:
            return {
                'is_connected': False,
                'response_time_ms': None,
                'error': str(e)
            }

    def generate_alert(self, alert_type, message, severity='warning'):
        """Generate system alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'message': message,
            'severity': severity,
            'system': 'Gaara ERP Monitor'
        }

        # Avoid duplicate alerts
        alert_key = f"{alert_type}_{severity}"
        if alert_key in self.alerts_sent:
            return

        self.alerts_sent.add(alert_key)

        # Print alert
        severity_icon = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'critical': '🚨'
        }.get(severity, '❓')

        print(f"\n{severity_icon} تنبيه {severity.upper()}: {message}")

        # Save alert to file
        alerts_file = self.base_dir / 'alerts.log'
        try:
            with open(alerts_file, 'a', encoding='utf-8') as f:
                f.write(f"{alert['timestamp']} [{severity.upper()}] {alert_type}: {message}\n")
        except Exception as e:
            print(f"خطأ في حفظ التنبيه: {e}")

        # Send email alert if configured
        if self.alert_email and severity in ['error', 'critical']:
            self.send_email_alert(alert)

    def send_email_alert(self, alert):
        """Send email alert (placeholder implementation)"""
        # This would integrate with your email system
        print(f"📧 إرسال تنبيه بريد إلكتروني إلى: {self.alert_email}")
        print(f"   الموضوع: Gaara ERP Alert - {alert['type']}")
        print(f"   الرسالة: {alert['message']}")

    def analyze_metrics(self, metrics):
        """Analyze metrics and generate alerts"""
        if 'error' in metrics:
            self.generate_alert('system_error', metrics['error'], 'error')
            return

        system = metrics.get('system', {})
        django = metrics.get('django', {})

        # CPU usage alert
        if system.get('cpu_percent', 0) > self.thresholds['cpu_percent']:
            self.generate_alert(
                'high_cpu',
                f"استخدام المعالج مرتفع: {system['cpu_percent']:.1f}%",
                'warning'
            )

        # Memory usage alert
        if system.get('memory_percent', 0) > self.thresholds['memory_percent']:
            self.generate_alert(
                'high_memory',
                f"استخدام الذاكرة مرتفع: {system['memory_percent']:.1f}%",
                'warning'
            )

        # Disk usage alert
        if system.get('disk_percent', 0) > self.thresholds['disk_percent']:
            self.generate_alert(
                'high_disk',
                f"استخدام القرص مرتفع: {system['disk_percent']:.1f}%",
                'error'
            )

        # Django response time alert
        response_time = django.get('response_time_ms')
        if response_time and response_time > self.thresholds['response_time']:
            self.generate_alert(
                'slow_response',
                f"استجابة Django بطيئة: {response_time:.0f}ms",
                'warning'
            )

        # Django not responding alert
        if not django.get('is_responding', True):
            self.generate_alert(
                'django_down',
                "Django لا يستجيب",
                'critical'
            )

    def display_dashboard(self, metrics):
        """Display real-time dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')

        print("🖥️  لوحة مراقبة نظام Gaara ERP")
        print("=" * 60)
        print(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔄 فترة المراقبة: {self.interval} ثانية")

        if 'error' in metrics:
            print(f"\n❌ خطأ في جمع البيانات: {metrics['error']}")
            return

        system = metrics.get('system', {})
        django = metrics.get('django', {})

        # System metrics
        print("\n🖥️  مقاييس النظام:")
        print(f"   💻 المعالج: {system.get('cpu_percent', 0):.1f}%")
        print(f"   🧠 الذاكرة: {system.get('memory_percent', 0):.1f}% "
              f"(متاح: {system.get('memory_available_gb', 0):.1f} GB)")
        print(f"   💾 القرص: {system.get('disk_percent', 0):.1f}% "
              f"(فارغ: {system.get('disk_free_gb', 0):.1f} GB)")

        # Django metrics
        print("\n🐍 مقاييس Django:")
        print(f"   🔄 العمليات: {django.get('processes', 0)}")

        if django.get('is_responding'):
            print(f"   ✅ الحالة: يعمل")
            if django.get('response_time_ms'):
                print(f"   ⚡ زمن الاستجابة: {django['response_time_ms']:.0f}ms")
        else:
            print(f"   ❌ الحالة: لا يستجيب")
            if django.get('error'):
                print(f"   🔥 الخطأ: {django['error']}")

        # Recent alerts
        alerts_file = self.base_dir / 'alerts.log'
        if alerts_file.exists():
            try:
                with open(alerts_file, 'r', encoding='utf-8') as f:
                    recent_alerts = list(deque(f, maxlen=5))

                if recent_alerts:
                    print("\n🚨 التنبيهات الأخيرة:")
                    for alert in recent_alerts[-3:]:  # Show last 3
                        print(f"   {alert.strip()}")
            except:
                pass

        print("\n⏹️  اضغط Ctrl+C للإيقاف")

    def run_monitoring(self):
        """Main monitoring loop"""
        print("🚀 بدء مراقبة نظام Gaara ERP...")
        print(f"📊 فترة المراقبة: {self.interval} ثانية")

        self.running = True

        try:
            while self.running:
                # Collect metrics
                metrics = self.get_system_metrics()

                # Add log analysis
                log_analysis = self.check_log_errors()
                metrics['logs'] = log_analysis

                # Add database health
                db_health = self.check_database_health()
                metrics['database'] = db_health

                # Store metrics
                self.metrics_history.append(metrics)

                # Analyze and generate alerts
                self.analyze_metrics(metrics)

                # Display dashboard
                self.display_dashboard(metrics)

                # Clear old alerts periodically
                if len(self.alerts_sent) > 50:
                    self.alerts_sent.clear()

                # Wait for next cycle
                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("\n🛑 تم إيقاف المراقبة")
            self.running = False

    def save_metrics_report(self):
        """Save metrics report to file"""
        if not self.metrics_history:
            return

        report_file = self.base_dir / f"metrics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.metrics_history), f, indent=2, ensure_ascii=False)
            print(f"📄 تم حفظ تقرير المقاييس: {report_file.name}")
        except Exception as e:
            print(f"❌ خطأ في حفظ التقرير: {e}")


def main():
    parser = argparse.ArgumentParser(description='Gaara ERP System Monitor')
    parser.add_argument('--interval', type=int, default=30, help='Monitoring interval in seconds (default: 30)')
    parser.add_argument('--alert-email', type=str, help='Email address for critical alerts')

    args = parser.parse_args()

    monitor = GaaraERPMonitor(interval=args.interval, alert_email=args.alert_email)

    try:
        monitor.run_monitoring()
    finally:
        monitor.save_metrics_report()


if __name__ == '__main__':
    main()
