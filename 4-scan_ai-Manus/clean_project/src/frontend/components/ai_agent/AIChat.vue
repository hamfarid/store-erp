// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/ai_agent/AIChat.vue
<template>
  <div class="ai-chat-container">
    <div class="chat-header">
      <h2 class="text-center">{{ title }}</h2>
    </div>
    
    <div class="chat-messages" ref="chatMessages">
      <div 
        v-for="(message, index) in messages" 
        :key="index" 
        :class="['message-container', message.sender === 'user' ? 'user-message' : 'ai-message']"
      >
        <div class="message-avatar">
          <img 
            v-if="message.sender === 'user' && userAvatar" 
            :src="userAvatar" 
            alt="صورة المستخدم" 
            class="avatar-image"
          />
          <v-icon v-else-if="message.sender === 'user'" size="40" color="primary">mdi-account-circle</v-icon>
          
          <img 
            v-if="message.sender === 'ai' && aiAvatar" 
            :src="aiAvatar" 
            alt="صورة الوكيل الذكي" 
            class="avatar-image"
          />
          <v-icon v-else-if="message.sender === 'ai'" size="40" color="accent">mdi-robot</v-icon>
        </div>
        
        <div class="message-content">
          <div class="message-sender">{{ message.sender === 'user' ? userName : agentName }}</div>
          <div class="message-text" v-html="formatMessage(message.text)"></div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          
          <div v-if="message.attachments && message.attachments.length > 0" class="message-attachments">
            <div v-for="(attachment, attIndex) in message.attachments" :key="attIndex" class="attachment-item">
              <v-btn 
                small 
                outlined 
                color="primary" 
                @click="openAttachment(attachment)"
                class="attachment-button"
              >
                <v-icon small left>{{ getAttachmentIcon(attachment) }}</v-icon>
                {{ getAttachmentName(attachment) }}
              </v-btn>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="isTyping" class="message-container ai-message">
        <div class="message-avatar">
          <img 
            v-if="aiAvatar" 
            :src="aiAvatar" 
            alt="صورة الوكيل الذكي" 
            class="avatar-image"
          />
          <v-icon v-else size="40" color="accent">mdi-robot</v-icon>
        </div>
        
        <div class="message-content">
          <div class="message-sender">{{ agentName }}</div>
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="chat-input">
      <div class="file-upload-container">
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileUpload" 
          multiple 
          style="display: none"
        />
        <v-btn 
          icon 
          color="primary" 
          @click="$refs.fileInput.click()" 
          class="upload-button"
          :disabled="isProcessing"
        >
          <v-icon>mdi-paperclip</v-icon>
        </v-btn>
        <div v-if="selectedFiles.length > 0" class="selected-files">
          <div v-for="(file, index) in selectedFiles" :key="index" class="selected-file">
            <span class="file-name">{{ file.name }}</span>
            <v-btn icon x-small @click="removeFile(index)" class="remove-file">
              <v-icon small>mdi-close</v-icon>
            </v-btn>
          </div>
        </div>
      </div>
      
      <v-textarea
        v-model="userInput"
        outlined
        hide-details
        rows="2"
        auto-grow
        placeholder="اكتب رسالتك هنا..."
        class="message-input"
        :disabled="isProcessing"
        @keydown.enter.prevent="sendMessage"
      ></v-textarea>
      
      <div class="action-buttons">
        <v-btn 
          icon 
          color="error" 
          @click="stopProcessing" 
          class="stop-button"
          :disabled="!isProcessing"
        >
          <v-icon>mdi-stop-circle</v-icon>
        </v-btn>
        
        <v-btn 
          icon 
          color="primary" 
          @click="sendMessage" 
          class="send-button"
          :disabled="!canSendMessage"
        >
          <v-icon>mdi-send</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * مكون محادثة الذكاء الاصطناعي
 * 
 * يوفر هذا المكون واجهة محادثة كاملة مع الوكيل الذكي
 * مع دعم إرسال الرسائل النصية والملفات وعرض المرفقات
 */
export default {
  name: 'AIChat',
  
  props: {
    /**
     * عنوان المحادثة
     */
    title: {
      type: String,
      default: 'محادثة مع الوكيل الذكي'
    },
    
    /**
     * اسم الوكيل الذكي
     */
    agentName: {
      type: String,
      default: 'الوكيل الذكي'
    },
    
    /**
     * اسم المستخدم
     */
    userName: {
      type: String,
      default: 'أنت'
    },
    
    /**
     * صورة الوكيل الذكي (اختياري)
     */
    aiAvatar: {
      type: String,
      default: null
    },
    
    /**
     * صورة المستخدم (اختياري)
     */
    userAvatar: {
      type: String,
      default: null
    },
    
    /**
     * معرف الوكيل الذكي للاتصال بالخادم
     */
    agentId: {
      type: String,
      required: true
    }
  },
  
  data() {
    return {
      messages: [],
      userInput: '',
      isTyping: false,
      isProcessing: false,
      selectedFiles: [],
      chatHistory: []
    };
  },
  
  computed: {
    /**
     * التحقق مما إذا كان يمكن إرسال رسالة
     */
    canSendMessage() {
      return !this.isProcessing && (this.userInput.trim() !== '' || this.selectedFiles.length > 0);
    }
  },
  
  watch: {
    /**
     * التمرير إلى أسفل عند إضافة رسائل جديدة
     */
    messages() {
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    }
  },
  
  mounted() {
    // تحميل سجل المحادثة السابق إذا كان متاحًا
    this.loadChatHistory();
  },
  
  methods: {
    /**
     * إرسال رسالة إلى الوكيل الذكي
     */
    async sendMessage() {
      if (!this.canSendMessage) return;
      
      const messageText = this.userInput.trim();
      const files = [...this.selectedFiles];
      
      // إضافة رسالة المستخدم إلى المحادثة
      if (messageText !== '' || files.length > 0) {
        const userMessage = {
          sender: 'user',
          text: messageText,
          timestamp: new Date(),
          attachments: files.map(file => ({
            name: file.name,
            type: file.type,
            size: file.size,
            data: file
          }))
        };
        
        this.messages.push(userMessage);
        this.userInput = '';
        this.selectedFiles = [];
        this.isProcessing = true;
        this.isTyping = true;
        
        try {
          // إرسال الرسالة إلى الخادم
          const response = await this.sendMessageToServer(messageText, files);
          
          // إضافة رد الوكيل الذكي إلى المحادثة
          this.isTyping = false;
          
          const aiMessage = {
            sender: 'ai',
            text: response.text || 'عذراً، لم أتمكن من فهم رسالتك. هل يمكنك إعادة صياغتها؟',
            timestamp: new Date(),
            attachments: response.attachments || []
          };
          
          this.messages.push(aiMessage);
          
          // حفظ سجل المحادثة
          this.saveChatHistory();
          
        } catch (error) {
          console.error('خطأ في إرسال الرسالة:', error);
          this.isTyping = false;
          
          // إضافة رسالة خطأ
          this.messages.push({
            sender: 'ai',
            text: 'عذراً، حدث خطأ أثناء معالجة رسالتك. يرجى المحاولة مرة أخرى.',
            timestamp: new Date(),
            attachments: []
          });
        } finally {
          this.isProcessing = false;
        }
      }
    },
    
    /**
     * إرسال الرسالة إلى الخادم
     * @param {String} text - نص الرسالة
     * @param {Array} files - الملفات المرفقة
     * @returns {Promise} - وعد بالرد من الخادم
     */
    async sendMessageToServer(text, files) {
      // هنا يتم الاتصال بالخادم لإرسال الرسالة والملفات
      // وهذه مجرد محاكاة للاستجابة
      
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            text: 'تلقيت رسالتك: "' + text + '"' + (files.length > 0 ? ' مع ' + files.length + ' ملفات مرفقة' : '') + '. كيف يمكنني مساعدتك؟',
            attachments: []
          });
        }, 1500);
      });
    },
    
    /**
     * إيقاف معالجة الرسالة الحالية
     */
    stopProcessing() {
      // هنا يتم إرسال طلب إيقاف المعالجة إلى الخادم
      this.isProcessing = false;
      this.isTyping = false;
      
      // إضافة رسالة إيقاف
      this.messages.push({
        sender: 'ai',
        text: 'تم إيقاف المعالجة بناءً على طلبك.',
        timestamp: new Date(),
        attachments: []
      });
    },
    
    /**
     * معالجة تحميل الملفات
     * @param {Event} event - حدث تغيير الملف
     */
    handleFileUpload(event) {
      const files = event.target.files;
      if (files.length > 0) {
        for (const file of files) {
          this.selectedFiles.push(file);
        }
      }
      // إعادة تعيين حقل الملف لتمكين تحميل نفس الملف مرة أخرى
      this.$refs.fileInput.value = '';
    },
    
    /**
     * إزالة ملف من قائمة الملفات المحددة
     * @param {Number} index - فهرس الملف المراد إزالته
     */
    removeFile(index) {
      this.selectedFiles.splice(index, 1);
    },
    
    /**
     * فتح المرفق
     * @param {Object} attachment - المرفق المراد فتحه
     */
    openAttachment(attachment) {
      // هنا يتم فتح المرفق حسب نوعه
      if (attachment.data) {
        const url = URL.createObjectURL(attachment.data);
        window.open(url, '_blank');
      } else if (attachment.url) {
        window.open(attachment.url, '_blank');
      }
    },
    
    /**
     * الحصول على أيقونة المرفق حسب نوعه
     * @param {Object} attachment - المرفق
     * @returns {String} - اسم أيقونة المرفق
     */
    getAttachmentIcon(attachment) {
      const type = attachment.type || '';
      
      if (type.startsWith('image/')) {
        return 'mdi-file-image';
      } else if (type.startsWith('video/')) {
        return 'mdi-file-video';
      } else if (type.startsWith('audio/')) {
        return 'mdi-file-music';
      } else if (type.includes('pdf')) {
        return 'mdi-file-pdf';
      } else if (type.includes('word') || type.includes('document')) {
        return 'mdi-file-word';
      } else if (type.includes('excel') || type.includes('sheet')) {
        return 'mdi-file-excel';
      } else if (type.includes('powerpoint') || type.includes('presentation')) {
        return 'mdi-file-powerpoint';
      } else if (type.includes('zip') || type.includes('compressed')) {
        return 'mdi-zip-box';
      } else {
        return 'mdi-file-document';
      }
    },
    
    /**
     * الحصول على اسم المرفق
     * @param {Object} attachment - المرفق
     * @returns {String} - اسم المرفق
     */
    getAttachmentName(attachment) {
      return attachment.name || 'مرفق';
    },
    
    /**
     * تنسيق الرسالة لعرضها
     * @param {String} message - نص الرسالة
     * @returns {String} - نص الرسالة المنسق
     */
    formatMessage(message) {
      if (!message) return '';
      
      // تحويل الروابط إلى روابط قابلة للنقر
      const urlRegex = /(https?:\/\/[^\s]+)/g;
      return message.replace(urlRegex, url => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`);
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
     * التمرير إلى أسفل المحادثة
     */
    scrollToBottom() {
      const container = this.$refs.chatMessages;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    
    /**
     * حفظ سجل المحادثة
     */
    saveChatHistory() {
      try {
        // حفظ آخر 50 رسالة فقط لتجنب تجاوز حجم التخزين
        const historyToSave = this.messages.slice(-50).map(msg => ({
          sender: msg.sender,
          text: msg.text,
          timestamp: msg.timestamp,
          // لا نحفظ الملفات الفعلية، فقط المعلومات الوصفية
          attachments: msg.attachments ? msg.attachments.map(att => ({
            name: att.name,
            type: att.type,
            size: att.size,
            url: att.url
          })) : []
        }));
        
        localStorage.setItem(`chat_history_${this.agentId}`, JSON.stringify(historyToSave));
      } catch (error) {
        console.error('خطأ في حفظ سجل المحادثة:', error);
      }
    },
    
    /**
     * تحميل سجل المحادثة
     */
    loadChatHistory() {
      try {
        const savedHistory = localStorage.getItem(`chat_history_${this.agentId}`);
        if (savedHistory) {
          this.messages = JSON.parse(savedHistory);
        }
      } catch (error) {
        console.error('خطأ في تحميل سجل المحادثة:', error);
      }
    }
  }
};
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--v-background-base, #f5f5f5);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-header {
  padding: 1rem;
  background-color: var(--v-primary-base);
  color: white;
  text-align: center;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message-container {
  display: flex;
  max-width: 80%;
  margin-bottom: 1rem;
}

.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.ai-message {
  align-self: flex-start;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 0.5rem;
  flex-shrink: 0;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-content {
  background-color: white;
  padding: 0.75rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
}

.user-message .message-content {
  background-color: var(--v-primary-lighten4);
  border-top-left-radius: 12px;
  border-top-right-radius: 0;
}

.ai-message .message-content {
  background-color: white;
  border-top-left-radius: 0;
  border-top-right-radius: 12px;
}

.message-sender {
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: var(--v-primary-darken1);
}

.message-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.message-time {
  font-size: 0.75rem;
  color: #888;
  text-align: left;
  margin-top: 0.25rem;
}

.message-attachments {
  margin-top: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.attachment-button {
  font-size: 0.75rem;
}

.chat-input {
  padding: 1rem;
  background-color: white;
  border-top: 1px solid #eee;
  display: flex;
  flex-direction: column;
}

.file-upload-container {
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
}

.selected-files {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-right: 0.5rem;
}

.selected-file {
  display: flex;
  align-items: center;
  background-color: var(--v-primary-lighten4);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.file-name {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.message-input {
  flex: 1;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
  gap: 0.5rem;
}

.typing-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 0;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  margin: 0 2px;
  background-color: #9E9E9E;
  border-radius: 50%;
  display: inline-block;
  animation: typing 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 600px) {
  .message-container {
    max-width: 90%;
  }
  
  .message-avatar {
    width: 32px;
    height: 32px;
  }
}
</style>
