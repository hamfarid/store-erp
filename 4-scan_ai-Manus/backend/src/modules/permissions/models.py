"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/permissions/models.py

نماذج وحدة الصلاحيات في نظام Gaara ERP
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ...database import Base, BaseModel

# جدول العلاقة بين الأدوار والصلاحيات
role_permission = Table(
    'role_permission',
    Base.metadata,
    Column(
        'role_id',
        String(36),
        ForeignKey('roles.id'),
        primary_key=True),
    Column(
        'permission_id',
        String(36),
        ForeignKey('permissions.id'),
        primary_key=True))

# جدول العلاقة بين المستخدمين والأدوار
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('role_id', String(36), ForeignKey('roles.id'), primary_key=True)
)


class Permission(Base, BaseModel):
    """
    نموذج الصلاحية في النظام
    """
    __tablename__ = 'permissions'

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    # نوع المورد (مثل: user, product, invoice)
    resource_type = Column(String(50), nullable=False)
    # الإجراء (مثل: create, read, update, delete)
    action = Column(String(50), nullable=False)

    # العلاقات
    roles = relationship(
        "Role",
        secondary=role_permission,
        back_populates="permissions")

    def __repr__(self):
        return f"<Permission {self.name}>"


class Role(Base, BaseModel):
    """
    نموذج الدور في النظام
    """
    __tablename__ = 'roles'

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    # هل هو دور نظام (لا يمكن تعديله)
    is_system_role = Column(Boolean, default=False)
    organization_id = Column(
        String(36),
        ForeignKey('organizations.id'),
        nullable=True)

    # العلاقات
    permissions = relationship(
        "Permission",
        secondary=role_permission,
        back_populates="roles")
    users = relationship("User", secondary=user_role, back_populates="roles")
    organization = relationship("Organization", back_populates="roles")

    def __repr__(self):
        return f"<Role {self.name}>"


class UserRole(Base):
    """
    نموذج العلاقة بين المستخدم والدور
    """
    __tablename__ = 'user_role'

    user_id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    role_id = Column(String(36), ForeignKey('roles.id'), primary_key=True)
    assigned_by = Column(String(36), ForeignKey('users.id'), nullable=True)
    assigned_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"


class RolePermission(Base):
    """
    نموذج العلاقة بين الدور والصلاحية
    """
    __tablename__ = 'role_permission'

    role_id = Column(String(36), ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(
        String(36),
        ForeignKey('permissions.id'),
        primary_key=True)
    assigned_by = Column(String(36), ForeignKey('users.id'), nullable=True)
    assigned_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<RolePermission role_id={self.role_id} permission_id={self.permission_id}>"
