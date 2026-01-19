# /home/ubuntu/ai_web_organized/src/modules/performance_monitoring/data_storage.py

"""
from flask import g
وحدة تخزين وتحليل بيانات الأداء (Performance Data Storage)

هذه الوحدة مسؤولة عن تخزين بيانات الأداء المجمعة من مختلف مكونات النظام،
وتوفير واجهة برمجية لاسترجاع وتحليل هذه البيانات.
"""

import os
import json
import logging
import datetime
import sqlite3
import pandas as pd
from typing import Dict, List, Any, Tuple

# تكوين نظام التسجيل
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class FileBasedStorage:
    """فئة التخزين المعتمد على الملفات - تخزن البيانات في ملفات JSON"""

    def __init__(self, data_dir: str = None):
        """
        تهيئة التخزين المعتمد على الملفات

        Args:
            data_dir (str, optional): مسار دليل تخزين البيانات. Defaults to None.
        """
        self.data_dir = data_dir or "/home/ubuntu/ai_web_organized/data/metrics"
        os.makedirs(self.data_dir, exist_ok=True)

        # تخزين مؤقت للمقاييس الأخيرة
        self.latest_metrics = {
            "system": {},
            "module": {},
            "ai": {},
            "database": {}
        }

    def store_metrics(self,
                      metrics: Dict[str,
                                    Any],
                      metric_type: str,
                      entity_id: str = None) -> bool:
        """
        تخزين المقاييس

        Args:
            metrics (Dict[str, Any]): المقاييس المراد تخزينها
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)

        Returns:
            bool: نجاح العملية
        """
        try:
            # تحديث التخزين المؤقت للمقاييس الأخيرة
            if metric_type == "system":
                self.latest_metrics[metric_type] = metrics
            elif entity_id:
                if metric_type not in self.latest_metrics:
                    self.latest_metrics[metric_type] = {}
                self.latest_metrics[metric_type][entity_id] = metrics

            # تخزين المقاييس في ملف
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{metric_type}"
            if entity_id:
                filename += f"_{entity_id}"
            filename += f"_{timestamp}.json"

            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(metrics, f, indent=2)

            logger.debug(f"Stored {metric_type} metrics to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error storing {metric_type} metrics: {e}")
            return False

    def get_metrics(self,
                    metric_type: str,
                    entity_id: str = None,
                    time_range: str = None,
                    aggregation: str = None) -> List[Dict[str,
                                                          Any]]:
        """
        استرجاع المقاييس

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)
            time_range (str, optional): نطاق زمني للبيانات (مثل "last_hour", "last_day", "last_week")
            aggregation (str, optional): نوع التجميع (مثل "avg", "max", "min")

        Returns:
            List[Dict[str, Any]]: قائمة المقاييس
        """
        try:
            # تحديد نطاق الوقت
            now = datetime.datetime.now()
            start_time = None

            if time_range == "last_hour":
                start_time = now - datetime.timedelta(hours=1)
            elif time_range == "last_day":
                start_time = now - datetime.timedelta(days=1)
            elif time_range == "last_week":
                start_time = now - datetime.timedelta(weeks=1)
            elif time_range == "last_month":
                start_time = now - datetime.timedelta(days=30)

            # البحث عن ملفات المقاييس المطابقة
            metrics_list = []
            prefix = f"{metric_type}"
            if entity_id:
                prefix += f"_{entity_id}"

            for filename in os.listdir(self.data_dir):
                if filename.startswith(prefix) and filename.endswith(".json"):
                    # استخراج الطابع الزمني من اسم الملف
                    try:
                        file_timestamp_str = filename.split(
                            '_')[-1].split('.')[0]
                        file_date_str = filename.split('_')[-2]
                        file_datetime_str = f"{file_date_str}_{file_timestamp_str}"
                        file_datetime = datetime.datetime.strptime(
                            file_datetime_str, "%Y%m%d_%H%M%S")

                        # التحقق من النطاق الزمني
                        if start_time and file_datetime < start_time:
                            continue

                        # قراءة ملف المقاييس
                        filepath = os.path.join(self.data_dir, filename)
                        with open(filepath, 'r') as f:
                            metrics = json.load(f)
                            metrics_list.append(metrics)
                    except Exception as e:
                        logger.warning(
                            f"Error processing metrics file {filename}: {e}")

            # تطبيق التجميع إذا كان مطلوباً
            if aggregation and metrics_list:
                return self._aggregate_metrics(metrics_list, aggregation)

            return metrics_list
        except Exception as e:
            logger.error(f"Error retrieving {metric_type} metrics: {e}")
            return []

    def _aggregate_metrics(
            self, metrics_list: List[Dict[str, Any]], aggregation: str) -> List[Dict[str, Any]]:
        """
        تجميع المقاييس

        Args:
            metrics_list (List[Dict[str, Any]]): قائمة المقاييس
            aggregation (str): نوع التجميع (مثل "avg", "max", "min")

        Returns:
            List[Dict[str, Any]]: قائمة المقاييس المجمعة
        """
        # تحويل قائمة المقاييس إلى DataFrame
        try:
            # استخراج القيم العددية من المقاييس
            numeric_values = {}
            timestamps = []

            for metrics in metrics_list:
                timestamp = metrics.get("timestamp", "")
                timestamps.append(timestamp)

                # استخراج القيم العددية من المقاييس
                self._extract_numeric_values(metrics, "", numeric_values)

            # إنشاء DataFrame
            df = pd.DataFrame(numeric_values)
            df["timestamp"] = timestamps

            # تطبيق التجميع
            if aggregation == "avg":
                aggregated = df.mean(numeric_only=True).to_dict()
            elif aggregation == "max":
                aggregated = df.max(numeric_only=True).to_dict()
            elif aggregation == "min":
                aggregated = df.min(numeric_only=True).to_dict()
            elif aggregation == "sum":
                aggregated = df.sum(numeric_only=True).to_dict()
            else:
                return metrics_list

            # إعادة بناء المقاييس المجمعة
            aggregated_metrics = {
                "timestamp": datetime.datetime.now().isoformat(),
                "aggregation": aggregation,
                "data_points": len(metrics_list),
                "metrics": aggregated
            }

            return [aggregated_metrics]
        except Exception as e:
            logger.error(f"Error aggregating metrics: {e}")
            return metrics_list

    def _extract_numeric_values(
            self, metrics: Dict[str, Any], prefix: str, result: Dict[str, List[float]]):
        """
        استخراج القيم العددية من المقاييس

        Args:
            metrics (Dict[str, Any]): المقاييس
            prefix (str): بادئة المفتاح
            result (Dict[str, List[float]]): قاموس النتائج
        """
        for key, value in metrics.items():
            if key == "timestamp":
                continue

            current_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                self._extract_numeric_values(value, current_key, result)
            elif isinstance(value, (int, float)):
                if current_key not in result:
                    result[current_key] = []
                result[current_key].append(value)

    def get_latest_metrics(self, metric_type: str,
                           entity_id: str = None) -> Dict[str, Any]:
        """
        الحصول على أحدث المقاييس

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)

        Returns:
            Dict[str, Any]: قاموس يحتوي على أحدث المقاييس
        """
        if metric_type == "system":
            return self.latest_metrics.get(metric_type, {})
        elif entity_id and metric_type in self.latest_metrics:
            return self.latest_metrics[metric_type].get(entity_id, {})
        return {}

    def clean_old_data(self, retention_period: int = 30) -> int:
        """
        تنظيف البيانات القديمة

        Args:
            retention_period (int, optional): فترة الاحتفاظ بالبيانات (بالأيام). Defaults to 30.

        Returns:
            int: عدد الملفات التي تم حذفها
        """
        try:
            deleted_count = 0
            now = datetime.datetime.now()
            cutoff_date = now - datetime.timedelta(days=retention_period)

            for filename in os.listdir(self.data_dir):
                if filename.endswith(".json"):
                    try:
                        # استخراج الطابع الزمني من اسم الملف
                        file_timestamp_str = filename.split(
                            '_')[-1].split('.')[0]
                        file_date_str = filename.split('_')[-2]
                        file_datetime_str = f"{file_date_str}_{file_timestamp_str}"
                        file_datetime = datetime.datetime.strptime(
                            file_datetime_str, "%Y%m%d_%H%M%S")

                        # التحقق من تاريخ الملف
                        if file_datetime < cutoff_date:
                            filepath = os.path.join(self.data_dir, filename)
                            os.remove(filepath)
                            deleted_count += 1
                    except Exception as e:
                        logger.warning(
                            f"Error processing file {filename} for cleanup: {e}")

            logger.info(f"Cleaned up {deleted_count} old metrics files.")
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning old data: {e}")
            return 0


class SQLiteStorage:
    """فئة التخزين المعتمد على SQLite - تخزن البيانات في قاعدة بيانات SQLite"""

    def __init__(self, db_path: str = None):
        """
        تهيئة التخزين المعتمد على SQLite

        Args:
            db_path (str, optional): مسار ملف قاعدة البيانات. Defaults to None.
        """
        self.db_path = db_path or "/home/ubuntu/ai_web_organized/data/metrics.db"
        self.conn = None

        # تخزين مؤقت للمقاييس الأخيرة
        self.latest_metrics = {
            "system": {},
            "module": {},
            "ai": {},
            "database": {}
        }

        # إنشاء قاعدة البيانات وجداولها
        self._init_database()

    def _init_database(self):
        """إنشاء قاعدة البيانات وجداولها"""
        try:
            # إنشاء دليل قاعدة البيانات إذا لم يكن موجوداً
            db_dir = os.path.dirname(self.db_path)
            os.makedirs(db_dir, exist_ok=True)

            # الاتصال بقاعدة البيانات
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()

            # إنشاء جدول المقاييس
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                entity_id TEXT,
                data TEXT NOT NULL
            )
            ''')

            # إنشاء فهرس للبحث السريع
            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_metrics_type_entity
            ON metrics (metric_type, entity_id)
            ''')

            cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_metrics_timestamp
            ON metrics (timestamp)
            ''')

            self.conn.commit()
            logger.info(f"Initialized SQLite database at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing SQLite database: {e}")

    def _ensure_connection(self):
        """التأكد من وجود اتصال بقاعدة البيانات"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)

    def store_metrics(self,
                      metrics: Dict[str,
                                    Any],
                      metric_type: str,
                      entity_id: str = None) -> bool:
        """
        تخزين المقاييس

        Args:
            metrics (Dict[str, Any]): المقاييس المراد تخزينها
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)

        Returns:
            bool: نجاح العملية
        """
        try:
            # تحديث التخزين المؤقت للمقاييس الأخيرة
            if metric_type == "system":
                self.latest_metrics[metric_type] = metrics
            elif entity_id:
                if metric_type not in self.latest_metrics:
                    self.latest_metrics[metric_type] = {}
                self.latest_metrics[metric_type][entity_id] = metrics

            # التأكد من وجود اتصال بقاعدة البيانات
            self._ensure_connection()

            # تحويل المقاييس إلى JSON
            metrics_json = json.dumps(metrics)

            # تخزين المقاييس في قاعدة البيانات
            timestamp = metrics.get(
                "timestamp", datetime.datetime.now().isoformat())

            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO metrics (timestamp, metric_type, entity_id, data) VALUES (?, ?, ?, ?)",
                (timestamp, metric_type, entity_id, metrics_json)
            )
            self.conn.commit()

            logger.debug(f"Stored {metric_type} metrics to SQLite database")
            return True
        except Exception as e:
            logger.error(
                f"Error storing {metric_type} metrics to SQLite database: {e}")
            return False

    def get_metrics(self,
                    metric_type: str,
                    entity_id: str = None,
                    time_range: str = None,
                    aggregation: str = None) -> List[Dict[str,
                                                          Any]]:
        """
        استرجاع المقاييس

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)
            time_range (str, optional): نطاق زمني للبيانات (مثل "last_hour", "last_day", "last_week")
            aggregation (str, optional): نوع التجميع (مثل "avg", "max", "min")

        Returns:
            List[Dict[str, Any]]: قائمة المقاييس
        """
        try:
            # التأكد من وجود اتصال بقاعدة البيانات
            self._ensure_connection()

            # تحديد نطاق الوقت
            now = datetime.datetime.now()
            start_time = None

            if time_range == "last_hour":
                start_time = now - datetime.timedelta(hours=1)
            elif time_range == "last_day":
                start_time = now - datetime.timedelta(days=1)
            elif time_range == "last_week":
                start_time = now - datetime.timedelta(weeks=1)
            elif time_range == "last_month":
                start_time = now - datetime.timedelta(days=30)

            # بناء استعلام SQL
            query = "SELECT data FROM metrics WHERE metric_type = ?"
            params = [metric_type]

            if entity_id:
                query += " AND entity_id = ?"
                params.append(entity_id)

            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time.isoformat())

            query += " ORDER BY timestamp DESC"

            # تنفيذ الاستعلام
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # تحويل النتائج إلى قائمة مقاييس
            metrics_list = []
            for row in rows:
                metrics = json.loads(row[0])
                metrics_list.append(metrics)

            # تطبيق التجميع إذا كان مطلوباً
            if aggregation and metrics_list:
                return self._aggregate_metrics(metrics_list, aggregation)

            return metrics_list
        except Exception as e:
            logger.error(
                f"Error retrieving {metric_type} metrics from SQLite database: {e}")
            return []

    def _aggregate_metrics(
            self, metrics_list: List[Dict[str, Any]], aggregation: str) -> List[Dict[str, Any]]:
        """
        تجميع المقاييس

        Args:
            metrics_list (List[Dict[str, Any]]): قائمة المقاييس
            aggregation (str): نوع التجميع (مثل "avg", "max", "min")

        Returns:
            List[Dict[str, Any]]: قائمة المقاييس المجمعة
        """
        # تحويل قائمة المقاييس إلى DataFrame
        try:
            # استخراج القيم العددية من المقاييس
            numeric_values = {}
            timestamps = []

            for metrics in metrics_list:
                timestamp = metrics.get("timestamp", "")
                timestamps.append(timestamp)

                # استخراج القيم العددية من المقاييس
                self._extract_numeric_values(metrics, "", numeric_values)

            # إنشاء DataFrame
            df = pd.DataFrame(numeric_values)
            df["timestamp"] = timestamps

            # تطبيق التجميع
            if aggregation == "avg":
                aggregated = df.mean(numeric_only=True).to_dict()
            elif aggregation == "max":
                aggregated = df.max(numeric_only=True).to_dict()
            elif aggregation == "min":
                aggregated = df.min(numeric_only=True).to_dict()
            elif aggregation == "sum":
                aggregated = df.sum(numeric_only=True).to_dict()
            else:
                return metrics_list

            # إعادة بناء المقاييس المجمعة
            aggregated_metrics = {
                "timestamp": datetime.datetime.now().isoformat(),
                "aggregation": aggregation,
                "data_points": len(metrics_list),
                "metrics": aggregated
            }

            return [aggregated_metrics]
        except Exception as e:
            logger.error(f"Error aggregating metrics: {e}")
            return metrics_list

    def _extract_numeric_values(
            self, metrics: Dict[str, Any], prefix: str, result: Dict[str, List[float]]):
        """
        استخراج القيم العددية من المقاييس

        Args:
            metrics (Dict[str, Any]): المقاييس
            prefix (str): بادئة المفتاح
            result (Dict[str, List[float]]): قاموس النتائج
        """
        for key, value in metrics.items():
            if key == "timestamp":
                continue

            current_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                self._extract_numeric_values(value, current_key, result)
            elif isinstance(value, (int, float)):
                if current_key not in result:
                    result[current_key] = []
                result[current_key].append(value)

    def get_latest_metrics(self, metric_type: str,
                           entity_id: str = None) -> Dict[str, Any]:
        """
        الحصول على أحدث المقاييس

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)

        Returns:
            Dict[str, Any]: قاموس يحتوي على أحدث المقاييس
        """
        try:
            # التأكد من وجود اتصال بقاعدة البيانات
            self._ensure_connection()

            # بناء استعلام SQL
            query = "SELECT data FROM metrics WHERE metric_type = ?"
            params = [metric_type]

            if entity_id:
                query += " AND entity_id = ?"
                params.append(entity_id)

            query += " ORDER BY timestamp DESC LIMIT 1"

            # تنفيذ الاستعلام
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()

            if row:
                return json.loads(row[0])
            else:
                return {}
        except Exception as e:
            logger.error(
                f"Error retrieving latest {metric_type} metrics from SQLite database: {e}")

            # استخدام التخزين المؤقت كاحتياطي
            if metric_type == "system":
                return self.latest_metrics.get(metric_type, {})
            elif entity_id and metric_type in self.latest_metrics:
                return self.latest_metrics[metric_type].get(entity_id, {})
            return {}

    def clean_old_data(self, retention_period: int = 30) -> int:
        """
        تنظيف البيانات القديمة

        Args:
            retention_period (int, optional): فترة الاحتفاظ بالبيانات (بالأيام). Defaults to 30.

        Returns:
            int: عدد السجلات التي تم حذفها
        """
        try:
            # التأكد من وجود اتصال بقاعدة البيانات
            self._ensure_connection()

            # تحديد تاريخ القطع
            cutoff_date = (
                datetime.datetime.now()
                - datetime.timedelta(
                    days=retention_period)).isoformat()

            # حذف السجلات القديمة
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM metrics WHERE timestamp < ?", (cutoff_date,))
            deleted_count = cursor.rowcount
            self.conn.commit()

            logger.info(
                f"Cleaned up {deleted_count} old metrics records from SQLite database.")
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning old data from SQLite database: {e}")
            return 0

    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.conn is not None:
            self.conn.close()
            self.conn = None


class PerformanceDataAnalyzer:
    """محلل بيانات الأداء - مسؤول عن تحليل بيانات الأداء واكتشاف الاتجاهات والمشكلات"""

    def __init__(self, storage):
        """
        تهيئة محلل بيانات الأداء

        Args:
            storage: مخزن البيانات (FileBasedStorage أو SQLiteStorage)
        """
        self.storage = storage

    def analyze_performance_trend(self,
                                  metric_type: str,
                                  entity_id: str = None,
                                  metric_path: str = None,
                                  time_range: str = "last_day") -> Dict[str,
                                                                        Any]:
        """
        تحليل اتجاه الأداء

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)
            metric_path (str, optional): مسار المقياس (مثل "cpu.total_percent")
            time_range (str, optional): نطاق زمني للبيانات. Defaults to "last_day".

        Returns:
            Dict[str, Any]: نتائج تحليل الاتجاه
        """
        metrics = self.storage.get_metrics(metric_type, entity_id, time_range)
        if not metrics:
            return {
                "status": "error",
                "message": "No metrics data available for analysis"}

        # تحليل الاتجاه
        trend_analysis = {
            "status": "success",
            "metric_type": metric_type,
            "entity_id": entity_id,
            "time_range": time_range,
            "data_points": len(metrics),
            "trends": {}
        }

        # استخراج قيم المقياس المحدد
        if metric_path:
            values = self._extract_metric_values(metrics, metric_path)
            if values:
                trend_analysis["trends"][metric_path] = self._analyze_numeric_trend(
                    values)
        else:
            # تحليل اتجاهات مختلفة حسب نوع المقياس
            if metric_type == "system":
                # تحليل اتجاه استخدام CPU
                cpu_values = self._extract_metric_values(
                    metrics, "cpu.total_percent")
                if cpu_values:
                    trend_analysis["trends"]["cpu.total_percent"] = self._analyze_numeric_trend(
                        cpu_values)

                # تحليل اتجاه استخدام الذاكرة
                memory_values = self._extract_metric_values(
                    metrics, "memory.percent")
                if memory_values:
                    trend_analysis["trends"]["memory.percent"] = self._analyze_numeric_trend(
                        memory_values)

                # تحليل اتجاه استخدام القرص
                disk_values = self._extract_metric_values(
                    metrics, "disk.percent")
                if disk_values:
                    trend_analysis["trends"]["disk.percent"] = self._analyze_numeric_trend(
                        disk_values)

            elif metric_type == "module":
                # تحليل اتجاه وقت الاستجابة
                response_time_values = self._extract_metric_values(
                    metrics, "performance.response_time_ms")
                if response_time_values:
                    trend_analysis["trends"]["performance.response_time_ms"] = self._analyze_numeric_trend(
                        response_time_values)

                # تحليل اتجاه معدل الأخطاء
                error_rate_values = self._extract_metric_values(
                    metrics, "performance.error_rate")
                if error_rate_values:
                    trend_analysis["trends"]["performance.error_rate"] = self._analyze_numeric_trend(
                        error_rate_values)

            elif metric_type == "ai":
                # تحليل اتجاه وقت الاستدلال
                inference_time_values = self._extract_metric_values(
                    metrics, "performance.inference_time_ms")
                if inference_time_values:
                    trend_analysis["trends"]["performance.inference_time_ms"] = self._analyze_numeric_trend(
                        inference_time_values)

                # تحليل اتجاه الدقة
                accuracy_values = self._extract_metric_values(
                    metrics, "performance.accuracy")
                if accuracy_values:
                    trend_analysis["trends"]["performance.accuracy"] = self._analyze_numeric_trend(
                        accuracy_values)

            elif metric_type == "database":
                # تحليل اتجاه وقت الاستعلام
                query_time_values = self._extract_metric_values(
                    metrics, "performance.query_time_ms")
                if query_time_values:
                    trend_analysis["trends"]["performance.query_time_ms"] = self._analyze_numeric_trend(
                        query_time_values)

                # تحليل اتجاه معدل الأخطاء
                error_rate_values = self._extract_metric_values(
                    metrics, "performance.error_rate")
                if error_rate_values:
                    trend_analysis["trends"]["performance.error_rate"] = self._analyze_numeric_trend(
                        error_rate_values)

        return trend_analysis

    def _extract_metric_values(
            self, metrics_list: List[Dict[str, Any]], metric_path: str) -> List[float]:
        """
        استخراج قيم المقياس من قائمة المقاييس

        Args:
            metrics_list (List[Dict[str, Any]]): قائمة المقاييس
            metric_path (str): مسار المقياس (مثل "cpu.total_percent")

        Returns:
            List[float]: قائمة قيم المقياس
        """
        values = []

        for metrics in metrics_list:
            # تقسيم مسار المقياس إلى أجزاء
            parts = metric_path.split(".")

            # استخراج قيمة المقياس
            value = metrics
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    value = None
                    break

            if value is not None and isinstance(value, (int, float)):
                values.append(value)

        return values

    def _analyze_numeric_trend(self, values: List[float]) -> Dict[str, Any]:
        """
        تحليل اتجاه القيم العددية

        Args:
            values (List[float]): قائمة القيم العددية

        Returns:
            Dict[str, Any]: نتائج تحليل الاتجاه
        """
        if not values:
            return {
                "status": "error",
                "message": "No values provided for analysis"}

        # حساب الإحصاءات الأساسية
        avg = sum(values) / len(values)
        min_val = min(values)
        max_val = max(values)

        # تحديد الاتجاه
        if len(values) >= 2:
            first_half = values[:len(values) // 2]
            second_half = values[len(values) // 2:]
            first_half_avg = sum(first_half) / len(first_half)
            second_half_avg = sum(second_half) / len(second_half)

            if second_half_avg > first_half_avg * 1.1:
                trend = "increasing"
                trend_percent = ((second_half_avg / first_half_avg) - 1) * 100
            elif second_half_avg < first_half_avg * 0.9:
                trend = "decreasing"
                trend_percent = (1 - (second_half_avg / first_half_avg)) * 100
            else:
                trend = "stable"
                trend_percent = ((second_half_avg / first_half_avg) - 1) * 100
        else:
            trend = "unknown"
            trend_percent = 0

        # حساب الانحراف المعياري
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5

        return {
            "avg": avg,
            "min": min_val,
            "max": max_val,
            "std_dev": std_dev,
            "trend": trend,
            "trend_percent": trend_percent,
            "data_points": len(values)
        }

    def detect_anomalies(self,
                         metric_type: str,
                         entity_id: str = None,
                         metric_path: str = None,
                         time_range: str = "last_day",
                         threshold: float = None,
                         std_dev_threshold: float = 3.0) -> List[Dict[str,
                                                                      Any]]:
        """
        اكتشاف الانحرافات في المقاييس

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)
            metric_path (str, optional): مسار المقياس (مثل "cpu.total_percent")
            time_range (str, optional): نطاق زمني للبيانات. Defaults to "last_day".
            threshold (float, optional): عتبة القيمة المطلقة. Defaults to None.
            std_dev_threshold (float, optional): عتبة الانحراف المعياري. Defaults to 3.0.

        Returns:
            List[Dict[str, Any]]: قائمة الانحرافات المكتشفة
        """
        metrics = self.storage.get_metrics(metric_type, entity_id, time_range)
        if not metrics:
            return []

        anomalies = []

        # استخراج قيم المقياس المحدد
        if metric_path:
            values_with_timestamps = self._extract_metric_values_with_timestamps(
                metrics, metric_path)
            if values_with_timestamps:
                anomalies.extend(
                    self._detect_anomalies_in_values(
                        values_with_timestamps,
                        metric_path,
                        threshold,
                        std_dev_threshold))
        else:
            # اكتشاف الانحرافات في مقاييس مختلفة حسب نوع المقياس
            if metric_type == "system":
                # اكتشاف انحرافات استخدام CPU
                cpu_values = self._extract_metric_values_with_timestamps(
                    metrics, "cpu.total_percent")
                if cpu_values:
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            cpu_values,
                            "cpu.total_percent",
                            threshold or 80,
                            std_dev_threshold))

                # اكتشاف انحرافات استخدام الذاكرة
                memory_values = self._extract_metric_values_with_timestamps(
                    metrics, "memory.percent")
                if memory_values:
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            memory_values,
                            "memory.percent",
                            threshold or 80,
                            std_dev_threshold))

                # اكتشاف انحرافات استخدام القرص
                disk_values = self._extract_metric_values_with_timestamps(
                    metrics, "disk.percent")
                if disk_values:
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            disk_values,
                            "disk.percent",
                            threshold or 90,
                            std_dev_threshold))

            elif metric_type == "module":
                # اكتشاف انحرافات وقت الاستجابة
                response_time_values = self._extract_metric_values_with_timestamps(
                    metrics, "performance.response_time_ms")
                if response_time_values:
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            response_time_values,
                            "performance.response_time_ms",
                            threshold or 500,
                            std_dev_threshold))

                # اكتشاف انحرافات معدل الأخطاء
                error_rate_values = self._extract_metric_values_with_timestamps(
                    metrics, "performance.error_rate")
                if error_rate_values:
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            error_rate_values,
                            "performance.error_rate",
                            threshold or 0.05,
                            std_dev_threshold))

            elif metric_type == "ai":
                # اكتشاف انحرافات وقت الاستدلال
                inference_time_values = self._extract_metric_values_with_timestamps(
                    metrics, "performance.inference_time_ms")
                if inference_time_values:
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            inference_time_values,
                            "performance.inference_time_ms",
                            threshold or 1000,
                            std_dev_threshold))

                # اكتشاف انحرافات الدقة
                accuracy_values = self._extract_metric_values_with_timestamps(
                    metrics, "performance.accuracy")
                if accuracy_values:
                    # لاحظ أن عتبة الدقة هي الحد الأدنى، وليس الحد الأقصى
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            accuracy_values,
                            "performance.accuracy",
                            threshold or 0.8,
                            std_dev_threshold,
                            is_lower_threshold=True))

            elif metric_type == "database":
                # اكتشاف انحرافات وقت الاستعلام
                query_time_values = self._extract_metric_values_with_timestamps(
                    metrics, "performance.query_time_ms")
                if query_time_values:
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            query_time_values,
                            "performance.query_time_ms",
                            threshold or 100,
                            std_dev_threshold))

                # اكتشاف انحرافات معدل الأخطاء
                error_rate_values = self._extract_metric_values_with_timestamps(
                    metrics, "performance.error_rate")
                if error_rate_values:
                    anomalies.extend(
                        self._detect_anomalies_in_values(
                            error_rate_values,
                            "performance.error_rate",
                            threshold or 0.05,
                            std_dev_threshold))

        return anomalies

    def _extract_metric_values_with_timestamps(
            self, metrics_list: List[Dict[str, Any]], metric_path: str) -> List[Tuple[str, float]]:
        """
        استخراج قيم المقياس مع الطوابع الزمنية من قائمة المقاييس

        Args:
            metrics_list (List[Dict[str, Any]]): قائمة المقاييس
            metric_path (str): مسار المقياس (مثل "cpu.total_percent")

        Returns:
            List[Tuple[str, float]]: قائمة أزواج (الطابع الزمني، القيمة)
        """
        values_with_timestamps = []

        for metrics in metrics_list:
            timestamp = metrics.get("timestamp", "")

            # تقسيم مسار المقياس إلى أجزاء
            parts = metric_path.split(".")

            # استخراج قيمة المقياس
            value = metrics
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    value = None
                    break

            if value is not None and isinstance(value, (int, float)):
                values_with_timestamps.append((timestamp, value))

        return values_with_timestamps

    def _detect_anomalies_in_values(self,
                                    values_with_timestamps: List[Tuple[str,
                                                                       float]],
                                    metric_path: str,
                                    threshold: float = None,
                                    std_dev_threshold: float = 3.0,
                                    is_lower_threshold: bool = False) -> List[Dict[str,
                                                                                   Any]]:
        """
        اكتشاف الانحرافات في قيم المقياس

        Args:
            values_with_timestamps (List[Tuple[str, float]]): قائمة أزواج (الطابع الزمني، القيمة)
            metric_path (str): مسار المقياس
            threshold (float, optional): عتبة القيمة المطلقة. Defaults to None.
            std_dev_threshold (float, optional): عتبة الانحراف المعياري. Defaults to 3.0.
            is_lower_threshold (bool, optional): هل العتبة هي الحد الأدنى. Defaults to False.

        Returns:
            List[Dict[str, Any]]: قائمة الانحرافات المكتشفة
        """
        if not values_with_timestamps:
            return []

        # استخراج القيم فقط (بدون الطوابع الزمنية)
        values = [v[1] for v in values_with_timestamps]

        # حساب المتوسط والانحراف المعياري
        avg = sum(values) / len(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5

        anomalies = []

        for timestamp, value in values_with_timestamps:
            # التحقق من الانحراف المعياري
            if std_dev > 0 and abs(value - avg) > std_dev * std_dev_threshold:
                anomalies.append({
                    "timestamp": timestamp,
                    "metric_path": metric_path,
                    "value": value,
                    "avg": avg,
                    "std_dev": std_dev,
                    "deviation": (value - avg) / std_dev if std_dev > 0 else 0,
                    "type": "statistical_anomaly"
                })

            # التحقق من العتبة المطلقة
            elif threshold is not None:
                if (is_lower_threshold and value < threshold) or (
                        not is_lower_threshold and value > threshold):
                    anomalies.append({
                        "timestamp": timestamp,
                        "metric_path": metric_path,
                        "value": value,
                        "threshold": threshold,
                        "excess": value - threshold if not is_lower_threshold else threshold - value,
                        "type": "threshold_violation"
                    })

        return anomalies

    def generate_performance_report(self,
                                    metric_type: str,
                                    entity_id: str = None,
                                    time_range: str = "last_day") -> Dict[str,
                                                                          Any]:
        """
        إنشاء تقرير أداء

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان (module_id, ai_model_id, db_name)
            time_range (str, optional): نطاق زمني للبيانات. Defaults to "last_day".

        Returns:
            Dict[str, Any]: تقرير الأداء
        """
        report = {
            "type": metric_type,
            "entity_id": entity_id,
            "time_range": time_range,
            "timestamp": datetime.datetime.now().isoformat(),
            "metrics_count": 0,
            "trends": {},
            "anomalies": [],
            "recommendations": []
        }

        # جمع المقاييس
        metrics = self.storage.get_metrics(metric_type, entity_id, time_range)
        report["metrics_count"] = len(metrics)

        # تحليل الاتجاهات
        trends = self.analyze_performance_trend(
            metric_type, entity_id, time_range=time_range)
        report["trends"] = trends.get("trends", {})

        # اكتشاف الانحرافات
        anomalies = self.detect_anomalies(
            metric_type, entity_id, time_range=time_range)
        report["anomalies"] = anomalies

        # توفير التوصيات
        recommendations = self._generate_recommendations(
            metric_type, entity_id, trends, anomalies)
        report["recommendations"] = recommendations

        return report

    def _generate_recommendations(self,
                                  metric_type: str,
                                  entity_id: str,
                                  trends: Dict[str,
                                               Any],
                                  anomalies: List[Dict[str,
                                                       Any]]) -> List[Dict[str,
                                                                           Any]]:
        """
        توفير توصيات لتحسين الأداء

        Args:
            metric_type (str): نوع المقياس
            entity_id (str): معرف الكيان
            trends (Dict[str, Any]): نتائج تحليل الاتجاهات
            anomalies (List[Dict[str, Any]]): قائمة الانحرافات المكتشفة

        Returns:
            List[Dict[str, Any]]: قائمة التوصيات
        """
        recommendations = []

        # توصيات بناءً على الاتجاهات
        for metric_path, trend in trends.items():
            if trend.get("trend") == "increasing" and trend.get(
                    "trend_percent", 0) > 20:
                # التحقق من نوع المقياس
                if "cpu" in metric_path or "memory" in metric_path or "disk" in metric_path:
                    recommendations.append({
                        "metric_path": metric_path,
                        "severity": "medium",
                        "issue": f"Increasing {metric_path} usage trend",
                        "recommendation": f"Monitor {metric_path} usage closely as it has increased by {trend.get('trend_percent', 0):.1f}% recently."
                    })
                elif "response_time" in metric_path or "inference_time" in metric_path or "query_time" in metric_path:
                    recommendations.append({
                        "metric_path": metric_path,
                        "severity": "medium",
                        "issue": f"Increasing {metric_path} trend",
                        "recommendation": f"Investigate performance issues as {metric_path} has increased by {trend.get('trend_percent', 0):.1f}% recently."
                    })
                elif "error_rate" in metric_path:
                    recommendations.append({
                        "metric_path": metric_path,
                        "severity": "high",
                        "issue": f"Increasing {metric_path} trend",
                        "recommendation": f"Investigate error causes as {metric_path} has increased by {trend.get('trend_percent', 0):.1f}% recently."
                    })

        # توصيات بناءً على الانحرافات
        for anomaly in anomalies:
            metric_path = anomaly.get("metric_path", "")
            anomaly_type = anomaly.get("type", "")

            if anomaly_type == "threshold_violation":
                if "cpu" in metric_path:
                    recommendations.append({
                        "metric_path": metric_path,
                        "severity": "high",
                        "issue": "High CPU usage",
                        "recommendation": "Consider optimizing CPU-intensive operations or scaling up resources."
                    })
                elif "memory" in metric_path:
                    recommendations.append({
                        "metric_path": metric_path,
                        "severity": "high",
                        "issue": "High memory usage",
                        "recommendation": "Check for memory leaks or consider increasing memory allocation."
                    })
                elif "disk" in metric_path:
                    recommendations.append({
                        "metric_path": metric_path,
                        "severity": "high",
                        "issue": "High disk usage",
                        "recommendation": "Clean up unnecessary files or consider adding more storage."
                    })
                elif "response_time" in metric_path:
                    recommendations.append({
                        "metric_path": metric_path,
                        "severity": "medium",
                        "issue": "Slow response time",
                        "recommendation": "Optimize code or database queries to improve response time."
                    })
                elif "error_rate" in metric_path:
                    recommendations.append({
                        "metric_path": metric_path,
                        "severity": "high",
                        "issue": "High error rate",
                        "recommendation": "Investigate and fix errors to improve reliability."
                    })

        # إزالة التوصيات المكررة
        unique_recommendations = []
        seen_issues = set()

        for recommendation in recommendations:
            issue = recommendation.get("issue", "")
            if issue not in seen_issues:
                seen_issues.add(issue)
                unique_recommendations.append(recommendation)

        return unique_recommendations


# مثال للاستخدام
if __name__ == "__main__":
    # إنشاء مخزن البيانات
    storage = FileBasedStorage()
    # storage = SQLiteStorage()

    # إنشاء محلل البيانات
    analyzer = PerformanceDataAnalyzer(storage)

    # تخزين بعض بيانات الاختبار
    test_metrics = {
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu": {
            "total_percent": 75.5,
            "user_percent": 50.2,
            "system_percent": 25.3,
            "idle_percent": 24.5
        },
        "memory": {
            "percent": 60.8,
            "total_bytes": 16 * 1024 * 1024 * 1024,
            "used_bytes": 9.7 * 1024 * 1024 * 1024
        },
        "disk": {
            "percent": 85.2,
            "total_bytes": 500 * 1024 * 1024 * 1024,
            "used_bytes": 425.6 * 1024 * 1024 * 1024
        }
    }

    storage.store_metrics(test_metrics, "system")

    # تحليل اتجاه الأداء
    trend_analysis = analyzer.analyze_performance_trend(
        "system", metric_path="cpu.total_percent")
    print("\nPerformance Trend Analysis:")
    print(f"Status: {trend_analysis['status']}")
    print(f"Data Points: {trend_analysis['data_points']}")
    for metric_path, trend in trend_analysis.get("trends", {}).items():
        print(f"\nMetric: {metric_path}")
        print(f"Average: {trend.get('avg', 0):.1f}")
        print(f"Trend: {trend.get('trend', 'unknown')}")
        print(f"Trend Percent: {trend.get('trend_percent', 0):.1f}%")

    # اكتشاف الانحرافات
    anomalies = analyzer.detect_anomalies(
        "system", metric_path="cpu.total_percent", threshold=70)
    print("\nAnomalies:")
    for anomaly in anomalies:
        print(f"\nTimestamp: {anomaly.get('timestamp', '')}")
        print(f"Metric: {anomaly.get('metric_path', '')}")
        print(f"Value: {anomaly.get('value', 0):.1f}")
        print(f"Type: {anomaly.get('type', '')}")
        if anomaly.get("type") == "threshold_violation":
            print(f"Threshold: {anomaly.get('threshold', 0):.1f}")
            print(f"Excess: {anomaly.get('excess', 0):.1f}")
        elif anomaly.get("type") == "statistical_anomaly":
            print(f"Average: {anomaly.get('avg', 0):.1f}")
            print(f"Standard Deviation: {anomaly.get('std_dev', 0):.1f}")
            print(f"Deviation: {anomaly.get('deviation', 0):.1f}")

    # إنشاء تقرير أداء
    report = analyzer.generate_performance_report("system")
    print("\nPerformance Report:")
    print(f"Timestamp: {report['timestamp']}")
    print(f"Metrics Count: {report['metrics_count']}")
    print(f"Anomalies Count: {len(report['anomalies'])}")
    print(f"Recommendations Count: {len(report['recommendations'])}")

    for recommendation in report.get("recommendations", []):
        print("\nRecommendation:")
        print(f"Severity: {recommendation.get('severity', '')}")
        print(f"Issue: {recommendation.get('issue', '')}")
        print(f"Recommendation: {recommendation.get('recommendation', '')}")
