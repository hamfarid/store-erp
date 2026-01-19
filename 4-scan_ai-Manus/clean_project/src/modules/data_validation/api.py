# File: /home/ubuntu/ai_web_organized/src/modules/data_validation/api.py
"""
واجهة برمجة التطبيقات لخدمة التحقق من صحة البيانات
توفر هذه الوحدة واجهة برمجية للتحقق من صحة البيانات وإصلاحها
"""

import os
from typing import Dict, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .validation_service import ValidationService
from src.modules.auth.auth_service import get_current_user, check_permission

# ثوابت الصلاحيات
PERMISSION_VIEW = "data_validation:view"

# إنشاء موجه التوجيه
router = APIRouter(
    prefix="/api/data-validation",
    tags=["data-validation"],
    responses={404: {"description": "Not found"}},
)

# إنشاء خدمة التحقق من صحة البيانات
validation_service = ValidationService()

# نماذج البيانات


class ValidationRequest(BaseModel):
    data: Optional[Union[Dict, List]] = None
    data_type: Optional[str] = None
    rules: Optional[Dict] = None


class ValidationTaskResponse(BaseModel):
    id: str
    type: str
    data_type: Optional[str] = None
    status: str
    created_at: str
    completed_at: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None


class FixRequest(BaseModel):
    validation_id: Optional[str] = None
    validation_file: Optional[str] = None
    auto_fix: Optional[bool] = None


class DatabaseValidationRequest(BaseModel):
    tables: Optional[List[str]] = None
    rules: Optional[Dict] = None


class ConfigUpdateRequest(BaseModel):
    config: Dict


class ValidationRulesUpdateRequest(BaseModel):
    data_type: str
    rules: Dict

# نقاط النهاية


@router.post("/validate", response_model=ValidationTaskResponse)
async def validate_data(
    request: ValidationRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    التحقق من صحة البيانات
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:validate")

    try:
        # التحقق من صحة البيانات
        task_info = validation_service.validate_data(
            data=request.data,
            data_type=request.data_type,
            rules=request.rules
        )

        return task_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate/file", response_model=ValidationTaskResponse)
async def validate_file(
    file: UploadFile = File(...),
    data_type: Optional[str] = Form(None),
    current_user: Dict = Depends(get_current_user)
):
    """
    التحقق من صحة ملف بيانات
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:validate")

    try:
        # حفظ الملف مؤقتاً
        temp_file_path = os.path.join(validation_service.config['temp_dir'], file.filename)

        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # التحقق من صحة البيانات
        task_info = validation_service.validate_data(
            data_file=temp_file_path,
            data_type=data_type
        )

        return task_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fix", response_model=ValidationTaskResponse)
async def fix_data(
    request: FixRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    إصلاح البيانات بناءً على نتائج التحقق
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:fix")

    try:
        # إصلاح البيانات
        task_info = validation_service.fix_data(
            validation_id=request.validation_id,
            validation_file=request.validation_file,
            auto_fix=request.auto_fix
        )

        return task_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate/database", response_model=ValidationTaskResponse)
async def validate_database(
    request: DatabaseValidationRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    التحقق من صحة قاعدة البيانات
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:validate_database")

    try:
        # التحقق من صحة قاعدة البيانات
        task_info = validation_service.validate_database(
            tables=request.tables,
            rules=request.rules
        )

        return task_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks", response_model=List[ValidationTaskResponse])
async def get_tasks(
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على قائمة المهام
    """
    # التحقق من الصلاحيات
    check_permission(current_user, PERMISSION_VIEW)

    try:
        # الحصول على قائمة المهام
        tasks = validation_service.get_all_tasks()

        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks/{task_id}", response_model=ValidationTaskResponse)
async def get_task(
    task_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على حالة مهمة
    """
    # التحقق من الصلاحيات
    check_permission(current_user, PERMISSION_VIEW)

    try:
        # الحصول على حالة المهمة
        task_info = validation_service.get_task_status(task_id)

        if task_info is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        return task_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/validations", response_model=List[Dict])
async def get_validations(
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على قائمة عمليات التحقق المتوفرة
    """
    # التحقق من الصلاحيات
    check_permission(current_user, PERMISSION_VIEW)

    try:
        # الحصول على قائمة عمليات التحقق
        validations = validation_service.get_validations()

        return validations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/validation-results/{validation_id}")
async def get_validation_results(
    validation_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على نتائج التحقق
    """
    # التحقق من الصلاحيات
    check_permission(current_user, PERMISSION_VIEW)

    try:
        # الحصول على نتائج التحقق
        validation_results = validation_service.get_validation_results(validation_id=validation_id)

        return validation_results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/config")
async def get_config(
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على إعدادات التحقق من صحة البيانات الحالية
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:view_config")

    try:
        # الحصول على الإعدادات
        config = validation_service.get_config()

        return config
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/config")
async def update_config(
    request: ConfigUpdateRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    تحديث إعدادات التحقق من صحة البيانات
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:update_config")

    try:
        # تحديث الإعدادات
        updated_config = validation_service.update_config(request.config)

        return updated_config
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/validation-rules")
async def get_validation_rules(
    data_type: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """
    الحصول على قواعد التحقق
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:view_rules")

    try:
        # الحصول على قواعد التحقق
        rules = validation_service.get_validation_rules(data_type)

        return rules
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validation-rules")
async def update_validation_rules(
    request: ValidationRulesUpdateRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    تحديث قواعد التحقق
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:update_rules")

    try:
        # تحديث قواعد التحقق
        updated_rules = validation_service.update_validation_rules(
            request.data_type,
            request.rules
        )

        return updated_rules
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/download/{file_path:path}")
async def download_file(
    file_path: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    تنزيل ملف
    """
    # التحقق من الصلاحيات
    check_permission(current_user, "data_validation:download")

    try:
        # التحقق من وجود الملف
        full_path = os.path.join(validation_service.config['validation_dir'], file_path)

        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail=f"File {file_path} not found")

        # تنزيل الملف
        return FileResponse(
            path=full_path,
            filename=os.path.basename(full_path),
            media_type="application/json"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
