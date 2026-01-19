"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/permissions/service.py

خدمة إدارة الصلاحيات في نظام Gaara ERP
"""

import logging
import uuid
from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ...database import get_db
from .models import Permission, Role, RolePermission, UserRole

# إعداد التسجيل
logger = logging.getLogger(__name__)


class PermissionService:
    """
    خدمة إدارة الصلاحيات في النظام
    """

    def __init__(self, db: Session):
        """
        تهيئة خدمة الصلاحيات

        Args:
            db (Session): جلسة قاعدة البيانات
        """
        self.db = db

    async def create_permission(
            self,
            name: str,
            description: str,
            resource_type: str,
            action: str) -> Permission:
        """
        إنشاء صلاحية جديدة

        Args:
            name (str): اسم الصلاحية
            description (str): وصف الصلاحية
            resource_type (str): نوع المورد
            action (str): الإجراء

        Returns:
            Permission: الصلاحية المنشأة

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            # التحقق من عدم وجود صلاحية بنفس الاسم
            existing_permission = self.db.query(
                Permission).filter(Permission.name == name).first()
            if existing_permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"الصلاحية بالاسم {name} موجودة بالفعل"
                )

            # إنشاء الصلاحية الجديدة
            permission = Permission(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                resource_type=resource_type,
                action=action
            )

            self.db.add(permission)
            self.db.commit()
            self.db.refresh(permission)

            logger.info(f"تم إنشاء صلاحية جديدة: {name}")
            return permission

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء الصلاحية: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في إنشاء الصلاحية: {str(e)}"
            )

    async def get_permission(self, permission_id: str) -> Permission:
        """
        الحصول على صلاحية بواسطة المعرف

        Args:
            permission_id (str): معرف الصلاحية

        Returns:
            Permission: الصلاحية المطلوبة

        Raises:
            HTTPException: في حالة عدم وجود الصلاحية
        """
        permission = self.db.query(Permission).filter(
            Permission.id == permission_id).first()
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"الصلاحية بالمعرف {permission_id} غير موجودة"
            )
        return permission

    async def get_permissions(self) -> List[Permission]:
        """
        الحصول على جميع الصلاحيات

        Returns:
            List[Permission]: قائمة الصلاحيات
        """
        return self.db.query(Permission).all()

    async def update_permission(
            self,
            permission_id: str,
            name: str = None,
            description: str = None,
            resource_type: str = None,
            action: str = None) -> Permission:
        """
        تحديث صلاحية

        Args:
            permission_id (str): معرف الصلاحية
            name (str, optional): الاسم الجديد
            description (str, optional): الوصف الجديد
            resource_type (str, optional): نوع المورد الجديد
            action (str, optional): الإجراء الجديد

        Returns:
            Permission: الصلاحية المحدثة

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            permission = await self.get_permission(permission_id)

            if name is not None:
                # التحقق من عدم وجود صلاحية أخرى بنفس الاسم
                existing_permission = self.db.query(Permission).filter(
                    Permission.name == name,
                    Permission.id != permission_id
                ).first()

                if existing_permission:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"الصلاحية بالاسم {name} موجودة بالفعل"
                    )

                permission.name = name

            if description is not None:
                permission.description = description

            if resource_type is not None:
                permission.resource_type = resource_type

            if action is not None:
                permission.action = action

            self.db.commit()
            self.db.refresh(permission)

            logger.info(f"تم تحديث الصلاحية: {permission.name}")
            return permission

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في تحديث الصلاحية: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في تحديث الصلاحية: {str(e)}"
            )

    async def delete_permission(self, permission_id: str) -> bool:
        """
        حذف صلاحية

        Args:
            permission_id (str): معرف الصلاحية

        Returns:
            bool: نجاح العملية

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            permission = await self.get_permission(permission_id)

            # التحقق من عدم ارتباط الصلاحية بأي أدوار
            if permission.roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="لا يمكن حذف الصلاحية لأنها مرتبطة بأدوار"
                )

            self.db.delete(permission)
            self.db.commit()

            logger.info(f"تم حذف الصلاحية: {permission.name}")
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في حذف الصلاحية: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في حذف الصلاحية: {str(e)}"
            )

    async def create_role(
            self,
            name: str,
            description: str,
            is_system_role: bool = False,
            organization_id: str = None) -> Role:
        """
        إنشاء دور جديد

        Args:
            name (str): اسم الدور
            description (str): وصف الدور
            is_system_role (bool, optional): هل هو دور نظام
            organization_id (str, optional): معرف المؤسسة

        Returns:
            Role: الدور المنشأ

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            # التحقق من عدم وجود دور بنفس الاسم
            existing_role = self.db.query(
                Role).filter(Role.name == name).first()
            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"الدور بالاسم {name} موجود بالفعل"
                )

            # إنشاء الدور الجديد
            role = Role(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                is_system_role=is_system_role,
                organization_id=organization_id
            )

            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)

            logger.info(f"تم إنشاء دور جديد: {name}")
            return role

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في إنشاء الدور: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في إنشاء الدور: {str(e)}"
            )

    async def get_role(self, role_id: str) -> Role:
        """
        الحصول على دور بواسطة المعرف

        Args:
            role_id (str): معرف الدور

        Returns:
            Role: الدور المطلوب

        Raises:
            HTTPException: في حالة عدم وجود الدور
        """
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"الدور بالمعرف {role_id} غير موجود"
            )
        return role

    async def get_role_by_name(self, name: str) -> Role:
        """
        الحصول على دور بواسطة الاسم

        Args:
            name (str): اسم الدور

        Returns:
            Role: الدور المطلوب

        Raises:
            HTTPException: في حالة عدم وجود الدور
        """
        role = self.db.query(Role).filter(Role.name == name).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"الدور بالاسم {name} غير موجود"
            )
        return role

    async def get_roles(self) -> List[Role]:
        """
        الحصول على جميع الأدوار

        Returns:
            List[Role]: قائمة الأدوار
        """
        return self.db.query(Role).all()

    async def get_organization_roles(self, organization_id: str) -> List[Role]:
        """
        الحصول على أدوار مؤسسة معينة

        Args:
            organization_id (str): معرف المؤسسة

        Returns:
            List[Role]: قائمة الأدوار
        """
        return self.db.query(Role).filter(
            Role.organization_id == organization_id).all()

    async def update_role(
            self,
            role_id: str,
            name: str = None,
            description: str = None,
            is_system_role: bool = None,
            organization_id: str = None) -> Role:
        """
        تحديث دور

        Args:
            role_id (str): معرف الدور
            name (str, optional): الاسم الجديد
            description (str, optional): الوصف الجديد
            is_system_role (bool, optional): هل هو دور نظام
            organization_id (str, optional): معرف المؤسسة

        Returns:
            Role: الدور المحدث

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            role = await self.get_role(role_id)

            # التحقق من عدم تعديل دور النظام
            if role.is_system_role and not is_system_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="لا يمكن تعديل دور النظام"
                )

            if name is not None:
                # التحقق من عدم وجود دور آخر بنفس الاسم
                existing_role = self.db.query(Role).filter(
                    Role.name == name,
                    Role.id != role_id
                ).first()

                if existing_role:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"الدور بالاسم {name} موجود بالفعل"
                    )

                role.name = name

            if description is not None:
                role.description = description

            if is_system_role is not None:
                role.is_system_role = is_system_role

            if organization_id is not None:
                role.organization_id = organization_id

            self.db.commit()
            self.db.refresh(role)

            logger.info(f"تم تحديث الدور: {role.name}")
            return role

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في تحديث الدور: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في تحديث الدور: {str(e)}"
            )

    async def delete_role(self, role_id: str) -> bool:
        """
        حذف دور

        Args:
            role_id (str): معرف الدور

        Returns:
            bool: نجاح العملية

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            role = await self.get_role(role_id)

            # التحقق من عدم حذف دور النظام
            if role.is_system_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="لا يمكن حذف دور النظام"
                )

            # التحقق من عدم ارتباط الدور بأي مستخدمين
            if role.users:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="لا يمكن حذف الدور لأنه مرتبط بمستخدمين"
                )

            self.db.delete(role)
            self.db.commit()

            logger.info(f"تم حذف الدور: {role.name}")
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في حذف الدور: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في حذف الدور: {str(e)}"
            )

    async def assign_permission_to_role(
            self,
            role_id: str,
            permission_id: str,
            assigned_by: str = None) -> bool:
        """
        تعيين صلاحية لدور

        Args:
            role_id (str): معرف الدور
            permission_id (str): معرف الصلاحية
            assigned_by (str, optional): معرف المستخدم الذي قام بالتعيين

        Returns:
            bool: نجاح العملية

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            role = await self.get_role(role_id)
            permission = await self.get_permission(permission_id)

            # التحقق من عدم وجود الصلاحية بالفعل في الدور
            if permission in role.permissions:
                return True  # الصلاحية موجودة بالفعل

            # إنشاء العلاقة بين الدور والصلاحية
            role_permission = RolePermission(
                role_id=role_id,
                permission_id=permission_id,
                assigned_by=assigned_by,
                assigned_at=datetime.utcnow()
            )

            self.db.add(role_permission)
            self.db.commit()

            logger.info(
                f"تم تعيين الصلاحية {permission.name} للدور {role.name}")
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في تعيين الصلاحية للدور: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في تعيين الصلاحية للدور: {str(e)}"
            )

    async def remove_permission_from_role(
            self, role_id: str, permission_id: str) -> bool:
        """
        إزالة صلاحية من دور

        Args:
            role_id (str): معرف الدور
            permission_id (str): معرف الصلاحية

        Returns:
            bool: نجاح العملية

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            role = await self.get_role(role_id)
            permission = await self.get_permission(permission_id)

            # التحقق من وجود الصلاحية في الدور
            if permission not in role.permissions:
                return True  # الصلاحية غير موجودة بالفعل

            # حذف العلاقة بين الدور والصلاحية
            role_permission = self.db.query(RolePermission).filter(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id
            ).first()

            if role_permission:
                self.db.delete(role_permission)
                self.db.commit()

            logger.info(
                f"تم إزالة الصلاحية {permission.name} من الدور {role.name}")
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في إزالة الصلاحية من الدور: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في إزالة الصلاحية من الدور: {str(e)}"
            )

    async def assign_role_to_user(
            self,
            user_id: str,
            role_id: str,
            assigned_by: str = None) -> bool:
        """
        تعيين دور لمستخدم

        Args:
            user_id (str): معرف المستخدم
            role_id (str): معرف الدور
            assigned_by (str, optional): معرف المستخدم الذي قام بالتعيين

        Returns:
            bool: نجاح العملية

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            role = await self.get_role(role_id)

            # التحقق من عدم وجود الدور بالفعل للمستخدم
            user_role = self.db.query(UserRole).filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id
            ).first()

            if user_role:
                return True  # الدور موجود بالفعل للمستخدم

            # إنشاء العلاقة بين المستخدم والدور
            user_role = UserRole(
                user_id=user_id,
                role_id=role_id,
                assigned_by=assigned_by,
                assigned_at=datetime.utcnow()
            )

            self.db.add(user_role)
            self.db.commit()

            logger.info(f"تم تعيين الدور {role.name} للمستخدم {user_id}")
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في تعيين الدور للمستخدم: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في تعيين الدور للمستخدم: {str(e)}"
            )

    async def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """
        إزالة دور من مستخدم

        Args:
            user_id (str): معرف المستخدم
            role_id (str): معرف الدور

        Returns:
            bool: نجاح العملية

        Raises:
            HTTPException: في حالة وجود خطأ
        """
        try:
            role = await self.get_role(role_id)

            # التحقق من وجود الدور للمستخدم
            user_role = self.db.query(UserRole).filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id
            ).first()

            if not user_role:
                return True  # الدور غير موجود بالفعل للمستخدم

            # حذف العلاقة بين المستخدم والدور
            self.db.delete(user_role)
            self.db.commit()

            logger.info(f"تم إزالة الدور {role.name} من المستخدم {user_id}")
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"خطأ في إزالة الدور من المستخدم: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"خطأ في إزالة الدور من المستخدم: {str(e)}"
            )

    async def get_user_roles(self, user_id: str) -> List[Role]:
        """
        الحصول على أدوار مستخدم

        Args:
            user_id (str): معرف المستخدم

        Returns:
            List[Role]: قائمة الأدوار
        """
        user_roles = self.db.query(UserRole).filter(
            UserRole.user_id == user_id).all()
        role_ids = [ur.role_id for ur in user_roles]

        return self.db.query(Role).filter(Role.id.in_(role_ids)).all()

    async def get_user_permissions(self, user_id: str) -> List[Permission]:
        """
        الحصول على صلاحيات مستخدم

        Args:
            user_id (str): معرف المستخدم

        Returns:
            List[Permission]: قائمة الصلاحيات
        """
        # الحصول على أدوار المستخدم
        user_roles = await self.get_user_roles(user_id)
        role_ids = [role.id for role in user_roles]

        # الحصول على صلاحيات الأدوار
        role_permissions = self.db.query(RolePermission).filter(
            RolePermission.role_id.in_(role_ids)).all()
        permission_ids = [rp.permission_id for rp in role_permissions]

        return self.db.query(Permission).filter(
            Permission.id.in_(permission_ids)).all()

    async def check_permission(
            self,
            user_id: str,
            permission: str,
            resource_id: str = None) -> bool:
        """
        التحقق من صلاحية مستخدم

        Args:
            user_id (str): معرف المستخدم
            permission (str): اسم الصلاحية
            resource_id (str, optional): معرف المورد

        Returns:
            bool: هل لديه الصلاحية
        """
        # الحصول على صلاحيات المستخدم
        user_permissions = await self.get_user_permissions(user_id)

        # التحقق من وجود الصلاحية
        for user_permission in user_permissions:
            if user_permission.name == permission:
                return True

        return False

    async def get_role_permissions(self, role_id: str) -> List[Permission]:
        """
        الحصول على صلاحيات دور

        Args:
            role_id (str): معرف الدور

        Returns:
            List[Permission]: قائمة الصلاحيات
        """
        role = await self.get_role(role_id)
        return role.permissions

    async def get_users_with_role(self, role_id: str) -> List[str]:
        """
        الحصول على معرفات المستخدمين الذين لديهم دور معين

        Args:
            role_id (str): معرف الدور

        Returns:
            List[str]: قائمة معرفات المستخدمين
        """
        user_roles = self.db.query(UserRole).filter(
            UserRole.role_id == role_id).all()
        return [ur.user_id for ur in user_roles]

    async def get_users_with_permission(self, permission_id: str) -> List[str]:
        """
        الحصول على معرفات المستخدمين الذين لديهم صلاحية معينة

        Args:
            permission_id (str): معرف الصلاحية

        Returns:
            List[str]: قائمة معرفات المستخدمين
        """
        # الحصول على الأدوار التي لديها الصلاحية
        role_permissions = self.db.query(RolePermission).filter(
            RolePermission.permission_id == permission_id).all()
        role_ids = [rp.role_id for rp in role_permissions]

        # الحصول على المستخدمين الذين لديهم هذه الأدوار
        user_roles = self.db.query(UserRole).filter(
            UserRole.role_id.in_(role_ids)).all()
        return [ur.user_id for ur in user_roles]


# دالة للحصول على خدمة الصلاحيات
def get_permission_service(db: Session = Depends(get_db)) -> PermissionService:
    """
    دالة للحصول على خدمة الصلاحيات

    Args:
        db (Session, optional): جلسة قاعدة البيانات

    Returns:
        PermissionService: خدمة الصلاحيات
    """
    return PermissionService(db)
