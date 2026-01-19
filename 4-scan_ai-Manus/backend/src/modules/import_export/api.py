"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/import_export/api.py
الوصف: واجهة برمجة التطبيقات لمديول الاستيراد والتصدير
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.database import get_db
from src.modules.activity_log.integration import log_activity
from src.modules.auth.dependencies import get_current_user
from src.modules.import_export import schemas, service
from src.modules.import_export.dependencies import (
    validate_export_request,
    validate_import_file,
)
from src.modules.permissions.dependencies import check_permission

# Constants for repeated string literals
TEMPLATE_NOT_FOUND = "Template not found"

router = APIRouter(
    prefix="/api/import-export",
    tags=["import-export"],
    responses={404: {"description": "Not found"}},
)


@router.get("/modules", response_model=List[schemas.ModuleInfo])
@log_activity(module_id="import_export", action_id="list_modules")
async def get_available_modules(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="view"))
):
    """
    الحصول على قائمة المديولات المتاحة للاستيراد والتصدير
    """
    return await service.get_available_modules(db, current_user)


@router.get("/templates", response_model=List[schemas.ImportExportTemplate])
@log_activity(module_id="import_export", action_id="list_templates")
async def get_templates(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="view"))
):
    """
    الحصول على قائمة قوالب الاستيراد والتصدير
    """
    return await service.get_templates(db, current_user)


@router.post("/templates", response_model=schemas.ImportExportTemplate)
@log_activity(module_id="import_export", action_id="create_template")
async def create_template(
    template: schemas.ImportExportTemplateCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="manage_templates"))
):
    """
    إنشاء قالب استيراد/تصدير جديد
    """
    return await service.create_template(db, template, current_user)


@router.get("/templates/{template_id}",
            response_model=schemas.ImportExportTemplate)
@log_activity(module_id="import_export", action_id="get_template")
async def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="view"))
):
    """
    الحصول على قالب استيراد/تصدير محدد
    """
    template = await service.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail=TEMPLATE_NOT_FOUND)
    return template


@router.put("/templates/{template_id}",
            response_model=schemas.ImportExportTemplate)
@log_activity(module_id="import_export", action_id="update_template")
async def update_template(
    template_id: int,
    template_update: schemas.ImportExportTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="manage_templates"))
):
    """
    تحديث قالب استيراد/تصدير محدد
    """
    template = await service.update_template(db, template_id, template_update, current_user)
    if not template:
        raise HTTPException(status_code=404, detail=TEMPLATE_NOT_FOUND)
    return template


@router.delete("/templates/{template_id}",
               response_model=schemas.DeleteResponse)
@log_activity(module_id="import_export", action_id="delete_template")
async def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="manage_templates"))
):
    """
    حذف قالب استيراد/تصدير محدد
    """
    success = await service.delete_template(db, template_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail=TEMPLATE_NOT_FOUND)
    return {"success": True, "message": "Template deleted successfully"}


@router.post("/import", response_model=schemas.ImportResult)
@log_activity(module_id="import_export", action_id="import_data")
async def import_data(  # pylint: disable=too-many-positional-arguments
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    module: str = Form(...),
    template_id: Optional[int] = Form(None),
    options: Optional[str] = Form("{}"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(
        check_permission(
        module="import_export",
        permission="import"))
):
    """
    استيراد بيانات من ملف
    """
    # التحقق من صحة الملف
    await validate_import_file(file, module)

    # استيراد البيانات
    result = await service.import_data(
        db,
        background_tasks,
        file,
        module,
        template_id,
        options,
        current_user
    )

    return result


@router.post("/export", response_model=schemas.ExportResult)
@log_activity(module_id="import_export", action_id="export_data")
async def export_data(
    background_tasks: BackgroundTasks,
    export_request: schemas.ExportRequest,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="export"))
):
    """
    تصدير بيانات إلى ملف
    """
    # التحقق من صحة طلب التصدير
    await validate_export_request(export_request)

    # تصدير البيانات
    result = await service.export_data(
        db,
        background_tasks,
        export_request,
        current_user
    )

    return result


@router.get("/download/{file_id}", response_class=FileResponse)
@log_activity(module_id="import_export", action_id="download_file")
async def download_export_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="export"))
):
    """
    تنزيل ملف مصدر
    """
    file_path = await service.get_export_file_path(db, file_id, current_user)
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/octet-stream"
    )


@router.get("/status/{job_id}", response_model=schemas.JobStatus)
@log_activity(module_id="import_export", action_id="check_job_status")
async def check_job_status(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="view"))
):
    """
    التحقق من حالة مهمة استيراد/تصدير
    """
    status = await service.get_job_status(db, job_id, current_user)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status


@router.get("/settings", response_model=schemas.ImportExportSettings)
@log_activity(module_id="import_export", action_id="get_settings")
async def get_settings(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="admin"))
):
    """
    الحصول على إعدادات الاستيراد والتصدير
    """
    return await service.get_settings(db, current_user)


@router.put("/settings", response_model=schemas.ImportExportSettings)
@log_activity(module_id="import_export", action_id="update_settings")
async def update_settings(
    settings: schemas.ImportExportSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="admin"))
):
    """
    تحديث إعدادات الاستيراد والتصدير
    """
    return await service.update_settings(db, settings, current_user)


@router.get("/history", response_model=schemas.PaginatedImportExportJobs)
@log_activity(module_id="import_export", action_id="get_history")
async def get_history(  # pylint: disable=too-many-positional-arguments
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    job_type: Optional[str] = Query(None),
    module: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(
        check_permission(
        module="import_export",
        permission="view"))
):
    """
    الحصول على سجل عمليات الاستيراد والتصدير
    """
    return await service.get_job_history(
        db,
        page,
        page_size,
        job_type,
        module,
        status,
        start_date,
        end_date,
        current_user
    )


@router.post("/validate-mapping", response_model=schemas.ValidationResult)
@log_activity(module_id="import_export", action_id="validate_mapping")
async def validate_field_mapping(
    validation_request: schemas.ValidationRequest,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user),
    _: bool = Depends(check_permission(module="import_export", permission="import"))
):
    """
    التحقق من صحة تعيين الحقول للاستيراد
    """
    return await service.validate_field_mapping(db, validation_request, current_user)
