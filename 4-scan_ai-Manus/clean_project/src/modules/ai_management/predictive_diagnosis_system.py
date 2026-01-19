# File: /home/ubuntu/clean_project/src/modules/ai_management/predictive_diagnosis_system.py
"""
نظام التشخيص الاستباقي
يتنبأ بالأمراض قبل ظهورها من خلال تحليل العوامل البيئية والوراثية
"""

import os
import json
import logging
import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import pickle
import warnings
warnings.filterwarnings('ignore')

# مكتبات التعلم الآلي والتحليل
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.cluster import DBSCAN, KMeans
import xgboost as xgb
import lightgbm as lgb

# مكتبات التحليل الإحصائي
from scipy import stats
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import seaborn as sns

# مكتبات الطقس والبيانات البيئية
import requests
from collections import defaultdict, deque
import time
import threading
import queue

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """مستويات المخاطر"""
    VERY_LOW = "very_low"      # منخفض جداً
    LOW = "low"                # منخفض
    MODERATE = "moderate"      # متوسط
    HIGH = "high"              # عالي
    VERY_HIGH = "very_high"    # عالي جداً
    CRITICAL = "critical"      # حرج

class AlertType(Enum):
    """أنواع التنبيهات"""
    DISEASE_RISK = "disease_risk"           # خطر مرض
    WEATHER_WARNING = "weather_warning"     # تحذير طقس
    PEST_OUTBREAK = "pest_outbreak"         # تفشي آفات
    NUTRIENT_DEFICIENCY = "nutrient_deficiency"  # نقص عناصر
    IRRIGATION_ALERT = "irrigation_alert"   # تنبيه ري
    HARVEST_TIMING = "harvest_timing"       # توقيت الحصاد

class PredictionModel(Enum):
    """نماذج التنبؤ"""
    LSTM_WEATHER = "lstm_weather"           # LSTM للطقس
    RF_DISEASE = "rf_disease"               # Random Forest للأمراض
    XGB_PEST = "xgb_pest"                   # XGBoost للآفات
    ENSEMBLE_RISK = "ensemble_risk"         # نموذج مجمع للمخاطر
    DEEP_MULTIMODAL = "deep_multimodal"     # نموذج عميق متعدد الوسائط

@dataclass
class EnvironmentalData:
    """البيانات البيئية"""
    timestamp: datetime
    location: Dict[str, float]  # lat, lon
    temperature: float          # درجة الحرارة (مئوية)
    humidity: float            # الرطوبة (%)
    rainfall: float            # هطول الأمطار (مم)
    wind_speed: float          # سرعة الرياح (كم/ساعة)
    wind_direction: float      # اتجاه الرياح (درجة)
    pressure: float            # الضغط الجوي (هكتوباسكال)
    solar_radiation: float     # الإشعاع الشمسي (واط/م²)
    soil_temperature: float    # درجة حرارة التربة
    soil_moisture: float       # رطوبة التربة (%)
    soil_ph: float            # حموضة التربة
    uv_index: float           # مؤشر الأشعة فوق البنفسجية

@dataclass
class PlantGeneticData:
    """البيانات الوراثية للنبات"""
    plant_id: str
    variety: str               # الصنف
    genetic_markers: List[str] # المؤشرات الوراثية
    resistance_genes: List[str] # جينات المقاومة
    susceptibility_factors: List[str] # عوامل القابلية للإصابة
    growth_stage: str          # مرحلة النمو
    age_days: int             # عمر النبات بالأيام
    health_history: List[Dict[str, Any]] # تاريخ الصحة

@dataclass
class DiseaseRiskPrediction:
    """تنبؤ خطر المرض"""
    prediction_id: str
    plant_id: str
    disease_name: str
    risk_level: RiskLevel
    probability: float         # احتمالية الإصابة (0-1)
    confidence: float          # ثقة التنبؤ (0-1)
    time_to_onset: int        # الوقت المتوقع للظهور (أيام)
    contributing_factors: List[Dict[str, Any]]
    recommended_actions: List[str]
    prediction_timestamp: datetime
    model_used: PredictionModel
    environmental_snapshot: EnvironmentalData

@dataclass
class EarlyWarningAlert:
    """تنبيه الإنذار المبكر"""
    alert_id: str
    alert_type: AlertType
    severity: RiskLevel
    title: str
    message: str
    affected_area: Dict[str, Any]  # المنطقة المتأثرة
    affected_crops: List[str]
    time_window: Dict[str, datetime]  # start_time, end_time
    recommended_actions: List[str]
    created_at: datetime
    expires_at: datetime
    acknowledged: bool = False
    resolved: bool = False

class WeatherDataCollector:
    """جامع البيانات الجوية"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        self.api_keys = api_keys or {}
        self.cache = {}
        self.cache_duration = 300  # 5 دقائق
        
        # مصادر البيانات المتعددة
        self.weather_sources = {
            "openweather": self._get_openweather_data,
            "weatherapi": self._get_weatherapi_data,
            "meteostat": self._get_meteostat_data
        }
    
    async def collect_environmental_data(self, location: Dict[str, float], 
                                       sources: List[str] = None) -> EnvironmentalData:
        """جمع البيانات البيئية من مصادر متعددة"""
        try:
            if sources is None:
                sources = list(self.weather_sources.keys())
            
            # فحص الكاش
            cache_key = f"{location['lat']}_{location['lon']}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if (datetime.now() - timestamp).seconds < self.cache_duration:
                    return cached_data
            
            # جمع البيانات من مصادر متعددة
            all_data = []
            for source in sources:
                if source in self.weather_sources:
                    try:
                        data = await self.weather_sources[source](location)
                        if data:
                            all_data.append(data)
                    except Exception as e:
                        logger.warning(f"فشل في جمع البيانات من {source}: {e}")
            
            if not all_data:
                # إنشاء بيانات افتراضية
                return self._create_default_environmental_data(location)
            
            # دمج البيانات من المصادر المختلفة
            merged_data = self._merge_environmental_data(all_data, location)
            
            # حفظ في الكاش
            self.cache[cache_key] = (merged_data, datetime.now())
            
            return merged_data
            
        except Exception as e:
            logger.error(f"خطأ في جمع البيانات البيئية: {e}")
            return self._create_default_environmental_data(location)
    
    async def _get_openweather_data(self, location: Dict[str, float]) -> Dict[str, Any]:
        """جمع البيانات من OpenWeatherMap"""
        # محاكاة استدعاء API
        await asyncio.sleep(0.1)
        
        # بيانات وهمية للمحاكاة
        return {
            "temperature": np.random.uniform(15, 35),
            "humidity": np.random.uniform(30, 90),
            "pressure": np.random.uniform(1000, 1020),
            "wind_speed": np.random.uniform(0, 20),
            "wind_direction": np.random.uniform(0, 360),
            "rainfall": np.random.exponential(2),
            "solar_radiation": np.random.uniform(200, 1000),
            "uv_index": np.random.uniform(1, 11)
        }
    
    async def _get_weatherapi_data(self, location: Dict[str, float]) -> Dict[str, Any]:
        """جمع البيانات من WeatherAPI"""
        await asyncio.sleep(0.1)
        
        return {
            "temperature": np.random.uniform(15, 35),
            "humidity": np.random.uniform(30, 90),
            "pressure": np.random.uniform(1000, 1020),
            "wind_speed": np.random.uniform(0, 20),
            "rainfall": np.random.exponential(2)
        }
    
    async def _get_meteostat_data(self, location: Dict[str, float]) -> Dict[str, Any]:
        """جمع البيانات من Meteostat"""
        await asyncio.sleep(0.1)
        
        return {
            "temperature": np.random.uniform(15, 35),
            "humidity": np.random.uniform(30, 90),
            "soil_temperature": np.random.uniform(10, 30),
            "soil_moisture": np.random.uniform(20, 80)
        }
    
    def _merge_environmental_data(self, data_list: List[Dict[str, Any]], 
                                location: Dict[str, float]) -> EnvironmentalData:
        """دمج البيانات من مصادر متعددة"""
        merged = {}
        
        # حساب المتوسط للقيم المتكررة
        for data in data_list:
            for key, value in data.items():
                if key not in merged:
                    merged[key] = []
                merged[key].append(value)
        
        # حساب المتوسطات
        for key in merged:
            merged[key] = np.mean(merged[key])
        
        # إنشاء كائن البيانات البيئية
        return EnvironmentalData(
            timestamp=datetime.now(),
            location=location,
            temperature=merged.get("temperature", 25.0),
            humidity=merged.get("humidity", 60.0),
            rainfall=merged.get("rainfall", 0.0),
            wind_speed=merged.get("wind_speed", 5.0),
            wind_direction=merged.get("wind_direction", 180.0),
            pressure=merged.get("pressure", 1013.0),
            solar_radiation=merged.get("solar_radiation", 500.0),
            soil_temperature=merged.get("soil_temperature", 20.0),
            soil_moisture=merged.get("soil_moisture", 50.0),
            soil_ph=merged.get("soil_ph", 6.5),
            uv_index=merged.get("uv_index", 5.0)
        )
    
    def _create_default_environmental_data(self, location: Dict[str, float]) -> EnvironmentalData:
        """إنشاء بيانات بيئية افتراضية"""
        return EnvironmentalData(
            timestamp=datetime.now(),
            location=location,
            temperature=25.0,
            humidity=60.0,
            rainfall=0.0,
            wind_speed=5.0,
            wind_direction=180.0,
            pressure=1013.0,
            solar_radiation=500.0,
            soil_temperature=20.0,
            soil_moisture=50.0,
            soil_ph=6.5,
            uv_index=5.0
        )

class DiseaseRiskModel:
    """نموذج تقييم مخاطر الأمراض"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_importance = {}
        
        # قواعد المعرفة للأمراض
        self.disease_rules = {
            "تبقع الأوراق": {
                "optimal_conditions": {
                    "temperature": (20, 30),
                    "humidity": (70, 95),
                    "rainfall": (5, 50)
                },
                "risk_factors": ["high_humidity", "moderate_temperature", "leaf_wetness"],
                "susceptible_stages": ["flowering", "fruit_development"]
            },
            "البياض الدقيقي": {
                "optimal_conditions": {
                    "temperature": (15, 25),
                    "humidity": (50, 80),
                    "wind_speed": (0, 5)
                },
                "risk_factors": ["low_wind", "moderate_humidity", "cool_temperature"],
                "susceptible_stages": ["vegetative", "early_flowering"]
            },
            "الذبول البكتيري": {
                "optimal_conditions": {
                    "temperature": (25, 35),
                    "soil_moisture": (80, 100),
                    "soil_ph": (6.0, 7.5)
                },
                "risk_factors": ["high_soil_moisture", "warm_temperature", "neutral_ph"],
                "susceptible_stages": ["all_stages"]
            }
        }
    
    def train_disease_models(self, training_data: pd.DataFrame):
        """تدريب نماذج الأمراض"""
        try:
            diseases = training_data['disease'].unique()
            
            for disease in diseases:
                logger.info(f"تدريب نموذج لمرض: {disease}")
                
                # تحضير البيانات
                disease_data = training_data[training_data['disease'] == disease].copy()
                
                # الميزات البيئية
                feature_columns = [
                    'temperature', 'humidity', 'rainfall', 'wind_speed',
                    'pressure', 'solar_radiation', 'soil_temperature',
                    'soil_moisture', 'soil_ph', 'uv_index'
                ]
                
                X = disease_data[feature_columns]
                y = disease_data['infected']  # 0 أو 1
                
                # تقسيم البيانات
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42, stratify=y
                )
                
                # تطبيع البيانات
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # تدريب نموذج مجمع
                ensemble_model = self._create_ensemble_model()
                ensemble_model.fit(X_train_scaled, y_train)
                
                # تقييم النموذج
                y_pred = ensemble_model.predict(X_test_scaled)
                accuracy = accuracy_score(y_test, y_pred)
                
                logger.info(f"دقة نموذج {disease}: {accuracy:.3f}")
                
                # حفظ النموذج والمعايرة
                self.models[disease] = ensemble_model
                self.scalers[disease] = scaler
                
                # حساب أهمية الميزات
                if hasattr(ensemble_model, 'feature_importances_'):
                    self.feature_importance[disease] = dict(
                        zip(feature_columns, ensemble_model.feature_importances_)
                    )
                
        except Exception as e:
            logger.error(f"خطأ في تدريب نماذج الأمراض: {e}")
    
    def _create_ensemble_model(self):
        """إنشاء نموذج مجمع للتنبؤ"""
        from sklearn.ensemble import VotingClassifier
        
        # نماذج متعددة
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        xgb_model = xgb.XGBClassifier(n_estimators=100, random_state=42)
        
        # نموذج مجمع
        ensemble = VotingClassifier(
            estimators=[
                ('rf', rf_model),
                ('gb', gb_model),
                ('xgb', xgb_model)
            ],
            voting='soft'
        )
        
        return ensemble
    
    async def predict_disease_risk(self, environmental_data: EnvironmentalData,
                                 plant_data: PlantGeneticData,
                                 disease_name: str) -> DiseaseRiskPrediction:
        """التنبؤ بخطر الإصابة بمرض معين"""
        try:
            # تحضير البيانات للتنبؤ
            features = self._prepare_features(environmental_data, plant_data)
            
            # التنبؤ باستخدام النموذج المدرب
            if disease_name in self.models:
                model = self.models[disease_name]
                scaler = self.scalers[disease_name]
                
                features_scaled = scaler.transform([features])
                probability = model.predict_proba(features_scaled)[0][1]  # احتمالية الإصابة
                
            else:
                # استخدام القواعد المعرفية
                probability = self._rule_based_prediction(environmental_data, disease_name)
            
            # تحديد مستوى المخاطر
            risk_level = self._calculate_risk_level(probability)
            
            # حساب الثقة
            confidence = self._calculate_confidence(environmental_data, plant_data, disease_name)
            
            # تقدير الوقت للظهور
            time_to_onset = self._estimate_time_to_onset(
                environmental_data, disease_name, probability
            )
            
            # تحديد العوامل المساهمة
            contributing_factors = self._identify_contributing_factors(
                environmental_data, plant_data, disease_name
            )
            
            # توصيات الإجراءات
            recommended_actions = self._generate_recommendations(
                risk_level, disease_name, contributing_factors
            )
            
            # إنشاء التنبؤ
            prediction = DiseaseRiskPrediction(
                prediction_id=f"pred_{int(datetime.now().timestamp())}",
                plant_id=plant_data.plant_id,
                disease_name=disease_name,
                risk_level=risk_level,
                probability=probability,
                confidence=confidence,
                time_to_onset=time_to_onset,
                contributing_factors=contributing_factors,
                recommended_actions=recommended_actions,
                prediction_timestamp=datetime.now(),
                model_used=PredictionModel.ENSEMBLE_RISK,
                environmental_snapshot=environmental_data
            )
            
            return prediction
            
        except Exception as e:
            logger.error(f"خطأ في التنبؤ بخطر المرض: {e}")
            # إرجاع تنبؤ افتراضي
            return self._create_default_prediction(plant_data.plant_id, disease_name)
    
    def _prepare_features(self, env_data: EnvironmentalData, 
                         plant_data: PlantGeneticData) -> List[float]:
        """تحضير الميزات للتنبؤ"""
        features = [
            env_data.temperature,
            env_data.humidity,
            env_data.rainfall,
            env_data.wind_speed,
            env_data.pressure,
            env_data.solar_radiation,
            env_data.soil_temperature,
            env_data.soil_moisture,
            env_data.soil_ph,
            env_data.uv_index
        ]
        
        # إضافة ميزات النبات
        features.extend([
            plant_data.age_days,
            len(plant_data.resistance_genes),
            len(plant_data.susceptibility_factors)
        ])
        
        return features
    
    def _rule_based_prediction(self, env_data: EnvironmentalData, 
                             disease_name: str) -> float:
        """التنبؤ باستخدام القواعد المعرفية"""
        if disease_name not in self.disease_rules:
            return 0.3  # احتمالية افتراضية
        
        rules = self.disease_rules[disease_name]
        optimal_conditions = rules["optimal_conditions"]
        
        risk_score = 0.0
        total_factors = len(optimal_conditions)
        
        # فحص الظروف المثلى
        for condition, (min_val, max_val) in optimal_conditions.items():
            if hasattr(env_data, condition):
                value = getattr(env_data, condition)
                if min_val <= value <= max_val:
                    risk_score += 1.0
                else:
                    # حساب المسافة من النطاق المثالي
                    if value < min_val:
                        distance = (min_val - value) / min_val
                    else:
                        distance = (value - max_val) / max_val
                    
                    risk_score += max(0, 1.0 - distance)
        
        return min(risk_score / total_factors, 1.0)
    
    def _calculate_risk_level(self, probability: float) -> RiskLevel:
        """تحديد مستوى المخاطر"""
        if probability >= 0.9:
            return RiskLevel.CRITICAL
        elif probability >= 0.7:
            return RiskLevel.VERY_HIGH
        elif probability >= 0.5:
            return RiskLevel.HIGH
        elif probability >= 0.3:
            return RiskLevel.MODERATE
        elif probability >= 0.1:
            return RiskLevel.LOW
        else:
            return RiskLevel.VERY_LOW
    
    def _calculate_confidence(self, env_data: EnvironmentalData,
                            plant_data: PlantGeneticData, 
                            disease_name: str) -> float:
        """حساب ثقة التنبؤ"""
        confidence = 0.5  # ثقة أساسية
        
        # زيادة الثقة بناءً على جودة البيانات
        if env_data.timestamp and (datetime.now() - env_data.timestamp).hours < 1:
            confidence += 0.2  # بيانات حديثة
        
        if len(plant_data.resistance_genes) > 0:
            confidence += 0.1  # معلومات وراثية متاحة
        
        if disease_name in self.models:
            confidence += 0.2  # نموذج مدرب متاح
        
        return min(confidence, 1.0)
    
    def _estimate_time_to_onset(self, env_data: EnvironmentalData,
                              disease_name: str, probability: float) -> int:
        """تقدير الوقت للظهور بالأيام"""
        base_time = {
            "تبقع الأوراق": 7,
            "البياض الدقيقي": 5,
            "الذبول البكتيري": 10
        }.get(disease_name, 7)
        
        # تعديل بناءً على الاحتمالية والظروف
        if probability > 0.8:
            return max(1, int(base_time * 0.5))
        elif probability > 0.6:
            return max(2, int(base_time * 0.7))
        elif probability > 0.4:
            return int(base_time)
        else:
            return int(base_time * 1.5)
    
    def _identify_contributing_factors(self, env_data: EnvironmentalData,
                                     plant_data: PlantGeneticData,
                                     disease_name: str) -> List[Dict[str, Any]]:
        """تحديد العوامل المساهمة في المخاطر"""
        factors = []
        
        # العوامل البيئية
        if env_data.humidity > 80:
            factors.append({
                "factor": "رطوبة عالية",
                "value": env_data.humidity,
                "impact": "عالي",
                "description": "الرطوبة العالية تزيد من خطر الأمراض الفطرية"
            })
        
        if env_data.temperature > 30:
            factors.append({
                "factor": "درجة حرارة عالية",
                "value": env_data.temperature,
                "impact": "متوسط",
                "description": "درجات الحرارة العالية قد تضعف مقاومة النبات"
            })
        
        if env_data.rainfall > 20:
            factors.append({
                "factor": "هطول أمطار غزير",
                "value": env_data.rainfall,
                "impact": "عالي",
                "description": "الأمطار الغزيرة تزيد من انتشار الأمراض"
            })
        
        # العوامل الوراثية
        if len(plant_data.susceptibility_factors) > len(plant_data.resistance_genes):
            factors.append({
                "factor": "قابلية وراثية للإصابة",
                "value": len(plant_data.susceptibility_factors),
                "impact": "عالي",
                "description": "الصنف لديه قابلية وراثية عالية للإصابة"
            })
        
        return factors
    
    def _generate_recommendations(self, risk_level: RiskLevel, disease_name: str,
                                contributing_factors: List[Dict[str, Any]]) -> List[str]:
        """توليد توصيات الإجراءات"""
        recommendations = []
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.VERY_HIGH, RiskLevel.CRITICAL]:
            recommendations.extend([
                "تطبيق مبيد فطري وقائي فوراً",
                "زيادة تهوية المحصول",
                "تقليل الري لتجنب الرطوبة الزائدة",
                "مراقبة يومية للنباتات"
            ])
        
        elif risk_level == RiskLevel.MODERATE:
            recommendations.extend([
                "مراقبة دورية للنباتات",
                "تحسين التهوية",
                "تجنب الري المفرط",
                "تحضير المبيدات الوقائية"
            ])
        
        # توصيات خاصة بالمرض
        disease_specific = {
            "تبقع الأوراق": [
                "إزالة الأوراق المصابة",
                "تجنب الري بالرش",
                "تطبيق مبيد نحاسي"
            ],
            "البياض الدقيقي": [
                "تحسين دوران الهواء",
                "تجنب الإفراط في التسميد النيتروجيني",
                "استخدام الكبريت الزراعي"
            ],
            "الذبول البكتيري": [
                "تحسين الصرف",
                "تجنب الجروح في الجذور",
                "استخدام مبيد بكتيري"
            ]
        }
        
        if disease_name in disease_specific:
            recommendations.extend(disease_specific[disease_name])
        
        return recommendations
    
    def _create_default_prediction(self, plant_id: str, disease_name: str) -> DiseaseRiskPrediction:
        """إنشاء تنبؤ افتراضي في حالة الخطأ"""
        return DiseaseRiskPrediction(
            prediction_id=f"default_{int(datetime.now().timestamp())}",
            plant_id=plant_id,
            disease_name=disease_name,
            risk_level=RiskLevel.LOW,
            probability=0.2,
            confidence=0.3,
            time_to_onset=14,
            contributing_factors=[],
            recommended_actions=["مراقبة دورية للنباتات"],
            prediction_timestamp=datetime.now(),
            model_used=PredictionModel.ENSEMBLE_RISK,
            environmental_snapshot=None
        )

class EarlyWarningSystem:
    """نظام الإنذار المبكر"""
    
    def __init__(self):
        self.active_alerts = {}
        self.alert_history = []
        self.notification_channels = []
        self.alert_rules = self._setup_alert_rules()
        
        # إعدادات التنبيهات
        self.alert_thresholds = {
            RiskLevel.MODERATE: 0.4,
            RiskLevel.HIGH: 0.6,
            RiskLevel.VERY_HIGH: 0.8,
            RiskLevel.CRITICAL: 0.9
        }
    
    def _setup_alert_rules(self) -> Dict[str, Any]:
        """إعداد قواعد التنبيهات"""
        return {
            "disease_outbreak": {
                "threshold": 0.7,
                "affected_area_min": 5,  # هكتار
                "time_window": 24  # ساعة
            },
            "weather_extreme": {
                "temperature_max": 40,
                "temperature_min": 0,
                "humidity_max": 95,
                "rainfall_max": 100,
                "wind_speed_max": 50
            },
            "pest_risk": {
                "threshold": 0.6,
                "population_density": 10  # آفات/م²
            }
        }
    
    async def evaluate_alert_conditions(self, predictions: List[DiseaseRiskPrediction],
                                      environmental_data: EnvironmentalData,
                                      area_info: Dict[str, Any]) -> List[EarlyWarningAlert]:
        """تقييم شروط التنبيه"""
        alerts = []
        
        try:
            # تقييم مخاطر الأمراض
            disease_alerts = await self._evaluate_disease_alerts(predictions, area_info)
            alerts.extend(disease_alerts)
            
            # تقييم التحذيرات الجوية
            weather_alerts = await self._evaluate_weather_alerts(environmental_data, area_info)
            alerts.extend(weather_alerts)
            
            # تقييم مخاطر الآفات
            pest_alerts = await self._evaluate_pest_alerts(environmental_data, area_info)
            alerts.extend(pest_alerts)
            
            # تقييم تنبيهات الري
            irrigation_alerts = await self._evaluate_irrigation_alerts(environmental_data, area_info)
            alerts.extend(irrigation_alerts)
            
            # حفظ التنبيهات النشطة
            for alert in alerts:
                self.active_alerts[alert.alert_id] = alert
                self.alert_history.append(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"خطأ في تقييم شروط التنبيه: {e}")
            return []
    
    async def _evaluate_disease_alerts(self, predictions: List[DiseaseRiskPrediction],
                                     area_info: Dict[str, Any]) -> List[EarlyWarningAlert]:
        """تقييم تنبيهات الأمراض"""
        alerts = []
        
        # تجميع التنبؤات حسب المرض
        disease_predictions = defaultdict(list)
        for pred in predictions:
            disease_predictions[pred.disease_name].append(pred)
        
        for disease, preds in disease_predictions.items():
            # حساب متوسط المخاطر
            avg_probability = np.mean([p.probability for p in preds])
            high_risk_count = sum(1 for p in preds if p.risk_level.value in ['high', 'very_high', 'critical'])
            
            # فحص شروط التنبيه
            if (avg_probability >= self.alert_thresholds[RiskLevel.HIGH] or
                high_risk_count >= len(preds) * 0.3):  # 30% من النباتات في خطر عالي
                
                severity = self._determine_alert_severity(avg_probability)
                
                alert = EarlyWarningAlert(
                    alert_id=f"disease_{disease}_{int(datetime.now().timestamp())}",
                    alert_type=AlertType.DISEASE_RISK,
                    severity=severity,
                    title=f"تحذير من خطر {disease}",
                    message=f"تم رصد خطر عالي للإصابة بـ {disease} في المنطقة. "
                           f"متوسط الاحتمالية: {avg_probability:.1%}",
                    affected_area=area_info,
                    affected_crops=list(set(p.plant_id for p in preds)),
                    time_window={
                        "start_time": datetime.now(),
                        "end_time": datetime.now() + timedelta(days=7)
                    },
                    recommended_actions=self._get_disease_alert_actions(disease, severity),
                    created_at=datetime.now(),
                    expires_at=datetime.now() + timedelta(days=7)
                )
                
                alerts.append(alert)
        
        return alerts
    
    async def _evaluate_weather_alerts(self, env_data: EnvironmentalData,
                                     area_info: Dict[str, Any]) -> List[EarlyWarningAlert]:
        """تقييم التحذيرات الجوية"""
        alerts = []
        rules = self.alert_rules["weather_extreme"]
        
        # فحص درجات الحرارة القصوى
        if env_data.temperature >= rules["temperature_max"]:
            alert = EarlyWarningAlert(
                alert_id=f"weather_heat_{int(datetime.now().timestamp())}",
                alert_type=AlertType.WEATHER_WARNING,
                severity=RiskLevel.HIGH,
                title="تحذير من موجة حر",
                message=f"درجة الحرارة المتوقعة {env_data.temperature}°م قد تضر بالمحاصيل",
                affected_area=area_info,
                affected_crops=["جميع المحاصيل"],
                time_window={
                    "start_time": datetime.now(),
                    "end_time": datetime.now() + timedelta(days=3)
                },
                recommended_actions=[
                    "زيادة الري",
                    "توفير الظل للنباتات الحساسة",
                    "تجنب العمليات الزراعية في ساعات الذروة"
                ],
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=3)
            )
            alerts.append(alert)
        
        # فحص الأمطار الغزيرة
        if env_data.rainfall >= rules["rainfall_max"]:
            alert = EarlyWarningAlert(
                alert_id=f"weather_rain_{int(datetime.now().timestamp())}",
                alert_type=AlertType.WEATHER_WARNING,
                severity=RiskLevel.HIGH,
                title="تحذير من أمطار غزيرة",
                message=f"هطول أمطار متوقع {env_data.rainfall}مم قد يسبب فيضانات",
                affected_area=area_info,
                affected_crops=["جميع المحاصيل"],
                time_window={
                    "start_time": datetime.now(),
                    "end_time": datetime.now() + timedelta(days=2)
                },
                recommended_actions=[
                    "تحسين الصرف",
                    "حماية النباتات الصغيرة",
                    "تأجيل عمليات الرش"
                ],
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=2)
            )
            alerts.append(alert)
        
        return alerts
    
    async def _evaluate_pest_alerts(self, env_data: EnvironmentalData,
                                  area_info: Dict[str, Any]) -> List[EarlyWarningAlert]:
        """تقييم تنبيهات الآفات"""
        alerts = []
        
        # محاكاة تقييم مخاطر الآفات
        pest_risk = self._calculate_pest_risk(env_data)
        
        if pest_risk >= self.alert_rules["pest_risk"]["threshold"]:
            alert = EarlyWarningAlert(
                alert_id=f"pest_risk_{int(datetime.now().timestamp())}",
                alert_type=AlertType.PEST_OUTBREAK,
                severity=RiskLevel.HIGH,
                title="تحذير من خطر الآفات",
                message=f"الظروف الجوية مناسبة لتكاثر الآفات (خطر: {pest_risk:.1%})",
                affected_area=area_info,
                affected_crops=["الخضروات الورقية", "الفواكه"],
                time_window={
                    "start_time": datetime.now(),
                    "end_time": datetime.now() + timedelta(days=5)
                },
                recommended_actions=[
                    "مراقبة دورية للآفات",
                    "تحضير المبيدات الحيوية",
                    "تفعيل المصائد الفرمونية"
                ],
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=5)
            )
            alerts.append(alert)
        
        return alerts
    
    async def _evaluate_irrigation_alerts(self, env_data: EnvironmentalData,
                                        area_info: Dict[str, Any]) -> List[EarlyWarningAlert]:
        """تقييم تنبيهات الري"""
        alerts = []
        
        # فحص نقص الرطوبة
        if env_data.soil_moisture < 30:
            alert = EarlyWarningAlert(
                alert_id=f"irrigation_{int(datetime.now().timestamp())}",
                alert_type=AlertType.IRRIGATION_ALERT,
                severity=RiskLevel.MODERATE,
                title="تنبيه نقص رطوبة التربة",
                message=f"رطوبة التربة منخفضة ({env_data.soil_moisture}%) - يحتاج الري",
                affected_area=area_info,
                affected_crops=["جميع المحاصيل"],
                time_window={
                    "start_time": datetime.now(),
                    "end_time": datetime.now() + timedelta(days=1)
                },
                recommended_actions=[
                    "بدء الري فوراً",
                    "فحص نظام الري",
                    "مراقبة رطوبة التربة"
                ],
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=1)
            )
            alerts.append(alert)
        
        return alerts
    
    def _calculate_pest_risk(self, env_data: EnvironmentalData) -> float:
        """حساب مخاطر الآفات"""
        risk = 0.0
        
        # درجة الحرارة المثلى للآفات (20-30°م)
        if 20 <= env_data.temperature <= 30:
            risk += 0.3
        
        # الرطوبة المثلى (60-80%)
        if 60 <= env_data.humidity <= 80:
            risk += 0.3
        
        # الرياح الخفيفة تساعد على انتشار الآفات
        if env_data.wind_speed < 10:
            risk += 0.2
        
        # الأمطار المعتدلة
        if 5 <= env_data.rainfall <= 20:
            risk += 0.2
        
        return min(risk, 1.0)
    
    def _determine_alert_severity(self, probability: float) -> RiskLevel:
        """تحديد شدة التنبيه"""
        if probability >= 0.9:
            return RiskLevel.CRITICAL
        elif probability >= 0.7:
            return RiskLevel.VERY_HIGH
        elif probability >= 0.5:
            return RiskLevel.HIGH
        else:
            return RiskLevel.MODERATE
    
    def _get_disease_alert_actions(self, disease: str, severity: RiskLevel) -> List[str]:
        """الحصول على إجراءات تنبيه المرض"""
        base_actions = [
            "مراقبة مكثفة للنباتات",
            "تحضير المبيدات المناسبة",
            "تحسين التهوية"
        ]
        
        if severity in [RiskLevel.HIGH, RiskLevel.VERY_HIGH, RiskLevel.CRITICAL]:
            base_actions.extend([
                "تطبيق المبيدات الوقائية فوراً",
                "عزل النباتات المشتبه بإصابتها",
                "إبلاغ الخبراء المحليين"
            ])
        
        return base_actions
    
    async def send_alert_notifications(self, alert: EarlyWarningAlert):
        """إرسال إشعارات التنبيه"""
        try:
            # إرسال عبر القنوات المختلفة
            for channel in self.notification_channels:
                await channel.send_notification(alert)
            
            logger.info(f"تم إرسال تنبيه: {alert.title}")
            
        except Exception as e:
            logger.error(f"خطأ في إرسال التنبيه: {e}")
    
    def get_active_alerts(self, area_filter: Dict[str, Any] = None) -> List[EarlyWarningAlert]:
        """الحصول على التنبيهات النشطة"""
        active = []
        current_time = datetime.now()
        
        for alert in self.active_alerts.values():
            if alert.expires_at > current_time and not alert.resolved:
                if area_filter is None or self._alert_matches_area(alert, area_filter):
                    active.append(alert)
        
        return active
    
    def _alert_matches_area(self, alert: EarlyWarningAlert, area_filter: Dict[str, Any]) -> bool:
        """فحص تطابق التنبيه مع المنطقة"""
        # تنفيذ مبسط للفحص
        return True
    
    def acknowledge_alert(self, alert_id: str, user_id: str):
        """تأكيد استلام التنبيه"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].acknowledged = True
            logger.info(f"تم تأكيد التنبيه {alert_id} من قبل {user_id}")
    
    def resolve_alert(self, alert_id: str, user_id: str, resolution_notes: str = ""):
        """حل التنبيه"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id].resolved = True
            logger.info(f"تم حل التنبيه {alert_id} من قبل {user_id}")

class PredictiveDiagnosisSystem:
    """النظام الرئيسي للتشخيص الاستباقي"""
    
    def __init__(self, database_path: str = "predictive_diagnosis.db"):
        self.database_path = database_path
        self.weather_collector = WeatherDataCollector()
        self.disease_model = DiseaseRiskModel()
        self.warning_system = EarlyWarningSystem()
        
        # قوائم انتظار المعالجة
        self.prediction_queue = queue.PriorityQueue()
        self.alert_queue = queue.Queue()
        
        # إحصائيات النظام
        self.system_stats = {
            "total_predictions": 0,
            "active_alerts": 0,
            "accuracy_rate": 0.0,
            "false_positive_rate": 0.0
        }
        
        # إعداد قاعدة البيانات
        self._setup_database()
        
        # حالة النظام
        self.is_running = False
        self.background_threads = []
    
    def _setup_database(self):
        """إعداد قاعدة البيانات"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # جدول التنبؤات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    prediction_id TEXT PRIMARY KEY,
                    plant_id TEXT,
                    disease_name TEXT,
                    risk_level TEXT,
                    probability REAL,
                    confidence REAL,
                    time_to_onset INTEGER,
                    contributing_factors TEXT,
                    recommended_actions TEXT,
                    prediction_timestamp TEXT,
                    model_used TEXT,
                    environmental_data TEXT,
                    actual_outcome TEXT,
                    outcome_timestamp TEXT
                )
            ''')
            
            # جدول التنبيهات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    alert_id TEXT PRIMARY KEY,
                    alert_type TEXT,
                    severity TEXT,
                    title TEXT,
                    message TEXT,
                    affected_area TEXT,
                    affected_crops TEXT,
                    time_window TEXT,
                    recommended_actions TEXT,
                    created_at TEXT,
                    expires_at TEXT,
                    acknowledged BOOLEAN DEFAULT FALSE,
                    resolved BOOLEAN DEFAULT FALSE,
                    resolution_notes TEXT
                )
            ''')
            
            # جدول البيانات البيئية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS environmental_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    location TEXT,
                    temperature REAL,
                    humidity REAL,
                    rainfall REAL,
                    wind_speed REAL,
                    wind_direction REAL,
                    pressure REAL,
                    solar_radiation REAL,
                    soil_temperature REAL,
                    soil_moisture REAL,
                    soil_ph REAL,
                    uv_index REAL
                )
            ''')
            
            # جدول بيانات النباتات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS plant_data (
                    plant_id TEXT PRIMARY KEY,
                    variety TEXT,
                    genetic_markers TEXT,
                    resistance_genes TEXT,
                    susceptibility_factors TEXT,
                    growth_stage TEXT,
                    age_days INTEGER,
                    health_history TEXT,
                    location TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("تم إعداد قاعدة بيانات التشخيص الاستباقي")
            
        except Exception as e:
            logger.error(f"خطأ في إعداد قاعدة البيانات: {e}")
            raise
    
    def start_system(self):
        """بدء النظام"""
        if not self.is_running:
            self.is_running = True
            
            # بدء خيوط المعالجة
            prediction_thread = threading.Thread(target=self._process_predictions)
            alert_thread = threading.Thread(target=self._process_alerts)
            monitoring_thread = threading.Thread(target=self._monitor_system)
            
            self.background_threads = [prediction_thread, alert_thread, monitoring_thread]
            
            for thread in self.background_threads:
                thread.start()
            
            logger.info("تم بدء نظام التشخيص الاستباقي")
    
    def stop_system(self):
        """إيقاف النظام"""
        self.is_running = False
        
        for thread in self.background_threads:
            thread.join()
        
        logger.info("تم إيقاف نظام التشخيص الاستباقي")
    
    def _process_predictions(self):
        """معالجة التنبؤات في الخلفية"""
        while self.is_running:
            try:
                priority, prediction_task = self.prediction_queue.get(timeout=1)
                asyncio.run(self._handle_prediction_task(prediction_task))
                self.prediction_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"خطأ في معالجة التنبؤ: {e}")
    
    def _process_alerts(self):
        """معالجة التنبيهات في الخلفية"""
        while self.is_running:
            try:
                alert_task = self.alert_queue.get(timeout=1)
                asyncio.run(self._handle_alert_task(alert_task))
                self.alert_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"خطأ في معالجة التنبيه: {e}")
    
    def _monitor_system(self):
        """مراقبة النظام"""
        while self.is_running:
            try:
                self._update_system_stats()
                time.sleep(60)  # تحديث كل دقيقة
                
            except Exception as e:
                logger.error(f"خطأ في مراقبة النظام: {e}")
                time.sleep(60)
    
    async def predict_disease_risks(self, plant_ids: List[str], 
                                  location: Dict[str, float],
                                  diseases: List[str] = None) -> List[DiseaseRiskPrediction]:
        """التنبؤ بمخاطر الأمراض لمجموعة من النباتات"""
        try:
            # جمع البيانات البيئية
            env_data = await self.weather_collector.collect_environmental_data(location)
            
            # حفظ البيانات البيئية
            await self._save_environmental_data(env_data)
            
            predictions = []
            
            for plant_id in plant_ids:
                # الحصول على بيانات النبات
                plant_data = await self._get_plant_data(plant_id)
                if not plant_data:
                    continue
                
                # تحديد الأمراض للتنبؤ
                target_diseases = diseases or ["تبقع الأوراق", "البياض الدقيقي", "الذبول البكتيري"]
                
                for disease in target_diseases:
                    # التنبؤ بخطر المرض
                    prediction = await self.disease_model.predict_disease_risk(
                        env_data, plant_data, disease
                    )
                    
                    predictions.append(prediction)
                    
                    # حفظ التنبؤ
                    await self._save_prediction(prediction)
            
            # تقييم شروط التنبيه
            area_info = {"location": location, "area_size": len(plant_ids)}
            alerts = await self.warning_system.evaluate_alert_conditions(
                predictions, env_data, area_info
            )
            
            # إضافة التنبيهات لقائمة المعالجة
            for alert in alerts:
                self.alert_queue.put(alert)
            
            # تحديث الإحصائيات
            self.system_stats["total_predictions"] += len(predictions)
            
            return predictions
            
        except Exception as e:
            logger.error(f"خطأ في التنبؤ بمخاطر الأمراض: {e}")
            return []
    
    async def get_area_risk_assessment(self, area_bounds: Dict[str, float],
                                     time_horizon: int = 7) -> Dict[str, Any]:
        """تقييم مخاطر منطقة جغرافية"""
        try:
            # جمع البيانات للمنطقة
            center_location = {
                "lat": (area_bounds["north"] + area_bounds["south"]) / 2,
                "lon": (area_bounds["east"] + area_bounds["west"]) / 2
            }
            
            env_data = await self.weather_collector.collect_environmental_data(center_location)
            
            # الحصول على النباتات في المنطقة
            plants_in_area = await self._get_plants_in_area(area_bounds)
            
            # التنبؤ بالمخاطر
            all_predictions = []
            if plants_in_area:
                predictions = await self.predict_disease_risks(
                    [p["plant_id"] for p in plants_in_area],
                    center_location
                )
                all_predictions.extend(predictions)
            
            # تحليل المخاطر
            risk_analysis = self._analyze_area_risks(all_predictions, env_data)
            
            # التنبيهات النشطة
            active_alerts = self.warning_system.get_active_alerts(area_bounds)
            
            return {
                "area_bounds": area_bounds,
                "assessment_time": datetime.now().isoformat(),
                "time_horizon_days": time_horizon,
                "environmental_conditions": asdict(env_data),
                "plants_count": len(plants_in_area),
                "predictions_count": len(all_predictions),
                "risk_analysis": risk_analysis,
                "active_alerts": [asdict(alert) for alert in active_alerts],
                "recommendations": self._generate_area_recommendations(risk_analysis, active_alerts)
            }
            
        except Exception as e:
            logger.error(f"خطأ في تقييم مخاطر المنطقة: {e}")
            return {}
    
    def _analyze_area_risks(self, predictions: List[DiseaseRiskPrediction],
                          env_data: EnvironmentalData) -> Dict[str, Any]:
        """تحليل مخاطر المنطقة"""
        if not predictions:
            return {"overall_risk": "منخفض", "disease_risks": {}}
        
        # تجميع المخاطر حسب المرض
        disease_risks = defaultdict(list)
        for pred in predictions:
            disease_risks[pred.disease_name].append(pred.probability)
        
        # حساب المخاطر لكل مرض
        disease_analysis = {}
        for disease, probabilities in disease_risks.items():
            disease_analysis[disease] = {
                "average_probability": np.mean(probabilities),
                "max_probability": np.max(probabilities),
                "affected_plants_count": len(probabilities),
                "high_risk_plants": sum(1 for p in probabilities if p >= 0.6)
            }
        
        # تحديد المخاطر الإجمالية
        all_probabilities = [pred.probability for pred in predictions]
        avg_risk = np.mean(all_probabilities)
        
        if avg_risk >= 0.7:
            overall_risk = "عالي جداً"
        elif avg_risk >= 0.5:
            overall_risk = "عالي"
        elif avg_risk >= 0.3:
            overall_risk = "متوسط"
        else:
            overall_risk = "منخفض"
        
        return {
            "overall_risk": overall_risk,
            "average_probability": avg_risk,
            "disease_risks": disease_analysis,
            "environmental_factors": {
                "temperature_risk": "عالي" if env_data.temperature > 30 else "منخفض",
                "humidity_risk": "عالي" if env_data.humidity > 80 else "منخفض",
                "rainfall_risk": "عالي" if env_data.rainfall > 20 else "منخفض"
            }
        }
    
    def _generate_area_recommendations(self, risk_analysis: Dict[str, Any],
                                     active_alerts: List[EarlyWarningAlert]) -> List[str]:
        """توليد توصيات للمنطقة"""
        recommendations = []
        
        overall_risk = risk_analysis.get("overall_risk", "منخفض")
        
        if overall_risk in ["عالي", "عالي جداً"]:
            recommendations.extend([
                "تطبيق برنامج مكافحة وقائية شامل",
                "زيادة تكرار المراقبة والتفتيش",
                "تحضير المبيدات والأدوات اللازمة",
                "تنسيق مع المزارعين المجاورين"
            ])
        
        elif overall_risk == "متوسط":
            recommendations.extend([
                "مراقبة دورية للنباتات",
                "تحضير خطة المكافحة",
                "تحسين الظروف البيئية"
            ])
        
        # توصيات خاصة بالتنبيهات النشطة
        for alert in active_alerts:
            recommendations.extend(alert.recommended_actions)
        
        return list(set(recommendations))  # إزالة التكرار
    
    async def _handle_prediction_task(self, task: Dict[str, Any]):
        """معالجة مهمة التنبؤ"""
        try:
            # تنفيذ مهمة التنبؤ
            task_type = task.get("type")
            
            if task_type == "batch_prediction":
                await self.predict_disease_risks(
                    task["plant_ids"],
                    task["location"],
                    task.get("diseases")
                )
            
            elif task_type == "area_assessment":
                await self.get_area_risk_assessment(
                    task["area_bounds"],
                    task.get("time_horizon", 7)
                )
            
        except Exception as e:
            logger.error(f"خطأ في معالجة مهمة التنبؤ: {e}")
    
    async def _handle_alert_task(self, alert: EarlyWarningAlert):
        """معالجة مهمة التنبيه"""
        try:
            # حفظ التنبيه
            await self._save_alert(alert)
            
            # إرسال الإشعارات
            await self.warning_system.send_alert_notifications(alert)
            
        except Exception as e:
            logger.error(f"خطأ في معالجة التنبيه: {e}")
    
    def _update_system_stats(self):
        """تحديث إحصائيات النظام"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # عدد التنبؤات الإجمالي
            cursor.execute("SELECT COUNT(*) FROM predictions")
            self.system_stats["total_predictions"] = cursor.fetchone()[0]
            
            # التنبيهات النشطة
            cursor.execute("SELECT COUNT(*) FROM alerts WHERE resolved = FALSE")
            self.system_stats["active_alerts"] = cursor.fetchone()[0]
            
            # حساب معدل الدقة (مبسط)
            cursor.execute("""
                SELECT COUNT(*) FROM predictions 
                WHERE actual_outcome IS NOT NULL
            """)
            total_verified = cursor.fetchone()[0]
            
            if total_verified > 0:
                cursor.execute("""
                    SELECT COUNT(*) FROM predictions 
                    WHERE actual_outcome IS NOT NULL 
                    AND ((probability >= 0.5 AND actual_outcome = 'infected') 
                         OR (probability < 0.5 AND actual_outcome = 'healthy'))
                """)
                correct_predictions = cursor.fetchone()[0]
                self.system_stats["accuracy_rate"] = correct_predictions / total_verified
            
            conn.close()
            
        except Exception as e:
            logger.error(f"خطأ في تحديث الإحصائيات: {e}")
    
    # دوال قاعدة البيانات المساعدة
    async def _save_environmental_data(self, env_data: EnvironmentalData):
        """حفظ البيانات البيئية"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO environmental_data 
                (timestamp, location, temperature, humidity, rainfall, wind_speed,
                 wind_direction, pressure, solar_radiation, soil_temperature,
                 soil_moisture, soil_ph, uv_index)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                env_data.timestamp.isoformat(),
                json.dumps(env_data.location),
                env_data.temperature, env_data.humidity, env_data.rainfall,
                env_data.wind_speed, env_data.wind_direction, env_data.pressure,
                env_data.solar_radiation, env_data.soil_temperature,
                env_data.soil_moisture, env_data.soil_ph, env_data.uv_index
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"خطأ في حفظ البيانات البيئية: {e}")
    
    async def _save_prediction(self, prediction: DiseaseRiskPrediction):
        """حفظ التنبؤ"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO predictions 
                (prediction_id, plant_id, disease_name, risk_level, probability,
                 confidence, time_to_onset, contributing_factors, recommended_actions,
                 prediction_timestamp, model_used, environmental_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prediction.prediction_id, prediction.plant_id, prediction.disease_name,
                prediction.risk_level.value, prediction.probability, prediction.confidence,
                prediction.time_to_onset, json.dumps(prediction.contributing_factors),
                json.dumps(prediction.recommended_actions),
                prediction.prediction_timestamp.isoformat(),
                prediction.model_used.value,
                json.dumps(asdict(prediction.environmental_snapshot)) if prediction.environmental_snapshot else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"خطأ في حفظ التنبؤ: {e}")
    
    async def _save_alert(self, alert: EarlyWarningAlert):
        """حفظ التنبيه"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO alerts 
                (alert_id, alert_type, severity, title, message, affected_area,
                 affected_crops, time_window, recommended_actions, created_at,
                 expires_at, acknowledged, resolved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert.alert_id, alert.alert_type.value, alert.severity.value,
                alert.title, alert.message, json.dumps(alert.affected_area),
                json.dumps(alert.affected_crops), json.dumps({
                    "start_time": alert.time_window["start_time"].isoformat(),
                    "end_time": alert.time_window["end_time"].isoformat()
                }),
                json.dumps(alert.recommended_actions),
                alert.created_at.isoformat(), alert.expires_at.isoformat(),
                alert.acknowledged, alert.resolved
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"خطأ في حفظ التنبيه: {e}")
    
    async def _get_plant_data(self, plant_id: str) -> Optional[PlantGeneticData]:
        """الحصول على بيانات النبات"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM plant_data WHERE plant_id = ?", (plant_id,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return PlantGeneticData(
                    plant_id=row[0],
                    variety=row[1],
                    genetic_markers=json.loads(row[2]) if row[2] else [],
                    resistance_genes=json.loads(row[3]) if row[3] else [],
                    susceptibility_factors=json.loads(row[4]) if row[4] else [],
                    growth_stage=row[5],
                    age_days=row[6],
                    health_history=json.loads(row[7]) if row[7] else []
                )
            
            # إنشاء بيانات افتراضية إذا لم توجد
            return PlantGeneticData(
                plant_id=plant_id,
                variety="غير محدد",
                genetic_markers=[],
                resistance_genes=[],
                susceptibility_factors=[],
                growth_stage="vegetative",
                age_days=30,
                health_history=[]
            )
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على بيانات النبات: {e}")
            return None
    
    async def _get_plants_in_area(self, area_bounds: Dict[str, float]) -> List[Dict[str, Any]]:
        """الحصول على النباتات في منطقة معينة"""
        try:
            # محاكاة البحث في المنطقة
            # في التطبيق الحقيقي، سيتم البحث في قاعدة البيانات الجغرافية
            
            sample_plants = []
            for i in range(10):  # 10 نباتات للمحاكاة
                sample_plants.append({
                    "plant_id": f"plant_{i+1}",
                    "location": {
                        "lat": np.random.uniform(area_bounds["south"], area_bounds["north"]),
                        "lon": np.random.uniform(area_bounds["west"], area_bounds["east"])
                    }
                })
            
            return sample_plants
            
        except Exception as e:
            logger.error(f"خطأ في البحث عن النباتات في المنطقة: {e}")
            return []
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات النظام"""
        return {
            **self.system_stats,
            "prediction_queue_size": self.prediction_queue.qsize(),
            "alert_queue_size": self.alert_queue.qsize(),
            "system_uptime": "متاح" if self.is_running else "متوقف"
        }

# إنشاء مثيل عام للنظام
predictive_system = PredictiveDiagnosisSystem()

# دوال مساعدة للاستخدام السهل
async def predict_plant_disease_risk(plant_id: str, location: Dict[str, float],
                                   disease: str = None) -> DiseaseRiskPrediction:
    """التنبؤ بخطر مرض لنبات واحد"""
    diseases = [disease] if disease else None
    predictions = await predictive_system.predict_disease_risks([plant_id], location, diseases)
    return predictions[0] if predictions else None

async def get_farm_risk_assessment(farm_bounds: Dict[str, float]) -> Dict[str, Any]:
    """تقييم مخاطر مزرعة"""
    return await predictive_system.get_area_risk_assessment(farm_bounds)

async def get_weather_based_alerts(location: Dict[str, float]) -> List[EarlyWarningAlert]:
    """الحصول على تنبيهات مبنية على الطقس"""
    env_data = await predictive_system.weather_collector.collect_environmental_data(location)
    area_info = {"location": location}
    return await predictive_system.warning_system._evaluate_weather_alerts(env_data, area_info)

if __name__ == "__main__":
    # اختبار النظام
    async def test_predictive_system():
        predictive_system.start_system()
        
        # اختبار التنبؤ
        test_location = {"lat": 30.0444, "lon": 31.2357}  # القاهرة
        
        prediction = await predict_plant_disease_risk(
            "test_plant_1", 
            test_location, 
            "تبقع الأوراق"
        )
        
        if prediction:
            print(f"التنبؤ: {prediction.disease_name}")
            print(f"مستوى المخاطر: {prediction.risk_level.value}")
            print(f"الاحتمالية: {prediction.probability:.2%}")
            print(f"الثقة: {prediction.confidence:.2%}")
        
        # اختبار تقييم المزرعة
        farm_bounds = {
            "north": 30.1,
            "south": 30.0,
            "east": 31.3,
            "west": 31.2
        }
        
        assessment = await get_farm_risk_assessment(farm_bounds)
        print(f"تقييم المزرعة: {assessment.get('risk_analysis', {}).get('overall_risk', 'غير متاح')}")
        
        # إحصائيات النظام
        stats = predictive_system.get_system_statistics()
        print(f"إحصائيات النظام: {stats}")
        
        await asyncio.sleep(2)
        predictive_system.stop_system()
    
    # تشغيل الاختبار
    asyncio.run(test_predictive_system())

