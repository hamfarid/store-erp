"""
Role Model
نموذج الأدوار
"""

from datetime import datetime
from database import db
import json


class Role(db.Model):
    """
    نموذج الدور
    """
    __tablename__ = "roles"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Role Info
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Permissions (JSON)
    permissions = db.Column(db.Text)  # JSON array of permission IDs or names

    # System Role
    is_system = db.Column(db.Boolean, default=False)  # الأدوار النظامية لا يمكن حذفها
    is_active = db.Column(db.Boolean, default=True)

    # Audit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))

    # Relationships - disabled to avoid mapper conflicts
    # users = db.relationship("User", secondary="user_roles", backref=db.backref("roles", lazy="dynamic"))
    # creator = db.relationship("User", foreign_keys=[created_by], backref=db.backref("created_roles", lazy="dynamic"))

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"

    def get_permissions(self):
        """الحصول على قائمة الأذونات"""
        if not self.permissions:
            return []
        
        try:
            return json.loads(self.permissions)
        except:
            return []

    def set_permissions(self, permissions_list):
        """تعيين قائمة الأذونات"""
        self.permissions = json.dumps(permissions_list)

    def has_permission(self, permission_name):
        """
        التحقق من وجود إذن معين
        
        Args:
            permission_name: اسم الإذن (مثال: 'products.create')
        
        Returns:
            bool: True إذا كان الدور يملك الإذن
        """
        perms = self.get_permissions()
        
        # التحقق المباشر
        if permission_name in perms:
            return True
        
        # التحقق من الإذن الشامل (مثال: 'products.*')
        resource = permission_name.split('.')[0]
        if f"{resource}.*" in perms:
            return True
        
        # التحقق من الإذن الكامل
        if "*" in perms or "all" in perms:
            return True
        
        return False

    def grant(self, permission_name):
        """
        منح إذن للدور
        
        Args:
            permission_name: اسم الإذن
        
        Returns:
            bool: نجاح العملية
        """
        perms = self.get_permissions()
        
        if permission_name not in perms:
            perms.append(permission_name)
            self.set_permissions(perms)
            db.session.commit()
            return True
        
        return False

    def revoke(self, permission_name):
        """
        سحب إذن من الدور
        
        Args:
            permission_name: اسم الإذن
        
        Returns:
            bool: نجاح العملية
        """
        perms = self.get_permissions()
        
        if permission_name in perms:
            perms.remove(permission_name)
            self.set_permissions(perms)
            db.session.commit()
            return True
        
        return False

    def grant_multiple(self, permission_names):
        """منح عدة أذونات"""
        perms = self.get_permissions()
        updated = False
        
        for perm_name in permission_names:
            if perm_name not in perms:
                perms.append(perm_name)
                updated = True
        
        if updated:
            self.set_permissions(perms)
            db.session.commit()
        
        return updated

    def revoke_multiple(self, permission_names):
        """سحب عدة أذونات"""
        perms = self.get_permissions()
        updated = False
        
        for perm_name in permission_names:
            if perm_name in perms:
                perms.remove(perm_name)
                updated = True
        
        if updated:
            self.set_permissions(perms)
            db.session.commit()
        
        return updated

    def get_users(self):
        """الحصول على قائمة المستخدمين الذين لديهم هذا الدور"""
        return self.users

    def get_users_count(self):
        """عدد المستخدمين الذين لديهم هذا الدور"""
        return len(self.users)

    def to_dict(self, include_users=False):
        """تحويل إلى Dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'permissions': self.get_permissions(),
            'is_system': self.is_system,
            'is_active': self.is_active,
            'users_count': self.get_users_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }
        
        if include_users:
            data['users'] = [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
                for user in self.users
            ]
        
        return data


# جدول الربط بين المستخدمين والأدوار
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow),
    db.Column('assigned_by', db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
)
