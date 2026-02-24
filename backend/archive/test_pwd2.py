import sys
import bcrypt
sys.path.insert(0, 'D:\\APPS_AI\\store\\Store\\backend')

from src.database import db
from src.models.user import User
from app import create_app

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print("✓ Admin user found")
        print(f"  Username: {admin.username}")
        print(f"  Email: {admin.email}")
        print(f"  Password hash: {admin.password_hash[:60]}...")
        
        # Test with bcrypt directly
        passwords = ['admin123', 'Admin123', 'admin', '123456']
        
        print("\nTesting passwords with bcrypt:")
        for pwd in passwords:
            try:
                result = bcrypt.checkpw(pwd.encode('utf-8'), admin.password_hash.encode('utf-8'))
                print(f"  '{pwd}': {'✓ MATCH!' if result else '✗ No match'}")
            except Exception as e:
                print(f"  '{pwd}': ERROR - {e}")
    else:
        print("✗ Admin user not found!")
