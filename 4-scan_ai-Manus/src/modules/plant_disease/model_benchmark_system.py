"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/plant_disease/model_benchmark_system.py

نظام شامل لاختبار ومقارنة نماذج تشخيص أمراض النباتات
يوفر هذا النظام أدوات لقياس أداء النماذج المختلفة من حيث الدقة والسرعة واستهلاك الموارد
ويقدم تقارير مفصلة ومرئية لمساعدة المستخدمين في اختيار النموذج المناسب لاحتياجاتهم
"""

import time
import psutil
import torch
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import pandas as pd
import threading
import gc
import json
import os
import warnings
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# تجاهل التحذيرات
warnings.filterwarnings('ignore')


class ModelBenchmarkSystem:
    """نظام شامل لاختبار ومقارنة النماذج"""

    def __init__(self, processor):
        """
        تهيئة نظام اختبار ومقارنة النماذج

        المعلمات:
            processor: معالج تشخيص أمراض النباتات المتقدم
        """
        self.processor = processor
        self.benchmark_results = {}
        self.performance_metrics = {}
        self.resource_usage = {}
        self.reports_dir = Path("/home/ubuntu/gaara_scan_ai_final_4.2/reports/benchmarks")

        # إنشاء مجلد التقارير إذا لم يكن موجوداً
        os.makedirs(self.reports_dir, exist_ok=True)

    def run_comprehensive_benchmark(self, test_images_path: List[str], ground_truth_labels: List[int],
                                    models_to_test: Optional[List[str]] = None, num_iterations: int = 3) -> Dict[str, Any]:
        """
        تشغيل اختبار شامل للنماذج

        المعلمات:
            test_images_path: قائمة بمسارات الصور للاختبار
            ground_truth_labels: التسميات الصحيحة للصور
            models_to_test: قائمة بأسماء النماذج للاختبار (إذا كانت None، يتم اختبار جميع النماذج المتاحة)
            num_iterations: عدد مرات تكرار الاختبار لكل نموذج

        العائد:
            قاموس يحتوي على نتائج الاختبار لكل نموذج
        """

        if models_to_test is None:
            models_to_test = list(self.processor.models.keys())

        print("🚀 بدء الاختبار الشامل للنماذج...")
        print(f"📊 عدد النماذج: {len(models_to_test)}")
        print(f"🖼️ عدد الصور: {len(test_images_path)}")
        print(f"🔄 عدد التكرارات: {num_iterations}")

        results = {}

        for model_name in models_to_test:
            print(f"\n🔍 اختبار النموذج: {model_name}")

            # تشغيل الاختبار متعدد التكرارات
            model_results = []
            for iteration in range(num_iterations):
                print(f"  📈 التكرار {iteration + 1}/{num_iterations}")

                result = self.benchmark_single_model(
                    model_name, test_images_path, ground_truth_labels, iteration
                )
                model_results.append(result)

                # تنظيف الذاكرة
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

            # حساب المتوسطات والإحصائيات
            results[model_name] = self.aggregate_results(model_results)

        self.benchmark_results = results
        self.generate_comparison_report()
        self.create_visualizations()

        return results

    def benchmark_single_model(self, model_name: str, test_images: List[str],
                               ground_truth: List[int], iteration: int) -> Dict[str, Any]:
        """
        اختبار نموذج واحد

        المعلمات:
            model_name: اسم النموذج للاختبار
            test_images: قائمة بمسارات الصور للاختبار
            ground_truth: التسميات الصحيحة للصور
            iteration: رقم التكرار الحالي

        العائد:
            قاموس يحتوي على نتائج الاختبار للنموذج
        """

        if model_name not in self.processor.models:
            return {"error": f"النموذج {model_name} غير متاح"}

        # إعداد مراقبة الموارد
        resource_monitor = ResourceMonitor()
        resource_monitor.start_monitoring()

        # تسجيل وقت البداية
        start_time = time.time()

        # قياس استهلاك الذاكرة قبل التنفيذ
        memory_before = psutil.virtual_memory().used / (1024**3)  # GB
        gpu_memory_before = self.get_gpu_memory() if torch.cuda.is_available() else 0

        # التنبؤات
        predictions = []
        confidences = []
        inference_times = []

        for i, image_path in enumerate(test_images):
            # قياس وقت التنبؤ لكل صورة
            img_start_time = time.time()

            try:
                result = self.processor.predict_single_model(image_path, model_name)

                if "error" not in result:
                    predictions.append(result['prediction'])
                    confidences.append(result['confidence'])
                else:
                    predictions.append(-1)  # خطأ
                    confidences.append(0.0)

            except Exception as e:
                print(f"❌ خطأ في الصورة {i}: {e}")
                predictions.append(-1)
                confidences.append(0.0)

            img_end_time = time.time()
            inference_times.append(img_end_time - img_start_time)

            # تحديث التقدم
            if (i + 1) % 10 == 0:
                print(f"    📸 تم معالجة {i + 1}/{len(test_images)} صورة")

        # تسجيل وقت النهاية
        end_time = time.time()
        total_time = end_time - start_time

        # قياس استهلاك الذاكرة بعد التنفيذ
        memory_after = psutil.virtual_memory().used / (1024**3)  # GB
        gpu_memory_after = self.get_gpu_memory() if torch.cuda.is_available() else 0

        # إيقاف مراقبة الموارد
        resource_stats = resource_monitor.stop_monitoring()

        # حساب المقاييس
        metrics = self.calculate_metrics(predictions, ground_truth, confidences)

        return {
            "model_name": model_name,
            "iteration": iteration,
            "predictions": predictions,
            "confidences": confidences,
            "metrics": metrics,
            "timing": {
                "total_time": total_time,
                "avg_inference_time": np.mean(inference_times),
                "min_inference_time": np.min(inference_times),
                "max_inference_time": np.max(inference_times),
                "fps": len(test_images) / total_time
            },
            "resource_usage": {
                "memory_used": memory_after - memory_before,
                "gpu_memory_used": gpu_memory_after - gpu_memory_before,
                "cpu_usage": resource_stats['avg_cpu_usage'],
                "peak_memory": resource_stats['peak_memory']
            },
            "inference_times": inference_times
        }

    def calculate_metrics(self, predictions: List[int], ground_truth: List[int],
                          confidences: List[float]) -> Dict[str, Any]:
        """
        حساب مقاييس الأداء

        المعلمات:
            predictions: قائمة بالتنبؤات
            ground_truth: قائمة بالتسميات الصحيحة
            confidences: قائمة بدرجات الثقة للتنبؤات

        العائد:
            قاموس يحتوي على مقاييس الأداء
        """

        # تصفية التنبؤات الخاطئة
        valid_indices = [i for i, pred in enumerate(predictions) if pred != -1]

        if not valid_indices:
            return {
                "accuracy": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "error_rate": 1.0,
                "avg_confidence": 0.0
            }

        valid_predictions = [predictions[i] for i in valid_indices]
        valid_ground_truth = [ground_truth[i] for i in valid_indices]
        valid_confidences = [confidences[i] for i in valid_indices]

        # حساب المقاييس الأساسية
        accuracy = accuracy_score(valid_ground_truth, valid_predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            valid_ground_truth, valid_predictions, average='weighted', zero_division=0
        )

        error_rate = 1.0 - (len(valid_indices) / len(predictions))
        avg_confidence = np.mean(valid_confidences)

        # مصفوفة الخلط
        cm = confusion_matrix(valid_ground_truth, valid_predictions)

        return {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "error_rate": float(error_rate),
            "avg_confidence": float(avg_confidence),
            "confusion_matrix": cm.tolist(),
            "valid_predictions": len(valid_indices),
            "total_predictions": len(predictions)
        }

    def aggregate_results(self, model_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        تجميع نتائج التكرارات المتعددة

        المعلمات:
            model_results: قائمة بنتائج التكرارات المتعددة للنموذج

        العائد:
            قاموس يحتوي على النتائج المجمعة
        """

        if not model_results or all("error" in result for result in model_results):
            return {"error": "فشل في جميع التكرارات"}

        # تصفية النتائج الصحيحة
        valid_results = [result for result in model_results if "error" not in result]

        if not valid_results:
            return {"error": "لا توجد نتائج صحيحة"}

        # تجميع المقاييس
        metrics_keys = ['accuracy', 'precision', 'recall', 'f1_score', 'error_rate', 'avg_confidence']
        timing_keys = ['total_time', 'avg_inference_time', 'fps']
        resource_keys = ['memory_used', 'gpu_memory_used', 'cpu_usage', 'peak_memory']

        aggregated = {
            "model_name": valid_results[0]["model_name"],
            "num_iterations": len(valid_results),
            "metrics": {},
            "timing": {},
            "resource_usage": {},
            "stability": {}
        }

        # تجميع المقاييس مع الإحصائيات
        for key in metrics_keys:
            values = [result["metrics"][key] for result in valid_results if key in result["metrics"]]
            if values:
                aggregated["metrics"][key] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values))
                }

        # تجميع التوقيتات
        for key in timing_keys:
            values = [result["timing"][key] for result in valid_results if key in result["timing"]]
            if values:
                aggregated["timing"][key] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values))
                }

        # تجميع استهلاك الموارد
        for key in resource_keys:
            values = [result["resource_usage"][key] for result in valid_results if key in result["resource_usage"]]
            if values:
                aggregated["resource_usage"][key] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values))
                }

        # حساب مقاييس الاستقرار
        accuracy_values = [result["metrics"]["accuracy"] for result in valid_results]
        timing_values = [result["timing"]["avg_inference_time"] for result in valid_results]

        aggregated["stability"] = {
            "accuracy_cv": float(np.std(accuracy_values) / np.mean(accuracy_values)) if accuracy_values else 0,
            "timing_cv": float(np.std(timing_values) / np.mean(timing_values)) if timing_values else 0,
            "consistency_score": 1.0 - float(np.std(accuracy_values)) if accuracy_values else 0
        }

        return aggregated

    def generate_comparison_report(self) -> None:
        """
        إنشاء تقرير مقارنة شامل
        """

        if not self.benchmark_results:
            print("❌ لا توجد نتائج للمقارنة")
            return

        print("\n" + "=" * 80)
        print("📊 تقرير مقارنة النماذج الشامل")
        print("=" * 80)

        # جدول الأداء الرئيسي
        self.print_performance_table()

        # جدول السرعة والموارد
        self.print_speed_resource_table()

        # التوصيات
        self.print_recommendations()

        # حفظ التقرير
        self.save_detailed_report()

    def print_performance_table(self) -> None:
        """
        طباعة جدول الأداء
        """

        print("\n🎯 أداء النماذج (الدقة والجودة)")
        print("-" * 80)

        data = []
        for model_name, results in self.benchmark_results.items():
            if "error" not in results:
                metrics = results["metrics"]
                stability = results["stability"]

                data.append({
                    "النموذج": model_name,
                    "الدقة (%)": f"{metrics['accuracy']['mean']*100:.2f} ± {metrics['accuracy']['std']*100:.2f}",
                    "F1-Score": f"{metrics['f1_score']['mean']:.3f}",
                    "الثقة المتوسطة": f"{metrics['avg_confidence']['mean']:.3f}",
                    "الاستقرار": f"{stability['consistency_score']:.3f}"
                })

        df = pd.DataFrame(data)
        print(df.to_string(index=False))

    def print_speed_resource_table(self) -> None:
        """
        طباعة جدول السرعة والموارد
        """

        print("\n⚡ السرعة واستهلاك الموارد")
        print("-" * 80)

        data = []
        for model_name, results in self.benchmark_results.items():
            if "error" not in results:
                timing = results["timing"]
                resources = results["resource_usage"]

                data.append({
                    "النموذج": model_name,
                    "FPS": f"{timing['fps']['mean']:.2f}",
                    "زمن التنبؤ (ثانية)": f"{timing['avg_inference_time']['mean']:.3f}",
                    "الذاكرة (GB)": f"{resources['memory_used']['mean']:.2f}",
                    "معالج مئوي (%)": f"{resources['cpu_usage']['mean']:.1f}"
                })

        df = pd.DataFrame(data)
        print(df.to_string(index=False))

    def print_recommendations(self) -> None:
        """
        طباعة التوصيات
        """

        print("\n💡 التوصيات")
        print("-" * 80)

        if not self.benchmark_results:
            return

        # أفضل نموذج للدقة
        best_accuracy_model = max(
            self.benchmark_results.items(),
            key=lambda x: x[1]["metrics"]["accuracy"]["mean"] if "error" not in x[1] else 0
        )

        # أسرع نموذج
        fastest_model = max(
            self.benchmark_results.items(),
            key=lambda x: x[1]["timing"]["fps"]["mean"] if "error" not in x[1] else 0
        )

        # أقل استهلاك للموارد
        most_efficient_model = min(
            self.benchmark_results.items(),
            key=lambda x: x[1]["resource_usage"]["memory_used"]["mean"] if "error" not in x[1] else float('inf')
        )

        print(f"🏆 أفضل دقة: {best_accuracy_model[0]} ({best_accuracy_model[1]['metrics']['accuracy']['mean']*100:.2f}%)")
        print(f"🚀 الأسرع: {fastest_model[0]} ({fastest_model[1]['timing']['fps']['mean']:.2f} FPS)")
        print(f"💾 الأكثر كفاءة: {most_efficient_model[0]} ({most_efficient_model[1]['resource_usage']['memory_used']['mean']:.2f} GB)")

        # توصيات الاستخدام
        print("\n📝 توصيات الاستخدام:")
        print("• للدقة العالية: استخدم", best_accuracy_model[0])
        print("• للتطبيقات الفورية: استخدم", fastest_model[0])
        print("• للأجهزة المحدودة: استخدم", most_efficient_model[0])

    def create_visualizations(self) -> None:
        """
        إنشاء المخططات البيانية
        """

        if not self.benchmark_results:
            return

        # إعداد البيانات للرسم
        models = []
        accuracies = []
        fps_values = []
        memory_usage = []

        for model_name, results in self.benchmark_results.items():
            if "error" not in results:
                models.append(model_name)
                accuracies.append(results["metrics"]["accuracy"]["mean"] * 100)
                fps_values.append(results["timing"]["fps"]["mean"])
                memory_usage.append(results["resource_usage"]["memory_used"]["mean"])

        # إنشاء المخططات
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('مقارنة أداء النماذج', fontsize=16, fontweight='bold')

        # مخطط الدقة
        axes[0, 0].bar(models, accuracies, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('دقة النماذج (%)')
        axes[0, 0].set_ylabel('الدقة (%)')
        axes[0, 0].tick_params(axis='x', rotation=45)

        # مخطط السرعة
        axes[0, 1].bar(models, fps_values, color='lightgreen', alpha=0.7)
        axes[0, 1].set_title('سرعة النماذج (FPS)')
        axes[0, 1].set_ylabel('إطارات في الثانية')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # مخطط استهلاك الذاكرة
        axes[1, 0].bar(models, memory_usage, color='lightcoral', alpha=0.7)
        axes[1, 0].set_title('استهلاك الذاكرة (GB)')
        axes[1, 0].set_ylabel('الذاكرة (GB)')
        axes[1, 0].tick_params(axis='x', rotation=45)

        # مخطط الأداء مقابل السرعة
        scatter = axes[1, 1].scatter(fps_values, accuracies, c=memory_usage,
                                     cmap='viridis', s=100, alpha=0.7)
        axes[1, 1].set_xlabel('السرعة (FPS)')
        axes[1, 1].set_ylabel('الدقة (%)')
        axes[1, 1].set_title('الأداء مقابل السرعة')

        # إضافة تسميات للنقاط
        for i, model in enumerate(models):
            axes[1, 1].annotate(model, (fps_values[i], accuracies[i]),
                                xytext=(5, 5), textcoords='offset points', fontsize=8)

        # إضافة شريط الألوان
        cbar = plt.colorbar(scatter, ax=axes[1, 1])
        cbar.set_label('استهلاك الذاكرة (GB)')

        plt.tight_layout()

        # إنشاء اسم ملف فريد بناءً على الوقت الحالي
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.reports_dir / f"model_comparison_{timestamp}.png"

        plt.savefig(report_path, dpi=300, bbox_inches='tight')
        print(f"\n📊 تم حفظ المخططات البيانية في: {report_path}")

    def save_detailed_report(self) -> None:
        """
        حفظ تقرير مفصل
        """

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "benchmark_results": self.benchmark_results,
            "summary": self.generate_summary()
        }

        # إنشاء اسم ملف فريد بناءً على الوقت الحالي
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.reports_dir / f"benchmark_report_{timestamp}.json"

        with open(report_path, "w", encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n💾 تم حفظ التقرير المفصل في: {report_path}")

    def generate_summary(self) -> Dict[str, Any]:
        """
        إنشاء ملخص النتائج

        العائد:
            قاموس يحتوي على ملخص النتائج
        """

        if not self.benchmark_results:
            return {}

        valid_results = {k: v for k, v in self.benchmark_results.items() if "error" not in v}

        if not valid_results:
            return {}

        summary = {
            "total_models_tested": len(self.benchmark_results),
            "successful_models": len(valid_results),
            "average_accuracy": np.mean([v["metrics"]["accuracy"]["mean"] for v in valid_results.values()]),
            "average_fps": np.mean([v["timing"]["fps"]["mean"] for v in valid_results.values()]),
            "average_memory_usage": np.mean([v["resource_usage"]["memory_used"]["mean"] for v in valid_results.values()])
        }

        return summary

    def get_gpu_memory(self) -> float:
        """
        الحصول على استهلاك ذاكرة GPU

        العائد:
            استهلاك ذاكرة GPU بالجيجابايت
        """

        if torch.cuda.is_available():
            return torch.cuda.memory_allocated() / (1024**3)  # GB
        return 0

    def get_best_model_for_scenario(self, scenario: str) -> str:
        """
        الحصول على أفضل نموذج لسيناريو معين

        المعلمات:
            scenario: السيناريو المطلوب ('accuracy', 'speed', 'efficiency')

        العائد:
            اسم أفضل نموذج للسيناريو المطلوب
        """

        if not self.benchmark_results:
            return "لا توجد نتائج متاحة"

        valid_results = {k: v for k, v in self.benchmark_results.items() if "error" not in v}

        if not valid_results:
            return "لا توجد نتائج صحيحة"

        if scenario == 'accuracy':
            best_model = max(
                valid_results.items(),
                key=lambda x: x[1]["metrics"]["accuracy"]["mean"]
            )
            return best_model[0]

        elif scenario == 'speed':
            best_model = max(
                valid_results.items(),
                key=lambda x: x[1]["timing"]["fps"]["mean"]
            )
            return best_model[0]

        elif scenario == 'efficiency':
            best_model = min(
                valid_results.items(),
                key=lambda x: x[1]["resource_usage"]["memory_used"]["mean"]
            )
            return best_model[0]

        else:
            return "سيناريو غير معروف"

    def export_results_to_csv(self, file_path: Optional[str] = None) -> str:
        """
        تصدير النتائج إلى ملف CSV

        المعلمات:
            file_path: مسار الملف للتصدير (اختياري)

        العائد:
            مسار الملف المصدر
        """

        if not self.benchmark_results:
            return "لا توجد نتائج للتصدير"

        # إنشاء البيانات للتصدير
        data = []
        for model_name, results in self.benchmark_results.items():
            if "error" not in results:
                metrics = results["metrics"]
                timing = results["timing"]
                resources = results["resource_usage"]
                stability = results["stability"]

                row = {
                    "model_name": model_name,
                    "accuracy": metrics["accuracy"]["mean"],
                    "accuracy_std": metrics["accuracy"]["std"],
                    "precision": metrics["precision"]["mean"],
                    "recall": metrics["recall"]["mean"],
                    "f1_score": metrics["f1_score"]["mean"],
                    "avg_confidence": metrics["avg_confidence"]["mean"],
                    "fps": timing["fps"]["mean"],
                    "avg_inference_time": timing["avg_inference_time"]["mean"],
                    "memory_used": resources["memory_used"]["mean"],
                    "cpu_usage": resources["cpu_usage"]["mean"],
                    "consistency_score": stability["consistency_score"]
                }

                data.append(row)

        # إنشاء DataFrame
        df = pd.DataFrame(data)

        # تحديد مسار الملف
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = str(self.reports_dir / f"benchmark_results_{timestamp}.csv")

        # تصدير إلى CSV
        df.to_csv(file_path, index=False)

        return file_path

    def analyze_model_learning(self, model_name: str) -> Dict[str, Any]:
        """
        تحليل كيفية تعلم النموذج وتحديد نقاط القوة والضعف

        المعلمات:
            model_name: اسم النموذج للتحليل

        العائد:
            قاموس يحتوي على نتائج التحليل
        """

        if model_name not in self.benchmark_results:
            return {"error": f"النموذج {model_name} غير متاح في النتائج"}

        results = self.benchmark_results[model_name]

        if "error" in results:
            return {"error": f"النموذج {model_name} لديه خطأ في النتائج"}

        # تحليل نقاط القوة والضعف
        metrics = results["metrics"]
        timing = results["timing"]

        # تحديد الفئات التي يتفوق فيها النموذج
        # (هذا يتطلب بيانات إضافية من مصفوفة الخلط)

        analysis = {
            "model_name": model_name,
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }

        # تحليل الدقة
        if metrics["accuracy"]["mean"] > 0.9:
            analysis["strengths"].append("دقة عالية جداً")
        elif metrics["accuracy"]["mean"] > 0.8:
            analysis["strengths"].append("دقة جيدة")
        else:
            analysis["weaknesses"].append("دقة منخفضة")
            analysis["recommendations"].append("تحسين الدقة عن طريق زيادة بيانات التدريب أو تعديل معلمات النموذج")

        # تحليل السرعة
        if timing["fps"]["mean"] > 30:
            analysis["strengths"].append("سرعة عالية جداً")
        elif timing["fps"]["mean"] > 10:
            analysis["strengths"].append("سرعة جيدة")
        else:
            analysis["weaknesses"].append("سرعة منخفضة")
            analysis["recommendations"].append("تحسين السرعة عن طريق تقليل حجم النموذج أو استخدام تقنيات التسريع")

        # تحليل الاستقرار
        if results["stability"]["consistency_score"] > 0.95:
            analysis["strengths"].append("استقرار ممتاز")
        elif results["stability"]["consistency_score"] > 0.9:
            analysis["strengths"].append("استقرار جيد")
        else:
            analysis["weaknesses"].append("استقرار منخفض")
            analysis["recommendations"].append("تحسين الاستقرار عن طريق زيادة تنوع بيانات التدريب")

        return analysis


class ResourceMonitor:
    """مراقب استهلاك الموارد"""

    def __init__(self):
        """
        تهيئة مراقب استهلاك الموارد
        """
        self.monitoring = False
        self.cpu_usage = []
        self.memory_usage = []
        self.monitor_thread = None

    def start_monitoring(self) -> None:
        """
        بدء مراقبة الموارد
        """
        self.monitoring = True
        self.cpu_usage = []
        self.memory_usage = []
        self.monitor_thread = threading.Thread(target=self._monitor_resources)
        self.monitor_thread.start()

    def stop_monitoring(self) -> Dict[str, float]:
        """
        إيقاف مراقبة الموارد

        العائد:
            قاموس يحتوي على إحصائيات استهلاك الموارد
        """
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()

        return {
            "avg_cpu_usage": np.mean(self.cpu_usage) if self.cpu_usage else 0,
            "peak_cpu_usage": np.max(self.cpu_usage) if self.cpu_usage else 0,
            "avg_memory": np.mean(self.memory_usage) if self.memory_usage else 0,
            "peak_memory": np.max(self.memory_usage) if self.memory_usage else 0
        }

    def _monitor_resources(self) -> None:
        """
        مراقبة الموارد في خيط منفصل
        """

        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory_percent = psutil.virtual_memory().percent

                self.cpu_usage.append(cpu_percent)
                self.memory_usage.append(memory_percent)

                time.sleep(0.1)  # مراقبة كل 100ms
            except BaseException:
                break


# مثال على الاستخدام
if __name__ == "__main__":
    print("✅ تم تحميل نظام اختبار النماذج بنجاح!")
