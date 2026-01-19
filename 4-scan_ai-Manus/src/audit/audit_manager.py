#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Audit and version control system for the Agricultural AI System.

This module provides functionality for tracking all changes to the system,
maintaining version history, and generating audit logs.
"""

import os
import json
import logging
import sqlite3
import hashlib
from datetime import datetime
import traceback
import shutil
import yaml
import csv
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('audit_manager')

class AuditManager:
    """
    Manages audit logging and version control for the Agricultural AI System.
    
    This class provides methods to:
    1. Log all system actions with user information
    2. Track changes to data, models, and configurations
    3. Maintain version history for all system components
    4. Generate audit reports
    5. Support rollback to previous versions
    """
    
    # Action types for audit logging
    ACTION_TYPES = {
        'USER': ['login', 'logout', 'password_change', 'role_change', 'permission_change'],
        'DATA': ['create', 'read', 'update', 'delete', 'import', 'export'],
        'MODEL': ['train', 'evaluate', 'deploy', 'rollback'],
        'SYSTEM': ['start', 'stop', 'restart', 'config_change', 'backup', 'restore'],
        'LEARNING': ['start', 'pause', 'resume', 'stop', 'distortion_detected']
    }
    
    def __init__(self, config=None):
        """
        Initialize the audit manager.
        
        Args:
            config (dict): Configuration dictionary with audit management settings
        """
        self.config = config or {}
        
        # Default configuration
        self.default_config = {
            'audit_dir': 'data/audit',
            'versions_dir': 'data/versions',
            'db_path': 'data/database/audit.db',
            'log_retention_days': 365,  # 1 year
            'max_versions_per_component': 10,
            'backup_dir': 'data/backups/audit',
        }
        
        # Merge with provided config
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
        
        # Create necessary directories
        for dir_key in ['audit_dir', 'versions_dir', 'backup_dir']:
            os.makedirs(self.config[dir_key], exist_ok=True)
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.config['db_path']), exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        logger.info("Audit manager initialized")
    
    def _init_database(self):
        """Initialize the SQLite database for audit management."""
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Create audit_log table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action_type TEXT NOT NULL,
                action TEXT NOT NULL,
                component TEXT NOT NULL,
                user_id INTEGER,
                username TEXT,
                organization TEXT,
                company TEXT,
                ip_address TEXT,
                details TEXT,
                status TEXT NOT NULL,
                affected_ids TEXT
            )
            ''')
            
            # Create versions table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                component TEXT NOT NULL,
                version TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                user_id INTEGER,
                username TEXT,
                file_path TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                description TEXT,
                parent_version TEXT,
                is_current BOOLEAN NOT NULL,
                UNIQUE(component, version)
            )
            ''')
            
            # Create daily_stats table for summary reporting
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                action_type TEXT NOT NULL,
                action TEXT NOT NULL,
                count INTEGER NOT NULL,
                UNIQUE(date, action_type, action)
            )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Audit database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def log_action(self, action_type, action, component, user_info=None, 
                  details=None, status='success', affected_ids=None):
        """
        Log a system action.
        
        Args:
            action_type (str): Type of action (USER, DATA, MODEL, SYSTEM, LEARNING)
            action (str): Specific action performed
            component (str): System component affected
            user_info (dict): Information about the user performing the action
            details (dict): Additional details about the action
            status (str): Status of the action (success, failed, warning)
            affected_ids (list): IDs of affected records
            
        Returns:
            int: ID of the created audit log entry
        """
        try:
            # Validate action type and action
            action_type = action_type.upper()
            if action_type not in self.ACTION_TYPES:
                logger.warning(f"Unknown action type: {action_type}")
            elif action not in self.ACTION_TYPES[action_type]:
                logger.warning(f"Unknown action '{action}' for type '{action_type}'")
            
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Extract user information
            user_id = user_info.get('id') if user_info else None
            username = user_info.get('username') if user_info else None
            organization = user_info.get('organization') if user_info else None
            company = user_info.get('company') if user_info else None
            ip_address = user_info.get('ip_address') if user_info else None
            
            # Convert details to JSON if provided
            details_json = json.dumps(details) if details else None
            
            # Convert affected_ids to JSON if provided
            affected_ids_json = json.dumps(affected_ids) if affected_ids else None
            
            # Insert the audit log entry
            cursor.execute('''
            INSERT INTO audit_log (
                timestamp, action_type, action, component, user_id, username,
                organization, company, ip_address, details, status, affected_ids
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                action_type,
                action,
                component,
                user_id,
                username,
                organization,
                company,
                ip_address,
                details_json,
                status,
                affected_ids_json
            ))
            
            log_id = cursor.lastrowid
            
            # Update daily stats
            today = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('''
            INSERT INTO daily_stats (date, action_type, action, count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(date, action_type, action)
            DO UPDATE SET count = count + 1
            ''', (today, action_type, action))
            
            conn.commit()
            conn.close()
            
            # Also save to file for backup
            self._save_audit_log_to_file(
                log_id, action_type, action, component, user_info,
                details, status, affected_ids
            )
            
            return log_id
            
        except Exception as e:
            logger.error(f"Error logging action: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return None
    
    def _save_audit_log_to_file(self, log_id, action_type, action, component, 
                               user_info, details, status, affected_ids):
        """
        Save an audit log entry to a file for backup.
        
        Args:
            log_id (int): ID of the audit log entry
            action_type (str): Type of action
            action (str): Specific action performed
            component (str): System component affected
            user_info (dict): Information about the user
            details (dict): Additional details
            status (str): Status of the action
            affected_ids (list): IDs of affected records
        """
        try:
            # Create directory structure
            today = datetime.now().strftime('%Y-%m-%d')
            log_dir = os.path.join(self.config['audit_dir'], today)
            os.makedirs(log_dir, exist_ok=True)
            
            # Prepare log data
            log_data = {
                'id': log_id,
                'timestamp': datetime.now().isoformat(),
                'action_type': action_type,
                'action': action,
                'component': component,
                'user': {
                    'id': user_info.get('id') if user_info else None,
                    'username': user_info.get('username') if user_info else None,
                    'organization': user_info.get('organization') if user_info else None,
                    'company': user_info.get('company') if user_info else None,
                    'ip_address': user_info.get('ip_address') if user_info else None
                },
                'details': details,
                'status': status,
                'affected_ids': affected_ids
            }
            
            # Save to JSON file
            log_file = os.path.join(log_dir, f"{log_id}.json")
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error saving audit log to file: {e}")
    
    def create_version(self, component, file_path, description=None, user_info=None):
        """
        Create a new version of a system component.
        
        Args:
            component (str): Name of the component
            file_path (str): Path to the component file
            description (str): Description of the version
            user_info (dict): Information about the user creating the version
            
        Returns:
            tuple: (success, message, version)
        """
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}", None
        
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Get the latest version for this component
            cursor.execute('''
            SELECT version FROM versions
            WHERE component = ?
            ORDER BY id DESC LIMIT 1
            ''', (component,))
            
            result = cursor.fetchone()
            
            if result:
                # Increment version
                latest_version = result[0]
                try:
                    version_parts = latest_version.split('.')
                    version_parts[-1] = str(int(version_parts[-1]) + 1)
                    new_version = '.'.join(version_parts)
                except:
                    # If version parsing fails, use timestamp
                    new_version = datetime.now().strftime("v%Y%m%d.%H%M%S")
            else:
                # First version
                new_version = "1.0.0"
            
            # Compute file hash
            file_hash = self._compute_file_hash(file_path)
            
            # Create versions directory for this component
            component_dir = os.path.join(self.config['versions_dir'], component)
            os.makedirs(component_dir, exist_ok=True)
            
            # Copy the file to versions directory
            version_file_name = f"{component}_{new_version}{os.path.splitext(file_path)[1]}"
            version_file_path = os.path.join(component_dir, version_file_name)
            shutil.copy2(file_path, version_file_path)
            
            # Extract user information
            user_id = user_info.get('id') if user_info else None
            username = user_info.get('username') if user_info else None
            
            # Mark all existing versions as not current
            cursor.execute('''
            UPDATE versions SET is_current = 0
            WHERE component = ?
            ''', (component,))
            
            # Insert the new version
            cursor.execute('''
            INSERT INTO versions (
                component, version, timestamp, user_id, username,
                file_path, file_hash, description, parent_version, is_current
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''', (
                component,
                new_version,
                datetime.now().isoformat(),
                user_id,
                username,
                version_file_path,
                file_hash,
                description,
                latest_version if result else None
            ))
            
            # Log the action
            self.log_action(
                action_type='SYSTEM',
                action='config_change',
                component=component,
                user_info=user_info,
                details={
                    'action': 'create_version',
                    'version': new_version,
                    'description': description
                }
            )
            
            # Prune old versions if needed
            self._prune_old_versions(component)
            
            conn.commit()
            conn.close()
            
            return True, f"Created version {new_version} for component {component}", new_version
            
        except Exception as e:
            logger.error(f"Error creating version: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error creating version: {str(e)}", None
    
    def _compute_file_hash(self, file_path):
        """
        Compute SHA-256 hash of a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: Hex digest of the hash
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def _prune_old_versions(self, component):
        """
        Prune old versions of a component to save space.
        
        Args:
            component (str): Name of the component
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Get all versions for this component, ordered by timestamp
            cursor.execute('''
            SELECT id, version, file_path FROM versions
            WHERE component = ? AND is_current = 0
            ORDER BY timestamp DESC
            ''', (component,))
            
            versions = cursor.fetchall()
            
            # Keep only the specified number of versions
            max_versions = self.config['max_versions_per_component']
            
            if len(versions) > max_versions:
                versions_to_delete = versions[max_versions:]
                
                for version_id, version, file_path in versions_to_delete:
                    # Delete the version file
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    
                    # Delete the version record
                    cursor.execute('DELETE FROM versions WHERE id = ?', (version_id,))
                    
                    logger.info(f"Pruned old version {version} of component {component}")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error pruning old versions: {e}")
            if conn:
                conn.close()
    
    def get_version_history(self, component):
        """
        Get version history for a component.
        
        Args:
            component (str): Name of the component
            
        Returns:
            list: List of version records
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, version, timestamp, username, file_path, 
                   file_hash, description, parent_version, is_current
            FROM versions
            WHERE component = ?
            ORDER BY timestamp DESC
            ''', (component,))
            
            versions = []
            for row in cursor.fetchall():
                id, version, timestamp, username, file_path, \
                file_hash, description, parent_version, is_current = row
                
                versions.append({
                    'id': id,
                    'version': version,
                    'timestamp': timestamp,
                    'username': username,
                    'file_path': file_path,
                    'file_hash': file_hash,
                    'description': description,
                    'parent_version': parent_version,
                    'is_current': bool(is_current)
                })
            
            conn.close()
            
            return versions
            
        except Exception as e:
            logger.error(f"Error getting version history: {e}")
            if conn:
                conn.close()
            return []
    
    def restore_version(self, component, version, target_path=None, user_info=None):
        """
        Restore a component to a previous version.
        
        Args:
            component (str): Name of the component
            version (str): Version to restore
            target_path (str): Path to restore to, or None to use original path
            user_info (dict): Information about the user performing the restoration
            
        Returns:
            tuple: (success, message)
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Find the version record
            cursor.execute('''
            SELECT file_path, file_hash
            FROM versions
            WHERE component = ? AND version = ?
            ''', (component, version))
            
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, f"Version {version} not found for component {component}"
            
            source_file_path, source_file_hash = result
            
            # Check if source file exists
            if not os.path.exists(source_file_path):
                conn.close()
                return False, f"Source file not found: {source_file_path}"
            
            # Verify file hash
            current_hash = self._compute_file_hash(source_file_path)
            if current_hash != source_file_hash:
                conn.close()
                return False, f"Source file has been modified: {source_file_path}"
            
            # Determine target path
            if not target_path:
                # Get the current version
                cursor.execute('''
                SELECT file_path
                FROM versions
                WHERE component = ? AND is_current = 1
                ''', (component,))
                
                current_result = cursor.fetchone()
                
                if not current_result:
                    conn.close()
                    return False, f"No current version found for component {component}"
                
                # Use the same path as the current version
                target_path = current_result[0]
            
            # Create backup of current file if it exists
            if os.path.exists(target_path):
                backup_dir = os.path.join(self.config['backup_dir'], component)
                os.makedirs(backup_dir, exist_ok=True)
                
                backup_file = os.path.join(
                    backup_dir, 
                    f"{os.path.basename(target_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                
                shutil.copy2(target_path, backup_file)
            
            # Copy version file to target
            shutil.copy2(source_file_path, target_path)
            
            # Update version records
            cursor.execute('''
            UPDATE versions SET is_current = 0
            WHERE component = ?
            ''', (component,))
            
            cursor.execute('''
            UPDATE versions SET is_current = 1
            WHERE component = ? AND version = ?
            ''', (component, version))
            
            # Log the action
            self.log_action(
                action_type='SYSTEM',
                action='config_change',
                component=component,
                user_info=user_info,
                details={
                    'action': 'restore_version',
                    'version': version,
                    'target_path': target_path
                }
            )
            
            conn.commit()
            conn.close()
            
            return True, f"Component {component} restored to version {version}"
            
        except Exception as e:
            logger.error(f"Error restoring version: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.close()
            return False, f"Error restoring version: {str(e)}"
    
    def get_audit_logs(self, filters=None, limit=100, offset=0):
        """
        Get audit logs with optional filtering.
        
        Args:
            filters (dict): Filters to apply
            limit (int): Maximum number of logs to return
            offset (int): Offset for pagination
            
        Returns:
            list: List of audit log entries
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Prepare query conditions
            conditions = []
            params = []
            
            if filters:
                for key, value in filters.items():
                    if key in ['action_type', 'action', 'component', 'username', 'status', 'organization', 'company']:
                        conditions.append(f"{key} = ?")
                        params.append(value)
                    elif key == 'user_id':
                        conditions.append("user_id = ?")
                        params.append(value)
                    elif key == 'start_date':
                        conditions.append("timestamp >= ?")
                        params.append(value)
                    elif key == 'end_date':
                        conditions.append("timestamp <= ?")
                        params.append(value)
            
            # Build the query
            query = '''
            SELECT id, timestamp, action_type, action, component, user_id, username,
                   organization, company, ip_address, details, status, affected_ids
            FROM audit_log
            '''
            
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
            
            query += ' ORDER BY timestamp DESC LIMIT ? OFFSET ?'
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            logs = []
            for row in cursor.fetchall():
                id, timestamp, action_type, action, component, user_id, username, \
                organization, company, ip_address, details_json, status, affected_ids_json = row
                
                # Parse JSON fields
                details = json.loads(details_json) if details_json else None
                affected_ids = json.loads(affected_ids_json) if affected_ids_json else None
                
                logs.append({
                    'id': id,
                    'timestamp': timestamp,
                    'action_type': action_type,
                    'action': action,
                    'component': component,
                    'user_id': user_id,
                    'username': username,
                    'organization': organization,
                    'company': company,
                    'ip_address': ip_address,
                    'details': details,
                    'status': status,
                    'affected_ids': affected_ids
                })
            
            conn.close()
            
            return logs
            
        except Exception as e:
            logger.error(f"Error getting audit logs: {e}")
            if conn:
                conn.close()
            return []
    
    def get_audit_stats(self, start_date=None, end_date=None, group_by='action_type'):
        """
        Get statistics from audit logs.
        
        Args:
            start_date (str): Start date for filtering (ISO format)
            end_date (str): End date for filtering (ISO format)
            group_by (str): Field to group by (action_type, action, component, username)
            
        Returns:
            dict: Statistics grouped by the specified field
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Prepare query conditions
            conditions = []
            params = []
            
            if start_date:
                conditions.append("timestamp >= ?")
                params.append(start_date)
            
            if end_date:
                conditions.append("timestamp <= ?")
                params.append(end_date)
            
            # Validate group_by field
            valid_group_fields = ['action_type', 'action', 'component', 'username', 'status', 'organization', 'company']
            if group_by not in valid_group_fields:
                group_by = 'action_type'
            
            # Build the query
            query = f'''
            SELECT {group_by}, COUNT(*) as count
            FROM audit_log
            '''
            
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
            
            query += f' GROUP BY {group_by}'
            
            cursor.execute(query, params)
            
            stats = {}
            for row in cursor.fetchall():
                key, count = row
                stats[key] = count
            
            conn.close()
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting audit stats: {e}")
            if conn:
                conn.close()
            return {}
    
    def generate_audit_report(self, start_date=None, end_date=None, format='json', file_path=None):
        """
        Generate a comprehensive audit report.
        
        Args:
            start_date (str): Start date for the report (ISO format)
            end_date (str): End date for the report (ISO format)
            format (str): Report format (json, csv, html)
            file_path (str): Path to save the report, or None for default
            
        Returns:
            tuple: (success, message, report_file_path)
        """
        try:
            # Get audit logs for the specified period
            filters = {}
            if start_date:
                filters['start_date'] = start_date
            if end_date:
                filters['end_date'] = end_date
            
            logs = self.get_audit_logs(filters=filters, limit=10000)
            
            if not logs:
                return False, "No audit logs found for the specified period", None
            
            # Prepare report data
            report_data = {
                'generated_at': datetime.now().isoformat(),
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'summary': {
                    'total_logs': len(logs),
                    'by_action_type': self.get_audit_stats(start_date, end_date, 'action_type'),
                    'by_action': self.get_audit_stats(start_date, end_date, 'action'),
                    'by_component': self.get_audit_stats(start_date, end_date, 'component'),
                    'by_status': self.get_audit_stats(start_date, end_date, 'status')
                },
                'logs': logs
            }
            
            # Determine report file path
            if not file_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"audit_report_{timestamp}.{format}"
                file_path = os.path.join(self.config['audit_dir'], 'reports', filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Generate report in the requested format
            if format == 'json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            elif format == 'csv':
                # Flatten the logs for CSV export
                flattened_logs = []
                for log in logs:
                    flat_log = {
                        'id': log['id'],
                        'timestamp': log['timestamp'],
                        'action_type': log['action_type'],
                        'action': log['action'],
                        'component': log['component'],
                        'user_id': log['user_id'],
                        'username': log['username'],
                        'organization': log['organization'],
                        'company': log['company'],
                        'ip_address': log['ip_address'],
                        'status': log['status'],
                        'details': json.dumps(log['details']) if log['details'] else '',
                        'affected_ids': json.dumps(log['affected_ids']) if log['affected_ids'] else ''
                    }
                    flattened_logs.append(flat_log)
                
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=flattened_logs[0].keys())
                    writer.writeheader()
                    writer.writerows(flattened_logs)
            
            elif format == 'html':
                # Generate a simple HTML report
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Audit Report</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        h1, h2 {{ color: #333; }}
                        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f2f2f2; }}
                        tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    </style>
                </head>
                <body>
                    <h1>Audit Report</h1>
                    <p>Generated at: {report_data['generated_at']}</p>
                    <p>Period: {report_data['period']['start_date'] or 'All time'} to {report_data['period']['end_date'] or 'Present'}</p>
                    
                    <h2>Summary</h2>
                    <p>Total logs: {report_data['summary']['total_logs']}</p>
                    
                    <h3>By Action Type</h3>
                    <table>
                        <tr><th>Action Type</th><th>Count</th></tr>
                """
                
                for action_type, count in report_data['summary']['by_action_type'].items():
                    html_content += f"<tr><td>{action_type}</td><td>{count}</td></tr>"
                
                html_content += """
                    </table>
                    
                    <h3>By Action</h3>
                    <table>
                        <tr><th>Action</th><th>Count</th></tr>
                """
                
                for action, count in report_data['summary']['by_action'].items():
                    html_content += f"<tr><td>{action}</td><td>{count}</td></tr>"
                
                html_content += """
                    </table>
                    
                    <h3>By Component</h3>
                    <table>
                        <tr><th>Component</th><th>Count</th></tr>
                """
                
                for component, count in report_data['summary']['by_component'].items():
                    html_content += f"<tr><td>{component}</td><td>{count}</td></tr>"
                
                html_content += """
                    </table>
                    
                    <h3>By Status</h3>
                    <table>
                        <tr><th>Status</th><th>Count</th></tr>
                """
                
                for status, count in report_data['summary']['by_status'].items():
                    html_content += f"<tr><td>{status}</td><td>{count}</td></tr>"
                
                html_content += """
                    </table>
                    
                    <h2>Logs</h2>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Timestamp</th>
                            <th>Action Type</th>
                            <th>Action</th>
                            <th>Component</th>
                            <th>Username</th>
                            <th>Organization</th>
                            <th>Company</th>
                            <th>Status</th>
                        </tr>
                """
                
                for log in logs:
                    html_content += f"""
                        <tr>
                            <td>{log['id']}</td>
                            <td>{log['timestamp']}</td>
                            <td>{log['action_type']}</td>
                            <td>{log['action']}</td>
                            <td>{log['component']}</td>
                            <td>{log['username'] or ''}</td>
                            <td>{log['organization'] or ''}</td>
                            <td>{log['company'] or ''}</td>
                            <td>{log['status']}</td>
                        </tr>
                    """
                
                html_content += """
                    </table>
                </body>
                </html>
                """
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            else:
                return False, f"Unsupported report format: {format}", None
            
            return True, f"Audit report generated successfully: {file_path}", file_path
            
        except Exception as e:
            logger.error(f"Error generating audit report: {e}")
            logger.error(traceback.format_exc())
            return False, f"Error generating audit report: {str(e)}", None
    
    def get_user_activity(self, user_id=None, username=None, limit=100):
        """
        Get activity history for a specific user.
        
        Args:
            user_id (int): ID of the user
            username (str): Username of the user
            limit (int): Maximum number of activities to return
            
        Returns:
            list: List of user activities
        """
        if not user_id and not username:
            return []
        
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Prepare query conditions
            conditions = []
            params = []
            
            if user_id:
                conditions.append("user_id = ?")
                params.append(user_id)
            elif username:
                conditions.append("username = ?")
                params.append(username)
            
            # Build the query
            query = '''
            SELECT id, timestamp, action_type, action, component, details, status
            FROM audit_log
            WHERE ''' + ' AND '.join(conditions) + '''
            ORDER BY timestamp DESC
            LIMIT ?
            '''
            
            params.append(limit)
            
            cursor.execute(query, params)
            
            activities = []
            for row in cursor.fetchall():
                id, timestamp, action_type, action, component, details_json, status = row
                
                # Parse JSON fields
                details = json.loads(details_json) if details_json else None
                
                activities.append({
                    'id': id,
                    'timestamp': timestamp,
                    'action_type': action_type,
                    'action': action,
                    'component': component,
                    'details': details,
                    'status': status
                })
            
            conn.close()
            
            return activities
            
        except Exception as e:
            logger.error(f"Error getting user activity: {e}")
            if conn:
                conn.close()
            return []
    
    def get_component_activity(self, component, limit=100):
        """
        Get activity history for a specific component.
        
        Args:
            component (str): Name of the component
            limit (int): Maximum number of activities to return
            
        Returns:
            list: List of component activities
        """
        try:
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, timestamp, action_type, action, username, details, status
            FROM audit_log
            WHERE component = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''', (component, limit))
            
            activities = []
            for row in cursor.fetchall():
                id, timestamp, action_type, action, username, details_json, status = row
                
                # Parse JSON fields
                details = json.loads(details_json) if details_json else None
                
                activities.append({
                    'id': id,
                    'timestamp': timestamp,
                    'action_type': action_type,
                    'action': action,
                    'username': username,
                    'details': details,
                    'status': status
                })
            
            conn.close()
            
            return activities
            
        except Exception as e:
            logger.error(f"Error getting component activity: {e}")
            if conn:
                conn.close()
            return []
    
    def cleanup_old_logs(self, days=None):
        """
        Clean up old audit logs to save space.
        
        Args:
            days (int): Number of days to keep logs for, or None to use default
            
        Returns:
            tuple: (success, message, count)
        """
        if days is None:
            days = self.config['log_retention_days']
        
        try:
            # Calculate cutoff date
            cutoff_date = (datetime.now() - datetime.timedelta(days=days)).isoformat()
            
            conn = sqlite3.connect(self.config['db_path'])
            cursor = conn.cursor()
            
            # Count logs to be deleted
            cursor.execute('''
            SELECT COUNT(*) FROM audit_log
            WHERE timestamp < ?
            ''', (cutoff_date,))
            
            count = cursor.fetchone()[0]
            
            if count == 0:
                conn.close()
                return True, "No old logs to clean up", 0
            
            # Delete old logs
            cursor.execute('''
            DELETE FROM audit_log
            WHERE timestamp < ?
            ''', (cutoff_date,))
            
            conn.commit()
            
            # Also clean up file system logs
            for root, dirs, files in os.walk(self.config['audit_dir']):
                for dir_name in dirs:
                    try:
                        # Check if directory name is a date
                        dir_date = datetime.strptime(dir_name, '%Y-%m-%d')
                        if dir_date < datetime.now() - datetime.timedelta(days=days):
                            dir_path = os.path.join(root, dir_name)
                            shutil.rmtree(dir_path)
                            logger.info(f"Removed old audit log directory: {dir_path}")
                    except ValueError:
                        # Not a date directory, skip
                        pass
            
            conn.close()
            
            return True, f"Cleaned up {count} old audit logs", count
            
        except Exception as e:
            logger.error(f"Error cleaning up old logs: {e}")
            if conn:
                conn.close()
            return False, f"Error cleaning up old logs: {str(e)}", 0


# Example usage
if __name__ == "__main__":
    # Example configuration
    config = {
        'audit_dir': 'data/audit',
        'versions_dir': 'data/versions',
        'db_path': 'data/database/audit.db',
    }
    
    # Create audit manager
    audit_manager = AuditManager(config)
    
    # Example: Log some actions
    user_info = {'id': 1, 'username': 'admin', 'organization': 'IT', 'company': 'AgriTech'}
    
    # Log a user login
    audit_manager.log_action(
        action_type='USER',
        action='login',
        component='auth_system',
        user_info=user_info,
        details={'ip_address': '192.168.1.100', 'device': 'desktop'},
        status='success'
    )
    
    # Log a data update
    audit_manager.log_action(
        action_type='DATA',
        action='update',
        component='disease_database',
        user_info=user_info,
        details={'records_updated': 5, 'disease_type': 'fungal'},
        status='success',
        affected_ids=[101, 102, 103, 104, 105]
    )
    
    # Example: Create a version of a component
    # First, create a sample file
    sample_file = os.path.join(config['audit_dir'], 'sample_config.json')
    os.makedirs(os.path.dirname(sample_file), exist_ok=True)
    
    with open(sample_file, 'w') as f:
        json.dump({'name': 'Sample Config', 'version': '1.0.0'}, f)
    
    # Create a version
    success, message, version = audit_manager.create_version(
        component='config',
        file_path=sample_file,
        description='Initial version',
        user_info=user_info
    )
    
    print(f"Version creation: {message}")
    
    # Example: Generate an audit report
    success, message, report_path = audit_manager.generate_audit_report(format='html')
    print(f"Audit report: {message}")
