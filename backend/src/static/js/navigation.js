/* ملف: /home/ubuntu/complete_inventory_system/backend/src/static/js/navigation.js
   JavaScript لقوائم التنقل العلوية */

class NavigationManager {
    constructor() {
        this.currentModule = '';
        this.currentPage = '';
        this.breadcrumbs = [];
        this.notifications = [];
        this.init();
    }

    init() {
        this.createNavigationBar();
        this.setupEventListeners();
        this.loadNotifications();
        this.updateBreadcrumbs();
        this.highlightCurrentPage();
    }

    createNavigationBar() {
        const navbar = document.createElement('nav');
        navbar.className = 'main-navbar';
        navbar.innerHTML = this.getNavigationHTML();
        
        // إدراج شريط التنقل في بداية الصفحة
        document.body.insertBefore(navbar, document.body.firstChild);
        
        // إنشاء شريط التنقل الثانوي
        const secondaryNavbar = document.createElement('div');
        secondaryNavbar.className = 'secondary-navbar';
        secondaryNavbar.innerHTML = this.getSecondaryNavigationHTML();
        
        navbar.insertAdjacentElement('afterend', secondaryNavbar);
    }

    getNavigationHTML() {
        return `
            <div class="navbar-container">
                <a href="/index.html" class="navbar-brand">
                    <span class="logo">🏢</span>
                    نظام إدارة المخزون
                </a>

                <ul class="navbar-menu">
                    <li class="navbar-item">
                        <a href="/dashboard.html" class="navbar-link" data-module="dashboard">
                            <span class="icon">🏠</span>
                            الرئيسية
                        </a>
                    </li>

                    <li class="navbar-item dropdown">
                        <a href="#" class="navbar-link" data-module="inventory">
                            <span class="icon">📦</span>
                            إدارة المخزون
                            <span class="dropdown-arrow">▼</span>
                        </a>
                        <div class="dropdown-menu">
                            <div class="dropdown-header">إدارة المخزون</div>
                            <a href="/inventory.html" class="dropdown-item">
                                <span class="icon">📋</span>
                                إدارة الأصناف
                            </a>
                            <a href="/inventory.html#categories" class="dropdown-item">
                                <span class="icon">🏷️</span>
                                الفئات
                            </a>
                            <a href="/inventory.html#warehouses" class="dropdown-item">
                                <span class="icon">🏪</span>
                                المخازن
                            </a>
                            <a href="/inventory.html#movements" class="dropdown-item">
                                <span class="icon">🔄</span>
                                حركات المخزون
                            </a>
                            <div class="dropdown-divider"></div>
                            <a href="/warehouse_transfer.html" class="dropdown-item">
                                <span class="icon">🚚</span>
                                تحويل المخزون
                            </a>
                        </div>
                    </li>

                    <li class="navbar-item dropdown">
                        <a href="#" class="navbar-link" data-module="sales">
                            <span class="icon">💰</span>
                            المبيعات
                            <span class="dropdown-arrow">▼</span>
                        </a>
                        <div class="dropdown-menu">
                            <div class="dropdown-header">إدارة المبيعات</div>
                            <a href="/sales.html" class="dropdown-item">
                                <span class="icon">🧾</span>
                                فواتير المبيعات
                            </a>
                            <a href="/sales.html#customers" class="dropdown-item">
                                <span class="icon">👥</span>
                                العملاء
                            </a>
                            <a href="/sales.html#quotations" class="dropdown-item">
                                <span class="icon">📄</span>
                                عروض الأسعار
                            </a>
                            <a href="/sales.html#reports" class="dropdown-item">
                                <span class="icon">📊</span>
                                تقارير المبيعات
                            </a>
                        </div>
                    </li>

                    <li class="navbar-item dropdown">
                        <a href="#" class="navbar-link" data-module="purchases">
                            <span class="icon">🛒</span>
                            المشتريات
                            <span class="dropdown-arrow">▼</span>
                        </a>
                        <div class="dropdown-menu">
                            <div class="dropdown-header">إدارة المشتريات</div>
                            <a href="/purchases.html" class="dropdown-item">
                                <span class="icon">🧾</span>
                                فواتير المشتريات
                            </a>
                            <a href="/purchases.html#suppliers" class="dropdown-item">
                                <span class="icon">🏭</span>
                                الموردين
                            </a>
                            <a href="/purchases.html#orders" class="dropdown-item">
                                <span class="icon">📝</span>
                                طلبات الشراء
                            </a>
                            <a href="/purchases.html#reports" class="dropdown-item">
                                <span class="icon">📊</span>
                                تقارير المشتريات
                            </a>
                        </div>
                    </li>

                    <li class="navbar-item dropdown">
                        <a href="#" class="navbar-link" data-module="regions">
                            <span class="icon">🗺️</span>
                            المناطق والمخازن
                            <span class="dropdown-arrow">▼</span>
                        </a>
                        <div class="dropdown-menu">
                            <div class="dropdown-header">إدارة المواقع</div>
                            <a href="/regions.html" class="dropdown-item">
                                <span class="icon">🌍</span>
                                إدارة المناطق
                            </a>
                            <a href="/regions.html#warehouses" class="dropdown-item">
                                <span class="icon">🏪</span>
                                إدارة المخازن
                            </a>
                            <a href="/regions.html#zones" class="dropdown-item">
                                <span class="icon">📍</span>
                                مناطق المخازن
                            </a>
                        </div>
                    </li>

                    <li class="navbar-item dropdown">
                        <a href="#" class="navbar-link" data-module="reports">
                            <span class="icon">📊</span>
                            التقارير
                            <span class="dropdown-arrow">▼</span>
                        </a>
                        <div class="dropdown-menu">
                            <div class="dropdown-header">التقارير والإحصائيات</div>
                            <a href="/reports.html" class="dropdown-item">
                                <span class="icon">📈</span>
                                تقارير المخزون
                            </a>
                            <a href="/reports.html#sales" class="dropdown-item">
                                <span class="icon">💹</span>
                                تقارير المبيعات
                            </a>
                            <a href="/reports.html#purchases" class="dropdown-item">
                                <span class="icon">📉</span>
                                تقارير المشتريات
                            </a>
                            <a href="/reports.html#financial" class="dropdown-item">
                                <span class="icon">💰</span>
                                التقارير المالية
                            </a>
                        </div>
                    </li>

                    <li class="navbar-item dropdown">
                        <a href="#" class="navbar-link" data-module="administration">
                            <span class="icon">⚙️</span>
                            الإدارة
                            <span class="dropdown-arrow">▼</span>
                        </a>
                        <div class="dropdown-menu">
                            <div class="dropdown-header">إدارة النظام</div>
                            <a href="/administration.html" class="dropdown-item">
                                <span class="icon">👤</span>
                                المستخدمين
                            </a>
                            <a href="/administration.html#roles" class="dropdown-item">
                                <span class="icon">🔐</span>
                                الأدوار والصلاحيات
                            </a>
                            <a href="/administration.html#permissions" class="dropdown-item">
                                <span class="icon">🛡️</span>
                                إدارة الصلاحيات
                            </a>
                            <a href="/administration.html#settings" class="dropdown-item">
                                <span class="icon">⚙️</span>
                                إعدادات النظام
                            </a>
                            <div class="dropdown-divider"></div>
                            <a href="/administration.html#backup" class="dropdown-item">
                                <span class="icon">💾</span>
                                النسخ الاحتياطي
                            </a>
                        </div>
                    </li>
                </ul>

                <div class="navbar-right">
                    <div class="quick-search">
                        <input type="text" class="search-input" placeholder="البحث السريع..." id="quickSearch">
                        <button class="search-btn" onclick="performQuickSearch()">🔍</button>
                    </div>

                    <div class="notifications">
                        <button class="notification-bell" onclick="toggleNotifications()">
                            🔔
                            <span class="notification-badge" id="notificationCount">3</span>
                        </button>
                    </div>

                    <div class="user-info dropdown">
                        <div class="user-avatar">👤</div>
                        <div class="user-details">
                            <div class="user-name" id="userName">مدير النظام</div>
                            <div class="user-role" id="userRole">مدير عام</div>
                        </div>
                        <div class="dropdown-menu" style="left: auto; right: 0;">
                            <a href="/profile.html" class="dropdown-item">
                                <span class="icon">👤</span>
                                الملف الشخصي
                            </a>
                            <a href="/settings.html" class="dropdown-item">
                                <span class="icon">⚙️</span>
                                الإعدادات
                            </a>
                            <div class="dropdown-divider"></div>
                            <a href="#" class="dropdown-item" onclick="logout()">
                                <span class="icon">🚪</span>
                                تسجيل الخروج
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getSecondaryNavigationHTML() {
        return `
            <div class="breadcrumb-container">
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb" id="breadcrumbNav">
                        <li class="breadcrumb-item">
                            <a href="/index.html">🏠 الرئيسية</a>
                        </li>
                    </ol>
                </nav>

                <div class="quick-actions" id="quickActions">
                    <!-- سيتم إضافة الأزرار ديناميكياً حسب الصفحة -->
                </div>
            </div>
        `;
    }

    setupEventListeners() {
        // البحث السريع
        const searchInput = document.getElementById('quickSearch');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performQuickSearch();
                }
            });

            // البحث التلقائي أثناء الكتابة
            searchInput.addEventListener('input', (e) => {
                if (e.target.value.length >= 3) {
                    this.performLiveSearch(e.target.value);
                }
            });
        }

        // تحديث الصفحة النشطة عند النقر على الروابط
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('navbar-link') || e.target.classList.contains('dropdown-item')) {
                this.updateActiveLink(e.target);
            }
        });

        // إغلاق القوائم المنسدلة عند النقر خارجها
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dropdown')) {
                this.closeAllDropdowns();
            }
        });
    }

    updateActiveLink(clickedLink) {
        // إزالة الفئة النشطة من جميع الروابط
        document.querySelectorAll('.navbar-link').forEach(link => {
            link.classList.remove('active');
        });

        // إضافة الفئة النشطة للرابط المنقور عليه
        if (clickedLink.classList.contains('navbar-link')) {
            clickedLink.classList.add('active');
            this.currentModule = clickedLink.dataset.module || '';
        }

        // تحديث مسار التنقل
        this.updateBreadcrumbs();
    }

    updateBreadcrumbs() {
        const breadcrumbNav = document.getElementById('breadcrumbNav');
        if (!breadcrumbNav) return;

        // تحديد المسار حسب الصفحة الحالية
        const currentPath = window.location.pathname;
        const breadcrumbs = this.generateBreadcrumbs(currentPath);

        breadcrumbNav.innerHTML = breadcrumbs.map((crumb, index) => {
            const isLast = index === breadcrumbs.length - 1;
            return `
                <li class="breadcrumb-item ${isLast ? 'active' : ''}">
                    ${isLast ? crumb.text : `<a href="${crumb.url}">${crumb.text}</a>`}
                </li>
            `;
        }).join('');

        // تحديث الأزرار السريعة
        this.updateQuickActions(currentPath);
    }

    generateBreadcrumbs(path) {
        const breadcrumbs = [
            { text: '🏠 الرئيسية', url: '/index.html' }
        ];

        const pathMap = {
            '/dashboard.html': [
                { text: '📊 لوحة المعلومات', url: '/dashboard.html' }
            ],
            '/inventory.html': [
                { text: '📦 إدارة المخزون', url: '/inventory.html' }
            ],
            '/sales.html': [
                { text: '💰 المبيعات', url: '/sales.html' }
            ],
            '/purchases.html': [
                { text: '🛒 المشتريات', url: '/purchases.html' }
            ],
            '/warehouse_transfer.html': [
                { text: '📦 إدارة المخزون', url: '/inventory.html' },
                { text: '🔄 تحويل المخزون', url: '/warehouse_transfer.html' }
            ],
            '/regions.html': [
                { text: '🗺️ المناطق والمخازن', url: '/regions.html' }
            ],
            '/reports.html': [
                { text: '📊 التقارير', url: '/reports.html' }
            ],
            '/administration.html': [
                { text: '⚙️ الإدارة', url: '/administration.html' }
            ]
        };

        if (pathMap[path]) {
            breadcrumbs.push(...pathMap[path]);
        }

        return breadcrumbs;
    }

    updateQuickActions(path) {
        const quickActions = document.getElementById('quickActions');
        if (!quickActions) return;

        const actionMap = {
            '/inventory.html': [
                { text: '➕ إضافة صنف', url: '#', onclick: 'addNewProduct()' },
                { text: '📊 تقرير المخزون', url: '#', onclick: 'generateInventoryReport()' }
            ],
            '/sales.html': [
                { text: '➕ فاتورة جديدة', url: '#', onclick: 'createNewInvoice()' },
                { text: '👤 عميل جديد', url: '#', onclick: 'addNewCustomer()' }
            ],
            '/purchases.html': [
                { text: '➕ فاتورة شراء', url: '#', onclick: 'createPurchaseInvoice()' },
                { text: '🏭 مورد جديد', url: '#', onclick: 'addNewSupplier()' }
            ],
            '/warehouse_transfer.html': [
                { text: '➕ تحويل جديد', url: '#', onclick: 'createNewTransfer()' },
                { text: '📋 تقرير التحويلات', url: '#', onclick: 'generateTransferReport()' }
            ],
            '/administration.html': [
                { text: '👤 مستخدم جديد', url: '#', onclick: 'addNewUser()' },
                { text: '🔐 دور جديد', url: '#', onclick: 'createNewRole()' }
            ]
        };

        const actions = actionMap[path] || [];
        quickActions.innerHTML = actions.map(action => `
            <a href="${action.url}" class="quick-action-btn" onclick="${action.onclick}">
                ${action.text}
            </a>
        `).join('');
    }

    performQuickSearch() {
        const searchInput = document.getElementById('quickSearch');
        const query = searchInput.value.trim();
        
        if (query.length < 2) {
            alert('يرجى إدخال كلمة بحث أطول');
            return;
        }

        // تنفيذ البحث
        this.executeSearch(query);
    }

    performLiveSearch(query) {
        // البحث المباشر أثناء الكتابة
        console.log('البحث المباشر:', query);
        // يمكن إضافة منطق البحث المباشر هنا
    }

    executeSearch(query) {
        // محاكاة البحث - يجب ربطها بـ API حقيقي
        console.log('تنفيذ البحث عن:', query);
        
        // إظهار نتائج البحث
        this.showSearchResults(query);
    }

    showSearchResults(query) {
        // إنشاء نافذة نتائج البحث
        const resultsModal = document.createElement('div');
        resultsModal.className = 'search-results-modal';
        resultsModal.innerHTML = `
            <div class="search-results-content">
                <div class="search-results-header">
                    <h3>نتائج البحث عن: "${query}"</h3>
                    <button onclick="this.closest('.search-results-modal').remove()">✕</button>
                </div>
                <div class="search-results-body">
                    <p>جاري البحث...</p>
                </div>
            </div>
        `;
        
        document.body.appendChild(resultsModal);
        
        // محاكاة تحميل النتائج
        setTimeout(() => {
            const resultsBody = resultsModal.querySelector('.search-results-body');
            resultsBody.innerHTML = `
                <div class="search-result-item">
                    <h4>📦 منتج: ${query}</h4>
                    <p>تم العثور على منتج مطابق في المخزون</p>
                </div>
                <div class="search-result-item">
                    <h4>👤 عميل: ${query}</h4>
                    <p>عميل مسجل في النظام</p>
                </div>
            `;
        }, 1000);
    }

    loadNotifications() {
        // تحميل الإشعارات من الخادم
        this.notifications = [
            { id: 1, text: 'تم إنشاء فاتورة جديدة', time: '5 دقائق', type: 'info' },
            { id: 2, text: 'نفاد مخزون صنف معين', time: '10 دقائق', type: 'warning' },
            { id: 3, text: 'تحويل مخزون معلق للموافقة', time: '15 دقيقة', type: 'pending' }
        ];

        this.updateNotificationBadge();
    }

    updateNotificationBadge() {
        const badge = document.getElementById('notificationCount');
        if (badge) {
            badge.textContent = this.notifications.length;
            badge.style.display = this.notifications.length > 0 ? 'flex' : 'none';
        }
    }

    toggleNotifications() {
        // إظهار/إخفاء قائمة الإشعارات
        let notificationPanel = document.getElementById('notificationPanel');
        
        if (notificationPanel) {
            notificationPanel.remove();
            return;
        }

        notificationPanel = document.createElement('div');
        notificationPanel.id = 'notificationPanel';
        notificationPanel.className = 'notification-panel';
        notificationPanel.innerHTML = `
            <div class="notification-header">
                <h4>الإشعارات</h4>
                <button onclick="this.closest('.notification-panel').remove()">✕</button>
            </div>
            <div class="notification-list">
                ${this.notifications.map(notification => `
                    <div class="notification-item ${notification.type}">
                        <div class="notification-text">${notification.text}</div>
                        <div class="notification-time">${notification.time}</div>
                    </div>
                `).join('')}
            </div>
            <div class="notification-footer">
                <a href="#" onclick="markAllAsRead()">تحديد الكل كمقروء</a>
            </div>
        `;

        document.body.appendChild(notificationPanel);
    }

    closeAllDropdowns() {
        // إغلاق جميع القوائم المنسدلة
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.style.opacity = '0';
            menu.style.visibility = 'hidden';
            menu.style.transform = 'translateY(-10px)';
        });
    }

    highlightCurrentPage() {
        // تمييز الصفحة الحالية في القائمة
        const currentPath = window.location.pathname;
        const currentLink = document.querySelector(`a[href="${currentPath}"]`);
        
        if (currentLink && currentLink.classList.contains('navbar-link')) {
            currentLink.classList.add('active');
            this.currentModule = currentLink.dataset.module || '';
        }
    }
}

// دوال مساعدة عامة
function logout() {
    if (confirm('هل أنت متأكد من تسجيل الخروج؟')) {
        window.location.href = '/index.html';
    }
}

function markAllAsRead() {
    const notificationPanel = document.getElementById('notificationPanel');
    if (notificationPanel) {
        notificationPanel.remove();
    }
    
    // تحديث عدد الإشعارات
    const badge = document.getElementById('notificationCount');
    if (badge) {
        badge.style.display = 'none';
    }
}

// دوال الأزرار السريعة (يجب تخصيصها حسب كل صفحة)
function addNewProduct() { alert('إضافة منتج جديد'); }
function generateInventoryReport() { alert('إنشاء تقرير المخزون'); }
function createNewInvoice() { alert('إنشاء فاتورة جديدة'); }
function addNewCustomer() { alert('إضافة عميل جديد'); }
function createPurchaseInvoice() { alert('إنشاء فاتورة شراء'); }
function addNewSupplier() { alert('إضافة مورد جديد'); }
function createNewTransfer() { alert('إنشاء تحويل جديد'); }
function generateTransferReport() { alert('إنشاء تقرير التحويلات'); }
function addNewUser() { alert('إضافة مستخدم جديد'); }
function createNewRole() { alert('إنشاء دور جديد'); }

// تهيئة النظام عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // التحقق من عدم وجود شريط تنقل مسبقاً
    if (!document.querySelector('.main-navbar')) {
        window.navigationManager = new NavigationManager();
    }
});

// تصدير الفئة للاستخدام العام
window.NavigationManager = NavigationManager;

