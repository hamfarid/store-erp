"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/plant_disease/processor_integration.py

تكامل نظام اختبار ومقارنة النماذج مع المعالج المتقدم لتشخيص أمراض النباتات
يوفر هذا الملف الربط بين نظام اختبار ومقارنة النماذج والمعالج المتقدم

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
تاريخ التعديل: 30 مايو 2025 - إضافة دعم محلل الانتباه ومحلل المتانة
"""

import logging
from typing import Any, Dict, List, Optional

from .advanced_processor import AdvancedPlantDiseaseProcessor
from .attention_analyzer import AttentionAnalyzer
from .model_benchmark_system import ModelBenchmarkSystem
from .model_comparison_api import ModelComparisonAPI
from .model_learning_system import ModelLearningSystem
from .robustness_analyzer import RobustnessAnalyzer

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('processor_integration')


class ProcessorIntegration:
    """تكامل نظام اختبار ومقارنة النماذج مع المعالج المتقدم"""

    def __init__(self, config_path: Optional[str] = None):
        """
        تهيئة نظام التكامل

        المعلمات:
            config_path: مسار ملف الإعدادات (اختياري)
        """
        self.config_path = config_path or "/home/ubuntu/gaara_scan_ai_final_4.2/config/plant_disease_config.json"

        # تهيئة المعالج المتقدم
        self.processor = AdvancedPlantDiseaseProcessor(
            config_path=self.config_path)

        # تهيئة نظام اختبار ومقارنة النماذج
        self.benchmark_system = ModelBenchmarkSystem(processor=self.processor)

        # تهيئة نظام التعلم من النماذج
        self.learning_system = ModelLearningSystem()

        # تهيئة محلل أنماط الانتباه
        self.attention_analyzer = AttentionAnalyzer(processor=self.processor)

        # تهيئة محلل قوة ومتانة النماذج
        self.robustness_analyzer = RobustnessAnalyzer(processor=self.processor)

        # تهيئة واجهة اختبار ومقارنة النماذج
        self.comparison_api = ModelComparisonAPI(
            processor=self.processor,
            benchmark_system=self.benchmark_system,
            learning_system=self.learning_system,
            attention_analyzer=self.attention_analyzer,
            robustness_analyzer=self.robustness_analyzer
        )

        logger.info("تم تهيئة نظام التكامل بنجاح")

    def initialize(self) -> bool:
        """
        تهيئة جميع المكونات

        العائد:
            نجاح العملية
        """
        try:
            # تهيئة المعالج المتقدم
            self.processor.initialize()

            # تهيئة نظام اختبار ومقارنة النماذج
            # (لا يحتاج إلى تهيئة إضافية)

            # تهيئة نظام التعلم من النماذج
            # (لا يحتاج إلى تهيئة إضافية)

            # تهيئة محلل أنماط الانتباه ومحلل المتانة
            # (لا يحتاجان إلى تهيئة إضافية)

            logger.info("تم تهيئة جميع المكونات بنجاح")
            return True

        except Exception as e:
            logger.error(f"خطأ في تهيئة المكونات: {e}")
            return False

    def get_available_models(self) -> Dict[str, Any]:
        """
        الحصول على قائمة النماذج المتاحة

        العائد:
            قاموس يحتوي على قائمة النماذج المتاحة وتفاصيلها
        """
        return self.comparison_api.get_available_models()

    def get_model_details(self, model_name: str) -> Dict[str, Any]:
        """
        الحصول على تفاصيل نموذج محدد

        المعلمات:
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على تفاصيل النموذج
        """
        return self.comparison_api.get_model_details(model_name)

    def upload_test_images(
            self, images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        تحميل صور للاختبار

        المعلمات:
            images: قائمة بالصور (كل صورة عبارة عن قاموس يحتوي على البيانات والتسمية)

        العائد:
            قاموس يحتوي على مسارات الصور المحملة
        """
        return self.comparison_api.upload_test_images(images)

    def run_benchmark(self,
                      image_paths: List[str],
                      ground_truth: List[int],
                      models: Optional[List[str]] = None,
                      iterations: int = 3) -> Dict[str,
                                                   Any]:
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
        return self.comparison_api.run_benchmark(
            image_paths, ground_truth, models, iterations)

    def get_previous_benchmarks(self) -> Dict[str, Any]:
        """
        الحصول على قائمة الاختبارات السابقة

        العائد:
            قاموس يحتوي على قائمة الاختبارات السابقة
        """
        return self.comparison_api.get_previous_benchmarks()

    def get_benchmark_details(self, benchmark_id: str) -> Dict[str, Any]:
        """
        الحصول على تفاصيل اختبار محدد

        المعلمات:
            benchmark_id: معرف الاختبار (التاريخ والوقت)

        العائد:
            قاموس يحتوي على تفاصيل الاختبار
        """
        return self.comparison_api.get_benchmark_details(benchmark_id)

    def predict_with_model(self, image_path: str,
                           model_name: str) -> Dict[str, Any]:
        """
        التنبؤ باستخدام نموذج محدد

        المعلمات:
            image_path: مسار الصورة
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على نتيجة التنبؤ
        """
        return self.comparison_api.predict_with_model(image_path, model_name)

    def predict_with_ensemble(
            self, image_path: str, models: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        التنبؤ باستخدام مجموعة نماذج

        المعلمات:
            image_path: مسار الصورة
            models: قائمة بأسماء النماذج (اختياري)

        العائد:
            قاموس يحتوي على نتيجة التنبؤ المجمع
        """
        return self.comparison_api.predict_with_ensemble(image_path, models)

    def learn_from_results(
            self, benchmark_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        التعلم من نتائج الاختبار

        المعلمات:
            benchmark_results: نتائج الاختبار

        العائد:
            قاموس يحتوي على نتائج التعلم
        """
        return self.comparison_api.learn_from_results(benchmark_results)

    # ===== وظائف محلل الانتباه =====

    def analyze_attention(
            self, image_paths: List[str], model_name: str) -> Dict[str, Any]:
        """
        تحليل أنماط الانتباه في النموذج

        المعلمات:
            image_paths: قائمة بمسارات الصور للتحليل
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على نتائج تحليل الانتباه
        """
        return self.comparison_api.analyze_attention(image_paths, model_name)

    def compare_attention_patterns(
            self, models: List[str], image_paths: List[str]) -> Dict[str, Any]:
        """
        مقارنة أنماط الانتباه بين النماذج المختلفة

        المعلمات:
            models: قائمة بأسماء النماذج للمقارنة
            image_paths: قائمة بمسارات الصور للتحليل

        العائد:
            قاموس يحتوي على نتائج المقارنة
        """
        return self.comparison_api.compare_attention_patterns(
            models, image_paths)

    def get_attention_reports(self) -> Dict[str, Any]:
        """
        الحصول على قائمة تقارير تحليل الانتباه السابقة

        العائد:
            قاموس يحتوي على قائمة التقارير
        """
        return self.comparison_api.get_attention_reports()

    # ===== وظائف محلل المتانة =====

    def test_model_robustness(
            self, image_paths: List[str], model_name: str) -> Dict[str, Any]:
        """
        اختبار قوة ومتانة النموذج

        المعلمات:
            image_paths: قائمة بمسارات الصور للاختبار
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على نتائج اختبار المتانة
        """
        return self.comparison_api.test_model_robustness(
            image_paths, model_name)

    def compare_models_robustness(
            self, models: List[str], image_paths: List[str]) -> Dict[str, Any]:
        """
        مقارنة متانة النماذج المختلفة

        المعلمات:
            models: قائمة بأسماء النماذج للمقارنة
            image_paths: قائمة بمسارات الصور للاختبار

        العائد:
            قاموس يحتوي على نتائج المقارنة
        """
        return self.comparison_api.compare_models_robustness(
            models, image_paths)

    def get_robustness_reports(self) -> Dict[str, Any]:
        """
        الحصول على قائمة تقارير اختبار المتانة السابقة

        العائد:
            قاموس يحتوي على قائمة التقارير
        """
        return self.comparison_api.get_robustness_reports()

    def install_external_model(
            self, model_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        تثبيت نموذج خارجي

        المعلمات:
            model_info: معلومات النموذج (المصدر، النوع، الاسم، إلخ)

        العائد:
            قاموس يحتوي على نتيجة التثبيت
        """
        try:
            # التحقق من صحة المعلومات
            required_fields = ["name", "source", "type"]
            for field in required_fields:
                if field not in model_info:
                    return {"error": f"الحقل {field} مطلوب"}

            # تثبيت النموذج باستخدام المعالج المتقدم
            result = self.processor.install_model(
                model_name=model_info["name"],
                model_source=model_info["source"],
                model_type=model_info["type"],
                model_config=model_info.get("config", {})
            )

            if result.get("success", False):
                logger.info(f"تم تثبيت النموذج {model_info['name']} بنجاح")
                return {
                    "success": True,
                    "message": f"تم تثبيت النموذج {model_info['name']} بنجاح",
                    "model_details": self.get_model_details(model_info["name"])
                }
            else:
                logger.error(
                    f"فشل في تثبيت النموذج {model_info['name']}: {result.get('error', 'خطأ غير معروف')}")
                return {
                    "success": False,
                    "error": result.get("error", "فشل في تثبيت النموذج")
                }

        except Exception as e:
            logger.error(f"خطأ في تثبيت النموذج الخارجي: {e}")
            return {
                "success": False,
                "error": f"خطأ في تثبيت النموذج الخارجي: {str(e)}"
            }

    def uninstall_model(self, model_name: str) -> Dict[str, Any]:
        """
        إزالة نموذج

        المعلمات:
            model_name: اسم النموذج

        العائد:
            قاموس يحتوي على نتيجة الإزالة
        """
        try:
            # التحقق من وجود النموذج
            if model_name not in self.processor.models:
                return {
                    "success": False,
                    "error": f"النموذج {model_name} غير موجود"
                }

            # إزالة النموذج باستخدام المعالج المتقدم
            result = self.processor.uninstall_model(model_name)

            if result.get("success", False):
                logger.info(f"تم إزالة النموذج {model_name} بنجاح")
                return {
                    "success": True,
                    "message": f"تم إزالة النموذج {model_name} بنجاح"
                }
            else:
                logger.error(
                    f"فشل في إزالة النموذج {model_name}: {result.get('error', 'خطأ غير معروف')}")
                return {
                    "success": False,
                    "error": result.get("error", "فشل في إزالة النموذج")
                }

        except Exception as e:
            logger.error(f"خطأ في إزالة النموذج: {e}")
            return {
                "success": False,
                "error": f"خطأ في إزالة النموذج: {str(e)}"
            }

    def get_learning_history(self) -> List[Dict[str, Any]]:
        """
        الحصول على سجل التعلم

        العائد:
            قائمة بسجلات التعلم
        """
        return self.learning_system.get_learning_history()

    def get_latest_learning(self) -> Optional[Dict[str, Any]]:
        """
        الحصول على آخر نتيجة تعلم

        العائد:
            آخر نتيجة تعلم أو None إذا لم يوجد
        """
        return self.learning_system.get_latest_learning()

    def clear_learning_history(self) -> bool:
        """
        مسح سجل التعلم

        العائد:
            نجاح العملية
        """
        return self.learning_system.clear_learning_history()

    def get_system_status(self) -> Dict[str, Any]:
        """
        الحصول على حالة النظام

        العائد:
            قاموس يحتوي على حالة النظام
        """
        try:
            # جمع معلومات حالة النظام
            models_count = len(self.processor.models)
            available_models = list(self.processor.models.keys())

            # الحصول على قائمة الاختبارات السابقة
            benchmarks = self.get_previous_benchmarks()

            # الحصول على آخر نتيجة تعلم
            latest_learning = self.get_latest_learning()

            # الحصول على قائمة تقارير تحليل الانتباه
            attention_reports = self.get_attention_reports()

            # الحصول على قائمة تقارير اختبار المتانة
            robustness_reports = self.get_robustness_reports()

            return {
                "status": "active",
                "models_count": models_count,
                "available_models": available_models,
                "benchmarks_count": benchmarks.get("count", 0),
                "latest_benchmark": benchmarks.get("benchmarks", [{}])[0] if benchmarks.get("benchmarks") else None,
                "latest_learning": latest_learning,
                "attention_reports_count": attention_reports.get("count", 0),
                "robustness_reports_count": robustness_reports.get("count", 0),
                "features": {
                    "benchmark": True,
                    "learning": self.learning_system is not None,
                    "attention_analysis": self.attention_analyzer is not None,
                    "robustness_testing": self.robustness_analyzer is not None
                }
            }

        except Exception as e:
            logger.error(f"خطأ في الحصول على حالة النظام: {e}")
            return {
                "status": "error",
                "error": f"خطأ في الحصول على حالة النظام: {str(e)}"
            }


# إنشاء نسخة واحدة من نظام التكامل للاستخدام في جميع أنحاء التطبيق
def get_processor_integration(config_path=None):
    """
    الحصول على نسخة من نظام التكامل

    المعلمات:
        config_path: مسار ملف الإعدادات (اختياري)

    العائد:
        نسخة من نظام التكامل
    """
    integration = ProcessorIntegration(config_path)
    integration.initialize()
    return integration
