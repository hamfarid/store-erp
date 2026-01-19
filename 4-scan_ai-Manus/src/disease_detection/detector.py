#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة الكشف عن الأمراض النباتية
===========================

توفر هذه الوحدة وظائف للكشف عن الأمراض النباتية (فيروسية، بكتيرية، فطرية)
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
logger = logging.getLogger("agricultural_ai.disease_detector")

class DiseaseDetector:
    """فئة للكشف عن الأمراض النباتية باستخدام نماذج التعلم العميق"""
    
    def __init__(self, config: Dict):
        """تهيئة كاشف الأمراض
        
        المعاملات:
            config (Dict): تكوين كاشف الأمراض
        """
        self.config = config
        self.model_base_path = self.config.get("model_path", "models/disease_detection")
        self.confidence_threshold = self.config.get("confidence_threshold", 0.75)
        self.enable_gpu = self.config.get("enable_gpu", True)
        self.image_size = tuple(self.config.get("image_size", [224, 224]))
        self.models_config = self.config.get("models", {})
        self.disease_db_path = self.config.get("database", {}).get("diseases_db", "database/diseases.db")
        
        # تهيئة معالج الصور
        self.image_processor = ImageProcessor()
        
        # تحميل النماذج
        self.models = self._load_models()
        
        # تحميل قاعدة بيانات الأمراض (إذا كانت موجودة)
        self.disease_info = self._load_disease_info()
        
        logger.info("تم تهيئة كاشف الأمراض")
        
    def _load_models(self) -> Dict[str, Optional[tf.keras.Model]]:
        """تحميل نماذج الكشف عن الأمراض"""
        models = {}
        for disease_type, model_config in self.models_config.items():
            model_file = model_config.get("model_file")
            classes_file = model_config.get("classes_file")
            
            if not model_file or not classes_file:
                logger.warning(f"لم يتم تحديد ملف النموذج أو ملف الفئات لنوع المرض: {disease_type}")
                models[disease_type] = None
                continue
            
            model_path = os.path.join(self.model_base_path, model_file)
            classes_path = os.path.join(self.model_base_path, classes_file)
            
            if not os.path.exists(model_path):
                logger.error(f"ملف النموذج غير موجود: {model_path} لنوع المرض: {disease_type}")
                models[disease_type] = None
                continue
            
            if not os.path.exists(classes_path):
                logger.error(f"ملف الفئات غير موجود: {classes_path} لنوع المرض: {disease_type}")
                models[disease_type] = None
                continue
            
            try:
                # تحميل النموذج
                model = load_model(model_path)
                logger.info(f"تم تحميل نموذج {disease_type} من: {model_path}")
                
                # تحميل الفئات
                with open(classes_path, "r", encoding="utf-8") as f:
                    classes = json.load(f)
                
                models[disease_type] = {
                    "model": model,
                    "classes": classes
                }
                
            except Exception as e:
                logger.error(f"فشل في تحميل نموذج {disease_type} من {model_path}: {str(e)}")
                models[disease_type] = None
                
        return models

    def _load_disease_info(self) -> Dict:
        """تحميل معلومات الأمراض من قاعدة البيانات (ملف JSON كمثال)"""
        # ملاحظة: في نظام حقيقي، يجب استخدام قاعدة بيانات فعلية (مثل SQLite أو PostgreSQL)
        # هنا نستخدم ملف JSON كمثال بسيط.
        disease_info = {}
        db_path = self.disease_db_path.replace(".db", ".json") # استخدام JSON كمثال
        if os.path.exists(db_path):
            try:
                with open(db_path, "r", encoding="utf-8") as f:
                    disease_info = json.load(f)
                logger.info(f"تم تحميل معلومات الأمراض من: {db_path}")
            except Exception as e:
                logger.error(f"فشل في تحميل معلومات الأمراض من {db_path}: {str(e)}")
        else:
            logger.warning(f"ملف معلومات الأمراض غير موجود: {db_path}")
        return disease_info

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

    def detect(self, image_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """الكشف عن الأمراض في الصورة
        
        المعاملات:
            image_path (str): مسار الصورة
            
        الإرجاع:
            Dict[str, List[Dict[str, Any]]]: قاموس يحتوي على نتائج الكشف لكل نوع مرض
        """
        results = {}
        
        # معالجة الصورة
        preprocessed_image = self._preprocess_image(image_path)
        if preprocessed_image is None:
            return {"error": f"فشل في معالجة الصورة: {image_path}"}
        
        # تحليل الصورة باستخدام كل نموذج متاح
        for disease_type, model_data in self.models.items():
            if model_data is None:
                logger.warning(f"تخطي الكشف عن {disease_type} لعدم توفر النموذج")
                results[disease_type] = []
                continue
            
            model = model_data["model"]
            classes = model_data["classes"]
            
            try:
                # إجراء التنبؤ
                predictions = model.predict(preprocessed_image)[0]
                
                # معالجة النتائج
                detected_diseases = []
                for i, prediction in enumerate(predictions):
                    if prediction >= self.confidence_threshold:
                        class_name = classes[str(i)] # الفئات قد تكون مفهرسة كسلاسل نصية في JSON
                        disease_details = self.disease_info.get(class_name, {})
                        detected_diseases.append({
                            "disease_name": class_name,
                            "confidence": float(prediction),
                            "type": disease_type,
                            "description": disease_details.get("description", "لا توجد معلومات إضافية متاحة."),
                            "symptoms": disease_details.get("symptoms", []),
                            "causes": disease_details.get("causes", [])
                        })
                
                # ترتيب النتائج حسب الثقة
                detected_diseases = sorted(detected_diseases, key=lambda x: x["confidence"], reverse=True)
                results[disease_type] = detected_diseases
                logger.info(f"تم الكشف عن {len(detected_diseases)} مرض من نوع {disease_type}")
                
            except Exception as e:
                logger.error(f"فشل في الكشف عن {disease_type} باستخدام النموذج: {str(e)}")
                results[disease_type] = []
        
        return results

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "model_path": "../../models/disease_detection", # مسار نسبي من موقع الملف
        "confidence_threshold": 0.5,
        "image_size": [224, 224],
        "models": {
            "viral": {
                "model_file": "viral_diseases_model.h5",
                "classes_file": "viral_diseases_classes.json"
            },
            "fungal": {
                "model_file": "fungal_diseases_model.h5",
                "classes_file": "fungal_diseases_classes.json"
            }
        },
        "database": {
            "diseases_db": "../../database/diseases.db" # مسار نسبي
        }
    }
    
    # إنشاء مجلدات وهمية وملفات نماذج وفئات وقاعدة بيانات (للتجربة فقط)
    os.makedirs("../../models/disease_detection", exist_ok=True)
    os.makedirs("../../database", exist_ok=True)
    
    # إنشاء ملفات نماذج وهمية
    try:
        # نموذج وهمي بسيط
        input_shape = (224, 224, 3)
        num_classes_viral = 5
        num_classes_fungal = 10
        
        viral_model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Conv2D(8, (3, 3), activation=\'relu\'),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(num_classes_viral, activation=\'softmax\')
        ])
        viral_model.save(os.path.join(dummy_config["model_path"], dummy_config["models"]["viral"]["model_file"]))
        
        fungal_model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Conv2D(8, (3, 3), activation=\'relu\'),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(num_classes_fungal, activation=\'softmax\')
        ])
        fungal_model.save(os.path.join(dummy_config["model_path"], dummy_config["models"]["fungal"]["model_file"]))
        
        # إنشاء ملفات فئات وهمية
        viral_classes = {str(i): f"Viral Disease {i+1}" for i in range(num_classes_viral)}
        with open(os.path.join(dummy_config["model_path"], dummy_config["models"]["viral"]["classes_file"]), "w") as f:
            json.dump(viral_classes, f)
            
        fungal_classes = {str(i): f"Fungal Disease {i+1}" for i in range(num_classes_fungal)}
        with open(os.path.join(dummy_config["model_path"], dummy_config["models"]["fungal"]["classes_file"]), "w") as f:
            json.dump(fungal_classes, f)
            
        # إنشاء ملف قاعدة بيانات أمراض وهمي (JSON)
        disease_db_data = {
            "Viral Disease 1": {"description": "وصف للمرض الفيروسي 1", "symptoms": ["عرض 1", "عرض 2"]},
            "Fungal Disease 3": {"description": "وصف للمرض الفطري 3", "causes": ["سبب 1"]}
        }
        db_path_json = dummy_config["database"]["diseases_db"].replace(".db", ".json")
        with open(db_path_json, "w", encoding="utf-8") as f:
            json.dump(disease_db_data, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        logger.error(f"حدث خطأ أثناء إنشاء الملفات الوهمية: {e}")

    # إنشاء صورة وهمية (بيضاء)
    dummy_image_path = "dummy_plant_image.png"
    dummy_image = np.ones((300, 300, 3), dtype=np.uint8) * 255
    cv2.imwrite(dummy_image_path, dummy_image)
    
    # تهيئة الكاشف
    detector = DiseaseDetector(dummy_config)
    
    # الكشف عن الأمراض في الصورة الوهمية
    detection_results = detector.detect(dummy_image_path)
    
    # طباعة النتائج
    print("\nنتائج الكشف عن الأمراض:")
    print(json.dumps(detection_results, indent=4, ensure_ascii=False))
    
    # تنظيف الملفات الوهمية
    # import shutil
    # os.remove(dummy_image_path)
    # shutil.rmtree("../../models")
    # shutil.rmtree("../../database")
    # logger.info("تم حذف الملفات والمجلدات الوهمية")
