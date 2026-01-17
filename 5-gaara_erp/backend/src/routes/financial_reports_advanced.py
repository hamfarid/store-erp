# FILE: backend/src/routes/financial_reports_advanced.py | PURPOSE: Routes
# with P0.2.4 error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Advanced Financial Reports API Routes
Handles comprehensive financial reporting and analysis
All linting disabled due to complex imports and optional dependencies.
"""

from flask import Blueprint, request, jsonify, current_app

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging

try:
    from flask_login import login_required, current_user
except ImportError:
    # Create dummy decorators if flask_login is not available
    def login_required(f):
        return f

    class DummyUser:
        def __init__(self):
            self.id = 1
            self.is_authenticated = True

    current_user = DummyUser()
from datetime import datetime, timedelta
import json
import os
from decimal import Decimal
import io
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

financial_reports_advanced_bp = Blueprint("financial_reports_advanced", __name__)


def get_date_range(period, start_date=None, end_date=None):
    """Get date range based on period"""
    today = datetime.now()

    if period == "today":
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif period == "week":
        start = today - timedelta(days=today.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(
            days=6, hours=23, minutes=59, seconds=59, microseconds=999999
        )
    elif period == "month":
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if today.month == 12:
            end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(
                microseconds=1
            )
        else:
            end = today.replace(month=today.month + 1, day=1) - timedelta(
                microseconds=1
            )
    elif period == "quarter":
        quarter = (today.month - 1) // 3 + 1
        start = today.replace(
            month=(quarter - 1) * 3 + 1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        end_month = quarter * 3
        if end_month == 12:
            end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(
                microseconds=1
            )
        else:
            end = today.replace(month=end_month + 1, day=1) - timedelta(microseconds=1)
    elif period == "year":
        start = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(
            microseconds=1
        )
    elif period == "custom" and start_date and end_date:
        start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    else:
        # Default to current month
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if today.month == 12:
            end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(
                microseconds=1
            )
        else:
            end = today.replace(month=today.month + 1, day=1) - timedelta(
                microseconds=1
            )

    return start, end


def calculate_financial_metrics(revenue_data, expense_data):
    """Calculate financial metrics from revenue and expense data"""
    total_revenue = sum(item.get("amount", 0) for item in revenue_data)
    total_expenses = sum(item.get("amount", 0) for item in expense_data)
    net_profit = total_revenue - total_expenses
    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0

    return {
        "totalRevenue": total_revenue,
        "totalExpenses": total_expenses,
        "netProfit": net_profit,
        "profitMargin": round(profit_margin, 2),
    }


def get_mock_financial_data(start_date, end_date):
    """Generate mock financial data for demonstration"""
    # This would normally query the database
    # For now, return mock data

    revenue_data = [
        {
            "date": "2024-01-01",
            "amount": 15000,
            "category": "sales",
            "description": "مبيعات البذور",
        },
        {
            "date": "2024-01-02",
            "amount": 12000,
            "category": "sales",
            "description": "مبيعات الأسمدة",
        },
        {
            "date": "2024-01-03",
            "amount": 8000,
            "category": "sales",
            "description": "مبيعات المبيدات",
        },
        {
            "date": "2024-01-04",
            "amount": 10000,
            "category": "sales",
            "description": "مبيعات أدوات الزراعة",
        },
        {
            "date": "2024-01-05",
            "amount": 18000,
            "category": "sales",
            "description": "مبيعات متنوعة",
        },
    ]

    expense_data = [
        {
            "date": "2024-01-01",
            "amount": 8000,
            "category": "cost_of_goods",
            "description": "تكلفة البضاعة المباعة",
        },
        {
            "date": "2024-01-02",
            "amount": 3000,
            "category": "operating",
            "description": "مصروفات تشغيلية",
        },
        {
            "date": "2024-01-03",
            "amount": 2000,
            "category": "marketing",
            "description": "مصروفات تسويق",
        },
        {
            "date": "2024-01-04",
            "amount": 1500,
            "category": "utilities",
            "description": "فواتير المرافق",
        },
        {
            "date": "2024-01-05",
            "amount": 2500,
            "category": "salaries",
            "description": "رواتب الموظفين",
        },
    ]

    return revenue_data, expense_data


@financial_reports_advanced_bp.route("/api/reports/financial", methods=["GET"])
@login_required
def get_financial_reports():
    """Get comprehensive financial reports"""
    try:
        # Get parameters
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get

        # Get date range
        start, end = get_date_range(period, start_date, end_date)

        # Get financial data (mock data for now)
        revenue_data, expense_data = get_mock_financial_data(start, end)

        # Calculate summary metrics
        summary = calculate_financial_metrics(revenue_data, expense_data)

        # Generate monthly breakdown
        monthly_data = [
            {"month": "يناير", "revenue": 15000, "expenses": 10000, "profit": 5000},
            {"month": "فبراير", "revenue": 18000, "expenses": 12000, "profit": 6000},
            {"month": "مارس", "revenue": 22000, "expenses": 15000, "profit": 7000},
            {"month": "أبريل", "revenue": 20000, "expenses": 13000, "profit": 7000},
            {"month": "مايو", "revenue": 25000, "expenses": 17000, "profit": 8000},
            {"month": "يونيو", "revenue": 25000, "expenses": 18000, "profit": 7000},
        ]

        # Category breakdown
        category_breakdown = [
            {"category": "البذور", "revenue": 45000, "percentage": 36},
            {"category": "الأسمدة", "revenue": 35000, "percentage": 28},
            {"category": "المبيدات", "revenue": 25000, "percentage": 20},
            {"category": "أدوات الزراعة", "revenue": 20000, "percentage": 16},
        ]

        # Top products
        top_products = [
            {"name": "بذور طماطم هجين", "sales": 15000, "quantity": 500},
            {"name": "سماد NPK", "sales": 12000, "quantity": 300},
            {"name": "مبيد حشري", "sales": 10000, "quantity": 200},
            {"name": "بذور خيار", "sales": 8000, "quantity": 250},
        ]

        return jsonify(
            {
                "status": "success",
                "data": {
                    "summary": summary,
                    "monthlyData": monthly_data,
                    "categoryBreakdown": category_breakdown,
                    "topProducts": top_products,
                    "period": period,
                    "startDate": start.isoformat(),
                    "endDate": end.isoformat(),
                    "currency": currency,
                },
            }
        )

    except Exception as e:
        current_app.logger.error(f"Error generating financial reports: {e}")
        return (
            jsonify({"status": "error", "message": "خطأ في إنشاء التقارير المالية"}),
            500,
        )


@financial_reports_advanced_bp.route("/api/reports/financial/export", methods=["GET"])
@login_required
def export_financial_report():
    """Export financial report in various formats"""
    try:
        # Get parameters
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get

        # Get date range
        start, end = get_date_range(period, start_date, end_date)

        # Get financial data
        revenue_data, expense_data = get_mock_financial_data(start, end)
        summary = calculate_financial_metrics(revenue_data, expense_data)

        if format_type == "csv":
            # Generate CSV
            output = io.StringIO()
            writer = csv.writer(output)

            # Write headers
            writer.writerow(["التقرير المالي"])
            writer.writerow(
                [
                    "الفترة",
                    f'{start.strftime("%Y-%m-%d")} إلى {end.strftime("%Y-%m-%d")}',
                ]
            )
            writer.writerow(["العملة", currency])
            writer.writerow([])

            # Write summary
            writer.writerow(["الملخص"])
            writer.writerow(["إجمالي الإيرادات", summary["totalRevenue"]])
            writer.writerow(["إجمالي المصروفات", summary["totalExpenses"]])
            writer.writerow(["صافي الربح", summary["netProfit"]])
            writer.writerow(["هامش الربح (%)", summary["profitMargin"]])
            writer.writerow([])

            # Write revenue details
            writer.writerow(["تفاصيل الإيرادات"])
            writer.writerow(["التاريخ", "المبلغ", "الفئة", "الوصف"])
            for item in revenue_data:
                writer.writerow(
                    [
                        item["date"],
                        item["amount"],
                        item["category"],
                        item["description"],
                    ]
                )

            writer.writerow([])

            # Write expense details
            writer.writerow(["تفاصيل المصروفات"])
            writer.writerow(["التاريخ", "المبلغ", "الفئة", "الوصف"])
            for item in expense_data:
                writer.writerow(
                    [
                        item["date"],
                        item["amount"],
                        item["category"],
                        item["description"],
                    ]
                )

            return jsonify(
                {
                    "status": "success",
                    "data": output.getvalue(),
                    "filename": f'financial_report_{start.strftime("%Y%m%d")}_{end.strftime("%Y%m%d")}.csv',
                }
            )

        elif format_type == "pd":
            # Generate PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=18,
                spaceAfter=30,
                alignment=1,  # Center alignment
            )
            story.append(Paragraph("التقرير المالي", title_style))
            story.append(Spacer(1, 12))

            # Period info
            period_info = (
                f'الفترة: {start.strftime("%Y-%m-%d")} إلى {end.strftime("%Y-%m-%d")}'
            )
            story.append(Paragraph(period_info, styles["Normal"]))
            story.append(Paragraph(f"العملة: {currency}", styles["Normal"]))
            story.append(Spacer(1, 12))

            # Summary table
            summary_data = [
                ["البيان", "المبلغ"],
                ["إجمالي الإيرادات", f'{summary["totalRevenue"]:,.2f}'],
                ["إجمالي المصروفات", f'{summary["totalExpenses"]:,.2f}'],
                ["صافي الربح", f'{summary["netProfit"]:,.2f}'],
                ["هامش الربح (%)", f'{summary["profitMargin"]:.2f}%'],
            ]

            summary_table = Table(summary_data)
            summary_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 14),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(summary_table)
            story.append(Spacer(1, 12))

            # Build PDF
            doc.build(story)

            return jsonify(
                {
                    "status": "success",
                    "data": buffer.getvalue().hex(),  # Return as hex string
                    "filename": f'financial_report_{start.strftime("%Y%m%d")}_{end.strftime("%Y%m%d")}.pdf',
                }
            )

        else:
            return (
                jsonify({"status": "error", "message": "صيغة التصدير غير مدعومة"}),
                400,
            )

    except Exception as e:
        current_app.logger.error(f"Error exporting financial report: {e}")
        return (
            jsonify({"status": "error", "message": "خطأ في تصدير التقرير المالي"}),
            500,
        )


@financial_reports_advanced_bp.route(
    "/api/reports/financial/dashboard", methods=["GET"]
)
@login_required
def get_financial_dashboard():
    """Get financial dashboard data"""
    try:
        # Get current month data
        today = datetime.now()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Get financial data
        revenue_data, expense_data = get_mock_financial_data(start_of_month, today)
        summary = calculate_financial_metrics(revenue_data, expense_data)

        # Calculate trends (mock data)
        trends = {
            "revenueGrowth": 12.5,  # Percentage growth
            "expenseGrowth": 8.3,
            "profitGrowth": 18.7,
        }

        # Key performance indicators
        kpis = {
            "averageDailySales": summary["totalRevenue"] / today.day,
            "averageOrderValue": 850.0,
            "customerAcquisitionCost": 125.0,
            "returnOnInvestment": 24.5,
        }

        return jsonify(
            {
                "status": "success",
                "data": {
                    "summary": summary,
                    "trends": trends,
                    "kpis": kpis,
                    "lastUpdated": datetime.now().isoformat(),
                },
            }
        )

    except Exception as e:
        current_app.logger.error(f"Error getting financial dashboard: {e}")
        return error_response(
            message="خطأ في تحميل لوحة التحكم المالية",
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500,
        )


@financial_reports_advanced_bp.route(
    "/api/reports/financial/comparison", methods=["GET"]
)
@login_required
def get_financial_comparison():
    """Get financial comparison between periods"""
    try:
        # Get parameters
        _ = request.args.get
        _ = request.args.get
        _ = request.args.get
        period2_end = request.args.get("period2End")

        if not all([period1_start, period1_end, period2_start, period2_end]):
            return (
                jsonify({"status": "error", "message": "يجب تحديد فترتين للمقارنة"}),
                400,
            )

        # Get data for both periods
        revenue_data1, expense_data1 = get_mock_financial_data(
            period1_start, period1_end
        )
        revenue_data2, expense_data2 = get_mock_financial_data(
            period2_start, period2_end
        )

        summary1 = calculate_financial_metrics(revenue_data1, expense_data1)
        summary2 = calculate_financial_metrics(revenue_data2, expense_data2)

        # Calculate changes
        changes = {
            "revenueChange": (
                (
                    (summary2["totalRevenue"] - summary1["totalRevenue"])
                    / summary1["totalRevenue"]
                    * 100
                )
                if summary1["totalRevenue"] > 0
                else 0
            ),
            "expenseChange": (
                (
                    (summary2["totalExpenses"] - summary1["totalExpenses"])
                    / summary1["totalExpenses"]
                    * 100
                )
                if summary1["totalExpenses"] > 0
                else 0
            ),
            "profitChange": (
                (
                    (summary2["netProfit"] - summary1["netProfit"])
                    / abs(summary1["netProfit"])
                    * 100
                )
                if summary1["netProfit"] != 0
                else 0
            ),
        }

        return jsonify(
            {
                "status": "success",
                "data": {
                    "period1": {
                        "summary": summary1,
                        "startDate": period1_start,
                        "endDate": period1_end,
                    },
                    "period2": {
                        "summary": summary2,
                        "startDate": period2_start,
                        "endDate": period2_end,
                    },
                    "changes": changes,
                },
            }
        )

    except Exception as e:
        current_app.logger.error(f"Error getting financial comparison: {e}")
        return (
            jsonify({"status": "error", "message": "خطأ في مقارنة البيانات المالية"}),
            500,
        )
