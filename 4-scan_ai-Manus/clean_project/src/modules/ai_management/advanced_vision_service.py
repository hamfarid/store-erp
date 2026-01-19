# File: /home/ubuntu/clean_project/src/modules/ai_management/advanced_vision_service.py
"""
خدمة الرؤية المتقدمة
تتضمن Vision Transformers، التصوير فائق الطيف، والتصوير ثلاثي الأبعاد
"""

import os
import json
import logging
import asyncio
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import (
    ViTImageProcessor, ViTForImageClassification,
    DeiTImageProcessor, DeiTForImageClassification,
    AutoImageProcessor, AutoModelForImageClassification
)
import cv2
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
from datetime import datetime
from typing import Dict, List, Optional, Union, Any, Tuple
import threading
import queue
from dataclasses import dataclass
import spectral
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import open3d as o3d

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VisionRequest:
    """طلب الرؤية المتقدمة"""
    request_id: str
    request_type: str  # 'classification', 'hyperspectral', '3d_analysis', 'multi_analysis'
    image_data: Union[bytes, np.ndarray]
    parameters: Dict[str, Any]
    user_id: str
    timestamp: datetime
    priority: int = 1

@dataclass
class VisionResponse:
    """استجابة الرؤية المتقدمة"""
    request_id: str
    response_type: str
    results: Dict[str, Any]
    confidence_scores: Dict[str, float]
    processing_time: float
    model_used: str
    timestamp: datetime

class VisionTransformerManager:
    """مدير نماذج Vision Transformer"""
    
    def __init__(self):
        self.models = {}
        self.processors = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_models()
    
    def load_models(self):
        """تحميل نماذج Vision Transformer"""
        try:
            # نموذج ViT للتصنيف العام
            vit_model_name = "google/vit-base-patch16-224"
            self.processors['vit_general'] = ViTImageProcessor.from_pretrained(vit_model_name)
            self.models['vit_general'] = ViTForImageClassification.from_pretrained(vit_model_name)
            
            # نموذج DeiT للتصنيف المحسن
            deit_model_name = "facebook/deit-base-distilled-patch16-224"
            self.processors['deit'] = DeiTImageProcessor.from_pretrained(deit_model_name)
            self.models['deit'] = DeiTForImageClassification.from_pretrained(deit_model_name)
            
            # نموذج مخصص لأمراض النباتات (محاكاة)
            self.models['plant_disease'] = self._create_plant_disease_model()
            
            # نقل النماذج إلى الجهاز المناسب
            for model_name, model in self.models.items():
                if hasattr(model, 'to'):
                    model.to(self.device)
            
            logger.info("تم تحميل نماذج Vision Transformer بنجاح")
            
        except Exception as e:
            logger.error(f"خطأ في تحميل نماذج Vision Transformer: {e}")
    
    def _create_plant_disease_model(self):
        """إنشاء نموذج مخصص لأمراض النباتات"""
        # نموذج مبسط للمحاكاة - يمكن استبداله بنموذج مدرب فعلياً
        class PlantDiseaseViT(nn.Module):
            def __init__(self, num_classes=50):  # 50 نوع مرض مختلف
                super().__init__()
                # استخدام ViT كأساس
                self.backbone = ViTForImageClassification.from_pretrained(
                    "google/vit-base-patch16-224",
                    num_labels=num_classes,
                    ignore_mismatched_sizes=True
                )
                
                # طبقات إضافية للتخصص في أمراض النباتات
                self.disease_classifier = nn.Sequential(
                    nn.Linear(768, 512),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(512, 256),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(256, num_classes)
                )
                
                # قائمة أمراض النباتات المدعومة
                self.disease_classes = [
                    "صحي", "تبقع الأوراق", "الصدأ", "البياض الدقيقي", "العفن الرمادي",
                    "تعفن الجذور", "فيروس الموزاييك", "البكتيريا الناعمة", "النيماتودا",
                    "حشرة المن", "الذبابة البيضاء", "العنكبوت الأحمر", "دودة الأوراق",
                    "نقص النيتروجين", "نقص الفوسفور", "نقص البوتاسيوم", "نقص الحديد",
                    "زيادة الري", "نقص الري", "حروق الشمس", "الصقيع", "ملوحة التربة",
                    "حموضة التربة", "نقص الأكسجين", "تلوث كيميائي", "إجهاد حراري",
                    "إجهاد مائي", "تلف ميكانيكي", "شيخوخة طبيعية", "طفرة وراثية",
                    "تلوث هوائي", "إشعاع زائد", "نقص الضوء", "رطوبة عالية",
                    "رطوبة منخفضة", "تغيرات مناخية", "تلوث التربة", "نقص المغذيات",
                    "زيادة الأسمدة", "تسمم معدني", "فطريات التربة", "بكتيريا التربة",
                    "فيروسات النبات", "مرض وراثي", "تشوه خلقي", "إصابة حشرية",
                    "إصابة فطرية", "إصابة بكتيرية", "إصابة فيروسية", "مرض مجهول"
                ]
            
            def forward(self, pixel_values):
                # استخراج الميزات من ViT
                outputs = self.backbone.vit(pixel_values)
                sequence_output = outputs.last_hidden_state
                
                # استخدام رمز التصنيف [CLS]
                cls_token = sequence_output[:, 0]
                
                # التصنيف النهائي
                logits = self.disease_classifier(cls_token)
                
                return {"logits": logits}
        
        return PlantDiseaseViT()
    
    async def classify_image(self, image_data: Union[bytes, np.ndarray], 
                           model_type: str = "vit_general") -> Dict[str, Any]:
        """تصنيف الصورة باستخدام Vision Transformer"""
        try:
            # تحويل البيانات إلى صورة PIL
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data)).convert('RGB')
            elif isinstance(image_data, np.ndarray):
                image = Image.fromarray(image_data).convert('RGB')
            else:
                raise ValueError("نوع بيانات الصورة غير مدعوم")
            
            if model_type not in self.models:
                raise ValueError(f"نوع النموذج غير مدعوم: {model_type}")
            
            model = self.models[model_type]
            
            # معالجة خاصة للنموذج المخصص
            if model_type == "plant_disease":
                return await self._classify_plant_disease(image, model)
            
            # معالجة النماذج العامة
            processor = self.processors[model_type]
            inputs = processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # استخراج النتائج
            predicted_class_idx = predictions.argmax().item()
            confidence = predictions.max().item()
            
            # الحصول على أسماء الفئات
            if hasattr(model.config, 'id2label'):
                class_name = model.config.id2label[predicted_class_idx]
            else:
                class_name = f"فئة_{predicted_class_idx}"
            
            # أفضل 5 تنبؤات
            top5_indices = predictions.argsort(descending=True)[0][:5]
            top5_predictions = []
            
            for idx in top5_indices:
                idx_item = idx.item()
                if hasattr(model.config, 'id2label'):
                    label = model.config.id2label[idx_item]
                else:
                    label = f"فئة_{idx_item}"
                
                top5_predictions.append({
                    "label": label,
                    "confidence": predictions[0][idx_item].item()
                })
            
            return {
                "predicted_class": class_name,
                "confidence": confidence,
                "top5_predictions": top5_predictions,
                "model_used": model_type
            }
            
        except Exception as e:
            logger.error(f"خطأ في تصنيف الصورة: {e}")
            raise
    
    async def _classify_plant_disease(self, image: Image.Image, model) -> Dict[str, Any]:
        """تصنيف أمراض النباتات باستخدام النموذج المخصص"""
        try:
            # معالجة الصورة للنموذج المخصص
            processor = self.processors['vit_general']  # استخدام معالج ViT العام
            inputs = processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(inputs['pixel_values'])
                predictions = torch.nn.functional.softmax(outputs['logits'], dim=-1)
            
            # استخراج النتائج
            predicted_class_idx = predictions.argmax().item()
            confidence = predictions.max().item()
            
            # الحصول على اسم المرض
            disease_name = model.disease_classes[predicted_class_idx]
            
            # أفضل 5 تنبؤات
            top5_indices = predictions.argsort(descending=True)[0][:5]
            top5_predictions = []
            
            for idx in top5_indices:
                idx_item = idx.item()
                top5_predictions.append({
                    "disease": model.disease_classes[idx_item],
                    "confidence": predictions[0][idx_item].item()
                })
            
            # تحليل إضافي للمرض
            disease_analysis = self._analyze_disease_details(disease_name, confidence)
            
            return {
                "predicted_disease": disease_name,
                "confidence": confidence,
                "top5_predictions": top5_predictions,
                "disease_analysis": disease_analysis,
                "model_used": "plant_disease_vit"
            }
            
        except Exception as e:
            logger.error(f"خطأ في تصنيف أمراض النباتات: {e}")
            raise
    
    def _analyze_disease_details(self, disease_name: str, confidence: float) -> Dict[str, Any]:
        """تحليل تفاصيل المرض"""
        # قاعدة معرفة مبسطة للأمراض
        disease_info = {
            "صحي": {
                "severity": "لا يوجد",
                "treatment": "استمر في العناية الجيدة",
                "prevention": "حافظ على الري المنتظم والتسميد المتوازن"
            },
            "تبقع الأوراق": {
                "severity": "متوسط",
                "treatment": "استخدم مبيد فطري مناسب",
                "prevention": "تجنب الري على الأوراق وحسن التهوية"
            },
            "الصدأ": {
                "severity": "عالي",
                "treatment": "مبيد فطري نحاسي أو كبريتي",
                "prevention": "تقليل الرطوبة وتحسين دوران الهواء"
            },
            "البياض الدقيقي": {
                "severity": "متوسط إلى عالي",
                "treatment": "مبيد فطري جهازي",
                "prevention": "تجنب الزراعة المكثفة وحسن التهوية"
            }
        }
        
        default_info = {
            "severity": "غير محدد",
            "treatment": "استشر خبير زراعي",
            "prevention": "اتبع ممارسات الزراعة الجيدة"
        }
        
        info = disease_info.get(disease_name, default_info)
        
        # تقييم مستوى الثقة
        if confidence > 0.9:
            confidence_level = "عالي جداً"
        elif confidence > 0.8:
            confidence_level = "عالي"
        elif confidence > 0.7:
            confidence_level = "متوسط"
        elif confidence > 0.6:
            confidence_level = "منخفض"
        else:
            confidence_level = "منخفض جداً - يحتاج فحص إضافي"
        
        return {
            **info,
            "confidence_level": confidence_level,
            "recommendation": self._get_treatment_recommendation(disease_name, confidence)
        }
    
    def _get_treatment_recommendation(self, disease_name: str, confidence: float) -> str:
        """الحصول على توصية العلاج"""
        if confidence < 0.6:
            return "الثقة في التشخيص منخفضة. يُنصح بإجراء فحص إضافي أو استشارة خبير."
        
        if disease_name == "صحي":
            return "النبات في حالة جيدة. استمر في العناية الحالية."
        
        return f"تم تشخيص {disease_name}. اتبع خطة العلاج المقترحة واستشر خبير إذا لم تتحسن الحالة."

class HyperspectralAnalyzer:
    """محلل التصوير فائق الطيف"""
    
    def __init__(self):
        self.wavelength_ranges = {
            "visible": (400, 700),      # الضوء المرئي
            "nir": (700, 1000),         # الأشعة تحت الحمراء القريبة
            "swir": (1000, 2500),       # الأشعة تحت الحمراء القصيرة
            "mwir": (3000, 5000),       # الأشعة تحت الحمراء المتوسطة
            "lwir": (8000, 14000)       # الأشعة تحت الحمراء الطويلة
        }
        
        # مؤشرات نباتية مهمة
        self.vegetation_indices = {
            "NDVI": "مؤشر الغطاء النباتي المعياري",
            "EVI": "مؤشر الغطاء النباتي المحسن",
            "SAVI": "مؤشر الغطاء النباتي المعدل للتربة",
            "MSAVI": "مؤشر الغطاء النباتي المعدل للتربة المحسن",
            "NDWI": "مؤشر المياه المعياري",
            "PRI": "مؤشر الانعكاس الضوئي",
            "CRI": "مؤشر الانعكاس الكاروتيني"
        }
    
    async def analyze_hyperspectral_image(self, hyperspectral_data: np.ndarray, 
                                        wavelengths: np.ndarray = None) -> Dict[str, Any]:
        """تحليل صورة فائقة الطيف"""
        try:
            if wavelengths is None:
                # إنشاء أطوال موجية افتراضية
                wavelengths = np.linspace(400, 2500, hyperspectral_data.shape[-1])
            
            # حساب المؤشرات النباتية
            vegetation_indices = self._calculate_vegetation_indices(hyperspectral_data, wavelengths)
            
            # تحليل الطيف
            spectral_analysis = self._analyze_spectral_signatures(hyperspectral_data, wavelengths)
            
            # كشف الشذوذ
            anomaly_detection = self._detect_spectral_anomalies(hyperspectral_data)
            
            # تصنيف المواد
            material_classification = self._classify_materials(hyperspectral_data, wavelengths)
            
            # تحليل صحة النبات
            plant_health = self._analyze_plant_health(vegetation_indices)
            
            return {
                "vegetation_indices": vegetation_indices,
                "spectral_analysis": spectral_analysis,
                "anomaly_detection": anomaly_detection,
                "material_classification": material_classification,
                "plant_health_assessment": plant_health,
                "wavelength_range": {
                    "min": float(wavelengths.min()),
                    "max": float(wavelengths.max()),
                    "count": len(wavelengths)
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الصورة فائقة الطيف: {e}")
            raise
    
    def _calculate_vegetation_indices(self, data: np.ndarray, wavelengths: np.ndarray) -> Dict[str, Any]:
        """حساب المؤشرات النباتية"""
        try:
            # العثور على أقرب أطوال موجية للحسابات
            red_idx = np.argmin(np.abs(wavelengths - 670))      # الأحمر
            nir_idx = np.argmin(np.abs(wavelengths - 800))      # الأشعة تحت الحمراء القريبة
            blue_idx = np.argmin(np.abs(wavelengths - 470))     # الأزرق
            green_idx = np.argmin(np.abs(wavelengths - 550))    # الأخضر
            swir_idx = np.argmin(np.abs(wavelengths - 1600))    # الأشعة تحت الحمراء القصيرة
            
            # استخراج القنوات
            red = data[:, :, red_idx].astype(float)
            nir = data[:, :, nir_idx].astype(float)
            blue = data[:, :, blue_idx].astype(float)
            green = data[:, :, green_idx].astype(float)
            swir = data[:, :, swir_idx].astype(float)
            
            # حساب المؤشرات
            indices = {}
            
            # NDVI - مؤشر الغطاء النباتي المعياري
            ndvi = (nir - red) / (nir + red + 1e-8)
            indices["NDVI"] = {
                "value": float(np.nanmean(ndvi)),
                "std": float(np.nanstd(ndvi)),
                "min": float(np.nanmin(ndvi)),
                "max": float(np.nanmax(ndvi))
            }
            
            # EVI - مؤشر الغطاء النباتي المحسن
            evi = 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)
            indices["EVI"] = {
                "value": float(np.nanmean(evi)),
                "std": float(np.nanstd(evi)),
                "min": float(np.nanmin(evi)),
                "max": float(np.nanmax(evi))
            }
            
            # SAVI - مؤشر الغطاء النباتي المعدل للتربة
            L = 0.5  # عامل تصحيح التربة
            savi = ((nir - red) / (nir + red + L)) * (1 + L)
            indices["SAVI"] = {
                "value": float(np.nanmean(savi)),
                "std": float(np.nanstd(savi)),
                "min": float(np.nanmin(savi)),
                "max": float(np.nanmax(savi))
            }
            
            # NDWI - مؤشر المياه المعياري
            ndwi = (green - nir) / (green + nir + 1e-8)
            indices["NDWI"] = {
                "value": float(np.nanmean(ndwi)),
                "std": float(np.nanstd(ndwi)),
                "min": float(np.nanmin(ndwi)),
                "max": float(np.nanmax(ndwi))
            }
            
            return indices
            
        except Exception as e:
            logger.error(f"خطأ في حساب المؤشرات النباتية: {e}")
            return {}
    
    def _analyze_spectral_signatures(self, data: np.ndarray, wavelengths: np.ndarray) -> Dict[str, Any]:
        """تحليل التوقيعات الطيفية"""
        try:
            # حساب متوسط الطيف
            mean_spectrum = np.mean(data.reshape(-1, data.shape[-1]), axis=0)
            
            # العثور على القمم والوديان
            peaks = []
            valleys = []
            
            for i in range(1, len(mean_spectrum) - 1):
                if mean_spectrum[i] > mean_spectrum[i-1] and mean_spectrum[i] > mean_spectrum[i+1]:
                    peaks.append({
                        "wavelength": float(wavelengths[i]),
                        "intensity": float(mean_spectrum[i]),
                        "index": i
                    })
                elif mean_spectrum[i] < mean_spectrum[i-1] and mean_spectrum[i] < mean_spectrum[i+1]:
                    valleys.append({
                        "wavelength": float(wavelengths[i]),
                        "intensity": float(mean_spectrum[i]),
                        "index": i
                    })
            
            # ترتيب القمم والوديان حسب الشدة
            peaks.sort(key=lambda x: x["intensity"], reverse=True)
            valleys.sort(key=lambda x: x["intensity"])
            
            # تحليل النطاقات الطيفية
            band_analysis = {}
            for band_name, (min_wl, max_wl) in self.wavelength_ranges.items():
                mask = (wavelengths >= min_wl) & (wavelengths <= max_wl)
                if np.any(mask):
                    band_data = mean_spectrum[mask]
                    band_analysis[band_name] = {
                        "mean_reflectance": float(np.mean(band_data)),
                        "std_reflectance": float(np.std(band_data)),
                        "min_reflectance": float(np.min(band_data)),
                        "max_reflectance": float(np.max(band_data)),
                        "wavelength_range": [min_wl, max_wl]
                    }
            
            return {
                "mean_spectrum": mean_spectrum.tolist(),
                "wavelengths": wavelengths.tolist(),
                "prominent_peaks": peaks[:5],  # أفضل 5 قمم
                "prominent_valleys": valleys[:5],  # أفضل 5 وديان
                "band_analysis": band_analysis,
                "overall_reflectance": {
                    "mean": float(np.mean(mean_spectrum)),
                    "std": float(np.std(mean_spectrum)),
                    "range": [float(np.min(mean_spectrum)), float(np.max(mean_spectrum))]
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل التوقيعات الطيفية: {e}")
            return {}
    
    def _detect_spectral_anomalies(self, data: np.ndarray) -> Dict[str, Any]:
        """كشف الشذوذ الطيفي"""
        try:
            # إعادة تشكيل البيانات
            reshaped_data = data.reshape(-1, data.shape[-1])
            
            # تحليل المكونات الرئيسية
            pca = PCA(n_components=min(10, reshaped_data.shape[1]))
            pca_data = pca.fit_transform(reshaped_data)
            
            # حساب المسافة من المتوسط
            mean_spectrum = np.mean(reshaped_data, axis=0)
            distances = np.linalg.norm(reshaped_data - mean_spectrum, axis=1)
            
            # تحديد العتبة للشذوذ (3 انحرافات معيارية)
            threshold = np.mean(distances) + 3 * np.std(distances)
            anomaly_mask = distances > threshold
            
            # إحصائيات الشذوذ
            anomaly_percentage = (np.sum(anomaly_mask) / len(anomaly_mask)) * 100
            
            # تجميع البيانات لتحديد أنماط الشذوذ
            kmeans = KMeans(n_clusters=min(5, len(reshaped_data)), random_state=42)
            clusters = kmeans.fit_predict(pca_data)
            
            return {
                "anomaly_percentage": float(anomaly_percentage),
                "total_pixels": int(len(reshaped_data)),
                "anomalous_pixels": int(np.sum(anomaly_mask)),
                "anomaly_threshold": float(threshold),
                "pca_explained_variance": pca.explained_variance_ratio_.tolist(),
                "cluster_count": len(np.unique(clusters)),
                "distance_statistics": {
                    "mean": float(np.mean(distances)),
                    "std": float(np.std(distances)),
                    "min": float(np.min(distances)),
                    "max": float(np.max(distances))
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في كشف الشذوذ الطيفي: {e}")
            return {}
    
    def _classify_materials(self, data: np.ndarray, wavelengths: np.ndarray) -> Dict[str, Any]:
        """تصنيف المواد بناءً على التوقيع الطيفي"""
        try:
            # قاعدة معرفة مبسطة للمواد
            material_signatures = {
                "نبات_صحي": {
                    "red_edge": (700, 750),
                    "chlorophyll_absorption": (670, 680),
                    "water_absorption": (1450, 1950)
                },
                "نبات_مريض": {
                    "reduced_nir": (750, 900),
                    "increased_red": (650, 700),
                    "stress_indicators": (531, 570)
                },
                "تربة": {
                    "iron_oxide": (850, 900),
                    "clay_minerals": (2200, 2300),
                    "organic_matter": (1700, 1800)
                },
                "ماء": {
                    "strong_absorption": (1400, 1500),
                    "secondary_absorption": (1900, 2000)
                }
            }
            
            # تحليل البيانات لكل مادة
            material_probabilities = {}
            
            for material, signature in material_signatures.items():
                probability = self._calculate_material_probability(data, wavelengths, signature)
                material_probabilities[material] = probability
            
            # تحديد المادة الأكثر احتمالاً
            most_likely_material = max(material_probabilities, key=material_probabilities.get)
            
            return {
                "material_probabilities": material_probabilities,
                "most_likely_material": most_likely_material,
                "confidence": material_probabilities[most_likely_material]
            }
            
        except Exception as e:
            logger.error(f"خطأ في تصنيف المواد: {e}")
            return {}
    
    def _calculate_material_probability(self, data: np.ndarray, wavelengths: np.ndarray, 
                                      signature: Dict[str, Tuple[int, int]]) -> float:
        """حساب احتمالية وجود مادة معينة"""
        try:
            total_score = 0
            feature_count = 0
            
            mean_spectrum = np.mean(data.reshape(-1, data.shape[-1]), axis=0)
            
            for feature, (min_wl, max_wl) in signature.items():
                mask = (wavelengths >= min_wl) & (wavelengths <= max_wl)
                if np.any(mask):
                    feature_intensity = np.mean(mean_spectrum[mask])
                    # تطبيع النتيجة بين 0 و 1
                    normalized_score = min(1.0, max(0.0, feature_intensity))
                    total_score += normalized_score
                    feature_count += 1
            
            return total_score / feature_count if feature_count > 0 else 0.0
            
        except Exception as e:
            logger.error(f"خطأ في حساب احتمالية المادة: {e}")
            return 0.0
    
    def _analyze_plant_health(self, vegetation_indices: Dict[str, Any]) -> Dict[str, Any]:
        """تحليل صحة النبات بناءً على المؤشرات النباتية"""
        try:
            health_score = 0
            health_factors = []
            
            # تحليل NDVI
            if "NDVI" in vegetation_indices:
                ndvi_value = vegetation_indices["NDVI"]["value"]
                if ndvi_value > 0.7:
                    health_factors.append("غطاء نباتي كثيف وصحي")
                    health_score += 25
                elif ndvi_value > 0.5:
                    health_factors.append("غطاء نباتي متوسط")
                    health_score += 15
                elif ndvi_value > 0.3:
                    health_factors.append("غطاء نباتي ضعيف")
                    health_score += 5
                else:
                    health_factors.append("غطاء نباتي ضعيف جداً أو غير موجود")
            
            # تحليل EVI
            if "EVI" in vegetation_indices:
                evi_value = vegetation_indices["EVI"]["value"]
                if evi_value > 0.5:
                    health_factors.append("نشاط ضوئي عالي")
                    health_score += 25
                elif evi_value > 0.3:
                    health_factors.append("نشاط ضوئي متوسط")
                    health_score += 15
                else:
                    health_factors.append("نشاط ضوئي منخفض")
                    health_score += 5
            
            # تحليل NDWI
            if "NDWI" in vegetation_indices:
                ndwi_value = vegetation_indices["NDWI"]["value"]
                if ndwi_value > 0.3:
                    health_factors.append("محتوى مائي عالي")
                    health_score += 25
                elif ndwi_value > 0.1:
                    health_factors.append("محتوى مائي متوسط")
                    health_score += 15
                else:
                    health_factors.append("محتوى مائي منخفض - قد يشير لإجهاد مائي")
                    health_score += 5
            
            # تحليل SAVI
            if "SAVI" in vegetation_indices:
                savi_value = vegetation_indices["SAVI"]["value"]
                if savi_value > 0.5:
                    health_factors.append("غطاء نباتي جيد مع تأثير تربة محدود")
                    health_score += 25
                elif savi_value > 0.3:
                    health_factors.append("غطاء نباتي متوسط مع تأثير تربة")
                    health_score += 15
                else:
                    health_factors.append("غطاء نباتي ضعيف أو تأثير تربة عالي")
                    health_score += 5
            
            # تحديد الحالة الصحية العامة
            if health_score >= 80:
                health_status = "ممتاز"
                health_color = "أخضر"
            elif health_score >= 60:
                health_status = "جيد"
                health_color = "أخضر فاتح"
            elif health_score >= 40:
                health_status = "متوسط"
                health_color = "أصفر"
            elif health_score >= 20:
                health_status = "ضعيف"
                health_color = "برتقالي"
            else:
                health_status = "سيء"
                health_color = "أحمر"
            
            # توصيات العلاج
            recommendations = self._generate_health_recommendations(health_score, vegetation_indices)
            
            return {
                "health_score": health_score,
                "health_status": health_status,
                "health_color": health_color,
                "health_factors": health_factors,
                "recommendations": recommendations,
                "detailed_analysis": {
                    "vegetation_density": self._assess_vegetation_density(vegetation_indices),
                    "water_stress": self._assess_water_stress(vegetation_indices),
                    "photosynthetic_activity": self._assess_photosynthetic_activity(vegetation_indices)
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل صحة النبات: {e}")
            return {}
    
    def _assess_vegetation_density(self, indices: Dict[str, Any]) -> str:
        """تقييم كثافة الغطاء النباتي"""
        if "NDVI" in indices:
            ndvi = indices["NDVI"]["value"]
            if ndvi > 0.7:
                return "كثيف جداً"
            elif ndvi > 0.5:
                return "كثيف"
            elif ndvi > 0.3:
                return "متوسط"
            elif ndvi > 0.1:
                return "خفيف"
            else:
                return "ضعيف جداً"
        return "غير محدد"
    
    def _assess_water_stress(self, indices: Dict[str, Any]) -> str:
        """تقييم الإجهاد المائي"""
        if "NDWI" in indices:
            ndwi = indices["NDWI"]["value"]
            if ndwi > 0.3:
                return "لا يوجد إجهاد مائي"
            elif ndwi > 0.1:
                return "إجهاد مائي خفيف"
            elif ndwi > -0.1:
                return "إجهاد مائي متوسط"
            else:
                return "إجهاد مائي شديد"
        return "غير محدد"
    
    def _assess_photosynthetic_activity(self, indices: Dict[str, Any]) -> str:
        """تقييم النشاط الضوئي"""
        if "EVI" in indices:
            evi = indices["EVI"]["value"]
            if evi > 0.5:
                return "نشاط عالي"
            elif evi > 0.3:
                return "نشاط متوسط"
            elif evi > 0.1:
                return "نشاط منخفض"
            else:
                return "نشاط ضعيف جداً"
        return "غير محدد"
    
    def _generate_health_recommendations(self, health_score: int, 
                                       indices: Dict[str, Any]) -> List[str]:
        """توليد توصيات العلاج"""
        recommendations = []
        
        if health_score < 40:
            recommendations.append("فحص شامل للنبات والتربة")
            recommendations.append("تحليل عينات التربة والأوراق")
        
        if "NDWI" in indices and indices["NDWI"]["value"] < 0.1:
            recommendations.append("زيادة الري أو تحسين نظام الري")
            recommendations.append("فحص نظام الصرف")
        
        if "NDVI" in indices and indices["NDVI"]["value"] < 0.3:
            recommendations.append("فحص الآفات والأمراض")
            recommendations.append("تحسين التسميد")
        
        if "EVI" in indices and indices["EVI"]["value"] < 0.3:
            recommendations.append("تحسين التعرض للضوء")
            recommendations.append("فحص نقص العناصر الغذائية")
        
        if health_score > 80:
            recommendations.append("استمر في نفس برنامج العناية")
            recommendations.append("مراقبة دورية للحفاظ على الحالة الممتازة")
        
        return recommendations

class ThreeDAnalyzer:
    """محلل التصوير ثلاثي الأبعاد"""
    
    def __init__(self):
        self.supported_formats = ['.ply', '.pcd', '.obj', '.stl']
    
    async def analyze_3d_data(self, point_cloud_data: Union[np.ndarray, str]) -> Dict[str, Any]:
        """تحليل البيانات ثلاثية الأبعاد"""
        try:
            # تحميل البيانات
            if isinstance(point_cloud_data, str):
                # مسار ملف
                pcd = o3d.io.read_point_cloud(point_cloud_data)
            else:
                # بيانات numpy
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(point_cloud_data)
            
            # التحليل الأساسي
            basic_analysis = self._basic_3d_analysis(pcd)
            
            # تحليل الشكل
            shape_analysis = self._shape_analysis(pcd)
            
            # تحليل الحجم
            volume_analysis = self._volume_analysis(pcd)
            
            # كشف العيوب
            defect_detection = self._detect_3d_defects(pcd)
            
            return {
                "basic_analysis": basic_analysis,
                "shape_analysis": shape_analysis,
                "volume_analysis": volume_analysis,
                "defect_detection": defect_detection,
                "point_count": len(pcd.points)
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل البيانات ثلاثية الأبعاد: {e}")
            raise
    
    def _basic_3d_analysis(self, pcd) -> Dict[str, Any]:
        """التحليل الأساسي للبيانات ثلاثية الأبعاد"""
        try:
            # الحصول على الحدود
            bbox = pcd.get_axis_aligned_bounding_box()
            
            # حساب الأبعاد
            dimensions = bbox.get_extent()
            
            # حساب المركز
            center = bbox.get_center()
            
            # حساب الكثافة
            volume = bbox.volume()
            density = len(pcd.points) / volume if volume > 0 else 0
            
            return {
                "dimensions": {
                    "width": float(dimensions[0]),
                    "height": float(dimensions[1]),
                    "depth": float(dimensions[2])
                },
                "center": {
                    "x": float(center[0]),
                    "y": float(center[1]),
                    "z": float(center[2])
                },
                "bounding_box_volume": float(volume),
                "point_density": float(density),
                "total_points": len(pcd.points)
            }
            
        except Exception as e:
            logger.error(f"خطأ في التحليل الأساسي ثلاثي الأبعاد: {e}")
            return {}
    
    def _shape_analysis(self, pcd) -> Dict[str, Any]:
        """تحليل الشكل"""
        try:
            # تقدير الأسطح العادية
            pcd.estimate_normals()
            
            # تحليل الانحناء
            curvatures = []
            if hasattr(pcd, 'normals') and len(pcd.normals) > 0:
                # حساب تقريبي للانحناء
                normals = np.asarray(pcd.normals)
                curvatures = np.linalg.norm(normals, axis=1)
            
            # تحليل التماثل
            symmetry_analysis = self._analyze_symmetry(pcd)
            
            # تحليل النعومة
            smoothness = self._analyze_smoothness(pcd)
            
            return {
                "curvature_statistics": {
                    "mean": float(np.mean(curvatures)) if curvatures else 0,
                    "std": float(np.std(curvatures)) if curvatures else 0,
                    "min": float(np.min(curvatures)) if curvatures else 0,
                    "max": float(np.max(curvatures)) if curvatures else 0
                },
                "symmetry_analysis": symmetry_analysis,
                "smoothness_score": smoothness
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الشكل: {e}")
            return {}
    
    def _volume_analysis(self, pcd) -> Dict[str, Any]:
        """تحليل الحجم"""
        try:
            # إنشاء شبكة من النقاط
            try:
                # محاولة إنشاء شبكة باستخدام Poisson
                mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
                
                # حساب الحجم
                volume = mesh.get_volume()
                surface_area = mesh.get_surface_area()
                
                # حساب نسبة السطح إلى الحجم
                surface_to_volume_ratio = surface_area / volume if volume > 0 else 0
                
                return {
                    "estimated_volume": float(volume),
                    "surface_area": float(surface_area),
                    "surface_to_volume_ratio": float(surface_to_volume_ratio),
                    "mesh_vertices": len(mesh.vertices),
                    "mesh_triangles": len(mesh.triangles)
                }
                
            except Exception:
                # إذا فشل Poisson، استخدم تقدير بسيط
                bbox = pcd.get_axis_aligned_bounding_box()
                estimated_volume = bbox.volume() * 0.5  # تقدير تقريبي
                
                return {
                    "estimated_volume": float(estimated_volume),
                    "surface_area": 0,
                    "surface_to_volume_ratio": 0,
                    "mesh_vertices": 0,
                    "mesh_triangles": 0,
                    "note": "تقدير تقريبي - فشل في إنشاء الشبكة"
                }
                
        except Exception as e:
            logger.error(f"خطأ في تحليل الحجم: {e}")
            return {}
    
    def _detect_3d_defects(self, pcd) -> Dict[str, Any]:
        """كشف العيوب في البيانات ثلاثية الأبعاد"""
        try:
            # كشف النقاط الشاذة
            outliers = self._detect_outliers(pcd)
            
            # كشف الثقوب
            holes = self._detect_holes(pcd)
            
            # كشف عدم الانتظام
            irregularities = self._detect_irregularities(pcd)
            
            return {
                "outliers": outliers,
                "holes": holes,
                "irregularities": irregularities,
                "overall_quality": self._assess_overall_quality(outliers, holes, irregularities)
            }
            
        except Exception as e:
            logger.error(f"خطأ في كشف العيوب ثلاثية الأبعاد: {e}")
            return {}
    
    def _detect_outliers(self, pcd) -> Dict[str, Any]:
        """كشف النقاط الشاذة"""
        try:
            # استخدام الطريقة الإحصائية لكشف النقاط الشاذة
            cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
            
            outlier_count = len(pcd.points) - len(cl.points)
            outlier_percentage = (outlier_count / len(pcd.points)) * 100
            
            return {
                "outlier_count": outlier_count,
                "outlier_percentage": float(outlier_percentage),
                "remaining_points": len(cl.points)
            }
            
        except Exception as e:
            logger.error(f"خطأ في كشف النقاط الشاذة: {e}")
            return {"outlier_count": 0, "outlier_percentage": 0, "remaining_points": len(pcd.points)}
    
    def _detect_holes(self, pcd) -> Dict[str, Any]:
        """كشف الثقوب"""
        try:
            # تحليل مبسط للثقوب بناءً على كثافة النقاط
            points = np.asarray(pcd.points)
            
            # تقسيم المساحة إلى شبكة وحساب كثافة النقاط
            grid_size = 10
            x_range = np.linspace(points[:, 0].min(), points[:, 0].max(), grid_size)
            y_range = np.linspace(points[:, 1].min(), points[:, 1].max(), grid_size)
            z_range = np.linspace(points[:, 2].min(), points[:, 2].max(), grid_size)
            
            # حساب كثافة النقاط في كل خلية
            densities = []
            for i in range(len(x_range)-1):
                for j in range(len(y_range)-1):
                    for k in range(len(z_range)-1):
                        mask = ((points[:, 0] >= x_range[i]) & (points[:, 0] < x_range[i+1]) &
                               (points[:, 1] >= y_range[j]) & (points[:, 1] < y_range[j+1]) &
                               (points[:, 2] >= z_range[k]) & (points[:, 2] < z_range[k+1]))
                        density = np.sum(mask)
                        densities.append(density)
            
            # تحديد الخلايا الفارغة كثقوب محتملة
            empty_cells = np.sum(np.array(densities) == 0)
            total_cells = len(densities)
            hole_percentage = (empty_cells / total_cells) * 100
            
            return {
                "potential_holes": empty_cells,
                "total_grid_cells": total_cells,
                "hole_percentage": float(hole_percentage)
            }
            
        except Exception as e:
            logger.error(f"خطأ في كشف الثقوب: {e}")
            return {"potential_holes": 0, "total_grid_cells": 0, "hole_percentage": 0}
    
    def _detect_irregularities(self, pcd) -> Dict[str, Any]:
        """كشف عدم الانتظام"""
        try:
            points = np.asarray(pcd.points)
            
            # حساب المسافات بين النقاط المجاورة
            from sklearn.neighbors import NearestNeighbors
            
            nbrs = NearestNeighbors(n_neighbors=6).fit(points)
            distances, indices = nbrs.kneighbors(points)
            
            # حساب متوسط المسافات لكل نقطة
            avg_distances = np.mean(distances[:, 1:], axis=1)  # تجاهل المسافة للنقطة نفسها
            
            # تحديد النقاط غير المنتظمة
            threshold = np.mean(avg_distances) + 2 * np.std(avg_distances)
            irregular_points = np.sum(avg_distances > threshold)
            irregularity_percentage = (irregular_points / len(points)) * 100
            
            return {
                "irregular_points": irregular_points,
                "irregularity_percentage": float(irregularity_percentage),
                "distance_statistics": {
                    "mean": float(np.mean(avg_distances)),
                    "std": float(np.std(avg_distances)),
                    "min": float(np.min(avg_distances)),
                    "max": float(np.max(avg_distances))
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في كشف عدم الانتظام: {e}")
            return {"irregular_points": 0, "irregularity_percentage": 0}
    
    def _analyze_symmetry(self, pcd) -> Dict[str, Any]:
        """تحليل التماثل"""
        try:
            points = np.asarray(pcd.points)
            center = np.mean(points, axis=0)
            
            # تحليل التماثل حول المحاور
            symmetry_scores = {}
            
            for axis, axis_name in enumerate(['x', 'y', 'z']):
                # انعكاس النقاط حول المحور
                reflected_points = points.copy()
                reflected_points[:, axis] = 2 * center[axis] - reflected_points[:, axis]
                
                # حساب أقرب نقطة لكل نقطة منعكسة
                from sklearn.neighbors import NearestNeighbors
                nbrs = NearestNeighbors(n_neighbors=1).fit(points)
                distances, _ = nbrs.kneighbors(reflected_points)
                
                # حساب نتيجة التماثل
                avg_distance = np.mean(distances)
                max_distance = np.max(distances)
                symmetry_score = 1 / (1 + avg_distance)  # نتيجة بين 0 و 1
                
                symmetry_scores[f'{axis_name}_axis'] = {
                    "score": float(symmetry_score),
                    "avg_distance": float(avg_distance),
                    "max_distance": float(max_distance)
                }
            
            return symmetry_scores
            
        except Exception as e:
            logger.error(f"خطأ في تحليل التماثل: {e}")
            return {}
    
    def _analyze_smoothness(self, pcd) -> float:
        """تحليل النعومة"""
        try:
            if not hasattr(pcd, 'normals') or len(pcd.normals) == 0:
                pcd.estimate_normals()
            
            normals = np.asarray(pcd.normals)
            points = np.asarray(pcd.points)
            
            # حساب تغير الأسطح العادية بين النقاط المجاورة
            from sklearn.neighbors import NearestNeighbors
            
            nbrs = NearestNeighbors(n_neighbors=6).fit(points)
            _, indices = nbrs.kneighbors(points)
            
            smoothness_scores = []
            for i, neighbors in enumerate(indices):
                current_normal = normals[i]
                neighbor_normals = normals[neighbors[1:]]  # تجاهل النقطة نفسها
                
                # حساب متوسط الزاوية بين الأسطح العادية
                dot_products = np.dot(neighbor_normals, current_normal)
                angles = np.arccos(np.clip(dot_products, -1, 1))
                avg_angle = np.mean(angles)
                
                # تحويل الزاوية إلى نتيجة نعومة (زاوية أصغر = نعومة أكبر)
                smoothness = 1 - (avg_angle / np.pi)
                smoothness_scores.append(smoothness)
            
            return float(np.mean(smoothness_scores))
            
        except Exception as e:
            logger.error(f"خطأ في تحليل النعومة: {e}")
            return 0.0
    
    def _assess_overall_quality(self, outliers: Dict, holes: Dict, irregularities: Dict) -> Dict[str, Any]:
        """تقييم الجودة الإجمالية"""
        try:
            # حساب نتيجة الجودة بناءً على العيوب المكتشفة
            quality_score = 100
            
            # خصم نقاط للنقاط الشاذة
            outlier_penalty = min(outliers.get("outlier_percentage", 0) * 2, 30)
            quality_score -= outlier_penalty
            
            # خصم نقاط للثقوب
            hole_penalty = min(holes.get("hole_percentage", 0) * 1.5, 25)
            quality_score -= hole_penalty
            
            # خصم نقاط لعدم الانتظام
            irregularity_penalty = min(irregularities.get("irregularity_percentage", 0) * 1, 20)
            quality_score -= irregularity_penalty
            
            quality_score = max(0, quality_score)
            
            # تحديد مستوى الجودة
            if quality_score >= 90:
                quality_level = "ممتاز"
            elif quality_score >= 75:
                quality_level = "جيد جداً"
            elif quality_score >= 60:
                quality_level = "جيد"
            elif quality_score >= 45:
                quality_level = "متوسط"
            elif quality_score >= 30:
                quality_level = "ضعيف"
            else:
                quality_level = "سيء"
            
            return {
                "quality_score": float(quality_score),
                "quality_level": quality_level,
                "penalties": {
                    "outliers": float(outlier_penalty),
                    "holes": float(hole_penalty),
                    "irregularities": float(irregularity_penalty)
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في تقييم الجودة الإجمالية: {e}")
            return {"quality_score": 0, "quality_level": "غير محدد"}

class AdvancedVisionService:
    """الخدمة الرئيسية للرؤية المتقدمة"""
    
    def __init__(self):
        self.vit_manager = VisionTransformerManager()
        self.hyperspectral_analyzer = HyperspectralAnalyzer()
        self.threed_analyzer = ThreeDAnalyzer()
        self.request_queue = queue.PriorityQueue()
        self.response_cache = {}
        self.is_running = False
        self.worker_thread = None
    
    def start_service(self):
        """بدء الخدمة"""
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._process_requests)
            self.worker_thread.start()
            logger.info("تم بدء خدمة الرؤية المتقدمة")
    
    def stop_service(self):
        """إيقاف الخدمة"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join()
        logger.info("تم إيقاف خدمة الرؤية المتقدمة")
    
    def _process_requests(self):
        """معالجة الطلبات في الخلفية"""
        while self.is_running:
            try:
                priority, request = self.request_queue.get(timeout=1)
                response = asyncio.run(self._handle_request(request))
                self.response_cache[request.request_id] = response
                self.request_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"خطأ في معالجة طلب الرؤية: {e}")
    
    async def _handle_request(self, request: VisionRequest) -> VisionResponse:
        """معالجة طلب واحد"""
        start_time = datetime.now()
        
        try:
            if request.request_type == "classification":
                results = await self._handle_classification_request(request)
                model_used = "vision_transformer"
                
            elif request.request_type == "hyperspectral":
                results = await self._handle_hyperspectral_request(request)
                model_used = "hyperspectral_analyzer"
                
            elif request.request_type == "3d_analysis":
                results = await self._handle_3d_request(request)
                model_used = "3d_analyzer"
                
            elif request.request_type == "multi_analysis":
                results = await self._handle_multi_analysis_request(request)
                model_used = "multi_modal"
                
            else:
                raise ValueError(f"نوع الطلب غير مدعوم: {request.request_type}")
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # استخراج نتائج الثقة
            confidence_scores = self._extract_confidence_scores(results)
            
            return VisionResponse(
                request_id=request.request_id,
                response_type=request.request_type,
                results=results,
                confidence_scores=confidence_scores,
                processing_time=processing_time,
                model_used=model_used,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"خطأ في معالجة طلب الرؤية {request.request_id}: {e}")
            
            return VisionResponse(
                request_id=request.request_id,
                response_type="error",
                results={"error": str(e)},
                confidence_scores={"error": 0.0},
                processing_time=processing_time,
                model_used="none",
                timestamp=datetime.now()
            )
    
    async def _handle_classification_request(self, request: VisionRequest) -> Dict[str, Any]:
        """معالجة طلب التصنيف"""
        model_type = request.parameters.get("model_type", "vit_general")
        return await self.vit_manager.classify_image(request.image_data, model_type)
    
    async def _handle_hyperspectral_request(self, request: VisionRequest) -> Dict[str, Any]:
        """معالجة طلب التصوير فائق الطيف"""
        wavelengths = request.parameters.get("wavelengths")
        return await self.hyperspectral_analyzer.analyze_hyperspectral_image(
            request.image_data, wavelengths
        )
    
    async def _handle_3d_request(self, request: VisionRequest) -> Dict[str, Any]:
        """معالجة طلب التحليل ثلاثي الأبعاد"""
        return await self.threed_analyzer.analyze_3d_data(request.image_data)
    
    async def _handle_multi_analysis_request(self, request: VisionRequest) -> Dict[str, Any]:
        """معالجة طلب التحليل متعدد الوسائط"""
        results = {}
        
        # تصنيف باستخدام ViT
        if "classification" in request.parameters.get("analysis_types", []):
            classification_result = await self.vit_manager.classify_image(
                request.image_data, 
                request.parameters.get("model_type", "plant_disease")
            )
            results["classification"] = classification_result
        
        # تحليل فائق الطيف إذا كانت البيانات متاحة
        if "hyperspectral" in request.parameters.get("analysis_types", []):
            if isinstance(request.image_data, np.ndarray) and len(request.image_data.shape) == 3:
                hyperspectral_result = await self.hyperspectral_analyzer.analyze_hyperspectral_image(
                    request.image_data,
                    request.parameters.get("wavelengths")
                )
                results["hyperspectral"] = hyperspectral_result
        
        # تحليل ثلاثي الأبعاد إذا كانت البيانات متاحة
        if "3d_analysis" in request.parameters.get("analysis_types", []):
            if "point_cloud_data" in request.parameters:
                threed_result = await self.threed_analyzer.analyze_3d_data(
                    request.parameters["point_cloud_data"]
                )
                results["3d_analysis"] = threed_result
        
        return results
    
    def _extract_confidence_scores(self, results: Dict[str, Any]) -> Dict[str, float]:
        """استخراج نتائج الثقة من النتائج"""
        confidence_scores = {}
        
        if "confidence" in results:
            confidence_scores["overall"] = results["confidence"]
        
        if "classification" in results and "confidence" in results["classification"]:
            confidence_scores["classification"] = results["classification"]["confidence"]
        
        if "plant_health_assessment" in results:
            health_assessment = results["plant_health_assessment"]
            if "health_score" in health_assessment:
                confidence_scores["health_assessment"] = health_assessment["health_score"] / 100
        
        if "3d_analysis" in results:
            threed_analysis = results["3d_analysis"]
            if "defect_detection" in threed_analysis:
                quality = threed_analysis["defect_detection"].get("overall_quality", {})
                if "quality_score" in quality:
                    confidence_scores["3d_quality"] = quality["quality_score"] / 100
        
        return confidence_scores
    
    def submit_request(self, request: VisionRequest) -> str:
        """إرسال طلب للمعالجة"""
        self.request_queue.put((request.priority, request))
        return request.request_id
    
    def get_response(self, request_id: str) -> Optional[VisionResponse]:
        """الحصول على استجابة طلب"""
        return self.response_cache.get(request_id)
    
    def get_service_status(self) -> Dict[str, Any]:
        """الحصول على حالة الخدمة"""
        return {
            "is_running": self.is_running,
            "queue_size": self.request_queue.qsize(),
            "cache_size": len(self.response_cache),
            "device": str(self.vit_manager.device),
            "models_loaded": {
                "vit": len(self.vit_manager.models),
                "processors": len(self.vit_manager.processors)
            },
            "supported_analysis_types": [
                "classification", "hyperspectral", "3d_analysis", "multi_analysis"
            ]
        }

# إنشاء مثيل عام للخدمة
advanced_vision_service = AdvancedVisionService()

# دوال مساعدة للاستخدام السهل
async def classify_plant_disease(image_data: Union[bytes, np.ndarray], **kwargs) -> Dict[str, Any]:
    """دالة مساعدة لتصنيف أمراض النباتات"""
    request = VisionRequest(
        request_id=f"plant_disease_{datetime.now().timestamp()}",
        request_type="classification",
        image_data=image_data,
        parameters={**kwargs, "model_type": "plant_disease"},
        user_id=kwargs.get("user_id", "system"),
        timestamp=datetime.now()
    )
    
    request_id = advanced_vision_service.submit_request(request)
    
    while True:
        response = advanced_vision_service.get_response(request_id)
        if response:
            return response.results
        await asyncio.sleep(0.1)

async def analyze_hyperspectral(hyperspectral_data: np.ndarray, 
                              wavelengths: np.ndarray = None, **kwargs) -> Dict[str, Any]:
    """دالة مساعدة لتحليل البيانات فائقة الطيف"""
    request = VisionRequest(
        request_id=f"hyperspectral_{datetime.now().timestamp()}",
        request_type="hyperspectral",
        image_data=hyperspectral_data,
        parameters={**kwargs, "wavelengths": wavelengths},
        user_id=kwargs.get("user_id", "system"),
        timestamp=datetime.now()
    )
    
    request_id = advanced_vision_service.submit_request(request)
    
    while True:
        response = advanced_vision_service.get_response(request_id)
        if response:
            return response.results
        await asyncio.sleep(0.1)

async def analyze_3d_plant(point_cloud_data: Union[np.ndarray, str], **kwargs) -> Dict[str, Any]:
    """دالة مساعدة لتحليل البيانات ثلاثية الأبعاد للنباتات"""
    request = VisionRequest(
        request_id=f"3d_plant_{datetime.now().timestamp()}",
        request_type="3d_analysis",
        image_data=point_cloud_data,
        parameters=kwargs,
        user_id=kwargs.get("user_id", "system"),
        timestamp=datetime.now()
    )
    
    request_id = advanced_vision_service.submit_request(request)
    
    while True:
        response = advanced_vision_service.get_response(request_id)
        if response:
            return response.results
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    # اختبار الخدمة
    async def test_advanced_vision():
        advanced_vision_service.start_service()
        
        # إنشاء صورة اختبار
        test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # اختبار تصنيف أمراض النباتات
        result = await classify_plant_disease(test_image)
        print(f"نتيجة تصنيف أمراض النباتات: {result}")
        
        # اختبار حالة الخدمة
        status = advanced_vision_service.get_service_status()
        print(f"حالة الخدمة: {status}")
        
        advanced_vision_service.stop_service()
    
    # تشغيل الاختبار
    asyncio.run(test_advanced_vision())

