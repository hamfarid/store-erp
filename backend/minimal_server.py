#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal Flask Server - No Database
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "Minimal Server Running"})


@app.route("/api/temp/auth/login", methods=["POST", "OPTIONS"])
def login():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if username == "admin" and password == "admin":
        return jsonify(
            {
                "success": True,
                "user": {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@example.com",
                    "full_name": "مدير النظام",
                    "role": "admin",
                },
                "tokens": {
                    "access_token": "temp_access_token_12345",
                    "refresh_token": "temp_refresh_token_67890",
                },
                "message": "تم تسجيل الدخول بنجاح",
            }
        )
    else:
        return (
            jsonify(
                {"success": False, "message": "اسم المستخدم أو كلمة المرور غير صحيحة"}
            ),
            401,
        )


@app.route("/api/dashboard/stats", methods=["GET"])
def dashboard_stats():
    """إحصائيات لوحة التحكم"""
    return jsonify(
        {
            "success": True,
            "data": {
                "total_products": 150,
                "total_customers": 45,
                "total_suppliers": 20,
                "total_invoices": 320,
                "total_revenue": 125000.50,
                "total_profit": 35000.25,
                "low_stock_products": 12,
                "pending_invoices": 8,
            },
        }
    )


@app.route("/api/products", methods=["GET"])
def get_products():
    """قائمة المنتجات"""
    return jsonify(
        {"success": True, "data": [], "total": 0, "message": "لا توجد منتجات حالياً"}
    )


@app.route("/api/customers", methods=["GET"])
def get_customers():
    """قائمة العملاء"""
    return jsonify(
        {"success": True, "data": [], "total": 0, "message": "لا توجد عملاء حالياً"}
    )


@app.route("/api/invoices", methods=["GET"])
def get_invoices():
    """قائمة الفواتير"""
    return jsonify(
        {"success": True, "data": [], "total": 0, "message": "لا توجد فواتير حالياً"}
    )


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Minimal Server Starting...")
    print("🌐 http://localhost:5002")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5002, debug=False, threaded=True)
