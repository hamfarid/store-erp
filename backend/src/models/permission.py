"""
Permission Model
نموذج الأذونات
"""

from datetime import datetime
from database import db


class Permission(db.Model):
    """
    نموذج الإذن
    """
    __tablename__ = "permissions"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Permission Info
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)  # مثال: products.create
    display_name = db.Column(db.String(150), nullable=False)  # مثال: إنشاء منتج
    description = db.Column(db.Text)

    # Resource and Action
    resource = db.Column(db.String(50), nullable=False, index=True)  # مثال: products
    action = db.Column(db.String(50), nullable=False, index=True)    # مثال: create, read, update, delete

    # Category
    category = db.Column(db.String(50), index=True)  # مثال: inventory, sales, reports

    # System Permission
    is_system = db.Column(db.Boolean, default=False)  # الأذونات النظامية لا يمكن حذفها
    is_active = db.Column(db.Boolean, default=True)

    # Audit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}')>"

    @staticmethod
    def check(user, resource, action):
        """
        التحقق من إذن المستخدم

        Args:
            user: المستخدم
            resource: المورد (مثال: 'products')
            action: الإجراء (مثال: 'create')

        Returns:
            bool: True إذا كان المستخدم لديه الإذن
        """
        if not user:
            return False

        # المسؤول الكامل
        if user.is_superuser:
            return True

        # التحقق من الأدوار
        permission_name = f"{resource}.{action}"

        for role in user.roles:
            if role.has_permission(permission_name):
                return True

        return False

    @staticmethod
    def validate(permission_name):
        """
        التحقق من صحة اسم الإذن

        Args:
            permission_name: اسم الإذن (مثال: 'products.create')

        Returns:
            tuple: (valid, error_message)
        """
        if not permission_name:
            return False, "اسم الإذن مطلوب"

        parts = permission_name.split('.')
        if len(parts) != 2:
            return False, "تنسيق الإذن غير صحيح (يجب أن يكون: resource.action)"

        resource, action = parts

        if not resource or not action:
            return False, "المورد والإجراء مطلوبان"

        # التحقق من الأحرف المسموحة
        allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789_-*')
        if not all(c in allowed_chars for c in resource.lower()):
            return False, "المورد يحتوي على أحرف غير مسموحة"

        if not all(c in allowed_chars for c in action.lower()):
            return False, "الإجراء يحتوي على أحرف غير مسموحة"

        return True, None

    @staticmethod
    def create_permission(name, display_name, description=None, category=None):
        """
        إنشاء إذن جديد

        Args:
            name: اسم الإذن (مثال: 'products.create')
            display_name: الاسم المعروض
            description: الوصف
            category: الفئة

        Returns:
            Permission: الإذن المنشأ
        """
        # التحقق من الصحة
        valid, error = Permission.validate(name)
        if not valid:
            raise ValueError(error)

        # استخراج المورد والإجراء
        resource, action = name.split('.')

        # التحقق من عدم التكرار
        existing = Permission.query.filter_by(name=name).first()
        if existing:
            raise ValueError(f"الإذن '{name}' موجود بالفعل")

        # إنشاء الإذن
        permission = Permission(
            name=name,
            display_name=display_name,
            description=description,
            resource=resource,
            action=action,
            category=category
        )

        db.session.add(permission)
        db.session.commit()

        return permission

    def to_dict(self):
        """تحويل إلى Dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'resource': self.resource,
            'action': self.action,
            'category': self.category,
            'is_system': self.is_system,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
