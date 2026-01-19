# /home/ubuntu/image_search_integration/auto_learning/keyword_management/api.py

"""
واجهة API للكلمات المفتاحية في مديول البحث الذاتي الذكي

يحتوي هذا الملف على مسارات API الخاصة بإدارة الكلمات المفتاحية،
مثل إنشاء وتحديث وحذف الكلمات المفتاحية وإدارة العلاقات بينها.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..utils.constants import DEFAULT_VALUES, ERROR_MESSAGES
from .schemas import (
    KeywordCreate,
    KeywordRelationCreate,
    KeywordRelationResponse,
    KeywordResponse,
    KeywordUpdate,
)
from .service import KeywordService

logger = logging.getLogger(__name__)

# Constants
KEYWORD_ID_DESC = "معرف الكلمة المفتاحية"

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./auto_learning.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    الحصول على جلسة قاعدة البيانات

    Returns:
        جلسة قاعدة البيانات
    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# إنشاء موجه API للكلمات المفتاحية
router = APIRouter(
    tags=["keywords"],
    responses={
        404: {"description": "الكلمة المفتاحية غير موجودة"},
        409: {"description": "الكلمة المفتاحية موجودة بالفعل"},
        500: {"description": "خطأ داخلي في الخادم"}
    }
)

# الحصول على خدمة الكلمات المفتاحية


def get_keyword_service(db: Session = Depends(get_db)):
    return KeywordService(db)


@router.post("/",
             response_model=KeywordResponse,
             status_code=status.HTTP_201_CREATED,
             summary="إنشاء كلمة مفتاحية جديدة")
async def create_keyword(
    keyword: KeywordCreate,
    service: KeywordService = Depends(get_keyword_service)
):
    """
    إنشاء كلمة مفتاحية جديدة

    Args:
        keyword: بيانات الكلمة المفتاحية الجديدة

    Returns:
        الكلمة المفتاحية التي تم إنشاؤها

    Raises:
        HTTPException: إذا كانت الكلمة المفتاحية موجودة بالفعل أو كانت البيانات غير صالحة
    """
    try:
        return service.create_keyword(keyword)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        )


@router.get("/",
            response_model=List[KeywordResponse],
            summary="الحصول على قائمة الكلمات المفتاحية")
async def get_keywords(
        skip: int = Query(
            0,
            description="عدد العناصر للتخطي"),
    limit: int = Query(
            DEFAULT_VALUES["PAGE_SIZE"],
            description="الحد الأقصى لعدد العناصر للإرجاع"),
        category: Optional[str] = Query(
            None,
            description="تصفية حسب التصنيف"),
        plant_part: Optional[str] = Query(
            None,
            description="تصفية حسب جزء النبات"),
        search: Optional[str] = Query(
            None,
            description="البحث في نص الكلمة المفتاحية"),
        service: KeywordService = Depends(get_keyword_service)):
    """
    الحصول على قائمة الكلمات المفتاحية مع دعم التصفية والبحث

    Args:
        skip: عدد العناصر للتخطي (للصفحات)
        limit: الحد الأقصى لعدد العناصر للإرجاع
        category: تصفية حسب التصنيف
        plant_part: تصفية حسب جزء النبات
        search: البحث في نص الكلمة المفتاحية

    Returns:
        قائمة الكلمات المفتاحية
    """
    try:
        return service.get_keywords(skip, limit, category, plant_part, search)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        )


@router.get("/{keyword_id}", response_model=KeywordResponse,
            summary="الحصول على كلمة مفتاحية محددة")
async def get_keyword(
    keyword_id: int = Path(..., description=KEYWORD_ID_DESC),
    service: KeywordService = Depends(get_keyword_service)
):
    """
    الحصول على كلمة مفتاحية محددة بواسطة المعرف

    Args:
        keyword_id: معرف الكلمة المفتاحية

    Returns:
        الكلمة المفتاحية المطلوبة

    Raises:
        HTTPException: إذا كانت الكلمة المفتاحية غير موجودة
    """
    keyword = service.get_keyword(keyword_id)
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["KEYWORD"]["NOT_FOUND"]
        )
    return keyword


@router.put("/{keyword_id}",
            response_model=KeywordResponse,
            summary="تحديث كلمة مفتاحية")
async def update_keyword(
    keyword_id: int = Path(..., description=KEYWORD_ID_DESC),
    keyword: KeywordUpdate = ...,
    service: KeywordService = Depends(get_keyword_service)
):
    """
    تحديث كلمة مفتاحية موجودة

    Args:
        keyword_id: معرف الكلمة المفتاحية
        keyword: بيانات التحديث

    Returns:
        الكلمة المفتاحية بعد التحديث

    Raises:
        HTTPException: إذا كانت الكلمة المفتاحية غير موجودة أو كانت البيانات غير صالحة
    """
    try:
        updated_keyword = service.update_keyword(keyword_id, keyword)
        if not updated_keyword:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERROR_MESSAGES["KEYWORD"]["NOT_FOUND"]
            )
        return updated_keyword
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        )


@router.delete("/{keyword_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="حذف كلمة مفتاحية")
async def delete_keyword(
    keyword_id: int = Path(..., description=KEYWORD_ID_DESC),
    service: KeywordService = Depends(get_keyword_service)
):
    """
    حذف كلمة مفتاحية موجودة

    Args:
        keyword_id: معرف الكلمة المفتاحية

    Raises:
        HTTPException: إذا كانت الكلمة المفتاحية غير موجودة
    """
    success = service.delete_keyword(keyword_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["KEYWORD"]["NOT_FOUND"]
        )


@router.post("/{keyword_id}/relations",
             response_model=KeywordRelationResponse,
             status_code=status.HTTP_201_CREATED,
             summary="إضافة علاقة بين كلمتين مفتاحيتين")
async def add_keyword_relation(
    keyword_id: int = Path(..., description="معرف الكلمة المفتاحية المصدر"),
    relation: KeywordRelationCreate = ...,
    service: KeywordService = Depends(get_keyword_service)
):
    """
    إضافة علاقة بين كلمتين مفتاحيتين

    Args:
        keyword_id: معرف الكلمة المفتاحية المصدر
        relation: بيانات العلاقة

    Returns:
        العلاقة التي تم إنشاؤها

    Raises:
        HTTPException: إذا كانت الكلمة المفتاحية غير موجودة أو كانت البيانات غير صالحة
    """
    try:
        return service.add_keyword_relation(keyword_id, relation)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        )


@router.get("/{keyword_id}/relations",
            response_model=List[KeywordRelationResponse],
            summary="الحصول على علاقات كلمة مفتاحية")
async def get_keyword_relations(
    keyword_id: int = Path(..., description=KEYWORD_ID_DESC),
    relation_type: Optional[str] = Query(None, description="تصفية حسب نوع العلاقة"),
    service: KeywordService = Depends(get_keyword_service)
):
    """
    الحصول على علاقات كلمة مفتاحية محددة

    Args:
        keyword_id: معرف الكلمة المفتاحية
        relation_type: تصفية حسب نوع العلاقة

    Returns:
        قائمة العلاقات

    Raises:
        HTTPException: إذا كانت الكلمة المفتاحية غير موجودة
    """
    keyword = service.get_keyword(keyword_id)
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["KEYWORD"]["NOT_FOUND"]
        )

    try:
        return service.get_keyword_relations(keyword_id, relation_type)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        )


@router.delete("/{keyword_id}/relations/{relation_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="حذف علاقة بين كلمتين مفتاحيتين")
async def delete_keyword_relation(
    keyword_id: int = Path(..., description="معرف الكلمة المفتاحية المصدر"),
    relation_id: int = Path(..., description="معرف العلاقة"),
    service: KeywordService = Depends(get_keyword_service)
):
    """
    حذف علاقة بين كلمتين مفتاحيتين

    Args:
        keyword_id: معرف الكلمة المفتاحية المصدر
        relation_id: معرف العلاقة

    Raises:
        HTTPException: إذا كانت الكلمة المفتاحية أو العلاقة غير موجودة
    """
    success = service.delete_keyword_relation(keyword_id, relation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["GENERAL"]["NOT_FOUND"]
        )
