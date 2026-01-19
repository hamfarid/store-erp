"""
إعداد السجلات - تكوين نظام السجلات للتطبيق
Logging Configuration - Setup logging system for the application
"""

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path


def setup_logging(
        log_level: str = "INFO",
        log_file: str = "./logs/gaara_scan_ai.log"):
    """
    إعداد نظام السجلات
    Setup logging system

    Args:
        log_level: مستوى السجلات
        log_file: مسار ملف السجلات
    """

    # إنشاء مجلد السجلات إذا لم يكن موجوداً
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # تكوين التنسيق
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # إعداد السجل الجذر
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # إزالة المعالجات الموجودة
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # معالج وحدة التحكم
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # معالج الملف مع التدوير
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(getattr(logging, log_level.upper()))
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # تسجيل بداية التشغيل
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("[START] بدء تشغيل نظام Gaara Scan AI")
    logger.info(
        f"📅 التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"[INFO] مستوى السجلات: {log_level}")
    logger.info(f"📁 ملف السجلات: {log_file}")
    logger.info("=" * 50)
