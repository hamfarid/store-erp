# File: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/api_client.js
/**
 * مسار الملف: /home/ubuntu/clean_project/src/web_interface/admin_panel/static/js/api_client.js
 * 
 * عميل API موحد للواجهة الأمامية
 * يوفر وظائف للتفاعل مع واجهات برمجة التطبيقات الخلفية
 */

class APIClient {
    constructor() {
        this.baseURL = '/api';
        this.token = localStorage.getItem('auth_token');
    }

    // إعداد الرؤوس الافتراضية
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        return headers;
    }

    // طلب HTTP عام
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getHeaders(),
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // طلبات GET
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    // طلبات POST
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // طلبات PUT
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // طلبات DELETE
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }

    // === واجهات المصادقة ===
    async login(username, password) {
        try {
            const response = await this.post('/auth/login', {
                username,
                password
            });
            
            if (response.access_token) {
                this.token = response.access_token;
                localStorage.setItem('auth_token', this.token);
            }
            
            return response;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    async getCurrentUser() {
        return this.get('/auth/me');
    }

    logout() {
        this.token = null;
        localStorage.removeItem('auth_token');
    }

    // === واجهات الذكاء الاصطناعي ===
    async getAIInfo() {
        return this.get('/ai-service/info');
    }

    async getAIAgents() {
        return this.get('/ai-service/agents');
    }

    async createAIAgent(agentData) {
        return this.post('/ai-service/agents', agentData);
    }

    // === واجهات تشخيص الأمراض ===
    async getCrops() {
        return this.get('/disease-diagnosis/crops');
    }

    async getDiseases() {
        return this.get('/disease-diagnosis/diseases');
    }

    async diagnosePlant(imageFile, cropId) {
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('crop_id', cropId);

        return this.request('/disease-diagnosis/diagnose', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': this.token ? `Bearer ${this.token}` : undefined
            }
        });
    }

    // === واجهات سجل النشاط ===
    async getActivityLogs(limit = 50) {
        return this.get(`/activity-log/logs?limit=${limit}`);
    }

    async createActivityLog(logData) {
        return this.post('/activity-log/logs', logData);
    }

    // === واجهات النظام ===
    async getSystemHealth() {
        return this.get('/health');
    }

    async getSystemInfo() {
        return this.get('/info');
    }
}

// إنشاء مثيل عام للعميل
const apiClient = new APIClient();

// تصدير للاستخدام في ملفات أخرى
window.apiClient = apiClient;

