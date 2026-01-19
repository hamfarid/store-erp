# /home/ubuntu/ai_web_organized/src/web_interface/agri_ai_webapp/src/routes/admin_panel/controllers/validation_ui_controller.py

"""
from flask import g
وحدة تحكم واجهة التحقق من صحة البيانات (Validation UI Controller)

هذه الوحدة مسؤولة عن التكامل بين نظام التحقق من صحة البيانات وواجهة المستخدم،
وتوفير واجهة برمجية للتفاعل مع نظام التحقق وعرض الأخطاء للمستخدمين.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash

# استيراد وحدات التحقق
from modules.data_validation.model_validator import ModelValidator
from modules.data_validation.database_validator import DatabaseValidator
from modules.data_validation.invalid_data_handler import InvalidDataHandler

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('validation_ui_controller')

# إنشاء Blueprint
validation_bp = Blueprint('validation', __name__, url_prefix='/admin/validation')

# إنشاء كائنات التحقق
model_validator = ModelValidator()
database_validator = DatabaseValidator()
invalid_data_handler = InvalidDataHandler()


@validation_bp.route('/', methods=['GET'])
def index():
    """
    عرض صفحة التحقق من صحة البيانات الرئيسية.
    """
    return render_template('admin_panel/validation/index.html')


@validation_bp.route('/models', methods=['GET'])
def list_models():
    """
    عرض قائمة النماذج المتاحة للتحقق.
    """
    models = model_validator.get_all_models()
    return render_template('admin_panel/validation/models.html', models=models)


@validation_bp.route('/models/<model_name>', methods=['GET'])
def view_model(model_name):
    """
    عرض تفاصيل نموذج محدد.
    """
    model = model_validator.get_model(model_name)
    if not model:
        flash(f"النموذج '{model_name}' غير موجود", 'error')
        return redirect(url_for('validation.list_models'))

    return render_template('admin_panel/validation/model_details.html', model_name=model_name, model=model)


@validation_bp.route('/models/<model_name>/validate', methods=['GET', 'POST'])
def validate_model_data(model_name):
    """
    التحقق من صحة البيانات وفقًا لنموذج محدد.
    """
    model = model_validator.get_model(model_name)
    if not model:
        flash(f"النموذج '{model_name}' غير موجود", 'error')
        return redirect(url_for('validation.list_models'))

    if request.method == 'POST':
        try:
            # الحصول على البيانات من النموذج
            data = request.form.get('data')
            auto_fix = request.form.get('auto_fix') == 'on'

            # تحويل البيانات من JSON
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                flash("تنسيق البيانات غير صالح. يرجى التأكد من أن البيانات بتنسيق JSON صالح.", 'error')
                return render_template('admin_panel/validation/validate_model.html', model_name=model_name, model=model)

            # التحقق من صحة البيانات
            is_valid, errors = model_validator.validate_data(data, model_name)

            if is_valid:
                flash("البيانات صحيحة وفقًا للنموذج", 'success')
                return render_template('admin_panel/validation/validate_model.html', model_name=model_name, model=model, data=data, is_valid=is_valid)

            # معالجة البيانات غير الصحيحة إذا تم تفعيل الإصلاح التلقائي
            if auto_fix:
                is_fixed, fixed_data, actions = invalid_data_handler.handle_invalid_model_data(data, model_name, auto_fix=True)

                if is_fixed:
                    flash("تم إصلاح البيانات بنجاح", 'success')
                    return render_template('admin_panel/validation/validate_model.html', model_name=model_name, model=model, data=data, fixed_data=fixed_data, actions=actions, is_valid=False, is_fixed=is_fixed)
                else:
                    flash("لم يتم إصلاح جميع المشكلات", 'warning')
                    return render_template('admin_panel/validation/validate_model.html', model_name=model_name, model=model, data=data, fixed_data=fixed_data, actions=actions, errors=errors, is_valid=False, is_fixed=False)
            else:
                flash("البيانات غير صحيحة وفقًا للنموذج", 'error')
                return render_template('admin_panel/validation/validate_model.html', model_name=model_name, model=model, data=data, errors=errors, is_valid=False)
        except Exception as e:
            logger.error(f"خطأ في التحقق من صحة البيانات: {str(e)}")
            flash(f"حدث خطأ أثناء التحقق من صحة البيانات: {str(e)}", 'error')
            return render_template('admin_panel/validation/validate_model.html', model_name=model_name, model=model)

    return render_template('admin_panel/validation/validate_model.html', model_name=model_name, model=model)


@validation_bp.route('/database', methods=['GET'])
def list_tables():
    """
    عرض قائمة الجداول المتاحة للتحقق.
    """
    # التأكد من الاتصال بقاعدة البيانات
    if not database_validator.connection:
        connected = database_validator.connect()
        if not connected:
            flash("فشل الاتصال بقاعدة البيانات", 'error')
            return render_template('admin_panel/validation/database.html', tables=[])

    tables = list(database_validator.constraints.keys())
    return render_template('admin_panel/validation/database.html', tables=tables)


@validation_bp.route('/database/<table_name>', methods=['GET'])
def view_table(table_name):
    """
    عرض تفاصيل جدول محدد.
    """
    # التأكد من الاتصال بقاعدة البيانات
    if not database_validator.connection:
        connected = database_validator.connect()
        if not connected:
            flash("فشل الاتصال بقاعدة البيانات", 'error')
            return redirect(url_for('validation.list_tables'))

    if table_name not in database_validator.constraints:
        flash(f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات", 'error')
        return redirect(url_for('validation.list_tables'))

    constraints = database_validator.get_constraints(table_name)
    schema = database_validator.get_table_schema(table_name)

    return render_template('admin_panel/validation/table_details.html', table_name=table_name, constraints=constraints, schema=schema)


@validation_bp.route('/database/<table_name>/validate', methods=['GET', 'POST'])
def validate_table_data(table_name):
    """
    التحقق من صحة البيانات في جدول محدد.
    """
    # التأكد من الاتصال بقاعدة البيانات
    if not database_validator.connection:
        connected = database_validator.connect()
        if not connected:
            flash("فشل الاتصال بقاعدة البيانات", 'error')
            return redirect(url_for('validation.list_tables'))

    if table_name not in database_validator.constraints:
        flash(f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات", 'error')
        return redirect(url_for('validation.list_tables'))

    if request.method == 'POST':
        try:
            # الحصول على الإعدادات من النموذج
            auto_fix = request.form.get('auto_fix') == 'on'

            # التحقق من صحة مخطط الجدول
            schema_valid, schema_errors = database_validator.validate_table_schema(table_name)

            if not schema_valid:
                flash("مخطط الجدول غير صحيح", 'error')
                return render_template('admin_panel/validation/validate_table.html', table_name=table_name, schema_errors=schema_errors, schema_valid=schema_valid)

            # التحقق من تكامل البيانات
            if auto_fix:
                is_valid, actions = invalid_data_handler.handle_invalid_database_data(table_name, auto_fix=True)

                if is_valid:
                    flash("تم إصلاح بيانات الجدول بنجاح", 'success')
                    return render_template('admin_panel/validation/validate_table.html', table_name=table_name, actions=actions, is_valid=is_valid, schema_valid=schema_valid)
                else:
                    flash("لم يتم إصلاح جميع مشكلات الجدول", 'warning')
                    return render_template('admin_panel/validation/validate_table.html', table_name=table_name, actions=actions, is_valid=is_valid, schema_valid=schema_valid)
            else:
                is_valid, errors = database_validator.validate_data_integrity(table_name)

                if is_valid:
                    flash("تكامل البيانات صحيح", 'success')
                    return render_template('admin_panel/validation/validate_table.html', table_name=table_name, is_valid=is_valid, schema_valid=schema_valid)
                else:
                    flash("تكامل البيانات غير صحيح", 'error')
                    return render_template('admin_panel/validation/validate_table.html', table_name=table_name, errors=errors, is_valid=is_valid, schema_valid=schema_valid)
        except Exception as e:
            logger.error(f"خطأ في التحقق من صحة بيانات الجدول: {str(e)}")
            flash(f"حدث خطأ أثناء التحقق من صحة بيانات الجدول: {str(e)}", 'error')
            return render_template('admin_panel/validation/validate_table.html', table_name=table_name)

    return render_template('admin_panel/validation/validate_table.html', table_name=table_name)


@validation_bp.route('/api/models', methods=['GET'])
def api_list_models():
    """
    واجهة برمجية للحصول على قائمة النماذج المتاحة للتحقق.
    """
    models = model_validator.get_all_models()
    return jsonify(models)


@validation_bp.route('/api/models/<model_name>', methods=['GET'])
def api_get_model(model_name):
    """
    واجهة برمجية للحصول على تفاصيل نموذج محدد.
    """
    model = model_validator.get_model(model_name)
    if not model:
        return jsonify({"error": f"النموذج '{model_name}' غير موجود"}), 404

    return jsonify(model)


@validation_bp.route('/api/models/<model_name>/validate', methods=['POST'])
def api_validate_model_data(model_name):
    """
    واجهة برمجية للتحقق من صحة البيانات وفقًا لنموذج محدد.
    """
    model = model_validator.get_model(model_name)
    if not model:
        return jsonify({"error": f"النموذج '{model_name}' غير موجود"}), 404

    try:
        # الحصول على البيانات من الطلب
        data = request.json
        auto_fix = request.args.get('auto_fix', 'false').lower() == 'true'

        if not data:
            return jsonify({"error": "لم يتم توفير بيانات للتحقق"}), 400

        # التحقق من صحة البيانات
        is_valid, errors = model_validator.validate_data(data, model_name)

        if is_valid:
            return jsonify({"valid": True, "data": data})

        # معالجة البيانات غير الصحيحة إذا تم تفعيل الإصلاح التلقائي
        if auto_fix:
            is_fixed, fixed_data, actions = invalid_data_handler.handle_invalid_model_data(data, model_name, auto_fix=True)

            if is_fixed:
                return jsonify({"valid": False, "fixed": True, "original_data": data, "fixed_data": fixed_data, "actions": actions})
            else:
                return jsonify({"valid": False, "fixed": False, "original_data": data, "fixed_data": fixed_data, "actions": actions, "errors": errors})
        else:
            return jsonify({"valid": False, "data": data, "errors": errors})
    except Exception as e:
        logger.error(f"خطأ في التحقق من صحة البيانات: {str(e)}")
        return jsonify({"error": f"حدث خطأ أثناء التحقق من صحة البيانات: {str(e)}"}), 500


@validation_bp.route('/api/database/tables', methods=['GET'])
def api_list_tables():
    """
    واجهة برمجية للحصول على قائمة الجداول المتاحة للتحقق.
    """
    # التأكد من الاتصال بقاعدة البيانات
    if not database_validator.connection:
        connected = database_validator.connect()
        if not connected:
            return jsonify({"error": "فشل الاتصال بقاعدة البيانات"}), 500

    tables = list(database_validator.constraints.keys())
    return jsonify(tables)


@validation_bp.route('/api/database/tables/<table_name>', methods=['GET'])
def api_get_table(table_name):
    """
    واجهة برمجية للحصول على تفاصيل جدول محدد.
    """
    # التأكد من الاتصال بقاعدة البيانات
    if not database_validator.connection:
        connected = database_validator.connect()
        if not connected:
            return jsonify({"error": "فشل الاتصال بقاعدة البيانات"}), 500

    if table_name not in database_validator.constraints:
        return jsonify({"error": f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات"}), 404

    constraints = database_validator.get_constraints(table_name)
    schema = database_validator.get_table_schema(table_name)

    return jsonify({"table_name": table_name, "constraints": constraints, "schema": schema})


@validation_bp.route('/api/database/tables/<table_name>/validate', methods=['POST'])
def api_validate_table_data(table_name):
    """
    واجهة برمجية للتحقق من صحة البيانات في جدول محدد.
    """
    # التأكد من الاتصال بقاعدة البيانات
    if not database_validator.connection:
        connected = database_validator.connect()
        if not connected:
            return jsonify({"error": "فشل الاتصال بقاعدة البيانات"}), 500

    if table_name not in database_validator.constraints:
        return jsonify({"error": f"الجدول '{table_name}' غير موجود في قيود قاعدة البيانات"}), 404

    try:
        # الحصول على الإعدادات من الطلب
        auto_fix = request.args.get('auto_fix', 'false').lower() == 'true'

        # التحقق من صحة مخطط الجدول
        schema_valid, schema_errors = database_validator.validate_table_schema(table_name)

        if not schema_valid:
            return jsonify({"schema_valid": False, "schema_errors": schema_errors}), 400

        # التحقق من تكامل البيانات
        if auto_fix:
            is_valid, actions = invalid_data_handler.handle_invalid_database_data(table_name, auto_fix=True)

            if is_valid:
                return jsonify({"schema_valid": True, "data_valid": True, "actions": actions})
            else:
                return jsonify({"schema_valid": True, "data_valid": False, "actions": actions})
        else:
            is_valid, errors = database_validator.validate_data_integrity(table_name)

            if is_valid:
                return jsonify({"schema_valid": True, "data_valid": True})
            else:
                return jsonify({"schema_valid": True, "data_valid": False, "errors": errors})
    except Exception as e:
        logger.error(f"خطأ في التحقق من صحة بيانات الجدول: {str(e)}")
        return jsonify({"error": f"حدث خطأ أثناء التحقق من صحة بيانات الجدول: {str(e)}"}), 500


@validation_bp.route('/api/database/validate-all', methods=['POST'])
def api_validate_all_tables():
    """
    واجهة برمجية للتحقق من صحة البيانات في جميع الجداول.
    """
    # التأكد من الاتصال بقاعدة البيانات
    if not database_validator.connection:
        connected = database_validator.connect()
        if not connected:
            return jsonify({"error": "فشل الاتصال بقاعدة البيانات"}), 500

    try:
        # الحصول على الإعدادات من الطلب
        auto_fix = request.args.get('auto_fix', 'false').lower() == 'true'

        # التحقق من صحة جميع الجداول
        if auto_fix:
            results = invalid_data_handler.handle_all_database_tables(auto_fix=True)
        else:
            results = database_validator.validate_all_tables()

        return jsonify(results)
    except Exception as e:
        logger.error(f"خطأ في التحقق من صحة بيانات جميع الجداول: {str(e)}")
        return jsonify({"error": f"حدث خطأ أثناء التحقق من صحة بيانات جميع الجداول: {str(e)}"}), 500


def register_blueprint(app):
    """
    تسجيل Blueprint في تطبيق Flask.
    """
    app.register_blueprint(validation_bp)
    logger.info("تم تسجيل Blueprint للتحقق من صحة البيانات بنجاح")
