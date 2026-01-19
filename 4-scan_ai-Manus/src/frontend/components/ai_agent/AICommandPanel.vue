// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/ai_agent/AICommandPanel.vue
<template>
  <div class="ai-command-panel">
    <v-card class="command-card">
      <v-card-title class="text-center">{{ title }}</v-card-title>
      
      <v-card-text>
        <div class="command-section">
          <div class="command-header">
            <h3 class="text-center">الأوامر السريعة</h3>
          </div>
          
          <div class="command-buttons">
            <v-btn
              v-for="(command, index) in quickCommands"
              :key="`quick-${index}`"
              color="primary"
              outlined
              class="command-button"
              @click="executeCommand(command)"
              :disabled="isProcessing"
            >
              <v-icon left>{{ command.icon }}</v-icon>
              {{ command.label }}
            </v-btn>
          </div>
        </div>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="command-section">
          <div class="command-header">
            <h3 class="text-center">الأوامر المخصصة</h3>
          </div>
          
          <div class="custom-command-input">
            <v-text-field
              v-model="customCommand"
              outlined
              dense
              hide-details
              placeholder="أدخل أمرًا مخصصًا..."
              :disabled="isProcessing"
              @keydown.enter="executeCustomCommand"
            ></v-text-field>
            
            <v-btn
              color="primary"
              icon
              class="ml-2"
              @click="executeCustomCommand"
              :disabled="!customCommand || isProcessing"
            >
              <v-icon>mdi-send</v-icon>
            </v-btn>
          </div>
        </div>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="command-section">
          <div class="command-header">
            <h3 class="text-center">الأوامر الأخيرة</h3>
          </div>
          
          <div class="recent-commands">
            <div
              v-for="(command, index) in recentCommands"
              :key="`recent-${index}`"
              class="recent-command"
              @click="setCustomCommand(command.text)"
            >
              <v-icon small class="mr-2">mdi-history</v-icon>
              <span class="command-text">{{ command.text }}</span>
              <span class="command-time">{{ formatTime(command.timestamp) }}</span>
            </div>
            
            <div v-if="recentCommands.length === 0" class="no-commands">
              لا توجد أوامر سابقة
            </div>
          </div>
        </div>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="error"
          text
          @click="clearRecentCommands"
          :disabled="recentCommands.length === 0"
        >
          مسح السجل
        </v-btn>
        <v-btn
          color="primary"
          text
          @click="refreshCommands"
          :loading="isRefreshing"
        >
          تحديث
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
/**
 * مكون لوحة أوامر الذكاء الاصطناعي
 * 
 * يوفر هذا المكون واجهة لإرسال الأوامر إلى الوكيل الذكي
 * مع دعم الأوامر السريعة والمخصصة وسجل الأوامر الأخيرة
 */
export default {
  name: 'AICommandPanel',
  
  props: {
    /**
     * عنوان لوحة الأوامر
     */
    title: {
      type: String,
      default: 'لوحة الأوامر'
    },
    
    /**
     * معرف الوكيل الذكي للاتصال بالخادم
     */
    agentId: {
      type: String,
      required: true
    },
    
    /**
     * قائمة الأوامر السريعة المتاحة
     */
    availableCommands: {
      type: Array,
      default: () => []
    }
  },
  
  data() {
    return {
      quickCommands: [
        { label: 'تحليل البيانات', command: 'analyze_data', icon: 'mdi-chart-bar' },
        { label: 'إنشاء تقرير', command: 'generate_report', icon: 'mdi-file-document' },
        { label: 'جدولة مهمة', command: 'schedule_task', icon: 'mdi-calendar' },
        { label: 'تحديث البيانات', command: 'update_data', icon: 'mdi-database-sync' },
        { label: 'إرسال إشعار', command: 'send_notification', icon: 'mdi-bell' },
        { label: 'مساعدة', command: 'help', icon: 'mdi-help-circle' }
      ],
      customCommand: '',
      recentCommands: [],
      isProcessing: false,
      isRefreshing: false
    };
  },
  
  created() {
    // دمج الأوامر المخصصة مع الأوامر الافتراضية
    if (this.availableCommands.length > 0) {
      this.quickCommands = this.availableCommands;
    }
    
    // تحميل الأوامر الأخيرة من التخزين المحلي
    this.loadRecentCommands();
  },
  
  methods: {
    /**
     * تنفيذ أمر سريع
     * @param {Object} command - الأمر المراد تنفيذه
     */
    executeCommand(command) {
      this.isProcessing = true;
      
      // إضافة الأمر إلى سجل الأوامر الأخيرة
      this.addToRecentCommands(command.command);
      
      // إرسال الأمر إلى الوكيل الذكي
      this.$emit('execute-command', {
        command: command.command,
        label: command.label,
        agentId: this.agentId
      });
      
      // محاكاة انتهاء المعالجة
      setTimeout(() => {
        this.isProcessing = false;
      }, 1500);
    },
    
    /**
     * تنفيذ أمر مخصص
     */
    executeCustomCommand() {
      if (!this.customCommand || this.isProcessing) return;
      
      this.isProcessing = true;
      
      // إضافة الأمر إلى سجل الأوامر الأخيرة
      this.addToRecentCommands(this.customCommand);
      
      // إرسال الأمر إلى الوكيل الذكي
      this.$emit('execute-command', {
        command: this.customCommand,
        label: 'أمر مخصص',
        agentId: this.agentId
      });
      
      // إعادة تعيين حقل الأمر المخصص
      this.customCommand = '';
      
      // محاكاة انتهاء المعالجة
      setTimeout(() => {
        this.isProcessing = false;
      }, 1500);
    },
    
    /**
     * إضافة أمر إلى سجل الأوامر الأخيرة
     * @param {String} commandText - نص الأمر
     */
    addToRecentCommands(commandText) {
      // التحقق من عدم تكرار نفس الأمر
      const existingIndex = this.recentCommands.findIndex(cmd => cmd.text === commandText);
      if (existingIndex !== -1) {
        // إزالة الأمر الموجود
        this.recentCommands.splice(existingIndex, 1);
      }
      
      // إضافة الأمر الجديد في بداية القائمة
      this.recentCommands.unshift({
        text: commandText,
        timestamp: new Date()
      });
      
      // الاحتفاظ بآخر 10 أوامر فقط
      if (this.recentCommands.length > 10) {
        this.recentCommands = this.recentCommands.slice(0, 10);
      }
      
      // حفظ الأوامر الأخيرة في التخزين المحلي
      this.saveRecentCommands();
    },
    
    /**
     * تعيين الأمر المخصص من سجل الأوامر الأخيرة
     * @param {String} commandText - نص الأمر
     */
    setCustomCommand(commandText) {
      this.customCommand = commandText;
    },
    
    /**
     * مسح سجل الأوامر الأخيرة
     */
    clearRecentCommands() {
      this.recentCommands = [];
      this.saveRecentCommands();
    },
    
    /**
     * تحديث قائمة الأوامر المتاحة
     */
    refreshCommands() {
      this.isRefreshing = true;
      
      // محاكاة تحديث الأوامر من الخادم
      setTimeout(() => {
        // يمكن هنا إضافة منطق لتحديث الأوامر المتاحة من الخادم
        this.isRefreshing = false;
      }, 1000);
    },
    
    /**
     * تنسيق الوقت
     * @param {Date} timestamp - الطابع الزمني
     * @returns {String} - الوقت المنسق
     */
    formatTime(timestamp) {
      if (!timestamp) return '';
      
      const date = new Date(timestamp);
      return date.toLocaleTimeString('ar-SA', {
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    /**
     * حفظ سجل الأوامر الأخيرة
     */
    saveRecentCommands() {
      try {
        localStorage.setItem(`recent_commands_${this.agentId}`, JSON.stringify(this.recentCommands));
      } catch (error) {
        console.error('خطأ في حفظ سجل الأوامر:', error);
      }
    },
    
    /**
     * تحميل سجل الأوامر الأخيرة
     */
    loadRecentCommands() {
      try {
        const savedCommands = localStorage.getItem(`recent_commands_${this.agentId}`);
        if (savedCommands) {
          this.recentCommands = JSON.parse(savedCommands);
        }
      } catch (error) {
        console.error('خطأ في تحميل سجل الأوامر:', error);
      }
    }
  }
};
</script>

<style scoped>
.ai-command-panel {
  width: 100%;
}

.command-card {
  border-radius: 8px;
  overflow: hidden;
}

.command-section {
  margin-bottom: 1rem;
}

.command-header {
  margin-bottom: 1rem;
}

.command-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}

.command-button {
  margin: 0.25rem;
  flex-grow: 1;
  max-width: calc(33.333% - 0.5rem);
  text-align: center;
}

.custom-command-input {
  display: flex;
  align-items: center;
}

.recent-commands {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 0.5rem;
}

.recent-command {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.recent-command:hover {
  background-color: var(--v-primary-lighten5);
}

.command-text {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.command-time {
  font-size: 0.75rem;
  color: #888;
  margin-right: 0.5rem;
}

.no-commands {
  text-align: center;
  padding: 1rem;
  color: #888;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 600px) {
  .command-button {
    max-width: calc(50% - 0.5rem);
  }
}
</style>
