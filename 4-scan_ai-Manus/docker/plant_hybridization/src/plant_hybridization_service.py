"""
خدمة تهجين النباتات المتقدمة
Advanced Plant Hybridization Service
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import json
import os
from pydantic import BaseModel

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="Plant Hybridization Service",
    description="خدمة تهجين النباتات المتقدمة",
    version="1.0.0"
)

# نماذج البيانات
class PlantVariety(BaseModel):
    """نموذج صنف النبات"""
    id: str
    name: str
    species: str
    traits: Dict[str, float]
    origin: str
    description: Optional[str] = None

class HybridizationRequest(BaseModel):
    """طلب تهجين"""
    parent1_id: str
    parent2_id: str
    target_traits: Dict[str, float]
    generations: int = 5
    population_size: int = 100

class HybridizationResult(BaseModel):
    """نتيجة التهجين"""
    hybrid_id: str
    parent1_id: str
    parent2_id: str
    predicted_traits: Dict[str, float]
    fitness_score: float
    generation: int
    success_probability: float

class PlantHybridizationService:
    """خدمة تهجين النباتات"""
    
    def __init__(self):
        """تهيئة خدمة التهجين"""
        self.varieties = {}
        self.traits_database = {}
        self.hybridization_history = []
        self.load_initial_data()
        logger.info("تم تهيئة خدمة تهجين النباتات")
        
    def load_initial_data(self):
        """تحميل البيانات الأولية"""
        # أصناف النباتات الأساسية
        self.varieties = {
            "tomato_cherry": PlantVariety(
                id="tomato_cherry",
                name="طماطم كرزية",
                species="Solanum lycopersicum",
                traits={
                    "size": 0.3,
                    "sweetness": 0.8,
                    "yield": 0.7,
                    "disease_resistance": 0.6,
                    "shelf_life": 0.5
                },
                origin="Mediterranean",
                description="طماطم صغيرة الحجم عالية الحلاوة"
            ),
            "tomato_beefsteak": PlantVariety(
                id="tomato_beefsteak",
                name="طماطم بيف ستيك",
                species="Solanum lycopersicum",
                traits={
                    "size": 0.9,
                    "sweetness": 0.6,
                    "yield": 0.5,
                    "disease_resistance": 0.7,
                    "shelf_life": 0.8
                },
                origin="America",
                description="طماطم كبيرة الحجم مناسبة للسلطات"
            ),
            "wheat_durum": PlantVariety(
                id="wheat_durum",
                name="قمح قاسي",
                species="Triticum durum",
                traits={
                    "protein_content": 0.8,
                    "yield": 0.7,
                    "drought_tolerance": 0.9,
                    "disease_resistance": 0.6,
                    "grain_size": 0.7
                },
                origin="Middle East",
                description="قمح عالي البروتين مقاوم للجفاف"
            )
        }
        
        # قاعدة بيانات الصفات
        self.traits_database = {
            "size": {"min": 0.1, "max": 1.0, "unit": "relative", "description": "الحجم النسبي"},
            "sweetness": {"min": 0.0, "max": 1.0, "unit": "relative", "description": "مستوى الحلاوة"},
            "yield": {"min": 0.1, "max": 1.0, "unit": "relative", "description": "الإنتاجية"},
            "disease_resistance": {"min": 0.0, "max": 1.0, "unit": "relative", "description": "مقاومة الأمراض"},
            "shelf_life": {"min": 0.1, "max": 1.0, "unit": "relative", "description": "مدة الحفظ"},
            "protein_content": {"min": 0.0, "max": 1.0, "unit": "relative", "description": "محتوى البروتين"},
            "drought_tolerance": {"min": 0.0, "max": 1.0, "unit": "relative", "description": "تحمل الجفاف"},
            "grain_size": {"min": 0.1, "max": 1.0, "unit": "relative", "description": "حجم الحبة"}
        }
        
    def simulate_hybridization(self, parent1: PlantVariety, parent2: PlantVariety, 
                             target_traits: Dict[str, float], generations: int = 5) -> HybridizationResult:
        """محاكاة عملية التهجين"""
        try:
            # حساب الصفات المتوقعة للهجين
            predicted_traits = {}
            for trait in set(list(parent1.traits.keys()) + list(parent2.traits.keys())):
                if trait in parent1.traits and trait in parent2.traits:
                    # متوسط الصفات مع تباين عشوائي
                    base_value = (parent1.traits[trait] + parent2.traits[trait]) / 2
                    variation = np.random.normal(0, 0.1)  # تباين عشوائي
                    predicted_traits[trait] = max(0, min(1, base_value + variation))
                elif trait in parent1.traits:
                    predicted_traits[trait] = parent1.traits[trait] * 0.7  # وراثة جزئية
                elif trait in parent2.traits:
                    predicted_traits[trait] = parent2.traits[trait] * 0.7
                    
            # حساب درجة الملاءمة
            fitness_score = self.calculate_fitness(predicted_traits, target_traits)
            
            # حساب احتمالية النجاح
            success_probability = min(0.95, fitness_score * 0.8 + 0.2)
            
            # إنشاء معرف فريد للهجين
            hybrid_id = f"hybrid_{parent1.id}_{parent2.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            result = HybridizationResult(
                hybrid_id=hybrid_id,
                parent1_id=parent1.id,
                parent2_id=parent2.id,
                predicted_traits=predicted_traits,
                fitness_score=fitness_score,
                generation=generations,
                success_probability=success_probability
            )
            
            # حفظ في التاريخ
            self.hybridization_history.append(result.dict())
            
            return result
            
        except Exception as e:
            logger.error(f"خطأ في محاكاة التهجين: {e}")
            raise HTTPException(status_code=500, detail=str(e))
            
    def calculate_fitness(self, predicted_traits: Dict[str, float], 
                         target_traits: Dict[str, float]) -> float:
        """حساب درجة الملاءمة"""
        if not target_traits:
            return 0.5
            
        total_score = 0
        trait_count = 0
        
        for trait, target_value in target_traits.items():
            if trait in predicted_traits:
                # حساب المسافة من القيمة المستهدفة
                distance = abs(predicted_traits[trait] - target_value)
                score = 1 - distance  # كلما قلت المسافة، زادت النقاط
                total_score += max(0, score)
                trait_count += 1
                
        return total_score / trait_count if trait_count > 0 else 0

# إنشاء مثيل الخدمة
hybridization_service = PlantHybridizationService()

@app.get("/")
async def root():
    """الصفحة الرئيسية"""
    return {
        "service": "Plant Hybridization Service",
        "version": "1.0.0",
        "status": "active",
        "available_varieties": len(hybridization_service.varieties),
        "available_traits": len(hybridization_service.traits_database),
        "endpoints": ["/health", "/varieties", "/traits", "/hybridize", "/history"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    """فحص صحة الخدمة"""
    return {
        "status": "healthy",
        "varieties_count": len(hybridization_service.varieties),
        "traits_count": len(hybridization_service.traits_database),
        "hybridization_history_count": len(hybridization_service.hybridization_history),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/varieties")
async def get_varieties():
    """الحصول على أصناف النباتات المتاحة"""
    return {
        "varieties": [variety.dict() for variety in hybridization_service.varieties.values()],
        "total_count": len(hybridization_service.varieties),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/traits")
async def get_traits():
    """الحصول على الصفات المتاحة"""
    return {
        "traits": hybridization_service.traits_database,
        "total_count": len(hybridization_service.traits_database),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/hybridize")
async def hybridize_plants(request: HybridizationRequest):
    """تهجين النباتات"""
    try:
        # التحقق من وجود الأصناف
        if request.parent1_id not in hybridization_service.varieties:
            raise HTTPException(status_code=404, detail=f"الصنف {request.parent1_id} غير موجود")
            
        if request.parent2_id not in hybridization_service.varieties:
            raise HTTPException(status_code=404, detail=f"الصنف {request.parent2_id} غير موجود")
            
        parent1 = hybridization_service.varieties[request.parent1_id]
        parent2 = hybridization_service.varieties[request.parent2_id]
        
        # تنفيذ التهجين
        result = hybridization_service.simulate_hybridization(
            parent1, parent2, request.target_traits, request.generations
        )
        
        return JSONResponse(content=result.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في عملية التهجين: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_hybridization_history():
    """الحصول على تاريخ عمليات التهجين"""
    return {
        "history": hybridization_service.hybridization_history,
        "total_count": len(hybridization_service.hybridization_history),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "plant_hybridization_service:app",
        host="0.0.0.0",
        port=8022,
        reload=False
    )

