// ملف: /home/ubuntu/gaara_development/gaara_ai_integrated/frontend/src/components/Analytics/AdvancedAnalytics.jsx
import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
  Area,
  AreaChart
} from 'recharts';
import ApiService from '../../services/ApiService';
import './Analytics.css';

const AdvancedAnalytics = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('month');
  const [selectedMetric, setSelectedMetric] = useState('all');

  useEffect(() => {
    loadAnalyticsData();
  }, [selectedPeriod, selectedMetric]);

  const loadAnalyticsData = async () => {
    try {
      setLoading(true);
      const data = await ApiService.getAnalytics();
      setAnalyticsData(data);
    } catch (error) {
      console.error('خطأ في تحميل بيانات التحليلات:', error);
    } finally {
      setLoading(false);
    }
  };

  // بيانات تجريبية للتحليلات المتقدمة
  const performanceData = [
    { period: 'الأسبوع 1', productivity: 85, efficiency: 78, quality: 92 },
    { period: 'الأسبوع 2', productivity: 88, efficiency: 82, quality: 89 },
    { period: 'الأسبوع 3', productivity: 92, efficiency: 85, quality: 94 },
    { period: 'الأسبوع 4', productivity: 87, efficiency: 80, quality: 91 }
  ];

  const trendData = [
    { month: 'يناير', diseases: 45, treatments: 42, success_rate: 93 },
    { month: 'فبراير', diseases: 38, treatments: 36, success_rate: 95 },
    { month: 'مارس', diseases: 52, treatments: 48, success_rate: 92 },
    { month: 'أبريل', diseases: 41, treatments: 39, success_rate: 95 },
    { month: 'مايو', diseases: 35, treatments: 34, success_rate: 97 },
    { month: 'يونيو', diseases: 29, treatments: 28, success_rate: 97 }
  ];

  const cropComparisonData = [
    { crop: 'الطماطم', yield_2023: 4.2, yield_2024: 4.8, improvement: 14.3 },
    { crop: 'الخيار', yield_2023: 3.1, yield_2024: 3.6, improvement: 16.1 },
    { crop: 'الفلفل', yield_2023: 2.8, yield_2024: 3.2, improvement: 14.3 },
    { crop: 'الباذنجان', yield_2023: 3.5, yield_2024: 4.1, improvement: 17.1 },
    { crop: 'الكوسا', yield_2023: 2.9, yield_2024: 3.4, improvement: 17.2 }
  ];

  const aiAccuracyData = [
    { week: 'الأسبوع 1', accuracy: 87.5, confidence: 82.1 },
    { week: 'الأسبوع 2', accuracy: 89.2, confidence: 84.3 },
    { week: 'الأسبوع 3', accuracy: 91.8, confidence: 87.2 },
    { week: 'الأسبوع 4', accuracy: 93.1, confidence: 89.5 }
  ];

  if (loading) {
    return (
      <div className="analytics-loading">
        <div className="loading-spinner"></div>
        <p>جاري تحميل التحليلات المتقدمة...</p>
      </div>
    );
  }

  return (
    <div className="advanced-analytics">
      <div className="analytics-header">
        <h1>التحليلات المتقدمة</h1>
        <div className="analytics-controls">
          <select 
            value={selectedPeriod} 
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="period-selector"
          >
            <option value="week">أسبوعي</option>
            <option value="month">شهري</option>
            <option value="quarter">ربع سنوي</option>
            <option value="year">سنوي</option>
          </select>
          
          <select 
            value={selectedMetric} 
            onChange={(e) => setSelectedMetric(e.target.value)}
            className="metric-selector"
          >
            <option value="all">جميع المؤشرات</option>
            <option value="productivity">الإنتاجية</option>
            <option value="diseases">الأمراض</option>
            <option value="ai_performance">أداء الذكاء الاصطناعي</option>
          </select>
        </div>
      </div>

      <div className="analytics-grid">
        {/* مؤشرات الأداء الرئيسية */}
        <div className="analytics-card kpi-card">
          <h3>مؤشرات الأداء الرئيسية</h3>
          <div className="kpi-grid">
            <div className="kpi-item">
              <div className="kpi-value">94.2%</div>
              <div className="kpi-label">دقة التشخيص</div>
              <div className="kpi-trend positive">+2.1%</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-value">87.5%</div>
              <div className="kpi-label">معدل الشفاء</div>
              <div className="kpi-trend positive">+1.8%</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-value">156</div>
              <div className="kpi-label">التشخيصات الشهرية</div>
              <div className="kpi-trend positive">+12%</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-value">23</div>
              <div className="kpi-label">المزارع النشطة</div>
              <div className="kpi-trend positive">+3</div>
            </div>
          </div>
        </div>

        {/* رسم بياني لأداء النظام */}
        <div className="analytics-card">
          <h3>أداء النظام الأسبوعي</h3>
          <ResponsiveContainer width="100%" height={300}>
            <ComposedChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="productivity" fill="#4ECDC4" name="الإنتاجية" />
              <Line type="monotone" dataKey="efficiency" stroke="#45B7D1" name="الكفاءة" />
              <Line type="monotone" dataKey="quality" stroke="#96CEB4" name="الجودة" />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* اتجاهات الأمراض والعلاج */}
        <div className="analytics-card">
          <h3>اتجاهات الأمراض والعلاج</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area 
                type="monotone" 
                dataKey="diseases" 
                stackId="1" 
                stroke="#FF6B6B" 
                fill="#FF6B6B" 
                fillOpacity={0.6}
                name="الأمراض المكتشفة"
              />
              <Area 
                type="monotone" 
                dataKey="treatments" 
                stackId="2" 
                stroke="#4ECDC4" 
                fill="#4ECDC4" 
                fillOpacity={0.6}
                name="العلاجات المطبقة"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* مقارنة إنتاجية المحاصيل */}
        <div className="analytics-card">
          <h3>مقارنة إنتاجية المحاصيل (طن/هكتار)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={cropComparisonData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="crop" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="yield_2023" fill="#E0E0E0" name="2023" />
              <Bar dataKey="yield_2024" fill="#4ECDC4" name="2024" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* دقة الذكاء الاصطناعي */}
        <div className="analytics-card">
          <h3>أداء الذكاء الاصطناعي</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={aiAccuracyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis domain={[80, 100]} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="accuracy" 
                stroke="#45B7D1" 
                strokeWidth={3}
                name="دقة التشخيص (%)"
              />
              <Line 
                type="monotone" 
                dataKey="confidence" 
                stroke="#96CEB4" 
                strokeWidth={2}
                name="مستوى الثقة (%)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* تحليل التحسينات */}
        <div className="analytics-card improvement-analysis">
          <h3>تحليل التحسينات</h3>
          <div className="improvement-list">
            {cropComparisonData.map((crop, index) => (
              <div key={index} className="improvement-item">
                <div className="crop-name">{crop.crop}</div>
                <div className="improvement-bar">
                  <div 
                    className="improvement-fill" 
                    style={{ width: `${crop.improvement * 5}%` }}
                  ></div>
                </div>
                <div className="improvement-value">+{crop.improvement}%</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* تقرير التوصيات */}
      <div className="analytics-card recommendations">
        <h3>التوصيات الذكية</h3>
        <div className="recommendations-list">
          <div className="recommendation-item high-priority">
            <div className="recommendation-icon">🎯</div>
            <div className="recommendation-content">
              <h4>تحسين دقة التشخيص</h4>
              <p>يُنصح بزيادة عدد عينات التدريب للطماطم لتحسين دقة التشخيص بنسبة 3-5%</p>
            </div>
          </div>
          <div className="recommendation-item medium-priority">
            <div className="recommendation-icon">📈</div>
            <div className="recommendation-content">
              <h4>توسيع نطاق المراقبة</h4>
              <p>إضافة 5 مزارع جديدة يمكن أن يزيد من فعالية النظام ودقة التنبؤات</p>
            </div>
          </div>
          <div className="recommendation-item low-priority">
            <div className="recommendation-icon">🔧</div>
            <div className="recommendation-content">
              <h4>تحديث خوارزميات التحليل</h4>
              <p>تحديث نماذج الذكاء الاصطناعي كل 3 أشهر لضمان أفضل أداء</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedAnalytics;

