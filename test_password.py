import sys
sys.path.insert(0, 'D:\\APPS_AI\\store\\Store\\backend')

from src.database import db
from src.models.user import User
from src.auth import AuthManager
from app import create_app

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print(f"✓ Admin user found")
        print(f"  Username: {admin.username}")
        print(f"  Email: {admin.email}")
        print(f"  Password hash (first 50 chars): {admin.password_hash[:50]}...")
        
        # Test different passwords
        passwords_to_test = [
            'admin123',
            'Admin123',
            'admin',
            '123456'
        ]
        
        print("\nTesting passwords:")
        for pwd in passwords_to_test:
            try:
                result = admin.check_password(pwd)
                print(f"  '{pwd}': {'✓ CORRECT' if result else '✗ Wrong'}")
            except Exception as e:
                print(f"  '{pwd}': ERROR - {e}")
    else:
        print("✗ Admin user not found!")
