#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 نسخ احتياطية آمنة ومشفرة
Secure Encrypted Backups
"""

import gzip
import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from cryptography.fernet import Fernet


class SecureBackup:
    """نظام النسخ الاحتياطية الآمنة"""

    def __init__(self):
        self.backup_dir = Path("secure_backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.encryption_key = self.get_or_create_key()

    def get_or_create_key(self):
        """الحصول على مفتاح التشفير أو إنشاؤه"""
        key_file = Path("backup_encryption.key")

        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)
            return key

    def calculate_checksum(self, file_path):
        """حساب checksum للملف"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def compress_and_encrypt(self, source_path, dest_path):
        """ضغط وتشفير الملف"""
        # ضغط الملف
        compressed_path = f"{dest_path}.gz"
        with open(source_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # تشفير الملف المضغوط
        fernet = Fernet(self.encryption_key)
        with open(compressed_path, 'rb') as f:
            encrypted_data = fernet.encrypt(f.read())

        with open(f"{dest_path}.encrypted", 'wb') as f:
            f.write(encrypted_data)

        # حذف الملف المضغوط المؤقت
        os.remove(compressed_path)

        return f"{dest_path}.encrypted"

    def backup_database(self):
        """نسخ احتياطية لقاعدة البيانات"""
        db_path = Path("backend/instance/inventory.db")
        if not db_path.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"database_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name

        # نسخ قاعدة البيانات
        shutil.copy2(db_path, f"{backup_path}.db")

        # ضغط وتشفير
        encrypted_file = self.compress_and_encrypt(f"{backup_path}.db", backup_path)

        # حذف النسخة غير المشفرة
        os.remove(f"{backup_path}.db")

        # حساب checksum
        checksum = self.calculate_checksum(encrypted_file)

        return {
            "file": encrypted_file,
            "checksum": checksum,
            "timestamp": timestamp,
            "type": "database"
        }

    def backup_config_files(self):
        """نسخ احتياطية للملفات التكوين"""
        config_files = [
            "backend/.env",
            "backend/src/security_config.py",
            "admin_credentials.json"
        ]

        backups = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for config_file in config_files:
            if Path(config_file).exists():
                file_name = Path(config_file).name
                backup_name = f"config_{file_name}_{timestamp}"
                backup_path = self.backup_dir / backup_name

                # نسخ الملف
                shutil.copy2(config_file, f"{backup_path}.orig")

                # ضغط وتشفير
                encrypted_file = self.compress_and_encrypt(f"{backup_path}.orig", backup_path)

                # حذف النسخة غير المشفرة
                os.remove(f"{backup_path}.orig")

                # حساب checksum
                checksum = self.calculate_checksum(encrypted_file)

                backups.append({
                    "file": encrypted_file,
                    "checksum": checksum,
                    "original": config_file,
                    "timestamp": timestamp,
                    "type": "config"
                })

        return backups

    def create_backup_manifest(self, backups):
        """إنشاء manifest للنسخ الاحتياطية"""
        manifest = {
            "created": datetime.now().isoformat(),
            "backups": backups,
            "encryption": "Fernet (AES 128)",
            "compression": "gzip",
            "total_files": len(backups)
        }

        manifest_file = self.backup_dir / f"manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        return manifest_file

    def run_full_backup(self):
        """تشغيل نسخة احتياطية كاملة"""
        print("💾 بدء النسخة الاحتياطية الآمنة...")

        all_backups = []

        # نسخ قاعدة البيانات
        db_backup = self.backup_database()
        if db_backup:
            all_backups.append(db_backup)
            print(f"✅ نسخ قاعدة البيانات: {db_backup['file']}")

        # نسخ ملفات التكوين
        config_backups = self.backup_config_files()
        all_backups.extend(config_backups)

        for backup in config_backups:
            print(f"✅ نسخ ملف التكوين: {backup['original']}")

        # إنشاء manifest
        manifest_file = self.create_backup_manifest(all_backups)
        print(f"✅ إنشاء manifest: {manifest_file}")

        print(f"\n🎉 تم إنشاء {len(all_backups)} نسخة احتياطية آمنة")
        print(f"📁 المجلد: {self.backup_dir}")
        print("🔐 مفتاح التشفير: backup_encryption.key")

        return all_backups


if __name__ == "__main__":
    try:
        backup_system = SecureBackup()
        backup_system.run_full_backup()
    except ImportError:
        print("❌ مكتبة cryptography غير متاحة")
        print("تثبيت: pip install cryptography")
    except Exception as e:
        print(f"❌ خطأ في النسخ الاحتياطي: {e}")
        print(f"❌ خطأ في النسخ الاحتياطي: {e}")
