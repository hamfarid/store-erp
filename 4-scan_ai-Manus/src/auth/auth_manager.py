#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Authentication and Authorization Module for Agricultural AI System.
Provides comprehensive user management with role-based access control.
"""

import os
import sys
import json
import logging
import datetime
import hashlib
import secrets
import jwt
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('auth_manager')


class AuthManager:
    """
    Enhanced Authentication and Authorization Manager.
    Provides user management, authentication, and role-based access control.
    """
    
    def __init__(self, config_path: str, audit_manager=None):
        """
        Initialize the Authentication Manager.
        
        Args:
            config_path: Path to configuration file
            audit_manager: Audit manager instance for logging actions
        """
        self.config_path = config_path
        self.audit_manager = audit_manager
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize data directories
        self._init_directories()
        
        # Load users, roles, organizations, and countries
        self.users = self._load_users()
        self.roles = self._load_roles()
        self.organizations = self._load_organizations()
        self.countries = self._load_countries()
        
        # JWT secret for token generation
        self.jwt_secret = self.config['auth'].get('jwt_secret', secrets.token_hex(32))
        if 'jwt_secret' not in self.config['auth']:
            self.config['auth']['jwt_secret'] = self.jwt_secret
            self._save_config()
        
        logger.info("Authentication Manager initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Get auth specific config
            if 'auth' not in config:
                config['auth'] = {
                    'data_dir': os.path.join(os.path.dirname(self.config_path), '../data/auth'),
                    'users_file': os.path.join(os.path.dirname(self.config_path), '../data/auth/users.json'),
                    'roles_dir': os.path.join(os.path.dirname(self.config_path), '../data/auth/roles'),
                    'organizations_file': os.path.join(os.path.dirname(self.config_path), '../data/auth/organizations.json'),
                    'countries_file': os.path.join(os.path.dirname(self.config_path), '../data/auth/countries.json'),
                    'token_expiry': 86400,  # 24 hours in seconds
                    'password_min_length': 8,
                    'password_require_uppercase': True,
                    'password_require_lowercase': True,
                    'password_require_number': True,
                    'password_require_special': True,
                    'max_login_attempts': 5,
                    'lockout_duration': 1800,  # 30 minutes in seconds
                    'default_roles': {
                        'admin': {
                            'name': 'Administrator',
                            'description': 'Full system access',
                            'permissions': ['*']
                        },
                        'support_manager': {
                            'name': 'Support Manager',
                            'description': 'Manages support operations',
                            'permissions': [
                                'view:*',
                                'edit:support_*',
                                'add:support_*',
                                'delete:support_*',
                                'view:reports',
                                'generate:reports'
                            ]
                        },
                        'development_manager': {
                            'name': 'Development Manager',
                            'description': 'Manages development operations',
                            'permissions': [
                                'view:*',
                                'edit:development_*',
                                'add:development_*',
                                'delete:development_*',
                                'view:reports',
                                'generate:reports'
                            ]
                        },
                        'support_engineer': {
                            'name': 'Support Engineer',
                            'description': 'Provides technical support',
                            'permissions': [
                                'view:support_*',
                                'edit:support_tickets',
                                'add:support_tickets',
                                'view:reports'
                            ]
                        },
                        'development_engineer': {
                            'name': 'Development Engineer',
                            'description': 'Develops system components',
                            'permissions': [
                                'view:development_*',
                                'edit:development_tasks',
                                'add:development_tasks',
                                'view:reports'
                            ]
                        },
                        'user': {
                            'name': 'Regular User',
                            'description': 'Basic system access',
                            'permissions': [
                                'view:public_*',
                                'add:user_data',
                                'edit:user_data',
                                'delete:user_data'
                            ]
                        }
                    }
                }
                
                # Save updated config
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
            
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Return default configuration
            return {
                'auth': {
                    'data_dir': os.path.join(os.path.dirname(self.config_path), '../data/auth'),
                    'users_file': os.path.join(os.path.dirname(self.config_path), '../data/auth/users.json'),
                    'roles_dir': os.path.join(os.path.dirname(self.config_path), '../data/auth/roles'),
                    'organizations_file': os.path.join(os.path.dirname(self.config_path), '../data/auth/organizations.json'),
                    'countries_file': os.path.join(os.path.dirname(self.config_path), '../data/auth/countries.json'),
                    'token_expiry': 86400,  # 24 hours in seconds
                    'password_min_length': 8,
                    'password_require_uppercase': True,
                    'password_require_lowercase': True,
                    'password_require_number': True,
                    'password_require_special': True,
                    'max_login_attempts': 5,
                    'lockout_duration': 1800,  # 30 minutes in seconds
                    'jwt_secret': secrets.token_hex(32),
                    'default_roles': {
                        'admin': {
                            'name': 'Administrator',
                            'description': 'Full system access',
                            'permissions': ['*']
                        },
                        'support_manager': {
                            'name': 'Support Manager',
                            'description': 'Manages support operations',
                            'permissions': [
                                'view:*',
                                'edit:support_*',
                                'add:support_*',
                                'delete:support_*',
                                'view:reports',
                                'generate:reports'
                            ]
                        },
                        'development_manager': {
                            'name': 'Development Manager',
                            'description': 'Manages development operations',
                            'permissions': [
                                'view:*',
                                'edit:development_*',
                                'add:development_*',
                                'delete:development_*',
                                'view:reports',
                                'generate:reports'
                            ]
                        },
                        'support_engineer': {
                            'name': 'Support Engineer',
                            'description': 'Provides technical support',
                            'permissions': [
                                'view:support_*',
                                'edit:support_tickets',
                                'add:support_tickets',
                                'view:reports'
                            ]
                        },
                        'development_engineer': {
                            'name': 'Development Engineer',
                            'description': 'Develops system components',
                            'permissions': [
                                'view:development_*',
                                'edit:development_tasks',
                                'add:development_tasks',
                                'view:reports'
                            ]
                        },
                        'user': {
                            'name': 'Regular User',
                            'description': 'Basic system access',
                            'permissions': [
                                'view:public_*',
                                'add:user_data',
                                'edit:user_data',
                                'delete:user_data'
                            ]
                        }
                    }
                }
            }
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            config['auth'] = self.config['auth']
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def _init_directories(self):
        """Initialize required directories."""
        # Create main data directories
        os.makedirs(self.config['auth']['data_dir'], exist_ok=True)
        os.makedirs(self.config['auth']['roles_dir'], exist_ok=True)
    
    def _load_users(self) -> Dict[str, Any]:
        """
        Load users from file.
        If file doesn't exist, create it with default admin user.
        
        Returns:
            Dictionary with users
        """
        users_file = self.config['auth']['users_file']
        
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading users: {e}")
        
        # Create default admin user
        default_users = {
            'admin': {
                'username': 'admin',
                'password_hash': self._hash_password('admin123'),  # Default password, should be changed
                'email': 'admin@example.com',
                'full_name': 'System Administrator',
                'role': 'admin',
                'organization': 'system',
                'country': 'global',
                'created_at': datetime.datetime.now().isoformat(),
                'last_login': None,
                'login_attempts': 0,
                'locked_until': None,
                'active': True,
                'api_key': secrets.token_hex(16)
            }
        }
        
        # Save default users
        try:
            os.makedirs(os.path.dirname(users_file), exist_ok=True)
            with open(users_file, 'w', encoding='utf-8') as f:
                json.dump(default_users, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving default users: {e}")
        
        return default_users
    
    def _save_users(self):
        """Save users to file."""
        try:
            with open(self.config['auth']['users_file'], 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving users: {e}")
    
    def _load_roles(self) -> Dict[str, Any]:
        """
        Load roles from files.
        If files don't exist, create them with default roles.
        
        Returns:
            Dictionary with roles
        """
        roles = {}
        roles_dir = self.config['auth']['roles_dir']
        
        # Check if roles directory exists and has files
        if os.path.exists(roles_dir) and os.listdir(roles_dir):
            # Load each role file
            for filename in os.listdir(roles_dir):
                if filename.endswith('.json'):
                    role_id = os.path.splitext(filename)[0]
                    role_file = os.path.join(roles_dir, filename)
                    
                    try:
                        with open(role_file, 'r', encoding='utf-8') as f:
                            roles[role_id] = json.load(f)
                    except Exception as e:
                        logger.error(f"Error loading role {role_id}: {e}")
        else:
            # Create default roles
            default_roles = self.config['auth']['default_roles']
            
            # Save each role to a separate file
            for role_id, role_data in default_roles.items():
                role_file = os.path.join(roles_dir, f"{role_id}.json")
                
                try:
                    os.makedirs(os.path.dirname(role_file), exist_ok=True)
                    with open(role_file, 'w', encoding='utf-8') as f:
                        json.dump(role_data, f, indent=2)
                except Exception as e:
                    logger.error(f"Error saving default role {role_id}: {e}")
                
                roles[role_id] = role_data
        
        return roles
    
    def _save_role(self, role_id: str, role_data: Dict[str, Any]):
        """
        Save role to file.
        
        Args:
            role_id: Role identifier
            role_data: Role data
        """
        try:
            role_file = os.path.join(self.config['auth']['roles_dir'], f"{role_id}.json")
            with open(role_file, 'w', encoding='utf-8') as f:
                json.dump(role_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving role {role_id}: {e}")
    
    def _load_organizations(self) -> Dict[str, Any]:
        """
        Load organizations from file.
        If file doesn't exist, create it with default organization.
        
        Returns:
            Dictionary with organizations
        """
        organizations_file = self.config['auth']['organizations_file']
        
        if os.path.exists(organizations_file):
            try:
                with open(organizations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading organizations: {e}")
        
        # Create default organization
        default_organizations = {
            'system': {
                'name': 'System',
                'description': 'System organization',
                'country': 'global',
                'created_at': datetime.datetime.now().isoformat(),
                'active': True
            }
        }
        
        # Save default organizations
        try:
            os.makedirs(os.path.dirname(organizations_file), exist_ok=True)
            with open(organizations_file, 'w', encoding='utf-8') as f:
                json.dump(default_organizations, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving default organizations: {e}")
        
        return default_organizations
    
    def _save_organizations(self):
        """Save organizations to file."""
        try:
            with open(self.config['auth']['organizations_file'], 'w', encoding='utf-8') as f:
                json.dump(self.organizations, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving organizations: {e}")
    
    def _load_countries(self) -> Dict[str, Any]:
        """
        Load countries from file.
        If file doesn't exist, create it with default countries.
        
        Returns:
            Dictionary with countries
        """
        countries_file = self.config['auth']['countries_file']
        
        if os.path.exists(countries_file):
            try:
                with open(countries_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading countries: {e}")
        
        # Create default countries
        default_countries = {
            'global': {
                'name': 'Global',
                'code': 'GL',
                'active': True
            },
            'egypt': {
                'name': 'Egypt',
                'code': 'EG',
                'active': True
            },
            'saudi_arabia': {
                'name': 'Saudi Arabia',
                'code': 'SA',
                'active': True
            },
            'united_arab_emirates': {
                'name': 'United Arab Emirates',
                'code': 'AE',
                'active': True
            },
            'kuwait': {
                'name': 'Kuwait',
                'code': 'KW',
                'active': True
            },
            'qatar': {
                'name': 'Qatar',
                'code': 'QA',
                'active': True
            },
            'bahrain': {
                'name': 'Bahrain',
                'code': 'BH',
                'active': True
            },
            'oman': {
                'name': 'Oman',
                'code': 'OM',
                'active': True
            },
            'jordan': {
                'name': 'Jordan',
                'code': 'JO',
                'active': True
            },
            'lebanon': {
                'name': 'Lebanon',
                'code': 'LB',
                'active': True
            },
            'iraq': {
                'name': 'Iraq',
                'code': 'IQ',
                'active': True
            },
            'syria': {
                'name': 'Syria',
                'code': 'SY',
                'active': True
            },
            'palestine': {
                'name': 'Palestine',
                'code': 'PS',
                'active': True
            },
            'yemen': {
                'name': 'Yemen',
                'code': 'YE',
                'active': True
            },
            'libya': {
                'name': 'Libya',
                'code': 'LY',
                'active': True
            },
            'tunisia': {
                'name': 'Tunisia',
                'code': 'TN',
                'active': True
            },
            'algeria': {
                'name': 'Algeria',
                'code': 'DZ',
                'active': True
            },
            'morocco': {
                'name': 'Morocco',
                'code': 'MA',
                'active': True
            },
            'sudan': {
                'name': 'Sudan',
                'code': 'SD',
                'active': True
            },
            'somalia': {
                'name': 'Somalia',
                'code': 'SO',
                'active': True
            }
        }
        
        # Save default countries
        try:
            os.makedirs(os.path.dirname(countries_file), exist_ok=True)
            with open(countries_file, 'w', encoding='utf-8') as f:
                json.dump(default_countries, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving default countries: {e}")
        
        return default_countries
    
    def _save_countries(self):
        """Save countries to file."""
        try:
            with open(self.config['auth']['countries_file'], 'w', encoding='utf-8') as f:
                json.dump(self.countries, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving countries: {e}")
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password: Password to hash
            
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Password to verify
            password_hash: Hash to verify against
            
        Returns:
            True if password matches hash, False otherwise
        """
        return self._hash_password(password) == password_hash
    
    def _validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check length
        if len(password) < self.config['auth']['password_min_length']:
            return False, f"Password must be at least {self.config['auth']['password_min_length']} characters long"
        
        # Check for uppercase letters
        if self.config['auth']['password_require_uppercase'] and not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for lowercase letters
        if self.config['auth']['password_require_lowercase'] and not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for numbers
        if self.config['auth']['password_require_number'] and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        # Check for special characters
        if self.config['auth']['password_require_special'] and not any(not c.isalnum() for c in password):
            return False, "Password must contain at least one special character"
        
        return True, ""
    
    def _generate_token(self, user_data: Dict[str, Any]) -> str:
        """
        Generate a JWT token for a user.
        
        Args:
            user_data: User data
            
        Returns:
            JWT token
        """
        payload = {
            'sub': user_data['username'],
            'role': user_data['role'],
            'organization': user_data['organization'],
            'country': user_data['country'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.config['auth']['token_expiry'])
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def _verify_token(self, token: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify a JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Tuple of (is_valid, payload)
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, {'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return False, {'error': 'Invalid token'}
    
    def register_user(self, username: str, password: str, email: str, full_name: str,
                     role: str = 'user', organization: str = 'system', country: str = 'global',
                     admin_user: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            username: Username
            password: Password
            email: Email address
            full_name: Full name
            role: Role (default: user)
            organization: Organization (default: system)
            country: Country (default: global)
            admin_user: Admin user data for authorization (required for non-user roles)
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if username already exists
            if username in self.users:
                return {
                    'success': False,
                    'error': f"Username '{username}' already exists"
                }
            
            # Check if role exists
            if role not in self.roles:
                return {
                    'success': False,
                    'error': f"Role '{role}' does not exist"
                }
            
            # Check if organization exists
            if organization not in self.organizations:
                return {
                    'success': False,
                    'error': f"Organization '{organization}' does not exist"
                }
            
            # Check if country exists
            if country not in self.countries:
                return {
                    'success': False,
                    'error': f"Country '{country}' does not exist"
                }
            
            # Check if admin authorization is required
            if role != 'user' and not admin_user:
                return {
                    'success': False,
                    'error': "Admin authorization required for non-user roles"
                }
            
            # Verify admin authorization if provided
            if admin_user:
                # Check if admin user exists
                if admin_user['username'] not in self.users:
                    return {
                        'success': False,
                        'error': f"Admin user '{admin_user['username']}' does not exist"
                    }
                
                # Check if admin user has admin role
                if self.users[admin_user['username']]['role'] != 'admin':
                    return {
                        'success': False,
                        'error': f"User '{admin_user['username']}' is not an admin"
                    }
                
                # Verify admin password
                if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                    return {
                        'success': False,
                        'error': "Invalid admin password"
                    }
            
            # Validate password strength
            is_valid, error_message = self._validate_password_strength(password)
            if not is_valid:
                return {
                    'success': False,
                    'error': error_message
                }
            
            # Create user
            user_data = {
                'username': username,
                'password_hash': self._hash_password(password),
                'email': email,
                'full_name': full_name,
                'role': role,
                'organization': organization,
                'country': country,
                'created_at': datetime.datetime.now().isoformat(),
                'last_login': None,
                'login_attempts': 0,
                'locked_until': None,
                'active': True,
                'api_key': secrets.token_hex(16)
            }
            
            # Add user
            self.users[username] = user_data
            
            # Save users
            self._save_users()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="register_user",
                    component="auth_manager",
                    user_info=admin_user or {'username': 'system'},
                    details={
                        "username": username,
                        "role": role,
                        "organization": organization,
                        "country": country
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"User '{username}' registered successfully",
                'api_key': user_data['api_key']
            }
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="register_user",
                    component="auth_manager",
                    user_info=admin_user or {'username': 'system'},
                    details={
                        "username": username,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error registering user: {str(e)}"
            }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login a user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if username exists
            if username not in self.users:
                return {
                    'success': False,
                    'error': "Invalid username or password"
                }
            
            user_data = self.users[username]
            
            # Check if user is active
            if not user_data.get('active', True):
                return {
                    'success': False,
                    'error': "Account is inactive"
                }
            
            # Check if user is locked
            if user_data.get('locked_until'):
                locked_until = datetime.datetime.fromisoformat(user_data['locked_until'])
                if locked_until > datetime.datetime.now():
                    return {
                        'success': False,
                        'error': f"Account is locked until {locked_until.strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                else:
                    # Reset login attempts if lock has expired
                    user_data['login_attempts'] = 0
                    user_data['locked_until'] = None
            
            # Verify password
            if not self._verify_password(password, user_data['password_hash']):
                # Increment login attempts
                user_data['login_attempts'] = user_data.get('login_attempts', 0) + 1
                
                # Check if max login attempts reached
                if user_data['login_attempts'] >= self.config['auth']['max_login_attempts']:
                    # Lock account
                    locked_until = datetime.datetime.now() + datetime.timedelta(seconds=self.config['auth']['lockout_duration'])
                    user_data['locked_until'] = locked_until.isoformat()
                    
                    # Save users
                    self._save_users()
                    
                    # Log the action
                    if self.audit_manager:
                        self.audit_manager.log_action(
                            action_type="AUTH",
                            action="login_failed_locked",
                            component="auth_manager",
                            user_info={'username': username},
                            details={
                                "login_attempts": user_data['login_attempts'],
                                "locked_until": user_data['locked_until']
                            },
                            status="error"
                        )
                    
                    return {
                        'success': False,
                        'error': f"Account is locked until {locked_until.strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                
                # Save users
                self._save_users()
                
                # Log the action
                if self.audit_manager:
                    self.audit_manager.log_action(
                        action_type="AUTH",
                        action="login_failed",
                        component="auth_manager",
                        user_info={'username': username},
                        details={
                            "login_attempts": user_data['login_attempts']
                        },
                        status="error"
                    )
                
                return {
                    'success': False,
                    'error': "Invalid username or password"
                }
            
            # Reset login attempts
            user_data['login_attempts'] = 0
            user_data['locked_until'] = None
            
            # Update last login
            user_data['last_login'] = datetime.datetime.now().isoformat()
            
            # Save users
            self._save_users()
            
            # Generate token
            token = self._generate_token(user_data)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="login",
                    component="auth_manager",
                    user_info={'username': username},
                    details={},
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"User '{username}' logged in successfully",
                'token': token,
                'user': {
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'full_name': user_data['full_name'],
                    'role': user_data['role'],
                    'organization': user_data['organization'],
                    'country': user_data['country'],
                    'api_key': user_data['api_key']
                }
            }
            
        except Exception as e:
            logger.error(f"Error logging in: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="login",
                    component="auth_manager",
                    user_info={'username': username},
                    details={
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error logging in: {str(e)}"
            }
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify a JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Dictionary with operation result
        """
        try:
            is_valid, payload = self._verify_token(token)
            
            if not is_valid:
                return {
                    'success': False,
                    'error': payload['error']
                }
            
            # Check if user exists
            if payload['sub'] not in self.users:
                return {
                    'success': False,
                    'error': "User not found"
                }
            
            user_data = self.users[payload['sub']]
            
            # Check if user is active
            if not user_data.get('active', True):
                return {
                    'success': False,
                    'error': "Account is inactive"
                }
            
            return {
                'success': True,
                'user': {
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'full_name': user_data['full_name'],
                    'role': user_data['role'],
                    'organization': user_data['organization'],
                    'country': user_data['country']
                }
            }
            
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return {
                'success': False,
                'error': f"Error verifying token: {str(e)}"
            }
    
    def verify_api_key(self, api_key: str) -> Dict[str, Any]:
        """
        Verify an API key.
        
        Args:
            api_key: API key
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Find user with API key
            for username, user_data in self.users.items():
                if user_data.get('api_key') == api_key:
                    # Check if user is active
                    if not user_data.get('active', True):
                        return {
                            'success': False,
                            'error': "Account is inactive"
                        }
                    
                    return {
                        'success': True,
                        'user': {
                            'username': user_data['username'],
                            'email': user_data['email'],
                            'full_name': user_data['full_name'],
                            'role': user_data['role'],
                            'organization': user_data['organization'],
                            'country': user_data['country']
                        }
                    }
            
            return {
                'success': False,
                'error': "Invalid API key"
            }
            
        except Exception as e:
            logger.error(f"Error verifying API key: {e}")
            return {
                'success': False,
                'error': f"Error verifying API key: {str(e)}"
            }
    
    def change_password(self, username: str, current_password: str, new_password: str) -> Dict[str, Any]:
        """
        Change a user's password.
        
        Args:
            username: Username
            current_password: Current password
            new_password: New password
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if username exists
            if username not in self.users:
                return {
                    'success': False,
                    'error': "User not found"
                }
            
            user_data = self.users[username]
            
            # Verify current password
            if not self._verify_password(current_password, user_data['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid current password"
                }
            
            # Validate new password strength
            is_valid, error_message = self._validate_password_strength(new_password)
            if not is_valid:
                return {
                    'success': False,
                    'error': error_message
                }
            
            # Update password
            user_data['password_hash'] = self._hash_password(new_password)
            
            # Save users
            self._save_users()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="change_password",
                    component="auth_manager",
                    user_info={'username': username},
                    details={},
                    status="success"
                )
            
            return {
                'success': True,
                'message': "Password changed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="change_password",
                    component="auth_manager",
                    user_info={'username': username},
                    details={
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error changing password: {str(e)}"
            }
    
    def reset_api_key(self, username: str, admin_user: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Reset a user's API key.
        
        Args:
            username: Username
            admin_user: Admin user data for authorization (required if not resetting own API key)
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if username exists
            if username not in self.users:
                return {
                    'success': False,
                    'error': "User not found"
                }
            
            # Check if admin authorization is required
            if admin_user and admin_user['username'] != username:
                # Check if admin user exists
                if admin_user['username'] not in self.users:
                    return {
                        'success': False,
                        'error': f"Admin user '{admin_user['username']}' does not exist"
                    }
                
                # Check if admin user has admin role
                if self.users[admin_user['username']]['role'] != 'admin':
                    return {
                        'success': False,
                        'error': f"User '{admin_user['username']}' is not an admin"
                    }
                
                # Verify admin password
                if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                    return {
                        'success': False,
                        'error': "Invalid admin password"
                    }
            
            # Generate new API key
            new_api_key = secrets.token_hex(16)
            
            # Update API key
            self.users[username]['api_key'] = new_api_key
            
            # Save users
            self._save_users()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="reset_api_key",
                    component="auth_manager",
                    user_info=admin_user or {'username': username},
                    details={
                        "target_user": username
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"API key for user '{username}' reset successfully",
                'api_key': new_api_key
            }
            
        except Exception as e:
            logger.error(f"Error resetting API key: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="reset_api_key",
                    component="auth_manager",
                    user_info=admin_user or {'username': username},
                    details={
                        "target_user": username,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error resetting API key: {str(e)}"
            }
    
    def update_user(self, username: str, user_data: Dict[str, Any], 
                   admin_user: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update a user's data.
        
        Args:
            username: Username
            user_data: User data to update
            admin_user: Admin user data for authorization (required if not updating own data)
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if username exists
            if username not in self.users:
                return {
                    'success': False,
                    'error': "User not found"
                }
            
            current_user_data = self.users[username]
            
            # Check if admin authorization is required
            if admin_user and admin_user['username'] != username:
                # Check if admin user exists
                if admin_user['username'] not in self.users:
                    return {
                        'success': False,
                        'error': f"Admin user '{admin_user['username']}' does not exist"
                    }
                
                # Check if admin user has admin role
                if self.users[admin_user['username']]['role'] != 'admin':
                    return {
                        'success': False,
                        'error': f"User '{admin_user['username']}' is not an admin"
                    }
                
                # Verify admin password
                if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                    return {
                        'success': False,
                        'error': "Invalid admin password"
                    }
            else:
                # Regular users can only update certain fields
                allowed_fields = ['email', 'full_name']
                for field in user_data:
                    if field not in allowed_fields:
                        return {
                            'success': False,
                            'error': f"Regular users cannot update field '{field}'"
                        }
            
            # Update user data
            for field, value in user_data.items():
                # Skip password field (use change_password method instead)
                if field == 'password' or field == 'password_hash':
                    continue
                
                # Skip username field (cannot be changed)
                if field == 'username':
                    continue
                
                # Validate role
                if field == 'role' and value not in self.roles:
                    return {
                        'success': False,
                        'error': f"Role '{value}' does not exist"
                    }
                
                # Validate organization
                if field == 'organization' and value not in self.organizations:
                    return {
                        'success': False,
                        'error': f"Organization '{value}' does not exist"
                    }
                
                # Validate country
                if field == 'country' and value not in self.countries:
                    return {
                        'success': False,
                        'error': f"Country '{value}' does not exist"
                    }
                
                # Update field
                current_user_data[field] = value
            
            # Save users
            self._save_users()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="update_user",
                    component="auth_manager",
                    user_info=admin_user or {'username': username},
                    details={
                        "target_user": username,
                        "updated_fields": list(user_data.keys())
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"User '{username}' updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="update_user",
                    component="auth_manager",
                    user_info=admin_user or {'username': username},
                    details={
                        "target_user": username,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error updating user: {str(e)}"
            }
    
    def deactivate_user(self, username: str, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deactivate a user.
        
        Args:
            username: Username
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if username exists
            if username not in self.users:
                return {
                    'success': False,
                    'error': "User not found"
                }
            
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Deactivate user
            self.users[username]['active'] = False
            
            # Save users
            self._save_users()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="deactivate_user",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "target_user": username
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"User '{username}' deactivated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deactivating user: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="deactivate_user",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "target_user": username,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error deactivating user: {str(e)}"
            }
    
    def activate_user(self, username: str, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Activate a user.
        
        Args:
            username: Username
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if username exists
            if username not in self.users:
                return {
                    'success': False,
                    'error': "User not found"
                }
            
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Activate user
            self.users[username]['active'] = True
            
            # Reset login attempts and lock
            self.users[username]['login_attempts'] = 0
            self.users[username]['locked_until'] = None
            
            # Save users
            self._save_users()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="activate_user",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "target_user": username
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"User '{username}' activated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error activating user: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="activate_user",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "target_user": username,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error activating user: {str(e)}"
            }
    
    def list_users(self, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all users.
        
        Args:
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Prepare user list (exclude password hashes)
            user_list = []
            for username, user_data in self.users.items():
                user_info = user_data.copy()
                user_info.pop('password_hash', None)
                user_list.append(user_info)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="list_users",
                    component="auth_manager",
                    user_info=admin_user,
                    details={},
                    status="success"
                )
            
            return {
                'success': True,
                'users': user_list
            }
            
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="list_users",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error listing users: {str(e)}"
            }
    
    def create_role(self, role_id: str, name: str, description: str, 
                   permissions: List[str], admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new role.
        
        Args:
            role_id: Role identifier
            name: Role name
            description: Role description
            permissions: List of permissions
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if role already exists
            if role_id in self.roles:
                return {
                    'success': False,
                    'error': f"Role '{role_id}' already exists"
                }
            
            # Create role
            role_data = {
                'name': name,
                'description': description,
                'permissions': permissions,
                'created_at': datetime.datetime.now().isoformat(),
                'created_by': admin_user['username']
            }
            
            # Add role
            self.roles[role_id] = role_data
            
            # Save role
            self._save_role(role_id, role_data)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="create_role",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "role_id": role_id,
                        "name": name
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Role '{role_id}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating role: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="create_role",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "role_id": role_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error creating role: {str(e)}"
            }
    
    def update_role(self, role_id: str, role_data: Dict[str, Any], 
                   admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a role.
        
        Args:
            role_id: Role identifier
            role_data: Role data to update
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if role exists
            if role_id not in self.roles:
                return {
                    'success': False,
                    'error': f"Role '{role_id}' does not exist"
                }
            
            current_role_data = self.roles[role_id]
            
            # Update role data
            for field, value in role_data.items():
                # Skip created_at and created_by fields
                if field in ['created_at', 'created_by']:
                    continue
                
                # Update field
                current_role_data[field] = value
            
            # Add updated_at and updated_by fields
            current_role_data['updated_at'] = datetime.datetime.now().isoformat()
            current_role_data['updated_by'] = admin_user['username']
            
            # Save role
            self._save_role(role_id, current_role_data)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="update_role",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "role_id": role_id,
                        "updated_fields": list(role_data.keys())
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Role '{role_id}' updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating role: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="update_role",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "role_id": role_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error updating role: {str(e)}"
            }
    
    def delete_role(self, role_id: str, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a role.
        
        Args:
            role_id: Role identifier
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if role exists
            if role_id not in self.roles:
                return {
                    'success': False,
                    'error': f"Role '{role_id}' does not exist"
                }
            
            # Check if role is in use
            for username, user_data in self.users.items():
                if user_data.get('role') == role_id:
                    return {
                        'success': False,
                        'error': f"Role '{role_id}' is in use by user '{username}'"
                    }
            
            # Delete role
            del self.roles[role_id]
            
            # Delete role file
            role_file = os.path.join(self.config['auth']['roles_dir'], f"{role_id}.json")
            if os.path.exists(role_file):
                os.remove(role_file)
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="delete_role",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "role_id": role_id
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Role '{role_id}' deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deleting role: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="delete_role",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "role_id": role_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error deleting role: {str(e)}"
            }
    
    def list_roles(self) -> Dict[str, Any]:
        """
        List all roles.
        
        Returns:
            Dictionary with operation result
        """
        try:
            return {
                'success': True,
                'roles': self.roles
            }
            
        except Exception as e:
            logger.error(f"Error listing roles: {e}")
            return {
                'success': False,
                'error': f"Error listing roles: {str(e)}"
            }
    
    def create_organization(self, org_id: str, name: str, description: str, 
                           country: str, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new organization.
        
        Args:
            org_id: Organization identifier
            name: Organization name
            description: Organization description
            country: Country identifier
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if organization already exists
            if org_id in self.organizations:
                return {
                    'success': False,
                    'error': f"Organization '{org_id}' already exists"
                }
            
            # Check if country exists
            if country not in self.countries:
                return {
                    'success': False,
                    'error': f"Country '{country}' does not exist"
                }
            
            # Create organization
            org_data = {
                'name': name,
                'description': description,
                'country': country,
                'created_at': datetime.datetime.now().isoformat(),
                'created_by': admin_user['username'],
                'active': True
            }
            
            # Add organization
            self.organizations[org_id] = org_data
            
            # Save organizations
            self._save_organizations()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="create_organization",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "org_id": org_id,
                        "name": name,
                        "country": country
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Organization '{org_id}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating organization: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="create_organization",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "org_id": org_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error creating organization: {str(e)}"
            }
    
    def update_organization(self, org_id: str, org_data: Dict[str, Any], 
                           admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an organization.
        
        Args:
            org_id: Organization identifier
            org_data: Organization data to update
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if organization exists
            if org_id not in self.organizations:
                return {
                    'success': False,
                    'error': f"Organization '{org_id}' does not exist"
                }
            
            current_org_data = self.organizations[org_id]
            
            # Update organization data
            for field, value in org_data.items():
                # Skip created_at and created_by fields
                if field in ['created_at', 'created_by']:
                    continue
                
                # Validate country
                if field == 'country' and value not in self.countries:
                    return {
                        'success': False,
                        'error': f"Country '{value}' does not exist"
                    }
                
                # Update field
                current_org_data[field] = value
            
            # Add updated_at and updated_by fields
            current_org_data['updated_at'] = datetime.datetime.now().isoformat()
            current_org_data['updated_by'] = admin_user['username']
            
            # Save organizations
            self._save_organizations()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="update_organization",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "org_id": org_id,
                        "updated_fields": list(org_data.keys())
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Organization '{org_id}' updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating organization: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="update_organization",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "org_id": org_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error updating organization: {str(e)}"
            }
    
    def deactivate_organization(self, org_id: str, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deactivate an organization.
        
        Args:
            org_id: Organization identifier
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if organization exists
            if org_id not in self.organizations:
                return {
                    'success': False,
                    'error': f"Organization '{org_id}' does not exist"
                }
            
            # Deactivate organization
            self.organizations[org_id]['active'] = False
            
            # Add updated_at and updated_by fields
            self.organizations[org_id]['updated_at'] = datetime.datetime.now().isoformat()
            self.organizations[org_id]['updated_by'] = admin_user['username']
            
            # Save organizations
            self._save_organizations()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="deactivate_organization",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "org_id": org_id
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Organization '{org_id}' deactivated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deactivating organization: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="deactivate_organization",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "org_id": org_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error deactivating organization: {str(e)}"
            }
    
    def activate_organization(self, org_id: str, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Activate an organization.
        
        Args:
            org_id: Organization identifier
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if organization exists
            if org_id not in self.organizations:
                return {
                    'success': False,
                    'error': f"Organization '{org_id}' does not exist"
                }
            
            # Activate organization
            self.organizations[org_id]['active'] = True
            
            # Add updated_at and updated_by fields
            self.organizations[org_id]['updated_at'] = datetime.datetime.now().isoformat()
            self.organizations[org_id]['updated_by'] = admin_user['username']
            
            # Save organizations
            self._save_organizations()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="activate_organization",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "org_id": org_id
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Organization '{org_id}' activated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error activating organization: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="activate_organization",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "org_id": org_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error activating organization: {str(e)}"
            }
    
    def list_organizations(self) -> Dict[str, Any]:
        """
        List all organizations.
        
        Returns:
            Dictionary with operation result
        """
        try:
            return {
                'success': True,
                'organizations': self.organizations
            }
            
        except Exception as e:
            logger.error(f"Error listing organizations: {e}")
            return {
                'success': False,
                'error': f"Error listing organizations: {str(e)}"
            }
    
    def create_country(self, country_id: str, name: str, code: str, 
                      admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new country.
        
        Args:
            country_id: Country identifier
            name: Country name
            code: Country code (ISO 3166-1 alpha-2)
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if country already exists
            if country_id in self.countries:
                return {
                    'success': False,
                    'error': f"Country '{country_id}' already exists"
                }
            
            # Create country
            country_data = {
                'name': name,
                'code': code,
                'created_at': datetime.datetime.now().isoformat(),
                'created_by': admin_user['username'],
                'active': True
            }
            
            # Add country
            self.countries[country_id] = country_data
            
            # Save countries
            self._save_countries()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="create_country",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "country_id": country_id,
                        "name": name,
                        "code": code
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Country '{country_id}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Error creating country: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="create_country",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "country_id": country_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error creating country: {str(e)}"
            }
    
    def update_country(self, country_id: str, country_data: Dict[str, Any], 
                      admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a country.
        
        Args:
            country_id: Country identifier
            country_data: Country data to update
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if country exists
            if country_id not in self.countries:
                return {
                    'success': False,
                    'error': f"Country '{country_id}' does not exist"
                }
            
            current_country_data = self.countries[country_id]
            
            # Update country data
            for field, value in country_data.items():
                # Skip created_at and created_by fields
                if field in ['created_at', 'created_by']:
                    continue
                
                # Update field
                current_country_data[field] = value
            
            # Add updated_at and updated_by fields
            current_country_data['updated_at'] = datetime.datetime.now().isoformat()
            current_country_data['updated_by'] = admin_user['username']
            
            # Save countries
            self._save_countries()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="update_country",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "country_id": country_id,
                        "updated_fields": list(country_data.keys())
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Country '{country_id}' updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating country: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="update_country",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "country_id": country_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error updating country: {str(e)}"
            }
    
    def deactivate_country(self, country_id: str, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deactivate a country.
        
        Args:
            country_id: Country identifier
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if country exists
            if country_id not in self.countries:
                return {
                    'success': False,
                    'error': f"Country '{country_id}' does not exist"
                }
            
            # Deactivate country
            self.countries[country_id]['active'] = False
            
            # Add updated_at and updated_by fields
            self.countries[country_id]['updated_at'] = datetime.datetime.now().isoformat()
            self.countries[country_id]['updated_by'] = admin_user['username']
            
            # Save countries
            self._save_countries()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="deactivate_country",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "country_id": country_id
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Country '{country_id}' deactivated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deactivating country: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="deactivate_country",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "country_id": country_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error deactivating country: {str(e)}"
            }
    
    def activate_country(self, country_id: str, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Activate a country.
        
        Args:
            country_id: Country identifier
            admin_user: Admin user data for authorization
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if admin user exists
            if admin_user['username'] not in self.users:
                return {
                    'success': False,
                    'error': f"Admin user '{admin_user['username']}' does not exist"
                }
            
            # Check if admin user has admin role
            if self.users[admin_user['username']]['role'] != 'admin':
                return {
                    'success': False,
                    'error': f"User '{admin_user['username']}' is not an admin"
                }
            
            # Verify admin password
            if not self._verify_password(admin_user['password'], self.users[admin_user['username']]['password_hash']):
                return {
                    'success': False,
                    'error': "Invalid admin password"
                }
            
            # Check if country exists
            if country_id not in self.countries:
                return {
                    'success': False,
                    'error': f"Country '{country_id}' does not exist"
                }
            
            # Activate country
            self.countries[country_id]['active'] = True
            
            # Add updated_at and updated_by fields
            self.countries[country_id]['updated_at'] = datetime.datetime.now().isoformat()
            self.countries[country_id]['updated_by'] = admin_user['username']
            
            # Save countries
            self._save_countries()
            
            # Log the action
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="activate_country",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "country_id": country_id
                    },
                    status="success"
                )
            
            return {
                'success': True,
                'message': f"Country '{country_id}' activated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error activating country: {e}")
            
            # Log the error
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type="AUTH",
                    action="activate_country",
                    component="auth_manager",
                    user_info=admin_user,
                    details={
                        "country_id": country_id,
                        "error": str(e)
                    },
                    status="error"
                )
            
            return {
                'success': False,
                'error': f"Error activating country: {str(e)}"
            }
    
    def list_countries(self) -> Dict[str, Any]:
        """
        List all countries.
        
        Returns:
            Dictionary with operation result
        """
        try:
            return {
                'success': True,
                'countries': self.countries
            }
            
        except Exception as e:
            logger.error(f"Error listing countries: {e}")
            return {
                'success': False,
                'error': f"Error listing countries: {str(e)}"
            }
    
    def check_permission(self, user_info: Dict[str, Any], permission: str) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            user_info: User information
            permission: Permission to check
            
        Returns:
            True if user has permission, False otherwise
        """
        try:
            # Get username
            username = user_info.get('username')
            
            # Check if user exists
            if username not in self.users:
                return False
            
            # Get user role
            role_id = self.users[username]['role']
            
            # Check if role exists
            if role_id not in self.roles:
                return False
            
            # Get role permissions
            role_permissions = self.roles[role_id]['permissions']
            
            # Check for wildcard permission
            if '*' in role_permissions:
                return True
            
            # Check for specific permission
            if permission in role_permissions:
                return True
            
            # Check for wildcard permission category
            permission_parts = permission.split(':')
            if len(permission_parts) == 2:
                action, resource = permission_parts
                wildcard_permission = f"{action}:*"
                
                if wildcard_permission in role_permissions:
                    return True
                
                # Check for resource wildcard permissions
                for role_permission in role_permissions:
                    if role_permission.endswith('*'):
                        role_permission_prefix = role_permission[:-1]
                        if permission.startswith(role_permission_prefix):
                            return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
    
    def get_user_permissions(self, username: str) -> Dict[str, Any]:
        """
        Get all permissions for a user.
        
        Args:
            username: Username
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Check if user exists
            if username not in self.users:
                return {
                    'success': False,
                    'error': "User not found"
                }
            
            # Get user role
            role_id = self.users[username]['role']
            
            # Check if role exists
            if role_id not in self.roles:
                return {
                    'success': False,
                    'error': f"Role '{role_id}' not found"
                }
            
            # Get role permissions
            role_permissions = self.roles[role_id]['permissions']
            
            return {
                'success': True,
                'username': username,
                'role': role_id,
                'permissions': role_permissions
            }
            
        except Exception as e:
            logger.error(f"Error getting user permissions: {e}")
            return {
                'success': False,
                'error': f"Error getting user permissions: {str(e)}"
            }
