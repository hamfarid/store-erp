#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copy products from products_advanced to products table
"""

from app import create_app
from src.database import db
from src.models.product_advanced import ProductAdvanced
from src.models.inventory import Product as SimpleProduct

app = create_app()

with app.app_context():
    print("\n📦 Copying products from products_advanced to products...")
    print("=" * 60)

    # Get all products from products_advanced
    advanced_products = ProductAdvanced.query.all()
    print(f"\n✅ Found {len(advanced_products)} products in products_advanced table")

    # Clear existing products in simple table
    SimpleProduct.query.delete()
    db.session.commit()
    print(f"✅ Cleared products table")

    # Copy each product
    copied_count = 0
    for adv_prod in advanced_products:
        try:
            # Create simple product with matching fields
            simple_prod = SimpleProduct(
                name=adv_prod.name,
                category_id=adv_prod.category_id,
                is_active=adv_prod.is_active,
            )

            # Copy optional fields if they exist in both models
            if hasattr(adv_prod, "sku") and hasattr(SimpleProduct, "sku"):
                simple_prod.sku = adv_prod.sku

            if hasattr(adv_prod, "barcode") and hasattr(SimpleProduct, "barcode"):
                simple_prod.barcode = adv_prod.barcode

            if hasattr(adv_prod, "description") and hasattr(
                SimpleProduct, "description"
            ):
                simple_prod.description = adv_prod.description

            if hasattr(adv_prod, "cost_price") and hasattr(SimpleProduct, "cost_price"):
                simple_prod.cost_price = adv_prod.cost_price

            if hasattr(adv_prod, "sale_price") and hasattr(SimpleProduct, "sale_price"):
                simple_prod.sale_price = adv_prod.sale_price

            if hasattr(adv_prod, "current_stock") and hasattr(
                SimpleProduct, "current_stock"
            ):
                simple_prod.current_stock = adv_prod.current_stock

            if hasattr(adv_prod, "min_quantity") and hasattr(
                SimpleProduct, "min_quantity"
            ):
                simple_prod.min_quantity = adv_prod.min_quantity

            if hasattr(adv_prod, "max_quantity") and hasattr(
                SimpleProduct, "max_quantity"
            ):
                simple_prod.max_quantity = adv_prod.max_quantity

            db.session.add(simple_prod)
            copied_count += 1
            print(f"  ✓ Copied: {adv_prod.name}")

        except Exception as e:
            print(f"  ✗ Failed to copy {adv_prod.name}: {e}")

    # Commit all changes
    db.session.commit()

    print(f"\n✅ Successfully copied {copied_count} products to products table")

    # Verify
    simple_count = SimpleProduct.query.count()
    print(f"✅ Verification: products table now has {simple_count} products")

    print("\n" + "=" * 60)
