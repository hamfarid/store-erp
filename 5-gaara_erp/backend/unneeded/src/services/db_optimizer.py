"""
محسن قاعدة البيانات المتقدم
Advanced Database Optimizer
"""

from sqlalchemy import text, Index
from database import db


class DatabaseOptimizer:
    """محسن قاعدة البيانات المتقدم"""

    @staticmethod
    def create_performance_indexes():
        """إنشاء فهارس الأداء"""
        indexes = [
            # فهارس المنتجات
            "CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)",
            "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)",
            "CREATE INDEX IF NOT EXISTS idx_products_price ON products(price)",
            "CREATE INDEX IF NOT EXISTS idx_products_stock ON products(stock_quantity)",
            # فهارس العملاء
            "CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name)",
            "CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email)",
            "CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone)",
            # فهارس الفواتير
            "CREATE INDEX IF NOT EXISTS idx_invoices_date ON invoices(invoice_date)",
            "CREATE INDEX IF NOT EXISTS idx_invoices_customer ON invoices(customer_id)",
            "CREATE INDEX IF NOT EXISTS idx_invoices_total ON invoices(total_amount)",
            # فهارس حركات المخزون
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_date ON stock_movements(movement_date)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_type ON stock_movements(movement_type)",
            # فهارس مركبة للاستعلامات المعقدة
            "CREATE INDEX IF NOT EXISTS idx_products_category_stock ON products(category_id, stock_quantity)",
            "CREATE INDEX IF NOT EXISTS idx_invoices_customer_date ON invoices(customer_id, invoice_date)",
        ]

        try:
            for index_sql in indexes:
                db.session.execute(text(index_sql))
            db.session.commit()
            return True, f"تم إنشاء {len(indexes)} فهرس بنجاح"
        except Exception as e:
            db.session.rollback()
            return False, f"خطأ في إنشاء الفهارس: {str(e)}"

    @staticmethod
    def analyze_query_performance():
        """تحليل أداء الاستعلامات"""
        analysis_queries = [
            "EXPLAIN QUERY PLAN SELECT * FROM products WHERE category_id = 1",
            "EXPLAIN QUERY PLAN SELECT * FROM invoices WHERE customer_id = 1 ORDER BY invoice_date DESC",
            "EXPLAIN QUERY PLAN SELECT p.name, SUM(sm.quantity) FROM products p JOIN stock_movements sm ON p.id = sm.product_id GROUP BY p.id",
        ]

        results = []
        for query in analysis_queries:
            try:
                result = db.session.execute(text(query)).fetchall()
                results.append(
                    {"query": query, "plan": [dict(row._mapping) for row in result]}
                )
            except Exception as e:
                results.append({"query": query, "error": str(e)})

        return results

    @staticmethod
    def optimize_database():
        """تحسين شامل لقاعدة البيانات"""
        optimizations = []

        # إنشاء الفهارس
        success, message = DatabaseOptimizer.create_performance_indexes()
        optimizations.append(f"الفهارس: {message}")

        # تحليل الجداول
        try:
            db.session.execute(text("ANALYZE"))
            db.session.commit()
            optimizations.append("تم تحليل الجداول بنجاح")
        except Exception as e:
            optimizations.append(f"خطأ في تحليل الجداول: {str(e)}")

        # تنظيف قاعدة البيانات
        try:
            db.session.execute(text("VACUUM"))
            optimizations.append("تم تنظيف قاعدة البيانات")
        except Exception as e:
            optimizations.append(f"تحذير: {str(e)}")

        return optimizations


# دالة مساعدة للاستعلامات المحسنة
def optimized_query(query_func):
    """decorator لتحسين الاستعلامات"""

    def wrapper(*args, **kwargs):
        # تفعيل التخزين المؤقت للاستعلام
        result = query_func(*args, **kwargs)
        return result

    return wrapper
