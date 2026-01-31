"""
إعدادات قاعدة البيانات المحسنة
Enhanced Database Configuration
"""

import os
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# إنشاء كائن قاعدة البيانات
db = SQLAlchemy()
migrate = Migrate()

logger = logging.getLogger(__name__)


def clear_test_database():
    """
    Clear and recreate database for testing between test runs.
    Ensures test isolation by providing a fresh database.
    """
    try:
        db.session.remove()
        db.drop_all()
        db.create_all()
        logger.debug("✓ Test database cleared and recreated")
        return True
    except Exception as e:
        logger.error(f"❌ Error clearing test database: {e}")
        return False


def configure_database(app):
    """تكوين قاعدة البيانات مع Flask app"""

    # Check for DATABASE_URL from environment (Docker/Production)
    # This allows Docker Compose to use PostgreSQL while development uses SQLite
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

        if database_url.startswith("sqlite:"):
            logger.info("✅ Using SQLite from DATABASE_URL environment variable")

            # If this is a file-backed SQLite DB, ensure parent directory exists.
            # Examples:
            # - sqlite:///:memory:
            # - sqlite:///D:/path/to/db.sqlite
            # - sqlite:////absolute/path/to/db.sqlite
            if ":memory:" not in database_url:
                url_no_query = database_url.split("?", 1)[0]
                if url_no_query.startswith("sqlite:////"):
                    db_path = url_no_query[len("sqlite:////") :]
                elif url_no_query.startswith("sqlite:///"):
                    db_path = url_no_query[len("sqlite:///") :]
                else:
                    db_path = ""

                if db_path:
                    db_path = os.path.normpath(db_path.replace("/", os.sep))
                    parent_dir = os.path.dirname(db_path)
                    if parent_dir:
                        os.makedirs(parent_dir, exist_ok=True)

            # SQLite-specific engine options
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                "pool_pre_ping": True,
                "pool_recycle": 300,
            }
        else:
            # Use PostgreSQL (Docker/Production)
            logger.info("✅ Using PostgreSQL from DATABASE_URL environment variable")
            # PostgreSQL-specific engine options
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                "pool_pre_ping": True,
                "pool_recycle": 300,
                "pool_size": 10,
                "max_overflow": 20,
            }
        # Fallback to SQLite for development
        basedir = os.path.abspath(os.path.dirname(__file__))
        instance_dir = os.path.join(os.path.dirname(basedir), "instance")

        # إنشاء مجلد instance إذا لم يكن موجوداً
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)

        # مسار قاعدة البيانات - استخدام SQLite افتراضيًا بدلًا من Localhost Postgres
        # لمنع الأخطاء عند عدم وجود DATABASE_URL
        database_path = os.path.join(instance_dir, "inventory.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
        logger.info(f"✅ Using SQLite for development: {database_path}")
        # SQLite-specific engine options
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }

    # Common configuration for both database types
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)
    migrate.init_app(app, db)

    return db


def create_tables(app):
    """إنشاء الجداول"""
    import logging

    logger = logging.getLogger(__name__)

    try:
        with app.app_context():
            # Preload all models so SQLAlchemy metadata includes all FK targets before create_all()
            # IMPORTANT: Load models in dependency order (base tables first)
            logger.info("🔄 Loading models in dependency order...")

            try:
                # Phase 1: Base tables (no FK dependencies)
                logger.debug("Phase 1: Loading base models...")
                try:
                    from src.models.user import User, Role  # noqa: F401
                except ImportError:
                    from models.user import User, Role  # noqa: F401

                try:
                    from src.models.sales_engineer import SalesEngineer  # noqa: F401
                except ImportError:
                    try:
                        from models.sales_engineer import SalesEngineer  # noqa: F401
                    except ImportError:
                        logger.warning("⚠️ SalesEngineer model not available")

                try:
                    from src.models.customer import Customer  # noqa: F401
                except ImportError:
                    from models.customer import Customer  # noqa: F401

                try:
                    from src.models.supplier import Supplier  # noqa: F401
                except ImportError:
                    from models.supplier import Supplier  # noqa: F401
                logger.debug("✓ Base models loaded")

                # Phase 2: Inventory base tables
                logger.debug("Phase 2: Loading inventory models...")
                try:
                    from src.models.inventory import (
                        Category,
                        Product,
                        Warehouse,
                    )  # noqa: F401
                except ImportError:
                    from models.inventory import (
                        Category,
                        Product,
                        Warehouse,
                    )  # noqa: F401
                logger.debug("✓ Inventory models loaded")

                # Phase 3: Enhanced models - DISABLED to avoid schema conflicts
                # enhanced_models.py redefines Category with extra fields (name_ar, etc)
                # which causes schema mismatches with inventory.py Category
                logger.debug("Phase 3: Skipping enhanced models (schema conflicts)")

                # Phase 4: Invoice models
                logger.debug("Phase 4: Loading invoice models...")
                try:
                    from src.models.unified_invoice import (  # noqa: F401
                        UnifiedInvoice,
                        UnifiedInvoiceItem,
                    )
                    from src.models.invoice_unified import InvoicePayment  # noqa: F401

                    logger.debug("✓ Invoice models loaded")
                except ImportError as e:
                    logger.warning(f"⚠️ Invoice models not available: {e}")

                # Phase 5: Advanced sales models (now enabled with FK support)
                logger.debug("Phase 5: Loading advanced sales models...")
                try:
                    try:
                        from src.models.sales_advanced import (  # noqa: F401
                            SalesInvoice,
                            SalesInvoiceItem,
                            CustomerPayment,
                        )
                    except ImportError:
                        from models.sales_advanced import (  # noqa: F401
                            SalesInvoice,
                            SalesInvoiceItem,
                            CustomerPayment,
                        )
                    logger.debug("✓ Advanced sales models loaded")
                except Exception as sales_err:
                    logger.warning(f"⚠️ Advanced sales skipped: {sales_err}")

                # Phase 6: Advanced product and batch models (required by PurchaseOrderItem FK)
                logger.debug("Phase 6: Loading advanced product models...")
                try:
                    from src.models.product_advanced import ProductAdvanced  # noqa: F401
                    from src.models.lot_advanced import LotAdvanced  # noqa: F401
                    logger.debug("✓ Advanced product models loaded")
                except ImportError as e:
                    logger.warning(f"⚠️ Advanced product models not available: {e}")

                # Phase 7: Purchase models (depends on advanced models)
                logger.debug("Phase 7: Loading purchase models...")
                try:
                    from src.models.purchase_order import PurchaseOrder  # noqa: F401
                    from src.models.purchase_order_item import PurchaseOrderItem  # noqa: F401
                    from src.models.purchase_receipt import PurchaseReceipt  # noqa: F401
                    logger.debug("✓ Purchase models loaded")
                except ImportError as e:
                    logger.warning(f"⚠️ Purchase models not available: {e}")

            except Exception as e:
                logger.error(f"❌ Model preload error: {e}")
                logger.warning("⚠️ Continuing with partial initialization")

            # إنشاء جميع الجداول
            logger.info("🔄 Creating all database tables...")
            db.create_all()
            logger.info("✅ تم إنشاء جداول قاعدة البيانات بنجاح")
            print("Tables created successfully")

            # Return models to pass to create_default_data (avoid duplicate imports)
            return True, User, Role, Category, Warehouse
    except Exception as e:
        logger.error(f"❌ خطأ في إنشاء الجداول: {e}", exc_info=True)
        print(f"Error creating tables: {e}")
        return False


def create_default_data(User=None, Role=None, Category=None, Warehouse=None):
    """إنشاء البيانات الأساسية

    Args:
        User, Role, Category, Warehouse: Model classes passed from init_database()
            to avoid duplicate imports/registrations
    """
    from flask import has_app_context
    from sqlalchemy import select, func, inspect
    import logging

    logger = logging.getLogger(__name__)

    try:
        # التأكد من وجود app context
        if not has_app_context():
            print("⚠️ لا يوجد Flask app context، تخطي إنشاء البيانات الأساسية")
            return True

        print("DEBUG: Starting create_default_data()...")
        print(
            f"DEBUG: Received models - User: {User}, Role: {Role}, Category: {Category}, Warehouse: {Warehouse}"
        )

        # استيراد النماذج فقط إذا لم يتم تمريرها (للاستدعاءات المستقلة)
        # ⚠️ WARNING: Avoid this path when called from init_database()
        if User is None or Role is None or Category is None or Warehouse is None:
            print("⚠️ DEBUG: Models not passed, importing...")
            try:
                from src.models.user import User, Role
                from src.models.inventory import Category, Warehouse
            except ImportError:
                from models.user import User, Role
                from models.inventory import Category, Warehouse
            print("DEBUG: Models imported successfully")
        else:
            print("DEBUG: Using passed models")

        # إنشاء الأدوار الأساسية
        # Query using raw SQL to avoid mapper configuration conflicts
        role_count = db.session.execute(db.text("SELECT COUNT(*) FROM roles")).scalar()

        if role_count == 0:
            inspector = inspect(db.engine)
            role_columns = {c["name"] for c in inspector.get_columns("roles")}

            role_rows = [
                {
                    "code": "admin",
                    "name": "admin",
                    "name_ar": "مدير النظام",
                    "description": "مدير النظام",
                    "description_ar": "مدير النظام",
                    "is_active": 1,
                    "is_system": 1,
                },
                {
                    "code": "user",
                    "name": "user",
                    "name_ar": "مستخدم عادي",
                    "description": "مستخدم عادي",
                    "description_ar": "مستخدم عادي",
                    "is_active": 1,
                    "is_system": 1,
                },
            ]

            # Only insert columns that actually exist in the current schema.
            insert_columns = [
                c
                for c in [
                    "code",
                    "name",
                    "name_ar",
                    "description",
                    "description_ar",
                    "is_active",
                    "is_system",
                ]
                if c in role_columns
            ]
            if not insert_columns:
                raise RuntimeError(
                    "roles table has no recognized columns for default insert"
                )

            values_sql = []
            params = {}
            for i, row in enumerate(role_rows):
                placeholders = []
                for col in insert_columns:
                    key = f"{col}_{i}"
                    placeholders.append(f":{key}")
                    params[key] = row.get(col)
                values_sql.append(f"({', '.join(placeholders)})")

            sql = (
                f"INSERT INTO roles ({', '.join(insert_columns)}) VALUES "
                + ", ".join(values_sql)
            )
            db.session.execute(db.text(sql), params)
            db.session.commit()
            print("Default roles created")

        # إنشاء المستخدم الإداري
        # Query using raw SQL
        admin_exists = db.session.execute(
            db.text("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        ).scalar()

        if admin_exists == 0:
            # Hash password using bcrypt directly
            import bcrypt

            password_hash = bcrypt.hashpw(
                "admin123".encode(), bcrypt.gensalt()
            ).decode()

            db.session.execute(
                db.text(
                    """
                INSERT INTO users (username, email, full_name, password_hash, role_id, is_active)
                VALUES ('admin', 'admin@store.com', 'مدير النظام', :pwd, 1, 1)
            """
                ),
                {"pwd": password_hash},
            )
            db.session.commit()
            print("Admin user created")

        # إنشاء الفئات الأساسية
        category_count = db.session.execute(
            db.text("SELECT COUNT(*) FROM categories")
        ).scalar()

        if category_count == 0:
            db.session.execute(
                db.text(
                    """
                INSERT INTO categories (name, description) VALUES
                ('إلكترونيات', 'الأجهزة الإلكترونية'),
                ('ملابس', 'الملابس والأزياء'),
                ('طعام', 'المواد الغذائية'),
                ('كتب', 'الكتب والمطبوعات'),
                ('أدوات', 'الأدوات والمعدات')
            """
                )
            )
            db.session.commit()
            print("Default categories created")

        # إنشاء المخازن الأساسية
        warehouse_count = db.session.execute(
            db.text("SELECT COUNT(*) FROM warehouses")
        ).scalar()

        if warehouse_count == 0:
            db.session.execute(
                db.text(
                    """
                INSERT INTO warehouses (name, code, address, is_active) VALUES
                ('المخزن الرئيسي', 'WH001', 'الرياض - المخزن الرئيسي للشركة', 1),
                ('مخزن فرعي', 'WH002', 'جدة - مخزن فرعي', 1)
            """
                )
            )
            db.session.commit()
            print("Default warehouses created")

        print("All default data created successfully")
        return True

    except Exception as e:
        import traceback

        print(f"Error creating default data: {e}")
        print("Full traceback:")
        traceback.print_exc()
        try:
            db.session.rollback()
        except Exception:  # noqa: BLE001
            pass
        return False


def get_database_info():
    """الحصول على معلومات قاعدة البيانات"""
    try:
        info = {"tables": [], "total_records": 0}

        # قائمة الجداول
        tables = db.metadata.tables.keys()
        info["tables"] = list(tables)

        # عدد السجلات في كل جدول
        from sqlalchemy import text

        for table_name in tables:
            try:
                # استخدام text() لتجنب تحذير SQL
                count_query = text(f"SELECT COUNT(*) FROM {table_name}")
                count = db.session.execute(count_query).scalar()
                info[f"{table_name}_count"] = count
                info["total_records"] += count
            except BaseException:
                info[f"{table_name}_count"] = 0

        return info

    except Exception as e:
        print(f"خطأ في الحصول على معلومات قاعدة البيانات: {e}")
        return {}


def backup_database():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    try:
        import shutil
        # datetime already imported at module level

        basedir = os.path.abspath(os.path.dirname(__file__))
        instance_dir = os.path.join(os.path.dirname(basedir), "instance")

        source_db = os.path.join(instance_dir, "inventory.db")
        backup_name = f"inventory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(instance_dir, backup_name)

        if os.path.exists(source_db):
            shutil.copy2(source_db, backup_path)
            print(f"✅ تم إنشاء نسخة احتياطية: {backup_name}")
            return backup_path
        else:
            print("❌ ملف قاعدة البيانات غير موجود")
            return None

    except Exception as e:
        print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
        return None


def optimize_database():
    """تحسين أداء قاعدة البيانات"""
    from sqlalchemy import text

    try:
        # تشغيل VACUUM لتحسين قاعدة البيانات
        db.session.execute(text("VACUUM;"))

        # تحليل الجداول لتحسين الاستعلامات
        db.session.execute(text("ANALYZE;"))

        db.session.commit()
        print("✅ تم تحسين قاعدة البيانات")
        return True

    except Exception as e:
        print(f"❌ خطأ في تحسين قاعدة البيانات: {e}")
        return False


# دوال مساعدة للتطوير
def reset_database():
    """إعادة تعيين قاعدة البيانات (للتطوير فقط)"""
    try:
        db.drop_all()
        db.create_all()
        create_default_data()
        print("✅ تم إعادة تعيين قاعدة البيانات")
        return True
    except Exception as e:
        print(f"❌ خطأ في إعادة تعيين قاعدة البيانات: {e}")
        return False


def check_database_health():
    """فحص صحة قاعدة البيانات"""
    from sqlalchemy import text

    try:
        # فحص الاتصال
        db.session.execute(text("SELECT 1;"))

        # فحص الجداول الأساسية
        required_tables = ["users", "roles", "products", "categories", "warehouses"]
        existing_tables = db.metadata.tables.keys()

        missing_tables = [
            table for table in required_tables if table not in existing_tables
        ]

        health_status = {
            "connection": True,
            "tables_exist": len(missing_tables) == 0,
            "missing_tables": missing_tables,
            "total_tables": len(existing_tables),
        }

        return health_status

    except Exception as e:
        return {
            "connection": False,
            "error": str(e),
            "tables_exist": False,
            "missing_tables": [],
            "total_tables": 0,
        }
