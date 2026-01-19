# /home/ubuntu/ai_web_organized/src/modules/performance_monitoring/data_collector.py

"""
from flask import g
وحدة جمع بيانات الأداء (Performance Data Collector)

هذه الوحدة مسؤولة عن جمع بيانات الأداء من مختلف مكونات النظام بشكل دوري،
وتوفير واجهة برمجية للتكامل مع وحدة مراقبة الأداء الرئيسية.
"""

import datetime
import json
import logging
import os
import threading
import time
from typing import Any, Dict

import psutil
import requests

# تكوين نظام التسجيل
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class ModulePerformanceCollector:
    """جامع بيانات أداء المديولات - مسؤول عن جمع بيانات الأداء من مديول محدد"""

    def __init__(self, module_id: str, module_api_url: str = None):
        """
        تهيئة جامع بيانات أداء المديول

        Args:
            module_id (str): معرف المديول
            module_api_url (str, optional): عنوان واجهة برمجة المديول. Defaults to None.
        """
        self.module_id = module_id
        self.module_api_url = module_api_url
        self.process_info = None
        self.pid = None

        # محاولة العثور على عملية المديول
        self._find_module_process()

    def _find_module_process(self):
        """البحث عن عملية المديول في قائمة العمليات النشطة"""
        try:
            # هذه الدالة تبحث عن عملية المديول بناءً على اسمه
            # في بيئة حقيقية، يمكن استخدام طرق أكثر دقة للعثور على العملية

            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # البحث عن اسم المديول في سطر الأوامر
                    if proc.info['cmdline'] and any(
                            self.module_id in cmd for cmd in proc.info['cmdline']):
                        self.pid = proc.info['pid']
                        self.process_info = proc
                        logger.info(
                            f"Found process for module {self.module_id}: PID={self.pid}")
                        return
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            logger.warning(
                f"Could not find process for module {self.module_id}")
        except Exception as e:
            logger.error(
                f"Error finding process for module {self.module_id}: {e}")

    def collect_metrics(self) -> Dict[str, Any]:
        """
        جمع مقاييس المديول

        Returns:
            Dict[str, Any]: قاموس يحتوي على مقاييس المديول
        """
        metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "module_id": self.module_id,
            "status": "active",  # يمكن أن تكون "active", "warning", "error", "inactive"
            "performance": {},
            "resources": {}
        }

        # محاولة جمع البيانات من واجهة برمجة المديول
        api_metrics = self._collect_from_api()
        if api_metrics:
            # دمج البيانات من واجهة البرمجة مع المقاييس
            metrics.update(api_metrics)

        # جمع بيانات استهلاك الموارد من العملية
        process_metrics = self._collect_from_process()
        if process_metrics:
            metrics["resources"] = process_metrics

        # إضافة بيانات مخصصة حسب نوع المديول
        custom_metrics = self._collect_custom_metrics()
        if custom_metrics:
            metrics["custom"] = custom_metrics

        return metrics

    def _collect_from_api(self) -> Dict[str, Any]:
        """
        جمع البيانات من واجهة برمجة المديول

        Returns:
            Dict[str, Any]: البيانات المجمعة من واجهة البرمجة
        """
        if not self.module_api_url:
            return {}

        try:
            response = requests.get(
                f"{self.module_api_url}/metrics", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Failed to collect metrics from API for module {self.module_id}: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(
                f"Error collecting metrics from API for module {self.module_id}: {e}")
            return {}

    def _collect_from_process(self) -> Dict[str, Any]:
        """
        جمع بيانات استهلاك الموارد من العملية

        Returns:
            Dict[str, Any]: بيانات استهلاك الموارد
        """
        if not self.pid:
            self._find_module_process()
            if not self.pid:
                return {}

        try:
            # تحديث معلومات العملية
            process = psutil.Process(self.pid)

            # جمع بيانات استهلاك الموارد
            cpu_percent = process.cpu_percent(interval=0.5)
            memory_info = process.memory_info()
            io_counters = process.io_counters() if hasattr(process, 'io_counters') else None

            resources = {
                "cpu_percent": cpu_percent,
                "memory_bytes": memory_info.rss,
                "memory_percent": process.memory_percent(),
                "threads_count": process.num_threads(),
                "open_files_count": len(process.open_files()),
                "connections_count": len(process.connections()),
            }

            if io_counters:
                resources.update({
                    "disk_read_bytes": io_counters.read_bytes,
                    "disk_write_bytes": io_counters.write_bytes,
                    "disk_read_count": io_counters.read_count,
                    "disk_write_count": io_counters.write_count
                })

            return resources
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.warning(
                f"Process for module {self.module_id} is no longer available: {e}")
            self.pid = None
            self.process_info = None
            return {}
        except Exception as e:
            logger.error(
                f"Error collecting process metrics for module {self.module_id}: {e}")
            return {}

    def _collect_custom_metrics(self) -> Dict[str, Any]:
        """
        جمع بيانات مخصصة حسب نوع المديول

        Returns:
            Dict[str, Any]: البيانات المخصصة
        """
        custom_metrics = {}

        # تخصيص المقاييس حسب نوع المديول
        if self.module_id == "backup_module":
            # جمع بيانات خاصة بمديول النسخ الاحتياطي
            try:
                # هذا مثال فقط، يجب تعديله حسب الهيكل الفعلي للمديول
                backups_dir = "/home/ubuntu/ai_web_organized/data/backups"
                if os.path.exists(backups_dir):
                    backup_files = [f for f in os.listdir(
                        backups_dir) if f.endswith(".tar.gz")]
                    custom_metrics["backup_count"] = len(backup_files)

                    if backup_files:
                        # الحصول على تاريخ آخر نسخة احتياطية
                        backup_files.sort(reverse=True)
                        latest_backup = backup_files[0]
                        backup_path = os.path.join(backups_dir, latest_backup)
                        backup_time = datetime.datetime.fromtimestamp(
                            os.path.getmtime(backup_path))
                        custom_metrics["last_backup_time"] = backup_time.isoformat(
                        )
                        custom_metrics["last_backup_size"] = os.path.getsize(
                            backup_path)
            except Exception as e:
                logger.error(
                    f"Error collecting custom metrics for backup_module: {e}")

        elif self.module_id == "data_validation":
            # جمع بيانات خاصة بمديول التحقق من البيانات
            try:
                # هذا مثال فقط، يجب تعديله حسب الهيكل الفعلي للمديول
                validation_log_path = "/home/ubuntu/ai_web_organized/logs/data_validation.log"
                if os.path.exists(validation_log_path):
                    with open(validation_log_path, 'r') as f:
                        log_lines = f.readlines()

                        # حساب عدد عمليات التحقق
                        validation_count = sum(
                            1 for line in log_lines if "Validation completed" in line)
                        custom_metrics["validation_count"] = validation_count

                        # حساب عدد الأخطاء
                        error_count = sum(
                            1 for line in log_lines if "Validation error" in line)
                        custom_metrics["validation_error_count"] = error_count

                        if validation_count > 0:
                            custom_metrics["validation_success_rate"] = 1 - \
                                (error_count / validation_count)
            except Exception as e:
                logger.error(
                    f"Error collecting custom metrics for data_validation: {e}")

        return custom_metrics


class AIModelPerformanceCollector:
    """جامع بيانات أداء نماذج الذكاء الصناعي - مسؤول عن جمع بيانات الأداء من نموذج ذكاء صناعي محدد"""

    def __init__(self, model_id: str, model_api_url: str = None):
        """
        تهيئة جامع بيانات أداء نموذج الذكاء الصناعي

        Args:
            model_id (str): معرف النموذج
            model_api_url (str, optional): عنوان واجهة برمجة النموذج. Defaults to None.
        """
        self.model_id = model_id
        self.model_api_url = model_api_url
        self.process_info = None
        self.pid = None

        # محاولة العثور على عملية النموذج
        self._find_model_process()

    def _find_model_process(self):
        """البحث عن عملية النموذج في قائمة العمليات النشطة"""
        try:
            # هذه الدالة تبحث عن عملية النموذج بناءً على اسمه
            # في بيئة حقيقية، يمكن استخدام طرق أكثر دقة للعثور على العملية

            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # البحث عن اسم النموذج في سطر الأوامر
                    if proc.info['cmdline'] and any(
                            self.model_id in cmd for cmd in proc.info['cmdline']):
                        self.pid = proc.info['pid']
                        self.process_info = proc
                        logger.info(
                            f"Found process for AI model {self.model_id}: PID={self.pid}")
                        return
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            logger.warning(
                f"Could not find process for AI model {self.model_id}")
        except Exception as e:
            logger.error(
                f"Error finding process for AI model {self.model_id}: {e}")

    def collect_metrics(self) -> Dict[str, Any]:
        """
        جمع مقاييس نموذج الذكاء الصناعي

        Returns:
            Dict[str, Any]: قاموس يحتوي على مقاييس النموذج
        """
        metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "ai_model_id": self.model_id,
            "status": "active",  # يمكن أن تكون "active", "suspended", "error"
            "performance": {},
            "resources": {}
        }

        # محاولة جمع البيانات من واجهة برمجة النموذج
        api_metrics = self._collect_from_api()
        if api_metrics:
            # دمج البيانات من واجهة البرمجة مع المقاييس
            metrics.update(api_metrics)

        # جمع بيانات استهلاك الموارد من العملية
        process_metrics = self._collect_from_process()
        if process_metrics:
            metrics["resources"] = process_metrics

        # إضافة بيانات مخصصة حسب نوع النموذج
        custom_metrics = self._collect_custom_metrics()
        if custom_metrics:
            metrics["custom"] = custom_metrics

        return metrics

    def _collect_from_api(self) -> Dict[str, Any]:
        """
        جمع البيانات من واجهة برمجة النموذج

        Returns:
            Dict[str, Any]: البيانات المجمعة من واجهة البرمجة
        """
        if not self.model_api_url:
            return {}

        try:
            response = requests.get(f"{self.model_api_url}/metrics", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(
                    f"Failed to collect metrics from API for AI model {self.model_id}: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(
                f"Error collecting metrics from API for AI model {self.model_id}: {e}")
            return {}

    def _collect_from_process(self) -> Dict[str, Any]:
        """
        جمع بيانات استهلاك الموارد من العملية

        Returns:
            Dict[str, Any]: بيانات استهلاك الموارد
        """
        if not self.pid:
            self._find_model_process()
            if not self.pid:
                return {}

        try:
            # تحديث معلومات العملية
            process = psutil.Process(self.pid)

            # جمع بيانات استهلاك الموارد
            cpu_percent = process.cpu_percent(interval=0.5)
            memory_info = process.memory_info()

            resources = {
                "cpu_percent": cpu_percent,
                "memory_bytes": memory_info.rss,
                "memory_percent": process.memory_percent(),
                "threads_count": process.num_threads(),
                "connections_count": len(process.connections()),
            }

            # محاولة جمع بيانات GPU إذا كانت متاحة
            gpu_metrics = self._collect_gpu_metrics()
            if gpu_metrics:
                resources.update(gpu_metrics)

            return resources
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.warning(
                f"Process for AI model {self.model_id} is no longer available: {e}")
            self.pid = None
            self.process_info = None
            return {}
        except Exception as e:
            logger.error(
                f"Error collecting process metrics for AI model {self.model_id}: {e}")
            return {}

    def _collect_gpu_metrics(self) -> Dict[str, Any]:
        """
        جمع بيانات استهلاك GPU

        Returns:
            Dict[str, Any]: بيانات استهلاك GPU
        """
        # هذه الدالة تحاول جمع بيانات استهلاك GPU
        # في بيئة حقيقية، يمكن استخدام مكتبات مثل pynvml أو gputil

        try:
            # هذا مثال فقط، يجب تعديله حسب البيئة الفعلية
            # محاولة تنفيذ أمر nvidia-smi للحصول على بيانات GPU
            import subprocess
            result = subprocess.run(['nvidia-smi',
                                     '--query-gpu=utilization.gpu,memory.used,memory.total',
                                     '--format=csv,noheader,nounits'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)

            if result.returncode == 0:
                # تحليل النتيجة
                output = result.stdout.strip()
                if output:
                    parts = output.split(',')
                    if len(parts) >= 3:
                        gpu_percent = float(parts[0].strip())
                        gpu_memory_used = float(
                            parts[1].strip()) * 1024 * 1024  # تحويل من ميجابايت إلى بايت
                        gpu_memory_total = float(
                            parts[2].strip()) * 1024 * 1024  # تحويل من ميجابايت إلى بايت

                        return {
                            "gpu_percent": gpu_percent,
                            "gpu_memory_bytes": gpu_memory_used,
                            "gpu_memory_total_bytes": gpu_memory_total,
                            "gpu_memory_percent": (
                                gpu_memory_used /
                                gpu_memory_total) *
                            100 if gpu_memory_total > 0 else 0}

            return {}
        except Exception as e:
            logger.debug(f"Error collecting GPU metrics: {e}")
            return {}

    def _collect_custom_metrics(self) -> Dict[str, Any]:
        """
        جمع بيانات مخصصة حسب نوع النموذج

        Returns:
            Dict[str, Any]: البيانات المخصصة
        """
        custom_metrics = {}

        # تخصيص المقاييس حسب نوع النموذج
        if self.model_id == "ai_agent_image_analyzer":
            # جمع بيانات خاصة بنموذج تحليل الصور
            try:
                # هذا مثال فقط، يجب تعديله حسب الهيكل الفعلي للنموذج
                log_path = "/home/ubuntu/ai_web_organized/logs/image_analyzer.log"
                if os.path.exists(log_path):
                    with open(log_path, 'r') as f:
                        log_lines = f.readlines()

                        # حساب عدد الصور التي تم تحليلها
                        image_count = sum(
                            1 for line in log_lines if "Image analysis completed" in line)
                        custom_metrics["image_count"] = image_count

                        # حساب متوسط وقت التحليل
                        analysis_times = []
                        for line in log_lines:
                            if "Analysis time:" in line:
                                try:
                                    time_str = line.split("Analysis time:")[
                                        1].strip().split(" ")[0]
                                    analysis_times.append(float(time_str))
                                except BaseException:
                                    pass

                        if analysis_times:
                            custom_metrics["average_analysis_time"] = sum(
                                analysis_times) / len(analysis_times)
            except Exception as e:
                logger.error(
                    f"Error collecting custom metrics for ai_agent_image_analyzer: {e}")

        elif self.model_id == "ai_agent_diagnosis":
            # جمع بيانات خاصة بنموذج التشخيص
            try:
                # هذا مثال فقط، يجب تعديله حسب الهيكل الفعلي للنموذج
                log_path = "/home/ubuntu/ai_web_organized/logs/diagnosis.log"
                if os.path.exists(log_path):
                    with open(log_path, 'r') as f:
                        log_lines = f.readlines()

                        # حساب عدد التشخيصات
                        diagnosis_count = sum(
                            1 for line in log_lines if "Diagnosis completed" in line)
                        custom_metrics["diagnosis_count"] = diagnosis_count

                        # حساب عدد التشخيصات الناجحة
                        success_count = sum(
                            1 for line in log_lines if "Diagnosis successful" in line)
                        if diagnosis_count > 0:
                            custom_metrics["diagnosis_success_rate"] = success_count / \
                                diagnosis_count
            except Exception as e:
                logger.error(
                    f"Error collecting custom metrics for ai_agent_diagnosis: {e}")

        return custom_metrics


class DatabasePerformanceCollector:
    """جامع بيانات أداء قاعدة البيانات - مسؤول عن جمع بيانات الأداء من قاعدة بيانات محددة"""

    def __init__(self, db_name: str, db_config: Dict[str, Any] = None):
        """
        تهيئة جامع بيانات أداء قاعدة البيانات

        Args:
            db_name (str): اسم قاعدة البيانات
            db_config (Dict[str, Any], optional): إعدادات قاعدة البيانات. Defaults to None.
        """
        self.db_name = db_name
        self.db_config = db_config or {}
        self.connection = None

        # محاولة الاتصال بقاعدة البيانات
        self._connect_to_db()

    def _connect_to_db(self):
        """الاتصال بقاعدة البيانات"""
        try:
            # هذه الدالة تحاول الاتصال بقاعدة البيانات
            # في بيئة حقيقية، يجب استخدام مكتبة قاعدة البيانات المناسبة

            db_type = self.db_config.get("type", "postgresql")

            if db_type == "postgresql":
                try:
                    import psycopg2
                    self.connection = psycopg2.connect(
                        host=self.db_config.get("host", "localhost"),
                        port=self.db_config.get("port", 5432),
                        database=self.db_name,
                        user=self.db_config.get("user", "postgres"),
                        password=self.db_config.get("password", "")
                    )
                    logger.info(
                        f"Connected to PostgreSQL database: {self.db_name}")
                except ImportError:
                    logger.warning(
                        "psycopg2 module not available. PostgreSQL metrics collection will be limited.")
                except Exception as e:
                    logger.error(
                        f"Error connecting to PostgreSQL database {self.db_name}: {e}")

            elif db_type == "mysql":
                try:
                    import mysql.connector
                    self.connection = mysql.connector.connect(
                        host=self.db_config.get("host", "localhost"),
                        port=self.db_config.get("port", 3306),
                        database=self.db_name,
                        user=self.db_config.get("user", "root"),
                        password=self.db_config.get("password", "")
                    )
                    logger.info(f"Connected to MySQL database: {self.db_name}")
                except ImportError:
                    logger.warning(
                        "mysql.connector module not available. MySQL metrics collection will be limited.")
                except Exception as e:
                    logger.error(
                        f"Error connecting to MySQL database {self.db_name}: {e}")

            elif db_type == "sqlite":
                try:
                    import sqlite3
                    db_path = self.db_config.get(
                        "path", f"/home/ubuntu/ai_web_organized/data/{self.db_name}.db")
                    self.connection = sqlite3.connect(db_path)
                    logger.info(f"Connected to SQLite database: {db_path}")
                except ImportError:
                    logger.warning(
                        "sqlite3 module not available. SQLite metrics collection will be limited.")
                except Exception as e:
                    logger.error(
                        f"Error connecting to SQLite database {self.db_name}: {e}")

            else:
                logger.warning(f"Unsupported database type: {db_type}")

        except Exception as e:
            logger.error(f"Error connecting to database {self.db_name}: {e}")

    def collect_metrics(self) -> Dict[str, Any]:
        """
        جمع مقاييس قاعدة البيانات

        Returns:
            Dict[str, Any]: قاموس يحتوي على مقاييس قاعدة البيانات
        """
        metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "db_name": self.db_name,
            "status": "active",  # يمكن أن تكون "active", "warning", "error"
            "performance": {},
            "resources": {}
        }

        # جمع بيانات الأداء من قاعدة البيانات
        db_metrics = self._collect_db_metrics()
        if db_metrics:
            metrics.update(db_metrics)

        # جمع بيانات استهلاك الموارد
        resource_metrics = self._collect_resource_metrics()
        if resource_metrics:
            metrics["resources"] = resource_metrics

        return metrics

    def _collect_db_metrics(self) -> Dict[str, Any]:
        """
        جمع بيانات الأداء من قاعدة البيانات

        Returns:
            Dict[str, Any]: بيانات الأداء
        """
        if not self.connection:
            self._connect_to_db()
            if not self.connection:
                return {}

        try:
            db_type = self.db_config.get("type", "postgresql")
            performance_metrics = {}

            if db_type == "postgresql":
                # جمع بيانات الأداء من PostgreSQL
                cursor = self.connection.cursor()

                # عدد الاتصالات النشطة
                cursor.execute(
                    "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'")
                active_connections = cursor.fetchone()[0]

                # متوسط وقت الاستعلام
                cursor.execute(
                    "SELECT mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 1")
                result = cursor.fetchone()
                avg_query_time = result[0] if result else 0

                # عدد الاستعلامات
                cursor.execute("SELECT sum(calls) FROM pg_stat_statements")
                result = cursor.fetchone()
                query_count = result[0] if result else 0

                # حجم قاعدة البيانات
                cursor.execute(f"SELECT pg_database_size('{self.db_name}')")
                db_size = cursor.fetchone()[0]

                performance_metrics["performance"] = {
                    "active_connections": active_connections,
                    "avg_query_time_ms": avg_query_time,
                    "query_count": query_count
                }

                performance_metrics["resources"] = {
                    "size_bytes": db_size
                }

                cursor.close()

            elif db_type == "mysql":
                # جمع بيانات الأداء من MySQL
                cursor = self.connection.cursor()

                # عدد الاتصالات النشطة
                cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
                result = cursor.fetchone()
                active_connections = int(result[1]) if result else 0

                # عدد الاستعلامات
                cursor.execute("SHOW STATUS LIKE 'Questions'")
                result = cursor.fetchone()
                query_count = int(result[1]) if result else 0

                # حجم قاعدة البيانات
                cursor.execute(
                    f"SELECT SUM(data_length + index_length) FROM information_schema.TABLES WHERE table_schema = '{self.db_name}'")
                result = cursor.fetchone()
                db_size = int(result[0]) if result and result[0] else 0

                performance_metrics["performance"] = {
                    "active_connections": active_connections,
                    "query_count": query_count
                }

                performance_metrics["resources"] = {
                    "size_bytes": db_size
                }

                cursor.close()

            elif db_type == "sqlite":
                # جمع بيانات الأداء من SQLite
                cursor = self.connection.cursor()

                # عدد الجداول
                cursor.execute(
                    "SELECT count(*) FROM sqlite_master WHERE type='table'")
                table_count = cursor.fetchone()[0]

                # حجم قاعدة البيانات
                db_path = self.db_config.get(
                    "path", f"/home/ubuntu/ai_web_organized/data/{self.db_name}.db")
                db_size = os.path.getsize(
                    db_path) if os.path.exists(db_path) else 0

                performance_metrics["performance"] = {
                    "table_count": table_count
                }

                performance_metrics["resources"] = {
                    "size_bytes": db_size
                }

                cursor.close()

            return performance_metrics

        except Exception as e:
            logger.error(
                f"Error collecting database metrics for {self.db_name}: {e}")
            # إعادة تعيين الاتصال في حالة حدوث خطأ
            try:
                if self.connection is not None:
                    self.connection.close()
            except BaseException:
                pass
            self.connection = None
            return {}

    def _collect_resource_metrics(self) -> Dict[str, Any]:
        """
        جمع بيانات استهلاك الموارد

        Returns:
            Dict[str, Any]: بيانات استهلاك الموارد
        """
        # هذه الدالة تحاول جمع بيانات استهلاك الموارد لعملية قاعدة البيانات
        # في بيئة حقيقية، يمكن استخدام طرق أكثر دقة للعثور على العملية

        try:
            db_type = self.db_config.get("type", "postgresql")
            process_name = ""

            if db_type == "postgresql":
                process_name = "postgres"
            elif db_type == "mysql":
                process_name = "mysqld"
            elif db_type == "sqlite":
                # SQLite يعمل ضمن العملية الرئيسية، لا يوجد عملية منفصلة
                return {}

            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and process_name in proc.info['name'].lower(
                    ):
                        # تحديث معلومات العملية
                        process = psutil.Process(proc.info['pid'])

                        # جمع بيانات استهلاك الموارد
                        cpu_percent = process.cpu_percent(interval=0.5)
                        memory_info = process.memory_info()

                        return {
                            "cpu_percent": cpu_percent,
                            "memory_bytes": memory_info.rss,
                            "memory_percent": process.memory_percent(),
                            "threads_count": process.num_threads(),
                            "connections_count": len(process.connections()),
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            return {}
        except Exception as e:
            logger.error(
                f"Error collecting resource metrics for database {self.db_name}: {e}")
            return {}


class SystemPerformanceCollector:
    """جامع بيانات أداء النظام - مسؤول عن جمع بيانات الأداء من النظام بشكل عام"""

    def __init__(self):
        """تهيئة جامع بيانات أداء النظام"""

    def collect_metrics(self) -> Dict[str, Any]:
        """
        جمع مقاييس النظام

        Returns:
            Dict[str, Any]: قاموس يحتوي على مقاييس النظام
        """
        metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "cpu": {},
            "memory": {},
            "disk": {},
            "network": {}
        }

        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_times = psutil.cpu_times_percent(interval=1)
            metrics["cpu"] = {
                "total_percent": cpu_percent,
                "user_percent": cpu_times.user,
                "system_percent": cpu_times.system,
                "idle_percent": cpu_times.idle,
                "core_count": psutil.cpu_count(),
                "per_core_percent": psutil.cpu_percent(interval=1, percpu=True)
            }

            # Memory metrics
            memory = psutil.virtual_memory()
            metrics["memory"] = {
                "total_bytes": memory.total,
                "available_bytes": memory.available,
                "used_bytes": memory.used,
                "percent": memory.percent,
                "swap_total": psutil.swap_memory().total,
                "swap_used": psutil.swap_memory().used,
                "swap_percent": psutil.swap_memory().percent
            }

            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            metrics["disk"] = {
                "total_bytes": disk.total,
                "used_bytes": disk.used,
                "free_bytes": disk.free,
                "percent": disk.percent,
                "read_count": disk_io.read_count if disk_io else 0,
                "write_count": disk_io.write_count if disk_io else 0,
                "read_bytes": disk_io.read_bytes if disk_io else 0,
                "write_bytes": disk_io.write_bytes if disk_io else 0
            }

            # Network metrics
            net_io = psutil.net_io_counters()
            metrics["network"] = {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout
            }

            return metrics
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return metrics


class PerformanceDataCollectorService:
    """خدمة جمع بيانات الأداء - مسؤولة عن تنسيق عملية جمع البيانات من مختلف المصادر"""

    def __init__(self, config_path=None):
        """
        تهيئة خدمة جمع بيانات الأداء

        Args:
            config_path (str, optional): مسار ملف التكوين. Defaults to None.
        """
        self.config = self._load_config(config_path)
        self.running = False
        self.collection_thread = None
        self.data_dir = self.config.get(
            "data_dir", "/home/ubuntu/ai_web_organized/data/metrics")
        os.makedirs(self.data_dir, exist_ok=True)

        # إنشاء جامعي البيانات
        self.system_collector = SystemPerformanceCollector()
        self.module_collectors = {}
        self.ai_model_collectors = {}
        self.db_collectors = {}

        # تهيئة جامعي البيانات
        self._init_collectors()

    def _load_config(self, config_path):
        """تحميل إعدادات التكوين من ملف"""
        default_config = {
            # الفاصل الزمني بين عمليات الجمع (بالثواني)
            "collection_interval": 60,
            "data_dir": "/home/ubuntu/ai_web_organized/data/metrics",
            "modules": [
                {"id": "backup_module", "api_url": None},
                {"id": "data_validation", "api_url": None}
            ],
            "ai_models": [
                {"id": "ai_agent", "api_url": None},
                {"id": "ai_agent_image_analyzer", "api_url": None},
                {"id": "ai_agent_diagnosis", "api_url": None}
            ],
            "databases": [
                {"name": "main_db", "type": "postgresql", "host": "localhost",
                    "port": 5432, "user": "postgres", "password": ""}
            ]
        }

        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # دمج الإعدادات المخصصة مع الإعدادات الافتراضية
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                logger.error(f"Error loading config from {config_path}: {e}")
                return default_config
        else:
            return default_config

    def _init_collectors(self):
        """تهيئة جامعي البيانات"""
        # تهيئة جامعي بيانات المديولات
        for module_config in self.config.get("modules", []):
            module_id = module_config.get("id")
            if module_id:
                self.module_collectors[module_id] = ModulePerformanceCollector(
                    module_id=module_id,
                    module_api_url=module_config.get("api_url")
                )

        # تهيئة جامعي بيانات نماذج الذكاء الصناعي
        for model_config in self.config.get("ai_models", []):
            model_id = model_config.get("id")
            if model_id:
                self.ai_model_collectors[model_id] = AIModelPerformanceCollector(
                    model_id=model_id,
                    model_api_url=model_config.get("api_url")
                )

        # تهيئة جامعي بيانات قواعد البيانات
        for db_config in self.config.get("databases", []):
            db_name = db_config.get("name")
            if db_name:
                self.db_collectors[db_name] = DatabasePerformanceCollector(
                    db_name=db_name,
                    db_config=db_config
                )

    def start_collection(self, interval=None):
        """
        بدء عملية جمع البيانات بشكل دوري

        Args:
            interval (int, optional): الفاصل الزمني بين عمليات الجمع (بالثواني).
                                     Defaults to config value.
        """
        if self.running is not None:
            logger.warning("Data collection is already running.")
            return

        if interval is None:
            interval = self.config.get("collection_interval", 60)

        self.running = True
        self.collection_thread = threading.Thread(
            target=self._collection_loop, args=(interval,))
        self.collection_thread.daemon = True
        self.collection_thread.start()
        logger.info(
            f"Started performance data collection with interval {interval} seconds.")

    def stop_collection(self):
        """إيقاف عملية جمع البيانات"""
        if not self.running:
            logger.warning("Data collection is not running.")
            return

        self.running = False
        if self.collection_thread is not None:
            self.collection_thread.join(timeout=5.0)
            if self.collection_thread.is_alive():
                logger.warning(
                    "Collection thread did not terminate gracefully.")
            else:
                logger.info("Stopped performance data collection.")

    def _collection_loop(self, interval):
        """حلقة جمع البيانات الدورية"""
        while self.running:
            try:
                # جمع مقاييس النظام
                system_metrics = self.system_collector.collect_metrics()
                self._store_metrics(system_metrics, "system")

                # جمع مقاييس المديولات
                for module_id, collector in self.module_collectors.items():
                    module_metrics = collector.collect_metrics()
                    self._store_metrics(module_metrics, "module", module_id)

                # جمع مقاييس نماذج الذكاء الصناعي
                for model_id, collector in self.ai_model_collectors.items():
                    ai_metrics = collector.collect_metrics()
                    self._store_metrics(ai_metrics, "ai", model_id)

                # جمع مقاييس قواعد البيانات
                for db_name, collector in self.db_collectors.items():
                    db_metrics = collector.collect_metrics()
                    self._store_metrics(db_metrics, "database", db_name)

            except Exception as e:
                logger.error(f"Error in collection loop: {e}")

            # انتظار الفاصل الزمني المحدد
            time.sleep(interval)

    def _store_metrics(self, metrics, metric_type, entity_id=None):
        """
        تخزين المقاييس في ملف

        Args:
            metrics (Dict[str, Any]): المقاييس المراد تخزينها
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)
        """
        try:
            # إنشاء اسم الملف
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{metric_type}"
            if entity_id:
                filename += f"_{entity_id}"
            filename += f"_{timestamp}.json"

            filepath = os.path.join(self.data_dir, filename)

            # تخزين المقاييس في ملف
            with open(filepath, 'w') as f:
                json.dump(metrics, f, indent=2)

            logger.debug(f"Stored {metric_type} metrics to {filepath}")
        except Exception as e:
            logger.error(f"Error storing {metric_type} metrics: {e}")

    def collect_all_metrics(self) -> Dict[str, Any]:
        """
        جمع جميع المقاييس مرة واحدة

        Returns:
            Dict[str, Any]: قاموس يحتوي على جميع المقاييس
        """
        all_metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "system": {},
            "modules": {},
            "ai_models": {},
            "databases": {}
        }

        try:
            # جمع مقاييس النظام
            all_metrics["system"] = self.system_collector.collect_metrics()

            # جمع مقاييس المديولات
            for module_id, collector in self.module_collectors.items():
                all_metrics["modules"][module_id] = collector.collect_metrics()

            # جمع مقاييس نماذج الذكاء الصناعي
            for model_id, collector in self.ai_model_collectors.items():
                all_metrics["ai_models"][model_id] = collector.collect_metrics()

            # جمع مقاييس قواعد البيانات
            for db_name, collector in self.db_collectors.items():
                all_metrics["databases"][db_name] = collector.collect_metrics()

            return all_metrics
        except Exception as e:
            logger.error(f"Error collecting all metrics: {e}")
            return all_metrics


# مثال للاستخدام
if __name__ == "__main__":
    # إنشاء خدمة جمع بيانات الأداء
    collector_service = PerformanceDataCollectorService()

    # بدء جمع البيانات
    collector_service.start_collection(interval=10)  # جمع البيانات كل 10 ثوانٍ

    try:
        # انتظار لجمع بعض البيانات
        print("Collecting performance data for 30 seconds...")
        time.sleep(30)

        # جمع جميع المقاييس مرة واحدة
        all_metrics = collector_service.collect_all_metrics()

        # عرض بعض المقاييس
        print("\nSystem Metrics:")
        print(
            f"CPU Usage: {all_metrics['system'].get('cpu', {}).get('total_percent', 0):.1f}%")
        print(
            f"Memory Usage: {all_metrics['system'].get('memory', {}).get('percent', 0):.1f}%")
        print(
            f"Disk Usage: {all_metrics['system'].get('disk', {}).get('percent', 0):.1f}%")

        print("\nModule Metrics:")
        for module_id, metrics in all_metrics.get("modules", {}).items():
            print(f"Module: {module_id}")
            print(f"Status: {metrics.get('status', 'unknown')}")
            print(
                f"CPU Usage: {metrics.get('resources', {}).get('cpu_percent', 0):.1f}%")
            print(
                f"Memory Usage: {metrics.get('resources', {}).get('memory_bytes', 0) / (1024 * 1024):.1f} MB")
            print()

        print("\nAI Model Metrics:")
        for model_id, metrics in all_metrics.get("ai_models", {}).items():
            print(f"AI Model: {model_id}")
            print(f"Status: {metrics.get('status', 'unknown')}")
            print(
                f"CPU Usage: {metrics.get('resources', {}).get('cpu_percent', 0):.1f}%")
            print(
                f"Memory Usage: {metrics.get('resources', {}).get('memory_bytes', 0) / (1024 * 1024):.1f} MB")
            print()

    finally:
        # إيقاف جمع البيانات
        collector_service.stop_collection()
        print("\nPerformance data collection stopped.")
