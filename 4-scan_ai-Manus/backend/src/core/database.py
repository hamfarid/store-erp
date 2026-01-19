"""
إعداد قاعدة البيانات - اتصال وتهيئة قاعدة البيانات
Database Setup - Database connection and initialization
"""

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Settings

logger = logging.getLogger(__name__)

# قاعدة النماذج
Base = declarative_base()


# Patch Base.metadata.drop_all to dispose the bound engine after dropping.
# This is especially important on Windows + SQLite, where open pooled
# connections can prevent deleting the database file in tests.
_original_drop_all = Base.metadata.drop_all


def _drop_all_and_dispose(*args, **kwargs):
    bind = kwargs.get("bind")
    if bind is None and len(args) >= 1:
        # MetaData.drop_all(bind, ...)
        bind = args[0]
    result = _original_drop_all(*args, **kwargs)
    try:
        if bind is not None and hasattr(bind, "dispose"):
            bind.dispose()
    except Exception:
        # Best-effort; never fail schema teardown
        pass
    return result


Base.metadata.drop_all = _drop_all_and_dispose

# متغيرات عامة
engine = None
SessionLocal = None


def init_database(settings: Settings):
    """
    تهيئة قاعدة البيانات
    Initialize database
    """
    global engine, SessionLocal

    try:
        db_url = settings.database_url

        # Configure engine based on database type
        if db_url.startswith("sqlite"):
            # SQLite-specific configuration
            engine = create_engine(
                db_url,
                connect_args={"check_same_thread": False},
                echo=settings.DEBUG
            )
        else:
            # PostgreSQL and other databases
            engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=settings.DEBUG
            )

        # إنشاء مصنع الجلسات
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )

        # اختبار الاتصال
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("[OK] تم الاتصال بقاعدة البيانات بنجاح")

    except Exception as e:
        logger.error("[ERROR] فشل في الاتصال بقاعدة البيانات: %s", e)
        raise


def get_db():
    """
    الحصول على جلسة قاعدة البيانات
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_health() -> bool:
    """
    فحص صحة قاعدة البيانات
    Check database health
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return True
    except Exception as e:
        logger.error("فحص صحة قاعدة البيانات فشل: %s", e)
        return False
