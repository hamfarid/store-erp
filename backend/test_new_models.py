from src.database import db
from app import app
from src.models.enhanced_models import Brand, ProductImage, StockMovement
from src.models.inventory import Product

with app.app_context():
    print("✓ TESTING MODEL QUERIES\n")

    # Test Brand
    try:
        brands = Brand.query.all()
        print(f"✅ Brand.query.all() - Found {len(brands)} brands")
    except Exception as e:
        print(f"❌ Brand query failed: {e}")

    # Test ProductImage
    try:
        images = ProductImage.query.all()
        print(f"✅ ProductImage.query.all() - Found {len(images)} images")
    except Exception as e:
        print(f"❌ ProductImage query failed: {e}")

    # Test StockMovement
    try:
        movements = StockMovement.query.all()
        print(f"✅ StockMovement.query.all() - Found {len(movements)} movements")
    except Exception as e:
        print(f"❌ StockMovement query failed: {e}")

    # Test Product with brand_id
    try:
        products = Product.query.all()
        print(f"✅ Product.query.all() - Found {len(products)} products")
        if products:
            product = products[0]
            print(f"   - First product: {product.name}")
            print(f"   - Has brand relationship: {hasattr(product, 'brand')}")
    except Exception as e:
        print(f"❌ Product query failed: {e}")

    print("\n✓ TESTING MODEL CREATION\n")

    # Create a test brand
    try:
        brand = Brand(
            name="Test Brand",
            name_ar="علامة تجارية",
            description="Test brand description",
            is_active=True,
        )
        db.session.add(brand)
        db.session.commit()
        print(f"✅ Created brand: {brand.to_dict()}")

        # Clean up
        db.session.delete(brand)
        db.session.commit()
        print("✅ Cleaned up test brand")
    except Exception as e:
        print(f"❌ Brand creation failed: {e}")
        db.session.rollback()
