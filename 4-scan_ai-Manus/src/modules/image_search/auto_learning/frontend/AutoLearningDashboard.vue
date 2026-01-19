# /home/ubuntu/image_search_integration/auto_learning/frontend/AutoLearningDashboard.vue
<template>
  <div class="auto-learning-dashboard">
    <div class="dashboard-header">
      <h1>{{ $t('لوحة تحكم البحث الذاتي الذكي') }}</h1>
      <div class="dashboard-actions">
        <el-button type="primary" @click="refreshData">
          <i class="el-icon-refresh"></i> {{ $t('تحديث') }}
        </el-button>
        <el-button type="success" @click="openSettings">
          <i class="el-icon-setting"></i> {{ $t('الإعدادات') }}
        </el-button>
      </div>
    </div>

    <el-row :gutter="20" class="dashboard-stats">
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="stat-card">
          <div class="stat-icon">
            <i class="el-icon-key"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.keywords.total }}</div>
            <div class="stat-label">{{ $t('الكلمات المفتاحية') }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="stat-card">
          <div class="stat-icon">
            <i class="el-icon-link"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.sources.total }}</div>
            <div class="stat-label">{{ $t('المصادر الموثوقة') }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="stat-card">
          <div class="stat-icon">
            <i class="el-icon-search"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.searchEngines.total }}</div>
            <div class="stat-label">{{ $t('محركات البحث') }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="stat-card">
          <div class="stat-icon">
            <i class="el-icon-data-analysis"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.searches.total }}</div>
            <div class="stat-label">{{ $t('عمليات البحث') }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-tabs v-model="activeTab" class="dashboard-tabs">
      <el-tab-pane :label="$t('الكلمات المفتاحية')" name="keywords">
        <KeywordManager />
      </el-tab-pane>
      <el-tab-pane :label="$t('المصادر الموثوقة')" name="sources">
        <SourceManager />
      </el-tab-pane>
      <el-tab-pane :label="$t('محركات البحث')" name="searchEngines">
        <SearchEngineManager />
      </el-tab-pane>
      <el-tab-pane :label="$t('التقارير والإحصائيات')" name="reports">
        <div class="reports-container">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card class="chart-card">
                <div slot="header" class="chart-header">
                  <span>{{ $t('أداء الكلمات المفتاحية') }}</span>
                </div>
                <KeywordPerformanceChart :data="keywordPerformanceData" />
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <div slot="header" class="chart-header">
                  <span>{{ $t('موثوقية المصادر') }}</span>
                </div>
                <SourceReliabilityChart :data="sourceReliabilityData" />
              </el-card>
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="12">
              <el-card class="chart-card">
                <div slot="header" class="chart-header">
                  <span>{{ $t('أداء محركات البحث') }}</span>
                </div>
                <SearchEnginePerformanceChart :data="searchEnginePerformanceData" />
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <div slot="header" class="chart-header">
                  <span>{{ $t('توزيع عمليات البحث') }}</span>
                </div>
                <SearchDistributionChart :data="searchDistributionData" />
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      :title="$t('إعدادات البحث الذاتي الذكي')"
      :visible.sync="settingsDialogVisible"
      width="60%"
    >
      <AutoLearningSettings @close="settingsDialogVisible = false" />
    </el-dialog>
  </div>
</template>

<script>
import KeywordManager from './KeywordManager.vue';
import SourceManager from './SourceManager.vue';
import SearchEngineManager from './SearchEngineManager.vue';
import AutoLearningSettings from './AutoLearningSettings.vue';
import KeywordPerformanceChart from './charts/KeywordPerformanceChart.vue';
import SourceReliabilityChart from './charts/SourceReliabilityChart.vue';
import SearchEnginePerformanceChart from './charts/SearchEnginePerformanceChart.vue';
import SearchDistributionChart from './charts/SearchDistributionChart.vue';
import { ApiService } from '../services/ApiService';

export default {
  name: 'AutoLearningDashboard',
  components: {
    KeywordManager,
    SourceManager,
    SearchEngineManager,
    AutoLearningSettings,
    KeywordPerformanceChart,
    SourceReliabilityChart,
    SearchEnginePerformanceChart,
    SearchDistributionChart
  },
  data() {
    return {
      activeTab: 'keywords',
      settingsDialogVisible: false,
      stats: {
        keywords: {
          total: 0
        },
        sources: {
          total: 0,
          verified: 0,
          blacklisted: 0
        },
        searchEngines: {
          total: 0,
          active: 0
        },
        searches: {
          total: 0,
          successful: 0,
          failed: 0
        }
      },
      keywordPerformanceData: [],
      sourceReliabilityData: [],
      searchEnginePerformanceData: [],
      searchDistributionData: []
    };
  },
  created() {
    this.fetchStats();
    this.fetchChartData();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await ApiService.get('/auto_learning/stats');
        this.stats = response.data;
      } catch (error) {
        console.error('Error fetching stats:', error);
        this.$message.error(this.$t('حدث خطأ أثناء جلب الإحصائيات'));
      }
    },
    async fetchChartData() {
      try {
        const [keywordResponse, sourceResponse, engineResponse, searchResponse] = await Promise.all([
          ApiService.get('/auto_learning/keywords/performance'),
          ApiService.get('/auto_learning/sources/reliability'),
          ApiService.get('/auto_learning/search_engines/performance'),
          ApiService.get('/auto_learning/searches/distribution')
        ]);
        
        this.keywordPerformanceData = keywordResponse.data;
        this.sourceReliabilityData = sourceResponse.data;
        this.searchEnginePerformanceData = engineResponse.data;
        this.searchDistributionData = searchResponse.data;
      } catch (error) {
        console.error('Error fetching chart data:', error);
        this.$message.error(this.$t('حدث خطأ أثناء جلب بيانات الرسوم البيانية'));
      }
    },
    refreshData() {
      this.fetchStats();
      this.fetchChartData();
      this.$message.success(this.$t('تم تحديث البيانات بنجاح'));
    },
    openSettings() {
      this.settingsDialogVisible = true;
    }
  }
};
</script>

<style lang="scss" scoped>
.auto-learning-dashboard {
  padding: 20px;
  font-family: 'Cairo', sans-serif;
  
  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h1 {
      margin: 0;
      color: #2c3e50;
      font-size: 24px;
    }
    
    .dashboard-actions {
      display: flex;
      gap: 10px;
    }
  }
  
  .dashboard-stats {
    margin-bottom: 30px;
    
    .stat-card {
      height: 120px;
      display: flex;
      align-items: center;
      
      .stat-icon {
        font-size: 40px;
        color: #409EFF;
        margin-right: 20px;
      }
      
      .stat-content {
        .stat-value {
          font-size: 28px;
          font-weight: bold;
          color: #2c3e50;
        }
        
        .stat-label {
          font-size: 14px;
          color: #606266;
        }
      }
    }
  }
  
  .dashboard-tabs {
    .reports-container {
      margin-top: 20px;
      
      .chart-card {
        margin-bottom: 20px;
        
        .chart-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
      }
    }
  }
}

/* RTL Support */
[dir="rtl"] {
  .auto-learning-dashboard {
    .stat-card {
      .stat-icon {
        margin-right: 0;
        margin-left: 20px;
      }
    }
  }
}
</style>
