# /home/ubuntu/image_search_integration/auto_learning/search_engine_management/api.py
"""
واجهة API لمحركات البحث في مديول البحث الذاتي الذكي

يحتوي هذا الملف على مسارات API الخاصة بإدارة محركات البحث،
مثل إنشاء وتحديث وحذف محركات البحث وإدارة إحصائيات الأداء.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from modules.image_search.auto_learning.search_engine_management.schemas import (
    LoadBalancingStrategyUpdate,
    SearchEngineCreate,
    SearchEngineResponse,
    SearchEngineStatsResponse,
    SearchEngineUpdate,
)
from modules.image_search.auto_learning.search_engine_management.service import (
    SearchEngineService,
)
from modules.image_search.auto_learning.utils.constants import (
    DEFAULT_VALUES,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
)

# ثوابت
SEARCH_ENGINE_ID_DESCRIPTION = "معرف محرك البحث"

# إنشاء موجه API لمحركات البحث
router = APIRouter(
    tags=["search_engines"],
    responses={
        404: {"description": "محرك البحث غير موجود"},
        409: {"description": "محرك البحث موجود بالفعل"},
        500: {"description": "خطأ داخلي في الخادم"},
    },
)


# الحصول على قاعدة البيانات
def get_db():
    """الحصول على جلسة قاعدة البيانات"""
    # يجب تطبيق هذه الوظيفة وفقاً لإعدادات قاعدة البيانات
    raise NotImplementedError("Database dependency not implemented")


# الحصول على خدمة محركات البحث
def get_search_engine_service(db: Session = Depends(get_db)):
    return SearchEngineService(db)


@router.post(
    "/",
    response_model=SearchEngineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="إنشاء محرك بحث جديد",
)
async def create_search_engine(
    search_engine: SearchEngineCreate,
    service: SearchEngineService = Depends(get_search_engine_service),
):
    """
    إنشاء محرك بحث جديد

    Args:
        search_engine: بيانات محرك البحث الجديد

    Returns:
        محرك البحث الذي تم إنشاؤه

    Raises:
        HTTPException: إذا كان محرك البحث موجوداً بالفعل أو كانت البيانات غير صالحة
    """
    try:
        return service.create_search_engine(search_engine)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"],
        ) from exc


@router.get(
    "/",
    response_model=List[SearchEngineResponse],
    summary="الحصول على قائمة محركات البحث",
)
async def get_search_engines(
    skip: int = Query(0, description="عدد العناصر للتخطي"),
    limit: int = Query(
        DEFAULT_VALUES["PAGE_SIZE"], description="الحد الأقصى لعدد العناصر للإرجاع"
    ),
    engine_type: Optional[str] = Query(None, description="تصفية حسب النوع"),
    active: Optional[bool] = Query(None, description="تصفية حسب الحالة النشطة"),
    search: Optional[str] = Query(None, description="البحث في اسم محرك البحث"),
    service: SearchEngineService = Depends(get_search_engine_service),
):
    """
    الحصول على قائمة محركات البحث مع دعم التصفية والبحث

    Args:
        skip: عدد العناصر للتخطي (للصفحات)
        limit: الحد الأقصى لعدد العناصر للإرجاع
        engine_type: تصفية حسب النوع
        active: تصفية حسب الحالة النشطة
        search: البحث في اسم محرك البحث

    Returns:
        قائمة محركات البحث
    """
    try:
        return service.get_search_engines(
            skip, limit, engine_type, active, search)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"],
        ) from exc


@router.get(
    "/{engine_id}",
    response_model=SearchEngineResponse,
    summary="الحصول على محرك بحث محدد",
)
async def get_search_engine(
    engine_id: int = Path(..., description=SEARCH_ENGINE_ID_DESCRIPTION),
    service: SearchEngineService = Depends(get_search_engine_service),
):
    """
    الحصول على محرك بحث محدد بواسطة المعرف

    Args:
        engine_id: معرف محرك البحث

    Returns:
        محرك البحث المطلوب

    Raises:
        HTTPException: إذا كان محرك البحث غير موجود
    """
    search_engine = service.get_search_engine(engine_id)
    if not search_engine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["SEARCH_ENGINE"]["NOT_FOUND"],
        )
    return search_engine


@router.put(
    "/{engine_id}",
    response_model=SearchEngineResponse,
    summary="تحديث محرك بحث",
)
async def update_search_engine(
    engine_id: int = Path(..., description=SEARCH_ENGINE_ID_DESCRIPTION),
    search_engine: SearchEngineUpdate = ...,
    service: SearchEngineService = Depends(get_search_engine_service),
):
    """
    تحديث محرك بحث موجود

    Args:
        engine_id: معرف محرك البحث
        search_engine: بيانات التحديث

    Returns:
        محرك البحث بعد التحديث

    Raises:
        HTTPException: إذا كان محرك البحث غير موجود أو كانت البيانات غير صالحة
    """
    try:
        updated_engine = service.update_search_engine(engine_id, search_engine)
        if not updated_engine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERROR_MESSAGES["SEARCH_ENGINE"]["NOT_FOUND"],
            )
        return updated_engine
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"],
        ) from exc


@router.delete(
    "/{engine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="حذف محرك بحث",
)
async def delete_search_engine(
    engine_id: int = Path(..., description=SEARCH_ENGINE_ID_DESCRIPTION),
    service: SearchEngineService = Depends(get_search_engine_service),
):
    """
    حذف محرك بحث موجود

    Args:
        engine_id: معرف محرك البحث

    Raises:
        HTTPException: إذا كان محرك البحث غير موجود
    """
    success = service.delete_search_engine(engine_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES["SEARCH_ENGINE"]["NOT_FOUND"],
        )


@router.get(
    "/{engine_id}/stats",
    response_model=SearchEngineStatsResponse,
    summary="الحصول على إحصائيات محرك بحث",
)
async def get_search_engine_stats(
    engine_id: int = Path(..., description=SEARCH_ENGINE_ID_DESCRIPTION),
    start_date: Optional[str] = Query(None, description="تاريخ البداية (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="تاريخ النهاية (YYYY-MM-DD)"),
    service: SearchEngineService = Depends(get_search_engine_service),
):
    """
    الحصول على إحصائيات محرك بحث محدد

    Args:
        engine_id: معرف محرك البحث
        start_date: تاريخ البداية (اختياري)
        end_date: تاريخ النهاية (اختياري)

    Returns:
        إحصائيات محرك البحث

    Raises:
        HTTPException: إذا كان محرك البحث غير موجود
    """
    try:
        stats = service.get_search_engine_stats(
            engine_id, start_date, end_date)
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERROR_MESSAGES["SEARCH_ENGINE"]["NOT_FOUND"],
            )
        return stats
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"],
        ) from exc


@router.post(
    "/{engine_id}/test",
    status_code=status.HTTP_200_OK,
    summary="اختبار محرك بحث",
)
async def test_search_engine(
    engine_id: int = Path(..., description=SEARCH_ENGINE_ID_DESCRIPTION),
    query: str = Query(..., description="استعلام الاختبار"),
    service: SearchEngineService = Depends(get_search_engine_service),
):
    """
    اختبار محرك بحث محدد باستعلام

    Args:
        engine_id: معرف محرك البحث
        query: استعلام الاختبار

    Returns:
        نتائج الاختبار

    Raises:
        HTTPException: إذا كان محرك البحث غير موجود أو فشل الاختبار
    """
    try:
        result = service.test_search_engine(engine_id, query)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERROR_MESSAGES["SEARCH_ENGINE"]["NOT_FOUND"],
            )
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"],
        ) from exc


@router.put(
    "/load-balancing",
    status_code=status.HTTP_200_OK,
    summary="تحديث استراتيجية توزيع الحمل",
)
async def update_load_balancing_strategy(
    strategy: LoadBalancingStrategyUpdate,
    service: SearchEngineService = Depends(get_search_engine_service),
):
    """
    تحديث استراتيجية توزيع الحمل لمحركات البحث

    Args:
        strategy: استراتيجية توزيع الحمل الجديدة

    Returns:
        نتيجة التحديث

    Raises:
        HTTPException: إذا فشل التحديث
    """
    try:
        result = service.update_load_balancing_strategy(strategy)
        return {
            "message": SUCCESS_MESSAGES["SEARCH_ENGINE"]["UPDATED"],
            "data": result}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_MESSAGES["GENERAL"]["INTERNAL_ERROR"],
        ) from exc
