// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/ai_agent/AIAgentCard.vue
<template>
  <v-card class="ai-agent-card" :class="{ 'active': isActive }">
    <div class="card-header">
      <div class="agent-avatar">
        <img 
          v-if="agent.avatar" 
          :src="agent.avatar" 
          :alt="agent.name" 
          class="avatar-image"
        />
        <v-icon v-else size="48" color="primary">mdi-robot</v-icon>
      </div>
      
      <div class="agent-status" :class="statusClass">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon 
              small 
              v-bind="attrs"
              v-on="on"
            >
              {{ statusIcon }}
            </v-icon>
          </template>
          <span>{{ statusText }}</span>
        </v-tooltip>
      </div>
    </div>
    
    <v-card-title class="text-center">{{ agent.name }}</v-card-title>
    
    <v-card-subtitle class="text-center">{{ agent.type }}</v-card-subtitle>
    
    <v-card-text>
      <p class="agent-description text-center">{{ agent.description }}</p>
      
      <v-divider class="my-3"></v-divider>
      
      <div class="agent-stats">
        <div class="stat-item">
          <div class="stat-label">الاستخدام اليومي</div>
          <div class="stat-value">{{ agent.stats.dailyUsage }}</div>
        </div>
        
        <div class="stat-item">
          <div class="stat-label">دقة الإجابات</div>
          <div class="stat-value">{{ agent.stats.accuracy }}%</div>
        </div>
        
        <div class="stat-item">
          <div class="stat-label">وقت الاستجابة</div>
          <div class="stat-value">{{ agent.stats.responseTime }}ms</div>
        </div>
      </div>
      
      <v-divider class="my-3"></v-divider>
      
      <div class="agent-capabilities">
        <div class="capabilities-title text-center">القدرات</div>
        <div class="capabilities-list">
          <v-chip
            v-for="(capability, index) in agent.capabilities"
            :key="index"
            small
            class="ma-1"
            :color="getCapabilityColor(capability)"
            text-color="white"
          >
            {{ capability }}
          </v-chip>
        </div>
      </div>
    </v-card-text>
    
    <v-card-actions>
      <v-btn
        text
        color="primary"
        @click="viewDetails"
        class="action-button"
      >
        <v-icon left>mdi-information</v-icon>
        التفاصيل
      </v-btn>
      
      <v-spacer></v-spacer>
      
      <v-btn
        text
        :color="isActive ? 'error' : 'success'"
        @click="toggleActive"
        class="action-button"
      >
        <v-icon left>{{ isActive ? 'mdi-stop' : 'mdi-play' }}</v-icon>
        {{ isActive ? 'إيقاف' : 'تشغيل' }}
      </v-btn>
      
      <v-btn
        text
        color="primary"
        @click="openChat"
        class="action-button"
        :disabled="!isActive"
      >
        <v-icon left>mdi-chat</v-icon>
        محادثة
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
/**
 * مكون بطاقة وكيل الذكاء الاصطناعي
 * 
 * يعرض هذا المكون معلومات وكيل الذكاء الاصطناعي في بطاقة
 * مع إمكانية عرض التفاصيل وتشغيل/إيقاف الوكيل وفتح المحادثة
 */
export default {
  name: 'AIAgentCard',
  
  props: {
    /**
     * بيانات وكيل الذكاء الاصطناعي
     */
    agent: {
      type: Object,
      required: true
    },
    
    /**
     * حالة نشاط الوكيل
     */
    active: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      isActive: this.active,
      capabilityColors: {
        'تحليل البيانات': 'blue',
        'معالجة اللغة الطبيعية': 'indigo',
        'معالجة الصور': 'purple',
        'التعلم المستمر': 'deep-purple',
        'التوصيات': 'teal',
        'التنبؤ': 'cyan',
        'التلخيص': 'light-blue',
        'الترجمة': 'blue-grey',
        'إنشاء المحتوى': 'green',
        'الإجابة على الأسئلة': 'light-green',
        'البحث': 'amber',
        'التحليل المالي': 'orange',
        'تحليل المشاعر': 'deep-orange',
        'التشخيص': 'red',
        'التخطيط': 'pink',
        'جدولة المهام': 'purple'
      }
    };
  },
  
  computed: {
    /**
     * حالة الوكيل (نشط، خامل، غير متصل)
     */
    statusClass() {
      if (!this.agent.online) return 'status-offline';
      return this.isActive ? 'status-active' : 'status-idle';
    },
    
    /**
     * أيقونة حالة الوكيل
     */
    statusIcon() {
      if (!this.agent.online) return 'mdi-lan-disconnect';
      return this.isActive ? 'mdi-circle' : 'mdi-circle-outline';
    },
    
    /**
     * نص حالة الوكيل
     */
    statusText() {
      if (!this.agent.online) return 'غير متصل';
      return this.isActive ? 'نشط' : 'خامل';
    }
  },
  
  watch: {
    /**
     * مراقبة تغيير حالة النشاط من الخارج
     */
    active(newValue) {
      this.isActive = newValue;
    }
  },
  
  methods: {
    /**
     * عرض تفاصيل الوكيل
     */
    viewDetails() {
      this.$emit('view-details', this.agent.id);
    },
    
    /**
     * تبديل حالة نشاط الوكيل
     */
    toggleActive() {
      this.isActive = !this.isActive;
      this.$emit('toggle-active', {
        agentId: this.agent.id,
        active: this.isActive
      });
    },
    
    /**
     * فتح محادثة مع الوكيل
     */
    openChat() {
      if (!this.isActive) return;
      this.$emit('open-chat', this.agent.id);
    },
    
    /**
     * الحصول على لون القدرة
     * @param {String} capability - اسم القدرة
     * @returns {String} - لون القدرة
     */
    getCapabilityColor(capability) {
      return this.capabilityColors[capability] || 'primary';
    }
  }
};
</script>

<style scoped>
.ai-agent-card {
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.ai-agent-card.active {
  box-shadow: 0 0 15px rgba(var(--v-primary-base), 0.3);
  border: 1px solid var(--v-primary-base);
}

.card-header {
  position: relative;
  display: flex;
  justify-content: center;
  padding-top: 1.5rem;
}

.agent-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--v-surface-base);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 3px solid var(--v-primary-base);
  z-index: 1;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.agent-status {
  position: absolute;
  top: 1.5rem;
  right: 1rem;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-active {
  color: var(--v-success-base);
}

.status-idle {
  color: var(--v-warning-base);
}

.status-offline {
  color: var(--v-error-base);
}

.agent-description {
  font-size: 0.9rem;
  color: var(--v-secondary-darken1);
  margin-bottom: 1rem;
  height: 3.6rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-clamp: 3;
}

.agent-stats {
  display: flex;
  justify-content: space-around;
  margin: 0.5rem 0;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--v-secondary-darken1);
}

.stat-value {
  font-weight: bold;
  color: var(--v-primary-base);
}

.capabilities-title {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: var(--v-secondary-darken1);
}

.capabilities-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.action-button {
  flex-grow: 1;
  text-align: center;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 600px) {
  .agent-avatar {
    width: 60px;
    height: 60px;
  }
  
  .agent-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
