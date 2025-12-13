#!/usr/bin/env python3
"""
مولد شهادات SSL وإعداد HTTPS
ملف: ssl_certificate_generator.py
"""

import os
import subprocess
import json
import ipaddress
from pathlib import Path
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class SSLCertificateGenerator:
    """فئة إنشاء وإدارة شهادات SSL"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.ssl_dir = self.base_dir / "ssl"
        self.ssl_dir.mkdir(exist_ok=True)

        self.results = {
            'timestamp': datetime.now().isoformat(),
            'certificates': {},
            'configurations': {},
            'summary': {
                'total_certificates': 0,
                'generated_certificates': 0,
                'failed_certificates': 0
            }
        }

    def log_certificate(self, name, status, message="", details=None):
        """تسجيل نتيجة إنشاء الشهادة"""
        self.results['certificates'][name] = {
            'status': status,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }

        self.results['summary']['total_certificates'] += 1
        if status == 'generated':
            self.results['summary']['generated_certificates'] += 1
            print(f"✅ {name}: {message}")
        elif status == 'failed':
            self.results['summary']['failed_certificates'] += 1
            print(f"❌ {name}: {message}")
        elif status == 'exists':
            print(f"ℹ️ {name}: موجود مسبقاً")

    def generate_private_key(self):
        """إنشاء مفتاح خاص"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        return private_key

    def create_self_signed_certificate(self,
                                       domain_name,
                                       private_key,
                                       validity_days=365):
        """إنشاء شهادة موقعة ذاتياً"""

        # إنشاء الموضوع
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "EG"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Cairo"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Cairo"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME,
                               "Inventory Management System"),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME,
                               "IT Department"),
            x509.NameAttribute(NameOID.COMMON_NAME, domain_name),
        ])

        # إنشاء الشهادة
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(domain_name),
                x509.DNSName(f"*.{domain_name}"),
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
                x509.DNSName("172.16.16.27"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                x509.IPAddress(ipaddress.IPv4Address("172.16.16.27")),
            ]),
            critical=False,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                data_encipherment=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
                x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH,
            ]),
            critical=True,
        ).sign(private_key, hashes.SHA256())

        return cert

    def save_certificate_files(self, name, private_key, certificate):
        """حفظ ملفات الشهادة"""

        # حفظ المفتاح الخاص
        key_path = self.ssl_dir / f"{name}.key"
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # حفظ الشهادة
        cert_path = self.ssl_dir / f"{name}.crt"
        with open(cert_path, "wb") as f:
            f.write(certificate.public_bytes(serialization.Encoding.PEM))

        # حفظ الشهادة والمفتاح معاً (للـ nginx)
        pem_path = self.ssl_dir / f"{name}.pem"
        with open(pem_path, "wb") as f:
            f.write(certificate.public_bytes(serialization.Encoding.PEM))
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        return {
            'key_path': str(key_path),
            'cert_path': str(cert_path),
            'pem_path': str(pem_path)
        }

    def generate_ca_certificate(self):
        """إنشاء شهادة CA (Certificate Authority)"""
        print("\n🔐 إنشاء شهادة CA...")

        try:
            # إنشاء مفتاح خاص للـ CA
            ca_private_key = self.generate_private_key()

            # إنشاء شهادة CA
            ca_subject = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "EG"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Cairo"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "Cairo"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME,
                                   "Inventory Management CA"),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME,
                                   "Certificate Authority"),
                x509.NameAttribute(NameOID.COMMON_NAME,
                                   "Inventory Management Root CA"),
            ])

            ca_cert = x509.CertificateBuilder().subject_name(
                ca_subject
            ).issuer_name(
                ca_subject  # Self-signed
            ).public_key(
                ca_private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=3650)  # 10 سنوات
            ).add_extension(
                x509.BasicConstraints(ca=True, path_length=None),
                critical=True,
            ).add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_encipherment=False,
                    key_agreement=False,
                    key_cert_sign=True,
                    crl_sign=True,
                    content_commitment=False,
                    data_encipherment=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            ).sign(ca_private_key, hashes.SHA256())

            # حفظ ملفات CA
            paths = self.save_certificate_files("ca", ca_private_key, ca_cert)

            self.log_certificate("CA Certificate", "generated",
                                 "شهادة CA تم إنشاؤها بنجاح", paths)

            return ca_private_key, ca_cert

        except Exception as e:
            self.log_certificate("CA Certificate", "failed", str(e))
            return None, None

    def generate_server_certificates(self):
        """إنشاء شهادات الخادم"""
        print("\n🌐 إنشاء شهادات الخادم...")

        # قائمة الخوادم المطلوب إنشاء شهادات لها
        servers = [
            {
                'name': 'backend',
                'domain': 'inventory-backend.local',
                'description': 'شهادة الواجهة الخلفية'
            },
            {
                'name': 'frontend',
                'domain': 'inventory-frontend.local',
                'description': 'شهادة الواجهة الأمامية'
            },
            {
                'name': 'api',
                'domain': 'api.inventory.local',
                'description': 'شهادة API'
            },
            {
                'name': 'nginx',
                'domain': 'inventory.local',
                'description': 'شهادة Nginx Proxy'
            }
        ]

        for server in servers:
            try:
                # إنشاء مفتاح خاص
                private_key = self.generate_private_key()

                # إنشاء شهادة
                certificate = self.create_self_signed_certificate(
                    server['domain'],
                    private_key,
                    validity_days=365
                )

                # حفظ الملفات
                paths = self.save_certificate_files(server['name'],
                                                    private_key,
                                                    certificate)

                self.log_certificate(
                    f"{server['name']} Certificate",
                    "generated",
                    server['description'],
                    {
                        'domain': server['domain'],
                        'paths': paths
                    }
                )

            except Exception as e:
                self.log_certificate(f"{server['name']} Certificate",
                                     "failed",
                                     str(e))

    def create_nginx_ssl_config(self):
        """إنشاء تكوين SSL لـ Nginx"""
        print("\n⚙️ إنشاء تكوين SSL لـ Nginx...")

        nginx_ssl_config = """
# تكوين SSL لـ Nginx - نظام إدارة المخزون
ssl_certificate {self.ssl_dir}/nginx.crt;
ssl_certificate_key {self.ssl_dir}/nginx.key;

# إعدادات SSL المتقدمة
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384;
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# HSTS (HTTP Strict Transport Security)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# إعدادات أمان إضافية
add_header X-Frame-Options DENY always;
add_header X-Content-Type-Options nosniff always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
"""

        ssl_config_path = self.ssl_dir / "nginx_ssl.conf"
        with open(ssl_config_path, 'w', encoding='utf-8') as f:
            f.write(nginx_ssl_config)

        self.results['configurations']['nginx_ssl'] = {
            'path': str(ssl_config_path),
            'status': 'created'
        }

        print(f"✅ تكوين SSL لـ Nginx: {ssl_config_path}")

    def create_backend_ssl_config(self):
        """إنشاء تكوين SSL للـ Backend"""
        print("\n🔧 إنشاء تكوين SSL للـ Backend...")

        backend_ssl_config = {
            'SSL_ENABLED': True,
            'SSL_CERT_PATH': str(self.ssl_dir / "backend.crt"),
            'SSL_KEY_PATH': str(self.ssl_dir / "backend.key"),
            'SSL_PROTOCOLS': ['TLSv1.2', 'TLSv1.3'],
            'SSL_CIPHERS': [
                'ECDHE-RSA-AES128-GCM-SHA256',
                'ECDHE-RSA-AES256-GCM-SHA384',
                'ECDHE-RSA-AES128-SHA256',
                'ECDHE-RSA-AES256-SHA384'
            ],
            'FORCE_HTTPS': True,
            'HSTS_MAX_AGE': 31536000,
            'SECURE_COOKIES': True
        }

        ssl_config_path = self.ssl_dir / "backend_ssl_config.json"
        with open(ssl_config_path, 'w', encoding='utf-8') as f:
            json.dump(backend_ssl_config, f, indent=2, ensure_ascii=False)

        self.results['configurations']['backend_ssl'] = {
            'path': str(ssl_config_path),
            'config': backend_ssl_config,
            'status': 'created'
        }

        print(f"✅ تكوين SSL للـ Backend: {ssl_config_path}")

    def create_docker_ssl_config(self):
        """إنشاء تكوين SSL لـ Docker"""
        print("\n🐳 إنشاء تكوين SSL لـ Docker...")

        # إنشاء مجلد SSL في nginx
        nginx_ssl_dir = self.base_dir / "nginx" / "ssl"
        nginx_ssl_dir.mkdir(parents=True, exist_ok=True)

        # نسخ الشهادات إلى مجلد nginx
        import shutil

        ssl_files = ['nginx.crt', 'nginx.key', 'nginx.pem']
        for ssl_file in ssl_files:
            src = self.ssl_dir / ssl_file
            dst = nginx_ssl_dir / ssl_file
            if src.exists():
                shutil.copy2(src, dst)

        # إنشاء تكوين nginx مع SSL
        nginx_ssl_conf = """
# تكوين Nginx مع SSL
events {{
    worker_connections 1024;
}}

http {{
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # إعدادات SSL
    include /etc/nginx/ssl/nginx_ssl.conf;

    # إعادة توجيه HTTP إلى HTTPS
    server {{
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }}

    # خادم HTTPS
    server {{
        listen 443 ssl http2;
        server_name inventory.local localhost;

        # شهادات SSL
        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;

        # إعدادات SSL
        include /etc/nginx/ssl/nginx_ssl.conf;

        # Proxy للـ Frontend
        location / {{
            proxy_pass http://frontend:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}

        # Proxy للـ Backend API
        location /api/ {{
            proxy_pass https://backend:8443/api/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # SSL للـ Backend
            proxy_ssl_verify off;
            proxy_ssl_session_reuse on;
        }}
    }}
}}
"""

        nginx_conf_path = nginx_ssl_dir.parent / "nginx_ssl.conf"
        with open(nginx_conf_path, 'w', encoding='utf-8') as f:
            f.write(nginx_ssl_conf)

        self.results['configurations']['docker_ssl'] = {
            'nginx_ssl_dir': str(nginx_ssl_dir),
            'nginx_con': str(nginx_conf_path),
            'status': 'created'
        }

        print(f"✅ تكوين SSL لـ Docker: {nginx_ssl_dir}")

    def generate_all_certificates(self):
        """إنشاء جميع الشهادات والتكوينات"""
        print("🔐 === بدء إنشاء شهادات SSL ===")
        print(f"⏰ التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 مجلد SSL: {self.ssl_dir}")

        # إضافة import مطلوب
        import ipaddress

        # إنشاء شهادة CA
        ca_key, ca_cert = self.generate_ca_certificate()

        # إنشاء شهادات الخوادم
        self.generate_server_certificates()

        # إنشاء التكوينات
        self.create_nginx_ssl_config()
        self.create_backend_ssl_config()
        self.create_docker_ssl_config()

        # عرض النتائج
        self.print_summary()

        # حفظ النتائج
        self.save_results()

        return self.results

    def print_summary(self):
        """عرض ملخص النتائج"""
        print("\n📊 === ملخص إنشاء شهادات SSL ===")
        summary = self.results['summary']

        print(f"إجمالي الشهادات: {summary['total_certificates']}")
        print(f"تم إنشاؤها: {summary['generated_certificates']}")
        print(f"فشلت: {summary['failed_certificates']}")

        if summary['total_certificates'] > 0:
            success_rate = (summary['generated_certificates'] / summary['total_certificates']) * 100
            print(f"معدل النجاح: {success_rate:.1f}%")

            if success_rate >= 90:
                print("🎉 تم إنشاء جميع الشهادات بنجاح!")
            elif success_rate >= 70:
                print("✅ تم إنشاء معظم الشهادات")
            else:
                print("⚠️ فشل في إنشاء عدة شهادات")

        # عرض الملفات المُنشأة
        print(f"\n📁 الملفات في {self.ssl_dir}:")
        if self.ssl_dir.exists():
            for file in self.ssl_dir.iterdir():
                if file.is_file():
                    print(f"  📄 {file.name}")

    def save_results(self):
        """حفظ النتائج"""
        results_file = self.base_dir / "ssl_generation_results.json"
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"\n💾 تم حفظ النتائج في: {results_file}")
        except Exception as e:
            print(f"❌ خطأ في حفظ النتائج: {e}")


def main():
    """الدالة الرئيسية"""
    generator = SSLCertificateGenerator()
    results = generator.generate_all_certificates()

    if results['summary']['failed_certificates'] == 0:
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
