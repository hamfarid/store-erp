// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/tables/MetricsTable.vue

<template>
  <div class="metrics-table-container">
    <div v-if="loading" class="table-loading">
      <div class="spinner"></div>
      <span>{{ $t('common.loading') }}</span>
    </div>
    
    <table class="metrics-table" v-else>
      <thead>
        <tr>
          <th>{{ $t('resource_monitoring.metric_name') }}</th>
          <th>{{ $t('resource_monitoring.resource_type') }}</th>
          <th>{{ $t('resource_monitoring.unit') }}</th>
          <th>{{ $t('resource_monitoring.description') }}</th>
          <th>{{ $t('common.actions') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="metrics.length === 0">
          <td colspan="5" class="no-data">{{ $t('resource_monitoring.no_metrics') }}</td>
        </tr>
        <tr v-for="metric in metrics" :key="metric.id">
          <td>{{ metric.displayName || metric.metricName }}</td>
          <td>{{ metric.resourceType }}</td>
          <td>{{ metric.unit }}</td>
          <td>{{ metric.description }}</td>
          <td class="actions-cell">
            <button class="btn btn-icon btn-edit" @click="$emit('edit-metric', metric)" title="تعديل">
              <i class="fas fa-edit"></i>
            </button>
            <button class="btn btn-icon btn-delete" @click="$emit('delete-metric', metric.id)" title="حذف">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'MetricsTable',
  
  props: {
    metrics: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['edit-metric', 'delete-metric']
};
</script>

<style scoped>
.metrics-table-container {
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

.metrics-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.metrics-table th,
.metrics-table td {
  padding: 12px 15px;
  text-align: right;
  border-bottom: 1px solid #e0e0e0;
}

.metrics-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.metrics-table tr:hover {
  background-color: #f9f9f9;
}

.no-data {
  text-align: center;
  color: #757575;
  padding: 30px 0;
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
