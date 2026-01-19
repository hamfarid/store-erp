<!-- صفحة المساعد الذكي -->
<template>
  <div class="ai-agent-page">
    <!-- Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fas fa-robot me-3"></i>
            المساعد الذكي
          </h1>
          <p class="page-subtitle">تفاعل مع المساعد الذكي للحصول على المساعدة والإرشادات</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-outline-primary" @click="clearChat">
            <i class="fas fa-trash me-2"></i>
            مسح المحادثة
          </button>
          <button class="btn btn-primary" @click="newChat">
            <i class="fas fa-plus me-2"></i>
            محادثة جديدة
          </button>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- قائمة المحادثات -->
      <div class="col-lg-3">
        <div class="chat-sidebar">
          <div class="sidebar-header">
            <h6>المحادثات السابقة</h6>
            <button class="btn btn-sm btn-outline-primary" @click="loadChatHistory">
              <i class="fas fa-sync-alt"></i>
            </button>
          </div>
          
          <div class="chat-list">
            <div class="chat-item" 
                 v-for="chat in chatHistory" 
                 :key="chat.id"
                 :class="{ active: currentChatId === chat.id }"
                 @click="loadChat(chat.id)">
              <div class="chat-preview">
                <div class="chat-title">{{ chat.title || 'محادثة جديدة' }}</div>
                <div class="chat-date">{{ formatDate(chat.created_at) }}</div>
                <div class="chat-snippet">{{ chat.last_message }}</div>
              </div>
              <div class="chat-actions">
                <button class="btn btn-sm btn-outline-danger" @click.stop="deleteChat(chat.id)">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- منطقة المحادثة -->
      <div class="col-lg-9">
        <div class="chat-container">
          <!-- رأس المحادثة -->
          <div class="chat-header">
            <div class="agent-info">
              <div class="agent-avatar">
                <i class="fas fa-robot"></i>
              </div>
              <div class="agent-details">
                <h6>مساعد Gaara الذكي</h6>
                <span class="agent-status online">متصل</span>
              </div>
            </div>
            
            <div class="chat-controls">
              <button class="btn btn-sm btn-outline-info" @click="showAgentSettings">
                <i class="fas fa-cog"></i>
              </button>
              <button class="btn btn-sm btn-outline-success" @click="exportChat">
                <i class="fas fa-download"></i>
              </button>
            </div>
          </div>
          
          <!-- منطقة الرسائل -->
          <div class="chat-messages" ref="messagesContainer">
            <div class="message-item" 
                 v-for="message in currentMessages" 
                 :key="message.id"
                 :class="{ 'user-message': message.sender === 'user', 'agent-message': message.sender === 'agent' }">
              
              <div class="message-avatar">
                <i v-if="message.sender === 'user'" class="fas fa-user"></i>
                <i v-else class="fas fa-robot"></i>
              </div>
              
              <div class="message-content">
                <div class="message-header">
                  <span class="message-sender">
                    {{ message.sender === 'user' ? 'أنت' : 'المساعد الذكي' }}
                  </span>
                  <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                </div>
                
                <div class="message-text" v-html="formatMessage(message.content)"></div>
                
                <!-- مرفقات الرسالة -->
                <div class="message-attachments" v-if="message.attachments && message.attachments.length">
                  <div class="attachment-item" v-for="attachment in message.attachments" :key="attachment.id">
                    <i class="fas fa-paperclip me-2"></i>
                    <a :href="attachment.url" target="_blank">{{ attachment.name }}</a>
                  </div>
                </div>
                
                <!-- أزرار الإجراءات للرسائل -->
                <div class="message-actions" v-if="message.sender === 'agent'">
                  <button class="btn btn-sm btn-outline-primary" @click="copyMessage(message.content)">
                    <i class="fas fa-copy"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-success" @click="likeMessage(message.id)">
                    <i class="fas fa-thumbs-up"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-warning" @click="dislikeMessage(message.id)">
                    <i class="fas fa-thumbs-down"></i>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- مؤشر الكتابة -->
            <div class="typing-indicator" v-if="isTyping">
              <div class="message-item agent-message">
                <div class="message-avatar">
                  <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                  <div class="typing-animation">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- منطقة الإدخال -->
          <div class="chat-input">
            <div class="input-container">
              <div class="input-group">
                <button class="btn btn-outline-secondary" @click="showAttachmentOptions">
                  <i class="fas fa-paperclip"></i>
                </button>
                
                <textarea class="form-control" 
                         v-model="newMessage"
                         @keydown.enter.prevent="sendMessage"
                         @keydown.shift.enter="newMessage += '\n'"
                         placeholder="اكتب رسالتك هنا... (Enter للإرسال، Shift+Enter لسطر جديد)"
                         rows="1"
                         ref="messageInput"></textarea>
                
                <button class="btn btn-primary" 
                        @click="sendMessage"
                        :disabled="!newMessage.trim() || isLoading">
                  <i v-if="isLoading" class="fas fa-spinner fa-spin"></i>
                  <i v-else class="fas fa-paper-plane"></i>
                </button>
              </div>
              
              <!-- اقتراحات سريعة -->
              <div class="quick-suggestions" v-if="quickSuggestions.length && !newMessage">
                <div class="suggestion-item" 
                     v-for="suggestion in quickSuggestions" 
                     :key="suggestion.id"
                     @click="selectSuggestion(suggestion.text)">
                  {{ suggestion.text }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- نافذة إعدادات المساعد -->
    <div class="modal fade" id="agentSettingsModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">إعدادات المساعد الذكي</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="setting-item">
              <label class="form-label">نمط المحادثة</label>
              <select class="form-select" v-model="agentSettings.conversation_mode">
                <option value="helpful">مساعد</option>
                <option value="professional">مهني</option>
                <option value="casual">ودود</option>
                <option value="technical">تقني</option>
              </select>
            </div>
            
            <div class="setting-item">
              <label class="form-label">مستوى التفصيل</label>
              <select class="form-select" v-model="agentSettings.detail_level">
                <option value="brief">مختصر</option>
                <option value="moderate">متوسط</option>
                <option value="detailed">مفصل</option>
              </select>
            </div>
            
            <div class="setting-item">
              <label class="form-label">اللغة المفضلة</label>
              <select class="form-select" v-model="agentSettings.language">
                <option value="ar">العربية</option>
                <option value="en">الإنجليزية</option>
                <option value="mixed">مختلطة</option>
              </select>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="agentSettings.enable_suggestions">
                <label class="form-check-label">تفعيل الاقتراحات السريعة</label>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="agentSettings.save_history">
                <label class="form-check-label">حفظ تاريخ المحادثات</label>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
            <button type="button" class="btn btn-primary" @click="saveAgentSettings">حفظ الإعدادات</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAIStore, useSystemStore } from '../../store/index.js'
import { aiAgentAPI } from '../../services/api.js'

export default {
  name: 'AIAgent',
  
  setup() {
    const router = useRouter()
    const aiStore = useAIStore()
    const systemStore = useSystemStore()
    
    const messagesContainer = ref(null)
    const messageInput = ref(null)
    
    // البيانات
    const currentChatId = ref(null)
    const newMessage = ref('')
    const isLoading = ref(false)
    const isTyping = ref(false)
    
    const agentSettings = ref({
      conversation_mode: 'helpful',
      detail_level: 'moderate',
      language: 'ar',
      enable_suggestions: true,
      save_history: true
    })
    
    const quickSuggestions = ref([
      { id: 1, text: 'كيف يمكنني تشخيص أمراض النباتات؟' },
      { id: 2, text: 'ما هي أفضل طرق تحسين الصور؟' },
      { id: 3, text: 'كيف أستخدم نظام إدارة الحاويات؟' },
      { id: 4, text: 'أريد مساعدة في تهجين النباتات' }
    ])
    
    // البيانات المحسوبة
    const chatHistory = computed(() => aiStore.chatHistory)
    const currentMessages = computed(() => aiStore.currentMessages)
    
    // الوظائف
    const newChat = async () => {
      try {
        const response = await aiAgentAPI.createNewChat()
        currentChatId.value = response.data.chat_id
        aiStore.setCurrentMessages([])
        
        systemStore.addNotification({
          type: 'success',
          title: 'محادثة جديدة',
          message: 'تم إنشاء محادثة جديدة'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ',
          message: 'فشل في إنشاء محادثة جديدة'
        })
      }
    }
    
    const loadChat = async (chatId) => {
      try {
        currentChatId.value = chatId
        const response = await aiAgentAPI.getChatMessages(chatId)
        aiStore.setCurrentMessages(response.data.messages)
        
        await nextTick()
        scrollToBottom()
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ',
          message: 'فشل في تحميل المحادثة'
        })
      }
    }
    
    const clearChat = () => {
      if (confirm('هل أنت متأكد من مسح المحادثة الحالية؟')) {
        aiStore.setCurrentMessages([])
        currentChatId.value = null
      }
    }
    
    const deleteChat = async (chatId) => {
      if (confirm('هل أنت متأكد من حذف هذه المحادثة؟')) {
        try {
          await aiAgentAPI.deleteChat(chatId)
          await loadChatHistory()
          
          if (currentChatId.value === chatId) {
            currentChatId.value = null
            aiStore.setCurrentMessages([])
          }
          
          systemStore.addNotification({
            type: 'success',
            title: 'تم الحذف',
            message: 'تم حذف المحادثة بنجاح'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ',
            message: 'فشل في حذف المحادثة'
          })
        }
      }
    }
    
    const sendMessage = async () => {
      if (!newMessage.value.trim() || isLoading.value) return
      
      const messageText = newMessage.value.trim()
      newMessage.value = ''
      
      // إضافة رسالة المستخدم
      const userMessage = {
        id: Date.now(),
        sender: 'user',
        content: messageText,
        timestamp: new Date().toISOString()
      }
      
      aiStore.addMessage(userMessage)
      
      await nextTick()
      scrollToBottom()
      
      // إرسال الرسالة للمساعد
      isLoading.value = true
      isTyping.value = true
      
      try {
        const response = await aiAgentAPI.sendMessage({
          chat_id: currentChatId.value,
          message: messageText,
          settings: agentSettings.value
        })
        
        // إضافة رد المساعد
        const agentMessage = {
          id: Date.now() + 1,
          sender: 'agent',
          content: response.data.response,
          timestamp: new Date().toISOString()
        }
        
        aiStore.addMessage(agentMessage)
        
        // تحديث معرف المحادثة إذا كانت جديدة
        if (!currentChatId.value) {
          currentChatId.value = response.data.chat_id
        }
        
        await nextTick()
        scrollToBottom()
        
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الإرسال',
          message: 'فشل في إرسال الرسالة'
        })
      } finally {
        isLoading.value = false
        isTyping.value = false
      }
    }
    
    const selectSuggestion = (suggestionText) => {
      newMessage.value = suggestionText
      messageInput.value.focus()
    }
    
    const formatMessage = (content) => {
      // تنسيق الرسالة (Markdown, روابط، إلخ)
      return content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>')
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ar-SA')
    }
    
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('ar-SA', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const scrollToBottom = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }
    
    const copyMessage = (content) => {
      navigator.clipboard.writeText(content).then(() => {
        systemStore.addNotification({
          type: 'success',
          title: 'تم النسخ',
          message: 'تم نسخ الرسالة إلى الحافظة'
        })
      })
    }
    
    const likeMessage = async (messageId) => {
      try {
        await aiAgentAPI.rateMessage(messageId, 'like')
        systemStore.addNotification({
          type: 'success',
          title: 'شكراً لك',
          message: 'تم تسجيل تقييمك'
        })
      } catch (error) {
        console.error('خطأ في تقييم الرسالة:', error)
      }
    }
    
    const dislikeMessage = async (messageId) => {
      try {
        await aiAgentAPI.rateMessage(messageId, 'dislike')
        systemStore.addNotification({
          type: 'info',
          title: 'تم التسجيل',
          message: 'سنعمل على تحسين الإجابات'
        })
      } catch (error) {
        console.error('خطأ في تقييم الرسالة:', error)
      }
    }
    
    const loadChatHistory = async () => {
      try {
        await aiStore.fetchChatHistory()
      } catch (error) {
        console.error('خطأ في تحميل تاريخ المحادثات:', error)
      }
    }
    
    const showAgentSettings = () => {
      const modal = new bootstrap.Modal(document.getElementById('agentSettingsModal'))
      modal.show()
    }
    
    const saveAgentSettings = async () => {
      try {
        await aiAgentAPI.updateSettings(agentSettings.value)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم الحفظ',
          message: 'تم حفظ إعدادات المساعد'
        })
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('agentSettingsModal'))
        modal.hide()
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ',
          message: 'فشل في حفظ الإعدادات'
        })
      }
    }
    
    const showAttachmentOptions = () => {
      systemStore.addNotification({
        type: 'info',
        title: 'قريباً',
        message: 'ستتوفر إمكانية إرفاق الملفات قريباً'
      })
    }
    
    const exportChat = () => {
      if (currentMessages.value.length === 0) {
        systemStore.addNotification({
          type: 'warning',
          title: 'لا توجد رسائل',
          message: 'لا توجد رسائل لتصديرها'
        })
        return
      }
      
      const chatData = currentMessages.value.map(msg => ({
        sender: msg.sender === 'user' ? 'المستخدم' : 'المساعد الذكي',
        message: msg.content,
        time: formatTime(msg.timestamp)
      }))
      
      const dataStr = JSON.stringify(chatData, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `chat-export-${new Date().toISOString().split('T')[0]}.json`
      link.click()
      
      URL.revokeObjectURL(url)
      
      systemStore.addNotification({
        type: 'success',
        title: 'تم التصدير',
        message: 'تم تصدير المحادثة بنجاح'
      })
    }
    
    // تحميل البيانات عند التحميل
    onMounted(async () => {
      await loadChatHistory()
      
      // تحميل الإعدادات المحفوظة
      try {
        const response = await aiAgentAPI.getSettings()
        agentSettings.value = { ...agentSettings.value, ...response.data }
      } catch (error) {
        console.error('خطأ في تحميل الإعدادات:', error)
      }
      
      // إنشاء محادثة جديدة إذا لم تكن موجودة
      if (!currentChatId.value) {
        await newChat()
      }
    })
    
    return {
      currentChatId,
      newMessage,
      isLoading,
      isTyping,
      agentSettings,
      quickSuggestions,
      chatHistory,
      currentMessages,
      messagesContainer,
      messageInput,
      newChat,
      loadChat,
      clearChat,
      deleteChat,
      sendMessage,
      selectSuggestion,
      formatMessage,
      formatDate,
      formatTime,
      copyMessage,
      likeMessage,
      dislikeMessage,
      loadChatHistory,
      showAgentSettings,
      saveAgentSettings,
      showAttachmentOptions,
      exportChat
    }
  }
}
</script>

<style scoped>
.ai-agent-page {
  padding: 20px;
  font-family: 'Cairo', sans-serif;
  height: calc(100vh - 100px);
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6c757d;
  margin-bottom: 0;
}

.chat-sidebar {
  background: white;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e3e6f0;
  display: flex;
  justify-content: between;
  align-items: center;
}

.sidebar-header h6 {
  margin: 0;
  font-weight: 600;
  color: #2c3e50;
  flex: 1;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.chat-item {
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-item:hover {
  background: #f8f9fc;
  border-color: #e3e6f0;
}

.chat-item.active {
  background: linear-gradient(45deg, #4e73df, #224abe);
  color: white;
}

.chat-preview {
  flex: 1;
}

.chat-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.chat-date {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-bottom: 0.25rem;
}

.chat-snippet {
  font-size: 0.8rem;
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-actions {
  margin-right: 0.5rem;
}

.chat-container {
  background: white;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e3e6f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.agent-info {
  display: flex;
  align-items: center;
}

.agent-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(45deg, #4e73df, #224abe);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  margin-left: 1rem;
}

.agent-details h6 {
  margin: 0;
  font-weight: 600;
  color: #2c3e50;
}

.agent-status {
  font-size: 0.8rem;
  color: #1cc88a;
}

.agent-status.online::before {
  content: '●';
  margin-left: 0.5rem;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.message-item {
  display: flex;
  margin-bottom: 1.5rem;
  align-items: flex-start;
}

.message-item.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
  margin: 0 1rem;
}

.user-message .message-avatar {
  background: linear-gradient(45deg, #1cc88a, #13855c);
}

.agent-message .message-avatar {
  background: linear-gradient(45deg, #4e73df, #224abe);
}

.message-content {
  max-width: 70%;
  background: #f8f9fc;
  border-radius: 15px;
  padding: 1rem;
  position: relative;
}

.user-message .message-content {
  background: linear-gradient(45deg, #4e73df, #224abe);
  color: white;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.message-sender {
  font-weight: 600;
  font-size: 0.85rem;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
}

.message-text {
  line-height: 1.5;
  word-wrap: break-word;
}

.message-attachments {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.attachment-item {
  margin-bottom: 0.25rem;
}

.attachment-item a {
  color: inherit;
  text-decoration: none;
}

.attachment-item a:hover {
  text-decoration: underline;
}

.message-actions {
  margin-top: 0.5rem;
  display: flex;
  gap: 0.25rem;
}

.message-actions .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.typing-indicator {
  margin-bottom: 1rem;
}

.typing-animation {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.typing-animation span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6c757d;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-animation span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-animation span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.chat-input {
  padding: 1.5rem;
  border-top: 1px solid #e3e6f0;
}

.input-container {
  position: relative;
}

.input-group textarea {
  resize: none;
  border-radius: 25px;
  padding: 0.75rem 1rem;
  font-family: 'Cairo', sans-serif;
}

.input-group .btn {
  border-radius: 50%;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quick-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.suggestion-item {
  background: #f8f9fc;
  border: 1px solid #e3e6f0;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.suggestion-item:hover {
  background: #4e73df;
  color: white;
  border-color: #4e73df;
}

.setting-item {
  margin-bottom: 1.5rem;
}

.setting-item:last-child {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .ai-agent-page {
    padding: 10px;
  }
  
  .page-header .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .chat-sidebar {
    height: 300px;
    margin-bottom: 1rem;
  }
  
  .chat-container {
    height: calc(100vh - 400px);
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .quick-suggestions {
    flex-direction: column;
  }
  
  .suggestion-item {
    text-align: center;
  }
}
</style>

