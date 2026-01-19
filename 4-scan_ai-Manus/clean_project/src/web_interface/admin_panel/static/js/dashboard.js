# File: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/dashboard.js
/**
 * مسار الملف: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/dashboard.js
 * 
 * ملف JavaScript للوحة التحكم
 * يحتوي على وظائف تحديث البيانات والمخططات
 */

document.addEventListener('DOMContentLoaded', function() {
    // تهيئة لوحة التحكم
    initDashboard();
});

async function initDashboard() {
    try {
        // تحديث إحصائيات النظام
        await updateSystemStats();
        
        // تحديث المخططات
        await updateCharts();
        
        // تحديث سجل النشاط
        await updateActivityLog();
        
        // إعداد التحديث التلقائي
        setInterval(updateSystemStats, 30000); // كل 30 ثانية
        setInterval(updateCharts, 60000); // كل دقيقة
        
    } catch (error) {
        console.error('خطأ في تهيئة لوحة التحكم:', error);
        showError('فشل في تحميل بيانات لوحة التحكم');
    }
}

async function updateSystemStats() {
    try {
        // الحصول على صحة النظام
        const healthData = await apiClient.getSystemHealth();
        updateHealthIndicator(healthData);
        
        // الحصول على معلومات الذكاء الاصطناعي
        const aiInfo = await apiClient.getAIInfo();
        updateAIStats(aiInfo);
        
    } catch (error) {
        console.error('خطأ في تحديث إحصائيات النظام:', error);
    }
}

function updateHealthIndicator(healthData) {
    const healthIndicator = document.querySelector('.health-indicator');
    if (healthIndicator) {
        healthIndicator.className = `health-indicator ${healthData.status}`;
        healthIndicator.textContent = healthData.status === 'healthy' ? 'سليم' : 'خطأ';
    }
}

function updateAIStats(aiInfo) {
    // تحديث دقة النموذج
    const accuracyElement = document.querySelector('.model-accuracy .value');
    if (accuracyElement && aiInfo.model_accuracy) {
        accuracyElement.textContent = `${aiInfo.model_accuracy}%`;
    }
    
    // تحديث عدد النماذج النشطة
    const activeModelsElement = document.querySelector('.active-models .value');
    if (activeModelsElement && aiInfo.active_models) {
        activeModelsElement.textContent = aiInfo.active_models;
    }
    
    // تحديث وقت الاستجابة
    const responseTimeElement = document.querySelector('.response-time .value');
    if (responseTimeElement && aiInfo.response_time) {
        responseTimeElement.textContent = `${aiInfo.response_time} ثانية`;
    }
}

async function updateCharts() {
    try {
        // مخطط استخدام النظام
        await updateSystemUsageChart();
        
        // مخطط أداء النموذج
        await updateModelPerformanceChart();
        
    } catch (error) {
        console.error('خطأ في تحديث المخططات:', error);
    }
}

async function updateSystemUsageChart() {
    const ctx = document.getElementById('systemUsageChart');
    if (!ctx) return;
    
    // بيانات وهمية للاختبار - يجب استبدالها ببيانات حقيقية
    const data = {
        labels: ['الساعة 1', 'الساعة 2', 'الساعة 3', 'الساعة 4', 'الساعة 5', 'الساعة 6'],
        datasets: [{
            label: 'استخدام المعالج',
            data: [65, 59, 80, 81, 56, 55],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1
        }, {
            label: 'استخدام الذاكرة',
            data: [45, 49, 60, 71, 46, 45],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.1
        }]
    };
    
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'استخدام موارد النظام'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

async function updateModelPerformanceChart() {
    const ctx = document.getElementById('modelPerformanceChart');
    if (!ctx) return;
    
    // بيانات وهمية للاختبار
    const data = {
        labels: ['الدقة', 'الاستدعاء', 'F1-Score', 'الدقة العامة'],
        datasets: [{
            label: 'أداء النموذج',
            data: [95, 87, 91, 93],
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    };
    
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'مقاييس أداء النموذج'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

async function updateActivityLog() {
    try {
        const logs = await apiClient.getActivityLogs(10);
        displayActivityLogs(logs);
    } catch (error) {
        console.error('خطأ في تحديث سجل النشاط:', error);
    }
}

function displayActivityLogs(logs) {
    const logContainer = document.querySelector('.activity-log-list');
    if (!logContainer) return;
    
    logContainer.innerHTML = '';
    
    if (!logs || logs.length === 0) {
        logContainer.innerHTML = '<p class="no-logs">لا توجد أنشطة حديثة</p>';
        return;
    }
    
    logs.forEach(log => {
        const logElement = document.createElement('div');
        logElement.className = 'activity-log-item';
        logElement.innerHTML = `
            <div class="log-icon">
                <i class="material-icons">${getLogIcon(log.type)}</i>
            </div>
            <div class="log-content">
                <p class="log-message">${log.message}</p>
                <span class="log-time">${formatTime(log.timestamp)}</span>
            </div>
        `;
        logContainer.appendChild(logElement);
    });
}

function getLogIcon(logType) {
    const icons = {
        'info': 'info',
        'warning': 'warning',
        'error': 'error',
        'success': 'check_circle',
        'ai': 'psychology',
        'diagnosis': 'biotech'
    };
    return icons[logType] || 'info';
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('ar-SA', {
        hour: '2-digit',
        minute: '2-digit',
        day: 'numeric',
        month: 'short'
    });
}

function showError(message) {
    // إظهار رسالة خطأ للمستخدم
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

