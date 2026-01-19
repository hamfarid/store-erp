#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Organization hierarchy management system for the Agricultural AI System.

This module provides functionality for managing organizations, companies,
and their hierarchical relationships, as well as user affiliations.
"""

import os
import json
import logging
import sqlite3
from datetime import datetime
import traceback
import shutil
import yaml
import csv
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('organization_manager')

class OrganizationManager:
    """
    Manages organizations, companies, and their hierarchical relationships.
    
    This class provides methods to:
    1. Create, update, and delete organizations and companies
    2. Manage hierarchical relationships between organizations
    3. Associate users with organizations and companies
    4. Retrieve organization and company information
    5. Validate user access based on organization hierarchy
    """
    
    def __init__(self, config=None, auth_manager=None, audit_manager=None):
        """
        Initialize the organization manager.
        
        Args:
            config (dict): Configuration dictionary with organization management settings
            auth_manager: Authentication manager instance for user validation
            audit_manager: Audit manager instance for logging actions
        """
        self.config = config or {}
        self.auth_manager = auth_manager
        self.audit_manager = audit_manager
        
        # Default configuration
        self.default_config = {
            'org_dir': 'data/organizations',
            'db_path': 'data/database/organizations.db',
            'backup_dir': 'data/backups/organizations',
        }
        
        # Merge with provided config
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
        
        # Create necessary directories
        for dir_key in ['org_dir', 'backup_dir']:
            os.makedirs(self.config[dir_key], exist_ok=True)
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.config['db_path']), exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info("Organization manager initialized")
    
    def _init_database(self):
        """Initialize the SQLite database for organization management."""
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Create organizations table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                description TEXT,
                logo_path TEXT,
                parent_id INTEGER,
                created_at TEXT NOT NULL,
                created_by TEXT,
                updated_at TEXT,
                updated_by TEXT,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY (parent_id) REFERENCES organizations (id)
            )
            ''')
            
            # Create companies table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                description TEXT,
                logo_path TEXT,
                organization_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                created_by TEXT,
                updated_at TEXT,
                updated_by TEXT,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                FOREIGN KEY (organization_id) REFERENCES organizations (id)
            )
            ''')
            
            # Create user_affiliations table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_affiliations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                organization_id INTEGER NOT NULL,
                company_id INTEGER,
                is_primary BOOLEAN NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                created_by TEXT,
                updated_at TEXT,
                updated_by TEXT,
                FOREIGN KEY (organization_id) REFERENCES organizations (id),
                FOREIGN KEY (company_id) REFERENCES companies (id),
                UNIQUE(user_id, organization_id, company_id)
            )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Organization database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def create_organization(self, name, code, description=None, logo_path=None, 
                           parent_id=None, user_info=None):
        """
        Create a new organization.
        
        Args:
            name (str): Name of the organization
            code (str): Unique code for the organization
            description (str): Description of the organization
            logo_path (str): Path to the organization logo
            parent_id (int): ID of the parent organization
            user_info (dict): Information about the user creating the organization
            
        Returns:
            tuple: (success, message, organization_id)
        """
        try:
            # Validate code format (alphanumeric with underscores)
            if not re.match(r'^[a-zA-Z0-9_]+$', code):
                return False, "Organization code must contain only letters, numbers, and underscores", None
            
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if code already exists
            cursor.execute('SELECT id FROM organizations WHERE code = ?', (code,))
            if cursor.fetchone():
                conn.close()
                return False, f"Organization with code '{code}' already exists", None
            
            # Validate parent organization if provided
            if parent_id:
                cursor.execute('SELECT id FROM organizations WHERE id = ?', (parent_id,))
                if not cursor.fetchone():
                    conn.close()
                    return False, f"Parent organization with ID {parent_id} not found", None
            
            # Extract user information
            username = user_info.get('username') if user_info else None
            
            # Insert the organization
            cursor.execute('''
            INSERT INTO organizations (
                name, code, description, logo_path, parent_id,
                created_at, created_by, updated_at, updated_by, is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''', (
                name, code, description, logo_path, parent_id,
                datetime.now().isoformat(), username,
                datetime.now().isoformat(), username
            ))
            
            organization_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='create',
                    component='organizations',
                    user_info=user_info,
                    details={
                        'organization_id': organization_id,
                        'name': name,
                        'code': code,
                        'parent_id': parent_id
                    },
                    status='success'
                )
            
            # Save organization to file for backup
            self._save_organization_to_file(organization_id, name, code, description, 
                                           logo_path, parent_id)
            
            return True, f"Organization '{name}' created successfully", organization_id
            
        except Exception as e:
            logger.error(f"Error creating organization: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error creating organization: {str(e)}", None
    
    def update_organization(self, organization_id, updates, user_info=None):
        """
        Update an existing organization.
        
        Args:
            organization_id (int): ID of the organization to update
            updates (dict): Dictionary of fields to update
            user_info (dict): Information about the user updating the organization
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if organization exists
            cursor.execute('SELECT * FROM organizations WHERE id = ?', (organization_id,))
            org = cursor.fetchone()
            
            if not org:
                conn.close()
                return False, f"Organization with ID {organization_id} not found"
            
            # Extract current values
            _, name, code, description, logo_path, parent_id, _, _, _, _, is_active = org
            
            # Prepare updates
            new_name = updates.get('name', name)
            new_code = updates.get('code', code)
            new_description = updates.get('description', description)
            new_logo_path = updates.get('logo_path', logo_path)
            new_parent_id = updates.get('parent_id', parent_id)
            new_is_active = updates.get('is_active', is_active)
            
            # Validate code format if changed
            if new_code != code and not re.match(r'^[a-zA-Z0-9_]+$', new_code):
                conn.close()
                return False, "Organization code must contain only letters, numbers, and underscores"
            
            # Check if new code already exists
            if new_code != code:
                cursor.execute('SELECT id FROM organizations WHERE code = ? AND id != ?', 
                              (new_code, organization_id))
                if cursor.fetchone():
                    conn.close()
                    return False, f"Organization with code '{new_code}' already exists"
            
            # Validate parent organization if changed
            if new_parent_id != parent_id and new_parent_id:
                cursor.execute('SELECT id FROM organizations WHERE id = ?', (new_parent_id,))
                if not cursor.fetchone():
                    conn.close()
                    return False, f"Parent organization with ID {new_parent_id} not found"
                
                # Prevent circular references
                if new_parent_id == organization_id:
                    conn.close()
                    return False, "Organization cannot be its own parent"
                
                # Check for deeper circular references
                parent_chain = [organization_id, new_parent_id]
                current_parent = new_parent_id
                
                while current_parent:
                    cursor.execute('SELECT parent_id FROM organizations WHERE id = ?', (current_parent,))
                    result = cursor.fetchone()
                    if not result or not result[0]:
                        break
                    
                    next_parent = result[0]
                    if next_parent in parent_chain:
                        conn.close()
                        return False, "Circular reference detected in organization hierarchy"
                    
                    parent_chain.append(next_parent)
                    current_parent = next_parent
            
            # Extract user information
            username = user_info.get('username') if user_info else None
            
            # Update the organization
            cursor.execute('''
            UPDATE organizations SET
                name = ?,
                code = ?,
                description = ?,
                logo_path = ?,
                parent_id = ?,
                updated_at = ?,
                updated_by = ?,
                is_active = ?
            WHERE id = ?
            ''', (
                new_name, new_code, new_description, new_logo_path, new_parent_id,
                datetime.now().isoformat(), username, new_is_active, organization_id
            ))
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='update',
                    component='organizations',
                    user_info=user_info,
                    details={
                        'organization_id': organization_id,
                        'updates': updates
                    },
                    status='success'
                )
            
            # Update organization file
            self._save_organization_to_file(organization_id, new_name, new_code, 
                                           new_description, new_logo_path, new_parent_id)
            
            return True, f"Organization updated successfully"
            
        except Exception as e:
            logger.error(f"Error updating organization: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error updating organization: {str(e)}"
    
    def delete_organization(self, organization_id, user_info=None):
        """
        Delete an organization.
        
        Args:
            organization_id (int): ID of the organization to delete
            user_info (dict): Information about the user deleting the organization
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if organization exists
            cursor.execute('SELECT name, code FROM organizations WHERE id = ?', (organization_id,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, f"Organization with ID {organization_id} not found"
            
            org_name, org_code = result
            
            # Check if organization has child organizations
            cursor.execute('SELECT COUNT(*) FROM organizations WHERE parent_id = ?', (organization_id,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False, f"Cannot delete organization '{org_name}' because it has child organizations"
            
            # Check if organization has companies
            cursor.execute('SELECT COUNT(*) FROM companies WHERE organization_id = ?', (organization_id,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False, f"Cannot delete organization '{org_name}' because it has associated companies"
            
            # Check if organization has user affiliations
            cursor.execute('SELECT COUNT(*) FROM user_affiliations WHERE organization_id = ?', (organization_id,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False, f"Cannot delete organization '{org_name}' because it has user affiliations"
            
            # Delete the organization
            cursor.execute('DELETE FROM organizations WHERE id = ?', (organization_id,))
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='delete',
                    component='organizations',
                    user_info=user_info,
                    details={
                        'organization_id': organization_id,
                        'name': org_name,
                        'code': org_code
                    },
                    status='success'
                )
            
            # Delete organization file
            self._delete_organization_file(org_code)
            
            return True, f"Organization '{org_name}' deleted successfully"
            
        except Exception as e:
            logger.error(f"Error deleting organization: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error deleting organization: {str(e)}"
    
    def create_company(self, name, code, organization_id, description=None, 
                      logo_path=None, user_info=None):
        """
        Create a new company within an organization.
        
        Args:
            name (str): Name of the company
            code (str): Unique code for the company
            organization_id (int): ID of the parent organization
            description (str): Description of the company
            logo_path (str): Path to the company logo
            user_info (dict): Information about the user creating the company
            
        Returns:
            tuple: (success, message, company_id)
        """
        try:
            # Validate code format (alphanumeric with underscores)
            if not re.match(r'^[a-zA-Z0-9_]+$', code):
                return False, "Company code must contain only letters, numbers, and underscores", None
            
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if code already exists
            cursor.execute('SELECT id FROM companies WHERE code = ?', (code,))
            if cursor.fetchone():
                conn.close()
                return False, f"Company with code '{code}' already exists", None
            
            # Validate parent organization
            cursor.execute('SELECT id FROM organizations WHERE id = ?', (organization_id,))
            if not cursor.fetchone():
                conn.close()
                return False, f"Organization with ID {organization_id} not found", None
            
            # Extract user information
            username = user_info.get('username') if user_info else None
            
            # Insert the company
            cursor.execute('''
            INSERT INTO companies (
                name, code, description, logo_path, organization_id,
                created_at, created_by, updated_at, updated_by, is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''', (
                name, code, description, logo_path, organization_id,
                datetime.now().isoformat(), username,
                datetime.now().isoformat(), username
            ))
            
            company_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='create',
                    component='companies',
                    user_info=user_info,
                    details={
                        'company_id': company_id,
                        'name': name,
                        'code': code,
                        'organization_id': organization_id
                    },
                    status='success'
                )
            
            # Save company to file for backup
            self._save_company_to_file(company_id, name, code, description, 
                                      logo_path, organization_id)
            
            return True, f"Company '{name}' created successfully", company_id
            
        except Exception as e:
            logger.error(f"Error creating company: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error creating company: {str(e)}", None
    
    def update_company(self, company_id, updates, user_info=None):
        """
        Update an existing company.
        
        Args:
            company_id (int): ID of the company to update
            updates (dict): Dictionary of fields to update
            user_info (dict): Information about the user updating the company
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if company exists
            cursor.execute('SELECT * FROM companies WHERE id = ?', (company_id,))
            company = cursor.fetchone()
            
            if not company:
                conn.close()
                return False, f"Company with ID {company_id} not found"
            
            # Extract current values
            _, name, code, description, logo_path, organization_id, _, _, _, _, is_active = company
            
            # Prepare updates
            new_name = updates.get('name', name)
            new_code = updates.get('code', code)
            new_description = updates.get('description', description)
            new_logo_path = updates.get('logo_path', logo_path)
            new_organization_id = updates.get('organization_id', organization_id)
            new_is_active = updates.get('is_active', is_active)
            
            # Validate code format if changed
            if new_code != code and not re.match(r'^[a-zA-Z0-9_]+$', new_code):
                conn.close()
                return False, "Company code must contain only letters, numbers, and underscores"
            
            # Check if new code already exists
            if new_code != code:
                cursor.execute('SELECT id FROM companies WHERE code = ? AND id != ?', 
                              (new_code, company_id))
                if cursor.fetchone():
                    conn.close()
                    return False, f"Company with code '{new_code}' already exists"
            
            # Validate organization if changed
            if new_organization_id != organization_id:
                cursor.execute('SELECT id FROM organizations WHERE id = ?', (new_organization_id,))
                if not cursor.fetchone():
                    conn.close()
                    return False, f"Organization with ID {new_organization_id} not found"
            
            # Extract user information
            username = user_info.get('username') if user_info else None
            
            # Update the company
            cursor.execute('''
            UPDATE companies SET
                name = ?,
                code = ?,
                description = ?,
                logo_path = ?,
                organization_id = ?,
                updated_at = ?,
                updated_by = ?,
                is_active = ?
            WHERE id = ?
            ''', (
                new_name, new_code, new_description, new_logo_path, new_organization_id,
                datetime.now().isoformat(), username, new_is_active, company_id
            ))
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='update',
                    component='companies',
                    user_info=user_info,
                    details={
                        'company_id': company_id,
                        'updates': updates
                    },
                    status='success'
                )
            
            # Update company file
            self._save_company_to_file(company_id, new_name, new_code, new_description, 
                                      new_logo_path, new_organization_id)
            
            return True, f"Company updated successfully"
            
        except Exception as e:
            logger.error(f"Error updating company: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error updating company: {str(e)}"
    
    def delete_company(self, company_id, user_info=None):
        """
        Delete a company.
        
        Args:
            company_id (int): ID of the company to delete
            user_info (dict): Information about the user deleting the company
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if company exists
            cursor.execute('SELECT name, code FROM companies WHERE id = ?', (company_id,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, f"Company with ID {company_id} not found"
            
            company_name, company_code = result
            
            # Check if company has user affiliations
            cursor.execute('SELECT COUNT(*) FROM user_affiliations WHERE company_id = ?', (company_id,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False, f"Cannot delete company '{company_name}' because it has user affiliations"
            
            # Delete the company
            cursor.execute('DELETE FROM companies WHERE id = ?', (company_id,))
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='delete',
                    component='companies',
                    user_info=user_info,
                    details={
                        'company_id': company_id,
                        'name': company_name,
                        'code': company_code
                    },
                    status='success'
                )
            
            # Delete company file
            self._delete_company_file(company_code)
            
            return True, f"Company '{company_name}' deleted successfully"
            
        except Exception as e:
            logger.error(f"Error deleting company: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error deleting company: {str(e)}"
    
    def add_user_affiliation(self, user_id, username, organization_id, company_id=None, 
                            is_primary=False, user_info=None):
        """
        Add a user affiliation to an organization and optionally a company.
        
        Args:
            user_id (int): ID of the user
            username (str): Username of the user
            organization_id (int): ID of the organization
            company_id (int): ID of the company (optional)
            is_primary (bool): Whether this is the user's primary affiliation
            user_info (dict): Information about the user creating the affiliation
            
        Returns:
            tuple: (success, message, affiliation_id)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Validate organization
            cursor.execute('SELECT id FROM organizations WHERE id = ?', (organization_id,))
            if not cursor.fetchone():
                conn.close()
                return False, f"Organization with ID {organization_id} not found", None
            
            # Validate company if provided
            if company_id:
                cursor.execute('SELECT organization_id FROM companies WHERE id = ?', (company_id,))
                result = cursor.fetchone()
                
                if not result:
                    conn.close()
                    return False, f"Company with ID {company_id} not found", None
                
                # Check if company belongs to the specified organization
                if result[0] != organization_id:
                    conn.close()
                    return False, f"Company with ID {company_id} does not belong to organization with ID {organization_id}", None
            
            # Check if affiliation already exists
            cursor.execute('''
            SELECT id FROM user_affiliations 
            WHERE user_id = ? AND organization_id = ? AND (company_id = ? OR (company_id IS NULL AND ? IS NULL))
            ''', (user_id, organization_id, company_id, company_id))
            
            existing = cursor.fetchone()
            if existing:
                conn.close()
                return False, f"User already has an affiliation with this organization/company", existing[0]
            
            # If this is a primary affiliation, update existing primary affiliations
            if is_primary:
                cursor.execute('''
                UPDATE user_affiliations SET is_primary = 0
                WHERE user_id = ?
                ''', (user_id,))
            
            # Extract user information
            admin_username = user_info.get('username') if user_info else None
            
            # Insert the affiliation
            cursor.execute('''
            INSERT INTO user_affiliations (
                user_id, username, organization_id, company_id, is_primary,
                created_at, created_by, updated_at, updated_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, username, organization_id, company_id, is_primary,
                datetime.now().isoformat(), admin_username,
                datetime.now().isoformat(), admin_username
            ))
            
            affiliation_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='create',
                    component='user_affiliations',
                    user_info=user_info,
                    details={
                        'affiliation_id': affiliation_id,
                        'user_id': user_id,
                        'username': username,
                        'organization_id': organization_id,
                        'company_id': company_id,
                        'is_primary': is_primary
                    },
                    status='success'
                )
            
            return True, f"User affiliation created successfully", affiliation_id
            
        except Exception as e:
            logger.error(f"Error adding user affiliation: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error adding user affiliation: {str(e)}", None
    
    def update_user_affiliation(self, affiliation_id, updates, user_info=None):
        """
        Update a user affiliation.
        
        Args:
            affiliation_id (int): ID of the affiliation to update
            updates (dict): Dictionary of fields to update
            user_info (dict): Information about the user updating the affiliation
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if affiliation exists
            cursor.execute('''
            SELECT user_id, organization_id, company_id, is_primary 
            FROM user_affiliations WHERE id = ?
            ''', (affiliation_id,))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False, f"User affiliation with ID {affiliation_id} not found"
            
            user_id, organization_id, company_id, is_primary = result
            
            # Prepare updates
            new_organization_id = updates.get('organization_id', organization_id)
            new_company_id = updates.get('company_id', company_id)
            new_is_primary = updates.get('is_primary', is_primary)
            
            # Validate organization if changed
            if new_organization_id != organization_id:
                cursor.execute('SELECT id FROM organizations WHERE id = ?', (new_organization_id,))
                if not cursor.fetchone():
                    conn.close()
                    return False, f"Organization with ID {new_organization_id} not found"
            
            # Validate company if changed
            if new_company_id != company_id:
                if new_company_id:
                    cursor.execute('SELECT organization_id FROM companies WHERE id = ?', (new_company_id,))
                    result = cursor.fetchone()
                    
                    if not result:
                        conn.close()
                        return False, f"Company with ID {new_company_id} not found"
                    
                    # Check if company belongs to the specified organization
                    if result[0] != new_organization_id:
                        conn.close()
                        return False, f"Company with ID {new_company_id} does not belong to organization with ID {new_organization_id}"
            
            # If this is becoming a primary affiliation, update existing primary affiliations
            if new_is_primary and not is_primary:
                cursor.execute('''
                UPDATE user_affiliations SET is_primary = 0
                WHERE user_id = ? AND id != ?
                ''', (user_id, affiliation_id))
            
            # Extract user information
            admin_username = user_info.get('username') if user_info else None
            
            # Update the affiliation
            cursor.execute('''
            UPDATE user_affiliations SET
                organization_id = ?,
                company_id = ?,
                is_primary = ?,
                updated_at = ?,
                updated_by = ?
            WHERE id = ?
            ''', (
                new_organization_id, new_company_id, new_is_primary,
                datetime.now().isoformat(), admin_username, affiliation_id
            ))
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='update',
                    component='user_affiliations',
                    user_info=user_info,
                    details={
                        'affiliation_id': affiliation_id,
                        'updates': updates
                    },
                    status='success'
                )
            
            return True, f"User affiliation updated successfully"
            
        except Exception as e:
            logger.error(f"Error updating user affiliation: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error updating user affiliation: {str(e)}"
    
    def remove_user_affiliation(self, affiliation_id, user_info=None):
        """
        Remove a user affiliation.
        
        Args:
            affiliation_id (int): ID of the affiliation to remove
            user_info (dict): Information about the user removing the affiliation
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Check if affiliation exists
            cursor.execute('''
            SELECT user_id, username, organization_id, company_id, is_primary 
            FROM user_affiliations WHERE id = ?
            ''', (affiliation_id,))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False, f"User affiliation with ID {affiliation_id} not found"
            
            user_id, username, organization_id, company_id, is_primary = result
            
            # Delete the affiliation
            cursor.execute('DELETE FROM user_affiliations WHERE id = ?', (affiliation_id,))
            
            # If this was a primary affiliation, set another one as primary if available
            if is_primary:
                cursor.execute('''
                SELECT id FROM user_affiliations
                WHERE user_id = ?
                ORDER BY created_at ASC
                LIMIT 1
                ''', (user_id,))
                
                new_primary = cursor.fetchone()
                if new_primary:
                    cursor.execute('''
                    UPDATE user_affiliations SET is_primary = 1
                    WHERE id = ?
                    ''', (new_primary[0],))
            
            conn.commit()
            conn.close()
            
            # Log the action if audit manager is available
            if self.audit_manager:
                self.audit_manager.log_action(
                    action_type='DATA',
                    action='delete',
                    component='user_affiliations',
                    user_info=user_info,
                    details={
                        'affiliation_id': affiliation_id,
                        'user_id': user_id,
                        'username': username,
                        'organization_id': organization_id,
                        'company_id': company_id
                    },
                    status='success'
                )
            
            return True, f"User affiliation removed successfully"
            
        except Exception as e:
            logger.error(f"Error removing user affiliation: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error removing user affiliation: {str(e)}"
    
    def get_organization(self, organization_id=None, code=None):
        """
        Get organization details.
        
        Args:
            organization_id (int): ID of the organization
            code (str): Code of the organization
            
        Returns:
            dict: Organization details, or None if not found
        """
        if not organization_id and not code:
            return None
        
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            if organization_id:
                cursor.execute('''
                SELECT id, name, code, description, logo_path, parent_id, 
                       created_at, created_by, updated_at, updated_by, is_active
                FROM organizations
                WHERE id = ?
                ''', (organization_id,))
            else:
                cursor.execute('''
                SELECT id, name, code, description, logo_path, parent_id, 
                       created_at, created_by, updated_at, updated_by, is_active
                FROM organizations
                WHERE code = ?
                ''', (code,))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return None
            
            id, name, code, description, logo_path, parent_id, \
            created_at, created_by, updated_at, updated_by, is_active = result
            
            # Get parent organization name if available
            parent_name = None
            if parent_id:
                cursor.execute('SELECT name FROM organizations WHERE id = ?', (parent_id,))
                parent_result = cursor.fetchone()
                if parent_result:
                    parent_name = parent_result[0]
            
            # Get child organizations
            cursor.execute('''
            SELECT id, name, code FROM organizations
            WHERE parent_id = ?
            ORDER BY name
            ''', (id,))
            
            children = []
            for child_row in cursor.fetchall():
                children.append({
                    'id': child_row[0],
                    'name': child_row[1],
                    'code': child_row[2]
                })
            
            # Get companies
            cursor.execute('''
            SELECT id, name, code FROM companies
            WHERE organization_id = ?
            ORDER BY name
            ''', (id,))
            
            companies = []
            for company_row in cursor.fetchall():
                companies.append({
                    'id': company_row[0],
                    'name': company_row[1],
                    'code': company_row[2]
                })
            
            organization = {
                'id': id,
                'name': name,
                'code': code,
                'description': description,
                'logo_path': logo_path,
                'parent_id': parent_id,
                'parent_name': parent_name,
                'created_at': created_at,
                'created_by': created_by,
                'updated_at': updated_at,
                'updated_by': updated_by,
                'is_active': bool(is_active),
                'children': children,
                'companies': companies
            }
            
            conn.close()
            return organization
            
        except Exception as e:
            logger.error(f"Error getting organization: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return None
    
    def get_company(self, company_id=None, code=None):
        """
        Get company details.
        
        Args:
            company_id (int): ID of the company
            code (str): Code of the company
            
        Returns:
            dict: Company details, or None if not found
        """
        if not company_id and not code:
            return None
        
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            if company_id:
                cursor.execute('''
                SELECT id, name, code, description, logo_path, organization_id, 
                       created_at, created_by, updated_at, updated_by, is_active
                FROM companies
                WHERE id = ?
                ''', (company_id,))
            else:
                cursor.execute('''
                SELECT id, name, code, description, logo_path, organization_id, 
                       created_at, created_by, updated_at, updated_by, is_active
                FROM companies
                WHERE code = ?
                ''', (code,))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return None
            
            id, name, code, description, logo_path, organization_id, \
            created_at, created_by, updated_at, updated_by, is_active = result
            
            # Get organization name
            cursor.execute('SELECT name, code FROM organizations WHERE id = ?', (organization_id,))
            org_result = cursor.fetchone()
            org_name = org_result[0] if org_result else None
            org_code = org_result[1] if org_result else None
            
            company = {
                'id': id,
                'name': name,
                'code': code,
                'description': description,
                'logo_path': logo_path,
                'organization_id': organization_id,
                'organization_name': org_name,
                'organization_code': org_code,
                'created_at': created_at,
                'created_by': created_by,
                'updated_at': updated_at,
                'updated_by': updated_by,
                'is_active': bool(is_active)
            }
            
            conn.close()
            return company
            
        except Exception as e:
            logger.error(f"Error getting company: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return None
    
    def get_user_affiliations(self, user_id=None, username=None):
        """
        Get user affiliations.
        
        Args:
            user_id (int): ID of the user
            username (str): Username of the user
            
        Returns:
            list: List of user affiliations
        """
        if not user_id and not username:
            return []
        
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                SELECT id, organization_id, company_id, is_primary,
                       created_at, updated_at
                FROM user_affiliations
                WHERE user_id = ?
                ORDER BY is_primary DESC, created_at ASC
                ''', (user_id,))
            else:
                cursor.execute('''
                SELECT id, organization_id, company_id, is_primary,
                       created_at, updated_at
                FROM user_affiliations
                WHERE username = ?
                ORDER BY is_primary DESC, created_at ASC
                ''', (username,))
            
            affiliations = []
            for row in cursor.fetchall():
                affiliation_id, organization_id, company_id, is_primary, created_at, updated_at = row
                
                # Get organization details
                cursor.execute('''
                SELECT name, code FROM organizations WHERE id = ?
                ''', (organization_id,))
                
                org_result = cursor.fetchone()
                org_name = org_result[0] if org_result else None
                org_code = org_result[1] if org_result else None
                
                # Get company details if available
                company_name = None
                company_code = None
                
                if company_id:
                    cursor.execute('''
                    SELECT name, code FROM companies WHERE id = ?
                    ''', (company_id,))
                    
                    company_result = cursor.fetchone()
                    if company_result:
                        company_name = company_result[0]
                        company_code = company_result[1]
                
                affiliations.append({
                    'id': affiliation_id,
                    'organization_id': organization_id,
                    'organization_name': org_name,
                    'organization_code': org_code,
                    'company_id': company_id,
                    'company_name': company_name,
                    'company_code': company_code,
                    'is_primary': bool(is_primary),
                    'created_at': created_at,
                    'updated_at': updated_at
                })
            
            conn.close()
            return affiliations
            
        except Exception as e:
            logger.error(f"Error getting user affiliations: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return []
    
    def get_primary_affiliation(self, user_id=None, username=None):
        """
        Get user's primary affiliation.
        
        Args:
            user_id (int): ID of the user
            username (str): Username of the user
            
        Returns:
            dict: Primary affiliation details, or None if not found
        """
        affiliations = self.get_user_affiliations(user_id, username)
        
        # Find primary affiliation
        for affiliation in affiliations:
            if affiliation['is_primary']:
                return affiliation
        
        # If no primary affiliation is set but there are affiliations, return the first one
        if affiliations:
            return affiliations[0]
        
        return None
    
    def get_all_organizations(self, include_inactive=False):
        """
        Get all organizations.
        
        Args:
            include_inactive (bool): Whether to include inactive organizations
            
        Returns:
            list: List of organizations
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            query = '''
            SELECT id, name, code, description, logo_path, parent_id, 
                   created_at, created_by, updated_at, updated_by, is_active
            FROM organizations
            '''
            
            if not include_inactive:
                query += ' WHERE is_active = 1'
            
            query += ' ORDER BY name'
            
            cursor.execute(query)
            
            organizations = []
            for row in cursor.fetchall():
                id, name, code, description, logo_path, parent_id, \
                created_at, created_by, updated_at, updated_by, is_active = row
                
                organizations.append({
                    'id': id,
                    'name': name,
                    'code': code,
                    'description': description,
                    'logo_path': logo_path,
                    'parent_id': parent_id,
                    'created_at': created_at,
                    'created_by': created_by,
                    'updated_at': updated_at,
                    'updated_by': updated_by,
                    'is_active': bool(is_active)
                })
            
            conn.close()
            return organizations
            
        except Exception as e:
            logger.error(f"Error getting all organizations: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return []
    
    def get_organization_hierarchy(self, include_inactive=False):
        """
        Get the complete organization hierarchy.
        
        Args:
            include_inactive (bool): Whether to include inactive organizations
            
        Returns:
            list: Hierarchical list of organizations
        """
        try:
            # Get all organizations
            organizations = self.get_all_organizations(include_inactive)
            
            # Create a mapping of organization IDs to their data
            org_map = {org['id']: org for org in organizations}
            
            # Create a mapping of parent IDs to their children
            children_map = {}
            for org in organizations:
                parent_id = org['parent_id']
                if parent_id not in children_map:
                    children_map[parent_id] = []
                children_map[parent_id].append(org['id'])
            
            # Build the hierarchy starting from root organizations (those with no parent)
            root_orgs = [org for org in organizations if org['parent_id'] is None]
            
            # Recursive function to build the hierarchy
            def build_hierarchy(org_id):
                org = org_map[org_id].copy()
                
                # Add children if any
                if org_id in children_map:
                    org['children'] = [build_hierarchy(child_id) for child_id in children_map[org_id]]
                else:
                    org['children'] = []
                
                return org
            
            # Build the complete hierarchy
            hierarchy = [build_hierarchy(org['id']) for org in root_orgs]
            
            return hierarchy
            
        except Exception as e:
            logger.error(f"Error getting organization hierarchy: {e}")
            logger.error(traceback.format_exc())
            return []
    
    def get_all_companies(self, organization_id=None, include_inactive=False):
        """
        Get all companies, optionally filtered by organization.
        
        Args:
            organization_id (int): ID of the organization to filter by
            include_inactive (bool): Whether to include inactive companies
            
        Returns:
            list: List of companies
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            query = '''
            SELECT c.id, c.name, c.code, c.description, c.logo_path, c.organization_id, 
                   c.created_at, c.created_by, c.updated_at, c.updated_by, c.is_active,
                   o.name as organization_name, o.code as organization_code
            FROM companies c
            JOIN organizations o ON c.organization_id = o.id
            '''
            
            params = []
            conditions = []
            
            if organization_id:
                conditions.append('c.organization_id = ?')
                params.append(organization_id)
            
            if not include_inactive:
                conditions.append('c.is_active = 1')
            
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
            
            query += ' ORDER BY c.name'
            
            cursor.execute(query, params)
            
            companies = []
            for row in cursor.fetchall():
                id, name, code, description, logo_path, organization_id, \
                created_at, created_by, updated_at, updated_by, is_active, \
                organization_name, organization_code = row
                
                companies.append({
                    'id': id,
                    'name': name,
                    'code': code,
                    'description': description,
                    'logo_path': logo_path,
                    'organization_id': organization_id,
                    'organization_name': organization_name,
                    'organization_code': organization_code,
                    'created_at': created_at,
                    'created_by': created_by,
                    'updated_at': updated_at,
                    'updated_by': updated_by,
                    'is_active': bool(is_active)
                })
            
            conn.close()
            return companies
            
        except Exception as e:
            logger.error(f"Error getting all companies: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return []
    
    def validate_user_access(self, user_id, organization_id=None, company_id=None):
        """
        Validate if a user has access to an organization or company.
        
        Args:
            user_id (int): ID of the user
            organization_id (int): ID of the organization
            company_id (int): ID of the company
            
        Returns:
            bool: True if user has access, False otherwise
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            if company_id:
                # Check if user has affiliation with the company
                cursor.execute('''
                SELECT COUNT(*) FROM user_affiliations
                WHERE user_id = ? AND company_id = ?
                ''', (user_id, company_id))
                
                if cursor.fetchone()[0] > 0:
                    conn.close()
                    return True
                
                # If not, check if the company belongs to an organization the user is affiliated with
                cursor.execute('''
                SELECT o.id FROM organizations o
                JOIN companies c ON c.organization_id = o.id
                JOIN user_affiliations ua ON ua.organization_id = o.id
                WHERE c.id = ? AND ua.user_id = ? AND ua.company_id IS NULL
                ''', (company_id, user_id))
                
                if cursor.fetchone():
                    conn.close()
                    return True
            
            elif organization_id:
                # Check if user has direct affiliation with the organization
                cursor.execute('''
                SELECT COUNT(*) FROM user_affiliations
                WHERE user_id = ? AND organization_id = ?
                ''', (user_id, organization_id))
                
                if cursor.fetchone()[0] > 0:
                    conn.close()
                    return True
                
                # Check if user has affiliation with a company in the organization
                cursor.execute('''
                SELECT COUNT(*) FROM user_affiliations ua
                JOIN companies c ON ua.company_id = c.id
                WHERE ua.user_id = ? AND c.organization_id = ?
                ''', (user_id, organization_id))
                
                if cursor.fetchone()[0] > 0:
                    conn.close()
                    return True
                
                # Check if user has affiliation with a parent organization
                # Get the chain of parent organizations
                parent_chain = []
                current_org = organization_id
                
                while current_org:
                    cursor.execute('SELECT parent_id FROM organizations WHERE id = ?', (current_org,))
                    result = cursor.fetchone()
                    if not result or not result[0]:
                        break
                    
                    parent_id = result[0]
                    parent_chain.append(parent_id)
                    current_org = parent_id
                
                if parent_chain:
                    placeholders = ','.join('?' for _ in parent_chain)
                    query = f'''
                    SELECT COUNT(*) FROM user_affiliations
                    WHERE user_id = ? AND organization_id IN ({placeholders})
                    '''
                    
                    cursor.execute(query, [user_id] + parent_chain)
                    if cursor.fetchone()[0] > 0:
                        conn.close()
                        return True
            
            conn.close()
            return False
            
        except Exception as e:
            logger.error(f"Error validating user access: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False
    
    def _save_organization_to_file(self, organization_id, name, code, description, 
                                  logo_path, parent_id):
        """
        Save organization details to a file for backup.
        
        Args:
            organization_id (int): ID of the organization
            name (str): Name of the organization
            code (str): Code of the organization
            description (str): Description of the organization
            logo_path (str): Path to the organization logo
            parent_id (int): ID of the parent organization
        """
        try:
            # Create directory if it doesn't exist
            org_dir = os.path.join(self.config['org_dir'], 'organizations')
            os.makedirs(org_dir, exist_ok=True)
            
            # Prepare data for file
            data = {
                'id': organization_id,
                'name': name,
                'code': code,
                'description': description,
                'logo_path': logo_path,
                'parent_id': parent_id,
                'last_updated': datetime.now().isoformat()
            }
            
            # Save to JSON file
            file_path = os.path.join(org_dir, f"{code}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error saving organization to file: {e}")
    
    def _save_company_to_file(self, company_id, name, code, description, 
                             logo_path, organization_id):
        """
        Save company details to a file for backup.
        
        Args:
            company_id (int): ID of the company
            name (str): Name of the company
            code (str): Code of the company
            description (str): Description of the company
            logo_path (str): Path to the company logo
            organization_id (int): ID of the parent organization
        """
        try:
            # Create directory if it doesn't exist
            company_dir = os.path.join(self.config['org_dir'], 'companies')
            os.makedirs(company_dir, exist_ok=True)
            
            # Prepare data for file
            data = {
                'id': company_id,
                'name': name,
                'code': code,
                'description': description,
                'logo_path': logo_path,
                'organization_id': organization_id,
                'last_updated': datetime.now().isoformat()
            }
            
            # Save to JSON file
            file_path = os.path.join(company_dir, f"{code}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error saving company to file: {e}")
    
    def _delete_organization_file(self, code):
        """
        Delete organization file.
        
        Args:
            code (str): Code of the organization
        """
        try:
            file_path = os.path.join(self.config['org_dir'], 'organizations', f"{code}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            logger.error(f"Error deleting organization file: {e}")
    
    def _delete_company_file(self, code):
        """
        Delete company file.
        
        Args:
            code (str): Code of the company
        """
        try:
            file_path = os.path.join(self.config['org_dir'], 'companies', f"{code}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            
        except Exception as e:
            logger.error(f"Error deleting company file: {e}")
    
    def export_organization_data(self, format='json', file_path=None):
        """
        Export all organization and company data.
        
        Args:
            format (str): Export format (json, csv, yaml)
            file_path (str): Path to save the file, or None for default
            
        Returns:
            tuple: (success, message, export_file_path)
        """
        try:
            # Get all organizations and companies
            organizations = self.get_all_organizations(include_inactive=True)
            companies = self.get_all_companies(include_inactive=True)
            
            # Prepare export data
            export_data = {
                'organizations': organizations,
                'companies': companies,
                'exported_at': datetime.now().isoformat()
            }
            
            # Determine export file path
            if not file_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"organization_data_{timestamp}.{format}"
                file_path = os.path.join(self.config['org_dir'], 'exports', filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Export in the requested format
            if format == 'json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            elif format == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(export_data, f, default_flow_style=False, allow_unicode=True)
            
            elif format == 'csv':
                # For CSV, we need to create separate files for organizations and companies
                base_path = os.path.splitext(file_path)[0]
                
                # Export organizations
                org_file = f"{base_path}_organizations.csv"
                with open(org_file, 'w', encoding='utf-8', newline='') as f:
                    fieldnames = ['id', 'name', 'code', 'description', 'logo_path', 
                                 'parent_id', 'created_at', 'created_by', 
                                 'updated_at', 'updated_by', 'is_active']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for org in organizations:
                        writer.writerow({k: v for k, v in org.items() if k in fieldnames})
                
                # Export companies
                company_file = f"{base_path}_companies.csv"
                with open(company_file, 'w', encoding='utf-8', newline='') as f:
                    fieldnames = ['id', 'name', 'code', 'description', 'logo_path', 
                                 'organization_id', 'organization_name', 'organization_code',
                                 'created_at', 'created_by', 'updated_at', 'updated_by', 'is_active']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for company in companies:
                        writer.writerow({k: v for k, v in company.items() if k in fieldnames})
                
                # Return both files
                return True, f"Organization data exported to {org_file} and {company_file}", [org_file, company_file]
            
            else:
                return False, f"Unsupported export format: {format}", None
            
            return True, f"Organization data exported to {file_path}", file_path
            
        except Exception as e:
            logger.error(f"Error exporting organization data: {e}")
            logger.error(traceback.format_exc())
            return False, f"Error exporting organization data: {str(e)}", None
    
    def import_organization_data(self, file_path, merge_strategy='update', user_info=None):
        """
        Import organization and company data.
        
        Args:
            file_path (str): Path to the file to import
            merge_strategy (str): Strategy for handling duplicates ('update', 'skip', 'replace')
            user_info (dict): Information about the user importing the data
            
        Returns:
            tuple: (success, message, stats)
        """
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}", None
        
        try:
            # Determine file format from extension
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Load data from file
            if file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)
            
            elif file_ext == '.yaml' or file_ext == '.yml':
                with open(file_path, 'r', encoding='utf-8') as f:
                    import_data = yaml.safe_load(f)
            
            else:
                return False, f"Unsupported file format: {file_ext}", None
            
            # Validate import data structure
            if not isinstance(import_data, dict) or 'organizations' not in import_data or 'companies' not in import_data:
                return False, "Invalid import data structure", None
            
            # Import organizations
            organizations = import_data['organizations']
            org_stats = {
                'total': len(organizations),
                'created': 0,
                'updated': 0,
                'skipped': 0,
                'failed': 0
            }
            
            # Create a mapping of imported organization IDs to new IDs
            org_id_map = {}
            
            for org in organizations:
                # Skip if missing required fields
                if not org.get('name') or not org.get('code'):
                    org_stats['failed'] += 1
                    continue
                
                # Check if organization already exists
                conn = sqlite3.connect(self.config['db_path'])
                cursor = conn.cursor()
                
                cursor.execute('SELECT id FROM organizations WHERE code = ?', (org['code'],))
                existing = cursor.fetchone()
                conn.close()
                
                if existing:
                    existing_id = existing[0]
                    org_id_map[org['id']] = existing_id
                    
                    if merge_strategy == 'skip':
                        org_stats['skipped'] += 1
                        continue
                    
                    elif merge_strategy == 'update':
                        # Update existing organization
                        success, _ = self.update_organization(
                            existing_id,
                            {
                                'name': org['name'],
                                'description': org.get('description'),
                                'logo_path': org.get('logo_path'),
                                # Don't update parent_id yet, will handle after all orgs are imported
                                'is_active': org.get('is_active', True)
                            },
                            user_info
                        )
                        
                        if success:
                            org_stats['updated'] += 1
                        else:
                            org_stats['failed'] += 1
                    
                    elif merge_strategy == 'replace':
                        # Delete and re-create
                        self.delete_organization(existing_id, user_info)
                        
                        success, _, new_id = self.create_organization(
                            name=org['name'],
                            code=org['code'],
                            description=org.get('description'),
                            logo_path=org.get('logo_path'),
                            # Don't set parent_id yet, will handle after all orgs are imported
                            user_info=user_info
                        )
                        
                        if success:
                            org_id_map[org['id']] = new_id
                            org_stats['created'] += 1
                        else:
                            org_stats['failed'] += 1
                
                else:
                    # Create new organization
                    success, _, new_id = self.create_organization(
                        name=org['name'],
                        code=org['code'],
                        description=org.get('description'),
                        logo_path=org.get('logo_path'),
                        # Don't set parent_id yet, will handle after all orgs are imported
                        user_info=user_info
                    )
                    
                    if success:
                        org_id_map[org['id']] = new_id
                        org_stats['created'] += 1
                    else:
                        org_stats['failed'] += 1
            
            # Update parent relationships
            for org in organizations:
                if org.get('parent_id') and org['id'] in org_id_map:
                    new_id = org_id_map[org['id']]
                    
                    # Map the parent ID to the new ID system
                    new_parent_id = org_id_map.get(org['parent_id'])
                    
                    if new_parent_id:
                        self.update_organization(
                            new_id,
                            {'parent_id': new_parent_id},
                            user_info
                        )
            
            # Import companies
            companies = import_data['companies']
            company_stats = {
                'total': len(companies),
                'created': 0,
                'updated': 0,
                'skipped': 0,
                'failed': 0
            }
            
            for company in companies:
                # Skip if missing required fields
                if not company.get('name') or not company.get('code') or not company.get('organization_id'):
                    company_stats['failed'] += 1
                    continue
                
                # Map the organization ID to the new ID system
                new_org_id = org_id_map.get(company['organization_id'])
                if not new_org_id:
                    company_stats['failed'] += 1
                    continue
                
                # Check if company already exists
                conn = sqlite3.connect(self.config['db_path'])
                cursor = conn.cursor()
                
                cursor.execute('SELECT id FROM companies WHERE code = ?', (company['code'],))
                existing = cursor.fetchone()
                conn.close()
                
                if existing:
                    existing_id = existing[0]
                    
                    if merge_strategy == 'skip':
                        company_stats['skipped'] += 1
                        continue
                    
                    elif merge_strategy == 'update':
                        # Update existing company
                        success, _ = self.update_company(
                            existing_id,
                            {
                                'name': company['name'],
                                'description': company.get('description'),
                                'logo_path': company.get('logo_path'),
                                'organization_id': new_org_id,
                                'is_active': company.get('is_active', True)
                            },
                            user_info
                        )
                        
                        if success:
                            company_stats['updated'] += 1
                        else:
                            company_stats['failed'] += 1
                    
                    elif merge_strategy == 'replace':
                        # Delete and re-create
                        self.delete_company(existing_id, user_info)
                        
                        success, _, _ = self.create_company(
                            name=company['name'],
                            code=company['code'],
                            organization_id=new_org_id,
                            description=company.get('description'),
                            logo_path=company.get('logo_path'),
                            user_info=user_info
                        )
                        
                        if success:
                            company_stats['created'] += 1
                        else:
                            company_stats['failed'] += 1
                
                else:
                    # Create new company
                    success, _, _ = self.create_company(
                        name=company['name'],
                        code=company['code'],
                        organization_id=new_org_id,
                        description=company.get('description'),
                        logo_path=company.get('logo_path'),
                        user_info=user_info
                    )
                    
                    if success:
                        company_stats['created'] += 1
                    else:
                        company_stats['failed'] += 1
            
            stats = {
                'organizations': org_stats,
                'companies': company_stats
            }
            
            return True, "Organization data imported successfully", stats
            
        except Exception as e:
            logger.error(f"Error importing organization data: {e}")
            logger.error(traceback.format_exc())
            return False, f"Error importing organization data: {str(e)}", None


# Example usage
if __name__ == "__main__":
    # Example configuration
    config = {
        'org_dir': 'data/organizations',
        'db_path': 'data/database/organizations.db',
    }
    
    # Create organization manager
    org_manager = OrganizationManager(config)
    
    # Example: Create some organizations
    user_info = {'id': 1, 'username': 'admin'}
    
    # Create a root organization
    success, message, org_id = org_manager.create_organization(
        name="Agricultural Research Institute",
        code="agri_research",
        description="Main research institute for agricultural studies",
        user_info=user_info
    )
    
    print(f"Create organization: {message}")
    
    # Create a child organization
    success, message, child_org_id = org_manager.create_organization(
        name="Plant Science Department",
        code="plant_science",
        description="Department focused on plant research",
        parent_id=org_id,
        user_info=user_info
    )
    
    print(f"Create child organization: {message}")
    
    # Create a company
    success, message, company_id = org_manager.create_company(
        name="Crop Research Lab",
        code="crop_lab",
        organization_id=child_org_id,
        description="Laboratory for crop research and development",
        user_info=user_info
    )
    
    print(f"Create company: {message}")
    
    # Add user affiliation
    success, message, affiliation_id = org_manager.add_user_affiliation(
        user_id=1,
        username="admin",
        organization_id=org_id,
        is_primary=True,
        user_info=user_info
    )
    
    print(f"Add user affiliation: {message}")
    
    # Get organization hierarchy
    hierarchy = org_manager.get_organization_hierarchy()
    print("Organization hierarchy:")
    print(json.dumps(hierarchy, indent=2))
    
    # Validate user access
    has_access = org_manager.validate_user_access(user_id=1, organization_id=child_org_id)
    print(f"User has access to child organization: {has_access}")
