#!/usr/bin/env python3
"""Simple login test with detailed error output"""
import sys
sys.path.insert(0, 'D:\\APPS_AI\\store\\Store\\backend')

try:
    from src.database import db
    from src.models.user import User
    from app import create_app

    print("Creating app...")
    app = create_app()
    
    with app.app_context():
        print("Querying admin user...")
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Admin user not found!")
            sys.exit(1)
            
        print(f"✓ Found admin: {admin.username}, email: {admin.email}")
        print(f"  Hash: {admin.password_hash[:50]}...")
        print(f"  Active: {admin.is_active}")
        
        print("\nTesting password check...")
        result = admin.check_password('admin123')
        print(f"  check_password('admin123'): {result}")
        
        if result:
            print("\n✅ PASSWORD VERIFICATION WORKS!")
            print("\nNow testing full login flow...")
            
            # Test the login endpoint
            import json
            with app.test_client() as client:
                response = client.post(
                    '/api/auth/login',
                    data=json.dumps({'username': 'admin', 'password': 'admin123'}),
                    content_type='application/json'
                )
                print(f"\nLogin Response:")
                print(f"  Status: {response.status_code}")
                print(f"  Body: {json.dumps(response.get_json(), indent=2)}")
                
                if response.status_code == 200:
                    print("\n✅✅✅ LOGIN SUCCESSFUL!")
                else:
                    print(f"\n❌ Login failed with status {response.status_code}")
        else:
            print("\n❌ PASSWORD CHECK FAILED")
            
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
