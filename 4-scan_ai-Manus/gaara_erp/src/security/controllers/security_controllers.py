"""
وحدات التحكم في الأمان
يحتوي هذا الملف على وحدات التحكم لإدارة الأمان والصلاحيات
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status, Request
from fastapi.responses import JSONResponse

from ...core.auth.auth_manager import get_current_user, check_permissions, get_optional_current_user
from ...core.database.db_manager import get_db_manager
from ..services.security_services import (
    PermissionService, RoleService, UserPermissionService,
    AuthService, ApiKeyService, SecurityPolicyService, SecurityAuditService
)


# إنشاء موجه API للأمان
security_router = APIRouter(prefix="/api/security", tags=["الأمان"])


# وحدات التحكم في الصلاحيات
@security_router.post("/permissions", response_model=Dict[str, Any])
async def create_permission(
    permission_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء صلاحية جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.permissions.create"])
    
    # إنشاء خدمة الصلاحيات
    permission_service = PermissionService(db_manager)
    
    # إنشاء الصلاحية
    try:
        permission = permission_service.create_permission(permission_data)
        return {"status": "success", "data": permission.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء الصلاحية: {str(e)}"
        )


@security_router.get("/permissions", response_model=Dict[str, Any])
async def get_all_permissions(
    module: Optional[str] = Query(None, description="الوحدة"),
    scope: Optional[str] = Query(None, description="النطاق"),
    is_active: Optional[bool] = Query(None, description="ما إذا كانت الصلاحية نشطة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع الصلاحيات"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.permissions.view"])
    
    # إنشاء خدمة الصلاحيات
    permission_service = PermissionService(db_manager)
    
    # الحصول على الصلاحيات
    try:
        permissions = permission_service.get_all_permissions(module, scope, is_active)
        return {
            "status": "success",
            "data": [permission.to_dict() for permission in permissions]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على الصلاحيات: {str(e)}"
        )


@security_router.get("/permissions/{permission_id}", response_model=Dict[str, Any])
async def get_permission(
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على صلاحية بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.permissions.view"])
    
    # إنشاء خدمة الصلاحيات
    permission_service = PermissionService(db_manager)
    
    # الحصول على الصلاحية
    permission = permission_service.get_permission(permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الصلاحية بالمعرف {permission_id}"
        )
    
    return {"status": "success", "data": permission.to_dict()}


@security_router.put("/permissions/{permission_id}", response_model=Dict[str, Any])
async def update_permission(
    permission_id: str = Path(..., description="معرف الصلاحية"),
    permission_data: Dict[str, Any] = Body(..., description="بيانات الصلاحية المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث صلاحية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.permissions.update"])
    
    # إنشاء خدمة الصلاحيات
    permission_service = PermissionService(db_manager)
    
    # تحديث الصلاحية
    try:
        permission = permission_service.update_permission(permission_id, permission_data)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الصلاحية بالمعرف {permission_id}"
            )
        
        return {"status": "success", "data": permission.to_dict()}
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
            detail=f"فشل في تحديث الصلاحية: {str(e)}"
        )


@security_router.delete("/permissions/{permission_id}", response_model=Dict[str, Any])
async def delete_permission(
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف صلاحية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.permissions.delete"])
    
    # إنشاء خدمة الصلاحيات
    permission_service = PermissionService(db_manager)
    
    # حذف الصلاحية
    try:
        success = permission_service.delete_permission(permission_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الصلاحية بالمعرف {permission_id}"
            )
        
        return {"status": "success", "message": "تم حذف الصلاحية بنجاح"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف الصلاحية: {str(e)}"
        )


# وحدات التحكم في الأدوار
@security_router.post("/roles", response_model=Dict[str, Any])
async def create_role(
    role_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء دور جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.roles.create"])
    
    # إضافة معرف المستخدم الذي أنشأ الدور
    role_data["created_by"] = current_user["user_id"]
    
    # إنشاء خدمة الأدوار
    role_service = RoleService(db_manager)
    
    # إنشاء الدور
    try:
        role = role_service.create_role(role_data)
        return {"status": "success", "data": role.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء الدور: {str(e)}"
        )


@security_router.get("/roles", response_model=Dict[str, Any])
async def get_all_roles(
    is_system_role: Optional[bool] = Query(None, description="ما إذا كان الدور نظاميًا"),
    is_active: Optional[bool] = Query(None, description="ما إذا كان الدور نشطًا"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع الأدوار"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.roles.view"])
    
    # إنشاء خدمة الأدوار
    role_service = RoleService(db_manager)
    
    # الحصول على الأدوار
    try:
        roles = role_service.get_all_roles(is_system_role, is_active)
        return {
            "status": "success",
            "data": [role.to_dict() for role in roles]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على الأدوار: {str(e)}"
        )


@security_router.get("/roles/{role_id}", response_model=Dict[str, Any])
async def get_role(
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على دور بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.roles.view"])
    
    # إنشاء خدمة الأدوار
    role_service = RoleService(db_manager)
    
    # الحصول على الدور
    role = role_service.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الدور بالمعرف {role_id}"
        )
    
    return {"status": "success", "data": role.to_dict()}


@security_router.put("/roles/{role_id}", response_model=Dict[str, Any])
async def update_role(
    role_id: str = Path(..., description="معرف الدور"),
    role_data: Dict[str, Any] = Body(..., description="بيانات الدور المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث دور"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.roles.update"])
    
    # إضافة معرف المستخدم الذي حدث الدور
    role_data["updated_by"] = current_user["user_id"]
    
    # إنشاء خدمة الأدوار
    role_service = RoleService(db_manager)
    
    # تحديث الدور
    try:
        role = role_service.update_role(role_id, role_data)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الدور بالمعرف {role_id}"
            )
        
        return {"status": "success", "data": role.to_dict()}
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
            detail=f"فشل في تحديث الدور: {str(e)}"
        )


@security_router.delete("/roles/{role_id}", response_model=Dict[str, Any])
async def delete_role(
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف دور"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.roles.delete"])
    
    # إنشاء خدمة الأدوار
    role_service = RoleService(db_manager)
    
    # حذف الدور
    try:
        success = role_service.delete_role(role_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الدور بالمعرف {role_id}"
            )
        
        return {"status": "success", "message": "تم حذف الدور بنجاح"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف الدور: {str(e)}"
        )


@security_router.get("/roles/{role_id}/permissions", response_model=Dict[str, Any])
async def get_role_permissions(
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على صلاحيات الدور"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.roles.view"])
    
    # إنشاء خدمة الأدوار
    role_service = RoleService(db_manager)
    
    # الحصول على الدور
    role = role_service.get_role(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الدور بالمعرف {role_id}"
        )
    
    # الحصول على صلاحيات الدور
    permissions = role_service.get_role_permissions(role_id)
    
    return {
        "status": "success",
        "data": {
            "role": role.to_dict(),
            "permissions": [permission.to_dict() for permission in permissions]
        }
    }


@security_router.post("/roles/{role_id}/permissions/{permission_id}", response_model=Dict[str, Any])
async def add_permission_to_role(
    role_id: str = Path(..., description="معرف الدور"),
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إضافة صلاحية إلى دور"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.roles.update"])
    
    # إنشاء خدمة الأدوار
    role_service = RoleService(db_manager)
    
    # إضافة الصلاحية إلى الدور
    try:
        role = role_service.add_permission_to_role(role_id, permission_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الدور بالمعرف {role_id}"
            )
        
        return {"status": "success", "data": role.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إضافة الصلاحية إلى الدور: {str(e)}"
        )


@security_router.delete("/roles/{role_id}/permissions/{permission_id}", response_model=Dict[str, Any])
async def remove_permission_from_role(
    role_id: str = Path(..., description="معرف الدور"),
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إزالة صلاحية من دور"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.roles.update"])
    
    # إنشاء خدمة الأدوار
    role_service = RoleService(db_manager)
    
    # إزالة الصلاحية من الدور
    try:
        role = role_service.remove_permission_from_role(role_id, permission_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الدور بالمعرف {role_id}"
            )
        
        return {"status": "success", "data": role.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إزالة الصلاحية من الدور: {str(e)}"
        )


# وحدات التحكم في صلاحيات المستخدمين
@security_router.post("/user-permissions", response_model=Dict[str, Any])
async def assign_permission_to_user(
    user_permission_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تعيين صلاحية لمستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.user_permissions.create"])
    
    # إضافة معرف المستخدم الذي منح الصلاحية
    user_permission_data["granted_by"] = current_user["user_id"]
    
    # إنشاء خدمة صلاحيات المستخدمين
    user_permission_service = UserPermissionService(db_manager)
    
    # تعيين الصلاحية للمستخدم
    try:
        user_permission = user_permission_service.assign_permission_to_user(user_permission_data)
        return {"status": "success", "data": user_permission.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تعيين الصلاحية للمستخدم: {str(e)}"
        )


@security_router.post("/user-roles", response_model=Dict[str, Any])
async def assign_role_to_user(
    user_role_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تعيين دور لمستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.user_roles.create"])
    
    # إضافة معرف المستخدم الذي منح الدور
    user_role_data["granted_by"] = current_user["user_id"]
    
    # إنشاء خدمة صلاحيات المستخدمين
    user_permission_service = UserPermissionService(db_manager)
    
    # تعيين الدور للمستخدم
    try:
        user_role = user_permission_service.assign_role_to_user(user_role_data)
        return {"status": "success", "data": user_role.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تعيين الدور للمستخدم: {str(e)}"
        )


@security_router.get("/users/{user_id}/permissions", response_model=Dict[str, Any])
async def get_user_permissions(
    user_id: str = Path(..., description="معرف المستخدم"),
    country_id: Optional[str] = Query(None, description="معرف الدولة"),
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على صلاحيات المستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.user_permissions.view"])
    
    # إنشاء خدمة صلاحيات المستخدمين
    user_permission_service = UserPermissionService(db_manager)
    
    # الحصول على صلاحيات المستخدم
    try:
        permissions = user_permission_service.get_user_permissions(user_id, country_id, company_id, branch_id)
        return {
            "status": "success",
            "data": [permission.to_dict() for permission in permissions]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على صلاحيات المستخدم: {str(e)}"
        )


@security_router.get("/users/{user_id}/roles", response_model=Dict[str, Any])
async def get_user_roles(
    user_id: str = Path(..., description="معرف المستخدم"),
    country_id: Optional[str] = Query(None, description="معرف الدولة"),
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على أدوار المستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.user_roles.view"])
    
    # إنشاء خدمة صلاحيات المستخدمين
    user_permission_service = UserPermissionService(db_manager)
    
    # الحصول على أدوار المستخدم
    try:
        roles = user_permission_service.get_user_roles(user_id, country_id, company_id, branch_id)
        return {
            "status": "success",
            "data": [role.to_dict() for role in roles]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على أدوار المستخدم: {str(e)}"
        )


@security_router.delete("/user-permissions/{user_permission_id}", response_model=Dict[str, Any])
async def revoke_permission_from_user(
    user_permission_id: str = Path(..., description="معرف صلاحية المستخدم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إلغاء صلاحية من مستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.user_permissions.delete"])
    
    # إنشاء خدمة صلاحيات المستخدمين
    user_permission_service = UserPermissionService(db_manager)
    
    # إلغاء الصلاحية من المستخدم
    try:
        success = user_permission_service.revoke_permission_from_user(user_permission_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على صلاحية المستخدم بالمعرف {user_permission_id}"
            )
        
        return {"status": "success", "message": "تم إلغاء الصلاحية من المستخدم بنجاح"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إلغاء الصلاحية من المستخدم: {str(e)}"
        )


@security_router.delete("/user-roles/{user_role_id}", response_model=Dict[str, Any])
async def revoke_role_from_user(
    user_role_id: str = Path(..., description="معرف دور المستخدم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إلغاء دور من مستخدم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.user_roles.delete"])
    
    # إنشاء خدمة صلاحيات المستخدمين
    user_permission_service = UserPermissionService(db_manager)
    
    # إلغاء الدور من المستخدم
    try:
        success = user_permission_service.revoke_role_from_user(user_role_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على دور المستخدم بالمعرف {user_role_id}"
            )
        
        return {"status": "success", "message": "تم إلغاء الدور من المستخدم بنجاح"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إلغاء الدور من المستخدم: {str(e)}"
        )


@security_router.get("/permissions/{permission_id}/users", response_model=Dict[str, Any])
async def get_users_by_permission(
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على المستخدمين الذين لديهم صلاحية معينة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.user_permissions.view"])
    
    # إنشاء خدمة صلاحيات المستخدمين
    user_permission_service = UserPermissionService(db_manager)
    
    # الحصول على المستخدمين
    try:
        users = user_permission_service.get_users_by_permission(permission_id)
        return {
            "status": "success",
            "data": users
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على المستخدمين: {str(e)}"
        )


@security_router.get("/roles/{role_id}/users", response_model=Dict[str, Any])
async def get_users_by_role(
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على المستخدمين الذين لديهم دور معين"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.user_roles.view"])
    
    # إنشاء خدمة صلاحيات المستخدمين
    user_permission_service = UserPermissionService(db_manager)
    
    # الحصول على المستخدمين
    try:
        users = user_permission_service.get_users_by_role(role_id)
        return {
            "status": "success",
            "data": users
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على المستخدمين: {str(e)}"
        )


# وحدات التحكم في المصادقة
@security_router.post("/auth/login", response_model=Dict[str, Any])
async def login(
    login_data: Dict[str, Any],
    request: Request,
    db_manager = Depends(get_db_manager)
):
    """تسجيل الدخول"""
    # التحقق من البيانات المطلوبة
    required_fields = ["username", "password"]
    for field in required_fields:
        if field not in login_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"الحقل {field} مطلوب"
            )
    
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # مصادقة المستخدم
    result = auth_service.authenticate(
        login_data["username"],
        login_data["password"],
        ip_address,
        user_agent
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["message"]
        )
    
    return {"status": "success", "data": result}


@security_router.post("/auth/verify-2fa", response_model=Dict[str, Any])
async def verify_two_factor(
    two_factor_data: Dict[str, Any],
    request: Request,
    db_manager = Depends(get_db_manager)
):
    """التحقق من المصادقة الثنائية"""
    # التحقق من البيانات المطلوبة
    required_fields = ["user_id", "code"]
    for field in required_fields:
        if field not in two_factor_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"الحقل {field} مطلوب"
            )
    
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # التحقق من المصادقة الثنائية
    result = auth_service.verify_two_factor(
        two_factor_data["user_id"],
        two_factor_data["code"],
        ip_address,
        user_agent
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["message"]
        )
    
    return {"status": "success", "data": result}


@security_router.post("/auth/refresh-token", response_model=Dict[str, Any])
async def refresh_token(
    refresh_data: Dict[str, Any],
    request: Request,
    db_manager = Depends(get_db_manager)
):
    """تحديث رمز الوصول"""
    # التحقق من البيانات المطلوبة
    if "refresh_token" not in refresh_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الحقل refresh_token مطلوب"
        )
    
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # تحديث رمز الوصول
    result = auth_service.refresh_token(
        refresh_data["refresh_token"],
        ip_address,
        user_agent
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["message"]
        )
    
    return {"status": "success", "data": result}


@security_router.post("/auth/logout", response_model=Dict[str, Any])
async def logout(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تسجيل الخروج"""
    # الحصول على رمز الوصول من الرأس
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="رمز الوصول غير موجود"
        )
    
    token = auth_header.split(" ")[1]
    
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # تسجيل الخروج
    result = auth_service.logout(token, ip_address, user_agent)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {"status": "success", "message": "تم تسجيل الخروج بنجاح"}


@security_router.post("/auth/change-password", response_model=Dict[str, Any])
async def change_password(
    password_data: Dict[str, Any],
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تغيير كلمة المرور"""
    # التحقق من البيانات المطلوبة
    required_fields = ["current_password", "new_password"]
    for field in required_fields:
        if field not in password_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"الحقل {field} مطلوب"
            )
    
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # تغيير كلمة المرور
    result = auth_service.change_password(
        current_user["user_id"],
        password_data["current_password"],
        password_data["new_password"],
        ip_address,
        user_agent
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {"status": "success", "message": "تم تغيير كلمة المرور بنجاح"}


@security_router.post("/auth/reset-password-request", response_model=Dict[str, Any])
async def reset_password_request(
    reset_data: Dict[str, Any],
    request: Request,
    db_manager = Depends(get_db_manager)
):
    """طلب إعادة تعيين كلمة المرور"""
    # التحقق من البيانات المطلوبة
    if "email" not in reset_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الحقل email مطلوب"
        )
    
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # طلب إعادة تعيين كلمة المرور
    result = auth_service.reset_password_request(
        reset_data["email"],
        ip_address,
        user_agent
    )
    
    # لأسباب أمنية، نعيد دائمًا رسالة نجاح حتى لو لم يكن البريد الإلكتروني موجودًا
    return {"status": "success", "message": "تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني"}


@security_router.post("/auth/reset-password", response_model=Dict[str, Any])
async def reset_password(
    reset_data: Dict[str, Any],
    request: Request,
    db_manager = Depends(get_db_manager)
):
    """إعادة تعيين كلمة المرور"""
    # التحقق من البيانات المطلوبة
    required_fields = ["token", "new_password"]
    for field in required_fields:
        if field not in reset_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"الحقل {field} مطلوب"
            )
    
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # إعادة تعيين كلمة المرور
    result = auth_service.reset_password(
        reset_data["token"],
        reset_data["new_password"],
        ip_address,
        user_agent
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {"status": "success", "message": "تم إعادة تعيين كلمة المرور بنجاح"}


@security_router.post("/auth/setup-2fa", response_model=Dict[str, Any])
async def setup_two_factor(
    setup_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إعداد المصادقة الثنائية"""
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # إعداد المصادقة الثنائية
    result = auth_service.setup_two_factor(
        current_user["user_id"],
        setup_data.get("method", "app")
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {"status": "success", "data": result["two_factor_auth"]}


@security_router.post("/auth/enable-2fa", response_model=Dict[str, Any])
async def enable_two_factor(
    enable_data: Dict[str, Any],
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تفعيل المصادقة الثنائية"""
    # التحقق من البيانات المطلوبة
    if "code" not in enable_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الحقل code مطلوب"
        )
    
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # تفعيل المصادقة الثنائية
    result = auth_service.enable_two_factor(
        current_user["user_id"],
        enable_data["code"],
        ip_address,
        user_agent
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {"status": "success", "message": "تم تفعيل المصادقة الثنائية بنجاح"}


@security_router.post("/auth/disable-2fa", response_model=Dict[str, Any])
async def disable_two_factor(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تعطيل المصادقة الثنائية"""
    # الحصول على عنوان IP ووكيل المستخدم
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # إنشاء خدمة المصادقة
    auth_service = AuthService(db_manager)
    
    # تعطيل المصادقة الثنائية
    result = auth_service.disable_two_factor(
        current_user["user_id"],
        ip_address,
        user_agent
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {"status": "success", "message": "تم تعطيل المصادقة الثنائية بنجاح"}


# وحدات التحكم في مفاتيح API
@security_router.post("/api-keys", response_model=Dict[str, Any])
async def create_api_key(
    api_key_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء مفتاح API جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.api_keys.create"])
    
    # إضافة معرف المستخدم الذي أنشأ المفتاح
    api_key_data["created_by"] = current_user["user_id"]
    
    # إنشاء خدمة مفاتيح API
    api_key_service = ApiKeyService(db_manager)
    
    # إنشاء مفتاح API
    try:
        api_key = api_key_service.create_api_key(api_key_data)
        return {"status": "success", "data": api_key.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء مفتاح API: {str(e)}"
        )


@security_router.get("/api-keys", response_model=Dict[str, Any])
async def get_all_api_keys(
    user_id: Optional[str] = Query(None, description="معرف المستخدم"),
    is_active: Optional[bool] = Query(None, description="ما إذا كان المفتاح نشطًا"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع مفاتيح API"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.api_keys.view"])
    
    # إنشاء خدمة مفاتيح API
    api_key_service = ApiKeyService(db_manager)
    
    # الحصول على مفاتيح API
    try:
        api_keys = api_key_service.get_all_api_keys(user_id, is_active)
        return {
            "status": "success",
            "data": [api_key.to_dict() for api_key in api_keys]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على مفاتيح API: {str(e)}"
        )


@security_router.get("/api-keys/{api_key_id}", response_model=Dict[str, Any])
async def get_api_key(
    api_key_id: str = Path(..., description="معرف مفتاح API"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على مفتاح API بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.api_keys.view"])
    
    # إنشاء خدمة مفاتيح API
    api_key_service = ApiKeyService(db_manager)
    
    # الحصول على مفتاح API
    api_key = api_key_service.get_api_key(api_key_id)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على مفتاح API بالمعرف {api_key_id}"
        )
    
    return {"status": "success", "data": api_key.to_dict()}


@security_router.put("/api-keys/{api_key_id}", response_model=Dict[str, Any])
async def update_api_key(
    api_key_id: str = Path(..., description="معرف مفتاح API"),
    api_key_data: Dict[str, Any] = Body(..., description="بيانات مفتاح API المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث مفتاح API"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.api_keys.update"])
    
    # إنشاء خدمة مفاتيح API
    api_key_service = ApiKeyService(db_manager)
    
    # تحديث مفتاح API
    try:
        api_key = api_key_service.update_api_key(api_key_id, api_key_data)
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على مفتاح API بالمعرف {api_key_id}"
            )
        
        return {"status": "success", "data": api_key.to_dict()}
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
            detail=f"فشل في تحديث مفتاح API: {str(e)}"
        )


@security_router.delete("/api-keys/{api_key_id}", response_model=Dict[str, Any])
async def delete_api_key(
    api_key_id: str = Path(..., description="معرف مفتاح API"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف مفتاح API"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.api_keys.delete"])
    
    # إنشاء خدمة مفاتيح API
    api_key_service = ApiKeyService(db_manager)
    
    # حذف مفتاح API
    try:
        success = api_key_service.delete_api_key(api_key_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على مفتاح API بالمعرف {api_key_id}"
            )
        
        return {"status": "success", "message": "تم حذف مفتاح API بنجاح"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف مفتاح API: {str(e)}"
        )


@security_router.post("/api-keys/{api_key_id}/regenerate", response_model=Dict[str, Any])
async def regenerate_api_key(
    api_key_id: str = Path(..., description="معرف مفتاح API"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إعادة توليد مفتاح API"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.api_keys.update"])
    
    # إنشاء خدمة مفاتيح API
    api_key_service = ApiKeyService(db_manager)
    
    # إعادة توليد مفتاح API
    try:
        api_key = api_key_service.regenerate_api_key(api_key_id)
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على مفتاح API بالمعرف {api_key_id}"
            )
        
        return {"status": "success", "data": api_key.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إعادة توليد مفتاح API: {str(e)}"
        )


@security_router.post("/api-keys/verify", response_model=Dict[str, Any])
async def verify_api_key(
    verify_data: Dict[str, Any],
    request: Request,
    current_user: Dict[str, Any] = Depends(get_optional_current_user),
    db_manager = Depends(get_db_manager)
):
    """التحقق من مفتاح API"""
    # التحقق من البيانات المطلوبة
    if "key" not in verify_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الحقل key مطلوب"
        )
    
    # الحصول على عنوان IP
    ip_address = request.client.host
    
    # إنشاء خدمة مفاتيح API
    api_key_service = ApiKeyService(db_manager)
    
    # التحقق من مفتاح API
    result = api_key_service.verify_api_key(verify_data["key"], ip_address)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["message"]
        )
    
    return {"status": "success", "data": result}


# وحدات التحكم في سياسات الأمان
@security_router.post("/security-policies", response_model=Dict[str, Any])
async def create_security_policy(
    policy_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء سياسة أمان جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.policies.create"])
    
    # إضافة معرف المستخدم الذي أنشأ السياسة
    policy_data["created_by"] = current_user["user_id"]
    
    # إنشاء خدمة سياسات الأمان
    security_policy_service = SecurityPolicyService(db_manager)
    
    # إنشاء سياسة الأمان
    try:
        security_policy = security_policy_service.create_security_policy(policy_data)
        return {"status": "success", "data": security_policy.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء سياسة الأمان: {str(e)}"
        )


@security_router.get("/security-policies", response_model=Dict[str, Any])
async def get_all_security_policies(
    is_active: Optional[bool] = Query(None, description="ما إذا كانت السياسة نشطة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع سياسات الأمان"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.policies.view"])
    
    # إنشاء خدمة سياسات الأمان
    security_policy_service = SecurityPolicyService(db_manager)
    
    # الحصول على سياسات الأمان
    try:
        security_policies = security_policy_service.get_all_security_policies(is_active)
        return {
            "status": "success",
            "data": [policy.to_dict() for policy in security_policies]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على سياسات الأمان: {str(e)}"
        )


@security_router.get("/security-policies/{policy_id}", response_model=Dict[str, Any])
async def get_security_policy(
    policy_id: str = Path(..., description="معرف سياسة الأمان"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على سياسة أمان بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.policies.view"])
    
    # إنشاء خدمة سياسات الأمان
    security_policy_service = SecurityPolicyService(db_manager)
    
    # الحصول على سياسة الأمان
    security_policy = security_policy_service.get_security_policy(policy_id)
    if not security_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على سياسة الأمان بالمعرف {policy_id}"
        )
    
    return {"status": "success", "data": security_policy.to_dict()}


@security_router.get("/security-policies/default", response_model=Dict[str, Any])
async def get_default_security_policy(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على سياسة الأمان الافتراضية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.policies.view"])
    
    # إنشاء خدمة سياسات الأمان
    security_policy_service = SecurityPolicyService(db_manager)
    
    # الحصول على سياسة الأمان الافتراضية
    security_policy = security_policy_service.get_default_security_policy()
    if not security_policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="لم يتم العثور على سياسة أمان افتراضية"
        )
    
    return {"status": "success", "data": security_policy.to_dict()}


@security_router.put("/security-policies/{policy_id}", response_model=Dict[str, Any])
async def update_security_policy(
    policy_id: str = Path(..., description="معرف سياسة الأمان"),
    policy_data: Dict[str, Any] = Body(..., description="بيانات سياسة الأمان المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث سياسة أمان"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.policies.update"])
    
    # إضافة معرف المستخدم الذي حدث السياسة
    policy_data["updated_by"] = current_user["user_id"]
    
    # إنشاء خدمة سياسات الأمان
    security_policy_service = SecurityPolicyService(db_manager)
    
    # تحديث سياسة الأمان
    try:
        security_policy = security_policy_service.update_security_policy(policy_id, policy_data)
        if not security_policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على سياسة الأمان بالمعرف {policy_id}"
            )
        
        return {"status": "success", "data": security_policy.to_dict()}
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
            detail=f"فشل في تحديث سياسة الأمان: {str(e)}"
        )


@security_router.delete("/security-policies/{policy_id}", response_model=Dict[str, Any])
async def delete_security_policy(
    policy_id: str = Path(..., description="معرف سياسة الأمان"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف سياسة أمان"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.policies.delete"])
    
    # إنشاء خدمة سياسات الأمان
    security_policy_service = SecurityPolicyService(db_manager)
    
    # حذف سياسة الأمان
    try:
        success = security_policy_service.delete_security_policy(policy_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على سياسة الأمان بالمعرف {policy_id}"
            )
        
        return {"status": "success", "message": "تم حذف سياسة الأمان بنجاح"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف سياسة الأمان: {str(e)}"
        )


@security_router.post("/security-policies/{policy_id}/set-default", response_model=Dict[str, Any])
async def set_default_security_policy(
    policy_id: str = Path(..., description="معرف سياسة الأمان"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تعيين سياسة أمان كافتراضية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.policies.update"])
    
    # إنشاء خدمة سياسات الأمان
    security_policy_service = SecurityPolicyService(db_manager)
    
    # تعيين سياسة الأمان كافتراضية
    try:
        security_policy = security_policy_service.set_default_security_policy(policy_id)
        if not security_policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على سياسة الأمان بالمعرف {policy_id}"
            )
        
        return {"status": "success", "data": security_policy.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تعيين سياسة الأمان كافتراضية: {str(e)}"
        )


# وحدات التحكم في سجلات تدقيق الأمان
@security_router.get("/audit-logs", response_model=Dict[str, Any])
async def get_security_audits(
    user_id: Optional[str] = Query(None, description="معرف المستخدم"),
    action: Optional[str] = Query(None, description="الإجراء"),
    resource_type: Optional[str] = Query(None, description="نوع المورد"),
    resource_id: Optional[str] = Query(None, description="معرف المورد"),
    ip_address: Optional[str] = Query(None, description="عنوان IP"),
    start_date: Optional[datetime] = Query(None, description="تاريخ البداية"),
    end_date: Optional[datetime] = Query(None, description="تاريخ النهاية"),
    limit: int = Query(100, description="عدد السجلات المراد إرجاعها"),
    offset: int = Query(0, description="عدد السجلات المراد تخطيها"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على سجلات تدقيق الأمان"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.audit_logs.view"])
    
    # إنشاء خدمة سجلات تدقيق الأمان
    security_audit_service = SecurityAuditService(db_manager)
    
    # الحصول على سجلات تدقيق الأمان
    try:
        audits, total = security_audit_service.get_security_audits(
            user_id, action, resource_type, resource_id,
            ip_address, start_date, end_date, limit, offset
        )
        
        return {
            "status": "success",
            "data": {
                "audits": [audit.to_dict() for audit in audits],
                "total": total,
                "limit": limit,
                "offset": offset
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على سجلات تدقيق الأمان: {str(e)}"
        )


@security_router.get("/audit-logs/{audit_id}", response_model=Dict[str, Any])
async def get_security_audit(
    audit_id: str = Path(..., description="معرف سجل تدقيق الأمان"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على سجل تدقيق أمان بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.audit_logs.view"])
    
    # إنشاء خدمة سجلات تدقيق الأمان
    security_audit_service = SecurityAuditService(db_manager)
    
    # الحصول على سجل تدقيق الأمان
    audit = security_audit_service.get_security_audit(audit_id)
    if not audit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على سجل تدقيق الأمان بالمعرف {audit_id}"
        )
    
    return {"status": "success", "data": audit.to_dict()}


@security_router.delete("/audit-logs/cleanup", response_model=Dict[str, Any])
async def cleanup_security_audits(
    days: int = Query(..., description="عدد الأيام للاحتفاظ بسجلات تدقيق الأمان"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف سجلات تدقيق الأمان القديمة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["security.audit_logs.delete"])
    
    # التحقق من عدد الأيام
    if days < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="يجب أن يكون عدد الأيام أكبر من صفر"
        )
    
    # إنشاء خدمة سجلات تدقيق الأمان
    security_audit_service = SecurityAuditService(db_manager)
    
    # حذف سجلات تدقيق الأمان القديمة
    try:
        count = security_audit_service.delete_security_audits_older_than(days)
        return {"status": "success", "message": f"تم حذف {count} سجل تدقيق أمان"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في حذف سجلات تدقيق الأمان القديمة: {str(e)}"
        )
