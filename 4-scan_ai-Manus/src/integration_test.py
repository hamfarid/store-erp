#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام التكامل والاختبار الشامل

هذا الملف يقوم بتكامل جميع مكونات نظام الذكاء الاصطناعي الزراعي واختبارها بشكل شامل.
"""

import os
import sys
import json
import datetime
import logging
import argparse
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# استيراد مكونات النظام
try:
    # مكونات الكشف عن الأمراض
    from disease_detection.detector import DiseaseDetector
    from disease_detection.image_segmentation import ImageSegmenter
    
    # مكونات تحليل نقص العناصر
    from nutrient_analysis.analyzer import NutrientAnalyzer
    
    # مكونات التهجين وتزاوج النباتات
    from plant_breeding.predictor import BreedingPredictor
    from plant_breeding.specifications_manager import SpecificationsManager
    
    # مكونات توصيات العلاج
    from treatment_recommendation.recommender import TreatmentRecommender
    from treatment_recommendation.enhanced_recommender import EnhancedTreatmentRecommender
    
    # مكونات جمع البيانات
    from data_collection.web_scraper import WebScraper
    from data_collection.image_search import ImageSearch
    from data_collection.advanced_scraper import AdvancedScraper
    from data_collection.source_verifier import SourceVerifier
    from data_collection.comprehensive_search import ComprehensiveSearch
    
    # مكونات التعلم المستمر
    from continuous_learning.learning_manager import LearningManager
    
    # مكونات قاعدة البيانات
    from database.database_manager import DatabaseManager
    
    # مكونات تحليل التربة
    from soil_analysis.color_analyzer import SoilColorAnalyzer
    
    # مكونات التحليل المقارن
    from analysis.comparative_analyzer import ComparativeAnalyzer
    from analysis.parallel_image_analysis import ParallelImageAnalyzer
    
    # مكونات إدارة المهام
    from task_management.task_manager import TaskManager
    
    # مكونات المراقبة
    from monitoring.metrics_collector import MetricsCollector
    from monitoring.alerter import Alerter
    
    # مكونات التصور
    from visualization.visualizer import Visualizer
    
    # مكونات حساب التكلفة
    from cost_management.cost_calculator import CostCalculator
    
    # مكونات إدارة المزارع
    from farm_management.farm_manager import FarmManager
    
    # مكونات إدارة المشاتل
    from nursery_management.nursery_manager import NurseryManager
    
    # مكونات مقارنة الأصناف
    from variety_comparison.variety_manager import VarietyManager
    
    # مكونات إدارة المخزون
    from inventory_management.inventory_manager import InventoryManager
    
    # مكونات التقارير المالية
    from financial_reporting.financial_reporting_system import FinancialReportingSystem
    
    # مكونات المساعد الذكي
    from ai_assistant.assistant_agent import AIAssistant
    
    # مكونات الأمان والمصادقة
    from auth.auth_manager import AuthManager
    
    # مكونات التدقيق
    from audit.audit_manager import AuditManager
    
    # مكونات مراقبة جودة البيانات
    from data_quality.data_quality_monitor import DataQualityMonitor
    
    # مكونات إدارة البيانات
    from data_management.data_manager import DataManager
    
    # مكونات إدارة الكلمات المفتاحية
    from keywords.keyword_manager import KeywordManager
    
    # مكونات إدارة المؤسسات
    from organization.organization_manager import OrganizationManager
    
    # مكونات المصادر الموثوقة
    from trusted_sources.trusted_sources_manager import TrustedSourcesManager
    
    # مكونات تنظيم المحاصيل
    from crop_organization.crop_organization_manager import CropOrganizationManager
    
    # المكونات المساعدة
    from utils.image_processor import ImageProcessor
    from utils.data_augmentation import DataAugmenter
    from utils.config_loader import ConfigLoader
    
    logger.info("تم استيراد جميع مكونات النظام بنجاح")
except ImportError as e:
    logger.error(f"خطأ في استيراد المكونات: {str(e)}")
    raise

class IntegratedAgriculturalAISystem:
    """
    نظام الذكاء الاصطناعي الزراعي المتكامل
    
    يقوم هذا النظام بتكامل جميع مكونات النظام الفرعية وتنسيق العمليات بينها.
    """
    
    def __init__(self, config_path: str = None):
        """
        تهيئة النظام المتكامل
        
        المعلمات:
            config_path (str): مسار ملف التكوين
        """
        try:
            # تحميل التكوين
            self.config = ConfigLoader(config_path).load_config() if config_path else {}
            
            # استخراج معلومات قاعدة البيانات من التكوين أو متغيرات البيئة
            db_uri = self.config.get('database', {}).get('uri', os.getenv('DATABASE_URI', 'sqlite:///agricultural_ai_system.db'))
            
            # تهيئة مدير قاعدة البيانات
            self.db_manager = DatabaseManager(db_uri)
            
            # تهيئة مكونات النظام
            self._initialize_components(db_uri)
            
            # تهيئة مدير المهام
            self.task_manager = TaskManager()
            
            # تهيئة مدير التدقيق
            self.audit_manager = AuditManager(db_uri)
            
            # تسجيل بدء تشغيل النظام
            self.audit_manager.log_action(
                user_id=0,  # النظام
                action_type="بدء_تشغيل_النظام",
                entity_type="system",
                entity_id=0,
                details="بدء تشغيل نظام الذكاء الاصطناعي الزراعي المتكامل"
            )
            
            logger.info("تم تهيئة نظام الذكاء الاصطناعي الزراعي المتكامل بنجاح")
        
        except Exception as e:
            logger.error(f"خطأ في تهيئة النظام المتكامل: {str(e)}")
            raise
    
    def _initialize_components(self, db_uri: str):
        """
        تهيئة مكونات النظام
        
        المعلمات:
            db_uri (str): رابط قاعدة البيانات
        """
        try:
            # تهيئة مكونات الكشف عن الأمراض
            self.disease_detector = DiseaseDetector()
            self.image_segmenter = ImageSegmenter()
            
            # تهيئة مكونات تحليل نقص العناصر
            self.nutrient_analyzer = NutrientAnalyzer()
            
            # تهيئة مكونات التهجين وتزاوج النباتات
            self.breeding_predictor = BreedingPredictor()
            self.specifications_manager = SpecificationsManager(db_uri)
            
            # تهيئة مكونات توصيات العلاج
            self.treatment_recommender = TreatmentRecommender()
            self.enhanced_treatment_recommender = EnhancedTreatmentRecommender(db_uri)
            
            # تهيئة مكونات جمع البيانات
            self.web_scraper = WebScraper()
            self.image_search = ImageSearch()
            self.advanced_scraper = AdvancedScraper()
            self.source_verifier = SourceVerifier()
            self.comprehensive_search = ComprehensiveSearch()
            
            # تهيئة مكونات التعلم المستمر
            self.learning_manager = LearningManager(db_uri)
            
            # تهيئة مكونات تحليل التربة
            self.soil_analyzer = SoilColorAnalyzer()
            
            # تهيئة مكونات التحليل المقارن
            self.comparative_analyzer = ComparativeAnalyzer()
            self.parallel_image_analyzer = ParallelImageAnalyzer()
            
            # تهيئة مكونات المراقبة
            self.metrics_collector = MetricsCollector(db_uri)
            self.alerter = Alerter(db_uri)
            
            # تهيئة مكونات التصور
            self.visualizer = Visualizer()
            
            # تهيئة مكونات حساب التكلفة
            self.cost_calculator = CostCalculator(db_uri)
            
            # تهيئة مكونات إدارة المزارع
            self.farm_manager = FarmManager(db_uri)
            
            # تهيئة مكونات إدارة المشاتل
            self.nursery_manager = NurseryManager(db_uri)
            
            # تهيئة مكونات مقارنة الأصناف
            self.variety_manager = VarietyManager(db_uri)
            
            # تهيئة مكونات إدارة المخزون
            self.inventory_manager = InventoryManager(db_uri)
            
            # تهيئة مكونات التقارير المالية
            self.financial_reporting = FinancialReportingSystem(db_uri)
            
            # تهيئة مكونات المساعد الذكي
            self.ai_assistant = AIAssistant(db_uri)
            
            # تهيئة مكونات الأمان والمصادقة
            self.auth_manager = AuthManager(db_uri)
            
            # تهيئة مكونات مراقبة جودة البيانات
            self.data_quality_monitor = DataQualityMonitor(db_uri)
            
            # تهيئة مكونات إدارة البيانات
            self.data_manager = DataManager(db_uri)
            
            # تهيئة مكونات إدارة الكلمات المفتاحية
            self.keyword_manager = KeywordManager(db_uri)
            
            # تهيئة مكونات إدارة المؤسسات
            self.organization_manager = OrganizationManager(db_uri)
            
            # تهيئة مكونات المصادر الموثوقة
            self.trusted_sources_manager = TrustedSourcesManager(db_uri)
            
            # تهيئة مكونات تنظيم المحاصيل
            self.crop_organization_manager = CropOrganizationManager(db_uri)
            
            # تهيئة المكونات المساعدة
            self.image_processor = ImageProcessor()
            self.data_augmenter = DataAugmenter()
            
            logger.info("تم تهيئة جميع مكونات النظام بنجاح")
        
        except Exception as e:
            logger.error(f"خطأ في تهيئة مكونات النظام: {str(e)}")
            raise
    
    def analyze_plant_image(self, image_path: str, user_id: int, 
                           use_primitive_system: bool = False,
                           use_auto_selection: bool = True) -> Dict:
        """
        تحليل صورة النبات للكشف عن الأمراض ونقص العناصر
        
        المعلمات:
            image_path (str): مسار الصورة
            user_id (int): معرف المستخدم
            use_primitive_system (bool): استخدام النظام الأولي
            use_auto_selection (bool): استخدام الاختيار التلقائي بين النظامين
            
        العائد:
            Dict: نتائج التحليل
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'analyze_image'):
                raise PermissionError("ليس لديك صلاحية لتحليل الصور")
            
            # تسجيل بدء التحليل
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_تحليل_صورة",
                entity_type="image",
                entity_id=0,
                details=f"بدء تحليل الصورة: {image_path}"
            )
            
            # معالجة الصورة
            processed_image = self.image_processor.preprocess_image(image_path)
            
            # تحليل الصورة باستخدام النظام القياسي
            standard_results = {}
            if not use_primitive_system or use_auto_selection:
                # الكشف عن الأمراض
                disease_results = self.disease_detector.detect(processed_image)
                
                # تحليل نقص العناصر
                nutrient_results = self.nutrient_analyzer.analyze(processed_image)
                
                standard_results = {
                    'disease_detection': disease_results,
                    'nutrient_analysis': nutrient_results
                }
            
            # تحليل الصورة باستخدام النظام الأولي
            primitive_results = {}
            if use_primitive_system or use_auto_selection:
                # تقسيم الصورة
                segmented_images = self.image_segmenter.segment(processed_image)
                
                # تحليل كل قطعة
                segment_results = []
                for i, segment in enumerate(segmented_images):
                    # الكشف عن الأمراض في القطعة
                    segment_disease_results = self.disease_detector.detect(segment)
                    
                    # تحليل نقص العناصر في القطعة
                    segment_nutrient_results = self.nutrient_analyzer.analyze(segment)
                    
                    segment_results.append({
                        'segment_id': i,
                        'disease_detection': segment_disease_results,
                        'nutrient_analysis': segment_nutrient_results
                    })
                
                primitive_results = {
                    'segmentation': {
                        'num_segments': len(segmented_images),
                        'segment_results': segment_results
                    }
                }
            
            # اختيار النتائج النهائية
            final_results = {}
            if use_auto_selection and standard_results and primitive_results:
                # مقارنة النتائج واختيار الأفضل
                comparison_results = self.comparative_analyzer.compare_analysis_methods(
                    standard_results, primitive_results
                )
                
                # اختيار الطريقة الأفضل بناءً على نتائج المقارنة
                if comparison_results.get('recommended_method') == 'primitive':
                    final_results = primitive_results
                    analysis_method = 'primitive'
                else:
                    final_results = standard_results
                    analysis_method = 'standard'
                
                final_results['comparison'] = comparison_results
            elif use_primitive_system:
                final_results = primitive_results
                analysis_method = 'primitive'
            else:
                final_results = standard_results
                analysis_method = 'standard'
            
            # إضافة توصيات العلاج
            if 'disease_detection' in final_results:
                diseases = final_results['disease_detection'].get('detected_diseases', [])
                treatment_recommendations = self.enhanced_treatment_recommender.recommend_treatments(diseases)
                final_results['treatment_recommendations'] = treatment_recommendations
            
            # تحليل التربة إذا كانت موجودة في الصورة
            soil_analysis = self.soil_analyzer.analyze(processed_image)
            if soil_analysis.get('soil_detected', False):
                final_results['soil_analysis'] = soil_analysis
            
            # تسجيل نتائج التحليل
            self.learning_manager.record_analysis_result(
                image_path=image_path,
                analysis_results=final_results,
                user_id=user_id,
                analysis_method=analysis_method
            )
            
            # تسجيل اكتمال التحليل
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_تحليل_صورة",
                entity_type="image",
                entity_id=0,
                details=f"اكتمال تحليل الصورة: {image_path}"
            )
            
            return final_results
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_تحليل_صورة",
                entity_type="image",
                entity_id=0,
                details=f"خطأ في تحليل الصورة: {image_path} - {str(e)}"
            )
            
            logger.error(f"خطأ في تحليل صورة النبات: {str(e)}")
            raise
    
    def search_plant_information(self, query: str, user_id: int, 
                               search_type: str = 'comprehensive',
                               max_results: int = 10) -> Dict:
        """
        البحث عن معلومات النبات
        
        المعلمات:
            query (str): استعلام البحث
            user_id (int): معرف المستخدم
            search_type (str): نوع البحث (comprehensive، web، image)
            max_results (int): الحد الأقصى للنتائج
            
        العائد:
            Dict: نتائج البحث
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'search_information'):
                raise PermissionError("ليس لديك صلاحية للبحث عن المعلومات")
            
            # تسجيل بدء البحث
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_بحث",
                entity_type="search",
                entity_id=0,
                details=f"بدء البحث عن: {query}"
            )
            
            # إجراء البحث حسب النوع
            results = {}
            
            if search_type == 'comprehensive' or search_type == 'all':
                # البحث الشامل
                results = self.comprehensive_search.search(query, max_results=max_results)
                
                # التحقق من مصداقية المصادر
                for i, result in enumerate(results.get('web_results', [])):
                    source_verification = self.source_verifier.verify_source(result.get('url', ''))
                    results['web_results'][i]['source_verification'] = source_verification
            
            elif search_type == 'web':
                # البحث في الويب
                web_results = self.web_scraper.search(query, max_results=max_results)
                
                # التحقق من مصداقية المصادر
                for i, result in enumerate(web_results):
                    source_verification = self.source_verifier.verify_source(result.get('url', ''))
                    web_results[i]['source_verification'] = source_verification
                
                results = {'web_results': web_results}
            
            elif search_type == 'image':
                # البحث عن الصور
                image_results = self.image_search.search(query, max_results=max_results)
                results = {'image_results': image_results}
            
            else:
                raise ValueError(f"نوع بحث غير صالح: {search_type}")
            
            # تسجيل نتائج البحث
            self.learning_manager.record_search_result(
                query=query,
                search_results=results,
                user_id=user_id,
                search_type=search_type
            )
            
            # تسجيل اكتمال البحث
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_بحث",
                entity_type="search",
                entity_id=0,
                details=f"اكتمال البحث عن: {query}"
            )
            
            return results
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_بحث",
                entity_type="search",
                entity_id=0,
                details=f"خطأ في البحث عن: {query} - {str(e)}"
            )
            
            logger.error(f"خطأ في البحث عن معلومات النبات: {str(e)}")
            raise
    
    def predict_breeding_results(self, parent1_id: int, parent2_id: int, 
                                user_id: int) -> Dict:
        """
        التنبؤ بنتائج التهجين
        
        المعلمات:
            parent1_id (int): معرف الأب الأول
            parent2_id (int): معرف الأب الثاني
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتائج التنبؤ
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'predict_breeding'):
                raise PermissionError("ليس لديك صلاحية للتنبؤ بنتائج التهجين")
            
            # تسجيل بدء التنبؤ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_تنبؤ_تهجين",
                entity_type="breeding",
                entity_id=0,
                details=f"بدء التنبؤ بنتائج التهجين بين {parent1_id} و {parent2_id}"
            )
            
            # الحصول على مواصفات الآباء
            parent1_specs = self.specifications_manager.get_variety_specifications(parent1_id)
            parent2_specs = self.specifications_manager.get_variety_specifications(parent2_id)
            
            # التنبؤ بنتائج التهجين
            breeding_results = self.breeding_predictor.predict(parent1_specs, parent2_specs)
            
            # البحث عن معلومات إضافية
            additional_info = self.search_plant_information(
                f"تهجين {parent1_specs.get('name', '')} و {parent2_specs.get('name', '')}",
                user_id,
                search_type='web',
                max_results=5
            )
            
            # دمج النتائج
            results = {
                'parent1': parent1_specs,
                'parent2': parent2_specs,
                'predicted_offspring': breeding_results,
                'additional_info': additional_info.get('web_results', [])
            }
            
            # تسجيل نتائج التنبؤ
            self.learning_manager.record_breeding_prediction(
                parent1_id=parent1_id,
                parent2_id=parent2_id,
                prediction_results=results,
                user_id=user_id
            )
            
            # تسجيل اكتمال التنبؤ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_تنبؤ_تهجين",
                entity_type="breeding",
                entity_id=0,
                details=f"اكتمال التنبؤ بنتائج التهجين بين {parent1_id} و {parent2_id}"
            )
            
            return results
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_تنبؤ_تهجين",
                entity_type="breeding",
                entity_id=0,
                details=f"خطأ في التنبؤ بنتائج التهجين بين {parent1_id} و {parent2_id} - {str(e)}"
            )
            
            logger.error(f"خطأ في التنبؤ بنتائج التهجين: {str(e)}")
            raise
    
    def manage_farm(self, action: str, farm_data: Dict, user_id: int) -> Dict:
        """
        إدارة المزرعة
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            farm_data (Dict): بيانات المزرعة
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'manage_farm'):
                raise PermissionError("ليس لديك صلاحية لإدارة المزارع")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"بدء_{action}_مزرعة",
                entity_type="farm",
                entity_id=farm_data.get('id', 0),
                details=f"بدء {action} مزرعة: {farm_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                farm_id = self.farm_manager.add_farm(
                    name=farm_data.get('name', ''),
                    location=farm_data.get('location', ''),
                    area=farm_data.get('area', 0),
                    area_unit=farm_data.get('area_unit', 'فدان'),
                    owner=farm_data.get('owner', ''),
                    notes=farm_data.get('notes', ''),
                    user_id=user_id
                )
                result = {'farm_id': farm_id}
            
            elif action == 'update':
                success = self.farm_manager.update_farm(
                    farm_id=farm_data.get('id', 0),
                    name=farm_data.get('name', None),
                    location=farm_data.get('location', None),
                    area=farm_data.get('area', None),
                    area_unit=farm_data.get('area_unit', None),
                    owner=farm_data.get('owner', None),
                    notes=farm_data.get('notes', None),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.farm_manager.delete_farm(
                    farm_id=farm_data.get('id', 0),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'get':
                farm = self.farm_manager.get_farm(farm_data.get('id', 0))
                result = farm
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"اكتمال_{action}_مزرعة",
                entity_type="farm",
                entity_id=farm_data.get('id', 0),
                details=f"اكتمال {action} مزرعة: {farm_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"خطأ_{action}_مزرعة",
                entity_type="farm",
                entity_id=farm_data.get('id', 0),
                details=f"خطأ في {action} مزرعة: {farm_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة المزرعة: {str(e)}")
            raise
    
    def manage_crop(self, action: str, crop_data: Dict, user_id: int) -> Dict:
        """
        إدارة المحصول
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            crop_data (Dict): بيانات المحصول
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'manage_crop'):
                raise PermissionError("ليس لديك صلاحية لإدارة المحاصيل")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"بدء_{action}_محصول",
                entity_type="crop",
                entity_id=crop_data.get('id', 0),
                details=f"بدء {action} محصول: {crop_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                crop_id = self.farm_manager.add_crop(
                    farm_id=crop_data.get('farm_id', 0),
                    name=crop_data.get('name', ''),
                    variety=crop_data.get('variety', ''),
                    planting_date=crop_data.get('planting_date', None),
                    area=crop_data.get('area', 0),
                    area_unit=crop_data.get('area_unit', 'فدان'),
                    expected_harvest_dates=crop_data.get('expected_harvest_dates', []),
                    notes=crop_data.get('notes', ''),
                    user_id=user_id
                )
                result = {'crop_id': crop_id}
            
            elif action == 'update':
                success = self.farm_manager.update_crop(
                    crop_id=crop_data.get('id', 0),
                    farm_id=crop_data.get('farm_id', None),
                    name=crop_data.get('name', None),
                    variety=crop_data.get('variety', None),
                    planting_date=crop_data.get('planting_date', None),
                    area=crop_data.get('area', None),
                    area_unit=crop_data.get('area_unit', None),
                    expected_harvest_dates=crop_data.get('expected_harvest_dates', None),
                    notes=crop_data.get('notes', None),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.farm_manager.delete_crop(
                    crop_id=crop_data.get('id', 0),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'get':
                crop = self.farm_manager.get_crop(crop_data.get('id', 0))
                result = crop
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"اكتمال_{action}_محصول",
                entity_type="crop",
                entity_id=crop_data.get('id', 0),
                details=f"اكتمال {action} محصول: {crop_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"خطأ_{action}_محصول",
                entity_type="crop",
                entity_id=crop_data.get('id', 0),
                details=f"خطأ في {action} محصول: {crop_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة المحصول: {str(e)}")
            raise
    
    def manage_nursery(self, action: str, nursery_data: Dict, user_id: int) -> Dict:
        """
        إدارة المشتل
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            nursery_data (Dict): بيانات المشتل
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'manage_nursery'):
                raise PermissionError("ليس لديك صلاحية لإدارة المشاتل")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"بدء_{action}_مشتل",
                entity_type="nursery",
                entity_id=nursery_data.get('id', 0),
                details=f"بدء {action} مشتل: {nursery_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                nursery_id = self.nursery_manager.add_nursery(
                    name=nursery_data.get('name', ''),
                    location=nursery_data.get('location', ''),
                    capacity=nursery_data.get('capacity', 0),
                    manager=nursery_data.get('manager', ''),
                    notes=nursery_data.get('notes', ''),
                    user_id=user_id
                )
                result = {'nursery_id': nursery_id}
            
            elif action == 'update':
                success = self.nursery_manager.update_nursery(
                    nursery_id=nursery_data.get('id', 0),
                    name=nursery_data.get('name', None),
                    location=nursery_data.get('location', None),
                    capacity=nursery_data.get('capacity', None),
                    manager=nursery_data.get('manager', None),
                    notes=nursery_data.get('notes', None),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.nursery_manager.delete_nursery(
                    nursery_id=nursery_data.get('id', 0),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'get':
                nursery = self.nursery_manager.get_nursery(nursery_data.get('id', 0))
                result = nursery
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"اكتمال_{action}_مشتل",
                entity_type="nursery",
                entity_id=nursery_data.get('id', 0),
                details=f"اكتمال {action} مشتل: {nursery_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"خطأ_{action}_مشتل",
                entity_type="nursery",
                entity_id=nursery_data.get('id', 0),
                details=f"خطأ في {action} مشتل: {nursery_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة المشتل: {str(e)}")
            raise
    
    def manage_seedling_batch(self, action: str, batch_data: Dict, user_id: int) -> Dict:
        """
        إدارة دفعة الشتلات
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            batch_data (Dict): بيانات دفعة الشتلات
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'manage_seedling_batch'):
                raise PermissionError("ليس لديك صلاحية لإدارة دفعات الشتلات")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"بدء_{action}_دفعة_شتلات",
                entity_type="seedling_batch",
                entity_id=batch_data.get('id', 0),
                details=f"بدء {action} دفعة شتلات: {batch_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                batch_id = self.nursery_manager.add_seedling_batch(
                    nursery_id=batch_data.get('nursery_id', 0),
                    plant_type=batch_data.get('plant_type', ''),
                    variety=batch_data.get('variety', ''),
                    quantity=batch_data.get('quantity', 0),
                    planting_date=batch_data.get('planting_date', None),
                    expected_ready_date=batch_data.get('expected_ready_date', None),
                    season=batch_data.get('season', 'صيف'),
                    customer_name=batch_data.get('customer_name', ''),
                    reservation_date=batch_data.get('reservation_date', None),
                    delivery_date=batch_data.get('delivery_date', None),
                    notes=batch_data.get('notes', ''),
                    user_id=user_id
                )
                result = {'batch_id': batch_id}
            
            elif action == 'update':
                success = self.nursery_manager.update_seedling_batch(
                    batch_id=batch_data.get('id', 0),
                    nursery_id=batch_data.get('nursery_id', None),
                    plant_type=batch_data.get('plant_type', None),
                    variety=batch_data.get('variety', None),
                    quantity=batch_data.get('quantity', None),
                    planting_date=batch_data.get('planting_date', None),
                    expected_ready_date=batch_data.get('expected_ready_date', None),
                    season=batch_data.get('season', None),
                    customer_name=batch_data.get('customer_name', None),
                    reservation_date=batch_data.get('reservation_date', None),
                    delivery_date=batch_data.get('delivery_date', None),
                    notes=batch_data.get('notes', None),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.nursery_manager.delete_seedling_batch(
                    batch_id=batch_data.get('id', 0),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'get':
                batch = self.nursery_manager.get_seedling_batch(batch_data.get('id', 0))
                result = batch
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"اكتمال_{action}_دفعة_شتلات",
                entity_type="seedling_batch",
                entity_id=batch_data.get('id', 0),
                details=f"اكتمال {action} دفعة شتلات: {batch_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"خطأ_{action}_دفعة_شتلات",
                entity_type="seedling_batch",
                entity_id=batch_data.get('id', 0),
                details=f"خطأ في {action} دفعة شتلات: {batch_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة دفعة الشتلات: {str(e)}")
            raise
    
    def manage_variety_trial(self, action: str, trial_data: Dict, user_id: int) -> Dict:
        """
        إدارة تجربة الأصناف
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            trial_data (Dict): بيانات تجربة الأصناف
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'manage_variety_trial'):
                raise PermissionError("ليس لديك صلاحية لإدارة تجارب الأصناف")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"بدء_{action}_تجربة_أصناف",
                entity_type="variety_trial",
                entity_id=trial_data.get('id', 0),
                details=f"بدء {action} تجربة أصناف: {trial_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                trial_id = self.variety_manager.add_trial(
                    name=trial_data.get('name', ''),
                    location=trial_data.get('location', ''),
                    start_date=trial_data.get('start_date', None),
                    end_date=trial_data.get('end_date', None),
                    area=trial_data.get('area', 0),
                    area_unit=trial_data.get('area_unit', 'فدان'),
                    reference_varieties=trial_data.get('reference_varieties', []),
                    test_varieties=trial_data.get('test_varieties', []),
                    notes=trial_data.get('notes', ''),
                    user_id=user_id
                )
                result = {'trial_id': trial_id}
            
            elif action == 'update':
                success = self.variety_manager.update_trial(
                    trial_id=trial_data.get('id', 0),
                    name=trial_data.get('name', None),
                    location=trial_data.get('location', None),
                    start_date=trial_data.get('start_date', None),
                    end_date=trial_data.get('end_date', None),
                    area=trial_data.get('area', None),
                    area_unit=trial_data.get('area_unit', None),
                    reference_varieties=trial_data.get('reference_varieties', None),
                    test_varieties=trial_data.get('test_varieties', None),
                    notes=trial_data.get('notes', None),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.variety_manager.delete_trial(
                    trial_id=trial_data.get('id', 0),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'get':
                trial = self.variety_manager.get_trial(trial_data.get('id', 0))
                result = trial
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"اكتمال_{action}_تجربة_أصناف",
                entity_type="variety_trial",
                entity_id=trial_data.get('id', 0),
                details=f"اكتمال {action} تجربة أصناف: {trial_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"خطأ_{action}_تجربة_أصناف",
                entity_type="variety_trial",
                entity_id=trial_data.get('id', 0),
                details=f"خطأ في {action} تجربة أصناف: {trial_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة تجربة الأصناف: {str(e)}")
            raise
    
    def add_variety_evaluation(self, trial_id: int, variety_id: int, 
                              evaluation_data: Dict, user_id: int) -> int:
        """
        إضافة تقييم صنف
        
        المعلمات:
            trial_id (int): معرف التجربة
            variety_id (int): معرف الصنف
            evaluation_data (Dict): بيانات التقييم
            user_id (int): معرف المستخدم
            
        العائد:
            int: معرف التقييم
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'add_variety_evaluation'):
                raise PermissionError("ليس لديك صلاحية لإضافة تقييمات الأصناف")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_إضافة_تقييم_صنف",
                entity_type="variety_evaluation",
                entity_id=0,
                details=f"بدء إضافة تقييم صنف {variety_id} في تجربة {trial_id}"
            )
            
            # إضافة التقييم
            evaluation_id = self.variety_manager.add_evaluation(
                trial_id=trial_id,
                variety_id=variety_id,
                evaluation_date=evaluation_data.get('evaluation_date', None),
                fruit_color=evaluation_data.get('fruit_color', ''),
                fruit_size=evaluation_data.get('fruit_size', ''),
                fruit_shape=evaluation_data.get('fruit_shape', ''),
                tolerance=evaluation_data.get('tolerance', ''),
                resistance=evaluation_data.get('resistance', ''),
                yield_amount=evaluation_data.get('yield_amount', 0),
                yield_unit=evaluation_data.get('yield_unit', 'كجم'),
                quality_score=evaluation_data.get('quality_score', 0),
                notes=evaluation_data.get('notes', ''),
                images=evaluation_data.get('images', []),
                user_id=user_id
            )
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_إضافة_تقييم_صنف",
                entity_type="variety_evaluation",
                entity_id=evaluation_id,
                details=f"اكتمال إضافة تقييم صنف {variety_id} في تجربة {trial_id}"
            )
            
            return evaluation_id
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_إضافة_تقييم_صنف",
                entity_type="variety_evaluation",
                entity_id=0,
                details=f"خطأ في إضافة تقييم صنف {variety_id} في تجربة {trial_id} - {str(e)}"
            )
            
            logger.error(f"خطأ في إضافة تقييم صنف: {str(e)}")
            raise
    
    def compare_varieties(self, trial_id: int, variety_ids: List[int], 
                         attributes: List[str], user_id: int) -> Dict:
        """
        مقارنة الأصناف
        
        المعلمات:
            trial_id (int): معرف التجربة
            variety_ids (List[int]): قائمة معرفات الأصناف
            attributes (List[str]): قائمة الصفات للمقارنة
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتائج المقارنة
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'compare_varieties'):
                raise PermissionError("ليس لديك صلاحية لمقارنة الأصناف")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_مقارنة_أصناف",
                entity_type="variety_comparison",
                entity_id=0,
                details=f"بدء مقارنة الأصناف {variety_ids} في تجربة {trial_id}"
            )
            
            # مقارنة الأصناف
            comparison_results = self.variety_manager.compare_varieties(
                trial_id=trial_id,
                variety_ids=variety_ids,
                attributes=attributes
            )
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_مقارنة_أصناف",
                entity_type="variety_comparison",
                entity_id=0,
                details=f"اكتمال مقارنة الأصناف {variety_ids} في تجربة {trial_id}"
            )
            
            return comparison_results
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_مقارنة_أصناف",
                entity_type="variety_comparison",
                entity_id=0,
                details=f"خطأ في مقارنة الأصناف {variety_ids} في تجربة {trial_id} - {str(e)}"
            )
            
            logger.error(f"خطأ في مقارنة الأصناف: {str(e)}")
            raise
    
    def manage_inventory(self, action: str, item_data: Dict, user_id: int) -> Dict:
        """
        إدارة المخزون
        
        المعلمات:
            action (str): الإجراء (add، use، adjust، get)
            item_data (Dict): بيانات العنصر
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'manage_inventory'):
                raise PermissionError("ليس لديك صلاحية لإدارة المخزون")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"بدء_{action}_مخزون",
                entity_type="inventory",
                entity_id=item_data.get('id', 0),
                details=f"بدء {action} مخزون: {item_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                item_id = self.inventory_manager.add_item(
                    name=item_data.get('name', ''),
                    category=item_data.get('category', ''),
                    quantity=item_data.get('quantity', 0),
                    unit=item_data.get('unit', ''),
                    unit_cost=item_data.get('unit_cost', 0),
                    min_threshold=item_data.get('min_threshold', 0),
                    expiry_date=item_data.get('expiry_date', None),
                    supplier=item_data.get('supplier', ''),
                    location=item_data.get('location', ''),
                    notes=item_data.get('notes', ''),
                    user_id=user_id
                )
                result = {'item_id': item_id}
            
            elif action == 'use':
                success = self.inventory_manager.use_item(
                    item_id=item_data.get('id', 0),
                    quantity=item_data.get('quantity', 0),
                    farm_id=item_data.get('farm_id', None),
                    crop_id=item_data.get('crop_id', None),
                    notes=item_data.get('notes', ''),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'adjust':
                success = self.inventory_manager.adjust_item(
                    item_id=item_data.get('id', 0),
                    new_quantity=item_data.get('new_quantity', 0),
                    reason=item_data.get('reason', ''),
                    user_id=user_id
                )
                result = {'success': success}
            
            elif action == 'get':
                item = self.inventory_manager.get_item(item_data.get('id', 0))
                result = item
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"اكتمال_{action}_مخزون",
                entity_type="inventory",
                entity_id=item_data.get('id', 0),
                details=f"اكتمال {action} مخزون: {item_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type=f"خطأ_{action}_مخزون",
                entity_type="inventory",
                entity_id=item_data.get('id', 0),
                details=f"خطأ في {action} مخزون: {item_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة المخزون: {str(e)}")
            raise
    
    def generate_financial_report(self, report_type: str, entity_id: int, 
                                 start_date: Optional[datetime.datetime] = None,
                                 end_date: Optional[datetime.datetime] = None,
                                 format: str = 'pdf', user_id: int = 1) -> str:
        """
        إنشاء تقرير مالي
        
        المعلمات:
            report_type (str): نوع التقرير (farm، crop، overall، cost_per_area، profitability)
            entity_id (int): معرف الكيان (المزرعة، المحصول)
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            format (str): تنسيق التقرير (pdf، excel، csv، json)
            user_id (int): معرف المستخدم
            
        العائد:
            str: مسار ملف التقرير
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'generate_financial_report'):
                raise PermissionError("ليس لديك صلاحية لإنشاء التقارير المالية")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_إنشاء_تقرير_مالي",
                entity_type="financial_report",
                entity_id=0,
                details=f"بدء إنشاء تقرير مالي من نوع {report_type}"
            )
            
            # إنشاء التقرير
            report_path = ""
            
            if report_type == 'farm':
                report_path = self.financial_reporting.generate_farm_financial_report(
                    farm_id=entity_id,
                    start_date=start_date,
                    end_date=end_date,
                    format=format
                )
            
            elif report_type == 'crop':
                report_path = self.financial_reporting.generate_crop_financial_report(
                    crop_id=entity_id,
                    start_date=start_date,
                    end_date=end_date,
                    format=format
                )
            
            elif report_type == 'overall':
                report_path = self.financial_reporting.generate_overall_financial_report(
                    start_date=start_date,
                    end_date=end_date,
                    format=format
                )
            
            elif report_type == 'cost_per_area':
                report_path = self.financial_reporting.generate_cost_per_area_report(
                    farm_id=entity_id,
                    start_date=start_date,
                    end_date=end_date,
                    format=format
                )
            
            elif report_type == 'profitability':
                report_path = self.financial_reporting.generate_profitability_analysis(
                    start_date=start_date,
                    end_date=end_date,
                    format=format
                )
            
            else:
                raise ValueError(f"نوع تقرير غير صالح: {report_type}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_إنشاء_تقرير_مالي",
                entity_type="financial_report",
                entity_id=0,
                details=f"اكتمال إنشاء تقرير مالي من نوع {report_type}: {report_path}"
            )
            
            return report_path
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_إنشاء_تقرير_مالي",
                entity_type="financial_report",
                entity_id=0,
                details=f"خطأ في إنشاء تقرير مالي من نوع {report_type} - {str(e)}"
            )
            
            logger.error(f"خطأ في إنشاء تقرير مالي: {str(e)}")
            raise
    
    def generate_financial_dashboard(self, 
                                    start_date: Optional[datetime.datetime] = None,
                                    end_date: Optional[datetime.datetime] = None,
                                    user_id: int = 1) -> str:
        """
        إنشاء لوحة معلومات مالية
        
        المعلمات:
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            user_id (int): معرف المستخدم
            
        العائد:
            str: مسار ملف لوحة المعلومات
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'generate_financial_dashboard'):
                raise PermissionError("ليس لديك صلاحية لإنشاء لوحة المعلومات المالية")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_إنشاء_لوحة_معلومات_مالية",
                entity_type="financial_dashboard",
                entity_id=0,
                details="بدء إنشاء لوحة معلومات مالية"
            )
            
            # إنشاء لوحة المعلومات
            dashboard_path = self.financial_reporting.generate_financial_dashboard(
                start_date=start_date,
                end_date=end_date
            )
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_إنشاء_لوحة_معلومات_مالية",
                entity_type="financial_dashboard",
                entity_id=0,
                details=f"اكتمال إنشاء لوحة معلومات مالية: {dashboard_path}"
            )
            
            return dashboard_path
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_إنشاء_لوحة_معلومات_مالية",
                entity_type="financial_dashboard",
                entity_id=0,
                details=f"خطأ في إنشاء لوحة معلومات مالية - {str(e)}"
            )
            
            logger.error(f"خطأ في إنشاء لوحة معلومات مالية: {str(e)}")
            raise
    
    def ask_ai_assistant(self, query: str, user_id: int, 
                        assistant_type: str = 'free') -> Dict:
        """
        سؤال المساعد الذكي
        
        المعلمات:
            query (str): السؤال
            user_id (int): معرف المستخدم
            assistant_type (str): نوع المساعد (free، premium)
            
        العائد:
            Dict: إجابة المساعد الذكي
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'use_ai_assistant'):
                raise PermissionError("ليس لديك صلاحية لاستخدام المساعد الذكي")
            
            # التحقق من صلاحية استخدام المساعد المدفوع
            if assistant_type == 'premium' and not self.auth_manager.check_permission(user_id, 'use_premium_assistant'):
                raise PermissionError("ليس لديك صلاحية لاستخدام المساعد الذكي المدفوع")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_سؤال_المساعد_الذكي",
                entity_type="ai_assistant",
                entity_id=0,
                details=f"بدء سؤال المساعد الذكي ({assistant_type}): {query}"
            )
            
            # سؤال المساعد الذكي
            answer = self.ai_assistant.ask(
                query=query,
                user_id=user_id,
                assistant_type=assistant_type
            )
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_سؤال_المساعد_الذكي",
                entity_type="ai_assistant",
                entity_id=0,
                details=f"اكتمال سؤال المساعد الذكي ({assistant_type}): {query}"
            )
            
            return answer
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_سؤال_المساعد_الذكي",
                entity_type="ai_assistant",
                entity_id=0,
                details=f"خطأ في سؤال المساعد الذكي ({assistant_type}): {query} - {str(e)}"
            )
            
            logger.error(f"خطأ في سؤال المساعد الذكي: {str(e)}")
            raise
    
    def manage_user(self, action: str, user_data: Dict, admin_id: int) -> Dict:
        """
        إدارة المستخدم
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            user_data (Dict): بيانات المستخدم
            admin_id (int): معرف المسؤول
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المسؤول
            if not self.auth_manager.check_permission(admin_id, 'manage_users'):
                raise PermissionError("ليس لديك صلاحية لإدارة المستخدمين")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"بدء_{action}_مستخدم",
                entity_type="user",
                entity_id=user_data.get('id', 0),
                details=f"بدء {action} مستخدم: {user_data.get('username', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                user_id = self.auth_manager.add_user(
                    username=user_data.get('username', ''),
                    password=user_data.get('password', ''),
                    email=user_data.get('email', ''),
                    full_name=user_data.get('full_name', ''),
                    role=user_data.get('role', 'user'),
                    organization_id=user_data.get('organization_id', None),
                    country_id=user_data.get('country_id', None),
                    company_id=user_data.get('company_id', None),
                    is_active=user_data.get('is_active', True),
                    admin_id=admin_id
                )
                result = {'user_id': user_id}
            
            elif action == 'update':
                success = self.auth_manager.update_user(
                    user_id=user_data.get('id', 0),
                    username=user_data.get('username', None),
                    password=user_data.get('password', None),
                    email=user_data.get('email', None),
                    full_name=user_data.get('full_name', None),
                    role=user_data.get('role', None),
                    organization_id=user_data.get('organization_id', None),
                    country_id=user_data.get('country_id', None),
                    company_id=user_data.get('company_id', None),
                    is_active=user_data.get('is_active', None),
                    admin_id=admin_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.auth_manager.delete_user(
                    user_id=user_data.get('id', 0),
                    admin_id=admin_id
                )
                result = {'success': success}
            
            elif action == 'get':
                user = self.auth_manager.get_user(user_data.get('id', 0))
                result = user
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"اكتمال_{action}_مستخدم",
                entity_type="user",
                entity_id=user_data.get('id', 0),
                details=f"اكتمال {action} مستخدم: {user_data.get('username', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"خطأ_{action}_مستخدم",
                entity_type="user",
                entity_id=user_data.get('id', 0),
                details=f"خطأ في {action} مستخدم: {user_data.get('username', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة المستخدم: {str(e)}")
            raise
    
    def manage_organization(self, action: str, org_data: Dict, admin_id: int) -> Dict:
        """
        إدارة المؤسسة
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            org_data (Dict): بيانات المؤسسة
            admin_id (int): معرف المسؤول
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المسؤول
            if not self.auth_manager.check_permission(admin_id, 'manage_organizations'):
                raise PermissionError("ليس لديك صلاحية لإدارة المؤسسات")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"بدء_{action}_مؤسسة",
                entity_type="organization",
                entity_id=org_data.get('id', 0),
                details=f"بدء {action} مؤسسة: {org_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                org_id = self.organization_manager.add_organization(
                    name=org_data.get('name', ''),
                    country_id=org_data.get('country_id', None),
                    address=org_data.get('address', ''),
                    contact_info=org_data.get('contact_info', ''),
                    admin_id=admin_id
                )
                result = {'organization_id': org_id}
            
            elif action == 'update':
                success = self.organization_manager.update_organization(
                    organization_id=org_data.get('id', 0),
                    name=org_data.get('name', None),
                    country_id=org_data.get('country_id', None),
                    address=org_data.get('address', None),
                    contact_info=org_data.get('contact_info', None),
                    admin_id=admin_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.organization_manager.delete_organization(
                    organization_id=org_data.get('id', 0),
                    admin_id=admin_id
                )
                result = {'success': success}
            
            elif action == 'get':
                org = self.organization_manager.get_organization(org_data.get('id', 0))
                result = org
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"اكتمال_{action}_مؤسسة",
                entity_type="organization",
                entity_id=org_data.get('id', 0),
                details=f"اكتمال {action} مؤسسة: {org_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"خطأ_{action}_مؤسسة",
                entity_type="organization",
                entity_id=org_data.get('id', 0),
                details=f"خطأ في {action} مؤسسة: {org_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة المؤسسة: {str(e)}")
            raise
    
    def manage_country(self, action: str, country_data: Dict, admin_id: int) -> Dict:
        """
        إدارة الدولة
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            country_data (Dict): بيانات الدولة
            admin_id (int): معرف المسؤول
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المسؤول
            if not self.auth_manager.check_permission(admin_id, 'manage_countries'):
                raise PermissionError("ليس لديك صلاحية لإدارة الدول")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"بدء_{action}_دولة",
                entity_type="country",
                entity_id=country_data.get('id', 0),
                details=f"بدء {action} دولة: {country_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                country_id = self.organization_manager.add_country(
                    name=country_data.get('name', ''),
                    code=country_data.get('code', ''),
                    admin_id=admin_id
                )
                result = {'country_id': country_id}
            
            elif action == 'update':
                success = self.organization_manager.update_country(
                    country_id=country_data.get('id', 0),
                    name=country_data.get('name', None),
                    code=country_data.get('code', None),
                    admin_id=admin_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.organization_manager.delete_country(
                    country_id=country_data.get('id', 0),
                    admin_id=admin_id
                )
                result = {'success': success}
            
            elif action == 'get':
                country = self.organization_manager.get_country(country_data.get('id', 0))
                result = country
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"اكتمال_{action}_دولة",
                entity_type="country",
                entity_id=country_data.get('id', 0),
                details=f"اكتمال {action} دولة: {country_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"خطأ_{action}_دولة",
                entity_type="country",
                entity_id=country_data.get('id', 0),
                details=f"خطأ في {action} دولة: {country_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة الدولة: {str(e)}")
            raise
    
    def manage_company(self, action: str, company_data: Dict, admin_id: int) -> Dict:
        """
        إدارة الشركة
        
        المعلمات:
            action (str): الإجراء (add، update، delete، get)
            company_data (Dict): بيانات الشركة
            admin_id (int): معرف المسؤول
            
        العائد:
            Dict: نتيجة الإجراء
        """
        try:
            # التحقق من صلاحيات المسؤول
            if not self.auth_manager.check_permission(admin_id, 'manage_companies'):
                raise PermissionError("ليس لديك صلاحية لإدارة الشركات")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"بدء_{action}_شركة",
                entity_type="company",
                entity_id=company_data.get('id', 0),
                details=f"بدء {action} شركة: {company_data.get('name', '')}"
            )
            
            # تنفيذ الإجراء
            result = {}
            
            if action == 'add':
                company_id = self.organization_manager.add_company(
                    name=company_data.get('name', ''),
                    country_id=company_data.get('country_id', None),
                    organization_id=company_data.get('organization_id', None),
                    address=company_data.get('address', ''),
                    contact_info=company_data.get('contact_info', ''),
                    admin_id=admin_id
                )
                result = {'company_id': company_id}
            
            elif action == 'update':
                success = self.organization_manager.update_company(
                    company_id=company_data.get('id', 0),
                    name=company_data.get('name', None),
                    country_id=company_data.get('country_id', None),
                    organization_id=company_data.get('organization_id', None),
                    address=company_data.get('address', None),
                    contact_info=company_data.get('contact_info', None),
                    admin_id=admin_id
                )
                result = {'success': success}
            
            elif action == 'delete':
                success = self.organization_manager.delete_company(
                    company_id=company_data.get('id', 0),
                    admin_id=admin_id
                )
                result = {'success': success}
            
            elif action == 'get':
                company = self.organization_manager.get_company(company_data.get('id', 0))
                result = company
            
            else:
                raise ValueError(f"إجراء غير صالح: {action}")
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"اكتمال_{action}_شركة",
                entity_type="company",
                entity_id=company_data.get('id', 0),
                details=f"اكتمال {action} شركة: {company_data.get('name', '')}"
            )
            
            return result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=admin_id,
                action_type=f"خطأ_{action}_شركة",
                entity_type="company",
                entity_id=company_data.get('id', 0),
                details=f"خطأ في {action} شركة: {company_data.get('name', '')} - {str(e)}"
            )
            
            logger.error(f"خطأ في إدارة الشركة: {str(e)}")
            raise
    
    def import_data(self, data_file: str, data_type: str, 
                   merge_mode: str = 'new', user_id: int = 1) -> Dict:
        """
        استيراد البيانات
        
        المعلمات:
            data_file (str): مسار ملف البيانات
            data_type (str): نوع البيانات
            merge_mode (str): وضع الدمج (new، merge)
            user_id (int): معرف المستخدم
            
        العائد:
            Dict: نتيجة الاستيراد
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'import_data'):
                raise PermissionError("ليس لديك صلاحية لاستيراد البيانات")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_استيراد_بيانات",
                entity_type="data_import",
                entity_id=0,
                details=f"بدء استيراد بيانات من نوع {data_type} من الملف {data_file}"
            )
            
            # التحقق من جودة البيانات
            validation_result = self.data_quality_monitor.validate_import_data(
                data_file=data_file,
                data_type=data_type
            )
            
            if not validation_result['is_valid']:
                raise ValueError(f"البيانات غير صالحة: {validation_result['errors']}")
            
            # التحقق من نسبة التشوه
            distortion_result = self.data_quality_monitor.check_data_distortion(
                data_file=data_file,
                data_type=data_type
            )
            
            if distortion_result['distortion_percentage'] > 5:
                raise ValueError(f"نسبة التشوه في البيانات تتجاوز 5%: {distortion_result['distortion_percentage']}%")
            
            # استيراد البيانات
            import_result = self.data_manager.import_data(
                data_file=data_file,
                data_type=data_type,
                merge_mode=merge_mode,
                user_id=user_id
            )
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_استيراد_بيانات",
                entity_type="data_import",
                entity_id=0,
                details=f"اكتمال استيراد بيانات من نوع {data_type} من الملف {data_file}"
            )
            
            return import_result
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_استيراد_بيانات",
                entity_type="data_import",
                entity_id=0,
                details=f"خطأ في استيراد بيانات من نوع {data_type} من الملف {data_file} - {str(e)}"
            )
            
            logger.error(f"خطأ في استيراد البيانات: {str(e)}")
            raise
    
    def export_data(self, data_type: str, output_file: str, 
                   filters: Dict = None, user_id: int = 1) -> str:
        """
        تصدير البيانات
        
        المعلمات:
            data_type (str): نوع البيانات
            output_file (str): مسار ملف الإخراج
            filters (Dict): مرشحات البيانات
            user_id (int): معرف المستخدم
            
        العائد:
            str: مسار ملف التصدير
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'export_data'):
                raise PermissionError("ليس لديك صلاحية لتصدير البيانات")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_تصدير_بيانات",
                entity_type="data_export",
                entity_id=0,
                details=f"بدء تصدير بيانات من نوع {data_type} إلى الملف {output_file}"
            )
            
            # تصدير البيانات
            export_file = self.data_manager.export_data(
                data_type=data_type,
                output_file=output_file,
                filters=filters,
                user_id=user_id
            )
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_تصدير_بيانات",
                entity_type="data_export",
                entity_id=0,
                details=f"اكتمال تصدير بيانات من نوع {data_type} إلى الملف {export_file}"
            )
            
            return export_file
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_تصدير_بيانات",
                entity_type="data_export",
                entity_id=0,
                details=f"خطأ في تصدير بيانات من نوع {data_type} إلى الملف {output_file} - {str(e)}"
            )
            
            logger.error(f"خطأ في تصدير البيانات: {str(e)}")
            raise
    
    def backup_data(self, backup_dir: str, user_id: int = 1) -> str:
        """
        نسخ البيانات احتياطيًا
        
        المعلمات:
            backup_dir (str): مجلد النسخ الاحتياطي
            user_id (int): معرف المستخدم
            
        العائد:
            str: مسار ملف النسخ الاحتياطي
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'backup_data'):
                raise PermissionError("ليس لديك صلاحية لنسخ البيانات احتياطيًا")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_نسخ_احتياطي",
                entity_type="data_backup",
                entity_id=0,
                details=f"بدء نسخ البيانات احتياطيًا إلى المجلد {backup_dir}"
            )
            
            # نسخ البيانات احتياطيًا
            backup_file = self.data_manager.backup_data(
                backup_dir=backup_dir,
                user_id=user_id
            )
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_نسخ_احتياطي",
                entity_type="data_backup",
                entity_id=0,
                details=f"اكتمال نسخ البيانات احتياطيًا إلى الملف {backup_file}"
            )
            
            return backup_file
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_نسخ_احتياطي",
                entity_type="data_backup",
                entity_id=0,
                details=f"خطأ في نسخ البيانات احتياطيًا إلى المجلد {backup_dir} - {str(e)}"
            )
            
            logger.error(f"خطأ في نسخ البيانات احتياطيًا: {str(e)}")
            raise
    
    def restore_data(self, backup_file: str, user_id: int = 1) -> bool:
        """
        استعادة البيانات من نسخة احتياطية
        
        المعلمات:
            backup_file (str): مسار ملف النسخة الاحتياطية
            user_id (int): معرف المستخدم
            
        العائد:
            bool: نجاح العملية
        """
        try:
            # التحقق من صلاحيات المستخدم
            if not self.auth_manager.check_permission(user_id, 'restore_data'):
                raise PermissionError("ليس لديك صلاحية لاستعادة البيانات من نسخة احتياطية")
            
            # تسجيل بدء الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="بدء_استعادة_بيانات",
                entity_type="data_restore",
                entity_id=0,
                details=f"بدء استعادة البيانات من الملف {backup_file}"
            )
            
            # استعادة البيانات
            success = self.data_manager.restore_data(
                backup_file=backup_file,
                user_id=user_id
            )
            
            # تسجيل اكتمال الإجراء
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="اكتمال_استعادة_بيانات",
                entity_type="data_restore",
                entity_id=0,
                details=f"اكتمال استعادة البيانات من الملف {backup_file}"
            )
            
            return success
        
        except Exception as e:
            # تسجيل الخطأ
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_استعادة_بيانات",
                entity_type="data_restore",
                entity_id=0,
                details=f"خطأ في استعادة البيانات من الملف {backup_file} - {str(e)}"
            )
            
            logger.error(f"خطأ في استعادة البيانات من نسخة احتياطية: {str(e)}")
            raise
    
    def login(self, username: str, password: str) -> Dict:
        """
        تسجيل الدخول
        
        المعلمات:
            username (str): اسم المستخدم
            password (str): كلمة المرور
            
        العائد:
            Dict: معلومات المستخدم وتوكن الجلسة
        """
        try:
            # تسجيل محاولة تسجيل الدخول
            self.audit_manager.log_action(
                user_id=0,  # غير معروف بعد
                action_type="محاولة_تسجيل_دخول",
                entity_type="auth",
                entity_id=0,
                details=f"محاولة تسجيل دخول للمستخدم: {username}"
            )
            
            # تسجيل الدخول
            login_result = self.auth_manager.login(
                username=username,
                password=password
            )
            
            if login_result['success']:
                # تسجيل نجاح تسجيل الدخول
                self.audit_manager.log_action(
                    user_id=login_result['user_id'],
                    action_type="نجاح_تسجيل_دخول",
                    entity_type="auth",
                    entity_id=login_result['user_id'],
                    details=f"نجاح تسجيل دخول للمستخدم: {username}"
                )
            else:
                # تسجيل فشل تسجيل الدخول
                self.audit_manager.log_action(
                    user_id=0,  # غير معروف
                    action_type="فشل_تسجيل_دخول",
                    entity_type="auth",
                    entity_id=0,
                    details=f"فشل تسجيل دخول للمستخدم: {username} - {login_result.get('message', '')}"
                )
            
            return login_result
        
        except Exception as e:
            # تسجيل خطأ تسجيل الدخول
            self.audit_manager.log_action(
                user_id=0,  # غير معروف
                action_type="خطأ_تسجيل_دخول",
                entity_type="auth",
                entity_id=0,
                details=f"خطأ في تسجيل دخول للمستخدم: {username} - {str(e)}"
            )
            
            logger.error(f"خطأ في تسجيل الدخول: {str(e)}")
            raise
    
    def logout(self, user_id: int, session_token: str) -> bool:
        """
        تسجيل الخروج
        
        المعلمات:
            user_id (int): معرف المستخدم
            session_token (str): توكن الجلسة
            
        العائد:
            bool: نجاح العملية
        """
        try:
            # تسجيل محاولة تسجيل الخروج
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="محاولة_تسجيل_خروج",
                entity_type="auth",
                entity_id=user_id,
                details=f"محاولة تسجيل خروج للمستخدم: {user_id}"
            )
            
            # تسجيل الخروج
            logout_result = self.auth_manager.logout(
                user_id=user_id,
                session_token=session_token
            )
            
            if logout_result:
                # تسجيل نجاح تسجيل الخروج
                self.audit_manager.log_action(
                    user_id=user_id,
                    action_type="نجاح_تسجيل_خروج",
                    entity_type="auth",
                    entity_id=user_id,
                    details=f"نجاح تسجيل خروج للمستخدم: {user_id}"
                )
            else:
                # تسجيل فشل تسجيل الخروج
                self.audit_manager.log_action(
                    user_id=user_id,
                    action_type="فشل_تسجيل_خروج",
                    entity_type="auth",
                    entity_id=user_id,
                    details=f"فشل تسجيل خروج للمستخدم: {user_id}"
                )
            
            return logout_result
        
        except Exception as e:
            # تسجيل خطأ تسجيل الخروج
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="خطأ_تسجيل_خروج",
                entity_type="auth",
                entity_id=user_id,
                details=f"خطأ في تسجيل خروج للمستخدم: {user_id} - {str(e)}"
            )
            
            logger.error(f"خطأ في تسجيل الخروج: {str(e)}")
            raise
    
    def run_system_test(self) -> Dict:
        """
        تشغيل اختبار النظام
        
        العائد:
            Dict: نتائج الاختبار
        """
        try:
            logger.info("بدء اختبار النظام")
            
            # قائمة الاختبارات
            tests = [
                "test_disease_detection",
                "test_nutrient_analysis",
                "test_breeding_prediction",
                "test_treatment_recommendation",
                "test_web_search",
                "test_image_search",
                "test_soil_analysis",
                "test_farm_management",
                "test_nursery_management",
                "test_variety_comparison",
                "test_inventory_management",
                "test_financial_reporting",
                "test_ai_assistant",
                "test_user_management",
                "test_organization_management",
                "test_data_management",
                "test_authentication"
            ]
            
            # نتائج الاختبارات
            results = {}
            
            # تنفيذ الاختبارات
            for test in tests:
                try:
                    logger.info(f"تنفيذ اختبار: {test}")
                    
                    # تنفيذ الاختبار
                    if hasattr(self, test) and callable(getattr(self, test)):
                        test_result = getattr(self, test)()
                        results[test] = {
                            "status": "success",
                            "result": test_result
                        }
                    else:
                        results[test] = {
                            "status": "skipped",
                            "message": "الاختبار غير متوفر"
                        }
                
                except Exception as e:
                    logger.error(f"خطأ في اختبار {test}: {str(e)}")
                    results[test] = {
                        "status": "failed",
                        "error": str(e)
                    }
            
            # تلخيص النتائج
            summary = {
                "total_tests": len(tests),
                "successful_tests": sum(1 for test in results if results[test]["status"] == "success"),
                "failed_tests": sum(1 for test in results if results[test]["status"] == "failed"),
                "skipped_tests": sum(1 for test in results if results[test]["status"] == "skipped"),
                "results": results
            }
            
            logger.info(f"اكتمال اختبار النظام: {summary['successful_tests']} ناجح، {summary['failed_tests']} فاشل، {summary['skipped_tests']} متخطى")
            
            return summary
        
        except Exception as e:
            logger.error(f"خطأ في تشغيل اختبار النظام: {str(e)}")
            raise

def main():
    """
    الدالة الرئيسية
    """
    # تحليل المعلمات
    parser = argparse.ArgumentParser(description="نظام الذكاء الاصطناعي الزراعي المتكامل")
    parser.add_argument("--config", help="مسار ملف التكوين")
    parser.add_argument("--test", action="store_true", help="تشغيل اختبار النظام")
    args = parser.parse_args()
    
    try:
        # تهيئة النظام
        system = IntegratedAgriculturalAISystem(config_path=args.config)
        
        # تشغيل اختبار النظام إذا تم تحديد المعلمة
        if args.test:
            test_results = system.run_system_test()
            print(json.dumps(test_results, indent=2, ensure_ascii=False))
        
        # يمكن إضافة المزيد من الوظائف هنا
        
    except Exception as e:
        logger.error(f"خطأ في تشغيل النظام: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
