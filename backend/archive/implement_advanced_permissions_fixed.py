#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لتطبيق نظام صلاحيات أكثر تفصيلاً
"""

import os
import json
import sqlite3
from datetime import datetime

def create_permissions_database_tables():
    """إنشاء جداول نظام الصلاحيات في قاعدة البيانات"""
    
    try:
        conn = sqlite3.connect('backend/instance/inventory.db')
        cursor = conn.cursor()
        
        # جدول الأدوار
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) UNIQUE NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول صلاحيات الأدوار
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS role_permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_id INTEGER NOT NULL,
                permission_name VARCHAR(100) NOT NULL,
                can_create BOOLEAN DEFAULT 0,
                can_read BOOLEAN DEFAULT 1,
                can_update BOOLEAN DEFAULT 0,
                can_delete BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
                UNIQUE(role_id, permission_name)
            )
        ''')
        
        # جدول ربط المستخدمين بالأدوار (إذا لم يكن موجوداً)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE CASCADE,
                UNIQUE(user_id, role_id)
            )
        ''')
        
        # إنشاء أدوار افتراضية
        default_roles = [
            ('admin', 'مدير النظام - صلاحيات كاملة'),
            ('manager', 'مدير - صلاحيات إدارية محدودة'),
            ('employee', 'موظف - صلاحيات أساسية'),
            ('viewer', 'مشاهد - صلاحيات قراءة فقط')
        ]
        
        for role_name, role_desc in default_roles:
            cursor.execute('''
                INSERT OR IGNORE INTO roles (name, description)
                VALUES (?, ?)
            ''', (role_name, role_desc))
        
        # إضافة صلاحيات افتراضية لدور المدير
        admin_permissions = [
            'products', 'categories', 'inventory', 'warehouses',
            'customers', 'suppliers', 'invoices', 'reports',
            'users', 'settings', 'permissions'
        ]
        
        # الحصول على معرف دور المدير
        cursor.execute('SELECT id FROM roles WHERE name = ?', ('admin',))
        admin_role = cursor.fetchone()
        
        if admin_role:
            admin_role_id = admin_role[0]
            for permission in admin_permissions:
                cursor.execute('''
                    INSERT OR IGNORE INTO role_permissions 
                    (role_id, permission_name, can_create, can_read, can_update, can_delete)
                    VALUES (?, ?, 1, 1, 1, 1)
                ''', (admin_role_id, permission))
        
        conn.commit()
        conn.close()
        
        print("   ✅ تم إنشاء جداول نظام الصلاحيات")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في إنشاء جداول الصلاحيات: {e}")
        return False

def create_advanced_permissions_backend():
    """إنشاء نظام الصلاحيات المتقدم في الخادم الخلفي"""
    
    permissions_code = '''
# نظام الصلاحيات المتقدم
@app.route('/api/permissions/roles', methods=['GET'])
def get_roles():
    """جلب جميع الأدوار"""
    try:
        conn = sqlite3.connect('instance/inventory.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, description, is_active, created_at FROM roles ORDER BY name")
        
        roles = []
        for row in cursor.fetchall():
            roles.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'is_active': bool(row[3]),
                'created_at': row[4]
            })
        
        conn.close()
        return jsonify({'success': True, 'data': roles})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/permissions/roles', methods=['POST'])
def create_role():
    """إنشاء دور جديد"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        permissions = data.get('permissions', [])
        
        if not name:
            return jsonify({'success': False, 'error': 'اسم الدور مطلوب'}), 400
        
        conn = sqlite3.connect('instance/inventory.db')
        cursor = conn.cursor()
        
        # إنشاء الدور
        cursor.execute("INSERT INTO roles (name, description, is_active, created_at) VALUES (?, ?, 1, ?)",
                      (name, description, datetime.now().isoformat()))
        
        role_id = cursor.lastrowid
        
        # إضافة الصلاحيات للدور
        for permission in permissions:
            cursor.execute("""INSERT INTO role_permissions 
                             (role_id, permission_name, can_create, can_read, can_update, can_delete)
                             VALUES (?, ?, ?, ?, ?, ?)""",
                          (role_id, permission['name'], 
                           permission.get('can_create', False),
                           permission.get('can_read', True),
                           permission.get('can_update', False),
                           permission.get('can_delete', False)))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'تم إنشاء الدور بنجاح', 'role_id': role_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/permissions/check', methods=['POST'])
def check_permission():
    """فحص صلاحية مستخدم لعملية معينة"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        permission_name = data.get('permission_name')
        action = data.get('action', 'read')  # create, read, update, delete
        
        if not user_id or not permission_name:
            return jsonify({'success': False, 'error': 'معرف المستخدم واسم الصلاحية مطلوبان'}), 400
        
        conn = sqlite3.connect('instance/inventory.db')
        cursor = conn.cursor()
        
        # التحقق من كون المستخدم مدير
        cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
        user_role = cursor.fetchone()
        
        if user_role and user_role[0] == 'admin':
            conn.close()
            return jsonify({'success': True, 'has_permission': True, 'reason': 'مدير النظام'})
        
        # فحص الصلاحيات التفصيلية
        action_column = f'can_{action}'
        query = f"""SELECT rp.{action_column}
                   FROM user_roles ur
                   JOIN role_permissions rp ON ur.role_id = rp.role_id
                   WHERE ur.user_id = ? AND rp.permission_name = ?"""
        
        cursor.execute(query, (user_id, permission_name))
        
        result = cursor.fetchone()
        has_permission = bool(result[0]) if result else False
        
        conn.close()
        return jsonify({'success': True, 'has_permission': has_permission})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/permissions/available', methods=['GET'])
def get_available_permissions():
    """جلب جميع الصلاحيات المتاحة في النظام"""
    try:
        available_permissions = [
            {'name': 'products', 'display_name': 'إدارة المنتجات', 'category': 'المخزون'},
            {'name': 'categories', 'display_name': 'إدارة الفئات', 'category': 'المخزون'},
            {'name': 'inventory', 'display_name': 'إدارة المخزون', 'category': 'المخزون'},
            {'name': 'warehouses', 'display_name': 'إدارة المخازن', 'category': 'المخزون'},
            {'name': 'customers', 'display_name': 'إدارة العملاء', 'category': 'العلاقات'},
            {'name': 'suppliers', 'display_name': 'إدارة الموردين', 'category': 'العلاقات'},
            {'name': 'invoices', 'display_name': 'إدارة الفواتير', 'category': 'المبيعات'},
            {'name': 'reports', 'display_name': 'التقارير', 'category': 'التقارير'},
            {'name': 'users', 'display_name': 'إدارة المستخدمين', 'category': 'الإدارة'},
            {'name': 'settings', 'display_name': 'إعدادات النظام', 'category': 'الإدارة'},
            {'name': 'permissions', 'display_name': 'إدارة الصلاحيات', 'category': 'الإدارة'},
        ]
        
        return jsonify({'success': True, 'data': available_permissions})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
'''
    
    # قراءة الخادم الحالي وإضافة نظام الصلاحيات
    backend_file = 'backend/minimal_working_app.py'
    
    try:
        with open(backend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # إضافة نظام الصلاحيات قبل السطر الأخير
        if "if __name__ == '__main__':" in content:
            content = content.replace("if __name__ == '__main__':", permissions_code + "\n\nif __name__ == '__main__':")
        else:
            content += "\n\n" + permissions_code
        
        with open(backend_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ تم إضافة نظام الصلاحيات المتقدم")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في إضافة نظام الصلاحيات: {e}")
        return False

def create_permissions_frontend_components():
    """إنشاء مكونات إدارة الصلاحيات في الواجهة الأمامية"""
    
    # مكون إدارة الأدوار
    roles_management_component = '''import React, { useState, useEffect } from 'react';

const RolesManagement = () => {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newRole, setNewRole] = useState({ name: '', description: '' });

  useEffect(() => {
    fetchRoles();
  }, []);

  const fetchRoles = async () => {
    try {
      const response = await fetch('http://localhost:5002/api/permissions/roles');
      const result = await response.json();
      if (result.success) {
        setRoles(result.data);
      }
    } catch (error) {
      console.error('خطأ في جلب الأدوار:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRole = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5002/api/permissions/roles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRole),
      });
      
      const result = await response.json();
      if (result.success) {
        setShowCreateModal(false);
        setNewRole({ name: '', description: '' });
        fetchRoles();
        alert('تم إنشاء الدور بنجاح');
      } else {
        alert('خطأ: ' + result.error);
      }
    } catch (error) {
      console.error('خطأ في إنشاء الدور:', error);
      alert('حدث خطأ في إنشاء الدور');
    }
  };

  if (loading) {
    return <div className="text-center p-8">جاري تحميل الأدوار...</div>;
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">إدارة الأدوار والصلاحيات</h2>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg"
        >
          إضافة دور جديد
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                اسم الدور
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                الوصف
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                الحالة
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                تاريخ الإنشاء
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {roles.map((role) => (
              <tr key={role.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {role.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {role.description}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    role.is_active 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {role.is_active ? 'نشط' : 'غير نشط'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(role.created_at).toLocaleDateString('ar-SA')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">إنشاء دور جديد</h3>
              <form onSubmit={handleCreateRole}>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    اسم الدور
                  </label>
                  <input
                    type="text"
                    value={newRole.name}
                    onChange={(e) => setNewRole({...newRole, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    الوصف
                  </label>
                  <textarea
                    value={newRole.description}
                    onChange={(e) => setNewRole({...newRole, description: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="3"
                  />
                </div>
                <div className="flex justify-end space-x-2">
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    إلغاء
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                  >
                    إنشاء
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RolesManagement;'''

    # إنشاء المجلدات والملفات
    permissions_dir = 'frontend/src/components/permissions'
    os.makedirs(permissions_dir, exist_ok=True)
    
    try:
        # كتابة مكون إدارة الأدوار
        with open(f'{permissions_dir}/RolesManagement.jsx', 'w', encoding='utf-8') as f:
            f.write(roles_management_component)
        
        print("   ✅ تم إنشاء مكونات إدارة الصلاحيات")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في إنشاء مكونات الصلاحيات: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔐 بدء تطبيق نظام الصلاحيات المتقدم...")
    print("=" * 50)
    
    success_count = 0
    total_tasks = 3
    
    # إنشاء جداول قاعدة البيانات
    print("🗄️  إنشاء جداول نظام الصلاحيات...")
    if create_permissions_database_tables():
        success_count += 1
    
    # إضافة نظام الصلاحيات في الخادم الخلفي
    print("🔧 إضافة نظام الصلاحيات في الخادم الخلفي...")
    if create_advanced_permissions_backend():
        success_count += 1
    
    # إنشاء مكونات الصلاحيات في الواجهة الأمامية
    print("🎨 إنشاء مكونات إدارة الصلاحيات...")
    if create_permissions_frontend_components():
        success_count += 1
    
    print("=" * 50)
    if success_count == total_tasks:
        print("✅ تم تطبيق نظام الصلاحيات المتقدم بنجاح!")
        print("الميزات المضافة:")
        print("  🔐 إدارة الأدوار والصلاحيات")
        print("  👥 تعيين الأدوار للمستخدمين")
        print("  🔍 فحص الصلاحيات التفصيلية")
        print("  📊 واجهات إدارة متقدمة")
    else:
        print(f"⚠️  تم إكمال {success_count} من {total_tasks} مهام بنجاح")
        print("يرجى مراجعة الأخطاء أعلاه")

if __name__ == "__main__":
    main()
