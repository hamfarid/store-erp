#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة دعم تعدد اللغات لنظام Gaara ERP
"""

import os
import logging
import json
import gettext
from functools import lru_cache

# إعداد التسجيل
logger = logging.getLogger(__name__)

class I18nManager:
    """مدير تعدد اللغات لنظام Gaara ERP"""
    
    _instance = None
    
    def __new__(cls):
        """تنفيذ نمط Singleton لضمان وجود نسخة واحدة فقط من مدير تعدد اللغات"""
        if cls._instance is None:
            cls._instance = super(I18nManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """تهيئة مدير تعدد اللغات"""
        if self._initialized:
            return
            
        from .config.config_manager import ConfigManager
        from .database.db_manager import DatabaseManager
        
        # الحصول على مدير التكوين وقاعدة البيانات
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        
        # إعدادات تعدد اللغات
        self.default_language = self.config_manager.get('i18n.default_language', 'ar')
        self.available_languages = self.config_manager.get('i18n.available_languages', ['ar', 'en'])
        self.rtl_languages = self.config_manager.get('i18n.rtl_languages', ['ar'])
        
        # مسار ملفات الترجمة
        self.locale_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'locale')
        
        # قاموس الترجمات المحملة
        self.translations = {}
        
        # تحميل الترجمات
        self._load_translations()
        
        self._initialized = True
        logger.info("تم تهيئة مدير تعدد اللغات بنجاح")
    
    def _load_translations(self):
        """تحميل الترجمات من قاعدة البيانات وملفات الترجمة"""
        try:
            # تحميل الترجمات من قاعدة البيانات
            for language_code in self.available_languages:
                self.translations[language_code] = self._load_db_translations(language_code)
            
            # تحميل ملفات الترجمة
            for language_code in self.available_languages:
                self._load_file_translations(language_code)
            
            logger.info("تم تحميل الترجمات بنجاح")
        except Exception as e:
            logger.error(f"فشل في تحميل الترجمات: {str(e)}")
    
    def _load_db_translations(self, language_code):
        """تحميل الترجمات من قاعدة البيانات للغة المحددة"""
        try:
            query = """
                SELECT translation_key, translation_value
                FROM erp.translations
                WHERE language_code = %s
            """
            result = self.db_manager.execute_query(query, (language_code,))
            
            translations = {}
            for row in result:
                translations[row['translation_key']] = row['translation_value']
            
            logger.info(f"تم تحميل {len(translations)} ترجمة من قاعدة البيانات للغة {language_code}")
            return translations
        except Exception as e:
            logger.error(f"فشل في تحميل الترجمات من قاعدة البيانات للغة {language_code}: {str(e)}")
            return {}
    
    def _load_file_translations(self, language_code):
        """تحميل ملفات الترجمة للغة المحددة"""
        try:
            # التحقق من وجود دليل اللغة
            locale_path = os.path.join(self.locale_dir, language_code, 'LC_MESSAGES')
            if not os.path.exists(locale_path):
                os.makedirs(locale_path, exist_ok=True)
            
            # مسار ملف الترجمة
            mo_file = os.path.join(locale_path, 'messages.mo')
            
            # التحقق من وجود ملف الترجمة
            if os.path.exists(mo_file):
                # تحميل ملف الترجمة
                translation = gettext.translation('messages', self.locale_dir, languages=[language_code])
                
                # دمج الترجمات من الملف مع الترجمات من قاعدة البيانات
                file_translations = translation._catalog
                for key, value in file_translations.items():
                    if isinstance(key, str) and key not in self.translations[language_code]:
                        self.translations[language_code][key] = value
                
                logger.info(f"تم تحميل ملف الترجمة للغة {language_code}")
            else:
                logger.warning(f"ملف الترجمة غير موجود للغة {language_code}: {mo_file}")
        except Exception as e:
            logger.error(f"فشل في تحميل ملف الترجمة للغة {language_code}: {str(e)}")
    
    def translate(self, key, language_code=None, default=None, **kwargs):
        """ترجمة النص إلى اللغة المحددة"""
        if language_code is None:
            language_code = self.default_language
        
        if language_code not in self.available_languages:
            language_code = self.default_language
        
        # البحث عن الترجمة
        translation = self.translations.get(language_code, {}).get(key)
        
        if translation is None:
            # إذا لم يتم العثور على الترجمة، استخدم القيمة الافتراضية أو المفتاح
            translation = default if default is not None else key
            
            # تسجيل المفتاح المفقود
            logger.debug(f"مفتاح الترجمة غير موجود: {key} للغة {language_code}")
        
        # استبدال المتغيرات في النص
        if kwargs and translation:
            try:
                translation = translation.format(**kwargs)
            except KeyError as e:
                logger.warning(f"متغير مفقود في نص الترجمة: {str(e)}")
        
        return translation
    
    def get_language_direction(self, language_code=None):
        """الحصول على اتجاه اللغة (RTL أو LTR)"""
        if language_code is None:
            language_code = self.default_language
        
        return 'rtl' if language_code in self.rtl_languages else 'ltr'
    
    def get_available_languages(self):
        """الحصول على قائمة اللغات المتاحة"""
        try:
            query = """
                SELECT language_code, language_name, is_active, is_rtl
                FROM erp.languages
                WHERE is_active = TRUE
                ORDER BY language_name
            """
            return self.db_manager.execute_query(query)
        except Exception as e:
            logger.error(f"فشل في الحصول على اللغات المتاحة: {str(e)}")
            return []
    
    def add_translation(self, language_code, key, value, module=None):
        """إضافة ترجمة جديدة إلى قاعدة البيانات"""
        try:
            # التحقق من وجود الترجمة
            query = """
                SELECT translation_id
                FROM erp.translations
                WHERE language_code = %s AND translation_key = %s
            """
            result = self.db_manager.execute_query(query, (language_code, key))
            
            if result:
                # تحديث الترجمة الموجودة
                update_query = """
                    UPDATE erp.translations
                    SET translation_value = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE language_code = %s AND translation_key = %s
                """
                self.db_manager.execute_query(update_query, (value, language_code, key), fetch=False)
            else:
                # إضافة ترجمة جديدة
                insert_query = """
                    INSERT INTO erp.translations
                    (language_code, translation_key, translation_value, module)
                    VALUES (%s, %s, %s, %s)
                """
                self.db_manager.execute_query(insert_query, (language_code, key, value, module), fetch=False)
            
            # تحديث الترجمات المحملة
            if language_code in self.translations:
                self.translations[language_code][key] = value
            else:
                self.translations[language_code] = {key: value}
            
            logger.info(f"تم إضافة/تحديث الترجمة: {key} للغة {language_code}")
            return True
        except Exception as e:
            logger.error(f"فشل في إضافة/تحديث الترجمة: {str(e)}")
            return False
    
    def export_translations(self, language_code, file_path=None):
        """تصدير الترجمات إلى ملف"""
        try:
            if language_code not in self.available_languages:
                logger.error(f"اللغة غير مدعومة: {language_code}")
                return False
            
            # الحصول على الترجمات
            translations = self.translations.get(language_code, {})
            
            # تحديد مسار الملف
            if file_path is None:
                file_path = os.path.join(self.locale_dir, f"{language_code}_translations.json")
            
            # إنشاء دليل الملف إذا لم يكن موجودًا
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # حفظ الترجمات إلى ملف
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=4)
            
            logger.info(f"تم تصدير الترجمات للغة {language_code} إلى: {file_path}")
            return True
        except Exception as e:
            logger.error(f"فشل في تصدير الترجمات: {str(e)}")
            return False
    
    def import_translations(self, language_code, file_path):
        """استيراد الترجمات من ملف"""
        try:
            if language_code not in self.available_languages:
                logger.error(f"اللغة غير مدعومة: {language_code}")
                return False
            
            # التحقق من وجود الملف
            if not os.path.exists(file_path):
                logger.error(f"ملف الترجمات غير موجود: {file_path}")
                return False
            
            # قراءة الترجمات من الملف
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)
            
            # إضافة الترجمات إلى قاعدة البيانات
            for key, value in translations.items():
                self.add_translation(language_code, key, value)
            
            logger.info(f"تم استيراد الترجمات للغة {language_code} من: {file_path}")
            return True
        except Exception as e:
            logger.error(f"فشل في استيراد الترجمات: {str(e)}")
            return False
    
    @lru_cache(maxsize=1024)
    def cached_translate(self, key, language_code=None, default=None, **kwargs):
        """ترجمة النص مع التخزين المؤقت للأداء"""
        return self.translate(key, language_code, default, **kwargs)

# نموذج استخدام
if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # تهيئة مدير تعدد اللغات
    i18n_manager = I18nManager()
    
    # مثال على الترجمة
    welcome_ar = i18n_manager.translate('welcome', 'ar', 'مرحبًا بك في نظام Gaara ERP')
    welcome_en = i18n_manager.translate('welcome', 'en', 'Welcome to Gaara ERP')
    
    print(f"الترجمة العربية: {welcome_ar}")
    print(f"الترجمة الإنجليزية: {welcome_en}")
    
    # مثال على الترجمة مع متغيرات
    greeting_ar = i18n_manager.translate('greeting', 'ar', 'مرحبًا {name}', name='أحمد')
    greeting_en = i18n_manager.translate('greeting', 'en', 'Hello {name}', name='Ahmed')
    
    print(f"التحية العربية: {greeting_ar}")
    print(f"التحية الإنجليزية: {greeting_en}")
    
    # مثال على إضافة ترجمة
    i18n_manager.add_translation('ar', 'save', 'حفظ', 'core')
    i18n_manager.add_translation('en', 'save', 'Save', 'core')
