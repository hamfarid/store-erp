import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  Search, 
  Database, 
  Activity, 
  TrendingUp,
  RefreshCw,
  Settings,
  Play,
  Pause,
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react';
import ApiService from '../services/ApiService';

const LearningDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState(null);
  const [schedulerStatus, setSchedulerStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 10000); // تحديث كل 10 ثواني
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // جلب إحصائيات قاعدة البيانات
      const statsResponse = await ApiService.get('/v1/data-management/stats');
      setStats(statsResponse.data);
      
      // جلب حالة المجدول
      const schedulerResponse = await ApiService.get('/v1/scheduled-updates/status');
      setSchedulerStatus(schedulerResponse.data);
      
      setError(null);
    } catch (err) {
      setError('فشل في تحميل البيانات');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSchedulerToggle = async () => {
    try {
      if (schedulerStatus?.is_running) {
        await ApiService.post('/v1/scheduled-updates/stop');
      } else {
        await ApiService.post('/v1/scheduled-updates/start');
      }
      fetchDashboardData();
    } catch (err) {
      setError('فشل في تغيير حالة المجدول');
      console.error(err);
    }
  };

  const handleManualUpdate = async (type) => {
    try {
      await ApiService.post(`/scheduled-updates/trigger/${type}`);
      alert(`تم تشغيل تحديث ${type} بنجاح`);
      fetchDashboardData();
    } catch (err) {
      alert('فشل في تشغيل التحديث');
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="bg-gradient-to-r from-green-500 to-blue-500 p-3 rounded-lg">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">
                لوحة التحكم في التعلم والبحث
              </h1>
              <p className="text-gray-600">
                إدارة شاملة لنظام التعلم الآلي والبحث عن الأمراض
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <button
              onClick={fetchDashboardData}
              className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
            >
              <RefreshCw className="w-5 h-5" />
              تحديث
            </button>
            
            <button
              onClick={handleSchedulerToggle}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition ${
                schedulerStatus?.is_running
                  ? 'bg-red-500 hover:bg-red-600'
                  : 'bg-green-500 hover:bg-green-600'
              } text-white`}
            >
              {schedulerStatus?.is_running ? (
                <>
                  <Pause className="w-5 h-5" />
                  إيقاف المجدول
                </>
              ) : (
                <>
                  <Play className="w-5 h-5" />
                  تشغيل المجدول
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-center gap-2">
          <AlertCircle className="w-5 h-5" />
          {error}
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          icon={<Database className="w-6 h-6" />}
          title="إجمالي الأمراض"
          value={stats?.total_diseases || 0}
          color="blue"
          loading={loading}
        />
        <StatCard
          icon={<CheckCircle className="w-6 h-6" />}
          title="محدثة مؤخراً"
          value={stats?.recently_updated || 0}
          color="green"
          loading={loading}
        />
        <StatCard
          icon={<AlertCircle className="w-6 h-6" />}
          title="تحتاج تحديث"
          value={stats?.needs_update || 0}
          color="orange"
          loading={loading}
        />
        <StatCard
          icon={<Activity className="w-6 h-6" />}
          title="حالة المجدول"
          value={schedulerStatus?.is_running ? 'نشط' : 'متوقف'}
          color={schedulerStatus?.is_running ? 'green' : 'red'}
          loading={loading}
        />
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-lg mb-6">
        <div className="flex border-b">
          {[
            { id: 'overview', label: 'نظرة عامة', icon: <Activity /> },
            { id: 'updates', label: 'التحديثات المباشرة', icon: <TrendingUp /> },
            { id: 'keywords', label: 'الكلمات المفتاحية', icon: <Search /> },
            { id: 'sources', label: 'محركات البحث', icon: <Database /> },
            { id: 'operations', label: 'العمليات الجارية', icon: <RefreshCw /> },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition ${
                activeTab === tab.id
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                  : 'text-gray-600 hover:text-blue-600 hover:bg-gray-50'
              }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </div>

        <div className="p-6">
          {activeTab === 'overview' && <OverviewTab stats={stats} schedulerStatus={schedulerStatus} onManualUpdate={handleManualUpdate} />}
          {activeTab === 'updates' && <UpdatesTab />}
          {activeTab === 'keywords' && <KeywordsTab />}
          {activeTab === 'sources' && <SourcesTab />}
          {activeTab === 'operations' && <OperationsTab />}
        </div>
      </div>
    </div>
  );
};

// مكون بطاقة الإحصائيات
const StatCard = ({ icon, title, value, color, loading }) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    orange: 'from-orange-500 to-orange-600',
    red: 'from-red-500 to-red-600',
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <div className={`bg-gradient-to-r ${colorClasses[color]} p-3 rounded-lg text-white`}>
          {icon}
        </div>
      </div>
      <h3 className="text-gray-600 text-sm mb-2">{title}</h3>
      {loading ? (
        <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
      ) : (
        <p className="text-3xl font-bold text-gray-800">{value}</p>
      )}
    </div>
  );
};

// تبويب النظرة العامة
const OverviewTab = ({ stats, schedulerStatus, onManualUpdate }) => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* معلومات قاعدة البيانات */}
        <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Database className="w-6 h-6 text-blue-600" />
            قاعدة البيانات
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">إجمالي الأمراض:</span>
              <span className="font-bold text-gray-800">{stats?.total_diseases || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">محدثة مؤخراً:</span>
              <span className="font-bold text-green-600">{stats?.recently_updated || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">تحتاج تحديث:</span>
              <span className="font-bold text-orange-600">{stats?.needs_update || 0}</span>
            </div>
          </div>
        </div>

        {/* حالة المجدول */}
        <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Clock className="w-6 h-6 text-green-600" />
            المجدول
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">الحالة:</span>
              <span className={`font-bold ${schedulerStatus?.is_running ? 'text-green-600' : 'text-red-600'}`}>
                {schedulerStatus?.is_running ? 'نشط' : 'متوقف'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">عدد المهام:</span>
              <span className="font-bold text-gray-800">{schedulerStatus?.jobs_count || 0}</span>
            </div>
          </div>
        </div>
      </div>

      {/* أزرار التحديث اليدوي */}
      <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">تحديث يدوي</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={() => onManualUpdate('database')}
            className="flex items-center justify-center gap-2 px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
          >
            <Database className="w-5 h-5" />
            تحديث قاعدة البيانات
          </button>
          <button
            onClick={() => onManualUpdate('nutrients')}
            className="flex items-center justify-center gap-2 px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
          >
            <TrendingUp className="w-5 h-5" />
            تحديث نقص العناصر
          </button>
          <button
            onClick={() => onManualUpdate('sources')}
            className="flex items-center justify-center gap-2 px-4 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition"
          >
            <Search className="w-5 h-5" />
            فحص المصادر
          </button>
        </div>
      </div>
    </div>
  );
};

// تبويب التحديثات المباشرة
const UpdatesTab = () => {
  const [updates, setUpdates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUpdates();
    const interval = setInterval(fetchUpdates, 5000); // تحديث كل 5 ثواني
    return () => clearInterval(interval);
  }, []);

  const fetchUpdates = async () => {
    try {
      const response = await ApiService.get('/v1/scheduled-updates/history?limit=20');
      setUpdates(response.data);
      setLoading(false);
    } catch (err) {
      console.error('فشل في جلب التحديثات:', err);
      setLoading(false);
    }
  };

  const getTypeLabel = (type) => {
    const labels = {
      'database_update': 'تحديث قاعدة البيانات',
      'nutrients_update': 'تحديث نقص العناصر',
      'sources_check': 'فحص المصادر',
    };
    return labels[type] || type;
  };

  const getTypeColor = (type) => {
    const colors = {
      'database_update': 'blue',
      'nutrients_update': 'green',
      'sources_check': 'purple',
    };
    return colors[type] || 'gray';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('ar-EG', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-gray-800">سجل التحديثات المباشرة</h3>
        <div className="flex items-center gap-2 text-green-600">
          <Activity className="w-5 h-5 animate-pulse" />
          <span className="font-medium">مباشر</span>
        </div>
      </div>

      {updates.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <AlertCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p>لا توجد تحديثات حتى الآن</p>
        </div>
      ) : (
        <div className="space-y-3">
          {updates.map((update, index) => (
            <div
              key={index}
              className="bg-white border-r-4 border-${getTypeColor(update.type)}-500 rounded-lg p-4 shadow hover:shadow-md transition"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`px-3 py-1 bg-${getTypeColor(update.type)}-100 text-${getTypeColor(update.type)}-700 rounded-full text-sm font-medium`}>
                      {getTypeLabel(update.type)}
                    </span>
                    <span className="text-gray-500 text-sm flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {formatDate(update.timestamp)}
                    </span>
                  </div>

                  {update.stats.error ? (
                    <div className="flex items-center gap-2 text-red-600">
                      <AlertCircle className="w-5 h-5" />
                      <span>{update.stats.error}</span>
                    </div>
                  ) : (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-3">
                      {update.stats.diseases_checked && (
                        <div className="text-sm">
                          <span className="text-gray-600">تم الفحص:</span>
                          <span className="font-bold text-gray-800 mr-2">
                            {update.stats.diseases_checked}
                          </span>
                        </div>
                      )}
                      {update.stats.diseases_updated && (
                        <div className="text-sm">
                          <span className="text-gray-600">تم التحديث:</span>
                          <span className="font-bold text-green-600 mr-2">
                            {update.stats.diseases_updated}
                          </span>
                        </div>
                      )}
                      {update.stats.diseases_added && (
                        <div className="text-sm">
                          <span className="text-gray-600">تم الإضافة:</span>
                          <span className="font-bold text-blue-600 mr-2">
                            {update.stats.diseases_added}
                          </span>
                        </div>
                      )}
                      {update.stats.duration_seconds && (
                        <div className="text-sm">
                          <span className="text-gray-600">المدة:</span>
                          <span className="font-bold text-gray-800 mr-2">
                            {update.stats.duration_seconds.toFixed(1)}ث
                          </span>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {!update.stats.error && (
                  <CheckCircle className="w-6 h-6 text-green-500" />
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
// تبويب الكلمات المفتاحية
const KeywordsTab = () => {
  const [keywords, setKeywords] = useState([]);
  const [newKeyword, setNewKeyword] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editValue, setEditValue] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchKeywords();
  }, []);

  const fetchKeywords = async () => {
    try {
      const response = await ApiService.get('/v1/data-management/diseases/common');
      const diseases = response.data.common_diseases || [];
      setKeywords(diseases.map((d, i) => ({ id: i, text: d, enabled: true })));
      setLoading(false);
    } catch (err) {
      console.error('فشل في جلب الكلمات المفتاحية:', err);
      setLoading(false);
    }
  };

  const handleAdd = () => {
    if (newKeyword.trim()) {
      const newId = Math.max(...keywords.map(k => k.id), 0) + 1;
      setKeywords([...keywords, { id: newId, text: newKeyword.trim(), enabled: true }]);
      setNewKeyword('');
    }
  };

  const handleDelete = (id) => {
    setKeywords(keywords.filter(k => k.id !== id));
  };

  const handleEdit = (id) => {
    const keyword = keywords.find(k => k.id === id);
    setEditingId(id);
    setEditValue(keyword.text);
  };

  const handleSaveEdit = (id) => {
    setKeywords(keywords.map(k => 
      k.id === id ? { ...k, text: editValue } : k
    ));
    setEditingId(null);
    setEditValue('');
  };

  const handleToggle = (id) => {
    setKeywords(keywords.map(k => 
      k.id === id ? { ...k, enabled: !k.enabled } : k
    ));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Search className="w-6 h-6 text-blue-600" />
          إدارة الكلمات المفتاحية للبحث
        </h3>
        <p className="text-gray-600 mb-6">
          أضف أو عدل الكلمات المفتاحية التي سيتم استخدامها في البحث عن الأمراض والإصابات
        </p>

        {/* إضافة كلمة جديدة */}
        <div className="flex gap-3 mb-6">
          <input
            type="text"
            value={newKeyword}
            onChange={(e) => setNewKeyword(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleAdd()}
            placeholder="أدخل كلمة مفتاحية جديدة (عربي أو إنجليزي)"
            className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
          />
          <button
            onClick={handleAdd}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition flex items-center gap-2"
          >
            <span className="text-xl">+</span>
            إضافة
          </button>
        </div>

        {/* إحصائيات */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-blue-600">{keywords.length}</p>
            <p className="text-gray-600 text-sm">إجمالي الكلمات</p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-green-600">
              {keywords.filter(k => k.enabled).length}
            </p>
            <p className="text-gray-600 text-sm">مفعلة</p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-gray-600">
              {keywords.filter(k => !k.enabled).length}
            </p>
            <p className="text-gray-600 text-sm">معطلة</p>
          </div>
        </div>
      </div>

      {/* قائمة الكلمات المفتاحية */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {keywords.map((keyword) => (
          <div
            key={keyword.id}
            className={`bg-white rounded-lg p-4 shadow border-2 transition ${
              keyword.enabled ? 'border-green-200' : 'border-gray-200 opacity-60'
            }`}
          >
            <div className="flex items-center justify-between">
              {editingId === keyword.id ? (
                <input
                  type="text"
                  value={editValue}
                  onChange={(e) => setEditValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSaveEdit(keyword.id)}
                  className="flex-1 px-3 py-2 border-2 border-blue-500 rounded-lg focus:outline-none"
                  autoFocus
                />
              ) : (
                <span className={`text-lg font-medium ${
                  keyword.enabled ? 'text-gray-800' : 'text-gray-400'
                }`}>
                  {keyword.text}
                </span>
              )}

              <div className="flex items-center gap-2">
                {editingId === keyword.id ? (
                  <>
                    <button
                      onClick={() => handleSaveEdit(keyword.id)}
                      className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 transition text-sm"
                    >
                      حفظ
                    </button>
                    <button
                      onClick={() => setEditingId(null)}
                      className="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 transition text-sm"
                    >
                      إلغاء
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      onClick={() => handleToggle(keyword.id)}
                      className={`px-3 py-1 rounded transition text-sm ${
                        keyword.enabled
                          ? 'bg-green-100 text-green-700 hover:bg-green-200'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {keyword.enabled ? 'مفعل' : 'معطل'}
                    </button>
                    <button
                      onClick={() => handleEdit(keyword.id)}
                      className="px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition text-sm"
                    >
                      تعديل
                    </button>
                    <button
                      onClick={() => handleDelete(keyword.id)}
                      className="px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 transition text-sm"
                    >
                      حذف
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* زر الحفظ النهائي */}
      <div className="flex justify-center">
        <button
          onClick={() => alert('تم حفظ الكلمات المفتاحية بنجاح!')}
          className="px-8 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-lg hover:from-green-600 hover:to-blue-600 transition font-bold text-lg"
        >
          حفظ جميع التغييرات
        </button>
      </div>
    </div>
  );
};
// تبويب محركات البحث
const SourcesTab = () => {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, academic, government, commercial

  useEffect(() => {
    fetchSources();
  }, []);

  const fetchSources = async () => {
    try {
      const response = await ApiService.get('/v1/data-management/sources');
      setSources(response.data.sources || []);
      setLoading(false);
    } catch (err) {
      console.error('فشل في جلب المصادر:', err);
      setLoading(false);
    }
  };

  const handleToggle = (sourceName) => {
    setSources(sources.map(s => 
      s.name === sourceName ? { ...s, enabled: !s.enabled } : s
    ));
  };

  const getTypeLabel = (type) => {
    const labels = {
      'academic': 'أكاديمي',
      'government': 'حكومي',
      'commercial': 'تجاري',
      'community': 'مجتمعي',
    };
    return labels[type] || type;
  };

  const getTypeColor = (type) => {
    const colors = {
      'academic': 'blue',
      'government': 'green',
      'commercial': 'orange',
      'community': 'purple',
    };
    return colors[type] || 'gray';
  };

  const getReliabilityColor = (reliability) => {
    if (reliability >= 0.95) return 'text-green-600';
    if (reliability >= 0.90) return 'text-blue-600';
    if (reliability >= 0.80) return 'text-yellow-600';
    return 'text-orange-600';
  };

  const filteredSources = filter === 'all' 
    ? sources 
    : sources.filter(s => s.type === filter);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Database className="w-6 h-6 text-green-600" />
          إدارة مصادر ومحركات البحث
        </h3>
        <p className="text-gray-600 mb-6">
          إدارة المصادر الموثوقة للبحث عن معلومات الأمراض والإصابات
        </p>

        {/* الفلاتر */}
        <div className="flex gap-3 mb-6 flex-wrap">
          {[
            { id: 'all', label: 'الكل' },
            { id: 'academic', label: 'أكاديمي' },
            { id: 'government', label: 'حكومي' },
            { id: 'commercial', label: 'تجاري' },
            { id: 'community', label: 'مجتمعي' },
          ].map((f) => (
            <button
              key={f.id}
              onClick={() => setFilter(f.id)}
              className={`px-4 py-2 rounded-lg transition ${
                filter === f.id
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>

        {/* إحصائيات */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-blue-600">{sources.length}</p>
            <p className="text-gray-600 text-sm">إجمالي المصادر</p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-green-600">
              {sources.filter(s => s.enabled).length}
            </p>
            <p className="text-gray-600 text-sm">مفعلة</p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-orange-600">
              {sources.filter(s => s.type === 'academic').length}
            </p>
            <p className="text-gray-600 text-sm">أكاديمية</p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-purple-600">
              {sources.filter(s => s.language === 'ar').length}
            </p>
            <p className="text-gray-600 text-sm">عربية</p>
          </div>
        </div>
      </div>

      {/* قائمة المصادر */}
      <div className="grid grid-cols-1 gap-4">
        {filteredSources.map((source) => (
          <div
            key={source.name}
            className={`bg-white rounded-lg p-6 shadow-lg border-2 transition ${
              source.enabled ? 'border-green-200' : 'border-gray-200 opacity-70'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-3">
                  <h4 className="text-xl font-bold text-gray-800">{source.name}</h4>
                  <span className={`px-3 py-1 bg-${getTypeColor(source.type)}-100 text-${getTypeColor(source.type)}-700 rounded-full text-sm font-medium`}>
                    {getTypeLabel(source.type)}
                  </span>
                  {source.language === 'ar' && (
                    <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                      عربي
                    </span>
                  )}
                </div>

                <p className="text-gray-600 mb-3">{source.description}</p>

                <div className="flex items-center gap-6 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-600">الموثوقية:</span>
                    <span className={`font-bold ${getReliabilityColor(source.reliability)}`}>
                      {(source.reliability * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-600">التحديث:</span>
                    <span className="font-medium text-gray-800">
                      {source.update_frequency === 'daily' && 'يومي'}
                      {source.update_frequency === 'weekly' && 'أسبوعي'}
                      {source.update_frequency === 'monthly' && 'شهري'}
                      {source.update_frequency === 'quarterly' && 'ربع سنوي'}
                    </span>
                  </div>
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-700 underline"
                  >
                    زيارة الموقع
                  </a>
                </div>
              </div>

              <button
                onClick={() => handleToggle(source.name)}
                className={`px-6 py-3 rounded-lg transition font-medium ${
                  source.enabled
                    ? 'bg-green-500 text-white hover:bg-green-600'
                    : 'bg-gray-300 text-gray-700 hover:bg-gray-400'
                }`}
              >
                {source.enabled ? 'مفعل' : 'معطل'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* زر الحفظ */}
      <div className="flex justify-center">
        <button
          onClick={() => alert('تم حفظ إعدادات المصادر بنجاح!')}
          className="px-8 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-lg hover:from-green-600 hover:to-blue-600 transition font-bold text-lg"
        >
          حفظ جميع التغييرات
        </button>
      </div>
    </div>
  );
};
// تبويب العمليات الجارية
const OperationsTab = () => {
  const [operations, setOperations] = useState([
    {
      id: 1,
      type: 'crawling',
      title: 'البحث عن صور البياض الدقيقي',
      status: 'running',
      progress: 65,
      details: {
        images_found: 42,
        images_downloaded: 28,
        images_processed: 15,
        current_source: 'Google Images',
      },
      started_at: new Date(Date.now() - 300000),
    },
    {
      id: 2,
      type: 'training',
      title: 'تدريب نموذج YOLO',
      status: 'running',
      progress: 35,
      details: {
        epoch: 7,
        total_epochs: 20,
        loss: 0.0234,
        accuracy: 0.87,
      },
      started_at: new Date(Date.now() - 900000),
    },
    {
      id: 3,
      type: 'database_update',
      title: 'تحديث قاعدة البيانات',
      status: 'completed',
      progress: 100,
      details: {
        diseases_checked: 45,
        diseases_updated: 12,
        diseases_added: 3,
      },
      started_at: new Date(Date.now() - 1800000),
      completed_at: new Date(Date.now() - 600000),
    },
  ]);

  const getStatusLabel = (status) => {
    const labels = {
      'running': 'جاري',
      'completed': 'مكتمل',
      'failed': 'فشل',
      'paused': 'متوقف',
    };
    return labels[status] || status;
  };

  const getStatusColor = (status) => {
    const colors = {
      'running': 'blue',
      'completed': 'green',
      'failed': 'red',
      'paused': 'yellow',
    };
    return colors[status] || 'gray';
  };

  const getTypeIcon = (type) => {
    if (type === 'crawling') return <Search className="w-5 h-5" />;
    if (type === 'training') return <Brain className="w-5 h-5" />;
    if (type === 'database_update') return <Database className="w-5 h-5" />;
    return <Activity className="w-5 h-5" />;
  };

  const formatDuration = (startDate, endDate = new Date()) => {
    const diff = Math.floor((endDate - startDate) / 1000);
    const minutes = Math.floor(diff / 60);
    const seconds = diff % 60;
    return `${minutes}د ${seconds}ث`;
  };

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Activity className="w-6 h-6 text-purple-600 animate-pulse" />
          العمليات الجارية والمكتملة
        </h3>
        <p className="text-gray-600 mb-6">
          متابعة مباشرة لجميع عمليات البحث والتعلم والتحديث
        </p>

        {/* إحصائيات */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-blue-600">
              {operations.filter(o => o.status === 'running').length}
            </p>
            <p className="text-gray-600 text-sm">جارية</p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-green-600">
              {operations.filter(o => o.status === 'completed').length}
            </p>
            <p className="text-gray-600 text-sm">مكتملة</p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-purple-600">{operations.length}</p>
            <p className="text-gray-600 text-sm">إجمالي</p>
          </div>
        </div>
      </div>

      {/* قائمة العمليات */}
      <div className="space-y-4">
        {operations.map((operation) => (
          <div
            key={operation.id}
            className="bg-white rounded-lg p-6 shadow-lg border-2 border-gray-200"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className={`p-3 bg-${getStatusColor(operation.status)}-100 rounded-lg`}>
                  {getTypeIcon(operation.type)}
                </div>
                <div>
                  <h4 className="text-lg font-bold text-gray-800">{operation.title}</h4>
                  <p className="text-sm text-gray-600">
                    بدأ منذ: {formatDuration(operation.started_at)}
                  </p>
                </div>
              </div>

              <span
                className={`px-4 py-2 bg-${getStatusColor(operation.status)}-100 text-${getStatusColor(operation.status)}-700 rounded-full text-sm font-medium`}
              >
                {getStatusLabel(operation.status)}
              </span>
            </div>

            {/* شريط التقدم */}
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600">التقدم:</span>
                <span className="text-sm font-bold text-gray-800">{operation.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className={`bg-gradient-to-r from-${getStatusColor(operation.status)}-400 to-${getStatusColor(operation.status)}-600 h-3 rounded-full transition-all duration-500`}
                  style={{ width: `${operation.progress}%` }}
                ></div>
              </div>
            </div>

            {/* التفاصيل */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h5 className="font-bold text-gray-800 mb-3">التفاصيل:</h5>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(operation.details).map(([key, value]) => (
                  <div key={key} className="text-sm">
                    <span className="text-gray-600 block mb-1">
                      {key.replace(/_/g, ' ')}
                    </span>
                    <span className="font-bold text-gray-800">
                      {typeof value === 'number' && value < 1 ? value.toFixed(4) : value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LearningDashboard;
