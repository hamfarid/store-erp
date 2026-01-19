# /home/ubuntu/image_search_integration/api.py
"""
واجهة برمجة التطبيقات لمديول البحث عن صور الإصابات والآفات النباتية
API for plant disease and pest image search module
"""

import os
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_user
from modules.image_search.search_client import search_client
from modules.image_search.image_collector import ImageCollector
from modules.image_search.storage import ImageStorage
from modules.image_search.models import PlantImage, Disease, Pest, Crop, ImageTag, ImageSearchHistory
from modules.image_search.schemas import (
    ImageSearchRequest, ImageSearchResponse, ImageCollectionRequest, ImageCollectionResponse,
    DiseaseImageSearchRequest, PestImageSearchRequest, CropImageSearchRequest,
    ImageUploadResponse
)

router = APIRouter(
    prefix="/api/image-search",
    tags=["image-search"],
    responses={404: {"description": "Not found"}},
)

# تهيئة الخدمات
image_collector = ImageCollector({
    "download_path": "/tmp/images/web_search_collected",
    "min_download_delay_seconds": 0.5,
    "max_download_delay_seconds": 2.0,
    "min_image_size_bytes": 10 * 1024,
    "min_image_dimension": 200,
})

image_storage = ImageStorage()


@router.post("/search", response_model=ImageSearchResponse)
async def search_images(
    request: ImageSearchRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """البحث عن صور باستخدام استعلام نصي."""
    try:
        # تنفيذ البحث
        image_urls = search_client.search_images(
            query=request.query,
            count=request.count,
            **request.search_params
        )

        # تسجيل سجل البحث
        search_history = ImageSearchHistory(
            user_id=current_user.id,
            query_text=request.query,
            filters=request.search_params,
            results_count=len(image_urls),
            search_time=0.0,  # يمكن قياس الوقت الفعلي
            created_at=datetime.now(timezone.utc)
        )
        db.add(search_history)
        db.commit()
        db.refresh(search_history)

        # إرجاع النتائج
        return {
            "query": request.query,
            "results_count": len(image_urls),
            "image_urls": image_urls,
            "search_id": search_history.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل البحث عن الصور: {str(e)}") from e


@router.post("/collect", response_model=ImageCollectionResponse)
async def collect_images(
    request: ImageCollectionRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """جمع وتنزيل صور بناءً على كلمات مفتاحية."""
    try:
        # جمع الصور
        collected_images = image_collector.collect_images_by_keywords(
            keywords=request.keywords,
            max_images_per_keyword=request.max_images_per_keyword
        )

        # تخزين البيانات الوصفية في قاعدة البيانات
        stored_images = []
        for img_data in collected_images:
            # إنشاء سجل صورة جديد
            plant_image = PlantImage(
                filename=os.path.basename(img_data["file_path"]),
                file_path=img_data["file_path"],
                file_size=img_data["size_bytes"],
                file_format=img_data["format"].lower() if isinstance(img_data["format"], str) else None,
                source_url=img_data["source_url"],
                title=f"Image for {img_data['query']}",
                description=f"Collected from web search for query: {img_data['query']}",
                user_id=current_user.id,
                organization_id=current_user.organization_id if hasattr(current_user, "organization_id") else None,
                branch_id=current_user.branch_id if hasattr(current_user, "branch_id") else None,
                created_at=datetime.now(timezone.utc),
                metadata={
                    "query": img_data["query"],
                    "collection_timestamp": img_data["timestamp"],
                    "dimensions": img_data["dimensions"]
                }
            )
            db.add(plant_image)
            db.commit()
            db.refresh(plant_image)

            # إضافة إلى قائمة الصور المخزنة
            stored_images.append({
                "id": plant_image.id,
                "filename": plant_image.filename,
                "file_path": plant_image.file_path,
                "source_url": plant_image.source_url,
                "query": img_data["query"]
            })

        # إرجاع النتائج
        return {
            "keywords": request.keywords,
            "total_collected": len(collected_images),
            "stored_images": stored_images
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل جمع الصور: {str(e)}") from e


@router.post("/search/disease", response_model=ImageSearchResponse)
async def search_disease_images(
    request: DiseaseImageSearchRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """البحث عن صور لمرض نباتي محدد."""
    try:
        # البحث عن المرض في قاعدة البيانات
        disease = db.query(Disease).filter(Disease.id == request.disease_id).first()
        if not disease:
            raise HTTPException(status_code=404, detail=f"المرض برقم المعرف {request.disease_id} غير موجود")

        # تنفيذ البحث
        image_urls = search_client.search_images_by_disease(
            disease_name=disease.name,
            count=request.count
        )

        # تسجيل سجل البحث
        search_history = ImageSearchHistory(
            user_id=current_user.id,
            query_text=f"disease:{disease.name}",
            filters={"disease_id": request.disease_id},
            results_count=len(image_urls),
            search_time=0.0,
            created_at=datetime.now(timezone.utc)
        )
        db.add(search_history)
        db.commit()
        db.refresh(search_history)

        # إرجاع النتائج
        return {
            "query": f"disease:{disease.name}",
            "results_count": len(image_urls),
            "image_urls": image_urls,
            "search_id": search_history.id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل البحث عن صور المرض: {str(e)}") from e


@router.post("/search/pest", response_model=ImageSearchResponse)
async def search_pest_images(
    request: PestImageSearchRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """البحث عن صور لآفة زراعية محددة."""
    try:
        # البحث عن الآفة في قاعدة البيانات
        pest = db.query(Pest).filter(Pest.id == request.pest_id).first()
        if not pest:
            raise HTTPException(status_code=404, detail=f"الآفة برقم المعرف {request.pest_id} غير موجود")

        # تنفيذ البحث
        image_urls = search_client.search_images_by_pest(
            pest_name=pest.name,
            count=request.count
        )

        # تسجيل سجل البحث
        search_history = ImageSearchHistory(
            user_id=current_user.id,
            query_text=f"pest:{pest.name}",
            filters={"pest_id": request.pest_id},
            results_count=len(image_urls),
            search_time=0.0,
            created_at=datetime.now(timezone.utc)
        )
        db.add(search_history)
        db.commit()
        db.refresh(search_history)

        # إرجاع النتائج
        return {
            "query": f"pest:{pest.name}",
            "results_count": len(image_urls),
            "image_urls": image_urls,
            "search_id": search_history.id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل البحث عن صور الآفة: {str(e)}") from e


@router.post("/search/crop", response_model=ImageSearchResponse)
async def search_crop_images(
    request: CropImageSearchRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """البحث عن صور لمحصول زراعي محدد."""
    try:
        # البحث عن المحصول في قاعدة البيانات
        crop = db.query(Crop).filter(Crop.id == request.crop_id).first()
        if not crop:
            raise HTTPException(status_code=404, detail=f"المحصول برقم المعرف {request.crop_id} غير موجود")

        # تنفيذ البحث
        image_urls = search_client.search_images_by_crop(
            crop_name=crop.name,
            count=request.count
        )

        # تسجيل سجل البحث
        search_history = ImageSearchHistory(
            user_id=current_user.id,
            query_text=f"crop:{crop.name}",
            filters={"crop_id": request.crop_id},
            results_count=len(image_urls),
            search_time=0.0,
            created_at=datetime.now(timezone.utc)
        )
        db.add(search_history)
        db.commit()
        db.refresh(search_history)

        # إرجاع النتائج
        return {
            "query": f"crop:{crop.name}",
            "results_count": len(image_urls),
            "image_urls": image_urls,
            "search_id": search_history.id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل البحث عن صور المحصول: {str(e)}") from e


def _add_disease_to_image(db: Session, plant_image: PlantImage, disease_id: int) -> None:
    """إضافة مرض إلى الصورة."""
    disease = db.query(Disease).filter(Disease.id == disease_id).first()
    if disease:
        plant_image.diseases.append(disease)


def _add_pest_to_image(db: Session, plant_image: PlantImage, pest_id: int) -> None:
    """إضافة آفة إلى الصورة."""
    pest = db.query(Pest).filter(Pest.id == pest_id).first()
    if pest:
        plant_image.pests.append(pest)


def _add_crops_to_image(db: Session, plant_image: PlantImage, crop_ids: str) -> None:
    """إضافة محاصيل إلى الصورة."""
    crop_id_list = [int(id.strip()) for id in crop_ids.split(',') if id.strip()]
    crops = db.query(Crop).filter(Crop.id.in_(crop_id_list)).all()
    plant_image.crops.extend(crops)


def _add_tags_to_image(db: Session, plant_image: PlantImage, tags: str) -> None:
    """إضافة وسوم إلى الصورة."""
    tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    for tag_name in tag_list:
        tag = db.query(ImageTag).filter(ImageTag.name == tag_name).first()
        if not tag:
            tag = ImageTag(name=tag_name)
            db.add(tag)
        plant_image.tags.append(tag)


def _create_plant_image(file: UploadFile, file_path: str, title: str, description: str, current_user) -> PlantImage:
    """إنشاء سجل صورة نباتية جديد."""
    return PlantImage(
        filename=file.filename,
        file_path=file_path,
        file_size=os.path.getsize(file_path),
        file_format=file.content_type.split('/')[-1].lower(),
        title=title or file.filename,
        description=description,
        user_id=current_user.id,
        organization_id=current_user.organization_id if hasattr(current_user, "organization_id") else None,
        branch_id=current_user.branch_id if hasattr(current_user, "branch_id") else None,
        created_at=datetime.now(timezone.utc)
    )


@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    title: str = Form(None),
    description: str = Form(None),
    disease_id: int = Form(None),
    pest_id: int = Form(None),
    crop_ids: str = Form(None),  # قائمة معرفات المحاصيل مفصولة بفواصل
    tags: str = Form(None),  # قائمة الوسوم مفصولة بفواصل
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """رفع صورة جديدة إلى النظام."""
    try:
        # حفظ الملف
        file_path = image_storage.save_uploaded_file(file)

        # إنشاء سجل الصورة
        plant_image = _create_plant_image(file, file_path, title, description, current_user)
        db.add(plant_image)
        db.commit()
        db.refresh(plant_image)

        # إضافة العلاقات
        if disease_id:
            _add_disease_to_image(db, plant_image, disease_id)

        if pest_id:
            _add_pest_to_image(db, plant_image, pest_id)

        if crop_ids:
            _add_crops_to_image(db, plant_image, crop_ids)

        if tags:
            _add_tags_to_image(db, plant_image, tags)

        db.commit()

        return {
            "id": plant_image.id,
            "filename": plant_image.filename,
            "file_path": plant_image.file_path,
            "title": plant_image.title,
            "description": plant_image.description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل رفع الصورة: {str(e)}") from e
