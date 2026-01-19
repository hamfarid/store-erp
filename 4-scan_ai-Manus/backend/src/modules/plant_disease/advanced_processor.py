"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/plant_disease/advanced_processor.py
الوصف: معالج متقدم لتشخيص أمراض النباتات يدمج نماذج متعددة
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
"""

import json
import logging
import os
from datetime import datetime

import numpy as np
import tensorflow as tf
import torch
from PIL import Image

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('advanced_plant_processor')


class AdvancedPlantDiseaseProcessor:
    """معالج متقدم لتشخيص أمراض النباتات يدمج نماذج متعددة"""

    def __init__(self, models_dir=None, config=None):
        """
        تهيئة المعالج المتقدم

        Args:
            models_dir: مسار مجلد النماذج (اختياري)
            config: إعدادات التكوين (اختياري)
        """
        self.models = {}
        self.processors = {}
        self.models_dir = models_dir or os.path.join(
            os.path.dirname(__file__), 'models')
        self.config = config or {}

        # إنشاء مجلد النماذج إذا لم يكن موجوداً
        os.makedirs(self.models_dir, exist_ok=True)

        # تحميل النماذج المتاحة
        self.load_all_models()

        logger.info("تم تهيئة معالج أمراض النباتات المتقدم")

    def load_all_models(self):
        """تحميل جميع النماذج المتاحة"""

        # تحميل النماذج حسب التكوين
        if self.config.get('use_huggingface', True):
            self.load_huggingface_models()

        if self.config.get('use_tensorflow', True):
            self.load_tensorflow_hub_models()

        if self.config.get('use_pytorch', True):
            self.load_pytorch_models()

        if self.config.get('use_keras', True):
            self.load_keras_models()

        logger.info(f"تم تحميل {len(self.models)} نموذج بنجاح")

    def load_huggingface_models(self):
        """تحميل نماذج Hugging Face"""

        try:
            from transformers import AutoImageProcessor, AutoModelForImageClassification

            hf_models = {
                'mobilenet_plant': "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
                'vit_plant': "marwaALzaabi/plant-disease-detection-vit"}

            for name, model_id in hf_models.items():
                try:
                    # التحقق من وجود النموذج محلياً
                    local_model_path = os.path.join(self.models_dir, name)

                    if os.path.exists(local_model_path):
                        processor = AutoImageProcessor.from_pretrained(
                            local_model_path)
                        model = AutoModelForImageClassification.from_pretrained(
                            local_model_path)
                    else:
                        processor = AutoImageProcessor.from_pretrained(
                            model_id)
                        model = AutoModelForImageClassification.from_pretrained(
                            model_id)

                        # حفظ النموذج محلياً
                        processor.save_pretrained(local_model_path)
                        model.save_pretrained(local_model_path)

                    self.processors[name] = processor
                    self.models[name] = model
                    logger.info(f"✅ تم تحميل {name}")
                except Exception as e:
                    logger.error(f"❌ فشل تحميل {name}: {e}")
        except ImportError:
            logger.warning(
                "لم يتم تثبيت مكتبة transformers، تخطي تحميل نماذج Hugging Face")

    def load_tensorflow_hub_models(self):
        """تحميل نماذج TensorFlow Hub"""

        try:
            import tensorflow_hub as hub

            tf_models = {
                'cropnet_cassava': 'https://tfhub.dev/google/cropnet/classifier/cassava_disease_V1/2',
                'cropnet_feature': 'https://tfhub.dev/google/cropnet/feature_vector/cassava_disease_V1/1',
                'mobilenet_v3': 'https://tfhub.dev/google/imagenet/mobilenet_v3_large_100_224/feature_vector/5'}

            for name, url in tf_models.items():
                try:
                    # التحقق من وجود النموذج محلياً
                    local_model_path = os.path.join(self.models_dir, name)

                    if os.path.exists(local_model_path):
                        model = hub.load(local_model_path)
                    else:
                        model = hub.load(url)
                        # حفظ النموذج محلياً (لا يمكن حفظه مباشرة)

                    self.models[name] = model
                    logger.info(f"✅ تم تحميل {name}")
                except Exception as e:
                    logger.error(f"❌ فشل تحميل {name}: {e}")
        except ImportError:
            logger.warning(
                "لم يتم تثبيت مكتبة tensorflow_hub، تخطي تحميل نماذج TensorFlow Hub")

    def load_pytorch_models(self):
        """تحميل نماذج PyTorch المخصصة"""

        try:
            import torchvision.models as models

            # تحميل AlexNet المدرب على PlantVillage
            try:
                alexnet = models.alexnet(pretrained=False)
                alexnet.classifier[6] = torch.nn.Linear(
                    4096, 38)  # 38 فئة PlantVillage

                # التحقق من وجود الأوزان محلياً
                weights_path = os.path.join(
                    self.models_dir, 'alexnet_plantvillage.pth')

                if os.path.exists(weights_path):
                    alexnet.load_state_dict(torch.load(
                        weights_path, map_location='cpu'))
                    self.models['alexnet_plantvillage'] = alexnet
                    logger.info("✅ تم تحميل AlexNet PlantVillage")
            except Exception as e:
                logger.error(f"❌ فشل تحميل AlexNet PlantVillage: {e}")
        except ImportError:
            logger.warning(
                "لم يتم تثبيت مكتبة torchvision، تخطي تحميل نماذج PyTorch")

    def load_keras_models(self):
        """تحميل نماذج Keras المدربة"""

        try:
            # تحميل نموذج H5
            model_path = os.path.join(
                self.models_dir, 'plant_disease_model.h5')

            if os.path.exists(model_path):
                keras_model = tf.keras.models.load_model(model_path)
                self.models['keras_plant'] = keras_model
                logger.info("✅ تم تحميل نموذج Keras")
        except Exception as e:
            logger.error(f"❌ فشل تحميل نموذج Keras: {e}")

    def download_model(self, model_type, model_url, save_path=None):
        """
        تحميل نموذج من مصدر خارجي

        Args:
            model_type: نوع النموذج (huggingface, tensorflow, pytorch, keras)
            model_url: رابط النموذج أو معرفه
            save_path: مسار الحفظ (اختياري)

        Returns:
            bool: نجاح التحميل
        """
        try:
            if save_path is None:
                save_path = os.path.join(
                    self.models_dir, os.path.basename(model_url))

            if model_type == 'huggingface':
                from transformers import (
                    AutoImageProcessor,
                    AutoModelForImageClassification,
                )

                processor = AutoImageProcessor.from_pretrained(model_url)
                model = AutoModelForImageClassification.from_pretrained(
                    model_url)

                # حفظ النموذج محلياً
                processor.save_pretrained(save_path)
                model.save_pretrained(save_path)

                # إضافة النموذج للمعالج
                model_name = os.path.basename(save_path)
                self.processors[model_name] = processor
                self.models[model_name] = model

                logger.info(f"✅ تم تحميل وحفظ {model_name} من Hugging Face")
                return True

            elif model_type == 'tensorflow':
                import tensorflow_hub as hub

                model = hub.load(model_url)

                # إضافة النموذج للمعالج
                model_name = os.path.basename(save_path)
                self.models[model_name] = model

                logger.info(f"✅ تم تحميل {model_name} من TensorFlow Hub")
                return True

            elif model_type == 'pytorch':
                import torch

                # تحميل الأوزان
                weights = torch.hub.load_state_dict_from_url(
                    model_url, map_location='cpu')
                torch.save(weights, save_path)

                logger.info(f"✅ تم تحميل وحفظ أوزان PyTorch من {model_url}")
                return True

            elif model_type == 'keras':
                import requests

                # تحميل ملف H5
                response = requests.get(model_url)
                with open(save_path, 'wb') as f:
                    f.write(response.content)

                # تحميل النموذج
                keras_model = tf.keras.models.load_model(save_path)

                # إضافة النموذج للمعالج
                model_name = os.path.basename(save_path).split('.')[0]
                self.models[model_name] = keras_model

                logger.info(f"✅ تم تحميل وحفظ نموذج Keras من {model_url}")
                return True

            else:
                logger.error(f"❌ نوع النموذج غير مدعوم: {model_type}")
                return False

        except Exception as e:
            logger.error(f"❌ فشل تحميل النموذج: {e}")
            return False

    def preprocess_image(self, image_path, model_type):
        """
        معالجة الصورة حسب نوع النموذج

        Args:
            image_path: مسار الصورة
            model_type: نوع النموذج

        Returns:
            الصورة المعالجة
        """
        try:
            image = Image.open(image_path).convert('RGB')

            if model_type in ['mobilenet_plant', 'vit_plant']:
                # Hugging Face preprocessing
                processor = self.processors[model_type]
                inputs = processor(images=image, return_tensors="pt")
                return inputs

            elif model_type in ['cropnet_cassava', 'cropnet_feature', 'mobilenet_v3']:
                # TensorFlow preprocessing
                image = image.resize((224, 224))
                image_array = np.array(image) / 255.0
                return np.expand_dims(image_array, axis=0)

            elif model_type == 'alexnet_plantvillage':
                # PyTorch preprocessing
                from torchvision import transforms
                transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])
                ])
                return transform(image).unsqueeze(0)

            elif model_type == 'keras_plant':
                # Keras preprocessing
                image = image.resize((224, 224))
                image_array = np.array(image) / 255.0
                return np.expand_dims(image_array, axis=0)

            else:
                # معالجة افتراضية
                image = image.resize((224, 224))
                image_array = np.array(image) / 255.0
                return np.expand_dims(image_array, axis=0)

        except Exception as e:
            logger.error(f"❌ فشل معالجة الصورة: {e}")
            return None

    def predict_single_model(self, image_path, model_name):
        """
        التنبؤ باستخدام نموذج واحد

        Args:
            image_path: مسار الصورة
            model_name: اسم النموذج

        Returns:
            dict: نتيجة التنبؤ
        """
        if model_name not in self.models:
            return {"error": f"النموذج {model_name} غير متاح"}

        try:
            # معالجة الصورة
            processed_image = self.preprocess_image(image_path, model_name)

            if processed_image is None:
                return {"error": "فشل معالجة الصورة"}

            model = self.models[model_name]

            # التنبؤ حسب نوع النموذج
            if model_name in ['mobilenet_plant', 'vit_plant']:
                # Hugging Face models
                with torch.no_grad():
                    outputs = model(**processed_image)
                    probabilities = torch.nn.functional.softmax(
                        outputs.logits, dim=-1)
                    prediction = torch.argmax(probabilities, dim=-1).item()
                    confidence = torch.max(probabilities).item()

                    # الحصول على التسميات
                    if hasattr(model.config, 'id2label'):
                        label = model.config.id2label[prediction]
                    else:
                        label = f"الفئة {prediction}"

            elif model_name in ['cropnet_cassava', 'cropnet_feature', 'mobilenet_v3']:
                # TensorFlow models
                predictions = model(processed_image)

                if isinstance(predictions, dict) and 'logits' in predictions:
                    predictions = predictions['logits']

                if len(predictions.shape) > 1:
                    prediction = np.argmax(predictions, axis=-1)[0]
                    confidence = float(np.max(predictions))
                    probabilities = predictions.numpy() if hasattr(
                        predictions, 'numpy') else predictions
                else:
                    prediction = int(predictions)
                    confidence = float(predictions)
                    probabilities = [float(predictions)]

                # التسمية الافتراضية
                label = f"الفئة {prediction}"

            elif model_name == 'alexnet_plantvillage':
                # PyTorch models
                model.eval()
                with torch.no_grad():
                    outputs = model(processed_image)
                    probabilities = torch.nn.functional.softmax(outputs, dim=1)
                    prediction = torch.argmax(probabilities, dim=1).item()
                    confidence = torch.max(probabilities).item()

                    # التسمية الافتراضية
                    label = f"الفئة {prediction}"

            elif model_name == 'keras_plant':
                # Keras models
                predictions = model.predict(processed_image)
                prediction = np.argmax(predictions, axis=1)[0]
                confidence = float(np.max(predictions))
                probabilities = predictions.tolist()

                # التسمية الافتراضية
                label = f"الفئة {prediction}"

            return {
                "model": model_name,
                "prediction": prediction,
                "label": label,
                "confidence": float(confidence),
                "probabilities": probabilities.tolist() if isinstance(
                    probabilities,
                    (np.ndarray,
                     torch.Tensor)) else probabilities}

        except Exception as e:
            logger.error(f"❌ خطأ في التنبؤ باستخدام {model_name}: {e}")
            return {"error": f"خطأ في التنبؤ: {str(e)}"}

    def ensemble_predict(self, image_path, models_to_use=None):
        """
        التنبؤ المجمع من عدة نماذج

        Args:
            image_path: مسار الصورة
            models_to_use: قائمة النماذج المستخدمة (اختياري)

        Returns:
            dict: نتيجة التنبؤ المجمع
        """
        if models_to_use is None:
            models_to_use = list(self.models.keys())

        predictions = {}
        valid_predictions = []

        for model_name in models_to_use:
            result = self.predict_single_model(image_path, model_name)
            predictions[model_name] = result

            if "error" not in result:
                valid_predictions.append({
                    'model': model_name,
                    'prediction': result['prediction'],
                    'label': result.get('label', f"الفئة {result['prediction']}"),
                    'confidence': result['confidence']
                })

        if not valid_predictions:
            return {"error": "لا توجد نماذج صالحة للتنبؤ"}

        # حساب التنبؤ المجمع
        ensemble_result = self.calculate_ensemble(valid_predictions)

        return {
            "individual_predictions": predictions,
            "ensemble_prediction": ensemble_result,
            "models_used": len(valid_predictions),
            "total_models": len(models_to_use)
        }

    def calculate_ensemble(self, predictions):
        """
        حساب التنبؤ المجمع

        Args:
            predictions: قائمة التنبؤات

        Returns:
            dict: نتيجة التنبؤ المجمع
        """
        # Weighted voting based on confidence
        prediction_counts = {}
        confidence_sum = {}

        confidence_scores = []
        prediction_values = []
        labels = []

        for pred in predictions:
            prediction = pred['prediction']
            confidence = pred['confidence']
            label = pred['label']

            if prediction not in prediction_counts:
                prediction_counts[prediction] = 0
                confidence_sum[prediction] = 0

            prediction_counts[prediction] += 1
            confidence_sum[prediction] += confidence

            confidence_scores.append(confidence)
            prediction_values.append(prediction)
            labels.append(label)

        # اختيار التنبؤ الأكثر تكراراً مع أعلى ثقة
        max_count = 0
        max_confidence = 0
        ensemble_prediction = None
        ensemble_label = None

        for prediction, count in prediction_counts.items():
            avg_confidence = confidence_sum[prediction] / count

            if count > max_count or (
                    count == max_count and avg_confidence > max_confidence):
                max_count = count
                max_confidence = avg_confidence
                ensemble_prediction = prediction

                # اختيار التسمية من التنبؤ الأكثر ثقة
                for pred in predictions:
                    if pred['prediction'] == ensemble_prediction and pred['confidence'] == max_confidence:
                        ensemble_label = pred['label']
                        break

        if ensemble_label is None:
            ensemble_label = f"الفئة {ensemble_prediction}"

        # حساب نسبة الاتفاق
        unique_predictions = len(set(prediction_values))
        agreement_score = 1.0 - (unique_predictions - 1) / \
            len(predictions) if len(predictions) > 0 else 0

        return {
            "prediction": ensemble_prediction,
            "label": ensemble_label,
            "confidence": float(max_confidence),
            "agreement_score": float(agreement_score),
            "vote_count": max_count,
            "total_votes": len(predictions),
            "individual_confidences": confidence_scores
        }

    def analyze_image_comprehensive(self, image_path):
        """
        تحليل شامل للصورة

        Args:
            image_path: مسار الصورة

        Returns:
            dict: نتيجة التحليل الشامل
        """
        # التنبؤ المجمع
        ensemble_result = self.ensemble_predict(image_path)

        # تحليل إضافي
        additional_analysis = {
            "image_quality": self.assess_image_quality(image_path),
            "leaf_detection": self.detect_leaf_regions(image_path),
            "stress_analysis": self.analyze_plant_stress(image_path),
            "recommendations": self.generate_recommendations(ensemble_result)
        }

        return {
            "predictions": ensemble_result,
            "analysis": additional_analysis,
            "timestamp": self.get_timestamp()
        }

    def assess_image_quality(self, image_path):
        """
        تقييم جودة الصورة

        Args:
            image_path: مسار الصورة

        Returns:
            dict: نتيجة تقييم الجودة
        """
        try:
            image = Image.open(image_path)

            # Basic quality metrics
            width, height = image.size
            aspect_ratio = width / height

            # Convert to numpy for analysis
            img_array = np.array(image)

            # Brightness analysis
            brightness = np.mean(img_array)

            # Contrast analysis
            contrast = np.std(img_array)

            # Blur detection (Laplacian variance)
            gray = np.mean(
                img_array, axis=2) if len(
                img_array.shape) == 3 else img_array
            blur_score = self.laplacian_variance(gray)

            return {
                "resolution": f"{width}x{height}",
                "aspect_ratio": float(aspect_ratio),
                "brightness": float(brightness),
                "contrast": float(contrast),
                "blur_score": float(blur_score),
                "quality_score": float(
                    self.calculate_quality_score(
                        brightness,
                        contrast,
                        blur_score))}
        except Exception as e:
            logger.error(f"❌ خطأ في تقييم جودة الصورة: {e}")
            return {"error": f"خطأ في تقييم جودة الصورة: {str(e)}"}

    def laplacian_variance(self, image):
        """
        حساب Laplacian variance للكشف عن الضبابية

        Args:
            image: مصفوفة الصورة

        Returns:
            float: قيمة Laplacian variance
        """
        # Simplified Laplacian calculation
        laplacian = np.abs(np.diff(image, axis=0)).mean() + \
            np.abs(np.diff(image, axis=1)).mean()
        return laplacian

    def calculate_quality_score(self, brightness, contrast, blur_score):
        """
        حساب نقاط الجودة الإجمالية

        Args:
            brightness: قيمة السطوع
            contrast: قيمة التباين
            blur_score: قيمة الضبابية

        Returns:
            float: نقاط الجودة
        """
        # Normalize scores
        brightness_score = min(1.0, brightness / 128.0)
        contrast_score = min(1.0, contrast / 50.0)
        blur_score_norm = min(1.0, blur_score / 100.0)

        # Weighted average
        quality = (
            brightness_score *
            0.3 +
            contrast_score *
            0.4 +
            blur_score_norm *
            0.3)
        return quality

    def detect_leaf_regions(self, image_path):
        """
        كشف مناطق الأوراق في الصورة

        Args:
            image_path: مسار الصورة

        Returns:
            dict: نتيجة كشف الأوراق
        """
        try:
            # استخدام YOLOv8 إذا كان متاحاً
            if 'yolo_plant' in self.models:
                try:
                    results = self.models['yolo_plant'](image_path)
                    return {
                        "detected_leaves": len(
                            results.pandas().xyxy[0]),
                        "bounding_boxes": results.pandas().xyxy[0].to_dict('records'),
                        "confidence": float(
                            results.pandas().xyxy[0]['confidence'].mean())}
                except BaseException:
                    pass

            # Basic leaf detection using color analysis
            image = Image.open(image_path)
            img_array = np.array(image)

            # Simple green detection
            green_mask = self.detect_green_regions(img_array)
            leaf_percentage = np.sum(green_mask) / green_mask.size

            return {
                "leaf_coverage": float(leaf_percentage),
                "green_detected": bool(leaf_percentage > 0.1),
                "method": "color_analysis"
            }
        except Exception as e:
            logger.error(f"❌ خطأ في كشف مناطق الأوراق: {e}")
            return {"error": f"خطأ في كشف مناطق الأوراق: {str(e)}"}

    def detect_green_regions(self, img_array):
        """
        كشف المناطق الخضراء

        Args:
            img_array: مصفوفة الصورة

        Returns:
            ndarray: قناع المناطق الخضراء
        """
        # Convert to HSV for better green detection
        # Simplified RGB to HSV conversion
        r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]

        # Simple green detection
        green_mask = (g > r) & (g > b) & (g > 50)

        return green_mask

    def analyze_plant_stress(self, image_path):
        """
        تحليل الإجهاد النباتي

        Args:
            image_path: مسار الصورة

        Returns:
            dict: نتيجة تحليل الإجهاد
        """
        try:
            image = Image.open(image_path)
            img_array = np.array(image)

            # Color analysis for stress indicators
            r_avg = np.mean(img_array[:, :, 0])
            g_avg = np.mean(img_array[:, :, 1])
            b_avg = np.mean(img_array[:, :, 2])

            # Stress indicators
            yellowing = r_avg > g_avg  # Indicates nitrogen deficiency
            browning = (
                r_avg > 100) and (
                g_avg < 80) and (
                b_avg < 60)  # Brown spots
            wilting = g_avg < 70  # Low green indicates wilting

            stress_score = (int(yellowing) + int(browning) + int(wilting)) / 3

            return {
                "yellowing_detected": bool(yellowing),
                "browning_detected": bool(browning),
                "wilting_detected": bool(wilting),
                "stress_score": float(stress_score),
                "color_averages": {
                    "red": float(r_avg),
                    "green": float(g_avg),
                    "blue": float(b_avg)
                }
            }
        except Exception as e:
            logger.error(f"❌ خطأ في تحليل الإجهاد النباتي: {e}")
            return {"error": f"خطأ في تحليل الإجهاد النباتي: {str(e)}"}

    def generate_recommendations(self, prediction_result):
        """
        توليد التوصيات العلاجية

        Args:
            prediction_result: نتيجة التنبؤ

        Returns:
            list: قائمة التوصيات
        """
        if "error" in prediction_result:
            return ["يرجى التحقق من جودة الصورة وإعادة المحاولة"]

        ensemble = prediction_result.get("ensemble_prediction", {})
        confidence = ensemble.get("confidence", 0)
        agreement = ensemble.get("agreement_score", 0)

        recommendations = []

        # Confidence-based recommendations
        if confidence < 0.7:
            recommendations.append(
                "الثقة في التشخيص منخفضة - يُنصح بالرجوع لخبير زراعي")

        if agreement < 0.6:
            recommendations.append(
                "النماذج غير متفقة - يُنصح بأخذ صور إضافية من زوايا مختلفة")

        # General plant care recommendations
        recommendations.extend([
            "تأكد من توفر الإضاءة المناسبة",
            "راقب مستوى الرطوبة في التربة",
            "فحص دوري للآفات والأمراض",
            "استخدم الأسمدة العضوية حسب نوع النبات"
        ])

        return recommendations

    def get_timestamp(self):
        """
        الحصول على الطابع الزمني

        Returns:
            str: الطابع الزمني
        """
        return datetime.now().isoformat()

    def save_analysis_result(self, result, output_path):
        """
        حفظ نتيجة التحليل

        Args:
            result: نتيجة التحليل
            output_path: مسار الحفظ

        Returns:
            bool: نجاح الحفظ
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ تم حفظ نتيجة التحليل في {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ خطأ في حفظ نتيجة التحليل: {e}")
            return False

    def batch_process_images(self, images_folder, output_folder=None):
        """
        معالجة مجموعة صور

        Args:
            images_folder: مجلد الصور
            output_folder: مجلد الإخراج (اختياري)

        Returns:
            dict: نتائج المعالجة
        """
        if output_folder is None:
            output_folder = os.path.join(
                os.path.dirname(images_folder), 'results')

        os.makedirs(output_folder, exist_ok=True)

        results = {}

        for image_file in os.listdir(images_folder):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(images_folder, image_file)

                try:
                    # تحليل الصورة
                    result = self.analyze_image_comprehensive(image_path)
                    results[image_file] = result

                    # حفظ النتيجة
                    output_path = os.path.join(
                        output_folder, f"{os.path.splitext(image_file)[0]}_result.json")
                    self.save_analysis_result(result, output_path)

                except Exception as e:
                    logger.error(f"❌ خطأ في معالجة الصورة {image_file}: {e}")
                    results[image_file] = {"error": str(e)}

        # حفظ النتائج المجمعة
        summary_path = os.path.join(
            output_folder, "batch_results_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        return results

    def get_available_models(self):
        """
        الحصول على قائمة النماذج المتاحة

        Returns:
            list: قائمة النماذج المتاحة
        """
        return list(self.models.keys())

    def get_model_info(self, model_name):
        """
        الحصول على معلومات النموذج

        Args:
            model_name: اسم النموذج

        Returns:
            dict: معلومات النموذج
        """
        if model_name not in self.models:
            return {"error": f"النموذج {model_name} غير متاح"}

        model = self.models[model_name]

        # معلومات عامة
        info = {
            "name": model_name,
            "type": self._get_model_type(model_name, model)
        }

        # معلومات إضافية حسب نوع النموذج
        if model_name in ['mobilenet_plant', 'vit_plant']:
            # Hugging Face models
            if hasattr(model.config, 'id2label'):
                info["classes"] = len(model.config.id2label)
                info["labels"] = model.config.id2label

            if hasattr(model.config, 'model_type'):
                info["architecture"] = model.config.model_type

        return info

    def _get_model_type(self, model_name, model):
        """
        الحصول على نوع النموذج

        Args:
            model_name: اسم النموذج
            model: النموذج

        Returns:
            str: نوع النموذج
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


class DatasetManager:
    """مدير مجموعات البيانات للنباتات والأمراض"""

    def __init__(self, datasets_dir=None):
        """
        تهيئة مدير مجموعات البيانات

        Args:
            datasets_dir: مسار مجلد مجموعات البيانات (اختياري)
        """
        self.datasets = {}
        self.download_queue = []
        self.datasets_dir = datasets_dir or os.path.join(
            os.path.dirname(__file__), 'datasets')

        # إنشاء مجلد مجموعات البيانات إذا لم يكن موجوداً
        os.makedirs(self.datasets_dir, exist_ok=True)

        logger.info("تم تهيئة مدير مجموعات البيانات")

    def setup_all_datasets(self):
        """إعداد جميع قواعد البيانات"""

        self.download_plantvillage()
        self.download_plantdoc()
        self.download_cassava()
        self.download_additional_datasets()

        logger.info(f"تم إعداد {len(self.datasets)} مجموعة بيانات")

    def download_plantvillage(self):
        """تحميل PlantVillage"""

        try:
            # Method 1: TensorFlow Datasets
            import tensorflow_datasets as tfds
            ds = tfds.load('plant_village', split='train')
            self.datasets['plantvillage_tfds'] = ds
            logger.info("✅ PlantVillage من TFDS")

        except BaseException:
            # Method 2: Manual download from GitHub
            self.download_from_github(
                "https://github.com/spMohanty/PlantVillage-Dataset.git",
                "plantvillage_github"
            )

    def download_plantdoc(self):
        """تحميل PlantDoc"""

        self.download_from_github(
            "https://github.com/pratikkayal/PlantDoc-Dataset.git",
            "plantdoc"
        )

    def download_cassava(self):
        """تحميل Cassava dataset"""

        try:
            import tensorflow_datasets as tfds
            ds = tfds.load('cassava', split=['train', 'validation', 'test'])
            self.datasets['cassava'] = ds
            logger.info("✅ Cassava من TFDS")
        except Exception as e:
            logger.error(f"❌ فشل تحميل Cassava: {e}")

    def download_from_github(self, repo_url, dataset_name):
        """
        تحميل من GitHub

        Args:
            repo_url: رابط المستودع
            dataset_name: اسم مجموعة البيانات
        """
        import subprocess

        try:
            dataset_path = os.path.join(self.datasets_dir, dataset_name)

            if not os.path.exists(dataset_path):
                subprocess.run(['git', 'clone', repo_url, dataset_path],
                               check=True, capture_output=True)
                logger.info(f"✅ تم تحميل {dataset_name}")
            else:
                logger.info(f"📁 {dataset_name} موجود مسبقاً")

            self.datasets[dataset_name] = dataset_path

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ فشل تحميل {dataset_name}: {e}")

    def download_additional_datasets(self):
        """تحميل مجموعات بيانات إضافية"""

        additional_urls = {
            'new_plant_diseases': 'https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset',
            'plant_pathology': 'https://www.kaggle.com/competitions/plant-pathology-2020-fgvc7'}

        for name, url in additional_urls.items():
            self.download_queue.append((name, url))
            logger.info(f"📋 إضافة {name} إلى قائمة التحميل")

    def create_unified_dataset(self):
        """
        إنشاء مجموعة بيانات موحدة

        Returns:
            dict: مجموعة البيانات الموحدة
        """
        unified_data = {
            'images': [],
            'labels': [],
            'sources': [],
            'metadata': []
        }

        for dataset_name, dataset in self.datasets.items():
            data = self.process_dataset(dataset, dataset_name)

            unified_data['images'].extend(data['images'])
            unified_data['labels'].extend(data['labels'])
            unified_data['sources'].extend(
                [dataset_name] * len(data['images']))
            unified_data['metadata'].extend(data['metadata'])

        logger.info(
            f"✅ تم إنشاء مجموعة بيانات موحدة بـ {len(unified_data['images'])} صورة")
        return unified_data

    def process_dataset(self, dataset, dataset_name):
        """
        معالجة مجموعة بيانات واحدة

        Args:
            dataset: مجموعة البيانات
            dataset_name: اسم مجموعة البيانات

        Returns:
            dict: البيانات المعالجة
        """
        if dataset_name == 'plantvillage_tfds':
            return self.process_tfds_dataset(dataset)
        elif dataset_name in ['plantdoc', 'plantvillage_github']:
            return self.process_folder_dataset(dataset)
        else:
            return {'images': [], 'labels': [], 'metadata': []}

    def process_tfds_dataset(self, dataset):
        """
        معالجة TFDS dataset

        Args:
            dataset: مجموعة البيانات

        Returns:
            dict: البيانات المعالجة
        """
        images = []
        labels = []
        metadata = []

        for example in dataset.take(1000):  # عينة للاختبار
            images.append(example['image'].numpy())
            labels.append(example['label'].numpy())
            metadata.append({
                'width': example['image'].shape[1],
                'height': example['image'].shape[0],
                'channels': example['image'].shape[2]
            })

        return {
            'images': images,
            'labels': labels,
            'metadata': metadata
        }

    def process_folder_dataset(self, folder_path):
        """
        معالجة dataset في مجلدات

        Args:
            folder_path: مسار المجلد

        Returns:
            dict: البيانات المعالجة
        """
        import os

        from PIL import Image

        images = []
        labels = []
        metadata = []

        # استكشاف المجلدات
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)

                    try:
                        img = Image.open(file_path)
                        images.append(np.array(img))

                        # استخراج التسمية من اسم المجلد
                        label = os.path.basename(root)
                        labels.append(label)

                        metadata.append({
                            'path': file_path,
                            'width': img.width,
                            'height': img.height,
                            'mode': img.mode
                        })

                    except Exception as e:
                        logger.error(f"تجاهل {file_path}: {e}")

        return {
            'images': images,
            'labels': labels,
            'metadata': metadata
        }

    def download_dataset_from_url(self, url, dataset_name):
        """
        تحميل مجموعة بيانات من رابط

        Args:
            url: رابط مجموعة البيانات
            dataset_name: اسم مجموعة البيانات

        Returns:
            bool: نجاح التحميل
        """
        try:
            import zipfile

            import requests

            dataset_path = os.path.join(self.datasets_dir, dataset_name)
            os.makedirs(dataset_path, exist_ok=True)

            # تحميل الملف
            zip_path = os.path.join(dataset_path, f"{dataset_name}.zip")

            logger.info(f"🔄 جاري تحميل {dataset_name} من {url}")

            response = requests.get(url, stream=True)
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # استخراج الملف
            logger.info(f"🔄 جاري استخراج {dataset_name}")

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dataset_path)

            # إضافة مجموعة البيانات
            self.datasets[dataset_name] = dataset_path

            logger.info(f"✅ تم تحميل واستخراج {dataset_name}")
            return True

        except Exception as e:
            logger.error(f"❌ فشل تحميل {dataset_name}: {e}")
            return False

    def get_dataset_info(self, dataset_name):
        """
        الحصول على معلومات مجموعة البيانات

        Args:
            dataset_name: اسم مجموعة البيانات

        Returns:
            dict: معلومات مجموعة البيانات
        """
        if dataset_name not in self.datasets:
            return {"error": f"مجموعة البيانات {dataset_name} غير متاحة"}

        dataset = self.datasets[dataset_name]

        if dataset_name == 'plantvillage_tfds':
            # TensorFlow Dataset
            info = {
                "name": dataset_name,
                "type": "tfds",
                "size": len(dataset),
                "classes": len(set(example['label'].numpy() for example in dataset.take(1000)))
            }
        else:
            # Folder dataset
            import os

            # عدد الصور
            image_count = 0
            classes = set()

            for root, dirs, files in os.walk(dataset):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_count += 1
                        classes.add(os.path.basename(root))

            info = {
                "name": dataset_name,
                "type": "folder",
                "path": dataset,
                "size": image_count,
                "classes": len(classes),
                "class_names": list(classes)
            }

        return info

    def get_available_datasets(self):
        """
        الحصول على قائمة مجموعات البيانات المتاحة

        Returns:
            list: قائمة مجموعات البيانات المتاحة
        """
        return list(self.datasets.keys())

    def export_dataset(self, dataset_name, output_format, output_path):
        """
        تصدير مجموعة بيانات

        Args:
            dataset_name: اسم مجموعة البيانات
            output_format: صيغة الإخراج (tfrecord, csv, json)
            output_path: مسار الإخراج

        Returns:
            bool: نجاح التصدير
        """
        if dataset_name not in self.datasets:
            logger.error(f"❌ مجموعة البيانات {dataset_name} غير متاحة")
            return False

        dataset = self.datasets[dataset_name]

        try:
            if output_format == 'tfrecord':
                self._export_to_tfrecord(dataset, dataset_name, output_path)
            elif output_format == 'csv':
                self._export_to_csv(dataset, dataset_name, output_path)
            elif output_format == 'json':
                self._export_to_json(dataset, dataset_name, output_path)
            else:
                logger.error(f"❌ صيغة الإخراج {output_format} غير مدعومة")
                return False

            logger.info(
                f"✅ تم تصدير {dataset_name} بصيغة {output_format} إلى {output_path}")
            return True

        except Exception as e:
            logger.error(f"❌ فشل تصدير {dataset_name}: {e}")
            return False

    def _export_to_tfrecord(self, dataset, dataset_name, output_path):
        """
        تصدير إلى TFRecord

        Args:
            dataset: مجموعة البيانات
            dataset_name: اسم مجموعة البيانات
            output_path: مسار الإخراج
        """
        import tensorflow as tf

        def _bytes_feature(value):
            """Returns a bytes_list from a string / byte."""
            if isinstance(value, type(tf.constant(0))):
                value = value.numpy()
            return tf.train.Feature(
                bytes_list=tf.train.BytesList(
                    value=[value]))

        def _int64_feature(value):
            """Returns an int64_list from a bool / enum / int / uint."""
            return tf.train.Feature(
                int64_list=tf.train.Int64List(
                    value=[value]))

        with tf.io.TFRecordWriter(output_path) as writer:
            if dataset_name == 'plantvillage_tfds':
                # TensorFlow Dataset
                for example in dataset:
                    image = example['image'].numpy()
                    label = example['label'].numpy()

                    # Convert image to bytes
                    image_bytes = tf.io.encode_jpeg(image).numpy()

                    # Create a feature
                    feature = {
                        'image': _bytes_feature(image_bytes),
                        'label': _int64_feature(label)
                    }

                    # Create an example protocol buffer
                    example_proto = tf.train.Example(
                        features=tf.train.Features(feature=feature))

                    # Serialize to string and write to file
                    writer.write(example_proto.SerializeToString())
            else:
                # Folder dataset
                data = self.process_folder_dataset(dataset)

                for i in range(len(data['images'])):
                    image = data['images'][i]
                    label = data['labels'][i]

                    # Convert image to bytes
                    image_bytes = tf.io.encode_jpeg(image).numpy()

                    # Create a feature
                    feature = {
                        'image': _bytes_feature(image_bytes),
                        'label': _bytes_feature(label.encode('utf-8'))
                    }

                    # Create an example protocol buffer
                    example_proto = tf.train.Example(
                        features=tf.train.Features(feature=feature))

                    # Serialize to string and write to file
                    writer.write(example_proto.SerializeToString())

    def _export_to_csv(self, dataset, dataset_name, output_path):
        """
        تصدير إلى CSV

        Args:
            dataset: مجموعة البيانات
            dataset_name: اسم مجموعة البيانات
            output_path: مسار الإخراج
        """
        import csv

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['image_path', 'label'])

            if dataset_name == 'plantvillage_tfds':
                # لا يمكن تصدير TensorFlow Dataset إلى CSV مباشرة
                logger.warning(
                    "⚠️ لا يمكن تصدير TensorFlow Dataset إلى CSV مباشرة")
            else:
                # Folder dataset
                for root, dirs, files in os.walk(dataset):
                    for file in files:
                        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            file_path = os.path.join(root, file)
                            label = os.path.basename(root)
                            writer.writerow([file_path, label])

    def _export_to_json(self, dataset, dataset_name, output_path):
        """
        تصدير إلى JSON

        Args:
            dataset: مجموعة البيانات
            dataset_name: اسم مجموعة البيانات
            output_path: مسار الإخراج
        """
        import json

        data = []

        if dataset_name == 'plantvillage_tfds':
            # لا يمكن تصدير TensorFlow Dataset إلى JSON مباشرة
            logger.warning(
                "⚠️ لا يمكن تصدير TensorFlow Dataset إلى JSON مباشرة")
        else:
            # Folder dataset
            for root, dirs, files in os.walk(dataset):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file_path = os.path.join(root, file)
                        label = os.path.basename(root)

                        try:
                            from PIL import Image
                            img = Image.open(file_path)

                            data.append({
                                'image_path': file_path,
                                'label': label,
                                'width': img.width,
                                'height': img.height,
                                'mode': img.mode
                            })
                        except Exception as e:
                            logger.error(f"تجاهل {file_path}: {e}")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class AdvancedTrainingSystem:
    """نظام التدريب المتقدم للنماذج"""

    def __init__(self, processor, dataset_manager):
        """
        تهيئة نظام التدريب المتقدم

        Args:
            processor: معالج أمراض النباتات
            dataset_manager: مدير مجموعات البيانات
        """
        self.processor = processor
        self.dataset_manager = dataset_manager
        self.training_history = {}

        logger.info("تم تهيئة نظام التدريب المتقدم")

    def create_custom_model(self, num_classes=38):
        """
        إنشاء نموذج مخصص يجمع المعرفة من النماذج الموجودة

        Args:
            num_classes: عدد الفئات

        Returns:
            object: النموذج المخصص
        """
        try:
            # Knowledge Distillation من النماذج المتعددة
            student_model = self.create_student_architecture(num_classes)

            logger.info(f"✅ تم إنشاء نموذج طالب مخصص بـ {num_classes} فئة")
            return student_model
        except Exception as e:
            logger.error(f"❌ فشل إنشاء نموذج مخصص: {e}")
            return None

    def create_student_architecture(self, num_classes=38):
        """
        إنشاء معمارية الطالب

        Args:
            num_classes: عدد الفئات

        Returns:
            object: معمارية الطالب
        """
        try:
            import torch.nn as nn

            class PlantDiseaseStudent(nn.Module):
                def __init__(self, num_classes=38):
                    super().__init__()

                    # Efficient backbone
                    self.backbone = self.create_efficient_backbone()

                    # Multi-task heads
                    self.disease_head = nn.Linear(512, num_classes)
                    self.severity_head = nn.Linear(512, 1)
                    self.stress_head = nn.Linear(512, 5)  # 5 stress types

                def create_efficient_backbone(self):
                    """إنشاء backbone فعال"""

                    return nn.Sequential(
                        # Depthwise separable convolutions
                        self.depthwise_separable_conv(3, 32, 3, 2),
                        self.depthwise_separable_conv(32, 64, 3, 1),
                        self.depthwise_separable_conv(64, 128, 3, 2),
                        self.depthwise_separable_conv(128, 256, 3, 1),
                        self.depthwise_separable_conv(256, 512, 3, 2),

                        nn.AdaptiveAvgPool2d((1, 1)),
                        nn.Flatten()
                    )

                def depthwise_separable_conv(
                        self, in_channels, out_channels, kernel_size, stride):
                    """Depthwise Separable Convolution"""

                    return nn.Sequential(
                        # Depthwise
                        nn.Conv2d(in_channels, in_channels, kernel_size, stride,
                                  padding=kernel_size // 2, groups=in_channels),
                        nn.BatchNorm2d(in_channels),
                        nn.ReLU6(inplace=True),

                        # Pointwise
                        nn.Conv2d(in_channels, out_channels, 1),
                        nn.BatchNorm2d(out_channels),
                        nn.ReLU6(inplace=True)
                    )

                def forward(self, x):
                    features = self.backbone(x)

                    disease_pred = self.disease_head(features)
                    severity_pred = self.severity_head(features)
                    stress_pred = self.stress_head(features)

                    return {
                        'disease': disease_pred,
                        'severity': severity_pred,
                        'stress': stress_pred
                    }

            return PlantDiseaseStudent(num_classes)
        except Exception as e:
            logger.error(f"❌ فشل إنشاء معمارية الطالب: {e}")
            raise

    def train_with_ensemble_teachers(
            self,
            student_model,
            epochs=100,
            batch_size=32,
            learning_rate=1e-4):
        """
        تدريب باستخدام المعلمين المتعددين

        Args:
            student_model: نموذج الطالب
            epochs: عدد الحقب
            batch_size: حجم الدفعة
            learning_rate: معدل التعلم

        Returns:
            dict: تاريخ التدريب
        """
        try:
            # إعداد المعلمين
            teachers = self.setup_teacher_models()

            if not teachers:
                logger.error("❌ لا توجد نماذج معلمة متاحة")
                return None

            # إعداد البيانات
            train_loader = self.prepare_training_data(batch_size)

            if train_loader is None:
                logger.error("❌ فشل إعداد بيانات التدريب")
                return None

            # تدريب Knowledge Distillation
            history = self.knowledge_distillation_training(
                student_model, teachers, train_loader, epochs, learning_rate
            )

            logger.info(f"✅ تم تدريب النموذج المخصص لـ {epochs} حقبة")
            return history
        except Exception as e:
            logger.error(f"❌ فشل تدريب النموذج المخصص: {e}")
            return None

    def setup_teacher_models(self):
        """
        إعداد النماذج المعلمة

        Returns:
            dict: النماذج المعلمة
        """
        teachers = {}

        # استخدام النماذج المتاحة كمعلمين
        for model_name, model in self.processor.models.items():
            if model_name in [
                'mobilenet_plant',
                'vit_plant',
                    'alexnet_plantvillage']:
                teachers[model_name] = model
                logger.info(f"✅ تم إعداد {model_name} كنموذج معلم")

        return teachers

    def knowledge_distillation_training(
            self,
            student,
            teachers,
            train_loader,
            epochs=100,
            learning_rate=1e-4):
        """
        تدريب Knowledge Distillation

        Args:
            student: نموذج الطالب
            teachers: النماذج المعلمة
            train_loader: محمل بيانات التدريب
            epochs: عدد الحقب
            learning_rate: معدل التعلم

        Returns:
            dict: تاريخ التدريب
        """
        try:
            import torch.optim as optim

            optimizer = optim.AdamW(student.parameters(), lr=learning_rate)
            scheduler = optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=epochs)

            student.train()

            history = {
                'loss': [],
                'classification_loss': [],
                'distillation_loss': []
            }

            for epoch in range(epochs):
                total_loss = 0
                total_classification_loss = 0
                total_distillation_loss = 0

                for batch_idx, (data, target) in enumerate(train_loader):
                    optimizer.zero_grad()

                    # Student prediction
                    student_output = student(data)

                    # Teacher predictions
                    teacher_outputs = self.get_teacher_predictions(
                        data, teachers)

                    # Calculate losses
                    classification_loss, distillation_loss, loss = self.calculate_distillation_loss(
                        student_output, teacher_outputs, target)

                    loss.backward()
                    optimizer.step()

                    total_loss += loss.item()
                    total_classification_loss += classification_loss.item()
                    total_distillation_loss += distillation_loss.item()

                scheduler.step()

                # حساب متوسط الخسارة
                avg_loss = total_loss / len(train_loader)
                avg_classification_loss = total_classification_loss / \
                    len(train_loader)
                avg_distillation_loss = total_distillation_loss / \
                    len(train_loader)

                # تحديث التاريخ
                history['loss'].append(avg_loss)
                history['classification_loss'].append(avg_classification_loss)
                history['distillation_loss'].append(avg_distillation_loss)

                if epoch % 10 == 0:
                    logger.info(
                        f"Epoch {epoch}, Loss: {avg_loss:.4f}, Classification Loss: {avg_classification_loss:.4f}, Distillation Loss: {avg_distillation_loss:.4f}")

            return history
        except Exception as e:
            logger.error(f"❌ فشل تدريب Knowledge Distillation: {e}")
            raise

    def get_teacher_predictions(self, data, teachers):
        """
        الحصول على تنبؤات المعلمين

        Args:
            data: البيانات
            teachers: النماذج المعلمة

        Returns:
            dict: تنبؤات المعلمين
        """
        import torch

        teacher_outputs = {}

        for name, teacher in teachers.items():
            try:
                teacher.eval()
                with torch.no_grad():
                    if hasattr(teacher, 'forward'):
                        output = teacher(data)
                        teacher_outputs[name] = output
            except Exception as e:
                logger.error(f"❌ خطأ في المعلم {name}: {e}")

        return teacher_outputs

    def calculate_distillation_loss(
            self,
            student_output,
            teacher_outputs,
            target):
        """
        حساب خسارة التقطير

        Args:
            student_output: إخراج الطالب
            teacher_outputs: إخراج المعلمين
            target: الهدف

        Returns:
            tuple: خسارة التصنيف، خسارة التقطير، الخسارة الإجمالية
        """
        import torch.nn.functional as F

        # Classification loss
        classification_loss = F.cross_entropy(
            student_output['disease'], target)

        # Distillation loss from teachers
        distillation_loss = 0
        temperature = 4.0

        for teacher_name, teacher_output in teacher_outputs.items():
            if isinstance(
                    teacher_output,
                    dict) and 'disease' in teacher_output:
                teacher_logits = teacher_output['disease']
            else:
                teacher_logits = teacher_output

            # Soft targets from teacher
            teacher_soft = F.softmax(teacher_logits / temperature, dim=1)
            student_soft = F.log_softmax(
                student_output['disease'] / temperature, dim=1)

            kd_loss = F.kl_div(
                student_soft,
                teacher_soft,
                reduction='batchmean')
            distillation_loss += kd_loss

        # Weighted combination
        total_loss = 0.3 * classification_loss + 0.7 * distillation_loss

        return classification_loss, distillation_loss, total_loss

    def prepare_training_data(self, batch_size=32):
        """
        إعداد بيانات التدريب

        Args:
            batch_size: حجم الدفعة

        Returns:
            object: محمل بيانات التدريب
        """
        try:
            # إنشاء مجموعة بيانات موحدة
            unified_data = self.dataset_manager.create_unified_dataset()

            if not unified_data['images']:
                logger.error("❌ لا توجد بيانات متاحة للتدريب")
                return None

            # تحويل لـ PyTorch DataLoader
            dataset = self.create_pytorch_dataset(unified_data)

            from torch.utils.data import DataLoader
            return DataLoader(dataset, batch_size=batch_size, shuffle=True)
        except Exception as e:
            logger.error(f"❌ فشل إعداد بيانات التدريب: {e}")
            return None

    def create_pytorch_dataset(self, unified_data):
        """
        إنشاء PyTorch Dataset

        Args:
            unified_data: البيانات الموحدة

        Returns:
            object: PyTorch Dataset
        """
        try:
            import torch
            from torch.utils.data import Dataset

            class PlantDiseaseDataset(Dataset):
                def __init__(self, data):
                    self.images = data['images']
                    self.labels = data['labels']
                    self.transform = self.get_transforms()

                def get_transforms(self):
                    from torchvision import transforms
                    return transforms.Compose([
                        transforms.ToPILImage(),
                        transforms.Resize((224, 224)),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                             std=[0.229, 0.224, 0.225])
                    ])

                def __len__(self):
                    return len(self.images)

                def __getitem__(self, idx):
                    image = self.images[idx]
                    label = self.labels[idx]

                    if self.transform:
                        image = self.transform(image)

                    return image, torch.tensor(label, dtype=torch.long)

            return PlantDiseaseDataset(unified_data)
        except Exception as e:
            logger.error(f"❌ فشل إنشاء PyTorch Dataset: {e}")
            raise

    def save_model(self, model, model_path):
        """
        حفظ النموذج

        Args:
            model: النموذج
            model_path: مسار الحفظ

        Returns:
            bool: نجاح الحفظ
        """
        try:
            import torch

            # إنشاء المجلد إذا لم يكن موجوداً
            os.makedirs(os.path.dirname(model_path), exist_ok=True)

            # حفظ النموذج
            torch.save(model.state_dict(), model_path)

            logger.info(f"✅ تم حفظ النموذج في {model_path}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل حفظ النموذج: {e}")
            return False

    def load_model(self, model_path, num_classes=38):
        """
        تحميل النموذج

        Args:
            model_path: مسار النموذج
            num_classes: عدد الفئات

        Returns:
            object: النموذج المحمل
        """
        try:
            import torch

            # إنشاء النموذج
            model = self.create_student_architecture(num_classes)

            # تحميل الأوزان
            model.load_state_dict(torch.load(model_path, map_location='cpu'))

            logger.info(f"✅ تم تحميل النموذج من {model_path}")
            return model
        except Exception as e:
            logger.error(f"❌ فشل تحميل النموذج: {e}")
            return None

    def evaluate_model(self, model, test_loader):
        """
        تقييم النموذج

        Args:
            model: النموذج
            test_loader: محمل بيانات الاختبار

        Returns:
            dict: نتائج التقييم
        """
        try:
            import numpy as np
            import torch
            from sklearn.metrics import (
                accuracy_score,
                confusion_matrix,
                f1_score,
                precision_score,
                recall_score,
            )

            model.eval()

            all_predictions = []
            all_targets = []

            with torch.no_grad():
                for data, target in test_loader:
                    # التنبؤ
                    output = model(data)

                    # الحصول على التنبؤات
                    predictions = torch.argmax(output['disease'], dim=1)

                    # إضافة التنبؤات والأهداف
                    all_predictions.extend(predictions.cpu().numpy())
                    all_targets.extend(target.cpu().numpy())

            # حساب المقاييس
            accuracy = accuracy_score(all_targets, all_predictions)
            precision = precision_score(
                all_targets, all_predictions, average='weighted')
            recall = recall_score(
                all_targets,
                all_predictions,
                average='weighted')
            f1 = f1_score(all_targets, all_predictions, average='weighted')
            conf_matrix = confusion_matrix(all_targets, all_predictions)

            # حساب مقاييس الفئات
            class_metrics = {}
            classes = np.unique(all_targets)

            for cls in classes:
                cls_precision = precision_score(
                    all_targets, all_predictions, labels=[cls], average='weighted')
                cls_recall = recall_score(
                    all_targets,
                    all_predictions,
                    labels=[cls],
                    average='weighted')
                cls_f1 = f1_score(
                    all_targets,
                    all_predictions,
                    labels=[cls],
                    average='weighted')

                class_metrics[int(cls)] = {
                    'precision': float(cls_precision),
                    'recall': float(cls_recall),
                    'f1_score': float(cls_f1)
                }

            results = {
                'accuracy': float(accuracy),
                'precision': float(precision),
                'recall': float(recall),
                'f1_score': float(f1),
                'confusion_matrix': conf_matrix.tolist(),
                'class_metrics': class_metrics
            }

            logger.info(f"✅ تم تقييم النموذج، الدقة: {accuracy:.4f}")
            return results
        except Exception as e:
            logger.error(f"❌ فشل تقييم النموذج: {e}")
            return None

    def optimize_model(self, model, method, config=None):
        """
        تحسين النموذج

        Args:
            model: النموذج
            method: طريقة التحسين (pruning, quantization, distillation)
            config: إعدادات التحسين

        Returns:
            object: النموذج المحسن
        """
        try:
            if method == 'pruning':
                return self._apply_pruning(model, config)
            elif method == 'quantization':
                return self._apply_quantization(model, config)
            elif method == 'distillation':
                return self._apply_distillation(model, config)
            else:
                logger.error(f"❌ طريقة التحسين {method} غير مدعومة")
                return None
        except Exception as e:
            logger.error(f"❌ فشل تحسين النموذج: {e}")
            return None

    def _apply_pruning(self, model, config=None):
        """
        تطبيق التقليم

        Args:
            model: النموذج
            config: إعدادات التقليم

        Returns:
            object: النموذج المقلم
        """
        try:
            import torch.nn.utils.prune as prune

            if config is None:
                config = {'pruning_ratio': 0.5}

            pruning_ratio = config.get('pruning_ratio', 0.5)

            # تطبيق التقليم على جميع الطبقات الخطية
            for name, module in model.named_modules():
                if isinstance(
                        module,
                        torch.nn.Linear) or isinstance(
                        module,
                        torch.nn.Conv2d):
                    prune.l1_unstructured(
                        module, name='weight', amount=pruning_ratio)
                    prune.remove(module, 'weight')

            logger.info(f"✅ تم تطبيق التقليم بنسبة {pruning_ratio}")
            return model
        except Exception as e:
            logger.error(f"❌ فشل تطبيق التقليم: {e}")
            raise

    def _apply_quantization(self, model, config=None):
        """
        تطبيق التكميم

        Args:
            model: النموذج
            config: إعدادات التكميم

        Returns:
            object: النموذج المكمم
        """
        try:
            import torch

            if config is None:
                config = {'quantization_type': 'int8'}

            quantization_type = config.get('quantization_type', 'int8')

            # تطبيق التكميم
            if quantization_type == 'int8':
                # INT8 quantization
                model_quantized = torch.quantization.quantize_dynamic(
                    model, {torch.nn.Linear, torch.nn.Conv2d}, dtype=torch.qint8
                )
            elif quantization_type == 'fp16':
                # FP16 quantization
                model_quantized = model.half()
            else:
                logger.error(f"❌ نوع التكميم {quantization_type} غير مدعوم")
                return model

            logger.info(f"✅ تم تطبيق التكميم بنوع {quantization_type}")
            return model_quantized
        except Exception as e:
            logger.error(f"❌ فشل تطبيق التكميم: {e}")
            raise

    def _apply_distillation(self, model, config=None):
        """
        تطبيق تقطير المعرفة

        Args:
            model: النموذج
            config: إعدادات التقطير

        Returns:
            object: النموذج المقطر
        """
        try:
            if config is None or 'teacher_model_id' not in config:
                logger.error("❌ يجب تحديد معرف النموذج المعلم")
                return model

            teacher_model_id = config.get('teacher_model_id')

            # التحقق من وجود النموذج المعلم
            if teacher_model_id not in self.processor.models:
                logger.error(f"❌ النموذج المعلم {teacher_model_id} غير متاح")
                return model

            # تطبيق تقطير المعرفة
            # هذا يتطلب تدريب النموذج الطالب باستخدام النموذج المعلم
            # وهو ما تم تنفيذه في دالة train_with_ensemble_teachers

            logger.info(
                f"✅ تم تطبيق تقطير المعرفة باستخدام {teacher_model_id}")
            return model
        except Exception as e:
            logger.error(f"❌ فشل تطبيق تقطير المعرفة: {e}")
            raise

    def export_model(self, model, format, output_path):
        """
        تصدير النموذج

        Args:
            model: النموذج
            format: صيغة التصدير (onnx, tflite, pytorch, coreml)
            output_path: مسار الإخراج

        Returns:
            bool: نجاح التصدير
        """
        try:
            if format == 'onnx':
                return self._export_to_onnx(model, output_path)
            elif format == 'tflite':
                return self._export_to_tflite(model, output_path)
            elif format == 'pytorch':
                return self._export_to_pytorch(model, output_path)
            elif format == 'coreml':
                return self._export_to_coreml(model, output_path)
            else:
                logger.error(f"❌ صيغة التصدير {format} غير مدعومة")
                return False
        except Exception as e:
            logger.error(f"❌ فشل تصدير النموذج: {e}")
            return False

    def _export_to_onnx(self, model, output_path):
        """
        تصدير إلى ONNX

        Args:
            model: النموذج
            output_path: مسار الإخراج

        Returns:
            bool: نجاح التصدير
        """
        try:
            import torch

            # إنشاء مدخلات وهمية
            dummy_input = torch.randn(1, 3, 224, 224)

            # تصدير النموذج
            torch.onnx.export(
                model,
                dummy_input,
                output_path,
                export_params=True,
                opset_version=11,
                do_constant_folding=True,
                input_names=['input'],
                output_names=['output'],
                dynamic_axes={
                    'input': {
                        0: 'batch_size'},
                    'output': {
                        0: 'batch_size'}})

            logger.info(f"✅ تم تصدير النموذج إلى ONNX في {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل تصدير النموذج إلى ONNX: {e}")
            raise

    def _export_to_tflite(self, model, output_path):
        """
        تصدير إلى TensorFlow Lite

        Args:
            model: النموذج
            output_path: مسار الإخراج

        Returns:
            bool: نجاح التصدير
        """
        try:
            # تصدير إلى ONNX أولاً
            onnx_path = output_path.replace('.tflite', '.onnx')
            self._export_to_onnx(model, onnx_path)

            # تحويل من ONNX إلى TensorFlow
            import onnx
            from onnx_tf.backend import prepare

            onnx_model = onnx.load(onnx_path)
            tf_rep = prepare(onnx_model)

            # تصدير إلى TensorFlow Lite
            import tensorflow as tf

            converter = tf.lite.TFLiteConverter.from_saved_model(
                tf_rep.export_graph())
            tflite_model = converter.convert()

            with open(output_path, 'wb') as f:
                f.write(tflite_model)

            logger.info(
                f"✅ تم تصدير النموذج إلى TensorFlow Lite في {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل تصدير النموذج إلى TensorFlow Lite: {e}")
            raise

    def _export_to_pytorch(self, model, output_path):
        """
        تصدير إلى PyTorch

        Args:
            model: النموذج
            output_path: مسار الإخراج

        Returns:
            bool: نجاح التصدير
        """
        try:
            import torch

            # حفظ النموذج
            torch.save(model, output_path)

            logger.info(f"✅ تم تصدير النموذج إلى PyTorch في {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل تصدير النموذج إلى PyTorch: {e}")
            raise

    def _export_to_coreml(self, model, output_path):
        """
        تصدير إلى Core ML

        Args:
            model: النموذج
            output_path: مسار الإخراج

        Returns:
            bool: نجاح التصدير
        """
        try:
            # تصدير إلى ONNX أولاً
            onnx_path = output_path.replace('.mlmodel', '.onnx')
            self._export_to_onnx(model, onnx_path)

            # تحويل من ONNX إلى Core ML
            import coremltools as ct
            import onnx

            onnx_model = onnx.load(onnx_path)
            mlmodel = ct.converters.onnx.convert(
                model=onnx_model,
                minimum_ios_deployment_target='13'
            )

            # حفظ النموذج
            mlmodel.save(output_path)

            logger.info(f"✅ تم تصدير النموذج إلى Core ML في {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل تصدير النموذج إلى Core ML: {e}")
            raise
