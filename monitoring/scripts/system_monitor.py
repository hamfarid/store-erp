#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FILE: monitoring/scripts/system_monitor.py | PURPOSE: Custom System Monitoring Script | OWNER: DevOps | RELATED: prometheus.yml | LAST-AUDITED: 2025-10-21

"""
سكريبت مراقبة مخصص لنظام إدارة المخزون العربي
Custom System Monitoring Script for Arabic Inventory Management System

يقوم هذا السكريبت بمراقبة:
- صحة التطبيق والخدمات
- أداء قاعدة البيانات
- مستويات المخزون
- أمان النظام
- النسخ الاحتياطية
"""

import os
import sys
import time
import json
import logging
import psutil
import requests
import psycopg2
import redis
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/system_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class MonitoringConfig:
    """تكوين المراقبة"""
    db_host: str = os.getenv('DB_HOST', 'database')
    db_port: int = int(os.getenv('DB_PORT', '5432'))
    db_name: str = os.getenv('DB_NAME', 'store_production')
    db_user: str = os.getenv('DB_USER', 'store_user')
    db_password: str = os.getenv('DB_PASSWORD', '')
    
    redis_host: str = os.getenv('REDIS_HOST', 'redis')
    redis_port: int = int(os.getenv('REDIS_PORT', '6379'))
    redis_password: str = os.getenv('REDIS_PASSWORD', '')
    
    backend_url: str = os.getenv('BACKEND_URL', 'http://backend:5000')
    frontend_url: str = os.getenv('FRONTEND_URL', 'http://frontend:80')
    
    alert_email: str = os.getenv('ALERT_EMAIL_RECIPIENTS', 'admin@example.com')
    smtp_server: str = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port: int = int(os.getenv('MAIL_PORT', '587'))
    smtp_user: str = os.getenv('MAIL_USERNAME', '')
    smtp_password: str = os.getenv('MAIL_PASSWORD', '')

@dataclass
class HealthStatus:
    """حالة صحة الخدمة"""
    service: str
    status: str
    response_time: float
    details: Dict[str, Any]
    timestamp: datetime

class SystemMonitor:
    """مراقب النظام الرئيسي"""
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.alerts = []
        
    def check_system_resources(self) -> HealthStatus:
        """فحص موارد النظام"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            details = {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': (disk.used / disk.total) * 100,
                'disk_free_gb': disk.free / (1024**3),
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            }
            
            # تحديد الحالة
            status = 'healthy'
            if cpu_percent > 80 or memory.percent > 85 or (disk.used / disk.total) * 100 > 90:
                status = 'warning'
                self.alerts.append(f"موارد النظام عالية: CPU {cpu_percent}%, Memory {memory.percent}%, Disk {(disk.used / disk.total) * 100:.1f}%")
            
            if cpu_percent > 95 or memory.percent > 95 or (disk.used / disk.total) * 100 > 95:
                status = 'critical'
            
            return HealthStatus(
                service='system_resources',
                status=status,
                response_time=0.0,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"خطأ في فحص موارد النظام: {e}")
            return HealthStatus(
                service='system_resources',
                status='error',
                response_time=0.0,
                details={'error': str(e)},
                timestamp=datetime.now()
            )
    
    def check_database(self) -> HealthStatus:
        """فحص قاعدة البيانات"""
        start_time = time.time()
        try:
            conn = psycopg2.connect(
                host=self.config.db_host,
                port=self.config.db_port,
                database=self.config.db_name,
                user=self.config.db_user,
                password=self.config.db_password,
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            
            # فحص الاتصالات النشطة
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
            active_connections = cursor.fetchone()[0]
            
            # فحص حجم قاعدة البيانات
            cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
            db_size = cursor.fetchone()[0]
            
            # فحص الاستعلامات الطويلة
            cursor.execute("""
                SELECT count(*) FROM pg_stat_activity 
                WHERE state = 'active' AND query_start < now() - interval '5 minutes';
            """)
            long_queries = cursor.fetchone()[0]
            
            # فحص مستويات المخزون المنخفضة
            cursor.execute("""
                SELECT count(*) FROM products 
                WHERE current_stock <= minimum_stock AND minimum_stock > 0;
            """)
            low_stock_items = cursor.fetchone()[0]
            
            response_time = time.time() - start_time
            
            details = {
                'active_connections': active_connections,
                'database_size': db_size,
                'long_running_queries': long_queries,
                'low_stock_items': low_stock_items,
                'response_time_ms': response_time * 1000
            }
            
            # تحديد الحالة
            status = 'healthy'
            if active_connections > 80 or long_queries > 0 or response_time > 2:
                status = 'warning'
                if long_queries > 0:
                    self.alerts.append(f"يوجد {long_queries} استعلام طويل المدى في قاعدة البيانات")
            
            if active_connections > 95 or long_queries > 5 or response_time > 5:
                status = 'critical'
            
            # تنبيه المخزون المنخفض
            if low_stock_items > 0:
                self.alerts.append(f"تحذير: {low_stock_items} منتج لديه مخزون منخفض")
            
            cursor.close()
            conn.close()
            
            return HealthStatus(
                service='database',
                status=status,
                response_time=response_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"خطأ في فحص قاعدة البيانات: {e}")
            self.alerts.append(f"فشل الاتصال بقاعدة البيانات: {str(e)}")
            return HealthStatus(
                service='database',
                status='critical',
                response_time=time.time() - start_time,
                details={'error': str(e)},
                timestamp=datetime.now()
            )
    
    def check_redis(self) -> HealthStatus:
        """فحص Redis"""
        start_time = time.time()
        try:
            r = redis.Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                password=self.config.redis_password,
                socket_connect_timeout=10,
                socket_timeout=10
            )
            
            # فحص الاتصال
            r.ping()
            
            # معلومات Redis
            info = r.info()
            response_time = time.time() - start_time
            
            details = {
                'used_memory_mb': info['used_memory'] / (1024 * 1024),
                'used_memory_percent': (info['used_memory'] / info.get('maxmemory', info['used_memory'] * 2)) * 100,
                'connected_clients': info['connected_clients'],
                'total_commands_processed': info['total_commands_processed'],
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'response_time_ms': response_time * 1000
            }
            
            # حساب معدل نجاح Cache
            if details['keyspace_hits'] + details['keyspace_misses'] > 0:
                details['cache_hit_rate'] = details['keyspace_hits'] / (details['keyspace_hits'] + details['keyspace_misses']) * 100
            else:
                details['cache_hit_rate'] = 100
            
            # تحديد الحالة
            status = 'healthy'
            if details['used_memory_percent'] > 80 or details['connected_clients'] > 100:
                status = 'warning'
                self.alerts.append(f"استخدام Redis عالي: Memory {details['used_memory_percent']:.1f}%, Clients {details['connected_clients']}")
            
            if details['used_memory_percent'] > 95 or details['connected_clients'] > 200:
                status = 'critical'
            
            return HealthStatus(
                service='redis',
                status=status,
                response_time=response_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"خطأ في فحص Redis: {e}")
            self.alerts.append(f"فشل الاتصال بـ Redis: {str(e)}")
            return HealthStatus(
                service='redis',
                status='critical',
                response_time=time.time() - start_time,
                details={'error': str(e)},
                timestamp=datetime.now()
            )
    
    def check_backend_api(self) -> HealthStatus:
        """فحص API الواجهة الخلفية"""
        start_time = time.time()
        try:
            # فحص صحة API
            response = requests.get(
                f"{self.config.backend_url}/health",
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    health_data = response.json()
                except:
                    health_data = {'status': 'ok'}
                
                details = {
                    'status_code': response.status_code,
                    'response_time_ms': response_time * 1000,
                    'health_data': health_data
                }
                
                status = 'healthy' if response_time < 2 else 'warning'
                if response_time > 5:
                    status = 'critical'
                    self.alerts.append(f"API الواجهة الخلفية بطيء: {response_time:.2f} ثانية")
                
            else:
                status = 'warning'
                details = {
                    'status_code': response.status_code,
                    'response_time_ms': response_time * 1000,
                    'error': f"HTTP {response.status_code}"
                }
                self.alerts.append(f"API الواجهة الخلفية يعيد خطأ: HTTP {response.status_code}")
            
            return HealthStatus(
                service='backend_api',
                status=status,
                response_time=response_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"خطأ في فحص API الواجهة الخلفية: {e}")
            self.alerts.append(f"فشل الاتصال بـ API الواجهة الخلفية: {str(e)}")
            return HealthStatus(
                service='backend_api',
                status='critical',
                response_time=time.time() - start_time,
                details={'error': str(e)},
                timestamp=datetime.now()
            )
    
    def check_frontend(self) -> HealthStatus:
        """فحص الواجهة الأمامية"""
        start_time = time.time()
        try:
            response = requests.get(
                f"{self.config.frontend_url}/health",
                timeout=10
            )
            response_time = time.time() - start_time
            
            details = {
                'status_code': response.status_code,
                'response_time_ms': response_time * 1000,
                'content_length': len(response.content)
            }
            
            status = 'healthy' if response.status_code == 200 else 'warning'
            if response.status_code >= 500:
                status = 'critical'
                self.alerts.append(f"الواجهة الأمامية تعيد خطأ خادم: HTTP {response.status_code}")
            
            return HealthStatus(
                service='frontend',
                status=status,
                response_time=response_time,
                details=details,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"خطأ في فحص الواجهة الأمامية: {e}")
            self.alerts.append(f"فشل الاتصال بالواجهة الأمامية: {str(e)}")
            return HealthStatus(
                service='frontend',
                status='critical',
                response_time=time.time() - start_time,
                details={'error': str(e)},
                timestamp=datetime.now()
            )
    
    def send_alert_email(self, subject: str, body: str):
        """إرسال تنبيه بالبريد الإلكتروني"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.smtp_user
            msg['To'] = self.config.alert_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()
            server.login(self.config.smtp_user, self.config.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"تم إرسال تنبيه بالبريد الإلكتروني: {subject}")
            
        except Exception as e:
            logger.error(f"فشل إرسال البريد الإلكتروني: {e}")
    
    def run_full_check(self) -> Dict[str, Any]:
        """تشغيل فحص شامل للنظام"""
        logger.info("بدء الفحص الشامل للنظام...")
        
        checks = [
            self.check_system_resources(),
            self.check_database(),
            self.check_redis(),
            self.check_backend_api(),
            self.check_frontend()
        ]
        
        # تجميع النتائج
        results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'checks': {},
            'alerts': self.alerts,
            'summary': {
                'total_checks': len(checks),
                'healthy': 0,
                'warning': 0,
                'critical': 0,
                'error': 0
            }
        }
        
        for check in checks:
            results['checks'][check.service] = {
                'status': check.status,
                'response_time': check.response_time,
                'details': check.details,
                'timestamp': check.timestamp.isoformat()
            }
            
            # تحديث الإحصائيات
            results['summary'][check.status] += 1
        
        # تحديد الحالة العامة
        if results['summary']['critical'] > 0:
            results['overall_status'] = 'critical'
        elif results['summary']['warning'] > 0 or results['summary']['error'] > 0:
            results['overall_status'] = 'warning'
        
        # إرسال التنبيهات إذا لزم الأمر
        if self.alerts:
            alert_subject = f"تنبيهات نظام إدارة المخزون - {results['overall_status'].upper()}"
            alert_body = f"""
تم اكتشاف {len(self.alerts)} تنبيه في نظام إدارة المخزون:

{chr(10).join(f"• {alert}" for alert in self.alerts)}

الحالة العامة: {results['overall_status']}
وقت الفحص: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

يرجى مراجعة النظام واتخاذ الإجراءات اللازمة.
            """
            
            if results['overall_status'] in ['critical', 'warning']:
                self.send_alert_email(alert_subject, alert_body)
        
        logger.info(f"انتهى الفحص الشامل - الحالة العامة: {results['overall_status']}")
        return results

def main():
    """الدالة الرئيسية"""
    config = MonitoringConfig()
    monitor = SystemMonitor(config)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        # التشغيل المستمر
        logger.info("بدء المراقبة المستمرة...")
        while True:
            try:
                results = monitor.run_full_check()
                
                # حفظ النتائج
                with open('/app/logs/monitoring_results.json', 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                
                # انتظار 5 دقائق قبل الفحص التالي
                time.sleep(300)
                
            except KeyboardInterrupt:
                logger.info("تم إيقاف المراقبة بواسطة المستخدم")
                break
            except Exception as e:
                logger.error(f"خطأ في المراقبة المستمرة: {e}")
                time.sleep(60)
    else:
        # فحص واحد
        results = monitor.run_full_check()
        print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
