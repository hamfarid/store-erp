import sys
sys.path.insert(0, 'backend')
from app import create_app
app = create_app()
from sqlalchemy.orm import class_mapper
with app.app_context():
    from src.models.product_unified import Product
    from src.models.category import Category
    pm = class_mapper(Product)
    cm = class_mapper(Category)
    print('Product mapper:', pm)
    print('Category mapper:', cm)
    rel = [r for r in pm.relationships if r.key=='category'][0]
    print('Product.category.mapper:', rel.mapper)
    rel2 = [r for r in cm.relationships if r.key=='products'][0]
    print('Category.products.mapper:', rel2.mapper)
