#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة تحليل نقص العناصر الغذائية
=============================

توفر هذه الوحدة وظائف لتحليل صور النباتات وتحديد علامات نقص العناصر الغذائية
باستخدام نماذج التعلم العميق وتحليل الصور.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# استيراد معالج الصور من وحدة الأدوات
from src.utils.image_processor import ImageProcessor

# إعداد السجل
logger = logging.getLogger("agricultural_ai.nutrient_analyzer")

class NutrientAnalyzer:
    """فئة لتحليل نقص العناصر الغذائية باستخدام نماذج التعلم العميق"""
    
    def __init__(self, config: Dict):
        """تهيئة محلل نقص العناصر
        
        المعاملات:
            config (Dict): تكوين محلل نقص العناصر
        """
        self.config = config
        self.model_base_path = self.config.get("model_path", "models/nutrient_analysis")
        self.confidence_threshold = self.config.get("confidence_threshold", 0.7)
        self.enable_gpu = self.config.get("enable_gpu", True)
        self.image_size = tuple(self.config.get("image_size", [299, 299])) # حجم مختلف قد يكون مناسبًا لنقص العناصر
        self.models_config = self.config.get("models", {})
        self.nutrient_db_path = self.config.get("database", {}).get("nutrients_db", "database/nutrients.db")
        
        # تهيئة معالج الصور
        self.image_processor = ImageProcessor()
        
        # تحميل النماذج
        self.models = self._load_models()
        
        # تحميل قاعدة بيانات العناصر الغذائية (إذا كانت موجودة)
        self.nutrient_info = self._load_nutrient_info()
        
        logger.info("تم تهيئة محلل نقص العناصر الغذائية")
        
    def _load_models(self) -> Dict[str, Optional[tf.keras.Model]]:
        """تحميل نماذج تحليل نقص العناصر"""
        models = {}
        for nutrient_category, model_config in self.models_config.items():
            model_file = model_config.get("model_file")
            classes_file = model_config.get("classes_file")
            
            if not model_file or not classes_file:
                logger.warning(f"لم يتم تحديد ملف النموذج أو ملف الفئات لفئة العناصر: {nutrient_category}")
                models[nutrient_category] = None
                continue
            
            model_path = os.path.join(self.model_base_path, model_file)
            classes_path = os.path.join(self.model_base_path, classes_file)
            
            if not os.path.exists(model_path):
                logger.error(f"ملف النموذج غير موجود: {model_path} لفئة العناصر: {nutrient_category}")
                models[nutrient_category] = None
                continue
            
            if not os.path.exists(classes_path):
                logger.error(f"ملف الفئات غير موجود: {classes_path} لفئة العناصر: {nutrient_category}")
                models[nutrient_category] = None
                continue
            
            try:
                # تحميل النموذج
                model = load_model(model_path)
                logger.info(f"تم تحميل نموذج {nutrient_category} من: {model_path}")
                
                # تحميل الفئات
                with open(classes_path, "r", encoding="utf-8") as f:
                    classes = json.load(f)
                
                models[nutrient_category] = {
                    "model": model,
                    "classes": classes
                }
                
            except Exception as e:
                logger.error(f"فشل في تحميل نموذج {nutrient_category} من {model_path}: {str(e)}")
                models[nutrient_category] = None
                
        return models

    def _load_nutrient_info(self) -> Dict:
        """تحميل معلومات العناصر الغذائية من قاعدة البيانات (ملف JSON كمثال)"""
        nutrient_info = {}
        db_path = self.nutrient_db_path.replace(".db", ".json") # استخدام JSON كمثال
        if os.path.exists(db_path):
            try:
                with open(db_path, "r", encoding="utf-8") as f:
                    nutrient_info = json.load(f)
                logger.info(f"تم تحميل معلومات العناصر الغذائية من: {db_path}")
            except Exception as e:
                logger.error(f"فشل في تحميل معلومات العناصر الغذائية من {db_path}: {str(e)}")
        else:
            logger.warning(f"ملف معلومات العناصر الغذائية غير موجود: {db_path}")
        return nutrient_info

    def _preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """معالجة الصورة قبل إدخالها للنموذج"""
        try:
            # تحميل الصورة باستخدام معالج الصور
            img = self.image_processor.load_image(image_path)
            
            # تغيير حجم الصورة إلى الحجم المطلوب للنموذج
            img = self.image_processor.resize_image(img, self.image_size)
            
            # تحويل الصورة إلى مصفوفة وتطبيع القيم
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # إضافة بعد الدفعة
            img_array = img_array / 255.0  # تطبيع القيم إلى [0, 1]
            
            return img_array
        except Exception as e:
            logger.error(f"فشل في معالجة الصورة {image_path}: {str(e)}")
            return None

    def analyze(self, image_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """تحليل نقص العناصر الغذائية في الصورة
        
        المعاملات:
            image_path (str): مسار الصورة
            
        الإرجاع:
            Dict[str, List[Dict[str, Any]]]: قاموس يحتوي على نتائج التحليل لكل فئة عنصر
        """
        results = {}
        
        # معالجة الصورة
        preprocessed_image = self._preprocess_image(image_path)
        if preprocessed_image is None:
            return {"error": f"فشل في معالجة الصورة: {image_path}"}
        
        # تحليل الصورة باستخدام كل نموذج متاح
        for nutrient_category, model_data in self.models.items():
            if model_data is None:
                logger.warning(f"تخطي تحليل {nutrient_category} لعدم توفر النموذج")
                results[nutrient_category] = []
                continue
            
            model = model_data["model"]
            classes = model_data["classes"]
            
            try:
                # إجراء التنبؤ
                predictions = model.predict(preprocessed_image)[0]
                
                # معالجة النتائج
                detected_deficiencies = []
                for i, prediction in enumerate(predictions):
                    if prediction >= self.confidence_threshold:
                        class_name = classes[str(i)] # الفئات قد تكون مفهرسة كسلاسل نصية في JSON
                        nutrient_details = self.nutrient_info.get(class_name, {})
                        detected_deficiencies.append({
                            "deficiency_name": class_name,
                            "confidence": float(prediction),
                            "category": nutrient_category,
                            "description": nutrient_details.get("description", "لا توجد معلومات إضافية متاحة."),
                            "symptoms": nutrient_details.get("symptoms", []),
                            "affected_plants": nutrient_details.get("affected_plants", [])
                        })
                
                # ترتيب النتائج حسب الثقة
                detected_deficiencies = sorted(detected_deficiencies, key=lambda x: x["confidence"], reverse=True)
                results[nutrient_category] = detected_deficiencies
                logger.info(f"تم الكشف عن {len(detected_deficiencies)} نقص عنصر من فئة {nutrient_category}")
                
            except Exception as e:
                logger.error(f"فشل في تحليل {nutrient_category} باستخدام النموذج: {str(e)}")
                results[nutrient_category] = []
        
        # يمكن إضافة تحليل إضافي هنا باستخدام image_processor.analyze_leaf_health
        try:
            leaf_health_analysis = self.image_processor.analyze_leaf_health(self.image_processor.load_image(image_path))
            results["leaf_health"] = leaf_health_analysis
            logger.info("تم إجراء تحليل صحة الأوراق")
        except Exception as e:
            logger.error(f"فشل في تحليل صحة الأوراق: {str(e)}")
            results["leaf_health"] = {"error": "فشل تحليل صحة الأوراق"}
            
        return results

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "model_path": "../../models/nutrient_analysis", # مسار نسبي
        "confidence_threshold": 0.6,
        "image_size": [299, 299],
        "models": {
            "major_nutrients": {
                "model_file": "major_nutrients_model.h5",
                "classes_file": "major_nutrients_classes.json"
            },
            "minor_nutrients": {
                "model_file": "minor_nutrients_model.h5",
                "classes_file": "minor_nutrients_classes.json"
            }
        },
        "database": {
            "nutrients_db": "../../database/nutrients.db" # مسار نسبي
        }
    }
    
    # إنشاء مجلدات وهمية وملفات نماذج وفئات وقاعدة بيانات (للتجربة فقط)
    os.makedirs("../../models/nutrient_analysis", exist_ok=True)
    os.makedirs("../../database", exist_ok=True)
    
    # إنشاء ملفات نماذج وهمية
    try:
        # نموذج وهمي بسيط
        input_shape = (299, 299, 3)
        num_classes_major = 6 # N, P, K, Ca, Mg, S
        num_classes_minor = 7 # Fe, Mn, Zn, Cu, B, Mo, Cl
        
        major_model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Conv2D(8, (3, 3), activation=\'relu\'),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(num_classes_major, activation=\'softmax\')
        ])
        major_model.save(os.path.join(dummy_config["model_path"], dummy_config["models"]["major_nutrients"]["model_file"]))
        
        minor_model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Conv2D(8, (3, 3), activation=\'relu\'),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(num_classes_minor, activation=\'softmax\')
        ])
        minor_model.save(os.path.join(dummy_config["model_path"], dummy_config["models"]["minor_nutrients"]["model_file"]))
        
        # إنشاء ملفات فئات وهمية
        major_classes = {str(i): name for i, name in enumerate(["Nitrogen Deficiency", "Phosphorus Deficiency", "Potassium Deficiency", "Calcium Deficiency", "Magnesium Deficiency", "Sulfur Deficiency"])}
        with open(os.path.join(dummy_config["model_path"], dummy_config["models"]["major_nutrients"]["classes_file"]), "w") as f:
            json.dump(major_classes, f)
            
        minor_classes = {str(i): name for i, name in enumerate(["Iron Deficiency", "Manganese Deficiency", "Zinc Deficiency", "Copper Deficiency", "Boron Deficiency", "Molybdenum Deficiency", "Chlorine Deficiency"])}
        with open(os.path.join(dummy_config["model_path"], dummy_config["models"]["minor_nutrients"]["classes_file"]), "w") as f:
            json.dump(minor_classes, f)
            
        # إنشاء ملف قاعدة بيانات عناصر وهمي (JSON)
        nutrient_db_data = {
            "Nitrogen Deficiency": {"description": "اصفرار الأوراق القديمة", "symptoms": ["اصفرار عام", "نمو بطيء"]},
            "Iron Deficiency": {"description": "اصفرار بين العروق في الأوراق الحديثة", "affected_plants": ["الحمضيات", "الورود"]}
        }
        db_path_json = dummy_config["database"]["nutrients_db"].replace(".db", ".json")
        with open(db_path_json, "w", encoding="utf-8") as f:
            json.dump(nutrient_db_data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        logger.error(f"حدث خطأ أثناء إنشاء الملفات الوهمية: {e}")

    # استخدام الصورة الوهمية التي تم إنشاؤها سابقًا
    dummy_image_path = "dummy_plant_image.png"
    if not os.path.exists(dummy_image_path):
        dummy_image = np.ones((300, 300, 3), dtype=np.uint8) * 255
        cv2.imwrite(dummy_image_path, dummy_image)
    
    # تهيئة المحلل
    analyzer = NutrientAnalyzer(dummy_config)
    
    # تحليل نقص العناصر في الصورة الوهمية
    analysis_results = analyzer.analyze(dummy_image_path)
    
    # طباعة النتائج
    print("\nنتائج تحليل نقص العناصر:")
    print(json.dumps(analysis_results, indent=4, ensure_ascii=False))
    
    # تنظيف الملفات الوهمية (اختياري)
    # import shutil
    # os.remove(dummy_image_path)
    # shutil.rmtree("../../models")
    # shutil.rmtree("../../database")
    # logger.info("تم حذف الملفات والمجلدات الوهمية")
