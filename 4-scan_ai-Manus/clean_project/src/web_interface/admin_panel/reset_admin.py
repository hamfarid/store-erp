from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def reset_admin():
    with app.app_context():
        # Delete existing admin user if exists
        User.query.filter_by(role='admin').delete()
        
        # Create new admin user
        admin = User(
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            role='admin',
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("Admin credentials have been reset!")
        print("Email: admin@example.com")
        print("Password: admin123")
        print("\nPlease change these credentials after logging in!")

if __name__ == '__main__':
    reset_admin() 