#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت لإضافة نظام النسخ الاحتياطي التلقائي
"""

import os
import json
import sqlite3
from datetime import datetime

def create_backup_system_backend():
    """إنشاء نظام النسخ الاحتياطي في الخادم الخلفي"""
    
    backup_code = '''
import shutil
import zipfile
import schedule
import threading
import time
from pathlib import Path

# نظام النسخ الاحتياطي التلقائي
backup_settings = {
    'enabled': True,
    'frequency': 'daily',  # daily, weekly, monthly
    'retention_days': 30,
    'backup_path': 'backups/',
    'include_uploads': True,
    'compress': True
}

def create_backup():
    """إنشاء نسخة احتياطية"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = Path(backup_settings['backup_path'])
        backup_dir.mkdir(exist_ok=True)
        
        backup_name = f'backup_{timestamp}'
        backup_path = backup_dir / backup_name
        
        # إنشاء مجلد النسخة الاحتياطية
        backup_path.mkdir(exist_ok=True)
        
        # نسخ قاعدة البيانات
        db_source = Path('instance/inventory.db')
        if db_source.exists():
            shutil.copy2(db_source, backup_path / 'inventory.db')
        
        # نسخ الملفات المرفوعة إذا كانت موجودة
        if backup_settings['include_uploads']:
            uploads_dir = Path('uploads')
            if uploads_dir.exists():
                shutil.copytree(uploads_dir, backup_path / 'uploads', dirs_exist_ok=True)
        
        # ضغط النسخة الاحتياطية إذا كان مطلوباً
        if backup_settings['compress']:
            zip_path = backup_dir / f'{backup_name}.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in backup_path.rglob('*'):
                    if file_path.is_file():
                        zipf.write(file_path, file_path.relative_to(backup_path))
            
            # حذف المجلد غير المضغوط
            shutil.rmtree(backup_path)
            backup_path = zip_path
        
        # تنظيف النسخ القديمة
        cleanup_old_backups()
        
        print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
        return str(backup_path)
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
        return None

def cleanup_old_backups():
    """تنظيف النسخ الاحتياطية القديمة"""
    try:
        backup_dir = Path(backup_settings['backup_path'])
        if not backup_dir.exists():
            return
        
        retention_days = backup_settings['retention_days']
        cutoff_time = datetime.now().timestamp() - (retention_days * 24 * 60 * 60)
        
        for backup_file in backup_dir.iterdir():
            if backup_file.is_file() and backup_file.name.startswith('backup_'):
                if backup_file.stat().st_mtime < cutoff_time:
                    backup_file.unlink()
                    print(f"🗑️  تم حذف النسخة الاحتياطية القديمة: {backup_file.name}")
    
    except Exception as e:
        print(f"❌ خطأ في تنظيف النسخ القديمة: {e}")

def schedule_backups():
    """جدولة النسخ الاحتياطية"""
    if not backup_settings['enabled']:
        return
    
    frequency = backup_settings['frequency']
    
    if frequency == 'daily':
        schedule.every().day.at("02:00").do(create_backup)
    elif frequency == 'weekly':
        schedule.every().sunday.at("02:00").do(create_backup)
    elif frequency == 'monthly':
        schedule.every().month.do(create_backup)
    
    print(f"📅 تم جدولة النسخ الاحتياطية: {frequency}")

def run_backup_scheduler():
    """تشغيل مجدول النسخ الاحتياطية"""
    while True:
        schedule.run_pending()
        time.sleep(60)  # فحص كل دقيقة

# بدء مجدول النسخ الاحتياطية في خيط منفصل
backup_thread = threading.Thread(target=run_backup_scheduler, daemon=True)
backup_thread.start()
schedule_backups()

@app.route('/api/backup/create', methods=['POST'])
def manual_backup():
    """إنشاء نسخة احتياطية يدوياً"""
    try:
        backup_path = create_backup()
        if backup_path:
            return jsonify({
                'success': True, 
                'message': 'تم إنشاء النسخة الاحتياطية بنجاح',
                'backup_path': backup_path
            })
        else:
            return jsonify({'success': False, 'error': 'فشل في إنشاء النسخة الاحتياطية'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/list', methods=['GET'])
def list_backups():
    """جلب قائمة النسخ الاحتياطية"""
    try:
        backup_dir = Path(backup_settings['backup_path'])
        backups = []
        
        if backup_dir.exists():
            for backup_file in backup_dir.iterdir():
                if backup_file.is_file() and backup_file.name.startswith('backup_'):
                    stat = backup_file.stat()
                    backups.append({
                        'name': backup_file.name,
                        'size': stat.st_size,
                        'created_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'path': str(backup_file)
                    })
        
        # ترتيب حسب تاريخ الإنشاء (الأحدث أولاً)
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({'success': True, 'data': backups})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/settings', methods=['GET'])
def get_backup_settings():
    """جلب إعدادات النسخ الاحتياطي"""
    try:
        return jsonify({'success': True, 'data': backup_settings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/settings', methods=['POST'])
def update_backup_settings():
    """تحديث إعدادات النسخ الاحتياطي"""
    try:
        data = request.get_json()
        
        # تحديث الإعدادات
        if 'enabled' in data:
            backup_settings['enabled'] = bool(data['enabled'])
        if 'frequency' in data:
            backup_settings['frequency'] = data['frequency']
        if 'retention_days' in data:
            backup_settings['retention_days'] = int(data['retention_days'])
        if 'include_uploads' in data:
            backup_settings['include_uploads'] = bool(data['include_uploads'])
        if 'compress' in data:
            backup_settings['compress'] = bool(data['compress'])
        
        # إعادة جدولة النسخ الاحتياطية
        schedule.clear()
        schedule_backups()
        
        return jsonify({'success': True, 'message': 'تم تحديث إعدادات النسخ الاحتياطي'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/backup/restore', methods=['POST'])
def restore_backup():
    """استعادة نسخة احتياطية"""
    try:
        data = request.get_json()
        backup_name = data.get('backup_name')
        
        if not backup_name:
            return jsonify({'success': False, 'error': 'اسم النسخة الاحتياطية مطلوب'}), 400
        
        backup_path = Path(backup_settings['backup_path']) / backup_name
        
        if not backup_path.exists():
            return jsonify({'success': False, 'error': 'النسخة الاحتياطية غير موجودة'}), 404
        
        # إنشاء نسخة احتياطية من الحالة الحالية قبل الاستعادة
        current_backup = create_backup()
        
        # استعادة النسخة الاحتياطية
        if backup_path.suffix == '.zip':
            # استخراج الملف المضغوط
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                temp_dir = Path('temp_restore')
                zipf.extractall(temp_dir)
                
                # استعادة قاعدة البيانات
                db_backup = temp_dir / 'inventory.db'
                if db_backup.exists():
                    shutil.copy2(db_backup, 'instance/inventory.db')
                
                # استعادة الملفات المرفوعة
                uploads_backup = temp_dir / 'uploads'
                if uploads_backup.exists():
                    uploads_dir = Path('uploads')
                    if uploads_dir.exists():
                        shutil.rmtree(uploads_dir)
                    shutil.copytree(uploads_backup, uploads_dir)
                
                # تنظيف المجلد المؤقت
                shutil.rmtree(temp_dir)
        
        return jsonify({
            'success': True, 
            'message': 'تم استعادة النسخة الاحتياطية بنجاح',
            'current_backup': current_backup
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
'''
    
    # قراءة الخادم الحالي وإضافة نظام النسخ الاحتياطي
    backend_file = 'backend/minimal_working_app.py'
    
    try:
        with open(backend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # إضافة استيراد schedule في بداية الملف
        if "import schedule" not in content:
            imports_section = "from flask import Flask, request, jsonify\nfrom flask_cors import CORS\nimport sqlite3\nfrom datetime import datetime\nfrom werkzeug.security import generate_password_hash, check_password_hash\nimport schedule"
            content = content.replace("from flask import Flask, request, jsonify\nfrom flask_cors import CORS\nimport sqlite3\nfrom datetime import datetime\nfrom werkzeug.security import generate_password_hash, check_password_hash", imports_section)
        
        # إضافة نظام النسخ الاحتياطي قبل السطر الأخير
        if "if __name__ == '__main__':" in content:
            content = content.replace("if __name__ == '__main__':", backup_code + "\n\nif __name__ == '__main__':")
        else:
            content += "\n\n" + backup_code
        
        with open(backend_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ تم إضافة نظام النسخ الاحتياطي التلقائي")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في إضافة نظام النسخ الاحتياطي: {e}")
        return False

def create_backup_frontend_components():
    """إنشاء مكونات إدارة النسخ الاحتياطية في الواجهة الأمامية"""
    
    backup_management_component = '''import React, { useState, useEffect } from 'react';

const BackupManagement = () => {
  const [backups, setBackups] = useState([]);
  const [settings, setSettings] = useState({});
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchBackups();
    fetchSettings();
  }, []);

  const fetchBackups = async () => {
    try {
      const response = await fetch('http://localhost:5002/api/backup/list');
      const result = await response.json();
      if (result.success) {
        setBackups(result.data);
      }
    } catch (error) {
      console.error('خطأ في جلب النسخ الاحتياطية:', error);
    }
  };

  const fetchSettings = async () => {
    try {
      const response = await fetch('http://localhost:5002/api/backup/settings');
      const result = await response.json();
      if (result.success) {
        setSettings(result.data);
      }
    } catch (error) {
      console.error('خطأ في جلب إعدادات النسخ الاحتياطي:', error);
    } finally {
      setLoading(false);
    }
  };

  const createBackup = async () => {
    setCreating(true);
    try {
      const response = await fetch('http://localhost:5002/api/backup/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const result = await response.json();
      if (result.success) {
        alert('تم إنشاء النسخة الاحتياطية بنجاح');
        fetchBackups();
      } else {
        alert('خطأ: ' + result.error);
      }
    } catch (error) {
      console.error('خطأ في إنشاء النسخة الاحتياطية:', error);
      alert('حدث خطأ في إنشاء النسخة الاحتياطية');
    } finally {
      setCreating(false);
    }
  };

  const updateSettings = async (newSettings) => {
    try {
      const response = await fetch('http://localhost:5002/api/backup/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSettings),
      });
      
      const result = await response.json();
      if (result.success) {
        setSettings({...settings, ...newSettings});
        alert('تم تحديث الإعدادات بنجاح');
      } else {
        alert('خطأ: ' + result.error);
      }
    } catch (error) {
      console.error('خطأ في تحديث الإعدادات:', error);
      alert('حدث خطأ في تحديث الإعدادات');
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (loading) {
    return <div className="text-center p-8">جاري تحميل النسخ الاحتياطية...</div>;
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">إدارة النسخ الاحتياطية</h2>
        <button
          onClick={createBackup}
          disabled={creating}
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
        >
          {creating ? 'جاري الإنشاء...' : 'إنشاء نسخة احتياطية'}
        </button>
      </div>

      {/* إعدادات النسخ الاحتياطي */}
      <div className="mb-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-4">إعدادات النسخ الاحتياطي</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={settings.enabled}
                onChange={(e) => updateSettings({enabled: e.target.checked})}
                className="mr-2"
              />
              تفعيل النسخ الاحتياطي التلقائي
            </label>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              تكرار النسخ الاحتياطي
            </label>
            <select
              value={settings.frequency}
              onChange={(e) => updateSettings({frequency: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="daily">يومي</option>
              <option value="weekly">أسبوعي</option>
              <option value="monthly">شهري</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              مدة الاحتفاظ (بالأيام)
            </label>
            <input
              type="number"
              value={settings.retention_days}
              onChange={(e) => updateSettings({retention_days: parseInt(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              min="1"
            />
          </div>
          <div>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={settings.compress}
                onChange={(e) => updateSettings({compress: e.target.checked})}
                className="mr-2"
              />
              ضغط النسخ الاحتياطية
            </label>
          </div>
        </div>
      </div>

      {/* قائمة النسخ الاحتياطية */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                اسم النسخة
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                الحجم
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                تاريخ الإنشاء
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                الإجراءات
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {backups.map((backup, index) => (
              <tr key={index}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {backup.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatFileSize(backup.size)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(backup.created_at).toLocaleString('ar-SA')}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button className="text-blue-600 hover:text-blue-900 mr-3">
                    تحميل
                  </button>
                  <button className="text-orange-600 hover:text-orange-900 mr-3">
                    استعادة
                  </button>
                  <button className="text-red-600 hover:text-red-900">
                    حذف
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {backups.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            لا توجد نسخ احتياطية متاحة
          </div>
        )}
      </div>
    </div>
  );
};

export default BackupManagement;'''

    # إنشاء المجلدات والملفات
    backup_dir = 'frontend/src/components/backup'
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        # كتابة مكون إدارة النسخ الاحتياطية
        with open(f'{backup_dir}/BackupManagement.jsx', 'w', encoding='utf-8') as f:
            f.write(backup_management_component)
        
        print("   ✅ تم إنشاء مكونات إدارة النسخ الاحتياطية")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في إنشاء مكونات النسخ الاحتياطية: {e}")
        return False

def install_schedule_package():
    """تثبيت مكتبة schedule"""
    try:
        import subprocess
        result = subprocess.run(['pip3', 'install', 'schedule'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ تم تثبيت مكتبة schedule")
            return True
        else:
            print(f"   ❌ خطأ في تثبيت مكتبة schedule: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ خطأ في تثبيت مكتبة schedule: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("💾 بدء إضافة نظام النسخ الاحتياطي التلقائي...")
    print("=" * 50)
    
    success_count = 0
    total_tasks = 3
    
    # تثبيت مكتبة schedule
    print("📦 تثبيت مكتبة schedule...")
    if install_schedule_package():
        success_count += 1
    
    # إضافة نظام النسخ الاحتياطي في الخادم الخلفي
    print("🔧 إضافة نظام النسخ الاحتياطي في الخادم الخلفي...")
    if create_backup_system_backend():
        success_count += 1
    
    # إنشاء مكونات النسخ الاحتياطية في الواجهة الأمامية
    print("🎨 إنشاء مكونات إدارة النسخ الاحتياطية...")
    if create_backup_frontend_components():
        success_count += 1
    
    print("=" * 50)
    if success_count == total_tasks:
        print("✅ تم إضافة نظام النسخ الاحتياطي التلقائي بنجاح!")
        print("الميزات المضافة:")
        print("  💾 نسخ احتياطية تلقائية مجدولة")
        print("  🗂️  إدارة النسخ الاحتياطية")
        print("  ⚙️  إعدادات قابلة للتخصيص")
        print("  🔄 استعادة النسخ الاحتياطية")
        print("  🗑️  تنظيف النسخ القديمة تلقائياً")
    else:
        print(f"⚠️  تم إكمال {success_count} من {total_tasks} مهام بنجاح")
        print("يرجى مراجعة الأخطاء أعلاه")

if __name__ == "__main__":
    main()
