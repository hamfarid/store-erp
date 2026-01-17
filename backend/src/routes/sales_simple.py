# FILE: backend/src/routes/sales_simple.py | PURPOSE: Routes with P0.2.4
# error envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# pylint: disable=all
# flake8: noqa
from flask import Blueprint, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)
import logging
import sqlite3
import os

sales_bp = Blueprint("sales", __name__)


def get_db_connection():
    """الحصول على اتصال قاعدة البيانات"""
    db_path = os.path.join(os.path.dirname(__file__), "../../instance/inventory.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@sales_bp.route("/api/sales/invoices", methods=["GET"])
def get_sales_invoices():
    """الحصول على قائمة فواتير المبيعات"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # استعلام بسيط للحصول على الفواتير
        cursor.execute(
            """
            SELECT
                si.id,
                si.invoice_number,
                si.invoice_date,
                si.total_amount,
                si.payment_status,
                c.name as customer_name,
                c.phone as customer_phone
            FROM sales_invoices si
            LEFT JOIN customers c ON si.customer_id = c.id
            ORDER BY si.created_at DESC
        """
        )

        invoices = []
        for row in cursor.fetchall():
            invoice = {
                "id": row["id"],
                "invoice_number": row["invoice_number"],
                "invoice_date": row["invoice_date"],
                "total_amount": (
                    float(row["total_amount"]) if row["total_amount"] else 0
                ),
                "payment_status": row["payment_status"],
                "customer_name": row["customer_name"] or "غير محدد",
                "customer_phone": row["customer_phone"] or "",
            }

            # الحصول على عناصر الفاتورة
            cursor.execute(
                """
                SELECT
                    sii.quantity,
                    sii.unit_price,
                    sii.total_price,
                    p.name as product_name,
                    p.unit
                FROM sales_invoice_items sii
                LEFT JOIN products p ON sii.product_id = p.id
                WHERE sii.invoice_id = ?
            """,
                (row["id"],),
            )

            items = []
            for item_row in cursor.fetchall():
                items.append(
                    {
                        "product_name": item_row["product_name"] or "غير محدد",
                        "quantity": (
                            float(item_row["quantity"]) if item_row["quantity"] else 0
                        ),
                        "unit_price": (
                            float(item_row["unit_price"])
                            if item_row["unit_price"]
                            else 0
                        ),
                        "total_price": (
                            float(item_row["total_price"])
                            if item_row["total_price"]
                            else 0
                        ),
                        "unit": item_row["unit"] or "قطعة",
                    }
                )

            invoice["items"] = items
            invoices.append(invoice)

        conn.close()

        return jsonify(invoices)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@sales_bp.route("/api/sales/invoices/<int:invoice_id>", methods=["GET"])
def get_sales_invoice(invoice_id):
    """الحصول على فاتورة مبيعات محددة"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                si.*,
                c.name as customer_name,
                c.phone as customer_phone,
                c.email as customer_email,
                c.address as customer_address
            FROM sales_invoices si
            LEFT JOIN customers c ON si.customer_id = c.id
            WHERE si.id = ?
        """,
            (invoice_id,),
        )

        invoice_row = cursor.fetchone()
        if not invoice_row:
            return jsonify({"error": "الفاتورة غير موجودة"}), 404

        invoice = dict(invoice_row)

        # الحصول على عناصر الفاتورة
        cursor.execute(
            """
            SELECT
                sii.*,
                p.name as product_name,
                p.unit,
                p.classification,
                p.supplier_name
            FROM sales_invoice_items sii
            LEFT JOIN products p ON sii.product_id = p.id
            WHERE sii.invoice_id = ?
        """,
            (invoice_id,),
        )

        items = [dict(row) for row in cursor.fetchall()]
        invoice["items"] = items

        conn.close()

        return jsonify(invoice)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@sales_bp.route("/api/sales/stats", methods=["GET"])
def get_sales_stats():
    """الحصول على إحصائيات المبيعات"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # إجمالي المبيعات
        cursor.execute("SELECT COUNT(*), SUM(total_amount) FROM sales_invoices")
        total_invoices, total_amount = cursor.fetchone()

        # المبيعات المدفوعة
        cursor.execute(
            """
            SELECT COUNT(*), SUM(total_amount)
            FROM sales_invoices
            WHERE payment_status = 'مدفوعة'
        """
        )
        paid_invoices, paid_amount = cursor.fetchone()

        # المبيعات المعلقة
        cursor.execute(
            """
            SELECT COUNT(*), SUM(total_amount)
            FROM sales_invoices
            WHERE payment_status = 'معلقة'
        """
        )
        pending_invoices, pending_amount = cursor.fetchone()

        conn.close()

        stats = {
            "total_invoices": total_invoices or 0,
            "total_amount": float(total_amount) if total_amount else 0,
            "paid_invoices": paid_invoices or 0,
            "paid_amount": float(paid_amount) if paid_amount else 0,
            "pending_invoices": pending_invoices or 0,
            "pending_amount": float(pending_amount) if pending_amount else 0,
        }

        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
