"""
وحدات التحكم في الإدارة
يحتوي هذا الملف على وحدات التحكم لإدارة المستخدمين والشركات والإعدادات وحالة النظام
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status, BackgroundTasks
from fastapi.responses import JSONResponse

from ...core.auth.auth_manager import get_current_user, check_permissions
from ...core.database.db_manager import get_db_manager
from ..services.admin_services import (
    UserService, CountryService, CompanyService, SystemSettingService,
    SystemLogService, ServerMonitorService, BackupService
)


# إنشاء موجه API للإدارة
admin_router = APIRouter(prefix="/api/admin", tags=["الإدارة"])


# وحدات التحكم في المستخدمين
@admin_router.post("/users", response_model=Dict[str, Any])
async def create_user(
    user_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء مستخدم جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.users.create"])
    
    # إنشاء خدمة المستخدمين
    user_service = UserService(db_manager)
    
    # إنشاء المستخدم
    try:
        user = user_service.create_user(user_data)
        return {"status": "success", "data": user.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء المستخدم: {str(e)}"
        )


@admin_router.get("/users", response_model=Dict[str, Any])
async def get_all_users(
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع"),
    country_id: Optional[str] = Query(None, description="معرف الدولة"),
    role: Optional[str] = Query(None, description="دور المستخدم"),
    is_active: Optional[bool] = Query(None, description="ما إذا كان المستخدم نشطًا"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع المستخدمين"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.users.view"])
    
    # إنشاء خدمة المستخدمين
    user_service = UserService(db_manager)
    
    # الحصول على المستخدمين
    try:
        users = user_service.get_all_users(company_id, branch_id, country_id, role, is_active)
        return {
            "status": "success",
            "data": [user.to_dict() for user in users]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على المستخدمين: {str(e)}"
        )


@admin_router.get("/users/{user_id}", response_model=Dict[str, Any])
async def get_user(
    user_id: str = Path(..., description="معرف المستخدم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على مستخدم بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.users.view"])
    
    # إنشاء خدمة المستخدمين
    user_service = UserService(db_manager)
    
    # الحصول على المستخدم
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على المستخدم بالمعرف {user_id}"
        )
    
    return {"status": "success", "data": user.to_dict()}


@admin_router.put("/users/{user_id}", response_model=Dict[str, Any])
async def update_user(
    user_id: str = Path(..., description="معرف المستخدم"),
    user_data: Dict[str, Any] = Body(..., description="بيانات المستخدم المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث مستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.users.update"])
    
    # إنشاء خدمة المستخدمين
    user_service = UserService(db_manager)
    
    # تحديث المستخدم
    try:
        user = user_service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المستخدم بالمعرف {user_id}"
            )
        
        return {"status": "success", "data": user.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث المستخدم: {str(e)}"
        )


@admin_router.delete("/users/{user_id}", response_model=Dict[str, Any])
async def delete_user(
    user_id: str = Path(..., description="معرف المستخدم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف مستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.users.delete"])
    
    # التحقق من أن المستخدم لا يحاول حذف نفسه
    if user_id == current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="لا يمكن حذف المستخدم الحالي"
        )
    
    # إنشاء خدمة المستخدمين
    user_service = UserService(db_manager)
    
    # حذف المستخدم
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على المستخدم بالمعرف {user_id}"
        )
    
    return {"status": "success", "message": "تم حذف المستخدم بنجاح"}


@admin_router.post("/users/{user_id}/permissions", response_model=Dict[str, Any])
async def update_user_permissions(
    user_id: str = Path(..., description="معرف المستخدم"),
    permissions: Dict[str, str] = Body(..., description="صلاحيات المستخدم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث صلاحيات المستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.users.update"])
    
    # إنشاء خدمة المستخدمين
    user_service = UserService(db_manager)
    
    # تحديث صلاحيات المستخدم
    try:
        user = user_service.update_user_permissions(user_id, permissions)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المستخدم بالمعرف {user_id}"
            )
        
        return {"status": "success", "data": user.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث صلاحيات المستخدم: {str(e)}"
        )


@admin_router.post("/users/{user_id}/change-password", response_model=Dict[str, Any])
async def change_user_password(
    user_id: str = Path(..., description="معرف المستخدم"),
    password_data: Dict[str, str] = Body(..., description="بيانات كلمة المرور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تغيير كلمة مرور المستخدم"""
    # التحقق من الصلاحيات
    if user_id != current_user["user_id"]:
        check_permissions(current_user, ["admin.users.update"])
    
    # التحقق من وجود كلمة المرور الجديدة
    if "new_password" not in password_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="كلمة المرور الجديدة مطلوبة"
        )
    
    # إنشاء خدمة المستخدمين
    user_service = UserService(db_manager)
    
    # تغيير كلمة المرور
    try:
        user = user_service.change_user_password(user_id, password_data["new_password"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المستخدم بالمعرف {user_id}"
            )
        
        return {"status": "success", "message": "تم تغيير كلمة المرور بنجاح"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تغيير كلمة المرور: {str(e)}"
        )


@admin_router.get("/users/statistics", response_model=Dict[str, Any])
async def get_user_statistics(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على إحصائيات المستخدمين"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.users.view"])
    
    # إنشاء خدمة المستخدمين
    user_service = UserService(db_manager)
    
    # الحصول على الإحصائيات
    try:
        stats = user_service.get_user_statistics()
        return {"status": "success", "data": stats.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على إحصائيات المستخدمين: {str(e)}"
        )


# وحدات التحكم في الدول
@admin_router.post("/countries", response_model=Dict[str, Any])
async def create_country(
    country_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء دولة جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.countries.create"])
    
    # إنشاء خدمة الدول
    country_service = CountryService(db_manager)
    
    # إنشاء الدولة
    try:
        country = country_service.create_country(country_data)
        return {"status": "success", "data": country.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء الدولة: {str(e)}"
        )


@admin_router.get("/countries", response_model=Dict[str, Any])
async def get_all_countries(
    is_active: Optional[bool] = Query(None, description="ما إذا كانت الدولة نشطة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع الدول"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.countries.view"])
    
    # إنشاء خدمة الدول
    country_service = CountryService(db_manager)
    
    # الحصول على الدول
    try:
        countries = country_service.get_all_countries(is_active)
        return {
            "status": "success",
            "data": [country.to_dict() for country in countries]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على الدول: {str(e)}"
        )


@admin_router.get("/countries/{country_id}", response_model=Dict[str, Any])
async def get_country(
    country_id: str = Path(..., description="معرف الدولة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على دولة بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.countries.view"])
    
    # إنشاء خدمة الدول
    country_service = CountryService(db_manager)
    
    # الحصول على الدولة
    country = country_service.get_country(country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الدولة بالمعرف {country_id}"
        )
    
    return {"status": "success", "data": country.to_dict()}


@admin_router.put("/countries/{country_id}", response_model=Dict[str, Any])
async def update_country(
    country_id: str = Path(..., description="معرف الدولة"),
    country_data: Dict[str, Any] = Body(..., description="بيانات الدولة المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث دولة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.countries.update"])
    
    # إنشاء خدمة الدول
    country_service = CountryService(db_manager)
    
    # تحديث الدولة
    try:
        country = country_service.update_country(country_id, country_data)
        if not country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الدولة بالمعرف {country_id}"
            )
        
        return {"status": "success", "data": country.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث الدولة: {str(e)}"
        )


@admin_router.delete("/countries/{country_id}", response_model=Dict[str, Any])
async def delete_country(
    country_id: str = Path(..., description="معرف الدولة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف دولة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.countries.delete"])
    
    # إنشاء خدمة الدول
    country_service = CountryService(db_manager)
    
    # حذف الدولة
    success = country_service.delete_country(country_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الدولة بالمعرف {country_id}"
        )
    
    return {"status": "success", "message": "تم حذف الدولة بنجاح"}


# وحدات التحكم في الشركات
@admin_router.post("/companies", response_model=Dict[str, Any])
async def create_company(
    company_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء شركة جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.create"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # إنشاء الشركة
    try:
        company = company_service.create_company(company_data)
        return {"status": "success", "data": company.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء الشركة: {str(e)}"
        )


@admin_router.get("/companies", response_model=Dict[str, Any])
async def get_all_companies(
    country_id: Optional[str] = Query(None, description="معرف الدولة"),
    is_active: Optional[bool] = Query(None, description="ما إذا كانت الشركة نشطة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع الشركات"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.view"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # الحصول على الشركات
    try:
        companies = company_service.get_all_companies(country_id, is_active)
        return {
            "status": "success",
            "data": [company.to_dict() for company in companies]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على الشركات: {str(e)}"
        )


@admin_router.get("/companies/{company_id}", response_model=Dict[str, Any])
async def get_company(
    company_id: str = Path(..., description="معرف الشركة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على شركة بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.view"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # الحصول على الشركة
    company = company_service.get_company(company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الشركة بالمعرف {company_id}"
        )
    
    return {"status": "success", "data": company.to_dict()}


@admin_router.put("/companies/{company_id}", response_model=Dict[str, Any])
async def update_company(
    company_id: str = Path(..., description="معرف الشركة"),
    company_data: Dict[str, Any] = Body(..., description="بيانات الشركة المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث شركة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.update"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # تحديث الشركة
    try:
        company = company_service.update_company(company_id, company_data)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الشركة بالمعرف {company_id}"
            )
        
        return {"status": "success", "data": company.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث الشركة: {str(e)}"
        )


@admin_router.delete("/companies/{company_id}", response_model=Dict[str, Any])
async def delete_company(
    company_id: str = Path(..., description="معرف الشركة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف شركة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.delete"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # حذف الشركة
    success = company_service.delete_company(company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الشركة بالمعرف {company_id}"
        )
    
    return {"status": "success", "message": "تم حذف الشركة بنجاح"}


@admin_router.post("/companies/{company_id}/branches", response_model=Dict[str, Any])
async def create_branch(
    company_id: str = Path(..., description="معرف الشركة"),
    branch_data: Dict[str, Any] = Body(..., description="بيانات الفرع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء فرع جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.update"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # إضافة معرف الشركة إلى بيانات الفرع
    branch_data["company_id"] = company_id
    
    # إنشاء الفرع
    try:
        branch = company_service.create_branch(branch_data)
        return {"status": "success", "data": branch.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء الفرع: {str(e)}"
        )


@admin_router.get("/branches", response_model=Dict[str, Any])
async def get_all_branches(
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    is_active: Optional[bool] = Query(None, description="ما إذا كان الفرع نشطًا"),
    is_main_branch: Optional[bool] = Query(None, description="ما إذا كان الفرع الرئيسي"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع الفروع"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.view"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # الحصول على الفروع
    try:
        branches = company_service.get_all_branches(company_id, is_active, is_main_branch)
        return {
            "status": "success",
            "data": [branch.to_dict() for branch in branches]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على الفروع: {str(e)}"
        )


@admin_router.get("/branches/{branch_id}", response_model=Dict[str, Any])
async def get_branch(
    branch_id: str = Path(..., description="معرف الفرع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على فرع بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.view"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # الحصول على الفرع
    branch = company_service.get_branch(branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الفرع بالمعرف {branch_id}"
        )
    
    return {"status": "success", "data": branch.to_dict()}


@admin_router.put("/branches/{branch_id}", response_model=Dict[str, Any])
async def update_branch(
    branch_id: str = Path(..., description="معرف الفرع"),
    branch_data: Dict[str, Any] = Body(..., description="بيانات الفرع المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث فرع"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.update"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # تحديث الفرع
    try:
        branch = company_service.update_branch(branch_id, branch_data)
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الفرع بالمعرف {branch_id}"
            )
        
        return {"status": "success", "data": branch.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث الفرع: {str(e)}"
        )


@admin_router.delete("/branches/{branch_id}", response_model=Dict[str, Any])
async def delete_branch(
    branch_id: str = Path(..., description="معرف الفرع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف فرع"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.companies.delete"])
    
    # إنشاء خدمة الشركات
    company_service = CompanyService(db_manager)
    
    # حذف الفرع
    success = company_service.delete_branch(branch_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الفرع بالمعرف {branch_id}"
        )
    
    return {"status": "success", "message": "تم حذف الفرع بنجاح"}


# وحدات التحكم في إعدادات النظام
@admin_router.post("/settings", response_model=Dict[str, Any])
async def create_setting(
    setting_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء إعداد جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.settings.create"])
    
    # إنشاء خدمة إعدادات النظام
    setting_service = SystemSettingService(db_manager)
    
    # إضافة معرف المستخدم الذي أنشأ الإعداد
    setting_data["created_by"] = current_user["user_id"]
    
    # إنشاء الإعداد
    try:
        setting = setting_service.create_setting(setting_data)
        return {"status": "success", "data": setting.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء الإعداد: {str(e)}"
        )


@admin_router.get("/settings", response_model=Dict[str, Any])
async def get_all_settings(
    category: Optional[str] = Query(None, description="فئة الإعداد"),
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع"),
    is_global: Optional[bool] = Query(None, description="ما إذا كان الإعداد عامًا"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع الإعدادات"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.settings.view"])
    
    # إنشاء خدمة إعدادات النظام
    setting_service = SystemSettingService(db_manager)
    
    # الحصول على الإعدادات
    try:
        settings = setting_service.get_all_settings(category, company_id, branch_id, is_global)
        return {
            "status": "success",
            "data": [setting.to_dict() for setting in settings]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على الإعدادات: {str(e)}"
        )


@admin_router.get("/settings/{setting_id}", response_model=Dict[str, Any])
async def get_setting(
    setting_id: str = Path(..., description="معرف الإعداد"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على إعداد بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.settings.view"])
    
    # إنشاء خدمة إعدادات النظام
    setting_service = SystemSettingService(db_manager)
    
    # الحصول على الإعداد
    setting = setting_service.get_setting(setting_id)
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الإعداد بالمعرف {setting_id}"
        )
    
    return {"status": "success", "data": setting.to_dict()}


@admin_router.put("/settings/{setting_id}", response_model=Dict[str, Any])
async def update_setting(
    setting_id: str = Path(..., description="معرف الإعداد"),
    setting_data: Dict[str, Any] = Body(..., description="بيانات الإعداد المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث إعداد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.settings.update"])
    
    # إنشاء خدمة إعدادات النظام
    setting_service = SystemSettingService(db_manager)
    
    # إضافة معرف المستخدم الذي حدث الإعداد
    setting_data["updated_by"] = current_user["user_id"]
    
    # تحديث الإعداد
    try:
        setting = setting_service.update_setting(setting_id, setting_data)
        if not setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الإعداد بالمعرف {setting_id}"
            )
        
        return {"status": "success", "data": setting.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث الإعداد: {str(e)}"
        )


@admin_router.delete("/settings/{setting_id}", response_model=Dict[str, Any])
async def delete_setting(
    setting_id: str = Path(..., description="معرف الإعداد"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف إعداد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.settings.delete"])
    
    # إنشاء خدمة إعدادات النظام
    setting_service = SystemSettingService(db_manager)
    
    # حذف الإعداد
    success = setting_service.delete_setting(setting_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الإعداد بالمعرف {setting_id}"
        )
    
    return {"status": "success", "message": "تم حذف الإعداد بنجاح"}


@admin_router.get("/settings/key/{key}", response_model=Dict[str, Any])
async def get_setting_by_key(
    key: str = Path(..., description="مفتاح الإعداد"),
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على إعداد بواسطة المفتاح"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.settings.view"])
    
    # إنشاء خدمة إعدادات النظام
    setting_service = SystemSettingService(db_manager)
    
    # الحصول على الإعداد
    setting = setting_service.get_setting_by_key(key, company_id, branch_id)
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الإعداد بالمفتاح {key}"
        )
    
    return {"status": "success", "data": setting.to_dict()}


@admin_router.post("/settings/value", response_model=Dict[str, Any])
async def set_setting_value(
    setting_data: Dict[str, Any] = Body(..., description="بيانات الإعداد"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تعيين قيمة إعداد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.settings.update"])
    
    # التحقق من وجود المفتاح والقيمة
    if "key" not in setting_data or "value" not in setting_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="المفتاح والقيمة مطلوبان"
        )
    
    # إنشاء خدمة إعدادات النظام
    setting_service = SystemSettingService(db_manager)
    
    # تعيين قيمة الإعداد
    try:
        setting = setting_service.set_setting_value(
            key=setting_data["key"],
            value=setting_data["value"],
            company_id=setting_data.get("company_id"),
            branch_id=setting_data.get("branch_id"),
            description=setting_data.get("description"),
            category=setting_data.get("category"),
            data_type=setting_data.get("data_type"),
            is_sensitive=setting_data.get("is_sensitive", False),
            created_by=current_user["user_id"]
        )
        
        return {"status": "success", "data": setting.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تعيين قيمة الإعداد: {str(e)}"
        )


# وحدات التحكم في سجلات النظام
@admin_router.get("/logs", response_model=Dict[str, Any])
async def get_logs(
    user_id: Optional[str] = Query(None, description="معرف المستخدم"),
    action: Optional[str] = Query(None, description="الإجراء المتخذ"),
    module: Optional[str] = Query(None, description="الوحدة المتأثرة"),
    entity_type: Optional[str] = Query(None, description="نوع الكيان المتأثر"),
    entity_id: Optional[str] = Query(None, description="معرف الكيان المتأثر"),
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع"),
    status: Optional[str] = Query(None, description="حالة الإجراء"),
    start_date: Optional[datetime] = Query(None, description="تاريخ البداية"),
    end_date: Optional[datetime] = Query(None, description="تاريخ النهاية"),
    limit: int = Query(100, description="عدد السجلات المراد إرجاعها"),
    offset: int = Query(0, description="عدد السجلات المراد تخطيها"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على سجلات النظام"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.logs.view"])
    
    # إنشاء خدمة سجلات النظام
    log_service = SystemLogService(db_manager)
    
    # الحصول على السجلات
    try:
        logs, total = log_service.get_logs(
            user_id, action, module, entity_type, entity_id,
            company_id, branch_id, status, start_date, end_date,
            limit, offset
        )
        
        return {
            "status": "success",
            "data": {
                "logs": [log.to_dict() for log in logs],
                "total": total,
                "limit": limit,
                "offset": offset
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على سجلات النظام: {str(e)}"
        )


@admin_router.get("/logs/{log_id}", response_model=Dict[str, Any])
async def get_log(
    log_id: str = Path(..., description="معرف السجل"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على سجل بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.logs.view"])
    
    # إنشاء خدمة سجلات النظام
    log_service = SystemLogService(db_manager)
    
    # الحصول على السجل
    log = log_service.get_log(log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على السجل بالمعرف {log_id}"
        )
    
    return {"status": "success", "data": log.to_dict()}


@admin_router.delete("/logs/cleanup", response_model=Dict[str, Any])
async def cleanup_logs(
    days: int = Query(..., description="عدد الأيام للاحتفاظ بالسجلات"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف السجلات القديمة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.logs.delete"])
    
    # التحقق من عدد الأيام
    if days < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="يجب أن يكون عدد الأيام أكبر من صفر"
        )
    
    # إنشاء خدمة سجلات النظام
    log_service = SystemLogService(db_manager)
    
    # حذف السجلات القديمة
    try:
        count = log_service.delete_logs_older_than(days)
        return {"status": "success", "message": f"تم حذف {count} سجل"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف السجلات القديمة: {str(e)}"
        )


# وحدات التحكم في حالة الخادم
@admin_router.get("/server/status", response_model=Dict[str, Any])
async def get_server_status(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على حالة الخادم الحالية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.server.view"])
    
    # إنشاء خدمة مراقبة الخادم
    server_service = ServerMonitorService(db_manager)
    
    # الحصول على حالة الخادم
    try:
        status = server_service.get_server_status()
        return {"status": "success", "data": status.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على حالة الخادم: {str(e)}"
        )


@admin_router.get("/server/status/history", response_model=Dict[str, Any])
async def get_server_status_history(
    start_date: Optional[datetime] = Query(None, description="تاريخ البداية"),
    end_date: Optional[datetime] = Query(None, description="تاريخ النهاية"),
    limit: int = Query(100, description="عدد السجلات المراد إرجاعها"),
    offset: int = Query(0, description="عدد السجلات المراد تخطيها"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على سجل حالة الخادم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.server.view"])
    
    # إنشاء خدمة مراقبة الخادم
    server_service = ServerMonitorService(db_manager)
    
    # الحصول على سجل حالة الخادم
    try:
        history, total = server_service.get_server_status_history(start_date, end_date, limit, offset)
        
        return {
            "status": "success",
            "data": {
                "history": [status.to_dict() for status in history],
                "total": total,
                "limit": limit,
                "offset": offset
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على سجل حالة الخادم: {str(e)}"
        )


@admin_router.delete("/server/status/cleanup", response_model=Dict[str, Any])
async def cleanup_server_status(
    days: int = Query(..., description="عدد الأيام للاحتفاظ بسجلات حالة الخادم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف سجلات حالة الخادم القديمة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.server.delete"])
    
    # التحقق من عدد الأيام
    if days < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="يجب أن يكون عدد الأيام أكبر من صفر"
        )
    
    # إنشاء خدمة مراقبة الخادم
    server_service = ServerMonitorService(db_manager)
    
    # حذف سجلات حالة الخادم القديمة
    try:
        count = server_service.delete_server_status_older_than(days)
        return {"status": "success", "message": f"تم حذف {count} سجل"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف سجلات حالة الخادم القديمة: {str(e)}"
        )


# وحدات التحكم في النسخ الاحتياطي
@admin_router.post("/backups", response_model=Dict[str, Any])
async def create_backup(
    backup_data: Dict[str, Any] = Body(..., description="بيانات النسخة الاحتياطية"),
    background_tasks: BackgroundTasks = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء نسخة احتياطية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.backups.create"])
    
    # إنشاء خدمة النسخ الاحتياطي
    backup_service = BackupService(db_manager)
    
    # إضافة معرف المستخدم الذي أنشأ النسخة الاحتياطية
    backup_data["created_by"] = current_user["user_id"]
    
    # إنشاء النسخة الاحتياطية في الخلفية
    if background_tasks:
        # إنشاء النسخة الاحتياطية في الخلفية
        background_tasks.add_task(backup_service.create_backup, **backup_data)
        return {"status": "success", "message": "تم بدء عملية النسخ الاحتياطي في الخلفية"}
    else:
        # إنشاء النسخة الاحتياطية مباشرة
        try:
            backup = backup_service.create_backup(**backup_data)
            return {"status": "success", "data": backup.to_dict()}
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"فشل في إنشاء النسخة الاحتياطية: {str(e)}"
            )


@admin_router.get("/backups", response_model=Dict[str, Any])
async def get_all_backups(
    backup_type: Optional[str] = Query(None, description="نوع النسخة الاحتياطية"),
    status: Optional[str] = Query(None, description="حالة النسخة الاحتياطية"),
    created_by: Optional[str] = Query(None, description="معرف المستخدم الذي أنشأ النسخة الاحتياطية"),
    is_automatic: Optional[bool] = Query(None, description="ما إذا كانت النسخة الاحتياطية تلقائية"),
    start_date: Optional[datetime] = Query(None, description="تاريخ البداية"),
    end_date: Optional[datetime] = Query(None, description="تاريخ النهاية"),
    limit: int = Query(100, description="عدد النسخ الاحتياطية المراد إرجاعها"),
    offset: int = Query(0, description="عدد النسخ الاحتياطية المراد تخطيها"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع النسخ الاحتياطية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.backups.view"])
    
    # إنشاء خدمة النسخ الاحتياطي
    backup_service = BackupService(db_manager)
    
    # الحصول على النسخ الاحتياطية
    try:
        backups, total = backup_service.get_all_backups(
            backup_type, status, created_by, is_automatic,
            start_date, end_date, limit, offset
        )
        
        return {
            "status": "success",
            "data": {
                "backups": [backup.to_dict() for backup in backups],
                "total": total,
                "limit": limit,
                "offset": offset
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على النسخ الاحتياطية: {str(e)}"
        )


@admin_router.get("/backups/{backup_id}", response_model=Dict[str, Any])
async def get_backup(
    backup_id: str = Path(..., description="معرف النسخة الاحتياطية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على نسخة احتياطية بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.backups.view"])
    
    # إنشاء خدمة النسخ الاحتياطي
    backup_service = BackupService(db_manager)
    
    # الحصول على النسخة الاحتياطية
    backup = backup_service.get_backup_info(backup_id)
    if not backup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على النسخة الاحتياطية بالمعرف {backup_id}"
        )
    
    return {"status": "success", "data": backup.to_dict()}


@admin_router.post("/backups/{backup_id}/restore", response_model=Dict[str, Any])
async def restore_backup(
    backup_id: str = Path(..., description="معرف النسخة الاحتياطية"),
    restore_data: Dict[str, Any] = Body(..., description="بيانات الاستعادة"),
    background_tasks: BackgroundTasks = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """استعادة نسخة احتياطية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.backups.restore"])
    
    # إنشاء خدمة النسخ الاحتياطي
    backup_service = BackupService(db_manager)
    
    # استخراج بيانات الاستعادة
    restore_files = restore_data.get("restore_files", True)
    restore_database = restore_data.get("restore_database", True)
    encryption_key = restore_data.get("encryption_key")
    
    # استعادة النسخة الاحتياطية في الخلفية
    if background_tasks:
        # استعادة النسخة الاحتياطية في الخلفية
        background_tasks.add_task(
            backup_service.restore_backup,
            backup_id,
            restore_files,
            restore_database,
            encryption_key
        )
        return {"status": "success", "message": "تم بدء عملية استعادة النسخة الاحتياطية في الخلفية"}
    else:
        # استعادة النسخة الاحتياطية مباشرة
        try:
            success = backup_service.restore_backup(
                backup_id,
                restore_files,
                restore_database,
                encryption_key
            )
            
            if success:
                return {"status": "success", "message": "تم استعادة النسخة الاحتياطية بنجاح"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="فشل في استعادة النسخة الاحتياطية"
                )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"فشل في استعادة النسخة الاحتياطية: {str(e)}"
            )


@admin_router.delete("/backups/{backup_id}", response_model=Dict[str, Any])
async def delete_backup(
    backup_id: str = Path(..., description="معرف النسخة الاحتياطية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف نسخة احتياطية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.backups.delete"])
    
    # إنشاء خدمة النسخ الاحتياطي
    backup_service = BackupService(db_manager)
    
    # حذف النسخة الاحتياطية
    try:
        success = backup_service.delete_backup(backup_id)
        if success:
            return {"status": "success", "message": "تم حذف النسخة الاحتياطية بنجاح"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="فشل في حذف النسخة الاحتياطية"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف النسخة الاحتياطية: {str(e)}"
        )


@admin_router.delete("/backups/cleanup", response_model=Dict[str, Any])
async def cleanup_backups(
    days: int = Query(..., description="عدد الأيام للاحتفاظ بالنسخ الاحتياطية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف النسخ الاحتياطية القديمة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["admin.backups.delete"])
    
    # التحقق من عدد الأيام
    if days < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="يجب أن يكون عدد الأيام أكبر من صفر"
        )
    
    # إنشاء خدمة النسخ الاحتياطي
    backup_service = BackupService(db_manager)
    
    # حذف النسخ الاحتياطية القديمة
    try:
        count = backup_service.delete_backups_older_than(days)
        return {"status": "success", "message": f"تم حذف {count} نسخة احتياطية"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف النسخ الاحتياطية القديمة: {str(e)}"
        )
