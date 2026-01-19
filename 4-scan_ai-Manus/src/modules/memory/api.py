"""
/home/ubuntu/implemented_files/v3/src/modules/memory/api.py

ملف واجهة برمجة التطبيقات (API) لمديول الذاكرة المركزية

يوفر هذا الملف نقاط نهاية API لمديول الذاكرة المركزية، بما في ذلك:
- إنشاء وتحديث واسترجاع وحذف الذكريات
- البحث في الذاكرة (نصي ودلالي)
- إدارة العلامات والكيانات
- استرجاع الإحصائيات
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.modules.permissions.service import PermissionService

from .service import MemoryService
from .schemas import (
    MemoryCreate, MemoryUpdate, MemoryResponse, MemoryList,
    MemorySearch, SemanticSearchResults,
    TagCreate, TagResponse, EntityCreate, EntityResponse,
    MemoryAccessLogResponse, MemoryStats
)

# إنشاء موجه API
router = APIRouter(
    prefix="/api/v3/memory",
    tags=["memory"],
    responses={404: {"description": "Not found"}},
)

# ثوابت
MEMORY_ID_DESCRIPTION = "معرف الذاكرة"

# ==================== نقاط نهاية إدارة الذاكرة ====================


@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    memory_data: MemoryCreate,
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    إنشاء ذاكرة جديدة

    المعلمات:
        memory_data: بيانات الذاكرة المراد إنشاؤها
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        MemoryResponse: الذاكرة المنشأة

    يرفع:
        HTTPException: إذا فشلت عملية الإنشاء أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    user_id = permission_service.get_current_user_id()
    if not permission_service.check_permission("memory", "create"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية إنشاء ذاكرة جديدة"
        )

    # إضافة معرف المستخدم إلى بيانات الذاكرة
    memory_data.created_by = user_id

    # إنشاء الذاكرة
    memory_service = MemoryService(db)
    try:
        memory = memory_service.create_memory(memory_data)
        return memory
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل إنشاء الذاكرة: {str(e)}"
        ) from e


@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: str = Path(..., description=MEMORY_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    استرجاع ذاكرة بواسطة المعرف

    المعلمات:
        memory_id: معرف الذاكرة
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        MemoryResponse: الذاكرة المسترجعة

    يرفع:
        HTTPException: إذا لم يتم العثور على الذاكرة أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    user_id = permission_service.get_current_user_id()

    # استرجاع الذاكرة
    memory_service = MemoryService(db)
    memory = memory_service.get_memory(memory_id, user_id)

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الذاكرة بالمعرف {memory_id}"
        )

    return memory


@router.put("/{memory_id}", response_model=MemoryResponse)
async def update_memory(
    memory_data: MemoryUpdate,
    memory_id: str = Path(..., description=MEMORY_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    تحديث ذاكرة موجودة

    المعلمات:
        memory_data: بيانات التحديث
        memory_id: معرف الذاكرة
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        MemoryResponse: الذاكرة المحدثة

    يرفع:
        HTTPException: إذا لم يتم العثور على الذاكرة أو فشل التحديث أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    user_id = permission_service.get_current_user_id()
    if not permission_service.check_permission("memory", "update"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية تحديث الذاكرة"
        )

    # تحديث الذاكرة
    memory_service = MemoryService(db)
    memory = memory_service.update_memory(memory_id, memory_data, user_id)

    if not memory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الذاكرة بالمعرف {memory_id} أو ليس لديك صلاحية تحديثها"
        )

    return memory


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: str = Path(..., description=MEMORY_ID_DESCRIPTION),
    permanent: bool = Query(False, description="ما إذا كان الحذف دائماً"),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    حذف ذاكرة

    المعلمات:
        memory_id: معرف الذاكرة
        permanent: ما إذا كان الحذف دائماً أم منطقياً
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        None

    يرفع:
        HTTPException: إذا لم يتم العثور على الذاكرة أو فشل الحذف أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    user_id = permission_service.get_current_user_id()

    # التحقق من صلاحية الحذف الدائم
    if permanent and not permission_service.check_permission("memory", "permanent_delete"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية الحذف الدائم للذاكرة"
        )

    # التحقق من صلاحية الحذف العادي
    if not permission_service.check_permission("memory", "delete"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية حذف الذاكرة"
        )

    # حذف الذاكرة
    memory_service = MemoryService(db)
    success = memory_service.delete_memory(memory_id, user_id, permanent)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الذاكرة بالمعرف {memory_id} أو ليس لديك صلاحية حذفها"
        )


@router.post("/{memory_id}/archive", status_code=status.HTTP_204_NO_CONTENT)
async def archive_memory(
    memory_id: str = Path(..., description=MEMORY_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    أرشفة ذاكرة

    المعلمات:
        memory_id: معرف الذاكرة
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        None

    يرفع:
        HTTPException: إذا لم يتم العثور على الذاكرة أو فشلت الأرشفة أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    user_id = permission_service.get_current_user_id()
    if not permission_service.check_permission("memory", "archive"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية أرشفة الذاكرة"
        )

    # أرشفة الذاكرة
    memory_service = MemoryService(db)
    success = memory_service.archive_memory(memory_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الذاكرة بالمعرف {memory_id} أو ليس لديك صلاحية أرشفتها"
        )


@router.post("/{memory_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_memory(
    memory_id: str = Path(..., description=MEMORY_ID_DESCRIPTION),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    استعادة ذاكرة مؤرشفة أو محذوفة

    المعلمات:
        memory_id: معرف الذاكرة
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        None

    يرفع:
        HTTPException: إذا لم يتم العثور على الذاكرة أو فشلت الاستعادة أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    user_id = permission_service.get_current_user_id()
    if not permission_service.check_permission("memory", "restore"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية استعادة الذاكرة"
        )

    # استعادة الذاكرة
    memory_service = MemoryService(db)
    success = memory_service.restore_memory(memory_id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الذاكرة بالمعرف {memory_id} أو ليس لديك صلاحية استعادتها"
        )

# ==================== نقاط نهاية البحث في الذاكرة ====================


@router.post("/search", response_model=MemoryList)
async def search_memories(
    search_params: MemorySearch,
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    البحث في الذاكرة

    المعلمات:
        search_params: معلمات البحث
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        MemoryList: قائمة الذكريات المطابقة لمعلمات البحث

    يرفع:
        HTTPException: إذا فشل البحث أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    user_id = permission_service.get_current_user_id()
    if not permission_service.check_permission("memory", "search"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية البحث في الذاكرة"
        )

    # البحث في الذاكرة
    memory_service = MemoryService(db)
    results = memory_service.search_memories(search_params, user_id)

    return results


@router.post("/semantic-search", response_model=SemanticSearchResults)
async def semantic_search(
    query: str = Body(..., embed=True, description="نص البحث"),
    top_k: int = Query(5, description="عدد النتائج المطلوبة"),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    البحث الدلالي في الذاكرة

    المعلمات:
        query: نص البحث
        top_k: عدد النتائج المطلوبة
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        SemanticSearchResults: نتائج البحث الدلالي

    يرفع:
        HTTPException: إذا فشل البحث أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    user_id = permission_service.get_current_user_id()
    if not permission_service.check_permission("memory", "semantic_search"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية البحث الدلالي في الذاكرة"
        )

    # البحث الدلالي في الذاكرة
    memory_service = MemoryService(db)
    results = memory_service.semantic_search(query, top_k, user_id)

    return results

# ==================== نقاط نهاية إدارة العلامات والكيانات ====================


@router.post("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    إنشاء علامة جديدة

    المعلمات:
        tag_data: بيانات العلامة
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        TagResponse: العلامة المنشأة

    يرفع:
        HTTPException: إذا فشلت عملية الإنشاء أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    if not permission_service.check_permission("memory", "manage_tags"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية إدارة العلامات"
        )

    # إنشاء العلامة
    memory_service = MemoryService(db)
    try:
        tag = memory_service.create_tag(tag_data)
        return tag
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل إنشاء العلامة: {str(e)}"
        ) from e


@router.get("/tags", response_model=List[TagResponse])
async def get_all_tags(
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    استرجاع جميع العلامات

    المعلمات:
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        List[TagResponse]: قائمة العلامات

    يرفع:
        HTTPException: إذا فشلت عملية الاسترجاع أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    if not permission_service.check_permission("memory", "view_tags"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية عرض العلامات"
        )

    # استرجاع العلامات
    memory_service = MemoryService(db)
    tags = memory_service.get_all_tags()

    return tags


@router.post("/entities", response_model=EntityResponse, status_code=status.HTTP_201_CREATED)
async def create_entity(
    entity_data: EntityCreate,
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    إنشاء كيان جديد

    المعلمات:
        entity_data: بيانات الكيان
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        EntityResponse: الكيان المنشأ

    يرفع:
        HTTPException: إذا فشلت عملية الإنشاء أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    if not permission_service.check_permission("memory", "manage_entities"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية إدارة الكيانات"
        )

    # إنشاء الكيان
    memory_service = MemoryService(db)
    try:
        entity = memory_service.create_entity(entity_data)
        return entity
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل إنشاء الكيان: {str(e)}"
        ) from e


@router.get("/entities/{entity_type}", response_model=List[EntityResponse])
async def get_entities_by_type(
    entity_type: str = Path(..., description="نوع الكيان"),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    استرجاع الكيانات حسب النوع

    المعلمات:
        entity_type: نوع الكيان
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        List[EntityResponse]: قائمة الكيانات

    يرفع:
        HTTPException: إذا فشلت عملية الاسترجاع أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    if not permission_service.check_permission("memory", "view_entities"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية عرض الكيانات"
        )

    # استرجاع الكيانات
    memory_service = MemoryService(db)
    entities = memory_service.get_entities_by_type(entity_type)

    return entities

# ==================== نقاط نهاية الإحصائيات والتحليل ====================


@router.get("/stats", response_model=MemoryStats)
async def get_memory_stats(
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    استرجاع إحصائيات الذاكرة

    المعلمات:
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        MemoryStats: إحصائيات الذاكرة

    يرفع:
        HTTPException: إذا فشلت عملية الاسترجاع أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    if not permission_service.check_permission("memory", "view_stats"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية عرض إحصائيات الذاكرة"
        )

    # استرجاع الإحصائيات
    memory_service = MemoryService(db)
    stats = memory_service.get_memory_stats()

    return stats


@router.get("/{memory_id}/access-logs", response_model=List[MemoryAccessLogResponse])
async def get_memory_access_logs(
    memory_id: str = Path(..., description=MEMORY_ID_DESCRIPTION),
    limit: int = Query(100, description="الحد الأقصى لعدد السجلات"),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    استرجاع سجلات الوصول للذاكرة

    المعلمات:
        memory_id: معرف الذاكرة
        limit: الحد الأقصى لعدد السجلات
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        List[MemoryAccessLogResponse]: قائمة سجلات الوصول

    يرفع:
        HTTPException: إذا فشلت عملية الاسترجاع أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    if not permission_service.check_permission("memory", "view_access_logs"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية عرض سجلات الوصول للذاكرة"
        )

    # استرجاع سجلات الوصول
    memory_service = MemoryService(db)
    logs = memory_service.get_memory_access_logs(memory_id, limit)

    return logs

# ==================== نقاط نهاية الصيانة ====================


@router.post("/maintenance/cleanup-expired", status_code=status.HTTP_200_OK)
async def cleanup_expired_memories(
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    تنظيف الذكريات منتهية الصلاحية

    المعلمات:
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        Dict: عدد الذكريات التي تم تنظيفها

    يرفع:
        HTTPException: إذا فشلت عملية التنظيف أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    if not permission_service.check_permission("memory", "maintenance"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية صيانة الذاكرة"
        )

    # تنظيف الذكريات منتهية الصلاحية
    memory_service = MemoryService(db)
    count = memory_service.cleanup_expired_memories()

    return {"cleaned_count": count}


@router.put("/{memory_id}/importance", status_code=status.HTTP_200_OK)
async def update_memory_importance(
    memory_id: str = Path(..., description=MEMORY_ID_DESCRIPTION),
    importance_score: float = Body(..., embed=True, description="درجة الأهمية الجديدة"),
    db: Session = Depends(get_db),
    permission_service: PermissionService = Depends()
):
    """
    تحديث درجة أهمية الذاكرة

    المعلمات:
        memory_id: معرف الذاكرة
        importance_score: درجة الأهمية الجديدة
        db: جلسة قاعدة البيانات
        permission_service: خدمة التحقق من الصلاحيات

    العوائد:
        Dict: حالة التحديث

    يرفع:
        HTTPException: إذا فشلت عملية التحديث أو لم يكن لدى المستخدم الصلاحيات اللازمة
    """
    # التحقق من الصلاحيات
    if not permission_service.check_permission("memory", "update"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية تحديث الذاكرة"
        )

    # تحديث درجة الأهمية
    memory_service = MemoryService(db)
    success = memory_service.update_memory_importance(memory_id, importance_score)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الذاكرة بالمعرف {memory_id} أو ليس لديك صلاحية تحديثها"
        )

    return {"status": "success", "message": "تم تحديث درجة الأهمية بنجاح"}
