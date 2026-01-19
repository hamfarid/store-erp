"""
FILE: backend/src/main.py | PURPOSE: Main application entry point | OWNER: Backend Team | LAST-AUDITED: 2025-11-18

تطبيق Gaara Scan AI الرئيسي المحسن
Enhanced Main Application for Gaara Scan AI System

تم تقسيم الملف إلى وحدات منفصلة لسهولة الصيانة
Split into separate modules for easier maintenance

Version: 3.0.0 (Canonical)
"""

from src.core.logging_config import setup_logging
from src.core.config import get_settings
from src.core.app_factory import create_app
import sys
from pathlib import Path

# إضافة المسار الجذر للمشروع
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# استيراد الوحدات الأساسية


def main():
    """
    نقطة الدخول الرئيسية للتطبيق
    Main entry point for the application
    """
    # إعداد السجلات
    setup_logging()

    # تحميل الإعدادات
    settings = get_settings()

    # إنشاء التطبيق
    app = create_app(settings)

    return app


# إنشاء مثيل التطبيق
app = main()

if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "backend.src.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )
