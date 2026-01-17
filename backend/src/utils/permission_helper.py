"""
Permission Helper Functions
دوال مساعدة لنظام الأذونات
"""

from database import db
from models.permission import Permission
from models.role import Role


# قائمة جميع الأذونات في النظام
PERMISSIONS = {
    # المنتجات
    'products': {
        'create': 'إنشاء منتج',
        'read': 'عرض المنتجات',
        'update': 'تعديل منتج',
        'delete': 'حذف منتج',
        'import': 'استيراد منتجات',
        'export': 'تصدير منتجات'
    },
    
    # اللوطات
    'batches': {
        'create': 'إنشاء لوط',
        'read': 'عرض اللوطات',
        'update': 'تعديل لوط',
        'delete': 'حذف لوط',
        'quality_test': 'فحص جودة',
        'ministry_approval': 'موافقة وزارة'
    },
    
    # المبيعات
    'sales': {
        'create': 'إنشاء فاتورة بيع',
        'read': 'عرض المبيعات',
        'update': 'تعديل فاتورة',
        'delete': 'حذف فاتورة',
        'approve': 'اعتماد فاتورة',
        'cancel': 'إلغاء فاتورة'
    },
    
    # المشتريات
    'purchases': {
        'create': 'إنشاء أمر شراء',
        'read': 'عرض المشتريات',
        'update': 'تعديل أمر شراء',
        'delete': 'حذف أمر شراء',
        'approve': 'اعتماد أمر شراء',
        'receive': 'استلام أمر شراء'
    },
    
    # نقطة البيع
    'pos': {
        'access': 'الوصول لنقطة البيع',
        'open_session': 'فتح جلسة',
        'close_session': 'إغلاق جلسة',
        'refund': 'استرجاع'
    },
    
    # العملاء
    'customers': {
        'create': 'إنشاء عميل',
        'read': 'عرض العملاء',
        'update': 'تعديل عميل',
        'delete': 'حذف عميل'
    },
    
    # الموردين
    'suppliers': {
        'create': 'إنشاء مورد',
        'read': 'عرض الموردين',
        'update': 'تعديل مورد',
        'delete': 'حذف مورد'
    },
    
    # المخازن
    'warehouses': {
        'create': 'إنشاء مخزن',
        'read': 'عرض المخازن',
        'update': 'تعديل مخزن',
        'delete': 'حذف مخزن',
        'transfer': 'نقل بين المخازن'
    },
    
    # التقارير
    'reports': {
        'sales': 'تقارير المبيعات',
        'purchases': 'تقارير المشتريات',
        'inventory': 'تقارير المخزون',
        'financial': 'تقارير مالية',
        'custom': 'تقارير مخصصة',
        'export': 'تصدير تقارير'
    },
    
    # المستخدمين
    'users': {
        'create': 'إنشاء مستخدم',
        'read': 'عرض المستخدمين',
        'update': 'تعديل مستخدم',
        'delete': 'حذف مستخدم',
        'reset_password': 'إعادة تعيين كلمة المرور'
    },
    
    # الأدوار والأذونات
    'roles': {
        'create': 'إنشاء دور',
        'read': 'عرض الأدوار',
        'update': 'تعديل دور',
        'delete': 'حذف دور',
        'assign': 'تعيين دور'
    },
    
    # الإعدادات
    'settings': {
        'read': 'عرض الإعدادات',
        'update': 'تعديل الإعدادات',
        'backup': 'النسخ الاحتياطي',
        'restore': 'الاستعادة'
    },
    
    # الجودة
    'quality': {
        'create_test': 'إنشاء فحص جودة',
        'read_tests': 'عرض فحوصات الجودة',
        'approve_test': 'اعتماد فحص',
        'reject_test': 'رفض فحص'
    }
}


# الأدوار الافتراضية
ROLES = {
    'superadmin': {
        'display_name': 'مسؤول النظام',
        'description': 'صلاحيات كاملة على النظام',
        'permissions': ['*'],  # جميع الأذونات
        'is_system': True
    },
    
    'admin': {
        'display_name': 'مدير',
        'description': 'صلاحيات إدارية',
        'permissions': [
            'products.*', 'batches.*', 'sales.*', 'purchases.*',
            'customers.*', 'suppliers.*', 'warehouses.*',
            'reports.*', 'users.read', 'users.create', 'users.update'
        ],
        'is_system': True
    },
    
    'manager': {
        'display_name': 'مدير فرع',
        'description': 'إدارة الفرع والعمليات اليومية',
        'permissions': [
            'products.read', 'products.update',
            'batches.read', 'batches.update',
            'sales.*', 'purchases.read', 'purchases.create',
            'customers.*', 'pos.*',
            'reports.sales', 'reports.inventory'
        ],
        'is_system': True
    },
    
    'cashier': {
        'display_name': 'كاشير',
        'description': 'نقطة البيع والعمليات البسيطة',
        'permissions': [
            'products.read',
            'batches.read',
            'sales.create', 'sales.read',
            'customers.read', 'customers.create',
            'pos.access', 'pos.open_session', 'pos.close_session'
        ],
        'is_system': True
    },
    
    'warehouse_keeper': {
        'display_name': 'أمين مخزن',
        'description': 'إدارة المخزون واللوطات',
        'permissions': [
            'products.read', 'products.update',
            'batches.*',
            'purchases.read', 'purchases.receive',
            'warehouses.read', 'warehouses.transfer',
            'quality.create_test', 'quality.read_tests',
            'reports.inventory'
        ],
        'is_system': True
    },
    
    'accountant': {
        'display_name': 'محاسب',
        'description': 'العمليات المالية والتقارير',
        'permissions': [
            'sales.read', 'sales.approve',
            'purchases.read', 'purchases.approve',
            'customers.read',
            'suppliers.read',
            'reports.sales', 'reports.purchases', 'reports.financial'
        ],
        'is_system': True
    },
    
    'viewer': {
        'display_name': 'مشاهد',
        'description': 'عرض فقط بدون تعديل',
        'permissions': [
            'products.read',
            'batches.read',
            'sales.read',
            'purchases.read',
            'customers.read',
            'suppliers.read',
            'warehouses.read',
            'reports.sales', 'reports.inventory'
        ],
        'is_system': True
    }
}


def seed_permissions():
    """
    إنشاء الأذونات الافتراضية
    
    Returns:
        int: عدد الأذونات المنشأة
    """
    count = 0
    
    for resource, actions in PERMISSIONS.items():
        for action, display_name in actions.items():
            permission_name = f"{resource}.{action}"
            
            # التحقق من عدم التكرار
            existing = Permission.query.filter_by(name=permission_name).first()
            if existing:
                continue
            
            # إنشاء الإذن
            permission = Permission(
                name=permission_name,
                display_name=display_name,
                description=f"إذن {display_name} في {resource}",
                resource=resource,
                action=action,
                category=get_category(resource),
                is_system=True
            )
            
            db.session.add(permission)
            count += 1
    
    db.session.commit()
    return count


def seed_roles():
    """
    إنشاء الأدوار الافتراضية
    
    Returns:
        int: عدد الأدوار المنشأة
    """
    count = 0
    
    for role_name, role_data in ROLES.items():
        # التحقق من عدم التكرار
        existing = Role.query.filter_by(name=role_name).first()
        if existing:
            continue
        
        # إنشاء الدور
        role = Role(
            name=role_name,
            display_name=role_data['display_name'],
            description=role_data['description'],
            is_system=role_data.get('is_system', False)
        )
        
        role.set_permissions(role_data['permissions'])
        
        db.session.add(role)
        count += 1
    
    db.session.commit()
    return count


def get_category(resource):
    """
    الحصول على فئة المورد
    
    Args:
        resource: اسم المورد
    
    Returns:
        str: الفئة
    """
    categories = {
        'products': 'inventory',
        'batches': 'inventory',
        'warehouses': 'inventory',
        'sales': 'sales',
        'pos': 'sales',
        'customers': 'sales',
        'purchases': 'purchases',
        'suppliers': 'purchases',
        'reports': 'reports',
        'users': 'admin',
        'roles': 'admin',
        'settings': 'admin',
        'quality': 'quality'
    }
    
    return categories.get(resource, 'other')


def check_user_permission(user_id, resource, action):
    """
    التحقق من إذن المستخدم
    
    Args:
        user_id: معرف المستخدم
        resource: المورد
        action: الإجراء
    
    Returns:
        bool: True إذا كان المستخدم لديه الإذن
    """
    from src.models.user import User
    
    user = User.query.get(user_id)
    if not user:
        return False
    
    return Permission.check(user, resource, action)


def get_user_roles(user_id):
    """
    الحصول على أدوار المستخدم
    
    Args:
        user_id: معرف المستخدم
    
    Returns:
        list: قائمة الأدوار
    """
    from src.models.user import User
    
    user = User.query.get(user_id)
    if not user:
        return []
    
    return [role.to_dict() for role in user.roles]


def get_role_permissions(role_id):
    """
    الحصول على أذونات الدور
    
    Args:
        role_id: معرف الدور
    
    Returns:
        list: قائمة الأذونات
    """
    role = Role.query.get(role_id)
    if not role:
        return []
    
    return role.get_permissions()


def get_all_permissions_grouped():
    """
    الحصول على جميع الأذونات مجمعة حسب المورد
    
    Returns:
        dict: الأذونات المجمعة
    """
    result = {}
    
    for resource, actions in PERMISSIONS.items():
        result[resource] = {
            'name': resource,
            'display_name': get_resource_display_name(resource),
            'category': get_category(resource),
            'permissions': []
        }
        
        for action, display_name in actions.items():
            result[resource]['permissions'].append({
                'name': f"{resource}.{action}",
                'action': action,
                'display_name': display_name
            })
    
    return result


def get_resource_display_name(resource):
    """
    الحصول على الاسم المعروض للمورد
    
    Args:
        resource: اسم المورد
    
    Returns:
        str: الاسم المعروض
    """
    names = {
        'products': 'المنتجات',
        'batches': 'اللوطات',
        'sales': 'المبيعات',
        'purchases': 'المشتريات',
        'pos': 'نقطة البيع',
        'customers': 'العملاء',
        'suppliers': 'الموردين',
        'warehouses': 'المخازن',
        'reports': 'التقارير',
        'users': 'المستخدمين',
        'roles': 'الأدوار',
        'settings': 'الإعدادات',
        'quality': 'الجودة'
    }
    
    return names.get(resource, resource)
