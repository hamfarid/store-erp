"""
#!/usr/bin/env python3

خادم HTTPS آمن للواجهة الخلفية
ملف: https_server.py
"""

import os
import ssl
import json
import logging
import time
from collections import defaultdict
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix


class HTTPSServer:
    """فئة خادم HTTPS آمن"""

    def __init__(self, app):
        self.app = app
        self.base_dir = Path(__file__).parent.parent.parent
        self.ssl_dir = self.base_dir / "ssl"
        self.config = self.load_ssl_config()

        # إعداد الخادم الآمن
        self.setup_ssl_context()
        self.setup_security_headers()
        self.setup_secure_session()

    def load_ssl_config(self):
        """تحميل تكوين SSL"""
        config_file = self.ssl_dir / "backend_ssl_config.json"

        default_config = {
            "SSL_ENABLED": True,
            "SSL_CERT_PATH": str(self.ssl_dir / "backend.crt"),
            "SSL_KEY_PATH": str(self.ssl_dir / "backend.key"),
            "SSL_PROTOCOLS": ["TLSv1.2", "TLSv1.3"],
            "FORCE_HTTPS": True,
            "HSTS_MAX_AGE": 31536000,
            "SECURE_COOKIES": True,
        }

        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                return {**default_config, **config}
            except (OSError, json.JSONDecodeError) as e:
                print(f"⚠️ خطأ في تحميل تكوين SSL: {e}")
                return default_config

        return default_config

    def setup_ssl_context(self):
        """إعداد سياق SSL"""
        if not self.config["SSL_ENABLED"]:
            self.ssl_context = None
            return

        try:
            # إنشاء سياق SSL
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

            # تحديد البروتوكولات المدعومة
            self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
            self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3

            # تحديد الخوارزميات المدعومة
            self.ssl_context.set_ciphers(
                ":".join(
                    [
                        "ECDHE+AESGCM",
                        "ECDHE+CHACHA20",
                        "DHE+AESGCM",
                        "DHE+CHACHA20",
                        "!aNULL",
                        "!MD5",
                        "!DSS",
                    ]
                )
            )

            # تحميل الشهادة والمفتاح
            cert_path = Path(self.config["SSL_CERT_PATH"])
            key_path = Path(self.config["SSL_KEY_PATH"])

            if cert_path.exists() and key_path.exists():
                self.ssl_context.load_cert_chain(
                    certfile=str(cert_path), keyfile=str(key_path)
                )
                print(f"✅ تم تحميل شهادة SSL: {cert_path}")
            else:
                print(f"❌ ملفات SSL غير موجودة: {cert_path}, {key_path}")
                self.ssl_context = None

        except (OSError, ValueError) as e:
            print(f"❌ خطأ في إعداد SSL: {e}")
            self.ssl_context = None

    def setup_security_headers(self):
        """إعداد رؤوس الأمان"""

        @self.app.after_request
        def add_security_headers(response):
            """إضافة رؤوس الأمان لجميع الاستجابات"""

            # HTTPS Strict Transport Security
            if self.config["FORCE_HTTPS"]:
                hsts_value = (
                    f"max-age={self.config['HSTS_MAX_AGE']}; "
                    "includeSubDomains; preload"
                )
                response.headers["Strict-Transport-Security"] = hsts_value

            # منع تضمين الصفحة في إطارات
            response.headers["X-Frame-Options"] = "DENY"

            # منع تخمين نوع المحتوى
            response.headers["X-Content-Type-Options"] = "nosniff"

            # حماية من XSS
            response.headers["X-XSS-Protection"] = "1; mode=block"

            # سياسة المرجع
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

            # سياسة أمان المحتوى
            csp_policy = [
                "default-src 'self'",
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
                "style-src 'self' 'unsafe-inline'",
                "img-src 'self' data: https:",
                "font-src 'self'",
                "connect-src 'self' https:",
                "frame-ancestors 'none'",
                "base-uri 'self'",
                "form-action 'self'",
            ]
            response.headers["Content-Security-Policy"] = "; ".join(csp_policy)

            # إزالة رؤوس الخادم الحساسة
            response.headers.pop("Server", None)
            response.headers.pop("X-Powered-By", None)

            return response

    def setup_secure_session(self):
        """إعداد جلسة آمنة"""

        # تكوين الجلسة الآمنة
        self.app.config.update(
            {
                "SESSION_COOKIE_SECURE": self.config["SECURE_COOKIES"],
                "SESSION_COOKIE_HTTPONLY": True,
                "SESSION_COOKIE_SAMESITE": "Lax",
                "PERMANENT_SESSION_LIFETIME": 3600,  # ساعة واحدة
                "SESSION_COOKIE_NAME": "inventory_session",
            }
        )

        # إعداد مفتاح سري قوي
        if not self.app.config.get("SECRET_KEY"):
            self.app.config["SECRET_KEY"] = os.urandom(32).hex()

    def force_https_redirect(self):
        """إجبار إعادة التوجيه إلى HTTPS"""

        @self.app.before_request
        def force_https():
            """إعادة توجيه HTTP إلى HTTPS"""
            if self.config["FORCE_HTTPS"] and not request.is_secure:
                if request.headers.get("X-Forwarded-Proto") != "https":
                    return (
                        jsonify(
                            {
                                "error": "HTTPS Required",
                                "message": "يجب استخدام HTTPS للوصول إلى هذا الخادم",
                                "redirect_url": request.url.replace(
                                    "http://", "https://"
                                ),
                            }
                        ),
                        426,
                    )  # Upgrade Required
            return None

    def setup_rate_limiting(self):
        """إعداد تحديد معدل الطلبات"""

        # تخزين مؤقت لمعدل الطلبات
        request_counts = defaultdict(list)

        @self.app.before_request
        def rate_limit():
            """تحديد معدل الطلبات"""
            client_ip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)
            current_time = time.time()

            # تنظيف الطلبات القديمة (أكثر من دقيقة)
            request_counts[client_ip] = [
                req_time
                for req_time in request_counts[client_ip]
                if current_time - req_time < 60
            ]

            # فحص عدد الطلبات
            if len(request_counts[client_ip]) >= 100:  # 100 طلب في الدقيقة
                return (
                    jsonify(
                        {
                            "error": "Rate Limit Exceeded",
                            "message": "تم تجاوز الحد المسموح من الطلبات",
                        }
                    ),
                    429,
                )

            # إضافة الطلب الحالي
            request_counts[client_ip].append(current_time)
            return None

    def setup_request_logging(self):
        """إعداد تسجيل الطلبات"""

        # إعداد نظام التسجيل
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("logs/https_server.log"),
                logging.StreamHandler(),
            ],
        )

        logger = logging.getLogger("https_server")

        @self.app.before_request
        def log_request():
            """تسجيل الطلبات"""
            logger.info(
                "Request: %s %s from %s",
                request.method,
                request.url,
                request.remote_addr,
            )

        @self.app.after_request
        def log_response(response):
            """تسجيل الاستجابات"""
            logger.info(
                "Response: %s for %s %s",
                response.status_code,
                request.method,
                request.url,
            )
            return response

    def run_server(self, host="172.16.16.27", port=8443, debug=False):
        """تشغيل الخادم الآمن"""

        # إعداد الميزات الأمنية
        self.force_https_redirect()
        self.setup_rate_limiting()
        self.setup_request_logging()

        # إعداد ProxyFix للعمل خلف reverse proxy
        self.app.wsgi_app = ProxyFix(
            self.app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

        print("🚀 بدء تشغيل خادم HTTPS الآمن...")
        print(f"🔗 العنوان: https://{host}:{port}")
        print(f"🔐 SSL: {'مُفعل' if self.ssl_context else 'معطل'}")
        print("🛡️ الأمان: مُفعل")

        try:
            if self.ssl_context:
                # تشغيل مع SSL
                self.app.run(
                    host=host,
                    port=port,
                    debug=debug,
                    ssl_context=self.ssl_context,
                    threaded=True,
                )
            else:
                print("⚠️ تحذير: يتم التشغيل بدون SSL")
                self.app.run(host=host, port=port, debug=debug, threaded=True)

        except (OSError, RuntimeError) as e:
            print(f"❌ خطأ في تشغيل الخادم: {e}")
            raise


def create_https_app():
    """إنشاء تطبيق Flask آمن"""

    # استيراد التطبيق الأساسي
    try:
        from main import app  # pylint: disable=import-outside-toplevel
    except ImportError:
        # إنشاء تطبيق أساسي إذا لم يكن موجوداً
        app = Flask(__name__)

        @app.route("/api/health")
        def health_check():
            return jsonify(
                {
                    "status": "healthy",
                    "ssl_enabled": True,
                    "timestamp": datetime.now().isoformat(),
                }
            )

    # إنشاء خادم HTTPS
    https_server = HTTPSServer(app)

    return app, https_server


def main():
    """الدالة الرئيسية"""
    _, https_server = create_https_app()

    # تشغيل الخادم
    https_server.run_server(
        host=os.environ.get("BACKEND_HOST", "172.16.16.27"),
        port=int(os.environ.get("BACKEND_HTTPS_PORT", 8443)),
        debug=os.environ.get("FLASK_DEBUG", "False").lower() == "true",
    )


if __name__ == "__main__":
    main()
