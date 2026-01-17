"""
نظام توثيق API التلقائي
Automatic API Documentation System
"""


import inspect
from flask import Blueprint, jsonify
from functools import wraps


class APIDocumentationGenerator:
    """مولد توثيق API التلقائي"""

    def __init__(self):
        self.endpoints = {}
        self.schemas = {}

    def document_endpoint(
        self, method="GET", description="", parameters=None, responses=None
    ):
        """decorator لتوثيق نقاط النهاية"""

        def decorator(func):
            endpoint_info = {
                "method": method,
                "description": description,
                "function_name": func.__name__,
                "parameters": parameters or {},
                "responses": responses or {},
                "docstring": inspect.getdoc(func),
            }

            # استخراج المسار من decorator الأصلي
            if hasattr(func, "_flask_route_path"):
                endpoint_info["path"] = func._flask_route_path

            self.endpoints[func.__name__] = endpoint_info

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def generate_openapi_spec(self):
        """توليد مواصفات OpenAPI"""
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Complete Inventory Management System API",
                "version": "1.5.0",
                "description": "نظام إدارة المخزون الشامل - واجهة برمجة التطبيقات",
            },
            "servers": [
                {"url": "http://localhost:5001", "description": "خادم التطوير"}
            ],
            "paths": {},
            "components": {
                "schemas": self.schemas,
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                    }
                },
            },
        }

        # إضافة نقاط النهاية
        for endpoint_name, endpoint_info in self.endpoints.items():
            path = endpoint_info.get("path", f"/{endpoint_name}")
            method = endpoint_info["method"].lower()

            if path not in spec["paths"]:
                spec["paths"][path] = {}

            spec["paths"][path][method] = {
                "summary": endpoint_info["description"],
                "description": endpoint_info.get("docstring", ""),
                "parameters": self._format_parameters(endpoint_info["parameters"]),
                "responses": self._format_responses(endpoint_info["responses"]),
            }

        return spec

    def _format_parameters(self, parameters):
        """تنسيق المعاملات لـ OpenAPI"""
        formatted = []
        for param_name, param_info in parameters.items():
            formatted.append(
                {
                    "name": param_name,
                    "in": param_info.get("in", "query"),
                    "description": param_info.get("description", ""),
                    "required": param_info.get("required", False),
                    "schema": {"type": param_info.get("type", "string")},
                }
            )
        return formatted

    def _format_responses(self, responses):
        """تنسيق الاستجابات لـ OpenAPI"""
        formatted = {}
        for status_code, response_info in responses.items():
            formatted[str(status_code)] = {
                "description": response_info.get("description", ""),
                "content": {
                    "application/json": {
                        "schema": response_info.get("schema", {"type": "object"})
                    }
                },
            }

        # إضافة استجابات افتراضية
        if "200" not in formatted:
            formatted["200"] = {
                "description": "نجح الطلب",
                "content": {"application/json": {"schema": {"type": "object"}}},
            }

        return formatted

    def generate_html_documentation(self):
        """توليد توثيق HTML"""
        html_template = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>توثيق API - نظام إدارة المخزون</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        .endpoint { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; }
        .method { display: inline-block; padding: 4px 8px; border-radius: 4px; color: white; font-weight: bold; }
        .get { background: #28a745; }
        .post { background: #007bff; }
        .put { background: #ffc107; color: #212529; }
        .delete { background: #dc3545; }
        .parameters { margin-top: 15px; }
        .parameter { background: white; padding: 10px; margin: 5px 0; border-radius: 4px; }
        code { background: #e9ecef; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 توثيق API - نظام إدارة المخزون الشامل</h1>
        <p><strong>الإصدار:</strong> 1.5.0</p>
        <p><strong>الخادم:</strong> http://localhost:5001</p>

        <h2>📋 نقاط النهاية المتاحة</h2>

        {% for endpoint_name, endpoint_info in endpoints.items() %}
        <div class="endpoint">
            <h3>
                <span class="method {{ endpoint_info.method.lower() }}">{{ endpoint_info.method }}</span>
                <code>{{ endpoint_info.get('path', '/' + endpoint_name) }}</code>
            </h3>
            <p><strong>الوصف:</strong> {{ endpoint_info.description or 'لا يوجد وصف' }}</p>

            {% if endpoint_info.docstring %}
            <p><strong>التفاصيل:</strong> {{ endpoint_info.docstring }}</p>
            {% endif %}

            {% if endpoint_info.parameters %}
            <div class="parameters">
                <h4>المعاملات:</h4>
                {% for param_name, param_info in endpoint_info.parameters.items() %}
                <div class="parameter">
                    <strong>{{ param_name }}</strong>
                    <span style="color: #6c757d;">({{ param_info.get('type', 'string') }})</span>
                    {% if param_info.get('required') %}<span style="color: #dc3545;">*</span>{% endif %}
                    <br>
                    {{ param_info.get('description', 'لا يوجد وصف') }}
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% endfor %}

        <h2>🔐 المصادقة</h2>
        <p>يستخدم النظام JWT للمصادقة. أضف الرمز في header:</p>
        <code>Authorization: Bearer YOUR_JWT_TOKEN</code>

        <h2>📊 أمثلة الاستجابات</h2>
        <div class="endpoint">
            <h4>استجابة ناجحة:</h4>
            <pre><code>{
  "success": true,
  "data": {...},
  "message": "تم بنجاح"
}</code></pre>
        </div>

        <div class="endpoint">
            <h4>استجابة خطأ:</h4>
            <pre><code>{
  "success": false,
  "error": "رسالة الخطأ",
  "code": "ERROR_CODE"
}</code></pre>
        </div>
    </div>
</body>
</html>
        """

        # استخدام string formatting بدلاً من jinja2
        endpoints_html = ""
        for endpoint_name, endpoint_info in self.endpoints.items():
            endpoints_html += f"""
        <div class="endpoint">
            <h3>
                <span class="method {endpoint_info['method'].lower()}">{endpoint_info['method']}</span>
                <code>{endpoint_info.get('path', '/' + endpoint_name)}</code>
            </h3>
            <p><strong>الوصف:</strong> {endpoint_info['description'] or 'لا يوجد وصف'}</p>
        </div>
            """

        return (
            html_template.replace(
                "{% for endpoint_name, endpoint_info in endpoints.items() %}", ""
            )
            .replace("{% endfor %}", "")
            .replace("{{ endpoints_html }}", endpoints_html)
        )


# إنشاء instance عام
api_docs = APIDocumentationGenerator()

# Blueprint للتوثيق
docs_bp = Blueprint("api_docs", __name__)


@docs_bp.route("/api/docs")
def api_documentation():
    """عرض توثيق API"""
    return api_docs.generate_html_documentation()


@docs_bp.route("/api/docs/openapi.json")
def openapi_spec():
    """مواصفات OpenAPI بصيغة JSON"""
    return jsonify(api_docs.generate_openapi_spec())
