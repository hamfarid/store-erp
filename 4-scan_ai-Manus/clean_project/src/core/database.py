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
        # إنشاء محرك قاعدة البيانات
        engine = create_engine(
            settings.database_url,
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
            logger.info("✅ تم الاتصال بقاعدة البيانات بنجاح")
            
    except Exception as e:
        logger.error(f"❌ فشل في الاتصال بقاعدة البيانات: {e}")
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
        logger.error(f"فحص صحة قاعدة البيانات فشل: {e}")
        return False

