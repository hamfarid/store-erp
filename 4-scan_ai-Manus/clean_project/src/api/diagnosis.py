"""
API التشخيص - تشخيص أمراض النباتات
Diagnosis API - Plant disease diagnosis
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

class DiagnosisRequest(BaseModel):
    file_id: str
    analysis_type: str = "basic"  # basic, advanced, detailed
    include_treatment: bool = True

class DiagnosisResult(BaseModel):
    diagnosis_id: str
    file_id: str
    disease_name: str
    confidence: float
    severity: str
    description: str
    treatment_recommendations: Optional[List[str]] = None
    prevention_tips: Optional[List[str]] = None
    analysis_date: datetime

class DiagnosisHistory(BaseModel):
    diagnosis_id: str
    file_id: str
    disease_name: str
    confidence: float
    analysis_date: datetime
    status: str

@router.post("/analyze", response_model=DiagnosisResult)
async def analyze_plant_disease(request: DiagnosisRequest):
    """
    تحليل وتشخيص أمراض النباتات
    Analyze and diagnose plant diseases
    """
    try:
        # إنشاء معرف فريد للتشخيص
        diagnosis_id = str(uuid.uuid4())
        
        # محاكاة عملية التشخيص (يجب استبدالها بالذكاء الاصطناعي الحقيقي)
        # هذا مثال تجريبي
        mock_diseases = [
            {
                "name": "تبقع الأوراق البكتيري",
                "confidence": 0.85,
                "severity": "متوسط",
                "description": "مرض بكتيري يصيب أوراق النباتات ويسبب ظهور بقع بنية اللون",
                "treatment": [
                    "استخدام مبيد بكتيري مناسب",
                    "إزالة الأوراق المصابة",
                    "تحسين التهوية حول النبات"
                ],
                "prevention": [
                    "تجنب الري على الأوراق",
                    "ضمان التصريف الجيد للتربة",
                    "تطهير الأدوات الزراعية"
                ]
            },
            {
                "name": "العفن الرمادي",
                "confidence": 0.78,
                "severity": "عالي",
                "description": "مرض فطري يصيب النباتات في الظروف الرطبة",
                "treatment": [
                    "استخدام مبيد فطري",
                    "تقليل الرطوبة",
                    "إزالة الأجزاء المصابة"
                ],
                "prevention": [
                    "تحسين التهوية",
                    "تجنب الإفراط في الري",
                    "إزالة الأوراق الميتة"
                ]
            }
        ]
        
        # اختيار مرض عشوائي للمحاكاة
        import random
        selected_disease = random.choice(mock_diseases)
        
        logger.info(f"تم تشخيص المرض: {selected_disease['name']} للملف: {request.file_id}")
        
        result = DiagnosisResult(
            diagnosis_id=diagnosis_id,
            file_id=request.file_id,
            disease_name=selected_disease["name"],
            confidence=selected_disease["confidence"],
            severity=selected_disease["severity"],
            description=selected_disease["description"],
            treatment_recommendations=selected_disease["treatment"] if request.include_treatment else None,
            prevention_tips=selected_disease["prevention"] if request.include_treatment else None,
            analysis_date=datetime.now()
        )
        
        return result
        
    except Exception as e:
        logger.error(f"خطأ في تشخيص المرض: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطأ في عملية التشخيص"
        )

@router.get("/history", response_model=List[DiagnosisHistory])
async def get_diagnosis_history(limit: int = 10, offset: int = 0):
    """
    الحصول على تاريخ التشخيصات
    Get diagnosis history
    """
    try:
        # محاكاة بيانات التاريخ (يجب استبدالها بقاعدة البيانات الحقيقية)
        mock_history = [
            DiagnosisHistory(
                diagnosis_id=str(uuid.uuid4()),
                file_id=str(uuid.uuid4()),
                disease_name="تبقع الأوراق البكتيري",
                confidence=0.85,
                analysis_date=datetime.now(),
                status="completed"
            ),
            DiagnosisHistory(
                diagnosis_id=str(uuid.uuid4()),
                file_id=str(uuid.uuid4()),
                disease_name="العفن الرمادي",
                confidence=0.78,
                analysis_date=datetime.now(),
                status="completed"
            )
        ]
        
        # تطبيق التصفح
        start = offset
        end = offset + limit
        
        return mock_history[start:end]
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على تاريخ التشخيصات: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطأ في الحصول على تاريخ التشخيصات"
        )

@router.get("/{diagnosis_id}", response_model=DiagnosisResult)
async def get_diagnosis_details(diagnosis_id: str):
    """
    الحصول على تفاصيل تشخيص محدد
    Get specific diagnosis details
    """
    try:
        # محاكاة البحث عن التشخيص (يجب استبدالها بقاعدة البيانات الحقيقية)
        mock_result = DiagnosisResult(
            diagnosis_id=diagnosis_id,
            file_id=str(uuid.uuid4()),
            disease_name="تبقع الأوراق البكتيري",
            confidence=0.85,
            severity="متوسط",
            description="مرض بكتيري يصيب أوراق النباتات ويسبب ظهور بقع بنية اللون",
            treatment_recommendations=[
                "استخدام مبيد بكتيري مناسب",
                "إزالة الأوراق المصابة",
                "تحسين التهوية حول النبات"
            ],
            prevention_tips=[
                "تجنب الري على الأوراق",
                "ضمان التصريف الجيد للتربة",
                "تطهير الأدوات الزراعية"
            ],
            analysis_date=datetime.now()
        )
        
        return mock_result
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على تفاصيل التشخيص: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطأ في الحصول على تفاصيل التشخيص"
        )

@router.get("/diseases/list")
async def get_supported_diseases():
    """
    الحصول على قائمة الأمراض المدعومة
    Get list of supported diseases
    """
    try:
        diseases = [
            {
                "id": "bacterial_leaf_spot",
                "name": "تبقع الأوراق البكتيري",
                "category": "بكتيري",
                "common_plants": ["الطماطم", "الخيار", "الفلفل"]
            },
            {
                "id": "gray_mold",
                "name": "العفن الرمادي",
                "category": "فطري",
                "common_plants": ["الفراولة", "العنب", "الخس"]
            },
            {
                "id": "powdery_mildew",
                "name": "البياض الدقيقي",
                "category": "فطري",
                "common_plants": ["الورود", "الخيار", "القرع"]
            },
            {
                "id": "rust",
                "name": "الصدأ",
                "category": "فطري",
                "common_plants": ["القمح", "الشعير", "الفول"]
            }
        ]
        
        return {"diseases": diseases, "total": len(diseases)}
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على قائمة الأمراض: {e}")
        raise HTTPException(
            status_code=500,
            detail="خطأ في الحصول على قائمة الأمراض"
        )

