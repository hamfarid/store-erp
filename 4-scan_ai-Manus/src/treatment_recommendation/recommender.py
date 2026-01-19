#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة توصيات العلاج
=================

توفر هذه الوحدة وظائف لتقديم توصيات علاجية متكاملة للأمراض النباتية
ونقص العناصر الغذائية، مع حساب الجرعات وتحديد التوقيت.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta

# إعداد السجل
logger = logging.getLogger("agricultural_ai.treatment_recommender")

class TreatmentRecommender:
    """فئة لتقديم توصيات العلاج"""
    
    def __init__(self, config: Dict):
        """تهيئة مقدم التوصيات
        
        المعاملات:
            config (Dict): تكوين مقدم التوصيات
        """
        self.config = config
        self.database_config = self.config.get("database", {})
        self.dosage_config = self.config.get("dosage_calculation", {})
        self.timing_config = self.config.get("timing", {})
        self.follow_up_config = self.config.get("follow_up", {})
        
        # تحميل قواعد بيانات العلاجات (مثال باستخدام ملفات JSON)
        self.treatments_data = self._load_db_data(self.database_config.get("treatments_db", "database/treatments.db"))
        self.pesticides_data = self._load_db_data(self.database_config.get("pesticides_db", "database/pesticides.db"))
        self.fertilizers_data = self._load_db_data(self.database_config.get("fertilizers_db", "database/fertilizers.db"))
        
        logger.info("تم تهيئة مقدم توصيات العلاج")

    def _load_db_data(self, db_path: str) -> Dict:
        """تحميل البيانات من قاعدة البيانات (ملف JSON كمثال)"""
        data = {}
        json_path = db_path.replace(".db", ".json") # استخدام JSON كمثال
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"تم تحميل البيانات من: {json_path}")
            except Exception as e:
                logger.error(f"فشل في تحميل البيانات من {json_path}: {str(e)}")
        else:
            logger.warning(f"ملف البيانات غير موجود: {json_path}")
        return data

    def _find_treatments_for_disease(self, disease_name: str) -> List[Dict]:
        """البحث عن علاجات لمرض معين"""
        treatments = []
        # البحث في قاعدة بيانات العلاجات العامة
        for treatment_id, treatment_info in self.treatments_data.items():
            if disease_name in treatment_info.get("targets", []):
                treatments.append({"id": treatment_id, "type": "general", **treatment_info})
        
        # البحث في قاعدة بيانات المبيدات
        for pesticide_id, pesticide_info in self.pesticides_data.items():
            if disease_name in pesticide_info.get("targets", []):
                treatments.append({"id": pesticide_id, "type": "pesticide", **pesticide_info})
                
        return treatments

    def _find_treatments_for_deficiency(self, deficiency_name: str) -> List[Dict]:
        """البحث عن علاجات لنقص عنصر معين"""
        treatments = []
        # البحث في قاعدة بيانات الأسمدة
        for fertilizer_id, fertilizer_info in self.fertilizers_data.items():
            # البحث عن العنصر في تركيبة السماد
            if any(nutrient.get("name") == deficiency_name.split(" ")[0] 
                   for nutrient in fertilizer_info.get("composition", [])):
                treatments.append({"id": fertilizer_id, "type": "fertilizer", **fertilizer_info})
                
        return treatments

    def _calculate_dosage(self, treatment_info: Dict, severity: float = 0.5, 
                         plant_size: Optional[float] = None, 
                         environmental_factors: Optional[Dict] = None) -> Dict:
        """حساب الجرعة الموصى بها
        
        المعاملات:
            treatment_info (Dict): معلومات العلاج
            severity (float): شدة المشكلة (0-1)
            plant_size (float, optional): حجم النبات (مثل الارتفاع أو المساحة)
            environmental_factors (Dict, optional): عوامل بيئية (مثل درجة الحرارة، الرطوبة)
            
        الإرجاع:
            Dict: معلومات الجرعة (الكمية، الوحدة، تعليمات التطبيق)
        """
        base_dosage = treatment_info.get("base_dosage", {}).get("amount", 1.0)
        unit = treatment_info.get("base_dosage", {}).get("unit", "وحدة")
        application_method = treatment_info.get("application_method", "غير محدد")
        
        # تعديل الجرعة بناءً على الشدة
        dosage = base_dosage * (1 + (severity - 0.5) * 0.5) # تعديل بنسبة +/- 25%
        
        # تعديل الجرعة بناءً على حجم النبات (إذا تم التكوين)
        if self.dosage_config.get("consider_plant_size") and plant_size is not None:
            # مثال بسيط: زيادة الجرعة مع زيادة الحجم
            size_factor = 1 + (plant_size / 100) * 0.1 # زيادة 10% لكل 100 وحدة حجم
            dosage *= size_factor
            
        # تعديل الجرعة بناءً على العوامل البيئية (إذا تم التكوين)
        if self.dosage_config.get("consider_environmental_factors") and environmental_factors:
            # مثال: تقليل الجرعة في درجات الحرارة العالية
            temp = environmental_factors.get("temperature")
            if temp and temp > 30:
                dosage *= 0.9 # تقليل 10%
        
        # تطبيق عامل الأمان
        safety_factor = self.dosage_config.get("safety_factor", 1.0)
        dosage *= safety_factor
        
        return {
            "amount": round(dosage, 2),
            "unit": unit,
            "application_method": application_method,
            "notes": treatment_info.get("dosage_notes", "")
        }

    def _determine_timing(self, treatment_info: Dict, 
                         weather_forecast: Optional[Dict] = None, 
                         growth_stage: Optional[str] = None, 
                         disease_lifecycle: Optional[str] = None) -> Dict:
        """تحديد التوقيت الأمثل للعلاج
        
        المعاملات:
            treatment_info (Dict): معلومات العلاج
            weather_forecast (Dict, optional): توقعات الطقس
            growth_stage (str, optional): مرحلة نمو النبات
            disease_lifecycle (str, optional): مرحلة دورة حياة المرض
            
        الإرجاع:
            Dict: معلومات التوقيت (الوقت الموصى به، التكرار، ملاحظات)
        """
        recommended_time = "في أقرب وقت ممكن" # قيمة افتراضية
        frequency = treatment_info.get("frequency", "مرة واحدة")
        timing_notes = treatment_info.get("timing_notes", "")
        
        # تعديل التوقيت بناءً على الطقس (إذا تم التكوين)
        if self.timing_config.get("consider_weather") and weather_forecast:
            # مثال: تجنب الرش قبل المطر
            if any(day.get("precipitation_probability", 0) > 0.5 for day in weather_forecast.get("daily", [])): 
                timing_notes += " تجنب الرش قبل هطول الأمطار المتوقع." 
                # يمكن تحديد وقت بديل هنا
        
        # تعديل التوقيت بناءً على مرحلة النمو (إذا تم التكوين)
        if self.timing_config.get("consider_growth_stage") and growth_stage:
            allowed_stages = treatment_info.get("allowed_growth_stages")
            if allowed_stages and growth_stage not in allowed_stages:
                timing_notes += f" العلاج غير موصى به في مرحلة النمو الحالية ({growth_stage}). المراحل المسموح بها: {', '.join(allowed_stages)}."
                recommended_time = "غير موصى به الآن"
        
        # تعديل التوقيت بناءً على دورة حياة المرض (إذا تم التكوين)
        if self.timing_config.get("consider_disease_lifecycle") and disease_lifecycle:
            optimal_stages = treatment_info.get("optimal_disease_stages")
            if optimal_stages and disease_lifecycle not in optimal_stages:
                timing_notes += f" قد تكون فعالية العلاج أقل في مرحلة المرض الحالية ({disease_lifecycle}). المراحل المثلى: {', '.join(optimal_stages)}."
        
        return {
            "recommended_time": recommended_time,
            "frequency": frequency,
            "notes": timing_notes.strip()
        }

    def _generate_follow_up_schedule(self, start_date: datetime = datetime.now()) -> List[Dict]:
        """إنشاء جدول متابعة"""
        schedule = []
        if self.follow_up_config.get("generate_schedule"): 
            intervals = self.follow_up_config.get("reminder_intervals", [3, 7, 14, 30])
            for interval in intervals:
                follow_up_date = start_date + timedelta(days=interval)
                schedule.append({
                    "date": follow_up_date.strftime("%Y-%m-%d"),
                    "action": "مراقبة فعالية العلاج وتقييم حالة النبات"
                })
        return schedule

    def recommend(self, 
                 disease_results: Optional[Dict[str, List[Dict[str, Any]]]] = None, 
                 nutrient_results: Optional[Dict[str, List[Dict[str, Any]]]] = None, 
                 plant_info: Optional[Dict] = None, 
                 weather_forecast: Optional[Dict] = None) -> List[Dict]:
        """تقديم توصيات العلاج بناءً على نتائج التشخيص
        
        المعاملات:
            disease_results (Dict): نتائج الكشف عن الأمراض
            nutrient_results (Dict): نتائج تحليل نقص العناصر
            plant_info (Dict, optional): معلومات إضافية عن النبات (الحجم، مرحلة النمو)
            weather_forecast (Dict, optional): توقعات الطقس
            
        الإرجاع:
            List[Dict]: قائمة بالتوصيات العلاجية
        """
        recommendations = []
        processed_issues = set() # لتجنب التوصيات المتكررة لنفس المشكلة
        
        # 1. معالجة الأمراض
        if disease_results:
            for disease_type, detections in disease_results.items():
                if disease_type == "error": continue
                
                for detection in detections:
                    disease_name = detection["disease_name"]
                    confidence = detection["confidence"]
                    
                    if disease_name in processed_issues:
                        continue
                    
                    # البحث عن علاجات للمرض
                    treatments = self._find_treatments_for_disease(disease_name)
                    
                    if not treatments:
                        logger.warning(f"لم يتم العثور على علاجات للمرض: {disease_name}")
                        continue
                    
                    # اختيار أفضل علاج (مثال: الأعلى تقييمًا أو الأكثر شيوعًا)
                    # هنا نختار العلاج الأول كمثال
                    best_treatment = treatments[0]
                    
                    # حساب الجرعة
                    dosage = self._calculate_dosage(
                        best_treatment,
                        severity=confidence, # استخدام الثقة كمؤشر للشدة
                        plant_size=plant_info.get("size") if plant_info else None,
                        environmental_factors=weather_forecast.get("current") if weather_forecast else None
                    )
                    
                    # تحديد التوقيت
                    timing = self._determine_timing(
                        best_treatment,
                        weather_forecast=weather_forecast,
                        growth_stage=plant_info.get("growth_stage") if plant_info else None,
                        disease_lifecycle=detection.get("stage") # إذا كانت متاحة من الكاشف
                    )
                    
                    # إنشاء التوصية
                    recommendations.append({
                        "issue_type": "disease",
                        "issue_name": disease_name,
                        "confidence": confidence,
                        "recommended_treatment": {
                            "id": best_treatment["id"],
                            "name": best_treatment.get("name", "علاج غير مسمى"),
                            "type": best_treatment["type"],
                            "description": best_treatment.get("description", "")
                        },
                        "dosage": dosage,
                        "timing": timing,
                        "follow_up": self._generate_follow_up_schedule()
                    })
                    processed_issues.add(disease_name)
        
        # 2. معالجة نقص العناصر
        if nutrient_results:
            for category, detections in nutrient_results.items():
                if category == "error" or category == "leaf_health": continue
                
                for detection in detections:
                    deficiency_name = detection["deficiency_name"]
                    confidence = detection["confidence"]
                    
                    if deficiency_name in processed_issues:
                        continue
                        
                    # البحث عن علاجات للنقص
                    treatments = self._find_treatments_for_deficiency(deficiency_name)
                    
                    if not treatments:
                        logger.warning(f"لم يتم العثور على علاجات لنقص: {deficiency_name}")
                        continue
                        
                    # اختيار أفضل علاج (مثال: السماد الأكثر تركيزًا بالعنصر)
                    # هنا نختار العلاج الأول كمثال
                    best_treatment = treatments[0]
                    
                    # حساب الجرعة
                    dosage = self._calculate_dosage(
                        best_treatment,
                        severity=confidence, # استخدام الثقة كمؤشر للشدة
                        plant_size=plant_info.get("size") if plant_info else None,
                        environmental_factors=weather_forecast.get("current") if weather_forecast else None
                    )
                    
                    # تحديد التوقيت
                    timing = self._determine_timing(
                        best_treatment,
                        weather_forecast=weather_forecast,
                        growth_stage=plant_info.get("growth_stage") if plant_info else None
                    )
                    
                    # إنشاء التوصية
                    recommendations.append({
                        "issue_type": "nutrient_deficiency",
                        "issue_name": deficiency_name,
                        "confidence": confidence,
                        "recommended_treatment": {
                            "id": best_treatment["id"],
                            "name": best_treatment.get("name", "سماد غير مسمى"),
                            "type": best_treatment["type"],
                            "description": best_treatment.get("description", "")
                        },
                        "dosage": dosage,
                        "timing": timing,
                        "follow_up": self._generate_follow_up_schedule()
                    })
                    processed_issues.add(deficiency_name)
                    
        # ترتيب التوصيات (اختياري، مثلاً حسب الأهمية أو الثقة)
        recommendations = sorted(recommendations, key=lambda x: x.get("confidence", 0), reverse=True)
        
        return recommendations

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "database": {
            "treatments_db": "../../database/treatments.db",
            "pesticides_db": "../../database/pesticides.db",
            "fertilizers_db": "../../database/fertilizers.db"
        },
        "dosage_calculation": {
            "safety_factor": 0.9,
            "consider_plant_size": True,
            "consider_environmental_factors": True
        },
        "timing": {
            "consider_weather": True,
            "consider_growth_stage": True,
            "consider_disease_lifecycle": True
        },
        "follow_up": {
            "generate_schedule": True,
            "reminder_intervals": [7, 14, 30]
        }
    }
    
    # إنشاء مجلدات وهمية وقواعد بيانات (للتجربة فقط)
    os.makedirs("../../database", exist_ok=True)
    
    # إنشاء ملفات قواعد بيانات وهمية (JSON)
    treatments_db_data = {
        "TRT001": {"name": "علاج فطري عام", "targets": ["Fungal Disease 1", "Fungal Disease 3"], "base_dosage": {"amount": 10, "unit": "مل/لتر"}, "application_method": "رش ورقي"}
    }
    pesticides_db_data = {
        "PES001": {"name": "مبيد حشري جهازي", "targets": ["Aphids"], "base_dosage": {"amount": 5, "unit": "مل/لتر"}, "application_method": "رش ورقي", "allowed_growth_stages": ["Vegetative", "Flowering"]}
    }
    fertilizers_db_data = {
        "FER001": {"name": "سماد نيتروجيني عالي", "composition": [{"name": "Nitrogen", "percentage": 20}], "base_dosage": {"amount": 50, "unit": "كجم/هكتار"}, "application_method": "تسميد أرضي"},
        "FER002": {"name": "سماد حديد مخلبي", "composition": [{"name": "Iron", "percentage": 6}], "base_dosage": {"amount": 2, "unit": "جم/لتر"}, "application_method": "رش ورقي"}
    }
    
    with open(dummy_config["database"]["treatments_db"].replace(".db", ".json"), "w", encoding="utf-8") as f:
        json.dump(treatments_db_data, f, ensure_ascii=False, indent=4)
    with open(dummy_config["database"]["pesticides_db"].replace(".db", ".json"), "w", encoding="utf-8") as f:
        json.dump(pesticides_db_data, f, ensure_ascii=False, indent=4)
    with open(dummy_config["database"]["fertilizers_db"].replace(".db", ".json"), "w", encoding="utf-8") as f:
        json.dump(fertilizers_db_data, f, ensure_ascii=False, indent=4)
        
    # تهيئة مقدم التوصيات
    recommender = TreatmentRecommender(dummy_config)
    
    # نتائج تشخيص وهمية
    dummy_disease_results = {
        "fungal": [
            {"disease_name": "Fungal Disease 3", "confidence": 0.85, "type": "fungal"}
        ]
    }
    dummy_nutrient_results = {
        "major_nutrients": [
            {"deficiency_name": "Nitrogen Deficiency", "confidence": 0.75, "category": "major_nutrients"}
        ],
        "minor_nutrients": [
            {"deficiency_name": "Iron Deficiency", "confidence": 0.90, "category": "minor_nutrients"}
        ]
    }
    
    # معلومات نبات وهمية
    dummy_plant_info = {
        "size": 150, # مثال: ارتفاع 150 سم
        "growth_stage": "Flowering"
    }
    
    # توقعات طقس وهمية
    dummy_weather_forecast = {
        "current": {"temperature": 28},
        "daily": [
            {"date": "2025-04-28", "precipitation_probability": 0.1},
            {"date": "2025-04-29", "precipitation_probability": 0.6} # مطر متوقع
        ]
    }
    
    # الحصول على التوصيات
    recommendations = recommender.recommend(
        disease_results=dummy_disease_results,
        nutrient_results=dummy_nutrient_results,
        plant_info=dummy_plant_info,
        weather_forecast=dummy_weather_forecast
    )
    
    # طباعة النتائج
    print("\nالتوصيات العلاجية:")
    print(json.dumps(recommendations, indent=4, ensure_ascii=False))
    
    # تنظيف الملفات الوهمية (اختياري)
    # import shutil
    # shutil.rmtree("../../database")
    # logger.info("تم حذف الملفات والمجلدات الوهمية")
