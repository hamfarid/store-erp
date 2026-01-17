"""
إعدادات قاعدة البيانات المحسنة
Enhanced Database Configuration
"""

import os
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# إنشاء كائن قاعدة البيانات
db = SQLAlchemy()
migrate = Migrate()


def configure_database(app):
    """تكوين قاعدة البيانات مع Flask app"""

    # إعدادات قاعدة البيانات
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(basedir, "instance")

    # إنشاء مجلد instance إذا لم يكن موجوداً
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    # مسار قاعدة البيانات
    database_path = os.path.join(instance_dir, "inventory.db")

    # تكوين Flask app
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)
    migrate.init_app(app, db)

    return db


def create_tables(app):
    """إنشاء الجداول - النماذج يجب أن تكون مستوردة مسبقاً في app.py"""
    try:
        with app.app_context():
            # لا نستورد النماذج هنا لتجنب التعريفات المكررة
            # النماذج يتم استيرادها في app.py

            # إنشاء جميع الجداول
            db.create_all()
            print("✅ تم إنشاء جداول قاعدة البيانات بنجاح")
            return True
    except Exception as e:
        print(f"❌ خطأ في إنشاء الجداول: {e}")
        import traceback

        traceback.print_exc()
        return False


def create_default_data():
    """إنشاء البيانات الأساسية - يتم استدعاؤها من app.py بعد استيراد النماذج"""
    try:
        # استخدام simple_recreate_db.py بدلاً من هذه الدالة
        # لتجنب مشاكل الاستيراد المكررة
        print("⚠️ استخدم simple_recreate_db.py لإنشاء البيانات الأساسية")
        return True

    except Exception as e:
        print("❌ خطأ: {}".format(e))
        return False
