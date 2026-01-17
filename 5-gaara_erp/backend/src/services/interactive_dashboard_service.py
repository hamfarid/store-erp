#!/usr/bin/env python3
# type: ignore
# pylint: disable=all
# flake8: noqa
"""
/home/ubuntu/upload/store_v1.1/complete_inventory_system/backend/src/services/interactive_dashboard_service.py

خدمة لوحات المعلومات التفاعلية
Interactive Dashboard Service

يوفر هذا الملف خدمات شاملة لإنشاء وإدارة لوحات المعلومات التفاعلية
"""

import logging
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy import and_, or_, func, text
from sqlalchemy.exc import IntegrityError

# استيراد النماذج
from src.models.inventory import Product, Category, Warehouse, StockMovement
from src.models.customer import Customer
from src.models.supplier import Supplier
from src.models.accounting_system import Invoice, InvoiceItem, Payment
from src.models.user import User
from src.database import db

# إعداد السجلات
logger = logging.getLogger(__name__)


class InteractiveDashboardService:
    """خدمة لوحات المعلومات التفاعلية"""

    def __init__(self):
        """تهيئة الخدمة"""
        self.logger = logger

    # ==================== لوحة المعلومات الرئيسية ====================

    def get_main_dashboard_data(
        self, user_id: int, date_range: str = "30d"
    ) -> Dict[str, Any]:
        """
        الحصول على بيانات لوحة المعلومات الرئيسية

        Args:
            user_id: معرف المستخدم
            date_range: نطاق التاريخ (7d, 30d, 90d, 1y)

        Returns:
            Dict: بيانات لوحة المعلومات
        """
        try:
            # تحديد نطاق التاريخ
            end_date = datetime.utcnow()
            if date_range == "7d":
                start_date = end_date - timedelta(days=7)
            elif date_range == "30d":
                start_date = end_date - timedelta(days=30)
            elif date_range == "90d":
                start_date = end_date - timedelta(days=90)
            elif date_range == "1y":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = end_date - timedelta(days=30)

            # جمع البيانات
            dashboard_data = {
                "overview": self._get_overview_metrics(start_date, end_date),
                "sales_analytics": self._get_sales_analytics(start_date, end_date),
                "inventory_analytics": self._get_inventory_analytics(),
                "financial_analytics": self._get_financial_analytics(
                    start_date, end_date
                ),
                "customer_analytics": self._get_customer_analytics(
                    start_date, end_date
                ),
                "performance_metrics": self._get_performance_metrics(
                    start_date, end_date
                ),
                "alerts_notifications": self._get_alerts_notifications(),
                "recent_activities": self._get_recent_activities(user_id, 10),
            }

            return {
                "success": True,
                "data": dashboard_data,
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                    "period": date_range,
                },
            }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على بيانات لوحة المعلومات: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على البيانات: {str(e)}",
            }

    def _get_overview_metrics(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """الحصول على المقاييس العامة"""
        try:
            # إجمالي المبيعات
            total_sales = (
                db.session.query(func.sum(Invoice.total_amount))
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "sale",
                    )
                )
                .scalar()
                or 0
            )

            # إجمالي المشتريات
            total_purchases = (
                db.session.query(func.sum(Invoice.total_amount))
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "purchase",
                    )
                )
                .scalar()
                or 0
            )

            # عدد العملاء الجدد
            new_customers = (
                db.session.query(func.count(Customer.id))
                .filter(
                    and_(
                        Customer.created_at >= start_date,
                        Customer.created_at <= end_date,
                    )
                )
                .scalar()
                or 0
            )

            # عدد المنتجات
            total_products = db.session.query(func.count(Product.id)).scalar() or 0

            # عدد الفواتير
            total_invoices = (
                db.session.query(func.count(Invoice.id))
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                    )
                )
                .scalar()
                or 0
            )

            # الربح الإجمالي
            gross_profit = total_sales - total_purchases

            return {
                "total_sales": float(total_sales),
                "total_purchases": float(total_purchases),
                "gross_profit": float(gross_profit),
                "new_customers": int(new_customers),
                "total_products": int(total_products),
                "total_invoices": int(total_invoices),
                "profit_margin": float(
                    (gross_profit / total_sales * 100) if total_sales > 0 else 0
                ),
            }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على المقاييس العامة: {str(e)}")
            return {}

    def _get_sales_analytics(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """تحليلات المبيعات"""
        try:
            # مبيعات يومية
            daily_sales = (
                db.session.query(
                    func.date(Invoice.invoice_date).label("date"),
                    func.sum(Invoice.total_amount).label("amount"),
                    func.count(Invoice.id).label("count"),
                )
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "sale",
                    )
                )
                .group_by(func.date(Invoice.invoice_date))
                .all()
            )

            # أفضل المنتجات مبيعاً
            top_products = (
                db.session.query(
                    Product.name,
                    func.sum(InvoiceItem.quantity).label("total_quantity"),
                    func.sum(InvoiceItem.total_price).label("total_amount"),
                )
                .join(InvoiceItem)
                .join(Invoice)
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "sale",
                    )
                )
                .group_by(Product.id, Product.name)
                .order_by(func.sum(InvoiceItem.total_price).desc())
                .limit(10)
                .all()
            )

            # أفضل العملاء
            top_customers = (
                db.session.query(
                    Customer.name,
                    func.sum(Invoice.total_amount).label("total_amount"),
                    func.count(Invoice.id).label("invoice_count"),
                )
                .join(Invoice)
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "sale",
                    )
                )
                .group_by(Customer.id, Customer.name)
                .order_by(func.sum(Invoice.total_amount).desc())
                .limit(10)
                .all()
            )

            return {
                "daily_sales": [
                    {
                        "date": sale.date.isoformat(),
                        "amount": float(sale.amount or 0),
                        "count": int(sale.count or 0),
                    }
                    for sale in daily_sales
                ],
                "top_products": [
                    {
                        "name": product.name,
                        "quantity": float(product.total_quantity or 0),
                        "amount": float(product.total_amount or 0),
                    }
                    for product in top_products
                ],
                "top_customers": [
                    {
                        "name": customer.name,
                        "amount": float(customer.total_amount or 0),
                        "invoice_count": int(customer.invoice_count or 0),
                    }
                    for customer in top_customers
                ],
            }

        except Exception as e:
            self.logger.error(f"خطأ في تحليلات المبيعات: {str(e)}")
            return {}

    def _get_inventory_analytics(self) -> Dict[str, Any]:
        """تحليلات المخزون"""
        try:
            # إجمالي قيمة المخزون
            total_inventory_value = (
                db.session.query(
                    func.sum(Product.current_stock * Product.cost_price)
                ).scalar()
                or 0
            )

            # المنتجات منخفضة المخزون
            low_stock_products = (
                db.session.query(Product)
                .filter(Product.current_stock <= Product.minimum_stock)
                .count()
            )

            # المنتجات نافدة المخزون
            out_of_stock_products = (
                db.session.query(Product).filter(Product.current_stock <= 0).count()
            )

            # توزيع المخزون حسب الفئات
            category_distribution = (
                db.session.query(
                    Category.name,
                    func.count(Product.id).label("product_count"),
                    func.sum(Product.current_stock * Product.cost_price).label(
                        "total_value"
                    ),
                )
                .join(Product)
                .group_by(Category.id, Category.name)
                .all()
            )

            # حركة المخزون الأخيرة
            recent_movements = (
                db.session.query(StockMovement)
                .order_by(StockMovement.created_at.desc())
                .limit(10)
                .all()
            )

            return {
                "total_inventory_value": float(total_inventory_value),
                "low_stock_products": int(low_stock_products),
                "out_of_stock_products": int(out_of_stock_products),
                "category_distribution": [
                    {
                        "category": cat.name,
                        "product_count": int(cat.product_count or 0),
                        "total_value": float(cat.total_value or 0),
                    }
                    for cat in category_distribution
                ],
                "recent_movements": [
                    {
                        "id": movement.id,
                        "product_name": (
                            movement.product.name if movement.product else ""
                        ),
                        "movement_type": movement.movement_type,
                        "quantity": float(movement.quantity),
                        "date": movement.created_at.isoformat(),
                    }
                    for movement in recent_movements
                ],
            }

        except Exception as e:
            self.logger.error(f"خطأ في تحليلات المخزون: {str(e)}")
            return {}

    def _get_financial_analytics(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """التحليلات المالية"""
        try:
            # إجمالي المدفوعات
            total_payments = (
                db.session.query(func.sum(Payment.amount))
                .filter(
                    and_(
                        Payment.payment_date >= start_date,
                        Payment.payment_date <= end_date,
                    )
                )
                .scalar()
                or 0
            )

            # المدفوعات المعلقة
            pending_payments = (
                db.session.query(func.sum(Invoice.total_amount))
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.payment_status == "pending",
                    )
                )
                .scalar()
                or 0
            )

            # تحليل التدفق النقدي
            cash_flow = (
                db.session.query(
                    func.date(Payment.payment_date).label("date"),
                    func.sum(Payment.amount).label("amount"),
                )
                .filter(
                    and_(
                        Payment.payment_date >= start_date,
                        Payment.payment_date <= end_date,
                    )
                )
                .group_by(func.date(Payment.payment_date))
                .all()
            )

            return {
                "total_payments": float(total_payments),
                "pending_payments": float(pending_payments),
                "cash_flow": [
                    {"date": flow.date.isoformat(), "amount": float(flow.amount or 0)}
                    for flow in cash_flow
                ],
            }

        except Exception as e:
            self.logger.error(f"خطأ في التحليلات المالية: {str(e)}")
            return {}

    def _get_customer_analytics(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """تحليلات العملاء"""
        try:
            # إجمالي العملاء
            total_customers = db.session.query(func.count(Customer.id)).scalar() or 0

            # العملاء النشطين
            active_customers = (
                db.session.query(func.count(func.distinct(Invoice.customer_id)))
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "sale",
                    )
                )
                .scalar()
                or 0
            )

            # متوسط قيمة الطلب
            avg_order_value = (
                db.session.query(func.avg(Invoice.total_amount))
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "sale",
                    )
                )
                .scalar()
                or 0
            )

            # توزيع العملاء حسب المنطقة
            customer_distribution = (
                db.session.query(
                    Customer.city, func.count(Customer.id).label("customer_count")
                )
                .group_by(Customer.city)
                .all()
            )

            return {
                "total_customers": int(total_customers),
                "active_customers": int(active_customers),
                "avg_order_value": float(avg_order_value),
                "customer_distribution": [
                    {
                        "city": dist.city or "غير محدد",
                        "count": int(dist.customer_count or 0),
                    }
                    for dist in customer_distribution
                ],
            }

        except Exception as e:
            self.logger.error(f"خطأ في تحليلات العملاء: {str(e)}")
            return {}

    def _get_performance_metrics(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """مقاييس الأداء"""
        try:
            # معدل نمو المبيعات
            current_sales = (
                db.session.query(func.sum(Invoice.total_amount))
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "sale",
                    )
                )
                .scalar()
                or 0
            )

            # المبيعات في الفترة السابقة
            period_days = (end_date - start_date).days
            prev_start = start_date - timedelta(days=period_days)
            prev_end = start_date

            previous_sales = (
                db.session.query(func.sum(Invoice.total_amount))
                .filter(
                    and_(
                        Invoice.invoice_date >= prev_start,
                        Invoice.invoice_date <= prev_end,
                        Invoice.invoice_type == "sale",
                    )
                )
                .scalar()
                or 0
            )

            # حساب معدل النمو
            growth_rate = 0
            if previous_sales > 0:
                growth_rate = ((current_sales - previous_sales) / previous_sales) * 100

            # معدل دوران المخزون
            avg_inventory = (
                db.session.query(
                    func.avg(Product.current_stock * Product.cost_price)
                ).scalar()
                or 1
            )

            cost_of_goods_sold = (
                db.session.query(
                    func.sum(InvoiceItem.quantity * InvoiceItem.unit_price)
                )
                .join(Invoice)
                .filter(
                    and_(
                        Invoice.invoice_date >= start_date,
                        Invoice.invoice_date <= end_date,
                        Invoice.invoice_type == "sale",
                    )
                )
                .scalar()
                or 0
            )

            inventory_turnover = (
                cost_of_goods_sold / avg_inventory if avg_inventory > 0 else 0
            )

            return {
                "sales_growth_rate": float(growth_rate),
                "inventory_turnover": float(inventory_turnover),
                "current_sales": float(current_sales),
                "previous_sales": float(previous_sales),
            }

        except Exception as e:
            self.logger.error(f"خطأ في مقاييس الأداء: {str(e)}")
            return {}

    def _get_alerts_notifications(self) -> Dict[str, Any]:
        """التنبيهات والإشعارات"""
        try:
            alerts = []

            # تنبيهات المخزون المنخفض
            low_stock_products = (
                db.session.query(Product)
                .filter(Product.current_stock <= Product.minimum_stock)
                .limit(5)
                .all()
            )

            for product in low_stock_products:
                alerts.append(
                    {
                        "type": "low_stock",
                        "severity": "warning",
                        "title": "مخزون منخفض",
                        "message": f"المنتج {product.name} وصل إلى الحد الأدنى للمخزون",
                        "product_id": product.id,
                        "current_stock": product.current_stock,
                        "minimum_stock": product.minimum_stock,
                    }
                )

            # تنبيهات المدفوعات المتأخرة
            overdue_invoices = (
                db.session.query(Invoice)
                .filter(
                    and_(
                        Invoice.due_date < datetime.utcnow(),
                        Invoice.payment_status == "pending",
                    )
                )
                .limit(5)
                .all()
            )

            for invoice in overdue_invoices:
                alerts.append(
                    {
                        "type": "overdue_payment",
                        "severity": "error",
                        "title": "دفعة متأخرة",
                        "message": f"الفاتورة {invoice.invoice_number} متأخرة عن موعد الاستحقاق",
                        "invoice_id": invoice.id,
                        "amount": float(invoice.total_amount),
                        "due_date": invoice.due_date.isoformat(),
                    }
                )

            return {"alerts": alerts, "total_alerts": len(alerts)}

        except Exception as e:
            self.logger.error(f"خطأ في التنبيهات: {str(e)}")
            return {"alerts": [], "total_alerts": 0}

    def _get_recent_activities(
        self, user_id: int, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """الأنشطة الأخيرة"""
        try:
            # الفواتير الأخيرة
            recent_invoices = (
                db.session.query(Invoice)
                .order_by(Invoice.created_at.desc())
                .limit(limit)
                .all()
            )

            activities = []
            for invoice in recent_invoices:
                activities.append(
                    {
                        "type": "invoice",
                        "title": f"فاتورة {invoice.invoice_type}",
                        "description": f"تم إنشاء فاتورة رقم {invoice.invoice_number}",
                        "amount": float(invoice.total_amount),
                        "date": invoice.created_at.isoformat(),
                        "user": (
                            invoice.created_by_user.username
                            if invoice.created_by_user
                            else "غير معروف"
                        ),
                    }
                )

            return activities

        except Exception as e:
            self.logger.error(f"خطأ في الأنشطة الأخيرة: {str(e)}")
            return []

    # ==================== لوحات معلومات مخصصة ====================

    def create_custom_dashboard(
        self, user_id: int, dashboard_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        إنشاء لوحة معلومات مخصصة

        Args:
            user_id: معرف المستخدم
            dashboard_data: بيانات لوحة المعلومات

        Returns:
            Dict: نتيجة العملية
        """
        try:
            # التحقق من البيانات المطلوبة
            required_fields = ["name", "widgets"]
            for field in required_fields:
                if field not in dashboard_data:
                    return {"success": False, "message": f"الحقل {field} مطلوب"}

            # إنشاء لوحة المعلومات
            dashboard = {
                "id": self._generate_dashboard_id(),
                "name": dashboard_data["name"],
                "description": dashboard_data.get("description", ""),
                "widgets": dashboard_data["widgets"],
                "layout": dashboard_data.get("layout", "grid"),
                "created_by": user_id,
                "created_at": datetime.utcnow().isoformat(),
                "is_public": dashboard_data.get("is_public", False),
            }

            # حفظ لوحة المعلومات (يمكن حفظها في قاعدة البيانات أو ملف)
            self._save_custom_dashboard(dashboard)

            return {
                "success": True,
                "message": "تم إنشاء لوحة المعلومات بنجاح",
                "dashboard": dashboard,
            }

        except Exception as e:
            self.logger.error(f"خطأ في إنشاء لوحة المعلومات المخصصة: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في إنشاء لوحة المعلومات: {str(e)}",
            }

    def get_widget_data(
        self, widget_type: str, widget_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        الحصول على بيانات ويدجت محدد

        Args:
            widget_type: نوع الويدجت
            widget_config: تكوين الويدجت

        Returns:
            Dict: بيانات الويدجت
        """
        try:
            if widget_type == "sales_chart":
                return self._get_sales_chart_data(widget_config)
            elif widget_type == "inventory_status":
                return self._get_inventory_status_data(widget_config)
            elif widget_type == "top_products":
                return self._get_top_products_data(widget_config)
            elif widget_type == "financial_summary":
                return self._get_financial_summary_data(widget_config)
            elif widget_type == "customer_analytics":
                return self._get_customer_analytics_data(widget_config)
            else:
                return {
                    "success": False,
                    "message": f"نوع الويدجت {widget_type} غير مدعوم",
                }

        except Exception as e:
            self.logger.error(f"خطأ في الحصول على بيانات الويدجت: {str(e)}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على البيانات: {str(e)}",
            }

    # ==================== الدوال المساعدة ====================

    def _generate_dashboard_id(self) -> str:
        """توليد معرف فريد للوحة المعلومات"""
        import uuid

        return str(uuid.uuid4())

    def _save_custom_dashboard(self, dashboard: Dict[str, Any]) -> None:
        """حفظ لوحة المعلومات المخصصة"""
        # يمكن حفظها في قاعدة البيانات أو ملف JSON
        # هنا نحفظها في ملف مؤقت
        import os

        dashboards_dir = "/tmp/custom_dashboards"
        os.makedirs(dashboards_dir, exist_ok=True)

        dashboard_file = os.path.join(dashboards_dir, f"{dashboard['id']}.json")
        with open(dashboard_file, "w", encoding="utf-8") as f:
            json.dump(dashboard, f, ensure_ascii=False, indent=2)

    def _get_sales_chart_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """بيانات مخطط المبيعات"""
        period = config.get("period", "30d")
        chart_type = config.get("chart_type", "line")

        # تحديد نطاق التاريخ
        end_date = datetime.utcnow()
        if period == "7d":
            start_date = end_date - timedelta(days=7)
        elif period == "30d":
            start_date = end_date - timedelta(days=30)
        elif period == "90d":
            start_date = end_date - timedelta(days=90)
        else:
            start_date = end_date - timedelta(days=30)

        # الحصول على بيانات المبيعات
        sales_data = (
            db.session.query(
                func.date(Invoice.invoice_date).label("date"),
                func.sum(Invoice.total_amount).label("amount"),
            )
            .filter(
                and_(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date,
                    Invoice.invoice_type == "sale",
                )
            )
            .group_by(func.date(Invoice.invoice_date))
            .all()
        )

        return {
            "success": True,
            "data": {
                "chart_type": chart_type,
                "labels": [sale.date.isoformat() for sale in sales_data],
                "datasets": [
                    {
                        "label": "المبيعات",
                        "data": [float(sale.amount or 0) for sale in sales_data],
                        "backgroundColor": "rgba(54, 162, 235, 0.2)",
                        "borderColor": "rgba(54, 162, 235, 1)",
                        "borderWidth": 2,
                    }
                ],
            },
        }

    def _get_inventory_status_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """بيانات حالة المخزون"""
        # المنتجات منخفضة المخزون
        low_stock = (
            db.session.query(func.count(Product.id))
            .filter(Product.current_stock <= Product.minimum_stock)
            .scalar()
            or 0
        )

        # المنتجات نافدة المخزون
        out_of_stock = (
            db.session.query(func.count(Product.id))
            .filter(Product.current_stock <= 0)
            .scalar()
            or 0
        )

        # المنتجات العادية
        normal_stock = (
            db.session.query(func.count(Product.id))
            .filter(Product.current_stock > Product.minimum_stock)
            .scalar()
            or 0
        )

        return {
            "success": True,
            "data": {
                "low_stock": int(low_stock),
                "out_of_stock": int(out_of_stock),
                "normal_stock": int(normal_stock),
                "total_products": int(low_stock + out_of_stock + normal_stock),
            },
        }

    def _get_top_products_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """بيانات أفضل المنتجات"""
        limit = config.get("limit", 10)
        period = config.get("period", "30d")

        # تحديد نطاق التاريخ
        end_date = datetime.utcnow()
        if period == "7d":
            start_date = end_date - timedelta(days=7)
        elif period == "30d":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=30)

        # أفضل المنتجات
        top_products = (
            db.session.query(
                Product.name,
                func.sum(InvoiceItem.quantity).label("total_quantity"),
                func.sum(InvoiceItem.total_price).label("total_amount"),
            )
            .join(InvoiceItem)
            .join(Invoice)
            .filter(
                and_(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date,
                    Invoice.invoice_type == "sale",
                )
            )
            .group_by(Product.id, Product.name)
            .order_by(func.sum(InvoiceItem.total_price).desc())
            .limit(limit)
            .all()
        )

        return {
            "success": True,
            "data": [
                {
                    "name": product.name,
                    "quantity": float(product.total_quantity or 0),
                    "amount": float(product.total_amount or 0),
                }
                for product in top_products
            ],
        }

    def _get_financial_summary_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """بيانات الملخص المالي"""
        period = config.get("period", "30d")

        # تحديد نطاق التاريخ
        end_date = datetime.utcnow()
        if period == "7d":
            start_date = end_date - timedelta(days=7)
        elif period == "30d":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=30)

        # المبيعات
        total_sales = (
            db.session.query(func.sum(Invoice.total_amount))
            .filter(
                and_(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date,
                    Invoice.invoice_type == "sale",
                )
            )
            .scalar()
            or 0
        )

        # المشتريات
        total_purchases = (
            db.session.query(func.sum(Invoice.total_amount))
            .filter(
                and_(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date,
                    Invoice.invoice_type == "purchase",
                )
            )
            .scalar()
            or 0
        )

        # المدفوعات
        total_payments = (
            db.session.query(func.sum(Payment.amount))
            .filter(
                and_(
                    Payment.payment_date >= start_date, Payment.payment_date <= end_date
                )
            )
            .scalar()
            or 0
        )

        return {
            "success": True,
            "data": {
                "total_sales": float(total_sales),
                "total_purchases": float(total_purchases),
                "total_payments": float(total_payments),
                "net_profit": float(total_sales - total_purchases),
            },
        }

    def _get_customer_analytics_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """بيانات تحليلات العملاء"""
        period = config.get("period", "30d")

        # تحديد نطاق التاريخ
        end_date = datetime.utcnow()
        if period == "7d":
            start_date = end_date - timedelta(days=7)
        elif period == "30d":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=30)

        # العملاء النشطين
        active_customers = (
            db.session.query(func.count(func.distinct(Invoice.customer_id)))
            .filter(
                and_(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date,
                    Invoice.invoice_type == "sale",
                )
            )
            .scalar()
            or 0
        )

        # العملاء الجدد
        new_customers = (
            db.session.query(func.count(Customer.id))
            .filter(
                and_(Customer.created_at >= start_date, Customer.created_at <= end_date)
            )
            .scalar()
            or 0
        )

        # متوسط قيمة الطلب
        avg_order_value = (
            db.session.query(func.avg(Invoice.total_amount))
            .filter(
                and_(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date,
                    Invoice.invoice_type == "sale",
                )
            )
            .scalar()
            or 0
        )

        return {
            "success": True,
            "data": {
                "active_customers": int(active_customers),
                "new_customers": int(new_customers),
                "avg_order_value": float(avg_order_value),
            },
        }


# إنشاء مثيل الخدمة
interactive_dashboard_service = InteractiveDashboardService()
