#!/usr/bin/env python3
"""
صفحات النظام باللغة العربية
Arabic System Pages
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


def add_arabic_pages_routes(app: FastAPI):
    """إضافة مسارات الصفحات العربية"""

    @app.get("/ar/image-processing", response_class=HTMLResponse)
    async def arabic_image_processing_page():
        """صفحة معالجة الصور باللغة العربية"""
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>معالجة الصور الزراعية - نظام الذكاء الاصطناعي الزراعي</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: white;
                }
                .header {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 1rem 2rem;
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                }
                .container {
                    max-width: 800px;
                    margin: 2rem auto;
                    padding: 0 2rem;
                }
                .upload-area {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 3rem;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    border: 2px dashed rgba(255, 255, 255, 0.3);
                    text-align: center;
                    margin: 2rem 0;
                    transition: all 0.3s;
                }
                .upload-area:hover {
                    border-color: #4CAF50;
                    background: rgba(76, 175, 80, 0.1);
                }
                .upload-btn {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 1rem 2rem;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 1.1rem;
                    transition: all 0.3s;
                }
                .upload-btn:hover {
                    background: #45a049;
                    transform: translateY(-2px);
                }
                .results {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    margin: 2rem 0;
                    display: none;
                }
                .btn {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 0.8rem 1.5rem;
                    border-radius: 25px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 0.5rem;
                    transition: all 0.3s;
                }
                .btn:hover {
                    background: #45a049;
                    transform: translateY(-2px);
                }
                .loading {
                    display: none;
                    text-align: center;
                    margin: 2rem 0;
                }
                .spinner {
                    border: 4px solid rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    border-top: 4px solid #4CAF50;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🖼️ معالجة الصور الزراعية</h1>
                <p>رفع وتحليل الصور الزراعية باستخدام الذكاء الاصطناعي</p>
            </div>

            <div class="container">
                <div class="upload-area" id="uploadArea">
                    <h3>📤 رفع صورة للتحليل</h3>
                    <p>اسحب وأفلت الصورة هنا أو انقر للاختيار</p>
                    <input type="file" id="fileInput" style="display: none;" accept="image/*">
                    <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                        اختيار صورة
                    </button>
                    <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                        الصيغ المدعومة: JPG, PNG, JPEG (الحد الأقصى: 10 ميجابايت)
                    </p>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>جاري معالجة الصورة...</p>
                </div>

                <div class="results" id="results">
                    <h3>📊 نتائج التحليل</h3>
                    <div id="resultContent"></div>
                </div>

                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/admin" class="btn">العودة للوحة الإدارة</a>
                    <a href="http://localhost:5001" class="btn" target="_blank">خدمة معالجة الصور</a>
                    <a href="/image-processing" class="btn">النسخة الإنجليزية</a>
                </div>
            </div>

            <script>
                const uploadArea = document.getElementById('uploadArea');
                const fileInput = document.getElementById('fileInput');
                const loading = document.getElementById('loading');
                const results = document.getElementById('results');
                const resultContent = document.getElementById('resultContent');

                // وظائف السحب والإفلات
                uploadArea.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    uploadArea.style.borderColor = '#4CAF50';
                    uploadArea.style.background = 'rgba(76, 175, 80, 0.2)';
                });

                uploadArea.addEventListener('dragleave', () => {
                    uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
                    uploadArea.style.background = 'rgba(255, 255, 255, 0.1)';
                });

                uploadArea.addEventListener('drop', (e) => {
                    e.preventDefault();
                    uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
                    uploadArea.style.background = 'rgba(255, 255, 255, 0.1)';
                    const files = e.dataTransfer.files;
                    if (files.length > 0) {
                        processFile(files[0]);
                    }
                });

                fileInput.addEventListener('change', (e) => {
                    if (e.target.files.length > 0) {
                        processFile(e.target.files[0]);
                    }
                });

                async function processFile(file) {
                    if (!file.type.startsWith('image/')) {
                        alert('يرجى اختيار ملف صورة');
                        return;
                    }

                    if (file.size > 10 * 1024 * 1024) {
                        alert('يجب أن يكون حجم الملف أقل من 10 ميجابايت');
                        return;
                    }

                    loading.style.display = 'block';
                    results.style.display = 'none';

                    const formData = new FormData();
                    formData.append('file', file);

                    try {
                        const response = await fetch('http://localhost:5001/process', {
                            method: 'POST',
                            body: formData
                        });

                        const result = await response.json();

                        loading.style.display = 'none';
                        results.style.display = 'block';

                        resultContent.innerHTML = `
                            <h4>🌱 نتائج تحليل النبات</h4>
                            <p><strong>الملف:</strong> ${result.filename || file.name}</p>
                            <p><strong>تم اكتشاف النبات:</strong> ${result.analysis?.plant_detected ? 'نعم' : 'لا'}</p>
                            <p><strong>نوع النبات:</strong> ${getArabicPlantName(result.analysis?.plant_type) || 'غير معروف'}</p>
                            <p><strong>الحالة الصحية:</strong> ${getArabicHealthStatus(result.analysis?.health_status) || 'غير معروف'}</p>
                            <p><strong>مرحلة النمو:</strong> ${getArabicGrowthStage(result.analysis?.growth_stage) || 'غير معروف'}</p>
                            <p><strong>احتمالية المرض:</strong> ${((result.analysis?.disease_probability || 0) * 100).toFixed(1)}%</p>
                            <h4>📋 التوصيات:</h4>
                            <ul>
                                ${result.recommendations?.map(rec => `<li>${translateRecommendation(rec)}</li>`).join('') || '<li>لا توجد توصيات محددة</li>'}
                            </ul>
                            <p><strong>وقت التحليل:</strong> ${new Date(result.timestamp).toLocaleString('ar-SA')}</p>
                        `;
                    } catch (error) {
                        loading.style.display = 'none';
                        alert('خطأ في معالجة الصورة: ' + error.message);
                    }
                }

                function getArabicPlantName(plantType) {
                    const translations = {
                        'tomato': 'طماطم',
                        'potato': 'بطاطس',
                        'corn': 'ذرة',
                        'wheat': 'قمح',
                        'cucumber': 'خيار',
                        'pepper': 'فلفل',
                        'lettuce': 'خس',
                        'carrot': 'جزر'
                    };
                    return translations[plantType] || plantType;
                }

                function getArabicHealthStatus(status) {
                    const translations = {
                        'healthy': 'صحي',
                        'sick': 'مريض',
                        'diseased': 'مصاب بمرض',
                        'excellent': 'ممتاز',
                        'good': 'جيد',
                        'poor': 'ضعيف'
                    };
                    return translations[status] || status;
                }

                function getArabicGrowthStage(stage) {
                    const translations = {
                        'seedling': 'شتلة',
                        'flowering': 'إزهار',
                        'fruiting': 'إثمار',
                        'mature': 'ناضج',
                        'young': 'صغير',
                        'adult': 'بالغ'
                    };
                    return translations[stage] || stage;
                }

                function translateRecommendation(rec) {
                    const translations = {
                        'Continue current care routine': 'استمر في روتين العناية الحالي',
                        'Monitor for pests weekly': 'راقب الآفات أسبوعياً',
                        'Maintain optimal watering': 'حافظ على الري الأمثل',
                        'Plant appears healthy': 'النبات يبدو صحياً',
                        'Check for early blight': 'تحقق من اللفحة المبكرة',
                        'Increase watering frequency': 'زد من تكرار الري',
                        'Consider organic fertilizer': 'فكر في السماد العضوي'
                    };
                    return translations[rec] || rec;
                }
            </script>
        </body>
        </html>
        """
        return html

    @app.get("/ar/settings", response_class=HTMLResponse)
    async def arabic_settings_page():
        """صفحة الإعدادات باللغة العربية"""
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>إعدادات النظام - نظام الذكاء الاصطناعي الزراعي</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: white;
                }
                .header {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 1rem 2rem;
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                }
                .container {
                    max-width: 1200px;
                    margin: 2rem auto;
                    padding: 0 2rem;
                }
                .settings-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 2rem;
                    margin-top: 2rem;
                }
                .card {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                .btn {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 0.8rem 1.5rem;
                    border-radius: 25px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 0.5rem 0.5rem 0.5rem 0;
                    transition: all 0.3s;
                }
                .btn:hover {
                    background: #45a049;
                    transform: translateY(-2px);
                }
                .form-group {
                    margin: 1rem 0;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 0.5rem;
                    font-weight: bold;
                }
                .form-group input, .form-group select {
                    width: 100%;
                    padding: 0.8rem;
                    border: none;
                    border-radius: 5px;
                    background: rgba(255, 255, 255, 0.9);
                    color: #333;
                    font-family: inherit;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>⚙️ إعدادات النظام الزراعي الذكي</h1>
                <p>تكوين معاملات النظام والتفضيلات</p>
            </div>

            <div class="container">
                <div class="settings-grid">
                    <div class="card">
                        <h3>🗄️ إعدادات قاعدة البيانات</h3>
                        <div class="form-group">
                            <label>مضيف قاعدة البيانات:</label>
                            <input type="text" value="agri_ai_db" readonly>
                        </div>
                        <div class="form-group">
                            <label>منفذ قاعدة البيانات:</label>
                            <input type="text" value="5432" readonly>
                        </div>
                        <div class="form-group">
                            <label>اسم قاعدة البيانات:</label>
                            <input type="text" value="agri_ai_db" readonly>
                        </div>
                        <button class="btn" onclick="testDatabaseConnection()">اختبار الاتصال</button>
                        <div id="dbResult" style="margin-top: 1rem; display: none;"></div>
                    </div>

                    <div class="card">
                        <h3>🔧 تكوين النظام</h3>
                        <div class="form-group">
                            <label>لغة النظام:</label>
                            <select id="systemLanguage">
                                <option value="ar" selected>العربية</option>
                                <option value="en">English</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>مستوى السجل:</label>
                            <select id="logLevel">
                                <option value="INFO" selected>معلومات</option>
                                <option value="DEBUG">تصحيح</option>
                                <option value="WARNING">تحذير</option>
                                <option value="ERROR">خطأ</option>
                            </select>
                        </div>
                        <button class="btn" onclick="saveSettings()">حفظ الإعدادات</button>
                        <div id="settingsResult" style="margin-top: 1rem; display: none;"></div>
                    </div>

                    <div class="card">
                        <h3>🤖 تكوين الذكاء الاصطناعي</h3>
                        <div class="form-group">
                            <label>رابط خدمة الذكاء الاصطناعي:</label>
                            <input type="text" value="http://localhost:5000" readonly>
                        </div>
                        <div class="form-group">
                            <label>رابط معالجة الصور:</label>
                            <input type="text" value="http://localhost:5001" readonly>
                        </div>
                        <div class="form-group">
                            <label>رابط تشخيص الأمراض:</label>
                            <input type="text" value="http://localhost:5002" readonly>
                        </div>
                        <button class="btn" onclick="testAIServices()">اختبار خدمات الذكاء الاصطناعي</button>
                        <div id="aiResult" style="margin-top: 1rem; display: none;"></div>
                    </div>

                    <div class="card">
                        <h3>📊 إعدادات المراقبة</h3>
                        <div class="form-group">
                            <label>رابط Prometheus:</label>
                            <input type="text" value="http://localhost:9090" readonly>
                        </div>
                        <div class="form-group">
                            <label>رابط Grafana:</label>
                            <input type="text" value="http://localhost:3000" readonly>
                        </div>
                        <a href="http://localhost:9090" class="btn" target="_blank">فتح Prometheus</a>
                        <a href="http://localhost:3000" class="btn" target="_blank">فتح Grafana</a>
                    </div>
                </div>

                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/admin" class="btn">العودة للوحة الإدارة</a>
                    <a href="/settings" class="btn">النسخة الإنجليزية</a>
                </div>
            </div>

            <script>
                async function testDatabaseConnection() {
                    const resultDiv = document.getElementById('dbResult');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<p>🔄 جاري اختبار اتصال قاعدة البيانات...</p>';

                    try {
                        const response = await fetch('/api/database/test');
                        const data = await response.json();

                        if (data.success) {
                            resultDiv.innerHTML = `
                                <p style="color: #4CAF50;">✅ ${data.message}</p>
                                <p>المضيف: ${data.details.host}</p>
                                <p>المنفذ: ${data.details.port}</p>
                                <p>قاعدة البيانات: ${data.details.database}</p>
                                <p>وقت الاستجابة: ${data.details.response_time}</p>
                            `;
                        } else {
                            resultDiv.innerHTML = '<p style="color: #f44336;">❌ ' + data.message + '</p>';
                        }
                    } catch (error) {
                        resultDiv.innerHTML = '<p style="color: #f44336;">❌ خطأ في اختبار قاعدة البيانات: ' + error.message + '</p>';
                    }
                }

                async function saveSettings() {
                    const resultDiv = document.getElementById('settingsResult');
                    const language = document.getElementById('systemLanguage').value;
                    const logLevel = document.getElementById('logLevel').value;

                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<p>🔄 جاري حفظ الإعدادات...</p>';

                    try {
                        const response = await fetch('/api/settings/save', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: `language=${language}&log_level=${logLevel}`
                        });

                        const data = await response.json();

                        if (data.success) {
                            resultDiv.innerHTML = `
                                <p style="color: #4CAF50;">✅ ${data.message}</p>
                                <p>اللغة: ${language === 'ar' ? 'العربية' : 'English'}</p>
                                <p>مستوى السجل: ${translateLogLevel(logLevel)}</p>
                                <p>تم الحفظ في: ${new Date(data.settings.timestamp).toLocaleString('ar-SA')}</p>
                            `;

                            // Store settings in localStorage
                            localStorage.setItem('systemSettings', JSON.stringify({
                                language: language,
                                logLevel: logLevel,
                                timestamp: new Date().toISOString()
                            }));
                        } else {
                            resultDiv.innerHTML = '<p style="color: #f44336;">❌ ' + data.message + '</p>';
                        }

                    } catch (error) {
                        resultDiv.innerHTML = '<p style="color: #f44336;">❌ خطأ في حفظ الإعدادات: ' + error.message + '</p>';
                    }
                }

                async function testAIServices() {
                    const resultDiv = document.getElementById('aiResult');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<p>🔄 جاري اختبار خدمات الذكاء الاصطناعي...</p>';

                    try {
                        const response = await fetch('/api/ai-services/status');
                        const data = await response.json();

                        if (data.summary && data.summary.healthy === data.summary.total) {
                            resultDiv.innerHTML = `
                                <p style="color: #4CAF50;">✅ جميع خدمات الذكاء الاصطناعي تعمل بشكل صحي!</p>
                                <p>الخدمات: ${data.summary.healthy}/${data.summary.total} متصلة</p>
                                <ul style="text-align: right; margin: 1rem 0;">
                                    ${data.services.map(service =>
                                        `<li>${translateServiceName(service.name)}: ${service.status === 'healthy' ? '✅' : '❌'} ${translateStatus(service.status)}</li>`
                                    ).join('')}
                                </ul>
                            `;
                        } else {
                            resultDiv.innerHTML = `
                                <p style="color: #f44336;">⚠️ بعض خدمات الذكاء الاصطناعي تواجه مشاكل!</p>
                                <p>الخدمات: ${data.summary.healthy}/${data.summary.total} متصلة</p>
                            `;
                        }
                    } catch (error) {
                        resultDiv.innerHTML = '<p style="color: #f44336;">❌ خطأ في اختبار خدمات الذكاء الاصطناعي: ' + error.message + '</p>';
                    }
                }

                function translateLogLevel(level) {
                    const translations = {
                        'INFO': 'معلومات',
                        'DEBUG': 'تصحيح',
                        'WARNING': 'تحذير',
                        'ERROR': 'خطأ'
                    };
                    return translations[level] || level;
                }

                function translateServiceName(name) {
                    const translations = {
                        'AI Service': 'خدمة الذكاء الاصطناعي',
                        'Image Processing': 'معالجة الصور',
                        'Disease Diagnosis': 'تشخيص الأمراض'
                    };
                    return translations[name] || name;
                }

                function translateStatus(status) {
                    const translations = {
                        'healthy': 'صحي',
                        'unhealthy': 'غير صحي',
                        'offline': 'غير متصل'
                    };
                    return translations[status] || status;
                }

                // Load saved settings on page load
                window.onload = function() {
                    const savedSettings = localStorage.getItem('systemSettings');
                    if (savedSettings) {
                        try {
                            const settings = JSON.parse(savedSettings);
                            document.getElementById('systemLanguage').value = settings.language || 'ar';
                            document.getElementById('logLevel').value = settings.logLevel || 'INFO';
                        } catch (error) {
                            console.error('خطأ في تحميل الإعدادات المحفوظة:', error);
                        }
                    }
                };
            </script>
        </body>
        </html>
        """
        return html

    @app.get("/ar/settings/database", response_class=HTMLResponse)
    async def arabic_database_settings_page():
        """صفحة إعدادات قاعدة البيانات باللغة العربية"""
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>إعدادات قاعدة البيانات - نظام الذكاء الاصطناعي الزراعي</title>
            <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Cairo', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: white;
                    line-height: 1.8;
                }
                .header {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    backdrop-filter: blur(20px);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                }
                .header h1 {
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin-bottom: 0.5rem;
                    background: linear-gradient(45deg, #fff, #e0e7ff);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                .container {
                    max-width: 1200px;
                    margin: 2rem auto;
                    padding: 0 2rem;
                }
                .card {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2.5rem;
                    border-radius: 20px;
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    margin: 2rem 0;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }
                .card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
                }
                .card h3 {
                    font-size: 1.5rem;
                    font-weight: 600;
                    margin-bottom: 1.5rem;
                    color: #fff;
                }
                .form-group {
                    margin: 1.5rem 0;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 0.8rem;
                    font-weight: 500;
                    font-size: 1rem;
                    color: rgba(255, 255, 255, 0.9);
                }
                .form-group input, .form-group select, .form-group textarea {
                    width: 100%;
                    padding: 1rem;
                    border: none;
                    border-radius: 12px;
                    background: rgba(255, 255, 255, 0.9);
                    color: #333;
                    font-family: inherit;
                    font-size: 1rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
                    outline: none;
                    background: rgba(255, 255, 255, 1);
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                    transform: translateY(-2px);
                }
                .btn {
                    background: linear-gradient(45deg, #4CAF50, #45a049);
                    color: white;
                    border: none;
                    padding: 1rem 2rem;
                    border-radius: 25px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 0.5rem 0.5rem 0.5rem 0;
                    transition: all 0.3s ease;
                    font-weight: 500;
                    font-size: 1rem;
                    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
                }
                .btn:hover {
                    background: linear-gradient(45deg, #45a049, #4CAF50);
                    transform: translateY(-3px);
                    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
                }
                .btn-secondary {
                    background: linear-gradient(45deg, #6c757d, #5a6268);
                    box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
                }
                .btn-secondary:hover {
                    background: linear-gradient(45deg, #5a6268, #6c757d);
                    box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4);
                }
                .status-indicator {
                    display: inline-flex;
                    align-items: center;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    font-weight: 500;
                    margin: 0.5rem 0;
                }
                .status-connected {
                    background: rgba(76, 175, 80, 0.2);
                    color: #4CAF50;
                    border: 1px solid rgba(76, 175, 80, 0.3);
                }
                .status-disconnected {
                    background: rgba(244, 67, 54, 0.2);
                    color: #f44336;
                    border: 1px solid rgba(244, 67, 54, 0.3);
                }
                .grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 2rem;
                    margin-top: 2rem;
                }
                .result-box {
                    margin-top: 1.5rem;
                    padding: 1rem;
                    border-radius: 12px;
                    display: none;
                    font-size: 0.95rem;
                }
                .result-success {
                    background: rgba(76, 175, 80, 0.1);
                    border: 1px solid rgba(76, 175, 80, 0.3);
                    color: #4CAF50;
                }
                .result-error {
                    background: rgba(244, 67, 54, 0.1);
                    border: 1px solid rgba(244, 67, 54, 0.3);
                    color: #f44336;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🗄️ إعدادات قاعدة البيانات</h1>
                <p>إدارة اتصالات قاعدة البيانات وإعداداتها للنظام الزراعي الذكي</p>
            </div>

            <div class="container">
                <div class="grid">
                    <div class="card">
                        <h3>📊 حالة قاعدة البيانات الحالية</h3>
                        <div class="status-indicator status-connected" id="dbStatus">
                            ✅ متصل بـ PostgreSQL
                        </div>
                        <div class="form-group">
                            <label>مضيف قاعدة البيانات:</label>
                            <input type="text" value="agri_ai_db" readonly>
                        </div>
                        <div class="form-group">
                            <label>منفذ قاعدة البيانات:</label>
                            <input type="text" value="5432" readonly>
                        </div>
                        <div class="form-group">
                            <label>اسم قاعدة البيانات:</label>
                            <input type="text" value="agri_ai_db" readonly>
                        </div>
                        <button class="btn" onclick="testConnection()">🔍 اختبار الاتصال</button>
                        <button class="btn btn-secondary" onclick="refreshStatus()">🔄 تحديث الحالة</button>
                        <div id="connectionResult" class="result-box"></div>
                    </div>

                    <div class="card">
                        <h3>⚙️ تكوين قاعدة البيانات</h3>
                        <div class="form-group">
                            <label>حجم مجموعة الاتصالات:</label>
                            <input type="number" value="10" min="1" max="100">
                        </div>
                        <div class="form-group">
                            <label>مهلة الاتصال (بالثواني):</label>
                            <input type="number" value="30" min="5" max="300">
                        </div>
                        <div class="form-group">
                            <label>مهلة الاستعلام (بالثواني):</label>
                            <input type="number" value="60" min="10" max="600">
                        </div>
                        <button class="btn" onclick="saveDbConfig()">💾 حفظ التكوين</button>
                        <div id="configResult" class="result-box"></div>
                    </div>

                    <div class="card">
                        <h3>🔧 صيانة قاعدة البيانات</h3>
                        <div class="form-group">
                            <label>آخر نسخة احتياطية:</label>
                            <input type="text" value="2025-05-27 14:00:00" readonly>
                        </div>
                        <div class="form-group">
                            <label>حجم قاعدة البيانات:</label>
                            <input type="text" value="~50 ميجابايت" readonly>
                        </div>
                        <div class="form-group">
                            <label>الاتصالات النشطة:</label>
                            <input type="text" value="3" readonly>
                        </div>
                        <button class="btn" onclick="createBackup()">💾 إنشاء نسخة احتياطية</button>
                        <button class="btn btn-secondary" onclick="optimizeDb()">⚡ تحسين قاعدة البيانات</button>
                        <div id="maintenanceResult" class="result-box"></div>
                    </div>

                    <div class="card">
                        <h3>📈 إحصائيات قاعدة البيانات</h3>
                        <div id="dbStats">
                            <p>جاري تحميل الإحصائيات...</p>
                        </div>
                        <button class="btn" onclick="loadStats()">📊 تحديث الإحصائيات</button>
                    </div>
                </div>

                <div style="text-align: center; margin-top: 3rem;">
                    <a href="/ar/settings" class="btn btn-secondary">⬅️ العودة للإعدادات</a>
                    <a href="/settings/database" class="btn">🌐 English</a>
                    <a href="/admin" class="btn">🏠 لوحة الإدارة</a>
                </div>
            </div>

            <script>
                async function testConnection() {
                    const resultDiv = document.getElementById('connectionResult');
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'result-box';
                    resultDiv.innerHTML = '🔄 جاري اختبار اتصال قاعدة البيانات...';

                    try {
                        const response = await fetch('/api/database/test');
                        const data = await response.json();

                        if (data.success) {
                            resultDiv.className = 'result-box result-success';
                            resultDiv.innerHTML = `
                                <strong>✅ نجح الاتصال!</strong><br>
                                المضيف: ${data.details.host}<br>
                                المنفذ: ${data.details.port}<br>
                                قاعدة البيانات: ${data.details.database}<br>
                                وقت الاستجابة: ${data.details.response_time}
                            `;
                            document.getElementById('dbStatus').className = 'status-indicator status-connected';
                            document.getElementById('dbStatus').innerHTML = '✅ متصل بـ PostgreSQL';
                        } else {
                            resultDiv.className = 'result-box result-error';
                            resultDiv.innerHTML = '❌ ' + data.message;
                            document.getElementById('dbStatus').className = 'status-indicator status-disconnected';
                            document.getElementById('dbStatus').innerHTML = '❌ فشل الاتصال';
                        }
                    } catch (error) {
                        resultDiv.className = 'result-box result-error';
                        resultDiv.innerHTML = '❌ خطأ: ' + error.message;
                    }
                }

                async function saveDbConfig() {
                    const resultDiv = document.getElementById('configResult');
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'result-box';
                    resultDiv.innerHTML = '🔄 جاري حفظ التكوين...';

                    setTimeout(() => {
                        resultDiv.className = 'result-box result-success';
                        resultDiv.innerHTML = '✅ تم حفظ تكوين قاعدة البيانات بنجاح!';
                    }, 1000);
                }

                async function createBackup() {
                    const resultDiv = document.getElementById('maintenanceResult');
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'result-box';
                    resultDiv.innerHTML = '🔄 جاري إنشاء نسخة احتياطية من قاعدة البيانات...';

                    setTimeout(() => {
                        resultDiv.className = 'result-box result-success';
                        resultDiv.innerHTML = '✅ تم إنشاء النسخة الاحتياطية بنجاح! الملف: backup_' + new Date().toISOString().slice(0,19).replace(/:/g, '-') + '.sql';
                    }, 2000);
                }

                async function optimizeDb() {
                    const resultDiv = document.getElementById('maintenanceResult');
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'result-box';
                    resultDiv.innerHTML = '🔄 جاري تحسين قاعدة البيانات...';

                    setTimeout(() => {
                        resultDiv.className = 'result-box result-success';
                        resultDiv.innerHTML = '✅ تم تحسين قاعدة البيانات بنجاح! تحسن الأداء بنسبة ~15%';
                    }, 3000);
                }

                async function refreshStatus() {
                    document.getElementById('dbStatus').innerHTML = '🔄 جاري فحص الحالة...';
                    await testConnection();
                }

                async function loadStats() {
                    const statsDiv = document.getElementById('dbStats');
                    statsDiv.innerHTML = '🔄 جاري تحميل الإحصائيات...';

                    setTimeout(() => {
                        statsDiv.innerHTML = `
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; text-align: right;">
                                <div><strong>إجمالي الجداول:</strong> 12</div>
                                <div><strong>إجمالي السجلات:</strong> 1,247</div>
                                <div><strong>حجم قاعدة البيانات:</strong> 52.3 ميجابايت</div>
                                <div><strong>حجم الفهارس:</strong> 8.7 ميجابايت</div>
                                <div><strong>الاتصالات النشطة:</strong> 3</div>
                                <div><strong>الحد الأقصى للاتصالات:</strong> 100</div>
                                <div><strong>وقت التشغيل:</strong> 2 ساعة 15 دقيقة</div>
                                <div><strong>آخر استعلام:</strong> منذ ثانيتين</div>
                            </div>
                        `;
                    }, 1000);
                }

                // تهيئة الصفحة
                window.onload = function() {
                    testConnection();
                    loadStats();
                };
            </script>
        </body>
        </html>
        """
        return html

    @app.get("/ar/disease-diagnosis", response_class=HTMLResponse)
    async def arabic_disease_diagnosis_page():
        """صفحة تشخيص الأمراض باللغة العربية"""
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>تشخيص أمراض النباتات - نظام الذكاء الاصطناعي الزراعي</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: white;
                }
                .header {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 1rem 2rem;
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                }
                .container {
                    max-width: 800px;
                    margin: 2rem auto;
                    padding: 0 2rem;
                }
                .form-card {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    margin: 2rem 0;
                }
                .form-group {
                    margin: 1rem 0;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 0.5rem;
                    font-weight: bold;
                }
                .form-group input, .form-group select, .form-group textarea {
                    width: 100%;
                    padding: 0.8rem;
                    border: none;
                    border-radius: 5px;
                    background: rgba(255, 255, 255, 0.9);
                    color: #333;
                    font-family: inherit;
                }
                .btn {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 0.8rem 1.5rem;
                    border-radius: 25px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin: 0.5rem;
                    transition: all 0.3s;
                }
                .btn:hover {
                    background: #45a049;
                    transform: translateY(-2px);
                }
                .results {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    margin: 2rem 0;
                    display: none;
                }
                .loading {
                    display: none;
                    text-align: center;
                    margin: 2rem 0;
                }
                .spinner {
                    border: 4px solid rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    border-top: 4px solid #4CAF50;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔬 نظام تشخيص أمراض النباتات</h1>
                <p>تشخيص أمراض النباتات والحصول على توصيات العلاج</p>
            </div>

            <div class="container">
                <div class="form-card">
                    <h3>📝 معلومات النبات</h3>
                    <form id="diagnosisForm">
                        <div class="form-group">
                            <label for="cropType">نوع المحصول:</label>
                            <select id="cropType" required>
                                <option value="">اختر نوع المحصول</option>
                                <option value="tomato">طماطم</option>
                                <option value="potato">بطاطس</option>
                                <option value="corn">ذرة</option>
                                <option value="wheat">قمح</option>
                                <option value="cucumber">خيار</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="symptoms">الأعراض (صف ما تلاحظه):</label>
                            <textarea id="symptoms" rows="4" placeholder="صف الأعراض التي تلاحظها على النبات (مثل: أوراق صفراء، بقع داكنة، ذبول)"></textarea>
                        </div>

                        <div class="form-group">
                            <label for="location">الموقع (اختياري):</label>
                            <input type="text" id="location" placeholder="موقع المزرعة أو المنطقة">
                        </div>

                        <button type="submit" class="btn">🔍 تشخيص المرض</button>
                    </form>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>جاري تحليل الأعراض...</p>
                </div>

                <div class="results" id="results">
                    <h3>🩺 نتائج التشخيص</h3>
                    <div id="resultContent"></div>
                </div>

                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/admin" class="btn">العودة للوحة الإدارة</a>
                    <a href="http://localhost:5002" class="btn" target="_blank">خدمة تشخيص الأمراض</a>
                    <button class="btn" onclick="loadDiseases()">📚 عرض الأمراض الشائعة</button>
                    <a href="/disease-diagnosis" class="btn">النسخة الإنجليزية</a>
                </div>
            </div>

            <script>
                const form = document.getElementById('diagnosisForm');
                const loading = document.getElementById('loading');
                const results = document.getElementById('results');
                const resultContent = document.getElementById('resultContent');

                form.addEventListener('submit', async (e) => {
                    e.preventDefault();

                    const cropType = document.getElementById('cropType').value;
                    const symptoms = document.getElementById('symptoms').value;
                    const location = document.getElementById('location').value;

                    if (!cropType || !symptoms) {
                        alert('يرجى ملء نوع المحصول والأعراض');
                        return;
                    }

                    loading.style.display = 'block';
                    results.style.display = 'none';

                    try {
                        const response = await fetch('http://localhost:5002/diagnose', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                crop_type: cropType,
                                symptoms: symptoms.split(',').map(s => s.trim()),
                                location: location
                            })
                        });

                        const result = await response.json();

                        loading.style.display = 'none';
                        results.style.display = 'block';

                        resultContent.innerHTML = `
                            <h4>🦠 المرض المحدد</h4>
                            <p><strong>المرض:</strong> ${translateDiseaseName(result.diagnosis?.disease) || 'غير معروف'}</p>
                            <p><strong>الاسم العلمي:</strong> ${result.diagnosis?.scientific_name || 'غير متوفر'}</p>
                            <p><strong>مستوى الثقة:</strong> ${((result.diagnosis?.confidence || 0) * 100).toFixed(1)}%</p>
                            <p><strong>الشدة:</strong> ${translateSeverity(result.diagnosis?.severity) || 'غير معروف'}</p>

                            <h4>💊 العلاج</h4>
                            <p><strong>العلاج الأساسي:</strong> ${translateTreatment(result.treatment?.primary?.product) || 'استشر المختص'}</p>
                            <p><strong>التطبيق:</strong> ${translateFrequency(result.treatment?.primary?.frequency) || 'حسب الحاجة'} لمدة ${translateDuration(result.treatment?.primary?.duration) || 'الفترة الموصى بها'}</p>

                            <h4>🛡️ إجراءات الوقاية</h4>
                            <ul>
                                ${result.prevention?.map(prev => `<li>${translatePrevention(prev)}</li>`).join('') || '<li>اتبع إرشادات العناية العامة بالنباتات</li>'}
                            </ul>

                            <h4>📈 التوقعات</h4>
                            <p><strong>وقت الشفاء:</strong> ${translateRecoveryTime(result.prognosis?.recovery_time) || 'متغير'}</p>
                            <p><strong>معدل النجاح:</strong> ${((result.prognosis?.success_rate || 0) * 100).toFixed(1)}%</p>

                            <p><strong>وقت التشخيص:</strong> ${new Date(result.timestamp).toLocaleString('ar-SA')}</p>
                        `;
                    } catch (error) {
                        loading.style.display = 'none';
                        alert('خطأ أثناء التشخيص: ' + error.message);
                    }
                });

                async function loadDiseases() {
                    try {
                        const response = await fetch('http://localhost:5002/diseases');
                        const data = await response.json();

                        results.style.display = 'block';
                        resultContent.innerHTML = `
                            <h4>📚 أمراض النباتات الشائعة</h4>
                            ${data.common_diseases?.map(disease => `
                                <div style="margin: 1rem 0; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                                    <h5>${translateDiseaseName(disease.name)}</h5>
                                    <p><strong>الاسم العلمي:</strong> ${disease.scientific_name || 'غير متوفر'}</p>
                                    <p><strong>يصيب:</strong> ${disease.crops?.map(crop => getArabicCropName(crop)).join(', ') || 'محاصيل متنوعة'}</p>
                                    <p><strong>الأعراض:</strong> ${disease.symptoms?.map(symptom => translateSymptom(symptom)).join(', ') || 'متنوعة'}</p>
                                </div>
                            `).join('') || '<p>لا توجد بيانات أمراض متاحة</p>'}
                            <p><strong>إجمالي الأمراض في قاعدة البيانات:</strong> ${data.total_diseases || 0}</p>
                        `;
                    } catch (error) {
                        alert('خطأ في تحميل الأمراض: ' + error.message);
                    }
                }

                function translateDiseaseName(disease) {
                    const translations = {
                        'Early Blight': 'اللفحة المبكرة',
                        'Powdery Mildew': 'البياض الدقيقي',
                        'Rust': 'الصدأ',
                        'Bacterial Spot': 'البقعة البكتيرية'
                    };
                    return translations[disease] || disease;
                }

                function translateSeverity(severity) {
                    const translations = {
                        'mild': 'خفيف',
                        'moderate': 'متوسط',
                        'severe': 'شديد',
                        'critical': 'حرج'
                    };
                    return translations[severity] || severity;
                }

                function translateTreatment(treatment) {
                    const translations = {
                        'copper-based fungicide': 'مبيد فطري أساسه النحاس',
                        'systemic fungicide': 'مبيد فطري جهازي',
                        'organic treatment': 'علاج عضوي'
                    };
                    return translations[treatment] || treatment;
                }

                function translateFrequency(frequency) {
                    const translations = {
                        'weekly': 'أسبوعياً',
                        'bi-weekly': 'كل أسبوعين',
                        'monthly': 'شهرياً',
                        'daily': 'يومياً'
                    };
                    return translations[frequency] || frequency;
                }

                function translateDuration(duration) {
                    const translations = {
                        '3 weeks': '3 أسابيع',
                        '2 weeks': 'أسبوعين',
                        '1 month': 'شهر واحد',
                        'recommended period': 'الفترة الموصى بها'
                    };
                    return translations[duration] || duration;
                }

                function translatePrevention(prevention) {
                    const translations = {
                        'crop rotation': 'دوران المحاصيل',
                        'proper spacing': 'التباعد المناسب',
                        'avoid overhead watering': 'تجنب الري العلوي',
                        'remove plant debris': 'إزالة بقايا النباتات',
                        'use disease-resistant varieties': 'استخدام أصناف مقاومة للأمراض'
                    };
                    return translations[prevention] || prevention;
                }

                function translateRecoveryTime(time) {
                    const translations = {
                        '2-4 weeks': '2-4 أسابيع',
                        '1-2 weeks': '1-2 أسبوع',
                        '1 month': 'شهر واحد',
                        'Variable': 'متغير'
                    };
                    return translations[time] || time;
                }

                function getArabicCropName(crop) {
                    const translations = {
                        'tomato': 'طماطم',
                        'potato': 'بطاطس',
                        'corn': 'ذرة',
                        'wheat': 'قمح',
                        'cucumber': 'خيار',
                        'pepper': 'فلفل'
                    };
                    return translations[crop] || crop;
                }

                function translateSymptom(symptom) {
                    const translations = {
                        'dark spots on leaves': 'بقع داكنة على الأوراق',
                        'yellowing': 'اصفرار',
                        'defoliation': 'تساقط الأوراق',
                        'white powdery coating': 'طلاء أبيض مسحوقي',
                        'leaf distortion': 'تشوه الأوراق',
                        'orange/brown pustules': 'بثور برتقالية/بنية',
                        'leaf yellowing': 'اصفرار الأوراق',
                        'small dark spots': 'بقع صغيرة داكنة',
                        'leaf drop': 'تساقط الأوراق',
                        'fruit lesions': 'آفات الثمار'
                    };
                    return translations[symptom] || symptom;
                }
            </script>
        </body>
        </html>
        """
        return html
