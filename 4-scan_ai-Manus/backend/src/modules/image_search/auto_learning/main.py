# /home/ubuntu/image_search_integration/auto_learning/main.py
"""
نقطة الدخول الرئيسية لمديول البحث الذاتي الذكي

يقوم هذا الملف بإعداد وتشغيل تطبيق FastAPI لمديول البحث الذاتي الذكي،
ويقوم بتسجيل جميع نقاط النهاية API وإعداد الاتصال بقاعدة البيانات والخدمات الأخرى.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .a2a_integration import a2a_integration
from .api import router as main_router
from .config import settings
from .keyword_management.api import router as keyword_router
from .memory_integration import memory_integration
from .search_engine_management.api import router as search_engine_router
from .source_management.api import router as source_router
from .utils.helpers import get_db

# إعداد التسجيل
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="مديول البحث الذاتي الذكي",
    description="واجهة برمجة التطبيقات لمديول البحث الذاتي الذكي في نظام Gaara ERP",
    version="1.0.0",
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل أجهزة التوجيه
app.include_router(
    main_router,
    prefix="/api/auto_learning",
    tags=["auto_learning"])
app.include_router(
    keyword_router, prefix="/api/auto_learning/keywords", tags=["keywords"]
)
app.include_router(
    source_router,
    prefix="/api/auto_learning/sources",
    tags=["sources"])
app.include_router(
    search_engine_router,
    prefix="/api/auto_learning/search_engines",
    tags=["search_engines"],
)


@app.on_event("startup")
async def startup_event():
    """
    يتم تنفيذ هذه الدالة عند بدء تشغيل التطبيق
    """
    logger.info("بدء تشغيل مديول البحث الذاتي الذكي")

    # التحقق من الاتصال بقاعدة البيانات
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        logger.info("تم الاتصال بقاعدة البيانات بنجاح")
    except Exception as e:
        logger.error(f"فشل الاتصال بقاعدة البيانات: {str(e)}")
        raise

    # التحقق من الاتصال بنظام الذاكرة المركزية
    if memory_integration.check_connection():
        logger.info("تم الاتصال بنظام الذاكرة المركزية بنجاح")
    else:
        logger.warning("فشل الاتصال بنظام الذاكرة المركزية")

    # التحقق من الاتصال بنظام A2A وتسجيل التطبيق
    if a2a_integration.check_connection():
        logger.info("تم الاتصال بنظام A2A بنجاح")
        if a2a_integration.register_app():
            logger.info("تم تسجيل التطبيق في نظام A2A بنجاح")
        else:
            logger.warning("فشل تسجيل التطبيق في نظام A2A")
    else:
        logger.warning("فشل الاتصال بنظام A2A")


@app.on_event("shutdown")
async def shutdown_event():
    """
    يتم تنفيذ هذه الدالة عند إيقاف تشغيل التطبيق
    """
    logger.info("إيقاف تشغيل مديول البحث الذاتي الذكي")


@app.get("/health")
async def health_check():
    """
    نقطة نهاية للتحقق من صحة التطبيق

    Returns:
        dict: حالة التطبيق
    """
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
