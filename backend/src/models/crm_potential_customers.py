"""
CRM - Potential Customers
إدارة العملاء المحتملين
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
import json


class PotentialCustomerCRM:
    """
    نظام إدارة العملاء المحتملين (CRM)
    يدير:
    - بطاقات العملاء المحتملين
    - متابعة العملاء المحتملين
    - تحويل العملاء المحتملين إلى عملاء فعليين
    - تقارير العملاء المحتملين
    """

    def __init__(self, db_connection=None):
        """تهيئة نظام CRM"""
        self.db = db_connection
        self._create_tables()

    def _create_tables(self):
        """إنشاء جداول العملاء المحتملين"""
        if not self.db:
            return

        cursor = self.db.cursor()

        # جدول العملاء المحتملين
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS potential_customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                title TEXT,
                sales_engineer_id INTEGER,
                sales_engineer_name TEXT,
                phone TEXT,
                phone2 TEXT,
                email TEXT,
                location TEXT,
                address TEXT,
                city TEXT,
                region TEXT,
                product_types TEXT,
                interested_in_fertilizers BOOLEAN DEFAULT 0,
                interested_in_pesticides BOOLEAN DEFAULT 0,
                interested_in_tools BOOLEAN DEFAULT 0,
                interested_in_seeds BOOLEAN DEFAULT 0,
                interested_in_seedlings BOOLEAN DEFAULT 0,
                company_name TEXT,
                company_type TEXT,
                estimated_value REAL,
                probability INTEGER DEFAULT 50,
                status TEXT DEFAULT 'new',
                source TEXT,
                notes TEXT,
                next_follow_up_date DATE,
                converted_to_customer BOOLEAN DEFAULT 0,
                converted_customer_id INTEGER,
                conversion_date DATE,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sales_engineer_id) REFERENCES users(id),
                FOREIGN KEY (converted_customer_id) REFERENCES contacts(id)
            )
        """
        )

        # جدول متابعات العملاء المحتملين
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS potential_customer_followups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                potential_customer_id INTEGER NOT NULL,
                followup_date DATE NOT NULL,
                followup_type TEXT NOT NULL,
                contact_method TEXT,
                notes TEXT,
                outcome TEXT,
                next_action TEXT,
                next_followup_date DATE,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (potential_customer_id) REFERENCES potential_customers(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """
        )

        # جدول عروض الأسعار للعملاء المحتملين
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS potential_customer_quotations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                potential_customer_id INTEGER NOT NULL,
                quotation_number TEXT NOT NULL UNIQUE,
                quotation_date DATE NOT NULL,
                valid_until DATE,
                total_amount REAL NOT NULL,
                discount_percentage REAL DEFAULT 0,
                discount_amount REAL DEFAULT 0,
                net_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                items TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (potential_customer_id) REFERENCES potential_customers(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """
        )

        # إنشاء فهارس
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_potential_customers_status
            ON potential_customers(status)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_potential_customers_sales_engineer
            ON potential_customers(sales_engineer_id)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_potential_customers_next_followup
            ON potential_customers(next_follow_up_date)
        """
        )

        self.db.commit()

    def create_potential_customer(
        self,
        name: str,
        phone: str,
        sales_engineer_id: Optional[int] = None,
        sales_engineer_name: Optional[str] = None,
        title: Optional[str] = None,
        email: Optional[str] = None,
        location: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        region: Optional[str] = None,
        product_types: Optional[List[str]] = None,
        interested_in_fertilizers: bool = False,
        interested_in_pesticides: bool = False,
        interested_in_tools: bool = False,
        interested_in_seeds: bool = False,
        interested_in_seedlings: bool = False,
        company_name: Optional[str] = None,
        company_type: Optional[str] = None,
        estimated_value: Optional[float] = None,
        probability: int = 50,
        source: Optional[str] = None,
        notes: Optional[str] = None,
        created_by: Optional[int] = None,
    ) -> int:
        """
        إنشاء عميل محتمل جديد

        Args:
            name: اسم العميل المحتمل
            phone: رقم الهاتف
            sales_engineer_id: معرف مهندس المبيعات
            sales_engineer_name: اسم مهندس المبيعات
            title: الصفة/المنصب
            email: البريد الإلكتروني
            location: الموقع
            address: العنوان
            city: المدينة
            region: المنطقة
            product_types: أنواع المنتجات المهتم بها
            interested_in_fertilizers: مهتم بالأسمدة
            interested_in_pesticides: مهتم بالمبيدات
            interested_in_tools: مهتم بالأدوات
            interested_in_seeds: مهتم بالبذور
            interested_in_seedlings: مهتم بالشتلات
            company_name: اسم الشركة
            company_type: نوع الشركة
            estimated_value: القيمة المتوقعة
            probability: احتمالية التحويل (0-100)
            source: مصدر العميل
            notes: ملاحظات
            created_by: معرف المستخدم المنشئ

        Returns:
            معرف العميل المحتمل المُنشأ
        """
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO potential_customers (
                name, title, sales_engineer_id, sales_engineer_name,
                phone, email, location, address, city, region,
                product_types, interested_in_fertilizers, interested_in_pesticides,
                interested_in_tools, interested_in_seeds, interested_in_seedlings,
                company_name, company_type, estimated_value, probability,
                source, notes, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                name,
                title,
                sales_engineer_id,
                sales_engineer_name,
                phone,
                email,
                location,
                address,
                city,
                region,
                json.dumps(product_types) if product_types else None,
                interested_in_fertilizers,
                interested_in_pesticides,
                interested_in_tools,
                interested_in_seeds,
                interested_in_seedlings,
                company_name,
                company_type,
                estimated_value,
                probability,
                source,
                notes,
                created_by,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def add_followup(
        self,
        potential_customer_id: int,
        followup_date: datetime,
        followup_type: str,
        notes: Optional[str] = None,
        contact_method: Optional[str] = None,
        outcome: Optional[str] = None,
        next_action: Optional[str] = None,
        next_followup_date: Optional[datetime] = None,
        created_by: Optional[int] = None,
    ) -> int:
        """
        إضافة متابعة لعميل محتمل

        Args:
            potential_customer_id: معرف العميل المحتمل
            followup_date: تاريخ المتابعة
            followup_type: نوع المتابعة (call, meeting, email, visit, etc.)
            notes: ملاحظات المتابعة
            contact_method: طريقة الاتصال
            outcome: نتيجة المتابعة
            next_action: الإجراء التالي
            next_followup_date: تاريخ المتابعة التالية
            created_by: معرف المستخدم

        Returns:
            معرف المتابعة المُنشأة
        """
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO potential_customer_followups (
                potential_customer_id, followup_date, followup_type,
                contact_method, notes, outcome, next_action,
                next_followup_date, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                potential_customer_id,
                followup_date.date(),
                followup_type,
                contact_method,
                notes,
                outcome,
                next_action,
                next_followup_date.date() if next_followup_date else None,
                created_by,
            ),
        )

        # تحديث تاريخ المتابعة التالية في بطاقة العميل
        if next_followup_date:
            cursor.execute(
                """
                UPDATE potential_customers
                SET next_follow_up_date = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """,
                (next_followup_date.date(), potential_customer_id),
            )

        self.db.commit()
        return cursor.lastrowid

    def convert_to_customer(
        self,
        potential_customer_id: int,
        customer_code: str,
        customer_type: str = "customer",
    ) -> Dict[str, Any]:
        """
        تحويل عميل محتمل إلى عميل فعلي

        Args:
            potential_customer_id: معرف العميل المحتمل
            customer_code: كود العميل الجديد
            customer_type: نوع العميل

        Returns:
            معلومات العميل المُنشأ
        """
        if not self.db:
            return {"success": False, "error": "لا يوجد اتصال بقاعدة البيانات"}

        cursor = self.db.cursor()

        # الحصول على بيانات العميل المحتمل
        cursor.execute(
            "SELECT * FROM potential_customers WHERE id = ?", (potential_customer_id,)
        )
        potential = cursor.fetchone()

        if not potential:
            return {"success": False, "error": "العميل المحتمل غير موجود"}

        # إنشاء عميل جديد في جدول contacts
        cursor.execute(
            """
            INSERT INTO contacts (
                code, name, type, phone, phone2, email, address,
                city, region, company_name, notes, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                customer_code,
                potential[1],  # name
                customer_type,
                potential[5],  # phone
                potential[6],  # phone2
                potential[7],  # email
                potential[9],  # address
                potential[10],  # city
                potential[11],  # region
                potential[17],  # company_name
                potential[23],  # notes
                "active",
            ),
        )

        customer_id = cursor.lastrowid

        # تحديث العميل المحتمل كمحول
        cursor.execute(
            """
            UPDATE potential_customers
            SET converted_to_customer = 1,
                converted_customer_id = ?,
                conversion_date = ?,
                status = 'converted',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (customer_id, datetime.now().date(), potential_customer_id),
        )

        self.db.commit()

        return {
            "success": True,
            "customer_id": customer_id,
            "customer_code": customer_code,
            "message": "تم تحويل العميل المحتمل إلى عميل فعلي بنجاح",
        }

    def get_potential_customers(
        self,
        status: Optional[str] = None,
        sales_engineer_id: Optional[int] = None,
        limit: int = 100,
    ) -> List[Dict]:
        """الحصول على قائمة العملاء المحتملين"""
        if not self.db:
            return []

        cursor = self.db.cursor()
        query = "SELECT * FROM potential_customers WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)
        if sales_engineer_id:
            query += " AND sales_engineer_id = ?"
            params.append(sales_engineer_id)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return [
            dict(zip([col[0] for col in cursor.description], row))
            for row in cursor.fetchall()
        ]
