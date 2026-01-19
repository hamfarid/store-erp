// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/tables/ThresholdsTable.vue

<template>
  <div class="thresholds-table-container">
    <div v-if="loading" class="table-loading">
      <div class="spinner"></div>
      <span>{{ $t('common.loading') }}</span>
    </div>
    
    <table class="thresholds-table" v-else>
      <thead>
        <tr>
          <th>{{ $t('resource_monitoring.metric') }}</th>
          <th>{{ $t('resource_monitoring.warning_threshold') }}</th>
          <th>{{ $t('resource_monitoring.critical_threshold') }}</th>
          <th>{{ $t('resource_monitoring.status') }}</th>
          <th>{{ $t('common.actions') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="thresholds.length === 0">
          <td colspan="5" class="no-data">{{ $t('resource_monitoring.no_thresholds') }}</td>
        </tr>
        <tr v-for="threshold in thresholds" :key="threshold.id">
          <td>{{ getMetricName(threshold.metricId) }}</td>
          <td>{{ threshold.warningThreshold }}{{ getMetricUnit(threshold.metricId) }}</td>
          <td>{{ threshold.criticalThreshold }}{{ getMetricUnit(threshold.metricId) }}</td>
          <td>
            <span class="status-badge" :class="threshold.enabled ? 'enabled' : 'disabled'">
              {{ threshold.enabled ? $t('common.enabled') : $t('common.disabled') }}
            </span>
          </td>
          <td class="actions-cell">
            <button class="btn btn-icon btn-edit" @click="$emit('edit-threshold', threshold)" title="تعديل">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn btn-icon btn-delete" @click="$emit('delete-threshold', threshold.id)" title="حذف">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'ThresholdsTable',
  
  props: {
    thresholds: {
      type: Array,
      required: true
    },
    metrics: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['edit-threshold', 'delete-threshold'],
  
  setup(props) {
    // Create a lookup map for metrics
    const metricsMap = computed(() => {
      const map = {};
      props.metrics.forEach(metric => {
        map[metric.id] = metric;
      });
      return map;
    });
    
    const getMetricName = (metricId) => {
      const metric = metricsMap.value[metricId];
      return metric ? (metric.displayName || metric.metricName) : $t('resource_monitoring.unknown_metric');
    };
    
    const getMetricUnit = (metricId) => {
      const metric = metricsMap.value[metricId];
      return metric ? metric.unit : '';
    };
    
    return {
      getMetricName,
      getMetricUnit
    };
  }
};
</script>

<style scoped>
.thresholds-table-container {
  position: relative;
  width: 100%;
  overflow-x: auto;
}

.table-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 10;
  min-height: 200px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(33, 150, 243, 0.3);
  border-radius: 50%;
  border-top-color: #2196F3;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.thresholds-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.thresholds-table th,
.thresholds-table td {
  padding: 12px 15px;
  text-align: right;
  border-bottom: 1px solid #e0e0e0;
}

.thresholds-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.thresholds-table tr:hover {
  background-color: #f9f9f9;
}

.no-data {
  text-align: center;
  color: #757575;
  padding: 30px 0;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.enabled {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status-badge.disabled {
  background-color: rgba(158, 158, 158, 0.1);
  color: #9E9E9E;
}

.actions-cell {
  white-space: nowrap;
  width: 100px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  margin-right: 5px;
  transition: background-color 0.2s;
}

.btn-edit {
  background-color: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.btn-edit:hover {
  background-color: rgba(33, 150, 243, 0.2);
}

.btn-delete {
  background-color: rgba(244, 67, 54, 0.1);
  color: #F44336;
}

.btn-delete:hover {
  background-color: rgba(244, 67, 54, 0.2);
}
</style>
