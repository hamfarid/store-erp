# File: /home/ubuntu/ai_web_organized/src/modules/disease_diagnosis/diagnosis_engine_enhanced.py
"""
from flask import g
محرك تشخيص الأمراض النباتية المحسن
يوفر هذا الملف محرك استدلال متقدم لتشخيص الأمراض النباتية باستخدام قاعدة المعرفة
مع دعم التعلم المستمر وتكامل مع نظام معالجة الصور
"""

import os
import json
import logging
from datetime import datetime
# import numpy as np  # Removed: unused import
from typing import Dict, List, Any, Optional, Tuple
from .disease_knowledge_base import DiseaseKnowledgeBase

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DiagnosisEngineEnhanced:
    """محرك تشخيص الأمراض النباتية المحسن مع دعم التعلم المستمر"""

    def __init__(self, knowledge_base_path=None, confidence_threshold=0.6, learning_rate=0.1):
        """
        تهيئة محرك التشخيص المحسن

        المعلمات:
            knowledge_base_path (str, optional): مسار ملف قاعدة المعرفة
            confidence_threshold (float, optional): عتبة الثقة للتشخيص (0-1)
            learning_rate (float, optional): معدل التعلم لتحديث النموذج (0-1)
        """
        # تحميل قاعدة المعرفة
        self.knowledge_base = DiseaseKnowledgeBase(knowledge_base_path)

        # مسار حفظ نتائج التشخيص
        self.results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
        os.makedirs(self.results_dir, exist_ok=True)

        # مسار حفظ نماذج التعلم
        self.models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
        os.makedirs(self.models_dir, exist_ok=True)

        # سجل التشخيصات السابقة
        self.diagnosis_history = []

        # إعدادات المحرك
        self.confidence_threshold = confidence_threshold
        self.learning_rate = learning_rate

        # أوزان الميزات المختلفة في التشخيص
        self.feature_weights = {
            "symptoms": 0.6,
            "image": 0.25,
            "environmental": 0.15
        }

        # تحميل نماذج التعلم إذا كانت موجودة
        self.symptom_weights = self._load_symptom_weights()

        logger.info("تم تهيئة محرك تشخيص الأمراض النباتية المحسن")

    def diagnose(self, symptoms: List[str], crop_type: str,
                 image_features: Optional[Dict[str, Any]] = None,
                 environmental_conditions: Optional[Dict[str, Any]] = None,
                 image_path: Optional[str] = None) -> Dict[str, Any]:
        """
        تشخيص المرض بناءً على الأعراض ونوع المحصول وميزات الصورة والظروف البيئية

        المعلمات:
            symptoms (List[str]): قائمة الأعراض المرصودة
            crop_type (str): نوع المحصول
            image_features (Dict[str, Any], optional): ميزات مستخرجة من الصورة
            environmental_conditions (Dict[str, Any], optional): الظروف البيئية
            image_path (str, optional): مسار صورة النبات المصاب

        العائد:
            Dict[str, Any]: نتيجة التشخيص
        """
        try:
            logger.info(f"بدء تشخيص المرض للمحصول: {crop_type}")

            # التحقق من صحة البيانات المدخلة
            validation_result = self._validate_input_data(symptoms, crop_type, image_features, environmental_conditions)
            if not validation_result["valid"]:
                logger.error(f"خطأ في البيانات المدخلة: {validation_result['error']}")
                return {
                    "success": False,
                    "error": validation_result["error"],
                    "timestamp": datetime.now().isoformat()
                }

            # الحصول على الأمراض المحتملة من قاعدة المعرفة
            possible_diseases = self.knowledge_base.get_diseases_by_crop(crop_type)

            if not possible_diseases:
                logger.warning(f"لم يتم العثور على أمراض مسجلة للمحصول: {crop_type}")
                return {
                    "success": False,
                    "error": f"لم يتم العثور على أمراض مسجلة للمحصول: {crop_type}",
                    "timestamp": datetime.now().isoformat()
                }

            # معالجة الصورة إذا كانت متوفرة ولم يتم توفير ميزات الصورة
            if image_path and not image_features:
                image_features = self._process_image(image_path)

            # حساب درجة التطابق لكل مرض
            disease_scores = []
            detailed_scores = {}

            for disease in possible_diseases:
                score, score_details = self._calculate_match_score(
                    disease, symptoms, image_features, environmental_conditions
                )

                disease_scores.append({
                    "disease": disease,
                    "score": score,
                    "score_details": score_details
                })

                detailed_scores[disease["name"]] = score_details

            # ترتيب الأمراض حسب درجة التطابق (من الأعلى إلى الأدنى)
            disease_scores.sort(key=lambda x: x["score"], reverse=True)

            # تحديد الأمراض المحتملة (التي تتجاوز عتبة الثقة)
            probable_diseases = [ds for ds in disease_scores if ds["score"] >= self.confidence_threshold]

            # إعداد نتيجة التشخيص
            diagnosis_result = {
                "success": True,
                "crop_type": crop_type,
                "symptoms": symptoms,
                "timestamp": datetime.now().isoformat(),
                "probable_diseases": probable_diseases,
                "all_diseases": disease_scores,
                "detailed_scores": detailed_scores,
                "confidence_threshold": self.confidence_threshold,
                "recommendations": self._generate_recommendations(probable_diseases)
            }

            # إضافة معلومات إضافية إذا كانت متوفرة
            if image_features:
                diagnosis_result["image_analysis"] = {
                    "features": image_features,
                    "confidence": self._calculate_image_confidence(image_features)
                }

            if environmental_conditions:
                diagnosis_result["environmental_analysis"] = {
                    "conditions": environmental_conditions,
                    "impact": self._analyze_environmental_impact(environmental_conditions, probable_diseases)
                }

            # حفظ نتيجة التشخيص
            self._save_diagnosis_result(diagnosis_result)

            # إضافة التشخيص إلى السجل
            self.diagnosis_history.append({
                "timestamp": diagnosis_result["timestamp"],
                "crop_type": crop_type,
                "result": "success" if probable_diseases else "no_match"
            })

            logger.info(f"تم الانتهاء من التشخيص للمحصول: {crop_type}")

            return diagnosis_result

        except Exception as e:
            logger.error(f"خطأ أثناء تشخيص المرض: {str(e)}")
            return {
                "success": False,
                "error": f"خطأ أثناء تشخيص المرض: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def _validate_input_data(self, symptoms: List[str], crop_type: str,
                             image_features: Optional[Dict[str, Any]],
                             environmental_conditions: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        التحقق من صحة البيانات المدخلة

        المعلمات:
            symptoms (List[str]): قائمة الأعراض المرصودة
            crop_type (str): نوع المحصول
            image_features (Dict[str, Any], optional): ميزات مستخرجة من الصورة
            environmental_conditions (Dict[str, Any], optional): الظروف البيئية

        العائد:
            Dict[str, Any]: نتيجة التحقق
        """
        # التحقق من وجود الأعراض ونوع المحصول
        if not symptoms:
            return {"valid": False, "error": "الأعراض غير محددة"}

        if not crop_type:
            return {"valid": False, "error": "نوع المحصول غير محدد"}

        # التحقق من وجود المحصول في قاعدة المعرفة
        if crop_type not in self.knowledge_base.crops:
            return {"valid": False, "error": f"المحصول '{crop_type}' غير موجود في قاعدة المعرفة"}

        # التحقق من صحة الظروف البيئية إذا كانت متوفرة
        if environmental_conditions:
            if not isinstance(environmental_conditions, dict):
                return {"valid": False, "error": "الظروف البيئية يجب أن تكون على شكل قاموس"}

            # التحقق من نطاقات القيم
            if "temperature" in environmental_conditions:
                temp = environmental_conditions["temperature"]
                if not isinstance(temp, (int, float)) or temp < -50 or temp > 60:
                    return {"valid": False, "error": "درجة الحرارة خارج النطاق المقبول (-50 إلى 60 درجة مئوية)"}

            if "humidity" in environmental_conditions:
                humidity = environmental_conditions["humidity"]
                if not isinstance(humidity, (int, float)) or humidity < 0 or humidity > 100:
                    return {"valid": False, "error": "الرطوبة خارج النطاق المقبول (0 إلى 100%)"}

        # التحقق من صحة ميزات الصورة إذا كانت متوفرة
        if image_features and not isinstance(image_features, dict):
            return {"valid": False, "error": "ميزات الصورة يجب أن تكون على شكل قاموس"}

        return {"valid": True}

    def _calculate_match_score(self, disease: Dict[str, Any], symptoms: List[str],
                               image_features: Optional[Dict[str, Any]],
                               environmental_conditions: Optional[Dict[str, Any]]) -> Tuple[float, Dict[str, Any]]:
        """
        حساب درجة تطابق المرض مع الأعراض المرصودة

        المعلمات:
            disease (Dict[str, Any]): معلومات المرض
            symptoms (List[str]): قائمة الأعراض المرصودة
            image_features (Dict[str, Any], optional): ميزات مستخرجة من الصورة
            environmental_conditions (Dict[str, Any], optional): الظروف البيئية

        العائد:
            Tuple[float, Dict[str, Any]]: درجة التطابق (0-1) وتفاصيل الحساب
        """
        try:
            score_details = {}

            # حساب درجة تطابق الأعراض
            symptom_score, symptom_details = self._calculate_symptom_match(disease, symptoms)
            score_details["symptom_score"] = symptom_score
            score_details["symptom_details"] = symptom_details

            # حساب درجة تطابق الصورة
            image_score = 0.0
            if image_features and "image_patterns" in disease:
                image_score, image_details = self._calculate_image_match(disease["image_patterns"], image_features)
                score_details["image_score"] = image_score
                score_details["image_details"] = image_details

            # حساب درجة تطابق الظروف البيئية
            env_score = 0.0
            if environmental_conditions and "conditions" in disease:
                env_score, env_details = self._calculate_environmental_match(disease["conditions"], environmental_conditions)
                score_details["environmental_score"] = env_score
                score_details["environmental_details"] = env_details

            # حساب الدرجة النهائية باستخدام الأوزان
            final_score = (
                self.feature_weights["symptoms"] * symptom_score
                + self.feature_weights["image"] * image_score
                + self.feature_weights["environmental"] * env_score
            )

            score_details["final_score"] = final_score
            score_details["weights"] = self.feature_weights

            return final_score, score_details

        except Exception as e:
            logger.error(f"خطأ أثناء حساب درجة التطابق: {str(e)}")
            return 0.0, {"error": str(e)}

    def _calculate_symptom_match(self, disease: Dict[str, Any], symptoms: List[str]) -> Tuple[float, Dict[str, Any]]:
        """
        حساب درجة تطابق الأعراض

        المعلمات:
            disease (Dict[str, Any]): معلومات المرض
            symptoms (List[str]): قائمة الأعراض المرصودة

        العائد:
            Tuple[float, Dict[str, Any]]: درجة التطابق (0-1) وتفاصيل الحساب
        """
        # الحصول على أعراض المرض
        disease_symptoms = disease.get("symptoms", [])

        if not disease_symptoms:
            return 0.0, {"matching_symptoms": [], "missing_symptoms": [], "extra_symptoms": symptoms}

        # حساب الأعراض المتطابقة والمفقودة والإضافية
        matching_symptoms = []
        symptom_weights = {}

        for symptom in symptoms:
            best_match = None
            best_score = 0.0

            for disease_symptom in disease_symptoms:
                # حساب درجة تشابه النصوص
                similarity = self._calculate_text_similarity(symptom, disease_symptom)

                if similarity > 0.7 and similarity > best_score:  # عتبة التشابه
                    best_match = disease_symptom
                    best_score = similarity

            if best_match:
                matching_symptoms.append({
                    "input_symptom": symptom,
                    "matched_symptom": best_match,
                    "similarity": best_score
                })

                # استخدام أوزان الأعراض المخزنة إذا كانت متوفرة
                symptom_weight = self.symptom_weights.get(best_match, 1.0)
                symptom_weights[best_match] = symptom_weight

        # حساب الأعراض المفقودة والإضافية
        matched_disease_symptoms = [match["matched_symptom"] for match in matching_symptoms]
        missing_symptoms = [s for s in disease_symptoms if s not in matched_disease_symptoms]
        extra_symptoms = [s for s in symptoms if not any(m["input_symptom"] == s for m in matching_symptoms)]

        # حساب درجة التطابق الإجمالية
        if not disease_symptoms:
            return 0.0, {
                "matching_symptoms": matching_symptoms,
                "missing_symptoms": missing_symptoms,
                "extra_symptoms": extra_symptoms
            }

        # حساب مجموع الأوزان للأعراض المتطابقة
        weighted_matches = sum(symptom_weights.get(match["matched_symptom"], 1.0) for match in matching_symptoms)
        total_weight = sum(self.symptom_weights.get(s, 1.0) for s in disease_symptoms)

        # حساب درجة التطابق مع مراعاة الأعراض الإضافية
        if total_weight > 0:
            match_score = weighted_matches / total_weight

            # خصم للأعراض الإضافية (غير المتوقعة)
            extra_penalty = len(extra_symptoms) * 0.1
            match_score = max(0.0, match_score - extra_penalty)
        else:
            match_score = 0.0

        return match_score, {
            "matching_symptoms": matching_symptoms,
            "missing_symptoms": missing_symptoms,
            "extra_symptoms": extra_symptoms,
            "symptom_weights": symptom_weights,
            "weighted_matches": weighted_matches,
            "total_weight": total_weight,
            "extra_penalty": len(extra_symptoms) * 0.1 if len(extra_symptoms) > 0 else 0.0
        }

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        حساب درجة تشابه النصوص

        المعلمات:
            text1 (str): النص الأول
            text2 (str): النص الثاني

        العائد:
            float: درجة التشابه (0-1)
        """
        # تنفيذ بسيط لحساب تشابه النصوص
        # في التطبيق الحقيقي، يمكن استخدام خوارزميات أكثر تعقيدًا مثل Levenshtein أو Jaccard أو نماذج لغوية

        # تحويل النصوص إلى أحرف صغيرة وتقسيمها إلى كلمات
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        # حساب تشابه جاكارد
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        if union == 0:
            return 0.0

        return intersection / union

    def _calculate_image_match(self, disease_patterns: Dict[str, Any],
                               image_features: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        حساب درجة تطابق أنماط الصورة مع ميزات الصورة المستخرجة

        المعلمات:
            disease_patterns (Dict[str, Any]): أنماط الصورة للمرض
            image_features (Dict[str, Any]): ميزات الصورة المستخرجة

        العائد:
            Tuple[float, Dict[str, Any]]: درجة التطابق (0-1) وتفاصيل الحساب
        """
        try:
            match_details = {}

            # في التطبيق الحقيقي، سيتم استخدام خوارزميات أكثر تعقيدًا لمطابقة الصور
            # هذه محاكاة بسيطة لعملية المطابقة

            # مطابقة ميزات اللون
            color_score = 0.0
            if "color_histogram" in image_features and "color_patterns" in disease_patterns:
                # حساب تشابه هيستوجرام الألوان
                color_score = 0.8  # قيمة افتراضية للمحاكاة
                match_details["color_match"] = color_score

            # مطابقة ميزات الشكل
            shape_score = 0.0
            if "shape_features" in image_features and "shape_patterns" in disease_patterns:
                # حساب تشابه ميزات الشكل
                shape_score = 0.7  # قيمة افتراضية للمحاكاة
                match_details["shape_match"] = shape_score

            # مطابقة ميزات النسيج
            texture_score = 0.0
            if "texture_features" in image_features and "texture_patterns" in disease_patterns:
                # حساب تشابه ميزات النسيج
                texture_score = 0.75  # قيمة افتراضية للمحاكاة
                match_details["texture_match"] = texture_score

            # حساب الدرجة الإجمالية
            total_score = 0.0
            count = 0

            if "color_match" in match_details:
                total_score += match_details["color_match"]
                count += 1

            if "shape_match" in match_details:
                total_score += match_details["shape_match"]
                count += 1

            if "texture_match" in match_details:
                total_score += match_details["texture_match"]
                count += 1

            if count > 0:
                final_score = total_score / count
            else:
                final_score = 0.5  # قيمة افتراضية إذا لم تتوفر ميزات للمطابقة

            match_details["final_score"] = final_score

            return final_score, match_details

        except Exception as e:
            logger.error(f"خطأ أثناء حساب تطابق الصورة: {str(e)}")
            return 0.0, {"error": str(e)}

    def _calculate_environmental_match(self, disease_conditions: Dict[str, Any],
                                       environmental_conditions: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        حساب درجة تطابق العوامل البيئية مع الظروف البيئية الحالية

        المعلمات:
            disease_conditions (Dict[str, Any]): الظروف البيئية المفضلة للمرض
            environmental_conditions (Dict[str, Any]): الظروف البيئية الحالية

        العائد:
            Tuple[float, Dict[str, Any]]: درجة التطابق (0-1) وتفاصيل الحساب
        """
        try:
            match_details = {}
            matches = 0
            total_factors = 0

            # التحقق من درجة الحرارة
            if "temperature" in disease_conditions and "temperature" in environmental_conditions:
                total_factors += 1
                disease_temp = disease_conditions["temperature"]
                actual_temp = environmental_conditions["temperature"]

                temp_match = 0.0

                # التحقق من نطاق درجة الحرارة
                if isinstance(disease_temp, dict) and "min" in disease_temp and "max" in disease_temp:
                    min_temp = disease_temp["min"]
                    max_temp = disease_temp["max"]

                    if min_temp <= actual_temp <= max_temp:
                        temp_match = 1.0
                    else:
                        # حساب درجة القرب من النطاق
                        if actual_temp < min_temp:
                            temp_match = max(0, 1 - (min_temp - actual_temp) / 10)
                        else:  # actual_temp > max_temp
                            temp_match = max(0, 1 - (actual_temp - max_temp) / 10)

                matches += temp_match
                match_details["temperature_match"] = temp_match

            # التحقق من الرطوبة
            if "humidity" in disease_conditions and "humidity" in environmental_conditions:
                total_factors += 1
                disease_humidity = disease_conditions["humidity"]
                actual_humidity = environmental_conditions["humidity"]

                humidity_match = 0.0

                # التحقق من نطاق الرطوبة
                if isinstance(disease_humidity, dict) and "min" in disease_humidity and "max" in disease_humidity:
                    min_humidity = disease_humidity["min"]
                    max_humidity = disease_humidity["max"]

                    if min_humidity <= actual_humidity <= max_humidity:
                        humidity_match = 1.0
                    else:
                        # حساب درجة القرب من النطاق
                        if actual_humidity < min_humidity:
                            humidity_match = max(0, 1 - (min_humidity - actual_humidity) / 20)
                        else:  # actual_humidity > max_humidity
                            humidity_match = max(0, 1 - (actual_humidity - max_humidity) / 20)

                matches += humidity_match
                match_details["humidity_match"] = humidity_match

            # التحقق من عوامل أخرى
            for factor in ["rainfall", "soil_ph", "light"]:
                if factor in disease_conditions and factor in environmental_conditions:
                    total_factors += 1
                    disease_value = disease_conditions[factor]
                    actual_value = environmental_conditions[factor]

                    factor_match = 0.0

                    # التحقق من نطاق القيمة
                    if isinstance(disease_value, dict) and "min" in disease_value and "max" in disease_value:
                        min_value = disease_value["min"]
                        max_value = disease_value["max"]

                        if min_value <= actual_value <= max_value:
                            factor_match = 1.0
                        else:
                            # حساب درجة القرب من النطاق
                            range_width = max_value - min_value
                            if range_width > 0:
                                if actual_value < min_value:
                                    factor_match = max(0, 1 - (min_value - actual_value) / range_width)
                                else:  # actual_value > max_value
                                    factor_match = max(0, 1 - (actual_value - max_value) / range_width)

                    matches += factor_match
                    match_details[f"{factor}_match"] = factor_match

            # حساب درجة التطابق الإجمالية
            if total_factors > 0:
                final_score = matches / total_factors
            else:
                final_score = 0.0

            match_details["final_score"] = final_score
            match_details["total_factors"] = total_factors
            match_details["matches"] = matches

            return final_score, match_details

        except Exception as e:
            logger.error(f"خطأ أثناء حساب تطابق العوامل البيئية: {str(e)}")
            return 0.0, {"error": str(e)}

    def _calculate_image_confidence(self, image_features: Dict[str, Any]) -> float:
        """
        حساب مستوى الثقة في تحليل الصورة

        المعلمات:
            image_features (Dict[str, Any]): ميزات الصورة المستخرجة

        العائد:
            float: مستوى الثقة (0-1)
        """
        try:
            # في التطبيق الحقيقي، سيتم استخدام نموذج أكثر تعقيدًا لحساب مستوى الثقة

            # التحقق من جودة الصورة
            if "quality_score" in image_features:
                quality_score = min(1.0, max(0.0, image_features["quality_score"]))
            else:
                quality_score = 0.7  # قيمة افتراضية

            # التحقق من وضوح الصورة
            if "clarity_score" in image_features:
                clarity_score = min(1.0, max(0.0, image_features["clarity_score"]))
            else:
                clarity_score = 0.7  # قيمة افتراضية

            # التحقق من تغطية الصورة للنبات
            if "coverage_score" in image_features:
                coverage_score = min(1.0, max(0.0, image_features["coverage_score"]))
            else:
                coverage_score = 0.7  # قيمة افتراضية

            # حساب مستوى الثقة الإجمالي
            confidence = (quality_score * 0.4 + clarity_score * 0.3 + coverage_score * 0.3)

            return confidence

        except Exception as e:
            logger.error(f"خطأ أثناء حساب مستوى الثقة في الصورة: {str(e)}")
            return 0.5

    def _analyze_environmental_impact(self, environmental_conditions: Dict[str, Any],
                                      probable_diseases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        تحليل تأثير الظروف البيئية على الأمراض المحتملة

        المعلمات:
            environmental_conditions (Dict[str, Any]): الظروف البيئية الحالية
            probable_diseases (List[Dict[str, Any]]): قائمة الأمراض المحتملة مع درجات التطابق

        العائد:
            Dict[str, Any]: تحليل تأثير الظروف البيئية
        """
        try:
            impact_analysis = {
                "favorable_conditions": [],
                "unfavorable_conditions": [],
                "disease_specific_impacts": [],
                "overall_impact": "neutral"
            }

            # التحقق من تأثير درجة الحرارة
            if "temperature" in environmental_conditions:
                temp = environmental_conditions["temperature"]

                if temp > 30:
                    impact_analysis["favorable_conditions"].append({
                        "condition": "درجة الحرارة المرتفعة",
                        "value": temp,
                        "impact": "تساعد على انتشار بعض الأمراض الفطرية مثل البياض الدقيقي"
                    })
                elif temp < 15:
                    impact_analysis["unfavorable_conditions"].append({
                        "condition": "درجة الحرارة المنخفضة",
                        "value": temp,
                        "impact": "تبطئ من تطور معظم الأمراض"
                    })

            # التحقق من تأثير الرطوبة
            if "humidity" in environmental_conditions:
                humidity = environmental_conditions["humidity"]

                if humidity > 70:
                    impact_analysis["favorable_conditions"].append({
                        "condition": "الرطوبة العالية",
                        "value": humidity,
                        "impact": "تساعد على انتشار الأمراض الفطرية والبكتيرية مثل اللفحة المتأخرة والبياض الزغبي"
                    })
                elif humidity < 40:
                    impact_analysis["unfavorable_conditions"].append({
                        "condition": "الرطوبة المنخفضة",
                        "value": humidity,
                        "impact": "تحد من انتشار معظم الأمراض الفطرية"
                    })

            # تحليل تأثير الظروف البيئية على كل مرض محتمل
            for disease_score in probable_diseases:
                disease = disease_score["disease"]
                disease_name = disease["name"]

                disease_impact = {
                    "disease_name": disease_name,
                    "favorable_factors": [],
                    "unfavorable_factors": []
                }

                # التحقق من الظروف المفضلة للمرض
                if "conditions" in disease:
                    disease_conditions = disease["conditions"]

                    # التحقق من درجة الحرارة
                    if "temperature" in disease_conditions and "temperature" in environmental_conditions:
                        disease_temp = disease_conditions["temperature"]
                        actual_temp = environmental_conditions["temperature"]

                        if isinstance(disease_temp, dict) and "min" in disease_temp and "max" in disease_temp:
                            min_temp = disease_temp["min"]
                            max_temp = disease_temp["max"]

                            if min_temp <= actual_temp <= max_temp:
                                disease_impact["favorable_factors"].append({
                                    "factor": "درجة الحرارة",
                                    "value": actual_temp,
                                    "optimal_range": f"{min_temp} - {max_temp}",
                                    "impact": "مناسبة لتطور المرض"
                                })
                            else:
                                disease_impact["unfavorable_factors"].append({
                                    "factor": "درجة الحرارة",
                                    "value": actual_temp,
                                    "optimal_range": f"{min_temp} - {max_temp}",
                                    "impact": "غير مناسبة لتطور المرض"
                                })

                    # التحقق من الرطوبة
                    if "humidity" in disease_conditions and "humidity" in environmental_conditions:
                        disease_humidity = disease_conditions["humidity"]
                        actual_humidity = environmental_conditions["humidity"]

                        if isinstance(disease_humidity, dict) and "min" in disease_humidity and "max" in disease_humidity:
                            min_humidity = disease_humidity["min"]
                            max_humidity = disease_humidity["max"]

                            if min_humidity <= actual_humidity <= max_humidity:
                                disease_impact["favorable_factors"].append({
                                    "factor": "الرطوبة",
                                    "value": actual_humidity,
                                    "optimal_range": f"{min_humidity} - {max_humidity}",
                                    "impact": "مناسبة لتطور المرض"
                                })
                            else:
                                disease_impact["unfavorable_factors"].append({
                                    "factor": "الرطوبة",
                                    "value": actual_humidity,
                                    "optimal_range": f"{min_humidity} - {max_humidity}",
                                    "impact": "غير مناسبة لتطور المرض"
                                })

                impact_analysis["disease_specific_impacts"].append(disease_impact)

            # تحديد التأثير العام
            if len(impact_analysis["favorable_conditions"]) > len(impact_analysis["unfavorable_conditions"]):
                impact_analysis["overall_impact"] = "favorable"
            elif len(impact_analysis["favorable_conditions"]) < len(impact_analysis["unfavorable_conditions"]):
                impact_analysis["overall_impact"] = "unfavorable"

            return impact_analysis

        except Exception as e:
            logger.error(f"خطأ أثناء تحليل تأثير الظروف البيئية: {str(e)}")
            return {
                "favorable_conditions": [],
                "unfavorable_conditions": [],
                "disease_specific_impacts": [],
                "overall_impact": "unknown",
                "error": str(e)
            }

    def _generate_recommendations(self, probable_diseases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        توليد توصيات بناءً على الأمراض المحتملة

        المعلمات:
            probable_diseases (List[Dict[str, Any]]): قائمة الأمراض المحتملة مع درجات التطابق

        العائد:
            Dict[str, Any]: توصيات للمزارع
        """
        try:
            if not probable_diseases:
                return {
                    "general": [
                        "لم يتم تحديد أي مرض محتمل. يرجى التقاط صور أوضح أو تقديم مزيد من المعلومات."
                    ],
                    "preventive": [
                        "الحفاظ على نظافة الحقل وإزالة النباتات المصابة",
                        "تطبيق برنامج وقائي للأمراض الشائعة في المنطقة",
                        "مراقبة النباتات بانتظام للكشف المبكر عن أي أعراض"
                    ]
                }

            # الحصول على المرض الأكثر احتمالاً
            top_disease = probable_diseases[0]["disease"]
            top_score = probable_diseases[0]["score"]

            # توليد توصيات علاجية
            treatment_recommendations = []
            if "treatments" in top_disease:
                treatment_recommendations = top_disease["treatments"]

            # توليد توصيات وقائية
            preventive_recommendations = []
            if "prevention" in top_disease:
                preventive_recommendations = top_disease["prevention"]
            else:
                preventive_recommendations = [
                    "إزالة النباتات المصابة وحرقها لمنع انتشار المرض",
                    "تطبيق برنامج رش وقائي منتظم",
                    "تحسين التهوية وتقليل الرطوبة حول النباتات"
                ]

            # توليد توصيات عامة
            general_recommendations = [
                f"المرض المحتمل: {top_disease['name']} (درجة التطابق: {top_score:.2f})"
            ]

            if "scientific_name" in top_disease:
                general_recommendations.append(f"الاسم العلمي: {top_disease['scientific_name']}")

            if "description" in top_disease:
                general_recommendations.append(f"وصف المرض: {top_disease['description']}")

            # إضافة توصيات للأمراض الأخرى المحتملة
            other_diseases = []
            if len(probable_diseases) > 1:
                for i in range(1, min(3, len(probable_diseases))):
                    other_disease = probable_diseases[i]["disease"]
                    other_score = probable_diseases[i]["score"]
                    other_diseases.append(f"{other_disease['name']} (درجة التطابق: {other_score:.2f})")

                if other_diseases:
                    general_recommendations.append(f"أمراض أخرى محتملة: {', '.join(other_diseases)}")

            # إضافة توصيات للمتابعة
            follow_up_recommendations = [
                "متابعة تطور الأعراض ومراقبة النباتات المجاورة",
                "إعادة التقييم بعد تطبيق العلاج للتأكد من فعاليته",
                "استشارة خبير زراعي إذا استمرت الأعراض أو تفاقمت"
            ]

            return {
                "general": general_recommendations,
                "treatment": treatment_recommendations,
                "preventive": preventive_recommendations,
                "follow_up": follow_up_recommendations
            }

        except Exception as e:
            logger.error(f"خطأ أثناء توليد التوصيات: {str(e)}")
            return {
                "general": [
                    "حدث خطأ أثناء توليد التوصيات. يرجى المحاولة مرة أخرى."
                ],
                "error": str(e)
            }

    def _process_image(self, image_path: str) -> Dict[str, Any]:
        """
        معالجة صورة النبات المصاب واستخراج الميزات

        المعلمات:
            image_path (str): مسار الصورة

        العائد:
            Dict[str, Any]: ميزات الصورة المستخرجة
        """
        try:
            # في التطبيق الحقيقي، سيتم استخدام مكتبات معالجة الصور مثل OpenCV أو PIL
            # وخوارزميات استخراج الميزات والتعلم الآلي

            # هذه محاكاة بسيطة لعملية معالجة الصورة
            logger.info(f"معالجة الصورة: {image_path}")

            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                logger.error(f"الصورة غير موجودة: {image_path}")
                return {}

            # محاكاة استخراج ميزات الصورة
            image_features = {
                "quality_score": 0.85,
                "clarity_score": 0.8,
                "coverage_score": 0.9,
                "color_histogram": {
                    "red": [0.1, 0.2, 0.3, 0.4],
                    "green": [0.2, 0.3, 0.4, 0.1],
                    "blue": [0.3, 0.4, 0.1, 0.2]
                },
                "texture_features": {
                    "contrast": 0.7,
                    "homogeneity": 0.6,
                    "energy": 0.5,
                    "correlation": 0.8
                },
                "shape_features": {
                    "area": 0.6,
                    "perimeter": 0.7,
                    "circularity": 0.4,
                    "elongation": 0.5
                }
            }

            return image_features

        except Exception as e:
            logger.error(f"خطأ أثناء معالجة الصورة: {str(e)}")
            return {}

    def _save_diagnosis_result(self, diagnosis_result: Dict[str, Any]) -> None:
        """
        حفظ نتيجة التشخيص

        المعلمات:
            diagnosis_result (Dict[str, Any]): نتيجة التشخيص
        """
        try:
            # إنشاء اسم ملف فريد
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            crop_type = diagnosis_result.get("crop_type", "unknown")
            filename = f"diagnosis_{crop_type}_{timestamp}.json"
            file_path = os.path.join(self.results_dir, filename)

            # حفظ النتيجة في ملف JSON
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(diagnosis_result, f, ensure_ascii=False, indent=2)

            logger.info(f"تم حفظ نتيجة التشخيص في: {file_path}")

        except Exception as e:
            logger.error(f"خطأ أثناء حفظ نتيجة التشخيص: {str(e)}")

    def _load_symptom_weights(self) -> Dict[str, float]:
        """
        تحميل أوزان الأعراض من ملف

        العائد:
            Dict[str, float]: أوزان الأعراض
        """
        try:
            weights_file = os.path.join(self.models_dir, "symptom_weights.json")

            if os.path.exists(weights_file):
                with open(weights_file, "r", encoding="utf-8") as f:
                    weights = json.load(f)

                logger.info(f"تم تحميل أوزان الأعراض من: {weights_file}")
                return weights
            else:
                logger.info("لم يتم العثور على ملف أوزان الأعراض. سيتم استخدام الأوزان الافتراضية.")
                return {}

        except Exception as e:
            logger.error(f"خطأ أثناء تحميل أوزان الأعراض: {str(e)}")
            return {}

    def _save_symptom_weights(self) -> None:
        """
        حفظ أوزان الأعراض في ملف
        """
        try:
            weights_file = os.path.join(self.models_dir, "symptom_weights.json")

            with open(weights_file, "w", encoding="utf-8") as f:
                json.dump(self.symptom_weights, f, ensure_ascii=False, indent=2)

            logger.info(f"تم حفظ أوزان الأعراض في: {weights_file}")

        except Exception as e:
            logger.error(f"خطأ أثناء حفظ أوزان الأعراض: {str(e)}")

    def update_model_from_feedback(self, diagnosis_id: str, feedback: Dict[str, Any]) -> bool:
        """
        تحديث النموذج بناءً على التغذية الراجعة من المستخدم

        المعلمات:
            diagnosis_id (str): معرف التشخيص
            feedback (Dict[str, Any]): التغذية الراجعة من المستخدم

        العائد:
            bool: نجاح التحديث
        """
        try:
            # التحقق من وجود التشخيص
            diagnosis_file = os.path.join(self.results_dir, f"{diagnosis_id}.json")

            if not os.path.exists(diagnosis_file):
                logger.error(f"التشخيص غير موجود: {diagnosis_id}")
                return False

            # تحميل التشخيص
            with open(diagnosis_file, "r", encoding="utf-8") as f:
                diagnosis = json.load(f)

            # التحقق من صحة التغذية الراجعة
            if "correct_disease" not in feedback:
                logger.error("التغذية الراجعة غير صالحة: يجب تحديد المرض الصحيح")
                return False

            correct_disease_name = feedback["correct_disease"]

            # الحصول على المرض الصحيح من قاعدة المعرفة
            correct_disease = self.knowledge_base.get_disease_by_name(correct_disease_name)

            if not correct_disease:
                logger.error(f"المرض غير موجود في قاعدة المعرفة: {correct_disease_name}")
                return False

            # تحديث أوزان الأعراض
            symptoms = diagnosis.get("symptoms", [])

            if not symptoms:
                logger.error("لا توجد أعراض في التشخيص")
                return False

            # زيادة أوزان الأعراض المتطابقة مع المرض الصحيح
            for symptom in correct_disease.get("symptoms", []):
                current_weight = self.symptom_weights.get(symptom, 1.0)

                # زيادة الوزن إذا كان العرض موجوداً في قائمة الأعراض المدخلة
                if any(self._calculate_text_similarity(symptom, s) > 0.7 for s in symptoms):
                    new_weight = current_weight + self.learning_rate
                else:
                    new_weight = current_weight - self.learning_rate * 0.5

                # التأكد من أن الوزن في النطاق المناسب
                new_weight = max(0.5, min(2.0, new_weight))

                self.symptom_weights[symptom] = new_weight

            # حفظ أوزان الأعراض المحدثة
            self._save_symptom_weights()

            # تحديث التشخيص بالتغذية الراجعة
            diagnosis["feedback"] = feedback
            diagnosis["updated_at"] = datetime.now().isoformat()

            # حفظ التشخيص المحدث
            with open(diagnosis_file, "w", encoding="utf-8") as f:
                json.dump(diagnosis, f, ensure_ascii=False, indent=2)

            logger.info(f"تم تحديث النموذج بناءً على التغذية الراجعة للتشخيص: {diagnosis_id}")

            return True

        except Exception as e:
            logger.error(f"خطأ أثناء تحديث النموذج: {str(e)}")
            return False

    def get_diagnosis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        الحصول على سجل التشخيصات السابقة

        المعلمات:
            limit (int, optional): عدد التشخيصات المراد استرجاعها

        العائد:
            List[Dict[str, Any]]: سجل التشخيصات
        """
        try:
            # ترتيب التشخيصات حسب التاريخ (من الأحدث إلى الأقدم)
            sorted_history = sorted(
                self.diagnosis_history,
                key=lambda x: x["timestamp"],
                reverse=True
            )

            # تحديد عدد التشخيصات المراد استرجاعها
            return sorted_history[:limit]

        except Exception as e:
            logger.error(f"خطأ أثناء استرجاع سجل التشخيصات: {str(e)}")
            return []

    def get_diagnosis_by_id(self, diagnosis_id: str) -> Optional[Dict[str, Any]]:
        """
        الحصول على تشخيص محدد بواسطة المعرف

        المعلمات:
            diagnosis_id (str): معرف التشخيص

        العائد:
            Optional[Dict[str, Any]]: التشخيص أو None إذا لم يتم العثور عليه
        """
        try:
            # التحقق من وجود التشخيص
            diagnosis_file = os.path.join(self.results_dir, f"{diagnosis_id}.json")

            if not os.path.exists(diagnosis_file):
                logger.error(f"التشخيص غير موجود: {diagnosis_id}")
                return None

            # تحميل التشخيص
            with open(diagnosis_file, "r", encoding="utf-8") as f:
                diagnosis = json.load(f)

            return diagnosis

        except Exception as e:
            logger.error(f"خطأ أثناء استرجاع التشخيص: {str(e)}")
            return None

    def export_knowledge_base(self, file_path: str) -> bool:
        """
        تصدير قاعدة المعرفة إلى ملف

        المعلمات:
            file_path (str): مسار الملف

        العائد:
            bool: نجاح التصدير
        """
        try:
            self.knowledge_base.save_knowledge_base(file_path)
            return True
        except Exception as e:
            logger.error(f"خطأ أثناء تصدير قاعدة المعرفة: {str(e)}")
            return False

    def import_knowledge_base(self, file_path: str) -> bool:
        """
        استيراد قاعدة المعرفة من ملف

        المعلمات:
            file_path (str): مسار الملف

        العائد:
            bool: نجاح الاستيراد
        """
        try:
            self.knowledge_base.load_knowledge_base(file_path)
            return True
        except Exception as e:
            logger.error(f"خطأ أثناء استيراد قاعدة المعرفة: {str(e)}")
            return False
