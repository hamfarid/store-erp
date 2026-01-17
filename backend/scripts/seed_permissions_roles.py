"""
Seed Permissions and Roles
إنشاء الأذونات والأدوار الافتراضية
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database import db
from flask import Flask
from utils.permission_helper import seed_permissions, seed_roles

def main():
    """تشغيل seed للأذونات والأدوار"""
    
    # إنشاء Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        print("🔧 بدء إنشاء الأذونات والأدوار...")
        
        # Seed permissions
        print("\n📝 إنشاء الأذونات...")
        perms_count = seed_permissions()
        print(f"✅ تم إنشاء {perms_count} إذن")
        
        # Seed roles
        print("\n👥 إنشاء الأدوار...")
        roles_count = seed_roles()
        print(f"✅ تم إنشاء {roles_count} دور")
        
        print("\n🎉 تم الانتهاء بنجاح!")
        print(f"📊 الإجمالي: {perms_count} إذن، {roles_count} دور")

if __name__ == "__main__":
    main()
