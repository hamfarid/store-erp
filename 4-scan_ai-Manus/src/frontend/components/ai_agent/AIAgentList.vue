// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/ai_agent/AIAgentList.vue
<template>
  <div class="ai-agent-list">
    <div class="list-header">
      <h2 class="text-center">{{ title }}</h2>
      
      <div class="filter-controls">
        <v-text-field
          v-model="searchQuery"
          outlined
          dense
          hide-details
          prepend-inner-icon="mdi-magnify"
          placeholder="بحث عن وكيل..."
          class="search-field"
          clearable
        ></v-text-field>
        
        <v-select
          v-model="typeFilter"
          :items="agentTypes"
          outlined
          dense
          hide-details
          prepend-inner-icon="mdi-filter-variant"
          placeholder="تصفية حسب النوع"
          class="filter-field"
          clearable
        ></v-select>
        
        <v-select
          v-model="statusFilter"
          :items="statusOptions"
          outlined
          dense
          hide-details
          prepend-inner-icon="mdi-filter-variant"
          placeholder="تصفية حسب الحالة"
          class="filter-field"
          clearable
        ></v-select>
      </div>
    </div>
    
    <div class="list-actions">
      <v-btn
        color="primary"
        @click="createNewAgent"
        class="action-button"
      >
        <v-icon left>mdi-plus</v-icon>
        إنشاء وكيل جديد
      </v-btn>
      
      <v-btn
        color="secondary"
        @click="refreshAgents"
        :loading="isLoading"
        class="action-button"
      >
        <v-icon left>mdi-refresh</v-icon>
        تحديث
      </v-btn>
      
      <v-btn
        color="error"
        @click="stopAllAgents"
        :disabled="!hasActiveAgents"
        class="action-button"
      >
        <v-icon left>mdi-stop-circle</v-icon>
        إيقاف الكل
      </v-btn>
    </div>
    
    <div v-if="isLoading" class="loading-container">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
      <div class="loading-text">جاري تحميل الوكلاء...</div>
    </div>
    
    <div v-else-if="filteredAgents.length === 0" class="empty-state">
      <v-icon size="64" color="grey lighten-1">mdi-robot-off</v-icon>
      <div class="empty-text">
        {{ searchQuery || typeFilter || statusFilter ? 'لا توجد وكلاء تطابق معايير البحث' : 'لا توجد وكلاء متاحة حالياً' }}
      </div>
      <v-btn
        color="primary"
        @click="createNewAgent"
        class="mt-4"
      >
        <v-icon left>mdi-plus</v-icon>
        إنشاء وكيل جديد
      </v-btn>
    </div>
    
    <v-row v-else class="agent-grid">
      <v-col
        v-for="agent in filteredAgents"
        :key="agent.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
        class="agent-col"
      >
        <ai-agent-card
          :agent="agent"
          :active="activeAgents.includes(agent.id)"
          @view-details="viewAgentDetails"
          @toggle-active="toggleAgentActive"
          @open-chat="openAgentChat"
        ></ai-agent-card>
      </v-col>
    </v-row>
    
    <div class="pagination-container" v-if="totalPages > 1">
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        :total-visible="7"
        circle
      ></v-pagination>
    </div>
  </div>
</template>

<script>
/**
 * مكون قائمة وكلاء الذكاء الاصطناعي
 * 
 * يعرض هذا المكون قائمة بوكلاء الذكاء الاصطناعي المتاحة
 * مع إمكانية البحث والتصفية وإنشاء وكلاء جديدة
 */
export default {
  name: 'AIAgentList',
  
  components: {
    'ai-agent-card': () => import('./AIAgentCard.vue')
  },
  
  props: {
    /**
     * عنوان القائمة
     */
    title: {
      type: String,
      default: 'وكلاء الذكاء الاصطناعي'
    },
    
    /**
     * قائمة الوكلاء
     */
    agents: {
      type: Array,
      default: () => []
    },
    
    /**
     * حالة التحميل
     */
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      searchQuery: '',
      typeFilter: null,
      statusFilter: null,
      currentPage: 1,
      pageSize: 12,
      activeAgents: [],
      isLoading: this.loading,
      
      // خيارات التصفية
      agentTypes: [
        { text: 'وكيل عام', value: 'general' },
        { text: 'وكيل تحليل', value: 'analytics' },
        { text: 'وكيل معالجة صور', value: 'image_processing' },
        { text: 'وكيل معالجة نصوص', value: 'text_processing' },
        { text: 'وكيل تنبؤ', value: 'prediction' },
        { text: 'وكيل توصيات', value: 'recommendation' }
      ],
      
      statusOptions: [
        { text: 'نشط', value: 'active' },
        { text: 'خامل', value: 'idle' },
        { text: 'غير متصل', value: 'offline' }
      ]
    };
  },
  
  computed: {
    /**
     * الوكلاء المصفاة حسب معايير البحث والتصفية
     */
    filteredAgents() {
      let result = [...this.agents];
      
      // تصفية حسب البحث
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(agent => 
          agent.name.toLowerCase().includes(query) || 
          agent.description.toLowerCase().includes(query)
        );
      }
      
      // تصفية حسب النوع
      if (this.typeFilter) {
        result = result.filter(agent => agent.type === this.typeFilter);
      }
      
      // تصفية حسب الحالة
      if (this.statusFilter) {
        if (this.statusFilter === 'active') {
          result = result.filter(agent => 
            agent.online && this.activeAgents.includes(agent.id)
          );
        } else if (this.statusFilter === 'idle') {
          result = result.filter(agent => 
            agent.online && !this.activeAgents.includes(agent.id)
          );
        } else if (this.statusFilter === 'offline') {
          result = result.filter(agent => !agent.online);
        }
      }
      
      // تطبيق الصفحة الحالية
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      
      return result.slice(startIndex, endIndex);
    },
    
    /**
     * إجمالي عدد الصفحات
     */
    totalPages() {
      if (!this.agents.length) return 0;
      
      let filteredCount = this.agents.length;
      
      // تصفية حسب البحث
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filteredCount = this.agents.filter(agent => 
          agent.name.toLowerCase().includes(query) || 
          agent.description.toLowerCase().includes(query)
        ).length;
      }
      
      // تصفية حسب النوع
      if (this.typeFilter) {
        filteredCount = this.agents.filter(agent => agent.type === this.typeFilter).length;
      }
      
      // تصفية حسب الحالة
      if (this.statusFilter) {
        if (this.statusFilter === 'active') {
          filteredCount = this.agents.filter(agent => 
            agent.online && this.activeAgents.includes(agent.id)
          ).length;
        } else if (this.statusFilter === 'idle') {
          filteredCount = this.agents.filter(agent => 
            agent.online && !this.activeAgents.includes(agent.id)
          ).length;
        } else if (this.statusFilter === 'offline') {
          filteredCount = this.agents.filter(agent => !agent.online).length;
        }
      }
      
      return Math.ceil(filteredCount / this.pageSize);
    },
    
    /**
     * التحقق من وجود وكلاء نشطة
     */
    hasActiveAgents() {
      return this.activeAgents.length > 0;
    }
  },
  
  watch: {
    /**
     * مراقبة تغيير حالة التحميل من الخارج
     */
    loading(newValue) {
      this.isLoading = newValue;
    },
    
    /**
     * إعادة تعيين الصفحة الحالية عند تغيير معايير البحث
     */
    searchQuery() {
      this.currentPage = 1;
    },
    
    /**
     * إعادة تعيين الصفحة الحالية عند تغيير تصفية النوع
     */
    typeFilter() {
      this.currentPage = 1;
    },
    
    /**
     * إعادة تعيين الصفحة الحالية عند تغيير تصفية الحالة
     */
    statusFilter() {
      this.currentPage = 1;
    }
  },
  
  mounted() {
    // تحميل الوكلاء النشطة من التخزين المحلي
    this.loadActiveAgents();
  },
  
  methods: {
    /**
     * عرض تفاصيل الوكيل
     * @param {String} agentId - معرف الوكيل
     */
    viewAgentDetails(agentId) {
      this.$emit('view-details', agentId);
    },
    
    /**
     * تبديل حالة نشاط الوكيل
     * @param {Object} data - بيانات تبديل النشاط
     */
    toggleAgentActive(data) {
      const { agentId, active } = data;
      
      if (active) {
        // إضافة الوكيل إلى قائمة الوكلاء النشطة
        if (!this.activeAgents.includes(agentId)) {
          this.activeAgents.push(agentId);
        }
      } else {
        // إزالة الوكيل من قائمة الوكلاء النشطة
        const index = this.activeAgents.indexOf(agentId);
        if (index !== -1) {
          this.activeAgents.splice(index, 1);
        }
      }
      
      // حفظ الوكلاء النشطة في التخزين المحلي
      this.saveActiveAgents();
      
      // إرسال حدث تبديل النشاط
      this.$emit('toggle-active', data);
    },
    
    /**
     * فتح محادثة مع الوكيل
     * @param {String} agentId - معرف الوكيل
     */
    openAgentChat(agentId) {
      this.$emit('open-chat', agentId);
    },
    
    /**
     * إنشاء وكيل جديد
     */
    createNewAgent() {
      this.$emit('create-agent');
    },
    
    /**
     * تحديث قائمة الوكلاء
     */
    refreshAgents() {
      this.isLoading = true;
      this.$emit('refresh-agents');
      
      // محاكاة انتهاء التحديث
      setTimeout(() => {
        this.isLoading = false;
      }, 1000);
    },
    
    /**
     * إيقاف جميع الوكلاء النشطة
     */
    stopAllAgents() {
      // إيقاف جميع الوكلاء النشطة
      this.activeAgents.forEach(agentId => {
        this.$emit('toggle-active', {
          agentId,
          active: false
        });
      });
      
      // إعادة تعيين قائمة الوكلاء النشطة
      this.activeAgents = [];
      
      // حفظ الوكلاء النشطة في التخزين المحلي
      this.saveActiveAgents();
      
      // إرسال حدث إيقاف جميع الوكلاء
      this.$emit('stop-all-agents');
    },
    
    /**
     * حفظ الوكلاء النشطة في التخزين المحلي
     */
    saveActiveAgents() {
      try {
        localStorage.setItem('active_agents', JSON.stringify(this.activeAgents));
      } catch (error) {
        console.error('خطأ في حفظ الوكلاء النشطة:', error);
      }
    },
    
    /**
     * تحميل الوكلاء النشطة من التخزين المحلي
     */
    loadActiveAgents() {
      try {
        const savedAgents = localStorage.getItem('active_agents');
        if (savedAgents) {
          this.activeAgents = JSON.parse(savedAgents);
        }
      } catch (error) {
        console.error('خطأ في تحميل الوكلاء النشطة:', error);
      }
    }
  }
};
</script>

<style scoped>
.ai-agent-list {
  width: 100%;
}

.list-header {
  margin-bottom: 1.5rem;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.search-field {
  flex-grow: 2;
  min-width: 250px;
}

.filter-field {
  flex-grow: 1;
  min-width: 200px;
}

.list-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.action-button {
  flex-grow: 1;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.loading-text {
  margin-top: 1rem;
  color: var(--v-primary-base);
  font-weight: bold;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.empty-text {
  margin-top: 1rem;
  color: var(--v-secondary-base);
  font-size: 1.1rem;
}

.agent-grid {
  margin: 0;
}

.agent-col {
  padding: 0.75rem;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 600px) {
  .filter-controls {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .search-field,
  .filter-field {
    width: 100%;
  }
  
  .list-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
