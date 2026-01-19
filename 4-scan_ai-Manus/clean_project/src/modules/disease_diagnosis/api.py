# File: /home/ubuntu/clean_project/src/modules/disease_diagnosis/api.py
"""
مسار الملف: /home/ubuntu/clean_project/src/modules/disease_diagnosis/api.py

واجهة برمجة تطبيقات تشخيص الأمراض - محدثة مع قاعدة البيانات الفعلية
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import sys
import os

# إضافة مسار src إلى Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from database_models import get_session, create_database, Crop, Disease, Diagnosis, User
from auth_service import require_auth, require_permission
from file_handler import save_uploaded_image, process_image_for_diagnosis
import random

router = APIRouter()
logger = logging.getLogger(__name__)

# إنشاء قاعدة البيانات
engine = create_database()

@router.get("/crops")
async def get_crops():
    """الحصول على قائمة المحاصيل المدعومة"""
    session = get_session(engine)
    try:
        crops = session.query(Crop).filter(Crop.is_active == True).all()
        
        return {
            "crops": [
                {
                    "id": crop.id,
                    "name": crop.name,
                    "scientific_name": crop.scientific_name,
                    "category": crop.category,
                    "description": crop.description,
                    "image_path": crop.image_path
                }
                for crop in crops
            ],
            "total": len(crops)
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على المحاصيل: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")
    finally:
        session.close()

@router.get("/diseases")
async def get_diseases(crop_id: Optional[int] = None):
    """الحصول على قائمة الأمراض"""
    session = get_session(engine)
    try:
        query = session.query(Disease).filter(Disease.is_active == True)
        
        if crop_id:
            query = query.filter(Disease.crop_id == crop_id)
        
        diseases = query.all()
        
        return {
            "diseases": [
                {
                    "id": disease.id,
                    "name": disease.name,
                    "crop_id": disease.crop_id,
                    "crop_name": disease.crop.name if disease.crop else None,
                    "severity": disease.severity,
                    "symptoms": disease.symptoms,
                    "treatment": disease.treatment,
                    "prevention": disease.prevention
                }
                for disease in diseases
            ],
            "total": len(diseases)
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على الأمراض: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")
    finally:
        session.close()

@router.post("/diagnose")
async def diagnose_plant(
    crop_id: int = Form(...),
    image: UploadFile = File(...),
    token: str = Form(...)
):
    """تشخيص النبات من الصورة"""
    session = get_session(engine)
    try:
        # التحقق من المصادقة
        auth_result = require_auth(token)
        if not auth_result.get("valid"):
            raise HTTPException(status_code=401, detail="غير مصرح")
        
        user_id = auth_result["user_id"]
        
        # التحقق من وجود المحصول
        crop = session.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            raise HTTPException(status_code=404, detail="المحصول غير موجود")
        
        # حفظ الصورة
        image_content = await image.read()
        file_result = save_uploaded_image(image_content, image.filename, user_id)
        
        if not file_result.get("success"):
            raise HTTPException(status_code=400, detail=file_result.get("message"))
        
        image_path = file_result["file_path"]
        
        # معالجة الصورة للتشخيص
        processed_image_path = process_image_for_diagnosis(image_path)
        
        # محاكاة التشخيص بالذكاء الاصطناعي
        diagnosis_result = simulate_ai_diagnosis(crop_id, session)
        
        # إنشاء سجل التشخيص
        diagnosis = Diagnosis(
            user_id=user_id,
            crop_id=crop_id,
            disease_id=diagnosis_result.get("disease_id"),
            image_path=image_path,
            confidence=diagnosis_result["confidence"],
            status="completed",
            results=diagnosis_result,
            processed_at=datetime.utcnow()
        )
        
        session.add(diagnosis)
        session.commit()
        
        logger.info(f"تم تشخيص جديد للمستخدم {user_id}")
        
        return {
            "diagnosis_id": diagnosis.id,
            "crop": {
                "id": crop.id,
                "name": crop.name
            },
            "disease": diagnosis_result.get("disease"),
            "confidence": diagnosis_result["confidence"],
            "severity": diagnosis_result.get("severity"),
            "treatment": diagnosis_result.get("treatment"),
            "prevention": diagnosis_result.get("prevention"),
            "image_info": file_result.get("image_info"),
            "processed_at": diagnosis.processed_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في التشخيص: {e}")
        raise HTTPException(status_code=500, detail="خطأ في التشخيص")
    finally:
        session.close()

def simulate_ai_diagnosis(crop_id: int, session) -> Dict[str, Any]:
    """محاكاة تشخيص الذكاء الاصطناعي"""
    try:
        # الحصول على الأمراض المحتملة للمحصول
        diseases = session.query(Disease).filter(
            Disease.crop_id == crop_id,
            Disease.is_active == True
        ).all()
        
        if not diseases:
            return {
                "disease_id": None,
                "disease": None,
                "confidence": 0.0,
                "severity": "unknown",
                "treatment": "لا توجد معلومات متاحة",
                "prevention": "لا توجد معلومات متاحة"
            }
        
        # اختيار مرض عشوائي (محاكاة)
        selected_disease = random.choice(diseases)
        confidence = round(random.uniform(0.75, 0.98), 2)
        
        return {
            "disease_id": selected_disease.id,
            "disease": {
                "id": selected_disease.id,
                "name": selected_disease.name,
                "symptoms": selected_disease.symptoms
            },
            "confidence": confidence,
            "severity": selected_disease.severity,
            "treatment": selected_disease.treatment,
            "prevention": selected_disease.prevention,
            "analysis_details": {
                "processing_time": round(random.uniform(0.5, 2.0), 2),
                "model_version": "v2.1",
                "detected_features": ["leaf_spots", "discoloration", "texture_changes"]
            }
        }
        
    except Exception as e:
        logger.error(f"خطأ في محاكاة التشخيص: {e}")
        return {
            "disease_id": None,
            "disease": None,
            "confidence": 0.0,
            "severity": "unknown",
            "treatment": "خطأ في التشخيص",
            "prevention": "خطأ في التشخيص"
        }

@router.get("/diagnosis/{diagnosis_id}")
async def get_diagnosis_details(diagnosis_id: int, token: str):
    """الحصول على تفاصيل تشخيص محدد"""
    session = get_session(engine)
    try:
        # التحقق من المصادقة
        auth_result = require_auth(token)
        if not auth_result.get("valid"):
            raise HTTPException(status_code=401, detail="غير مصرح")
        
        diagnosis = session.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        
        if not diagnosis:
            raise HTTPException(status_code=404, detail="التشخيص غير موجود")
        
        return {
            "id": diagnosis.id,
            "crop": {
                "id": diagnosis.crop.id,
                "name": diagnosis.crop.name
            } if diagnosis.crop else None,
            "disease": {
                "id": diagnosis.disease.id,
                "name": diagnosis.disease.name,
                "severity": diagnosis.disease.severity,
                "treatment": diagnosis.disease.treatment,
                "prevention": diagnosis.disease.prevention
            } if diagnosis.disease else None,
            "confidence": diagnosis.confidence,
            "status": diagnosis.status,
            "results": diagnosis.results,
            "image_path": diagnosis.image_path,
            "created_at": diagnosis.created_at.isoformat(),
            "processed_at": diagnosis.processed_at.isoformat() if diagnosis.processed_at else None,
            "user": {
                "id": diagnosis.user.id,
                "username": diagnosis.user.username,
                "full_name": diagnosis.user.full_name
            } if diagnosis.user else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في الحصول على تفاصيل التشخيص: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")
    finally:
        session.close()

@router.get("/statistics")
async def get_diagnosis_statistics():
    """الحصول على إحصائيات التشخيص"""
    session = get_session(engine)
    try:
        # إجمالي التشخيصات
        total_diagnoses = session.query(Diagnosis).count()
        
        # التشخيصات اليوم
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_diagnoses = session.query(Diagnosis).filter(
            Diagnosis.created_at >= today_start
        ).count()
        
        # التشخيصات حسب المحصول
        crop_stats = session.query(
            Crop.name,
            session.query(Diagnosis).filter(Diagnosis.crop_id == Crop.id).count().label('count')
        ).all()
        
        # التشخيصات حسب الحالة
        status_stats = session.query(
            Diagnosis.status,
            session.query(Diagnosis).filter(Diagnosis.status == Diagnosis.status).count().label('count')
        ).distinct().all()
        
        return {
            "total_diagnoses": total_diagnoses,
            "today_diagnoses": today_diagnoses,
            "success_rate": 94.2,  # محاكاة
            "average_confidence": 89.5,  # محاكاة
            "crop_distribution": [
                {
                    "crop": crop_name,
                    "count": count,
                    "percentage": round((count / total_diagnoses * 100) if total_diagnoses > 0 else 0, 1)
                }
                for crop_name, count in crop_stats
            ],
            "status_distribution": [
                {
                    "status": status,
                    "count": count
                }
                for status, count in status_stats
            ],
            "monthly_trend": [
                {"month": "يناير", "count": 145},
                {"month": "فبراير", "count": 167},
                {"month": "مارس", "count": 189},
                {"month": "أبريل", "count": 234},
                {"month": "مايو", "count": 278},
                {"month": "يونيو", "count": 312}
            ]
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على إحصائيات التشخيص: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")
    finally:
        session.close()

@router.get("/user-diagnoses")
async def get_user_diagnoses(token: str, limit: int = 20, offset: int = 0):
    """الحصول على تشخيصات المستخدم"""
    session = get_session(engine)
    try:
        # التحقق من المصادقة
        auth_result = require_auth(token)
        if not auth_result.get("valid"):
            raise HTTPException(status_code=401, detail="غير مصرح")
        
        user_id = auth_result["user_id"]
        
        # الحصول على التشخيصات
        diagnoses = session.query(Diagnosis).filter(
            Diagnosis.user_id == user_id
        ).order_by(Diagnosis.created_at.desc()).offset(offset).limit(limit).all()
        
        total = session.query(Diagnosis).filter(Diagnosis.user_id == user_id).count()
        
        return {
            "diagnoses": [
                {
                    "id": diagnosis.id,
                    "crop_name": diagnosis.crop.name if diagnosis.crop else "غير محدد",
                    "disease_name": diagnosis.disease.name if diagnosis.disease else "غير محدد",
                    "confidence": diagnosis.confidence,
                    "status": diagnosis.status,
                    "created_at": diagnosis.created_at.isoformat(),
                    "processed_at": diagnosis.processed_at.isoformat() if diagnosis.processed_at else None
                }
                for diagnosis in diagnoses
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في الحصول على تشخيصات المستخدم: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")
    finally:
        session.close()

