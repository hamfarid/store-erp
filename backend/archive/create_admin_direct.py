#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct Admin User Creation Script
Creates admin user by directly accessing the database without loading all routes.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import only what we need
from flask import Flask  # noqa: E402
from flask_sqlalchemy import SQLAlchemy  # noqa: E402
from sqlalchemy.exc import SQLAlchemyError  # noqa: E402
import hashlib  # noqa: E402

# Create minimal Flask app
app = Flask(__name__)

# Get the correct database path
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'inventory.db')
db_dir = os.path.dirname(db_path)

# Create instance directory if it doesn't exist
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    print(f"✅ Created directory: {db_dir}")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

print(f"📁 Database path: {db_path}")

# Initialize database
db = SQLAlchemy(app)


# Define minimal models
class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    permissions = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_active = db.Column(db.Boolean, default=True)
    
    role = db.relationship('Role', backref='users')
    
    def set_password(self, password):
        """Set password using SHA-256 (same as the fallback in auth.py)"""
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        """Check password using SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password_hash


def create_admin():
    """Create admin user"""
    with app.app_context():
        try:
            # Check if admin exists
            existing_admin = User.query.filter_by(username='admin').first()
            if existing_admin:
                print("✅ Admin user already exists!")
                print(f"   Username: {existing_admin.username}")
                print(f"   Email: {existing_admin.email}")
                
                # Test password
                if existing_admin.check_password('admin123'):
                    print("✅ Password 'admin123' is correct!")
                else:
                    print("⚠️  Password 'admin123' does not match. Updating...")
                    existing_admin.set_password('admin123')
                    db.session.commit()
                    print("✅ Password updated to 'admin123'")
                
                return existing_admin
            
            # Create admin role
            admin_role = Role.query.filter_by(name='admin').first()
            if not admin_role:
                admin_role = Role()
                admin_role.name = 'admin'
                admin_role.description = 'System Administrator'
                admin_role.permissions = {'all': True}
                admin_role.is_active = True
                db.session.add(admin_role)
                db.session.flush()
                print("✅ Created admin role")
            
            # Create admin user using model helper
            admin_user: User = User.create_user(  # type: ignore[attr-defined]
                username='admin',
                password=os.getenv('ADMIN_PASSWORD', 'change_me'),
                email='admin@inventory.com',
                full_name='System Administrator',
                role_id=admin_role.id,
                is_active=True
            )
            
            print("✅ Admin user created successfully!")
            print("   Username: admin")
            print("   Password: admin123")
            print(f"   Email: {admin_user.email}")
            
            # Verify password works
            if admin_user.check_password('admin123'):
                print("✅ Password verification successful!")
            else:
                print("❌ Password verification failed!")
            
            return admin_user
        
        except (SQLAlchemyError, ValueError) as exc:
            print(f"❌ Error: {exc}")
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return None


if __name__ == '__main__':
    print("=" * 60)
    print("Creating Admin User")
    print("=" * 60)
    
    admin = create_admin()
    
    if admin:
        print("\n" + "=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nFrontend: http://localhost:5502")
        print("Backend: http://127.0.0.1:8000")
        print("=" * 60)
    else:
        print("\n❌ Failed to create admin user")
        sys.exit(1)

