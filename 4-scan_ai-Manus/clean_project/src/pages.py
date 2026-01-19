#!/usr/bin/env python3
"""
صفحات النظام الإضافية
Additional System Pages
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


def add_pages_routes(app: FastAPI) -> None:
    """إضافة مسارات الصفحات الإضافية"""

    @app.get("/image-processing", response_class=HTMLResponse)
    async def image_processing_page() -> str:
        """صفحة معالجة الصور"""
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Image Processing - Agricultural AI System</title>
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
                .upload-area.dragover {
                    border-color: #4CAF50;
                    background: rgba(76, 175, 80, 0.2);
                }
                .file-input {
                    display: none;
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
                <h1>🖼️ Agricultural Image Processing</h1>
                <p>Upload and analyze agricultural images using AI</p>
            </div>

            <div class="container">
                <div class="upload-area" id="uploadArea">
                    <h3>📤 Upload Image for Analysis</h3>
                    <p>Drag and drop an image here or click to select</p>
                    <input type="file" id="fileInput" class="file-input" accept="image/*">
                    <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                        Select Image
                    </button>
                    <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                        Supported formats: JPG, PNG, JPEG (Max: 10MB)
                    </p>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Processing image...</p>
                </div>

                <div class="results" id="results">
                    <h3>📊 Analysis Results</h3>
                    <div id="resultContent"></div>
                </div>

                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/admin" class="btn">Back to Admin Panel</a>
                    <a href="http://localhost:5001" class="btn" target="_blank">Image Service API</a>
                </div>
            </div>

            <script>
                const uploadArea = document.getElementById('uploadArea');
                const fileInput = document.getElementById('fileInput');
                const loading = document.getElementById('loading');
                const results = document.getElementById('results');
                const resultContent = document.getElementById('resultContent');

                // Drag and drop functionality
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
                        alert('Please select an image file');
                        return;
                    }

                    if (file.size > 10 * 1024 * 1024) {
                        alert('File size must be less than 10MB');
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
                            <h4>🌱 Plant Analysis Results</h4>
                            <p><strong>File:</strong> ${result.filename || file.name}</p>
                            <p><strong>Plant Detected:</strong> ${result.analysis?.plant_detected ? 'Yes' : 'No'}</p>
                            <p><strong>Plant Type:</strong> ${result.analysis?.plant_type || 'Unknown'}</p>
                            <p><strong>Health Status:</strong> ${result.analysis?.health_status || 'Unknown'}</p>
                            <p><strong>Growth Stage:</strong> ${result.analysis?.growth_stage || 'Unknown'}</p>
                            <p><strong>Disease Probability:</strong> ${((result.analysis?.disease_probability || 0) * 100).toFixed(1)}%</p>
                            <h4>📋 Recommendations:</h4>
                            <ul>
                                ${result.recommendations?.map(rec => `<li>${rec}</li>`).join('') || '<li>No specific recommendations</li>'}
                            </ul>
                            <p><strong>Analysis Time:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
                        `;
                    } catch (error) {
                        loading.style.display = 'none';
                        alert('Error processing image: ' + error.message);
                    }
                }
            </script>
        </body>
        </html>
        """
        return html

    @app.get("/disease-diagnosis", response_class=HTMLResponse)
    async def disease_diagnosis_page() -> str:
        """صفحة تشخيص الأمراض"""
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Disease Diagnosis - Agricultural AI System</title>
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
                <h1>🔬 Disease Diagnosis System</h1>
                <p>Diagnose plant diseases and get treatment recommendations</p>
            </div>

            <div class="container">
                <div class="form-card">
                    <h3>📝 Plant Information</h3>
                    <form id="diagnosisForm">
                        <div class="form-group">
                            <label for="cropType">Crop Type:</label>
                            <select id="cropType" required>
                                <option value="">Select crop type</option>
                                <option value="tomato">Tomato</option>
                                <option value="potato">Potato</option>
                                <option value="corn">Corn</option>
                                <option value="wheat">Wheat</option>
                                <option value="cucumber">Cucumber</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="symptoms">Symptoms (describe what you observe):</label>
                            <textarea id="symptoms" rows="4" placeholder="Describe the symptoms you observe on the plant (e.g., yellow leaves, dark spots, wilting)"></textarea>
                        </div>

                        <div class="form-group">
                            <label for="location">Location (optional):</label>
                            <input type="text" id="location" placeholder="Farm location or region">
                        </div>

                        <button type="submit" class="btn">🔍 Diagnose Disease</button>
                    </form>
                </div>

                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing symptoms...</p>
                </div>

                <div class="results" id="results">
                    <h3>🩺 Diagnosis Results</h3>
                    <div id="resultContent"></div>
                </div>

                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/admin" class="btn">Back to Admin Panel</a>
                    <a href="http://localhost:5002" class="btn" target="_blank">Diagnosis Service API</a>
                    <button class="btn" onclick="loadDiseases()">📚 View Common Diseases</button>
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
                        alert('Please fill in crop type and symptoms');
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
                            <h4>🦠 Disease Identified</h4>
                            <p><strong>Disease:</strong> ${result.diagnosis?.disease || 'Unknown'}</p>
                            <p><strong>Scientific Name:</strong> ${result.diagnosis?.scientific_name || 'N/A'}</p>
                            <p><strong>Confidence:</strong> ${((result.diagnosis?.confidence || 0) * 100).toFixed(1)}%</p>
                            <p><strong>Severity:</strong> ${result.diagnosis?.severity || 'Unknown'}</p>

                            <h4>💊 Treatment</h4>
                            <p><strong>Primary Treatment:</strong> ${result.treatment?.primary?.product || 'Consult specialist'}</p>
                            <p><strong>Application:</strong> ${result.treatment?.primary?.frequency || 'As needed'} for ${result.treatment?.primary?.duration || 'recommended period'}</p>

                            <h4>🛡️ Prevention Measures</h4>
                            <ul>
                                ${result.prevention?.map(prev => `<li>${prev}</li>`).join('') || '<li>Follow general plant care guidelines</li>'}
                            </ul>

                            <h4>📈 Prognosis</h4>
                            <p><strong>Recovery Time:</strong> ${result.prognosis?.recovery_time || 'Variable'}</p>
                            <p><strong>Success Rate:</strong> ${((result.prognosis?.success_rate || 0) * 100).toFixed(1)}%</p>

                            <p><strong>Diagnosis Time:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
                        `;
                    } catch (error) {
                        loading.style.display = 'none';
                        alert('Error during diagnosis: ' + error.message);
                    }
                });

                async function loadDiseases() {
                    try {
                        const response = await fetch('http://localhost:5002/diseases');
                        const data = await response.json();

                        results.style.display = 'block';
                        resultContent.innerHTML = `
                            <h4>📚 Common Plant Diseases</h4>
                            ${data.common_diseases?.map(disease => `
                                <div style="margin: 1rem 0; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                                    <h5>${disease.name}</h5>
                                    <p><strong>Scientific Name:</strong> ${disease.scientific_name || 'N/A'}</p>
                                    <p><strong>Affects:</strong> ${disease.crops?.join(', ') || 'Various crops'}</p>
                                    <p><strong>Symptoms:</strong> ${disease.symptoms?.join(', ') || 'Varies'}</p>
                                </div>
                            `).join('') || '<p>No disease data available</p>'}
                            <p><strong>Total Diseases in Database:</strong> ${data.total_diseases || 0}</p>
                        `;
                    } catch (error) {
                        alert('Error loading diseases: ' + error.message);
                    }
                }
            </script>
        </body>
        </html>
        """
        return html

    @app.get("/ai-services", response_class=HTMLResponse)
    async def ai_services_page() -> str:
        """صفحة خدمات الذكاء الاصطناعي"""
        html = """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI Services - Agricultural AI System</title>
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
                .service-card {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 2rem;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    margin: 2rem 0;
                }
                .service-card h3 {
                    margin-bottom: 1rem;
                }
                .service-card p {
                    margin-bottom: 1rem;
                    line-height: 1.6;
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
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🤖 AI Services</h1>
                <p>Explore our advanced AI-powered agricultural services</p>
            </div>

            <div class="container">
                <div class="service-card">
                    <h3>🌱 Plant Analysis</h3>
                    <p>Upload images of your plants for instant analysis. Our AI will identify plant species, assess health status, and detect potential diseases.</p>
                    <a href="/image-processing" class="btn">Try Plant Analysis</a>
                </div>

                <div class="service-card">
                    <h3>🔬 Disease Diagnosis</h3>
                    <p>Get accurate disease diagnosis and treatment recommendations based on symptoms and plant type. Our AI system uses advanced algorithms to provide precise diagnoses.</p>
                    <a href="/disease-diagnosis" class="btn">Try Disease Diagnosis</a>
                </div>

                <div class="service-card">
                    <h3>📊 Yield Prediction</h3>
                    <p>Predict crop yields based on historical data, weather conditions, and current plant health. Make informed decisions about your harvest.</p>
                    <a href="/yield-prediction" class="btn">Try Yield Prediction</a>
                </div>

                <div class="service-card">
                    <h3>🌦️ Weather Analysis</h3>
                    <p>Get detailed weather analysis and forecasts specifically tailored for agricultural needs. Plan your farming activities with confidence.</p>
                    <a href="/weather-analysis" class="btn">Try Weather Analysis</a>
                </div>

                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/admin" class="btn">Back to Admin Panel</a>
                </div>
            </div>
        </body>
        </html>
        """
        return html
