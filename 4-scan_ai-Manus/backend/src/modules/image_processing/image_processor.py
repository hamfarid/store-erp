# File:
# /home/ubuntu/ai_web_organized/src/modules/image_processing/image_processor.py

"""
معالج الصور الزراعية
يوفر هذا الملف وظائف لمعالجة وتحليل الصور الزراعية

NOTE: This module requires tensorflow and keras. Install with:
    pip install tensorflow pillow
"""

# Standard library imports
import json
import logging
import os
from datetime import datetime

# Third-party imports
import cv2  # pylint: disable=import-error
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input

# Constants
QUALITY_MEDIUM = 'متوسط'
UNKNOWN = 'غير معروف'
QUALITY_AVERAGE = 'مقبول'
QUALITY_HIGH = 'عالي'

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ImageProcessor:
    """معالج الصور الزراعية"""

    def __init__(self, model_path=None):
        """تهيئة معالج الصور"""
        # مسار حفظ الصور المعالجة
        self.processed_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'processed')
        os.makedirs(self.processed_dir, exist_ok=True)

        # مسار حفظ نتائج التحليل
        self.results_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'results')
        os.makedirs(self.results_dir, exist_ok=True)

        # تحميل نموذج التعلم العميق
        self.model = self._load_model(model_path)

        # سجل معالجة الصور
        self.processing_history = []

        logger.info("تم تهيئة معالج الصور الزراعية")

    def _load_model(self, model_path=None):
        """
        تحميل نموذج التعلم العميق

        المعلمات:
            model_path (str, optional): مسار ملف النموذج

        العائد:
            object: نموذج التعلم العميق
        """
        try:
            if model_path and os.path.exists(model_path):
                # تحميل نموذج مخصص
                logger.info("جاري تحميل النموذج من: %s", model_path)
                model = tf.keras.models.load_model(model_path)
            else:
                # استخدام نموذج ResNet-50 المدرب مسبقًا
                logger.info("جاري تحميل نموذج ResNet-50 المدرب مسبقًا")
                model = ResNet50(
                    weights='imagenet',
                    include_top=False,
                    pooling='avg')

            return model

        except Exception as e:
            logger.error("خطأ أثناء تحميل النموذج: %s", str(e))
            # إرجاع نموذج ResNet-50 كبديل
            return ResNet50(
                weights='imagenet',
                include_top=False,
                pooling='avg')

    def process_image(
            self,
            image_path,
            crop_type=None,
            processing_options=None):
        """
        معالجة الصورة وتحليلها

        المعلمات:
            image_path (str): مسار ملف الصورة
            crop_type (str, optional): نوع المحصول
            processing_options (dict, optional): خيارات المعالجة

        العائد:
            dict: نتيجة المعالجة
        """
        try:
            logger.info("بدء معالجة الصورة: %s", image_path)

            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                logger.error("الصورة غير موجودة: %s", image_path)
                return {
                    "success": False,
                    "error": "الصورة غير موجودة",
                    "timestamp": datetime.now().isoformat()
                }

            # تحميل الصورة
            img = cv2.imread(image_path)  # pylint: disable=no-member
            if img is None:
                logger.error("فشل في قراءة الصورة: %s", image_path)
                return {
                    "success": False,
                    "error": "فشل في قراءة الصورة",
                    "timestamp": datetime.now().isoformat()
                }

            # تحويل الصورة من BGR إلى RGB
            img_rgb = cv2.cvtColor(
                img, cv2.COLOR_BGR2RGB)  # pylint: disable=no-member

            # تحسين جودة الصورة
            enhanced_img = self._enhance_image(img_rgb, processing_options)

            # استخراج ميزات الصورة
            features = self._extract_features(enhanced_img)

            # تحليل الصورة
            analysis_result = self._analyze_image(
                enhanced_img, features, crop_type)

            # حفظ الصورة المعالجة
            processed_image_path = self._save_processed_image(
                enhanced_img, image_path)

            # إعداد نتيجة المعالجة
            processing_result = {
                "success": True,
                "original_image": image_path,
                "processed_image": processed_image_path,
                "timestamp": datetime.now().isoformat(),
                "features": features,
                "analysis": analysis_result
            }

            # إضافة نوع المحصول إذا كان متوفرًا
            if crop_type:
                processing_result["crop_type"] = crop_type

            # حفظ نتيجة المعالجة
            self._save_processing_result(processing_result)

            # إضافة المعالجة إلى السجل
            self.processing_history.append({
                "timestamp": processing_result["timestamp"],
                "image_path": image_path,
                "crop_type": crop_type,
                "result": "success"
            })

            logger.info("تم الانتهاء من معالجة الصورة: %s", image_path)

            return processing_result

        except Exception as e:
            logger.error("خطأ أثناء معالجة الصورة: %s", str(e))
            return {
                "success": False,
                "error": "خطأ أثناء معالجة الصورة: %s" % str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _enhance_image(self, img, options=None):
        """
        تحسين جودة الصورة

        المعلمات:
            img (numpy.ndarray): الصورة
            options (dict, optional): خيارات التحسين

        العائد:
            numpy.ndarray: الصورة المحسنة
        """
        try:
            # نسخة من الصورة الأصلية
            enhanced = img.copy()

            # تهيئة خيارات التحسين
            if options is None:
                options = {}

            # تطبيق تحسين التباين
            if options.get("enhance_contrast", True):
                # تحويل الصورة إلى LAB
                lab = cv2.cvtColor(
                    enhanced, cv2.COLOR_RGB2LAB)  # pylint: disable=no-member
                # تقسيم القنوات
                l, a, b = cv2.split(lab)  # pylint: disable=no-member
                # تطبيق تحسين التباين على قناة الإضاءة
                clahe = cv2.createCLAHE(
                    clipLimit=2.0, tileGridSize=(
                        8, 8))  # pylint: disable=no-member
                cl = clahe.apply(l)
                # دمج القنوات
                limg = cv2.merge((cl, a, b))  # pylint: disable=no-member
                # تحويل الصورة مرة أخرى إلى RGB
                enhanced = cv2.cvtColor(
                    limg, cv2.COLOR_LAB2RGB)  # pylint: disable=no-member

            # تطبيق تقليل الضوضاء
            if options.get("reduce_noise", True):
                enhanced = cv2.fastNlMeansDenoisingColored(
                    enhanced, None, 10, 10, 7, 21)  # pylint: disable=no-member

            # تطبيق تحسين الحدة
            if options.get("sharpen", True):
                kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                enhanced = cv2.filter2D(
                    enhanced, -1, kernel)  # pylint: disable=no-member

            return enhanced

        except Exception as e:
            logger.error("خطأ أثناء تحسين الصورة: %s", str(e))
            return img

    def _extract_features(self, img):
        """
        استخراج ميزات الصورة

        المعلمات:
            img (numpy.ndarray): الصورة

        العائد:
            dict: ميزات الصورة
        """
        try:
            features = {}

            # حساب هيستوجرام الألوان
            color_hist = self._calculate_color_histogram(img)
            features["color_histogram"] = color_hist

            # استخراج ميزات النسيج
            texture_features = self._calculate_texture_features(img)
            features["texture_features"] = texture_features

            # استخراج ميزات الشكل
            shape_features = self._calculate_shape_features(img)
            features["shape_features"] = shape_features

            # استخراج ميزات التعلم العميق
            deep_features = self._extract_deep_features(img)
            features["deep_features"] = deep_features

            # حساب درجة جودة الصورة
            quality_score = self._calculate_quality_score(img)
            features["quality_score"] = quality_score

            return features

        except Exception as e:
            logger.error("خطأ أثناء استخراج ميزات الصورة: %s", str(e))
            return {}

    def _calculate_color_histogram(self, img):
        """
        حساب هيستوجرام الألوان

        المعلمات:
            img (numpy.ndarray): الصورة

        العائد:
            dict: هيستوجرام الألوان
        """
        try:
            # تقسيم قنوات الألوان
            channels = cv2.split(img)  # pylint: disable=no-member

            # حساب هيستوجرام لكل قناة
            hist_r = cv2.calcHist([channels[0]], [0], None, [256], [
                                  0, 256])  # pylint: disable=no-member
            hist_g = cv2.calcHist([channels[1]], [0], None, [256], [
                                  0, 256])  # pylint: disable=no-member
            hist_b = cv2.calcHist([channels[2]], [0], None, [256], [
                                  0, 256])  # pylint: disable=no-member

            # تطبيع الهيستوجرام
            hist_r = cv2.normalize(
                hist_r, hist_r).flatten()  # pylint: disable=no-member
            hist_g = cv2.normalize(
                hist_g, hist_g).flatten()  # pylint: disable=no-member
            hist_b = cv2.normalize(
                hist_b, hist_b).flatten()  # pylint: disable=no-member

            return {
                "red": hist_r.tolist(),
                "green": hist_g.tolist(),
                "blue": hist_b.tolist()
            }

        except Exception as e:
            logger.error("خطأ أثناء حساب هيستوجرام الألوان: %s", str(e))
            return {}

    def _calculate_texture_features(self, img):
        """
        حساب ميزات النسيج

        المعلمات:
            img (numpy.ndarray): الصورة

        العائد:
            dict: ميزات النسيج
        """
        try:
            # تحويل الصورة إلى HSV
            hsv = cv2.cvtColor(
                img, cv2.COLOR_RGB2HSV)  # pylint: disable=no-member
            h, s, v = cv2.split(hsv)  # pylint: disable=no-member

            # حساب الإحصائيات الأساسية
            texture_features = {
                "hue_mean": float(np.mean(h)),
                "hue_std": float(np.std(h)),
                "saturation_mean": float(np.mean(s)),
                "saturation_std": float(np.std(s)),
                "value_mean": float(np.mean(v)),
                "value_std": float(np.std(v))
            }

            return texture_features

        except Exception as e:
            logger.error("خطأ أثناء حساب ميزات النسيج: %s", str(e))
            return {}

    def _calculate_shape_features(self, img):
        """
        حساب ميزات الشكل

        المعلمات:
            img (numpy.ndarray): الصورة

        العائد:
            dict: ميزات الشكل
        """
        try:
            # تحويل الصورة إلى رمادي
            gray = cv2.cvtColor(
                img, cv2.COLOR_RGB2GRAY)  # pylint: disable=no-member

            # تطبيق عتبة للحصول على صورة ثنائية
            _, binary = cv2.threshold(
                gray, 128, 255, cv2.THRESH_BINARY)  # pylint: disable=no-member

            # العثور على الكنتورات
            contours, _ = cv2.findContours(
                binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # pylint: disable=no-member

            if not contours:
                return {"contour_count": 0}

            # حساب ميزات الشكل للكنتور الأكبر
            largest_contour = max(
                contours, key=cv2.contourArea)  # pylint: disable=no-member
            area = cv2.contourArea(
                largest_contour)  # pylint: disable=no-member

            # حساب المحيط
            perimeter = cv2.arcLength(
                largest_contour, True)  # pylint: disable=no-member

            # حساب نسبة الدائرية
            circularity = 4 * np.pi * area / \
                (perimeter * perimeter) if perimeter > 0 else 0

            shape_features = {
                "contour_count": len(contours),
                "largest_area": float(area),
                "largest_perimeter": float(perimeter),
                "circularity": float(circularity)
            }

            return shape_features

        except Exception as e:
            logger.error("خطأ أثناء حساب ميزات الشكل: %s", str(e))
            return {}

    def _extract_deep_features(self, img):
        """
        استخراج ميزات التعلم العميق

        المعلمات:
            img (numpy.ndarray): الصورة

        العائد:
            list: ميزات التعلم العميق
        """
        try:
            # تغيير حجم الصورة للنموذج
            resized_img = cv2.resize(
                img, (224, 224))  # pylint: disable=no-member

            # تحضير الصورة للنموذج
            img_array = np.expand_dims(resized_img, axis=0)
            img_array = preprocess_input(img_array)

            # استخراج الميزات
            features = self.model.predict(img_array, verbose=0)

            return features.flatten().tolist()

        except Exception as e:
            logger.error("خطأ أثناء استخراج ميزات التعلم العميق: %s", str(e))
            return []

    def _calculate_quality_score(self, img):
        """
        حساب درجة جودة الصورة

        المعلمات:
            img (numpy.ndarray): الصورة

        العائد:
            float: درجة الجودة
        """
        try:
            # تحويل الصورة إلى رمادي
            gray = cv2.cvtColor(
                img, cv2.COLOR_RGB2GRAY)  # pylint: disable=no-member

            # حساب تباين الصورة (مؤشر على الحدة)
            laplacian_var = cv2.Laplacian(
                gray, cv2.CV_64F).var()  # pylint: disable=no-member

            # تطبيع النتيجة
            quality_score = min(laplacian_var / 1000.0, 1.0)

            return float(quality_score)

        except Exception as e:
            logger.error("خطأ أثناء حساب درجة جودة الصورة: %s", str(e))
            return 0.0

    def _analyze_image(self, img, features, crop_type=None):
        """
        تحليل الصورة

        المعلمات:
            img (numpy.ndarray): الصورة
            features (dict): ميزات الصورة
            crop_type (str, optional): نوع المحصول

        العائد:
            dict: نتيجة التحليل
        """
        try:
            analysis_result = {}

            # حساب مؤشر النباتات
            vegetation_index = self._calculate_vegetation_index(img)
            analysis_result["vegetation_index"] = vegetation_index

            # تحليل الألوان
            if "color_histogram" in features:
                color_analysis = self._analyze_colors(
                    features["color_histogram"])
                analysis_result["color_analysis"] = color_analysis

            # تحليل النسيج
            if "texture_features" in features:
                texture_analysis = self._analyze_texture(
                    features["texture_features"])
                analysis_result["texture_analysis"] = texture_analysis

            # تقييم الجودة
            if "quality_score" in features:
                quality_assessment = self._assess_quality(
                    features["quality_score"])
                analysis_result["quality_assessment"] = quality_assessment

            # تحليل خاص بنوع المحصول
            if crop_type:
                crop_analysis = self._analyze_crop_specific(
                    img, features, crop_type)
                analysis_result["crop_specific_analysis"] = crop_analysis

            return analysis_result

        except Exception as e:
            logger.error("خطأ أثناء تحليل الصورة: %s", str(e))
            return {}

    def _calculate_vegetation_index(self, img):
        """
        حساب مؤشر النباتات

        المعلمات:
            img (numpy.ndarray): الصورة

        العائد:
            dict: مؤشرات النباتات
        """
        try:
            # تقسيم قنوات الألوان
            channels = cv2.split(img)  # pylint: disable=no-member
            r, g, b = channels[0], channels[1], channels[2]

            # حساب مؤشر النباتات الأخضر
            # NDVI تقريبي باستخدام الأحمر والأخضر
            with np.errstate(divide='ignore', invalid='ignore'):
                ndvi = (g.astype(float) - r.astype(float)) / \
                    (g.astype(float) + r.astype(float))
                ndvi = np.nan_to_num(ndvi)

            # حساب الإحصائيات
            ndvi_mean = float(np.mean(ndvi))
            ndvi_std = float(np.std(ndvi))

            # حساب نسبة الخضرة
            green_ratio = float(
                np.mean(g) / (np.mean(r) + np.mean(g) + np.mean(b)))

            vegetation_indices = {
                "ndvi_mean": ndvi_mean,
                "ndvi_std": ndvi_std,
                "green_ratio": green_ratio
            }

            return vegetation_indices

        except Exception as e:
            logger.error("خطأ أثناء حساب مؤشر النباتات: %s", str(e))
            return {}

    def _analyze_colors(self, color_histogram):
        """
        تحليل الألوان

        المعلمات:
            color_histogram (dict): هيستوجرام الألوان

        العائد:
            dict: تحليل الألوان
        """
        try:
            color_analysis = {}

            # تحليل كل قناة لون
            for color, hist in color_histogram.items():
                if hist:
                    hist_array = np.array(hist)
                    color_analysis[color] = {
                        "dominant_value": int(np.argmax(hist_array)),
                        "mean_intensity": float(np.mean(hist_array)),
                        "std_intensity": float(np.std(hist_array))
                    }

            return color_analysis

        except Exception as e:
            logger.error("خطأ أثناء تحليل الألوان: %s", str(e))
            return {}

    def _analyze_texture(self, texture_features):
        """
        تحليل النسيج

        المعلمات:
            texture_features (dict): ميزات النسيج

        العائد:
            dict: تحليل النسيج
        """
        try:
            texture_analysis = {
                "uniformity": "منتظم" if texture_features.get(
                    "hue_std",
                    0) < 30 else "غير منتظم",
                "saturation_level": "عالي" if texture_features.get(
                    "saturation_mean",
                    0) > 128 else "منخفض",
                "brightness_level": "مشرق" if texture_features.get(
                    "value_mean",
                    0) > 128 else "مظلم"}

            return texture_analysis

        except Exception as e:
            logger.error("خطأ أثناء تحليل النسيج: %s", str(e))
            return {}

    def _assess_quality(self, quality_score):
        """
        تقييم جودة الصورة

        المعلمات:
            quality_score (float): درجة الجودة

        العائد:
            dict: تقييم الجودة
        """
        try:
            if quality_score > 0.7:
                quality_level = QUALITY_HIGH
                recommendation = "جودة ممتازة للتحليل"
            elif quality_score > 0.4:
                quality_level = QUALITY_MEDIUM
                recommendation = "جودة مقبولة، يمكن تحسينها"
            else:
                quality_level = "منخفض"
                recommendation = "جودة منخفضة، يُنصح بتحسين الصورة"

            quality_assessment = {
                "score": quality_score,
                "level": quality_level,
                "recommendation": recommendation
            }

            return quality_assessment

        except Exception as e:
            logger.error("خطأ أثناء تقييم جودة الصورة: %s", str(e))
            return {}

    def _analyze_crop_specific(self, img, features, crop_type):
        """
        تحليل خاص بنوع المحصول

        المعلمات:
            img (numpy.ndarray): الصورة
            features (dict): ميزات الصورة
            crop_type (str): نوع المحصول

        العائد:
            dict: تحليل خاص بالمحصول
        """
        try:
            crop_analysis = {
                "crop_type": crop_type,
                "analysis_date": datetime.now().isoformat()
            }

            # تحليل خاص بالطماطم
            if crop_type.lower() in ["tomato", "طماطم"]:
                # تحليل لون الطماطم
                red_dominance = features.get(
                    "color_histogram", {}).get(
                    "red", [])
                if red_dominance:
                    red_peak = np.argmax(red_dominance)
                    if red_peak > 150:
                        crop_analysis["ripeness"] = "ناضج"
                    elif red_peak > 100:
                        crop_analysis["ripeness"] = "نصف ناضج"
                    else:
                        crop_analysis["ripeness"] = "أخضر"

            # تحليل خاص بالخضروات الورقية
            elif crop_type.lower() in ["lettuce", "spinach", "خس", "سبانخ"]:
                vegetation_index = features.get("vegetation_index", {})
                green_ratio = vegetation_index.get("green_ratio", 0)
                if green_ratio > 0.4:
                    crop_analysis["health"] = "صحي"
                else:
                    crop_analysis["health"] = "يحتاج عناية"

            # تحليل عام للمحاصيل الأخرى
            else:
                crop_analysis["status"] = "تحليل عام"
                crop_analysis["recommendation"] = "يُنصح بتحليل أكثر تفصيلاً"

            return crop_analysis

        except Exception as e:
            logger.error("خطأ أثناء التحليل الخاص بالمحصول: %s", str(e))
            return {}

    def _save_processed_image(self, img, original_image_path):
        """
        حفظ الصورة المعالجة

        المعلمات:
            img (numpy.ndarray): الصورة المعالجة
            original_image_path (str): مسار الصورة الأصلية

        العائد:
            str: مسار الصورة المحفوظة
        """
        try:
            # إنشاء اسم ملف فريد
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = os.path.basename(original_image_path)
            name, ext = os.path.splitext(original_filename)
            processed_filename = "%s_processed_%s%s" % (name, timestamp, ext)

            # مسار الحفظ
            save_path = os.path.join(self.processed_dir, processed_filename)

            # حفظ الصورة
            cv2.imwrite(
                save_path, cv2.cvtColor(
                    img, cv2.COLOR_RGB2BGR))  # pylint: disable=no-member

            logger.info("تم حفظ الصورة المعالجة: %s", save_path)
            return save_path

        except Exception as e:
            logger.error("خطأ أثناء حفظ الصورة المعالجة: %s", str(e))
            return None

    def _save_processing_result(self, processing_result):
        """
        حفظ نتيجة المعالجة

        المعلمات:
            processing_result (dict): نتيجة المعالجة
        """
        try:
            # إنشاء اسم ملف فريد
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_filename = "processing_result_%s.json" % timestamp

            # مسار الحفظ
            save_path = os.path.join(self.results_dir, result_filename)

            # حفظ النتيجة
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(processing_result, f, ensure_ascii=False, indent=2)

            logger.info("تم حفظ نتيجة المعالجة: %s", save_path)

        except Exception as e:
            logger.error("خطأ أثناء حفظ نتيجة المعالجة: %s", str(e))

    def get_processing_history(self, limit=10):
        """
        الحصول على سجل معالجة الصور

        المعلمات:
            limit (int): عدد العناصر المطلوب إرجاعها

        العائد:
            list: سجل معالجة الصور
        """
        return self.processing_history[-limit:
                                       ] if self.processing_history else []

    def get_processing_statistics(self):
        """
        الحصول على إحصائيات معالجة الصور

        العائد:
            dict: إحصائيات معالجة الصور
        """
        try:
            total_processings = len(self.processing_history)

            if total_processings == 0:
                return {
                    "total_processings": 0,
                    "success_rate": 0,
                    "crop_distribution": {}
                }

            # حساب معدل النجاح
            successful_processings = sum(
                1 for p in self.processing_history if p["result"] == "success")
            success_rate = successful_processings / total_processings

            # حساب توزيع المحاصيل
            crop_distribution = {}
            for processing in self.processing_history:
                crop_type = processing.get("crop_type", "غير محدد")
                if crop_type in crop_distribution:
                    crop_distribution[crop_type] += 1
                else:
                    crop_distribution[crop_type] = 1

            # تحويل التوزيع إلى نسب مئوية
            for crop in crop_distribution:
                crop_distribution[crop] = crop_distribution[crop] / \
                    total_processings

            return {
                "total_processings": total_processings,
                "success_rate": success_rate,
                "crop_distribution": crop_distribution
            }

        except Exception as e:
            logger.error("خطأ أثناء حساب إحصائيات معالجة الصور: %s", str(e))
            return {
                "total_processings": 0,
                "success_rate": 0,
                "crop_distribution": {}
            }

    def load_image(self, image_path):
        """Load an image from the given path and return as a numpy array (RGB)."""
        try:
            img = cv2.imread(image_path)  # pylint: disable=no-member
            if img is not None:
                return cv2.cvtColor(
                    img, cv2.COLOR_BGR2RGB)  # pylint: disable=no-member
            else:
                logger.error("Failed to load image: %s", image_path)
                return None
        except Exception as e:
            logger.error("Error loading image: %s", str(e))
            return None

    def resize_image(self, img, width, height):
        """Resize the image to the given width and height."""
        try:
            if img is None or width is None or height is None:
                logger.error("Invalid arguments for resize_image.")
                return None
            return cv2.resize(img, (int(width), int(height))
                              )  # pylint: disable=no-member
        except Exception as e:
            logger.error("Error resizing image: %s", str(e))
            return None

    def crop_image(self, img, x, y, width, height):
        """Crop the image to the given rectangle."""
        try:
            if img is None:
                logger.error("Image is None in crop_image.")
                return None
            x, y, width, height = int(x), int(y), int(width), int(height)
            return img[y:y + height, x:x + width]
        except Exception as e:
            logger.error("Error cropping image: %s", str(e))
            return None

    def enhance_contrast(self, img, clip_limit=2.0, tile_grid_size=(8, 8)):
        """Enhance the contrast of the image using CLAHE."""
        try:
            if img is None:
                logger.error("Image is None in enhance_contrast.")
                return None
            lab = cv2.cvtColor(
                img, cv2.COLOR_RGB2LAB)  # pylint: disable=no-member
            l, a, b = cv2.split(lab)  # pylint: disable=no-member
            clahe = cv2.createCLAHE(
                clipLimit=float(clip_limit),
                tileGridSize=tuple(tile_grid_size))  # pylint: disable=no-member
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))  # pylint: disable=no-member
            return cv2.cvtColor(
                limg, cv2.COLOR_LAB2RGB)  # pylint: disable=no-member
        except Exception as e:
            logger.error("Error enhancing contrast: %s", str(e))
            return None

    def apply_filters(self, img, filter_type='gaussian', kernel_size=5):
        """Apply a filter to the image (gaussian, median, etc.)."""
        try:
            if img is None:
                logger.error("Image is None in apply_filters.")
                return None
            if filter_type == 'gaussian':
                return cv2.GaussianBlur(
                    img, (int(kernel_size), int(kernel_size)), 0)  # pylint: disable=no-member
            elif filter_type == 'median':
                return cv2.medianBlur(
                    img, int(kernel_size))  # pylint: disable=no-member
            elif filter_type == 'bilateral':
                return cv2.bilateralFilter(
                    img, int(kernel_size), 75, 75)  # pylint: disable=no-member
            else:
                logger.error("Unknown filter type: %s", filter_type)
                return img
        except Exception as e:
            logger.error("Error applying filter: %s", str(e))
            return None

    def segment_image(self, img, threshold=128):
        """Segment the image using a simple threshold."""
        try:
            if img is None:
                logger.error("Image is None in segment_image.")
                return None, None
            gray = cv2.cvtColor(
                img, cv2.COLOR_RGB2GRAY)  # pylint: disable=no-member
            _, mask = cv2.threshold(
                gray, int(threshold), 255, cv2.THRESH_BINARY)  # pylint: disable=no-member
            segmented = cv2.bitwise_and(
                img, img, mask=mask)  # pylint: disable=no-member
            return mask, segmented
        except Exception as e:
            logger.error("Error segmenting image: %s", str(e))
            return None, None

    def detect_edges(self, img, threshold1=100, threshold2=200):
        """Detect edges in the image using Canny edge detector."""
        try:
            if img is None:
                logger.error("Image is None in detect_edges.")
                return None
            gray = cv2.cvtColor(
                img, cv2.COLOR_RGB2GRAY)  # pylint: disable=no-member
            edges = cv2.Canny(gray, int(threshold1), int(
                threshold2))  # pylint: disable=no-member
            return edges
        except Exception as e:
            logger.error("Error detecting edges: %s", str(e))
            return None

    def save_image(self, img, filename):
        """Save the image to the processed directory."""
        try:
            if img is None:
                logger.error("Image is None in save_image.")
                return None
            save_path = os.path.join(self.processed_dir, filename)
            cv2.imwrite(
                save_path, cv2.cvtColor(
                    img, cv2.COLOR_RGB2BGR))  # pylint: disable=no-member
            logger.info("Image saved to: %s", save_path)
            return save_path
        except Exception as e:
            logger.error("Error saving image: %s", str(e))
            return None

    def extract_features(self, img):
        """Extract features from the image (public wrapper)."""
        return self._extract_features(img)

    def analyze_color_distribution(self, img):
        """Analyze color distribution in the image (public wrapper)."""
        return self._calculate_color_histogram(img)

    def visualize_results(
            self,
            original_img,
            processed_images: dict,
            save_path: str):
        """
        Create a visualization (montage) of the original and processed images and save to save_path.
        Args:
            original_img (np.ndarray): The original image (RGB).
            processed_images (dict): Dict of processed images {operation: image}.
            save_path (str): Path to save the visualization image.
        """
        try:
            images = [original_img] + \
                [img for img in processed_images.values() if img is not None]
            titles = ["Original"] + [str(k) for k in processed_images.keys()]
            # Resize all images to the same size as the original
            h, w = original_img.shape[:2]
            images = [cv2.resize(img, (w, h)) if img.shape[:2] != (
                h, w) else img for img in images]  # pylint: disable=no-member
            # Add titles as text overlays
            for i, (img, title) in enumerate(zip(images, titles)):
                cv2.putText(img, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 2, cv2.LINE_AA)  # pylint: disable=no-member
            # Concatenate images horizontally (or in a grid if too many)
            if len(images) <= 4:
                montage = np.concatenate(images, axis=1)
            else:
                # Arrange in 2 rows
                mid = (len(images) + 1) // 2
                row1 = np.concatenate(images[:mid], axis=1)
                row2 = np.concatenate(images[mid:], axis=1) if len(
                    images) > mid else None
                montage = np.concatenate(
                    [row1, row2], axis=0) if row2 is not None else row1
            # Save the montage
            cv2.imwrite(
                save_path,
                cv2.cvtColor(
                    montage,
                    cv2.COLOR_RGB2BGR))  # pylint: disable=no-member
            logger.info("Visualization saved to: %s", save_path)
        except Exception as e:
            logger.error("Error in visualize_results: %s", str(e))
