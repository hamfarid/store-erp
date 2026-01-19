"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/plant_disease/model_comparison_api.py

واجهة برمجية موحدة لاختبار ومقارنة نماذج تشخيص أمراض النباتات
توفر هذه الواجهة نقاط نهاية للتفاعل مع نظام اختبار ومقارنة النماذج من خلال الواجهة الأمامية
وتتيح للمستخدمين اختيار النماذج وتحميل الصور وعرض نتائج المقارنات بشكل ديناميكي

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
تاريخ التعديل: 30 مايو 2025 - إضافة دعم محلل الانتباه ومحلل المتانة
"""

import os
import json
import logging
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('model_comparison_api')


class ModelComparisonAPI:
    """واجهة برمجية موحدة لاختبار ومقارنة النماذج"""

    def __init__(self, processor, benchmark_system, learning_system=None,
                 attention_analyzer=None, robustness_analyzer=None):
        """
        تهيئة الواجهة البرمجية

        المعلمات:
            processor: معالج تشخيص أمراض النباتات المتقدم
            benchmark_system: نظام اختبار ومقارنة النماذج
            learning_system: نظام التعلم من النماذج (اختياري)
            attention_analyzer: محلل أنماط الانتباه (اختياري)
            robustness_analyzer: محلل قوة ومتانة النماذج (اختياري)
        """
        self.processor = processor
        self.benchmark_system = benchmark_system
        self.learning_system = learning_system
        self.attention_analyzer = attention_analyzer
        self.robustness_analyzer = robustness_analyzer
        self.upload_dir = Path("/home/ubuntu/gaara_scan_ai_final_4.2/uploads/test_images")
        self.results_dir = Path("/home/ubuntu/gaara_scan_ai_final_4.2/reports/benchmarks")
        self.attention_dir = Path("/home/ubuntu/gaara_scan_ai_final_4.2/reports/attention")
        self.robustness_dir = Path("/home/ubuntu/gaara_scan_ai_final_4.2/reports/robustness")

        # إنشاء المجلدات إذا لم تكن موجودة
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.attention_dir, exist_ok=True)
        os.makedirs(self.robustness_dir, exist_ok=True)

        logger.info("تم تهيئة واجهة اختبار ومقارنة النماذج")

    def get_available_models(self) -> Dict[str, Any]:
        """
        الحصول على قائمة النماذج المتاحة

        العائد:
            قاموس يحتوي على قائمة النماذج المتاحة وتفاصيلها
        """
        models = {}

        for model_name in self.processor.models.keys():
            models[model_name] = self.get_model_details(model_name)

        return {
            "count": len(models),
            "models": models
        }

    def get_model_details(self, model_name: str) -> Dict[str, Any]:
        """
        الحصول على تفاصيل نموذج محدد

        المعلمات:
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على تفاصيل النموذج
        """
        if model_name not in self.processor.models:
            return {"error": f"النموذج {model_name} غير متاح"}

        # الحصول على تفاصيل النموذج
        model = self.processor.models[model_name]
        model_type = self._get_model_type(model_name)

        return {
            "name": model_name,
            "type": model_type,
            "parameters": self._get_model_parameters(model, model_type),
            "input_shape": self._get_model_input_shape(model, model_type),
            "output_shape": self._get_model_output_shape(model, model_type),
            "description": self._get_model_description(model_name, model_type)
        }

    def upload_test_images(self, images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        تحميل صور للاختبار

        المعلمات:
            images: قائمة بالصور (كل صورة عبارة عن قاموس يحتوي على البيانات والتسمية)

        العائد:
            قاموس يحتوي على مسارات الصور المحملة
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = self.upload_dir / f"session_{timestamp}"
        os.makedirs(session_dir, exist_ok=True)

        image_paths = []
        ground_truth = []

        for i, img_data in enumerate(images):
            try:
                # استخراج بيانات الصورة
                if "base64_data" in img_data:
                    # تحويل البيانات من Base64 إلى صورة
                    img_binary = base64.b64decode(img_data["base64_data"])
                    img = Image.open(BytesIO(img_binary))
                elif "url" in img_data:
                    # تحميل الصورة من URL
                    from urllib.request import urlopen
                    img = Image.open(urlopen(img_data["url"]))
                else:
                    continue

                # حفظ الصورة
                label = img_data.get("label", -1)
                img_path = session_dir / f"image_{i:04d}_label_{label}.jpg"
                img.save(img_path)

                image_paths.append(str(img_path))
                ground_truth.append(int(label))

            except Exception as e:
                logger.error(f"خطأ في تحميل الصورة {i}: {e}")

        return {
            "session_id": timestamp,
            "image_count": len(image_paths),
            "image_paths": image_paths,
            "ground_truth": ground_truth
        }

    def run_benchmark(self, image_paths: List[str], ground_truth: List[int],
                      models: Optional[List[str]] = None, iterations: int = 3) -> Dict[str, Any]:
        """
        تشغيل اختبار للنماذج

        المعلمات:
            image_paths: قائمة بمسارات الصور للاختبار
            ground_truth: التسميات الصحيحة للصور
            models: قائمة بأسماء النماذج للاختبار (اختياري)
            iterations: عدد مرات تكرار الاختبار لكل نموذج

        العائد:
            قاموس يحتوي على نتائج الاختبار
        """
        try:
            # التحقق من وجود الصور
            valid_paths = [path for path in image_paths if os.path.exists(path)]

            if not valid_paths:
                return {"error": "لا توجد صور صالحة للاختبار"}

            # التحقق من تطابق عدد الصور مع التسميات
            if len(valid_paths) != len(ground_truth):
                return {"error": "عدد الصور لا يتطابق مع عدد التسميات"}

            # تشغيل الاختبار
            results = self.benchmark_system.run_comprehensive_benchmark(
                valid_paths, ground_truth, models, iterations
            )

            # حفظ النتائج
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.results_dir / f"benchmark_report_{timestamp}.json"

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            # إنشاء المخططات البيانية
            plot_path = self.benchmark_system.create_visualizations()

            # التعلم من النتائج إذا كان نظام التعلم متاحاً
            learning_results = None
            if self.learning_system:
                learning_results = self.learning_system.analyze_benchmark_results(results)

            return {
                "timestamp": timestamp,
                "results": results,
                "report_path": str(report_path),
                "plot_path": plot_path,
                "learning_results": learning_results
            }

        except Exception as e:
            logger.error(f"خطأ في تشغيل الاختبار: {e}")
            return {"error": f"خطأ في تشغيل الاختبار: {str(e)}"}

    def get_previous_benchmarks(self) -> Dict[str, Any]:
        """
        الحصول على قائمة الاختبارات السابقة

        العائد:
            قاموس يحتوي على قائمة الاختبارات السابقة
        """
        benchmarks = []

        try:
            for file in self.results_dir.glob("benchmark_report_*.json"):
                try:
                    timestamp = file.stem.replace("benchmark_report_", "")
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # استخراج معلومات موجزة
                    models_tested = list(data.keys()) if isinstance(data, dict) else []

                    benchmarks.append({
                        "timestamp": timestamp,
                        "path": str(file),
                        "models_count": len(models_tested),
                        "models_tested": models_tested
                    })
                except Exception as e:
                    logger.error(f"خطأ في قراءة ملف الاختبار {file}: {e}")

        except Exception as e:
            logger.error(f"خطأ في الحصول على قائمة الاختبارات السابقة: {e}")

        return {
            "count": len(benchmarks),
            "benchmarks": sorted(benchmarks, key=lambda x: x["timestamp"], reverse=True)
        }

    def get_benchmark_details(self, benchmark_id: str) -> Dict[str, Any]:
        """
        الحصول على تفاصيل اختبار محدد

        المعلمات:
            benchmark_id: معرف الاختبار (التاريخ والوقت)

        العائد:
            قاموس يحتوي على تفاصيل الاختبار
        """
        report_path = self.results_dir / f"benchmark_report_{benchmark_id}.json"
        plot_path = self.results_dir / f"model_comparison_{benchmark_id}.png"

        if not report_path.exists():
            return {"error": f"الاختبار {benchmark_id} غير موجود"}

        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return {
                "timestamp": benchmark_id,
                "results": data,
                "report_path": str(report_path),
                "plot_path": str(plot_path) if plot_path.exists() else None
            }

        except Exception as e:
            logger.error(f"خطأ في قراءة تفاصيل الاختبار {benchmark_id}: {e}")
            return {"error": f"خطأ في قراءة تفاصيل الاختبار: {str(e)}"}

    def predict_with_model(self, image_path: str, model_name: str) -> Dict[str, Any]:
        """
        التنبؤ باستخدام نموذج محدد

        المعلمات:
            image_path: مسار الصورة
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على نتيجة التنبؤ
        """
        try:
            result = self.processor.predict_single_model(image_path, model_name)
            return result
        except Exception as e:
            logger.error(f"خطأ في التنبؤ باستخدام {model_name}: {e}")
            return {"error": f"خطأ في التنبؤ: {str(e)}"}

    def predict_with_ensemble(self, image_path: str, models: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        التنبؤ باستخدام مجموعة نماذج

        المعلمات:
            image_path: مسار الصورة
            models: قائمة بأسماء النماذج (اختياري)

        العائد:
            قاموس يحتوي على نتيجة التنبؤ المجمع
        """
        try:
            result = self.processor.ensemble_predict(image_path, models)
            return result
        except Exception as e:
            logger.error(f"خطأ في التنبؤ المجمع: {e}")
            return {"error": f"خطأ في التنبؤ المجمع: {str(e)}"}

    def learn_from_results(self, benchmark_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        التعلم من نتائج الاختبار

        المعلمات:
            benchmark_results: نتائج الاختبار

        العائد:
            قاموس يحتوي على نتائج التعلم
        """
        if not self.learning_system:
            return {"error": "نظام التعلم غير متاح"}

        try:
            return self.learning_system.analyze_benchmark_results(benchmark_results)
        except Exception as e:
            logger.error(f"خطأ في التعلم من النتائج: {e}")
            return {"error": f"خطأ في التعلم من النتائج: {str(e)}"}

    # ===== وظائف محلل الانتباه =====

    def analyze_attention(self, image_paths: List[str], model_name: str) -> Dict[str, Any]:
        """
        تحليل أنماط الانتباه في النموذج

        المعلمات:
            image_paths: قائمة بمسارات الصور للتحليل
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على نتائج تحليل الانتباه
        """
        if not self.attention_analyzer:
            return {"error": "محلل الانتباه غير متاح"}

        try:
            # التحقق من وجود الصور
            valid_paths = [path for path in image_paths if os.path.exists(path)]

            if not valid_paths:
                return {"error": "لا توجد صور صالحة للتحليل"}

            # تحليل أنماط الانتباه
            attention_results = self.attention_analyzer.analyze_attention_patterns(model_name, valid_paths)

            # حفظ النتائج
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.attention_dir / f"attention_report_{model_name}_{timestamp}.json"

            # تحويل المصفوفات إلى قوائم للتخزين في JSON
            serializable_results = self._make_serializable(attention_results)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, ensure_ascii=False, indent=2)

            # استخراج مسارات التفسيرات البصرية
            visual_explanations = {}
            for img_id, img_data in attention_results.get("visual_explanations", {}).items():
                if img_data and "explanation_path" in img_data and img_data["explanation_path"]:
                    visual_explanations[img_id] = img_data["explanation_path"]

            return {
                "timestamp": timestamp,
                "model_name": model_name,
                "attention_statistics": attention_results.get("attention_statistics", {}),
                "focus_regions": attention_results.get("focus_regions", {}),
                "visual_explanations": visual_explanations,
                "report_path": str(report_path)
            }

        except Exception as e:
            logger.error(f"خطأ في تحليل أنماط الانتباه: {e}")
            return {"error": f"خطأ في تحليل أنماط الانتباه: {str(e)}"}

    def compare_attention_patterns(self, models: List[str], image_paths: List[str]) -> Dict[str, Any]:
        """
        مقارنة أنماط الانتباه بين النماذج المختلفة

        المعلمات:
            models: قائمة بأسماء النماذج للمقارنة
            image_paths: قائمة بمسارات الصور للتحليل

        العائد:
            قاموس يحتوي على نتائج المقارنة
        """
        if not self.attention_analyzer:
            return {"error": "محلل الانتباه غير متاح"}

        try:
            # التحقق من وجود الصور
            valid_paths = [path for path in image_paths if os.path.exists(path)]

            if not valid_paths:
                return {"error": "لا توجد صور صالحة للتحليل"}

            # تحليل أنماط الانتباه لكل نموذج
            for model_name in models:
                self.attention_analyzer.analyze_attention_patterns(model_name, valid_paths)

            # إنشاء مقارنة بين النماذج
            self.attention_analyzer.create_attention_comparison(models)

            # الحصول على مسار مخطط المقارنة
            comparison_chart_path = "/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/attention_comparison.png"

            # حفظ النتائج
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.attention_dir / f"attention_comparison_{timestamp}.json"

            comparison_data = {}
            for model_name in models:
                if model_name in self.attention_analyzer.attention_data:
                    stats = self.attention_analyzer.attention_data[model_name].get("attention_statistics", {})
                    comparison_data[model_name] = stats

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(comparison_data, f, ensure_ascii=False, indent=2)

            return {
                "timestamp": timestamp,
                "models_compared": models,
                "comparison_data": comparison_data,
                "comparison_chart_path": comparison_chart_path if os.path.exists(comparison_chart_path) else None,
                "report_path": str(report_path)
            }

        except Exception as e:
            logger.error(f"خطأ في مقارنة أنماط الانتباه: {e}")
            return {"error": f"خطأ في مقارنة أنماط الانتباه: {str(e)}"}

    def get_attention_reports(self) -> Dict[str, Any]:
        """
        الحصول على قائمة تقارير تحليل الانتباه السابقة

        العائد:
            قاموس يحتوي على قائمة التقارير
        """
        reports = []

        try:
            for file in self.attention_dir.glob("attention_report_*.json"):
                try:
                    filename = file.stem
                    parts = filename.split('_')
                    if len(parts) >= 4:
                        model_name = parts[2]
                        timestamp = '_'.join(parts[3:])

                        reports.append({
                            "model_name": model_name,
                            "timestamp": timestamp,
                            "path": str(file)
                        })
                except Exception as e:
                    logger.error(f"خطأ في قراءة ملف تقرير الانتباه {file}: {e}")

            # تقارير المقارنة
            for file in self.attention_dir.glob("attention_comparison_*.json"):
                try:
                    timestamp = file.stem.replace("attention_comparison_", "")

                    reports.append({
                        "model_name": "مقارنة",
                        "timestamp": timestamp,
                        "path": str(file)
                    })
                except Exception as e:
                    logger.error(f"خطأ في قراءة ملف مقارنة الانتباه {file}: {e}")

        except Exception as e:
            logger.error(f"خطأ في الحصول على قائمة تقارير الانتباه: {e}")

        return {
            "count": len(reports),
            "reports": sorted(reports, key=lambda x: x["timestamp"], reverse=True)
        }

    # ===== وظائف محلل المتانة =====

    def test_model_robustness(self, image_paths: List[str], model_name: str) -> Dict[str, Any]:
        """
        اختبار قوة ومتانة النموذج

        المعلمات:
            image_paths: قائمة بمسارات الصور للاختبار
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على نتائج اختبار المتانة
        """
        if not self.robustness_analyzer:
            return {"error": "محلل المتانة غير متاح"}

        try:
            # التحقق من وجود الصور
            valid_paths = [path for path in image_paths if os.path.exists(path)]

            if not valid_paths:
                return {"error": "لا توجد صور صالحة للاختبار"}

            # اختبار المتانة الشامل
            robustness_results = self.robustness_analyzer.test_comprehensive_robustness(model_name, valid_paths)

            # حفظ النتائج
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.robustness_dir / f"robustness_report_{model_name}_{timestamp}.json"

            # تحويل المصفوفات إلى قوائم للتخزين في JSON
            serializable_results = self._make_serializable(robustness_results)

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, ensure_ascii=False, indent=2)

            # الحصول على مسارات المخططات البيانية
            chart_paths = {
                "radar_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_robustness_radar.png",
                "noise_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_noise_robustness_chart.png",
                "brightness_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_brightness_robustness_chart.png",
                "contrast_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_contrast_robustness_chart.png",
                "rotation_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_rotation_robustness_chart.png",
                "blur_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_blur_robustness_chart.png",
                "scale_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_scale_robustness_chart.png",
                "occlusion_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_occlusion_robustness_chart.png",
                "compression_chart": f"/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/{model_name}_compression_robustness_chart.png"
            }

            # التحقق من وجود المخططات
            valid_charts = {}
            for chart_name, chart_path in chart_paths.items():
                if os.path.exists(chart_path):
                    valid_charts[chart_name] = chart_path

            return {
                "timestamp": timestamp,
                "model_name": model_name,
                "overall_robustness": robustness_results.get("overall_robustness", {}),
                "test_results": {
                    "noise": robustness_results.get("noise_robustness", {}),
                    "brightness": robustness_results.get("brightness_robustness", {}),
                    "contrast": robustness_results.get("contrast_robustness", {}),
                    "rotation": robustness_results.get("rotation_robustness", {}),
                    "blur": robustness_results.get("blur_robustness", {}),
                    "scale": robustness_results.get("scale_robustness", {}),
                    "occlusion": robustness_results.get("occlusion_robustness", {}),
                    "compression": robustness_results.get("compression_robustness", {})
                },
                "chart_paths": valid_charts,
                "report_path": str(report_path)
            }

        except Exception as e:
            logger.error(f"خطأ في اختبار متانة النموذج: {e}")
            return {"error": f"خطأ في اختبار متانة النموذج: {str(e)}"}

    def compare_models_robustness(self, models: List[str], image_paths: List[str]) -> Dict[str, Any]:
        """
        مقارنة متانة النماذج المختلفة

        المعلمات:
            models: قائمة بأسماء النماذج للمقارنة
            image_paths: قائمة بمسارات الصور للاختبار

        العائد:
            قاموس يحتوي على نتائج المقارنة
        """
        if not self.robustness_analyzer:
            return {"error": "محلل المتانة غير متاح"}

        try:
            # التحقق من وجود الصور
            valid_paths = [path for path in image_paths if os.path.exists(path)]

            if not valid_paths:
                return {"error": "لا توجد صور صالحة للاختبار"}

            # اختبار المتانة لكل نموذج
            for model_name in models:
                self.robustness_analyzer.test_comprehensive_robustness(model_name, valid_paths)

            # مقارنة متانة النماذج
            comparison_results = self.robustness_analyzer.compare_models_robustness(models)

            # الحصول على مسار مخطط المقارنة
            comparison_chart_path = "/home/ubuntu/gaara_scan_ai_final_4.2/static/reports/robustness_comparison_chart.png"

            # حفظ النتائج
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.robustness_dir / f"robustness_comparison_{timestamp}.json"

            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(comparison_results, f, ensure_ascii=False, indent=2)

            return {
                "timestamp": timestamp,
                "models_compared": models,
                "comparison_data": comparison_results.get("comparison_data", {}),
                "best_models": comparison_results.get("best_models", {}),
                "comparison_chart_path": comparison_chart_path if os.path.exists(comparison_chart_path) else None,
                "report_path": str(report_path)
            }

        except Exception as e:
            logger.error(f"خطأ في مقارنة متانة النماذج: {e}")
            return {"error": f"خطأ في مقارنة متانة النماذج: {str(e)}"}

    def get_robustness_reports(self) -> Dict[str, Any]:
        """
        الحصول على قائمة تقارير اختبار المتانة السابقة

        العائد:
            قاموس يحتوي على قائمة التقارير
        """
        reports = []

        try:
            for file in self.robustness_dir.glob("robustness_report_*.json"):
                try:
                    filename = file.stem
                    parts = filename.split('_')
                    if len(parts) >= 4:
                        model_name = parts[2]
                        timestamp = '_'.join(parts[3:])

                        reports.append({
                            "model_name": model_name,
                            "timestamp": timestamp,
                            "path": str(file)
                        })
                except Exception as e:
                    logger.error(f"خطأ في قراءة ملف تقرير المتانة {file}: {e}")

            # تقارير المقارنة
            for file in self.robustness_dir.glob("robustness_comparison_*.json"):
                try:
                    timestamp = file.stem.replace("robustness_comparison_", "")

                    reports.append({
                        "model_name": "مقارنة",
                        "timestamp": timestamp,
                        "path": str(file)
                    })
                except Exception as e:
                    logger.error(f"خطأ في قراءة ملف مقارنة المتانة {file}: {e}")

        except Exception as e:
            logger.error(f"خطأ في الحصول على قائمة تقارير المتانة: {e}")

        return {
            "count": len(reports),
            "reports": sorted(reports, key=lambda x: x["timestamp"], reverse=True)
        }

    # ===== وظائف مساعدة =====

    def _get_model_type(self, model_name: str) -> str:
        """
        تحديد نوع النموذج

        المعلمات:
            model_name: اسم النموذج

        العائد:
            نوع النموذج
        """
        if model_name in ['mobilenet_plant', 'vit_plant']:
            return "huggingface"
        elif model_name in ['cropnet_cassava', 'cropnet_feature', 'mobilenet_v3']:
            return "tensorflow"
        elif model_name == 'alexnet_plantvillage':
            return "pytorch"
        elif model_name == 'keras_plant':
            return "keras"
        else:
            return "unknown"

    def _get_model_parameters(self, model, model_type: str) -> Union[int, str]:
        """
        الحصول على عدد معلمات النموذج

        المعلمات:
            model: النموذج
            model_type: نوع النموذج

        العائد:
            عدد المعلمات
        """
        try:
            if model_type in ["huggingface", "pytorch"]:
                return sum(p.numel() for p in model.parameters())
            elif model_type == "tensorflow":
                return model.count_params() if hasattr(model, 'count_params') else "غير متاح"
            elif model_type == "keras":
                return model.count_params()
            else:
                return "غير متاح"
        except BaseException:
            return "غير متاح"

    def _get_model_input_shape(self, model, model_type: str) -> List[int]:
        """
        الحصول على شكل المدخلات للنموذج

        المعلمات:
            model: النموذج
            model_type: نوع النموذج

        العائد:
            شكل المدخلات
        """
        try:
            if model_type == "huggingface":
                return [3, 224, 224]  # افتراضي
            elif model_type in ["tensorflow", "keras"]:
                return model.input_shape[1:] if hasattr(model, 'input_shape') else [224, 224, 3]
            else:
                return [224, 224, 3]  # افتراضي
        except BaseException:
            return [224, 224, 3]  # افتراضي

    def _get_model_output_shape(self, model, model_type: str) -> Union[List[int], str]:
        """
        الحصول على شكل المخرجات للنموذج

        المعلمات:
            model: النموذج
            model_type: نوع النموذج

        العائد:
            شكل المخرجات
        """
        try:
            if model_type == "huggingface":
                return [len(model.config.id2label)] if hasattr(model.config, 'id2label') else "غير متاح"
            elif model_type in ["tensorflow", "keras"]:
                return model.output_shape[1:] if hasattr(model, 'output_shape') else "غير متاح"
            else:
                return "غير متاح"
        except BaseException:
            return "غير متاح"

    def _get_model_description(self, model_name: str, model_type: str) -> str:
        """
        الحصول على وصف النموذج

        المعلمات:
            model_name: اسم النموذج
            model_type: نوع النموذج

        العائد:
            وصف النموذج
        """
        descriptions = {
            'mobilenet_plant': "نموذج MobileNet V2 مدرب على تحديد أمراض النباتات من Hugging Face",
            'vit_plant': "نموذج Vision Transformer مدرب على تحديد أمراض النباتات من Hugging Face",
            'cropnet_cassava': "نموذج CropNet مدرب على تحديد أمراض الكاسافا من TensorFlow Hub",
            'cropnet_feature': "نموذج CropNet لاستخراج الميزات من صور النباتات من TensorFlow Hub",
            'mobilenet_v3': "نموذج MobileNet V3 لاستخراج الميزات من صور النباتات من TensorFlow Hub",
            'alexnet_plantvillage': "نموذج AlexNet مدرب على مجموعة بيانات PlantVillage",
            'keras_plant': "نموذج Keras مدرب على تحديد أمراض النباتات"
        }

        return descriptions.get(model_name, f"نموذج {model_type} لتحديد أمراض النباتات")

    def _make_serializable(self, data: Any) -> Any:
        """
        تحويل البيانات إلى شكل قابل للتخزين في JSON

        المعلمات:
            data: البيانات المراد تحويلها

        العائد:
            البيانات بعد التحويل
        """
        if isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, dict):
            return {k: self._make_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._make_serializable(item) for item in data]
        elif isinstance(data, (np.int32, np.int64)):
            return int(data)
        elif isinstance(data, (np.float32, np.float64)):
            return float(data)
        else:
            return data
