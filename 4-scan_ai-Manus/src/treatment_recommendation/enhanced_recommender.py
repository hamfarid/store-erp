#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام توصيات العلاج المحسن مع البحث عن الجرعات
=======================================
هذه الوحدة مسؤولة عن تقديم توصيات العلاج المحسنة مع البحث عن الجرعات المناسبة
من مصادر موثوقة على الإنترنت ومن خلال التعلم من تجارب المستخدمين.
"""

import os
import json
import datetime
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from ..database.database_manager import DatabaseManager
from ..audit.audit_manager import AuditManager
from ..auth.auth_manager import AuthManager
from ..data_collection.web_scraper import WebScraper
from ..data_collection.comprehensive_search import ComprehensiveSearch
from ..trusted_sources.trusted_sources_manager import TrustedSourcesManager

# تحميل متغيرات البيئة
load_dotenv()

class EnhancedTreatmentRecommender:
    """نظام توصيات العلاج المحسن مع البحث عن الجرعات"""
    
    def __init__(self, db_manager=None, audit_manager=None, auth_manager=None):
        """
        تهيئة نظام توصيات العلاج المحسن
        
        المعاملات:
            db_manager (DatabaseManager): مدير قاعدة البيانات
            audit_manager (AuditManager): مدير التدقيق
            auth_manager (AuthManager): مدير المصادقة
        """
        self.db_manager = db_manager or DatabaseManager()
        self.audit_manager = audit_manager or AuditManager()
        self.auth_manager = auth_manager or AuthManager()
        self.web_scraper = WebScraper()
        self.search_engine = ComprehensiveSearch()
        self.trusted_sources = TrustedSourcesManager()
        
        # تحميل قائمة المصادر الموثوقة للمعلومات الزراعية
        self.trusted_domains = self.trusted_sources.get_trusted_domains('treatment')
        
        # تحميل قاعدة بيانات العلاجات المعروفة
        self.known_treatments = self._load_known_treatments()
        
        # تحميل سجل الجرعات السابقة
        self.dosage_history = self._load_dosage_history()
        
        # تحديد الحد الأقصى للتشوه في البيانات (5%)
        self.max_data_distortion = 0.05
    
    def _load_known_treatments(self):
        """
        تحميل قاعدة بيانات العلاجات المعروفة
        
        العائد:
            dict: قاعدة بيانات العلاجات المعروفة
        """
        try:
            query = """
                SELECT id, name, type, target_disease, active_ingredient, 
                       recommended_dosage, application_method, safety_period, 
                       effectiveness_rating, side_effects, environmental_impact,
                       last_updated, source
                FROM treatments
            """
            results = self.db_manager.execute_query(query)
            
            treatments = {}
            for row in results:
                treatment_id = row[0]
                treatments[treatment_id] = {
                    'id': treatment_id,
                    'name': row[1],
                    'type': row[2],
                    'target_disease': row[3],
                    'active_ingredient': row[4],
                    'recommended_dosage': row[5],
                    'application_method': row[6],
                    'safety_period': row[7],
                    'effectiveness_rating': row[8],
                    'side_effects': row[9],
                    'environmental_impact': row[10],
                    'last_updated': row[11],
                    'source': row[12]
                }
            
            return treatments
            
        except Exception as e:
            print(f"Error loading known treatments: {str(e)}")
            return {}
    
    def _load_dosage_history(self):
        """
        تحميل سجل الجرعات السابقة
        
        العائد:
            dict: سجل الجرعات السابقة
        """
        try:
            query = """
                SELECT treatment_id, disease_id, crop_id, dosage, 
                       effectiveness_rating, application_date, user_id
                FROM treatment_applications
                ORDER BY application_date DESC
            """
            results = self.db_manager.execute_query(query)
            
            dosage_history = {}
            for row in results:
                treatment_id = row[0]
                disease_id = row[1]
                crop_id = row[2]
                
                key = f"{treatment_id}_{disease_id}_{crop_id}"
                if key not in dosage_history:
                    dosage_history[key] = []
                
                dosage_history[key].append({
                    'treatment_id': treatment_id,
                    'disease_id': disease_id,
                    'crop_id': crop_id,
                    'dosage': row[3],
                    'effectiveness_rating': row[4],
                    'application_date': row[5],
                    'user_id': row[6]
                })
            
            return dosage_history
            
        except Exception as e:
            print(f"Error loading dosage history: {str(e)}")
            return {}
    
    def recommend_treatment(self, disease_id, crop_id, severity, growth_stage, user_id):
        """
        توصية بالعلاج المناسب لمرض معين في محصول معين
        
        المعاملات:
            disease_id (int): معرف المرض
            crop_id (int): معرف المحصول
            severity (str): شدة الإصابة (mild, moderate, severe)
            growth_stage (str): مرحلة نمو المحصول
            user_id (int): معرف المستخدم
            
        العائد:
            dict: توصيات العلاج
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'view_treatment_recommendations'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استعلام عن معلومات المرض
            disease_query = """
                SELECT name, causal_agent, symptoms, conditions
                FROM diseases
                WHERE id = %s
            """
            disease_result = self.db_manager.execute_query(disease_query, (disease_id,))
            
            if not disease_result:
                return {'success': False, 'message': 'Disease not found'}
            
            disease_name = disease_result[0][0]
            causal_agent = disease_result[0][1]
            disease_symptoms = disease_result[0][2]
            disease_conditions = disease_result[0][3]
            
            # استعلام عن معلومات المحصول
            crop_query = """
                SELECT name, type, family
                FROM crops
                WHERE id = %s
            """
            crop_result = self.db_manager.execute_query(crop_query, (crop_id,))
            
            if not crop_result:
                return {'success': False, 'message': 'Crop not found'}
            
            crop_name = crop_result[0][0]
            crop_type = crop_result[0][1]
            crop_family = crop_result[0][2]
            
            # البحث عن العلاجات المناسبة في قاعدة البيانات
            treatment_query = """
                SELECT t.id, t.name, t.type, t.active_ingredient, 
                       t.recommended_dosage, t.application_method, 
                       t.safety_period, t.effectiveness_rating,
                       t.side_effects, t.environmental_impact
                FROM treatments t
                JOIN treatment_disease_crop tdc ON t.id = tdc.treatment_id
                WHERE tdc.disease_id = %s AND tdc.crop_id = %s
                ORDER BY t.effectiveness_rating DESC
            """
            treatment_results = self.db_manager.execute_query(treatment_query, (disease_id, crop_id))
            
            # تحضير قائمة العلاجات
            treatments = []
            for row in treatment_results:
                treatment_id = row[0]
                treatment = {
                    'id': treatment_id,
                    'name': row[1],
                    'type': row[2],
                    'active_ingredient': row[3],
                    'recommended_dosage': row[4],
                    'application_method': row[5],
                    'safety_period': row[6],
                    'effectiveness_rating': row[7],
                    'side_effects': row[8],
                    'environmental_impact': row[9]
                }
                
                # البحث عن الجرعات السابقة لهذا العلاج
                key = f"{treatment_id}_{disease_id}_{crop_id}"
                if key in self.dosage_history:
                    # حساب متوسط الجرعة وفعاليتها
                    dosages = [entry['dosage'] for entry in self.dosage_history[key]]
                    effectiveness = [entry['effectiveness_rating'] for entry in self.dosage_history[key]]
                    
                    avg_dosage = sum(dosages) / len(dosages)
                    avg_effectiveness = sum(effectiveness) / len(effectiveness)
                    
                    treatment['historical_dosage'] = {
                        'average_dosage': avg_dosage,
                        'average_effectiveness': avg_effectiveness,
                        'sample_size': len(dosages),
                        'last_used': self.dosage_history[key][0]['application_date']
                    }
                
                treatments.append(treatment)
            
            # إذا لم يتم العثور على علاجات في قاعدة البيانات، ابحث على الإنترنت
            if not treatments:
                online_treatments = self._search_online_treatments(disease_name, crop_name, causal_agent)
                treatments.extend(online_treatments)
            
            # تعديل الجرعات بناءً على شدة الإصابة ومرحلة النمو
            for treatment in treatments:
                adjusted_dosage = self._adjust_dosage(
                    treatment['recommended_dosage'],
                    severity,
                    growth_stage,
                    crop_name,
                    treatment['name']
                )
                treatment['adjusted_dosage'] = adjusted_dosage
            
            # ترتيب العلاجات حسب الفعالية
            treatments.sort(key=lambda x: x.get('effectiveness_rating', 0), reverse=True)
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='recommend_treatment',
                entity_type='disease',
                entity_id=str(disease_id),
                details=f"Generated treatment recommendations for {disease_name} in {crop_name}"
            )
            
            return {
                'success': True,
                'disease': {
                    'id': disease_id,
                    'name': disease_name,
                    'causal_agent': causal_agent,
                    'symptoms': disease_symptoms,
                    'conditions': disease_conditions
                },
                'crop': {
                    'id': crop_id,
                    'name': crop_name,
                    'type': crop_type,
                    'family': crop_family
                },
                'severity': severity,
                'growth_stage': growth_stage,
                'treatments': treatments,
                'recommendation_date': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error recommending treatment: {str(e)}'}
    
    def _search_online_treatments(self, disease_name, crop_name, causal_agent):
        """
        البحث عن العلاجات على الإنترنت
        
        المعاملات:
            disease_name (str): اسم المرض
            crop_name (str): اسم المحصول
            causal_agent (str): العامل المسبب للمرض
            
        العائد:
            list: قائمة العلاجات المكتشفة
        """
        try:
            # تحضير استعلام البحث
            search_query = f"{disease_name} {crop_name} treatment dosage"
            
            # البحث عن المعلومات
            search_results = self.search_engine.search(search_query, max_results=10)
            
            # تصفية النتائج للمصادر الموثوقة فقط
            trusted_results = []
            for result in search_results:
                url = result.get('url', '')
                domain = self._extract_domain(url)
                if domain in self.trusted_domains:
                    trusted_results.append(result)
            
            # استخراج معلومات العلاج من النتائج
            treatments = []
            for result in trusted_results:
                url = result.get('url', '')
                
                # استخراج محتوى الصفحة
                page_content = self.web_scraper.scrape_page(url)
                if not page_content:
                    continue
                
                # تحليل محتوى الصفحة
                soup = BeautifulSoup(page_content, 'html.parser')
                
                # البحث عن معلومات العلاج
                treatment_info = self._extract_treatment_info(soup, disease_name, crop_name)
                if treatment_info:
                    treatment_info['source'] = url
                    treatments.append(treatment_info)
            
            return treatments
            
        except Exception as e:
            print(f"Error searching online treatments: {str(e)}")
            return []
    
    def _extract_domain(self, url):
        """
        استخراج اسم النطاق من URL
        
        المعاملات:
            url (str): عنوان URL
            
        العائد:
            str: اسم النطاق
        """
        try:
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            return domain
        except:
            return ""
    
    def _extract_treatment_info(self, soup, disease_name, crop_name):
        """
        استخراج معلومات العلاج من صفحة ويب
        
        المعاملات:
            soup (BeautifulSoup): كائن BeautifulSoup للصفحة
            disease_name (str): اسم المرض
            crop_name (str): اسم المحصول
            
        العائد:
            dict: معلومات العلاج
        """
        try:
            # البحث عن اسم العلاج
            treatment_name = None
            for heading in soup.find_all(['h1', 'h2', 'h3']):
                text = heading.get_text().lower()
                if 'treatment' in text or 'control' in text or 'management' in text:
                    treatment_name = heading.get_text().strip()
                    break
            
            if not treatment_name:
                return None
            
            # البحث عن المادة الفعالة
            active_ingredient = None
            for p in soup.find_all('p'):
                text = p.get_text().lower()
                if 'active ingredient' in text or 'chemical' in text:
                    active_ingredient = p.get_text().strip()
                    break
            
            # البحث عن الجرعة الموصى بها
            recommended_dosage = None
            for p in soup.find_all(['p', 'li']):
                text = p.get_text().lower()
                if 'dosage' in text or 'rate' in text or 'dose' in text:
                    recommended_dosage = p.get_text().strip()
                    break
            
            # البحث عن طريقة التطبيق
            application_method = None
            for p in soup.find_all(['p', 'li']):
                text = p.get_text().lower()
                if 'application' in text or 'apply' in text or 'spray' in text:
                    application_method = p.get_text().strip()
                    break
            
            # البحث عن فترة الأمان
            safety_period = None
            for p in soup.find_all(['p', 'li']):
                text = p.get_text().lower()
                if 'safety' in text or 'harvest interval' in text or 'phi' in text:
                    safety_period = p.get_text().strip()
                    break
            
            # تقدير فعالية العلاج
            effectiveness_rating = 0.7  # قيمة افتراضية
            
            # تحضير معلومات العلاج
            treatment_info = {
                'name': treatment_name,
                'type': 'Unknown',
                'active_ingredient': active_ingredient,
                'recommended_dosage': recommended_dosage,
                'application_method': application_method,
                'safety_period': safety_period,
                'effectiveness_rating': effectiveness_rating,
                'side_effects': 'Unknown',
                'environmental_impact': 'Unknown',
                'source_type': 'online'
            }
            
            return treatment_info
            
        except Exception as e:
            print(f"Error extracting treatment info: {str(e)}")
            return None
    
    def _adjust_dosage(self, base_dosage, severity, growth_stage, crop_name, treatment_name):
        """
        تعديل الجرعة بناءً على شدة الإصابة ومرحلة النمو
        
        المعاملات:
            base_dosage (str): الجرعة الأساسية
            severity (str): شدة الإصابة (mild, moderate, severe)
            growth_stage (str): مرحلة نمو المحصول
            crop_name (str): اسم المحصول
            treatment_name (str): اسم العلاج
            
        العائد:
            dict: معلومات الجرعة المعدلة
        """
        try:
            # استخراج القيمة العددية والوحدة من الجرعة الأساسية
            import re
            
            # التعامل مع الجرعة كنص إذا كانت كذلك
            if isinstance(base_dosage, str):
                match = re.search(r'(\d+(?:\.\d+)?)\s*([a-zA-Z/]+)', base_dosage)
                if match:
                    value = float(match.group(1))
                    unit = match.group(2)
                else:
                    return {
                        'value': base_dosage,
                        'unit': 'unknown',
                        'adjustment_factor': 1.0,
                        'notes': 'Could not parse base dosage'
                    }
            else:
                value = float(base_dosage)
                unit = 'unknown'
            
            # تحديد معامل التعديل بناءً على شدة الإصابة
            severity_factor = 1.0
            if severity == 'mild':
                severity_factor = 0.8
            elif severity == 'moderate':
                severity_factor = 1.0
            elif severity == 'severe':
                severity_factor = 1.2
            
            # تحديد معامل التعديل بناءً على مرحلة النمو
            stage_factor = 1.0
            if growth_stage == 'seedling':
                stage_factor = 0.7
            elif growth_stage == 'vegetative':
                stage_factor = 0.9
            elif growth_stage == 'flowering':
                stage_factor = 1.0
            elif growth_stage == 'fruiting':
                stage_factor = 0.9
            elif growth_stage == 'mature':
                stage_factor = 0.8
            
            # حساب معامل التعديل الإجمالي
            adjustment_factor = severity_factor * stage_factor
            
            # حساب الجرعة المعدلة
            adjusted_value = value * adjustment_factor
            
            # تحضير ملاحظات التعديل
            notes = []
            if severity_factor != 1.0:
                notes.append(f"Adjusted for {severity} severity (factor: {severity_factor})")
            if stage_factor != 1.0:
                notes.append(f"Adjusted for {growth_stage} growth stage (factor: {stage_factor})")
            
            return {
                'value': adjusted_value,
                'unit': unit,
                'base_value': value,
                'adjustment_factor': adjustment_factor,
                'notes': '; '.join(notes) if notes else 'No adjustments needed'
            }
            
        except Exception as e:
            print(f"Error adjusting dosage: {str(e)}")
            return {
                'value': base_dosage,
                'unit': 'unknown',
                'adjustment_factor': 1.0,
                'notes': f'Error adjusting dosage: {str(e)}'
            }
    
    def compare_treatments(self, treatments, criteria=None, user_id=None):
        """
        مقارنة بين العلاجات المختلفة
        
        المعاملات:
            treatments (list): قائمة معرفات العلاجات للمقارنة
            criteria (list): معايير المقارنة
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتائج المقارنة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if user_id and not self.auth_manager.has_permission(user_id, 'view_treatment_comparisons'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # تحديد معايير المقارنة الافتراضية إذا لم يتم تحديدها
            if not criteria:
                criteria = [
                    'effectiveness_rating',
                    'safety_period',
                    'side_effects',
                    'environmental_impact',
                    'cost'
                ]
            
            # استعلام عن معلومات العلاجات
            treatment_data = []
            for treatment_id in treatments:
                query = """
                    SELECT id, name, type, active_ingredient, 
                           recommended_dosage, application_method, 
                           safety_period, effectiveness_rating,
                           side_effects, environmental_impact,
                           (SELECT AVG(cost) FROM treatment_costs WHERE treatment_id = treatments.id) as avg_cost
                    FROM treatments
                    WHERE id = %s
                """
                result = self.db_manager.execute_query(query, (treatment_id,))
                
                if result:
                    treatment = {
                        'id': result[0][0],
                        'name': result[0][1],
                        'type': result[0][2],
                        'active_ingredient': result[0][3],
                        'recommended_dosage': result[0][4],
                        'application_method': result[0][5],
                        'safety_period': result[0][6],
                        'effectiveness_rating': result[0][7],
                        'side_effects': result[0][8],
                        'environmental_impact': result[0][9],
                        'cost': result[0][10] if result[0][10] else 0
                    }
                    treatment_data.append(treatment)
            
            # إعداد جدول المقارنة
            comparison_table = {}
            for criterion in criteria:
                comparison_table[criterion] = {}
                for treatment in treatment_data:
                    treatment_id = treatment['id']
                    treatment_name = treatment['name']
                    value = treatment.get(criterion, 'N/A')
                    comparison_table[criterion][treatment_id] = {
                        'treatment_name': treatment_name,
                        'value': value
                    }
            
            # تحديد العلاج الأفضل لكل معيار
            best_treatments = {}
            for criterion in criteria:
                if criterion == 'effectiveness_rating' or criterion == 'cost':
                    # للفعالية، القيمة الأعلى هي الأفضل
                    # للتكلفة، القيمة الأقل هي الأفضل
                    sort_reverse = (criterion == 'effectiveness_rating')
                    sorted_treatments = sorted(
                        treatment_data,
                        key=lambda x: x.get(criterion, 0) if x.get(criterion) is not None else 0,
                        reverse=sort_reverse
                    )
                    if sorted_treatments:
                        best_treatment = sorted_treatments[0]
                        best_treatments[criterion] = {
                            'treatment_id': best_treatment['id'],
                            'treatment_name': best_treatment['name'],
                            'value': best_treatment.get(criterion, 'N/A')
                        }
            
            # تسجيل العملية
            if user_id:
                self.audit_manager.log_action(
                    user_id=user_id,
                    action_type='compare_treatments',
                    entity_type='treatments',
                    entity_id=','.join(str(t) for t in treatments),
                    details=f"Compared treatments: {', '.join(str(t) for t in treatments)}"
                )
            
            return {
                'success': True,
                'treatments': treatment_data,
                'criteria': criteria,
                'comparison_table': comparison_table,
                'best_treatments': best_treatments,
                'comparison_date': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error comparing treatments: {str(e)}'}
    
    def search_treatment_dosage(self, treatment_name, disease_name, crop_name, user_id):
        """
        البحث عن جرعة العلاج المناسبة
        
        المعاملات:
            treatment_name (str): اسم العلاج
            disease_name (str): اسم المرض
            crop_name (str): اسم المحصول
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتائج البحث عن الجرعة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'search_treatment_dosage'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # البحث في قاعدة البيانات أولاً
            query = """
                SELECT t.id, t.name, t.recommended_dosage, t.application_method, 
                       t.safety_period, t.active_ingredient
                FROM treatments t
                JOIN treatment_disease_crop tdc ON t.id = tdc.treatment_id
                JOIN diseases d ON tdc.disease_id = d.id
                JOIN crops c ON tdc.crop_id = c.id
                WHERE t.name LIKE %s AND d.name LIKE %s AND c.name LIKE %s
            """
            results = self.db_manager.execute_query(
                query, 
                (f"%{treatment_name}%", f"%{disease_name}%", f"%{crop_name}%")
            )
            
            # تحضير نتائج البحث من قاعدة البيانات
            db_results = []
            for row in results:
                db_results.append({
                    'id': row[0],
                    'name': row[1],
                    'recommended_dosage': row[2],
                    'application_method': row[3],
                    'safety_period': row[4],
                    'active_ingredient': row[5],
                    'source': 'database'
                })
            
            # البحث على الإنترنت
            search_query = f"{treatment_name} dosage {disease_name} {crop_name}"
            online_results = self._search_online_dosage(search_query)
            
            # دمج النتائج
            all_results = db_results + online_results
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='search_treatment_dosage',
                entity_type='treatment',
                entity_id=treatment_name,
                details=f"Searched dosage for {treatment_name} for {disease_name} in {crop_name}"
            )
            
            return {
                'success': True,
                'treatment_name': treatment_name,
                'disease_name': disease_name,
                'crop_name': crop_name,
                'results': all_results,
                'search_date': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error searching treatment dosage: {str(e)}'}
    
    def _search_online_dosage(self, search_query):
        """
        البحث عن جرعة العلاج على الإنترنت
        
        المعاملات:
            search_query (str): استعلام البحث
            
        العائد:
            list: نتائج البحث
        """
        try:
            # البحث عن المعلومات
            search_results = self.search_engine.search(search_query, max_results=10)
            
            # تصفية النتائج للمصادر الموثوقة فقط
            trusted_results = []
            for result in search_results:
                url = result.get('url', '')
                domain = self._extract_domain(url)
                if domain in self.trusted_domains:
                    trusted_results.append(result)
            
            # استخراج معلومات الجرعة من النتائج
            dosage_results = []
            for result in trusted_results:
                url = result.get('url', '')
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                
                # استخراج محتوى الصفحة
                page_content = self.web_scraper.scrape_page(url)
                if not page_content:
                    continue
                
                # تحليل محتوى الصفحة
                soup = BeautifulSoup(page_content, 'html.parser')
                
                # البحث عن معلومات الجرعة
                dosage_info = self._extract_dosage_info(soup)
                if dosage_info:
                    dosage_info['url'] = url
                    dosage_info['title'] = title
                    dosage_info['snippet'] = snippet
                    dosage_info['source'] = 'online'
                    dosage_results.append(dosage_info)
            
            return dosage_results
            
        except Exception as e:
            print(f"Error searching online dosage: {str(e)}")
            return []
    
    def _extract_dosage_info(self, soup):
        """
        استخراج معلومات الجرعة من صفحة ويب
        
        المعاملات:
            soup (BeautifulSoup): كائن BeautifulSoup للصفحة
            
        العائد:
            dict: معلومات الجرعة
        """
        try:
            # البحث عن الجرعة الموصى بها
            recommended_dosage = None
            for p in soup.find_all(['p', 'li', 'td']):
                text = p.get_text().lower()
                if 'dosage' in text or 'rate' in text or 'dose' in text:
                    recommended_dosage = p.get_text().strip()
                    break
            
            if not recommended_dosage:
                return None
            
            # البحث عن طريقة التطبيق
            application_method = None
            for p in soup.find_all(['p', 'li', 'td']):
                text = p.get_text().lower()
                if 'application' in text or 'apply' in text or 'spray' in text:
                    application_method = p.get_text().strip()
                    break
            
            # البحث عن فترة الأمان
            safety_period = None
            for p in soup.find_all(['p', 'li', 'td']):
                text = p.get_text().lower()
                if 'safety' in text or 'harvest interval' in text or 'phi' in text:
                    safety_period = p.get_text().strip()
                    break
            
            # البحث عن المادة الفعالة
            active_ingredient = None
            for p in soup.find_all(['p', 'li', 'td']):
                text = p.get_text().lower()
                if 'active ingredient' in text or 'chemical' in text:
                    active_ingredient = p.get_text().strip()
                    break
            
            # تحضير معلومات الجرعة
            dosage_info = {
                'recommended_dosage': recommended_dosage,
                'application_method': application_method,
                'safety_period': safety_period,
                'active_ingredient': active_ingredient
            }
            
            return dosage_info
            
        except Exception as e:
            print(f"Error extracting dosage info: {str(e)}")
            return None
    
    def record_treatment_application(self, treatment_id, disease_id, crop_id, farm_id, 
                                    area, dosage, application_date, user_id):
        """
        تسجيل تطبيق علاج
        
        المعاملات:
            treatment_id (int): معرف العلاج
            disease_id (int): معرف المرض
            crop_id (int): معرف المحصول
            farm_id (int): معرف المزرعة
            area (float): المساحة المعالجة
            dosage (str): الجرعة المستخدمة
            application_date (str): تاريخ التطبيق
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التسجيل
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'record_treatment_application'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # إدخال بيانات التطبيق
            query = """
                INSERT INTO treatment_applications
                (treatment_id, disease_id, crop_id, farm_id, area, dosage, application_date, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (treatment_id, disease_id, crop_id, farm_id, area, dosage, application_date, user_id)
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to record treatment application'}
            
            application_id = result[0][0]
            
            # تحديث سجل الجرعات
            key = f"{treatment_id}_{disease_id}_{crop_id}"
            if key not in self.dosage_history:
                self.dosage_history[key] = []
            
            self.dosage_history[key].append({
                'treatment_id': treatment_id,
                'disease_id': disease_id,
                'crop_id': crop_id,
                'dosage': dosage,
                'effectiveness_rating': None,  # سيتم تحديثه لاحقاً
                'application_date': application_date,
                'user_id': user_id
            })
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='record_treatment_application',
                entity_type='treatment_application',
                entity_id=str(application_id),
                details=f"Recorded application of treatment {treatment_id} for disease {disease_id} in crop {crop_id}"
            )
            
            return {
                'success': True,
                'application_id': application_id,
                'message': 'Treatment application recorded successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error recording treatment application: {str(e)}'}
    
    def rate_treatment_effectiveness(self, application_id, effectiveness_rating, notes, user_id):
        """
        تقييم فعالية العلاج
        
        المعاملات:
            application_id (int): معرف تطبيق العلاج
            effectiveness_rating (float): تقييم الفعالية (0-10)
            notes (str): ملاحظات
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة التقييم
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'rate_treatment_effectiveness'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من وجود تطبيق العلاج
            query = """
                SELECT treatment_id, disease_id, crop_id
                FROM treatment_applications
                WHERE id = %s
            """
            result = self.db_manager.execute_query(query, (application_id,))
            
            if not result:
                return {'success': False, 'message': 'Treatment application not found'}
            
            treatment_id = result[0][0]
            disease_id = result[0][1]
            crop_id = result[0][2]
            
            # تحديث تقييم الفعالية
            update_query = """
                UPDATE treatment_applications
                SET effectiveness_rating = %s, effectiveness_notes = %s, rating_date = %s, rating_user_id = %s
                WHERE id = %s
            """
            self.db_manager.execute_query(
                update_query, 
                (effectiveness_rating, notes, datetime.datetime.now().isoformat(), user_id, application_id)
            )
            
            # تحديث سجل الجرعات
            key = f"{treatment_id}_{disease_id}_{crop_id}"
            if key in self.dosage_history:
                for entry in self.dosage_history[key]:
                    if entry.get('application_id') == application_id:
                        entry['effectiveness_rating'] = effectiveness_rating
                        break
            
            # تحديث تقييم فعالية العلاج في جدول العلاجات
            # حساب متوسط التقييمات
            avg_query = """
                SELECT AVG(effectiveness_rating)
                FROM treatment_applications
                WHERE treatment_id = %s AND effectiveness_rating IS NOT NULL
            """
            avg_result = self.db_manager.execute_query(avg_query, (treatment_id,))
            
            if avg_result and avg_result[0][0]:
                avg_rating = avg_result[0][0]
                
                # تحديث تقييم الفعالية في جدول العلاجات
                update_treatment_query = """
                    UPDATE treatments
                    SET effectiveness_rating = %s, last_updated = %s
                    WHERE id = %s
                """
                self.db_manager.execute_query(
                    update_treatment_query, 
                    (avg_rating, datetime.datetime.now().isoformat(), treatment_id)
                )
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='rate_treatment_effectiveness',
                entity_type='treatment_application',
                entity_id=str(application_id),
                details=f"Rated effectiveness of treatment application {application_id} as {effectiveness_rating}/10"
            )
            
            return {
                'success': True,
                'message': 'Treatment effectiveness rated successfully',
                'application_id': application_id,
                'effectiveness_rating': effectiveness_rating
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error rating treatment effectiveness: {str(e)}'}
    
    def check_for_new_treatments(self, disease_id, crop_id, user_id):
        """
        البحث عن علاجات جديدة لمرض معين في محصول معين
        
        المعاملات:
            disease_id (int): معرف المرض
            crop_id (int): معرف المحصول
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتائج البحث
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'check_new_treatments'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # استعلام عن معلومات المرض
            disease_query = """
                SELECT name, causal_agent
                FROM diseases
                WHERE id = %s
            """
            disease_result = self.db_manager.execute_query(disease_query, (disease_id,))
            
            if not disease_result:
                return {'success': False, 'message': 'Disease not found'}
            
            disease_name = disease_result[0][0]
            causal_agent = disease_result[0][1]
            
            # استعلام عن معلومات المحصول
            crop_query = """
                SELECT name
                FROM crops
                WHERE id = %s
            """
            crop_result = self.db_manager.execute_query(crop_query, (crop_id,))
            
            if not crop_result:
                return {'success': False, 'message': 'Crop not found'}
            
            crop_name = crop_result[0][0]
            
            # استعلام عن العلاجات الحالية
            current_treatments_query = """
                SELECT t.id, t.name
                FROM treatments t
                JOIN treatment_disease_crop tdc ON t.id = tdc.treatment_id
                WHERE tdc.disease_id = %s AND tdc.crop_id = %s
            """
            current_treatments_result = self.db_manager.execute_query(
                current_treatments_query, 
                (disease_id, crop_id)
            )
            
            current_treatments = []
            for row in current_treatments_result:
                current_treatments.append({
                    'id': row[0],
                    'name': row[1]
                })
            
            # البحث عن علاجات جديدة على الإنترنت
            search_query = f"new treatment {disease_name} {crop_name} {datetime.datetime.now().year}"
            online_treatments = self._search_online_treatments(disease_name, crop_name, causal_agent)
            
            # تصفية العلاجات الجديدة
            new_treatments = []
            for treatment in online_treatments:
                is_new = True
                for current in current_treatments:
                    if current['name'].lower() in treatment['name'].lower() or treatment['name'].lower() in current['name'].lower():
                        is_new = False
                        break
                
                if is_new:
                    new_treatments.append(treatment)
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='check_new_treatments',
                entity_type='disease',
                entity_id=str(disease_id),
                details=f"Checked for new treatments for {disease_name} in {crop_name}"
            )
            
            return {
                'success': True,
                'disease': {
                    'id': disease_id,
                    'name': disease_name
                },
                'crop': {
                    'id': crop_id,
                    'name': crop_name
                },
                'current_treatments': current_treatments,
                'new_treatments': new_treatments,
                'search_date': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error checking for new treatments: {str(e)}'}
    
    def add_treatment_from_user(self, treatment_data, user_id):
        """
        إضافة علاج جديد من المستخدم
        
        المعاملات:
            treatment_data (dict): بيانات العلاج
            user_id (int): معرف المستخدم
            
        العائد:
            dict: نتيجة الإضافة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.has_permission(user_id, 'add_treatment'):
                return {'success': False, 'message': 'Insufficient permissions'}
            
            # التحقق من تشوه البيانات
            distortion = self._check_data_distortion(treatment_data)
            if distortion > self.max_data_distortion:
                # إيقاف التعلم وإرسال إشعار
                return {
                    'success': False,
                    'message': f'Data distortion detected ({distortion:.2%}), learning stopped',
                    'distortion': distortion,
                    'requires_review': True
                }
            
            # استخراج بيانات العلاج
            name = treatment_data.get('name', '')
            treatment_type = treatment_data.get('type', '')
            active_ingredient = treatment_data.get('active_ingredient', '')
            recommended_dosage = treatment_data.get('recommended_dosage', '')
            application_method = treatment_data.get('application_method', '')
            safety_period = treatment_data.get('safety_period', '')
            effectiveness_rating = treatment_data.get('effectiveness_rating', 0)
            side_effects = treatment_data.get('side_effects', '')
            environmental_impact = treatment_data.get('environmental_impact', '')
            disease_ids = treatment_data.get('disease_ids', [])
            crop_ids = treatment_data.get('crop_ids', [])
            
            # إدخال بيانات العلاج
            query = """
                INSERT INTO treatments
                (name, type, active_ingredient, recommended_dosage, application_method, 
                safety_period, effectiveness_rating, side_effects, environmental_impact, 
                last_updated, source, added_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = self.db_manager.execute_query(
                query, 
                (
                    name, treatment_type, active_ingredient, recommended_dosage, 
                    application_method, safety_period, effectiveness_rating, 
                    side_effects, environmental_impact, 
                    datetime.datetime.now().isoformat(), 'user', user_id
                )
            )
            
            if not result:
                return {'success': False, 'message': 'Failed to add treatment'}
            
            treatment_id = result[0][0]
            
            # إضافة العلاقات بين العلاج والأمراض والمحاصيل
            for disease_id in disease_ids:
                for crop_id in crop_ids:
                    relation_query = """
                        INSERT INTO treatment_disease_crop
                        (treatment_id, disease_id, crop_id)
                        VALUES (%s, %s, %s)
                    """
                    self.db_manager.execute_query(relation_query, (treatment_id, disease_id, crop_id))
            
            # تحديث قاعدة بيانات العلاجات المعروفة
            self.known_treatments[treatment_id] = {
                'id': treatment_id,
                'name': name,
                'type': treatment_type,
                'target_disease': ', '.join(str(d) for d in disease_ids),
                'active_ingredient': active_ingredient,
                'recommended_dosage': recommended_dosage,
                'application_method': application_method,
                'safety_period': safety_period,
                'effectiveness_rating': effectiveness_rating,
                'side_effects': side_effects,
                'environmental_impact': environmental_impact,
                'last_updated': datetime.datetime.now().isoformat(),
                'source': 'user'
            }
            
            # تسجيل العملية
            self.audit_manager.log_action(
                user_id=user_id,
                action_type='add_treatment',
                entity_type='treatment',
                entity_id=str(treatment_id),
                details=f"Added new treatment: {name}"
            )
            
            return {
                'success': True,
                'treatment_id': treatment_id,
                'message': 'Treatment added successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error adding treatment: {str(e)}'}
    
    def _check_data_distortion(self, data):
        """
        التحقق من تشوه البيانات
        
        المعاملات:
            data (dict): البيانات للتحقق
            
        العائد:
            float: نسبة التشوه
        """
        try:
            # تنفيذ فحوصات بسيطة للتحقق من صحة البيانات
            distortion = 0.0
            
            # التحقق من وجود الحقول الإلزامية
            required_fields = ['name', 'type', 'active_ingredient', 'recommended_dosage']
            for field in required_fields:
                if field not in data or not data[field]:
                    distortion += 0.25
            
            # التحقق من صحة تقييم الفعالية
            effectiveness_rating = data.get('effectiveness_rating', 0)
            if not isinstance(effectiveness_rating, (int, float)) or effectiveness_rating < 0 or effectiveness_rating > 10:
                distortion += 0.25
            
            # التحقق من وجود علاقات مع الأمراض والمحاصيل
            if 'disease_ids' not in data or not data['disease_ids']:
                distortion += 0.25
            
            if 'crop_ids' not in data or not data['crop_ids']:
                distortion += 0.25
            
            return distortion
            
        except Exception as e:
            print(f"Error checking data distortion: {str(e)}")
            return 1.0  # أقصى تشوه في حالة حدوث خطأ
