#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة إدارة المصادر الموثوقة
=========================
هذه الوحدة مسؤولة عن إدارة وتوثيق المصادر الموثوقة للمعلومات الزراعية.
تتضمن وظائف للتحقق من موثوقية المصادر، وتصنيفها، وتخزينها، وتحديثها.
"""

import os
import json
import datetime
import requests
from urllib.parse import urlparse
import pandas as pd
from dotenv import load_dotenv
from ..database.database_manager import DatabaseManager
from ..audit.audit_manager import AuditManager
from ..auth.auth_manager import AuthManager

# تحميل متغيرات البيئة
load_dotenv()

class TrustedSourcesManager:
    """مدير المصادر الموثوقة للنظام"""
    
    def __init__(self, db_manager=None, audit_manager=None, auth_manager=None):
        """
        تهيئة مدير المصادر الموثوقة
        
        المعاملات:
            db_manager (DatabaseManager): مدير قاعدة البيانات
            audit_manager (AuditManager): مدير التدقيق
            auth_manager (AuthManager): مدير المصادقة
        """
        self.db_manager = db_manager or DatabaseManager()
        self.audit_manager = audit_manager or AuditManager()
        self.auth_manager = auth_manager or AuthManager()
        
        # إنشاء مجلدات المصادر إذا لم تكن موجودة
        self.system_sources_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'trusted_sources', 'system')
        self.admin_sources_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'trusted_sources', 'admin')
        
        os.makedirs(self.system_sources_dir, exist_ok=True)
        os.makedirs(self.admin_sources_dir, exist_ok=True)
        
        # تحميل قوائم المصادر الموثوقة
        self.system_sources = self._load_sources(os.path.join(self.system_sources_dir, 'system_sources.json'))
        self.admin_sources = self._load_sources(os.path.join(self.admin_sources_dir, 'admin_sources.json'))
        
        # قائمة بالمجالات الموثوقة افتراضياً
        self.default_trusted_domains = [
            'fao.org',           # منظمة الأغذية والزراعة للأمم المتحدة
            'cgiar.org',         # المجموعة الاستشارية للبحوث الزراعية الدولية
            'usda.gov',          # وزارة الزراعة الأمريكية
            'ars.usda.gov',      # خدمة البحوث الزراعية الأمريكية
            'extension.org',     # خدمة الإرشاد التعاوني الأمريكية
            'wur.nl',            # جامعة فاغينينغن للبحوث
            'cabi.org',          # المركز الدولي للزراعة والعلوم البيولوجية
            'plantvillage.psu.edu', # موقع PlantVillage لتشخيص أمراض النبات
            'apsnet.org',        # الجمعية الأمريكية لأمراض النبات
            'cropscience.org',   # الجمعية الدولية لعلوم المحاصيل
            'ippc.int',          # الاتفاقية الدولية لوقاية النباتات
            'worldagroforestry.org', # المركز العالمي للزراعة الحرجية
            'icarda.org',        # المركز الدولي للبحوث الزراعية في المناطق الجافة
            'irri.org',          # المعهد الدولي لبحوث الأرز
            'cimmyt.org',        # المركز الدولي لتحسين الذرة والقمح
            'iita.org',          # المعهد الدولي للزراعة الاستوائية
            'agrilinks.org',     # شبكة المعلومات الزراعية
            'sciencedirect.com', # قاعدة بيانات علمية
            'springer.com',      # ناشر علمي
            'wiley.com',         # ناشر علمي
            'nature.com',        # مجلة علمية
            'frontiersin.org',   # ناشر علمي مفتوح المصدر
            'mdpi.com',          # ناشر علمي مفتوح المصدر
            'researchgate.net',  # شبكة اجتماعية للباحثين
            'academia.edu',      # شبكة اجتماعية للباحثين
            'scholar.google.com' # محرك بحث للأوراق العلمية
        ]
    
    def _load_sources(self, file_path):
        """
        تحميل قائمة المصادر من ملف JSON
        
        المعاملات:
            file_path (str): مسار ملف المصادر
            
        العائد:
            list: قائمة المصادر
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        else:
            # إنشاء ملف فارغ إذا لم يكن موجوداً
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            return []
    
    def _save_sources(self, sources, file_path):
        """
        حفظ قائمة المصادر إلى ملف JSON
        
        المعاملات:
            sources (list): قائمة المصادر
            file_path (str): مسار ملف المصادر
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sources, f, ensure_ascii=False, indent=4)
    
    def add_source(self, url, title, description, category, tags, reliability_score, user_id, is_admin=False):
        """
        إضافة مصدر جديد إلى قائمة المصادر الموثوقة
        
        المعاملات:
            url (str): رابط المصدر
            title (str): عنوان المصدر
            description (str): وصف المصدر
            category (str): تصنيف المصدر (مثل: أمراض، تربة، أصناف)
            tags (list): وسوم المصدر
            reliability_score (float): درجة موثوقية المصدر (0-100)
            user_id (int): معرف المستخدم الذي أضاف المصدر
            is_admin (bool): هل المصدر يضاف إلى قائمة المسؤول
            
        العائد:
            bool: نجاح العملية
        """
        # التحقق من صلاحيات المستخدم
        if is_admin and not self.auth_manager.has_permission(user_id, 'manage_trusted_sources'):
            return False
        
        # التحقق من صحة الرابط
        if not self._validate_url(url):
            return False
        
        # إنشاء كائن المصدر
        source = {
            'url': url,
            'title': title,
            'description': description,
            'category': category,
            'tags': tags,
            'reliability_score': reliability_score,
            'added_by': user_id,
            'added_date': datetime.datetime.now().isoformat(),
            'last_verified': datetime.datetime.now().isoformat(),
            'verification_status': 'pending',
            'domain': urlparse(url).netloc
        }
        
        # إضافة المصدر إلى القائمة المناسبة
        if is_admin:
            self.admin_sources.append(source)
            self._save_sources(self.admin_sources, os.path.join(self.admin_sources_dir, 'admin_sources.json'))
        else:
            self.system_sources.append(source)
            self._save_sources(self.system_sources, os.path.join(self.system_sources_dir, 'system_sources.json'))
        
        # تسجيل العملية
        self.audit_manager.log_action(
            user_id=user_id,
            action_type='add_trusted_source',
            entity_type='trusted_source',
            entity_id=url,
            details=f"Added trusted source: {title} ({url})"
        )
        
        # إضافة المصدر إلى قاعدة البيانات
        self.db_manager.execute_query(
            """
            INSERT INTO trusted_sources 
            (url, title, description, category, tags, reliability_score, added_by, added_date, last_verified, verification_status, domain, is_admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (url, title, description, category, json.dumps(tags), reliability_score, user_id, 
             source['added_date'], source['last_verified'], source['verification_status'], source['domain'], is_admin)
        )
        
        return True
    
    def remove_source(self, url, user_id, is_admin=False):
        """
        إزالة مصدر من قائمة المصادر الموثوقة
        
        المعاملات:
            url (str): رابط المصدر
            user_id (int): معرف المستخدم الذي يزيل المصدر
            is_admin (bool): هل المصدر يزال من قائمة المسؤول
            
        العائد:
            bool: نجاح العملية
        """
        # التحقق من صلاحيات المستخدم
        if is_admin and not self.auth_manager.has_permission(user_id, 'manage_trusted_sources'):
            return False
        
        # إزالة المصدر من القائمة المناسبة
        if is_admin:
            self.admin_sources = [s for s in self.admin_sources if s['url'] != url]
            self._save_sources(self.admin_sources, os.path.join(self.admin_sources_dir, 'admin_sources.json'))
        else:
            self.system_sources = [s for s in self.system_sources if s['url'] != url]
            self._save_sources(self.system_sources, os.path.join(self.system_sources_dir, 'system_sources.json'))
        
        # تسجيل العملية
        self.audit_manager.log_action(
            user_id=user_id,
            action_type='remove_trusted_source',
            entity_type='trusted_source',
            entity_id=url,
            details=f"Removed trusted source: {url}"
        )
        
        # إزالة المصدر من قاعدة البيانات
        self.db_manager.execute_query(
            "DELETE FROM trusted_sources WHERE url = %s AND is_admin = %s",
            (url, is_admin)
        )
        
        return True
    
    def verify_source(self, url, user_id):
        """
        التحقق من مصدر وتحديث حالته
        
        المعاملات:
            url (str): رابط المصدر
            user_id (int): معرف المستخدم الذي يتحقق من المصدر
            
        العائد:
            dict: نتائج التحقق
        """
        # التحقق من صلاحيات المستخدم
        if not self.auth_manager.has_permission(user_id, 'verify_trusted_sources'):
            return {'success': False, 'message': 'Insufficient permissions'}
        
        try:
            # محاولة الوصول إلى الرابط
            response = requests.head(url, timeout=10)
            status_code = response.status_code
            
            # تحديث حالة المصدر في القوائم
            for sources_list in [self.system_sources, self.admin_sources]:
                for source in sources_list:
                    if source['url'] == url:
                        source['last_verified'] = datetime.datetime.now().isoformat()
                        if 200 <= status_code < 400:
                            source['verification_status'] = 'verified'
                        else:
                            source['verification_status'] = 'failed'
            
            # حفظ التغييرات
            self._save_sources(self.system_sources, os.path.join(self.system_sources_dir, 'system_sources.json'))
            self._save_sources(self.admin_sources, os.path.join(self.admin_sources_dir, 'admin_sources.json'))
            
            # تحديث قاعدة البيانات
            self.db_manager.execute_query(
                """
                UPDATE trusted_sources 
                SET last_verified = %s, verification_status = %s
                WHERE url = %s
                """,
                (datetime.datetime.now().isoformat(), 
                 'verified' if 200 <= status_code < 400 else 'failed', 
                 url)
            )
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='verify_trusted_source',
                entity_type='trusted_source',
                entity_id=url,
                details=f"Verified trusted source: {url}, Status: {status_code}"
            )
            
            return {
                'success': True, 
                'status_code': status_code,
                'verification_status': 'verified' if 200 <= status_code < 400 else 'failed',
                'message': 'Source verified successfully'
            }
            
        except requests.RequestException as e:
            # تحديث حالة المصدر في حالة الفشل
            for sources_list in [self.system_sources, self.admin_sources]:
                for source in sources_list:
                    if source['url'] == url:
                        source['last_verified'] = datetime.datetime.now().isoformat()
                        source['verification_status'] = 'failed'
            
            # حفظ التغييرات
            self._save_sources(self.system_sources, os.path.join(self.system_sources_dir, 'system_sources.json'))
            self._save_sources(self.admin_sources, os.path.join(self.admin_sources_dir, 'admin_sources.json'))
            
            # تحديث قاعدة البيانات
            self.db_manager.execute_query(
                """
                UPDATE trusted_sources 
                SET last_verified = %s, verification_status = %s
                WHERE url = %s
                """,
                (datetime.datetime.now().isoformat(), 'failed', url)
            )
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='verify_trusted_source',
                entity_type='trusted_source',
                entity_id=url,
                details=f"Failed to verify trusted source: {url}, Error: {str(e)}"
            )
            
            return {
                'success': False, 
                'error': str(e),
                'verification_status': 'failed',
                'message': 'Failed to verify source'
            }
    
    def get_sources_by_category(self, category, is_admin=False):
        """
        الحصول على المصادر حسب التصنيف
        
        المعاملات:
            category (str): تصنيف المصادر
            is_admin (bool): هل يتم البحث في قائمة المسؤول
            
        العائد:
            list: قائمة المصادر المطابقة
        """
        sources = self.admin_sources if is_admin else self.system_sources
        return [s for s in sources if s['category'] == category]
    
    def get_sources_by_tags(self, tags, is_admin=False):
        """
        الحصول على المصادر حسب الوسوم
        
        المعاملات:
            tags (list): قائمة الوسوم
            is_admin (bool): هل يتم البحث في قائمة المسؤول
            
        العائد:
            list: قائمة المصادر المطابقة
        """
        sources = self.admin_sources if is_admin else self.system_sources
        return [s for s in sources if any(tag in s['tags'] for tag in tags)]
    
    def search_sources(self, query, is_admin=False):
        """
        البحث في المصادر
        
        المعاملات:
            query (str): نص البحث
            is_admin (bool): هل يتم البحث في قائمة المسؤول
            
        العائد:
            list: قائمة المصادر المطابقة
        """
        sources = self.admin_sources if is_admin else self.system_sources
        query = query.lower()
        return [s for s in sources if 
                query in s['title'].lower() or 
                query in s['description'].lower() or 
                query in s['url'].lower() or 
                any(query in tag.lower() for tag in s['tags'])]
    
    def export_sources_to_csv(self, file_path, is_admin=False):
        """
        تصدير المصادر إلى ملف CSV
        
        المعاملات:
            file_path (str): مسار ملف التصدير
            is_admin (bool): هل يتم تصدير قائمة المسؤول
            
        العائد:
            bool: نجاح العملية
        """
        sources = self.admin_sources if is_admin else self.system_sources
        try:
            df = pd.DataFrame(sources)
            df.to_csv(file_path, index=False, encoding='utf-8')
            return True
        except Exception:
            return False
    
    def import_sources_from_csv(self, file_path, user_id, is_admin=False, merge_mode='append'):
        """
        استيراد المصادر من ملف CSV
        
        المعاملات:
            file_path (str): مسار ملف الاستيراد
            user_id (int): معرف المستخدم الذي يستورد المصادر
            is_admin (bool): هل يتم الاستيراد إلى قائمة المسؤول
            merge_mode (str): طريقة الدمج ('append' أو 'replace')
            
        العائد:
            dict: نتائج الاستيراد
        """
        # التحقق من صلاحيات المستخدم
        if is_admin and not self.auth_manager.has_permission(user_id, 'manage_trusted_sources'):
            return {'success': False, 'message': 'Insufficient permissions'}
        
        try:
            # قراءة ملف CSV
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # التحقق من صحة البيانات
            required_columns = ['url', 'title', 'description', 'category', 'tags', 'reliability_score']
            if not all(col in df.columns for col in required_columns):
                return {'success': False, 'message': 'Invalid CSV format. Missing required columns.'}
            
            # تحويل البيانات إلى قائمة مصادر
            new_sources = []
            for _, row in df.iterrows():
                # تحويل الوسوم من نص إلى قائمة إذا لزم الأمر
                tags = row['tags']
                if isinstance(tags, str):
                    try:
                        tags = json.loads(tags)
                    except json.JSONDecodeError:
                        tags = [tag.strip() for tag in tags.split(',')]
                
                source = {
                    'url': row['url'],
                    'title': row['title'],
                    'description': row['description'],
                    'category': row['category'],
                    'tags': tags,
                    'reliability_score': float(row['reliability_score']),
                    'added_by': user_id,
                    'added_date': datetime.datetime.now().isoformat(),
                    'last_verified': datetime.datetime.now().isoformat(),
                    'verification_status': 'pending',
                    'domain': urlparse(row['url']).netloc
                }
                
                # التحقق من صحة الرابط
                if self._validate_url(source['url']):
                    new_sources.append(source)
            
            # تحديد القائمة المستهدفة
            target_sources = self.admin_sources if is_admin else self.system_sources
            target_file = os.path.join(self.admin_sources_dir if is_admin else self.system_sources_dir, 
                                      'admin_sources.json' if is_admin else 'system_sources.json')
            
            # دمج المصادر حسب الوضع المحدد
            if merge_mode == 'replace':
                target_sources = new_sources
            else:  # append
                # إزالة التكرارات
                existing_urls = {s['url'] for s in target_sources}
                target_sources.extend([s for s in new_sources if s['url'] not in existing_urls])
            
            # حفظ التغييرات
            if is_admin:
                self.admin_sources = target_sources
            else:
                self.system_sources = target_sources
                
            self._save_sources(target_sources, target_file)
            
            # تحديث قاعدة البيانات
            if merge_mode == 'replace':
                # حذف المصادر القديمة
                self.db_manager.execute_query(
                    "DELETE FROM trusted_sources WHERE is_admin = %s",
                    (is_admin,)
                )
            
            # إضافة المصادر الجديدة
            for source in new_sources:
                # التحقق من وجود المصدر
                result = self.db_manager.execute_query(
                    "SELECT COUNT(*) FROM trusted_sources WHERE url = %s AND is_admin = %s",
                    (source['url'], is_admin)
                )
                
                if result[0][0] == 0:
                    # إضافة المصدر الجديد
                    self.db_manager.execute_query(
                        """
                        INSERT INTO trusted_sources 
                        (url, title, description, category, tags, reliability_score, added_by, added_date, last_verified, verification_status, domain, is_admin)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (source['url'], source['title'], source['description'], source['category'], 
                         json.dumps(source['tags']), source['reliability_score'], user_id, 
                         source['added_date'], source['last_verified'], source['verification_status'], source['domain'], is_admin)
                    )
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='import_trusted_sources',
                entity_type='trusted_sources',
                entity_id=file_path,
                details=f"Imported {len(new_sources)} trusted sources from {file_path}, Mode: {merge_mode}"
            )
            
            return {
                'success': True, 
                'imported_count': len(new_sources),
                'message': f'Successfully imported {len(new_sources)} sources'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Import failed: {str(e)}'}
    
    def _validate_url(self, url):
        """
        التحقق من صحة الرابط
        
        المعاملات:
            url (str): الرابط المراد التحقق منه
            
        العائد:
            bool: صحة الرابط
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def is_trusted_domain(self, url):
        """
        التحقق مما إذا كان المجال موثوقاً
        
        المعاملات:
            url (str): الرابط المراد التحقق منه
            
        العائد:
            bool: هل المجال موثوق
        """
        try:
            domain = urlparse(url).netloc
            
            # التحقق من المجالات الافتراضية
            if any(domain.endswith(trusted_domain) for trusted_domain in self.default_trusted_domains):
                return True
            
            # التحقق من المجالات في قوائم المصادر
            system_domains = {s['domain'] for s in self.system_sources}
            admin_domains = {s['domain'] for s in self.admin_sources}
            
            return domain in system_domains or domain in admin_domains
        except:
            return False
    
    def get_reliability_score(self, url):
        """
        الحصول على درجة موثوقية المصدر
        
        المعاملات:
            url (str): رابط المصدر
            
        العائد:
            float: درجة الموثوقية (0-100)، أو -1 إذا لم يتم العثور على المصدر
        """
        # البحث في قوائم المصادر
        for sources_list in [self.system_sources, self.admin_sources]:
            for source in sources_list:
                if source['url'] == url:
                    return source['reliability_score']
        
        # التحقق من المجال
        try:
            domain = urlparse(url).netloc
            
            # التحقق من المجالات الافتراضية
            if any(domain.endswith(trusted_domain) for trusted_domain in self.default_trusted_domains):
                return 80  # درجة موثوقية افتراضية للمجالات المعروفة
            
            # البحث عن مصادر من نفس المجال
            for sources_list in [self.system_sources, self.admin_sources]:
                domain_sources = [s for s in sources_list if s['domain'] == domain]
                if domain_sources:
                    # حساب متوسط درجة الموثوقية
                    return sum(s['reliability_score'] for s in domain_sources) / len(domain_sources)
        except:
            pass
        
        return -1  # لم يتم العثور على المصدر
    
    def verify_all_sources(self, user_id):
        """
        التحقق من جميع المصادر
        
        المعاملات:
            user_id (int): معرف المستخدم الذي يتحقق من المصادر
            
        العائد:
            dict: نتائج التحقق
        """
        # التحقق من صلاحيات المستخدم
        if not self.auth_manager.has_permission(user_id, 'verify_trusted_sources'):
            return {'success': False, 'message': 'Insufficient permissions'}
        
        results = {
            'total': 0,
            'verified': 0,
            'failed': 0,
            'details': []
        }
        
        # جمع جميع المصادر
        all_sources = self.system_sources + self.admin_sources
        results['total'] = len(all_sources)
        
        # التحقق من كل مصدر
        for source in all_sources:
            result = self.verify_source(source['url'], user_id)
            if result['success'] and result['verification_status'] == 'verified':
                results['verified'] += 1
            else:
                results['failed'] += 1
            
            results['details'].append({
                'url': source['url'],
                'result': result
            })
        
        return results
    
    def get_sources_stats(self):
        """
        الحصول على إحصائيات المصادر
        
        العائد:
            dict: إحصائيات المصادر
        """
        system_categories = {}
        admin_categories = {}
        
        # حساب عدد المصادر لكل تصنيف
        for source in self.system_sources:
            category = source['category']
            system_categories[category] = system_categories.get(category, 0) + 1
        
        for source in self.admin_sources:
            category = source['category']
            admin_categories[category] = admin_categories.get(category, 0) + 1
        
        # حساب عدد المصادر حسب حالة التحقق
        system_verification = {
            'verified': len([s for s in self.system_sources if s['verification_status'] == 'verified']),
            'failed': len([s for s in self.system_sources if s['verification_status'] == 'failed']),
            'pending': len([s for s in self.system_sources if s['verification_status'] == 'pending'])
        }
        
        admin_verification = {
            'verified': len([s for s in self.admin_sources if s['verification_status'] == 'verified']),
            'failed': len([s for s in self.admin_sources if s['verification_status'] == 'failed']),
            'pending': len([s for s in self.admin_sources if s['verification_status'] == 'pending'])
        }
        
        return {
            'system_sources_count': len(self.system_sources),
            'admin_sources_count': len(self.admin_sources),
            'system_categories': system_categories,
            'admin_categories': admin_categories,
            'system_verification': system_verification,
            'admin_verification': admin_verification
        }
