from flask import request, send_file
from fastapi import APIRouter
# File: /home/ubuntu/ai_web_organized/src/modules/ai_usage_reports/api.py
"""
from flask import g
واجهة برمجة التطبيقات لمديول تقارير استخدام الذكاء الصناعي
يوفر هذا الملف واجهات برمجية لإنشاء وإدارة تقارير استخدام الذكاء الصناعي
"""

import os
import logging

from src.modules.ai_usage_reports.report_generator import AIUsageReportGenerator

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# إنشاء مولد تقارير استخدام الذكاء الصناعي
report_generator = AIUsageReportGenerator()

# إنشاء Blueprint للواجهة البرمجية
router = APIRouter(prefix="/api", tags=["api"])


@router.get("/")
def add_usage_record():
    """
    إضافة سجل استخدام جديد

    المعلمات (JSON):
        user_id (str): معرف المستخدم
        agent_id (str): معرف وكيل الذكاء الصناعي
        question (str): السؤال المطروح
        answer (str): الإجابة المقدمة
        timestamp (str, optional): الطابع الزمني
        module (str, optional): المديول المستخدم
        is_within_scope (bool, optional): هل السؤال والإجابة ضمن اختصاصات المستخدم والوكيل

    العائد:
        JSON: نتيجة العملية
    """
    try:
        # استخراج البيانات من الطلب
        data = request.get_json()

        # التحقق من وجود البيانات المطلوبة
        required_fields = ['user_id', 'agent_id', 'question', 'answer']
        for field in required_fields:
            if field not in data:
                return {'success': False, 'error': f'الحقل {field} مطلوب'}, 400

        # إضافة سجل استخدام جديد
        success = report_generator.add_usage_record(
            user_id=data['user_id'],
            agent_id=data['agent_id'],
            question=data['question'],
            answer=data['answer'],
            timestamp=data.get('timestamp'),
            module=data.get('module'),
            is_within_scope=data.get('is_within_scope')
        )

        if success:
            return {'success': True, 'message': 'تم إضافة سجل الاستخدام بنجاح'}, 201
        else:
            return {'success': False, 'error': 'فشل إضافة سجل الاستخدام'}, 500

    except Exception as e:
        logger.error("خطأ أثناء إضافة سجل استخدام: %s", str(e))
        return {'success': False, 'error': str(e)}, 500


@router.get("/")
def daily_report():
    """
    إنشاء تقرير يومي لاستخدام الذكاء الصناعي

    المعلمات (Query):
        date (str, optional): التاريخ (بتنسيق YYYY-MM-DD)

    العائد:
        JSON: تقرير استخدام الذكاء الصناعي
    """
    try:
        # استخراج التاريخ من الطلب
        date = request.args.get('date')

        # إنشاء تقرير يومي
        report = report_generator.generate_daily_report(date=date)

        return report, 200

    except Exception as e:
        logger.error("خطأ أثناء إنشاء التقرير اليومي: %s", str(e))
        return {'success': False, 'error': str(e)}, 500


@router.get("/")
def weekly_report():
    """
    إنشاء تقرير أسبوعي لاستخدام الذكاء الصناعي

    المعلمات (Query):
        end_date (str, optional): تاريخ نهاية الأسبوع (بتنسيق YYYY-MM-DD)

    العائد:
        JSON: تقرير استخدام الذكاء الصناعي
    """
    try:
        # استخراج تاريخ نهاية الأسبوع من الطلب
        end_date = request.args.get('end_date')

        # إنشاء تقرير أسبوعي
        report = report_generator.generate_weekly_report(end_date=end_date)

        return report, 200

    except Exception as e:
        logger.error("خطأ أثناء إنشاء التقرير الأسبوعي: %s", str(e))
        return {'success': False, 'error': str(e)}, 500


@router.get("/")
def monthly_report():
    """
    إنشاء تقرير شهري لاستخدام الذكاء الصناعي

    المعلمات (Query):
        month (int, optional): الشهر (1-12)
        year (int, optional): السنة

    العائد:
        JSON: تقرير استخدام الذكاء الصناعي
    """
    try:
        # استخراج الشهر والسنة من الطلب
        month = request.args.get('month')
        year = request.args.get('year')

        # تحويل الشهر والسنة إلى أعداد صحيحة إذا كانت موجودة
        if month:
            month = int(month)
        if year:
            year = int(year)

        # إنشاء تقرير شهري
        report = report_generator.generate_monthly_report(month=month, year=year)

        return report, 200

    except Exception as e:
        logger.error("خطأ أثناء إنشاء التقرير الشهري: %s", str(e))
        return {'success': False, 'error': str(e)}, 500


@router.get("/")
def user_report():
    """
    إنشاء تقرير استخدام الذكاء الصناعي لمستخدم معين

    المعلمات (Query):
        user_id (str): معرف المستخدم
        start_date (str, optional): تاريخ البداية (بتنسيق YYYY-MM-DD)
        end_date (str, optional): تاريخ النهاية (بتنسيق YYYY-MM-DD)

    العائد:
        JSON: تقرير استخدام الذكاء الصناعي
    """
    try:
        # استخراج معرف المستخدم وتاريخ البداية والنهاية من الطلب
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # التحقق من وجود معرف المستخدم
        if not user_id:
            return {'success': False, 'error': 'معرف المستخدم مطلوب'}, 400

        # إنشاء تقرير المستخدم
        report = report_generator.generate_user_report(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        return report, 200

    except Exception as e:
        logger.error("خطأ أثناء إنشاء تقرير المستخدم: %s", str(e))
        return {'success': False, 'error': str(e)}, 500


@router.get("/")
def agent_report():
    """
    إنشاء تقرير استخدام وكيل ذكاء اصطناعي معين

    المعلمات (Query):
        agent_id (str): معرف وكيل الذكاء الصناعي
        start_date (str, optional): تاريخ البداية (بتنسيق YYYY-MM-DD)
        end_date (str, optional): تاريخ النهاية (بتنسيق YYYY-MM-DD)

    العائد:
        JSON: تقرير استخدام الذكاء الصناعي
    """
    try:
        # استخراج معرف وكيل الذكاء الصناعي وتاريخ البداية والنهاية من الطلب
        agent_id = request.args.get('agent_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # التحقق من وجود معرف وكيل الذكاء الصناعي
        if not agent_id:
            return {'success': False, 'error': 'معرف وكيل الذكاء الصناعي مطلوب'}, 400

        # إنشاء تقرير وكيل الذكاء الصناعي
        report = report_generator.generate_agent_report(
            agent_id=agent_id,
            start_date=start_date,
            end_date=end_date
        )

        return report, 200

    except Exception as e:
        logger.error("خطأ أثناء إنشاء تقرير وكيل الذكاء الصناعي: %s", str(e))
        return {'success': False, 'error': str(e)}, 500


@router.get("/")
def module_report():
    """
    إنشاء تقرير استخدام الذكاء الصناعي لمديول معين

    المعلمات (Query):
        module (str): المديول
        start_date (str, optional): تاريخ البداية (بتنسيق YYYY-MM-DD)
        end_date (str, optional): تاريخ النهاية (بتنسيق YYYY-MM-DD)

    العائد:
        JSON: تقرير استخدام الذكاء الصناعي
    """
    try:
        # استخراج المديول وتاريخ البداية والنهاية من الطلب
        module = request.args.get('module')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # التحقق من وجود المديول
        if not module:
            return {'success': False, 'error': 'المديول مطلوب'}, 400

        # إنشاء تقرير المديول
        report = report_generator.generate_module_report(
            module=module,
            start_date=start_date,
            end_date=end_date
        )

        return report, 200

    except Exception as e:
        logger.error("خطأ أثناء إنشاء تقرير المديول: %s", str(e))
        return {'success': False, 'error': str(e)}, 500


@router.get("/")
def export_data():
    """
    تصدير بيانات استخدام الذكاء الصناعي

    المعلمات (Query):
        format (str, optional): تنسيق التصدير (json, csv)
        start_date (str, optional): تاريخ البداية (بتنسيق YYYY-MM-DD)
        end_date (str, optional): تاريخ النهاية (بتنسيق YYYY-MM-DD)
        module (str, optional): المديول

    العائد:
        File: ملف التصدير
    """
    try:
        # Extract query parameters from the request
        format = request.args.get('format')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        module = request.args.get('module')

        # تصدير البيانات
        # Provide default values if any are None
        export_path = report_generator.export_data(
            format=format or '',
            start_date=start_date or '',
            end_date=end_date or '',
            module=module or ''
        )

        if export_path:
            # إرسال الملف
            return send_file(export_path, as_attachment=True)
        else:
            return {'success': False, 'error': 'فشل تصدير البيانات'}, 500

    except Exception as e:
        logger.error("خطأ أثناء تصدير البيانات: %s", str(e))
        return {'success': False, 'error': str(e)}, 500


@router.get("/")
def visual_report(report_type):
    """
    الحصول على التقرير المرئي

    المعلمات:
        report_type (str): نوع التقرير (daily, weekly, monthly, user, agent, module)

    المعلمات (Query):
        date (str, optional): التاريخ (للتقرير اليومي)
        end_date (str, optional): تاريخ نهاية الأسبوع (للتقرير الأسبوعي)
        month (int, optional): الشهر (للتقرير الشهري)
        year (int, optional): السنة (للتقرير الشهري)
        user_id (str, optional): معرف المستخدم (لتقرير المستخدم)
        agent_id (str, optional): معرف وكيل الذكاء الصناعي (لتقرير وكيل الذكاء الصناعي)
        module (str, optional): المديول (لتقرير المديول)
        start_date (str, optional): تاريخ البداية (لتقارير المستخدم ووكيل الذكاء الصناعي والمديول)
        end_date (str, optional): تاريخ النهاية (لتقارير المستخدم ووكيل الذكاء الصناعي والمديول)
        chart_type (str, optional): نوع الرسم البياني (module_distribution, user_activity, agent_activity, daily_activity, weekly_activity, within_scope)

    العائد:
        File: ملف الرسم البياني
    """
    try:
        # استخراج نوع الرسم البياني من الطلب
        chart_type = request.args.get('chart_type')

        # تحديد مسار الرسم البياني
        visual_reports_dir = os.path.join(report_generator.reports_dir, 'visual')

        # إنشاء التقرير المناسب حسب نوع التقرير
        if report_type == 'daily':
            date = request.args.get('date')
            report = report_generator.generate_daily_report(date=date)
            report_filename = f"daily_visual_report_{report['date']}"

        elif report_type == 'weekly':
            end_date = request.args.get('end_date')
            report = report_generator.generate_weekly_report(end_date=end_date)
            report_filename = f"weekly_visual_report_{report['start_date']}_{report['end_date']}"

        elif report_type == 'monthly':
            month = request.args.get('month')
            year = request.args.get('year')

            if month:
                month = int(month)
            if year:
                year = int(year)

            report = report_generator.generate_monthly_report(month=month, year=year)
            report_filename = f"monthly_visual_report_{report['year']}_{report['month']:02d}"

        elif report_type == 'user':
            user_id = request.args.get('user_id')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            if not user_id:
                return {'success': False, 'error': 'معرف المستخدم مطلوب'}, 400

            report = report_generator.generate_user_report(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date
            )
            report_filename = f"user_visual_report_{report['user_id']}_{report['start_date']}_{report['end_date']}"

        elif report_type == 'agent':
            agent_id = request.args.get('agent_id')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            if not agent_id:
                return {'success': False, 'error': 'معرف وكيل الذكاء الصناعي مطلوب'}, 400

            report = report_generator.generate_agent_report(
                agent_id=agent_id,
                start_date=start_date,
                end_date=end_date
            )
            report_filename = f"agent_visual_report_{report['agent_id']}_{report['start_date']}_{report['end_date']}"

        elif report_type == 'module':
            module = request.args.get('module')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            if not module:
                return {'success': False, 'error': 'المديول مطلوب'}, 400

            report = report_generator.generate_module_report(
                module=module,
                start_date=start_date,
                end_date=end_date
            )
            report_filename = f"module_visual_report_{report['module']}_{report['start_date']}_{report['end_date']}"

        else:
            return {'success': False, 'error': 'نوع التقرير غير صالح'}, 400

        # تحديد مسار الرسم البياني
        chart_path = os.path.join(visual_reports_dir, f"{report_filename}_{chart_type}.png")

        # التحقق من وجود الرسم البياني
        if os.path.exists(chart_path):
            # إرسال الرسم البياني
            return send_file(chart_path, mimetype='image/png')
        else:
            return {'success': False, 'error': 'الرسم البياني غير موجود'}, 404

    except Exception as e:
        logger.error("خطأ أثناء الحصول على التقرير المرئي: %s", str(e))
        return {'success': False, 'error': str(e)}, 500
