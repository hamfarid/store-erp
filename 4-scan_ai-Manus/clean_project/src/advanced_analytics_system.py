# File: /home/ubuntu/clean_project/src/advanced_analytics_system.py
"""
مسار الملف: /home/ubuntu/clean_project/src/advanced_analytics_system.py

نظام التحليلات المتقدمة وذكاء الأعمال
يوفر تحليلات شاملة ومتقدمة للبيانات مع ذكاء الأعمال
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from enum import Enum
import asyncio
import json
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# تكوين matplotlib للغة العربية
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

class AnalyticsType(Enum):
    """أنواع التحليلات"""
    DESCRIPTIVE = "descriptive"  # وصفية
    DIAGNOSTIC = "diagnostic"    # تشخيصية
    PREDICTIVE = "predictive"    # تنبؤية
    PRESCRIPTIVE = "prescriptive"  # توجيهية

class ChartType(Enum):
    """أنواع المخططات"""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    HISTOGRAM = "histogram"
    BOX = "box"
    VIOLIN = "violin"
    TREEMAP = "treemap"
    SUNBURST = "sunburst"
    GAUGE = "gauge"
    FUNNEL = "funnel"

class MetricType(Enum):
    """أنواع المقاييس"""
    COUNT = "count"
    SUM = "sum"
    AVERAGE = "average"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"
    PERCENTAGE = "percentage"
    GROWTH_RATE = "growth_rate"
    CONVERSION_RATE = "conversion_rate"

class TimeGranularity(Enum):
    """دقة الوقت"""
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"

@dataclass
class AnalyticsQuery:
    """استعلام التحليلات"""
    id: str
    name: str
    description: str
    analytics_type: AnalyticsType
    data_sources: List[str]
    metrics: List[Dict[str, Any]]
    dimensions: List[str]
    filters: Dict[str, Any] = field(default_factory=dict)
    time_range: Optional[Dict[str, Any]] = None
    granularity: TimeGranularity = TimeGranularity.DAY
    limit: Optional[int] = None
    sort_by: Optional[str] = None
    sort_order: str = "desc"

@dataclass
class AnalyticsResult:
    """نتيجة التحليل"""
    query_id: str
    data: pd.DataFrame
    metadata: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    charts: List[Dict[str, Any]]
    execution_time: float
    timestamp: datetime

@dataclass
class BusinessMetric:
    """مقياس الأعمال"""
    id: str
    name: str
    description: str
    formula: str
    category: str
    target_value: Optional[float] = None
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None
    unit: str = ""
    format_type: str = "number"

@dataclass
class Dashboard:
    """لوحة المعلومات"""
    id: str
    name: str
    description: str
    widgets: List[Dict[str, Any]]
    layout: Dict[str, Any]
    filters: Dict[str, Any] = field(default_factory=dict)
    refresh_interval: int = 300  # ثواني
    permissions: List[str] = field(default_factory=list)
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)

class DataProcessor:
    """معالج البيانات"""
    
    def __init__(self):
        self.logger = logging.getLogger('data_processor')
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """تنظيف البيانات"""
        try:
            # إزالة الصفوف المكررة
            df = df.drop_duplicates()
            
            # معالجة القيم المفقودة
            for column in df.columns:
                if df[column].dtype in ['int64', 'float64']:
                    # ملء القيم الرقمية بالمتوسط
                    df[column] = df[column].fillna(df[column].mean())
                else:
                    # ملء القيم النصية بـ "غير محدد"
                    df[column] = df[column].fillna('غير محدد')
            
            # إزالة القيم الشاذة للأعمدة الرقمية
            for column in df.select_dtypes(include=[np.number]).columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
            
            self.logger.info(f"Data cleaned: {len(df)} rows remaining")
            return df
            
        except Exception as e:
            self.logger.error(f"Error cleaning data: {e}")
            return df
    
    def aggregate_data(self, df: pd.DataFrame, group_by: List[str], 
                      metrics: List[Dict[str, Any]]) -> pd.DataFrame:
        """تجميع البيانات"""
        try:
            agg_dict = {}
            
            for metric in metrics:
                column = metric['column']
                operation = metric['operation']
                
                if operation == 'count':
                    agg_dict[f"{column}_count"] = (column, 'count')
                elif operation == 'sum':
                    agg_dict[f"{column}_sum"] = (column, 'sum')
                elif operation == 'mean':
                    agg_dict[f"{column}_avg"] = (column, 'mean')
                elif operation == 'median':
                    agg_dict[f"{column}_median"] = (column, 'median')
                elif operation == 'min':
                    agg_dict[f"{column}_min"] = (column, 'min')
                elif operation == 'max':
                    agg_dict[f"{column}_max"] = (column, 'max')
                elif operation == 'std':
                    agg_dict[f"{column}_std"] = (column, 'std')
            
            result = df.groupby(group_by).agg(agg_dict).reset_index()
            
            # تسطيح أسماء الأعمدة
            result.columns = [col[0] if col[1] == '' else col[1] for col in result.columns]
            
            self.logger.info(f"Data aggregated: {len(result)} groups")
            return result
            
        except Exception as e:
            self.logger.error(f"Error aggregating data: {e}")
            return df
    
    def calculate_time_series_metrics(self, df: pd.DataFrame, 
                                    date_column: str, value_column: str) -> Dict[str, Any]:
        """حساب مقاييس السلاسل الزمنية"""
        try:
            # تحويل عمود التاريخ
            df[date_column] = pd.to_datetime(df[date_column])
            df = df.sort_values(date_column)
            
            # حساب المقاييس
            metrics = {
                'total_value': df[value_column].sum(),
                'average_value': df[value_column].mean(),
                'median_value': df[value_column].median(),
                'min_value': df[value_column].min(),
                'max_value': df[value_column].max(),
                'std_value': df[value_column].std(),
                'growth_rate': self._calculate_growth_rate(df, value_column),
                'trend': self._calculate_trend(df, value_column),
                'seasonality': self._detect_seasonality(df, date_column, value_column),
                'volatility': df[value_column].std() / df[value_column].mean() if df[value_column].mean() != 0 else 0
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating time series metrics: {e}")
            return {}
    
    def _calculate_growth_rate(self, df: pd.DataFrame, value_column: str) -> float:
        """حساب معدل النمو"""
        try:
            if len(df) < 2:
                return 0.0
            
            first_value = df[value_column].iloc[0]
            last_value = df[value_column].iloc[-1]
            
            if first_value == 0:
                return 0.0
            
            return ((last_value - first_value) / first_value) * 100
            
        except Exception:
            return 0.0
    
    def _calculate_trend(self, df: pd.DataFrame, value_column: str) -> str:
        """تحديد الاتجاه"""
        try:
            if len(df) < 2:
                return "مستقر"
            
            # حساب الانحدار الخطي البسيط
            x = np.arange(len(df))
            y = df[value_column].values
            
            slope = np.polyfit(x, y, 1)[0]
            
            if slope > 0.1:
                return "صاعد"
            elif slope < -0.1:
                return "هابط"
            else:
                return "مستقر"
                
        except Exception:
            return "غير محدد"
    
    def _detect_seasonality(self, df: pd.DataFrame, date_column: str, value_column: str) -> bool:
        """كشف الموسمية"""
        try:
            if len(df) < 24:  # نحتاج بيانات كافية
                return False
            
            # تجميع البيانات حسب الشهر
            df['month'] = df[date_column].dt.month
            monthly_avg = df.groupby('month')[value_column].mean()
            
            # حساب معامل التباين
            cv = monthly_avg.std() / monthly_avg.mean()
            
            return cv > 0.2  # إذا كان التباين أكبر من 20%
            
        except Exception:
            return False

class ChartGenerator:
    """مولد المخططات"""
    
    def __init__(self):
        self.logger = logging.getLogger('chart_generator')
        self.color_palette = px.colors.qualitative.Set3
    
    def create_line_chart(self, df: pd.DataFrame, x_column: str, y_column: str,
                         title: str = "", **kwargs) -> Dict[str, Any]:
        """إنشاء مخطط خطي"""
        try:
            fig = px.line(df, x=x_column, y=y_column, title=title,
                         color_discrete_sequence=self.color_palette)
            
            fig.update_layout(
                font=dict(family="Arial Unicode MS, Tahoma", size=12),
                title_font_size=16,
                xaxis_title=kwargs.get('x_title', x_column),
                yaxis_title=kwargs.get('y_title', y_column)
            )
            
            return {
                'type': 'line',
                'data': fig.to_json(),
                'config': {'displayModeBar': True, 'responsive': True}
            }
            
        except Exception as e:
            self.logger.error(f"Error creating line chart: {e}")
            return {}
    
    def create_bar_chart(self, df: pd.DataFrame, x_column: str, y_column: str,
                        title: str = "", orientation: str = "v", **kwargs) -> Dict[str, Any]:
        """إنشاء مخطط أعمدة"""
        try:
            if orientation == "h":
                fig = px.bar(df, x=y_column, y=x_column, orientation='h', title=title,
                           color_discrete_sequence=self.color_palette)
            else:
                fig = px.bar(df, x=x_column, y=y_column, title=title,
                           color_discrete_sequence=self.color_palette)
            
            fig.update_layout(
                font=dict(family="Arial Unicode MS, Tahoma", size=12),
                title_font_size=16,
                xaxis_title=kwargs.get('x_title', x_column),
                yaxis_title=kwargs.get('y_title', y_column)
            )
            
            return {
                'type': 'bar',
                'data': fig.to_json(),
                'config': {'displayModeBar': True, 'responsive': True}
            }
            
        except Exception as e:
            self.logger.error(f"Error creating bar chart: {e}")
            return {}
    
    def create_pie_chart(self, df: pd.DataFrame, values_column: str, names_column: str,
                        title: str = "", **kwargs) -> Dict[str, Any]:
        """إنشاء مخطط دائري"""
        try:
            fig = px.pie(df, values=values_column, names=names_column, title=title,
                        color_discrete_sequence=self.color_palette)
            
            fig.update_layout(
                font=dict(family="Arial Unicode MS, Tahoma", size=12),
                title_font_size=16
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            return {
                'type': 'pie',
                'data': fig.to_json(),
                'config': {'displayModeBar': True, 'responsive': True}
            }
            
        except Exception as e:
            self.logger.error(f"Error creating pie chart: {e}")
            return {}
    
    def create_heatmap(self, df: pd.DataFrame, x_column: str, y_column: str, 
                      values_column: str, title: str = "", **kwargs) -> Dict[str, Any]:
        """إنشاء خريطة حرارية"""
        try:
            # تحويل البيانات إلى مصفوفة
            pivot_df = df.pivot(index=y_column, columns=x_column, values=values_column)
            
            fig = px.imshow(pivot_df, title=title, aspect="auto",
                          color_continuous_scale='RdYlBu_r')
            
            fig.update_layout(
                font=dict(family="Arial Unicode MS, Tahoma", size=12),
                title_font_size=16
            )
            
            return {
                'type': 'heatmap',
                'data': fig.to_json(),
                'config': {'displayModeBar': True, 'responsive': True}
            }
            
        except Exception as e:
            self.logger.error(f"Error creating heatmap: {e}")
            return {}
    
    def create_scatter_plot(self, df: pd.DataFrame, x_column: str, y_column: str,
                           title: str = "", size_column: str = None, 
                           color_column: str = None, **kwargs) -> Dict[str, Any]:
        """إنشاء مخطط نقطي"""
        try:
            fig = px.scatter(df, x=x_column, y=y_column, title=title,
                           size=size_column, color=color_column,
                           color_discrete_sequence=self.color_palette)
            
            fig.update_layout(
                font=dict(family="Arial Unicode MS, Tahoma", size=12),
                title_font_size=16,
                xaxis_title=kwargs.get('x_title', x_column),
                yaxis_title=kwargs.get('y_title', y_column)
            )
            
            return {
                'type': 'scatter',
                'data': fig.to_json(),
                'config': {'displayModeBar': True, 'responsive': True}
            }
            
        except Exception as e:
            self.logger.error(f"Error creating scatter plot: {e}")
            return {}
    
    def create_gauge_chart(self, value: float, title: str = "", 
                          min_value: float = 0, max_value: float = 100,
                          threshold_ranges: List[Dict] = None) -> Dict[str, Any]:
        """إنشاء مخطط مقياس"""
        try:
            if threshold_ranges is None:
                threshold_ranges = [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ]
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = value,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': title, 'font': {'size': 16}},
                delta = {'reference': (min_value + max_value) / 2},
                gauge = {
                    'axis': {'range': [min_value, max_value]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [min_value, max_value], 'color': "lightgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': max_value * 0.9
                    }
                }
            ))
            
            fig.update_layout(
                font=dict(family="Arial Unicode MS, Tahoma", size=12)
            )
            
            return {
                'type': 'gauge',
                'data': fig.to_json(),
                'config': {'displayModeBar': True, 'responsive': True}
            }
            
        except Exception as e:
            self.logger.error(f"Error creating gauge chart: {e}")
            return {}
    
    def create_funnel_chart(self, df: pd.DataFrame, values_column: str, 
                           stages_column: str, title: str = "") -> Dict[str, Any]:
        """إنشاء مخطط قمع"""
        try:
            fig = go.Figure(go.Funnel(
                y = df[stages_column],
                x = df[values_column],
                textinfo = "value+percent initial"
            ))
            
            fig.update_layout(
                title=title,
                font=dict(family="Arial Unicode MS, Tahoma", size=12),
                title_font_size=16
            )
            
            return {
                'type': 'funnel',
                'data': fig.to_json(),
                'config': {'displayModeBar': True, 'responsive': True}
            }
            
        except Exception as e:
            self.logger.error(f"Error creating funnel chart: {e}")
            return {}

class InsightGenerator:
    """مولد الرؤى والتوصيات"""
    
    def __init__(self):
        self.logger = logging.getLogger('insight_generator')
    
    def generate_insights(self, df: pd.DataFrame, metrics: Dict[str, Any]) -> List[str]:
        """توليد الرؤى"""
        insights = []
        
        try:
            # رؤى حول الاتجاهات
            if 'trend' in metrics:
                trend = metrics['trend']
                if trend == "صاعد":
                    insights.append("📈 يظهر البيانات اتجاهاً صاعداً إيجابياً")
                elif trend == "هابط":
                    insights.append("📉 يظهر البيانات اتجاهاً هابطاً يحتاج انتباه")
                else:
                    insights.append("📊 البيانات تظهر استقراراً نسبياً")
            
            # رؤى حول النمو
            if 'growth_rate' in metrics:
                growth = metrics['growth_rate']
                if growth > 10:
                    insights.append(f"🚀 معدل نمو ممتاز: {growth:.1f}%")
                elif growth > 0:
                    insights.append(f"📈 نمو إيجابي: {growth:.1f}%")
                elif growth < -10:
                    insights.append(f"⚠️ انخفاض كبير: {growth:.1f}%")
                else:
                    insights.append(f"📊 تغيير طفيف: {growth:.1f}%")
            
            # رؤى حول التقلبات
            if 'volatility' in metrics:
                volatility = metrics['volatility']
                if volatility > 0.5:
                    insights.append("⚡ البيانات تظهر تقلبات عالية")
                elif volatility > 0.2:
                    insights.append("📊 البيانات تظهر تقلبات متوسطة")
                else:
                    insights.append("✅ البيانات مستقرة نسبياً")
            
            # رؤى حول الموسمية
            if 'seasonality' in metrics and metrics['seasonality']:
                insights.append("🔄 تم اكتشاف نمط موسمي في البيانات")
            
            # رؤى حول التوزيع
            if len(df) > 0:
                numeric_columns = df.select_dtypes(include=[np.number]).columns
                for col in numeric_columns:
                    skewness = df[col].skew()
                    if abs(skewness) > 1:
                        if skewness > 0:
                            insights.append(f"📊 {col}: توزيع منحرف إلى اليمين")
                        else:
                            insights.append(f"📊 {col}: توزيع منحرف إلى اليسار")
            
            # رؤى حول القيم الشاذة
            outliers_count = self._detect_outliers_count(df)
            if outliers_count > 0:
                insights.append(f"⚠️ تم اكتشاف {outliers_count} قيمة شاذة")
            
            return insights[:10]  # أقصى 10 رؤى
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {e}")
            return ["❌ خطأ في توليد الرؤى"]
    
    def generate_recommendations(self, df: pd.DataFrame, metrics: Dict[str, Any]) -> List[str]:
        """توليد التوصيات"""
        recommendations = []
        
        try:
            # توصيات بناءً على الاتجاه
            if 'trend' in metrics:
                trend = metrics['trend']
                if trend == "هابط":
                    recommendations.append("🔍 يُنصح بتحليل أسباب الانخفاض واتخاذ إجراءات تصحيحية")
                    recommendations.append("📋 مراجعة الاستراتيجيات الحالية وتطوير خطط تحسين")
                elif trend == "صاعد":
                    recommendations.append("💪 الاستمرار في الاستراتيجيات الحالية الناجحة")
                    recommendations.append("📈 استكشاف فرص التوسع والنمو")
            
            # توصيات بناءً على التقلبات
            if 'volatility' in metrics:
                volatility = metrics['volatility']
                if volatility > 0.5:
                    recommendations.append("⚖️ تطبيق استراتيجيات لتقليل التقلبات")
                    recommendations.append("📊 زيادة تكرار المراقبة والتحليل")
            
            # توصيات بناءً على الموسمية
            if 'seasonality' in metrics and metrics['seasonality']:
                recommendations.append("📅 تطوير خطط موسمية للاستفادة من الأنماط المكتشفة")
                recommendations.append("🎯 تخصيص الموارد بناءً على التوقعات الموسمية")
            
            # توصيات بناءً على جودة البيانات
            missing_data_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
            if missing_data_ratio > 0.1:
                recommendations.append("🔧 تحسين جودة البيانات وتقليل القيم المفقودة")
                recommendations.append("📝 مراجعة عمليات جمع وإدخال البيانات")
            
            # توصيات عامة
            recommendations.append("📊 إجراء تحليلات دورية لمتابعة التطورات")
            recommendations.append("🎯 تحديد مؤشرات أداء رئيسية (KPIs) للمراقبة المستمرة")
            
            return recommendations[:8]  # أقصى 8 توصيات
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return ["❌ خطأ في توليد التوصيات"]
    
    def _detect_outliers_count(self, df: pd.DataFrame) -> int:
        """عد القيم الشاذة"""
        try:
            outliers_count = 0
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            
            for column in numeric_columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
                outliers_count += len(outliers)
            
            return outliers_count
            
        except Exception:
            return 0

class BusinessIntelligenceEngine:
    """محرك ذكاء الأعمال"""
    
    def __init__(self):
        self.data_processor = DataProcessor()
        self.chart_generator = ChartGenerator()
        self.insight_generator = InsightGenerator()
        self.logger = logging.getLogger('business_intelligence_engine')
        self.metrics_registry = {}
        self.dashboards = {}
    
    def register_business_metric(self, metric: BusinessMetric):
        """تسجيل مقياس أعمال"""
        self.metrics_registry[metric.id] = metric
        self.logger.info(f"Business metric registered: {metric.name}")
    
    def create_dashboard(self, dashboard: Dashboard):
        """إنشاء لوحة معلومات"""
        self.dashboards[dashboard.id] = dashboard
        self.logger.info(f"Dashboard created: {dashboard.name}")
    
    async def execute_analytics_query(self, query: AnalyticsQuery) -> AnalyticsResult:
        """تنفيذ استعلام تحليلي"""
        start_time = datetime.now()
        
        try:
            # جلب البيانات
            df = await self._fetch_data(query.data_sources, query.filters, query.time_range)
            
            if df.empty:
                return AnalyticsResult(
                    query_id=query.id,
                    data=df,
                    metadata={'error': 'لا توجد بيانات متاحة'},
                    insights=[],
                    recommendations=[],
                    charts=[],
                    execution_time=0,
                    timestamp=datetime.now()
                )
            
            # تنظيف البيانات
            df = self.data_processor.clean_data(df)
            
            # تطبيق المرشحات
            df = self._apply_filters(df, query.filters)
            
            # تجميع البيانات
            if query.dimensions:
                df = self.data_processor.aggregate_data(df, query.dimensions, query.metrics)
            
            # ترتيب البيانات
            if query.sort_by:
                df = df.sort_values(query.sort_by, ascending=(query.sort_order == 'asc'))
            
            # تحديد عدد النتائج
            if query.limit:
                df = df.head(query.limit)
            
            # حساب المقاييس
            metrics = {}
            if len(df) > 0 and any(col for col in df.columns if df[col].dtype in ['int64', 'float64']):
                numeric_column = df.select_dtypes(include=[np.number]).columns[0]
                if 'date' in df.columns or 'timestamp' in df.columns:
                    date_column = 'date' if 'date' in df.columns else 'timestamp'
                    metrics = self.data_processor.calculate_time_series_metrics(df, date_column, numeric_column)
            
            # توليد المخططات
            charts = await self._generate_charts(df, query)
            
            # توليد الرؤى والتوصيات
            insights = self.insight_generator.generate_insights(df, metrics)
            recommendations = self.insight_generator.generate_recommendations(df, metrics)
            
            # حساب وقت التنفيذ
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AnalyticsResult(
                query_id=query.id,
                data=df,
                metadata={
                    'row_count': len(df),
                    'column_count': len(df.columns),
                    'metrics': metrics,
                    'data_sources': query.data_sources
                },
                insights=insights,
                recommendations=recommendations,
                charts=charts,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error executing analytics query {query.id}: {e}")
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AnalyticsResult(
                query_id=query.id,
                data=pd.DataFrame(),
                metadata={'error': str(e)},
                insights=[f"❌ خطأ في تنفيذ الاستعلام: {str(e)}"],
                recommendations=["🔧 يُرجى مراجعة معايير الاستعلام والمحاولة مرة أخرى"],
                charts=[],
                execution_time=execution_time,
                timestamp=datetime.now()
            )
    
    async def _fetch_data(self, data_sources: List[str], filters: Dict[str, Any], 
                         time_range: Optional[Dict[str, Any]]) -> pd.DataFrame:
        """جلب البيانات من المصادر"""
        try:
            # هنا يمكن تطبيق منطق جلب البيانات الفعلي من قواعد البيانات
            # للتجربة، سننشئ بيانات وهمية
            
            np.random.seed(42)
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
            
            data = {
                'date': dates,
                'sales': np.random.normal(1000, 200, len(dates)) + np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 100,
                'customers': np.random.poisson(50, len(dates)),
                'revenue': np.random.normal(5000, 1000, len(dates)),
                'category': np.random.choice(['A', 'B', 'C'], len(dates)),
                'region': np.random.choice(['الشمال', 'الجنوب', 'الشرق', 'الغرب'], len(dates))
            }
            
            df = pd.DataFrame(data)
            
            # تطبيق نطاق زمني إذا كان محدداً
            if time_range:
                start_date = time_range.get('start_date')
                end_date = time_range.get('end_date')
                
                if start_date:
                    df = df[df['date'] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df['date'] <= pd.to_datetime(end_date)]
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching data: {e}")
            return pd.DataFrame()
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """تطبيق المرشحات"""
        try:
            for column, filter_value in filters.items():
                if column in df.columns:
                    if isinstance(filter_value, list):
                        df = df[df[column].isin(filter_value)]
                    elif isinstance(filter_value, dict):
                        if 'min' in filter_value:
                            df = df[df[column] >= filter_value['min']]
                        if 'max' in filter_value:
                            df = df[df[column] <= filter_value['max']]
                    else:
                        df = df[df[column] == filter_value]
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error applying filters: {e}")
            return df
    
    async def _generate_charts(self, df: pd.DataFrame, query: AnalyticsQuery) -> List[Dict[str, Any]]:
        """توليد المخططات"""
        charts = []
        
        try:
            if len(df) == 0:
                return charts
            
            # مخطط خطي للبيانات الزمنية
            if 'date' in df.columns and len(df.select_dtypes(include=[np.number]).columns) > 0:
                numeric_col = df.select_dtypes(include=[np.number]).columns[0]
                chart = self.chart_generator.create_line_chart(
                    df, 'date', numeric_col, 
                    title=f"اتجاه {numeric_col} عبر الزمن"
                )
                if chart:
                    charts.append(chart)
            
            # مخطط أعمدة للفئات
            categorical_cols = df.select_dtypes(include=['object']).columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                cat_col = categorical_cols[0]
                num_col = numeric_cols[0]
                
                # تجميع البيانات للمخطط
                grouped_df = df.groupby(cat_col)[num_col].sum().reset_index()
                
                chart = self.chart_generator.create_bar_chart(
                    grouped_df, cat_col, num_col,
                    title=f"توزيع {num_col} حسب {cat_col}"
                )
                if chart:
                    charts.append(chart)
                
                # مخطط دائري إذا كان عدد الفئات قليل
                if len(grouped_df) <= 10:
                    chart = self.chart_generator.create_pie_chart(
                        grouped_df, num_col, cat_col,
                        title=f"نسب {num_col} حسب {cat_col}"
                    )
                    if chart:
                        charts.append(chart)
            
            # مخطط نقطي للعلاقات
            if len(numeric_cols) >= 2:
                chart = self.chart_generator.create_scatter_plot(
                    df, numeric_cols[0], numeric_cols[1],
                    title=f"العلاقة بين {numeric_cols[0]} و {numeric_cols[1]}"
                )
                if chart:
                    charts.append(chart)
            
            return charts[:5]  # أقصى 5 مخططات
            
        except Exception as e:
            self.logger.error(f"Error generating charts: {e}")
            return charts
    
    async def calculate_business_metric(self, metric_id: str, 
                                      data_context: Dict[str, Any]) -> Dict[str, Any]:
        """حساب مقياس أعمال"""
        try:
            if metric_id not in self.metrics_registry:
                return {'error': f'مقياس غير موجود: {metric_id}'}
            
            metric = self.metrics_registry[metric_id]
            
            # هنا يمكن تطبيق منطق حساب المقياس بناءً على الصيغة
            # للتجربة، سنحسب قيماً وهمية
            
            value = np.random.uniform(0, 100)
            
            # تحديد حالة المقياس
            status = "normal"
            if metric.threshold_critical and value <= metric.threshold_critical:
                status = "critical"
            elif metric.threshold_warning and value <= metric.threshold_warning:
                status = "warning"
            elif metric.target_value and value >= metric.target_value:
                status = "excellent"
            
            return {
                'metric_id': metric_id,
                'name': metric.name,
                'value': value,
                'unit': metric.unit,
                'status': status,
                'target_value': metric.target_value,
                'calculated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating business metric {metric_id}: {e}")
            return {'error': str(e)}
    
    async def generate_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """توليد بيانات لوحة المعلومات"""
        try:
            if dashboard_id not in self.dashboards:
                return {'error': f'لوحة معلومات غير موجودة: {dashboard_id}'}
            
            dashboard = self.dashboards[dashboard_id]
            dashboard_data = {
                'id': dashboard.id,
                'name': dashboard.name,
                'description': dashboard.description,
                'widgets': [],
                'generated_at': datetime.now().isoformat()
            }
            
            # توليد بيانات كل widget
            for widget in dashboard.widgets:
                widget_data = await self._generate_widget_data(widget)
                dashboard_data['widgets'].append(widget_data)
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Error generating dashboard data {dashboard_id}: {e}")
            return {'error': str(e)}
    
    async def _generate_widget_data(self, widget: Dict[str, Any]) -> Dict[str, Any]:
        """توليد بيانات widget"""
        try:
            widget_type = widget.get('type')
            
            if widget_type == 'metric':
                # widget مقياس
                metric_id = widget.get('metric_id')
                if metric_id:
                    metric_data = await self.calculate_business_metric(metric_id, {})
                    return {
                        'type': 'metric',
                        'title': widget.get('title', ''),
                        'data': metric_data
                    }
            
            elif widget_type == 'chart':
                # widget مخطط
                query_config = widget.get('query')
                if query_config:
                    query = AnalyticsQuery(**query_config)
                    result = await self.execute_analytics_query(query)
                    
                    return {
                        'type': 'chart',
                        'title': widget.get('title', ''),
                        'data': {
                            'charts': result.charts,
                            'insights': result.insights[:3],  # أول 3 رؤى
                            'metadata': result.metadata
                        }
                    }
            
            elif widget_type == 'table':
                # widget جدول
                query_config = widget.get('query')
                if query_config:
                    query = AnalyticsQuery(**query_config)
                    result = await self.execute_analytics_query(query)
                    
                    return {
                        'type': 'table',
                        'title': widget.get('title', ''),
                        'data': {
                            'columns': result.data.columns.tolist(),
                            'rows': result.data.to_dict('records'),
                            'total_rows': len(result.data)
                        }
                    }
            
            return {
                'type': widget_type,
                'title': widget.get('title', ''),
                'data': {'error': 'نوع widget غير مدعوم'}
            }
            
        except Exception as e:
            self.logger.error(f"Error generating widget data: {e}")
            return {
                'type': widget.get('type', 'unknown'),
                'title': widget.get('title', ''),
                'data': {'error': str(e)}
            }

# مثيل عام لمحرك ذكاء الأعمال
business_intelligence_engine = BusinessIntelligenceEngine()

# تسجيل مقاييس الأعمال الأساسية
default_metrics = [
    BusinessMetric(
        id="total_sales",
        name="إجمالي المبيعات",
        description="إجمالي قيمة المبيعات",
        formula="SUM(sales_amount)",
        category="مبيعات",
        unit="ريال",
        format_type="currency"
    ),
    BusinessMetric(
        id="customer_count",
        name="عدد العملاء",
        description="إجمالي عدد العملاء",
        formula="COUNT(DISTINCT customer_id)",
        category="عملاء",
        unit="عميل",
        format_type="number"
    ),
    BusinessMetric(
        id="conversion_rate",
        name="معدل التحويل",
        description="نسبة تحويل الزوار إلى عملاء",
        formula="(conversions / visitors) * 100",
        category="تسويق",
        target_value=5.0,
        threshold_warning=3.0,
        threshold_critical=1.0,
        unit="%",
        format_type="percentage"
    ),
    BusinessMetric(
        id="avg_order_value",
        name="متوسط قيمة الطلب",
        description="متوسط قيمة الطلب الواحد",
        formula="SUM(order_value) / COUNT(orders)",
        category="مبيعات",
        unit="ريال",
        format_type="currency"
    )
]

# تسجيل المقاييس
for metric in default_metrics:
    business_intelligence_engine.register_business_metric(metric)

# دوال مساعدة
async def create_analytics_query(name: str, data_sources: List[str], 
                               metrics: List[Dict[str, Any]], 
                               dimensions: List[str] = None,
                               filters: Dict[str, Any] = None) -> str:
    """إنشاء استعلام تحليلي"""
    query = AnalyticsQuery(
        id=f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        name=name,
        description=f"استعلام تحليلي: {name}",
        analytics_type=AnalyticsType.DESCRIPTIVE,
        data_sources=data_sources,
        metrics=metrics,
        dimensions=dimensions or [],
        filters=filters or {}
    )
    
    return query.id

async def execute_business_analysis(query_id: str) -> Dict[str, Any]:
    """تنفيذ تحليل أعمال"""
    # إنشاء استعلام تجريبي
    query = AnalyticsQuery(
        id=query_id,
        name="تحليل المبيعات",
        description="تحليل شامل للمبيعات",
        analytics_type=AnalyticsType.DESCRIPTIVE,
        data_sources=["sales", "customers"],
        metrics=[
            {"column": "sales", "operation": "sum"},
            {"column": "customers", "operation": "count"}
        ],
        dimensions=["region", "category"]
    )
    
    result = await business_intelligence_engine.execute_analytics_query(query)
    
    return {
        'query_id': result.query_id,
        'data_summary': {
            'rows': len(result.data),
            'columns': len(result.data.columns) if not result.data.empty else 0
        },
        'insights': result.insights,
        'recommendations': result.recommendations,
        'charts_count': len(result.charts),
        'execution_time': result.execution_time,
        'timestamp': result.timestamp.isoformat()
    }

if __name__ == "__main__":
    # مثال على الاستخدام
    async def main():
        # إنشاء استعلام تحليلي
        query_id = await create_analytics_query(
            name="تحليل المبيعات الشهرية",
            data_sources=["sales"],
            metrics=[{"column": "revenue", "operation": "sum"}],
            dimensions=["month", "region"]
        )
        
        # تنفيذ التحليل
        result = await execute_business_analysis(query_id)
        print(f"نتائج التحليل: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # حساب مقياس أعمال
        metric_result = await business_intelligence_engine.calculate_business_metric("total_sales", {})
        print(f"مقياس المبيعات: {json.dumps(metric_result, indent=2, ensure_ascii=False)}")
    
    asyncio.run(main())

