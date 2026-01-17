"""
Import/Export Service
خدمة الاستيراد والتصدير - استيراد وتصدير البيانات من وإلى Excel/CSV
"""

import pandas as pd
import openpyxl
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
import os
import json


class ImportExportService:
    """
    خدمة الاستيراد والتصدير
    تدعم:
    - استيراد/تصدير الأصناف
    - استيراد/تصدير العملاء
    - استيراد/تصدير الموردين
    - استيراد/تصدير دليل الحسابات
    - استيراد/تصدير الأرصدة الافتتاحية
    """

    def __init__(self, db_connection=None):
        """تهيئة خدمة الاستيراد والتصدير"""
        self.db = db_connection
        self.error_log = []
        self.success_count = 0
        self.error_count = 0

    # ==================== استيراد الأصناف ====================

    def import_products_from_excel(
        self, file_path: str, sheet_name: str = "Products", skip_errors: bool = True
    ) -> Dict[str, Any]:
        """
        استيراد الأصناف من ملف Excel

        Args:
            file_path: مسار ملف Excel
            sheet_name: اسم الورقة
            skip_errors: تخطي الأخطاء أم إيقاف العملية

        Returns:
            تقرير الاستيراد
        """
        self._reset_counters()

        try:
            # قراءة ملف Excel
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            # التحقق من الأعمدة المطلوبة
            required_columns = ["code", "name", "category", "unit", "price"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                return {
                    "success": False,
                    "error": f'الأعمدة المطلوبة مفقودة: {", ".join(missing_columns)}',
                    "required_columns": required_columns,
                    "found_columns": list(df.columns),
                }

            # معالجة كل صف
            for index, row in df.iterrows():
                try:
                    self._import_product_row(row, index + 2)  # type: ignore[arg-type]  # +2 لأن الصف الأول هو العناوين
                    self.success_count += 1
                except Exception as e:
                    self.error_count += 1
                    self._log_error(index + 2, "product", str(e), row.to_dict())  # type: ignore[arg-type]
                    if not skip_errors:
                        raise

            return self._generate_import_report("products")

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "success_count": self.success_count,
                "error_count": self.error_count,
                "errors": self.error_log,
            }

    def _import_product_row(self, row: pd.Series, row_number: int):
        """استيراد صف منتج واحد"""
        if not self.db:
            raise Exception("لا يوجد اتصال بقاعدة البيانات")

        # التحقق من البيانات
        if pd.isna(row["code"]) or pd.isna(row["name"]):
            raise ValueError("كود الصنف والاسم مطلوبان")

        # التحقق من عدم وجود الصنف مسبقاً
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM products WHERE code = ?", (row["code"],))
        existing = cursor.fetchone()

        if existing:
            # تحديث الصنف الموجود
            cursor.execute(
                """
                UPDATE products SET
                    name = ?, category = ?, unit = ?, price = ?,
                    description = ?, barcode = ?, min_stock = ?, max_stock = ?,
                    registration_number = ?, registration_date = ?, expiry_date = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE code = ?
            """,
                (
                    row["name"],
                    row.get("category"),
                    row.get("unit"),
                    row.get("price", 0),
                    row.get("description"),
                    row.get("barcode"),
                    row.get("min_stock", 0),
                    row.get("max_stock", 0),
                    row.get("registration_number"),
                    row.get("registration_date"),
                    row.get("expiry_date"),
                    row["code"],
                ),
            )
        else:
            # إضافة صنف جديد
            cursor.execute(
                """
                INSERT INTO products (
                    code, name, category, unit, price, description, barcode,
                    min_stock, max_stock, registration_number, registration_date,
                    expiry_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    row["code"],
                    row["name"],
                    row.get("category"),
                    row.get("unit"),
                    row.get("price", 0),
                    row.get("description"),
                    row.get("barcode"),
                    row.get("min_stock", 0),
                    row.get("max_stock", 0),
                    row.get("registration_number"),
                    row.get("registration_date"),
                    row.get("expiry_date"),
                ),
            )

        self.db.commit()

    # ==================== استيراد العملاء ====================

    def import_customers_from_excel(
        self, file_path: str, sheet_name: str = "Customers", skip_errors: bool = True
    ) -> Dict[str, Any]:
        """استيراد العملاء من ملف Excel"""
        self._reset_counters()

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            required_columns = ["code", "name", "type"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                return {
                    "success": False,
                    "error": f'الأعمدة المطلوبة مفقودة: {", ".join(missing_columns)}',
                }

            for index, row in df.iterrows():
                try:
                    self._import_customer_row(row, index + 2)  # type: ignore[arg-type]
                    self.success_count += 1
                except Exception as e:
                    self.error_count += 1
                    self._log_error(index + 2, "customer", str(e), row.to_dict())  # type: ignore[arg-type]
                    if not skip_errors:
                        raise

            return self._generate_import_report("customers")

        except Exception as e:
            return {"success": False, "error": str(e), "errors": self.error_log}

    def _import_customer_row(self, row: pd.Series, row_number: int):
        """استيراد صف عميل واحد"""
        if not self.db:
            raise Exception("لا يوجد اتصال بقاعدة البيانات")

        if pd.isna(row["code"]) or pd.isna(row["name"]):
            raise ValueError("كود العميل والاسم مطلوبان")

        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM contacts WHERE code = ?", (row["code"],))
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                """
                UPDATE contacts SET
                    name = ?, type = ?, phone = ?, email = ?, address = ?,
                    tax_number = ?, credit_limit = ?, payment_term_days = ?,
                    grade = ?, status = ?, structure_type = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE code = ?
            """,
                (
                    row["name"],
                    row.get("type", "customer"),
                    row.get("phone"),
                    row.get("email"),
                    row.get("address"),
                    row.get("tax_number"),
                    row.get("credit_limit", 0),
                    row.get("payment_term_days", 0),
                    row.get("grade", "C"),
                    row.get("status", "active"),
                    row.get("structure_type", "individual"),
                    row["code"],
                ),
            )
        else:
            cursor.execute(
                """
                INSERT INTO contacts (
                    code, name, type, phone, email, address, tax_number,
                    credit_limit, payment_term_days, grade, status, structure_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    row["code"],
                    row["name"],
                    row.get("type", "customer"),
                    row.get("phone"),
                    row.get("email"),
                    row.get("address"),
                    row.get("tax_number"),
                    row.get("credit_limit", 0),
                    row.get("payment_term_days", 0),
                    row.get("grade", "C"),
                    row.get("status", "active"),
                    row.get("structure_type", "individual"),
                ),
            )

        self.db.commit()

    # ==================== تصدير البيانات ====================

    def export_products_to_excel(
        self, file_path: str, filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """تصدير الأصناف إلى ملف Excel"""
        try:
            if not self.db:
                raise Exception("لا يوجد اتصال بقاعدة البيانات")

            cursor = self.db.cursor()
            query = "SELECT * FROM products WHERE 1=1"
            params = []

            if filters:
                if "category" in filters:
                    query += " AND category = ?"
                    params.append(filters["category"])
                if "active_only" in filters and filters["active_only"]:
                    query += " AND status = ?"
                    params.append("active")

            cursor.execute(query, params)
            rows = cursor.fetchall()

            # تحويل إلى DataFrame
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

            # حفظ إلى Excel
            df.to_excel(file_path, sheet_name="Products", index=False)

            return {
                "success": True,
                "file_path": file_path,
                "records_count": len(rows),
                "message": f"تم تصدير {len(rows)} صنف بنجاح",
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    # ==================== وظائف مساعدة ====================

    def _reset_counters(self):
        """إعادة تعيين العدادات"""
        self.error_log = []
        self.success_count = 0
        self.error_count = 0

    def _log_error(self, row_number: int, record_type: str, error: str, data: Dict):
        """تسجيل خطأ"""
        self.error_log.append(
            {
                "row_number": row_number,
                "record_type": record_type,
                "error": error,
                "data": data,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def _generate_import_report(self, data_type: str) -> Dict[str, Any]:
        """إنشاء تقرير الاستيراد"""
        return {
            "success": True,
            "data_type": data_type,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "total_count": self.success_count + self.error_count,
            "errors": self.error_log,
            "message": f"تم استيراد {self.success_count} سجل بنجاح، {self.error_count} خطأ",
        }

    def save_error_log_to_file(self, file_path: str) -> bool:
        """حفظ سجل الأخطاء إلى ملف"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.error_log, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
