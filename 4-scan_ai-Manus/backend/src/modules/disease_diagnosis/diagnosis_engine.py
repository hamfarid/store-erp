# File:
# /home/ubuntu/ai_web_organized/src/modules/disease_diagnosis/diagnosis_engine.py
"""
from flask import g
محرك تشخيص الأمراض النباتية
يوفر هذا الملف محرك استدلال لتشخيص الأمراض النباتية باستخدام قاعدة المعرفة
"""

import json
import logging
import os
from datetime import datetime

# import numpy as np  # Removed: unused import
from .disease_knowledge_base import DiseaseKnowledgeBase

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DiagnosisEngine:
    """محرك تشخيص الأمراض النباتية"""

    def __init__(self, knowledge_base_path=None):
        """تهيئة محرك التشخيص"""
        # تحميل قاعدة المعرفة
        self.knowledge_base = DiseaseKnowledgeBase(knowledge_base_path)

        # مسار حفظ نتائج التشخيص
        self.results_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            'results')
        os.makedirs(self.results_dir, exist_ok=True)

        # سجل التشخيصات السابقة
        self.diagnosis_history = []

        logger.info("تم تهيئة محرك تشخيص الأمراض النباتية")

    def diagnose(
            self,
            symptoms,
            crop_type,
            image_features=None,
            environmental_conditions=None):
        """
        تشخيص المرض بناءً على الأعراض ونوع المحصول وميزات الصورة والظروف البيئية

        المعلمات:
            symptoms (list): قائمة الأعراض المرصودة
            crop_type (str): نوع المحصول
            image_features (dict, optional): ميزات مستخرجة من الصورة
            environmental_conditions (dict, optional): الظروف البيئية

        العائد:
            dict: نتيجة التشخيص
        """
        try:
            logger.info(f"بدء تشخيص المرض للمحصول: {crop_type}")

            # التحقق من وجود الأعراض ونوع المحصول
            if not symptoms or not crop_type:
                logger.error("الأعراض أو نوع المحصول غير محددة")
                return {
                    "success": False,
                    "error": "الأعراض أو نوع المحصول غير محددة",
                    "timestamp": datetime.now().isoformat()
                }

            # الحصول على الأمراض المحتملة من قاعدة المعرفة
            possible_diseases = self.knowledge_base.get_diseases_by_crop(
                crop_type)

            if not possible_diseases:
                logger.warning(
                    f"لم يتم العثور على أمراض مسجلة للمحصول: {crop_type}")
                return {
                    "success": False,
                    "error": f"لم يتم العثور على أمراض مسجلة للمحصول: {crop_type}",
                    "timestamp": datetime.now().isoformat()}

            # حساب درجة التطابق لكل مرض
            disease_scores = []
            for disease in possible_diseases:
                score = self._calculate_match_score(
                    disease, symptoms, image_features, environmental_conditions)
                disease_scores.append({
                    "disease": disease,
                    "score": score
                })

            # ترتيب الأمراض حسب درجة التطابق (من الأعلى إلى الأدنى)
            disease_scores.sort(key=lambda x: x["score"], reverse=True)

            # تحديد الأمراض المحتملة (التي تتجاوز عتبة معينة)
            threshold = 0.5  # عتبة التطابق
            probable_diseases = [
                ds for ds in disease_scores if ds["score"] >= threshold]

            # إعداد نتيجة التشخيص
            diagnosis_result = {
                "success": True,
                "crop_type": crop_type,
                "symptoms": symptoms,
                "timestamp": datetime.now().isoformat(),
                "probable_diseases": probable_diseases,
                "recommendations": self._generate_recommendations(probable_diseases)}

            # إضافة معلومات إضافية إذا كانت متوفرة
            if image_features:
                diagnosis_result["image_analysis"] = {
                    "features": image_features,
                    "confidence": self._calculate_image_confidence(image_features)}

            if environmental_conditions:
                diagnosis_result["environmental_analysis"] = {
                    "conditions": environmental_conditions,
                    "impact": self._analyze_environmental_impact(
                        environmental_conditions,
                        probable_diseases)}

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

    def _calculate_match_score(
            self,
            disease,
            symptoms,
            image_features=None,
            environmental_conditions=None):
        """
        حساب درجة تطابق المرض مع الأعراض المرصودة

        المعلمات:
            disease (dict): معلومات المرض
            symptoms (list): قائمة الأعراض المرصودة
            image_features (dict, optional): ميزات مستخرجة من الصورة
            environmental_conditions (dict, optional): الظروف البيئية

        العائد:
            float: درجة التطابق (0-1)
        """
        try:
            # الحصول على أعراض المرض
            disease_symptoms = disease.get("symptoms", [])

            if not disease_symptoms:
                return 0.0

            # حساب عدد الأعراض المتطابقة
            matching_symptoms = [s for s in symptoms if s in disease_symptoms]

            # حساب درجة تطابق الأعراض
            symptom_score = len(matching_symptoms) / \
                max(len(symptoms), len(disease_symptoms))

            # الوزن الأساسي لدرجة تطابق الأعراض
            base_weight = 0.7

            # الوزن النهائي
            final_score = base_weight * symptom_score

            # إضافة تأثير ميزات الصورة إذا كانت متوفرة
            if image_features and "image_patterns" in disease:
                image_weight = 0.2
                image_score = self._calculate_image_match(
                    disease["image_patterns"], image_features)
                final_score += image_weight * image_score

            # إضافة تأثير الظروف البيئية إذا كانت متوفرة
            if environmental_conditions and "environmental_factors" in disease:
                env_weight = 0.1
                env_score = self._calculate_environmental_match(
                    disease["environmental_factors"], environmental_conditions)
                final_score += env_weight * env_score

            return min(1.0, final_score)  # التأكد من أن الدرجة لا تتجاوز 1.0

        except Exception as e:
            logger.error(f"خطأ أثناء حساب درجة التطابق: {str(e)}")
            return 0.0

    def _calculate_image_match(self, disease_patterns, image_features):
        """
        حساب درجة تطابق أنماط الصورة مع ميزات الصورة المستخرجة

        المعلمات:
            disease_patterns (dict): أنماط الصورة للمرض
            image_features (dict): ميزات الصورة المستخرجة

        العائد:
            float: درجة التطابق (0-1)
        """
        try:
            # في التطبيق الحقيقي، سيتم استخدام خوارزميات أكثر تعقيدًا لمطابقة الصور
            # هذه مجرد محاكاة بسيطة

            # التحقق من وجود ميزات اللون
            if "color_histogram" in image_features and "color_patterns" in disease_patterns:
                # حساب تشابه هيستوجرام الألوان
                color_similarity = 0.8  # قيمة افتراضية للمحاكاة
                return color_similarity

            return 0.5  # قيمة افتراضية

        except Exception as e:
            logger.error(f"خطأ أثناء حساب تطابق الصورة: {str(e)}")
            return 0.0

    def _calculate_environmental_match(
            self, disease_factors, environmental_conditions):
        """
        حساب درجة تطابق العوامل البيئية مع الظروف البيئية الحالية

        المعلمات:
            disease_factors (dict): العوامل البيئية للمرض
            environmental_conditions (dict): الظروف البيئية الحالية

        العائد:
            float: درجة التطابق (0-1)
        """
        try:
            # في التطبيق الحقيقي، سيتم استخدام نموذج أكثر تعقيدًا لتحليل تأثير العوامل البيئية
            # هذه مجرد محاكاة بسيطة

            matches = 0
            total_factors = 0

            # التحقق من درجة الحرارة
            if "temperature" in disease_factors and "temperature" in environmental_conditions:
                total_factors += 1
                disease_temp = disease_factors["temperature"]
                actual_temp = environmental_conditions["temperature"]

                # التحقق من نطاق درجة الحرارة
                if isinstance(
                        disease_temp,
                        dict) and "min" in disease_temp and "max" in disease_temp:
                    if disease_temp["min"] <= actual_temp <= disease_temp["max"]:
                        matches += 1

            # التحقق من الرطوبة
            if "humidity" in disease_factors and "humidity" in environmental_conditions:
                total_factors += 1
                disease_humidity = disease_factors["humidity"]
                actual_humidity = environmental_conditions["humidity"]

                # التحقق من نطاق الرطوبة
                if isinstance(
                        disease_humidity,
                        dict) and "min" in disease_humidity and "max" in disease_humidity:
                    if disease_humidity["min"] <= actual_humidity <= disease_humidity["max"]:
                        matches += 1

            # التحقق من عوامل أخرى
            for factor in ["rainfall", "soil_ph", "light"]:
                if factor in disease_factors and factor in environmental_conditions:
                    total_factors += 1
                    if disease_factors[factor] == environmental_conditions[factor]:
                        matches += 1

            # حساب درجة التطابق
            if total_factors > 0:
                return matches / total_factors
            else:
                return 0.0

        except Exception as e:
            logger.error(f"خطأ أثناء حساب تطابق العوامل البيئية: {str(e)}")
            return 0.0

    def _calculate_image_confidence(self, image_features):
        """
        حساب مستوى الثقة في تحليل الصورة

        المعلمات:
            image_features (dict): ميزات الصورة المستخرجة

        العائد:
            float: مستوى الثقة (0-1)
        """
        try:
            # في التطبيق الحقيقي، سيتم استخدام نموذج أكثر تعقيدًا لحساب مستوى الثقة
            # هذه مجرد محاكاة بسيطة

            # التحقق من جودة الصورة
            if "quality_score" in image_features:
                return min(1.0, image_features["quality_score"])

            return 0.7  # قيمة افتراضية

        except Exception as e:
            logger.error(f"خطأ أثناء حساب مستوى الثقة في الصورة: {str(e)}")
            return 0.5

    def _analyze_environmental_impact(
            self,
            environmental_conditions,
            probable_diseases):
        """
        تحليل تأثير الظروف البيئية على الأمراض المحتملة

        المعلمات:
            environmental_conditions (dict): الظروف البيئية الحالية
            probable_diseases (list): قائمة الأمراض المحتملة مع درجات التطابق

        العائد:
            dict: تحليل تأثير الظروف البيئية
        """
        try:
            # في التطبيق الحقيقي، سيتم استخدام نموذج أكثر تعقيدًا لتحليل تأثير الظروف البيئية
            # هذه مجرد محاكاة بسيطة

            impact_analysis = {
                "favorable_conditions": [],
                "unfavorable_conditions": [],
                "overall_impact": "neutral"
            }

            # التحقق من تأثير درجة الحرارة
            if "temperature" in environmental_conditions:
                temp = environmental_conditions["temperature"]

                if temp > 30:
                    impact_analysis["favorable_conditions"].append(
                        "درجة الحرارة المرتفعة تساعد على انتشار بعض الأمراض الفطرية")
                elif temp < 15:
                    impact_analysis["unfavorable_conditions"].append(
                        "درجة الحرارة المنخفضة تبطئ من تطور معظم الأمراض")

            # التحقق من تأثير الرطوبة
            if "humidity" in environmental_conditions:
                humidity = environmental_conditions["humidity"]

                if humidity > 70:
                    impact_analysis["favorable_conditions"].append(
                        "الرطوبة العالية تساعد على انتشار الأمراض الفطرية والبكتيرية")
                elif humidity < 40:
                    impact_analysis["unfavorable_conditions"].append(
                        "الرطوبة المنخفضة تحد من انتشار معظم الأمراض الفطرية")

            # تحديد التأثير العام
            if len(impact_analysis["favorable_conditions"]) > len(
                    impact_analysis["unfavorable_conditions"]):
                impact_analysis["overall_impact"] = "favorable"
            elif len(impact_analysis["favorable_conditions"]) < len(impact_analysis["unfavorable_conditions"]):
                impact_analysis["overall_impact"] = "unfavorable"

            return impact_analysis

        except Exception as e:
            logger.error(f"خطأ أثناء تحليل تأثير الظروف البيئية: {str(e)}")
            return {
                "favorable_conditions": [],
                "unfavorable_conditions": [],
                "overall_impact": "unknown"
            }

    def _generate_recommendations(self, probable_diseases):
        """
        توليد توصيات بناءً على الأمراض المحتملة

        المعلمات:
            probable_diseases (list): قائمة الأمراض المحتملة مع درجات التطابق

        العائد:
            dict: توصيات للمزارع
        """
        try:
            if not probable_diseases:
                return {
                    "general": [
                        "لم يتم تحديد أي مرض محتمل. يرجى التقاط صور أوضح أو تقديم مزيد من المعلومات."
                    ],
                    "preventive": [
                        "الحفاظ على نظافة الحقل وإزالة النباتات المصابة",
                        "تطبيق برنامج وقائي للأمراض الشائعة في المنطقة"
                    ]
                }

            # الحصول على المرض الأكثر احتمالاً
            top_disease = probable_diseases[0]["disease"]

            # توليد توصيات علاجية
            treatment_recommendations = []
            if "treatments" in top_disease:
                treatment_recommendations = top_disease["treatments"]

            # توليد توصيات وقائية
            preventive_recommendations = [
                "إزالة النباتات المصابة وحرقها لمنع انتشار المرض",
                "تطبيق برنامج رش وقائي منتظم",
                "تحسين التهوية وتقليل الرطوبة حول النباتات"
            ]

            # توليد توصيات عامة
            general_recommendations = [
                f"المرض المحتمل: {top_disease['name']} (درجة التطابق: {probable_diseases[0]['score']:.2f})",
                f"وصف المرض: {top_disease.get('description', 'غير متوفر')}"]

            return {
                "general": general_recommendations,
                "treatment": treatment_recommendations,
                "preventive": preventive_recommendations
            }

        except Exception as e:
            logger.error(f"خطأ أثناء توليد التوصيات: {str(e)}")
            return {
                "general": ["حدث خطأ أثناء توليد التوصيات"],
                "treatment": [],
                "preventive": []
            }

    def _save_diagnosis_result(self, diagnosis_result):
        """
        حفظ نتيجة التشخيص

        المعلمات:
            diagnosis_result (dict): نتيجة التشخيص
        """
        try:
            # إنشاء اسم ملف فريد
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            crop_type = diagnosis_result["crop_type"].replace(" ", "_")
            filename = f"diagnosis_{crop_type}_{timestamp}.json"

            # حفظ النتيجة في ملف JSON
            filepath = os.path.join(self.results_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(diagnosis_result, f, ensure_ascii=False, indent=2)

            logger.info(f"تم حفظ نتيجة التشخيص في: {filepath}")

        except Exception as e:
            logger.error(f"خطأ أثناء حفظ نتيجة التشخيص: {str(e)}")

    def get_diagnosis_history(self, limit=10):
        """
        الحصول على سجل التشخيصات السابقة

        المعلمات:
            limit (int): عدد النتائج المطلوبة

        العائد:
            list: سجل التشخيصات السابقة
        """
        # ترتيب السجل حسب التاريخ (الأحدث أولاً)
        sorted_history = sorted(
            self.diagnosis_history,
            key=lambda x: x["timestamp"],
            reverse=True)

        # تحديد عدد النتائج المطلوبة
        return sorted_history[:limit]

    def get_diagnosis_statistics(self):
        """
        الحصول على إحصائيات التشخيص

        العائد:
            dict: إحصائيات التشخيص
        """
        try:
            total_diagnoses = len(self.diagnosis_history)

            if total_diagnoses == 0:
                return {
                    "total_diagnoses": 0,
                    "success_rate": 0,
                    "crop_distribution": {}
                }

            # حساب معدل النجاح
            successful_diagnoses = sum(
                1 for d in self.diagnosis_history if d["result"] == "success")
            success_rate = successful_diagnoses / total_diagnoses

            # حساب توزيع المحاصيل
            crop_distribution = {}
            for diagnosis in self.diagnosis_history:
                crop_type = diagnosis["crop_type"]
                if crop_type in crop_distribution:
                    crop_distribution[crop_type] += 1
                else:
                    crop_distribution[crop_type] = 1

            # تحويل التوزيع إلى نسب مئوية
            for crop in crop_distribution:
                crop_distribution[crop] = crop_distribution[crop] / \
                    total_diagnoses

            return {
                "total_diagnoses": total_diagnoses,
                "success_rate": success_rate,
                "crop_distribution": crop_distribution
            }

        except Exception as e:
            logger.error(f"خطأ أثناء حساب إحصائيات التشخيص: {str(e)}")
            return {
                "total_diagnoses": 0,
                "success_rate": 0,
                "crop_distribution": {}
            }
