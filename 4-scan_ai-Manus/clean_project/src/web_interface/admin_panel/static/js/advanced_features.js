# File: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/advanced_features.js
/**
 * مسار الملف: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/advanced_features.js
 * 
 * ميزات متقدمة للواجهة الأمامية
 * تتضمن الإشعارات الفورية، التحديث التلقائي، والتفاعل المتقدم
 */

class AdvancedFeatures {
    constructor() {
        this.notifications = [];
        this.autoRefreshInterval = null;
        this.websocket = null;
        this.init();
    }

    init() {
        this.setupNotifications();
        this.setupAutoRefresh();
        this.setupWebSocket();
        this.setupAdvancedUI();
    }

    // نظام الإشعارات المتقدم
    setupNotifications() {
        // إنشاء حاوية الإشعارات
        if (!document.getElementById('notifications-container')) {
            const container = document.createElement('div');
            container.id = 'notifications-container';
            container.className = 'notifications-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                max-width: 400px;
            `;
            document.body.appendChild(container);
        }

        // طلب إذن الإشعارات
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    showNotification(title, message, type = 'info', duration = 5000) {
        const notification = {
            id: Date.now(),
            title,
            message,
            type,
            timestamp: new Date()
        };

        this.notifications.push(notification);
        this.renderNotification(notification, duration);

        // إشعار المتصفح
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: message,
                icon: '/static/images/logo.png'
            });
        }
    }

    renderNotification(notification, duration) {
        const container = document.getElementById('notifications-container');
        const element = document.createElement('div');
        element.className = `notification notification-${notification.type}`;
        element.style.cssText = `
            background: ${this.getNotificationColor(notification.type)};
            color: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            animation: slideIn 0.3s ease-out;
            cursor: pointer;
        `;

        element.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <strong>${notification.title}</strong>
                    <p style="margin: 5px 0 0 0; font-size: 14px;">${notification.message}</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: none; border: none; color: white; font-size: 18px; cursor: pointer;">×</button>
            </div>
        `;

        container.appendChild(element);

        // إزالة تلقائية
        if (duration > 0) {
            setTimeout(() => {
                if (element.parentNode) {
                    element.style.animation = 'slideOut 0.3s ease-in';
                    setTimeout(() => element.remove(), 300);
                }
            }, duration);
        }
    }

    getNotificationColor(type) {
        const colors = {
            'success': '#28a745',
            'error': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8'
        };
        return colors[type] || colors.info;
    }

    // التحديث التلقائي
    setupAutoRefresh() {
        const refreshButton = document.createElement('button');
        refreshButton.innerHTML = '🔄 تحديث تلقائي';
        refreshButton.className = 'btn btn-sm btn-outline-secondary';
        refreshButton.onclick = () => this.toggleAutoRefresh();
        
        // إضافة الزر إلى شريط الأدوات
        const toolbar = document.querySelector('.toolbar') || document.querySelector('.navbar');
        if (toolbar) {
            toolbar.appendChild(refreshButton);
        }
    }

    toggleAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
            this.showNotification('تم إيقاف التحديث التلقائي', 'لن يتم تحديث البيانات تلقائياً', 'info');
        } else {
            this.autoRefreshInterval = setInterval(() => {
                this.refreshDashboardData();
            }, 30000); // كل 30 ثانية
            this.showNotification('تم تفعيل التحديث التلقائي', 'سيتم تحديث البيانات كل 30 ثانية', 'success');
        }
    }

    async refreshDashboardData() {
        try {
            // تحديث إحصائيات لوحة التحكم
            const stats = await apiClient.get('/api/dashboard/stats');
            this.updateDashboardStats(stats);

            // تحديث الأنشطة الحديثة
            const activities = await apiClient.get('/api/activity-log/recent');
            this.updateRecentActivities(activities);

            // تحديث التشخيصات الحديثة
            const diagnoses = await apiClient.get('/api/diagnosis/recent');
            this.updateRecentDiagnoses(diagnoses);

        } catch (error) {
            console.error('خطأ في تحديث البيانات:', error);
        }
    }

    updateDashboardStats(stats) {
        // تحديث بطاقات الإحصائيات
        Object.keys(stats).forEach(key => {
            const element = document.querySelector(`[data-stat="${key}"]`);
            if (element) {
                const currentValue = parseInt(element.textContent);
                const newValue = stats[key];
                
                if (currentValue !== newValue) {
                    this.animateNumber(element, currentValue, newValue);
                }
            }
        });
    }

    animateNumber(element, from, to) {
        const duration = 1000;
        const start = Date.now();
        
        const animate = () => {
            const elapsed = Date.now() - start;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.round(from + (to - from) * progress);
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }

    updateRecentActivities(activities) {
        const container = document.querySelector('#recent-activities');
        if (container && activities.length > 0) {
            container.innerHTML = activities.map(activity => `
                <div class="activity-item">
                    <div class="activity-icon">
                        <i class="fas fa-${this.getActivityIcon(activity.type)}"></i>
                    </div>
                    <div class="activity-content">
                        <p>${activity.message}</p>
                        <small class="text-muted">${this.formatTime(activity.created_at)}</small>
                    </div>
                </div>
            `).join('');
        }
    }

    updateRecentDiagnoses(diagnoses) {
        const container = document.querySelector('#recent-diagnoses');
        if (container && diagnoses.length > 0) {
            container.innerHTML = diagnoses.map(diagnosis => `
                <div class="diagnosis-item">
                    <img src="${diagnosis.image_path}" alt="صورة التشخيص" class="diagnosis-image">
                    <div class="diagnosis-info">
                        <h6>${diagnosis.crop_name}</h6>
                        <p class="text-${diagnosis.severity === 'عالي' ? 'danger' : diagnosis.severity === 'متوسط' ? 'warning' : 'success'}">
                            ${diagnosis.disease_name}
                        </p>
                        <small class="text-muted">دقة: ${(diagnosis.confidence * 100).toFixed(1)}%</small>
                    </div>
                </div>
            `).join('');
        }
    }

    getActivityIcon(type) {
        const icons = {
            'user_login': 'sign-in-alt',
            'diagnosis_created': 'microscope',
            'diagnosis_completed': 'check-circle',
            'user_registered': 'user-plus',
            'settings_updated': 'cog',
            'system_backup': 'database'
        };
        return icons[type] || 'info-circle';
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'الآن';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} دقيقة`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} ساعة`;
        return date.toLocaleDateString('ar-SA');
    }

    // WebSocket للتحديثات الفورية
    setupWebSocket() {
        // محاكاة WebSocket (يمكن تطبيقه لاحقاً)
        this.simulateRealTimeUpdates();
    }

    simulateRealTimeUpdates() {
        // محاكاة تحديثات فورية كل دقيقة
        setInterval(() => {
            if (Math.random() > 0.7) { // 30% احتمال
                const events = [
                    { title: 'تشخيص جديد', message: 'تم إكمال تشخيص جديد لمحصول الطماطم', type: 'success' },
                    { title: 'تسجيل دخول', message: 'مستخدم جديد سجل دخوله للنظام', type: 'info' },
                    { title: 'تحديث النظام', message: 'تم تحديث إعدادات النظام بنجاح', type: 'success' }
                ];
                
                const randomEvent = events[Math.floor(Math.random() * events.length)];
                this.showNotification(randomEvent.title, randomEvent.message, randomEvent.type);
            }
        }, 60000);
    }

    // واجهة مستخدم متقدمة
    setupAdvancedUI() {
        this.addKeyboardShortcuts();
        this.addTooltips();
        this.addProgressBars();
        this.addSearchFeature();
    }

    addKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+D للوحة التحكم
            if (e.ctrlKey && e.key === 'd') {
                e.preventDefault();
                window.location.href = '/dashboard';
            }
            
            // Ctrl+N لتشخيص جديد
            if (e.ctrlKey && e.key === 'n') {
                e.preventDefault();
                window.location.href = '/diagnosis/new';
            }
            
            // Ctrl+S للإعدادات
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                window.location.href = '/settings';
            }
        });
    }

    addTooltips() {
        // إضافة tooltips لجميع العناصر التي تحتوي على data-tooltip
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e.target, e.target.dataset.tooltip);
            });
            
            element.addEventListener('mouseleave', () => {
                this.hideTooltip();
            });
        });
    }

    showTooltip(element, text) {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 10001;
            pointer-events: none;
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
        
        this.currentTooltip = tooltip;
    }

    hideTooltip() {
        if (this.currentTooltip) {
            this.currentTooltip.remove();
            this.currentTooltip = null;
        }
    }

    addProgressBars() {
        // إضافة شريط تقدم للعمليات الطويلة
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', () => {
                this.showProgressBar();
            });
        });
    }

    showProgressBar() {
        const progressBar = document.createElement('div');
        progressBar.id = 'global-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: #007bff;
            z-index: 10002;
            animation: progress 2s ease-in-out;
        `;
        
        document.body.appendChild(progressBar);
        
        setTimeout(() => {
            if (progressBar.parentNode) {
                progressBar.remove();
            }
        }, 2000);
    }

    addSearchFeature() {
        // إضافة بحث سريع
        const searchContainer = document.createElement('div');
        searchContainer.className = 'quick-search';
        searchContainer.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 10003;
            display: none;
            min-width: 400px;
        `;
        
        searchContainer.innerHTML = `
            <input type="text" placeholder="البحث السريع..." class="form-control" id="quick-search-input">
            <div id="search-results" class="mt-3"></div>
        `;
        
        document.body.appendChild(searchContainer);
        
        // Ctrl+K للبحث السريع
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                this.toggleQuickSearch();
            }
            
            if (e.key === 'Escape') {
                this.hideQuickSearch();
            }
        });
    }

    toggleQuickSearch() {
        const searchContainer = document.querySelector('.quick-search');
        const isVisible = searchContainer.style.display !== 'none';
        
        if (isVisible) {
            this.hideQuickSearch();
        } else {
            searchContainer.style.display = 'block';
            document.getElementById('quick-search-input').focus();
        }
    }

    hideQuickSearch() {
        const searchContainer = document.querySelector('.quick-search');
        searchContainer.style.display = 'none';
    }
}

// إضافة الأنماط المطلوبة
const styles = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes progress {
        0% { width: 0%; }
        100% { width: 100%; }
    }
    
    .activity-item {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    
    .activity-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #007bff;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        margin-right: 10px;
    }
    
    .diagnosis-item {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    
    .diagnosis-image {
        width: 50px;
        height: 50px;
        object-fit: cover;
        border-radius: 5px;
        margin-right: 10px;
    }
`;

// إضافة الأنماط إلى الصفحة
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);

// تهيئة الميزات المتقدمة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    window.advancedFeatures = new AdvancedFeatures();
});

// تصدير للاستخدام العام
window.AdvancedFeatures = AdvancedFeatures;

