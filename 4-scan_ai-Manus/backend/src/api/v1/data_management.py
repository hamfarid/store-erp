"""
API endpoints لإدارة مصادر البيانات وتحديث قواعد البيانات
Data Management API Endpoints
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...services.data_sources import get_data_source_manager
from ...services.database_updater import get_database_updater
from ...services.image_processor import get_image_processor

router = APIRouter(prefix="/data-management", tags=["Data Management"])


# Pydantic Models
class DataSourceResponse(BaseModel):
    name: str
    url: str
    type: str
    language: str
    reliability: float
    update_frequency: str


class UpdateStatsResponse(BaseModel):
    started_at: str
    completed_at: Optional[str] = None
    diseases_checked: int
    diseases_updated: int
    diseases_added: int
    images_updated: int
    errors: List[str]
    duration_seconds: Optional[float] = None


class DatabaseStatsResponse(BaseModel):
    total_diseases: int
    recently_updated: int
    needs_update: int
    last_check: str


class ImageProcessRequest(BaseModel):
    enhance: bool = True
    remove_background: bool = False
    target_size: tuple = (512, 512)


# Endpoints

@router.get("/sources", response_model=List[DataSourceResponse])
async def get_data_sources(
    source_type: Optional[str] = None,
    language: Optional[str] = None,
    min_reliability: float = 0.0
):
    """
    الحصول على قائمة مصادر البيانات الموثوقة

    - **source_type**: نوع المصدر (academic, government, commercial, community)
    - **language**: اللغة (en, ar)
    - **min_reliability**: الحد الأدنى للموثوقية (0.0-1.0)
    """
    try:
        dsm = get_data_source_manager()

        sources = dsm.sources

        # تصفية حسب النوع
        if source_type:
            sources = [s for s in sources if s.source_type == source_type]

        # تصفية حسب اللغة
        if language:
            sources = [s for s in sources if s.language == language]

        # تصفية حسب الموثوقية
        sources = [s for s in sources if s.reliability >= min_reliability]

        return [
            DataSourceResponse(
                name=s.name,
                url=s.url,
                type=s.source_type,
                language=s.language,
                reliability=s.reliability,
                update_frequency=s.update_frequency
            )
            for s in sources
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sources/types")
async def get_source_types():
    """الحصول على أنواع المصادر المتاحة"""
    return {
        "types": ["academic", "government", "commercial", "community"],
        "languages": ["en", "ar"],
        "description": {
            "academic": "مصادر أكاديمية وبحثية",
            "government": "مصادر حكومية رسمية",
            "commercial": "مصادر تجارية",
            "community": "مصادر مجتمعية"
        }
    }


@router.post("/update/database", response_model=UpdateStatsResponse)
async def update_disease_database(
    background_tasks: BackgroundTasks,
    force_update: bool = False,
    update_images: bool = True,
    db: Session = Depends(get_db)
):
    """
    تحديث قاعدة بيانات الأمراض من المصادر الموثوقة

    - **force_update**: فرض التحديث حتى للأمراض المحدثة مؤخراً
    - **update_images**: تحديث الصور أيضاً

    ⚠️ هذه العملية قد تستغرق وقتاً طويلاً
    """
    try:
        updater = get_database_updater(db)

        # تشغيل التحديث في الخلفية
        stats = await updater.update_disease_database(
            force_update=force_update,
            update_images=update_images
        )

        return UpdateStatsResponse(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update/nutrients", response_model=UpdateStatsResponse)
async def update_nutrient_deficiencies(
    db: Session = Depends(get_db)
):
    """
    تحديث معلومات نقص العناصر الغذائية
    """
    try:
        updater = get_database_updater(db)
        stats = await updater.update_nutrient_deficiencies()

        return UpdateStatsResponse(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=DatabaseStatsResponse)
async def get_database_statistics(
    db: Session = Depends(get_db)
):
    """
    الحصول على إحصائيات قاعدة البيانات
    """
    try:
        updater = get_database_updater(db)
        stats = updater.get_update_statistics()

        return DatabaseStatsResponse(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/images/process")
async def process_image(
    file: UploadFile = File(...),
    enhance: bool = True,
    remove_background: bool = False
):
    """
    معالجة وتحسين صورة

    - **file**: ملف الصورة
    - **enhance**: تحسين جودة الصورة
    - **remove_background**: إزالة الخلفية
    """
    try:
        # قراءة الصورة
        image_data = await file.read()

        # معالجة الصورة
        processor = get_image_processor()
        processed_data, metadata = processor.process_disease_image(
            image_data,
            enhance=enhance,
            remove_background=remove_background
        )

        return {
            "success": True,
            "metadata": metadata,
            "message": "Image processed successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/images/batch-process")
async def batch_process_images(
    files: List[UploadFile] = File(...),
    enhance: bool = True,
    remove_background: bool = False
):
    """
    معالجة دفعة من الصور
    """
    try:
        processor = get_image_processor()

        # قراءة جميع الصور
        images_data = []
        for file in files:
            data = await file.read()
            images_data.append(data)

        # معالجة الدفعة
        results = processor.batch_process_images(
            images_data,
            enhance=enhance,
            remove_background=remove_background
        )

        # إعداد النتائج
        processed_count = sum(1 for r in results if r[0] is not None)
        failed_count = len(results) - processed_count

        return {
            "success": True,
            "total": len(results),
            "processed": processed_count,
            "failed": failed_count,
            "results": [
                {
                    "index": i,
                    "success": r[0] is not None,
                    "metadata": r[1]
                }
                for i, r in enumerate(results)
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/images/compare")
async def compare_images(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """
    مقارنة صورتين وإرجاع نسبة التشابه
    """
    try:
        # قراءة الصور
        image1_data = await file1.read()
        image2_data = await file2.read()

        # مقارنة الصور
        processor = get_image_processor()
        similarity = processor.compare_images(image1_data, image2_data)

        return {
            "success": True,
            "similarity": similarity,
            "similarity_percentage": f"{similarity * 100:.2f}%",
            "message": "Images compared successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sources/recommended/{disease_name}")
async def get_recommended_sources(
    disease_name: str,
    max_sources: int = 5
):
    """
    الحصول على المصادر الموصى بها لمرض معين
    """
    try:
        dsm = get_data_source_manager()
        sources = dsm.get_recommended_sources_for_disease(disease_name, max_sources)

        return {
            "disease_name": disease_name,
            "recommended_sources": [
                {
                    "name": s.name,
                    "url": s.url,
                    "type": s.source_type,
                    "reliability": s.reliability,
                    "language": s.language
                }
                for s in sources
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diseases/common")
async def get_common_diseases():
    """الحصول على قائمة الأمراض الشائعة"""
    from ...services.data_sources import COMMON_PLANT_DISEASES, MAJOR_CROPS

    return {
        "common_diseases": COMMON_PLANT_DISEASES,
        "major_crops": MAJOR_CROPS,
        "total_diseases": len(COMMON_PLANT_DISEASES),
        "total_crops": len(MAJOR_CROPS)
    }


@router.get("/health")
async def health_check():
    """فحص صحة النظام"""
    return {
        "status": "healthy",
        "service": "Data Management API",
        "timestamp": datetime.utcnow().isoformat()
    }
