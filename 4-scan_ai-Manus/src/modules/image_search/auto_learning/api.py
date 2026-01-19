# /home/ubuntu/image_search_integration/auto_learning/api.py
"""
نقطة دخول API الرئيسية لمديول البحث الذاتي الذكي

يحتوي هذا الملف على نقطة دخول API الرئيسية لمديول البحث الذاتي الذكي،
ويقوم بتسجيل جميع مسارات API الخاصة بالمديول.
"""

from fastapi import APIRouter, HTTPException

from .keyword_management.api import router as keyword_router
from .source_management.api import router as source_router
from .search_engine_management.api import router as search_engine_router

# إنشاء موجه API الرئيسي
router = APIRouter(
    prefix="/api/auto_learning",
    tags=["auto_learning"],
    responses={
        404: {"description": "العنصر غير موجود"},
        500: {"description": "خطأ داخلي في الخادم"}
    }
)

# تسجيل موجهات API الفرعية
router.include_router(keyword_router, prefix="/keywords")
router.include_router(source_router, prefix="/sources")
router.include_router(search_engine_router, prefix="/search_engines")


@router.get("/", summary="الحصول على معلومات المديول")
async def get_module_info():
    """
    الحصول على معلومات مديول البحث الذاتي الذكي
    """
    return {
        "name": "مديول البحث الذاتي الذكي",
        "version": "1.0.0",
        "description": "مديول لإدارة الكلمات المفتاحية والمصادر الموثوقة ومحركات البحث لتحسين عمليات البحث الذاتي عن صور الإصابات والآفات النباتية",
        "endpoints": {
            "keywords": "/api/auto_learning/keywords",
            "sources": "/api/auto_learning/sources",
            "search_engines": "/api/auto_learning/search_engines"
        }
    }


@router.get("/health", summary="فحص صحة المديول")
async def health_check():
    """
    فحص صحة مديول البحث الذاتي الذكي
    """
    return {
        "status": "healthy",
        "message": "مديول البحث الذاتي الذكي يعمل بشكل صحيح"
    }


@router.get("/stats", summary="الحصول على إحصائيات المديول")
async def get_module_stats():
    """
    الحصول على إحصائيات مديول البحث الذاتي الذكي
    """
    try:
        # هنا يمكن إضافة منطق لجمع الإحصائيات من الخدمات المختلفة
        return {
            "keywords": {
                "total": 0,  # سيتم استبدالها بالقيم الفعلية
                "by_category": {}
            },
            "sources": {
                "total": 0,  # سيتم استبدالها بالقيم الفعلية
                "verified": 0,
                "blacklisted": 0
            },
            "search_engines": {
                "total": 0,  # سيتم استبدالها بالقيم الفعلية
                "active": 0
            },
            "searches": {
                "total": 0,  # سيتم استبدالها بالقيم الفعلية
                "successful": 0,
                "failed": 0
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="خطأ داخلي في الخادم"
        ) from e
