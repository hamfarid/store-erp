#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.60: Barcode and QR Code Generation

Utilities for generating barcodes and QR codes for products.
"""

import io
import base64
import logging
from typing import Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BarcodeConfig:
    """Configuration for barcode generation."""

    width: int = 300
    height: int = 100
    font_size: int = 10
    include_text: bool = True
    format: str = "PNG"  # PNG, SVG


@dataclass
class QRCodeConfig:
    """Configuration for QR code generation."""

    size: int = 200
    error_correction: str = "M"  # L, M, Q, H
    border: int = 4
    format: str = "PNG"
    fill_color: str = "black"
    back_color: str = "white"


class BarcodeGenerator:
    """
    P2.60: Generate various barcode formats.

    Supports:
    - EAN-13 (standard retail)
    - EAN-8
    - Code 128
    - Code 39
    - UPC-A
    """

    BARCODE_TYPES = ["ean13", "ean8", "code128", "code39", "upca", "isbn13", "isbn10"]

    def __init__(self, config: BarcodeConfig = None):
        self.config = config or BarcodeConfig()

    def generate(
        self, data: str, barcode_type: str = "code128", config: BarcodeConfig = None
    ) -> bytes:
        """
        Generate a barcode image.

        Args:
            data: Data to encode
            barcode_type: Type of barcode (ean13, ean8, code128, code39, upca)
            config: Optional custom configuration

        Returns:
            Barcode image as bytes
        """
        try:
            import barcode
            from barcode.writer import ImageWriter
        except ImportError:
            logger.error(
                "python-barcode not installed. Install with: pip install python-barcode[images]"
            )
            raise ImportError("python-barcode required for barcode generation")

        cfg = config or self.config

        # Get barcode class
        barcode_class = barcode.get_barcode_class(barcode_type)

        # Configure writer
        writer = ImageWriter()

        # Generate barcode
        barcode_obj = barcode_class(data, writer=writer)

        # Write to bytes
        output = io.BytesIO()
        barcode_obj.write(
            output,
            options={
                "module_width": 0.2,
                "module_height": 15,
                "font_size": cfg.font_size,
                "text_distance": 5,
                "quiet_zone": 6.5,
                "write_text": cfg.include_text,
            },
        )
        output.seek(0)

        return output.getvalue()

    def generate_base64(
        self, data: str, barcode_type: str = "code128", config: BarcodeConfig = None
    ) -> str:
        """Generate barcode and return as base64 string."""
        image_data = self.generate(data, barcode_type, config)
        return base64.b64encode(image_data).decode("utf-8")

    def generate_svg(self, data: str, barcode_type: str = "code128") -> str:
        """Generate barcode as SVG string."""
        try:
            import barcode
            from barcode.writer import SVGWriter
        except ImportError:
            raise ImportError("python-barcode required for barcode generation")

        barcode_class = barcode.get_barcode_class(barcode_type)
        barcode_obj = barcode_class(data, writer=SVGWriter())

        output = io.BytesIO()
        barcode_obj.write(output)
        output.seek(0)

        return output.getvalue().decode("utf-8")

    @staticmethod
    def validate_ean13(data: str) -> bool:
        """Validate EAN-13 barcode data."""
        if len(data) != 13 or not data.isdigit():
            return False

        # Calculate checksum
        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(data[:12]))
        check_digit = (10 - (total % 10)) % 10

        return int(data[12]) == check_digit

    @staticmethod
    def generate_ean13_check_digit(data: str) -> str:
        """Generate check digit for EAN-13."""
        if len(data) != 12 or not data.isdigit():
            raise ValueError("EAN-13 requires 12 digits")

        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(data))
        check_digit = (10 - (total % 10)) % 10

        return data + str(check_digit)


class QRCodeGenerator:
    """
    P2.60: Generate QR codes.

    Supports various data types:
    - Plain text
    - URLs
    - Product info
    - vCards
    - WiFi credentials
    """

    def __init__(self, config: QRCodeConfig = None):
        self.config = config or QRCodeConfig()

    def generate(self, data: str, config: QRCodeConfig = None) -> bytes:
        """
        Generate a QR code image.

        Args:
            data: Data to encode
            config: Optional custom configuration

        Returns:
            QR code image as bytes
        """
        try:
            import qrcode
            from qrcode.constants import (
                ERROR_CORRECT_L,
                ERROR_CORRECT_M,
                ERROR_CORRECT_Q,
                ERROR_CORRECT_H,
            )
        except ImportError:
            logger.error("qrcode not installed. Install with: pip install qrcode[pil]")
            raise ImportError("qrcode required for QR code generation")

        cfg = config or self.config

        # Map error correction levels
        error_levels = {
            "L": ERROR_CORRECT_L,
            "M": ERROR_CORRECT_M,
            "Q": ERROR_CORRECT_Q,
            "H": ERROR_CORRECT_H,
        }

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_levels.get(cfg.error_correction, ERROR_CORRECT_M),
            box_size=10,
            border=cfg.border,
        )

        qr.add_data(data)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color=cfg.fill_color, back_color=cfg.back_color)

        # Resize if needed
        if cfg.size != 200:
            img = img.resize((cfg.size, cfg.size))

        # Write to bytes
        output = io.BytesIO()
        img.save(output, format=cfg.format)
        output.seek(0)

        return output.getvalue()

    def generate_base64(self, data: str, config: QRCodeConfig = None) -> str:
        """Generate QR code and return as base64 string."""
        image_data = self.generate(data, config)
        return base64.b64encode(image_data).decode("utf-8")

    def generate_product_qr(
        self,
        product_id: int,
        product_name: str,
        price: float = None,
        sku: str = None,
        url: str = None,
    ) -> bytes:
        """Generate QR code with product information."""
        # Build product data
        lines = [
            f"Product: {product_name}",
            f"ID: {product_id}",
        ]

        if sku:
            lines.append(f"SKU: {sku}")
        if price:
            lines.append(f"Price: ${price:.2f}")
        if url:
            lines.append(f"URL: {url}")

        data = "\n".join(lines)
        return self.generate(data)

    def generate_url_qr(self, url: str) -> bytes:
        """Generate QR code for a URL."""
        return self.generate(url)

    def generate_vcard_qr(
        self,
        name: str,
        phone: str = None,
        email: str = None,
        company: str = None,
        address: str = None,
    ) -> bytes:
        """Generate QR code with vCard data."""
        vcard_lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{name}",
        ]

        if phone:
            vcard_lines.append(f"TEL:{phone}")
        if email:
            vcard_lines.append(f"EMAIL:{email}")
        if company:
            vcard_lines.append(f"ORG:{company}")
        if address:
            vcard_lines.append(f"ADR:{address}")

        vcard_lines.append("END:VCARD")

        data = "\n".join(vcard_lines)
        return self.generate(data)

    def generate_wifi_qr(
        self, ssid: str, password: str, security: str = "WPA"
    ) -> bytes:
        """Generate QR code for WiFi credentials."""
        # WiFi QR format: WIFI:T:WPA;S:MySSID;P:MyPassword;;
        data = f"WIFI:T:{security};S:{ssid};P:{password};;"
        return self.generate(data)


# =============================================================================
# Flask Routes Integration
# =============================================================================


def init_barcode_routes(app):
    """Initialize barcode routes in Flask app."""
    from flask import Blueprint, request, jsonify, make_response

    barcode_bp = Blueprint("barcode", __name__, url_prefix="/api/barcode")

    barcode_gen = BarcodeGenerator()
    qr_gen = QRCodeGenerator()

    @barcode_bp.route("/generate", methods=["POST"])
    def generate_barcode():
        data = request.get_json()

        barcode_data = data.get("data")
        barcode_type = data.get("type", "code128")
        format_type = data.get("format", "png")

        if not barcode_data:
            return jsonify({"success": False, "error": "Data is required"}), 400

        if barcode_type not in BarcodeGenerator.BARCODE_TYPES:
            valid_types = BarcodeGenerator.BARCODE_TYPES
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Invalid barcode type. Valid types: {valid_types}",
                    }
                ),
                400,
            )

        try:
            if format_type == "base64":
                image_data = barcode_gen.generate_base64(barcode_data, barcode_type)
                return jsonify(
                    {
                        "success": True,
                        "data": {"image": f"data:image/png;base64,{image_data}"},
                    }
                )
            elif format_type == "svg":
                svg_data = barcode_gen.generate_svg(barcode_data, barcode_type)
                return jsonify({"success": True, "data": {"svg": svg_data}})
            else:
                image_data = barcode_gen.generate(barcode_data, barcode_type)
                response = make_response(image_data)
                response.headers["Content-Type"] = "image/png"
                response.headers["Content-Disposition"] = (
                    f"attachment; filename=barcode.png"
                )
                return response

        except Exception as e:
            logger.error(f"Barcode generation error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @barcode_bp.route("/qr", methods=["POST"])
    def generate_qr():
        data = request.get_json()

        qr_data = data.get("data")
        format_type = data.get("format", "base64")
        size = data.get("size", 200)

        if not qr_data:
            return jsonify({"success": False, "error": "Data is required"}), 400

        try:
            config = QRCodeConfig(size=size)

            if format_type == "base64":
                image_data = qr_gen.generate_base64(qr_data, config)
                return jsonify(
                    {
                        "success": True,
                        "data": {"image": f"data:image/png;base64,{image_data}"},
                    }
                )
            else:
                image_data = qr_gen.generate(qr_data, config)
                response = make_response(image_data)
                response.headers["Content-Type"] = "image/png"
                response.headers["Content-Disposition"] = (
                    f"attachment; filename=qrcode.png"
                )
                return response

        except Exception as e:
            logger.error(f"QR code generation error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @barcode_bp.route("/product/<int:product_id>/barcode", methods=["GET"])
    def get_product_barcode(product_id):
        from src.models.product import Product

        product = Product.query.get_or_404(product_id)

        format_type = request.args.get("format", "base64")
        barcode_type = request.args.get("type", "code128")

        # Use barcode or SKU
        barcode_data = product.barcode or product.sku or str(product.id)

        try:
            if format_type == "base64":
                image_data = barcode_gen.generate_base64(barcode_data, barcode_type)
                return jsonify(
                    {
                        "success": True,
                        "data": {
                            "product_id": product_id,
                            "barcode_data": barcode_data,
                            "image": f"data:image/png;base64,{image_data}",
                        },
                    }
                )
            else:
                image_data = barcode_gen.generate(barcode_data, barcode_type)
                response = make_response(image_data)
                response.headers["Content-Type"] = "image/png"
                response.headers["Content-Disposition"] = (
                    f"attachment; filename=product_{product_id}_barcode.png"
                )
                return response

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @barcode_bp.route("/product/<int:product_id>/qr", methods=["GET"])
    def get_product_qr(product_id):
        from src.models.product import Product

        product = Product.query.get_or_404(product_id)

        format_type = request.args.get("format", "base64")
        size = request.args.get("size", 200, type=int)

        try:
            image_data = qr_gen.generate_product_qr(
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                sku=product.sku,
            )

            if format_type == "base64":
                b64_data = base64.b64encode(image_data).decode("utf-8")
                return jsonify(
                    {
                        "success": True,
                        "data": {
                            "product_id": product_id,
                            "image": f"data:image/png;base64,{b64_data}",
                        },
                    }
                )
            else:
                response = make_response(image_data)
                response.headers["Content-Type"] = "image/png"
                response.headers["Content-Disposition"] = (
                    f"attachment; filename=product_{product_id}_qr.png"
                )
                return response

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    app.register_blueprint(barcode_bp)
    return barcode_bp


__all__ = [
    "BarcodeGenerator",
    "QRCodeGenerator",
    "BarcodeConfig",
    "QRCodeConfig",
    "init_barcode_routes",
]
