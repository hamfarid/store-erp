#!/usr/bin/env python3
"""
File: create_admin_user.py
Script to create an admin user for Gaara ERP system

SECURITY FIX (2025-12-01): Removed hardcoded credentials
Per GLOBAL_PROFESSIONAL_CORE_PROMPT - Zero Tolerance Constraints

Usage: 
    python create_admin_user.py
    
Environment Variables:
    ADMIN_USERNAME: Admin username (default: admin)
    ADMIN_EMAIL: Admin email (default: admin@gaara-erp.com)
    ADMIN_PASSWORD: Admin password (REQUIRED - no default for security)
"""

import os
import sys
import secrets
import string
import django

# Add the project directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'gaara_erp'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model
from django.db import IntegrityError


def generate_secure_password(length: int = 16) -> str:
    """Generate a secure random password.
    
    Args:
        length: Password length (default: 16)
        
    Returns:
        str: Secure random password
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Ensure at least one of each type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    # Fill the rest
    password += [secrets.choice(alphabet) for _ in range(length - 4)]
    # Shuffle
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


def create_admin_user():
    """Create admin user from environment variables or generate secure credentials."""
    User = get_user_model()
    
    # Get credentials from environment variables (SECURITY: no hardcoded defaults for password)
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@gaara-erp.com')
    password = os.environ.get('ADMIN_PASSWORD')
    
    # If no password provided, generate a secure one
    generated_password = False
    if not password:
        password = generate_secure_password()
        generated_password = True
        print("⚠️  No ADMIN_PASSWORD environment variable set.")
        print("🔐 Generating secure random password...")
    
    try:
        # Check if admin user already exists
        if User.objects.filter(username=username).exists():
            print(f"✅ Admin user '{username}' already exists.")
            return
            
        if User.objects.filter(email=email).exists():
            print(f"✅ User with email '{email}' already exists.")
            return
        
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print(f"✅ Admin user '{username}' created successfully!")
        print(f"📧 Email: {email}")
        
        if generated_password:
            print(f"🔑 Generated Password: {password}")
            print("⚠️  IMPORTANT: Save this password securely! It cannot be recovered.")
            print("⚠️  Consider setting ADMIN_PASSWORD environment variable for consistent deployments.")
        else:
            print("🔑 Password: (set via ADMIN_PASSWORD environment variable)")
            
        print("⚠️  Please change the password after first login for security.")
        
    except IntegrityError as e:
        print(f"❌ Error creating admin user: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == '__main__':
    create_admin_user()
