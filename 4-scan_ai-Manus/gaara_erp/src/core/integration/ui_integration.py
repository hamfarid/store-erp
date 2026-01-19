"""
وحدة تكامل واجهات المستخدم بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي

هذه الوحدة مسؤولة عن:
1. عرض بيانات نظام الذكاء الاصطناعي في واجهات نظام ERP
2. إرسال البيانات من واجهات نظام ERP إلى نظام الذكاء الاصطناعي
3. توفير واجهات موحدة للتفاعل مع كلا النظامين
4. عرض نتائج تحليلات الذكاء الاصطناعي بشكل مرئي
"""

import os
import json
import logging
import requests
from datetime import datetime
from flask import render_template, jsonify, request, Blueprint, current_app
from werkzeug.utils import secure_filename

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ui_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ui_integration")

class UIIntegration:
    """فئة تكامل واجهات المستخدم بين نظام Gaara ERP ونظام الذكاء الاصطناعي الزراعي"""
    
    def __init__(self, config_path=None):
        """
        تهيئة وحدة تكامل واجهات المستخدم
        
        المعلمات:
            config_path (str): مسار ملف التكوين (اختياري)
        """
        self.config = self._load_config(config_path)
        self.ai_api_url = self.config.get('ai_api_url', 'http://localhost:8000/api')
        self.api_key = self.config.get('api_key', '')
        self.upload_folder = self.config.get('upload_folder', '/tmp/uploads')
        
        # إنشاء مجلد التحميل إذا لم يكن موجوداً
        os.makedirs(self.upload_folder, exist_ok=True)
        
        logger.info("تم تهيئة وحدة تكامل واجهات المستخدم بنجاح")
    
    def _load_config(self, config_path):
        """
        تحميل ملف التكوين
        
        المعلمات:
            config_path (str): مسار ملف التكوين
            
        العوائد:
            dict: بيانات التكوين
        """
        default_config = {
            'ai_api_url': 'http://localhost:8000/api',
            'api_key': 'your_api_key_here',
            'upload_folder': '/tmp/uploads',
            'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif'],
            'max_file_size': 10 * 1024 * 1024,  # 10 ميجابايت
            'timeout': 30,  # ثانية
            'cache_timeout': 300,  # 5 دقائق
            'ui_components': {
                'disease_detection': {
                    'enabled': True,
                    'route': '/disease-detection',
                    'template': 'ai/disease_detection.html',
                    'api_endpoint': '/detect-disease'
                },
                'plant_breeding': {
                    'enabled': True,
                    'route': '/plant-breeding',
                    'template': 'ai/plant_breeding.html',
                    'api_endpoint': '/breeding-simulation'
                },
                'soil_analysis': {
                    'enabled': True,
                    'route': '/soil-analysis',
                    'template': 'ai/soil_analysis.html',
                    'api_endpoint': '/analyze-soil'
                },
                'crop_recommendation': {
                    'enabled': True,
                    'route': '/crop-recommendation',
                    'template': 'ai/crop_recommendation.html',
                    'api_endpoint': '/recommend-crop'
                },
                'yield_prediction': {
                    'enabled': True,
                    'route': '/yield-prediction',
                    'template': 'ai/yield_prediction.html',
                    'api_endpoint': '/predict-yield'
                }
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # دمج التكوين المخصص مع التكوين الافتراضي
                    for key, value in config.items():
                        if isinstance(value, dict) and key in default_config and isinstance(default_config[key], dict):
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
                logger.info(f"تم تحميل ملف التكوين من {config_path}")
            except Exception as e:
                logger.error(f"خطأ في تحميل ملف التكوين: {str(e)}")
        else:
            logger.warning("لم يتم تحديد ملف تكوين، استخدام الإعدادات الافتراضية")
        
        return default_config
    
    def create_blueprint(self):
        """
        إنشاء Blueprint لتكامل واجهات المستخدم
        
        العوائد:
            Blueprint: كائن Blueprint لتكامل واجهات المستخدم
        """
        ai_integration_bp = Blueprint('ai_integration', __name__, url_prefix='/ai')
        
        # تسجيل المسارات لمكونات واجهة المستخدم
        for component_name, component_config in self.config.get('ui_components', {}).items():
            if component_config.get('enabled', False):
                route = component_config.get('route')
                template = component_config.get('template')
                
                # إنشاء مسار لعرض الصفحة
                ai_integration_bp.add_url_rule(
                    route,
                    endpoint=f'view_{component_name}',
                    view_func=self._create_view_function(component_name, template),
                    methods=['GET']
                )
                
                # إنشاء مسار لمعالجة الطلبات
                ai_integration_bp.add_url_rule(
                    f'{route}/process',
                    endpoint=f'process_{component_name}',
                    view_func=self._create_process_function(component_name, component_config.get('api_endpoint')),
                    methods=['POST']
                )
                
                logger.info(f"تم تسجيل مسارات لمكون {component_name}")
        
        # مسار لعرض نتائج سابقة
        ai_integration_bp.add_url_rule(
            '/results/<result_id>',
            endpoint='view_result',
            view_func=self.view_result,
            methods=['GET']
        )
        
        # مسار لحالة نظام الذكاء الاصطناعي
        ai_integration_bp.add_url_rule(
            '/status',
            endpoint='ai_status',
            view_func=self.get_ai_status,
            methods=['GET']
        )
        
        # مسار للبحث في نتائج الذكاء الاصطناعي
        ai_integration_bp.add_url_rule(
            '/search',
            endpoint='search_results',
            view_func=self.search_results,
            methods=['GET', 'POST']
        )
        
        logger.info("تم إنشاء Blueprint لتكامل واجهات المستخدم")
        
        return ai_integration_bp
    
    def _create_view_function(self, component_name, template):
        """
        إنشاء دالة عرض لمكون واجهة المستخدم
        
        المعلمات:
            component_name (str): اسم المكون
            template (str): قالب المكون
            
        العوائد:
            function: دالة العرض
        """
        def view_function():
            # جلب البيانات المطلوبة من نظام الذكاء الاصطناعي
            context = self._get_component_context(component_name)
            return render_template(template, **context)
        
        return view_function
    
    def _create_process_function(self, component_name, api_endpoint):
        """
        إنشاء دالة معالجة لمكون واجهة المستخدم
        
        المعلمات:
            component_name (str): اسم المكون
            api_endpoint (str): نقطة نهاية API
            
        العوائد:
            function: دالة المعالجة
        """
        def process_function():
            try:
                # معالجة البيانات المرسلة
                data = {}
                files = {}
                
                # معالجة البيانات العادية
                for key, value in request.form.items():
                    data[key] = value
                
                # معالجة الملفات المرفقة
                for key, file in request.files.items():
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(self.upload_folder, filename)
                        file.save(file_path)
                        files[key] = (filename, open(file_path, 'rb'), file.content_type)
                
                # إرسال الطلب إلى نظام الذكاء الاصطناعي
                response = self._send_request_to_ai_system(api_endpoint, data, files)
                
                # إغلاق ملفات الملفات المرفقة
                for key, file_tuple in files.items():
                    file_tuple[1].close()
                
                # حفظ النتيجة في قاعدة البيانات
                result_id = self._save_result(component_name, data, response)
                
                # إعداد الاستجابة
                result = {
                    'success': True,
                    'result_id': result_id,
                    'data': response
                }
                
                return jsonify(result)
            
            except Exception as e:
                logger.error(f"خطأ في معالجة طلب {component_name}: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        return process_function
    
    def _get_component_context(self, component_name):
        """
        جلب سياق مكون واجهة المستخدم
        
        المعلمات:
            component_name (str): اسم المكون
            
        العوائد:
            dict: سياق المكون
        """
        context = {
            'component_name': component_name,
            'page_title': self._get_component_title(component_name)
        }
        
        try:
            # جلب البيانات المطلوبة حسب نوع المكون
            if component_name == 'disease_detection':
                # جلب قائمة الأمراض المعروفة
                diseases = self._get_known_diseases()
                context['diseases'] = diseases
                
                # جلب قائمة المحاصيل المدعومة
                crops = self._get_supported_crops()
                context['crops'] = crops
                
                # جلب آخر عمليات تشخيص
                recent_detections = self._get_recent_detections(limit=5)
                context['recent_detections'] = recent_detections
            
            elif component_name == 'plant_breeding':
                # جلب قائمة الأصناف المتاحة للتهجين
                varieties = self._get_available_varieties()
                context['varieties'] = varieties
                
                # جلب قائمة الصفات المستهدفة
                traits = self._get_target_traits()
                context['traits'] = traits
                
                # جلب آخر عمليات تهجين
                recent_breedings = self._get_recent_breedings(limit=5)
                context['recent_breedings'] = recent_breedings
            
            elif component_name == 'soil_analysis':
                # جلب قائمة أنواع التربة
                soil_types = self._get_soil_types()
                context['soil_types'] = soil_types
                
                # جلب قائمة العناصر الغذائية
                nutrients = self._get_soil_nutrients()
                context['nutrients'] = nutrients
                
                # جلب آخر تحليلات التربة
                recent_analyses = self._get_recent_soil_analyses(limit=5)
                context['recent_analyses'] = recent_analyses
            
            elif component_name == 'crop_recommendation':
                # جلب قائمة المناطق الزراعية
                regions = self._get_agricultural_regions()
                context['regions'] = regions
                
                # جلب قائمة المحاصيل المدعومة
                crops = self._get_supported_crops()
                context['crops'] = crops
                
                # جلب آخر توصيات المحاصيل
                recent_recommendations = self._get_recent_crop_recommendations(limit=5)
                context['recent_recommendations'] = recent_recommendations
            
            elif component_name == 'yield_prediction':
                # جلب قائمة المحاصيل المدعومة
                crops = self._get_supported_crops()
                context['crops'] = crops
                
                # جلب قائمة المناطق الزراعية
                regions = self._get_agricultural_regions()
                context['regions'] = regions
                
                # جلب آخر تنبؤات الإنتاج
                recent_predictions = self._get_recent_yield_predictions(limit=5)
                context['recent_predictions'] = recent_predictions
        
        except Exception as e:
            logger.error(f"خطأ في جلب سياق المكون {component_name}: {str(e)}")
            context['error'] = str(e)
        
        return context
    
    def _get_component_title(self, component_name):
        """
        الحصول على عنوان مكون واجهة المستخدم
        
        المعلمات:
            component_name (str): اسم المكون
            
        العوائد:
            str: عنوان المكون
        """
        titles = {
            'disease_detection': 'تشخيص أمراض النباتات',
            'plant_breeding': 'محاكاة تهجين النباتات',
            'soil_analysis': 'تحليل التربة',
            'crop_recommendation': 'توصية المحاصيل',
            'yield_prediction': 'التنبؤ بالإنتاج'
        }
        
        return titles.get(component_name, 'تكامل الذكاء الاصطناعي')
    
    def _send_request_to_ai_system(self, endpoint, data, files=None):
        """
        إرسال طلب إلى نظام الذكاء الاصطناعي
        
        المعلمات:
            endpoint (str): نقطة نهاية API
            data (dict): البيانات المرسلة
            files (dict): الملفات المرفقة (اختياري)
            
        العوائد:
            dict: استجابة نظام الذكاء الاصطناعي
        """
        url = f"{self.ai_api_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        timeout = self.config.get('timeout', 30)
        
        try:
            if files:
                # إرسال طلب مع ملفات مرفقة
                response = requests.post(url, data=data, files=files, headers=headers, timeout=timeout)
            else:
                # إرسال طلب بدون ملفات مرفقة
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في إرسال الطلب إلى نظام الذكاء الاصطناعي: {str(e)}")
            raise Exception(f"فشل الاتصال بنظام الذكاء الاصطناعي: {str(e)}")
    
    def _save_result(self, component_name, request_data, response_data):
        """
        حفظ نتيجة في قاعدة البيانات
        
        المعلمات:
            component_name (str): اسم المكون
            request_data (dict): بيانات الطلب
            response_data (dict): بيانات الاستجابة
            
        العوائد:
            str: معرف النتيجة
        """
        # توليد معرف فريد للنتيجة
        result_id = f"{component_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # إعداد بيانات النتيجة
        result = {
            'id': result_id,
            'component': component_name,
            'timestamp': datetime.now().isoformat(),
            'request': request_data,
            'response': response_data
        }
        
        # حفظ النتيجة في ملف JSON
        result_dir = os.path.join(self.upload_folder, 'results')
        os.makedirs(result_dir, exist_ok=True)
        
        result_file = os.path.join(result_dir, f"{result_id}.json")
        
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=4)
        
        logger.info(f"تم حفظ النتيجة {result_id}")
        
        return result_id
    
    def view_result(self, result_id):
        """
        عرض نتيجة سابقة
        
        المعلمات:
            result_id (str): معرف النتيجة
            
        العوائد:
            Response: استجابة Flask
        """
        try:
            # قراءة ملف النتيجة
            result_file = os.path.join(self.upload_folder, 'results', f"{result_id}.json")
            
            if not os.path.exists(result_file):
                return jsonify({
                    'success': False,
                    'error': 'النتيجة غير موجودة'
                }), 404
            
            with open(result_file, 'r') as f:
                result = json.load(f)
            
            # تحديد القالب المناسب
            component_name = result.get('component')
            template = self.config.get('ui_components', {}).get(component_name, {}).get('template', 'ai/result.html')
            
            # إعداد سياق العرض
            context = {
                'result': result,
                'page_title': f"نتيجة {self._get_component_title(component_name)}"
            }
            
            return render_template(template.replace('.html', '_result.html'), **context)
        
        except Exception as e:
            logger.error(f"خطأ في عرض النتيجة {result_id}: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_ai_status(self):
        """
        الحصول على حالة نظام الذكاء الاصطناعي
        
        العوائد:
            Response: استجابة Flask
        """
        try:
            # إرسال طلب للحصول على حالة نظام الذكاء الاصطناعي
            url = f"{self.ai_api_url}/status"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            status_data = response.json()
            
            # إعداد سياق العرض
            context = {
                'status': status_data,
                'page_title': 'حالة نظام الذكاء الاصطناعي'
            }
            
            return render_template('ai/status.html', **context)
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على حالة نظام الذكاء الاصطناعي: {str(e)}")
            
            # إعداد سياق العرض مع رسالة الخطأ
            context = {
                'status': {
                    'status': 'error',
                    'error': str(e)
                },
                'page_title': 'حالة نظام الذكاء الاصطناعي'
            }
            
            return render_template('ai/status.html', **context)
    
    def search_results(self):
        """
        البحث في نتائج الذكاء الاصطناعي
        
        العوائد:
            Response: استجابة Flask
        """
        try:
            # الحصول على معايير البحث
            if request.method == 'POST':
                search_criteria = request.form
            else:
                search_criteria = request.args
            
            component = search_criteria.get('component', '')
            start_date = search_criteria.get('start_date', '')
            end_date = search_criteria.get('end_date', '')
            keyword = search_criteria.get('keyword', '')
            
            # البحث في ملفات النتائج
            results = []
            result_dir = os.path.join(self.upload_folder, 'results')
            
            if os.path.exists(result_dir):
                for filename in os.listdir(result_dir):
                    if filename.endswith('.json'):
                        file_path = os.path.join(result_dir, filename)
                        
                        with open(file_path, 'r') as f:
                            result = json.load(f)
                        
                        # تطبيق معايير البحث
                        if component and result.get('component') != component:
                            continue
                        
                        timestamp = result.get('timestamp', '')
                        
                        if start_date and timestamp < start_date:
                            continue
                        
                        if end_date and timestamp > end_date:
                            continue
                        
                        if keyword:
                            # البحث في بيانات الطلب والاستجابة
                            request_str = json.dumps(result.get('request', {}), ensure_ascii=False).lower()
                            response_str = json.dumps(result.get('response', {}), ensure_ascii=False).lower()
                            
                            if keyword.lower() not in request_str and keyword.lower() not in response_str:
                                continue
                        
                        # إضافة النتيجة إلى قائمة النتائج
                        results.append(result)
            
            # ترتيب النتائج حسب التاريخ (الأحدث أولاً)
            results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            # إعداد سياق العرض
            context = {
                'results': results,
                'search_criteria': search_criteria,
                'components': self.config.get('ui_components', {}),
                'page_title': 'البحث في نتائج الذكاء الاصطناعي'
            }
            
            return render_template('ai/search.html', **context)
        
        except Exception as e:
            logger.error(f"خطأ في البحث في نتائج الذكاء الاصطناعي: {str(e)}")
            
            # إعداد سياق العرض مع رسالة الخطأ
            context = {
                'error': str(e),
                'search_criteria': {},
                'components': self.config.get('ui_components', {}),
                'page_title': 'البحث في نتائج الذكاء الاصطناعي'
            }
            
            return render_template('ai/search.html', **context)
    
    # دوال مساعدة لجلب البيانات من نظام الذكاء الاصطناعي
    
    def _get_known_diseases(self):
        """
        جلب قائمة الأمراض المعروفة
        
        العوائد:
            list: قائمة الأمراض المعروفة
        """
        try:
            url = f"{self.ai_api_url}/diseases"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('diseases', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب قائمة الأمراض المعروفة: {str(e)}")
            return []
    
    def _get_supported_crops(self):
        """
        جلب قائمة المحاصيل المدعومة
        
        العوائد:
            list: قائمة المحاصيل المدعومة
        """
        try:
            url = f"{self.ai_api_url}/crops"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('crops', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب قائمة المحاصيل المدعومة: {str(e)}")
            return []
    
    def _get_recent_detections(self, limit=5):
        """
        جلب آخر عمليات تشخيص
        
        المعلمات:
            limit (int): عدد النتائج المطلوبة
            
        العوائد:
            list: قائمة آخر عمليات تشخيص
        """
        try:
            url = f"{self.ai_api_url}/recent-detections?limit={limit}"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('detections', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب آخر عمليات تشخيص: {str(e)}")
            return []
    
    def _get_available_varieties(self):
        """
        جلب قائمة الأصناف المتاحة للتهجين
        
        العوائد:
            list: قائمة الأصناف المتاحة للتهجين
        """
        try:
            url = f"{self.ai_api_url}/varieties"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('varieties', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب قائمة الأصناف المتاحة للتهجين: {str(e)}")
            return []
    
    def _get_target_traits(self):
        """
        جلب قائمة الصفات المستهدفة
        
        العوائد:
            list: قائمة الصفات المستهدفة
        """
        try:
            url = f"{self.ai_api_url}/traits"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('traits', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب قائمة الصفات المستهدفة: {str(e)}")
            return []
    
    def _get_recent_breedings(self, limit=5):
        """
        جلب آخر عمليات تهجين
        
        المعلمات:
            limit (int): عدد النتائج المطلوبة
            
        العوائد:
            list: قائمة آخر عمليات تهجين
        """
        try:
            url = f"{self.ai_api_url}/recent-breedings?limit={limit}"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('breedings', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب آخر عمليات تهجين: {str(e)}")
            return []
    
    def _get_soil_types(self):
        """
        جلب قائمة أنواع التربة
        
        العوائد:
            list: قائمة أنواع التربة
        """
        try:
            url = f"{self.ai_api_url}/soil-types"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('soil_types', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب قائمة أنواع التربة: {str(e)}")
            return []
    
    def _get_soil_nutrients(self):
        """
        جلب قائمة العناصر الغذائية
        
        العوائد:
            list: قائمة العناصر الغذائية
        """
        try:
            url = f"{self.ai_api_url}/nutrients"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('nutrients', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب قائمة العناصر الغذائية: {str(e)}")
            return []
    
    def _get_recent_soil_analyses(self, limit=5):
        """
        جلب آخر تحليلات التربة
        
        المعلمات:
            limit (int): عدد النتائج المطلوبة
            
        العوائد:
            list: قائمة آخر تحليلات التربة
        """
        try:
            url = f"{self.ai_api_url}/recent-soil-analyses?limit={limit}"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('analyses', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب آخر تحليلات التربة: {str(e)}")
            return []
    
    def _get_agricultural_regions(self):
        """
        جلب قائمة المناطق الزراعية
        
        العوائد:
            list: قائمة المناطق الزراعية
        """
        try:
            url = f"{self.ai_api_url}/regions"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('regions', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب قائمة المناطق الزراعية: {str(e)}")
            return []
    
    def _get_recent_crop_recommendations(self, limit=5):
        """
        جلب آخر توصيات المحاصيل
        
        المعلمات:
            limit (int): عدد النتائج المطلوبة
            
        العوائد:
            list: قائمة آخر توصيات المحاصيل
        """
        try:
            url = f"{self.ai_api_url}/recent-recommendations?limit={limit}"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('recommendations', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب آخر توصيات المحاصيل: {str(e)}")
            return []
    
    def _get_recent_yield_predictions(self, limit=5):
        """
        جلب آخر تنبؤات الإنتاج
        
        المعلمات:
            limit (int): عدد النتائج المطلوبة
            
        العوائد:
            list: قائمة آخر تنبؤات الإنتاج
        """
        try:
            url = f"{self.ai_api_url}/recent-predictions?limit={limit}"
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            return response.json().get('predictions', [])
        
        except Exception as e:
            logger.error(f"خطأ في جلب آخر تنبؤات الإنتاج: {str(e)}")
            return []


# مثال على الاستخدام
def register_ui_integration(app, config_path=None):
    """
    تسجيل تكامل واجهات المستخدم في تطبيق Flask
    
    المعلمات:
        app (Flask): تطبيق Flask
        config_path (str): مسار ملف التكوين (اختياري)
    """
    ui_integration = UIIntegration(config_path)
    blueprint = ui_integration.create_blueprint()
    app.register_blueprint(blueprint)
    
    # إضافة ui_integration إلى سياق التطبيق
    app.config['UI_INTEGRATION'] = ui_integration
    
    logger.info("تم تسجيل تكامل واجهات المستخدم في تطبيق Flask")


if __name__ == "__main__":
    # مثال على إنشاء تطبيق Flask وتسجيل تكامل واجهات المستخدم
    from flask import Flask
    
    app = Flask(__name__)
    register_ui_integration(app)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
