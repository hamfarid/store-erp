#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق Flask مبسط - للاختبار فقط
Simple Flask Application - For Testing Only
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# تكوين بسيط
app.config["SECRET_KEY"] = "dev-secret-key-12345"


@app.route("/")
def index():
    return jsonify(
        {
            "success": True,
            "message": "Simple Inventory Management System API",
            "version": "1.5.0-simple",
            "status": "running",
        }
    )


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "message": "Server is running"})


@app.route("/api/temp/auth/login", methods=["POST"])
def temp_login():
    """تسجيل دخول مؤقت"""
    try:
        data = request.get_json() or {}
        username = data.get("username", "")
        password = data.get("password", "")

        # تسجيل دخول مؤقت
        if username == "admin" and password == "admin":
            return jsonify(
                {
                    "success": True,
                    "data": {
                        "token": "temp_token_12345",
                        "user": {
                            "id": 1,
                            "username": "admin",
                            "email": "admin@example.com",
                            "full_name": "مدير النظام",
                            "role": "admin",
                        },
                    },
                    "message": "تم تسجيل الدخول بنجاح",
                }
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "اسم المستخدم أو كلمة المرور غير صحيحة",
                    }
                ),
                401,
            )

    except Exception as e:
        return (
            jsonify(
                {"success": False, "error": str(e), "message": "خطأ في تسجيل الدخول"}
            ),
            500,
        )


@app.route("/api/temp/products", methods=["GET"])
def get_products():
    """منتجات تجريبية"""
    return jsonify(
        {
            "success": True,
            "data": [
                {
                    "id": 1,
                    "name": "منتج تجريبي 1",
                    "sku": "PROD001",
                    "price": 100.0,
                    "quantity": 50,
                },
                {
                    "id": 2,
                    "name": "منتج تجريبي 2",
                    "sku": "PROD002",
                    "price": 200.0,
                    "quantity": 30,
                },
            ],
        }
    )


if __name__ == "__main__":
    print("=" * 80)
    print("🚀 Starting Simple Inventory Management System")
    print("🌐 Server: http://0.0.0.0:5002")
    print("=" * 80)
    app.run(host="0.0.0.0", port=5002, debug=False)
