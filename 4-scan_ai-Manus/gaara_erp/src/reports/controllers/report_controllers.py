"""
وحدات التحكم في التقارير
يحتوي هذا الملف على وحدات التحكم للتقارير
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse

from ...core.auth.auth_manager import get_current_user, check_permissions
from ...core.database.db_manager import get_db_manager
from ..services.report_services import ReportService
from ..models.report_models import ReportType, ReportFormat, ReportFrequency, ReportStatus


# إنشاء موجه API للتقارير
reports_router = APIRouter(prefix="/api/reports", tags=["التقارير"])


# وحدات التحكم في قوالب التقارير
@reports_router.post("/templates", response_model=Dict[str, Any])
async def create_report_template(
    template_data: Dict[str, Any] = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء قالب تقرير جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.templates.create"])
    
    # إضافة معرف المستخدم
    template_data["created_by"] = current_user["user_id"]
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    try:
        # إنشاء قالب تقرير
        template = report_service.create_report_template(template_data)
        
        return {"status": "success", "data": template.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء قالب التقرير: {str(e)}"
        )


@reports_router.get("/templates/{template_id}", response_model=Dict[str, Any])
async def get_report_template(
    template_id: str = Path(..., description="معرف قالب التقرير"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على قالب تقرير بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.templates.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # الحصول على قالب التقرير
    template = report_service.get_report_template(template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على قالب التقرير بالمعرف {template_id}"
        )
    
    return {"status": "success", "data": template.to_dict()}


@reports_router.get("/templates", response_model=Dict[str, Any])
async def get_all_report_templates(
    report_type: Optional[str] = Query(None, description="نوع التقرير"),
    is_system: Optional[bool] = Query(None, description="هل هو قالب نظامي"),
    is_active: Optional[bool] = Query(None, description="هل هو قالب نشط"),
    limit: int = Query(100, description="عدد النتائج"),
    offset: int = Query(0, description="بداية النتائج"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع قوالب التقارير"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.templates.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # تحويل نوع التقرير إلى نوع ReportType إذا تم توفيره
    report_type_enum = None
    if report_type:
        try:
            report_type_enum = ReportType(report_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"نوع التقرير غير صالح: {report_type}"
            )
    
    # الحصول على قوالب التقارير
    templates, total = report_service.get_all_report_templates(
        report_type=report_type_enum,
        is_system=is_system,
        is_active=is_active,
        limit=limit,
        offset=offset
    )
    
    return {
        "status": "success",
        "data": {
            "templates": [template.to_dict() for template in templates],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }


@reports_router.put("/templates/{template_id}", response_model=Dict[str, Any])
async def update_report_template(
    template_id: str = Path(..., description="معرف قالب التقرير"),
    template_data: Dict[str, Any] = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث قالب تقرير"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.templates.update"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    try:
        # تحديث قالب التقرير
        template = report_service.update_report_template(template_id, template_data)
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على قالب التقرير بالمعرف {template_id}"
            )
        
        return {"status": "success", "data": template.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث قالب التقرير: {str(e)}"
        )


@reports_router.delete("/templates/{template_id}", response_model=Dict[str, Any])
async def delete_report_template(
    template_id: str = Path(..., description="معرف قالب التقرير"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف قالب تقرير"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.templates.delete"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    try:
        # حذف قالب التقرير
        success = report_service.delete_report_template(template_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على قالب التقرير بالمعرف {template_id}"
            )
        
        return {"status": "success", "message": "تم حذف قالب التقرير بنجاح"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف قالب التقرير: {str(e)}"
        )


# وحدات التحكم في التقارير
@reports_router.post("/generate", response_model=Dict[str, Any])
async def create_report(
    report_data: Dict[str, Any] = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء تقرير جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.generate"])
    
    # إضافة معرف المستخدم
    report_data["created_by"] = current_user["user_id"]
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    try:
        # إنشاء تقرير
        report = report_service.create_report(report_data)
        
        # توليد التقرير
        success = report_service.generate_report(report.report_id)
        
        if not success:
            return {
                "status": "warning",
                "message": "تم إنشاء التقرير ولكن فشل في توليده",
                "data": report.to_dict()
            }
        
        return {"status": "success", "data": report.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء التقرير: {str(e)}"
        )


@reports_router.get("/{report_id}", response_model=Dict[str, Any])
async def get_report(
    report_id: str = Path(..., description="معرف التقرير"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على تقرير بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # الحصول على التقرير
    report = report_service.get_report(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على التقرير بالمعرف {report_id}"
        )
    
    return {"status": "success", "data": report.to_dict()}


@reports_router.get("", response_model=Dict[str, Any])
async def get_all_reports(
    template_id: Optional[str] = Query(None, description="معرف قالب التقرير"),
    status: Optional[str] = Query(None, description="حالة التقرير"),
    limit: int = Query(100, description="عدد النتائج"),
    offset: int = Query(0, description="بداية النتائج"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع التقارير"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # تحويل حالة التقرير إلى نوع ReportStatus إذا تم توفيرها
    report_status = None
    if status:
        try:
            report_status = ReportStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"حالة التقرير غير صالحة: {status}"
            )
    
    # الحصول على التقارير
    reports, total = report_service.get_all_reports(
        template_id=template_id,
        created_by=current_user["user_id"],
        status=report_status,
        limit=limit,
        offset=offset
    )
    
    return {
        "status": "success",
        "data": {
            "reports": [report.to_dict() for report in reports],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }


@reports_router.get("/{report_id}/download", response_class=FileResponse)
async def download_report(
    report_id: str = Path(..., description="معرف التقرير"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تنزيل ملف التقرير"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # الحصول على التقرير
    report = report_service.get_report(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على التقرير بالمعرف {report_id}"
        )
    
    # التحقق من أن التقرير مكتمل
    if report.status != ReportStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"لا يمكن تنزيل التقرير لأنه في حالة {report.status.value}"
        )
    
    # التحقق من وجود مسار الملف
    if not report.file_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="لا يوجد ملف للتقرير"
        )
    
    # تحديد نوع المحتوى
    media_type = None
    if report.report_format == ReportFormat.PDF:
        media_type = "application/pdf"
    elif report.report_format == ReportFormat.EXCEL:
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif report.report_format == ReportFormat.CSV:
        media_type = "text/csv"
    elif report.report_format == ReportFormat.HTML:
        media_type = "text/html"
    elif report.report_format == ReportFormat.JSON:
        media_type = "application/json"
    
    # تنزيل الملف
    return FileResponse(
        path=report.file_path,
        media_type=media_type,
        filename=report.file_path.split("/")[-1]
    )


# وحدات التحكم في التقارير المجدولة
@reports_router.post("/scheduled", response_model=Dict[str, Any])
async def create_scheduled_report(
    schedule_data: Dict[str, Any] = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء تقرير مجدول جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.schedule"])
    
    # إضافة معرف المستخدم
    schedule_data["created_by"] = current_user["user_id"]
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    try:
        # إنشاء تقرير مجدول
        scheduled_report = report_service.create_scheduled_report(schedule_data)
        
        return {"status": "success", "data": scheduled_report.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء التقرير المجدول: {str(e)}"
        )


@reports_router.get("/scheduled/{schedule_id}", response_model=Dict[str, Any])
async def get_scheduled_report(
    schedule_id: str = Path(..., description="معرف التقرير المجدول"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على تقرير مجدول بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.schedule.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # الحصول على التقرير المجدول
    scheduled_report = report_service.get_scheduled_report(schedule_id)
    
    if not scheduled_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على التقرير المجدول بالمعرف {schedule_id}"
        )
    
    # التحقق من أن التقرير المجدول ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if scheduled_report.created_by != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["reports.schedule.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى هذا التقرير المجدول"
        )
    
    return {"status": "success", "data": scheduled_report.to_dict()}


@reports_router.get("/scheduled", response_model=Dict[str, Any])
async def get_all_scheduled_reports(
    template_id: Optional[str] = Query(None, description="معرف قالب التقرير"),
    is_active: Optional[bool] = Query(None, description="هل هو تقرير مجدول نشط"),
    limit: int = Query(100, description="عدد النتائج"),
    offset: int = Query(0, description="بداية النتائج"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع التقارير المجدولة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.schedule.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # الحصول على التقارير المجدولة
    scheduled_reports, total = report_service.get_all_scheduled_reports(
        template_id=template_id,
        created_by=current_user["user_id"],
        is_active=is_active,
        limit=limit,
        offset=offset
    )
    
    return {
        "status": "success",
        "data": {
            "scheduled_reports": [report.to_dict() for report in scheduled_reports],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }


@reports_router.put("/scheduled/{schedule_id}", response_model=Dict[str, Any])
async def update_scheduled_report(
    schedule_id: str = Path(..., description="معرف التقرير المجدول"),
    schedule_data: Dict[str, Any] = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث تقرير مجدول"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.schedule.update"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # التحقق من وجود التقرير المجدول
    scheduled_report = report_service.get_scheduled_report(schedule_id)
    if not scheduled_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على التقرير المجدول بالمعرف {schedule_id}"
        )
    
    # التحقق من أن التقرير المجدول ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if scheduled_report.created_by != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["reports.schedule.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لتحديث هذا التقرير المجدول"
        )
    
    try:
        # تحديث التقرير المجدول
        updated_report = report_service.update_scheduled_report(schedule_id, schedule_data)
        
        return {"status": "success", "data": updated_report.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث التقرير المجدول: {str(e)}"
        )


@reports_router.delete("/scheduled/{schedule_id}", response_model=Dict[str, Any])
async def delete_scheduled_report(
    schedule_id: str = Path(..., description="معرف التقرير المجدول"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف تقرير مجدول"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.schedule.delete"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # التحقق من وجود التقرير المجدول
    scheduled_report = report_service.get_scheduled_report(schedule_id)
    if not scheduled_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على التقرير المجدول بالمعرف {schedule_id}"
        )
    
    # التحقق من أن التقرير المجدول ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if scheduled_report.created_by != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["reports.schedule.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لحذف هذا التقرير المجدول"
        )
    
    try:
        # حذف التقرير المجدول
        success = report_service.delete_scheduled_report(schedule_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على التقرير المجدول بالمعرف {schedule_id}"
            )
        
        return {"status": "success", "message": "تم حذف التقرير المجدول بنجاح"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف التقرير المجدول: {str(e)}"
        )


@reports_router.post("/scheduled/{schedule_id}/run", response_model=Dict[str, Any])
async def run_scheduled_report(
    schedule_id: str = Path(..., description="معرف التقرير المجدول"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تشغيل تقرير مجدول"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.schedule.run"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # التحقق من وجود التقرير المجدول
    scheduled_report = report_service.get_scheduled_report(schedule_id)
    if not scheduled_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على التقرير المجدول بالمعرف {schedule_id}"
        )
    
    # التحقق من أن التقرير المجدول ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if scheduled_report.created_by != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["reports.schedule.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لتشغيل هذا التقرير المجدول"
        )
    
    # تشغيل التقرير المجدول
    report_id = report_service.run_scheduled_report(schedule_id)
    
    if not report_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فشل في تشغيل التقرير المجدول"
        )
    
    return {
        "status": "success",
        "message": "تم تشغيل التقرير المجدول بنجاح",
        "data": {"report_id": report_id}
    }


# وحدات التحكم في لوحات تحكم التقارير
@reports_router.post("/dashboards", response_model=Dict[str, Any])
async def create_report_dashboard(
    dashboard_data: Dict[str, Any] = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء لوحة تحكم تقارير جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.dashboards.create"])
    
    # إضافة معرف المستخدم
    dashboard_data["created_by"] = current_user["user_id"]
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    try:
        # إنشاء لوحة تحكم تقارير
        dashboard = report_service.create_report_dashboard(dashboard_data)
        
        return {"status": "success", "data": dashboard.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء لوحة تحكم التقارير: {str(e)}"
        )


@reports_router.get("/dashboards/{dashboard_id}", response_model=Dict[str, Any])
async def get_report_dashboard(
    dashboard_id: str = Path(..., description="معرف لوحة تحكم التقارير"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على لوحة تحكم تقارير بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.dashboards.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # الحصول على لوحة تحكم التقارير
    dashboard = report_service.get_report_dashboard(dashboard_id)
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على لوحة تحكم التقارير بالمعرف {dashboard_id}"
        )
    
    # التحقق من أن لوحة تحكم التقارير عامة أو تنتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if not dashboard.is_public and dashboard.created_by != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["reports.dashboards.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى لوحة تحكم التقارير هذه"
        )
    
    return {"status": "success", "data": dashboard.to_dict()}


@reports_router.get("/dashboards", response_model=Dict[str, Any])
async def get_all_report_dashboards(
    is_public: Optional[bool] = Query(None, description="هل هي لوحة تحكم عامة"),
    is_active: Optional[bool] = Query(None, description="هل هي لوحة تحكم نشطة"),
    limit: int = Query(100, description="عدد النتائج"),
    offset: int = Query(0, description="بداية النتائج"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع لوحات تحكم التقارير"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.dashboards.view"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # الحصول على لوحات تحكم التقارير
    dashboards, total = report_service.get_all_report_dashboards(
        created_by=current_user["user_id"],
        is_public=is_public,
        is_active=is_active,
        limit=limit,
        offset=offset
    )
    
    return {
        "status": "success",
        "data": {
            "dashboards": [dashboard.to_dict() for dashboard in dashboards],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }


@reports_router.put("/dashboards/{dashboard_id}", response_model=Dict[str, Any])
async def update_report_dashboard(
    dashboard_id: str = Path(..., description="معرف لوحة تحكم التقارير"),
    dashboard_data: Dict[str, Any] = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث لوحة تحكم تقارير"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.dashboards.update"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # التحقق من وجود لوحة تحكم التقارير
    dashboard = report_service.get_report_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على لوحة تحكم التقارير بالمعرف {dashboard_id}"
        )
    
    # التحقق من أن لوحة تحكم التقارير تنتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if dashboard.created_by != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["reports.dashboards.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لتحديث لوحة تحكم التقارير هذه"
        )
    
    try:
        # تحديث لوحة تحكم التقارير
        updated_dashboard = report_service.update_report_dashboard(dashboard_id, dashboard_data)
        
        return {"status": "success", "data": updated_dashboard.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث لوحة تحكم التقارير: {str(e)}"
        )


@reports_router.delete("/dashboards/{dashboard_id}", response_model=Dict[str, Any])
async def delete_report_dashboard(
    dashboard_id: str = Path(..., description="معرف لوحة تحكم التقارير"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف لوحة تحكم تقارير"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["reports.dashboards.delete"])
    
    # إنشاء خدمة التقارير
    report_service = ReportService(db_manager)
    
    # التحقق من وجود لوحة تحكم التقارير
    dashboard = report_service.get_report_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على لوحة تحكم التقارير بالمعرف {dashboard_id}"
        )
    
    # التحقق من أن لوحة تحكم التقارير تنتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if dashboard.created_by != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["reports.dashboards.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لحذف لوحة تحكم التقارير هذه"
        )
    
    try:
        # حذف لوحة تحكم التقارير
        success = report_service.delete_report_dashboard(dashboard_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على لوحة تحكم التقارير بالمعرف {dashboard_id}"
            )
        
        return {"status": "success", "message": "تم حذف لوحة تحكم التقارير بنجاح"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف لوحة تحكم التقارير: {str(e)}"
        )
