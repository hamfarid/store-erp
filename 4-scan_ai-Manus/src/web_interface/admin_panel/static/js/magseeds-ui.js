/* File: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/magseeds-ui.js */
/* JavaScript للتفاعلات والميزات المتقدمة مستوحى من MAGseeds */

class MagseedsUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupSidebar();
        this.setupAnimations();
        this.setupFormValidation();
        this.setupTooltips();
        this.setupProgressBars();
        this.setupCharts();
        this.setupNotifications();
        this.setupTheme();
    }

    // إعداد الشريط الجانبي
    setupSidebar() {
        const sidebarToggle = document.querySelector('.sidebar-toggle');
        const sidebar = document.querySelector('.magseeds-sidebar');
        const overlay = document.querySelector('.sidebar-overlay');

        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', () => {
                sidebar.classList.toggle('open');
                if (overlay) overlay.classList.toggle('active');
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('open');
                overlay.classList.remove('active');
            });
        }

        // تفعيل الرابط النشط
        const currentPath = window.location.pathname;
        const sidebarLinks = document.querySelectorAll('.magseeds-sidebar-menu a');
        
        sidebarLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

    // إعداد الرسوم المتحركة
    setupAnimations() {
        // تأثير الظهور التدريجي للبطاقات
        const cards = document.querySelectorAll('.magseeds-card');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
            observer.observe(card);
        });

        // تأثير الأزرار
        const buttons = document.querySelectorAll('.magseeds-btn');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    // إعداد التحقق من النماذج
    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('.magseeds-input, .magseeds-textarea, .magseeds-select');
            
            inputs.forEach(input => {
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => this.clearFieldError(input));
            });
            
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required');
        const type = field.getAttribute('type');
        
        let isValid = true;
        let errorMessage = '';

        if (isRequired && !value) {
            isValid = false;
            errorMessage = 'هذا الحقل مطلوب';
        } else if (value) {
            switch (type) {
                case 'email':
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(value)) {
                        isValid = false;
                        errorMessage = 'يرجى إدخال بريد إلكتروني صحيح';
                    }
                    break;
                case 'tel':
                    const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
                    if (!phoneRegex.test(value)) {
                        isValid = false;
                        errorMessage = 'يرجى إدخال رقم هاتف صحيح';
                    }
                    break;
                case 'url':
                    try {
                        new URL(value);
                    } catch {
                        isValid = false;
                        errorMessage = 'يرجى إدخال رابط صحيح';
                    }
                    break;
            }
        }

        this.showFieldValidation(field, isValid, errorMessage);
        return isValid;
    }

    showFieldValidation(field, isValid, errorMessage) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) existingError.remove();

        if (!isValid) {
            field.classList.add('error');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.textContent = errorMessage;
            errorDiv.style.color = 'var(--magseeds-error)';
            errorDiv.style.fontSize = '0.75rem';
            errorDiv.style.marginTop = '0.25rem';
            field.parentNode.appendChild(errorDiv);
        } else {
            field.classList.remove('error');
        }
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) existingError.remove();
    }

    validateForm(form) {
        const inputs = form.querySelectorAll('.magseeds-input, .magseeds-textarea, .magseeds-select');
        let isFormValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isFormValid = false;
            }
        });

        return isFormValid;
    }

    // إعداد التلميحات
    setupTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                const tooltip = document.createElement('div');
                tooltip.className = 'magseeds-tooltip';
                tooltip.textContent = e.target.getAttribute('data-tooltip');
                tooltip.style.cssText = `
                    position: absolute;
                    background: var(--magseeds-gray-800);
                    color: white;
                    padding: 0.5rem 0.75rem;
                    border-radius: var(--magseeds-border-radius);
                    font-size: 0.75rem;
                    z-index: 1000;
                    pointer-events: none;
                    opacity: 0;
                    transition: opacity 0.2s;
                `;
                
                document.body.appendChild(tooltip);
                
                const rect = e.target.getBoundingClientRect();
                tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
                tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
                
                setTimeout(() => tooltip.style.opacity = '1', 10);
                
                e.target._tooltip = tooltip;
            });
            
            element.addEventListener('mouseleave', (e) => {
                if (e.target._tooltip) {
                    e.target._tooltip.remove();
                    delete e.target._tooltip;
                }
            });
        });
    }

    // إعداد أشرطة التقدم
    setupProgressBars() {
        const progressBars = document.querySelectorAll('.magseeds-progress');
        
        progressBars.forEach(bar => {
            const value = bar.getAttribute('data-value') || 0;
            const fill = bar.querySelector('.progress-fill');
            
            if (fill) {
                setTimeout(() => {
                    fill.style.width = value + '%';
                }, 100);
            }
        });
    }

    // إعداد الرسوم البيانية
    setupCharts() {
        // رسم بياني بسيط للإحصائيات
        const chartElements = document.querySelectorAll('.magseeds-chart');
        
        chartElements.forEach(chart => {
            const data = JSON.parse(chart.getAttribute('data-chart') || '[]');
            this.createSimpleChart(chart, data);
        });
    }

    createSimpleChart(container, data) {
        if (!data.length) return;
        
        const maxValue = Math.max(...data.map(d => d.value));
        const chartHTML = data.map(item => `
            <div class="chart-bar" style="height: ${(item.value / maxValue) * 100}%; background: var(--magseeds-primary);">
                <span class="chart-label">${item.label}</span>
                <span class="chart-value">${item.value}</span>
            </div>
        `).join('');
        
        container.innerHTML = `<div class="chart-container">${chartHTML}</div>`;
        container.style.cssText = `
            display: flex;
            align-items: end;
            gap: 0.5rem;
            height: 200px;
            padding: 1rem;
        `;
    }

    // إعداد الإشعارات
    setupNotifications() {
        window.showNotification = (message, type = 'info', duration = 5000) => {
            const notification = document.createElement('div');
            notification.className = `magseeds-notification magseeds-notification-${type}`;
            notification.innerHTML = `
                <div class="notification-content">
                    <span class="notification-icon">${this.getNotificationIcon(type)}</span>
                    <span class="notification-message">${message}</span>
                    <button class="notification-close">&times;</button>
                </div>
            `;
            
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                left: 20px;
                background: white;
                border-radius: var(--magseeds-border-radius);
                box-shadow: var(--magseeds-shadow-lg);
                padding: 1rem;
                z-index: 1000;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                border-right: 4px solid var(--magseeds-${type === 'error' ? 'error' : type === 'warning' ? 'warning' : type === 'success' ? 'success' : 'info'});
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.transform = 'translateX(0)';
            }, 10);
            
            const closeBtn = notification.querySelector('.notification-close');
            closeBtn.addEventListener('click', () => {
                notification.style.transform = 'translateX(-100%)';
                setTimeout(() => notification.remove(), 300);
            });
            
            if (duration > 0) {
                setTimeout(() => {
                    notification.style.transform = 'translateX(-100%)';
                    setTimeout(() => notification.remove(), 300);
                }, duration);
            }
        };
    }

    getNotificationIcon(type) {
        const icons = {
            success: '✓',
            error: '✗',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[type] || icons.info;
    }

    // إعداد السمة
    setupTheme() {
        const themeToggle = document.querySelector('.theme-toggle');
        const currentTheme = localStorage.getItem('magseeds-theme') || 'light';
        
        document.documentElement.setAttribute('data-theme', currentTheme);
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const newTheme = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('magseeds-theme', newTheme);
            });
        }
    }

    // دوال مساعدة
    static formatNumber(num) {
        return new Intl.NumberFormat('ar-SA').format(num);
    }

    static formatDate(date) {
        return new Intl.DateTimeFormat('ar-SA').format(new Date(date));
    }

    static formatCurrency(amount, currency = 'SAR') {
        return new Intl.NumberFormat('ar-SA', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }
}

// تهيئة النظام عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    new MagseedsUI();
});

// إضافة أنماط CSS للتأثيرات
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    .magseeds-input.error,
    .magseeds-textarea.error,
    .magseeds-select.error {
        border-color: var(--magseeds-error);
        box-shadow: 0 0 0 3px rgba(244, 67, 54, 0.1);
    }

    .magseeds-progress {
        width: 100%;
        height: 8px;
        background: var(--magseeds-gray-200);
        border-radius: 4px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--magseeds-primary), var(--magseeds-secondary));
        width: 0%;
        transition: width 1s ease-in-out;
    }

    [data-theme="dark"] {
        --magseeds-gray-50: #1a1a1a;
        --magseeds-gray-100: #2d2d2d;
        --magseeds-gray-200: #404040;
        --magseeds-gray-800: #f5f5f5;
        --magseeds-gray-900: #ffffff;
    }

    [data-theme="dark"] body {
        background-color: var(--magseeds-gray-50);
        color: var(--magseeds-gray-800);
    }

    [data-theme="dark"] .magseeds-card {
        background: var(--magseeds-gray-100);
        border-color: var(--magseeds-gray-200);
    }
`;
document.head.appendChild(style);

