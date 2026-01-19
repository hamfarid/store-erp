from app import app, db
from models import User, SystemSettings
from werkzeug.security import generate_password_hash
import os


def fix_database():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        
        # Create default system settings
        settings = SystemSettings(
            system_name='Smart Agricultural System',
            language='ar',
            timezone='UTC',
            date_format='%Y-%m-%d',
            session_timeout=30,
            max_login_attempts=5,
            password_expiry=90,
            enable_2fa=False
        )
        
        try:
            db.session.add(admin)
            db.session.add(settings)
            db.session.commit()
            print("Database has been reset and initialized successfully!")
            print("\nAdmin login credentials:")
            print("Email: admin@example.com")
            print("Password: admin123")
            print("\nPlease change these credentials after logging in!")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            db.session.rollback()


if __name__ == '__main__':
    fix_database() 