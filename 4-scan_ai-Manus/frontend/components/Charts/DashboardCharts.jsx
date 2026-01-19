// ملف: /home/ubuntu/gaara_development/gaara_ai_integrated/frontend/src/components/Charts/DashboardCharts.jsx
import React from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

// بيانات تجريبية للرسوم البيانية
const farmProductionData = [
  { month: 'يناير', production: 4000, target: 4500 },
  { month: 'فبراير', production: 3000, target: 3200 },
  { month: 'مارس', production: 5000, target: 4800 },
  { month: 'أبريل', production: 4500, target: 4200 },
  { month: 'مايو', production: 6000, target: 5500 },
  { month: 'يونيو', production: 5500, target: 5800 }
];

const diseaseDistributionData = [
  { name: 'البياض الدقيقي', value: 35, color: '#FF6B6B' },
  { name: 'تبقع الأوراق', value: 25, color: '#4ECDC4' },
  { name: 'العفن الرمادي', value: 20, color: '#45B7D1' },
  { name: 'الذبول البكتيري', value: 15, color: '#96CEB4' },
  { name: 'أخرى', value: 5, color: '#FFEAA7' }
];

const cropHealthData = [
  { crop: 'الطماطم', healthy: 85, diseased: 15 },
  { crop: 'الخيار', healthy: 92, diseased: 8 },
  { crop: 'الفلفل', healthy: 78, diseased: 22 },
  { crop: 'الباذنجان', healthy: 88, diseased: 12 },
  { crop: 'الكوسا', healthy: 95, diseased: 5 }
];

const monthlyDiagnosisData = [
  { month: 'يناير', diagnoses: 120 },
  { month: 'فبراير', diagnoses: 98 },
  { month: 'مارس', diagnoses: 156 },
  { month: 'أبريل', diagnoses: 134 },
  { month: 'مايو', diagnoses: 189 },
  { month: 'يونيو', diagnoses: 167 }
];

// مكون الرسم البياني الخطي للإنتاج
export const ProductionChart = ({ data = farmProductionData }) => (
  <div className="chart-container">
    <h3 className="chart-title">إنتاج المزارع الشهري</h3>
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line 
          type="monotone" 
          dataKey="production" 
          stroke="#4ECDC4" 
          strokeWidth={3}
          name="الإنتاج الفعلي"
        />
        <Line 
          type="monotone" 
          dataKey="target" 
          stroke="#FF6B6B" 
          strokeWidth={2}
          strokeDasharray="5 5"
          name="الهدف المطلوب"
        />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

// مكون الرسم البياني الدائري لتوزيع الأمراض
export const DiseaseDistributionChart = ({ data = diseaseDistributionData }) => (
  <div className="chart-container">
    <h3 className="chart-title">توزيع الأمراض النباتية</h3>
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  </div>
);

// مكون الرسم البياني العمودي لصحة المحاصيل
export const CropHealthChart = ({ data = cropHealthData }) => (
  <div className="chart-container">
    <h3 className="chart-title">حالة صحة المحاصيل</h3>
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="crop" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="healthy" stackId="a" fill="#96CEB4" name="سليم" />
        <Bar dataKey="diseased" stackId="a" fill="#FF6B6B" name="مصاب" />
      </BarChart>
    </ResponsiveContainer>
  </div>
);

// مكون الرسم البياني المساحي للتشخيصات الشهرية
export const MonthlyDiagnosisChart = ({ data = monthlyDiagnosisData }) => (
  <div className="chart-container">
    <h3 className="chart-title">التشخيصات الشهرية</h3>
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Area 
          type="monotone" 
          dataKey="diagnoses" 
          stroke="#45B7D1" 
          fill="#45B7D1" 
          fillOpacity={0.6}
          name="عدد التشخيصات"
        />
      </AreaChart>
    </ResponsiveContainer>
  </div>
);

// مكون شامل يجمع جميع الرسوم البيانية
export const DashboardCharts = () => (
  <div className="dashboard-charts">
    <div className="charts-grid">
      <div className="chart-item">
        <ProductionChart />
      </div>
      <div className="chart-item">
        <DiseaseDistributionChart />
      </div>
      <div className="chart-item">
        <CropHealthChart />
      </div>
      <div className="chart-item">
        <MonthlyDiagnosisChart />
      </div>
    </div>
  </div>
);

export default DashboardCharts;

