# /home/ubuntu/ai_web_organized/src/modules/performance_monitoring/performance_analyzer.py

"""
from flask import g
وحدة تحليل الأداء (Performance Analyzer)

هذه الوحدة مسؤولة عن تحليل بيانات الأداء واكتشاف الانحرافات والاتجاهات،
وتوفير توصيات لتحسين الأداء وتحديد المديولات ذات الأداء المنخفض.
"""

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

# تكوين نظام التسجيل
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# محاولة استيراد مكتبات تحليل البيانات
try:
    from evidently.dashboard import Dashboard
    from evidently.tabs import CatTargetDriftTab, DataDriftTab
    EVIDENTLY_AVAILABLE = True
except ImportError:
    logger.warning(
        "Evidently library not available. Data drift detection will be limited.")
    EVIDENTLY_AVAILABLE = False


@dataclass
class TrendAnalysis:
    """فئة تمثل نتائج تحليل الاتجاه"""
    entity_id: str
    metric_type: str
    time_range: str
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_slope: float
    trend_confidence: float
    data_points: List[Dict[str, Any]]
    last_value: float
    average_value: float
    min_value: float
    max_value: float
    prediction_next_hour: Optional[float] = None
    prediction_next_day: Optional[float] = None


@dataclass
class Anomaly:
    """فئة تمثل انحرافاً في الأداء"""
    entity_id: str
    metric_type: str
    metric_name: str
    timestamp: str
    value: float
    expected_value: float
    deviation_percent: float
    severity: str  # "low", "medium", "high", "critical"
    description: str


@dataclass
class Recommendation:
    """فئة تمثل توصية لتحسين الأداء"""
    entity_id: str
    metric_type: str
    priority: str  # "low", "medium", "high", "critical"
    description: str
    expected_improvement: str
    implementation_difficulty: str  # "easy", "medium", "hard"
    implementation_steps: List[str]


class PerformanceAnalyzer:
    """محلل الأداء - مسؤول عن تحليل بيانات الأداء واكتشاف الانحرافات"""

    def __init__(self, data_store, config_path=None):
        """
        تهيئة محلل الأداء

        Args:
            data_store: مخزن بيانات الأداء
            config_path (str, optional): مسار ملف التكوين. Defaults to None.
        """
        self.data_store = data_store
        self.config = self._load_config(config_path)
        self.anomaly_thresholds = self.config.get("anomaly_thresholds", {
            "cpu_percent": {"medium": 70, "high": 85, "critical": 95},
            "memory_percent": {"medium": 70, "high": 85, "critical": 95},
            "disk_percent": {"medium": 70, "high": 85, "critical": 95},
            "error_rate": {"medium": 0.05, "high": 0.1, "critical": 0.2},
            "response_time_ms": {"medium": 500, "high": 1000, "critical": 2000}
        })

    def _load_config(self, config_path):
        """تحميل إعدادات التكوين من ملف"""
        default_config = {
            "anomaly_detection": {
                "enabled": True,
                "sensitivity": "medium",  # "low", "medium", "high"
                "lookback_period": "1d",  # "1h", "6h", "1d", "7d"
                "min_data_points": 10
            },
            "trend_analysis": {
                "enabled": True,
                "min_data_points": 24,
                "prediction_enabled": True
            },
            "recommendations": {
                "enabled": True,
                "max_recommendations": 5
            }
        }

        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # دمج الإعدادات المخصصة مع الإعدادات الافتراضية
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                        elif isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if subkey not in config[key]:
                                    config[key][subkey] = subvalue
                    return config
            except Exception as e:
                logger.error(f"Error loading config from {config_path}: {e}")
                return default_config
        else:
            return default_config

    def analyze_performance_trend(
            self, metric_type: str, entity_id: str = None,
            time_range: str = "1d") -> Optional[TrendAnalysis]:
        """
        تحليل اتجاه الأداء

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان. Defaults to None.
            time_range (str, optional): النطاق الزمني. Defaults to "1d".

        Returns:
            Optional[TrendAnalysis]: نتائج تحليل الاتجاه
        """
        if not self.config["trend_analysis"]["enabled"]:
            logger.info("Trend analysis is disabled in configuration.")
            return None

        try:
            # الحصول على البيانات من مخزن البيانات
            metrics = self.data_store.get_metrics(
                metric_type, entity_id, time_range)
            if not metrics or len(
                    metrics) < self.config["trend_analysis"]["min_data_points"]:
                logger.warning(
                    f"Not enough data points for trend analysis. Got {len(metrics) if metrics else 0}, "
                    f"need {self.config['trend_analysis']['min_data_points']}.")
                return None

            # تحويل البيانات إلى DataFrame للتحليل
            df = pd.DataFrame(metrics)

            # تحديد المقاييس الرئيسية حسب نوع الكيان
            if metric_type == "system":
                main_metrics = [
                    "cpu.total_percent",
                    "memory.percent",
                    "disk.percent"]
            elif metric_type == "module":
                main_metrics = [
                    "performance.response_time_ms",
                    "performance.error_rate",
                    "resources.cpu_percent"]
            elif metric_type == "ai":
                main_metrics = [
                    "performance.inference_time_ms",
                    "performance.accuracy",
                    "resources.gpu_percent"]
            elif metric_type == "database":
                main_metrics = [
                    "performance.query_time_ms",
                    "performance.error_rate",
                    "resources.connection_usage_percent"]
            else:
                main_metrics = []

            # اختيار المقياس الأول المتاح للتحليل
            target_metric = None
            for metric in main_metrics:
                if metric in df.columns:
                    target_metric = metric
                    break

            if not target_metric:
                logger.warning(
                    f"No suitable metrics found for trend analysis of {metric_type}.")
                return None

            # تحليل الاتجاه للمقياس المستهدف
            values = df[target_metric].values
            timestamps = pd.to_datetime(df["timestamp"].values)

            # حساب الاتجاه باستخدام الانحدار الخطي
            x = np.arange(len(values))
            coeffs = np.polyfit(x, values, 1)
            slope = coeffs[0]

            # تحديد اتجاه الاتجاه
            if abs(slope) < 0.01:  # عتبة للاستقرار
                trend_direction = "stable"
            elif slope > 0:
                trend_direction = "increasing"
            else:
                trend_direction = "decreasing"

            # حساب معامل الثقة (R²)
            p = np.poly1d(coeffs)
            y_pred = p(x)
            y_mean = np.mean(values)
            ss_tot = np.sum((values - y_mean) ** 2)
            ss_res = np.sum((values - y_pred) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

            # التنبؤ بالقيم المستقبلية
            prediction_next_hour = None
            prediction_next_day = None

            if self.config["trend_analysis"]["prediction_enabled"]:
                # التنبؤ بالساعة التالية (افتراض أن البيانات بفاصل ساعة)
                prediction_next_hour = p(len(values))
                # التنبؤ باليوم التالي (افتراض 24 نقطة بيانات في اليوم)
                prediction_next_day = p(len(values) + 24)

            # إنشاء كائن تحليل الاتجاه
            trend_analysis = TrendAnalysis(
                entity_id=entity_id or "system",
                metric_type=metric_type,
                time_range=time_range,
                trend_direction=trend_direction,
                trend_slope=slope,
                trend_confidence=r_squared,
                data_points=[{"timestamp": t, "value": v} for t, v in zip(timestamps, values)],
                last_value=values[-1] if len(values) > 0 else 0,
                average_value=np.mean(values),
                min_value=np.min(values),
                max_value=np.max(values),
                prediction_next_hour=prediction_next_hour,
                prediction_next_day=prediction_next_day
            )

            return trend_analysis

        except Exception as e:
            logger.error(f"Error analyzing performance trend: {e}")
            return None

    def detect_performance_anomalies(
            self, metric_type: str, entity_id: str = None,
            time_range: str = "1d") -> List[Anomaly]:
        """
        اكتشاف الانحرافات في الأداء

        Args:
            metric_type (str): نوع المقياس (system, module, ai, database)
            entity_id (str, optional): معرف الكيان. Defaults to None.
            time_range (str, optional): النطاق الزمني. Defaults to "1d".

        Returns:
            List[Anomaly]: قائمة الانحرافات المكتشفة
        """
        if not self.config["anomaly_detection"]["enabled"]:
            logger.info("Anomaly detection is disabled in configuration.")
            return []

        try:
            # الحصول على البيانات من مخزن البيانات
            metrics = self.data_store.get_metrics(
                metric_type, entity_id, time_range)
            if not metrics or len(
                    metrics) < self.config["anomaly_detection"]["min_data_points"]:
                logger.warning(
                    f"Not enough data points for anomaly detection. Got {len(metrics) if metrics else 0}, "
                    f"need {self.config['anomaly_detection']['min_data_points']}.")
                return []

            # تحويل البيانات إلى DataFrame للتحليل
            df = pd.DataFrame(metrics)

            # قائمة الانحرافات المكتشفة
            anomalies = []

            # تحديد المقاييس الرئيسية حسب نوع الكيان
            if metric_type == "system":
                metrics_to_check = {
                    "cpu.total_percent": "CPU Usage",
                    "memory.percent": "Memory Usage",
                    "disk.percent": "Disk Usage"
                }
            elif metric_type == "module":
                metrics_to_check = {
                    "performance.response_time_ms": "Response Time",
                    "performance.error_rate": "Error Rate",
                    "resources.cpu_percent": "CPU Usage"
                }
            elif metric_type == "ai":
                metrics_to_check = {
                    "performance.inference_time_ms": "Inference Time",
                    "performance.accuracy": "Accuracy",
                    "resources.gpu_percent": "GPU Usage"
                }
            elif metric_type == "database":
                metrics_to_check = {
                    "performance.query_time_ms": "Query Time",
                    "performance.error_rate": "Error Rate",
                    "resources.connection_usage_percent": "Connection Usage"
                }
            else:
                metrics_to_check = {}

            # فحص كل مقياس للانحرافات
            for metric_key, metric_name in metrics_to_check.items():
                if metric_key not in df.columns:
                    continue

                values = df[metric_key].values
                timestamps = df["timestamp"].values

                # حساب المتوسط والانحراف المعياري
                mean = np.mean(values)
                std = np.std(values)

                # تحديد عتبة الانحراف حسب حساسية الكشف
                sensitivity = self.config["anomaly_detection"]["sensitivity"]
                if sensitivity == "low":
                    threshold_multiplier = 3.0  # 3 sigma
                elif sensitivity == "medium":
                    threshold_multiplier = 2.5  # 2.5 sigma
                else:  # high
                    threshold_multiplier = 2.0  # 2 sigma

                threshold = threshold_multiplier * std

                # فحص كل نقطة بيانات للانحرافات
                for i, (timestamp, value) in enumerate(
                        zip(timestamps, values)):
                    # تجاهل القيم الأولى لتجنب الإنذارات الكاذبة
                    if i < 3:
                        continue

                    deviation = abs(value - mean)
                    if deviation > threshold:
                        # حساب نسبة الانحراف
                        deviation_percent = (
                            deviation / mean) * 100 if mean != 0 else 0

                        # تحديد شدة الانحراف
                        severity = "low"
                        if metric_key in self.anomaly_thresholds:
                            thresholds = self.anomaly_thresholds[metric_key]
                            if value >= thresholds.get(
                                    "critical", float('inf')):
                                severity = "critical"
                            elif value >= thresholds.get("high", float('inf')):
                                severity = "high"
                            elif value >= thresholds.get("medium", float('inf')):
                                severity = "medium"

                        # إنشاء كائن انحراف
                        anomaly = Anomaly(
                            entity_id=entity_id or "system",
                            metric_type=metric_type,
                            metric_name=metric_name,
                            timestamp=timestamp,
                            value=value,
                            expected_value=mean,
                            deviation_percent=deviation_percent,
                            severity=severity,
                            description=f"Anomaly detected in {metric_name}: value {value:.2f} "
                            f"deviates {deviation_percent:.2f}% from expected {mean:.2f}")

                        anomalies.append(anomaly)

            # ترتيب الانحرافات حسب الشدة والوقت
            severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            anomalies.sort(
                key=lambda a: (
                    severity_order.get(
                        a.severity,
                        4),
                    a.timestamp),
                reverse=True)

            return anomalies

        except Exception as e:
            logger.error(f"Error detecting performance anomalies: {e}")
            return []

    def identify_low_performing_modules(
            self,
            threshold: float = None,
            time_range: str = "1d") -> List[str]:
        """
        تحديد المديولات ذات الأداء المنخفض

        Args:
            threshold (float, optional): عتبة الأداء المنخفض. Defaults to None.
            time_range (str, optional): النطاق الزمني. Defaults to "1d".

        Returns:
            List[str]: قائمة معرفات المديولات ذات الأداء المنخفض
        """
        try:
            # الحصول على قائمة المديولات النشطة
            active_modules = self.data_store.get_active_entities("module")

            # قائمة المديولات ذات الأداء المنخفض
            low_performing_modules = []

            # تحديد عتبة الأداء المنخفض إذا لم يتم تحديدها
            if threshold is None:
                threshold = 0.8  # 80% من الأداء المتوقع

            # فحص كل مديول
            for module_id in active_modules:
                # الحصول على مقاييس المديول
                metrics = self.data_store.get_metrics(
                    "module", module_id, time_range)
                if not metrics:
                    continue

                # تحويل البيانات إلى DataFrame للتحليل
                df = pd.DataFrame(metrics)

                # حساب متوسط وقت الاستجابة ومعدل الأخطاء
                response_time_key = "performance.response_time_ms"
                error_rate_key = "performance.error_rate"

                if response_time_key in df.columns and error_rate_key in df.columns:
                    avg_response_time = df[response_time_key].mean()
                    avg_error_rate = df[error_rate_key].mean()

                    # تحديد ما إذا كان المديول ذو أداء منخفض
                    is_low_performing = False

                    # فحص وقت الاستجابة
                    if avg_response_time > 1000:  # أكثر من 1 ثانية
                        is_low_performing = True

                    # فحص معدل الأخطاء
                    if avg_error_rate > 0.05:  # أكثر من 5%
                        is_low_performing = True

                    if is_low_performing:
                        low_performing_modules.append(module_id)

            return low_performing_modules

        except Exception as e:
            logger.error(f"Error identifying low performing modules: {e}")
            return []

    def identify_resource_intensive_modules(
            self, resource_type: str, threshold: float = None,
            time_range: str = "1d") -> List[str]:
        """
        تحديد المديولات التي تستهلك موارد كثيرة

        Args:
            resource_type (str): نوع المورد (cpu, memory, disk, network)
            threshold (float, optional): عتبة استهلاك الموارد. Defaults to None.
            time_range (str, optional): النطاق الزمني. Defaults to "1d".

        Returns:
            List[str]: قائمة معرفات المديولات التي تستهلك موارد كثيرة
        """
        try:
            # الحصول على قائمة المديولات النشطة
            active_modules = self.data_store.get_active_entities("module")

            # قائمة المديولات التي تستهلك موارد كثيرة
            resource_intensive_modules = []

            # تحديد عتبة استهلاك الموارد إذا لم يتم تحديدها
            if threshold is None:
                if resource_type == "cpu":
                    threshold = 70  # 70% من CPU
                elif resource_type == "memory":
                    threshold = 70  # 70% من الذاكرة
                elif resource_type == "disk":
                    threshold = 70  # 70% من القرص
                elif resource_type == "network":
                    threshold = 70  # 70% من الشبكة
                else:
                    threshold = 70  # قيمة افتراضية

            # تحديد مفتاح المورد في البيانات
            if resource_type == "cpu":
                resource_key = "resources.cpu_percent"
            elif resource_type == "memory":
                resource_key = "resources.memory_percent"
            elif resource_type == "disk":
                resource_key = "resources.disk_bytes"
            elif resource_type == "network":
                resource_key = "resources.network_bytes_out"
            else:
                logger.warning(f"Unknown resource type: {resource_type}")
                return []

            # فحص كل مديول
            for module_id in active_modules:
                # الحصول على مقاييس المديول
                metrics = self.data_store.get_metrics(
                    "module", module_id, time_range)
                if not metrics:
                    continue

                # تحويل البيانات إلى DataFrame للتحليل
                df = pd.DataFrame(metrics)

                if resource_key in df.columns:
                    # حساب متوسط استهلاك المورد
                    avg_resource_usage = df[resource_key].mean()

                    # تحديد ما إذا كان المديول يستهلك موارد كثيرة
                    if avg_resource_usage > threshold:
                        resource_intensive_modules.append(module_id)

            # ترتيب المديولات حسب استهلاك الموارد (من الأعلى إلى الأدنى)
            resource_intensive_modules.sort(
                key=lambda module_id: self._get_average_resource_usage(
                    module_id, resource_key, time_range), reverse=True)

            return resource_intensive_modules

        except Exception as e:
            logger.error(f"Error identifying resource intensive modules: {e}")
            return []

    def _get_average_resource_usage(self, module_id, resource_key, time_range):
        """
        الحصول على متوسط استهلاك المورد للمديول

        Args:
            module_id (str): معرف المديول
            resource_key (str): مفتاح المورد
            time_range (str): النطاق الزمني

        Returns:
            float: متوسط استهلاك المورد
        """
        try:
            metrics = self.data_store.get_metrics(
                "module", module_id, time_range)
            if not metrics:
                return 0

            df = pd.DataFrame(metrics)
            if resource_key in df.columns:
                return df[resource_key].mean()
            else:
                return 0
        except Exception:
            return 0

    def generate_performance_recommendations(
            self, entity_id: str = None) -> List[Recommendation]:
        """
        توفير توصيات لتحسين الأداء

        Args:
            entity_id (str, optional): معرف الكيان. Defaults to None.

        Returns:
            List[Recommendation]: قائمة التوصيات
        """
        if not self.config["recommendations"]["enabled"]:
            logger.info("Recommendations are disabled in configuration.")
            return []

        try:
            recommendations = []

            # تحديد نوع الكيان
            if entity_id is None:
                # توصيات على مستوى النظام
                system_recommendations = self._generate_system_recommendations()
                recommendations.extend(system_recommendations)

                # توصيات للمديولات ذات الأداء المنخفض
                low_performing_modules = self.identify_low_performing_modules()
                for module_id in low_performing_modules:
                    module_recommendations = self._generate_module_recommendations(
                        module_id)
                    recommendations.extend(module_recommendations)

                # توصيات لنماذج الذكاء الصناعي
                ai_models = self.data_store.get_active_entities("ai")
                for ai_model_id in ai_models:
                    ai_recommendations = self._generate_ai_recommendations(
                        ai_model_id)
                    recommendations.extend(ai_recommendations)

                # توصيات لقواعد البيانات
                databases = self.data_store.get_active_entities("database")
                for db_name in databases:
                    db_recommendations = self._generate_database_recommendations(
                        db_name)
                    recommendations.extend(db_recommendations)
            else:
                # تحديد نوع الكيان من معرفه
                entity_type = self._determine_entity_type(entity_id)

                if entity_type == "module":
                    recommendations = self._generate_module_recommendations(
                        entity_id)
                elif entity_type == "ai":
                    recommendations = self._generate_ai_recommendations(
                        entity_id)
                elif entity_type == "database":
                    recommendations = self._generate_database_recommendations(
                        entity_id)
                else:
                    logger.warning(f"Unknown entity type for {entity_id}")

            # ترتيب التوصيات حسب الأولوية
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            recommendations.sort(
                key=lambda r: priority_order.get(
                    r.priority, 4))

            # تحديد عدد التوصيات
            max_recommendations = self.config["recommendations"]["max_recommendations"]
            if max_recommendations > 0 and len(
                    recommendations) > max_recommendations:
                recommendations = recommendations[:max_recommendations]

            return recommendations

        except Exception as e:
            logger.error(f"Error generating performance recommendations: {e}")
            return []

    def _determine_entity_type(self, entity_id):
        """
        تحديد نوع الكيان من معرفه

        Args:
            entity_id (str): معرف الكيان

        Returns:
            str: نوع الكيان (module, ai, database)
        """
        # هذه الدالة تحدد نوع الكيان بناءً على معرفه
        # في بيئة حقيقية، يمكن استخدام طرق أكثر دقة

        if entity_id.startswith("ai_"):
            return "ai"
        elif entity_id.endswith("_db"):
            return "database"
        else:
            return "module"

    def _generate_system_recommendations(self) -> List[Recommendation]:
        """
        توليد توصيات على مستوى النظام

        Returns:
            List[Recommendation]: قائمة التوصيات
        """
        recommendations = []

        # الحصول على مقاييس النظام
        system_metrics = self.data_store.get_metrics("system", None, "1d")
        if not system_metrics:
            return recommendations

        df = pd.DataFrame(system_metrics)

        # فحص استهلاك CPU
        if "cpu.total_percent" in df.columns:
            avg_cpu = df["cpu.total_percent"].mean()
            if avg_cpu > 80:
                recommendations.append(
                    Recommendation(
                        entity_id="system",
                        metric_type="system",
                        priority="high",
                        description="High CPU usage detected. Consider scaling up CPU resources or optimizing CPU-intensive operations.",
                        expected_improvement="Reduced CPU usage and improved system responsiveness.",
                        implementation_difficulty="medium",
                        implementation_steps=[
                            "Identify CPU-intensive modules using the performance monitoring system.",
                            "Optimize code in identified modules or consider parallelization.",
                            "If optimization is not sufficient, consider scaling up CPU resources."]))

        # فحص استهلاك الذاكرة
        if "memory.percent" in df.columns:
            avg_memory = df["memory.percent"].mean()
            if avg_memory > 80:
                recommendations.append(
                    Recommendation(
                        entity_id="system",
                        metric_type="system",
                        priority="high",
                        description="High memory usage detected. Consider scaling up memory resources or optimizing memory-intensive operations.",
                        expected_improvement="Reduced memory usage and prevention of out-of-memory errors.",
                        implementation_difficulty="medium",
                        implementation_steps=[
                            "Identify memory-intensive modules using the performance monitoring system.",
                            "Check for memory leaks and optimize memory usage in identified modules.",
                            "If optimization is not sufficient, consider scaling up memory resources."]))

        # فحص استهلاك القرص
        if "disk.percent" in df.columns:
            avg_disk = df["disk.percent"].mean()
            if avg_disk > 80:
                recommendations.append(
                    Recommendation(
                        entity_id="system",
                        metric_type="system",
                        priority="medium",
                        description="High disk usage detected. Consider cleaning up unnecessary files or scaling up disk resources.",
                        expected_improvement="Reduced disk usage and prevention of disk space errors.",
                        implementation_difficulty="easy",
                        implementation_steps=[
                            "Identify large files and directories using disk usage analysis tools.",
                            "Clean up temporary files and logs.",
                            "Consider implementing a log rotation policy.",
                            "If cleanup is not sufficient, consider scaling up disk resources."]))

        return recommendations

    def _generate_module_recommendations(
            self, module_id: str) -> List[Recommendation]:
        """
        توليد توصيات للمديول

        Args:
            module_id (str): معرف المديول

        Returns:
            List[Recommendation]: قائمة التوصيات
        """
        recommendations = []

        # الحصول على مقاييس المديول
        module_metrics = self.data_store.get_metrics("module", module_id, "1d")
        if not module_metrics:
            return recommendations

        df = pd.DataFrame(module_metrics)

        # فحص وقت الاستجابة
        if "performance.response_time_ms" in df.columns:
            avg_response_time = df["performance.response_time_ms"].mean()
            if avg_response_time > 1000:  # أكثر من 1 ثانية
                recommendations.append(
                    Recommendation(
                        entity_id=module_id,
                        metric_type="module",
                        priority="high",
                        description=f"High response time detected in module {module_id}. Consider optimizing code or database queries.",
                        expected_improvement="Reduced response time and improved user experience.",
                        implementation_difficulty="medium",
                        implementation_steps=[
                            "Profile the module to identify slow operations.",
                            "Optimize database queries and indexes.",
                            "Consider caching frequently accessed data.",
                            "Optimize algorithms and data structures."]))

        # فحص معدل الأخطاء
        if "performance.error_rate" in df.columns:
            avg_error_rate = df["performance.error_rate"].mean()
            if avg_error_rate > 0.05:  # أكثر من 5%
                recommendations.append(
                    Recommendation(
                        entity_id=module_id,
                        metric_type="module",
                        priority="critical",
                        description=f"High error rate detected in module {module_id}. Investigate and fix errors.",
                        expected_improvement="Reduced error rate and improved reliability.",
                        implementation_difficulty="hard",
                        implementation_steps=[
                            "Review error logs to identify common errors.",
                            "Fix bugs and handle edge cases.",
                            "Implement better error handling and recovery mechanisms.",
                            "Add more comprehensive input validation."]))

        # فحص استهلاك CPU
        if "resources.cpu_percent" in df.columns:
            avg_cpu = df["resources.cpu_percent"].mean()
            if avg_cpu > 70:
                recommendations.append(
                    Recommendation(
                        entity_id=module_id,
                        metric_type="module",
                        priority="medium",
                        description=f"High CPU usage detected in module {module_id}. Consider optimizing CPU-intensive operations.",
                        expected_improvement="Reduced CPU usage and improved system responsiveness.",
                        implementation_difficulty="medium",
                        implementation_steps=[
                            "Profile the module to identify CPU-intensive operations.",
                            "Optimize algorithms and data structures.",
                            "Consider parallelization or asynchronous processing.",
                            "Evaluate if the module can be scaled horizontally."]))

        return recommendations

    def _generate_ai_recommendations(
            self, ai_model_id: str) -> List[Recommendation]:
        """
        توليد توصيات لنموذج الذكاء الصناعي

        Args:
            ai_model_id (str): معرف نموذج الذكاء الصناعي

        Returns:
            List[Recommendation]: قائمة التوصيات
        """
        recommendations = []

        # الحصول على مقاييس نموذج الذكاء الصناعي
        ai_metrics = self.data_store.get_metrics("ai", ai_model_id, "1d")
        if not ai_metrics:
            return recommendations

        df = pd.DataFrame(ai_metrics)

        # فحص وقت الاستدلال
        if "performance.inference_time_ms" in df.columns:
            avg_inference_time = df["performance.inference_time_ms"].mean()
            if avg_inference_time > 500:  # أكثر من 500 مللي ثانية
                recommendations.append(
                    Recommendation(
                        entity_id=ai_model_id,
                        metric_type="ai",
                        priority="high",
                        description=f"High inference time detected in AI model {ai_model_id}. Consider model optimization or hardware acceleration.",
                        expected_improvement="Reduced inference time and improved user experience.",
                        implementation_difficulty="hard",
                        implementation_steps=[
                            "Consider model quantization to reduce model size and improve inference speed.",
                            "Evaluate hardware acceleration options (GPU, TPU).",
                            "Optimize batch processing for inference.",
                            "Consider model distillation or pruning to create a smaller, faster model."]))

        # فحص دقة النموذج
        if "performance.accuracy" in df.columns:
            avg_accuracy = df["performance.accuracy"].mean()
            if avg_accuracy < 0.8:  # أقل من 80%
                recommendations.append(
                    Recommendation(
                        entity_id=ai_model_id,
                        metric_type="ai",
                        priority="high",
                        description=f"Low accuracy detected in AI model {ai_model_id}. Consider model retraining or improvement.",
                        expected_improvement="Improved model accuracy and reliability.",
                        implementation_difficulty="hard",
                        implementation_steps=[
                            "Analyze model errors to identify patterns.",
                            "Collect more training data, especially for error cases.",
                            "Consider feature engineering or model architecture changes.",
                            "Retrain the model with improved data and parameters."]))

        # فحص استهلاك GPU
        if "resources.gpu_percent" in df.columns:
            avg_gpu = df["resources.gpu_percent"].mean()
            if avg_gpu > 80:
                recommendations.append(
                    Recommendation(
                        entity_id=ai_model_id,
                        metric_type="ai",
                        priority="medium",
                        description=f"High GPU usage detected in AI model {ai_model_id}. Consider optimizing GPU utilization or scaling GPU resources.",
                        expected_improvement="Optimized GPU usage and improved inference throughput.",
                        implementation_difficulty="medium",
                        implementation_steps=[
                            "Optimize batch size for inference.",
                            "Consider model quantization to reduce GPU memory usage.",
                            "Evaluate if multiple models can share the same GPU.",
                            "If optimization is not sufficient, consider scaling up GPU resources."]))

        return recommendations

    def _generate_database_recommendations(
            self, db_name: str) -> List[Recommendation]:
        """
        توليد توصيات لقاعدة البيانات

        Args:
            db_name (str): اسم قاعدة البيانات

        Returns:
            List[Recommendation]: قائمة التوصيات
        """
        recommendations = []

        # الحصول على مقاييس قاعدة البيانات
        db_metrics = self.data_store.get_metrics("database", db_name, "1d")
        if not db_metrics:
            return recommendations

        df = pd.DataFrame(db_metrics)

        # فحص وقت الاستعلام
        if "performance.query_time_ms" in df.columns:
            avg_query_time = df["performance.query_time_ms"].mean()
            if avg_query_time > 100:  # أكثر من 100 مللي ثانية
                recommendations.append(
                    Recommendation(
                        entity_id=db_name,
                        metric_type="database",
                        priority="high",
                        description=f"High query time detected in database {db_name}. Consider query optimization or index creation.",
                        expected_improvement="Reduced query time and improved system responsiveness.",
                        implementation_difficulty="medium",
                        implementation_steps=[
                            "Identify slow queries using database monitoring tools.",
                            "Analyze query execution plans and optimize queries.",
                            "Create appropriate indexes for frequently queried columns.",
                            "Consider denormalization for read-heavy workloads."]))

        # فحص عدد الاتصالات النشطة
        if "performance.active_connections" in df.columns:
            avg_connections = df["performance.active_connections"].mean()
            max_connections = df["resources.connection_limit"].mean(
            ) if "resources.connection_limit" in df.columns else 100
            if avg_connections > 0.7 * max_connections:  # أكثر من 70% من الحد الأقصى
                recommendations.append(
                    Recommendation(
                        entity_id=db_name,
                        metric_type="database",
                        priority="medium",
                        description=f"High number of active connections detected in database {db_name}. Consider connection pooling or scaling.",
                        expected_improvement="Optimized connection usage and prevention of connection errors.",
                        implementation_difficulty="medium",
                        implementation_steps=[
                            "Implement or optimize connection pooling.",
                            "Review application code to ensure connections are properly closed.",
                            "Consider increasing the maximum number of connections if resources allow.",
                            "Evaluate if read-heavy workloads can be offloaded to read replicas."]))

        # فحص معدل الأخطاء
        if "performance.error_rate" in df.columns:
            avg_error_rate = df["performance.error_rate"].mean()
            if avg_error_rate > 0.01:  # أكثر من 1%
                recommendations.append(
                    Recommendation(
                        entity_id=db_name,
                        metric_type="database",
                        priority="critical",
                        description=f"High error rate detected in database {db_name}. Investigate and fix database errors.",
                        expected_improvement="Reduced error rate and improved reliability.",
                        implementation_difficulty="hard",
                        implementation_steps=[
                            "Review database error logs to identify common errors.",
                            "Fix data integrity issues and constraints.",
                            "Implement better error handling in application code.",
                            "Consider database maintenance operations (vacuum, reindex)."]))

        return recommendations

    def detect_data_drift(
            self,
            reference_data,
            current_data,
            column_mapping=None):
        """
        اكتشاف انحراف البيانات باستخدام Evidently

        Args:
            reference_data: البيانات المرجعية
            current_data: البيانات الحالية
            column_mapping: تعيين الأعمدة

        Returns:
            Dashboard: لوحة معلومات انحراف البيانات
        """
        if not EVIDENTLY_AVAILABLE:
            logger.warning(
                "Evidently library not available. Cannot detect data drift.")
            return None

        try:
            # إنشاء لوحة معلومات انحراف البيانات
            dashboard = Dashboard(tabs=[DataDriftTab()])
            dashboard.calculate(
                reference_data,
                current_data,
                column_mapping=column_mapping)
            return dashboard
        except Exception as e:
            logger.error(f"Error detecting data drift: {e}")
            return None

    def detect_target_drift(
            self,
            reference_data,
            current_data,
            column_mapping=None):
        """
        اكتشاف انحراف الهدف باستخدام Evidently

        Args:
            reference_data: البيانات المرجعية
            current_data: البيانات الحالية
            column_mapping: تعيين الأعمدة

        Returns:
            Dashboard: لوحة معلومات انحراف الهدف
        """
        if not EVIDENTLY_AVAILABLE:
            logger.warning(
                "Evidently library not available. Cannot detect target drift.")
            return None

        try:
            # إنشاء لوحة معلومات انحراف الهدف
            dashboard = Dashboard(tabs=[CatTargetDriftTab()])
            dashboard.calculate(
                reference_data,
                current_data,
                column_mapping=column_mapping)
            return dashboard
        except Exception as e:
            logger.error(f"Error detecting target drift: {e}")
            return None
