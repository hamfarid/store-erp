/**
 * فحص شامل للواجهة الأمامية
 * ملف: frontend_comprehensive_check.js
 */

class FrontendComprehensiveChecker {
    constructor() {
        this.results = {
            timestamp: new Date().toISOString(),
            components: {},
            pages: {},
            routing: {},
            state_management: {},
            ui_elements: {},
            performance: {},
            accessibility: {},
            summary: {
                total_checks: 0,
                passed: 0,
                failed: 0,
                warnings: 0
            }
        };
    }

    logCheck(category, name, status, message = "") {
        if (!this.results[category]) {
            this.results[category] = {};
        }

        this.results[category][name] = {
            status: status,
            message: message,
            timestamp: new Date().toISOString()
        };

        this.results.summary.total_checks++;
        
        if (status === 'passed') {
            this.results.summary.passed++;
            console.log(`✅ ${category}/${name}`);
        } else if (status === 'failed') {
            this.results.summary.failed++;
            console.log(`❌ ${category}/${name}: ${message}`);
        } else if (status === 'warning') {
            this.results.summary.warnings++;
            console.log(`⚠️ ${category}/${name}: ${message}`);
        }

        if (message && status === 'passed') {
            console.log(`   ℹ️ ${message}`);
        }
    }

    // فحص المكونات الأساسية
    checkCoreComponents() {
        console.log('\n🧩 فحص المكونات الأساسية...');

        const coreComponents = [
            'Dashboard',
            'ProductsAdvanced', 
            'CustomersAdvanced',
            'SuppliersAdvanced',
            'LotManagement',
            'CashBoxes',
            'PaymentVouchers',
            'InventoryReports',
            'AdminUsers',
            'AdminRoles',
            'AdminSecurity'
        ];

        coreComponents.forEach(componentName => {
            try {
                // فحص وجود المكون في DOM
                const componentExists = document.querySelector(`[data-component="${componentName}"]`) ||
                                      document.querySelector(`.${componentName}`) ||
                                      document.body.textContent.includes(componentName);

                if (componentExists) {
                    this.logCheck('components', `core_${componentName}`, 'passed', 'موجود في DOM');
                } else {
                    this.logCheck('components', `core_${componentName}`, 'warning', 'غير موجود في DOM الحالي');
                }
            } catch (error) {
                this.logCheck('components', `core_${componentName}`, 'failed', error.message);
            }
        });
    }

    // فحص الصفحات والمسارات
    checkPagesAndRouting() {
        console.log('\n📄 فحص الصفحات والمسارات...');

        const pages = [
            { path: '/', name: 'الصفحة الرئيسية' },
            { path: '/products', name: 'المنتجات' },
            { path: '/customers', name: 'العملاء' },
            { path: '/suppliers', name: 'الموردين' },
            { path: '/batches', name: 'اللوطات' },
            { path: '/accounting/cash-boxes', name: 'الصناديق' },
            { path: '/accounting/vouchers', name: 'قسائم الدفع' },
            { path: '/reports/inventory', name: 'تقارير المخزون' },
            { path: '/admin/users', name: 'إدارة المستخدمين' },
            { path: '/admin/security', name: 'الأمان والمراقبة' }
        ];

        pages.forEach(page => {
            try {
                // محاولة الانتقال للصفحة
                const originalPath = window.location.pathname;
                window.history.pushState({}, '', page.path);
                
                setTimeout(() => {
                    const currentPath = window.location.pathname;
                    const hasContent = document.body.textContent.trim().length > 100;
                    const hasError = document.body.textContent.includes('404') || 
                                   document.body.textContent.includes('خطأ');

                    if (currentPath === page.path && hasContent && !hasError) {
                        this.logCheck('pages', `page_${page.path.replace(/[\/\-]/g, '_')}`, 'passed', page.name);
                    } else if (hasError) {
                        this.logCheck('pages', `page_${page.path.replace(/[\/\-]/g, '_')}`, 'failed', 'صفحة خطأ');
                    } else {
                        this.logCheck('pages', `page_${page.path.replace(/[\/\-]/g, '_')}`, 'warning', 'محتوى قليل أو إعادة توجيه');
                    }

                    // العودة للمسار الأصلي
                    window.history.pushState({}, '', originalPath);
                }, 500);

            } catch (error) {
                this.logCheck('pages', `page_${page.path.replace(/[\/\-]/g, '_')}`, 'failed', error.message);
            }
        });
    }

    // فحص عناصر واجهة المستخدم
    checkUIElements() {
        console.log('\n🎨 فحص عناصر واجهة المستخدم...');

        // فحص الشريط الجانبي
        const sidebar = document.querySelector('.sidebar, nav, [role="navigation"]');
        if (sidebar) {
            const sidebarLinks = sidebar.querySelectorAll('a, button');
            this.logCheck('ui_elements', 'sidebar', 'passed', `${sidebarLinks.length} رابط/زر`);
        } else {
            this.logCheck('ui_elements', 'sidebar', 'failed', 'الشريط الجانبي غير موجود');
        }

        // فحص الهيدر
        const header = document.querySelector('header, .header, .navbar');
        if (header) {
            this.logCheck('ui_elements', 'header', 'passed', 'موجود');
        } else {
            this.logCheck('ui_elements', 'header', 'warning', 'الهيدر غير موجود');
        }

        // فحص الأزرار
        const buttons = document.querySelectorAll('button');
        this.logCheck('ui_elements', 'buttons', 'passed', `${buttons.length} زر`);

        // فحص النماذج
        const forms = document.querySelectorAll('form');
        const inputs = document.querySelectorAll('input, select, textarea');
        this.logCheck('ui_elements', 'forms', 'passed', `${forms.length} نموذج، ${inputs.length} حقل إدخال`);

        // فحص الجداول
        const tables = document.querySelectorAll('table, .table, .grid');
        this.logCheck('ui_elements', 'tables', 'passed', `${tables.length} جدول/شبكة`);

        // فحص النوافذ المنبثقة
        const modals = document.querySelectorAll('.modal, .dialog, [role="dialog"]');
        this.logCheck('ui_elements', 'modals', 'passed', `${modals.length} نافذة منبثقة`);
    }

    // فحص إدارة الحالة
    checkStateManagement() {
        console.log('\n🔄 فحص إدارة الحالة...');

        // فحص React Context
        try {
            const reactFiberNode = document.querySelector('#root')._reactInternalFiber ||
                                 document.querySelector('#root')._reactInternalInstance;
            
            if (reactFiberNode) {
                this.logCheck('state_management', 'react_context', 'passed', 'React Context متاح');
            } else {
                this.logCheck('state_management', 'react_context', 'warning', 'React Context غير مكتشف');
            }
        } catch (error) {
            this.logCheck('state_management', 'react_context', 'warning', 'لا يمكن فحص React Context');
        }

        // فحص Local Storage
        try {
            const localStorageKeys = Object.keys(localStorage);
            if (localStorageKeys.length > 0) {
                this.logCheck('state_management', 'local_storage', 'passed', `${localStorageKeys.length} مفتاح`);
            } else {
                this.logCheck('state_management', 'local_storage', 'warning', 'Local Storage فارغ');
            }
        } catch (error) {
            this.logCheck('state_management', 'local_storage', 'failed', error.message);
        }

        // فحص Session Storage
        try {
            const sessionStorageKeys = Object.keys(sessionStorage);
            this.logCheck('state_management', 'session_storage', 'passed', `${sessionStorageKeys.length} مفتاح`);
        } catch (error) {
            this.logCheck('state_management', 'session_storage', 'failed', error.message);
        }
    }

    // فحص الأداء
    checkPerformance() {
        console.log('\n⚡ فحص الأداء...');

        // فحص زمن التحميل
        if (window.performance && window.performance.timing) {
            const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
            
            if (loadTime < 3000) {
                this.logCheck('performance', 'load_time', 'passed', `${loadTime}ms`);
            } else if (loadTime < 5000) {
                this.logCheck('performance', 'load_time', 'warning', `${loadTime}ms - بطيء نسبياً`);
            } else {
                this.logCheck('performance', 'load_time', 'failed', `${loadTime}ms - بطيء جداً`);
            }
        }

        // فحص حجم DOM
        const domSize = document.querySelectorAll('*').length;
        if (domSize < 1000) {
            this.logCheck('performance', 'dom_size', 'passed', `${domSize} عنصر`);
        } else if (domSize < 2000) {
            this.logCheck('performance', 'dom_size', 'warning', `${domSize} عنصر - كبير نسبياً`);
        } else {
            this.logCheck('performance', 'dom_size', 'failed', `${domSize} عنصر - كبير جداً`);
        }

        // فحص الذاكرة (إذا كان متاحاً)
        if (window.performance && window.performance.memory) {
            const memoryUsage = window.performance.memory.usedJSHeapSize / 1024 / 1024;
            if (memoryUsage < 50) {
                this.logCheck('performance', 'memory_usage', 'passed', `${memoryUsage.toFixed(2)}MB`);
            } else if (memoryUsage < 100) {
                this.logCheck('performance', 'memory_usage', 'warning', `${memoryUsage.toFixed(2)}MB`);
            } else {
                this.logCheck('performance', 'memory_usage', 'failed', `${memoryUsage.toFixed(2)}MB`);
            }
        }
    }

    // فحص إمكانية الوصول
    checkAccessibility() {
        console.log('\n♿ فحص إمكانية الوصول...');

        // فحص العناوين
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        if (headings.length > 0) {
            this.logCheck('accessibility', 'headings', 'passed', `${headings.length} عنوان`);
        } else {
            this.logCheck('accessibility', 'headings', 'warning', 'لا توجد عناوين');
        }

        // فحص النصوص البديلة للصور
        const images = document.querySelectorAll('img');
        const imagesWithAlt = document.querySelectorAll('img[alt]');
        if (images.length === 0) {
            this.logCheck('accessibility', 'image_alt', 'passed', 'لا توجد صور');
        } else if (imagesWithAlt.length === images.length) {
            this.logCheck('accessibility', 'image_alt', 'passed', 'جميع الصور لها نص بديل');
        } else {
            this.logCheck('accessibility', 'image_alt', 'warning', `${images.length - imagesWithAlt.length} صورة بدون نص بديل`);
        }

        // فحص labels للحقول
        const inputs = document.querySelectorAll('input, select, textarea');
        const labelsCount = document.querySelectorAll('label').length;
        if (inputs.length === 0) {
            this.logCheck('accessibility', 'form_labels', 'passed', 'لا توجد حقول إدخال');
        } else if (labelsCount >= inputs.length * 0.8) {
            this.logCheck('accessibility', 'form_labels', 'passed', 'معظم الحقول لها labels');
        } else {
            this.logCheck('accessibility', 'form_labels', 'warning', 'بعض الحقول بدون labels');
        }

        // فحص ARIA attributes
        const ariaElements = document.querySelectorAll('[aria-label], [aria-labelledby], [role]');
        if (ariaElements.length > 0) {
            this.logCheck('accessibility', 'aria_attributes', 'passed', `${ariaElements.length} عنصر مع ARIA`);
        } else {
            this.logCheck('accessibility', 'aria_attributes', 'warning', 'لا توجد ARIA attributes');
        }
    }

    // فحص التوافق مع المتصفحات
    checkBrowserCompatibility() {
        console.log('\n🌐 فحص التوافق مع المتصفحات...');

        // فحص ميزات JavaScript الحديثة
        const modernFeatures = [
            { name: 'fetch', check: () => typeof fetch !== 'undefined' },
            { name: 'Promise', check: () => typeof Promise !== 'undefined' },
            { name: 'arrow_functions', check: () => { try { eval('() => {}'); return true; } catch { return false; } } },
            { name: 'const_let', check: () => { try { eval('const x = 1; let y = 2;'); return true; } catch { return false; } } },
            { name: 'template_literals', check: () => { try { eval('`template`'); return true; } catch { return false; } } }
        ];

        modernFeatures.forEach(feature => {
            try {
                if (feature.check()) {
                    this.logCheck('browser_compatibility', feature.name, 'passed', 'مدعوم');
                } else {
                    this.logCheck('browser_compatibility', feature.name, 'failed', 'غير مدعوم');
                }
            } catch (error) {
                this.logCheck('browser_compatibility', feature.name, 'failed', error.message);
            }
        });

        // فحص معلومات المتصفح
        const userAgent = navigator.userAgent;
        const browserInfo = {
            chrome: userAgent.includes('Chrome'),
            firefox: userAgent.includes('Firefox'),
            safari: userAgent.includes('Safari') && !userAgent.includes('Chrome'),
            edge: userAgent.includes('Edge')
        };

        const detectedBrowser = Object.keys(browserInfo).find(browser => browserInfo[browser]);
        if (detectedBrowser) {
            this.logCheck('browser_compatibility', 'browser_detection', 'passed', `${detectedBrowser} مكتشف`);
        } else {
            this.logCheck('browser_compatibility', 'browser_detection', 'warning', 'متصفح غير معروف');
        }
    }

    // تشغيل جميع الفحوصات
    async runAllChecks() {
        console.log('🚀 === بدء فحص شامل للواجهة الأمامية ===');
        console.log(`⏰ التاريخ: ${new Date().toLocaleString('ar-EG')}`);

        // تشغيل جميع الفحوصات
        this.checkCoreComponents();
        
        // انتظار قصير للسماح بتحديث DOM
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.checkPagesAndRouting();
        
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        this.checkUIElements();
        this.checkStateManagement();
        this.checkPerformance();
        this.checkAccessibility();
        this.checkBrowserCompatibility();

        // عرض النتائج النهائية
        this.printSummary();

        return this.results;
    }

    // عرض ملخص النتائج
    printSummary() {
        console.log('\n📊 === ملخص فحص الواجهة الأمامية ===');
        const summary = this.results.summary;

        console.log(`إجمالي الفحوصات: ${summary.total_checks}`);
        console.log(`نجح: ${summary.passed}`);
        console.log(`فشل: ${summary.failed}`);
        console.log(`تحذيرات: ${summary.warnings}`);

        if (summary.total_checks > 0) {
            const successRate = (summary.passed / summary.total_checks) * 100;
            console.log(`معدل النجاح: ${successRate.toFixed(1)}%`);

            if (successRate >= 90) {
                console.log('🎉 الواجهة الأمامية تعمل بشكل ممتاز!');
            } else if (successRate >= 70) {
                console.log('✅ الواجهة الأمامية تعمل مع بعض التحذيرات');
            } else {
                console.log('⚠️ الواجهة الأمامية تحتاج إلى إصلاحات');
            }
        }

        // عرض تفاصيل الفئات
        console.log('\n📋 تفاصيل الفئات:');
        Object.keys(this.results).forEach(category => {
            if (category === 'summary' || category === 'timestamp') return;

            const checks = this.results[category];
            if (typeof checks === 'object' && checks !== null) {
                const passed = Object.values(checks).filter(check => 
                    typeof check === 'object' && check.status === 'passed'
                ).length;
                const total = Object.keys(checks).length;
                
                if (total > 0) {
                    const rate = (passed / total) * 100;
                    console.log(`📂 ${category}: ${passed}/${total} (${rate.toFixed(1)}%)`);
                }
            }
        });
    }

    // حفظ النتائج
    saveResults() {
        const resultsJson = JSON.stringify(this.results, null, 2);
        const blob = new Blob([resultsJson], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `frontend_check_results_${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        console.log('💾 تم حفظ النتائج في ملف JSON');
    }
}

// تصدير الفئة للاستخدام
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FrontendComprehensiveChecker;
}

// إنشاء مثيل عام للاستخدام في المتصفح
if (typeof window !== 'undefined') {
    window.FrontendComprehensiveChecker = FrontendComprehensiveChecker;

    // دالة سريعة لتشغيل الاختبار
    window.checkFrontendComprehensive = async function() {
        const checker = new FrontendComprehensiveChecker();
        const results = await checker.runAllChecks();
        checker.saveResults();
        return results;
    };

    console.log('📝 لتشغيل فحص الواجهة الأمامية الشامل، اكتب: checkFrontendComprehensive()');
}
