<template>
  <div class="hybridization-dashboard-container">
    <h1 class="dashboard-title">{{ $t('hybridization.dashboard') }}</h1>
    
    <v-row>
      <v-col cols="12" md="6" lg="3">
        <v-card class="dashboard-card">
          <v-card-text class="text-center">
            <v-icon size="48" color="green">mdi-sprout</v-icon>
            <div class="stat-value">{{ stats.totalExperiments }}</div>
            <div class="stat-label">{{ $t('hybridization.totalExperiments') }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6" lg="3">
        <v-card class="dashboard-card">
          <v-card-text class="text-center">
            <v-icon size="48" color="blue">mdi-flask</v-icon>
            <div class="stat-value">{{ stats.activeExperiments }}</div>
            <div class="stat-label">{{ $t('hybridization.activeExperiments') }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6" lg="3">
        <v-card class="dashboard-card">
          <v-card-text class="text-center">
            <v-icon size="48" color="orange">mdi-dna</v-icon>
            <div class="stat-value">{{ stats.totalStrains }}</div>
            <div class="stat-label">{{ $t('hybridization.totalStrains') }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6" lg="3">
        <v-card class="dashboard-card">
          <v-card-text class="text-center">
            <v-icon size="48" color="purple">mdi-check-decagram</v-icon>
            <div class="stat-value">{{ stats.successRate }}%</div>
            <div class="stat-label">{{ $t('hybridization.successRate') }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('hybridization.experimentsByStatus') }}</v-card-title>
          <v-card-text>
            <canvas ref="statusChart"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('hybridization.experimentsByType') }}</v-card-title>
          <v-card-text>
            <canvas ref="typeChart"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>{{ $t('hybridization.experimentTrend') }}</v-card-title>
          <v-card-text>
            <canvas ref="trendChart"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between">
            <span>{{ $t('hybridization.recentExperiments') }}</span>
            <v-btn
              text
              color="primary"
              :to="{ name: 'hybridization-list' }"
            >
              {{ $t('hybridization.viewAll') }}
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-title>
          
          <v-data-table
            :headers="headers"
            :items="recentExperiments"
            :items-per-page="5"
            class="elevation-0"
          >
            <template v-slot:item.type="{ item }">
              <v-chip
                small
                :color="getTypeColor(item.type)"
                text-color="white"
              >
                {{ getTypeLabel(item.type) }}
              </v-chip>
            </template>
            
            <template v-slot:item.status="{ item }">
              <v-chip
                small
                :color="getStatusColor(item.status)"
                text-color="white"
              >
                {{ getStatusLabel(item.status) }}
              </v-chip>
            </template>
            
            <template v-slot:item.start_date="{ item }">
              {{ formatDate(item.start_date) }}
            </template>
            
            <template v-slot:item.actions="{ item }">
              <v-btn
                small
                text
                color="primary"
                :to="{ name: 'hybridization-details', params: { id: item.id } }"
              >
                {{ $t('hybridization.view') }}
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('hybridization.topStrains') }}</v-card-title>
          <v-list>
            <v-list-item
              v-for="(strain, index) in stats.topStrains"
              :key="index"
            >
              <v-list-item-avatar>
                <v-avatar color="green" size="40">
                  <v-icon dark>mdi-sprout</v-icon>
                </v-avatar>
              </v-list-item-avatar>
              
              <v-list-item-content>
                <v-list-item-title>{{ strain.name }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ $t('hybridization.successCount') }}: {{ strain.success_count }} | 
                  {{ $t('hybridization.usageCount') }}: {{ strain.usage_count }}
                </v-list-item-subtitle>
              </v-list-item-content>
              
              <v-list-item-action>
                <v-btn
                  icon
                  small
                  :to="{ name: 'strain-details', params: { id: strain.id } }"
                >
                  <v-icon>mdi-information-outline</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('hybridization.upcomingHarvests') }}</v-card-title>
          <v-list>
            <v-list-item
              v-for="(harvest, index) in stats.upcomingHarvests"
              :key="index"
            >
              <v-list-item-avatar>
                <v-avatar color="amber" size="40">
                  <v-icon dark>mdi-calendar-clock</v-icon>
                </v-avatar>
              </v-list-item-avatar>
              
              <v-list-item-content>
                <v-list-item-title>{{ harvest.experiment_name }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ $t('hybridization.harvestDate') }}: {{ formatDate(harvest.harvest_date) }}
                </v-list-item-subtitle>
              </v-list-item-content>
              
              <v-list-item-action>
                <v-btn
                  icon
                  small
                  :to="{ name: 'hybridization-details', params: { id: harvest.experiment_id } }"
                >
                  <v-icon>mdi-arrow-right</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>{{ $t('hybridization.quickActions') }}</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="primary"
                  class="mb-2"
                  :to="{ name: 'hybridization-form' }"
                >
                  <v-icon left>mdi-plus</v-icon>
                  {{ $t('hybridization.newExperiment') }}
                </v-btn>
              </v-col>
              
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="secondary"
                  class="mb-2"
                  :to="{ name: 'strain-management' }"
                >
                  <v-icon left>mdi-dna</v-icon>
                  {{ $t('hybridization.manageStrains') }}
                </v-btn>
              </v-col>
              
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="info"
                  class="mb-2"
                  :to="{ name: 'hybridization-reports' }"
                >
                  <v-icon left>mdi-file-chart</v-icon>
                  {{ $t('hybridization.reports') }}
                </v-btn>
              </v-col>
              
              <v-col cols="12" sm="6" md="3">
                <v-btn
                  block
                  color="success"
                  class="mb-2"
                  :to="{ name: 'hybridization-calendar' }"
                >
                  <v-icon left>mdi-calendar</v-icon>
                  {{ $t('hybridization.calendar') }}
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

/**
 * @component HybridizationDashboard
 * @description A dashboard component for displaying plant hybridization statistics and analytics.
 * This component provides an overview of hybridization experiments with charts, statistics,
 * and a list of recent experiments.
 */
export default {
  name: 'HybridizationDashboard',
  
  data() {
    return {
      /**
       * Loading state
       * @type {Boolean}
       */
      loading: false,
      
      /**
       * Hybridization statistics
       * @type {Object}
       * @property {Number} totalExperiments - Total number of hybridization experiments
       * @property {Number} activeExperiments - Number of active experiments
       * @property {Number} totalStrains - Total number of plant strains
       * @property {Number} successRate - Success rate percentage
       * @property {Array} topStrains - List of top performing strains
       * @property {Array} upcomingHarvests - List of upcoming harvests
       */
      stats: {
        totalExperiments: 0,
        activeExperiments: 0,
        totalStrains: 0,
        successRate: 0,
        topStrains: [],
        upcomingHarvests: []
      },
      
      /**
       * Recent experiments
       * @type {Array}
       */
      recentExperiments: [],
      
      /**
       * Data table headers
       * @type {Array}
       */
      headers: [
        { text: this.$t('hybridization.experimentName'), value: 'name', sortable: true },
        { text: this.$t('hybridization.type'), value: 'type', sortable: true },
        { text: this.$t('hybridization.status'), value: 'status', sortable: true },
        { text: this.$t('hybridization.startDate'), value: 'start_date', sortable: true },
        { text: this.$t('hybridization.actions'), value: 'actions', sortable: false }
      ],
      
      /**
       * Chart instances
       * @type {Object}
       * @property {Chart|null} statusChart - Experiments by status chart
       * @property {Chart|null} typeChart - Experiments by type chart
       * @property {Chart|null} trendChart - Experiment trend chart
       */
      charts: {
        statusChart: null,
        typeChart: null,
        trendChart: null
      }
    }
  },
  
  mounted() {
    this.loadDashboardData();
  },
  
  beforeDestroy() {
    // Destroy chart instances to prevent memory leaks
    Object.values(this.charts).forEach(chart => {
      if (chart) chart.destroy();
    });
  },
  
  methods: {
    /**
     * Load dashboard data from the API
     * @returns {Promise<void>}
     */
    async loadDashboardData() {
      this.loading = true;
      
      try {
        const response = await this.$api.hybridization.getDashboardData();
        const data = response.data;
        
        // Update statistics
        this.stats = {
          totalExperiments: data.stats.total_experiments,
          activeExperiments: data.stats.active_experiments,
          totalStrains: data.stats.total_strains,
          successRate: data.stats.success_rate,
          topStrains: data.stats.top_strains,
          upcomingHarvests: data.stats.upcoming_harvests
        };
        
        // Update recent experiments
        this.recentExperiments = data.recent_experiments;
        
        // Initialize charts
        this.$nextTick(() => {
          this.initStatusChart(data.stats.by_status);
          this.initTypeChart(data.stats.by_type);
          this.initTrendChart(data.stats.trend);
        });
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * Initialize experiments by status chart
     * @param {Object} data - Experiment count by status
     */
    initStatusChart(data) {
      const ctx = this.$refs.statusChart.getContext('2d');
      
      // Destroy existing chart if it exists
      if (this.charts.statusChart) {
        this.charts.statusChart.destroy();
      }
      
      const labels = Object.keys(data).map(status => this.getStatusLabel(status));
      const values = Object.values(data);
      const backgroundColors = Object.keys(data).map(status => this.getStatusColor(status));
      
      this.charts.statusChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels,
          datasets: [{
            data: values,
            backgroundColor: backgroundColors
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'right'
            }
          }
        }
      });
    },
    
    /**
     * Initialize experiments by type chart
     * @param {Object} data - Experiment count by type
     */
    initTypeChart(data) {
      const ctx = this.$refs.typeChart.getContext('2d');
      
      // Destroy existing chart if it exists
      if (this.charts.typeChart) {
        this.charts.typeChart.destroy();
      }
      
      const labels = Object.keys(data).map(type => this.getTypeLabel(type));
      const values = Object.values(data);
      const backgroundColors = Object.keys(data).map(type => this.getTypeColor(type));
      
      this.charts.typeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels,
          datasets: [{
            data: values,
            backgroundColor: backgroundColors
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'right'
            }
          }
        }
      });
    },
    
    /**
     * Initialize experiment trend chart
     * @param {Object} data - Experiment trend data
     * @param {Array} data.labels - Time period labels
     * @param {Array} data.values - Experiment count values
     */
    initTrendChart(data) {
      const ctx = this.$refs.trendChart.getContext('2d');
      
      // Destroy existing chart if it exists
      if (this.charts.trendChart) {
        this.charts.trendChart.destroy();
      }
      
      this.charts.trendChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: this.$t('hybridization.experimentCount'),
            data: data.values,
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            }
          }
        }
      });
    },
    
    /**
     * Get color for experiment type
     * @param {String} type - Experiment type
     * @returns {String} - Color name
     */
    getTypeColor(type) {
      const colors = {
        cross_pollination: '#4CAF50', // green
        self_pollination: '#2196F3', // blue
        backcross: '#9C27B0', // purple
        mutation: '#FF9800', // orange
        tissue_culture: '#795548', // brown
        other: '#757575' // grey
      };
      
      return colors[type] || '#757575';
    },
    
    /**
     * Get label for experiment type
     * @param {String} type - Experiment type
     * @returns {String} - Translated label
     */
    getTypeLabel(type) {
      return this.$t(`hybridization.types.${type.replace('_', '')}`) || type;
    },
    
    /**
     * Get color for experiment status
     * @param {String} status - Experiment status
     * @returns {String} - Color name
     */
    getStatusColor(status) {
      const colors = {
        planned: '#2196F3', // blue
        in_progress: '#FF9800', // orange
        completed: '#4CAF50', // green
        failed: '#F44336', // red
        on_hold: '#9E9E9E' // grey
      };
      
      return colors[status] || '#757575';
    },
    
    /**
     * Get label for experiment status
     * @param {String} status - Experiment status
     * @returns {String} - Translated label
     */
    getStatusLabel(status) {
      return this.$t(`hybridization.status.${status.replace('_', '')}`) || status;
    },
    
    /**
     * Format date to localized string
     * @param {String} dateString - ISO date string
     * @returns {String} - Formatted date
     */
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleString(this.$i18n.locale, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    }
  }
}
</script>

<style scoped>
.hybridization-dashboard-container {
  padding: 20px;
}

.dashboard-title {
  margin-bottom: 24px;
  color: var(--v-primary-base);
  font-weight: 500;
}

.dashboard-card {
  height: 100%;
}

.stat-value {
  font-size: 36px;
  font-weight: 500;
  margin-top: 8px;
}

.stat-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.6);
}
</style>
