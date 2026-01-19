import { useState, useEffect } from 'react';
import axios from 'axios';

const ImageCrawler = () => {
  const [query, setQuery] = useState('');
  const [maxImages, setMaxImages] = useState(50);
  const [languages, setLanguages] = useState(['en', 'ar']);
  const [sources, setSources] = useState(['google', 'bing']);
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [diseases, setDiseases] = useState([]);

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:1005/api/v1';

  useEffect(() => {
    fetchStats();
    fetchDiseases();
  }, []);

  useEffect(() => {
    if (taskId) {
      const interval = setInterval(() => {
        fetchStatus();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [taskId]);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/crawler/knowledge/stats`);
      if (response.data.success) {
        setStats(response.data.data);
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const fetchDiseases = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/crawler/diseases`);
      if (response.data.success) {
        setDiseases(response.data.data);
      }
    } catch (error) {
      console.error('Failed to fetch diseases:', error);
    }
  };

  const fetchStatus = async () => {
    if (!taskId) return;
    
    try {
      const response = await axios.get(`${API_BASE_URL}/crawler/status/${taskId}`);
      if (response.data.success) {
        setStatus(response.data.data);
        
        if (response.data.data.status === 'completed' || response.data.data.status === 'failed') {
          setLoading(false);
          fetchStats();
          fetchDiseases();
        }
      }
    } catch (error) {
      console.error('Failed to fetch status:', error);
    }
  };

  const startCrawl = async () => {
    if (!query.trim()) {
      alert('Please enter a search query');
      return;
    }

    setLoading(true);
    setStatus(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/crawler/start`, {
        query,
        max_images: maxImages,
        languages,
        sources
      });

      if (response.data.success) {
        setTaskId(response.data.data.task_id);
      }
    } catch (error) {
      console.error('Failed to start crawl:', error);
      alert('Failed to start crawl: ' + error.message);
      setLoading(false);
    }
  };

  const toggleLanguage = (lang) => {
    setLanguages(prev => 
      prev.includes(lang) 
        ? prev.filter(l => l !== lang)
        : [...prev, lang]
    );
  };

  const toggleSource = (source) => {
    setSources(prev => 
      prev.includes(source) 
        ? prev.filter(s => s !== source)
        : [...prev, source]
    );
  };

  return (
    <div className="container mx-auto p-6" dir="rtl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">البحث الذكي عن صور الأمراض</h1>
        <p className="text-gray-600">
          ابحث عن صور أمراض النباتات من الإنترنت وقم بتحليلها تلقائيًا
        </p>
      </div>

      {/* Statistics */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-blue-50 p-6 rounded-lg">
            <div className="text-3xl font-bold text-blue-600">{stats.total_images}</div>
            <div className="text-gray-600">إجمالي الصور</div>
          </div>
          <div className="bg-green-50 p-6 rounded-lg">
            <div className="text-3xl font-bold text-green-600">{stats.total_diseases}</div>
            <div className="text-gray-600">الأمراض المكتشفة</div>
          </div>
          <div className="bg-purple-50 p-6 rounded-lg">
            <div className="text-3xl font-bold text-purple-600">
              {stats.top_diseases?.length || 0}
            </div>
            <div className="text-gray-600">الأمراض الأكثر شيوعًا</div>
          </div>
        </div>
      )}

      {/* Search Form */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">
            استعلام البحث
          </label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="مثال: tomato leaf disease"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">
            عدد الصور (الحد الأقصى)
          </label>
          <input
            type="number"
            value={maxImages}
            onChange={(e) => setMaxImages(parseInt(e.target.value))}
            min="10"
            max="200"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">اللغات</label>
          <div className="flex gap-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={languages.includes('en')}
                onChange={() => toggleLanguage('en')}
                disabled={loading}
                className="mr-2"
              />
              English
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={languages.includes('ar')}
                onChange={() => toggleLanguage('ar')}
                disabled={loading}
                className="mr-2"
              />
              العربية
            </label>
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">المصادر</label>
          <div className="flex gap-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={sources.includes('google')}
                onChange={() => toggleSource('google')}
                disabled={loading}
                className="mr-2"
              />
              Google
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={sources.includes('bing')}
                onChange={() => toggleSource('bing')}
                disabled={loading}
                className="mr-2"
              />
              Bing
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={sources.includes('unsplash')}
                onChange={() => toggleSource('unsplash')}
                disabled={loading}
                className="mr-2"
              />
              Unsplash
            </label>
          </div>
        </div>

        <button
          onClick={startCrawl}
          disabled={loading || !query.trim()}
          className={`w-full py-3 rounded-lg font-bold text-white ${
            loading || !query.trim()
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {loading ? 'جاري البحث...' : 'بدء البحث'}
        </button>
      </div>

      {/* Status */}
      {status && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-bold mb-4">حالة المهمة</h2>
          
          <div className="mb-4">
            <div className="flex justify-between mb-2">
              <span>التقدم</span>
              <span>{status.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className="bg-blue-600 h-4 rounded-full transition-all duration-300"
                style={{ width: `${status.progress}%` }}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <div className="text-gray-600">الحالة</div>
              <div className="font-bold">{status.status}</div>
            </div>
            <div>
              <div className="text-gray-600">الصور المحملة</div>
              <div className="font-bold">{status.total_images}</div>
            </div>
            <div>
              <div className="text-gray-600">الصور المحللة</div>
              <div className="font-bold">{status.analyzed_images}</div>
            </div>
            <div>
              <div className="text-gray-600">الرسالة</div>
              <div className="font-bold text-sm">{status.message}</div>
            </div>
          </div>
        </div>
      )}

      {/* Diseases List */}
      {diseases.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">الأمراض في قاعدة المعرفة</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {diseases.map((disease, index) => (
              <div key={index} className="border border-gray-200 p-4 rounded-lg">
                <div className="font-bold text-lg mb-2">{disease.name}</div>
                <div className="text-sm text-gray-600">
                  عدد الصور: {disease.image_count}
                </div>
                {disease.avg_confidence && (
                  <div className="text-sm text-gray-600">
                    متوسط الثقة: {(disease.avg_confidence * 100).toFixed(1)}%
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageCrawler;
