#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مدير التعلم المستمر
=================

توفر هذه الوحدة وظائف للتعلم المستمر وتحديث النماذج بناءً على البيانات الجديدة.
تتضمن آليات لتقييم أداء النماذج، وتحديد الحاجة للتدريب، وإعادة تدريب النماذج.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import json
import logging
import time
import datetime
import numpy as np
import tensorflow as tf
from typing import Dict, List, Any, Optional, Union, Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# إعداد السجل
logger = logging.getLogger("agricultural_ai.continuous_learning")

class LearningManager:
    """فئة لإدارة التعلم المستمر وتحديث النماذج"""
    
    def __init__(self, config: Dict):
        """تهيئة مدير التعلم
        
        المعاملات:
            config (Dict): تكوين مدير التعلم
        """
        self.config = config.get("continuous_learning", {})
        self.models_dir = self.config.get("models_dir", "models")
        self.training_data_dir = self.config.get("training_data_dir", "data/training")
        self.validation_data_dir = self.config.get("validation_data_dir", "data/validation")
        self.performance_threshold = self.config.get("performance_threshold", 0.75)
        self.retraining_interval = self.config.get("retraining_interval_days", 30)
        self.auto_update = self.config.get("auto_update", False)
        self.metrics_history_file = self.config.get("metrics_history_file", "data/metrics_history.json")
        self.feedback_dir = self.config.get("feedback_dir", "data/feedback")
        
        # إنشاء المجلدات إذا لم تكن موجودة
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.training_data_dir, exist_ok=True)
        os.makedirs(self.validation_data_dir, exist_ok=True)
        os.makedirs(self.feedback_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.metrics_history_file), exist_ok=True)
        
        # تحميل سجل المقاييس إذا كان موجودًا
        self.metrics_history = self._load_metrics_history()
        
        logger.info("تم تهيئة مدير التعلم المستمر")

    def _load_metrics_history(self) -> Dict:
        """تحميل سجل مقاييس الأداء"""
        if os.path.exists(self.metrics_history_file):
            try:
                with open(self.metrics_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"فشل في تحميل سجل المقاييس: {e}")
        return {"models": {}}

    def _save_metrics_history(self):
        """حفظ سجل مقاييس الأداء"""
        try:
            with open(self.metrics_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.metrics_history, f, ensure_ascii=False, indent=4)
            logger.info("تم حفظ سجل المقاييس")
        except Exception as e:
            logger.error(f"فشل في حفظ سجل المقاييس: {e}")

    def evaluate_model(self, model_name: str, model: tf.keras.Model, 
                      validation_data: Tuple[np.ndarray, np.ndarray]) -> Dict[str, float]:
        """تقييم أداء النموذج على بيانات التحقق
        
        المعاملات:
            model_name (str): اسم النموذج
            model (tf.keras.Model): النموذج المراد تقييمه
            validation_data (Tuple): بيانات التحقق (المدخلات، المخرجات)
            
        الإرجاع:
            Dict[str, float]: مقاييس الأداء
        """
        try:
            x_val, y_val = validation_data
            
            # تقييم النموذج
            evaluation = model.evaluate(x_val, y_val, verbose=0)
            metrics = dict(zip(model.metrics_names, evaluation))
            
            # حساب مقاييس إضافية
            y_pred = model.predict(x_val)
            y_pred_classes = np.argmax(y_pred, axis=1)
            y_true_classes = np.argmax(y_val, axis=1) if len(y_val.shape) > 1 else y_val
            
            additional_metrics = {
                "accuracy": accuracy_score(y_true_classes, y_pred_classes),
                "precision": precision_score(y_true_classes, y_pred_classes, average='weighted'),
                "recall": recall_score(y_true_classes, y_pred_classes, average='weighted'),
                "f1": f1_score(y_true_classes, y_pred_classes, average='weighted')
            }
            
            # دمج المقاييس
            metrics.update(additional_metrics)
            
            # تحديث سجل المقاييس
            if model_name not in self.metrics_history["models"]:
                self.metrics_history["models"][model_name] = {"history": []}
                
            self.metrics_history["models"][model_name]["history"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "metrics": metrics
            })
            
            # حفظ سجل المقاييس
            self._save_metrics_history()
            
            logger.info(f"تم تقييم النموذج {model_name}: الدقة = {metrics.get('accuracy', 0):.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"فشل في تقييم النموذج {model_name}: {e}")
            return {"error": str(e)}

    def needs_retraining(self, model_name: str) -> bool:
        """تحديد ما إذا كان النموذج بحاجة إلى إعادة تدريب
        
        المعاملات:
            model_name (str): اسم النموذج
            
        الإرجاع:
            bool: True إذا كان النموذج بحاجة إلى إعادة تدريب
        """
        if model_name not in self.metrics_history["models"]:
            logger.info(f"النموذج {model_name} ليس له سجل مقاييس، يحتاج إلى تدريب")
            return True
            
        model_history = self.metrics_history["models"][model_name]
        
        # التحقق من وجود سجل مقاييس
        if not model_history.get("history"):
            logger.info(f"النموذج {model_name} ليس له سجل مقاييس، يحتاج إلى تدريب")
            return True
            
        # التحقق من تاريخ آخر تدريب
        last_training = model_history["history"][-1]["timestamp"]
        last_training_date = datetime.datetime.fromisoformat(last_training)
        days_since_last_training = (datetime.datetime.now() - last_training_date).days
        
        if days_since_last_training >= self.retraining_interval:
            logger.info(f"النموذج {model_name} تم تدريبه قبل {days_since_last_training} يومًا، يحتاج إلى إعادة تدريب")
            return True
            
        # التحقق من أداء النموذج
        last_metrics = model_history["history"][-1]["metrics"]
        if last_metrics.get("accuracy", 0) < self.performance_threshold:
            logger.info(f"أداء النموذج {model_name} أقل من الحد الأدنى المطلوب، يحتاج إلى إعادة تدريب")
            return True
            
        # التحقق من وجود بيانات تدريب جديدة
        feedback_count = self._count_new_feedback(model_name)
        if feedback_count > self.config.get("min_feedback_for_retraining", 10):
            logger.info(f"هناك {feedback_count} ملاحظات جديدة للنموذج {model_name}، يحتاج إلى إعادة تدريب")
            return True
            
        logger.info(f"النموذج {model_name} لا يحتاج إلى إعادة تدريب حاليًا")
        return False

    def _count_new_feedback(self, model_name: str) -> int:
        """حساب عدد الملاحظات الجديدة للنموذج"""
        feedback_dir = os.path.join(self.feedback_dir, model_name)
        if not os.path.exists(feedback_dir):
            return 0
            
        # الحصول على تاريخ آخر تدريب
        if model_name in self.metrics_history["models"] and self.metrics_history["models"][model_name].get("history"):
            last_training = self.metrics_history["models"][model_name]["history"][-1]["timestamp"]
            last_training_date = datetime.datetime.fromisoformat(last_training)
        else:
            last_training_date = datetime.datetime.min
            
        # حساب عدد ملفات الملاحظات الجديدة
        count = 0
        for filename in os.listdir(feedback_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(feedback_dir, filename)
                file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mod_time > last_training_date:
                    count += 1
                    
        return count

    def retrain_model(self, model_name: str, model_type: str, 
                     custom_training_params: Optional[Dict] = None) -> Dict:
        """إعادة تدريب النموذج
        
        المعاملات:
            model_name (str): اسم النموذج
            model_type (str): نوع النموذج (disease_detection, nutrient_analysis, etc.)
            custom_training_params (Dict, optional): معلمات تدريب مخصصة
            
        الإرجاع:
            Dict: نتائج التدريب
        """
        try:
            # تحميل بيانات التدريب
            training_data = self._load_training_data(model_name, model_type)
            if not training_data:
                return {"error": "لا توجد بيانات تدريب كافية"}
                
            # تحميل بيانات التحقق
            validation_data = self._load_validation_data(model_name, model_type)
            if not validation_data:
                return {"error": "لا توجد بيانات تحقق كافية"}
                
            # تحميل النموذج الحالي إذا كان موجودًا
            model_path = os.path.join(self.models_dir, model_type, f"{model_name}.h5")
            if os.path.exists(model_path):
                try:
                    model = tf.keras.models.load_model(model_path)
                    logger.info(f"تم تحميل النموذج الحالي: {model_path}")
                except Exception as e:
                    logger.warning(f"فشل في تحميل النموذج الحالي، سيتم إنشاء نموذج جديد: {e}")
                    model = self._create_new_model(model_name, model_type)
            else:
                model = self._create_new_model(model_name, model_type)
                
            # دمج معلمات التدريب
            training_params = self.config.get("default_training_params", {}).copy()
            if custom_training_params:
                training_params.update(custom_training_params)
                
            # تدريب النموذج
            x_train, y_train = training_data
            history = model.fit(
                x_train, y_train,
                validation_data=validation_data,
                epochs=training_params.get("epochs", 10),
                batch_size=training_params.get("batch_size", 32),
                verbose=training_params.get("verbose", 1)
            )
            
            # تقييم النموذج بعد التدريب
            metrics = self.evaluate_model(model_name, model, validation_data)
            
            # حفظ النموذج
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            model.save(model_path)
            logger.info(f"تم حفظ النموذج المعاد تدريبه: {model_path}")
            
            # تحديث سجل التدريب
            training_history = {
                "timestamp": datetime.datetime.now().isoformat(),
                "metrics": metrics,
                "training_params": training_params,
                "history": {key: [float(val) for val in values] for key, values in history.history.items()}
            }
            
            if model_name not in self.metrics_history["models"]:
                self.metrics_history["models"][model_name] = {"history": []}
                
            self.metrics_history["models"][model_name]["last_training"] = training_history
            self._save_metrics_history()
            
            logger.info(f"تم إعادة تدريب النموذج {model_name} بنجاح")
            return {
                "status": "success",
                "model_path": model_path,
                "metrics": metrics,
                "training_history": training_history
            }
            
        except Exception as e:
            logger.error(f"فشل في إعادة تدريب النموذج {model_name}: {e}")
            return {"error": str(e)}

    def _load_training_data(self, model_name: str, model_type: str) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """تحميل بيانات التدريب للنموذج"""
        try:
            # تحميل بيانات التدريب الأساسية
            data_path = os.path.join(self.training_data_dir, model_type, f"{model_name}_data.npz")
            if not os.path.exists(data_path):
                logger.warning(f"ملف بيانات التدريب غير موجود: {data_path}")
                return None
                
            data = np.load(data_path)
            x_train, y_train = data['x'], data['y']
            
            # دمج بيانات الملاحظات إذا كانت موجودة
            feedback_data = self._load_feedback_data(model_name)
            if feedback_data:
                x_feedback, y_feedback = feedback_data
                x_train = np.concatenate([x_train, x_feedback])
                y_train = np.concatenate([y_train, y_feedback])
                logger.info(f"تم دمج {len(x_feedback)} ملاحظات مع بيانات التدريب")
                
            return x_train, y_train
            
        except Exception as e:
            logger.error(f"فشل في تحميل بيانات التدريب للنموذج {model_name}: {e}")
            return None

    def _load_validation_data(self, model_name: str, model_type: str) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """تحميل بيانات التحقق للنموذج"""
        try:
            data_path = os.path.join(self.validation_data_dir, model_type, f"{model_name}_data.npz")
            if not os.path.exists(data_path):
                logger.warning(f"ملف بيانات التحقق غير موجود: {data_path}")
                return None
                
            data = np.load(data_path)
            return data['x'], data['y']
            
        except Exception as e:
            logger.error(f"فشل في تحميل بيانات التحقق للنموذج {model_name}: {e}")
            return None

    def _load_feedback_data(self, model_name: str) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """تحميل بيانات الملاحظات للنموذج"""
        feedback_dir = os.path.join(self.feedback_dir, model_name)
        if not os.path.exists(feedback_dir):
            return None
            
        try:
            # البحث عن ملفات الملاحظات
            feedback_files = [f for f in os.listdir(feedback_dir) if f.endswith('.npz')]
            if not feedback_files:
                return None
                
            # تحميل ودمج بيانات الملاحظات
            x_list, y_list = [], []
            for file_name in feedback_files:
                file_path = os.path.join(feedback_dir, file_name)
                data = np.load(file_path)
                x_list.append(data['x'])
                y_list.append(data['y'])
                
            if x_list and y_list:
                x_feedback = np.concatenate(x_list)
                y_feedback = np.concatenate(y_list)
                return x_feedback, y_feedback
                
            return None
            
        except Exception as e:
            logger.error(f"فشل في تحميل بيانات الملاحظات للنموذج {model_name}: {e}")
            return None

    def _create_new_model(self, model_name: str, model_type: str) -> tf.keras.Model:
        """إنشاء نموذج جديد بناءً على نوع النموذج"""
        logger.info(f"إنشاء نموذج جديد: {model_name} (النوع: {model_type})")
        
        # تحديد بنية النموذج بناءً على نوعه
        if model_type == "disease_detection":
            # مثال لنموذج كشف الأمراض
            input_shape = (224, 224, 3)  # حجم الصورة المدخلة
            num_classes = 10  # عدد فئات الأمراض
            
            model = tf.keras.Sequential([
                tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(num_classes, activation='softmax')
            ])
            
        elif model_type == "nutrient_analysis":
            # مثال لنموذج تحليل نقص العناصر
            input_shape = (299, 299, 3)  # حجم الصورة المدخلة
            num_classes = 8  # عدد فئات نقص العناصر
            
            model = tf.keras.Sequential([
                tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(num_classes, activation='softmax')
            ])
            
        else:
            # نموذج افتراضي
            input_shape = (224, 224, 3)
            num_classes = 5
            
            model = tf.keras.Sequential([
                tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dense(num_classes, activation='softmax')
            ])
            
        # تجميع النموذج
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    def add_feedback(self, model_name: str, input_data: np.ndarray, 
                   correct_output: np.ndarray, metadata: Optional[Dict] = None) -> Dict:
        """إضافة ملاحظة لتحسين النموذج
        
        المعاملات:
            model_name (str): اسم النموذج
            input_data (np.ndarray): بيانات المدخلات
            correct_output (np.ndarray): المخرجات الصحيحة
            metadata (Dict, optional): بيانات وصفية إضافية
            
        الإرجاع:
            Dict: نتيجة إضافة الملاحظة
        """
        try:
            # إنشاء مجلد الملاحظات إذا لم يكن موجودًا
            feedback_dir = os.path.join(self.feedback_dir, model_name)
            os.makedirs(feedback_dir, exist_ok=True)
            
            # إنشاء معرف فريد للملاحظة
            feedback_id = f"{int(time.time())}_{os.urandom(4).hex()}"
            
            # حفظ بيانات الملاحظة
            feedback_path = os.path.join(feedback_dir, f"{feedback_id}.npz")
            np.savez(feedback_path, x=input_data, y=correct_output)
            
            # حفظ البيانات الوصفية إذا كانت موجودة
            if metadata:
                metadata_path = os.path.join(feedback_dir, f"{feedback_id}_metadata.json")
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=4)
                    
            logger.info(f"تم إضافة ملاحظة جديدة للنموذج {model_name}: {feedback_id}")
            
            # التحقق مما إذا كان يجب إعادة تدريب النموذج تلقائيًا
            if self.auto_update and self.needs_retraining(model_name):
                logger.info(f"بدء إعادة تدريب النموذج {model_name} تلقائيًا")
                # تحديد نوع النموذج (يمكن تحسين هذا الجزء)
                model_type = "unknown"
                for type_name in ["disease_detection", "nutrient_analysis"]:
                    if os.path.exists(os.path.join(self.models_dir, type_name, f"{model_name}.h5")):
                        model_type = type_name
                        break
                        
                if model_type != "unknown":
                    self.retrain_model(model_name, model_type)
                    
            return {
                "status": "success",
                "feedback_id": feedback_id,
                "model_name": model_name
            }
            
        except Exception as e:
            logger.error(f"فشل في إضافة ملاحظة للنموذج {model_name}: {e}")
            return {"error": str(e)}

    def get_model_performance_history(self, model_name: str) -> Dict:
        """الحصول على سجل أداء النموذج
        
        المعاملات:
            model_name (str): اسم النموذج
            
        الإرجاع:
            Dict: سجل أداء النموذج
        """
        if model_name not in self.metrics_history["models"]:
            return {"error": f"النموذج {model_name} غير موجود في سجل المقاييس"}
            
        model_history = self.metrics_history["models"][model_name]
        
        # استخراج تطور المقاييس عبر الزمن
        timestamps = []
        accuracy_values = []
        precision_values = []
        recall_values = []
        f1_values = []
        
        for entry in model_history.get("history", []):
            timestamps.append(entry["timestamp"])
            metrics = entry["metrics"]
            accuracy_values.append(metrics.get("accuracy", 0))
            precision_values.append(metrics.get("precision", 0))
            recall_values.append(metrics.get("recall", 0))
            f1_values.append(metrics.get("f1", 0))
            
        return {
            "model_name": model_name,
            "timestamps": timestamps,
            "metrics": {
                "accuracy": accuracy_values,
                "precision": precision_values,
                "recall": recall_values,
                "f1": f1_values
            },
            "last_training": model_history.get("last_training")
        }

    def check_all_models(self) -> Dict[str, List[str]]:
        """التحقق من جميع النماذج وتحديد النماذج التي تحتاج إلى إعادة تدريب
        
        الإرجاع:
            Dict[str, List[str]]: قائمة بالنماذج التي تحتاج إلى إعادة تدريب مصنفة حسب النوع
        """
        models_to_retrain = {}
        
        # البحث عن جميع النماذج في مجلد النماذج
        for model_type in os.listdir(self.models_dir):
            type_dir = os.path.join(self.models_dir, model_type)
            if os.path.isdir(type_dir):
                models_to_retrain[model_type] = []
                
                for model_file in os.listdir(type_dir):
                    if model_file.endswith('.h5'):
                        model_name = os.path.splitext(model_file)[0]
                        
                        if self.needs_retraining(model_name):
                            models_to_retrain[model_type].append(model_name)
                            
        logger.info(f"تم تحديد النماذج التي تحتاج إلى إعادة تدريب: {models_to_retrain}")
        return models_to_retrain

    def retrain_all_needed_models(self) -> Dict[str, Dict[str, str]]:
        """إعادة تدريب جميع النماذج التي تحتاج إلى إعادة تدريب
        
        الإرجاع:
            Dict[str, Dict[str, str]]: نتائج إعادة التدريب
        """
        models_to_retrain = self.check_all_models()
        results = {}
        
        for model_type, model_names in models_to_retrain.items():
            results[model_type] = {}
            
            for model_name in model_names:
                logger.info(f"إعادة تدريب النموذج {model_name} (النوع: {model_type})")
                retrain_result = self.retrain_model(model_name, model_type)
                
                if "error" in retrain_result:
                    results[model_type][model_name] = f"فشل: {retrain_result['error']}"
                else:
                    results[model_type][model_name] = "نجاح"
                    
        return results

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "continuous_learning": {
            "models_dir": "../../models",
            "training_data_dir": "../../data/training",
            "validation_data_dir": "../../data/validation",
            "feedback_dir": "../../data/feedback",
            "metrics_history_file": "../../data/metrics_history.json",
            "performance_threshold": 0.8,
            "retraining_interval_days": 30,
            "auto_update": False,
            "min_feedback_for_retraining": 10,
            "default_training_params": {
                "epochs": 10,
                "batch_size": 32,
                "verbose": 1
            }
        }
    }
    
    # إنشاء مجلدات وهمية
    os.makedirs("../../models/disease_detection", exist_ok=True)
    os.makedirs("../../models/nutrient_analysis", exist_ok=True)
    os.makedirs("../../data/training/disease_detection", exist_ok=True)
    os.makedirs("../../data/validation/disease_detection", exist_ok=True)
    os.makedirs("../../data/feedback", exist_ok=True)
    
    # تهيئة مدير التعلم
    learning_manager = LearningManager(dummy_config)
    
    # إنشاء بيانات تدريب وتحقق وهمية
    print("\n--- إنشاء بيانات وهمية للتجربة ---")
    
    # بيانات تدريب وهمية
    x_train = np.random.rand(100, 224, 224, 3)
    y_train = np.eye(10)[np.random.randint(0, 10, 100)]
    
    train_data_path = os.path.join(dummy_config["continuous_learning"]["training_data_dir"], 
                                 "disease_detection", "fungal_disease_model_data.npz")
    os.makedirs(os.path.dirname(train_data_path), exist_ok=True)
    np.savez(train_data_path, x=x_train, y=y_train)
    print(f"تم إنشاء بيانات تدريب وهمية: {train_data_path}")
    
    # بيانات تحقق وهمية
    x_val = np.random.rand(20, 224, 224, 3)
    y_val = np.eye(10)[np.random.randint(0, 10, 20)]
    
    val_data_path = os.path.join(dummy_config["continuous_learning"]["validation_data_dir"], 
                               "disease_detection", "fungal_disease_model_data.npz")
    os.makedirs(os.path.dirname(val_data_path), exist_ok=True)
    np.savez(val_data_path, x=x_val, y=y_val)
    print(f"تم إنشاء بيانات تحقق وهمية: {val_data_path}")
    
    # تدريب نموذج وهمي
    print("\n--- تدريب نموذج وهمي ---")
    model_name = "fungal_disease_model"
    model_type = "disease_detection"
    
    # تعديل معلمات التدريب للتجربة السريعة
    custom_params = {"epochs": 2, "batch_size": 32, "verbose": 1}
    
    training_result = learning_manager.retrain_model(model_name, model_type, custom_params)
    if "error" in training_result:
        print(f"فشل في تدريب النموذج: {training_result['error']}")
    else:
        print(f"تم تدريب النموذج بنجاح: {training_result['model_path']}")
        print(f"الدقة: {training_result['metrics'].get('accuracy', 0):.4f}")
    
    # إضافة ملاحظة
    print("\n--- إضافة ملاحظة ---")
    feedback_input = np.random.rand(1, 224, 224, 3)
    feedback_output = np.eye(10)[np.random.randint(0, 10, 1)]
    
    feedback_result = learning_manager.add_feedback(
        model_name,
        feedback_input,
        feedback_output,
        {"source": "user_correction", "confidence": 0.9}
    )
    
    print(f"نتيجة إضافة الملاحظة: {feedback_result}")
    
    # التحقق من أداء النموذج
    print("\n--- التحقق من أداء النموذج ---")
    performance = learning_manager.get_model_performance_history(model_name)
    
    print(f"عدد مرات تدريب النموذج: {len(performance.get('timestamps', []))}")
    if performance.get('metrics', {}).get('accuracy'):
        print(f"تطور الدقة: {performance['metrics']['accuracy']}")
    
    # التحقق من الحاجة لإعادة التدريب
    print("\n--- التحقق من الحاجة لإعادة التدريب ---")
    needs_retraining = learning_manager.needs_retraining(model_name)
    print(f"هل النموذج {model_name} يحتاج إلى إعادة تدريب؟ {needs_retraining}")
    
    # التحقق من جميع النماذج
    print("\n--- التحقق من جميع النماذج ---")
    models_to_retrain = learning_manager.check_all_models()
    print(f"النماذج التي تحتاج إلى إعادة تدريب: {models_to_retrain}")
    
    # تنظيف الملفات الوهمية (اختياري)
    # import shutil
    # shutil.rmtree("../../models")
    # shutil.rmtree("../../data")
    # print("\nتم حذف الملفات الوهمية")
