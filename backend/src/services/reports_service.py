#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.76: Reporting Service

Backend service for generating various reports.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from sqlalchemy import func, desc, and_, extract
from src.database import db
from src.models.invoice import Invoice
import logging

logger = logging.getLogger(__name__)


@dataclass
class ReportPeriod:
    """Report time period."""

    start_date: datetime
    end_date: datetime

    @classmethod
    def today(cls):
        today = datetime.utcnow().date()
        return cls(
            start_date=datetime.combine(today, datetime.min.time()),
            end_date=datetime.combine(today, datetime.max.time()),
        )

    @classmethod
    def this_week(cls):
        today = datetime.utcnow().date()
        start = today - timedelta(days=today.weekday())
        return cls(
            start_date=datetime.combine(start, datetime.min.time()),
            end_date=datetime.combine(today, datetime.max.time()),
        )

    @classmethod
    def this_month(cls):
        today = datetime.utcnow().date()
        start = today.replace(day=1)
        return cls(
            start_date=datetime.combine(start, datetime.min.time()),
            end_date=datetime.combine(today, datetime.max.time()),
        )

    @classmethod
    def this_year(cls):
        today = datetime.utcnow().date()
        start = today.replace(month=1, day=1)
        return cls(
            start_date=datetime.combine(start, datetime.min.time()),
            end_date=datetime.combine(today, datetime.max.time()),
        )

    @classmethod
    def custom(cls, start: datetime, end: datetime):
        return cls(start_date=start, end_date=end)


class ReportsService:
    """
    P2.76: Reporting service for analytics and business intelligence.
    """

    @staticmethod
    def get_sales_summary(period: ReportPeriod) -> Dict[str, Any]:
        """Get sales summary for a period."""
        from src.models.invoice import Invoice

        query = Invoice.query.filter(
            Invoice.created_at >= period.start_date,
            Invoice.created_at <= period.end_date,
            Invoice.status != "cancelled",
        )

        total_sales = query.with_entities(func.sum(Invoice.total)).scalar() or 0
        total_orders = query.count()
        average_order = total_sales / total_orders if total_orders > 0 else 0

        # Paid vs unpaid
        paid = (
            query.filter(Invoice.status == "paid")
            .with_entities(func.sum(Invoice.total))
            .scalar()
            or 0
        )
        unpaid = (
            query.filter(Invoice.status.in_(["pending", "overdue"]))
            .with_entities(func.sum(Invoice.total))
            .scalar()
            or 0
        )

        return {
            "period": {
                "start": period.start_date.isoformat(),
                "end": period.end_date.isoformat(),
            },
            "total_sales": round(total_sales, 2),
            "total_orders": total_orders,
            "average_order_value": round(average_order, 2),
            "paid_amount": round(paid, 2),
            "unpaid_amount": round(unpaid, 2),
            "collection_rate": round(
                (paid / total_sales * 100) if total_sales > 0 else 0, 1
            ),
        }

    @staticmethod
    def get_sales_by_day(period: ReportPeriod) -> List[Dict[str, Any]]:
        """Get daily sales breakdown."""
        from src.models.invoice import Invoice

        query = (
            db.session.query(
                func.date(Invoice.created_at).label("date"),
                func.sum(Invoice.total).label("total"),
                func.count(Invoice.id).label("orders"),
            )
            .filter(
                Invoice.created_at >= period.start_date,
                Invoice.created_at <= period.end_date,
                Invoice.status != "cancelled",
            )
            .group_by(func.date(Invoice.created_at))
            .order_by("date")
        )

        return [
            {
                "date": row.date.isoformat(),
                "total": round(row.total or 0, 2),
                "orders": row.orders,
            }
            for row in query.all()
        ]

    @staticmethod
    def get_top_products(period: ReportPeriod, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top selling products."""
        from src.models.invoice import InvoiceItem
        from src.models.product import Product

        query = (
            db.session.query(
                Product.id,
                Product.name,
                func.sum(InvoiceItem.quantity).label("total_qty"),
                func.sum(InvoiceItem.total).label("total_revenue"),
            )
            .join(InvoiceItem, InvoiceItem.product_id == Product.id)
            .join(InvoiceItem.invoice)
            .filter(
                InvoiceItem.invoice.has(
                    and_(
                        Invoice.created_at >= period.start_date,
                        Invoice.created_at <= period.end_date,
                        Invoice.status != "cancelled",
                    )
                )
            )
            .group_by(Product.id)
            .order_by(desc("total_revenue"))
            .limit(limit)
        )

        from src.models.invoice import Invoice  # Import here to avoid circular

        return [
            {
                "id": row.id,
                "name": row.name,
                "quantity_sold": row.total_qty or 0,
                "revenue": round(row.total_revenue or 0, 2),
            }
            for row in query.all()
        ]

    @staticmethod
    def get_top_customers(
        period: ReportPeriod, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get top customers by purchase amount."""
        from src.models.invoice import Invoice
        from src.models.partners import Customer

        query = (
            db.session.query(
                Customer.id,
                Customer.name,
                func.count(Invoice.id).label("order_count"),
                func.sum(Invoice.total).label("total_spent"),
            )
            .join(Invoice, Invoice.customer_id == Customer.id)
            .filter(
                Invoice.created_at >= period.start_date,
                Invoice.created_at <= period.end_date,
                Invoice.status != "cancelled",
            )
            .group_by(Customer.id)
            .order_by(desc("total_spent"))
            .limit(limit)
        )

        return [
            {
                "id": row.id,
                "name": row.name,
                "order_count": row.order_count,
                "total_spent": round(row.total_spent or 0, 2),
            }
            for row in query.all()
        ]

    @staticmethod
    def get_inventory_report() -> Dict[str, Any]:
        """Get inventory status report."""
        from src.models.product import Product

        total_products = Product.query.count()

        # Stock value
        stock_value = (
            db.session.query(func.sum(Product.quantity * Product.cost)).scalar() or 0
        )

        # Retail value
        retail_value = (
            db.session.query(func.sum(Product.quantity * Product.price)).scalar() or 0
        )

        # Low stock
        low_stock = Product.query.filter(
            Product.quantity <= Product.min_stock_level
        ).count()

        # Out of stock
        out_of_stock = Product.query.filter(Product.quantity <= 0).count()

        # Top low stock items
        low_stock_items = (
            Product.query.filter(
                Product.quantity <= Product.min_stock_level, Product.quantity > 0
            )
            .order_by(Product.quantity)
            .limit(10)
            .all()
        )

        return {
            "total_products": total_products,
            "stock_value": round(stock_value, 2),
            "retail_value": round(retail_value, 2),
            "potential_profit": round(retail_value - stock_value, 2),
            "low_stock_count": low_stock,
            "out_of_stock_count": out_of_stock,
            "low_stock_items": [
                {
                    "id": p.id,
                    "name": p.name,
                    "quantity": p.quantity,
                    "min_stock": p.min_stock_level,
                }
                for p in low_stock_items
            ],
        }

    @staticmethod
    def get_profit_report(period: ReportPeriod) -> Dict[str, Any]:
        """Get profit and loss report."""
        from src.models.invoice import Invoice, InvoiceItem

        # Revenue (Sales)
        revenue = (
            db.session.query(func.sum(Invoice.total))
            .filter(
                Invoice.created_at >= period.start_date,
                Invoice.created_at <= period.end_date,
                Invoice.status != "cancelled",
            )
            .scalar()
            or 0
        )

        # Cost of Goods Sold (approximate)
        cogs = (
            db.session.query(func.sum(InvoiceItem.quantity * InvoiceItem.cost))
            .join(Invoice)
            .filter(
                Invoice.created_at >= period.start_date,
                Invoice.created_at <= period.end_date,
                Invoice.status != "cancelled",
            )
            .scalar()
            or 0
        )

        gross_profit = revenue - cogs
        gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0

        return {
            "period": {
                "start": period.start_date.isoformat(),
                "end": period.end_date.isoformat(),
            },
            "revenue": round(revenue, 2),
            "cost_of_goods_sold": round(cogs, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_margin_percent": round(gross_margin, 1),
        }

    @staticmethod
    def get_sales_by_category(period: ReportPeriod) -> List[Dict[str, Any]]:
        """Get sales breakdown by category."""
        from src.models.invoice import Invoice, InvoiceItem
        from src.models.product import Product
        from src.models.category import Category

        query = (
            db.session.query(
                Category.id,
                Category.name,
                func.sum(InvoiceItem.total).label("total_sales"),
                func.count(InvoiceItem.id).label("items_sold"),
            )
            .join(Product, Product.category_id == Category.id)
            .join(InvoiceItem, InvoiceItem.product_id == Product.id)
            .join(Invoice, Invoice.id == InvoiceItem.invoice_id)
            .filter(
                Invoice.created_at >= period.start_date,
                Invoice.created_at <= period.end_date,
                Invoice.status != "cancelled",
            )
            .group_by(Category.id)
            .order_by(desc("total_sales"))
        )

        return [
            {
                "id": row.id,
                "name": row.name,
                "total_sales": round(row.total_sales or 0, 2),
                "items_sold": row.items_sold,
            }
            for row in query.all()
        ]

    @staticmethod
    def get_payment_summary(period: ReportPeriod) -> Dict[str, Any]:
        """Get payment method breakdown."""
        from src.models.invoice import Invoice

        query = (
            db.session.query(
                Invoice.payment_method,
                func.sum(Invoice.total).label("total"),
                func.count(Invoice.id).label("count"),
            )
            .filter(
                Invoice.created_at >= period.start_date,
                Invoice.created_at <= period.end_date,
                Invoice.status == "paid",
            )
            .group_by(Invoice.payment_method)
        )

        return {
            "by_method": [
                {
                    "method": row.payment_method or "غير محدد",
                    "total": round(row.total or 0, 2),
                    "count": row.count,
                }
                for row in query.all()
            ]
        }

    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        """Get quick dashboard summary."""
        today = ReportPeriod.today()
        this_month = ReportPeriod.this_month()

        return {
            "today": ReportsService.get_sales_summary(today),
            "this_month": ReportsService.get_sales_summary(this_month),
            "inventory": ReportsService.get_inventory_report(),
            "top_products": ReportsService.get_top_products(this_month, 5),
            "top_customers": ReportsService.get_top_customers(this_month, 5),
        }


__all__ = ["ReportsService", "ReportPeriod"]
