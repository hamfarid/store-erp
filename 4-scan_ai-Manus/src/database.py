"""
Database module for Gaara ERP system

هذا الملف يوفر اتصال قاعدة البيانات وتعريفات النماذج الأساسية للنظام.
يتضمن آليات للاتصال بقاعدة البيانات، إدارة الجلسات، والتعامل مع الأخطاء.

المسار: /home/ubuntu/clean_project/src/database.py
"""

from sqlalchemy import create_engine, Column, String, DateTime, Boolean, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import uuid
import os
import time
import logging
from typing import Any, Dict, Generator
from contextlib import contextmanager
from datetime import datetime, timezone

from dotenv import load_dotenv


# Setup logging
logger = logging.getLogger(__name__)


# Load environment variables
load_dotenv()


# Get database connection info from environment variables
DB_USER = os.getenv("DB_USER", "agri_ai_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ATNqj7prF7au")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "agri_ai_db")


# Database connection settings
DB_CONNECTION_RETRIES = int(os.getenv("DB_CONNECTION_RETRIES", "3"))
DB_CONNECTION_RETRY_DELAY = int(os.getenv("DB_CONNECTION_RETRY_DELAY", "5"))
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))


# Create database connection URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class DatabaseConnectionError(Exception):
    """
    استثناء مخصص لأخطاء اتصال قاعدة البيانات

    يتم رفع هذا الاستثناء عندما تفشل جميع محاولات الاتصال بقاعدة البيانات.
    """
    pass


def create_db_engine(retries: int = DB_CONNECTION_RETRIES) -> Any:
    """
    إنشاء محرك قاعدة البيانات مع آلية إعادة المحاولة

    Args:
        retries (int): عدد محاولات إعادة الاتصال

    Returns:
        Any: محرك قاعدة البيانات

    Raises:
        DatabaseConnectionError: إذا فشلت جميع محاولات الاتصال
    """
    for attempt in range(retries):
        try:
            engine = create_engine(
                DATABASE_URL,
                pool_size=DB_POOL_SIZE,
                max_overflow=DB_MAX_OVERFLOW,
                pool_timeout=DB_POOL_TIMEOUT,
                pool_pre_ping=True,
                pool_recycle=DB_POOL_RECYCLE,
                echo=False
            )

            # Test connection
            with engine.connect() as conn:
                conn.execute("SELECT 1")

            logger.info("Successfully connected to database")
            return engine

        except OperationalError as e:
            if attempt < retries - 1:
                logger.warning(
                    f"Database connection failed (attempt {attempt + 1}/{retries}): {str(e)}")
                time.sleep(DB_CONNECTION_RETRY_DELAY)
            else:
                logger.error(
                    f"Database connection failed after {retries} attempts: {str(e)}")
                raise DatabaseConnectionError(
                    f"Database connection failed: {str(e)}")


# Create database engine (lazy initialization)
engine = None


def get_engine() -> Any:
    """
    الحصول على محرك قاعدة البيانات أو إنشاؤه إذا لم يكن موجودًا

    Returns:
        Any: محرك قاعدة البيانات

    Raises:
        DatabaseConnectionError: إذا فشل إنشاء محرك قاعدة البيانات
    """
    global engine
    if engine is None:
        engine = create_db_engine()
    return engine


# Create database session (lazy initialization)
SessionLocal = None
db_session = None


def get_session() -> scoped_session:
    """
    الحصول على جلسة قاعدة البيانات أو إنشاؤها إذا لم تكن موجودة

    Returns:
        scoped_session: جلسة قاعدة البيانات
    """
    global SessionLocal, db_session
    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine())
        db_session = scoped_session(SessionLocal)
    return db_session


# Create base model for all database models
Base = declarative_base()


def init_base() -> None:
    """
    تهيئة النموذج الأساسي مع خاصية الاستعلام
    """
    Base.query = get_session().query_property()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    مدير سياق لجلسة قاعدة البيانات

    يوفر هذا المدير جلسة قاعدة بيانات مع التعامل التلقائي مع الالتزام والتراجع.

    Yields:
        Session: جلسة قاعدة البيانات

    Raises:
        SQLAlchemyError: إذا حدث خطأ في قاعدة البيانات
    """
    if SessionLocal is None:
        get_session()

    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()


def check_db_health() -> Dict[str, Any]:
    """
    التحقق من صحة اتصال قاعدة البيانات

    Returns:
        Dict[str, Any]: معلومات صحة قاعدة البيانات
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            # Check connection
            conn.execute("SELECT 1")

            # Get active sessions info
            active_sessions = conn.execute("""
                SELECT count(*) as active_sessions
                FROM pg_stat_activity
                WHERE datname = %s
            """, (DB_NAME,)).scalar()

            # Get database size info
            db_size = conn.execute("""
                SELECT pg_size_pretty(pg_database_size(%s)) as size
            """, (DB_NAME,)).scalar()

            return {
                "status": "healthy",
                "active_sessions": active_sessions,
                "database_size": db_size,
                "pool_size": engine.pool.size(),
                "checked_at": datetime.now(timezone.utc)
            }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "checked_at": datetime.now(timezone.utc)
        }


def create_tables() -> None:
    """
    إنشاء جميع جداول قاعدة البيانات

    Raises:
        SQLAlchemyError: إذا فشل إنشاء الجداول
    """
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise


def drop_tables() -> None:
    """
    حذف جميع جداول قاعدة البيانات

    Raises:
        SQLAlchemyError: إذا فشل حذف الجداول
    """
    try:
        engine = get_engine()
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to drop database tables: {str(e)}")
        raise


class BaseModel:
    """
    النموذج الأساسي مع الحقول المشتركة لجميع النماذج

    يوفر هذا النموذج الحقول الأساسية التي يجب أن تكون موجودة في جميع نماذج قاعدة البيانات،
    مثل المعرف، تاريخ الإنشاء، تاريخ التحديث، وحالة النشاط.
    """
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل النموذج إلى قاموس

        Returns:
            Dict[str, Any]: قاموس يحتوي على بيانات النموذج
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@event.listens_for(Base.metadata, 'before_create')
def receive_before_create(target: Any, connection: Any, **kw: Any) -> None:
    """
    معالج الحدث قبل إنشاء الجدول

    Args:
        target: الهدف (عادة metadata)
        connection: اتصال قاعدة البيانات
        **kw: معلمات إضافية
    """
    logger.info(f"Creating tables in database {DB_NAME}")


@event.listens_for(Base.metadata, 'after_create')
def receive_after_create(target: Any, connection: Any, **kw: Any) -> None:
    """
    معالج الحدث بعد إنشاء الجدول

    Args:
        target: الهدف (عادة metadata)
        connection: اتصال قاعدة البيانات
        **kw: معلمات إضافية
    """
    logger.info("Tables created successfully")


def init_db() -> None:
    """
    تهيئة قاعدة البيانات

    تقوم هذه الدالة بتهيئة النموذج الأساسي، إنشاء الجداول إذا لم تكن موجودة،
    والتحقق من صحة الاتصال.

    Raises:
        Exception: إذا فشلت تهيئة قاعدة البيانات
    """
    try:
        # Initialize Base
        init_base()

        # Create tables if they don't exist
        create_tables()

        # Check connection health
        health_info = check_db_health()
        if health_info["status"] == "healthy":
            logger.info("Database initialized successfully")
            logger.info(f"Database info: {health_info}")
        else:
            logger.error(f"Database health check failed: {health_info}")

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise


# Run initial setup if file is run directly
if __name__ == "__main__":
    init_db()
