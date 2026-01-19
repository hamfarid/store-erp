document.addEventListener("DOMContentLoaded", () => {
    // --- DOM Elements ---
    const imageInput = document.getElementById("plant-image-input");
    const uploadArea = document.querySelector(".upload-area");
    const uploadLabel = document.querySelector(".upload-label");
    const imagePreviewContainer = document.getElementById("image-preview-container");
    const imagePreview = document.getElementById("image-preview");
    const removeImageBtn = document.getElementById("remove-image-btn");
    const analyzeImageBtn = document.getElementById("analyze-image-btn");
    const resultsSection = document.getElementById("results-section");
    const loadingIndicator = document.getElementById("loading-indicator");
    const analysisResults = document.getElementById("analysis-results");
    const visualizationArea = document.getElementById("visualization-area");

    const breedingPredictionForm = document.getElementById("breeding-prediction-form");
    const parent1Input = document.getElementById("parent1-strain");
    const parent2Input = document.getElementById("parent2-strain");

    const breedingSuggestionForm = document.getElementById("breeding-suggestion-form");
    const targetTraitInput = document.getElementById("target-trait");
    const targetValueInput = document.getElementById("target-value");

    const breedingResults = document.getElementById("breeding-results");

    const historySection = document.getElementById("history-section");
    const analysisHistory = document.getElementById("analysis-history");
    const noHistoryMsg = document.getElementById("no-history-msg");
    const clearHistoryBtn = document.getElementById("clear-history-btn");

    const toastContainer = document.getElementById("toast-container");

    let currentImageFile = null;
    const API_BASE_URL = "/api/v1"; // Example API base URL
    let currentAnalysisChart = null; // To hold the chart instance

    // --- Initialization ---
    loadHistory();
    setupChartJs(); // Ensure Chart.js is ready

    // --- Image Upload Handling ---
    uploadLabel.addEventListener("click", () => imageInput.click());
    uploadLabel.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
            imageInput.click();
        }
    });

    imageInput.addEventListener("change", (event) => {
        const files = event.target.files;
        if (files && files.length > 0) {
            handleFile(files[0]);
        }
    });

    uploadArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", () => {
        uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", (event) => {
        event.preventDefault();
        uploadArea.classList.remove("dragover");
        const files = event.dataTransfer.files;
        if (files && files.length > 0) {
            handleFile(files[0]);
            imageInput.files = files; // Update file input
        }
    });

    function handleFile(file) {
        if (file && file.type.startsWith("image/")) {
            currentImageFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreviewContainer.style.display = "block";
                uploadLabel.style.display = "none";
                analyzeImageBtn.disabled = false;
                showToast("تم اختيار الصورة بنجاح.", "success");
            };
            reader.onerror = () => {
                showToast("حدث خطأ أثناء قراءة ملف الصورة.", "error");
                resetImageUpload();
            };
            reader.readAsDataURL(file);
        } else {
            showToast("يرجى تحديد ملف صورة صالح (مثل JPG, PNG, WebP).", "error");
            resetImageUpload();
        }
    }

    removeImageBtn.addEventListener("click", resetImageUpload);

    function resetImageUpload() {
        currentImageFile = null;
        imageInput.value = "";
        imagePreview.src = "#";
        imagePreviewContainer.style.display = "none";
        uploadLabel.style.display = "block";
        analyzeImageBtn.disabled = true;
        resultsSection.style.display = "none";
        analysisResults.innerHTML = 
            `<p class="placeholder">ستظهر نتائج التحليل هنا.</p>`;
        visualizationArea.style.display = "none";
        visualizationArea.innerHTML = 
            `<h4><i class="fas fa-chart-bar"></i> تصور النتائج</h4>
             <p>سيتم عرض الرسوم البيانية والتصورات هنا.</p>
             <canvas id="analysisChart" width="400" height="200"></canvas>`; // Reset canvas
        if (currentAnalysisChart) {
            currentAnalysisChart.destroy();
            currentAnalysisChart = null;
        }
    }

    // --- API Call Simulation/Structure ---
    async function simulateApiCall(endpoint, method = "GET", body = null, delay = 1500) {
        console.log(`Simulating ${method} request to ${endpoint}...`);
        await new Promise(resolve => setTimeout(resolve, delay));

        // Simulate different responses based on endpoint
        if (endpoint === `${API_BASE_URL}/analyze` && method === "POST") {
            if (Math.random() < 0.1) { // Simulate occasional failure
                 return { ok: false, status: 500, error: "Internal Server Error (Simulated)" };
            }
            return { ok: true, status: 200, data: getMockAnalysisResults() };
        }
        if (endpoint === `${API_BASE_URL}/predict_breeding` && method === "POST") {
             return { ok: true, status: 200, data: getMockBreedingPrediction() };
        }
        if (endpoint === `${API_BASE_URL}/suggest_breeding_pairs` && method === "POST") {
             return { ok: true, status: 200, data: getMockBreedingSuggestions() };
        }

        // Default simulation for other endpoints
        return { ok: false, status: 404, error: "Endpoint not found (Simulated)" };
    }

    // --- Analysis Handling ---
    analyzeImageBtn.addEventListener("click", async () => {
        if (!currentImageFile) return;

        resultsSection.style.display = "block";
        loadingIndicator.style.display = "block";
        analysisResults.innerHTML = "";
        visualizationArea.style.display = "none";
        if (currentAnalysisChart) currentAnalysisChart.destroy(); // Clear previous chart
        analyzeImageBtn.disabled = true;
        analyzeImageBtn.innerHTML = 
            `<i class="fas fa-spinner fa-spin"></i> جاري التحليل...`;

        const formData = new FormData();
        formData.append("image", currentImageFile);
        formData.append("analysis_mode", "auto");
        formData.append("analysis_type", "all");

        try {
            // Simulate API call using the helper function
            const response = await simulateApiCall(`${API_BASE_URL}/analyze`, "POST", formData, 2500);

            if (!response.ok) {
                throw new Error(response.error || `HTTP error! status: ${response.status}`);
            }
            
            const results = response.data;
            console.log("Analysis results received:", results);
            displayAnalysisResults(results);
            saveToHistory(currentImageFile.name, results);
            showToast("اكتمل التحليل بنجاح.", "success");

        } catch (error) {
            console.error("Analysis failed:", error);
            analysisResults.innerHTML = 
                `<p class="error-message">فشل التحليل. يرجى المحاولة مرة أخرى. (${error.message})</p>`;
            showToast(`فشل التحليل: ${error.message}`, "error");
        } finally {
            loadingIndicator.style.display = "none";
            analyzeImageBtn.disabled = false;
            analyzeImageBtn.innerHTML = 
                `<i class="fas fa-flask"></i> بدء التحليل`;
        }
    });

    function getMockAnalysisResults() {
        // (Mock data remains the same as previous version)
        return {
            request_id: `req_${Date.now()}`,
            timestamp: new Date().toISOString(),
            image_info: {
                name: currentImageFile?.name || "unknown.jpg",
                size: currentImageFile?.size || 0,
                type: currentImageFile?.type || "image/jpeg"
            },
            analysis_mode_used: "auto",
            comparison: {
                preferred_system: "primitive",
                reason: "Primitive system showed higher confidence in detecting subtle nutrient deficiencies.",
                standard_score: 0.75,
                primitive_score: 0.82
            },
            combined_results: {
                disease_detection: [
                    { id: "D001", name: "لفحة متأخرة (فطري)", confidence: Math.random() * 0.3 + 0.6, type: "fungal", description: "مرض فطري شائع يصيب الطماطم والبطاطس.", symptoms: ["بقع بنية غير منتظمة على الأوراق", "عفن رمادي على الجانب السفلي", "عفن بني داكن على الثمار"], source_system: "primitive" },
                    { id: "D015", name: "فيروس تبرقش التبغ (فيروسي)", confidence: Math.random() * 0.4 + 0.3, type: "viral", description: "فيروس يسبب تبرقش وتشوه الأوراق.", symptoms: ["بقع صفراء وخضراء فاتحة بشكل فسيفسائي", "تجعد وتشوه الأوراق الحديثة"], source_system: "standard" }
                ],
                nutrient_analysis: [
                    { id: "N001", name: "نقص النيتروجين", confidence: Math.random() * 0.3 + 0.5, category: "major", description: "يؤدي إلى اصفرار الأوراق القديمة وضعف النمو.", symptoms: ["اصفرار عام يبدأ من الأوراق السفلية وينتشر للأعلى", "نمو متقزم وسيقان رفيعة"], source_system: "standard" },
                    { id: "N005", name: "نقص الحديد", confidence: Math.random() * 0.2 + 0.75, category: "minor", description: "يسبب اصفرار الأوراق الحديثة مع بقاء العروق خضراء.", symptoms: ["اصفرار حاد بين العروق في الأوراق العلوية (الحديثة)", "قد تصبح الأوراق بيضاء بالكامل في الحالات الشديدة"], source_system: "primitive" }
                ],
                soil_analysis: {
                    color_based_estimation: {
                        color_hex: "#8B4513",
                        estimated_properties: {
                            organic_matter: "متوسط",
                            drainage: "جيد",
                            potential_ph_range: "6.0 - 7.0"
                        },
                        confidence: Math.random() * 0.3 + 0.5,
                        notes: "التقدير يعتمد على اللون فقط وقد لا يكون دقيقًا."
                    }
                }
            },
            treatment_recommendations: [
                {
                    issue_id: "D001", issue_type: "disease", issue_name: "لفحة متأخرة (فطري)", confidence: 0.85,
                    recommended_treatment: { id: "T005", name: "مبيد فطري يحتوي على المانكوزيب والنحاس", type: "fungicide" },
                    dosage: { amount: 2.5, unit: "جم/لتر ماء", application_method: "رش ورقي يغطي السطحين العلوي والسفلي" },
                    timing: { recommended_time: "صباحًا كل 7 أيام عند بدء ظهور الأعراض أو كوقاية", notes: "تجنب الرش أثناء الحر الشديد أو المطر. التزم بفترة الأمان." },
                    alternatives: [{ id: "T012", name: "مبيد فطري يحتوي على أزوكسي ستروبين", type: "fungicide" }]
                },
                {
                    issue_id: "N005", issue_type: "nutrient_deficiency", issue_name: "نقص الحديد", confidence: 0.92,
                    recommended_treatment: { id: "T020", name: "حديد مخلبي (EDDHA أو EDDHSA)", type: "fertilizer" },
                    dosage: { amount: 1, unit: "جم/لتر ماء (رش ورقي) أو 5-10 جم/شجرة (تسميد أرضي)", application_method: "رش ورقي أو مع الري" },
                    timing: { recommended_time: "عند ظهور الأعراض، يكرر كل 2-3 أسابيع حسب الحاجة", notes: "يفضل تطبيقه في الصباح الباكر أو المساء. فعال أكثر في التربة القلوية." }
                }
            ],
            visualization_data: { 
                detections: (
                    (results.combined_results?.disease_detection || []).concat(results.combined_results?.nutrient_analysis || [])
                ).map(d => ({ name: d.name, confidence: d.confidence }))
            }
        };
    }

    function displayAnalysisResults(results) {
        analysisResults.innerHTML = ""; // Clear previous results
        const combined = results.combined_results;
        let contentHtml = "";

        // Display Comparison Info
        if (results.comparison) {
            contentHtml += `
                <div class="result-item comparison-info">
                    <h4><i class="fas fa-balance-scale"></i> مقارنة أنظمة التحليل</h4>
                    <p>النظام المفضل: <strong>${results.comparison.preferred_system === 'primitive' ? 'النظام الأولي (تقسيم)' : 'النظام القياسي'}</strong> (السبب: ${results.comparison.reason || 'غير محدد'})</p>
                </div>
            `;
        }

        // Display Detections (Diseases & Nutrients)
        const detections = (combined.disease_detection || []).concat(combined.nutrient_analysis || []);
        if (detections.length > 0) {
            contentHtml += `<div class="result-item"><h3><i class="fas fa-microscope"></i> التشخيصات المكتشفة</h3>`;
            detections.sort((a, b) => b.confidence - a.confidence); // Sort by confidence
            detections.forEach(d => {
                const typeLabel = d.category ? `عنصر غذائي (${d.category})` : `مرض (${d.type})`;
                contentHtml += `
                    <p>
                        <strong>${d.name} (${typeLabel})</strong> - 
                        ثقة: <span class="confidence confidence-${getConfidenceLevel(d.confidence)}">${(d.confidence * 100).toFixed(1)}%</span><br>
                        <em>${d.description || ''}</em><br>
                        الأعراض: ${d.symptoms ? d.symptoms.join(", ") : 'غير محددة.'}
                    </p>
                `;
            });
            contentHtml += `</div>`;
        }

        // Display Soil Analysis
        if (combined.soil_analysis?.color_based_estimation) {
            const soil = combined.soil_analysis.color_based_estimation;
            contentHtml += `<div class="result-item"><h3><i class="fas fa-mountain"></i> تحليل التربة (حسب اللون)</h3>`;
            contentHtml += `
                <p>
                    اللون المقدر: <span style="display: inline-block; width: 20px; height: 20px; background-color: ${soil.color_hex || '#ccc'}; border: 1px solid #666; vertical-align: middle;"></span> ${soil.color_hex || 'N/A'}<br>
                    الخصائص المقدرة: مادة عضوية (${soil.estimated_properties?.organic_matter || '؟'}), صرف (${soil.estimated_properties?.drainage || '؟'}), حموضة (${soil.estimated_properties?.potential_ph_range || '؟'})<br>
                    ثقة التقدير: <span class="confidence confidence-${getConfidenceLevel(soil.confidence)}">${(soil.confidence * 100).toFixed(1)}%</span><br>
                    <em>${soil.notes || ''}</em>
                </p>
            `;
            contentHtml += `</div>`;
        }

        // Display Treatment Recommendations
        if (results.treatment_recommendations && results.treatment_recommendations.length > 0) {
            contentHtml += `<div class="result-item"><h3><i class="fas fa-prescription-bottle-alt"></i> توصيات العلاج</h3>`;
            results.treatment_recommendations.forEach(t => {
                contentHtml += `
                    <p>
                        <strong>لـ ${t.issue_name}:</strong><br>
                        العلاج: ${t.recommended_treatment.name} (${t.recommended_treatment.type})<br>
                        الجرعة: ${t.dosage.amount} ${t.dosage.unit} (${t.dosage.application_method})<br>
                        التوقيت: ${t.timing.recommended_time} ${t.timing.notes ? ", " + t.timing.notes : ''}<br>
                        ${t.alternatives ? `بدائل: ${t.alternatives.map(alt => alt.name).join(', ')}` : ''}
                    </p>
                `;
            });
            contentHtml += `</div>`;
        }

        if (contentHtml === "") {
            analysisResults.innerHTML = "<p class='placeholder'>لم يتم العثور على مشاكل واضحة أو أن الثقة أقل من الحد المطلوب.</p>";
        } else {
            analysisResults.innerHTML = contentHtml;
        }

        // Display Visualization
        if (results.visualization_data?.detections?.length > 0) {
            visualizationArea.style.display = "block";
            renderAnalysisChart(results.visualization_data.detections);
        } else {
             visualizationArea.style.display = "none";
        }
    }

    function getConfidenceLevel(confidence) {
        if (confidence >= 0.8) return 'high';
        if (confidence >= 0.6) return 'medium';
        return 'low';
    }

    // --- Breeding Handling ---
    breedingPredictionForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const parent1 = parent1Input.value.trim();
        const parent2 = parent2Input.value.trim();

        breedingResults.style.display = "block";
        breedingResults.innerHTML = `<p><i class="fas fa-spinner fa-spin"></i> جاري التنبؤ...</p>`;

        try {
            const response = await simulateApiCall(`${API_BASE_URL}/predict_breeding`, "POST", { parent1, parent2 }, 1500);
            if (!response.ok) throw new Error(response.error || `HTTP error! status: ${response.status}`);
            displayBreedingResults(response.data, "prediction");
            showToast("تم التنبؤ بنتائج التهجين بنجاح.", "success");
        } catch (error) {
            console.error("Breeding prediction failed:", error);
            breedingResults.innerHTML = `<p class="error-message">فشل التنبؤ. (${error.message})</p>`;
            showToast(`فشل التنبؤ: ${error.message}`, "error");
        }
    });

    breedingSuggestionForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const trait = targetTraitInput.value.trim();
        const value = targetValueInput.value.trim();

        breedingResults.style.display = "block";
        breedingResults.innerHTML = `<p><i class="fas fa-spinner fa-spin"></i> جاري البحث عن اقتراحات...</p>`;

        try {
            const response = await simulateApiCall(`${API_BASE_URL}/suggest_breeding_pairs`, "POST", { target_trait: trait, target_value: value }, 2000);
            if (!response.ok) throw new Error(response.error || `HTTP error! status: ${response.status}`);
            displayBreedingResults(response.data, "suggestion");
            showToast("تم العثور على اقتراحات تهجين.", "success");
        } catch (error) {
            console.error("Breeding suggestion failed:", error);
            breedingResults.innerHTML = `<p class="error-message">فشل البحث عن اقتراحات. (${error.message})</p>`;
            showToast(`فشل البحث عن اقتراحات: ${error.message}`, "error");
        }
    });

    function getMockBreedingPrediction() {
        // (Mock data remains the same)
        return {
            predicted_offspring: {
                quantitative_traits: {
                    "الإنتاجية (طن/هكتار)": 125.5,
                    "ارتفاع النبات (سم)": 57.0,
                    "مقاومة الجفاف (مقياس 1-10)": 7.5
                },
                mendelian_traits: {
                    "لون الزهرة": { "أحمر (Rr)": 0.5, "أبيض (rr)": 0.5 },
                    "شكل الورقة": { "عادي (LL)": 0.25, "عادي (Ll)": 0.5, "مجعد (ll)": 0.25 }
                }
            },
            simulation_results: {
                 "quantitative_traits_distribution": {
                    "الإنتاجية (طن/هكتار)": { "mean": 126.1, "std_dev": 12.3, "confidence_interval": [123.5, 128.7] }
                 }
            },
            notes: "التنبؤات تعتمد على النماذج الوراثية وقد تختلف النتائج الفعلية."
        };
    }

    function getMockBreedingSuggestions() {
        // (Mock data remains the same)
        return [
            { parent1: "سلالة الأمل", parent2: "سلالة النور", predicted_value: 135.0, score: 5.0, notes: "مزيج جيد للإنتاجية العالية." },
            { parent1: "سلالة الصحراء", parent2: "سلالة الوادي", predicted_value: 110.0, score: 20.0, notes: "مقاومة جيدة للجفاف." }
        ];
    }

    function displayBreedingResults(results, type) {
        breedingResults.innerHTML = ""; // Clear previous
        let html = `<h3>${type === 'prediction' ? 'نتائج التنبؤ المتوقعة:' : 'أزواج التهجين المقترحة:'}</h3>`;

        if (type === "prediction") {
            // (Display logic remains the same)
             html += "<h4>الصفات الكمية المتوقعة (المتوسط):</h4><ul>";
            for (const [trait, val] of Object.entries(results.predicted_offspring.quantitative_traits)) {
                html += `<li>${trait}: ${val.toFixed(1)}</li>`;
            }
            html += "</ul>";

            html += "<h4>الصفات المندلية المتوقعة (الاحتمالات):</h4><ul>";
            for (const [trait, genotypes] of Object.entries(results.predicted_offspring.mendelian_traits)) {
                html += `<li>${trait}: ${Object.entries(genotypes).map(([g, p]) => `${g} (${(p * 100).toFixed(0)}%)`).join(", ")}</li>`;
            }
            html += "</ul>";
            
            if(results.simulation_results?.quantitative_traits_distribution) {
                 html += "<h4>نتائج المحاكاة (مثال: الإنتاجية):</h4>";
                 const yieldSim = results.simulation_results.quantitative_traits_distribution["الإنتاجية (طن/هكتار)"];
                 if (yieldSim) {
                    html += `<p>المتوسط: ${yieldSim.mean.toFixed(1)}, الانحراف المعياري: ${yieldSim.std_dev.toFixed(1)}, فترة الثقة 95%: [${yieldSim.confidence_interval[0].toFixed(1)} - ${yieldSim.confidence_interval[1].toFixed(1)}]</p>`;
                 }
            }
            if (results.notes) {
                html += `<p><em>ملاحظة: ${results.notes}</em></p>`;
            }
        } else if (type === "suggestion") {
            // (Display logic remains the same)
            if (results.length > 0) {
                html += "<ul>";
                results.forEach(s => {
                    html += `<li><strong>${s.parent1} x ${s.parent2}</strong><br>القيمة المتوقعة للصفة: ${s.predicted_value.toFixed(1)}<br><em>${s.notes || ''}</em></li>`;
                });
                html += "</ul>";
            } else {
                html += "<p>لم يتم العثور على اقتراحات مناسبة للمعايير المحددة.</p>";
            }
        }
        breedingResults.innerHTML = html;
    }

    // --- History Handling (Using Local Storage) ---
    const HISTORY_KEY = "agriculturalAiHistory_v2"; // Use new key if format changes

    function loadHistory() {
        const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
        analysisHistory.innerHTML = "";
        if (history.length === 0) {
            analysisHistory.appendChild(noHistoryMsg);
            clearHistoryBtn.style.display = "none";
        } else {
            noHistoryMsg.style.display = "none";
            history.forEach(item => addHistoryItemToDOM(item));
            clearHistoryBtn.style.display = "inline-flex";
        }
    }

    function saveToHistory(imageName, resultsData) {
        const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
        const timestamp = new Date();
        const historyItem = {
            id: `hist_${timestamp.getTime()}`,
            date: timestamp.toLocaleString('ar-EG'),
            imageName: imageName,
            summary: {
                diseases: resultsData.combined_results?.disease_detection?.map(d => d.name) || [],
                nutrients: resultsData.combined_results?.nutrient_analysis?.map(n => n.name) || [],
                soil: resultsData.combined_results?.soil_analysis?.color_based_estimation ? 'تم تحليل التربة' : null
            },
            // Store full results for retrieval
            fullResults: resultsData 
        };

        history.unshift(historyItem); // Add to the beginning
        const MAX_HISTORY = 20;
        if (history.length > MAX_HISTORY) {
            history.pop();
        }

        try {
            localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
            addHistoryItemToDOM(historyItem, true);
            noHistoryMsg.style.display = "none";
            clearHistoryBtn.style.display = "inline-flex";
        } catch (e) {
            console.error("Failed to save history to localStorage:", e);
            showToast("فشل حفظ السجل، قد تكون مساحة التخزين ممتلئة.", "error");
            // Optionally remove oldest item and try again
            if (e.name === 'QuotaExceededError' && history.length > 0) {
                history.pop(); // Remove oldest
                try {
                    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
                    showToast("تم حذف أقدم سجل لتوفير مساحة.", "warning");
                } catch (e2) { /* Still failed */ }
            }
        }
    }

    function addHistoryItemToDOM(item, prepend = false) {
        const div = document.createElement("div");
        div.className = "history-item";
        div.setAttribute("data-id", item.id);
        const summaryText = [
            ...(item.summary.diseases || []),
            ...(item.summary.nutrients || []),
            item.summary.soil
        ].filter(Boolean).join(', ') || 'لا يوجد';

        div.innerHTML = `
            <p class="history-date">${item.date}</p>
            <p><strong>الصورة:</strong> ${item.imageName}</p>
            <p><strong>الملخص:</strong> ${summaryText}</p>
            <button class="btn btn-sm btn-info view-history-details" aria-label="عرض تفاصيل السجل ${item.id}">عرض التفاصيل</button>
        `;
        
        div.querySelector('.view-history-details').addEventListener('click', () => {
            const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
            const fullItem = history.find(h => h.id === item.id);
            if (fullItem?.fullResults) {
                resultsSection.style.display = 'block';
                displayAnalysisResults(fullItem.fullResults);
                resultsSection.scrollIntoView({ behavior: 'smooth' });
                showToast(`تم عرض تفاصيل السجل لـ ${item.imageName}.`, "info");
            } else {
                showToast("لم يتم العثور على التفاصيل الكاملة لهذا السجل.", "warning");
            }
        });

        if (prepend && analysisHistory.firstChild && analysisHistory.firstChild !== noHistoryMsg) {
            analysisHistory.insertBefore(div, analysisHistory.firstChild);
        } else {
             if (analysisHistory.firstChild === noHistoryMsg) {
                 analysisHistory.removeChild(noHistoryMsg);
             }
            analysisHistory.appendChild(div);
        }
    }

    clearHistoryBtn.addEventListener("click", () => {
        if (confirm("هل أنت متأكد أنك تريد مسح سجل التحليلات بالكامل؟ لا يمكن التراجع عن هذا الإجراء.")) {
            localStorage.removeItem(HISTORY_KEY);
            analysisHistory.innerHTML = "";
            analysisHistory.appendChild(noHistoryMsg);
            noHistoryMsg.style.display = "block";
            clearHistoryBtn.style.display = "none";
            showToast("تم مسح سجل التحليلات.", "info");
        }
    });

    // --- Toast Notifications ---
    function showToast(message, type = "info", duration = 4000) {
        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        toast.setAttribute("role", "alert");
        toast.textContent = message;
        toastContainer.appendChild(toast);
        toast.offsetHeight; // Trigger reflow
        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
            setTimeout(() => toast.remove(), 500);
        }, duration);
    }

    // --- Visualization (using Chart.js) ---
    function setupChartJs() {
        if (!window.Chart) {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            script.async = true;
            document.body.appendChild(script);
            script.onload = () => console.log("Chart.js loaded dynamically.");
            script.onerror = () => console.error("Failed to load Chart.js");
        }
    }

    function renderAnalysisChart(detections) {
        const ctx = document.getElementById('analysisChart')?.getContext('2d');
        if (!ctx || !window.Chart) {
            console.warn("Chart.js library not found or canvas element missing.");
            visualizationArea.innerHTML = `
                <h4><i class="fas fa-chart-bar"></i> تصور النتائج</h4>
                <p class="error-message">لا يمكن عرض الرسم البياني. مكتبة Chart.js غير محملة أو حدث خطأ.</p>`;
            return;
        }

        if (currentAnalysisChart) {
            currentAnalysisChart.destroy(); // Destroy previous chart instance
        }

        const labels = detections.map(d => d.name);
        const dataPoints = detections.map(d => d.confidence * 100);
        const backgroundColors = detections.map(d => {
            const level = getConfidenceLevel(d.confidence);
            if (level === 'high') return 'rgba(40, 167, 69, 0.7)'; // Green
            if (level === 'medium') return 'rgba(255, 193, 7, 0.7)'; // Yellow
            return 'rgba(220, 53, 69, 0.7)'; // Red
        });

        const data = {
            labels: labels,
            datasets: [{
                label: 'مستوى الثقة (%)',
                data: dataPoints,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(c => c.replace('0.7', '1')), // Darker border
                borderWidth: 1
            }]
        };

        currentAnalysisChart = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                indexAxis: 'y', // Horizontal bar chart for better readability with long labels
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'نسبة الثقة (%)'
                        }
                    },
                    y: {
                         ticks: { autoSkip: false } // Ensure all labels are shown
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'مستوى الثقة في التشخيصات المكتشفة'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.x !== null) {
                                    label += context.parsed.x.toFixed(1) + '%';
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }

});

// Add dynamic styles (same as before)
const dynamicStyles = `
.toast-container { position: fixed; bottom: 20px; left: 20px; z-index: 1050; }
.toast { background-color: #333; color: #fff; padding: 15px 20px; border-radius: 8px; margin-bottom: 10px; opacity: 0; transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out; min-width: 250px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); transform: translateX(-100%); }
.toast.show { opacity: 1; transform: translateX(0); }
.toast-success { background-color: #4CAF50; }
.toast-error { background-color: #dc3545; }
.toast-warning { background-color: #ffc107; color: #333; }
.toast-info { background-color: #17a2b8; }
.confidence { font-weight: bold; padding: 2px 5px; border-radius: 4px; color: white; }
.confidence-high { background-color: #28a745; }
.confidence-medium { background-color: #ffc107; color: #333; }
.confidence-low { background-color: #dc3545; }
.error-message { color: #dc3545; font-weight: bold; }
.placeholder { color: #6c757d; font-style: italic; text-align: center; padding: 2rem 0; }
.btn-sm { padding: 0.25rem 0.5rem; font-size: 0.875rem; border-radius: 0.2rem; }
.btn-info { color: #fff; background-color: #17a2b8; border-color: #17a2b8; }
.btn-info:hover { color: #fff; background-color: #138496; border-color: #117a8b; }
.comparison-info { background-color: #e9f5e9; border-left: 5px solid #4CAF50; }
#visualization-area canvas { max-height: 300px; }
`;
const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = dynamicStyles;
document.head.appendChild(styleSheet);

