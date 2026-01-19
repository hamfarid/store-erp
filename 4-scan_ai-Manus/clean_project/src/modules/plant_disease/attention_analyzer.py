"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/plant_disease/attention_analyzer.py

محلل أنماط الانتباه والتفسير
يوفر هذا الملف أدوات لتحليل أنماط الانتباه في نماذج تشخيص أمراض النباتات

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from PIL import Image
import cv2
import tempfile
import os
import logging
from typing import Dict, Any, List, Optional

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('attention_analyzer')


class AttentionAnalyzer:
    """محلل أنماط الانتباه والتفسير"""

    def __init__(self, processor):
        """
        تهيئة محلل أنماط الانتباه

        المعلمات:
            processor: معالج أمراض النباتات المتقدم
        """
        self.processor = processor
        self.attention_data = {}
        logger.info("تم تهيئة محلل أنماط الانتباه")

    def analyze_attention_patterns(self, model_name: str, test_images: List[str]) -> Dict[str, Any]:
        """
        تحليل أنماط الانتباه في النموذج

        المعلمات:
            model_name: اسم النموذج المراد تحليله
            test_images: قائمة بمسارات الصور للاختبار

        العائد:
            قاموس يحتوي على نتائج تحليل الانتباه
        """

        logger.info(f"تحليل أنماط الانتباه للنموذج: {model_name}")

        attention_analysis = {
            "attention_maps": {},
            "focus_regions": {},
            "attention_statistics": {},
            "visual_explanations": {}
        }

        # عينة من الصور للتحليل
        sample_images = test_images[:min(3, len(test_images))]

        for i, image_path in enumerate(sample_images):
            try:
                logger.info(f"معالجة الصورة {i+1}/{len(sample_images)}")

                # استخراج خرائط الانتباه
                attention_map = self.generate_attention_map(model_name, image_path)

                if attention_map is not None:
                    attention_analysis["attention_maps"][f"image_{i}"] = attention_map.tolist()

                    # تحليل المناطق المركزية
                    focus_regions = self.analyze_focus_regions(attention_map)
                    attention_analysis["focus_regions"][f"image_{i}"] = focus_regions

                    # إنشاء تفسير بصري
                    visual_explanation = self.create_visual_explanation(image_path, attention_map)
                    attention_analysis["visual_explanations"][f"image_{i}"] = visual_explanation

            except Exception as e:
                logger.error(f"خطأ في تحليل الانتباه للصورة {i}: {e}")

        # حساب إحصائيات عامة
        attention_analysis["attention_statistics"] = self.calculate_attention_statistics(
            attention_analysis["focus_regions"]
        )

        self.attention_data[model_name] = attention_analysis
        return attention_analysis

    def generate_attention_map(self, model_name: str, image_path: str) -> Optional[np.ndarray]:
        """
        توليد خريطة الانتباه باستخدام Grad-CAM

        المعلمات:
            model_name: اسم النموذج
            image_path: مسار الصورة

        العائد:
            مصفوفة numpy تمثل خريطة الانتباه أو None في حالة الفشل
        """

        try:
            # تحميل وتحضير الصورة
            image = Image.open(image_path).convert('RGB')
            processed_image = self.processor.preprocess_image(image_path, model_name)

            if isinstance(processed_image, torch.Tensor):
                return self.generate_gradcam_pytorch(
                    self.processor.models[model_name],
                    processed_image,
                    np.array(image)
                )
            else:
                return self.generate_gradcam_tensorflow(
                    self.processor.models[model_name],
                    processed_image,
                    np.array(image)
                )

        except Exception as e:
            logger.error(f"خطأ في توليد خريطة الانتباه: {e}")
            return None

    def generate_gradcam_pytorch(self, model: torch.nn.Module, input_tensor: torch.Tensor,
                                 original_image: np.ndarray) -> Optional[np.ndarray]:
        """
        توليد Grad-CAM لنموذج PyTorch

        المعلمات:
            model: نموذج PyTorch
            input_tensor: تنسور المدخلات
            original_image: الصورة الأصلية كمصفوفة numpy

        العائد:
            مصفوفة numpy تمثل خريطة الانتباه أو None في حالة الفشل
        """

        try:
            model.eval()

            # العثور على آخر طبقة conv
            target_layer = None
            for name, module in reversed(list(model.named_modules())):
                if isinstance(module, (torch.nn.Conv2d, torch.nn.modules.conv.Conv2d)):
                    target_layer = module
                    break

            if target_layer is None:
                logger.warning("لم يتم العثور على طبقة conv في النموذج")
                return None

            # متغيرات لحفظ التدرجات والميزات
            gradients = None
            activations = None

            def backward_hook(module, grad_input, grad_output):
                nonlocal gradients
                gradients = grad_output[0]

            def forward_hook(module, input, output):
                nonlocal activations
                activations = output

            # تسجيل hooks
            backward_handle = target_layer.register_backward_hook(backward_hook)
            forward_handle = target_layer.register_forward_hook(forward_hook)

            try:
                # Forward pass
                input_tensor = input_tensor.clone().detach().requires_grad_(True)
                output = model(input_tensor)

                # الحصول على الفئة المتوقعة
                pred_class = output.argmax(dim=1)

                # Backward pass
                model.zero_grad()
                class_loss = output[0, pred_class[0]]
                class_loss.backward()

                if gradients is not None and activations is not None:
                    # حساب الأوزان
                    weights = torch.mean(gradients, dim=[2, 3], keepdim=True)

                    # حساب Grad-CAM
                    cam = torch.sum(weights * activations, dim=1).squeeze()
                    cam = F.relu(cam)

                    # تطبيع وتغيير الحجم
                    cam = cam.detach().cpu().numpy()
                    cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)

                    # تغيير حجم خريطة الانتباه لحجم الصورة الأصلية
                    cam_resized = cv2.resize(cam, (original_image.shape[1], original_image.shape[0]))

                    return cam_resized
                else:
                    logger.warning("فشل في الحصول على التدرجات أو التنشيطات")

            finally:
                backward_handle.remove()
                forward_handle.remove()

        except Exception as e:
            logger.error(f"خطأ في Grad-CAM PyTorch: {e}")

        return None

    def generate_gradcam_tensorflow(self, model, input_array: np.ndarray,
                                    original_image: np.ndarray) -> Optional[np.ndarray]:
        """
        توليد Grad-CAM لنموذج TensorFlow

        المعلمات:
            model: نموذج TensorFlow
            input_array: مصفوفة المدخلات
            original_image: الصورة الأصلية كمصفوفة numpy

        العائد:
            مصفوفة numpy تمثل خريطة الانتباه أو None في حالة الفشل
        """

        try:
            import tensorflow as tf

            # العثور على آخر طبقة conv
            conv_layer = None
            for layer in reversed(model.layers):
                if 'conv' in layer.__class__.__name__.lower():
                    conv_layer = layer
                    break

            if conv_layer is None:
                logger.warning("لم يتم العثور على طبقة conv في النموذج")
                return None

            # إنشاء نموذج Grad-CAM
            grad_model = tf.keras.models.Model(
                inputs=[model.inputs],
                outputs=[conv_layer.output, model.output]
            )

            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(input_array)
                class_idx = tf.argmax(predictions[0])
                class_output = predictions[:, class_idx]

            # حساب التدرجات
            grads = tape.gradient(class_output, conv_outputs)

            # حساب الأوزان
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

            # حساب Grad-CAM
            conv_outputs = conv_outputs[0]
            heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)

            # تطبيع
            heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

            # تغيير الحجم
            heatmap_resized = cv2.resize(
                heatmap.numpy(),
                (original_image.shape[1], original_image.shape[0])
            )

            return heatmap_resized

        except Exception as e:
            logger.error(f"خطأ في Grad-CAM TensorFlow: {e}")

        return None

    def analyze_focus_regions(self, attention_map: np.ndarray) -> Dict[str, Any]:
        """
        تحليل المناطق التي يركز عليها النموذج

        المعلمات:
            attention_map: خريطة الانتباه

        العائد:
            قاموس يحتوي على تحليل المناطق المركزية
        """

        if attention_map is None:
            return {}

        # العثور على المناطق عالية الانتباه
        threshold = np.percentile(attention_map, 80)  # أعلى 20%
        high_attention = attention_map > threshold

        # حساب إحصائيات المناطق
        total_pixels = attention_map.size
        high_attention_pixels = np.sum(high_attention)
        focus_ratio = high_attention_pixels / total_pixels

        # العثور على مركز الانتباه
        y_indices, x_indices = np.where(high_attention)
        if len(y_indices) > 0:
            center_y = np.mean(y_indices) / attention_map.shape[0]
            center_x = np.mean(x_indices) / attention_map.shape[1]
        else:
            center_y, center_x = 0.5, 0.5

        # تحليل توزيع الانتباه
        attention_entropy = self.calculate_attention_entropy(attention_map)
        attention_spread = np.std(attention_map)

        return {
            "focus_ratio": float(focus_ratio),
            "center_y": float(center_y),
            "center_x": float(center_x),
            "max_attention": float(np.max(attention_map)),
            "mean_attention": float(np.mean(attention_map)),
            "attention_spread": float(attention_spread),
            "attention_entropy": float(attention_entropy),
            "focus_distribution": self.analyze_focus_distribution(attention_map)
        }

    def calculate_attention_entropy(self, attention_map: np.ndarray) -> float:
        """
        حساب إنتروبيا الانتباه

        المعلمات:
            attention_map: خريطة الانتباه

        العائد:
            قيمة الإنتروبيا
        """

        # تطبيع خريطة الانتباه لتصبح توزيع احتمالي
        normalized_map = attention_map / (np.sum(attention_map) + 1e-8)

        # حساب الإنتروبيا
        entropy = -np.sum(normalized_map * np.log(normalized_map + 1e-8))

        return entropy

    def analyze_focus_distribution(self, attention_map: np.ndarray) -> Dict[str, float]:
        """
        تحليل توزيع التركيز في المناطق المختلفة

        المعلمات:
            attention_map: خريطة الانتباه

        العائد:
            قاموس يحتوي على توزيع التركيز في المناطق المختلفة
        """

        h, w = attention_map.shape

        # تقسيم الصورة إلى 9 مناطق (3x3)
        regions = {}

        for i in range(3):
            for j in range(3):
                start_y = i * h // 3
                end_y = (i + 1) * h // 3
                start_x = j * w // 3
                end_x = (j + 1) * w // 3

                region_attention = attention_map[start_y:end_y, start_x:end_x]
                regions[f"region_{i}_{j}"] = float(np.mean(region_attention))

        return regions

    def create_visual_explanation(self, image_path: str, attention_map: np.ndarray) -> Dict[str, Any]:
        """
        إنشاء تفسير بصري للانتباه

        المعلمات:
            image_path: مسار الصورة
            attention_map: خريطة الانتباه

        العائد:
            قاموس يحتوي على التفسير البصري
        """

        try:
            # تحميل الصورة الأصلية
            original_image = Image.open(image_path).convert('RGB')

            # إنشاء التصور المركب
            explanation_path = self.create_combined_visualization(original_image, attention_map)

            return {
                "has_visualization": explanation_path is not None,
                "explanation_path": explanation_path,
                "attention_summary": self.generate_attention_summary(attention_map)
            }

        except Exception as e:
            logger.error(f"خطأ في إنشاء التفسير البصري: {e}")
            return {"has_visualization": False, "explanation_path": None}

    def create_combined_visualization(self, original_image: Image.Image,
                                      attention_map: np.ndarray) -> Optional[str]:
        """
        إنشاء تصور مركب للصورة وخريطة الانتباه

        المعلمات:
            original_image: الصورة الأصلية
            attention_map: خريطة الانتباه

        العائد:
            مسار الملف المحفوظ أو None في حالة الفشل
        """

        try:
            # إنشاء ملف مؤقت للحفظ
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_path = temp_file.name
            temp_file.close()

            # إنشاء التصور
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))

            # الصورة الأصلية
            axes[0].imshow(original_image)
            axes[0].set_title('الصورة الأصلية')
            axes[0].axis('off')

            # خريطة الانتباه
            im = axes[1].imshow(attention_map, cmap='hot', alpha=0.8)
            axes[1].set_title('خريطة الانتباه')
            axes[1].axis('off')
            plt.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)

            # التصور المركب
            axes[2].imshow(original_image)
            axes[2].imshow(attention_map, cmap='hot', alpha=0.4)
            axes[2].set_title('التصور المركب')
            axes[2].axis('off')

            plt.tight_layout()
            plt.savefig(temp_path, dpi=300, bbox_inches='tight')
            plt.close()

            return temp_path

        except Exception as e:
            logger.error(f"خطأ في إنشاء التصور المركب: {e}")
            return None

    def generate_attention_summary(self, attention_map: np.ndarray) -> str:
        """
        توليد ملخص نصي للانتباه

        المعلمات:
            attention_map: خريطة الانتباه

        العائد:
            ملخص نصي للانتباه
        """

        if attention_map is None:
            return "غير متاح"

        max_attention = np.max(attention_map)

        # تحديد مستوى التركيز
        if max_attention > 0.8:
            focus_level = "عالي جداً"
        elif max_attention > 0.6:
            focus_level = "عالي"
        elif max_attention > 0.4:
            focus_level = "متوسط"
        else:
            focus_level = "منخفض"

        # تحديد نمط التوزيع
        attention_std = np.std(attention_map)
        if attention_std > 0.3:
            distribution_pattern = "متركز في مناطق محددة"
        elif attention_std > 0.15:
            distribution_pattern = "موزع نسبياً"
        else:
            distribution_pattern = "موزع بانتظام"

        summary = f"مستوى التركيز: {focus_level} | النمط: {distribution_pattern}"

        return summary

    def calculate_attention_statistics(self, focus_regions_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        حساب إحصائيات عامة للانتباه

        المعلمات:
            focus_regions_data: بيانات المناطق المركزية

        العائد:
            قاموس يحتوي على إحصائيات الانتباه
        """

        if not focus_regions_data:
            return {}

        # جمع البيانات من جميع الصور
        all_focus_ratios = []
        all_attention_spreads = []
        all_entropies = []

        for image_data in focus_regions_data.values():
            if "focus_ratio" in image_data:
                all_focus_ratios.append(image_data["focus_ratio"])
            if "attention_spread" in image_data:
                all_attention_spreads.append(image_data["attention_spread"])
            if "attention_entropy" in image_data:
                all_entropies.append(image_data["attention_entropy"])

        statistics = {}

        if all_focus_ratios:
            statistics["focus_ratio"] = {
                "mean": float(np.mean(all_focus_ratios)),
                "std": float(np.std(all_focus_ratios)),
                "min": float(np.min(all_focus_ratios)),
                "max": float(np.max(all_focus_ratios))
            }

        if all_attention_spreads:
            statistics["attention_spread"] = {
                "mean": float(np.mean(all_attention_spreads)),
                "std": float(np.std(all_attention_spreads)),
                "min": float(np.min(all_attention_spreads)),
                "max": float(np.max(all_attention_spreads))
            }

        if all_entropies:
            statistics["attention_entropy"] = {
                "mean": float(np.mean(all_entropies)),
                "std": float(np.std(all_entropies)),
                "min": float(np.min(all_entropies)),
                "max": float(np.max(all_entropies))
            }

        return statistics

    def create_attention_comparison(self, models_to_compare: Optional[List[str]] = None) -> None:
        """
        إنشاء مقارنة بين أنماط الانتباه للنماذج المختلفة

        المعلمات:
            models_to_compare: قائمة بأسماء النماذج للمقارنة (اختياري)
        """

        if not self.attention_data:
            logger.warning("لا توجد بيانات انتباه للمقارنة")
            return

        if models_to_compare is None:
            models_to_compare = list(self.attention_data.keys())

        logger.info("إنشاء مقارنة أنماط الانتباه...")

        # إعداد البيانات للمقارنة
        comparison_data = {}

        for model_name in models_to_compare:
            if model_name in self.attention_data:
                stats = self.attention_data[model_name].get("attention_statistics", {})
                comparison_data[model_name] = stats

        # إنشاء المخططات المقارنة
        self.plot_attention_comparison(comparison_data)

        # طباعة جدول المقارنة
        self.print_attention_comparison_table(comparison_data)

    def plot_attention_comparison(self, comparison_data: Dict[str, Dict[str, Any]]) -> None:
        """
        رسم مخططات مقارنة الانتباه

        المعلمات:
            comparison_data: بيانات المقارنة
        """

        if not comparison_data:
            return

        models = list(comparison_data.keys())

        # استخراج البيانات
        focus_means = []
        spread_means = []
        entropy_means = []

        for model in models:
            stats = comparison_data[model]

            focus_means.append(stats.get("focus_ratio", {}).get("mean", 0))
            spread_means.append(stats.get("attention_spread", {}).get("mean", 0))
            entropy_means.append(stats.get("attention_entropy", {}).get("mean", 0))

        # إنشاء المخططات
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('مقارنة أنماط الانتباه بين النماذج', fontsize=16, fontweight='bold')

        # مخطط نسبة التركيز
        bars1 = axes[0].bar(models, focus_means, color='skyblue', alpha=0.7)
        axes[0].set_title('متوسط نسبة التركيز')
        axes[0].set_ylabel('نسبة التركيز')
        axes[0].tick_params(axis='x', rotation=45)

        for bar, value in zip(bars1, focus_means):
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width() / 2., height,
                         f'{value:.3f}', ha='center', va='bottom', fontsize=10)

        # مخطط انتشار الانتباه
        bars2 = axes[1].bar(models, spread_means, color='lightgreen', alpha=0.7)
        axes[1].set_title('متوسط انتشار الانتباه')
        axes[1].set_ylabel('انتشار الانتباه')
        axes[1].tick_params(axis='x', rotation=45)

        for bar, value in zip(bars2, spread_means):
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width() / 2., height,
                         f'{value:.3f}', ha='center', va='bottom', fontsize=10)

        # مخطط إنتروبيا الانتباه
        bars3 = axes[2].bar(models, entropy_means, color='lightcoral', alpha=0.7)
        axes[2].set_title('متوسط إنتروبيا الانتباه')
        axes[2].set_ylabel('الإنتروبيا')
        axes[2].tick_params(axis='x', rotation=45)

        for bar, value in zip(bars3, entropy_means):
            height = bar.get_height()
            axes[2].text(bar.get_x() + bar.get_width() / 2., height,
                         f'{value:.3f}', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        # حفظ المخطط
        output_dir = "/home/ubuntu/gaara_scan_ai_final_4.2/static/reports"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'attention_comparison.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"تم حفظ مخطط مقارنة الانتباه في: {output_path}")

    def print_attention_comparison_table(self, comparison_data: Dict[str, Dict[str, Any]]) -> None:
        """
        طباعة جدول مقارنة الانتباه

        المعلمات:
            comparison_data: بيانات المقارنة
        """

        logger.info("جدول مقارنة أنماط الانتباه")

        import pandas as pd

        data = []
        for model_name, stats in comparison_data.items():
            row = {"النموذج": model_name}

            if "focus_ratio" in stats:
                row["نسبة التركيز"] = f"{stats['focus_ratio']['mean']:.3f} ± {stats['focus_ratio']['std']:.3f}"

            if "attention_spread" in stats:
                row["انتشار الانتباه"] = f"{stats['attention_spread']['mean']:.3f} ± {stats['attention_spread']['std']:.3f}"

            if "attention_entropy" in stats:
                row["إنتروبيا الانتباه"] = f"{stats['attention_entropy']['mean']:.3f} ± {stats['attention_entropy']['std']:.3f}"

            data.append(row)

        if data:
            df = pd.DataFrame(data)
            logger.info("\n" + df.to_string(index=False))

            # تحليل الأنماط
            logger.info("تحليل الأنماط:")

            # النموذج الأكثر تركيزاً
            focus_values = [float(d.get("نسبة التركيز", "0").split(" ± ")[0]) for d in data if "نسبة التركيز" in d]
            if focus_values:
                max_focus_idx = np.argmax(focus_values)
                logger.info(f"• الأكثر تركيزاً: {data[max_focus_idx]['النموذج']}")

            # النموذج الأكثر انتشاراً
            spread_values = [float(d.get("انتشار الانتباه", "0").split(" ± ")[0]) for d in data if "انتشار الانتباه" in d]
            if spread_values:
                max_spread_idx = np.argmax(spread_values)
                logger.info(f"• الأكثر انتشاراً: {data[max_spread_idx]['النموذج']}")

            # النموذج الأكثر تنوعاً (إنتروبيا عالية)
            entropy_values = [float(d.get("إنتروبيا الانتباه", "0").split(" ± ")[0]) for d in data if "إنتروبيا الانتباه" in d]
            if entropy_values:
                max_entropy_idx = np.argmax(entropy_values)
                logger.info(f"• الأكثر تنوعاً: {data[max_entropy_idx]['النموذج']}")
