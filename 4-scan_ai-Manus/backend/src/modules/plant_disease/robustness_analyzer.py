"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/plant_disease/robustness_analyzer.py
الوصف: محلل قوة ومتانة النماذج
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
"""

import json
import os
import tempfile
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from sklearn.metrics import accuracy_score


class RobustnessAnalyzer:
    """محلل قوة ومتانة النماذج"""

    def __init__(self, processor):
        self.processor = processor
        self.robustness_data = {}

    def test_comprehensive_robustness(self, model_name, test_images):
        """اختبار شامل لقوة ومتانة النموذج

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبارات المتانة المختلفة
        """
        print(f"🛡️ اختبار المتانة الشامل للنموذج: {model_name}")

        robustness_tests = {
            "noise_robustness": self.test_noise_robustness(model_name, test_images[:10]),
            "brightness_robustness": self.test_brightness_robustness(model_name, test_images[:10]),
            "contrast_robustness": self.test_contrast_robustness(model_name, test_images[:10]),
            "rotation_robustness": self.test_rotation_robustness(model_name, test_images[:10]),
            "blur_robustness": self.test_blur_robustness(model_name, test_images[:10]),
            "scale_robustness": self.test_scale_robustness(model_name, test_images[:10]),
            "occlusion_robustness": self.test_occlusion_robustness(model_name, test_images[:10]),
            "compression_robustness": self.test_compression_robustness(model_name, test_images[:10])
        }

        # حساب متوسط المتانة
        avg_robustness = {}
        for test_name, test_results in robustness_tests.items():
            if test_results:
                accuracies = []
                for key, value in test_results.items():
                    if isinstance(value, dict) and "accuracy" in value:
                        accuracies.append(value["accuracy"])
                if accuracies:
                    avg_robustness[test_name] = sum(
                        accuracies) / len(accuracies)

        # تصنيف المتانة الإجمالية
        if avg_robustness:
            overall_robustness = sum(
                avg_robustness.values()) / len(avg_robustness)
            robustness_category = self._categorize_robustness(
                overall_robustness)
        else:
            overall_robustness = 0
            robustness_category = "غير معروف"

        # إضافة النتائج الإجمالية
        robustness_tests["overall_results"] = {
            "average_robustness": overall_robustness,
            "robustness_category": robustness_category,
            "test_details": avg_robustness
        }

        # حفظ النتائج
        self.robustness_data[model_name] = robustness_tests

        return robustness_tests

    def _categorize_robustness(self, robustness_score):
        """تصنيف درجة المتانة

        المعلمات:
            robustness_score (float): درجة المتانة (0-1)

        العائد:
            str: تصنيف المتانة
        """
        if robustness_score >= 0.9:
            return "ممتاز"
        elif robustness_score >= 0.8:
            return "جيد جداً"
        elif robustness_score >= 0.7:
            return "جيد"
        elif robustness_score >= 0.6:
            return "متوسط"
        elif robustness_score >= 0.5:
            return "مقبول"
        else:
            return "ضعيف"

    def test_noise_robustness(self, model_name, test_images):
        """اختبار مقاومة الضوضاء

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبار مقاومة الضوضاء
        """
        print(f"  🔊 اختبار مقاومة الضوضاء للنموذج: {model_name}")

        noise_levels = [0.05, 0.1, 0.15, 0.2, 0.25]
        results = {}

        for noise_level in noise_levels:
            original_predictions = []
            noisy_predictions = []

            for image_path in test_images:
                try:
                    original_result = self.processor.predict_single_model(
                        image_path, model_name)
                    if "error" in original_result:
                        continue

                    noisy_image_path = self.add_noise(image_path, noise_level)
                    noisy_result = self.processor.predict_single_model(
                        noisy_image_path, model_name)

                    if "error" not in noisy_result:
                        original_predictions.append(
                            original_result['prediction'])
                        noisy_predictions.append(noisy_result['prediction'])

                    if os.path.exists(noisy_image_path):
                        os.remove(noisy_image_path)

                except Exception:
                    continue

            if original_predictions and noisy_predictions:
                accuracy = accuracy_score(
                    original_predictions, noisy_predictions)
                results[f"noise_{noise_level}"] = {
                    "accuracy": float(accuracy),
                    "samples_tested": len(original_predictions)
                }

        return results

    def add_noise(self, image_path, noise_level):
        """إضافة ضوضاء للصورة

        المعلمات:
            image_path (str): مسار الصورة الأصلية
            noise_level (float): مستوى الضوضاء (0-1)

        العائد:
            str: مسار الصورة المعدلة
        """
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            if image is None:
                return image_path

            # إضافة ضوضاء جاوسية
            mean = 0
            sigma = noise_level * 255
            gauss = np.random.normal(mean, sigma, image.shape)
            gauss = gauss.reshape(image.shape)
            noisy_image = image + gauss
            noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

            # حفظ الصورة المعدلة
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            cv2.imwrite(temp_path, noisy_image)

            return temp_path
        except Exception as e:
            print(f"خطأ في إضافة الضوضاء: {str(e)}")
            return image_path

    def test_brightness_robustness(self, model_name, test_images):
        """اختبار مقاومة تغييرات الإضاءة

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبار مقاومة تغييرات الإضاءة
        """
        print(f"  💡 اختبار مقاومة تغييرات الإضاءة للنموذج: {model_name}")

        brightness_factors = [0.5, 0.75, 1.25, 1.5, 2.0]
        results = {}

        for factor in brightness_factors:
            original_predictions = []
            modified_predictions = []

            for image_path in test_images:
                try:
                    original_result = self.processor.predict_single_model(
                        image_path, model_name)
                    if "error" in original_result:
                        continue

                    modified_image_path = self.adjust_brightness(
                        image_path, factor)
                    modified_result = self.processor.predict_single_model(
                        modified_image_path, model_name)

                    if "error" not in modified_result:
                        original_predictions.append(
                            original_result['prediction'])
                        modified_predictions.append(
                            modified_result['prediction'])

                    if os.path.exists(modified_image_path):
                        os.remove(modified_image_path)

                except Exception:
                    continue

            if original_predictions and modified_predictions:
                accuracy = accuracy_score(
                    original_predictions, modified_predictions)
                results[f"brightness_{factor}"] = {
                    "accuracy": float(accuracy),
                    "samples_tested": len(original_predictions)
                }

        return results

    def adjust_brightness(self, image_path, factor):
        """تعديل إضاءة الصورة

        المعلمات:
            image_path (str): مسار الصورة الأصلية
            factor (float): عامل تعديل الإضاءة

        العائد:
            str: مسار الصورة المعدلة
        """
        try:
            # قراءة الصورة
            image = Image.open(image_path)

            # تعديل الإضاءة
            enhancer = ImageEnhance.Brightness(image)
            modified_image = enhancer.enhance(factor)

            # حفظ الصورة المعدلة
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            modified_image.save(temp_path)

            return temp_path
        except Exception as e:
            print(f"خطأ في تعديل الإضاءة: {str(e)}")
            return image_path

    def test_contrast_robustness(self, model_name, test_images):
        """اختبار مقاومة تغييرات التباين

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبار مقاومة تغييرات التباين
        """
        print(f"  🌓 اختبار مقاومة تغييرات التباين للنموذج: {model_name}")

        contrast_factors = [0.5, 0.75, 1.25, 1.5, 2.0]
        results = {}

        for factor in contrast_factors:
            original_predictions = []
            modified_predictions = []

            for image_path in test_images:
                try:
                    original_result = self.processor.predict_single_model(
                        image_path, model_name)
                    if "error" in original_result:
                        continue

                    modified_image_path = self.adjust_contrast(
                        image_path, factor)
                    modified_result = self.processor.predict_single_model(
                        modified_image_path, model_name)

                    if "error" not in modified_result:
                        original_predictions.append(
                            original_result['prediction'])
                        modified_predictions.append(
                            modified_result['prediction'])

                    if os.path.exists(modified_image_path):
                        os.remove(modified_image_path)

                except Exception:
                    continue

            if original_predictions and modified_predictions:
                accuracy = accuracy_score(
                    original_predictions, modified_predictions)
                results[f"contrast_{factor}"] = {
                    "accuracy": float(accuracy),
                    "samples_tested": len(original_predictions)
                }

        return results

    def adjust_contrast(self, image_path, factor):
        """تعديل تباين الصورة

        المعلمات:
            image_path (str): مسار الصورة الأصلية
            factor (float): عامل تعديل التباين

        العائد:
            str: مسار الصورة المعدلة
        """
        try:
            # قراءة الصورة
            image = Image.open(image_path)

            # تعديل التباين
            enhancer = ImageEnhance.Contrast(image)
            modified_image = enhancer.enhance(factor)

            # حفظ الصورة المعدلة
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            modified_image.save(temp_path)

            return temp_path
        except Exception as e:
            print(f"خطأ في تعديل التباين: {str(e)}")
            return image_path

    def test_rotation_robustness(self, model_name, test_images):
        """اختبار مقاومة الدوران

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبار مقاومة الدوران
        """
        print(f"  🔄 اختبار مقاومة الدوران للنموذج: {model_name}")

        rotation_angles = [15, 30, 45, 60, 90]
        results = {}

        for angle in rotation_angles:
            original_predictions = []
            modified_predictions = []

            for image_path in test_images:
                try:
                    original_result = self.processor.predict_single_model(
                        image_path, model_name)
                    if "error" in original_result:
                        continue

                    modified_image_path = self.rotate_image(image_path, angle)
                    modified_result = self.processor.predict_single_model(
                        modified_image_path, model_name)

                    if "error" not in modified_result:
                        original_predictions.append(
                            original_result['prediction'])
                        modified_predictions.append(
                            modified_result['prediction'])

                    if os.path.exists(modified_image_path):
                        os.remove(modified_image_path)

                except Exception:
                    continue

            if original_predictions and modified_predictions:
                accuracy = accuracy_score(
                    original_predictions, modified_predictions)
                results[f"rotation_{angle}"] = {
                    "accuracy": float(accuracy),
                    "samples_tested": len(original_predictions)
                }

        return results

    def rotate_image(self, image_path, angle):
        """دوران الصورة

        المعلمات:
            image_path (str): مسار الصورة الأصلية
            angle (float): زاوية الدوران بالدرجات

        العائد:
            str: مسار الصورة المعدلة
        """
        try:
            # قراءة الصورة
            image = Image.open(image_path)

            # دوران الصورة
            rotated_image = image.rotate(angle, expand=True)

            # حفظ الصورة المعدلة
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            rotated_image.save(temp_path)

            return temp_path
        except Exception as e:
            print(f"خطأ في دوران الصورة: {str(e)}")
            return image_path

    def test_blur_robustness(self, model_name, test_images):
        """اختبار مقاومة الضبابية

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبار مقاومة الضبابية
        """
        print(f"  🌫️ اختبار مقاومة الضبابية للنموذج: {model_name}")

        blur_radii = [1, 2, 3, 4, 5]
        results = {}

        for radius in blur_radii:
            original_predictions = []
            blurred_predictions = []

            for image_path in test_images:
                try:
                    original_result = self.processor.predict_single_model(
                        image_path, model_name)
                    if "error" in original_result:
                        continue

                    blurred_image_path = self.blur_image(image_path, radius)
                    blurred_result = self.processor.predict_single_model(
                        blurred_image_path, model_name)

                    if "error" not in blurred_result:
                        original_predictions.append(
                            original_result['prediction'])
                        blurred_predictions.append(
                            blurred_result['prediction'])

                    if os.path.exists(blurred_image_path):
                        os.remove(blurred_image_path)

                except Exception:
                    continue

            if original_predictions and blurred_predictions:
                accuracy = accuracy_score(
                    original_predictions, blurred_predictions)
                results[f"blur_{radius}"] = {
                    "accuracy": float(accuracy),
                    "samples_tested": len(original_predictions)
                }

        return results

    def blur_image(self, image_path, radius):
        """تضبيب الصورة

        المعلمات:
            image_path (str): مسار الصورة الأصلية
            radius (int): نصف قطر الضبابية

        العائد:
            str: مسار الصورة المعدلة
        """
        try:
            # قراءة الصورة
            image = Image.open(image_path)

            # تضبيب الصورة
            blurred_image = image.filter(
                ImageFilter.GaussianBlur(radius=radius))

            # حفظ الصورة المعدلة
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            blurred_image.save(temp_path)

            return temp_path
        except Exception as e:
            print(f"خطأ في تضبيب الصورة: {str(e)}")
            return image_path

    def test_scale_robustness(self, model_name, test_images):
        """اختبار مقاومة تغيير الحجم

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبار مقاومة تغيير الحجم
        """
        print(f"  📏 اختبار مقاومة تغيير الحجم للنموذج: {model_name}")

        scale_factors = [0.5, 0.75, 1.25, 1.5, 2.0]
        results = {}

        for factor in scale_factors:
            original_predictions = []
            scaled_predictions = []

            for image_path in test_images:
                try:
                    original_result = self.processor.predict_single_model(
                        image_path, model_name)
                    if "error" in original_result:
                        continue

                    scaled_image_path = self.scale_image(image_path, factor)
                    scaled_result = self.processor.predict_single_model(
                        scaled_image_path, model_name)

                    if "error" not in scaled_result:
                        original_predictions.append(
                            original_result['prediction'])
                        scaled_predictions.append(scaled_result['prediction'])

                    if os.path.exists(scaled_image_path):
                        os.remove(scaled_image_path)

                except Exception:
                    continue

            if original_predictions and scaled_predictions:
                accuracy = accuracy_score(
                    original_predictions, scaled_predictions)
                results[f"scale_{factor}"] = {
                    "accuracy": float(accuracy),
                    "samples_tested": len(original_predictions)
                }

        return results

    def scale_image(self, image_path, factor):
        """تغيير حجم الصورة

        المعلمات:
            image_path (str): مسار الصورة الأصلية
            factor (float): عامل تغيير الحجم

        العائد:
            str: مسار الصورة المعدلة
        """
        try:
            # قراءة الصورة
            image = Image.open(image_path)

            # تغيير حجم الصورة
            width, height = image.size
            new_width = int(width * factor)
            new_height = int(height * factor)
            scaled_image = image.resize((new_width, new_height), Image.LANCZOS)

            # إعادة تغيير الحجم إلى الحجم الأصلي
            scaled_image = scaled_image.resize((width, height), Image.LANCZOS)

            # حفظ الصورة المعدلة
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            scaled_image.save(temp_path)

            return temp_path
        except Exception as e:
            print(f"خطأ في تغيير حجم الصورة: {str(e)}")
            return image_path

    def test_occlusion_robustness(self, model_name, test_images):
        """اختبار مقاومة الحجب

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبار مقاومة الحجب
        """
        print(f"  🚫 اختبار مقاومة الحجب للنموذج: {model_name}")

        occlusion_percentages = [0.1, 0.2, 0.3, 0.4, 0.5]
        results = {}

        for percentage in occlusion_percentages:
            original_predictions = []
            occluded_predictions = []

            for image_path in test_images:
                try:
                    original_result = self.processor.predict_single_model(
                        image_path, model_name)
                    if "error" in original_result:
                        continue

                    occluded_image_path = self.add_occlusion(
                        image_path, percentage)
                    occluded_result = self.processor.predict_single_model(
                        occluded_image_path, model_name)

                    if "error" not in occluded_result:
                        original_predictions.append(
                            original_result['prediction'])
                        occluded_predictions.append(
                            occluded_result['prediction'])

                    if os.path.exists(occluded_image_path):
                        os.remove(occluded_image_path)

                except Exception:
                    continue

            if original_predictions and occluded_predictions:
                accuracy = accuracy_score(
                    original_predictions, occluded_predictions)
                results[f"occlusion_{percentage}"] = {
                    "accuracy": float(accuracy),
                    "samples_tested": len(original_predictions)
                }

        return results

    def add_occlusion(self, image_path, percentage):
        """إضافة حجب للصورة

        المعلمات:
            image_path (str): مسار الصورة الأصلية
            percentage (float): نسبة الحجب (0-1)

        العائد:
            str: مسار الصورة المعدلة
        """
        try:
            # قراءة الصورة
            image = cv2.imread(image_path)
            if image is None:
                return image_path

            # الحصول على أبعاد الصورة
            height, width = image.shape[:2]

            # حساب حجم المستطيل
            rect_width = int(width * np.sqrt(percentage))
            rect_height = int(height * np.sqrt(percentage))

            # اختيار موقع عشوائي للمستطيل
            x = np.random.randint(0, width - rect_width)
            y = np.random.randint(0, height - rect_height)

            # إضافة المستطيل الأسود
            image[y:y + rect_height, x:x + rect_width] = 0

            # حفظ الصورة المعدلة
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            cv2.imwrite(temp_path, image)

            return temp_path
        except Exception as e:
            print(f"خطأ في إضافة الحجب: {str(e)}")
            return image_path

    def test_compression_robustness(self, model_name, test_images):
        """اختبار مقاومة الضغط

        المعلمات:
            model_name (str): اسم النموذج المراد اختباره
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج اختبار مقاومة الضغط
        """
        print(f"  📉 اختبار مقاومة الضغط للنموذج: {model_name}")

        quality_levels = [90, 70, 50, 30, 10]
        results = {}

        for quality in quality_levels:
            original_predictions = []
            compressed_predictions = []

            for image_path in test_images:
                try:
                    original_result = self.processor.predict_single_model(
                        image_path, model_name)
                    if "error" in original_result:
                        continue

                    compressed_image_path = self.compress_image(
                        image_path, quality)
                    compressed_result = self.processor.predict_single_model(
                        compressed_image_path, model_name)

                    if "error" not in compressed_result:
                        original_predictions.append(
                            original_result['prediction'])
                        compressed_predictions.append(
                            compressed_result['prediction'])

                    if os.path.exists(compressed_image_path):
                        os.remove(compressed_image_path)

                except Exception:
                    continue

            if original_predictions and compressed_predictions:
                accuracy = accuracy_score(
                    original_predictions, compressed_predictions)
                results[f"compression_{quality}"] = {
                    "accuracy": float(accuracy),
                    "samples_tested": len(original_predictions)
                }

        return results

    def compress_image(self, image_path, quality):
        """ضغط الصورة

        المعلمات:
            image_path (str): مسار الصورة الأصلية
            quality (int): جودة الضغط (0-100)

        العائد:
            str: مسار الصورة المعدلة
        """
        try:
            # قراءة الصورة
            image = Image.open(image_path)

            # حفظ الصورة بجودة منخفضة
            fd, temp_path = tempfile.mkstemp(suffix=".jpg")
            os.close(fd)
            image.save(temp_path, quality=quality)

            return temp_path
        except Exception as e:
            print(f"خطأ في ضغط الصورة: {str(e)}")
            return image_path

    def create_robustness_comparison(self, models_to_compare, test_images):
        """إنشاء مقارنة متانة بين النماذج

        المعلمات:
            models_to_compare (list): قائمة بأسماء النماذج للمقارنة
            test_images (list): قائمة بمسارات الصور للاختبار

        العائد:
            dict: نتائج مقارنة المتانة
        """
        print(f"📊 إنشاء مقارنة متانة بين {len(models_to_compare)} نماذج")

        # اختبار متانة كل نموذج
        for model_name in models_to_compare:
            if model_name not in self.robustness_data:
                self.test_comprehensive_robustness(model_name, test_images)

        # إنشاء مقارنة
        comparison = {
            "models": models_to_compare,
            "test_images_count": len(test_images),
            "timestamp": time.time(),
            "comparison_results": {}
        }

        # مقارنة نتائج كل اختبار
        test_types = [
            "noise_robustness",
            "brightness_robustness",
            "contrast_robustness",
            "rotation_robustness",
            "blur_robustness",
            "scale_robustness",
            "occlusion_robustness",
            "compression_robustness"
        ]

        for test_type in test_types:
            comparison["comparison_results"][test_type] = {}
            for model_name in models_to_compare:
                if model_name in self.robustness_data and test_type in self.robustness_data[
                        model_name]:
                    comparison["comparison_results"][test_type][model_name] = self.robustness_data[model_name][test_type]

        # إضافة النتائج الإجمالية
        comparison["overall_comparison"] = {}
        for model_name in models_to_compare:
            if model_name in self.robustness_data and "overall_results" in self.robustness_data[
                    model_name]:
                comparison["overall_comparison"][model_name] = self.robustness_data[model_name]["overall_results"]

        # تحديد النموذج الأكثر متانة
        if comparison["overall_comparison"]:
            best_model = max(
                comparison["overall_comparison"].items(),
                key=lambda x: x[1]["average_robustness"] if "average_robustness" in x[1] else 0)
            comparison["most_robust_model"] = {
                "model_name": best_model[0], "average_robustness": best_model[1].get(
                    "average_robustness", 0), "robustness_category": best_model[1].get(
                    "robustness_category", "غير معروف")}

        return comparison

    def visualize_robustness_comparison(
            self, comparison_results, output_dir=None):
        """تصور مقارنة المتانة بين النماذج

        المعلمات:
            comparison_results (dict): نتائج مقارنة المتانة
            output_dir (str, optional): مسار حفظ المخططات البيانية

        العائد:
            dict: مسارات المخططات البيانية
        """
        if not comparison_results or "models" not in comparison_results:
            return {}

        models = comparison_results["models"]
        if not models:
            return {}

        # إنشاء مجلد الإخراج إذا لم يكن موجوداً
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        plots = {}

        # مخطط المتانة الإجمالية
        if "overall_comparison" in comparison_results:
            plt.figure(figsize=(10, 6))
            model_names = []
            robustness_scores = []

            for model_name in models:
                if model_name in comparison_results["overall_comparison"]:
                    model_names.append(model_name)
                    robustness_scores.append(
                        comparison_results["overall_comparison"][model_name].get(
                            "average_robustness", 0))

            if model_names and robustness_scores:
                plt.bar(model_names, robustness_scores, color='skyblue')
                plt.xlabel('النماذج')
                plt.ylabel('متوسط المتانة')
                plt.title('مقارنة المتانة الإجمالية بين النماذج')
                plt.ylim(0, 1)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()

                if output_dir:
                    plot_path = os.path.join(
                        output_dir, "overall_robustness_comparison.png")
                    plt.savefig(plot_path)
                    plots["overall_robustness"] = plot_path
                else:
                    plt.close()

        # مخططات لكل نوع من اختبارات المتانة
        test_types = [
            ("noise_robustness", "مقاومة الضوضاء"),
            ("brightness_robustness", "مقاومة تغييرات الإضاءة"),
            ("contrast_robustness", "مقاومة تغييرات التباين"),
            ("rotation_robustness", "مقاومة الدوران"),
            ("blur_robustness", "مقاومة الضبابية"),
            ("scale_robustness", "مقاومة تغيير الحجم"),
            ("occlusion_robustness", "مقاومة الحجب"),
            ("compression_robustness", "مقاومة الضغط")
        ]

        for test_type, test_title in test_types:
            if test_type in comparison_results["comparison_results"]:
                plt.figure(figsize=(12, 7))

                for model_name in models:
                    if model_name in comparison_results["comparison_results"][test_type]:
                        test_results = comparison_results["comparison_results"][test_type][model_name]

                        x_values = []
                        y_values = []

                        for key, value in test_results.items():
                            if isinstance(value, dict) and "accuracy" in value:
                                # استخراج القيمة الرقمية من المفتاح
                                param_value = float(key.split('_')[1])
                                x_values.append(param_value)
                                y_values.append(value["accuracy"])

                        if x_values and y_values:
                            # ترتيب النقاط حسب قيمة x
                            points = sorted(zip(x_values, y_values))
                            x_values = [p[0] for p in points]
                            y_values = [p[1] for p in points]

                            plt.plot(
                                x_values, y_values, marker='o', label=model_name)

                plt.xlabel('مستوى التغيير')
                plt.ylabel('الدقة')
                plt.title(f'مقارنة {test_title} بين النماذج')
                plt.ylim(0, 1)
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.legend()
                plt.tight_layout()

                if output_dir:
                    plot_path = os.path.join(
                        output_dir, f"{test_type}_comparison.png")
                    plt.savefig(plot_path)
                    plots[test_type] = plot_path
                else:
                    plt.close()

        return plots

    def generate_robustness_report(self, comparison_results, output_dir=None):
        """إنشاء تقرير متانة للنماذج

        المعلمات:
            comparison_results (dict): نتائج مقارنة المتانة
            output_dir (str, optional): مسار حفظ التقرير

        العائد:
            str: مسار التقرير
        """
        if not comparison_results or "models" not in comparison_results:
            return None

        models = comparison_results["models"]
        if not models:
            return None

        # إنشاء مجلد الإخراج إذا لم يكن موجوداً
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # إنشاء المخططات البيانية
        plots = self.visualize_robustness_comparison(
            comparison_results, output_dir)

        # إنشاء التقرير
        report = {
            "title": "تقرير متانة النماذج",
            "timestamp": time.time(),
            "models_compared": models,
            "test_images_count": comparison_results.get(
                "test_images_count",
                0),
            "overall_results": comparison_results.get(
                "overall_comparison",
                {}),
            "most_robust_model": comparison_results.get(
                "most_robust_model",
                {}),
            "detailed_results": comparison_results.get(
                "comparison_results",
                {}),
            "plots": plots}

        # حفظ التقرير
        if output_dir:
            report_path = os.path.join(output_dir, "robustness_report.json")
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            return report_path

        return None

    def analyze_robustness_data(self, comparison_results):
        """تحليل بيانات المتانة واستخلاص الرؤى

        المعلمات:
            comparison_results (dict): نتائج مقارنة المتانة

        العائد:
            dict: الرؤى المستخلصة من بيانات المتانة
        """
        if not comparison_results or "models" not in comparison_results:
            return {}

        models = comparison_results["models"]
        if not models:
            return {}

        insights = {
            "strengths_and_weaknesses": {},
            "recommendations": {},
            "comparative_analysis": {}
        }

        # تحليل نقاط القوة والضعف لكل نموذج
        for model_name in models:
            strengths = []
            weaknesses = []

            if "overall_comparison" in comparison_results and model_name in comparison_results[
                    "overall_comparison"]:
                # تحليل نتائج الاختبارات المختلفة
                test_types = [
                    ("noise_robustness", "مقاومة الضوضاء"),
                    ("brightness_robustness", "مقاومة تغييرات الإضاءة"),
                    ("contrast_robustness", "مقاومة تغييرات التباين"),
                    ("rotation_robustness", "مقاومة الدوران"),
                    ("blur_robustness", "مقاومة الضبابية"),
                    ("scale_robustness", "مقاومة تغيير الحجم"),
                    ("occlusion_robustness", "مقاومة الحجب"),
                    ("compression_robustness", "مقاومة الضغط")
                ]

                for test_type, test_name in test_types:
                    if test_type in comparison_results["comparison_results"] and model_name in comparison_results["comparison_results"][test_type]:
                        test_results = comparison_results["comparison_results"][test_type][model_name]
                        accuracies = [
                            value["accuracy"] for key,
                            value in test_results.items() if isinstance(
                                value,
                                dict) and "accuracy" in value]

                        if accuracies:
                            avg_accuracy = sum(accuracies) / len(accuracies)
                            if avg_accuracy >= 0.8:
                                strengths.append(
                                    f"{test_name} ({avg_accuracy:.2f})")
                            elif avg_accuracy <= 0.5:
                                weaknesses.append(
                                    f"{test_name} ({avg_accuracy:.2f})")

            insights["strengths_and_weaknesses"][model_name] = {
                "strengths": strengths,
                "weaknesses": weaknesses
            }

            # توصيات لتحسين المتانة
            recommendations = []
            if "weaknesses" in insights["strengths_and_weaknesses"][model_name]:
                for weakness in insights["strengths_and_weaknesses"][model_name]["weaknesses"]:
                    if "الضوضاء" in weakness:
                        recommendations.append(
                            "تحسين مقاومة الضوضاء عن طريق تدريب النموذج على صور مع ضوضاء مختلفة")
                    elif "الإضاءة" in weakness:
                        recommendations.append(
                            "تحسين مقاومة تغييرات الإضاءة عن طريق تدريب النموذج على صور بمستويات إضاءة مختلفة")
                    elif "التباين" in weakness:
                        recommendations.append(
                            "تحسين مقاومة تغييرات التباين عن طريق تدريب النموذج على صور بمستويات تباين مختلفة")
                    elif "الدوران" in weakness:
                        recommendations.append(
                            "تحسين مقاومة الدوران عن طريق تدريب النموذج على صور مدورة بزوايا مختلفة")
                    elif "الضبابية" in weakness:
                        recommendations.append(
                            "تحسين مقاومة الضبابية عن طريق تدريب النموذج على صور مضببة بدرجات مختلفة")
                    elif "الحجم" in weakness:
                        recommendations.append(
                            "تحسين مقاومة تغيير الحجم عن طريق تدريب النموذج على صور بأحجام مختلفة")
                    elif "الحجب" in weakness:
                        recommendations.append(
                            "تحسين مقاومة الحجب عن طريق تدريب النموذج على صور مع حجب جزئي")
                    elif "الضغط" in weakness:
                        recommendations.append(
                            "تحسين مقاومة الضغط عن طريق تدريب النموذج على صور مضغوطة بجودات مختلفة")

            insights["recommendations"][model_name] = recommendations

        # تحليل مقارن بين النماذج
        if "overall_comparison" in comparison_results:
            # النموذج الأكثر متانة
            most_robust_model = max(
                [
                    (model,
                     data.get(
                         "average_robustness",
                         0)) for model,
                    data in comparison_results["overall_comparison"].items()],
                key=lambda x: x[1])
            insights["comparative_analysis"]["most_robust_model"] = most_robust_model[0]

            # النموذج الأقل متانة
            least_robust_model = min(
                [
                    (model,
                     data.get(
                         "average_robustness",
                         0)) for model,
                    data in comparison_results["overall_comparison"].items()],
                key=lambda x: x[1])
            insights["comparative_analysis"]["least_robust_model"] = least_robust_model[0]

            # تحليل نقاط القوة المشتركة والضعف المشتركة
            common_strengths = set()
            common_weaknesses = set()
            first_model = True

            for model_name in models:
                if model_name in insights["strengths_and_weaknesses"]:
                    strengths = set([s.split(
                        " (")[0] for s in insights["strengths_and_weaknesses"][model_name]["strengths"]])
                    weaknesses = set([w.split(
                        " (")[0] for w in insights["strengths_and_weaknesses"][model_name]["weaknesses"]])

                    if first_model:
                        common_strengths = strengths
                        common_weaknesses = weaknesses
                        first_model = False
                    else:
                        common_strengths &= strengths
                        common_weaknesses &= weaknesses

            insights["comparative_analysis"]["common_strengths"] = list(
                common_strengths)
            insights["comparative_analysis"]["common_weaknesses"] = list(
                common_weaknesses)

        return insights


# مثال على الاستخدام
if __name__ == "__main__":
    print("✅ تم تحميل محلل المتانة بنجاح!")
