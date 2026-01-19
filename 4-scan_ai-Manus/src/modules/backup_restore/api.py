"""
Backup and Restore API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import logging

from src.modules.auth.auth_service import get_current_user
from .backup_service_enhanced import EnhancedBackupService
from .schemas import BackupRequest, BackupResponse, RestoreRequest, RestoreResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/backup", tags=["backup"])
backup_service = EnhancedBackupService()


@router.post("/create", response_model=BackupResponse)
async def create_backup(
    request: BackupRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    إنشاء نسخة احتياطية جديدة
    
    Args:
        request: طلب النسخ الاحتياطي
        current_user: المستخدم الحالي
        
    Returns:
        BackupResponse: معلومات النسخة الاحتياطية
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لإنشاء نسخة احتياطية"
            )
        
        # إنشاء النسخة الاحتياطية
        result = await backup_service.create_backup(
            backup_type=request.backup_type,
            description=request.description,
            include_media=request.include_media,
            compress=request.compress
        )
        
        return BackupResponse(**result)
        
    except Exception as e:
        logger.error(f"خطأ في إنشاء النسخة الاحتياطية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=List[BackupResponse])
async def list_backups(
    current_user: dict = Depends(get_current_user)
):
    """
    عرض قائمة النسخ الاحتياطية المتاحة
    
    Args:
        current_user: المستخدم الحالي
        
    Returns:
        List[BackupResponse]: قائمة النسخ الاحتياطية
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لعرض النسخ الاحتياطية"
            )
        
        # الحصول على قائمة النسخ الاحتياطية
        backups = await backup_service.list_backups()
        
        return [BackupResponse(**backup) for backup in backups]
        
    except Exception as e:
        logger.error(f"خطأ في عرض النسخ الاحتياطية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/restore", response_model=RestoreResponse)
async def restore_backup(
    request: RestoreRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    استعادة نسخة احتياطية
    
    Args:
        request: طلب الاستعادة
        current_user: المستخدم الحالي
        
    Returns:
        RestoreResponse: نتيجة الاستعادة
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لاستعادة النسخ الاحتياطية"
            )
        
        # استعادة النسخة الاحتياطية
        result = await backup_service.restore_backup(
            backup_id=request.backup_id,
            restore_database=request.restore_database,
            restore_media=request.restore_media,
            restore_config=request.restore_config
        )
        
        return RestoreResponse(**result)
        
    except Exception as e:
        logger.error(f"خطأ في استعادة النسخة الاحتياطية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{backup_id}")
async def delete_backup(
    backup_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    حذف نسخة احتياطية
    
    Args:
        backup_id: معرف النسخة الاحتياطية
        current_user: المستخدم الحالي
        
    Returns:
        dict: نتيجة الحذف
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لحذف النسخ الاحتياطية"
            )
        
        # حذف النسخة الاحتياطية
        await backup_service.delete_backup(backup_id)
        
        return {"success": True, "message": "تم حذف النسخة الاحتياطية بنجاح"}
        
    except Exception as e:
        logger.error(f"خطأ في حذف النسخة الاحتياطية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedule")
async def schedule_backup(
    schedule_config: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """
    جدولة نسخة احتياطية تلقائية
    
    Args:
        schedule_config: إعدادات الجدولة
        current_user: المستخدم الحالي
        
    Returns:
        dict: نتيجة الجدولة
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لجدولة النسخ الاحتياطية"
            )
        
        # جدولة النسخة الاحتياطية
        result = await backup_service.schedule_backup(schedule_config)
        
        return result
        
    except Exception as e:
        logger.error(f"خطأ في جدولة النسخة الاحتياطية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedule/list")
async def list_scheduled_backups(
    current_user: dict = Depends(get_current_user)
):
    """
    عرض قائمة النسخ الاحتياطية المجدولة
    
    Args:
        current_user: المستخدم الحالي
        
    Returns:
        List[dict]: قائمة الجدولات
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لعرض الجدولات"
            )
        
        # الحصول على قائمة الجدولات
        schedules = await backup_service.list_scheduled_backups()
        
        return schedules
        
    except Exception as e:
        logger.error(f"خطأ في عرض الجدولات: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/schedule/{schedule_id}")
async def delete_scheduled_backup(
    schedule_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    حذف جدولة نسخة احتياطية
    
    Args:
        schedule_id: معرف الجدولة
        current_user: المستخدم الحالي
        
    Returns:
        dict: نتيجة الحذف
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لحذف الجدولات"
            )
        
        # حذف الجدولة
        await backup_service.delete_scheduled_backup(schedule_id)
        
        return {"success": True, "message": "تم حذف الجدولة بنجاح"}
        
    except Exception as e:
        logger.error(f"خطأ في حذف الجدولة: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{backup_id}")
async def get_backup_status(
    backup_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    الحصول على حالة نسخة احتياطية
    
    Args:
        backup_id: معرف النسخة الاحتياطية
        current_user: المستخدم الحالي
        
    Returns:
        dict: حالة النسخة الاحتياطية
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لعرض حالة النسخ الاحتياطية"
            )
        
        # الحصول على حالة النسخة الاحتياطية
        status = await backup_service.get_backup_status(backup_id)
        
        return status
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على حالة النسخة الاحتياطية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify/{backup_id}")
async def verify_backup(
    backup_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    التحقق من سلامة نسخة احتياطية
    
    Args:
        backup_id: معرف النسخة الاحتياطية
        current_user: المستخدم الحالي
        
    Returns:
        dict: نتيجة التحقق
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية للتحقق من النسخ الاحتياطية"
            )
        
        # التحقق من النسخة الاحتياطية
        result = await backup_service.verify_backup(backup_id)
        
        return result
        
    except Exception as e:
        logger.error(f"خطأ في التحقق من النسخة الاحتياطية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/storage/info")
async def get_storage_info(
    current_user: dict = Depends(get_current_user)
):
    """
    الحصول على معلومات التخزين
    
    Args:
        current_user: المستخدم الحالي
        
    Returns:
        dict: معلومات التخزين
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لعرض معلومات التخزين"
            )
        
        # الحصول على معلومات التخزين
        storage_info = await backup_service.get_storage_info()
        
        return storage_info
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على معلومات التخزين: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup")
async def cleanup_old_backups(
    days_to_keep: int = 30,
    current_user: dict = Depends(get_current_user)
):
    """
    تنظيف النسخ الاحتياطية القديمة
    
    Args:
        days_to_keep: عدد الأيام للاحتفاظ بالنسخ
        current_user: المستخدم الحالي
        
    Returns:
        dict: نتيجة التنظيف
    """
    try:
        # التحقق من الصلاحيات
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="ليس لديك صلاحية لتنظيف النسخ الاحتياطية"
            )
        
        # تنظيف النسخ القديمة
        result = await backup_service.cleanup_old_backups(days_to_keep)
        
        return result
        
    except Exception as e:
        logger.error(f"خطأ في تنظيف النسخ الاحتياطية: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Database connection setup (if needed)
def get_db():
    """Get database session"""
    from src.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
