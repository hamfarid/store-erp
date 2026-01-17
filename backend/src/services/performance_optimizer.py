#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/performance_optimizer.py

خدمة تحسين الأداء واستعلامات قاعدة البيانات
Performance Optimizer Service

تشمل:
- تحسين استعلامات قاعدة البيانات
- إدارة الفهارس (Indexes)
- تحسين الذاكرة والتخزين المؤقت
- مراقبة الأداء
- تحليل الاستعلامات البطيئة
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy import text, func, inspect, Index
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from flask import current_app
import logging
import time
import json
from decimal import Decimal
import psutil
import threading
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """خدمة تحسين الأداء واستعلامات قاعدة البيانات"""

    def __init__(self, db_session: Session, engine: Engine):
        self.db = db_session
        self.engine = engine
        self.query_cache = {}
        self.slow_queries = deque(maxlen=100)  # آخر 100 استعلام بطيء
        self.performance_metrics = defaultdict(list)
        self._cache_lock = threading.Lock()

    # ==================== تحسين الاستعلامات ====================

    def optimize_query_performance(self) -> Dict[str, Any]:
        """تحسين أداء الاستعلامات العامة"""
        try:
            optimizations = []

            # 1. تحليل الاستعلامات البطيئة
            slow_queries_analysis = self._analyze_slow_queries()
            optimizations.append(
                {"type": "slow_queries_analysis", "data": slow_queries_analysis}
            )

            # 2. تحسين فهارس قاعدة البيانات
            indexes_optimization = self._optimize_database_indexes()
            optimizations.append(
                {"type": "indexes_optimization", "data": indexes_optimization}
            )

            # 3. تحسين استعلامات التقارير
            reports_optimization = self._optimize_reports_queries()
            optimizations.append(
                {"type": "reports_optimization", "data": reports_optimization}
            )

            # 4. تحسين استعلامات المخزون
            inventory_optimization = self._optimize_inventory_queries()
            optimizations.append(
                {"type": "inventory_optimization", "data": inventory_optimization}
            )

            return {
                "success": True,
                "data": {
                    "optimizations": optimizations,
                    "total_optimizations": len(optimizations),
                    "optimization_date": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"خطأ في تحسين أداء الاستعلامات: {str(e)}")
            return {"success": False, "error": str(e)}

    def _analyze_slow_queries(self) -> Dict[str, Any]:
        """تحليل الاستعلامات البطيئة"""
        try:
            # تحليل آخر 100 استعلام بطيء
            slow_queries_data = []
            total_slow_time = 0

            for query_info in self.slow_queries:
                slow_queries_data.append(
                    {
                        "query": (
                            query_info["query"][:200] + "..."
                            if len(query_info["query"]) > 200
                            else query_info["query"]
                        ),
                        "execution_time": query_info["execution_time"],
                        "timestamp": query_info["timestamp"],
                        "table_scans": query_info.get("table_scans", 0),
                        "rows_examined": query_info.get("rows_examined", 0),
                    }
                )
                total_slow_time += query_info["execution_time"]

            # اقتراحات التحسين
            suggestions = []

            if len(slow_queries_data) > 10:
                suggestions.append(
                    {
                        "type": "high_slow_queries_count",
                        "message": f"عدد كبير من الاستعلامات البطيئة: {len(slow_queries_data)}",
                        "recommendation": "يُنصح بمراجعة الفهارس وتحسين الاستعلامات",
                    }
                )

            if total_slow_time > 30:  # أكثر من 30 ثانية إجمالي
                suggestions.append(
                    {
                        "type": "high_total_slow_time",
                        "message": f"إجمالي وقت الاستعلامات البطيئة: {total_slow_time:.2f} ثانية",
                        "recommendation": "يُنصح بتحسين الاستعلامات الأكثر استخداماً",
                    }
                )

            return {
                "slow_queries_count": len(slow_queries_data),
                "total_slow_time": total_slow_time,
                "avg_slow_time": (
                    total_slow_time / len(slow_queries_data) if slow_queries_data else 0
                ),
                "slow_queries": slow_queries_data[-10:],  # آخر 10 استعلامات
                "suggestions": suggestions,
            }

        except Exception as e:
            logger.error(f"خطأ في تحليل الاستعلامات البطيئة: {str(e)}")
            return {"error": str(e)}

    def _optimize_database_indexes(self) -> Dict[str, Any]:
        """تحسين فهارس قاعدة البيانات"""
        try:
            # قائمة الفهارس المقترحة للتحسين
            suggested_indexes = [
                {
                    "table": "products",
                    "columns": ["sku"],
                    "type": "unique",
                    "reason": "تحسين البحث بـ SKU",
                },
                {
                    "table": "products",
                    "columns": ["category_id", "active"],
                    "type": "composite",
                    "reason": "تحسين فلترة المنتجات حسب الفئة والحالة",
                },
                {
                    "table": "stock_movements",
                    "columns": ["product_id", "warehouse_id", "created_at"],
                    "type": "composite",
                    "reason": "تحسين تقارير حركة المخزون",
                },
                {
                    "table": "sales_invoices",
                    "columns": ["customer_id", "invoice_date"],
                    "type": "composite",
                    "reason": "تحسين تقارير مبيعات العملاء",
                },
                {
                    "table": "sales_invoices",
                    "columns": ["sales_person_id", "invoice_date"],
                    "type": "composite",
                    "reason": "تحسين تقارير مبيعات المهندسين",
                },
                {
                    "table": "sales_invoice_items",
                    "columns": ["product_id", "invoice_id"],
                    "type": "composite",
                    "reason": "تحسين تقارير مبيعات المنتجات",
                },
                {
                    "table": "customers",
                    "columns": ["sales_engineer_id"],
                    "type": "index",
                    "reason": "تحسين ربط العملاء بالمهندسين",
                },
                {
                    "table": "batches",
                    "columns": ["expiry_date", "product_id"],
                    "type": "composite",
                    "reason": "تحسين تقارير انتهاء الصلاحية",
                },
            ]

            # فحص الفهارس الموجودة
            existing_indexes = self._get_existing_indexes()

            # تحديد الفهارس المفقودة
            missing_indexes = []
            for suggested in suggested_indexes:
                index_exists = self._check_index_exists(
                    suggested["table"], suggested["columns"], existing_indexes
                )

                if not index_exists:
                    missing_indexes.append(suggested)

            # إنشاء الفهارس المفقودة
            created_indexes = []
            for index_info in missing_indexes:
                try:
                    success = self._create_index(index_info)
                    if success:
                        created_indexes.append(index_info)
                except Exception as e:
                    logger.warning(f"فشل في إنشاء الفهرس {index_info}: {str(e)}")

            return {
                "total_suggested": len(suggested_indexes),
                "existing_indexes_count": len(existing_indexes),
                "missing_indexes_count": len(missing_indexes),
                "created_indexes_count": len(created_indexes),
                "created_indexes": created_indexes,
                "missing_indexes": missing_indexes,
            }

        except Exception as e:
            logger.error(f"خطأ في تحسين فهارس قاعدة البيانات: {str(e)}")
            return {"error": str(e)}

    def _get_existing_indexes(self) -> List[Dict]:
        """الحصول على الفهارس الموجودة"""
        try:
            inspector = inspect(self.engine)
            all_indexes = []

            # الحصول على جميع الجداول
            tables = inspector.get_table_names()

            for table in tables:
                indexes = inspector.get_indexes(table)
                for index in indexes:
                    all_indexes.append(
                        {
                            "table": table,
                            "name": index["name"],
                            "columns": index["column_names"],
                            "unique": index["unique"],
                        }
                    )

            return all_indexes

        except Exception as e:
            logger.error(f"خطأ في الحصول على الفهارس الموجودة: {str(e)}")
            return []

    def _check_index_exists(
        self, table: str, columns: List[str], existing_indexes: List[Dict]
    ) -> bool:
        """فحص وجود فهرس معين"""
        for index in existing_indexes:
            if index["table"] == table and set(index["columns"]) == set(columns):
                return True
        return False

    def _create_index(self, index_info: Dict) -> bool:
        """إنشاء فهرس جديد"""
        try:
            table = index_info["table"]
            columns = index_info["columns"]
            index_type = index_info.get("type", "index")

            # تكوين اسم الفهرس
            index_name = f"idx_{table}_{'_'.join(columns)}"

            # تكوين SQL لإنشاء الفهرس
            columns_str = ", ".join(columns)

            if index_type == "unique":
                sql = f"CREATE UNIQUE INDEX {index_name} ON {table} ({columns_str})"
            else:
                sql = f"CREATE INDEX {index_name} ON {table} ({columns_str})"

            # تنفيذ الاستعلام
            self.db.execute(text(sql))
            self.db.commit()

            logger.info(f"تم إنشاء الفهرس: {index_name}")
            return True

        except Exception as e:
            logger.error(f"خطأ في إنشاء الفهرس: {str(e)}")
            self.db.rollback()
            return False

    def _optimize_reports_queries(self) -> Dict[str, Any]:
        """تحسين استعلامات التقارير"""
        try:
            optimizations = []

            # 1. تحسين استعلام تقرير المبيعات
            sales_optimization = self._optimize_sales_report_query()
            optimizations.append(
                {"query_type": "sales_report", "optimization": sales_optimization}
            )

            # 2. تحسين استعلام تقرير المخزون
            inventory_optimization = self._optimize_inventory_report_query()
            optimizations.append(
                {
                    "query_type": "inventory_report",
                    "optimization": inventory_optimization,
                }
            )

            # 3. تحسين استعلام تقرير العملاء
            customers_optimization = self._optimize_customers_report_query()
            optimizations.append(
                {
                    "query_type": "customers_report",
                    "optimization": customers_optimization,
                }
            )

            return {
                "optimized_queries": len(optimizations),
                "optimizations": optimizations,
            }

        except Exception as e:
            logger.error(f"خطأ في تحسين استعلامات التقارير: {str(e)}")
            return {"error": str(e)}

    def _optimize_sales_report_query(self) -> Dict[str, Any]:
        """تحسين استعلام تقرير المبيعات"""
        try:
            # إنشاء view محسن لتقرير المبيعات
            optimized_view_sql = """
            CREATE OR REPLACE VIEW v_sales_report_optimized AS
            SELECT
                si.id as invoice_id,
                si.invoice_number,
                si.invoice_date,
                si.total_amount,
                si.paid_amount,
                (si.total_amount - si.paid_amount) as outstanding_amount,
                c.id as customer_id,
                c.name as customer_name,
                u.id as sales_person_id,
                u.username as sales_person_name,
                COUNT(sii.id) as items_count,
                SUM(sii.quantity) as total_quantity
            FROM sales_invoices si
            LEFT JOIN customers c ON si.customer_id = c.id
            LEFT JOIN users u ON si.sales_person_id = u.id
            LEFT JOIN sales_invoice_items sii ON si.id = sii.invoice_id
            GROUP BY si.id,
                si.invoice_number,
                si.invoice_date,
                si.total_amount,
                     si.paid_amount, c.id, c.name, u.id, u.username
            """

            self.db.execute(text(optimized_view_sql))
            self.db.commit()

            return {
                "status": "success",
                "message": "تم إنشاء view محسن لتقرير المبيعات",
                "view_name": "v_sales_report_optimized",
            }

        except Exception as e:
            logger.error(f"خطأ في تحسين استعلام تقرير المبيعات: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _optimize_inventory_report_query(self) -> Dict[str, Any]:
        """تحسين استعلام تقرير المخزون"""
        try:
            # إنشاء view محسن لتقرير المخزون
            optimized_view_sql = """
            CREATE OR REPLACE VIEW v_inventory_report_optimized AS
            SELECT
                p.id as product_id,
                p.name as product_name,
                p.sku,
                p.cost_price,
                p.selling_price,
                c.name as category_name,
                w.id as warehouse_id,
                w.name as warehouse_name,
                COALESCE(SUM(sm.quantity_change), 0) as current_stock,
                COALESCE(SUM(sm.quantity_change * p.cost_price),
                    0) as stock_value,
                COUNT(sm.id) as movement_count,
                MAX(sm.created_at) as last_movement_date
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN stock_movements sm ON p.id = sm.product_id
            LEFT JOIN warehouses w ON sm.warehouse_id = w.id
            WHERE p.active = true
            GROUP BY p.id, p.name, p.sku, p.cost_price, p.selling_price,
                     c.name, w.id, w.name
            """

            self.db.execute(text(optimized_view_sql))
            self.db.commit()

            return {
                "status": "success",
                "message": "تم إنشاء view محسن لتقرير المخزون",
                "view_name": "v_inventory_report_optimized",
            }

        except Exception as e:
            logger.error(f"خطأ في تحسين استعلام تقرير المخزون: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _optimize_customers_report_query(self) -> Dict[str, Any]:
        """تحسين استعلام تقرير العملاء"""
        try:
            # إنشاء view محسن لتقرير العملاء
            optimized_view_sql = """
            CREATE OR REPLACE VIEW v_customers_report_optimized AS
            SELECT
                c.id as customer_id,
                c.name as customer_name,
                c.phone,
                c.email,
                c.address,
                u.username as sales_engineer_name,
                COUNT(si.id) as invoices_count,
                COALESCE(SUM(si.total_amount), 0) as total_sales,
                COALESCE(SUM(si.paid_amount), 0) as total_paid,
                COALESCE(SUM(si.total_amount - si.paid_amount),
                    0) as outstanding_amount,
                MAX(si.invoice_date) as last_invoice_date,
                MIN(si.invoice_date) as first_invoice_date
            FROM customers c
            LEFT JOIN users u ON c.sales_engineer_id = u.id
            LEFT JOIN sales_invoices si ON c.id = si.customer_id
            GROUP BY c.id, c.name, c.phone, c.email, c.address, u.username
            """

            self.db.execute(text(optimized_view_sql))
            self.db.commit()

            return {
                "status": "success",
                "message": "تم إنشاء view محسن لتقرير العملاء",
                "view_name": "v_customers_report_optimized",
            }

        except Exception as e:
            logger.error(f"خطأ في تحسين استعلام تقرير العملاء: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _optimize_inventory_queries(self) -> Dict[str, Any]:
        """تحسين استعلامات المخزون"""
        try:
            optimizations = []

            # 1. تحسين استعلام حساب الرصيد الحالي
            current_stock_optimization = self._create_current_stock_function()
            optimizations.append(
                {"type": "current_stock_function", "result": current_stock_optimization}
            )

            # 2. تحسين استعلام حركات المخزون
            stock_movements_optimization = self._optimize_stock_movements_query()
            optimizations.append(
                {
                    "type": "stock_movements_optimization",
                    "result": stock_movements_optimization,
                }
            )

            return {
                "optimizations_count": len(optimizations),
                "optimizations": optimizations,
            }

        except Exception as e:
            logger.error(f"خطأ في تحسين استعلامات المخزون: {str(e)}")
            return {"error": str(e)}

    def _create_current_stock_function(self) -> Dict[str, Any]:
        """إنشاء دالة محسنة لحساب الرصيد الحالي"""
        try:
            # إنشاء دالة SQL محسنة لحساب الرصيد
            function_sql = """
            CREATE OR REPLACE FUNCTION get_current_stock(
                p_product_id INTEGER,
                p_warehouse_id INTEGER DEFAULT NULL
            ) RETURNS DECIMAL(15,3) AS $$
            DECLARE
                current_stock DECIMAL(15,3) := 0;
            BEGIN
                SELECT COALESCE(SUM(quantity_change), 0)
                INTO current_stock
                FROM stock_movements
                WHERE product_id = p_product_id
                AND (p_warehouse_id IS NULL OR warehouse_id = p_warehouse_id);

                RETURN current_stock;
            END;
            $$ LANGUAGE plpgsql;
            """

            self.db.execute(text(function_sql))
            self.db.commit()

            return {
                "status": "success",
                "message": "تم إنشاء دالة محسنة لحساب الرصيد الحالي",
                "function_name": "get_current_stock",
            }

        except Exception as e:
            logger.error(f"خطأ في إنشاء دالة الرصيد الحالي: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _optimize_stock_movements_query(self) -> Dict[str, Any]:
        """تحسين استعلام حركات المخزون"""
        try:
            # إنشاء view محسن لحركات المخزون
            optimized_view_sql = """
            CREATE OR REPLACE VIEW v_stock_movements_optimized AS
            SELECT
                sm.id,
                sm.movement_type,
                sm.quantity_change,
                sm.reference_type,
                sm.reference_id,
                sm.notes,
                sm.created_at,
                p.name as product_name,
                p.sku,
                w.name as warehouse_name,
                u.username as created_by_name,
                CASE
                    WHEN sm.movement_type = 'in' THEN 'وارد'
                    WHEN sm.movement_type = 'out' THEN 'صادر'
                    WHEN sm.movement_type = 'transfer' THEN 'تحويل'
                    WHEN sm.movement_type = 'adjustment' THEN 'تسوية'
                    ELSE sm.movement_type
                END as movement_type_ar
            FROM stock_movements sm
            LEFT JOIN products p ON sm.product_id = p.id
            LEFT JOIN warehouses w ON sm.warehouse_id = w.id
            LEFT JOIN users u ON sm.created_by = u.id
            ORDER BY sm.created_at DESC
            """

            self.db.execute(text(optimized_view_sql))
            self.db.commit()

            return {
                "status": "success",
                "message": "تم إنشاء view محسن لحركات المخزون",
                "view_name": "v_stock_movements_optimized",
            }

        except Exception as e:
            logger.error(f"خطأ في تحسين استعلام حركات المخزون: {str(e)}")
            return {"status": "error", "message": str(e)}

    # ==================== مراقبة الأداء ====================

    def monitor_query_performance(
        self, query: str, execution_time: float, additional_info: Dict = None
    ):
        """مراقبة أداء الاستعلامات"""
        try:
            # تسجيل الاستعلام إذا كان بطيئاً (أكثر من ثانية واحدة)
            if execution_time > 1.0:
                query_info = {
                    "query": query,
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat(),
                    "additional_info": additional_info or {},
                }

                with self._cache_lock:
                    self.slow_queries.append(query_info)

            # تسجيل مقاييس الأداء
            current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)

            with self._cache_lock:
                self.performance_metrics[current_hour].append(
                    {
                        "execution_time": execution_time,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        except Exception as e:
            logger.error(f"خطأ في مراقبة أداء الاستعلام: {str(e)}")

    def get_performance_metrics(self, hours_back: int = 24) -> Dict[str, Any]:
        """الحصول على مقاييس الأداء"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours_back)

            metrics_data = []
            total_queries = 0
            total_time = 0
            slow_queries_count = 0

            with self._cache_lock:
                for hour, queries in self.performance_metrics.items():
                    if hour >= cutoff_time:
                        hour_queries = len(queries)
                        hour_total_time = sum(q["execution_time"] for q in queries)
                        hour_avg_time = (
                            hour_total_time / hour_queries if hour_queries else 0
                        )
                        hour_slow_queries = sum(
                            1 for q in queries if q["execution_time"] > 1.0
                        )

                        metrics_data.append(
                            {
                                "hour": hour.isoformat(),
                                "queries_count": hour_queries,
                                "total_time": hour_total_time,
                                "avg_time": hour_avg_time,
                                "slow_queries_count": hour_slow_queries,
                            }
                        )

                        total_queries += hour_queries
                        total_time += hour_total_time
                        slow_queries_count += hour_slow_queries

            # إحصائيات النظام
            system_stats = self._get_system_stats()

            return {
                "success": True,
                "data": {
                    "time_range_hours": hours_back,
                    "total_queries": total_queries,
                    "total_execution_time": total_time,
                    "avg_execution_time": (
                        total_time / total_queries if total_queries else 0
                    ),
                    "slow_queries_count": slow_queries_count,
                    "slow_queries_percentage": (
                        (slow_queries_count / total_queries * 100)
                        if total_queries
                        else 0
                    ),
                    "hourly_metrics": metrics_data,
                    "system_stats": system_stats,
                    "generated_at": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"خطأ في الحصول على مقاييس الأداء: {str(e)}")
            return {"success": False, "error": str(e)}

    def _get_system_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات النظام"""
        try:
            # إحصائيات الذاكرة
            memory = psutil.virtual_memory()

            # إحصائيات المعالج
            cpu_percent = psutil.cpu_percent(interval=1)

            # إحصائيات القرص
            disk = psutil.disk_usage("/")

            return {
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "percentage": memory.percent,
                },
                "cpu": {"percentage": cpu_percent, "count": psutil.cpu_count()},
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percentage": (disk.used / disk.total) * 100,
                },
            }

        except Exception as e:
            logger.error(f"خطأ في الحصول على إحصائيات النظام: {str(e)}")
            return {"error": str(e)}

    # ==================== تنظيف وصيانة ====================

    def cleanup_old_data(self, days_to_keep: int = 90) -> Dict[str, Any]:
        """تنظيف البيانات القديمة"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            cleanup_results = []

            # تنظيف سجلات الأداء القديمة
            with self._cache_lock:
                old_metrics = [
                    hour
                    for hour in self.performance_metrics.keys()
                    if hour < cutoff_date
                ]

                for hour in old_metrics:
                    del self.performance_metrics[hour]

                cleanup_results.append(
                    {"type": "performance_metrics", "cleaned_hours": len(old_metrics)}
                )

            # تنظيف الاستعلامات البطيئة القديمة
            old_slow_queries = []
            for query in list(self.slow_queries):
                query_time = datetime.fromisoformat(query["timestamp"])
                if query_time < cutoff_date:
                    old_slow_queries.append(query)

            for query in old_slow_queries:
                self.slow_queries.remove(query)

            cleanup_results.append(
                {"type": "slow_queries", "cleaned_queries": len(old_slow_queries)}
            )

            # تنظيف التخزين المؤقت
            cache_cleaned = len(self.query_cache)
            self.query_cache.clear()

            cleanup_results.append(
                {"type": "query_cache", "cleaned_entries": cache_cleaned}
            )

            return {
                "success": True,
                "data": {
                    "cleanup_date": cutoff_date.isoformat(),
                    "days_kept": days_to_keep,
                    "cleanup_results": cleanup_results,
                    "total_cleaned_items": sum(
                        r.get("cleaned_hours", 0)
                        + r.get("cleaned_queries", 0)
                        + r.get("cleaned_entries", 0)
                        for r in cleanup_results
                    ),
                },
            }

        except Exception as e:
            logger.error(f"خطأ في تنظيف البيانات القديمة: {str(e)}")
            return {"success": False, "error": str(e)}

    def analyze_database_health(self) -> Dict[str, Any]:
        """تحليل صحة قاعدة البيانات"""
        try:
            health_checks = []

            # 1. فحص حجم قاعدة البيانات
            db_size_check = self._check_database_size()
            health_checks.append({"check": "database_size", "result": db_size_check})

            # 2. فحص الجداول الكبيرة
            large_tables_check = self._check_large_tables()
            health_checks.append(
                {"check": "large_tables", "result": large_tables_check}
            )

            # 3. فحص الفهارس غير المستخدمة
            unused_indexes_check = self._check_unused_indexes()
            health_checks.append(
                {"check": "unused_indexes", "result": unused_indexes_check}
            )

            # 4. فحص الاستعلامات المكررة
            duplicate_queries_check = self._check_duplicate_queries()
            health_checks.append(
                {"check": "duplicate_queries", "result": duplicate_queries_check}
            )

            # تقييم الصحة العامة
            overall_health = self._calculate_overall_health(health_checks)

            return {
                "success": True,
                "data": {
                    "overall_health": overall_health,
                    "health_checks": health_checks,
                    "recommendations": self._generate_health_recommendations(
                        health_checks
                    ),
                    "analysis_date": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"خطأ في تحليل صحة قاعدة البيانات: {str(e)}")
            return {"success": False, "error": str(e)}

    def _check_database_size(self) -> Dict[str, Any]:
        """فحص حجم قاعدة البيانات"""
        try:
            # استعلام حجم قاعدة البيانات (PostgreSQL)
            size_query = """
            SELECT pg_size_pretty(pg_database_size(current_database())) as size,
                   pg_database_size(current_database()) as size_bytes
            """

            result = self.db.execute(text(size_query)).fetchone()

            size_bytes = result.size_bytes if result else 0
            size_mb = size_bytes / (1024 * 1024)

            # تقييم الحجم
            if size_mb < 100:
                status = "excellent"
                message = "حجم قاعدة البيانات مثالي"
            elif size_mb < 500:
                status = "good"
                message = "حجم قاعدة البيانات جيد"
            elif size_mb < 1000:
                status = "warning"
                message = "حجم قاعدة البيانات كبير نسبياً"
            else:
                status = "critical"
                message = "حجم قاعدة البيانات كبير جداً"

            return {
                "status": status,
                "message": message,
                "size_pretty": result.size if result else "غير معروف",
                "size_mb": size_mb,
                "size_bytes": size_bytes,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"خطأ في فحص حجم قاعدة البيانات: {str(e)}",
            }

    def _check_large_tables(self) -> Dict[str, Any]:
        """فحص الجداول الكبيرة"""
        try:
            # استعلام أكبر الجداول
            tables_query = """
            SELECT
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            LIMIT 10
            """

            results = self.db.execute(text(tables_query)).fetchall()

            large_tables = []
            for result in results:
                size_mb = result.size_bytes / (1024 * 1024)
                large_tables.append(
                    {
                        "table_name": result.tablename,
                        "size_pretty": result.size,
                        "size_mb": size_mb,
                        "size_bytes": result.size_bytes,
                    }
                )

            # تقييم الجداول الكبيرة
            max_size_mb = (
                max([t["size_mb"] for t in large_tables]) if large_tables else 0
            )

            if max_size_mb < 10:
                status = "excellent"
                message = "جميع الجداول بحجم مناسب"
            elif max_size_mb < 50:
                status = "good"
                message = "أحجام الجداول جيدة"
            elif max_size_mb < 100:
                status = "warning"
                message = "بعض الجداول كبيرة نسبياً"
            else:
                status = "critical"
                message = "توجد جداول كبيرة جداً"

            return {
                "status": status,
                "message": message,
                "large_tables": large_tables,
                "max_table_size_mb": max_size_mb,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"خطأ في فحص الجداول الكبيرة: {str(e)}",
            }

    def _check_unused_indexes(self) -> Dict[str, Any]:
        """فحص الفهارس غير المستخدمة"""
        try:
            # استعلام الفهارس غير المستخدمة (PostgreSQL)
            unused_indexes_query = """
            SELECT
                schemaname,
                tablename,
                indexname,
                idx_scan,
                pg_size_pretty(pg_relation_size(indexname::regclass)) as size
            FROM pg_stat_user_indexes
            WHERE idx_scan = 0
            AND schemaname = 'public'
            ORDER BY pg_relation_size(indexname::regclass) DESC
            """

            results = self.db.execute(text(unused_indexes_query)).fetchall()

            unused_indexes = []
            for result in results:
                unused_indexes.append(
                    {
                        "table_name": result.tablename,
                        "index_name": result.indexname,
                        "size": result.size,
                        "scan_count": result.idx_scan,
                    }
                )

            # تقييم الفهارس غير المستخدمة
            if len(unused_indexes) == 0:
                status = "excellent"
                message = "جميع الفهارس مستخدمة"
            elif len(unused_indexes) <= 3:
                status = "good"
                message = "عدد قليل من الفهارس غير المستخدمة"
            elif len(unused_indexes) <= 10:
                status = "warning"
                message = "عدد متوسط من الفهارس غير المستخدمة"
            else:
                status = "critical"
                message = "عدد كبير من الفهارس غير المستخدمة"

            return {
                "status": status,
                "message": message,
                "unused_indexes": unused_indexes,
                "unused_count": len(unused_indexes),
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"خطأ في فحص الفهارس غير المستخدمة: {str(e)}",
            }

    def _check_duplicate_queries(self) -> Dict[str, Any]:
        """فحص الاستعلامات المكررة"""
        try:
            # تحليل الاستعلامات البطيئة للبحث عن التكرار
            query_patterns = defaultdict(int)

            for query_info in self.slow_queries:
                # تبسيط الاستعلام لاكتشاف الأنماط
                simplified_query = self._simplify_query(query_info["query"])
                query_patterns[simplified_query] += 1

            # البحث عن الاستعلامات المكررة
            duplicate_queries = []
            for pattern, count in query_patterns.items():
                if count > 1:
                    duplicate_queries.append(
                        {"query_pattern": pattern, "occurrence_count": count}
                    )

            # تقييم التكرار
            if len(duplicate_queries) == 0:
                status = "excellent"
                message = "لا توجد استعلامات مكررة"
            elif len(duplicate_queries) <= 2:
                status = "good"
                message = "عدد قليل من الاستعلامات المكررة"
            elif len(duplicate_queries) <= 5:
                status = "warning"
                message = "عدد متوسط من الاستعلامات المكررة"
            else:
                status = "critical"
                message = "عدد كبير من الاستعلامات المكررة"

            return {
                "status": status,
                "message": message,
                "duplicate_queries": duplicate_queries,
                "duplicate_count": len(duplicate_queries),
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"خطأ في فحص الاستعلامات المكررة: {str(e)}",
            }

    def _simplify_query(self, query: str) -> str:
        """تبسيط الاستعلام لاكتشاف الأنماط"""
        try:
            # إزالة القيم المتغيرة والاحتفاظ بالهيكل
            import re

            # إزالة الأرقام والقيم النصية
            simplified = re.sub(r"\d+", "N", query)
            simplified = re.sub(r"'[^']*'", "'VALUE'", simplified)
            simplified = re.sub(r'"[^"]*"', '"VALUE"', simplified)

            # إزالة المسافات الزائدة
            simplified = re.sub(r"\s+", " ", simplified)

            return simplified.strip()

        except Exception:
            return query[:100]  # إرجاع أول 100 حرف في حالة الخطأ

    def _calculate_overall_health(self, health_checks: List[Dict]) -> Dict[str, Any]:
        """حساب الصحة العامة لقاعدة البيانات"""
        try:
            status_scores = {
                "excellent": 100,
                "good": 80,
                "warning": 60,
                "critical": 30,
                "error": 0,
            }

            total_score = 0
            valid_checks = 0

            for check in health_checks:
                result = check["result"]
                if "status" in result and result["status"] in status_scores:
                    total_score += status_scores[result["status"]]
                    valid_checks += 1

            if valid_checks == 0:
                return {
                    "score": 0,
                    "status": "unknown",
                    "message": "لا يمكن تحديد الصحة العامة",
                }

            avg_score = total_score / valid_checks

            if avg_score >= 90:
                status = "excellent"
                message = "قاعدة البيانات في حالة ممتازة"
            elif avg_score >= 75:
                status = "good"
                message = "قاعدة البيانات في حالة جيدة"
            elif avg_score >= 60:
                status = "warning"
                message = "قاعدة البيانات تحتاج لبعض التحسينات"
            else:
                status = "critical"
                message = "قاعدة البيانات تحتاج لتحسينات عاجلة"

            return {
                "score": avg_score,
                "status": status,
                "message": message,
                "checks_count": valid_checks,
            }

        except Exception as e:
            return {
                "score": 0,
                "status": "error",
                "message": f"خطأ في حساب الصحة العامة: {str(e)}",
            }

    def _generate_health_recommendations(self, health_checks: List[Dict]) -> List[str]:
        """إنشاء توصيات لتحسين صحة قاعدة البيانات"""
        recommendations = []

        for check in health_checks:
            result = check["result"]
            check_type = check["check"]

            if result.get("status") == "critical":
                if check_type == "database_size":
                    recommendations.append(
                        "يُنصح بتنظيف البيانات القديمة أو ترقية الخادم"
                    )
                elif check_type == "large_tables":
                    recommendations.append(
                        "يُنصح بتقسيم الجداول الكبيرة أو أرشفة البيانات القديمة"
                    )
                elif check_type == "unused_indexes":
                    recommendations.append(
                        "يُنصح بحذف الفهارس غير المستخدمة لتوفير المساحة"
                    )
                elif check_type == "duplicate_queries":
                    recommendations.append(
                        "يُنصح بتحسين الاستعلامات المكررة وإضافة تخزين مؤقت"
                    )

            elif result.get("status") == "warning":
                if check_type == "database_size":
                    recommendations.append("مراقبة نمو قاعدة البيانات والتخطيط للتوسع")
                elif check_type == "large_tables":
                    recommendations.append(
                        "مراقبة نمو الجداول الكبيرة وتحسين الاستعلامات"
                    )
                elif check_type == "unused_indexes":
                    recommendations.append(
                        "مراجعة الفهارس غير المستخدمة وتقييم ضرورتها"
                    )
                elif check_type == "duplicate_queries":
                    recommendations.append("تحسين الاستعلامات المكررة لتحسين الأداء")

        if not recommendations:
            recommendations.append(
                "قاعدة البيانات في حالة جيدة، استمر في المراقبة الدورية"
            )

        return recommendations
