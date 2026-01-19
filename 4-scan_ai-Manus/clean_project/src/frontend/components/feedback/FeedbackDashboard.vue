<template>
  <div class="feedback-dashboard-container">
    <h1 class="dashboard-title">{{ $t('feedback.dashboard') }}</h1>
    
    <v-row>
      <v-col cols="12" md="6" lg="3">
        <v-card class="dashboard-card">
          <v-card-text class="text-center">
            <v-icon size="48" color="primary">mdi-message-text</v-icon>
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">{{ $t('feedback.totalFeedback') }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6" lg="3">
        <v-card class="dashboard-card">
          <v-card-text class="text-center">
            <v-icon size="48" color="blue">mdi-message-alert</v-icon>
            <div class="stat-value">{{ stats.new }}</div>
            <div class="stat-label">{{ $t('feedback.newFeedback') }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6" lg="3">
        <v-card class="dashboard-card">
          <v-card-text class="text-center">
            <v-icon size="48" color="orange">mdi-message-processing</v-icon>
            <div class="stat-value">{{ stats.inProgress }}</div>
            <div class="stat-label">{{ $t('feedback.inProgressFeedback') }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6" lg="3">
        <v-card class="dashboard-card">
          <v-card-text class="text-center">
            <v-icon size="48" color="green">mdi-message-check</v-icon>
            <div class="stat-value">{{ stats.resolved }}</div>
            <div class="stat-label">{{ $t('feedback.resolvedFeedback') }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('feedback.feedbackByType') }}</v-card-title>
          <v-card-text>
            <canvas ref="typeChart"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('feedback.feedbackByStatus') }}</v-card-title>
          <v-card-text>
            <canvas ref="statusChart"></canvas>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>{{ $t('feedback.feedbackTrend') }}</v-card-title>
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
            <span>{{ $t('feedback.recentFeedback') }}</span>
            <v-btn
              text
              color="primary"
              :to="{ name: 'feedback-list' }"
            >
              {{ $t('feedback.viewAll') }}
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-title>
          
          <v-data-table
            :headers="headers"
            :items="recentFeedback"
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
            
            <template v-slot:item.created_at="{ item }">
              {{ formatDate(item.created_at) }}
            </template>
            
            <template v-slot:item.actions="{ item }">
              <v-btn
                small
                text
                color="primary"
                :to="{ name: 'feedback-details', params: { id: item.id } }"
              >
                {{ $t('feedback.view') }}
              </v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('feedback.responseRate') }}</v-card-title>
          <v-card-text class="text-center">
            <v-progress-circular
              :rotate="-90"
              :size="200"
              :width="15"
              :value="stats.responseRate"
              color="primary"
            >
              {{ stats.responseRate }}%
            </v-progress-circular>
            <div class="mt-3">{{ $t('feedback.averageResponseTime') }}: {{ stats.avgResponseTime }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('feedback.topContributors') }}</v-card-title>
          <v-list>
            <v-list-item
              v-for="(contributor, index) in stats.topContributors"
              :key="index"
            >
              <v-list-item-avatar>
                <v-avatar color="primary" v-if="!contributor.avatar">
                  <span class="white--text">{{ getInitials(contributor.name) }}</span>
                </v-avatar>
                <v-img v-else :src="contributor.avatar"></v-img>
              </v-list-item-avatar>
              
              <v-list-item-content>
                <v-list-item-title>{{ contributor.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ $t('feedback.feedbackCount') }}: {{ contributor.count }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

/**
 * @component FeedbackDashboard
 * @description A dashboard component for displaying feedback statistics and analytics.
 * This component provides an overview of feedback data with charts, statistics,
 * and a list of recent feedback items.
 */
export default {
  name: 'FeedbackDashboard',
  
  data() {
    return {
      /**
       * Loading state
       * @type {Boolean}
       */
      loading: false,
      
      /**
       * Feedback statistics
       * @type {Object}
       * @property {Number} total - Total number of feedback items
       * @property {Number} new - Number of new feedback items
       * @property {Number} inProgress - Number of in-progress feedback items
       * @property {Number} resolved - Number of resolved feedback items
       * @property {Number} responseRate - Percentage of feedback items with responses
       * @property {String} avgResponseTime - Average response time (formatted)
       * @property {Array} topContributors - List of top feedback contributors
       */
      stats: {
        total: 0,
        new: 0,
        inProgress: 0,
        resolved: 0,
        responseRate: 0,
        avgResponseTime: '',
        topContributors: []
      },
      
      /**
       * Recent feedback items
       * @type {Array}
       */
      recentFeedback: [],
      
      /**
       * Data table headers
       * @type {Array}
       */
      headers: [
        { text: this.$t('feedback.subject'), value: 'subject', sortable: true },
        { text: this.$t('feedback.type'), value: 'type', sortable: true },
        { text: this.$t('feedback.status'), value: 'status', sortable: true },
        { text: this.$t('feedback.submittedOn'), value: 'created_at', sortable: true },
        { text: this.$t('feedback.actions'), value: 'actions', sortable: false }
      ],
      
      /**
       * Chart instances
       * @type {Object}
       * @property {Chart|null} typeChart - Feedback by type chart
       * @property {Chart|null} statusChart - Feedback by status chart
       * @property {Chart|null} trendChart - Feedback trend chart
       */
      charts: {
        typeChart: null,
        statusChart: null,
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
        const response = await this.$api.feedback.getDashboardData();
        const data = response.data;
        
        // Update statistics
        this.stats = {
          total: data.stats.total,
          new: data.stats.by_status.new || 0,
          inProgress: data.stats.by_status.in_progress || 0,
          resolved: data.stats.by_status.resolved || 0,
          responseRate: data.stats.response_rate,
          avgResponseTime: data.stats.avg_response_time,
          topContributors: data.stats.top_contributors
        };
        
        // Update recent feedback
        this.recentFeedback = data.recent_feedback;
        
        // Initialize charts
        this.$nextTick(() => {
          this.initTypeChart(data.stats.by_type);
          this.initStatusChart(data.stats.by_status);
          this.initTrendChart(data.stats.trend);
        });
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * Initialize feedback by type chart
     * @param {Object} data - Feedback count by type
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
     * Initialize feedback by status chart
     * @param {Object} data - Feedback count by status
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
     * Initialize feedback trend chart
     * @param {Object} data - Feedback trend data
     * @param {Array} data.labels - Time period labels
     * @param {Array} data.values - Feedback count values
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
            label: this.$t('feedback.feedbackCount'),
            data: data.values,
            borderColor: '#1976D2',
            backgroundColor: 'rgba(25, 118, 210, 0.1)',
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
     * Get color for feedback type
     * @param {String} type - Feedback type
     * @returns {String} - Color name
     */
    getTypeColor(type) {
      const colors = {
        suggestion: '#2196F3', // blue
        bug: '#F44336', // red
        feature: '#4CAF50', // green
        comment: '#9C27B0', // purple
        other: '#757575' // grey
      };
      
      return colors[type] || '#757575';
    },
    
    /**
     * Get label for feedback type
     * @param {String} type - Feedback type
     * @returns {String} - Translated label
     */
    getTypeLabel(type) {
      return this.$t(`feedback.types.${type}`) || type;
    },
    
    /**
     * Get color for feedback status
     * @param {String} status - Feedback status
     * @returns {String} - Color name
     */
    getStatusColor(status) {
      const colors = {
        new: '#2196F3', // blue
        in_progress: '#FF9800', // orange
        resolved: '#4CAF50', // green
        closed: '#757575', // grey
        rejected: '#F44336' // red
      };
      
      return colors[status] || '#757575';
    },
    
    /**
     * Get label for feedback status
     * @param {String} status - Feedback status
     * @returns {String} - Translated label
     */
    getStatusLabel(status) {
      return this.$t(`feedback.status.${status.replace('_', '')}`) || status;
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
    },
    
    /**
     * Get initials from name
     * @param {String} name - Full name
     * @returns {String} - Initials
     */
    getInitials(name) {
      if (!name) return '';
      
      return name
        .split(' ')
        .map(part => part.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2);
    }
  }
}
</script>

<style scoped>
.feedback-dashboard-container {
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
