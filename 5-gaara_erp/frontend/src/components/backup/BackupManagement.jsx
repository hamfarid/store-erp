import React, { useState, useEffect } from 'react';

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

export default BackupManagement;