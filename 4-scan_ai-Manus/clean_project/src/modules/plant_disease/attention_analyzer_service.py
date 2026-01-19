"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/plant_disease/attention_analyzer_service.py
الوصف: خدمة تحليل أنماط الانتباه للنماذج
المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
"""

from flask import Flask, request, jsonify
import os
import sys
import json
import time
import logging
from werkzeug.utils import secure_filename

# استيراد محلل أنماط الانتباه
from src.modules.plant_disease.attention_analyzer import AttentionAnalyzer
from src.modules.plant_disease.advanced_processor import AdvancedPlantDiseaseProcessor

# إعداد السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(os.getenv('LOG_DIR', '/app/logs'), 'attention_analyzer_service.log'))
    ]
)
logger = logging.getLogger('attention_analyzer_service')

# إنشاء تطبيق Flask
app = Flask(__name__)

# تكوين المسارات
UPLOAD_FOLDER = os.getenv('UPLOAD_DIR', '/app/uploads/attention_analysis')
REPORT_FOLDER = os.getenv('REPORT_STORAGE_PATH', '/app/reports/attention_analysis')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'}

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# تكوين التطبيق
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 ميجابايت كحد أقصى

# إعدادات تحليل الانتباه
VISUALIZATION_METHOD = os.getenv('VISUALIZATION_METHOD', 'gradcam')
COLORMAP = os.getenv('COLORMAP', 'jet')
OVERLAY_OPACITY = float(os.getenv('OVERLAY_OPACITY', '0.7'))

# تهيئة المعالج ومحلل الانتباه
processor = None
attention_analyzer = None


def allowed_file(filename: str) -> bool:
    """
    التحقق من أن امتداد الملف مسموح به

    المعلمات:
        filename (str): اسم الملف للتحقق منه

    العائد:
        bool: True إذا كان الامتداد مسموحًا به، False خلاف ذلك
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_services():
    """
    تهيئة المعالج ومحلل الانتباه
    """
    global processor, attention_analyzer

    logger.info("بدء تهيئة المعالج ومحلل الانتباه...")

    try:
        # تهيئة المعالج المتقدم
        processor = AdvancedPlantDiseaseProcessor()

        # تهيئة محلل الانتباه
        attention_analyzer = AttentionAnalyzer(processor)

        logger.info("تم تهيئة المعالج ومحلل الانتباه بنجاح")
    except Exception as e:
        logger.error(f"خطأ في تهيئة المعالج ومحلل الانتباه: {str(e)}")
        raise


@app.get('/health')
async def health_check():
    """
    نقطة نهاية للتحقق من صحة الخدمة
    """
    return {
        'status': 'healthy',
        'service': 'attention_analyzer_service',
        'timestamp': time.time()
    }


@app.route('/analyze', methods=['POST'])
def analyze_attention():
    """
    نقطة نهاية لتحليل أنماط الانتباه للنموذج
    """
    # التحقق من وجود الملف
    if 'image' not in request.files:
        return jsonify({'error': 'لم يتم توفير ملف الصورة'}), 400

    file = request.files['image']

    # التحقق من أن الملف ليس فارغًا
    if file.filename == '':
        return jsonify({'error': 'لم يتم اختيار ملف'}), 400

    # التحقق من امتداد الملف
    if not allowed_file(file.filename):
        return jsonify({'error': 'امتداد الملف غير مسموح به'}), 400

    # الحصول على اسم النموذج
    model_name = request.form.get('model_name')
    if not model_name:
        return jsonify({'error': 'لم يتم توفير اسم النموذج'}), 400

    try:
        # حفظ الملف
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # تحليل أنماط الانتباه
        result = attention_analyzer.analyze_attention_patterns(model_name, [file_path])

        # إضافة مسار الصورة الأصلية
        result['original_image'] = file_path

        # حفظ التقرير
        timestamp = int(time.time())
        report_filename = f"attention_analysis_{model_name}_{timestamp}.json"
        report_path = os.path.join(REPORT_FOLDER, report_filename)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # إضافة مسار التقرير
        result['report_path'] = report_path

        return jsonify(result)

    except Exception as e:
        logger.error(f"خطأ في تحليل أنماط الانتباه: {str(e)}")
        return jsonify({'error': f'خطأ في تحليل أنماط الانتباه: {str(e)}'}), 500


@app.route('/compare', methods=['POST'])
def compare_attention():
    """
    نقطة نهاية لمقارنة أنماط الانتباه بين النماذج
    """
    # التحقق من وجود الملفات
    if 'images' not in request.files:
        return jsonify({'error': 'لم يتم توفير ملفات الصور'}), 400

    files = request.files.getlist('images')

    # التحقق من أن الملفات ليست فارغة
    if len(files) == 0:
        return jsonify({'error': 'لم يتم اختيار ملفات'}), 400

    # الحصول على أسماء النماذج
    models = request.form.get('models')
    if not models:
        return jsonify({'error': 'لم يتم توفير أسماء النماذج'}), 400

    try:
        models = json.loads(models)
    except json.JSONDecodeError:
        return jsonify({'error': 'تنسيق أسماء النماذج غير صالح'}), 400

    try:
        # حفظ الملفات
        file_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)

        # مقارنة أنماط الانتباه
        comparison_result = attention_analyzer.create_attention_comparison(models, file_paths)

        # حفظ التقرير
        timestamp = int(time.time())
        report_filename = f"attention_comparison_{timestamp}.json"
        report_path = os.path.join(REPORT_FOLDER, report_filename)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(comparison_result, f, ensure_ascii=False, indent=2)

        # إضافة مسار التقرير
        comparison_result['report_path'] = report_path

        return jsonify(comparison_result)

    except Exception as e:
        logger.error(f"خطأ في مقارنة أنماط الانتباه: {str(e)}")
        return jsonify({'error': f'خطأ في مقارنة أنماط الانتباه: {str(e)}'}), 500


@app.route('/settings', methods=['GET', 'PUT'])
def manage_settings():
    """
    نقطة نهاية لإدارة إعدادات تحليل الانتباه
    """
    global VISUALIZATION_METHOD, COLORMAP, OVERLAY_OPACITY
    
    if request.method == 'GET':
        # الحصول على الإعدادات الحالية
        settings = {
            'visualization_method': VISUALIZATION_METHOD,
            'colormap': COLORMAP,
            'overlay_opacity': OVERLAY_OPACITY
        }
        return jsonify(settings)

    elif request.method == 'PUT':
        # تحديث الإعدادات
        try:
            data = request.json

            if 'visualization_method' in data:
                VISUALIZATION_METHOD = data['visualization_method']

            if 'colormap' in data:
                COLORMAP = data['colormap']

            if 'overlay_opacity' in data:
                OVERLAY_OPACITY = float(data['overlay_opacity'])

            # تحديث إعدادات محلل الانتباه
            if attention_analyzer:
                attention_analyzer.update_settings(
                    visualization_method=VISUALIZATION_METHOD,
                    colormap=COLORMAP,
                    overlay_opacity=OVERLAY_OPACITY
                )

            return jsonify({
                'status': 'success',
                'message': 'تم تحديث الإعدادات بنجاح',
                'settings': {
                    'visualization_method': VISUALIZATION_METHOD,
                    'colormap': COLORMAP,
                    'overlay_opacity': OVERLAY_OPACITY
                }
            })

        except Exception as e:
            logger.error(f"خطأ في تحديث الإعدادات: {str(e)}")
            return jsonify({'error': f'خطأ في تحديث الإعدادات: {str(e)}'}), 500


@app.route('/reports', methods=['GET'])
def get_reports():
    """
    نقطة نهاية للحصول على قائمة تقارير تحليل الانتباه
    """
    try:
        reports = []

        # الحصول على جميع ملفات التقارير
        for filename in os.listdir(REPORT_FOLDER):
            if filename.endswith('.json'):
                file_path = os.path.join(REPORT_FOLDER, filename)

                # استخراج معلومات التقرير من اسم الملف
                parts = filename.split('_')

                if len(parts) >= 3 and parts[0] == 'attention':
                    report_type = parts[1]

                    if report_type == 'analysis':
                        model_name = parts[2]
                        timestamp = parts[3].split('.')[0]
                    elif report_type == 'comparison':
                        model_name = 'مقارنة'
                        timestamp = parts[2].split('.')[0]
                    else:
                        continue

                    reports.append({
                        'type': report_type,
                        'model_name': model_name,
                        'timestamp': timestamp,
                        'path': file_path
                    })

        # ترتيب التقارير حسب الطابع الزمني (الأحدث أولاً)
        reports.sort(key=lambda x: x['timestamp'], reverse=True)

        return jsonify({'reports': reports})

    except Exception as e:
        logger.error(f"خطأ في الحصول على قائمة التقارير: {str(e)}")
        return jsonify({'error': f'خطأ في الحصول على قائمة التقارير: {str(e)}'}), 500


@app.route('/reports/<timestamp>', methods=['GET'])
def get_report(timestamp):
    """
    نقطة نهاية للحصول على تقرير تحليل الانتباه محدد

    المعلمات:
        timestamp (str): الطابع الزمني للتقرير
    """
    try:
        # البحث عن التقرير
        for filename in os.listdir(REPORT_FOLDER):
            if filename.endswith('.json') and timestamp in filename:
                file_path = os.path.join(REPORT_FOLDER, filename)

                # قراءة محتوى التقرير
                with open(file_path, 'r', encoding='utf-8') as f:
                    report = json.load(f)

                return jsonify(report)

        return jsonify({'error': 'التقرير غير موجود'}), 404

    except Exception as e:
        logger.error(f"خطأ في الحصول على التقرير: {str(e)}")
        return jsonify({'error': f'خطأ في الحصول على التقرير: {str(e)}'}), 500


if __name__ == '__main__':
    # تهيئة الخدمات
    init_services()

    # تشغيل التطبيق
    port = int(os.getenv('ATTENTION_ANALYSIS_PORT', '5011'))
    app.run(host='0.0.0.0', port=port, debug=False)
