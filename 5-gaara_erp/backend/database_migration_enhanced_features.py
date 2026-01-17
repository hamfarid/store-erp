#!/usr/bin/env python3
# flake8: noqa: E501
"""
Database Migration Script for Enhanced Features
إضافة الجداول الجديدة للميزات المتقدمة:
- حسابات العملاء والموردين
- الأرصدة الافتتاحية والخزنة
- تحسينات على قيود المخازن وأوامر الرفع والاستلام

Note: Line length checking disabled due to SQL statements
"""

import sqlite3
import os
import sys
import logging

# إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("migration_enhanced_features.log"),
        logging.StreamHandler(),
    ],
)


class EnhancedFeaturesMigration:
    def __init__(self, db_path="inventory_system.db"):
        """
        تهيئة كلاس Migration

        Args:
            db_path (str): مسار قاعدة البيانات
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        """إنشاء اتصال بقاعدة البيانات"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            logging.info(f"تم الاتصال بقاعدة البيانات: {self.db_path}")
            return True
        except Exception as e:
            logging.error(f"فشل في الاتصال بقاعدة البيانات: {e}")
            return False

    def disconnect(self):
        """إغلاق اتصال قاعدة البيانات"""
        if self.connection:
            self.connection.close()
            logging.info("تم إغلاق اتصال قاعدة البيانات")

    def execute_sql(self, sql, params=None):
        """
        تنفيذ استعلام SQL

        Args:
            sql (str): استعلام SQL
            params (tuple): معاملات الاستعلام

        Returns:
            bool: True إذا تم التنفيذ بنجاح
        """
        if not self.cursor or not self.connection:
            logging.error("لا يوجد اتصال بقاعدة البيانات")
            return False

        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.connection.commit()
            return True
        except Exception as e:
            logging.error(f"فشل في تنفيذ الاستعلام: {e}")
            logging.error(f"SQL: {sql}")
            return False

    def table_exists(self, table_name):
        """
        فحص وجود جدول

        Args:
            table_name (str): اسم الجدول

        Returns:
            bool: True إذا كان الجدول موجود
        """
        if not self.cursor:
            logging.error("لا يوجد اتصال بقاعدة البيانات")
            return False

        sql = """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name=?
        """
        try:
            self.cursor.execute(sql, (table_name,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            logging.error(f"خطأ في فحص وجود الجدول {table_name}: {e}")
            return False

    def create_customer_supplier_accounts_table(self):
        """إنشاء جدول حسابات العملاء والموردين"""
        sql = """
        CREATE TABLE IF NOT EXISTS customer_supplier_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number VARCHAR(50) UNIQUE NOT NULL,
            account_name VARCHAR(255) NOT NULL,
            account_type VARCHAR(20) NOT NULL
                CHECK (account_type IN ('customer', 'supplier')),
            currency VARCHAR(3) DEFAULT 'SAR',
            current_balance DECIMAL(15,2) DEFAULT 0.00,
            credit_limit DECIMAL(15,2) DEFAULT 0.00,
            payment_terms VARCHAR(20) DEFAULT 'net_30',
            contact_person VARCHAR(255),
            phone VARCHAR(20),
            email VARCHAR(255),
            address TEXT,
            status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active',
                'inactive',
                'suspended')),
            notes TEXT,
            total_debits DECIMAL(15,2) DEFAULT 0.00,
            total_credits DECIMAL(15,2) DEFAULT 0.00,
            last_transaction_date DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            updated_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (updated_by) REFERENCES users(id)
        )
        """

        if self.execute_sql(sql):
            logging.info("تم إنشاء جدول customer_supplier_accounts بنجاح")

            # إنشاء فهارس
            indexes = [
                (
                    "CREATE INDEX IF NOT EXISTS idx_csa_account_number "
                    "ON customer_supplier_accounts(account_number)"
                ),
                (
                    "CREATE INDEX IF NOT EXISTS idx_csa_account_type "
                    "ON customer_supplier_accounts(account_type)"
                ),
                (
                    "CREATE INDEX IF NOT EXISTS idx_csa_status "
                    "ON customer_supplier_accounts(status)"
                ),
                (
                    "CREATE INDEX IF NOT EXISTS idx_csa_currency "
                    "ON customer_supplier_accounts(currency)"
                ),
            ]

            for index_sql in indexes:
                self.execute_sql(index_sql)

            return True
        return False

    def create_account_transactions_table(self):
        """إنشاء جدول حركات الحسابات"""
        sql = """
        CREATE TABLE IF NOT EXISTS account_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('debit',
                'credit')),
            amount DECIMAL(15,2) NOT NULL,
            description TEXT,
            reference_number VARCHAR(100),
            transaction_date DATE NOT NULL,
            running_balance DECIMAL(15,2) NOT NULL,
            related_document_type VARCHAR(50),
            related_document_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (account_id) REFERENCES customer_supplier_accounts(id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
        """

        if self.execute_sql(sql):
            logging.info("تم إنشاء جدول account_transactions بنجاح")

            # إنشاء فهارس
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_at_account_id ON account_transactions(account_id)",
                "CREATE INDEX IF NOT EXISTS idx_at_transaction_date ON account_transactions(transaction_date)",
                "CREATE INDEX IF NOT EXISTS idx_at_transaction_type ON account_transactions(transaction_type)",
                "CREATE INDEX IF NOT EXISTS idx_at_reference_number ON account_transactions(reference_number)",
            ]

            for index_sql in indexes:
                self.execute_sql(index_sql)

            return True
        return False

    def create_opening_balances_table(self):
        """إنشاء جدول الأرصدة الافتتاحية"""
        sql = """
        CREATE TABLE IF NOT EXISTS opening_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            balance_code VARCHAR(50) UNIQUE NOT NULL,
            balance_name VARCHAR(255) NOT NULL,
            balance_type VARCHAR(20) NOT NULL CHECK (balance_type IN ('customer',
                'supplier',
                'product',
                'warehouse',
                'treasury',
                'general')),
            fiscal_year INTEGER NOT NULL,
            opening_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
            current_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
            currency VARCHAR(3) DEFAULT 'SAR',
            period_start_date DATE NOT NULL,
            period_end_date DATE NOT NULL,
            is_confirmed BOOLEAN DEFAULT FALSE,
            is_posted BOOLEAN DEFAULT FALSE,
            confirmed_at DATETIME,
            posted_at DATETIME,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            updated_by INTEGER,
            confirmed_by INTEGER,
            posted_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (updated_by) REFERENCES users(id),
            FOREIGN KEY (confirmed_by) REFERENCES users(id),
            FOREIGN KEY (posted_by) REFERENCES users(id)
        )
        """

        if self.execute_sql(sql):
            logging.info("تم إنشاء جدول opening_balances بنجاح")

            # إنشاء فهارس
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_ob_balance_code ON opening_balances(balance_code)",
                "CREATE INDEX IF NOT EXISTS idx_ob_balance_type ON opening_balances(balance_type)",
                "CREATE INDEX IF NOT EXISTS idx_ob_fiscal_year ON opening_balances(fiscal_year)",
                "CREATE INDEX IF NOT EXISTS idx_ob_currency ON opening_balances(currency)",
                "CREATE INDEX IF NOT EXISTS idx_ob_is_confirmed ON opening_balances(is_confirmed)",
                "CREATE INDEX IF NOT EXISTS idx_ob_is_posted ON opening_balances(is_posted)",
            ]

            for index_sql in indexes:
                self.execute_sql(index_sql)

            return True
        return False

    def create_treasuries_table(self):
        """إنشاء جدول الخزائن"""
        sql = """
        CREATE TABLE IF NOT EXISTS treasuries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            treasury_code VARCHAR(50) UNIQUE NOT NULL,
            treasury_name VARCHAR(255) NOT NULL,
            treasury_type VARCHAR(20) NOT NULL CHECK (treasury_type IN ('cash',
                'bank',
                'credit_card')),
            currency VARCHAR(3) DEFAULT 'SAR',
            initial_balance DECIMAL(15,2) DEFAULT 0.00,
            current_balance DECIMAL(15,2) DEFAULT 0.00,
            available_balance DECIMAL(15,2) DEFAULT 0.00,
            daily_limit DECIMAL(15,2) DEFAULT 0.00,
            monthly_limit DECIMAL(15,2) DEFAULT 0.00,
            location VARCHAR(255),
            responsible_person VARCHAR(255),
            bank_name VARCHAR(255),
            account_number VARCHAR(100),
            iban VARCHAR(50),
            swift_code VARCHAR(20),
            status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active',
                'inactive',
                'suspended')),
            notes TEXT,
            last_transaction_date DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            updated_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id),
            FOREIGN KEY (updated_by) REFERENCES users(id)
        )
        """

        if self.execute_sql(sql):
            logging.info("تم إنشاء جدول treasuries بنجاح")

            # إنشاء فهارس
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_t_treasury_code ON treasuries(treasury_code)",
                "CREATE INDEX IF NOT EXISTS idx_t_treasury_type ON treasuries(treasury_type)",
                "CREATE INDEX IF NOT EXISTS idx_t_currency ON treasuries(currency)",
                "CREATE INDEX IF NOT EXISTS idx_t_status ON treasuries(status)",
            ]

            for index_sql in indexes:
                self.execute_sql(index_sql)

            return True
        return False

    def create_treasury_transactions_table(self):
        """إنشاء جدول حركات الخزنة"""
        sql = """
        CREATE TABLE IF NOT EXISTS treasury_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            treasury_id INTEGER NOT NULL,
            transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('receipt',
                'payment',
                'transfer_in',
                'transfer_out')),
            amount DECIMAL(15,2) NOT NULL,
            description TEXT,
            counterpart_type VARCHAR(20),
            counterpart_id INTEGER,
            reference_number VARCHAR(100),
            transaction_date DATE NOT NULL,
            running_balance DECIMAL(15,2) NOT NULL,
            related_document_type VARCHAR(50),
            related_document_id INTEGER,
            transfer_to_treasury_id INTEGER,
            exchange_rate DECIMAL(10,4) DEFAULT 1.0000,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (treasury_id) REFERENCES treasuries(id) ON DELETE CASCADE,
            FOREIGN KEY (transfer_to_treasury_id) REFERENCES treasuries(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
        """

        if self.execute_sql(sql):
            logging.info("تم إنشاء جدول treasury_transactions بنجاح")

            # إنشاء فهارس
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_tt_treasury_id ON treasury_transactions(treasury_id)",
                "CREATE INDEX IF NOT EXISTS idx_tt_transaction_date ON treasury_transactions(transaction_date)",
                "CREATE INDEX IF NOT EXISTS idx_tt_transaction_type ON treasury_transactions(transaction_type)",
                "CREATE INDEX IF NOT EXISTS idx_tt_reference_number ON treasury_transactions(reference_number)",
            ]

            for index_sql in indexes:
                self.execute_sql(index_sql)

            return True
        return False

    def enhance_existing_tables(self):
        """تحسين الجداول الموجودة"""
        enhancements = []

        # تحسينات على جدول warehouse_constraints
        if self.table_exists("warehouse_constraints"):
            enhancements.extend(
                [
                    "ALTER TABLE warehouse_constraints ADD COLUMN priority_level INTEGER DEFAULT 1",
                    "ALTER TABLE warehouse_constraints ADD COLUMN auto_apply BOOLEAN DEFAULT FALSE",
                    "ALTER TABLE warehouse_constraints ADD COLUMN notification_enabled BOOLEAN DEFAULT TRUE",
                ]
            )

        # تحسينات على جدول pickup_delivery_orders
        if self.table_exists("pickup_delivery_orders"):
            enhancements.extend(
                [
                    "ALTER TABLE pickup_delivery_orders ADD COLUMN estimated_duration INTEGER",
                    "ALTER TABLE pickup_delivery_orders ADD COLUMN actual_duration INTEGER",
                    "ALTER TABLE pickup_delivery_orders ADD COLUMN driver_id INTEGER",
                    "ALTER TABLE pickup_delivery_orders ADD COLUMN vehicle_id INTEGER",
                    "ALTER TABLE pickup_delivery_orders ADD COLUMN tracking_number VARCHAR(100)",
                ]
            )

        # تطبيق التحسينات
        for enhancement in enhancements:
            try:
                self.execute_sql(enhancement)
                logging.info(f"تم تطبيق التحسين: {enhancement}")
            except Exception as e:
                logging.warning(f"فشل في تطبيق التحسين: {enhancement} - {e}")

    def create_enhanced_reports_views(self):
        """إنشاء views للتقارير المحسنة"""
        views = [
            # عرض ملخص حسابات العملاء والموردين
            """
            CREATE VIEW IF NOT EXISTS v_customer_supplier_summary AS
            SELECT
                csa.id,
                csa.account_number,
                csa.account_name,
                csa.account_type,
                csa.currency,
                csa.current_balance,
                csa.credit_limit,
                (csa.credit_limit - csa.current_balance) as available_credit,
                csa.payment_terms,
                csa.status,
                COUNT(at.id) as transactions_count,
                MAX(at.transaction_date) as last_transaction_date,
                SUM(CASE WHEN at.transaction_type = 'debit' THEN at.amount ELSE 0 END) as total_debits,
                SUM(CASE WHEN at.transaction_type = 'credit' THEN at.amount ELSE 0 END) as total_credits
            FROM customer_supplier_accounts csa
            LEFT JOIN account_transactions at ON csa.id = at.account_id
            GROUP BY csa.id
            """,
            # عرض ملخص الخزائن
            """
            CREATE VIEW IF NOT EXISTS v_treasury_summary AS
            SELECT
                t.id,
                t.treasury_code,
                t.treasury_name,
                t.treasury_type,
                t.currency,
                t.current_balance,
                t.available_balance,
                t.daily_limit,
                t.monthly_limit,
                t.status,
                COUNT(tt.id) as transactions_count,
                MAX(tt.transaction_date) as last_transaction_date,
                SUM(CASE WHEN tt.transaction_type IN ('receipt',
                    'transfer_in') THEN tt.amount ELSE 0 END) as total_receipts,
                SUM(CASE WHEN tt.transaction_type IN ('payment',
                    'transfer_out') THEN tt.amount ELSE 0 END) as total_payments
            FROM treasuries t
            LEFT JOIN treasury_transactions tt ON t.id = tt.treasury_id
            GROUP BY t.id
            """,
            # عرض الأرصدة الافتتاحية المؤكدة
            """
            CREATE VIEW IF NOT EXISTS v_confirmed_opening_balances AS
            SELECT
                ob.*,
                u1.username as created_by_username,
                u2.username as confirmed_by_username,
                u3.username as posted_by_username
            FROM opening_balances ob
            LEFT JOIN users u1 ON ob.created_by = u1.id
            LEFT JOIN users u2 ON ob.confirmed_by = u2.id
            LEFT JOIN users u3 ON ob.posted_by = u3.id
            WHERE ob.is_confirmed = TRUE
            """,
        ]

        for view_sql in views:
            if self.execute_sql(view_sql):
                logging.info("تم إنشاء view بنجاح")
            else:
                logging.error(f"فشل في إنشاء view: {view_sql[:100]}...")

    def insert_sample_data(self):
        """إدراج بيانات تجريبية"""
        try:
            # إدراج خزنة افتراضية
            treasury_sql = """
            INSERT OR IGNORE INTO treasuries
            (treasury_code,
                treasury_name,
                treasury_type,
                currency,
                initial_balance,
                current_balance,
                available_balance,
                daily_limit,
                monthly_limit,
                location,
                responsible_person,
                status,
                created_by)
            VALUES
            ('CASH001',
                'الخزنة الرئيسية',
                'cash',
                'SAR',
                10000.00,
                10000.00,
                10000.00,
                5000.00,
                50000.00,
                'المكتب الرئيسي',
                'أمين الصندوق',
                'active',
                1)
            """
            self.execute_sql(treasury_sql)

            # إدراج رصيد افتتاحي تجريبي
            opening_balance_sql = """
            INSERT OR IGNORE INTO opening_balances
            (balance_code,
                balance_name,
                balance_type,
                fiscal_year,
                opening_balance,
                current_balance,
                currency,
                period_start_date,
                period_end_date,
                is_confirmed,
                created_by)
            VALUES
            ('OB2024001',
                'رصيد افتتاحي للخزنة الرئيسية',
                'treasury',
                2024,
                10000.00,
                10000.00,
                'SAR',
                '2024-01-01',
                '2024-12-31',
                TRUE,
                1)
            """
            self.execute_sql(opening_balance_sql)

            logging.info("تم إدراج البيانات التجريبية بنجاح")

        except Exception as e:
            logging.error(f"فشل في إدراج البيانات التجريبية: {e}")

    def create_triggers(self):
        """إنشاء triggers لتحديث الأرصدة تلقائياً"""
        triggers = [
            # Trigger لتحديث رصيد الحساب عند إضافة حركة
            """
            CREATE TRIGGER IF NOT EXISTS update_account_balance_after_transaction
            AFTER INSERT ON account_transactions
            BEGIN
                UPDATE customer_supplier_accounts
                SET
                    current_balance = current_balance +
                        CASE
                            WHEN NEW.transaction_type = 'debit' THEN NEW.amount
                            ELSE -NEW.amount
                        END,
                    total_debits = total_debits +
                        CASE
                            WHEN NEW.transaction_type = 'debit' THEN NEW.amount
                            ELSE 0
                        END,
                    total_credits = total_credits +
                        CASE
                            WHEN NEW.transaction_type = 'credit' THEN NEW.amount
                            ELSE 0
                        END,
                    last_transaction_date = NEW.transaction_date,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = NEW.account_id;
            END
            """,
            # Trigger لتحديث رصيد الخزنة عند إضافة حركة
            """
            CREATE TRIGGER IF NOT EXISTS update_treasury_balance_after_transaction
            AFTER INSERT ON treasury_transactions
            BEGIN
                UPDATE treasuries
                SET
                    current_balance = current_balance +
                        CASE
                            WHEN NEW.transaction_type IN ('receipt',
                                'transfer_in') THEN NEW.amount
                            ELSE -NEW.amount
                        END,
                    available_balance = current_balance,
                    last_transaction_date = NEW.transaction_date,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = NEW.treasury_id;
            END
            """,
            # Trigger لتحديث updated_at عند تعديل الحسابات
            """
            CREATE TRIGGER IF NOT EXISTS update_account_timestamp
            AFTER UPDATE ON customer_supplier_accounts
            BEGIN
                UPDATE customer_supplier_accounts
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = NEW.id;
            END
            """,
            # Trigger لتحديث updated_at عند تعديل الخزائن
            """
            CREATE TRIGGER IF NOT EXISTS update_treasury_timestamp
            AFTER UPDATE ON treasuries
            BEGIN
                UPDATE treasuries
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = NEW.id;
            END
            """,
        ]

        for trigger_sql in triggers:
            if self.execute_sql(trigger_sql):
                logging.info("تم إنشاء trigger بنجاح")
            else:
                logging.error("فشل في إنشاء trigger")

    def run_migration(self):
        """تشغيل عملية Migration الكاملة"""
        logging.info("بدء عملية Migration للميزات المحسنة...")

        if not self.connect():
            return False

        try:
            # إنشاء الجداول الجديدة
            tables_created = 0

            if self.create_customer_supplier_accounts_table():
                tables_created += 1

            if self.create_account_transactions_table():
                tables_created += 1

            if self.create_opening_balances_table():
                tables_created += 1

            if self.create_treasuries_table():
                tables_created += 1

            if self.create_treasury_transactions_table():
                tables_created += 1

            logging.info(f"تم إنشاء {tables_created} جدول جديد")

            # تحسين الجداول الموجودة
            self.enhance_existing_tables()

            # إنشاء Views للتقارير
            self.create_enhanced_reports_views()

            # إنشاء Triggers
            self.create_triggers()

            # إدراج البيانات التجريبية
            self.insert_sample_data()

            logging.info("تمت عملية Migration بنجاح!")
            return True

        except Exception as e:
            logging.error(f"فشلت عملية Migration: {e}")
            return False

        finally:
            self.disconnect()

    def verify_migration(self):
        """التحقق من نجاح عملية Migration"""
        if not self.connect():
            return False

        try:
            required_tables = [
                "customer_supplier_accounts",
                "account_transactions",
                "opening_balances",
                "treasuries",
                "treasury_transactions",
            ]

            missing_tables = []
            for table in required_tables:
                if not self.table_exists(table):
                    missing_tables.append(table)

            if missing_tables:
                logging.error(f"الجداول التالية مفقودة: {missing_tables}")
                return False

            # فحص عدد الأعمدة في كل جدول
            if self.cursor:
                for table in required_tables:
                    self.cursor.execute(f"PRAGMA table_info({table})")
                    columns = self.cursor.fetchall()
                    logging.info(f"جدول {table}: {len(columns)} عمود")

            logging.info("تم التحقق من Migration بنجاح - جميع الجداول موجودة")
            return True

        except Exception as e:
            logging.error(f"فشل في التحقق من Migration: {e}")
            return False

        finally:
            self.disconnect()


def main():
    """الدالة الرئيسية"""
    print("🚀 بدء عملية Migration للميزات المحسنة...")

    # تحديد مسار قاعدة البيانات
    db_path = os.path.join(os.path.dirname(__file__), "inventory_system.db")

    # إنشاء كائن Migration
    migration = EnhancedFeaturesMigration(db_path)

    # تشغيل Migration
    if migration.run_migration():
        print("✅ تمت عملية Migration بنجاح!")

        # التحقق من النتائج
        if migration.verify_migration():
            print("✅ تم التحقق من Migration بنجاح!")
        else:
            print("❌ فشل في التحقق من Migration")
            return 1
    else:
        print("❌ فشلت عملية Migration")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
