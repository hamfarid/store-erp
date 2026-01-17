#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.57: Dashboard Widgets API

API endpoints for dashboard statistics and widgets.
"""

import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from sqlalchemy import func, extract
from src.database import db
from src.routes.auth_unified import token_required
from src.permissions import require_permission, Permissions

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


# =============================================================================
# Helper Functions
# =============================================================================


def get_date_range(period: str):
    """Get start and end dates for a period."""
    today = datetime.now().date()

    if period == "today":
        return today, today
    elif period == "yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday, yesterday
    elif period == "week":
        start = today - timedelta(days=today.weekday())
        return start, today
    elif period == "month":
        start = today.replace(day=1)
        return start, today
    elif period == "year":
        start = today.replace(month=1, day=1)
        return start, today
    elif period == "last_month":
        first_this_month = today.replace(day=1)
        last_last_month = first_this_month - timedelta(days=1)
        first_last_month = last_last_month.replace(day=1)
        return first_last_month, last_last_month
    else:
        # Default to current month
        return today.replace(day=1), today


def calculate_change(current: float, previous: float) -> dict:
    """Calculate percentage change between two values."""
    if previous == 0:
        percentage = 100 if current > 0 else 0
    else:
        percentage = ((current - previous) / previous) * 100

    return {
        "value": round(current, 2),
        "previous": round(previous, 2),
        "change": round(percentage, 2),
        "trend": "up" if percentage > 0 else ("down" if percentage < 0 else "neutral"),
    }


# =============================================================================
# Routes
# =============================================================================


@dashboard_bp.route("/summary", methods=["GET"])
@token_required
@require_permission(Permissions.DASHBOARD_VIEW)
def get_summary():
    """
    Get dashboard summary statistics.

    Returns key metrics for the dashboard overview.
    """
    from src.models.invoice import Invoice
    from src.models.product import Product
    from src.models.partners import Customer, Supplier

    period = request.args.get("period", "month")
    start_date, end_date = get_date_range(period)

    # Calculate previous period for comparison
    period_days = (end_date - start_date).days + 1
    prev_end = start_date - timedelta(days=1)
    prev_start = prev_end - timedelta(days=period_days - 1)

    # Current period metrics
    current_sales = (
        db.session.query(func.coalesce(func.sum(Invoice.total), 0))
        .filter(
            Invoice.type == "sale",
            func.date(Invoice.created_at) >= start_date,
            func.date(Invoice.created_at) <= end_date,
        )
        .scalar()
        or 0
    )

    current_purchases = (
        db.session.query(func.coalesce(func.sum(Invoice.total), 0))
        .filter(
            Invoice.type == "purchase",
            func.date(Invoice.created_at) >= start_date,
            func.date(Invoice.created_at) <= end_date,
        )
        .scalar()
        or 0
    )

    # Previous period metrics
    prev_sales = (
        db.session.query(func.coalesce(func.sum(Invoice.total), 0))
        .filter(
            Invoice.type == "sale",
            func.date(Invoice.created_at) >= prev_start,
            func.date(Invoice.created_at) <= prev_end,
        )
        .scalar()
        or 0
    )

    prev_purchases = (
        db.session.query(func.coalesce(func.sum(Invoice.total), 0))
        .filter(
            Invoice.type == "purchase",
            func.date(Invoice.created_at) >= prev_start,
            func.date(Invoice.created_at) <= prev_end,
        )
        .scalar()
        or 0
    )

    # Counts
    total_products = Product.query.count()
    total_customers = Customer.query.count()
    total_suppliers = Supplier.query.count()

    # Low stock products
    low_stock = Product.query.filter(
        Product.quantity <= Product.min_stock_level
    ).count()

    # Pending invoices
    pending_invoices = Invoice.query.filter(Invoice.status == "pending").count()

    return jsonify(
        {
            "success": True,
            "data": {
                "period": period,
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                },
                "sales": calculate_change(float(current_sales), float(prev_sales)),
                "purchases": calculate_change(
                    float(current_purchases), float(prev_purchases)
                ),
                "profit": calculate_change(
                    float(current_sales - current_purchases),
                    float(prev_sales - prev_purchases),
                ),
                "counts": {
                    "products": total_products,
                    "customers": total_customers,
                    "suppliers": total_suppliers,
                    "low_stock": low_stock,
                    "pending_invoices": pending_invoices,
                },
            },
        }
    )


@dashboard_bp.route("/sales-chart", methods=["GET"])
@token_required
@require_permission(Permissions.DASHBOARD_VIEW)
def get_sales_chart():
    """
    Get sales data for charts.

    Query params:
        period: week, month, year
        type: daily, weekly, monthly
    """
    from src.models.invoice import Invoice

    period = request.args.get("period", "month")
    chart_type = request.args.get("type", "daily")

    start_date, end_date = get_date_range(period)

    # Build query based on grouping
    if chart_type == "daily":
        sales_data = (
            db.session.query(
                func.date(Invoice.created_at).label("date"),
                func.coalesce(func.sum(Invoice.total), 0).label("total"),
            )
            .filter(
                Invoice.type == "sale",
                func.date(Invoice.created_at) >= start_date,
                func.date(Invoice.created_at) <= end_date,
            )
            .group_by(func.date(Invoice.created_at))
            .order_by("date")
            .all()
        )

    elif chart_type == "weekly":
        sales_data = (
            db.session.query(
                extract("week", Invoice.created_at).label("week"),
                extract("year", Invoice.created_at).label("year"),
                func.coalesce(func.sum(Invoice.total), 0).label("total"),
            )
            .filter(
                Invoice.type == "sale",
                func.date(Invoice.created_at) >= start_date,
                func.date(Invoice.created_at) <= end_date,
            )
            .group_by("week", "year")
            .order_by("year", "week")
            .all()
        )

    else:  # monthly
        sales_data = (
            db.session.query(
                extract("month", Invoice.created_at).label("month"),
                extract("year", Invoice.created_at).label("year"),
                func.coalesce(func.sum(Invoice.total), 0).label("total"),
            )
            .filter(
                Invoice.type == "sale",
                func.date(Invoice.created_at) >= start_date,
                func.date(Invoice.created_at) <= end_date,
            )
            .group_by("month", "year")
            .order_by("year", "month")
            .all()
        )

    # Format response
    if chart_type == "daily":
        chart_data = [
            {"label": row.date.strftime("%Y-%m-%d"), "value": float(row.total)}
            for row in sales_data
        ]
    elif chart_type == "weekly":
        chart_data = [
            {"label": f"W{int(row.week)}/{int(row.year)}", "value": float(row.total)}
            for row in sales_data
        ]
    else:
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        chart_data = [
            {
                "label": f"{months[int(row.month) - 1]} {int(row.year)}",
                "value": float(row.total),
            }
            for row in sales_data
        ]

    return jsonify(
        {
            "success": True,
            "data": {
                "type": chart_type,
                "period": period,
                "labels": [d["label"] for d in chart_data],
                "values": [d["value"] for d in chart_data],
                "total": sum(d["value"] for d in chart_data),
            },
        }
    )


@dashboard_bp.route("/top-products", methods=["GET"])
@token_required
@require_permission(Permissions.DASHBOARD_VIEW)
def get_top_products():
    """
    Get top selling products.

    Query params:
        period: week, month, year
        limit: Number of products (default 10)
    """
    from src.models.invoice import Invoice, InvoiceItem
    from src.models.product import Product

    period = request.args.get("period", "month")
    limit = request.args.get("limit", 10, type=int)

    start_date, end_date = get_date_range(period)

    # Query top products by quantity sold
    top_products = (
        db.session.query(
            Product.id,
            Product.name,
            Product.sku,
            func.sum(InvoiceItem.quantity).label("quantity_sold"),
            func.sum(InvoiceItem.total).label("revenue"),
        )
        .join(InvoiceItem, InvoiceItem.product_id == Product.id)
        .join(Invoice, Invoice.id == InvoiceItem.invoice_id)
        .filter(
            Invoice.type == "sale",
            func.date(Invoice.created_at) >= start_date,
            func.date(Invoice.created_at) <= end_date,
        )
        .group_by(Product.id)
        .order_by(func.sum(InvoiceItem.quantity).desc())
        .limit(limit)
        .all()
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "period": period,
                "products": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "sku": p.sku,
                        "quantity_sold": int(p.quantity_sold),
                        "revenue": float(p.revenue),
                    }
                    for p in top_products
                ],
            },
        }
    )


@dashboard_bp.route("/top-customers", methods=["GET"])
@token_required
@require_permission(Permissions.DASHBOARD_VIEW)
def get_top_customers():
    """
    Get top customers by purchase amount.
    """
    from src.models.invoice import Invoice
    from src.models.partners import Customer

    period = request.args.get("period", "month")
    limit = request.args.get("limit", 10, type=int)

    start_date, end_date = get_date_range(period)

    top_customers = (
        db.session.query(
            Customer.id,
            Customer.name,
            func.count(Invoice.id).label("order_count"),
            func.sum(Invoice.total).label("total_spent"),
        )
        .join(Invoice, Invoice.customer_id == Customer.id)
        .filter(
            Invoice.type == "sale",
            func.date(Invoice.created_at) >= start_date,
            func.date(Invoice.created_at) <= end_date,
        )
        .group_by(Customer.id)
        .order_by(func.sum(Invoice.total).desc())
        .limit(limit)
        .all()
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "period": period,
                "customers": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "order_count": int(c.order_count),
                        "total_spent": float(c.total_spent),
                    }
                    for c in top_customers
                ],
            },
        }
    )


@dashboard_bp.route("/low-stock", methods=["GET"])
@token_required
@require_permission(Permissions.INVENTORY_VIEW)
def get_low_stock():
    """
    Get products with low stock.
    """
    from src.models.product import Product

    limit = request.args.get("limit", 20, type=int)

    low_stock_products = (
        Product.query.filter(Product.quantity <= Product.min_stock_level)
        .order_by(Product.quantity.asc())
        .limit(limit)
        .all()
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "total_count": Product.query.filter(
                    Product.quantity <= Product.min_stock_level
                ).count(),
                "products": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "sku": p.sku,
                        "quantity": p.quantity,
                        "min_stock_level": p.min_stock_level,
                        "shortage": p.min_stock_level - p.quantity,
                    }
                    for p in low_stock_products
                ],
            },
        }
    )


@dashboard_bp.route("/recent-activity", methods=["GET"])
@token_required
@require_permission(Permissions.DASHBOARD_VIEW)
def get_recent_activity():
    """
    Get recent activity feed.
    """
    from src.models.invoice import Invoice
    from src.models.stock_movement import StockMovement

    limit = request.args.get("limit", 20, type=int)

    # Recent invoices
    recent_invoices = (
        Invoice.query.order_by(Invoice.created_at.desc()).limit(limit // 2).all()
    )

    # Recent stock movements
    recent_movements = (
        StockMovement.query.order_by(StockMovement.created_at.desc())
        .limit(limit // 2)
        .all()
    )

    # Combine and sort
    activities = []

    for inv in recent_invoices:
        activities.append(
            {
                "type": "invoice",
                "action": f"{'Sale' if inv.type == 'sale' else 'Purchase'} #{inv.invoice_number}",
                "description": f"Total: ${inv.total:.2f}",
                "timestamp": inv.created_at.isoformat(),
                "id": inv.id,
            }
        )

    for mov in recent_movements:
        activities.append(
            {
                "type": "stock",
                "action": f"Stock {mov.movement_type}",
                "description": f"{mov.quantity} units of product #{mov.product_id}",
                "timestamp": mov.created_at.isoformat(),
                "id": mov.id,
            }
        )

    # Sort by timestamp
    activities.sort(key=lambda x: x["timestamp"], reverse=True)

    return jsonify({"success": True, "data": {"activities": activities[:limit]}})


@dashboard_bp.route("/payment-status", methods=["GET"])
@token_required
@require_permission(Permissions.DASHBOARD_VIEW)
def get_payment_status():
    """
    Get payment status breakdown.
    """
    from src.models.invoice import Invoice

    period = request.args.get("period", "month")
    start_date, end_date = get_date_range(period)

    # Get totals by status
    status_totals = (
        db.session.query(
            Invoice.status,
            func.count(Invoice.id).label("count"),
            func.coalesce(func.sum(Invoice.total), 0).label("total"),
        )
        .filter(
            func.date(Invoice.created_at) >= start_date,
            func.date(Invoice.created_at) <= end_date,
        )
        .group_by(Invoice.status)
        .all()
    )

    status_map = {
        s.status: {"count": s.count, "total": float(s.total)} for s in status_totals
    }

    return jsonify(
        {
            "success": True,
            "data": {
                "period": period,
                "paid": status_map.get("paid", {"count": 0, "total": 0}),
                "pending": status_map.get("pending", {"count": 0, "total": 0}),
                "overdue": status_map.get("overdue", {"count": 0, "total": 0}),
                "cancelled": status_map.get("cancelled", {"count": 0, "total": 0}),
            },
        }
    )


__all__ = ["dashboard_bp"]
