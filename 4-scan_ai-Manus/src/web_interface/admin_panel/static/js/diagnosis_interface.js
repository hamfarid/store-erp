# File: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/diagnosis_interface.js
/**
 * مسار الملف: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/diagnosis_interface.js
 * 
 * واجهة تشخيص الأمراض التفاعلية
 * تتضمن رفع الصور، التحليل، وعرض النتائج
 */

class DiagnosisInterface {
    constructor() {
        this.currentImage = null;
        this.currentDiagnosis = null;
        this.init();
    }

    init() {
        this.setupFileUpload();
        this.setupEventListeners();
        this.loadRecentDiagnoses();
    }

    setupFileUpload() {
        const uploadArea = document.getElementById('uploadArea');
        const imageInput = document.getElementById('imageInput');
        const previewContainer = document.getElementById('previewContainer');
        const imagePreview = document.getElementById('imagePreview');

        // النقر على منطقة الرفع
        uploadArea.addEventListener('click', () => {
            imageInput.click();
        });

        // تغيير الملف
        imageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.handleImageUpload(file);
            }
        });

        // السحب والإفلات
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleImageUpload(files[0]);
            }
        });
    }

    setupEventListeners() {
        // زر التشخيص
        document.getElementById('diagnoseBtn').addEventListener('click', () => {
            this.startDiagnosis();
        });

        // زر إعادة التعيين
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetInterface();
        });

        // زر حفظ النتيجة
        document.getElementById('saveResultBtn').addEventListener('click', () => {
            this.saveResult();
        });

        // زر المشاركة
        document.getElementById('shareResultBtn').addEventListener('click', () => {
            this.shareResult();
        });

        // زر الإبلاغ عن خطأ
        document.getElementById('reportErrorBtn').addEventListener('click', () => {
            this.reportError();
        });
    }

    handleImageUpload(file) {
        // التحقق من نوع الملف
        if (!file.type.startsWith('image/')) {
            this.showError('يرجى اختيار ملف صورة صحيح');
            return;
        }

        // التحقق من حجم الملف (5MB كحد أقصى)
        if (file.size > 5 * 1024 * 1024) {
            this.showError('حجم الملف كبير جداً. الحد الأقصى 5 ميجابايت');
            return;
        }

        this.currentImage = file;

        // عرض معاينة الصورة
        const reader = new FileReader();
        reader.onload = (e) => {
            const imagePreview = document.getElementById('imagePreview');
            imagePreview.src = e.target.result;
            
            document.getElementById('previewContainer').style.display = 'block';
            document.getElementById('uploadArea').style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    async startDiagnosis() {
        if (!this.currentImage) {
            this.showError('يرجى اختيار صورة أولاً');
            return;
        }

        const cropSelect = document.getElementById('cropSelect');
        if (!cropSelect.value) {
            this.showError('يرجى اختيار نوع المحصول');
            return;
        }

        // إظهار مؤشر التحميل
        this.showLoading(true);

        try {
            // إنشاء FormData لرفع الصورة
            const formData = new FormData();
            formData.append('image', this.currentImage);
            formData.append('crop_type', cropSelect.value);

            // إرسال الطلب
            const response = await fetch('/api/diagnosis/analyze', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('فشل في تحليل الصورة');
            }

            const result = await response.json();
            this.displayResults(result);

        } catch (error) {
            console.error('خطأ في التشخيص:', error);
            this.showError('حدث خطأ أثناء تحليل الصورة. يرجى المحاولة مرة أخرى');
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(result) {
        this.currentDiagnosis = result;

        // إخفاء مؤشر التحميل وإظهار النتائج
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('diagnosisResults').style.display = 'block';

        // عرض معلومات المرض
        const diseaseInfo = document.getElementById('diseaseInfo');
        diseaseInfo.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6>المرض المكتشف:</h6>
                    <h4 class="text-${this.getSeverityColor(result.severity)}">${result.disease_name}</h4>
                </div>
                <div class="col-md-6">
                    <h6>مستوى الثقة:</h6>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${result.confidence * 100}%"></div>
                    </div>
                    <small>${(result.confidence * 100).toFixed(1)}%</small>
                </div>
            </div>
            
            <div class="mt-3">
                <h6>الأعراض:</h6>
                <p>${result.symptoms}</p>
            </div>
        `;

        // عرض معلومات العلاج
        const treatmentInfo = document.getElementById('treatmentInfo');
        treatmentInfo.innerHTML = `
            <h6><i class="fas fa-medkit"></i> العلاج الموصى به:</h6>
            <p>${result.treatment}</p>
            
            <h6><i class="fas fa-shield-alt"></i> الوقاية:</h6>
            <p>${result.prevention}</p>
        `;

        // تحديث الإحصائيات
        this.updateStats();
        this.loadRecentDiagnoses();
    }

    getSeverityColor(severity) {
        const colors = {
            'عالي': 'danger',
            'متوسط': 'warning',
            'منخفض': 'success'
        };
        return colors[severity] || 'info';
    }

    async saveResult() {
        if (!this.currentDiagnosis) {
            this.showError('لا توجد نتائج للحفظ');
            return;
        }

        try {
            const response = await apiClient.post('/api/diagnosis/save', {
                diagnosis_id: this.currentDiagnosis.id,
                notes: prompt('ملاحظات إضافية (اختياري):') || ''
            });

            if (response.success) {
                this.showSuccess('تم حفظ النتيجة بنجاح');
                this.loadRecentDiagnoses();
            } else {
                this.showError('فشل في حفظ النتيجة');
            }
        } catch (error) {
            console.error('خطأ في حفظ النتيجة:', error);
            this.showError('حدث خطأ أثناء حفظ النتيجة');
        }
    }

    shareResult() {
        if (!this.currentDiagnosis) {
            this.showError('لا توجد نتائج للمشاركة');
            return;
        }

        // إنشاء رابط المشاركة
        const shareData = {
            title: 'نتيجة تشخيص أمراض النباتات',
            text: `تم اكتشاف ${this.currentDiagnosis.disease_name} بدقة ${(this.currentDiagnosis.confidence * 100).toFixed(1)}%`,
            url: window.location.href
        };

        if (navigator.share) {
            navigator.share(shareData);
        } else {
            // نسخ الرابط إلى الحافظة
            navigator.clipboard.writeText(window.location.href).then(() => {
                this.showSuccess('تم نسخ الرابط إلى الحافظة');
            });
        }
    }

    async reportError() {
        if (!this.currentDiagnosis) {
            this.showError('لا توجد نتائج للإبلاغ عنها');
            return;
        }

        const reason = prompt('يرجى وصف المشكلة:');
        if (!reason) return;

        try {
            const response = await apiClient.post('/api/diagnosis/report-error', {
                diagnosis_id: this.currentDiagnosis.id,
                reason: reason
            });

            if (response.success) {
                this.showSuccess('تم إرسال التقرير بنجاح. شكراً لمساعدتنا في تحسين النظام');
            } else {
                this.showError('فشل في إرسال التقرير');
            }
        } catch (error) {
            console.error('خطأ في إرسال التقرير:', error);
            this.showError('حدث خطأ أثناء إرسال التقرير');
        }
    }

    resetInterface() {
        this.currentImage = null;
        this.currentDiagnosis = null;
        
        document.getElementById('uploadArea').style.display = 'block';
        document.getElementById('previewContainer').style.display = 'none';
        document.getElementById('diagnosisResults').style.display = 'none';
        document.getElementById('loadingSpinner').style.display = 'none';
        
        document.getElementById('imageInput').value = '';
        document.getElementById('cropSelect').value = '';
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        const diagnoseBtn = document.getElementById('diagnoseBtn');
        
        if (show) {
            spinner.style.display = 'block';
            diagnoseBtn.disabled = true;
            diagnoseBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري التحليل...';
        } else {
            spinner.style.display = 'none';
            diagnoseBtn.disabled = false;
            diagnoseBtn.innerHTML = '<i class="fas fa-search"></i> بدء التشخيص';
        }
    }

    async loadRecentDiagnoses() {
        try {
            const response = await apiClient.get('/api/diagnosis/recent?limit=5');
            const container = document.getElementById('recentDiagnoses');
            
            if (response.length === 0) {
                container.innerHTML = '<p class="text-muted text-center">لا توجد تشخيصات حديثة</p>';
                return;
            }

            container.innerHTML = response.map(diagnosis => `
                <div class="history-item" onclick="this.showDiagnosisDetails('${diagnosis.id}')">
                    <img src="${diagnosis.image_path}" alt="صورة التشخيص" class="history-image">
                    <div class="flex-grow-1">
                        <h6 class="mb-1">${diagnosis.crop_name}</h6>
                        <p class="mb-1 text-${this.getSeverityColor(diagnosis.severity)}">${diagnosis.disease_name}</p>
                        <small class="text-muted">دقة: ${(diagnosis.confidence * 100).toFixed(1)}%</small>
                        <br>
                        <small class="text-muted">${this.formatDate(diagnosis.created_at)}</small>
                    </div>
                </div>
            `).join('');

        } catch (error) {
            console.error('خطأ في تحميل التشخيصات الحديثة:', error);
        }
    }

    async showDiagnosisDetails(diagnosisId) {
        try {
            const response = await apiClient.get(`/api/diagnosis/${diagnosisId}`);
            
            const modalBody = document.getElementById('modalBody');
            modalBody.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <img src="${response.image_path}" alt="صورة التشخيص" class="img-fluid rounded">
                    </div>
                    <div class="col-md-6">
                        <h5>${response.crop_name}</h5>
                        <h6 class="text-${this.getSeverityColor(response.severity)}">${response.disease_name}</h6>
                        <p><strong>الدقة:</strong> ${(response.confidence * 100).toFixed(1)}%</p>
                        <p><strong>التاريخ:</strong> ${this.formatDate(response.created_at)}</p>
                        
                        <h6>الأعراض:</h6>
                        <p>${response.symptoms}</p>
                        
                        <h6>العلاج:</h6>
                        <p>${response.treatment}</p>
                        
                        <h6>الوقاية:</h6>
                        <p>${response.prevention}</p>
                    </div>
                </div>
            `;
            
            const modal = new bootstrap.Modal(document.getElementById('diagnosisModal'));
            modal.show();

        } catch (error) {
            console.error('خطأ في تحميل تفاصيل التشخيص:', error);
            this.showError('فشل في تحميل تفاصيل التشخيص');
        }
    }

    async updateStats() {
        try {
            const response = await apiClient.get('/api/diagnosis/stats/today');
            
            document.getElementById('todayDiagnoses').textContent = response.total_diagnoses;
            document.getElementById('accuracyRate').textContent = `${response.average_accuracy.toFixed(1)}%`;

        } catch (error) {
            console.error('خطأ في تحديث الإحصائيات:', error);
        }
    }

    async loadInitialData() {
        await Promise.all([
            this.loadRecentDiagnoses(),
            this.updateStats()
        ]);
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'الآن';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} دقيقة`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} ساعة`;
        return date.toLocaleDateString('ar-SA');
    }

    showSuccess(message) {
        if (window.advancedFeatures) {
            window.advancedFeatures.showNotification('نجح', message, 'success');
        } else {
            alert(message);
        }
    }

    showError(message) {
        if (window.advancedFeatures) {
            window.advancedFeatures.showNotification('خطأ', message, 'error');
        } else {
            alert(message);
        }
    }
}

// تصدير للاستخدام العام
window.DiagnosisInterface = DiagnosisInterface;

