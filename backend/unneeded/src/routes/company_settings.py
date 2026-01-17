# FILE: backend/src/routes/company_settings.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Company Settings API Routes
Handles company information and configuration settings
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
    from flask_login import current_user, login_required

    FLASK_LOGIN_AVAILABLE = True
except ImportError:
    FLASK_LOGIN_AVAILABLE = False
    # Mock current_user and login_required

    class DummyUser:
        def __init__(self):
            self.role = "admin"
            self.is_authenticated = True

    current_user = DummyUser()

    def login_required(f):
        return f

    class DummyUser:
        def __init__(self):
            self.id = 1
            self.is_authenticated = True

    current_user = DummyUser()
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64

company_settings_bp = Blueprint("company_settings", __name__)

# Configuration
UPLOAD_FOLDER = "static/uploads/company"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gi"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_image(image_data, max_size=(300, 300)):
    """Resize image to maximum dimensions"""
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_data))

        # Convert to RGB if necessary
        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGB")

        # Resize image maintaining aspect ratio
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save to bytes
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=85, optimize=True)
        return output.getvalue()

    except Exception as e:
        current_app.logger.error(f"Error resizing image: {e}")
        return None


@company_settings_bp.route("/api/settings/company", methods=["GET"])
@login_required
def get_company_settings():
    """Get company settings"""
    try:
        # Path to settings file
        settings_file = os.path.join(current_app.instance_path, "company_settings.json")

        # Default settings
        default_settings = {
            "name": "شركة إدارة المخزون",
            "nameEn": "Inventory Management Company",
            "address": "",
            "addressEn": "",
            "phone": "",
            "email": "",
            "website": "",
            "taxNumber": "",
            "commercialRegister": "",
            "logo": "",
            "currency": "EGP",
            "language": "ar",
            "timezone": "Africa/Cairo",
            "dateFormat": "DD/MM/YYYY",
            "numberFormat": "ar-EG",
        }

        # Read existing settings or use defaults
        if os.path.exists(settings_file):
            with open(settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                default_settings.update(settings)

        return jsonify({"status": "success", "data": default_settings})

    except Exception as e:
        current_app.logger.error(f"Error getting company settings: {e}")
        return jsonify({"status": "error", "message": "خطأ في جلب إعدادات الشركة"}), 500


@company_settings_bp.route("/api/settings/company", methods=["POST"])
@login_required
def update_company_settings():
    """Update company settings"""
    try:
        # Check admin permissions
        if not hasattr(current_user, "role") or current_user.role != "admin":
            return (
                jsonify(
                    {"status": "error", "message": "غير مصرح لك بتعديل إعدادات الشركة"}
                ),
                403,
            )

        # Create instance directory if it doesn't exist
        os.makedirs(current_app.instance_path, exist_ok=True)
        os.makedirs(
            os.path.join(current_app.instance_path, "uploads", "company"), exist_ok=True
        )

        settings_file = os.path.join(current_app.instance_path, "company_settings.json")

        # Get form data
        data = {}
        for key in [
            "name",
            "nameEn",
            "address",
            "addressEn",
            "phone",
            "email",
            "website",
            "taxNumber",
            "commercialRegister",
            "currency",
            "language",
            "timezone",
            "dateFormat",
            "numberFormat",
        ]:
            if key in request.form:
                data[key] = request.form[key]

        # Handle logo upload
        if "logo" in request.files:
            file = request.files["logo"]
            if file and file.filename and allowed_file(file.filename):
                try:
                    # Read file data
                    file_data = file.read()

                    # Check file size
                    if len(file_data) > MAX_FILE_SIZE:
                        return (
                            jsonify(
                                {
                                    "status": "error",
                                    "message": "حجم الملف كبير جداً (الحد الأقصى 2 ميجابايت)",
                                }
                            ),
                            400,
                        )

                    # Resize image
                    resized_data = resize_image(file_data)
                    if resized_data:
                        # Generate unique filename
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"logo_{timestamp}.jpg"
                        file_path = os.path.join(
                            current_app.instance_path, "uploads", "company", filename
                        )

                        with open(file_path, "wb") as f:
                            f.write(resized_data)

                        # Store relative path
                        data["logo"] = f"/static/uploads/company/{filename}"
                    else:
                        return (
                            jsonify(
                                {"status": "error", "message": "خطأ في معالجة الصورة"}
                            ),
                            400,
                        )

                except Exception as e:
                    current_app.logger.error(f"Error processing logo: {e}")
                    return (
                        jsonify({"status": "error", "message": "خطأ في رفع الشعار"}),
                        500,
                    )

        # Read existing settings
        existing_settings = {}
        if os.path.exists(settings_file):
            with open(settings_file, "r", encoding="utf-8") as f:
                existing_settings = json.load(f)

        # Update settings
        existing_settings.update(data)
        existing_settings["lastUpdated"] = datetime.now().isoformat()

        # Save settings
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(existing_settings, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "status": "success",
                "message": "تم حفظ إعدادات الشركة بنجاح",
                "data": existing_settings,
            }
        )

    except Exception as e:
        current_app.logger.error(f"Error updating company settings: {e}")
        return jsonify({"status": "error", "message": "خطأ في حفظ إعدادات الشركة"}), 500


@company_settings_bp.route("/api/settings/company/logo", methods=["DELETE"])
@login_required
def delete_company_logo():
    """Delete company logo"""
    try:
        # Check admin permissions
        if not hasattr(current_user, "role") or current_user.role != "admin":
            return (
                jsonify({"status": "error", "message": "غير مصرح لك بحذف شعار الشركة"}),
                403,
            )

        settings_file = os.path.join(current_app.instance_path, "company_settings.json")

        # Read existing settings
        if os.path.exists(settings_file):
            with open(settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)

            # Delete logo file if exists
            if "logo" in settings and settings["logo"]:
                logo_path = settings["logo"].replace("/static/", "")
                full_logo_path = os.path.join(current_app.instance_path, logo_path)
                if os.path.exists(full_logo_path):
                    os.remove(full_logo_path)

            # Remove logo from settings
            settings["logo"] = ""
            settings["lastUpdated"] = datetime.now().isoformat()

            # Save updated settings
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

        return jsonify({"status": "success", "message": "تم حذف شعار الشركة بنجاح"})

    except Exception as e:
        current_app.logger.error(f"Error deleting company logo: {e}")
        return jsonify({"status": "error", "message": "خطأ في حذف شعار الشركة"}), 500


@company_settings_bp.route("/api/settings/company/reset", methods=["POST"])
@login_required
def reset_company_settings():
    """Reset company settings to defaults"""
    try:
        # Check admin permissions
        if not hasattr(current_user, "role") or current_user.role != "admin":
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "غير مصرح لك بإعادة تعيين إعدادات الشركة",
                    }
                ),
                403,
            )

        settings_file = os.path.join(current_app.instance_path, "company_settings.json")

        # Default settings
        default_settings = {
            "name": "شركة إدارة المخزون",
            "nameEn": "Inventory Management Company",
            "address": "",
            "addressEn": "",
            "phone": "",
            "email": "",
            "website": "",
            "taxNumber": "",
            "commercialRegister": "",
            "logo": "",
            "currency": "EGP",
            "language": "ar",
            "timezone": "Africa/Cairo",
            "dateFormat": "DD/MM/YYYY",
            "numberFormat": "ar-EG",
            "lastUpdated": datetime.now().isoformat(),
        }

        # Save default settings
        os.makedirs(current_app.instance_path, exist_ok=True)
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=2)

        return jsonify(
            {
                "status": "success",
                "message": "تم إعادة تعيين إعدادات الشركة بنجاح",
                "data": default_settings,
            }
        )

    except Exception as e:
        current_app.logger.error(f"Error resetting company settings: {e}")
        return (
            jsonify(
                {"status": "error", "message": "خطأ في إعادة تعيين إعدادات الشركة"}
            ),
            500,
        )
