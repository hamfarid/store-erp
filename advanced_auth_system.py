#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 نظام المصادقة المتقدم
Advanced Authentication System

نظام مصادقة شامل يدعم:
- تسجيل الدخول والخروج
- إدارة الجلسات
- الأدوار والصلاحيات
- حماية نقاط النهاية
"""

import hashlib
import secrets
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session, g

class AdvancedAuthSystem:
    def __init__(self, db_path='instance/inventory.db'):
        self.db_path = db_path
        self.init_auth_tables()
    
    def init_auth_tables(self):
        """تهيئة جداول المصادقة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الجلسات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # جدول الأدوار
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                permissions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول ربط المستخدمين بالأدوار
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                assigned_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (role_id) REFERENCES roles (id),
                FOREIGN KEY (assigned_by) REFERENCES users (id),
                UNIQUE(user_id, role_id)
            )
        ''')
        
        # إنشاء الأدوار الأساسية
        default_roles = [
            ('admin', 'مدير النظام', 'all'),
            ('manager', 'مدير', 'read,write,manage_inventory,view_reports'),
            ('employee', 'موظف', 'read,write'),
            ('viewer', 'مشاهد', 'read')
        ]
        
        for role_name, description, permissions in default_roles:
            cursor.execute('''
                INSERT OR IGNORE INTO roles (name, description, permissions)
                VALUES (?, ?, ?)
            ''', (role_name, description, permissions))
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """تشفير كلمة المرور"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return salt + password_hash.hex()
    
    def verify_password(self, password, stored_hash):
        """التحقق من كلمة المرور"""
        try:
            salt = stored_hash[:32]
            stored_password_hash = stored_hash[32:]
            password_hash = hashlib.pbkdf2_hmac('sha256',
                                              password.encode('utf-8'),
                                              salt.encode('utf-8'),
                                              100000)
            return password_hash.hex() == stored_password_hash
        except:
            return False
    
    def create_user(self, username, password, email, full_name, role='employee'):
        """إنشاء مستخدم جديد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # التحقق من عدم وجود المستخدم
            cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                         (username, email))
            if cursor.fetchone():
                return {'success': False, 'error': 'المستخدم موجود بالفعل'}
            
            # تشفير كلمة المرور
            password_hash = self.hash_password(password)
            
            # إنشاء المستخدم
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, full_name, is_active, created_at)
                VALUES (?, ?, ?, ?, 1, ?)
            ''', (username, password_hash, email, full_name, datetime.now()))
            
            user_id = cursor.lastrowid
            
            # تعيين الدور
            cursor.execute('SELECT id FROM roles WHERE name = ?', (role,))
            role_row = cursor.fetchone()
            if role_row:
                cursor.execute('''
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (?, ?)
                ''', (user_id, role_row[0]))
            
            conn.commit()
            return {'success': True, 'user_id': user_id}
            
        except Exception as e:
            conn.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            conn.close()
    
    def authenticate_user(self, username, password):
        """مصادقة المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # البحث عن المستخدم
            cursor.execute('''
                SELECT id, username, password_hash, email, full_name, is_active
                FROM users 
                WHERE username = ? OR email = ?
            ''', (username, username))
            
            user = cursor.fetchone()
            if not user:
                return {'success': False, 'error': 'بيانات تسجيل الدخول غير صحيحة'}
            
            user_id, username, password_hash, email, full_name, is_active = user
            
            if not is_active:
                return {'success': False, 'error': 'الحساب معطل'}
            
            # التحقق من كلمة المرور
            if not self.verify_password(password, password_hash):
                return {'success': False, 'error': 'بيانات تسجيل الدخول غير صحيحة'}
            
            # الحصول على أدوار المستخدم
            cursor.execute('''
                SELECT r.name, r.permissions
                FROM roles r
                JOIN user_roles ur ON r.id = ur.role_id
                WHERE ur.user_id = ?
            ''', (user_id,))
            
            roles = cursor.fetchall()
            permissions = set()
            role_names = []
            
            for role_name, role_permissions in roles:
                role_names.append(role_name)
                if role_permissions:
                    permissions.update(role_permissions.split(','))
            
            # إنشاء جلسة
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)
            
            cursor.execute('''
                INSERT INTO user_sessions (user_id, session_token, expires_at, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, session_token, expires_at, 
                  request.remote_addr if request else None,
                  request.headers.get('User-Agent') if request else None))
            
            conn.commit()
            
            return {
                'success': True,
                'user': {
                    'id': user_id,
                    'username': username,
                    'email': email,
                    'full_name': full_name,
                    'roles': role_names,
                    'permissions': list(permissions)
                },
                'session_token': session_token,
                'expires_at': expires_at.isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            conn.close()
    
    def validate_session(self, session_token):
        """التحقق من صحة الجلسة"""
        if not session_token:
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT s.user_id, s.expires_at, u.username, u.email, u.full_name, u.is_active
                FROM user_sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.session_token = ? AND s.is_active = 1
            ''', (session_token,))
            
            session_data = cursor.fetchone()
            if not session_data:
                return None
            
            user_id, expires_at, username, email, full_name, is_active = session_data
            
            # التحقق من انتهاء الجلسة
            if datetime.fromisoformat(expires_at) < datetime.now():
                # إلغاء الجلسة المنتهية
                cursor.execute('''
                    UPDATE user_sessions SET is_active = 0 
                    WHERE session_token = ?
                ''', (session_token,))
                conn.commit()
                return None
            
            if not is_active:
                return None
            
            # الحصول على الأدوار والصلاحيات
            cursor.execute('''
                SELECT r.name, r.permissions
                FROM roles r
                JOIN user_roles ur ON r.id = ur.role_id
                WHERE ur.user_id = ?
            ''', (user_id,))
            
            roles = cursor.fetchall()
            permissions = set()
            role_names = []
            
            for role_name, role_permissions in roles:
                role_names.append(role_name)
                if role_permissions:
                    permissions.update(role_permissions.split(','))
            
            return {
                'id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name,
                'roles': role_names,
                'permissions': list(permissions)
            }
            
        except Exception:
            return None
        finally:
            conn.close()
    
    def logout_user(self, session_token):
        """تسجيل خروج المستخدم"""
        if not session_token:
            return {'success': False, 'error': 'لا توجد جلسة نشطة'}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE user_sessions SET is_active = 0 
                WHERE session_token = ?
            ''', (session_token,))
            
            conn.commit()
            return {'success': True, 'message': 'تم تسجيل الخروج بنجاح'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            conn.close()
    
    def require_auth(self, required_permission=None):
        """ديكوريتر للتحقق من المصادقة والصلاحيات"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # الحصول على رمز الجلسة
                session_token = None
                
                # البحث في الهيدر
                auth_header = request.headers.get('Authorization')
                if auth_header and auth_header.startswith('Bearer '):
                    session_token = auth_header[7:]
                
                # البحث في الكوكيز
                if not session_token:
                    session_token = request.cookies.get('session_token')
                
                # التحقق من الجلسة
                user = self.validate_session(session_token)
                if not user:
                    return jsonify({
                        'success': False,
                        'error': 'غير مصرح لك بالوصول'
                    }), 401
                
                # التحقق من الصلاحية المطلوبة
                if required_permission:
                    if (required_permission not in user['permissions'] and 
                        'all' not in user['permissions']):
                        return jsonify({
                            'success': False,
                            'error': 'ليس لديك صلاحية للقيام بهذا الإجراء'
                        }), 403
                
                # إضافة بيانات المستخدم للطلب
                g.current_user = user
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator

# إنشاء مثيل عام للنظام
auth_system = AdvancedAuthSystem()

# ديكوريتر سهل الاستخدام
def require_auth(permission=None):
    return auth_system.require_auth(permission)

def require_admin():
    return auth_system.require_auth('all')

def require_manager():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = getattr(g, 'current_user', None)
            if not user or ('admin' not in user['roles'] and 'manager' not in user['roles']):
                return jsonify({
                    'success': False,
                    'error': 'يتطلب صلاحيات إدارية'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
