#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
الملف الرئيسي لنظام Gaara ERP
"""

import os
import logging
import argparse
from dotenv import load_dotenv

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة
load_dotenv()

def initialize_system():
    """تهيئة النظام وإعداد المكونات الأساسية"""
    try:
        logger.info("بدء تهيئة نظام Gaara ERP")
        
        # استيراد مديري النظام الأساسيين
        from src.core.database.db_manager import DatabaseManager
        from src.core.config.config_manager import ConfigManager
        from src.core.auth.auth_manager import AuthManager
        from src.core.i18n.i18n_manager import I18nManager
        from src.core.integration.integration_manager import IntegrationManager
        
        # تهيئة مدير قاعدة البيانات
        logger.info("تهيئة مدير قاعدة البيانات")
        db_manager = DatabaseManager()
        
        # تهيئة قاعدة البيانات إذا لزم الأمر
        if os.getenv('INITIALIZE_DB', 'false').lower() == 'true':
            script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'database_init.sql')
            db_manager.initialize_database(script_path)
        
        # تهيئة مدير التكوين
        logger.info("تهيئة مدير التكوين")
        config_manager = ConfigManager()
        
        # تهيئة مدير المصادقة
        logger.info("تهيئة مدير المصادقة")
        auth_manager = AuthManager()
        
        # تهيئة مدير تعدد اللغات
        logger.info("تهيئة مدير تعدد اللغات")
        i18n_manager = I18nManager()
        
        # تهيئة مدير التكامل
        logger.info("تهيئة مدير التكامل")
        integration_manager = IntegrationManager()
        
        logger.info("تم تهيئة نظام Gaara ERP بنجاح")
        return True
    except Exception as e:
        logger.error(f"فشل في تهيئة النظام: {str(e)}")
        return False

def start_api_server():
    """بدء تشغيل خادم واجهة برمجة التطبيقات"""
    try:
        logger.info("بدء تشغيل خادم واجهة برمجة التطبيقات")
        
        # استيراد وتهيئة خادم واجهة برمجة التطبيقات
        # هذا مجرد مثال، يجب تعديله حسب إطار العمل المستخدم
        # مثال: from src.api.server import start_server
        # start_server()
        
        logger.info("تم بدء تشغيل خادم واجهة برمجة التطبيقات بنجاح")
        return True
    except Exception as e:
        logger.error(f"فشل في بدء تشغيل خادم واجهة برمجة التطبيقات: {str(e)}")
        return False

def start_web_server():
    """بدء تشغيل خادم الويب"""
    try:
        logger.info("بدء تشغيل خادم الويب")
        
        # استيراد وتهيئة خادم الويب
        # هذا مجرد مثال، يجب تعديله حسب إطار العمل المستخدم
        # مثال: from src.web.server import start_server
        # start_server()
        
        logger.info("تم بدء تشغيل خادم الويب بنجاح")
        return True
    except Exception as e:
        logger.error(f"فشل في بدء تشغيل خادم الويب: {str(e)}")
        return False

def main():
    """الدالة الرئيسية للنظام"""
    parser = argparse.ArgumentParser(description='نظام Gaara ERP')
    parser.add_argument('--init-db', action='store_true', help='تهيئة قاعدة البيانات')
    parser.add_argument('--api-only', action='store_true', help='تشغيل خادم واجهة برمجة التطبيقات فقط')
    parser.add_argument('--web-only', action='store_true', help='تشغيل خادم الويب فقط')
    args = parser.parse_args()
    
    # تعيين متغير البيئة لتهيئة قاعدة البيانات
    if args.init_db:
        os.environ['INITIALIZE_DB'] = 'true'
    
    # تهيئة النظام
    if not initialize_system():
        logger.error("فشل في تهيئة النظام، إيقاف التشغيل")
        return
    
    # بدء تشغيل الخوادم
    if args.api_only:
        start_api_server()
    elif args.web_only:
        start_web_server()
    else:
        start_api_server()
        start_web_server()

if __name__ == "__main__":
    main()
