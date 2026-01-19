"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/plant_disease/model_learning_system.py

نظام التعلم من نتائج اختبار النماذج وتوليد توصيات آلية لتحسين الأداء
يوفر هذا النظام آليات لتحليل نتائج اختبار النماذج واكتشاف الأنماط وتوليد توصيات لتحسين الأداء

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
"""

import os
import json

import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('model_learning_system')


class ModelLearningSystem:
    """نظام التعلم من نتائج اختبار النماذج وتوليد توصيات آلية لتحسين الأداء"""

    def __init__(self, history_dir=None):
        """
        تهيئة نظام التعلم من النماذج

        المعلمات:
            history_dir: مسار مجلد سجل التعلم (اختياري)
        """
        self.history_dir = history_dir or Path("/home/ubuntu/gaara_scan_ai_final_4.2/reports/learning")

        # إنشاء مجلد السجل إذا لم يكن موجوداً
        os.makedirs(self.history_dir, exist_ok=True)

        # سجل التعلم
        self.learning_history = []

        # تحميل سجل التعلم السابق
        self.load_learning_history()

        logger.info("تم تهيئة نظام التعلم من النماذج")

    def load_learning_history(self):
        """تحميل سجل التعلم السابق"""

        try:
            history_file = self.history_dir / "learning_history.json"

            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.learning_history = json.load(f)

                logger.info(f"تم تحميل سجل التعلم السابق: {len(self.learning_history)} سجل")
            else:
                logger.info("لم يتم العثور على سجل تعلم سابق")

        except Exception as e:
            logger.error(f"خطأ في تحميل سجل التعلم السابق: {e}")

    def save_learning_history(self):
        """حفظ سجل التعلم الحالي"""

        try:
            history_file = self.history_dir / "learning_history.json"

            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_history, f, ensure_ascii=False, indent=2)

            logger.info(f"تم حفظ سجل التعلم: {len(self.learning_history)} سجل")

        except Exception as e:
            logger.error(f"خطأ في حفظ سجل التعلم: {e}")

    def analyze_benchmark_results(self, benchmark_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل نتائج اختبار النماذج واكتشاف الأنماط وتوليد توصيات

        المعلمات:
            benchmark_results: نتائج اختبار النماذج

        العائد:
            قاموس يحتوي على نتائج التحليل والتوصيات
        """
        try:
            # التحقق من صحة البيانات
            if not benchmark_results or not isinstance(benchmark_results, dict):
                return {
                    "error": "بيانات غير صالحة للتحليل",
                    "timestamp": datetime.now().isoformat()
                }

            # استخراج بيانات النماذج
            models_data = {}

            for model_name, result in benchmark_results.items():
                if "error" in result:
                    continue

                # استخراج مقاييس الأداء
                if "metrics" in result:
                    metrics = result["metrics"]

                    models_data[model_name] = {
                        "accuracy": metrics.get("accuracy", {}).get("mean", 0),
                        "precision": metrics.get("precision", {}).get("mean", 0),
                        "recall": metrics.get("recall", {}).get("mean", 0),
                        "f1_score": metrics.get("f1_score", {}).get("mean", 0),
                        "error_rate": metrics.get("error_rate", {}).get("mean", 0),
                        "avg_confidence": metrics.get("avg_confidence", {}).get("mean", 0)
                    }

                # استخراج مقاييس السرعة
                if "timing" in result:
                    timing = result["timing"]

                    models_data[model_name].update({
                        "fps": timing.get("fps", {}).get("mean", 0),
                        "avg_inference_time": timing.get("avg_inference_time", {}).get("mean", 0),
                        "total_time": timing.get("total_time", {}).get("mean", 0)
                    })

                # استخراج مقاييس استهلاك الموارد
                if "resource_usage" in result:
                    resources = result["resource_usage"]

                    models_data[model_name].update({
                        "memory_used": resources.get("memory_used", {}).get("mean", 0),
                        "cpu_usage": resources.get("cpu_usage", {}).get("mean", 0),
                        "gpu_memory_used": resources.get("gpu_memory_used", {}).get("mean", 0) if "gpu_memory_used" in resources else 0
                    })

                # استخراج مقاييس الاستقرار
                if "stability" in result:
                    stability = result["stability"]

                    models_data[model_name].update({
                        "accuracy_cv": stability.get("accuracy_cv", 0),
                        "timing_cv": stability.get("timing_cv", 0),
                        "consistency_score": stability.get("consistency_score", 0)
                    })

            # تحويل البيانات إلى DataFrame للتحليل
            df = pd.DataFrame.from_dict(models_data, orient='index')

            # تحليل البيانات
            analysis_results = self.analyze_data(df)

            # اكتشاف الأنماط
            patterns = self.discover_patterns(df)

            # توليد التوصيات
            recommendations = self.generate_recommendations(df, analysis_results, patterns)

            # إنشاء نتيجة التحليل
            learning_result = {
                "timestamp": datetime.now().isoformat(),
                "models_analyzed": len(models_data),
                "analysis": analysis_results,
                "patterns": patterns,
                "recommendations": recommendations
            }

            # إضافة النتيجة إلى سجل التعلم
            self.learning_history.append(learning_result)

            # حفظ سجل التعلم
            self.save_learning_history()

            return learning_result

        except Exception as e:
            logger.error(f"خطأ في تحليل نتائج الاختبار: {e}")
            return {
                "error": f"خطأ في تحليل نتائج الاختبار: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def analyze_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        تحليل بيانات النماذج

        المعلمات:
            df: DataFrame يحتوي على بيانات النماذج

        العائد:
            قاموس يحتوي على نتائج التحليل
        """
        analysis = {}

        # التحليل الإحصائي الأساسي
        analysis["statistics"] = {
            "accuracy": {
                "mean": float(df["accuracy"].mean()),
                "std": float(df["accuracy"].std()),
                "min": float(df["accuracy"].min()),
                "max": float(df["accuracy"].max())
            },
            "fps": {
                "mean": float(df["fps"].mean()),
                "std": float(df["fps"].std()),
                "min": float(df["fps"].min()),
                "max": float(df["fps"].max())
            },
            "memory_used": {
                "mean": float(df["memory_used"].mean()),
                "std": float(df["memory_used"].std()),
                "min": float(df["memory_used"].min()),
                "max": float(df["memory_used"].max())
            }
        }

        # تحليل العلاقات
        correlations = {}

        # العلاقة بين الدقة والسرعة
        correlations["accuracy_vs_fps"] = float(df["accuracy"].corr(df["fps"]))

        # العلاقة بين الدقة واستهلاك الذاكرة
        correlations["accuracy_vs_memory"] = float(df["accuracy"].corr(df["memory_used"]))

        # العلاقة بين السرعة واستهلاك الذاكرة
        correlations["fps_vs_memory"] = float(df["fps"].corr(df["memory_used"]))

        analysis["correlations"] = correlations

        # تحليل أفضل النماذج
        best_models = {}

        # أفضل نموذج من حيث الدقة
        best_accuracy_idx = df["accuracy"].idxmax()
        best_models["accuracy"] = {
            "model": best_accuracy_idx,
            "accuracy": float(df.loc[best_accuracy_idx, "accuracy"]),
            "fps": float(df.loc[best_accuracy_idx, "fps"]),
            "memory_used": float(df.loc[best_accuracy_idx, "memory_used"])
        }

        # أفضل نموذج من حيث السرعة
        best_fps_idx = df["fps"].idxmax()
        best_models["fps"] = {
            "model": best_fps_idx,
            "accuracy": float(df.loc[best_fps_idx, "accuracy"]),
            "fps": float(df.loc[best_fps_idx, "fps"]),
            "memory_used": float(df.loc[best_fps_idx, "memory_used"])
        }

        # أفضل نموذج من حيث استهلاك الذاكرة
        best_memory_idx = df["memory_used"].idxmin()
        best_models["memory"] = {
            "model": best_memory_idx,
            "accuracy": float(df.loc[best_memory_idx, "accuracy"]),
            "fps": float(df.loc[best_memory_idx, "fps"]),
            "memory_used": float(df.loc[best_memory_idx, "memory_used"])
        }

        analysis["best_models"] = best_models

        return analysis

    def discover_patterns(self, df: pd.DataFrame) -> List[str]:
        """
        اكتشاف الأنماط في بيانات النماذج

        المعلمات:
            df: DataFrame يحتوي على بيانات النماذج

        العائد:
            قائمة بالأنماط المكتشفة
        """
        patterns = []

        # نمط العلاقة بين الدقة والسرعة
        acc_fps_corr = df["accuracy"].corr(df["fps"])
        if acc_fps_corr > 0.7:
            patterns.append("هناك علاقة إيجابية قوية بين الدقة والسرعة، مما يشير إلى أن النماذج الأكثر دقة هي أيضاً الأسرع")
        elif acc_fps_corr < -0.7:
            patterns.append("هناك علاقة سلبية قوية بين الدقة والسرعة، مما يشير إلى وجود مقايضة بين الدقة والسرعة")

        # نمط العلاقة بين الدقة واستهلاك الذاكرة
        acc_mem_corr = df["accuracy"].corr(df["memory_used"])
        if acc_mem_corr > 0.7:
            patterns.append("هناك علاقة إيجابية قوية بين الدقة واستهلاك الذاكرة، مما يشير إلى أن النماذج الأكثر دقة تستهلك ذاكرة أكبر")
        elif acc_mem_corr < -0.7:
            patterns.append("هناك علاقة سلبية قوية بين الدقة واستهلاك الذاكرة، مما يشير إلى أن النماذج الأكثر دقة تستهلك ذاكرة أقل")

        # نمط تأثير نوع النموذج على الأداء
        model_types = [idx.split('_')[0] for idx in df.index]
        unique_types = set(model_types)

        for model_type in unique_types:
            type_indices = [idx for idx in df.index if idx.startswith(model_type)]
            if len(type_indices) > 1:
                type_df = df.loc[type_indices]

                avg_accuracy = type_df["accuracy"].mean()
                avg_fps = type_df["fps"].mean()

                overall_avg_accuracy = df["accuracy"].mean()
                overall_avg_fps = df["fps"].mean()

                if avg_accuracy > overall_avg_accuracy * 1.2:
                    patterns.append(f"نماذج {model_type} تظهر أداءً أفضل من المتوسط من حيث الدقة بنسبة {((avg_accuracy / overall_avg_accuracy) - 1) * 100:.1f}%")

                if avg_fps > overall_avg_fps * 1.2:
                    patterns.append(f"نماذج {model_type} تظهر أداءً أفضل من المتوسط من حيث السرعة بنسبة {((avg_fps / overall_avg_fps) - 1) * 100:.1f}%")

        # نمط الاستقرار
        if "consistency_score" in df.columns:
            high_consistency = df[df["consistency_score"] > 0.9].index.tolist()
            if high_consistency:
                patterns.append(f"النماذج التالية تظهر استقراراً عالياً في الأداء: {', '.join(high_consistency)}")

            low_consistency = df[df["consistency_score"] < 0.5].index.tolist()
            if low_consistency:
                patterns.append(f"النماذج التالية تظهر تبايناً كبيراً في الأداء: {', '.join(low_consistency)}")

        return patterns

    def generate_recommendations(self, df: pd.DataFrame, analysis: Dict[str, Any], patterns: List[str]) -> List[str]:
        """
        توليد توصيات لتحسين الأداء

        المعلمات:
            df: DataFrame يحتوي على بيانات النماذج
            analysis: نتائج التحليل
            patterns: الأنماط المكتشفة

        العائد:
            قائمة بالتوصيات
        """
        recommendations = []

        # توصيات بناءً على أفضل النماذج
        best_accuracy_model = analysis["best_models"]["accuracy"]["model"]
        best_fps_model = analysis["best_models"]["fps"]["model"]
        best_memory_model = analysis["best_models"]["memory"]["model"]

        recommendations.append(f"للتطبيقات التي تتطلب دقة عالية، استخدم نموذج {best_accuracy_model} (الدقة: {analysis['best_models']['accuracy']['accuracy']*100:.1f}%)")
        recommendations.append(f"للتطبيقات التي تتطلب استجابة فورية، استخدم نموذج {best_fps_model} (السرعة: {analysis['best_models']['fps']['fps']:.1f} FPS)")
        recommendations.append(f"للأجهزة ذات الموارد المحدودة، استخدم نموذج {best_memory_model} (استهلاك الذاكرة: {analysis['best_models']['memory']['memory_used']:.2f} GB)")

        # توصيات بناءً على العلاقات
        acc_fps_corr = analysis["correlations"]["accuracy_vs_fps"]
        if acc_fps_corr < -0.5:
            recommendations.append("هناك مقايضة واضحة بين الدقة والسرعة. حدد أولوياتك بناءً على متطلبات التطبيق")

        # توصيات بناءً على أنواع النماذج
        model_types = {}
        for model_name in df.index:
            model_type = model_name.split('_')[0]
            if model_type not in model_types:
                model_types[model_type] = []
            model_types[model_type].append(model_name)

        for model_type, models in model_types.items():
            if len(models) > 1:
                type_df = df.loc[models]
                best_model = type_df["accuracy"].idxmax()

                if model_type == "mobilenet":
                    recommendations.append(f"نماذج MobileNet مناسبة للأجهزة المحمولة، ونوصي باستخدام {best_model}")
                elif model_type == "vit":
                    recommendations.append(f"نماذج Vision Transformer توفر دقة عالية، ونوصي باستخدام {best_model}")
                elif model_type == "cropnet":
                    recommendations.append(f"نماذج CropNet مخصصة للمحاصيل الزراعية، ونوصي باستخدام {best_model}")

        # توصيات للتحسين
        low_accuracy_models = df[df["accuracy"] < 0.7].index.tolist()
        if low_accuracy_models:
            recommendations.append(f"النماذج التالية تحتاج إلى تحسين الدقة: {', '.join(low_accuracy_models)}")

        slow_models = df[df["fps"] < 5].index.tolist()
        if slow_models:
            recommendations.append(f"النماذج التالية تحتاج إلى تحسين السرعة: {', '.join(slow_models)}")

        # توصيات للاستخدام المتوازن
        balanced_score = df["accuracy"] * 0.6 + (df["fps"] / df["fps"].max()) * 0.3 - (df["memory_used"] / df["memory_used"].max()) * 0.1
        balanced_model = balanced_score.idxmax()

        recommendations.append(f"للتوازن الأمثل بين الدقة والسرعة واستهلاك الموارد، نوصي باستخدام نموذج {balanced_model}")

        # توصيات للتعلم المستمر
        recommendations.append("قم بتدريب النماذج على مجموعات بيانات أكبر وأكثر تنوعاً لتحسين الدقة والتعميم")
        recommendations.append("استخدم تقنيات تقليل حجم النموذج مثل التقطير (distillation) وتقليم الأوزان (pruning) لتحسين السرعة واستهلاك الموارد")

        return recommendations

    def get_learning_history(self) -> List[Dict[str, Any]]:
        """
        الحصول على سجل التعلم

        العائد:
            قائمة بسجلات التعلم
        """
        return self.learning_history

    def get_latest_learning(self) -> Optional[Dict[str, Any]]:
        """
        الحصول على آخر نتيجة تعلم

        العائد:
            آخر نتيجة تعلم أو None إذا لم يوجد
        """
        if self.learning_history:
            return self.learning_history[-1]
        return None

    def clear_learning_history(self) -> bool:
        """
        مسح سجل التعلم

        العائد:
            نجاح العملية
        """
        try:
            self.learning_history = []
            self.save_learning_history()
            return True
        except Exception as e:
            logger.error(f"خطأ في مسح سجل التعلم: {e}")
            return False
