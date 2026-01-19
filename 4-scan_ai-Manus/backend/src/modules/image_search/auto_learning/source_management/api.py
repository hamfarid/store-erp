# /home/ubuntu/image_search_integration/auto_learning/source_management/api.py
"""
واجهة API للمصادر الموثوقة في مديول البحث الذاتي الذكي

يحتوي هذا الملف على مسارات API الخاصة بإدارة المصادر الموثوقة،
مثل إنشاء وتحديث وحذف المصادر وإدارة التحقق منها وتقييم مستويات الثقة.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.modules.image_search.auto_learning.source_management.schemas import (
    SourceVerificationCreate,
    SourceVerificationResponse,
    TrustedSourceCreate,
    TrustedSourceResponse,
    TrustedSourceUpdate,
)
from src.modules.image_search.auto_learning.source_management.service import (
    SourceService,
)
from src.modules.image_search.auto_learning.utils.constants import (
    DEFAULT_VALUES,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
)

# Constants for repeated string literals
SOURCE_ID_DESC = "معرف المصدر"

# إنشاء موجه API للمصادر الموثوقة
router = APIRouter(
    tags=["sources"],
    responses={
        404: {"description": "المصدر غير موجود"},
        409: {"description": "المصدر موجود بالفعل"},
        500: {"description": "خطأ داخلي في الخادم"}
    }
)

# تعريف دالة get_db


def get_db():
    """
    الحصول على جلسة قاعدة البيانات

    Returns:
        جلسة قاعدة البيانات
    """
    # هذه الدالة يجب أن تكون موجودة في ملف آخر وتستورد هنا
    # لكن تم تعريفها هنا للتبسيط
    SQLALCHEMY_DATABASE_URL = "sqlite:///./auto_learning.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)

    db = session_local()
    try:
        yield db
    finally:
        db.close()

# الحصول على خدمة المصادر الموثوقة


def get_source_service(db: Session = Depends(get_db)):
    return SourceService(db)


@router.post("/",
             response_model=TrustedSourceResponse,
             status_code=status.HTTP_201_CREATED,
             summary="إنشاء مصدر موثوق جديد")
async def create_source(
    source: TrustedSourceCreate,
    service: SourceService = Depends(get_source_service)
):
    """
    إنشاء مصدر موثوق جديد

    Args:
        source: بيانات المصدر الجديد

    Returns:
        المصدر الذي تم إنشاؤه

    Raises:
        HTTPException: إذا كان المصدر موجوداً بالفعل أو كانت البيانات غير صالحة
    """
    try:
        return service.create_source(source)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        ) from exc


@router.get("/",
            response_model=List[TrustedSourceResponse],
            summary="الحصول على قائمة المصادر الموثوقة")
async def get_sources(
        skip: int = Query(
            0,
            description="عدد العناصر للتخطي"),
    limit: int = Query(
            DEFAULT_VALUES["PAGE_SIZE"],
            description="الحد الأقصى لعدد العناصر للإرجاع"),
        category: Optional[str] = Query(
            None,
            description="تصفية حسب التصنيف"),
        min_trust_level: Optional[int] = Query(
            None,
            description="الحد الأدنى لمستوى الثقة"),
        search: Optional[str] = Query(
            None,
            description="البحث في نطاق المصدر"),
        service: SourceService = Depends(get_source_service)):
    """
    الحصول على قائمة المصادر الموثوقة مع دعم التصفية والبحث

    Args:
        skip: عدد العناصر للتخطي (للصفحات)
        limit: الحد الأقصى لعدد العناصر للإرجاع
        category: تصفية حسب التصنيف
        min_trust_level: الحد الأدنى لمستوى الثقة
        search: البحث في نطاق المصدر

    Returns:
        قائمة المصادر الموثوقة
    """
    try:
        return service.get_sources(
            skip, limit, category, min_trust_level, search)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        ) from exc


@router.get("/{source_id}",
            response_model=TrustedSourceResponse,
            summary="الحصول على مصدر موثوق محدد")
async def get_source(
    source_id: int = Path(..., description=SOURCE_ID_DESC),
    service: SourceService = Depends(get_source_service)
):
    """
    الحصول على مصدر موثوق محدد بواسطة المعرف

    Args:
        source_id: معرف المصدر

    Returns:
        المصدر المطلوب

    Raises:
        HTTPException: إذا كان المصدر غير موجود
    """
    source = service.get_source(source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["SOURCE"]["NOT_FOUND"]
        )
    return source


@router.put("/{source_id}",
            response_model=TrustedSourceResponse,
            summary="تحديث مصدر موثوق")
async def update_source(
    source_id: int = Path(..., description=SOURCE_ID_DESC),
    source: TrustedSourceUpdate = ...,
    service: SourceService = Depends(get_source_service)
):
    """
    تحديث مصدر موثوق موجود

    Args:
        source_id: معرف المصدر
        source: بيانات التحديث

    Returns:
        المصدر بعد التحديث

    Raises:
        HTTPException: إذا كان المصدر غير موجود أو كانت البيانات غير صالحة
    """
    try:
        updated_source = service.update_source(source_id, source)
        if not updated_source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERROR_MESSAGES["SOURCE"]["NOT_FOUND"]
            )
        return updated_source
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        ) from exc


@router.delete("/{source_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="حذف مصدر موثوق")
async def delete_source(
    source_id: int = Path(..., description=SOURCE_ID_DESC),
    service: SourceService = Depends(get_source_service)
):
    """
    حذف مصدر موثوق موجود

    Args:
        source_id: معرف المصدر

    Raises:
        HTTPException: إذا كان المصدر غير موجود
    """
    success = service.delete_source(source_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["SOURCE"]["NOT_FOUND"]
        )


@router.post("/{source_id}/verify",
             response_model=SourceVerificationResponse,
             status_code=status.HTTP_201_CREATED,
             summary="إضافة تحقق من مصدر")
async def add_source_verification(
    source_id: int = Path(..., description=SOURCE_ID_DESC),
    verification: SourceVerificationCreate = ...,
    service: SourceService = Depends(get_source_service)
):
    """
    إضافة تحقق جديد لمصدر موثوق

    Args:
        source_id: معرف المصدر
        verification: بيانات التحقق

    Returns:
        التحقق الذي تم إنشاؤه

    Raises:
        HTTPException: إذا كان المصدر غير موجود أو كانت البيانات غير صالحة
    """
    try:
        return service.add_source_verification(source_id, verification)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        ) from exc


@router.get("/{source_id}/verifications",
            response_model=List[SourceVerificationResponse],
            summary="الحصول على تحققات مصدر")
async def get_source_verifications(
    source_id: int = Path(..., description=SOURCE_ID_DESC),
    service: SourceService = Depends(get_source_service)
):
    """
    الحصول على جميع التحققات الخاصة بمصدر محدد

    Args:
        source_id: معرف المصدر

    Returns:
        قائمة التحققات

    Raises:
        HTTPException: إذا كان المصدر غير موجود
    """
    try:
        return service.get_source_verifications(source_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        ) from exc


@router.post("/{source_id}/blacklist",
             status_code=status.HTTP_200_OK,
             summary="إضافة مصدر إلى القائمة السوداء")
async def blacklist_source(
    source_id: int = Path(..., description=SOURCE_ID_DESC),
    reason: str = Query(..., description="سبب الإضافة إلى القائمة السوداء"),
    service: SourceService = Depends(get_source_service)
):
    """
    إضافة مصدر إلى القائمة السوداء

    Args:
        source_id: معرف المصدر
        reason: سبب الإضافة إلى القائمة السوداء

    Raises:
        HTTPException: إذا كان المصدر غير موجود
    """
    try:
        success = service.blacklist_source(source_id, reason)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERROR_MESSAGES["SOURCE"]["NOT_FOUND"]
            )
        return {"message": SUCCESS_MESSAGES["SOURCE"]["BLACKLISTED"]}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        ) from exc


@router.post("/{source_id}/remove-from-blacklist",
             status_code=status.HTTP_200_OK,
             summary="إزالة مصدر من القائمة السوداء")
async def remove_from_blacklist(
    source_id: int = Path(..., description=SOURCE_ID_DESC),
    service: SourceService = Depends(get_source_service)
):
    """
    إزالة مصدر من القائمة السوداء

    Args:
        source_id: معرف المصدر

    Raises:
        HTTPException: إذا كان المصدر غير موجود
    """
    try:
        success = service.remove_from_blacklist(source_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERROR_MESSAGES["SOURCE"]["NOT_FOUND"]
            )
        return {
            "message": SUCCESS_MESSAGES["SOURCE"]["REMOVED_FROM_BLACKLIST"]}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"]
        ) from exc
