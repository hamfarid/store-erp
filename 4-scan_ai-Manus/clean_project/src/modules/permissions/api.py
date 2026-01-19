"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/permissions/api.py

واجهة برمجة التطبيقات لوحدة الصلاحيات في نظام Gaara ERP
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import Dict, Any, Optional
import logging

from .service import PermissionService, get_permission_service
from ...modules.authentication.service import get_current_user

# إعداد التسجيل
logger = logging.getLogger(__name__)

# إنشاء موجه API
router = APIRouter(
    prefix="/api/v1/permissions",
    tags=["permissions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=Dict[str, Any])
async def create_permission(
    name: str,
    description: str,
    resource_type: str,
    action: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    إنشاء صلاحية جديدة

    Args:
        name: اسم الصلاحية
        description: وصف الصلاحية
        resource_type: نوع المورد
        action: الإجراء

    Returns:
        الصلاحية المنشأة
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="create_permission"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإنشاء صلاحيات جديدة"
        )

    try:
        permission = await permission_service.create_permission(
            name=name,
            description=description,
            resource_type=resource_type,
            action=action
        )

        return {
            "status": "success",
            "message": "تم إنشاء الصلاحية بنجاح",
            "data": permission
        }

    except Exception as e:
        logger.error(f"خطأ في إنشاء الصلاحية: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في إنشاء الصلاحية: {str(e)}"
        )


@router.get("/all", response_model=Dict[str, Any])
async def get_all_permissions(
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على جميع الصلاحيات

    Returns:
        قائمة الصلاحيات
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_permissions"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض الصلاحيات"
        )

    try:
        permissions = await permission_service.get_permissions()

        return {
            "status": "success",
            "message": "تم الحصول على الصلاحيات بنجاح",
            "data": permissions
        }

    except Exception as e:
        logger.error(f"خطأ في الحصول على الصلاحيات: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على الصلاحيات: {str(e)}"
        )


@router.get("/{permission_id}", response_model=Dict[str, Any])
async def get_permission_by_id(
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على صلاحية بواسطة المعرف

    Args:
        permission_id: معرف الصلاحية

    Returns:
        الصلاحية المطلوبة
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_permissions"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض الصلاحيات"
        )

    try:
        permission = await permission_service.get_permission(permission_id)

        return {
            "status": "success",
            "message": "تم الحصول على الصلاحية بنجاح",
            "data": permission
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في الحصول على الصلاحية: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على الصلاحية: {str(e)}"
        )


@router.put("/{permission_id}", response_model=Dict[str, Any])
async def update_permission_by_id(
    permission_id: str = Path(..., description="معرف الصلاحية"),
    name: Optional[str] = None,
    description: Optional[str] = None,
    resource_type: Optional[str] = None,
    action: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    تحديث صلاحية بواسطة المعرف

    Args:
        permission_id: معرف الصلاحية
        name: الاسم الجديد
        description: الوصف الجديد
        resource_type: نوع المورد الجديد
        action: الإجراء الجديد

    Returns:
        الصلاحية المحدثة
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="update_permission"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لتحديث الصلاحيات"
        )

    try:
        permission = await permission_service.update_permission(
            permission_id=permission_id,
            name=name,
            description=description,
            resource_type=resource_type,
            action=action
        )

        return {
            "status": "success",
            "message": "تم تحديث الصلاحية بنجاح",
            "data": permission
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في تحديث الصلاحية: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في تحديث الصلاحية: {str(e)}"
        )


@router.delete("/{permission_id}", response_model=Dict[str, Any])
async def delete_permission_by_id(
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    حذف صلاحية بواسطة المعرف

    Args:
        permission_id: معرف الصلاحية

    Returns:
        رسالة نجاح العملية
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="delete_permission"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لحذف الصلاحيات"
        )

    try:
        await permission_service.delete_permission(permission_id)

        return {
            "status": "success",
            "message": "تم حذف الصلاحية بنجاح"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في حذف الصلاحية: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في حذف الصلاحية: {str(e)}"
        )


@router.post("/roles/create", response_model=Dict[str, Any])
async def create_role(
    name: str,
    description: str,
    is_system_role: bool = False,
    organization_id: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    إنشاء دور جديد

    Args:
        name: اسم الدور
        description: وصف الدور
        is_system_role: هل هو دور نظام
        organization_id: معرف المؤسسة

    Returns:
        الدور المنشأ
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="create_role"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإنشاء أدوار جديدة"
        )

    try:
        role = await permission_service.create_role(
            name=name,
            description=description,
            is_system_role=is_system_role,
            organization_id=organization_id
        )

        return {
            "status": "success",
            "message": "تم إنشاء الدور بنجاح",
            "data": role
        }

    except Exception as e:
        logger.error(f"خطأ في إنشاء الدور: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في إنشاء الدور: {str(e)}"
        )


@router.get("/roles/all", response_model=Dict[str, Any])
async def get_all_roles(
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على جميع الأدوار

    Returns:
        قائمة الأدوار
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_roles"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض الأدوار"
        )

    try:
        roles = await permission_service.get_roles()

        return {
            "status": "success",
            "message": "تم الحصول على الأدوار بنجاح",
            "data": roles
        }

    except Exception as e:
        logger.error(f"خطأ في الحصول على الأدوار: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على الأدوار: {str(e)}"
        )


@router.get("/roles/{role_id}", response_model=Dict[str, Any])
async def get_role_by_id(
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على دور بواسطة المعرف

    Args:
        role_id: معرف الدور

    Returns:
        الدور المطلوب
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_roles"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض الأدوار"
        )

    try:
        role = await permission_service.get_role(role_id)

        return {
            "status": "success",
            "message": "تم الحصول على الدور بنجاح",
            "data": role
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في الحصول على الدور: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على الدور: {str(e)}"
        )


@router.put("/roles/{role_id}", response_model=Dict[str, Any])
async def update_role_by_id(
    role_id: str = Path(..., description="معرف الدور"),
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_system_role: Optional[bool] = None,
    organization_id: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    تحديث دور بواسطة المعرف

    Args:
        role_id: معرف الدور
        name: الاسم الجديد
        description: الوصف الجديد
        is_system_role: هل هو دور نظام
        organization_id: معرف المؤسسة

    Returns:
        الدور المحدث
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="update_role"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لتحديث الأدوار"
        )

    try:
        role = await permission_service.update_role(
            role_id=role_id,
            name=name,
            description=description,
            is_system_role=is_system_role,
            organization_id=organization_id
        )

        return {
            "status": "success",
            "message": "تم تحديث الدور بنجاح",
            "data": role
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في تحديث الدور: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في تحديث الدور: {str(e)}"
        )


@router.delete("/roles/{role_id}", response_model=Dict[str, Any])
async def delete_role_by_id(
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    حذف دور بواسطة المعرف

    Args:
        role_id: معرف الدور

    Returns:
        رسالة نجاح العملية
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="delete_role"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لحذف الأدوار"
        )

    try:
        await permission_service.delete_role(role_id)

        return {
            "status": "success",
            "message": "تم حذف الدور بنجاح"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في حذف الدور: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في حذف الدور: {str(e)}"
        )


@router.post("/roles/{role_id}/permissions/{permission_id}", response_model=Dict[str, Any])
async def assign_permission_to_role(
    role_id: str = Path(..., description="معرف الدور"),
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    تعيين صلاحية لدور

    Args:
        role_id: معرف الدور
        permission_id: معرف الصلاحية

    Returns:
        رسالة نجاح العملية
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="assign_permission_to_role"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لتعيين الصلاحيات للأدوار"
        )

    try:
        await permission_service.assign_permission_to_role(
            role_id=role_id,
            permission_id=permission_id,
            assigned_by=current_user["id"]
        )

        return {
            "status": "success",
            "message": "تم تعيين الصلاحية للدور بنجاح"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في تعيين الصلاحية للدور: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في تعيين الصلاحية للدور: {str(e)}"
        )


@router.delete("/roles/{role_id}/permissions/{permission_id}", response_model=Dict[str, Any])
async def remove_permission_from_role(
    role_id: str = Path(..., description="معرف الدور"),
    permission_id: str = Path(..., description="معرف الصلاحية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    إزالة صلاحية من دور

    Args:
        role_id: معرف الدور
        permission_id: معرف الصلاحية

    Returns:
        رسالة نجاح العملية
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="remove_permission_from_role"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإزالة الصلاحيات من الأدوار"
        )

    try:
        await permission_service.remove_permission_from_role(
            role_id=role_id,
            permission_id=permission_id
        )

        return {
            "status": "success",
            "message": "تم إزالة الصلاحية من الدور بنجاح"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في إزالة الصلاحية من الدور: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في إزالة الصلاحية من الدور: {str(e)}"
        )


@router.post("/users/{user_id}/roles/{role_id}", response_model=Dict[str, Any])
async def assign_role_to_user(
    user_id: str = Path(..., description="معرف المستخدم"),
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    تعيين دور لمستخدم

    Args:
        user_id: معرف المستخدم
        role_id: معرف الدور

    Returns:
        رسالة نجاح العملية
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="assign_role_to_user"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لتعيين الأدوار للمستخدمين"
        )

    try:
        await permission_service.assign_role_to_user(
            user_id=user_id,
            role_id=role_id,
            assigned_by=current_user["id"]
        )

        return {
            "status": "success",
            "message": "تم تعيين الدور للمستخدم بنجاح"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في تعيين الدور للمستخدم: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في تعيين الدور للمستخدم: {str(e)}"
        )


@router.delete("/users/{user_id}/roles/{role_id}", response_model=Dict[str, Any])
async def remove_role_from_user(
    user_id: str = Path(..., description="معرف المستخدم"),
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    إزالة دور من مستخدم

    Args:
        user_id: معرف المستخدم
        role_id: معرف الدور

    Returns:
        رسالة نجاح العملية
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="remove_role_from_user"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإزالة الأدوار من المستخدمين"
        )

    try:
        await permission_service.remove_role_from_user(
            user_id=user_id,
            role_id=role_id
        )

        return {
            "status": "success",
            "message": "تم إزالة الدور من المستخدم بنجاح"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في إزالة الدور من المستخدم: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في إزالة الدور من المستخدم: {str(e)}"
        )


@router.get("/users/{user_id}/roles", response_model=Dict[str, Any])
async def get_user_roles(
    user_id: str = Path(..., description="معرف المستخدم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على أدوار مستخدم

    Args:
        user_id: معرف المستخدم

    Returns:
        قائمة الأدوار
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_user_roles"
    )

    if not has_permission and current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض أدوار المستخدمين"
        )

    try:
        roles = await permission_service.get_user_roles(user_id)

        return {
            "status": "success",
            "message": "تم الحصول على أدوار المستخدم بنجاح",
            "data": roles
        }

    except Exception as e:
        logger.error(f"خطأ في الحصول على أدوار المستخدم: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على أدوار المستخدم: {str(e)}"
        )


@router.get("/users/{user_id}/permissions", response_model=Dict[str, Any])
async def get_user_permissions(
    user_id: str = Path(..., description="معرف المستخدم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على صلاحيات مستخدم

    Args:
        user_id: معرف المستخدم

    Returns:
        قائمة الصلاحيات
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_user_permissions"
    )

    if not has_permission and current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض صلاحيات المستخدمين"
        )

    try:
        permissions = await permission_service.get_user_permissions(user_id)

        return {
            "status": "success",
            "message": "تم الحصول على صلاحيات المستخدم بنجاح",
            "data": permissions
        }

    except Exception as e:
        logger.error(f"خطأ في الحصول على صلاحيات المستخدم: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على صلاحيات المستخدم: {str(e)}"
        )


@router.get("/check", response_model=Dict[str, Any])
async def check_user_permission(
    permission: str = Query(..., description="اسم الصلاحية"),
    resource_id: Optional[str] = Query(None, description="معرف المورد"),
    user_id: Optional[str] = Query(None, description="معرف المستخدم (اختياري، يستخدم المستخدم الحالي إذا لم يتم تحديده)"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    التحقق من صلاحية مستخدم

    Args:
        permission: اسم الصلاحية
        resource_id: معرف المورد (اختياري)
        user_id: معرف المستخدم (اختياري، يستخدم المستخدم الحالي إذا لم يتم تحديده)

    Returns:
        نتيجة التحقق
    """
    # استخدام المستخدم الحالي إذا لم يتم تحديد معرف المستخدم
    check_user_id = user_id if user_id else current_user["id"]

    # التحقق من صلاحية المستخدم الحالي للتحقق من صلاحيات مستخدم آخر
    if user_id and user_id != current_user["id"]:
        has_admin_permission = await permission_service.check_permission(
            user_id=current_user["id"],
            permission="check_user_permissions"
        )

        if not has_admin_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="ليس لديك صلاحية للتحقق من صلاحيات المستخدمين الآخرين"
            )

    try:
        has_permission = await permission_service.check_permission(
            user_id=check_user_id,
            permission=permission,
            resource_id=resource_id
        )

        return {
            "status": "success",
            "message": "تم التحقق من الصلاحية بنجاح",
            "data": {
                "has_permission": has_permission
            }
        }

    except Exception as e:
        logger.error(f"خطأ في التحقق من الصلاحية: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في التحقق من الصلاحية: {str(e)}"
        )


@router.get("/roles/{role_id}/permissions", response_model=Dict[str, Any])
async def get_role_permissions(
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على صلاحيات دور

    Args:
        role_id: معرف الدور

    Returns:
        قائمة الصلاحيات
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_role_permissions"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض صلاحيات الأدوار"
        )

    try:
        permissions = await permission_service.get_role_permissions(role_id)

        return {
            "status": "success",
            "message": "تم الحصول على صلاحيات الدور بنجاح",
            "data": permissions
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في الحصول على صلاحيات الدور: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على صلاحيات الدور: {str(e)}"
        )


@router.get("/roles/{role_id}/users", response_model=Dict[str, Any])
async def get_users_with_role(
    role_id: str = Path(..., description="معرف الدور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على معرفات المستخدمين الذين لديهم دور معين

    Args:
        role_id: معرف الدور

    Returns:
        قائمة معرفات المستخدمين
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_role_users"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض مستخدمي الأدوار"
        )

    try:
        user_ids = await permission_service.get_users_with_role(role_id)

        return {
            "status": "success",
            "message": "تم الحصول على مستخدمي الدور بنجاح",
            "data": user_ids
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"خطأ في الحصول على مستخدمي الدور: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على مستخدمي الدور: {str(e)}"
        )


@router.get("/organization/{organization_id}/roles", response_model=Dict[str, Any])
async def get_organization_roles(
    organization_id: str = Path(..., description="معرف المؤسسة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service)
):
    """
    الحصول على أدوار مؤسسة معينة

    Args:
        organization_id: معرف المؤسسة

    Returns:
        قائمة الأدوار
    """
    # التحقق من صلاحية المستخدم
    has_permission = await permission_service.check_permission(
        user_id=current_user["id"],
        permission="view_organization_roles"
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لعرض أدوار المؤسسة"
        )

    try:
        roles = await permission_service.get_organization_roles(organization_id)

        return {
            "status": "success",
            "message": "تم الحصول على أدوار المؤسسة بنجاح",
            "data": roles
        }

    except Exception as e:
        logger.error(f"خطأ في الحصول على أدوار المؤسسة: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في الحصول على أدوار المؤسسة: {str(e)}"
        )
